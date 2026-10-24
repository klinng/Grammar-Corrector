from corrector.spell import fix_spelling


def test_correct_text_is_unchanged():
    assert fix_spelling("He walked home.") == "He walked home."


def test_typo_is_fixed():
    assert fix_spelling("He left sudenly.") == "He left suddenly."


from corrector.spell import find_ambiguous


def test_user_choice_is_applied():
    out = fix_spelling("They cuuked dinner.", {"cuuked": "cooked"})
    assert out == "They cooked dinner."


def test_correct_text_has_no_ambiguity():
    assert find_ambiguous("He walked home.") == {}