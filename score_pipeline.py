"""Score the pipeline modes on a slice of the JFLEG test set (a second source)."""

import argparse

import evaluate
from datasets import load_dataset

from corrector.pipeline import correct_sentence, load_model, restore_commas
from corrector.safety import safe_correct
from corrector.spell import fix_with_context


def main():
    parser = argparse.ArgumentParser(description="Score pipeline modes on JFLEG.")
    parser.add_argument("-n", type=int, default=150, help="number of test sentences")
    args = parser.parse_args()

    rows = load_dataset("jhu-clsp/jfleg")["test"].select(range(args.n))
    sources = [r["sentence"].strip() for r in rows]
    refs = [[c.strip() for c in r["corrections"]] for r in rows]

    tokenizer, model = load_model()
    outputs = {
        "model only": [],
        "model + safety (no spell)": [],
        "spell + model (no safety)": [],
        "full pipeline": [],
    }
    for i, sentence in enumerate(sources, 1):
        raw = correct_sentence(sentence, tokenizer, model)
        spelled, _unsure = fix_with_context(sentence)
        after_spell = correct_sentence(spelled, tokenizer, model)
        outputs["model only"].append(restore_commas(sentence, raw))
        outputs["model + safety (no spell)"].append(
            restore_commas(sentence, safe_correct(sentence, raw))
        )
        outputs["spell + model (no safety)"].append(restore_commas(spelled, after_spell))
        outputs["full pipeline"].append(
            restore_commas(spelled, safe_correct(spelled, after_spell))
        )
        if i % 25 == 0:
            print(f"{i}/{len(sources)} sentences done")

    gleu = evaluate.load("google_bleu")

    def score(preds):
        return gleu.compute(predictions=preds, references=refs)["google_bleu"]

    print(f"\nSentences scored: {len(sources)}")
    print(f"{'no change':30s} {score(sources):.4f}")
    for name, preds in outputs.items():
        print(f"{name:30s} {score(preds):.4f}")


if __name__ == "__main__":
    main()
