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


if __name__ == "__main__":
    data = load_jfleg()
    print(data)
    pairs = make_pairs(data["validation"])
    print("Number of pairs:", len(pairs))
    for src, tgt in pairs[:3]:
        print("IN :", src)
        print("OUT:", tgt)
        print()