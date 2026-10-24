from difflib import SequenceMatcher


def is_safe(original, corrected, min_similarity=0.6, max_length_ratio=1.5):
    """Accept a correction only if it stays close to the original."""
    if not corrected.strip():
        return False
    similarity = SequenceMatcher(None, original.lower(), corrected.lower()).ratio()
    length_ratio = len(corrected) / max(len(original), 1)
    return similarity >= min_similarity and length_ratio <= max_length_ratio


def safe_correct(original, corrected):
    return corrected if is_safe(original, corrected) else original