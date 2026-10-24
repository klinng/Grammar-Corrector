import re

from corrector.safety import safe_correct
from corrector.spell import fix_with_context

MODEL_DIR = "models/t5-small-gec"


def clean_text(text):
    """Collapse repeated spaces and line breaks into single spaces."""
    return re.sub(r"\s+", " ", text).strip()


def split_sentences(text):
    """Cut text after . ! or ? followed by a space."""
    parts = re.split(r"(?<=[.!?])\s+", clean_text(text))
    return [p for p in parts if p]


def load_model(model_dir=MODEL_DIR):
    from transformers import T5ForConditionalGeneration, T5Tokenizer

    tokenizer = T5Tokenizer.from_pretrained(model_dir)
    model = T5ForConditionalGeneration.from_pretrained(model_dir)
    return tokenizer, model


def correct_sentence(sentence, tokenizer, model):
    inputs = tokenizer(
        "fix grammar: " + sentence, return_tensors="pt", truncation=True, max_length=128
    )
    out = model.generate(**inputs, max_new_tokens=128)
    return tokenizer.decode(out[0], skip_special_tokens=True)


def correct_text(text, tokenizer, model, choices=None):
    results = []
    for sentence in split_sentences(text):
        spelled, _unsure = fix_with_context(sentence)
        corrected = correct_sentence(spelled, tokenizer, model)
        results.append(safe_correct(spelled, corrected))
    return " ".join(results)


if __name__ == "__main__":
    tokenizer, model = load_model()
    print("Type a text (empty line to quit).")
    while True:
        text = input("> ")
        if not text.strip():
            break
        print("FIXED:", correct_text(text, tokenizer, model))