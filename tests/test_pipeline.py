from corrector.pipeline import (
    clean_text,
    restore_commas,
    split_sentences,
    tidy_punctuation,
)


def test_clean_text_collapses_spaces():
    assert clean_text("  Hello    world \n again ") == "Hello world again"


def test_split_sentences():
    assert split_sentences("I run. You walk! Do we?") == ["I run.", "You walk!", "Do we?"]


def test_tidy_punctuation():
    assert tidy_punctuation("Yesterday , we left .") == "Yesterday, we left."


def test_restore_commas():
    out = restore_commas("It rains, so we stay.", "It rains so we stay.")
    assert out == "It rains, so we stay."
