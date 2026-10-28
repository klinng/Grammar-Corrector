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

def wrong_verb_form(sentence, rng):
    """Put a verb after 'to' in the past tense (like: to cooked)."""
    words = sentence.split()
    candidates = [
        i
        for i in range(1, len(words))
        if words[i - 1].lower() == "to" and words[i].isalpha() and len(words[i]) >= 3
    ]
    if not candidates:
        return sentence
    i = rng.choice(candidates)
    w = words[i]
    words[i] = w + ("d" if w.endswith("e") else "ed")
    return " ".join(words)


AGREEMENT = {"is": "are", "are": "is", "was": "were", "were": "was", "has": "have", "have": "has"}


def wrong_agreement(sentence, rng):
    """Swap is/are, was/were, has/have (like: they was)."""
    words = sentence.split()
    candidates = [i for i, w in enumerate(words) if w.lower() in AGREEMENT]
    if not candidates:
        return sentence
    i = rng.choice(candidates)
    words[i] = AGREEMENT[words[i].lower()]
    return " ".join(words)


def wrong_did(sentence, rng):
    """Put the past tense after did (like: did went)."""
    words = sentence.split()
    candidates = [i for i in range(len(words) - 1) if words[i].lower() in {"did", "didn't"}]
    if not candidates:
        return sentence
    i = rng.choice(candidates)
    nxt = words[i + 1]
    if not nxt.isalpha() or len(nxt) < 2:
        return sentence
    words[i + 1] = nxt + ("d" if nxt.endswith("e") else "ed")
    return " ".join(words)


def drop_plural(sentence, rng):
    """Remove a final 's' from a plural-looking word (like: two cat)."""
    words = sentence.split()
    candidates = [
        i for i, w in enumerate(words) if len(w) >= 4 and w.endswith("s") and w.isalpha()
    ]
    if not candidates:
        return sentence
    i = rng.choice(candidates)
    words[i] = words[i][:-1]
    return " ".join(words)

IRREGULAR = {
    "go": ("went", "gone"), "run": ("ran", "run"), "eat": ("ate", "eaten"),
    "see": ("saw", "seen"), "take": ("took", "taken"), "write": ("wrote", "written"),
    "come": ("came", "come"), "give": ("gave", "given"), "know": ("knew", "known"),
    "buy": ("bought", "bought"), "bring": ("brought", "brought"),
    "think": ("thought", "thought"), "begin": ("began", "begun"),
    "drink": ("drank", "drunk"), "drive": ("drove", "driven"),
    "fall": ("fell", "fallen"), "forget": ("forgot", "forgotten"),
    "get": ("got", "got"), "have": ("had", "had"), "make": ("made", "made"),
    "say": ("said", "said"), "tell": ("told", "told"), "choose": ("chose", "chosen"),
    "break": ("broke", "broken"), "speak": ("spoke", "spoken"),
    "swim": ("swam", "swum"), "wear": ("wore", "worn"), "win": ("won", "won"),
    "leave": ("left", "left"), "find": ("found", "found"), "feel": ("felt", "felt"),
    "keep": ("kept", "kept"), "sit": ("sat", "sat"), "stand": ("stood", "stood"),
    "teach": ("taught", "taught"), "catch": ("caught", "caught"),
    "fly": ("flew", "flown"), "grow": ("grew", "grown"),
    "throw": ("threw", "thrown"), "draw": ("drew", "drawn"), "sing": ("sang", "sung"),
}

PAST_TO_BASE = {}
for _base, _forms in IRREGULAR.items():
    for _form in _forms:
        if _form != _base:
            PAST_TO_BASE.setdefault(_form, _base)

_PUNCT = ".,!?;:"


def wrong_conjugation(sentence, rng):
    """Replace an irregular past form by a wrong one (went -> goed or go)."""
    words = sentence.split()
    candidates = [
        i for i, w in enumerate(words) if w.lower().strip(_PUNCT) in PAST_TO_BASE
    ]
    if not candidates:
        return sentence
    i = rng.choice(candidates)
    raw = words[i]
    base = PAST_TO_BASE[raw.lower().strip(_PUNCT)]
    tail = raw[len(raw.rstrip(_PUNCT)):]
    regular = base + ("d" if base.endswith("e") else "ed")
    new = rng.choice([regular, base])
    if raw[0].isupper():
        new = new.capitalize()
    words[i] = new + tail
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
    wrong_verb_form,
    wrong_agreement,
    wrong_did,
    drop_plural,
    wrong_conjugation,
]


def corrupt(sentence, rng=None):
    """Apply 1 or 2 random errors. Returns (bad, good)."""
    rng = rng or random.Random()
    bad = sentence
    for func in rng.sample(ERROR_FUNCS, k=rng.choice([1, 2, 3 , 4])):
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