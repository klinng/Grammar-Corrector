import random

from corrector.error_gen import (
    add_typo,
    corrupt,
    drop_apostrophe,
    drop_article,
    drop_letter,
    drop_plural,
    lowercase_start,
    wrong_a_an,
    wrong_agreement,
    wrong_conjugation,
    wrong_did,
    wrong_verb_form,
)


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


def test_lowercase_start():
    assert lowercase_start("I went home.", random.Random(0)) == "i went home."


def test_drop_apostrophe():
    assert drop_apostrophe("Don't go.", random.Random(0)) == "Dont go."

def test_wrong_verb_form():
    assert wrong_verb_form("I want to cook now.", random.Random(0)) == "I want to cooked now."


def test_wrong_agreement():
    assert wrong_agreement("They were here.", random.Random(0)) == "They was here."


def test_wrong_did():
    assert wrong_did("She did go home.", random.Random(0)) == "She did goed home."


def test_drop_plural():
    assert drop_plural("Cats sleep.", random.Random(0)) == "Cat sleep."

def test_wrong_conjugation():
    out = wrong_conjugation("She went home.", random.Random(0))
    assert out in {"She goed home.", "She go home."}