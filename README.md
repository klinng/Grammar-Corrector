# Grammar Corrector

A grammar and spelling corrector built by fine-tuning T5 on public data
and synthetic errors. No private data is used.

## How it works

```
text -> cleaner -> sentence splitter -> spell-check -> T5 model -> safety check -> merger
```

- **Spell-check** (pyspellchecker) fixes typos like `walkad` -> `walked`.
- **T5-small**, fine-tuned for grammar, tense, capitals and punctuation.
- **Safety check** keeps the input sentence when the model changes too much.

## Data

- JFLEG (public grammar-correction dataset), `validation` split for training
- WikiText-2 sentences (Wikipedia), broken on purpose by an error generator
- 9 synthetic error types: typos, dropped letters, a/an, their/there, apostrophes...
- The JFLEG `test` split is never used for training.

## Results

Scored on the full JFLEG test set (748 sentences), GLEU, model only:

| System | GLEU |
|---|---|
| No change (baseline) | 0.7736 |
| Fine-tuned T5-small | 0.7909 |

## Examples

| Input | Output |
|---|---|
| i wnet there before | I went there before. |
| i walkad hame at night sudenly soemthign strenge happended | I walked in the night suddenly something strange happened. |
| she go to school yesterday | She went to school yesterday. |

## Install

```bash
git clone https://github.com/klinng/Grammar-Corrector.git
cd Grammar-Corrector
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

The trained model is not stored in the repo. Train it with
`python src/corrector/train.py` (a few minutes on a free Colab GPU).

## Usage

```bash
python app.py "i wnet there before"
python app.py -f input.txt -o output.txt
```

## Limitations

- `t5-small` is a small model: it has little sense of context.
- The spell-checker has no context, so `hame` can become `away` instead of `home`.
- The safety check can let through small meaning changes
  (`thier going` -> `they will go`).
- The score is for the model alone, not the full pipeline.

## Ideas for the future

- Train `t5-base` on Colab
- More real-world typo data
- Score the full pipeline, not only the model