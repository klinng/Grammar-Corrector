import re
from difflib import SequenceMatcher

from corrector.similarity import similarity


def is_safe(original, corrected, min_similarity=0.6, max_length_ratio=1.5):
    """Accept a correction only if it stays close to the original."""
    if not corrected.strip():
        return False
    similarity = SequenceMatcher(None, original.lower(), corrected.lower()).ratio()
    length_ratio = len(corrected) / max(len(original), 1)
    return similarity >= min_similarity and length_ratio <= max_length_ratio


def revert_wild_words(original, corrected, min_similarity=0.7):
    """If a word was replaced by a very different word, put the original back.

    Only works when both texts have the same number of words.
    """
    orig = original.split()
    new = corrected.split()
    if len(orig) != len(new):
        return corrected
    out = []
    for o, n in zip(orig, new):
        o_core = re.sub(r"\W", "", o).lower()
        n_core = re.sub(r"\W", "", n).lower()
        wild = (
            len(o_core) >= 4
            and n_core
            and o_core != n_core
            and similarity(o_core, n_core) < min_similarity
        )
        out.append(o if wild else n)
    return " ".join(out)


def safe_correct(original, corrected):
    if not is_safe(original, corrected):
        return original
    return revert_wild_words(original, corrected)