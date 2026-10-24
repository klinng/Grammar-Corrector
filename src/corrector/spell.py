import re

# A word, optionally with an apostrophe part (don't, it's)
_WORD = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
_spell = None


def _get_spell():
    global _spell
    if _spell is None:
        from spellchecker import SpellChecker

        _spell = SpellChecker()
    return _spell


def fix_spelling(text):
    """Fix words that are not in the dictionary. Leave everything else alone."""
    spell = _get_spell()

    def fix(match):
        word = match.group(0)
        if len(word) < 3 or "'" in word:
            return word
        if match.start() > 0 and word[0].isupper():
            return word  # probably a name, skip it
        if word.lower() in spell:
            return word
        best = spell.correction(word.lower())
        if not best:
            return word
        return best.capitalize() if word[0].isupper() else best

    return _WORD.sub(fix, text)