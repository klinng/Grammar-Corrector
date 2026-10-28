from datasets import load_dataset

PREFIX = "fix grammar: "


def load_jfleg():
    """Load JFLEG from Hugging Face (public, free)."""
    return load_dataset("jhu-clsp/jfleg")


def make_pairs(split):
    """Return a list of (input_text, target_text) pairs.

    JFLEG gives one bad sentence and several corrections.
    We make one pair per correction.
    """
    pairs = []
    for row in split:
        bad = row["sentence"].strip()
        for good in row["corrections"]:
            good = good.strip()
            if bad and good:
                pairs.append((PREFIX + bad, good))
    return pairs

def make_synthetic_pairs(split, per_sentence=3, seed=0):
    """Break clean JFLEG corrections on purpose to make extra pairs."""
    import random

    from corrector.error_gen import corrupt

    rng = random.Random(seed)
    clean = {c.strip() for row in split for c in row["corrections"] if c.strip()}
    pairs = []
    for good in sorted(clean):
        for _ in range(per_sentence):
            bad, good_text = corrupt(good, rng)
            if bad != good_text:
                pairs.append((PREFIX + bad, good_text))
    return pairs

def load_clean_sentences(max_sentences=10000, seed=0):
    """Short, clean sentences from Wikipedia (WikiText-2)."""
    import random
    import re

    ds = load_dataset("Salesforce/wikitext", "wikitext-2-raw-v1", split="train")
    sentences = []
    for row in ds:
        text = row["text"].strip()
        if not text or text.startswith("="):
            continue
        for s in re.split(r"(?<=[.!?])\s+", text):
            s = s.replace(" @-@ ", "-").replace(" @,@ ", ",").replace(" @.@ ", ".")
            words = s.split()
            if 5 <= len(words) <= 20 and s[0].isupper() and s.endswith("."):
                sentences.append(s)
    random.Random(seed).shuffle(sentences)
    return sentences[:max_sentences]

if __name__ == "__main__":
    data = load_jfleg()
    print(data)
    pairs = make_pairs(data["validation"])
    print("Number of pairs:", len(pairs))
    for src, tgt in pairs[:3]:
        print("IN :", src)
        print("OUT:", tgt)
        print()

def make_wiki_pairs(per_sentence=2, seed=0):
    """Break the Wikipedia sentences on purpose to make extra pairs."""
    import random

    from corrector.error_gen import corrupt

    rng = random.Random(seed)
    pairs = []
    for good in load_clean_sentences():
        for _ in range(per_sentence):
            bad, good_text = corrupt(good, rng)
            if bad != good_text:
                pairs.append((PREFIX + bad, good_text))
    return pairs