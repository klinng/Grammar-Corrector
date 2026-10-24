from corrector.spell import fix_spelling


def test_correct_text_is_unchanged():
    assert fix_spelling("He walked home.") == "He walked home."


def test_typo_is_fixed():
    assert fix_spelling("He left sudenly.") == "He left suddenly."