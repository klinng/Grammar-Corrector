"""Targeted grammar errors: generators, template sentences and mining for training."""

import random

from corrector.error_gen import PAST_TO_BASE

_PUNCT = ".,!?;:\"'()"

AUX = {
    "will", "would", "can", "could", "shall", "should", "may", "might", "must",
    "is", "are", "was", "were", "am", "be", "been", "being", "have", "has", "had",
    "do", "does", "did", "not", "don't", "doesn't", "didn't", "isn't", "aren't",
    "wasn't", "weren't", "won't", "can't", "couldn't", "wouldn't", "shouldn't",
    "haven't", "hasn't", "hadn't", "also", "never", "always", "just", "still",
    "even", "only", "really", "already", "often", "usually", "ever",
}
SUBJECTS = {"i", "you", "we", "they", "he", "she", "it"}
DETS = {"the", "my", "our", "his", "her", "their", "this", "that"}

COMPARATIVES = [
    "bigger", "smaller", "taller", "shorter", "faster", "slower", "smarter", "stronger",
    "weaker", "older", "younger", "longer", "harder", "easier", "cheaper", "richer",
    "poorer", "darker", "lighter", "colder", "warmer", "hotter", "cooler", "louder",
    "quieter", "nicer", "safer", "larger", "higher", "lower", "newer", "closer",
    "deeper", "wider", "narrower", "simpler", "happier", "heavier", "busier",
    "cleaner", "kinder", "braver", "prettier", "funnier", "healthier", "tougher",
]
SUPERLATIVES = [
    "biggest", "smallest", "tallest", "shortest", "fastest", "slowest", "smartest",
    "strongest", "weakest", "oldest", "youngest", "longest", "hardest", "easiest",
    "cheapest", "richest", "poorest", "darkest", "coldest", "warmest", "hottest",
    "coolest", "loudest", "nicest", "safest", "largest", "highest", "lowest",
    "newest", "closest", "deepest", "widest", "simplest", "happiest", "heaviest",
    "busiest", "cleanest", "kindest", "bravest", "prettiest", "funniest",
    "healthiest", "toughest",
]
_COMP = set(COMPARATIVES)
_SUP = set(SUPERLATIVES)

NUMBERS = {
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "eleven", "twelve", "fifteen", "twenty", "thirty", "several", "a", "an",
}
UNITS = {"year", "years", "month", "months", "week", "weeks", "day", "days", "hour", "hours"}
BE_FORM = {"i": "am", "you": "are", "we": "are", "they": "are", "he": "is", "she": "is"}
AGREE = {"agree": "agree", "agrees": "agree", "disagree": "disagree", "disagrees": "disagree"}
OBJECT = {"i": "me", "we": "us", "he": "him", "she": "her", "they": "them", "you": "you"}
SUGGEST = {"suggested", "suggests", "suggest", "recommended", "recommends", "recommend"}
WH = {"where", "what", "when", "why", "how"}
BE_VERBS = {"was", "is", "were", "are"}
REPORT = {
    "asked", "ask", "asking", "know", "knew", "wonder", "wondered", "wondering", "tell",
    "told", "understand", "remember", "remembered", "forgot", "explain", "explained",
    "see", "saw", "show", "showed", "guess", "idea",
}
HOMOPHONES = {
    "week": "weak", "weak": "week", "hear": "here", "here": "hear", "know": "no",
    "no": "know", "new": "knew", "knew": "new", "buy": "by", "meet": "meat",
    "meat": "meet", "piece": "peace", "peace": "piece", "wait": "weight",
    "weight": "wait", "sea": "see", "whole": "hole", "hole": "whole",
}


def _swap(raw, new):
    """Replace the word inside raw, keeping punctuation and a leading capital."""
    core = raw.strip(_PUNCT)
    if not core:
        return raw
    start = raw.index(core)
    head, tail = raw[:start], raw[start + len(core):]
    if core[:1].isupper():
        new = new[:1].upper() + new[1:]
    return head + new + tail


def _core(word):
    return word.strip(_PUNCT).lower()


def double_comparative(sentence, rng):
    """taller -> more taller, tallest -> most tallest."""
    words = sentence.split()
    spots = []
    for i, w in enumerate(words):
        prev = _core(words[i - 1]) if i else ""
        if prev in {"more", "most", "less", "least"}:
            continue
        if _core(w) in _COMP or _core(w) in _SUP:
            spots.append(i)
    if not spots:
        return sentence
    i = rng.choice(spots)
    core = _core(words[i])
    words[i] = _swap(words[i], ("more " if core in _COMP else "most ") + core)
    return " ".join(words)


def wrong_since(sentence, rng):
    """for ten years -> since ten years."""
    words = sentence.split()
    spots = [
        i
        for i in range(len(words) - 2)
        if words[i].lower() == "for"
        and (_core(words[i + 1]) in NUMBERS or words[i + 1].isdigit())
        and _core(words[i + 2]) in UNITS
    ]
    if not spots:
        return sentence
    i = rng.choice(spots)
    words[i] = _swap(words[i], "since")
    return " ".join(words)


def am_agree(sentence, rng):
    """I agree -> I am agree."""
    words = sentence.split()
    spots = [
        i
        for i in range(len(words) - 1)
        if words[i].lower() in BE_FORM and _core(words[i + 1]) in AGREE
    ]
    if not spots:
        return sentence
    i = rng.choice(spots)
    be = BE_FORM[words[i].lower()]
    words[i + 1] = _swap(words[i + 1], AGREE[_core(words[i + 1])])
    words[i] = words[i] + " " + be
    return " ".join(words)


def _present_base(word, singular):
    low = _core(word)
    if not low.isalpha() or low in AUX or low in PAST_TO_BASE or low.endswith("ed"):
        return None
    if singular:
        if low.endswith(("oes", "ches", "shes", "sses", "xes", "zes")):
            return low[:-2]
        if low.endswith("ies"):
            return low[:-3] + "y"
        if low.endswith("s") and not low.endswith("ss"):
            return low[:-1]
        return None
    return None if low.endswith("s") and not low.endswith("ss") else low


def wrong_future(sentence, rng):
    """If it rains -> If it will rain."""
    words = sentence.split()
    spots = []
    for i, w in enumerate(words):
        if w.lower() != "if" or (i and _core(words[i - 1]) in {"as", "what"}):
            continue
        j = i + 1
        if j + 1 < len(words) and words[j].lower() in SUBJECTS:
            singular, vi = words[j].lower() in {"he", "she", "it"}, j + 1
        elif j + 2 < len(words) and words[j].lower() in DETS:
            singular, vi = True, j + 2
        else:
            continue
        base = _present_base(words[vi], singular)
        if base:
            spots.append((vi, base))
    if not spots:
        return sentence
    vi, base = rng.choice(spots)
    raw = words[vi]
    core = raw.strip(_PUNCT)
    start = raw.index(core)
    words[vi] = raw[:start] + "will " + base + raw[start + len(core):]
    return " ".join(words)


def wrong_suggest(sentence, rng):
    """suggested that I take -> suggested me to take."""
    words = sentence.split()
    spots = []
    for i in range(len(words) - 3):
        if _core(words[i]) not in SUGGEST or _core(words[i + 1]) != "that":
            continue
        if words[i + 2].lower() not in OBJECT:
            continue
        verb = _core(words[i + 3])
        if (
            verb.isalpha() 
            and verb not in AUX 
            and verb not in PAST_TO_BASE
            and not verb.endswith('ed') 
            and not verb.endswith('s') 
            and not verb.endswith('ss')
        ):
            spots.append(i)

    if not spots:
        return sentence
    i = rng.choice(spots)
    words[i + 1:i + 3] = [OBJECT[words[i + 2].lower()], "to"]
    return " ".join(words)


def wrong_wh_order(sentence, rng):
    """where the station was -> where was the station (in an embedded question)."""
    words = sentence.split()
    spots = []
    for i, w in enumerate(words):
        if _core(w) not in WH or not any(_core(p) in REPORT for p in words[max(0, i - 3):i]):
            continue
        if (
            i + 3 < len(words) 
            and _core(words[i + 1]) in (DETS | {"a", "an"})
            and words[i + 2].isalpha() 
            and _core(words[i + 3]) in BE_VERBS
        ):
            spots.append(("noun", i))


        if (
            i + 2 < len(words) 
            and _core(words[i + 1]) in SUBJECTS
            and _core(words[i + 2]) in BE_VERBS
        ):
            spots.append(("pron", i))

    if not spots:
        return sentence
    kind, i = rng.choice(spots)
    n = 3 if kind == "noun" else 2
    be_raw = words[i + n]
    be = be_raw.strip(_PUNCT)
    tail = be_raw[len(be_raw.rstrip(_PUNCT)):]
    moved = words[i + 1:i + n]
    moved[-1] = moved[-1] + tail
    words[i + 1:i + n + 1] = [be] + moved
    return " ".join(words)


def wrong_homophone(sentence, rng):
    """week -> weak, know -> no (real words that sound alike)."""
    words = sentence.split()
    spots = [i for i, w in enumerate(words) if _core(w) in HOMOPHONES]
    if not spots:
        return sentence
    i = rng.choice(spots)
    words[i] = _swap(words[i], HOMOPHONES[_core(words[i])])
    return " ".join(words)


NAMES = ["Tom", "Anna", "Maria", "Ahmed", "Lina", "Karim", "Sara", "John", "Emma", "Omar"]
CITIES = ["Paris", "London", "Tunis", "Madrid", "Rome", "Berlin", "Lisbon"]
PLACES = ["bank", "library", "market", "hospital", "pharmacy", "museum", "airport", "school"]


def clean_comparative(rng):
    name = rng.choice(NAMES)
    if rng.random() < 0.5:
        comp = rng.choice(COMPARATIVES)
        other = rng.choice(["his brother", "her cousin", "their neighbor", "the others"])
        return rng.choice([
            f"{name} is {comp} than {other}.",
            f"My neighbor's house is {comp} than ours.",
            f"The new model is {comp} than the old one.",
            f"This road is {comp} than the one we took yesterday.",
        ])
    sup = rng.choice(SUPERLATIVES)
    thing = rng.choice(["building", "bridge", "tree", "hill", "tower", "shop"])
    where = rng.choice(["city", "town", "country", "village"])
    return rng.choice([
        f"This is the {sup} {thing} in the {where}.",
        f"{name} is the {sup} person I know.",
        f"It was the {sup} day of the whole year.",
    ])


def clean_since(rng):
    n = rng.choice(["two", "three", "four", "five", "six", "seven", "ten", "twelve"])
    unit = rng.choice(["years", "months", "weeks", "days", "hours"])
    return rng.choice([
        f"I have lived in {rng.choice(CITIES)} for {n} {unit}.",
        f"{rng.choice(NAMES)} has worked at the {rng.choice(PLACES)} for {n} {unit}.",
        f"They have been friends for {n} {unit}.",
        f"We have waited for {n} {unit} without any news.",
        f"She has studied English for {n} {unit}.",
    ])


def clean_agree(rng):
    name = rng.choice(NAMES)
    thing = rng.choice(["exam", "meal", "lecture", "trip", "speech"])
    adj = rng.choice(["long", "hard", "expensive", "short", "loud"])
    topic = rng.choice(["the budget", "the new rules", "the trip", "the schedule"])
    return rng.choice([
        f"I agree that the {thing} was too {adj}.",
        f"I agree with what {name} said about {topic}.",
        "We agree on the price, so we can sign the contract.",
        "They disagree about the plan, but they respect each other.",
        "He agrees with the teacher, and she agrees too.",
        "I disagree with the decision, but I will follow it.",
    ])


def clean_future(rng):
    when = rng.choice(["tonight", "on Sunday", "this weekend", "later today", "next month"])
    plan = rng.choice([
        "cancel the picnic", "watch a movie", "play indoors", "take the bus", "order pizza",
    ])
    return rng.choice([
        f"If it rains {when}, we will {plan}.",
        "If you study hard, you will pass the exam.",
        "If he calls me, I will tell him the news.",
        "If they arrive early, we will start the meeting sooner.",
        "If the weather improves, the match will start at noon.",
        "If she comes to the party, I will introduce her to my friends.",
        "If the price drops, we will buy two.",
    ])


def clean_suggest(rng):
    subject = rng.choice([
        "My teacher", "The doctor", "My friend", "Her father", "Our manager", "My sister",
    ])
    verb = rng.choice(["suggested", "recommended"])
    pron = rng.choice(["I", "we", "he", "she", "they"])
    action = rng.choice([
        "take the bus", "call a doctor", "read the book", "visit the museum",
        "try the soup", "wait until Monday", "check the schedule",
    ])
    return f"{subject} {verb} that {pron} {action}."


def clean_wh(rng):
    place = rng.choice(PLACES)
    thing = rng.choice(["door", "window", "shop", "bank"])
    return rng.choice([
        f"She asked me where the {place} was.",
        "I forgot where my keys were.",
        "Can you tell me what the time is?",
        f"He wondered why the {thing} was open.",
        "I don't know where he was last night.",
        "Do you know where she is?",
    ])


def clean_homophone(rng):
    rel = rng.choice(["aunt", "uncle", "cousin", "grandmother", "teacher"])
    thing = rng.choice(["bag", "phone", "jacket", "book", "bike"])
    food = rng.choice(["cake", "bread", "pie", "cheese"])
    place = rng.choice(PLACES)
    return rng.choice([
        f"Next week we will visit my {rel}.",
        "This week was very busy at work.",
        "I can hear the music from here.",
        "She didn't know the answer to the question.",
        f"He bought a new {thing} yesterday.",
        f"We will meet at the {place} at noon.",
        f"I would like a piece of {food}.",
        "The whole family was at home.",
        "We walked along the sea after lunch.",
        "Please wait here for a moment.",
    ])


FAMILIES = {
    "double_comparative": (double_comparative, clean_comparative),
    "since_for": (wrong_since, clean_since),
    "am_agree": (am_agree, clean_agree),
    "future_if": (wrong_future, clean_future),
    "suggest_me": (wrong_suggest, clean_suggest),
    "wh_order": (wrong_wh_order, clean_wh),
    "homophone": (wrong_homophone, clean_homophone),
}


def _mine_pool(wiki_max=40000):
    """Clean sentences from WikiText and the JFLEG corrections."""
    from corrector.data_prep import load_clean_sentences, load_jfleg

    pool = list(load_clean_sentences(max_sentences=wiki_max))
    for row in load_jfleg()["validation"]:
        pool.extend(c.strip() for c in row["corrections"] if c.strip())
    return pool


def make_targeted_pairs(per_family=300, identity=40, seed=0, pool=None):
    """(bad, good) pairs for each grammar family, mined and built from templates.

    Pass pool=[] to use templates only.
    """
    from corrector.data_prep import PREFIX

    rng = random.Random(seed)
    if pool is None:
        pool = _mine_pool()
    pairs = []
    for func, make_clean in FAMILIES.values():
        mined = []
        for sentence in pool:
            bad = func(sentence, rng)
            if bad != sentence:
                mined.append((bad, sentence))
        rng.shuffle(mined)
        chosen = mined[: per_family // 2]
        tries = 0
        while len(chosen) < per_family and tries < per_family * 30:
            tries += 1
            clean = make_clean(rng)
            bad = func(clean, rng)
            if bad != clean:
                chosen.append((bad, clean))
        for _ in range(identity):
            clean = make_clean(rng)
            chosen.append((clean, clean))
        pairs.extend((PREFIX + bad, good) for bad, good in chosen)
    return pairs
