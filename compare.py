"""Run messy paragraphs through the corrector and write the results to a file."""

from corrector.pipeline import correct_text, load_model

INPUT = "examples/messy.txt"
OUTPUT = "examples/results.md"


def read_paragraphs(path):
    with open(path, encoding="utf-8") as f:
        blocks = f.read().split("\n\n")
    return [b.strip() for b in blocks if b.strip()]


def main():
    paragraphs = read_paragraphs(INPUT)
    tokenizer, model = load_model()
    lines = ["# Results", ""]
    for i, text in enumerate(paragraphs, 1):
        out = correct_text(text, tokenizer, model)
        lines += [f"## Example {i}", "", "**Input**", "", f"> {text}", ""]
        lines += ["**Output**", "", f"> {out}", ""]
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("Saved to", OUTPUT)


if __name__ == "__main__":
    main()