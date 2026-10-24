import evaluate
from datasets import load_dataset
from transformers import T5ForConditionalGeneration, T5Tokenizer

MODEL_DIR = "models/t5-small-gec"
N = 200  # number of test sentences; raise to 748 for the full test set


def correct_batch(sentences, tokenizer, model, batch_size=16):
    results = []
    for i in range(0, len(sentences), batch_size):
        batch = ["fix grammar: " + s for s in sentences[i : i + batch_size]]
        enc = tokenizer(
            batch, return_tensors="pt", padding=True, truncation=True, max_length=128
        )
        out = model.generate(**enc, max_new_tokens=128)
        results.extend(tokenizer.batch_decode(out, skip_special_tokens=True))
    return results


def main():
    test = load_dataset("jhu-clsp/jfleg")["test"]
    rows = test.select(range(N))
    sources = [r["sentence"].strip() for r in rows]
    refs = [[c.strip() for c in r["corrections"]] for r in rows]

    tokenizer = T5Tokenizer.from_pretrained(MODEL_DIR)
    model = T5ForConditionalGeneration.from_pretrained(MODEL_DIR)
    preds = correct_batch(sources, tokenizer, model)

    gleu = evaluate.load("google_bleu")
    base = gleu.compute(predictions=sources, references=refs)["google_bleu"]
    ours = gleu.compute(predictions=preds, references=refs)["google_bleu"]
    print(f"Sentences scored : {N}")
    print(f"Baseline (no change): {base:.4f}")
    print(f"Our model            : {ours:.4f}")


if __name__ == "__main__":
    main()