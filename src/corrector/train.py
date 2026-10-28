import random

from datasets import Dataset
from transformers import (
    DataCollatorForSeq2Seq,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments,
    T5ForConditionalGeneration,
    T5Tokenizer,
)

from corrector.data_prep import (
    load_jfleg,
    make_pairs,
    make_synthetic_pairs,
    make_wiki_pairs,
)

MODEL_NAME = "t5-small"
OUTPUT_DIR = "models/t5-small-gec"
MAX_EXAMPLES = 20000


def build_dataset(tokenizer):
    data = load_jfleg()
    real = make_pairs(data["validation"])
    synthetic = make_synthetic_pairs(data["validation"])
    wiki = make_wiki_pairs()
    pairs = real + synthetic + wiki
    random.Random(0).shuffle(pairs)
    print("Pairs available:", len(pairs))
    pairs = pairs[:MAX_EXAMPLES]

    ds = Dataset.from_dict(
        {"source": [p[0] for p in pairs], "target": [p[1] for p in pairs]}
    )

    def tokenize(batch):
        enc = tokenizer(batch["source"], max_length=128, truncation=True)
        labels = tokenizer(text_target=batch["target"], max_length=128, truncation=True)
        enc["labels"] = labels["input_ids"]
        return enc

    return ds.map(tokenize, batched=True, remove_columns=["source", "target"])


def main():
    tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
    model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)
    train_ds = build_dataset(tokenizer)

    args = Seq2SeqTrainingArguments(
        output_dir=OUTPUT_DIR,
        per_device_train_batch_size=8,
        learning_rate=3e-4,
        num_train_epochs=2,
        logging_steps=20,
        save_strategy="no",
        report_to="none",
    )
    trainer = Seq2SeqTrainer(
        model=model,
        args=args,
        train_dataset=train_ds,
        data_collator=DataCollatorForSeq2Seq(tokenizer, model=model),
    )
    trainer.train()
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print("Saved to", OUTPUT_DIR)


if __name__ == "__main__":
    main()