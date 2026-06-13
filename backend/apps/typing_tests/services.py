"""
Typing Tests — Services
========================
Business logic for test generation and submission processing.
"""

import random

from django.db.models import F

from apps.wordlists.models import Quote, WordList


class TestGenerationService:
    """Generates typing test content based on mode and configuration."""

    VALID_MODES = ["time", "words", "quote", "custom", "code"]
    VALID_DURATIONS = [15, 30, 60, 120]
    VALID_WORD_COUNTS = [10, 25, 50, 100]

    @classmethod
    def generate(cls, mode, language="en", duration=30, word_count=50,
                 wordlist_id=None, difficulty=None, punctuation=False, numbers=False):
        """
        Generate typing test content.

        Args:
            mode: Test mode (time, words, quote, custom, code)
            language: Language code
            duration: Duration in seconds (for time mode)
            word_count: Number of words (for words mode)
            wordlist_id: Specific word list ID
            difficulty: Word list difficulty filter
            punctuation: Include punctuation
            numbers: Include numbers

        Returns:
            dict with test configuration and words
        """
        if mode == "quote":
            return cls._generate_quote(language, difficulty)
        elif mode == "custom" and wordlist_id:
            return cls._generate_from_wordlist(wordlist_id, word_count)
        else:
            return cls._generate_words(
                language=language,
                count=cls._get_word_count(mode, duration, word_count),
                difficulty=difficulty,
                punctuation=punctuation,
                numbers=numbers,
            )

    @classmethod
    def _get_word_count(cls, mode, duration, word_count):
        """Determine how many words to generate based on mode."""
        if mode == "time":
            # Generate enough words for the duration (assume ~100 WPM max)
            return max(50, int(duration / 60 * 150))
        elif mode == "words":
            return word_count
        return 50  # Default

    @classmethod
    def _generate_words(cls, language="en", count=50, difficulty=None,
                        punctuation=False, numbers=False):
        """Generate a random word sequence from available word lists."""
        filters = {"language__code": language, "is_public": True}
        if difficulty:
            filters["difficulty"] = difficulty

        word_lists = WordList.objects.filter(**filters)

        # Prefer default word lists
        default_lists = word_lists.filter(is_default=True)
        if default_lists.exists():
            word_list = default_lists.first()
        elif word_lists.exists():
            word_list = word_lists.first()
        else:
            # Fallback: return basic English words
            return cls._fallback_words(count)

        # Increment usage counter
        WordList.objects.filter(pk=word_list.pk).update(times_used=F("times_used") + 1)

        # Select random words
        words = word_list.words
        if not words:
            return cls._fallback_words(count)

        selected = [random.choice(words) for _ in range(count)]

        # Apply punctuation
        if punctuation:
            selected = cls._apply_punctuation(selected)

        # Apply numbers
        if numbers:
            selected = cls._apply_numbers(selected)

        return {
            "words": selected,
            "word_count": len(selected),
            "language": language,
            "wordlist_id": word_list.id,
            "wordlist_name": word_list.name,
        }

    @classmethod
    def _generate_quote(cls, language="en", difficulty=None):
        """Generate a random quote for quote mode."""
        filters = {"language__code": language, "is_active": True}
        if difficulty:
            filters["difficulty"] = difficulty

        quotes = Quote.objects.filter(**filters)
        if not quotes.exists():
            return cls._fallback_words(50)

        quote = random.choice(list(quotes[:100]))  # Pick from top 100
        words = quote.text.split()

        return {
            "words": words,
            "word_count": len(words),
            "language": language,
            "quote_id": quote.id,
            "quote_source": quote.source,
            "quote_author": quote.author,
        }

    @classmethod
    def _generate_from_wordlist(cls, wordlist_id, word_count):
        """Generate from a specific word list."""
        try:
            word_list = WordList.objects.get(pk=wordlist_id)
        except WordList.DoesNotExist:
            return cls._fallback_words(word_count)

        WordList.objects.filter(pk=word_list.pk).update(times_used=F("times_used") + 1)

        words = word_list.words
        selected = [random.choice(words) for _ in range(word_count)]

        return {
            "words": selected,
            "word_count": len(selected),
            "language": word_list.language.code,
            "wordlist_id": word_list.id,
            "wordlist_name": word_list.name,
        }

    @classmethod
    def _apply_punctuation(cls, words):
        """Randomly apply punctuation to some words."""
        punctuation_marks = [".", ",", ";", ":", "!", "?"]
        result = []
        for i, word in enumerate(words):
            result.append(word)
            # ~15% chance of punctuation after a word
            if random.random() < 0.15 and i < len(words) - 1:
                result[-1] = word + random.choice(punctuation_marks)
        # Capitalize first word and words after sentence-ending punctuation
        for i in range(len(result)):
            if i == 0 or (i > 0 and result[i - 1][-1] in ".!?"):
                result[i] = result[i][0].upper() + result[i][1:] if result[i] else result[i]
        return result

    @classmethod
    def _apply_numbers(cls, words):
        """Randomly insert numbers into the word sequence."""
        result = list(words)
        num_insertions = max(1, len(words) // 10)
        for _ in range(num_insertions):
            pos = random.randint(0, len(result) - 1)
            result[pos] = str(random.randint(1, 9999))
        return result

    @classmethod
    def _fallback_words(cls, count):
        """Fallback word list when no database words are available."""
        fallback = [
            "the", "be", "to", "of", "and", "a", "in", "that", "have", "I",
            "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
            "this", "but", "his", "by", "from", "they", "we", "say", "her",
            "she", "or", "an", "will", "my", "one", "all", "would", "there",
            "their", "what", "so", "up", "out", "if", "about", "who", "get",
            "which", "go", "me", "when", "make", "can", "like", "time", "no",
            "just", "him", "know", "take", "people", "into", "year", "your",
            "good", "some", "could", "them", "see", "other", "than", "then",
            "now", "look", "only", "come", "its", "over", "think", "also",
            "back", "after", "use", "two", "how", "our", "work", "first",
            "well", "way", "even", "new", "want", "because", "any", "these",
            "give", "day", "most", "us", "great", "between", "need", "large",
        ]
        return {
            "words": [random.choice(fallback) for _ in range(count)],
            "word_count": count,
            "language": "en",
            "wordlist_id": None,
            "wordlist_name": "fallback",
        }
