export const ENGLISH_WORDS = [
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
  "night", "talk", "boy", "door", "room", "book", "eye", "face", "try"
];

interface WordOptions {
  punctuation?: boolean;
  numbers?: boolean;
}

const PUNCTUATIONS = [",", ".", "?", "!", "-", "'", '"', "(", ")", ":"];

export const QUOTES = [
  "The only limit to our realization of tomorrow will be our doubts of today.",
  "In the end, it's not the years in your life that count. It's the life in your years.",
  "Success is not final, failure is not fatal: it is the courage to continue that counts.",
  "The future belongs to those who believe in the beauty of their dreams.",
  "Tell me and I forget. Teach me and I remember. Involve me and I learn."
];

/**
 * Returns an array of randomly selected words.
 */
export function generateWords(count: number, options?: WordOptions): string[] {
  const result: string[] = [];
  for (let i = 0; i < count; i++) {
    const randomIndex = Math.floor(Math.random() * ENGLISH_WORDS.length);
    let word = ENGLISH_WORDS[randomIndex];

    if (options?.numbers && Math.random() < 0.15) {
      word = Math.floor(Math.random() * 1000).toString();
    } else if (options?.punctuation) {
      if (Math.random() < 0.2) {
        const punc = PUNCTUATIONS[Math.floor(Math.random() * PUNCTUATIONS.length)];
        if (punc === '(') word = `(${word}`;
        else if (punc === '"') word = `"${word}"`;
        else word = `${word}${punc}`;
      }
      if (Math.random() < 0.1) {
        word = word.charAt(0).toUpperCase() + word.slice(1);
      }
    }
    result.push(word);
  }
  return result;
}

export function generateQuote(): string[] {
  const quote = QUOTES[Math.floor(Math.random() * QUOTES.length)];
  return quote.split(' ');
}
