"""Run messy paragraphs through the corrector and score them against gold text."""

import os

from corrector.pipeline import correct_text, load_model

INPUT = "examples/messy.txt"
GOLD = "examples/gold.txt"
OUTPUT = "examples/results.md"


def read_blocks(path):
    with open(path, encoding="utf-8") as f:
        return [b.strip() for b in f.read().split("\n\n") if b.strip()]


def gleu(predictions, golds):
    import evaluate

    metric = evaluate.load("google_bleu")
    per = [
        metric.compute(predictions=[p], references=[[g]])["google_bleu"]
        for p, g in zip(predictions, golds)
    ]
    total = metric.compute(predictions=predictions, references=[[g] for g in golds])
    return per, total["google_bleu"]


def main():
    paragraphs = read_blocks(INPUT)
    tokenizer, model = load_model()
    outputs = [correct_text(t, tokenizer, model) for t in paragraphs]

    golds = read_blocks(GOLD) if os.path.exists(GOLD) else None
    if golds and len(golds) != len(paragraphs):
        print("gold.txt and messy.txt must have the same number of blocks")
        golds = None
    if golds:
        per, total = gleu(outputs, golds)
        _, base = gleu(paragraphs, golds)

    lines = ["# Results", ""]
    for i, (text, out) in enumerate(zip(paragraphs, outputs), 1):
        lines += [f"## Example {i}", "", "**Input**", "", f"> {text}", ""]
        lines += ["**Output**", "", f"> {out}", ""]
        if golds:
            lines += [f"GLEU vs gold: {per[i - 1]:.3f}", ""]
    if golds:
        lines += [f"**Overall GLEU:** {total:.3f} (no change: {base:.3f})", ""]
        print(f"Overall GLEU: {total:.3f} (no change: {base:.3f})")
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("Saved to", OUTPUT)


if __name__ == "__main__":
    main()
