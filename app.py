import argparse
import sys

from corrector.pipeline import correct_text, load_model


def main():
    parser = argparse.ArgumentParser(description="Fix spelling and grammar.")
    parser.add_argument("text", nargs="?", help="text to correct")
    parser.add_argument("-f", "--file", help="read the text from a file")
    parser.add_argument("-o", "--output", help="write the result to a file")
    args = parser.parse_args()

    if args.file:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        parser.print_help()
        sys.exit(1)

    tokenizer, model = load_model()
    result = correct_text(text, tokenizer, model)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print("Saved to", args.output)
    else:
        print(result)


if __name__ == "__main__":
    main()