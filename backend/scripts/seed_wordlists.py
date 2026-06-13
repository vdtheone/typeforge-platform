"""
Seed Script — Word Lists & Languages
======================================
Run: python manage.py shell < scripts/seed_wordlists.py
"""

import os
import sys

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from apps.wordlists.models import Language, Quote, WordList

# =============================================================================
# Languages
# =============================================================================
LANGUAGES = [
    {"name": "English", "code": "en", "flag_emoji": "🇺🇸"},
    {"name": "Spanish", "code": "es", "flag_emoji": "🇪🇸"},
    {"name": "French", "code": "fr", "flag_emoji": "🇫🇷"},
    {"name": "German", "code": "de", "flag_emoji": "🇩🇪"},
    {"name": "Portuguese", "code": "pt", "flag_emoji": "🇧🇷"},
    {"name": "Italian", "code": "it", "flag_emoji": "🇮🇹"},
    {"name": "Hindi", "code": "hi", "flag_emoji": "🇮🇳"},
    {"name": "Japanese", "code": "ja", "flag_emoji": "🇯🇵"},
]

# =============================================================================
# English Word Lists (Top 200 most common words)
# =============================================================================
ENGLISH_1K = [
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "I",
    "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
    "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
    "or", "an", "will", "my", "one", "all", "would", "there", "their", "what",
    "so", "up", "out", "if", "about", "who", "get", "which", "go", "me",
    "when", "make", "can", "like", "time", "no", "just", "him", "know", "take",
    "people", "into", "year", "your", "good", "some", "could", "them", "see",
    "other", "than", "then", "now", "look", "only", "come", "its", "over",
    "think", "also", "back", "after", "use", "two", "how", "our", "work",
    "first", "well", "way", "even", "new", "want", "because", "any", "these",
    "give", "day", "most", "us", "great", "between", "need", "large", "often",
    "ask", "where", "small", "must", "home", "big", "long", "own", "still",
    "each", "tell", "should", "around", "move", "live", "found", "every",
    "name", "under", "read", "old", "never", "place", "same", "keep", "help",
    "start", "show", "city", "country", "point", "head", "might", "world",
    "went", "right", "hand", "part", "high", "while", "last", "number",
    "water", "life", "very", "let", "change", "much", "off", "house",
    "play", "turn", "put", "thought", "hard", "close", "open", "seem",
    "together", "next", "both", "few", "got", "group", "begin", "always",
    "those", "run", "left", "along", "until", "children", "something", "may",
    "late", "kind", "mean", "end", "near", "important", "family", "young",
    "girl", "side", "early", "car", "call", "white", "school", "state",
    "learn", "father", "second", "enough", "across", "food", "mother",
    "night", "talk", "boy", "door", "room", "book", "eye", "face", "try",
    "set", "stop", "real", "better", "line", "idea", "body", "cut",
    "sure", "stand", "care", "story", "watch", "short", "problem", "love",
    "nothing", "full", "pick", "leave", "clear", "fact", "word", "feel",
    "power", "remember", "possible", "light", "system", "today", "since",
    "hear", "develop", "already", "reach", "late", "best", "morning",
    "become", "add", "money", "bring", "hour", "happen", "among", "quite",
    "letter", "rest", "case", "job", "area", "person", "hold", "free",
    "question", "class", "during", "black", "grow", "ground", "music",
    "table", "though", "example", "able", "special", "paper", "result",
    "appear", "believe", "include", "grow", "market", "program", "common",
    "least", "level", "local", "game", "team", "create", "produce",
    "study", "report", "inside", "present", "center", "moment", "form",
    "offer", "follow", "road", "lead", "least", "cost", "voice", "maybe",
    "record", "strong", "half", "value", "reason", "south", "north",
    "friend", "building", "land", "step", "bring", "age", "mind",
    "matter", "window", "answer", "color", "walk", "plan", "wait",
    "drive", "true", "air", "stage", "fire", "field", "type", "front",
    "subject", "almost", "human", "position", "action", "language",
    "education", "information", "political", "service", "company",
    "continue", "process", "public", "thousand", "provide", "social",
    "against", "interest", "develop", "member", "business", "community",
]

# =============================================================================
# Quotes
# =============================================================================
QUOTES = [
    {
        "text": "The only way to do great work is to love what you do.",
        "author": "Steve Jobs",
        "source": "Stanford Commencement Address",
    },
    {
        "text": "In the middle of difficulty lies opportunity.",
        "author": "Albert Einstein",
        "source": "",
    },
    {
        "text": "The best time to plant a tree was 20 years ago. The second best time is now.",
        "author": "Chinese Proverb",
        "source": "",
    },
    {
        "text": "It does not matter how slowly you go as long as you do not stop.",
        "author": "Confucius",
        "source": "",
    },
    {
        "text": "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "author": "Winston Churchill",
        "source": "",
    },
    {
        "text": "The future belongs to those who believe in the beauty of their dreams.",
        "author": "Eleanor Roosevelt",
        "source": "",
    },
    {
        "text": "Talk is cheap. Show me the code.",
        "author": "Linus Torvalds",
        "source": "",
    },
    {
        "text": "Any fool can write code that a computer can understand. Good programmers write code that humans can understand.",
        "author": "Martin Fowler",
        "source": "Refactoring",
    },
    {
        "text": "First, solve the problem. Then, write the code.",
        "author": "John Johnson",
        "source": "",
    },
    {
        "text": "The most damaging phrase in the language is: We have always done it this way.",
        "author": "Grace Hopper",
        "source": "",
    },
]


def seed():
    # Seed languages
    lang_count = 0
    for lang_data in LANGUAGES:
        _, created = Language.objects.update_or_create(
            code=lang_data["code"],
            defaults=lang_data,
        )
        if created:
            lang_count += 1
    print(f"✅ Languages: {lang_count} created")

    # Get English language
    en = Language.objects.get(code="en")

    # Seed English word list
    wl, created = WordList.objects.update_or_create(
        slug="english-1k",
        defaults={
            "name": "English 1K",
            "description": "Top 1000 most common English words",
            "words": ENGLISH_1K,
            "language": en,
            "difficulty": "easy",
            "is_public": True,
            "is_default": True,
        },
    )
    print(f"✅ Word List 'English 1K': {'created' if created else 'updated'} ({wl.word_count} words)")

    # Seed quotes
    quote_count = 0
    for q in QUOTES:
        _, created = Quote.objects.get_or_create(
            text=q["text"],
            defaults={
                "author": q["author"],
                "source": q.get("source", ""),
                "language": en,
            },
        )
        if created:
            quote_count += 1
    print(f"✅ Quotes: {quote_count} created")


if __name__ == "__main__":
    seed()
else:
    seed()
