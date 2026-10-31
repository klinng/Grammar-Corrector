import random

from corrector.targeted import (
    am_agree,
    double_comparative,
    make_targeted_pairs,
    wrong_future,
    wrong_homophone,
    wrong_since,
    wrong_suggest,
    wrong_wh_order,
)


def rng():
    return random.Random(0)


def test_double_comparative():
    assert double_comparative("She is taller than him.", rng()) == "She is more taller than him."


def test_double_superlative():
    assert double_comparative("It is the tallest tree.", rng()) == "It is the most tallest tree."


def test_since_for():
    assert wrong_since("I lived there for ten years.", rng()) == "I lived there since ten years."


def test_am_agree():
    assert am_agree("I agree with you.", rng()) == "I am agree with you."


def test_future_if():
    assert wrong_future("If it rains, we stay.", rng()) == "If it will rain, we stay."


def test_future_if_skips_auxiliaries():
    assert wrong_future("If it is late, we leave.", rng()) == "If it is late, we leave."


def test_suggest():
    out = wrong_suggest("She suggested that I take the bus.", rng())
    assert out == "She suggested me to take the bus."


def test_wh_order():
    out = wrong_wh_order("She asked me where the bank was.", rng())
    assert out == "She asked me where was the bank."


def test_homophone():
    assert wrong_homophone("Next week is busy.", rng()) == "Next weak is busy."


def test_targeted_pairs_from_templates():
    pairs = make_targeted_pairs(per_family=5, identity=1, pool=[])
    assert len(pairs) >= 7 * 5
    assert all(source.startswith("fix grammar: ") for source, _ in pairs)
