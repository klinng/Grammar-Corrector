# Grammar Corrector

A grammar and spelling corrector built by fine-tuning **T5-small** on public data and synthetic errors. No private data is used. It has a light mode that runs on a laptop, and a smart mode (an instruction model on Colab) for very messy text.

## How it works

Grammar correction is treated as a sequence-to-sequence task: a noisy sentence goes in, a corrected sentence comes out.

```
text -> cleaner -> sentence splitter -> context spell-check -> T5 model -> safety checks -> merger
```

| Step | What it does |
|---|---|
| Cleaner / splitter | Normalizes spaces and cuts the text into sentences (regex) |
| Context spell-check | `pyspellchecker` proposes candidates, `distilgpt2` picks the one that fits the sentence |
| T5-small | Fine-tuned for grammar, tense, capitals and punctuation |
| Safety checks | Reject a rewrite that drifts too far, and put back words T5 replaced with very different ones |

The language model scores a sentence as `P(w1..wn) = product of P(wi | w1..wi-1)`. T5 uses subword tokenization, so misspelled words are split into pieces instead of crashing the model.

## Data

- **JFLEG** (public grammar-correction dataset): the `validation` split is used for training.
- **WikiText-2**: clean Wikipedia sentences, broken on purpose by an error generator.
- **Error generator:** 13 error types (typos, dropped and doubled letters, a/an, their/there, apostrophes, lowercase start, verb forms after `to` and `did`, subject-verb agreement, plurals), with 1 to 4 errors per sentence.
- The JFLEG `test` split is **never** used for training.

## Results

Scored on the full JFLEG test set (748 sentences), GLEU, **T5 model only** (without the spell-check and safety steps):

| System | GLEU |
|---|---|
| No change (baseline) | 0.7736 |
| Fine-tuned T5-small | 0.7933 |

## Examples

| Input | Output |
|---|---|
| i wnet there before | I went there before. |
| Because they were very hungry, they decided to cuuked a masive dinr on the sidewalk. | Because they were very hungry, they decided to cook a massive dinner on the sidewalk. |

Very messy text (spelled by sound, 40+ errors):

| Mode | Result |
|---|---|
| Input | `Mi frend Jon, wich are normaly veri bravest, comed to runen awai bekaus he wer so much skared of the animles.` |
| Light mode (T5-small) | `Mi friend Jon, which is normal very brave, comes to run away beaus he wears so much scared of the animes.` |
| Smart mode (Qwen2.5-3B) | `My friend Jon, who is usually very brave, ran away because he was so scared of the animal.` |

## Install

```bash
git clone https://github.com/klinng/Grammar-Corrector.git
cd Grammar-Corrector
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

The trained model is not stored in the repo. Train it with `python src/corrector/train.py`, or on a free Colab GPU with `notebooks/colab_train.ipynb` (about 3 minutes), then unzip the result so you get `models/t5-small-gec`.

## Usage

```bash
python app.py "i wnet there before"
python app.py -f input.txt -o output.txt
streamlit run web.py
```

## Smart mode

`notebooks/smart_mode.ipynb` runs **Qwen2.5-3B-Instruct** on a free Colab T4 GPU, with two prompts: *fix* (keep the meaning and sentences) and *rewrite* (more natural wording). It needs about 7 GB of GPU memory, so it does not run on a small laptop.

## Tests and CI

- 22 tests with `pytest`, style checked with `ruff`.
- GitHub Actions runs both on every push and pull request.

## Limitations

- T5-small is a small model. It has little sense of context and can invent words for badly damaged text.
- The spell-checker compares letters, so heavily misspelled words (`woz`, `bekaus`) are hard for light mode.
- The safety checks prefer leaving a typo over inventing a word.
- The score covers the T5 model alone, not the full pipeline.
- Smart mode can change meaning slightly, so *fix* should be the default.

## Ideas for the future

- Score the full pipeline, not only the model
- Train `t5-base` on Colab, with real learner data (for example BEA-2019)
- A web page with *Fix* and *Rewrite* buttons backed by a hosted model
- Research idea, not implemented: quantum NLP (for example with `lambeq`), as a separate learning experiment
