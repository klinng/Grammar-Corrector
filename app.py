import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="Fix spelling and grammar.")
    parser.add_argument("text", nargs="?", help="text to correct")
    parser.add_argument("-f", "--file", help="read the text from a file")
    parser.add_argument("-o", "--output", help="write the result to a file")
    parser.add_argument(
        "-m",
        "--mode",
        choices=["light", "fix", "rewrite", "improve"],
        default="light",
        help="light = T5 on this PC; fix/rewrite/improve = Ollama model",
    )
    parser.add_argument("-t", "--tone", default="natural", help="tone for improve mode")
    args = parser.parse_args()

    if args.file:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        parser.print_help()
        sys.exit(1)

    if args.mode == "light":
        from corrector.pipeline import correct_text, load_model

        tokenizer, model = load_model()
        result = correct_text(text, tokenizer, model)
    else:
        from corrector.smart import smart_correct

        result = smart_correct(text, args.mode, args.tone)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print("Saved to", args.output)
    else:
        print(result)


if __name__ == "__main__":
    main()