# Grammar Corrector

A grammar and spelling corrector I trained myself: **FLAN-T5-base fine-tuned on public data plus a synthetic error generator**, wrapped in a pipeline with a context-aware spell step and safety checks. No private data is used.

## Results

JFLEG test set, 748 sentences never used for training, GLEU score, model only:

| System | GLEU |
|---|---|
| No change (baseline) | 0.7736 |
| T5-small, fine-tuned here | 0.7969 |
| **FLAN-T5-base, fine-tuned here** | **0.8288** |

My own messy-text test: 25 paragraphs with reference answers (`examples/messy.txt` and `examples/gold.txt`), full pipeline, GLEU:

| System | GLEU |
|---|---|
| No change (baseline) | 0.355 |
| T5-small pipeline | 0.663 |
| **FLAN-T5-base pipeline** | **0.687** |

The first 5 paragraphs were used while tuning, and 25 paragraphs is a small sample, so differences of about 0.02 are within noise. The JFLEG numbers are the more reliable ones.

Run the comparison yourself:

```bash
python compare.py
```

It scores three modes (full pipeline, model + safety checks, model only) against the reference answers and writes every output to `examples/results.md`.

## How it works

```
text -> cleaner -> sentence splitter -> context spell-check -> T5 model -> safety checks -> merger
```

- **Context spell-check:** `pyspellchecker` proposes candidates and `distilgpt2` picks the one that fits the sentence.
- **Model:** a pretrained FLAN-T5-base, fine-tuned here for grammar, tense, vocabulary and punctuation.
- **Safety checks:** reject a rewrite that drifts too far, and put back any word the model replaced with a very different one. A typo left alone is better than an invented word.

### Training data

- **JFLEG** (`validation` split) and **WikiText-2** sentences broken on purpose.
- An **error generator** with 16 error types: typos, dropped and doubled letters, a/an, their/there, apostrophes, lowercase start, verb forms after `to` and `did`, agreement, plurals, irregular verb conjugation, confusable words (then/than, lose/loose) and sound-spelling (woz, bekaus), 1 to 4 errors per sentence.
- 24,733 training pairs available, 20,000 used, 2 epochs.
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

The trained model (about 1 GB) is not stored in the repo. Train it yourself on a free Colab GPU with `notebooks/colab_train.ipynb` (about 15 to 30 minutes on a T4), then unzip the result so you get `models/t5-small-gec`. The folder keeps this name for historical reasons, and it now holds FLAN-T5-base.

## Usage

```bash
python app.py "i wnet there before"
python app.py -f input.txt -o output.txt
```

## Tests and CI

Unit tests with `pytest`, style checked with `ruff`, both run by GitHub Actions on every push.

## Limitations

- The model is still small. It has limited sense of context and can invent words for badly damaged text.
- The spell step compares letters, so words spelled by sound are hard.
- Rule-made training errors teach the model only the mistakes I thought of.
- Running the model on a CPU is slow with the base-size model.

## Roadmap

1. Compare the full pipeline with the model alone, and simplify if the spell step no longer helps.
2. More training and real learner data (for example BEA-2019, after checking its license).
3. A larger, more varied messy-text test set.
