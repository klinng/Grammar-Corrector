from corrector.safety import is_safe, safe_correct


def test_small_fix_is_accepted():
    assert is_safe("I has a apple.", "I have a apple.")


def test_invented_text_is_rejected():
    original = "i walkad hame at night sudenly soemthign strenge happended"
    bad = "i walkad hame at night because at night it was happening because it happened."
    assert safe_correct(original, bad) == original