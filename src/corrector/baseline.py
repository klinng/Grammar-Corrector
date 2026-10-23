from transformers import T5ForConditionalGeneration, T5Tokenizer

MODEL_NAME = "t5-small"


def load_model():
    tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
    model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)
    return tokenizer, model


def correct(text, tokenizer, model):
    inputs = tokenizer("fix grammar: " + text, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=64)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


if __name__ == "__main__":
    tokenizer, model = load_model()
    samples = [
        "She go to school yesterday.",
        "I has a apple.",
        "Their going to the park tomorow.",
    ]
    for s in samples:
        print("IN :", s)
        print("OUT:", correct(s, tokenizer, model))
        print()