# Grammar Corrector

A grammar and spelling corrector I trained myself: **T5-small fine-tuned on public data plus a synthetic error generator**, wrapped in a pipeline with a context-aware spell step and safety checks. It runs on a laptop, with no cloud and no private data.

An optional smart mode compares it with a larger model (Qwen via Ollama), so you can see where the small model is strong and where it is not.

## See it working

Run the same messy texts through every mode and read the result:

```bash
python compare.py
```

This writes [`examples/results.md`](examples/results.md): input, light-mode output, and the smart-mode outputs side by side. The inputs are in `examples/messy.txt`; add your own.

### Examples (light mode, my model)

| Input | Output |
|---|---|
| i wnet there before | I went there before. |
| Because they were very hungry, they decided to cuuked a masive dinr on the sidewalk. | Because they were very hungry, they decided to cook a massive dinner on the sidewalk. |

### Where it still fails (on purpose, shown openly)

| Input | Light mode | Smart mode (fix) |
|---|---|---|
| his there hosw your dasy today was it good to ahve you herer | It there how your day today was it good to have you here. | How was your day? Was it good to have you here? |

Light mode repairs typos and common grammar mistakes well. Text spelled by sound, or with many errors per sentence, is where a larger model wins. That gap is what the training work in the roadmap aims to close.

## Results

JFLEG test set, 748 sentences never used for training, GLEU score, T5 model only:

| System | GLEU |
|---|---|
| No change (baseline) | 0.7736 |
| Fine-tuned T5-small (this project) | 0.7969 |

## How it works

```
text -> cleaner -> sentence splitter -> context spell-check -> T5 model -> safety checks -> merger
```

- **Context spell-check:** `pyspellchecker` proposes candidates and `distilgpt2` picks the one that fits the sentence.
- **T5-small:** fine-tuned for grammar, tense, capitals and punctuation.
- **Safety checks:** reject a rewrite that drifts too far, and put back any word T5 replaced with a very different one. A typo left alone is better than an invented word.

### Training data

- **JFLEG** (`validation` split) and **WikiText-2** sentences broken on purpose.
- An **error generator** with 13 error types (typos, dropped and doubled letters, a/an, their/there, apostrophes, lowercase start, verb forms after `to` and `did`, agreement, plurals), 1 to 4 per sentence.
- The JFLEG `test` split is never used for training.

## Install

```bash
git clone https://github.com/klinng/Grammar-Corrector.git
cd Grammar-Corrector
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

Train the model with `python src/corrector/train.py`, or on a free Colab GPU with `notebooks/colab_train.ipynb` (about 3 minutes). You need `models/t5-small-gec` before running the app.

## Usage

```bash
python app.py "i wnet there before"
python app.py -f input.txt -o output.txt
```

### Optional: smart mode (local)

Install [Ollama](https://ollama.com), run `ollama pull qwen2.5:3b-instruct`, then:

```bash
python app.py "i wnet there before" --mode fix
python app.py "i wnet there before" --mode improve --tone friendly
```

Smart mode uses a model I did not train. It is there for comparison and for text the light mode cannot handle.

## Tests and CI

22 tests with `pytest`, style checked with `ruff`, both run by GitHub Actions on every push.

## Limitations

- T5-small is small: little sense of context, and it can invent words for badly damaged text.
- The spell step compares letters, so words spelled by sound are hard.
- The benchmark score covers the T5 model alone, not the full pipeline.

## Roadmap

1. Phonetic error generator (`woz`, `bekaus`) so training matches real messy writing.
2. A dataset of messy paragraphs with clean targets, then train `flan-t5-base` on Colab.
3. Score the full pipeline and my own messy test set, not only JFLEG.
