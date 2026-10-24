import random

CONFUSIONS = {
    "their": ["there", "they're"],
    "there": ["their", "they're"],
    "they're": ["their", "there"],
    "your": ["you're"],
    "you're": ["your"],
    "its": ["it's"],
    "it's": ["its"],
}

ARTICLES = {"a", "an", "the"}


def add_typo(sentence, rng):
    """Swap two neighbouring letters inside one random word."""
    words = sentence.split()
    candidates = [i for i, w in enumerate(words) if len(w) >= 4 and w.isalpha()]
    if not candidates:
        return sentence
    i = rng.choice(candidates)
    w = words[i]
    j = rng.randrange(1, len(w) - 2)
    words[i] = w[:j] + w[j + 1] + w[j] + w[j + 2:]
    return " ".join(words)


def drop_article(sentence, rng):
    """Remove one article (a, an, the)."""
    words = sentence.split()
    candidates = [i for i, w in enumerate(words) if w.lower() in ARTICLES]
    if not candidates:
        return sentence
    del words[rng.choice(candidates)]
    return " ".join(words)


def confuse_word(sentence, rng):
    """Replace their/there/your/its with a wrong lookalike."""
    words = sentence.split()
    candidates = [i for i, w in enumerate(words) if w.lower() in CONFUSIONS]
    if not candidates:
        return sentence
    i = rng.choice(candidates)
    words[i] = rng.choice(CONFUSIONS[words[i].lower()])
    return " ".join(words)

def wrong_a_an(sentence, rng):
    """Swap a/an so it no longer matches the next word."""
    words = sentence.split()
    candidates = [i for i, w in enumerate(words) if w.lower() in {"a", "an"}]
    if not candidates:
        return sentence
    i = rng.choice(candidates)
    words[i] = "an" if words[i].lower() == "a" else "a"
    return " ".join(words)


def drop_letter(sentence, rng):
    """Remove one letter from a random word (like tomorow)."""
    words = sentence.split()
    candidates = [i for i, w in enumerate(words) if len(w) >= 5 and w.isalpha()]
    if not candidates:
        return sentence
    i = rng.choice(candidates)
    w = words[i]
    j = rng.randrange(1, len(w) - 1)
    words[i] = w[:j] + w[j + 1 :]
    return " ".join(words)


def double_letter(sentence, rng):
    """Repeat one letter in a random word (like developped)."""
    words = sentence.split()
    candidates = [i for i, w in enumerate(words) if len(w) >= 4 and w.isalpha()]
    if not candidates:
        return sentence
    i = rng.choice(candidates)
    w = words[i]
    j = rng.randrange(1, len(w) - 1)
    words[i] = w[: j + 1] + w[j] + w[j + 1 :]
    return " ".join(words)

def lowercase_start(sentence, rng):
    """Make the first letter lowercase (like: i went home)."""
    if not sentence or not sentence[0].isupper():
        return sentence
    return sentence[0].lower() + sentence[1:]


def drop_apostrophe(sentence, rng):
    """Remove an apostrophe (like: dont, hows)."""
    candidates = [i for i, ch in enumerate(sentence) if ch == "'"]
    if not candidates:
        return sentence
    i = rng.choice(candidates)
    return sentence[:i] + sentence[i + 1 :]


def swap_neighbours(sentence, rng):
    """Swap two neighbouring letters in a short word (like: wnet, rlife)."""
    words = sentence.split()
    candidates = [i for i, w in enumerate(words) if len(w) >= 3 and w.isalpha()]
    if not candidates:
        return sentence
    i = rng.choice(candidates)
    w = words[i]
    j = rng.randrange(0, len(w) - 1)
    words[i] = w[:j] + w[j + 1] + w[j] + w[j + 2 :]
    return " ".join(words)

ERROR_FUNCS = [
    add_typo,
    drop_article,
    confuse_word,
    wrong_a_an,
    drop_letter,
    double_letter,
    lowercase_start,
    drop_apostrophe,
    swap_neighbours,
]


def corrupt(sentence, rng=None):
    """Apply 1 or 2 random errors. Returns (bad, good)."""
    rng = rng or random.Random()
    bad = sentence
    for func in rng.sample(ERROR_FUNCS, k=rng.choice([1, 2])):
        bad = func(bad, rng)
    return bad, sentence


if __name__ == "__main__":
    rng = random.Random(42)
    clean = [
        "I saw the dog in their garden yesterday.",
        "She bought a new phone because the old one broke.",
        "It is important to finish your homework before dinner.",
    ]
    for s in clean:
        bad, good = corrupt(s, rng)
        print("BAD :", bad)
        print("GOOD:", good)
        print()