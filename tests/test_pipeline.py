from corrector.pipeline import clean_text, split_sentences


def test_clean_text_collapses_spaces():
    assert clean_text("  Hello    world \n again ") == "Hello world again"


def test_split_sentences():
    assert split_sentences("I run. You walk! Do we?") == ["I run.", "You walk!", "Do we?"]