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
| **FLAN-T5-base pipeline** | **0.708** |

The first 5 paragraphs were used while tuning, and 25 paragraphs is a small sample, so differences of about 0.02 are within noise. The JFLEG numbers are the more reliable ones.

Run the comparison yourself:

```bash
python compare.py
```

It scores three modes (full pipeline, model + safety checks, model only) against the reference answers and writes every output to `examples/results.md`.

## Experiments

Every change was measured before it was kept. JFLEG scores are on the 748-sentence test set, the messy score is on my 25-paragraph set (reference-based GLEU).

| # | Change | Result | Decision |
|---|---|---|---|
| 1 | Synthetic errors added to training | small gain (about +0.004 on a 200-sentence check) | kept |
| 2 | Heavier typos (1 to 4 errors) and grammar errors, 8,000 pairs | JFLEG 0.7909 -> 0.7933 | kept |
| 3 | Conjugation, confusable-word and sound-spelling errors, 20,000 pairs | JFLEG 0.7933 -> 0.7969 | kept |
| 4 | Context-aware spell step (language model picks the candidate) | fixed cases like `cuuked ... dinr` by sentence meaning | kept |
| 5 | Per-word safety check (revert words the model changed too much) | stopped invented words (`cuddle`, `drink`), but it also undid good grammar fixes (see 9 and 10) | replaced by 10 |
| 6 | Run the model before the spell step | messy GLEU 0.411 vs 0.435 (5 paragraphs) | rejected |
| 7 | Local Ollama (Qwen) as an extra mode | worked well, but it is not my model | removed, used only to compare |
| 8 | FLAN-T5-base instead of T5-small | JFLEG 0.7969 -> **0.8288**, messy 0.663 -> **0.687** | kept |
| 9 | Ablation of the pipeline steps (tables below) | spell step helps; the safety check cost 0.02 on messy text | led to 10 |
| 10 | Safety check never reverts real words (only typos can be reverted) | messy 0.687 -> **0.708**; JFLEG pipeline (150 sentences) 0.8379 -> 0.8387 | kept |
| 11 | Remove spaces before punctuation in the output | no score change (GLEU splits punctuation), cleaner text | kept |

### Pipeline ablation (FLAN-T5-base)

My 25 messy paragraphs (current code):

| Mode | GLEU |
|---|---|
| No change | 0.355 |
| Full pipeline (spell + model + safety) | **0.708** |
| Spell + model, no safety checks | **0.708** |
| Model only | 0.664 |
| Model + safety, no spell | 0.645 |

JFLEG test set, first 150 sentences (`python score_pipeline.py -n 150`):

| Mode | GLEU |
|---|---|
| No change | 0.7483 |
| Model only | 0.8332 |
| Model + safety, no spell | 0.8336 |
| Spell + model, no safety checks | 0.8383 |
| **Full pipeline** | **0.8387** |

The spell step helps on both sets. Before experiment 10 the safety check cost points on messy text, because it judged words by letter similarity and undid fixes like `have` -> `has`. Now it only reverts a word that is not a real word, so it blocks invented replacements (`cuddle`, `drink`, `pick`) without hurting grammar fixes. The 25-paragraph set is small, so differences under about 0.02 are within noise.

## How it works

```
text -> cleaner -> sentence splitter -> context spell-check -> T5 model -> safety checks -> merger
```

- **Context spell-check:** `pyspellchecker` proposes candidates and `distilgpt2` picks the one that fits the sentence.
- **Model:** a pretrained FLAN-T5-base, fine-tuned here for grammar, tense, vocabulary and punctuation.
- **Safety checks:** reject a rewrite that drifts too far, and put back a misspelled word that the model replaced with a very different one. Real words are never reverted, so grammar fixes survive. A typo left alone is better than an invented word.

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

1. A fresh held-out messy test set (`examples/messy_fresh.txt`), scored with `python compare.py --fresh`.
2. Error generators for grammar the model has not seen: double comparatives (`more taller`), `since`/`for`, `I am agree`, adjective for adverb (`rain hardly`), wrong conditionals. Then retrain and measure on the fresh set.
3. A guard so the spell step skips wrong irregular verbs (`goed`, `swimed`) and leaves them to the model.
4. Real learner data (for example BEA-2019, after checking its license).
