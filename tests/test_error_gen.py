import random

from corrector.error_gen import add_typo, corrupt, drop_article, drop_letter, wrong_a_an


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


def test_wrong_a_an_swaps_article():
    out = wrong_a_an("I have a apple.", random.Random(0))
    assert out == "I have an apple."


def test_drop_letter_shortens_word():
    s = "tomorrow"
    out = drop_letter(s, random.Random(0))
    assert len(out) == len(s) - 1