"""Run messy paragraphs through several modes and score them against gold text."""

import os
import sys

from corrector.pipeline import (
    correct_sentence,
    correct_text,
    load_model,
    restore_commas,
    split_sentences,
    tidy_punctuation,
)
from corrector.safety import safe_correct

SUFFIX = "_fresh" if "--fresh" in sys.argv else ""
INPUT = f"examples/messy{SUFFIX}.txt"
GOLD = f"examples/gold{SUFFIX}.txt"
OUTPUT = f"examples/results{SUFFIX}.md"


def model_safe(text, tokenizer, model):
    """Model + safety checks, without the spell step."""
    out = []
    for sentence in split_sentences(text):
        raw = correct_sentence(sentence, tokenizer, model)
        out.append(restore_commas(sentence, safe_correct(sentence, raw)))
    return tidy_punctuation(" ".join(out))


def model_only(text, tokenizer, model):
    """The raw model output, no spell step and no safety checks."""
    parts = [
        restore_commas(s, correct_sentence(s, tokenizer, model))
        for s in split_sentences(text)
    ]
    return tidy_punctuation(" ".join(parts))


def spell_model(text, tokenizer, model):
    """Spell step + model, without the safety checks."""
    from corrector.spell import fix_with_context

    out = []
    for sentence in split_sentences(text):
        spelled, _unsure = fix_with_context(sentence)
        out.append(restore_commas(spelled, correct_sentence(spelled, tokenizer, model)))
    return tidy_punctuation(" ".join(out))


MODES = {
    "pipeline (spell + model + safety)": correct_text,
    "model + safety (no spell)": model_safe,
    "model only": model_only,
    "spell + model (no safety)": spell_model,
}


def read_blocks(path):
    with open(path, encoding="utf-8") as f:
        return [b.strip() for b in f.read().split("\n\n") if b.strip()]


def overall_gleu(predictions, golds):
    import evaluate

    metric = evaluate.load("google_bleu")
    refs = [[g] for g in golds]
    return metric.compute(predictions=predictions, references=refs)["google_bleu"]


def main():
    paragraphs = read_blocks(INPUT)
    golds = read_blocks(GOLD) if os.path.exists(GOLD) else None
    if golds and len(golds) != len(paragraphs):
        print("gold.txt and messy.txt must have the same number of blocks")
        golds = None

    tokenizer, model = load_model()
    results = {
        name: [fn(text, tokenizer, model) for text in paragraphs]
        for name, fn in MODES.items()
    }

    lines = ["# Results", ""]
    if golds:
        lines += ["| Mode | GLEU vs gold |", "|---|---|"]
        base = overall_gleu(paragraphs, golds)
        lines.append(f"| no change | {base:.3f} |")
        print(f"{'no change':36s} {base:.3f}")
        for name, outs in results.items():
            score = overall_gleu(outs, golds)
            lines.append(f"| {name} | {score:.3f} |")
            print(f"{name:36s} {score:.3f}")
        lines.append("")

    for i, text in enumerate(paragraphs, 1):
        lines += [f"## Example {i}", "", "**Input**", "", f"> {text}", ""]
        for name, outs in results.items():
            lines += [f"**{name}**", "", f"> {outs[i - 1]}", ""]
        if golds:
            lines += ["**Gold**", "", f"> {golds[i - 1]}", ""]

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("Saved to", OUTPUT)


if __name__ == "__main__":
    main()
