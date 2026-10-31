import re
from difflib import SequenceMatcher

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


def tidy_punctuation(text):
    """Remove spaces before , . ! ? ; : (the model copies JFLEG's spaced style)."""
    return re.sub(r"\s+([,.!?;:])", r"\1", text)


def restore_commas(original, corrected):
    """Put back commas the model dropped (only where the word before it is unchanged)."""
    orig = original.split()
    new = corrected.split()

    def core(word):
        return re.sub(r"\W", "", word).lower()

    matcher = SequenceMatcher(None, [core(w) for w in orig], [core(w) for w in new])
    out = list(new)
    for tag, i1, i2, j1, _j2 in matcher.get_opcodes():
        if tag != "equal":
            continue
        for k in range(i2 - i1):
            has_comma = orig[i1 + k].endswith(",")
            if has_comma and not out[j1 + k].endswith((",", ".", "!", "?", ";", ":")):
                out[j1 + k] += ","
    return " ".join(out)


def correct_text(text, tokenizer, model, choices=None):
    results = []
    for sentence in split_sentences(text):
        spelled, _unsure = fix_with_context(sentence)
        corrected = correct_sentence(spelled, tokenizer, model)
        safe = safe_correct(spelled, corrected)
        results.append(restore_commas(spelled, safe))
    return tidy_punctuation(" ".join(results))


if __name__ == "__main__":
    tokenizer, model = load_model()
    print("Type a text (empty line to quit).")
    while True:
        text = input("> ")
        if not text.strip():
            break
        print("FIXED:", correct_text(text, tokenizer, model))