from transformers import T5ForConditionalGeneration, T5Tokenizer

MODEL_DIR = "models/t5-small-gec"

tokenizer = T5Tokenizer.from_pretrained(MODEL_DIR)
model = T5ForConditionalGeneration.from_pretrained(MODEL_DIR)

samples = [
    "She go to school yesterday.",
    "I has a apple.",
    "Their going to the park tomorow.",
    "i walkad hame at night sudenly soemthign strenge happended",
    "Because they were very hungry, they decided to cooked a massive dinner on the sidewalk.",
]
for s in samples:
    inputs = tokenizer("fix grammar: " + s, return_tensors="pt")
    out = model.generate(**inputs, max_new_tokens=64)
    print("IN :", s)
    print("OUT:", tokenizer.decode(out[0], skip_special_tokens=True))
    print()