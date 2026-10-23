import random

from corrector.error_gen import add_typo, corrupt, drop_article


def test_corrupt_keeps_good_sentence():
    _bad, good = corrupt("The cat sat on the mat.", random.Random(0))
    assert good == "The cat sat on the mat."


def test_drop_article_removes_one_word():
    out = drop_article("The cat sat on the mat.", random.Random(0))
    assert len(out.split()) == 5


def test_typo_changes_word_but_not_length():
    s = "Important sentence here"
    out = add_typo(s, random.Random(1))
    assert out != s
    assert len(out) == len(s)