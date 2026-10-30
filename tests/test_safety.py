from corrector.safety import is_safe, revert_wild_words, safe_correct


def test_small_fix_is_accepted():
    assert is_safe("I has a apple.", "I have a apple.")


def test_invented_text_is_rejected():
    original = "i walkad hame at night sudenly soemthign strenge happended"
    bad = "i walkad hame at night because at night it was happening because it happened."
    assert safe_correct(original, bad) == original


def test_wild_word_is_reverted():
    original = "they decided to cuuked a masive dinr today"
    corrected = "they decided to cuddle a massive drink today"
    out = revert_wild_words(original, corrected)
    assert "cuuked" in out and "dinr" in out
    assert "massive" in out


def test_good_fix_is_kept():
    assert revert_wild_words("she wos here", "she was here") == "she was here"


def test_real_word_fix_is_kept():
    out = revert_wild_words("he have two", "he has two", is_known=lambda w: True)
    assert out == "he has two"