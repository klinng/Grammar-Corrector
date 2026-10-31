"""List the paragraphs where the pipeline output differs from the gold text."""

import re
import sys

PIPELINE = "pipeline (spell + model + safety)"


def norm(text):
    return re.sub(r"\s+([,.!?;:])", r"\1", text).strip()


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "examples/results_fresh.md"
    with open(path, encoding="utf-8") as f:
        chunks = f.read().split("## Example ")[1:]
    wrong = 0
    for chunk in chunks:
        fields = dict(re.findall(r"\*\*(.+?)\*\*\n\n> (.*?)\n", chunk))
        out, gold = fields.get(PIPELINE), fields.get("Gold")
        if out is None or gold is None:
            continue
        if norm(out) != norm(gold):
            wrong += 1
            print(f"#{chunk.split()[0]}")
            print("  IN  :", fields.get("Input"))
            print("  OUT :", out)
            print("  GOLD:", gold)
            print()
    print(f"{wrong} of {len(chunks)} paragraphs differ from the gold text")


if __name__ == "__main__":
    main()
