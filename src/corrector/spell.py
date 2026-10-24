import math
import re
from difflib import SequenceMatcher

# A word, optionally with an apostrophe part (don't, it's)
_WORD = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
_spell = None

# Words we never suggest automatically.
BLOCKED = {"fuck", "fucked", "fucking", "shit", "bitch", "dick", "cock"}

MIN_SIMILARITY = 0.6  # below this, a guess is too far from what was typed
AMBIGUITY_MARGIN = 0.2  # two guesses this close = we can't tell


def _get_spell():
    global _spell
    if _spell is None:
        from spellchecker import SpellChecker

        _spell = SpellChecker()
    return _spell


def _ranked_candidates(word, spell):
    """Allowed candidates as (similarity, frequency, word), best first."""
    found = spell.candidates(word) or set()
    scored = [
        (SequenceMatcher(None, word, c).ratio(), spell.word_usage_frequency(c), c)
        for c in found
        if c not in BLOCKED
    ]
    scored.sort(reverse=True)
    return scored


def _best_candidate(word, spell):
    scored = _ranked_candidates(word, spell)
    if not scored or scored[0][0] < MIN_SIMILARITY:
        return None
    return scored[0][2]


def _should_check(match, spell):
    """True for words we are allowed to treat as possible typos."""
    word = match.group(0)
    if len(word) < 3 or "'" in word:
        return False
    if match.start() > 0 and word[0].isupper():
        return False  # probably a name
    return word.lower() not in spell


def find_ambiguous(text, margin=AMBIGUITY_MARGIN, max_options=4):
    """Return {typed_word: [options]} for words we cannot decide alone."""
    spell = _get_spell()
    found = {}
    for match in _WORD.finditer(text):
        if not _should_check(match, spell):
            continue
        low = match.group(0).lower()
        if low in found:
            continue
        scored = [s for s in _ranked_candidates(low, spell) if s[0] >= MIN_SIMILARITY]
        if len(scored) >= 2 and scored[0][0] - scored[1][0] < margin:
            top = scored[0][0]
            options = [c for sim, _, c in scored if top - sim < margin]
            found[low] = options[:max_options]
    return found


def fix_spelling(text, choices=None):
    """Fix unknown words. `choices` maps a typed word to the user's pick."""
    spell = _get_spell()
    choices = choices or {}

    def fix(match):
        word = match.group(0)
        if not _should_check(match, spell):
            return word
        low = word.lower()
        best = choices.get(low) or _best_candidate(low, spell)
        if not best:
            return word
        return best.capitalize() if word[0].isupper() else best

    return _WORD.sub(fix, text)


def _candidate_words(low, spell, limit=40):
    """1-edit words first. Use 2-edit words only if the close list is thin."""
    found = {
        c
        for c in (spell.candidates(low) or set())
        if c not in BLOCKED and SequenceMatcher(None, low, c).ratio() >= 0.7
    }
    if not found and len(low) <= 12:
        wider = spell.known(spell.edit_distance_2(low))
        found |= {
            c
            for c in wider
            if c not in BLOCKED and SequenceMatcher(None, low, c).ratio() >= 0.7
        }
    return sorted(found, key=spell.word_usage_frequency, reverse=True)[:limit]


def fix_with_context(text, min_gap=2.0):
    """Choose each spelling fix using the whole sentence.

    Returns (fixed_text, unsure). `unsure` only lists real ties.
    """
    from corrector.context import sentence_score

    spell = _get_spell()
    parts = re.split(r"([A-Za-z]+(?:'[A-Za-z]+)?)", text)
    unsure = {}
    for i in range(1, len(parts), 2):
        word = parts[i]
        low = word.lower()
        if len(word) < 3 or "'" in word or low in spell:
            continue
        if word[0].isupper() and sum(len(p) for p in parts[:i]) > 0:
            continue  # probably a name
        candidates = _candidate_words(low, spell)
        if not candidates:
            continue
        if len(candidates) == 1:
            parts[i] = candidates[0].capitalize() if word[0].isupper() else candidates[0]
            continue
        scored = []
        for c in candidates:
            trial = list(parts)
            trial[i] = c.capitalize() if word[0].isupper() else c
            lm = sentence_score("".join(trial))
            prior = 0.1 * math.log(spell.word_usage_frequency(c) + 1e-9)
            closeness = 12 * SequenceMatcher(None, low, c).ratio()
            scored.append((lm + prior + closeness, c))
        scored.sort(reverse=True)
        best = scored[0][1]
        scored = []
        for c in candidates:
            trial = list(parts)
            trial[i] = c.capitalize() if word[0].isupper() else c
            lm = sentence_score("".join(trial))
            prior = 0.1 * math.log(spell.word_usage_frequency(c) + 1e-9)
            closeness = 12 * SequenceMatcher(None, low, c).ratio()
            scored.append((lm + prior + closeness, c))
        scored.sort(reverse=True)
        best = scored[0][1]
        if SequenceMatcher(None, low, best).ratio() < 0.7:
            continue
        if len(scored) > 1 and scored[0][0] - scored[1][0] < min_gap:
            unsure[low] = [c for _, c in scored[:3]]
            continue
        parts[i] = best.capitalize() if word[0].isupper() else best
    return "".join(parts), unsure