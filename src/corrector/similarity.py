import re
from difflib import SequenceMatcher


def _skeleton(word):
    return re.sub(r"[aeiou]", "a", word)


def similarity(a, b):
    """Letter similarity that forgives wrong vowels (cuuked ~ cooked)."""
    plain = SequenceMatcher(None, a, b).ratio()
    vowel_blind = SequenceMatcher(None, _skeleton(a), _skeleton(b)).ratio() * 0.95
    return max(plain, vowel_blind)