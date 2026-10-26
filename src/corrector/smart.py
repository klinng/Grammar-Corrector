import json
import urllib.error
import urllib.request

URL = "http://127.0.0.1:11434/api/chat"
MODEL = "qwen2.5:3b-instruct"

PROMPTS = {
    "fix": (
        "Fix the spelling, grammar and punctuation of the text. Keep every part "
        "of the message: do not delete words or greetings, and do not add new "
        "information. Return only the corrected text."
    ),
    "rewrite": (
        "Rewrite the text in natural, fluent English with good flow. Keep every "
        "part of the message and do not add new information. Fix all errors. "
        "Return only the final text."
    ),
    "improve": (
        "You are an expert editor. Rewrite the text so it reads better than the "
        "writer likely imagined: fix every error, then improve word choice, use "
        "stronger and more precise verbs, vary the sentence structure and add "
        "smooth transitions. Tone: {tone}. Keep the original meaning and every "
        "fact. Do not invent new events, names, numbers or details. "
        "Return only the final text."
    ),
}

TONES = ["natural", "formal", "friendly", "vivid storytelling", "professional email"]


def smart_correct(text, mode="fix", tone="natural", model=MODEL):
    system = PROMPTS[mode].format(tone=tone) if mode == "improve" else PROMPTS[mode]
    payload = {
        "model": model,
        "stream": False,
        "options": {"temperature": 0.4 if mode == "improve" else 0},
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": text},
        ],
    }
    req = urllib.request.Request(
        URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            return json.load(resp)["message"]["content"].strip()
    except urllib.error.HTTPError as err:
        raise RuntimeError(
            f"Ollama does not have the model '{model}'. "
            f"Run 'ollama pull {model}' or check 'ollama list'."
        ) from err
    except urllib.error.URLError as err:
        raise RuntimeError(
            "Cannot reach Ollama. Install it from ollama.com and make sure it is running."
        ) from err