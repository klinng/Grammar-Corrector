"""Try different safety-check settings on the messy set, reusing one model run."""

import evaluate

from corrector.pipeline import correct_sentence, load_model, split_sentences
from corrector.safety import is_safe, revert_wild_words
from corrector.spell import fix_with_context

INPUT = "examples/messy.txt"
GOLD = "examples/gold.txt"


def read_blocks(path):
    with open(path, encoding="utf-8") as f:
        return [b.strip() for b in f.read().split("\n\n") if b.strip()]


def apply_safety(spelled, out, drift, wild):
    """drift: min similarity for is_safe (None = off). wild: revert threshold (None = off)."""
    result = out
    if drift is not None and not is_safe(spelled, out, min_similarity=drift):
        return spelled
    if wild is not None:
        result = revert_wild_words(spelled, result, min_similarity=wild)
    return result


def main():
    paragraphs = read_blocks(INPUT)
    golds = read_blocks(GOLD)
    tokenizer, model = load_model()

    # run the slow parts once: (spelled sentence, model output) per sentence
    cache = []
    for text in paragraphs:
        pairs = []
        for sentence in split_sentences(text):
            spelled, _unsure = fix_with_context(sentence)
            pairs.append((spelled, correct_sentence(spelled, tokenizer, model)))
        cache.append(pairs)

    gleu = evaluate.load("google_bleu")
    refs = [[g] for g in golds]

    def score(drift, wild):
        preds = [
            " ".join(apply_safety(s, o, drift, wild) for s, o in pairs) for pairs in cache
        ]
        return gleu.compute(predictions=preds, references=refs)["google_bleu"]

    print(f"{'drift check':14s} {'word revert':12s} GLEU")
    for drift in (None, 0.6):
        for wild in (None, 0.4, 0.5, 0.6, 0.7):
            d = "off" if drift is None else f">= {drift}"
            w = "off" if wild is None else f"< {wild}"
            print(f"{d:14s} {w:12s} {score(drift, wild):.3f}")


if __name__ == "__main__":
    main()
