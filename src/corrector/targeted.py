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
        verb = _core(words[i + 3])
        if (
            verb.isalpha()
            and verb not in AUX
            and verb not in PAST_TO_BASE
            and not verb.endswith("ed")
            and not (verb.endswith("s") and not verb.endswith("ss"))
        ):
            spots.append(i)
            if not verb.endswith("ed") and not (verb.endswith("s") and not verb.endswith("ss")):
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
    if rng.random() < 0.3:
        thing = rng.choice(["exam", "meal", "lecture", "trip", "speech"])
        adj = rng.choice(["long", "hard", "expensive", "short", "loud"])
        return f"I agree that the {thing} was too {adj}."
    if rng.random() < 0.2:
        topic = rng.choice(["the budget", "the new rules", "the trip", "the schedule"])
        return f"I agree with what {name} said about {topic}."
    clause = rng.choice([
        "I agree", "we agree", "they agree", "he agrees", "she agrees",
        "I disagree", "we disagree", "they disagree", "he disagrees", "she disagrees",
    ])
    cont = rng.choice([
        "with you", "with the plan", "about the price", "that it is a good idea",
        "that the test was hard", "with the teacher", "on the date", "with the decision",
    ])
    tail = rng.choice([
        ".", ", so we can continue.", ", but it is not easy.", ", and that is final.",
        ", because it makes sense.", ", even if it costs more.",
    ])
    return f"{clause} {cont}{tail}"


def clean_future(rng):
    clause = rng.choice([
        "it rains tonight", "it snows on Sunday", "you study hard", "he calls me",
        "they arrive early", "she comes to the party", "we leave now", "you hurry",
        "he finds the key", "they win the game", "she passes the exam", "it gets colder",
        "the weather improves", "the price drops", "the shop opens early",
        "the train leaves soon", "you ask her", "we finish early", "he tells the truth",
    ])
    main = rng.choice([
        "we will cancel the picnic", "we will watch a movie", "we will play indoors",
        "we will take the bus", "we will order pizza", "I will call you", "you will be fine",
        "they will be happy", "she will help us", "we will go home", "I will tell him",
        "everyone will know", "it will be easier",
    ])
    return f"If {clause}, {main}."


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
    reporter, end = rng.choice([
        ("She asked me", "."), ("He wondered", "."), ("I forgot", "."),
        ("Can you tell me", "?"), ("Do you know", "?"), ("I don't know", "."),
        ("They asked", "."), ("I wonder", "."), ("She explained", "."),
        ("Could you tell me", "?"), ("I have no idea", "."), ("I can't remember", "."),
    ])
    place = rng.choice(PLACES)
    clause = rng.choice([
        f"where the {place} is", f"where the {place} was",
        "where my keys were", "where my phone was", "where my wallet was",
        "where my glasses were", "where my bag was", "what the time is",
        f"why the {rng.choice(['door', 'window', 'shop', 'bank'])} was open",
        f"why the {rng.choice(['door', 'window', 'shop', 'bank'])} was closed",
        "where he was", "where she is", "where they were", "where it is",
        f"when the {rng.choice(['meeting', 'concert', 'exam', 'match', 'lesson'])} was",
        f"when the {rng.choice(['meeting', 'concert', 'exam', 'match', 'lesson'])} is",
    ])
    return f"{reporter} {clause}{end}"


def clean_homophone(rng):
    name = rng.choice(NAMES)
    rel = rng.choice(["aunt", "uncle", "cousin", "grandmother", "teacher"])
    thing = rng.choice(["bag", "phone", "jacket", "book", "bike"])
    food = rng.choice(["cake", "bread", "pie", "cheese"])
    place = rng.choice(PLACES)
    city = rng.choice(CITIES)
    return rng.choice([
        f"Next week we will visit my {rel}.",
        f"Last week {name} called me.",
        f"Every week {name} goes to the {place}.",
        "This week was very busy at work.",
        "We had a weak signal in the mountains.",
        "I can hear the music from here.",
        f"Can you hear {name} from the {place}?",
        "She didn't know the answer to the question.",
        f"I know {name} from school.",
        f"He bought a new {thing} yesterday.",
        f"I bought a new {thing} at the {place}.",
        f"We will meet at the {place} at noon.",
        f"{name} and I will meet after class.",
        f"I would like a piece of {food}.",
        f"Cut a piece of {food} for {name}.",
        "The whole family was at home.",
        f"I read the whole {thing} in one night.",
        "We walked along the sea after lunch.",
        f"She lives near the sea in {city}.",
        "Please wait here for a moment.",
        f"Wait for {name} at the {place}.",
        f"The weight of the {thing} was too much.",
        "We hope for peace in the whole world.",
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
        chosen = []
        seen = set()
        for item in mined:
            if item not in seen and len(chosen) < per_family // 2:
                seen.add(item)
                chosen.append(item)
        tries = 0
        while len(chosen) < per_family and tries < per_family * 30:
            tries += 1
            clean = make_clean(rng)
            item = (func(clean, rng), clean)
            if item[0] != clean and item not in seen:
                seen.add(item)
                chosen.append(item)
        for _ in range(identity):
            clean = make_clean(rng)
            if (clean, clean) not in seen:
                seen.add((clean, clean))
                chosen.append((clean, clean))
        pairs.extend((PREFIX + bad, good) for bad, good in chosen)
    return pairs
