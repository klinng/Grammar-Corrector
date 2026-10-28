"""Run messy paragraphs through every mode and write a comparison file."""

from corrector.pipeline import correct_text, load_model

INPUT = "examples/messy.txt"
OUTPUT = "examples/results.md"


def read_paragraphs(path):
    with open(path, encoding="utf-8") as f:
        blocks = f.read().split("\n\n")
    return [b.strip() for b in blocks if b.strip()]


def try_smart(text, mode):
    from corrector.smart import smart_correct

    try:
        return smart_correct(text, mode)
    except RuntimeError:
        return None


def main():
    paragraphs = read_paragraphs(INPUT)
    tokenizer, model = load_model()
    lines = ["# Comparison: light mode vs smart mode", ""]
    for i, text in enumerate(paragraphs, 1):
        light = correct_text(text, tokenizer, model)
        lines += [f"## Example {i}", "", "**Input**", "", f"> {text}", ""]
        lines += ["**Light mode (T5-small, trained in this project)**", "", f"> {light}", ""]
        for mode in ("fix", "improve"):
            out = try_smart(text, mode)
            if out:
                lines += [f"**Smart mode: {mode} (Qwen via Ollama)**", "", f"> {out}", ""]
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("Saved to", OUTPUT)


if __name__ == "__main__":
    main()
