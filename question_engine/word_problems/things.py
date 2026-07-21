"""Classroom / math-friendly thing bank and selection for word problems.

Mirrors ``names.py`` letter-then-item sampling:

  1. Choose a letter that has things in the bank.
  2. Choose a random plural noun from that letter's list.

When multiple things are needed, default to distinct starting letters
(and distinct nouns) so the items are easy to tell apart. Callers can
prefer the same first letter (still distinct nouns) for harder prompts.
"""

from __future__ import annotations

import random
from typing import Sequence

# Continuous D at/above this unlocks same-first-letter pairs (extra confusion).
SAME_LETTER_MIN_DIFFICULTY = 20.0

# Plural classroom / snack / school-supply nouns; Q/X/Z keep short lists.
THINGS_BY_LETTER: dict[str, tuple[str, ...]] = {
    "A": ("apples", "aprons", "atlases", "arrows"),
    "B": ("binders", "books", "balloons", "beads", "badges"),
    "C": ("cookies", "crayons", "cups", "cards", "clips"),
    "D": ("dice", "donuts", "dollars", "dominoes"),
    "E": ("erasers", "envelopes", "earrings"),
    "F": ("folders", "flags", "figs", "frames"),
    "G": ("grapes", "goggles", "gliders", "games"),
    "H": ("hats", "highlighters", "hooks", "hoops"),
    "I": ("invitations", "instruments", "inboxes"),
    "J": ("jars", "journals", "jackets"),
    "K": ("keys", "kits", "kites", "knobs"),
    "L": ("labels", "lollipops", "locks", "lanterns"),
    "M": ("markers", "marbles", "magnets", "mugs"),
    "N": ("notebooks", "napkins", "nails", "necklaces"),
    "O": ("oranges", "olives", "owls"),
    "P": ("pencils", "pens", "paperclips", "posters", "pins"),
    "Q": ("quilts", "quarters", "quills"),
    "R": ("rulers", "ribbons", "rocks", "rings"),
    "S": ("stickers", "stamps", "staples", "spoons"),
    "T": ("tickets", "tokens", "toys", "tapes"),
    "U": ("umbrellas", "uniforms"),
    "V": ("vases", "visors", "vouchers"),
    "W": ("worksheets", "watches", "wallets", "whistles"),
    "X": ("xylophones",),
    "Y": ("yo-yos", "yarns"),
    "Z": ("zippers", "ziplocks"),
}


def letters_with_things() -> tuple[str, ...]:
    """Letters that have at least one thing in the bank."""
    return tuple(THINGS_BY_LETTER.keys())


def things_for_letter(letter: str) -> tuple[str, ...]:
    """Return things for ``letter`` (case-insensitive). Empty if unknown."""
    return THINGS_BY_LETTER.get(letter.upper(), ())


def first_letter(thing: str) -> str:
    """Uppercase first alphabetic character of ``thing`` (fallback: first char)."""
    for ch in thing:
        if ch.isalpha():
            return ch.upper()
    return thing[:1].upper() if thing else ""


def pick_things(
    count: int = 1,
    *,
    rng: random.Random | None = None,
    exclude: Sequence[str] | None = None,
    prefer_same_first_letter: bool = False,
) -> list[str]:
    """Pick ``count`` plural nouns via letter-then-thing sampling.

    Default: prefer distinct starting letters, then distinct nouns.
    When ``prefer_same_first_letter`` is True, later picks prefer the first
    item's letter when that letter still has unused nouns; otherwise fall
    back to distinct letters. Never returns the same noun twice when the
    bank has enough distinct entries.
    """
    if count < 1:
        return []

    chooser = rng if rng is not None else random
    excluded = {n for n in (exclude or ()) if n}
    letters = list(THINGS_BY_LETTER.keys())
    used_letters: set[str] = set()
    used_things: set[str] = set(excluded)
    result: list[str] = []
    anchor_letter: str | None = None

    for _ in range(count):
        if prefer_same_first_letter and anchor_letter is not None:
            same_pool = [
                n
                for n in THINGS_BY_LETTER[anchor_letter]
                if n not in used_things
            ]
            if same_pool:
                thing = chooser.choice(same_pool)
                result.append(thing)
                used_letters.add(anchor_letter)
                used_things.add(thing)
                continue

        preferred = [L for L in letters if L not in used_letters]
        pool_letters = preferred or letters

        usable = [
            L
            for L in pool_letters
            if any(n not in used_things for n in THINGS_BY_LETTER[L])
        ]
        if not usable:
            usable = [
                L
                for L in letters
                if any(n not in used_things for n in THINGS_BY_LETTER[L])
            ]
        if not usable:
            usable = letters

        letter = chooser.choice(usable)
        candidates = [n for n in THINGS_BY_LETTER[letter] if n not in used_things]
        if not candidates:
            candidates = list(THINGS_BY_LETTER[letter])
        thing = chooser.choice(candidates)
        result.append(thing)
        used_letters.add(letter)
        used_things.add(thing)
        if anchor_letter is None:
            anchor_letter = letter

    return result


def pick_thing(
    *,
    rng: random.Random | None = None,
    exclude: Sequence[str] | None = None,
) -> str:
    """Pick a single plural noun (letter, then thing within that letter)."""
    return pick_things(1, rng=rng, exclude=exclude)[0]
