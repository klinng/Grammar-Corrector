# Grammar Corrector

A grammar and spelling corrector I trained myself: **FLAN-T5-base fine-tuned on public data plus a synthetic error generator**, wrapped in a pipeline with a context-aware spell step and safety checks. No private data is used.

## Results

JFLEG test set, 748 sentences never used for training, GLEU score, model only:

| System | GLEU |
|---|---|
| No change (baseline) | 0.7736 |
| T5-small, fine-tuned here | 0.7969 |
| **FLAN-T5-base, fine-tuned here** | **0.8288** |
| FLAN-T5-base + targeted grammar data | 0.8276 (same, within run-to-run noise) |

My own messy-text test: 25 paragraphs with reference answers (`examples/messy.txt` and `examples/gold.txt`), full pipeline, GLEU:

| System | GLEU |
|---|---|
| No change (baseline) | 0.355 |
| T5-small pipeline | 0.663 |
| FLAN-T5-base pipeline | 0.708 |
| **+ targeted grammar data** | **0.715** |

The first 5 paragraphs were used while tuning, and 25 paragraphs is a small sample, so differences of about 0.02 are within noise. The JFLEG numbers are the more reliable ones.

### Held-out test (third set)

20 paragraphs (`examples/messy_fresh2.txt`, `examples/gold_fresh2.txt`) that were not used to design generators or tune anything. I checked that no training template reproduces them. Full pipeline, GLEU:

| Model | GLEU |
|---|---|
| No change (baseline) | 0.620 |--fresh2` |
| FLAN-T5-base, before the targeted grammar data | 0.794 |
| **FLAN-T5-base + targeted grammar data** | **0.948** |

Caveats: I wrote this set around the same grammar families the new generators target, so it shows the model learned those patterns on new sentences, not that it handles all real writing. It is also only 20 paragraphs, and I have since looked at its failures, so it is no longer a clean test. A fourth set is needed for the next round.

Run the comparison yourself:

```bash
python compare.py            # first 25 paragraphs
python compare.py --fresh2   # held-out set
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
| 12 | Restore commas the model drops | second paragraph set 0.849 -> 0.870; first set and JFLEG unchanged | kept |
| 13 | Targeted grammar generators (double comparatives, `since`/`for`, `I am agree`, `if ... will`, `suggested me to`, embedded-question word order, homophones), built from mined real sentences and templates, then retrain | held-out set 0.794 -> **0.948**; JFLEG 0.8290 -> 0.8276 and first set 0.708 -> 0.715 (no regression) | kept |

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

Held-out set, after the targeted grammar data:

| Mode | GLEU |
|---|---|
| Full pipeline (spell + model + safety) | **0.948** |
| Spell + model, no safety checks | **0.948** |
| Model only | 0.927 |
| Model + safety, no spell | 0.916 |

The spell step helps on every set. Before experiment 10 the safety check cost points on messy text, because it judged words by letter similarity and undid fixes like `have` -> `has`. Now it only reverts a word that is not a real word, so it blocks invented replacements (`cuddle`, `drink`, `pick`) without hurting grammar fixes. The 25-paragraph set is small, so differences under about 0.02 are within noise.

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
- Targeted grammar pairs for seven families that the general generator rarely produced (double comparatives, `since`/`for`, `I am agree`, `if ... will`, `suggested me to`, word order in embedded questions, homophones). They are mined from real sentences and built from templates, with unchanged sentences mixed in so correct text is left alone, and they are added on top of the 20,000-pair cap.
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
- Remaining errors on the held-out set (5 of 20 paragraphs): tense with a duration (`are waiting ... for two hours` instead of `have been waiting`), simple past versus participle (`eated` -> `eaten`, `have forgot`), and lowercase proper adjectives (`spanish`).
- Running the model on a CPU is slow with the base-size model.

## Roadmap

1. A fourth held-out set, written before the next round of generators.
2. A second round of targeted generators: irregular past versus participle (`have forgot`, `eated`), lowercase proper nouns and adjectives (`spanish`, `monday`), and present perfect with durations.
3. A guard so the spell step skips wrong irregular verbs (`goed`, `swimed`) and leaves them to the model.
4. Real learner data (for example BEA-2019, after checking its license).
