"""First-name bank and selection for word problems.

Selection algorithm (per name slot):
  1. Choose a random letter that has names in the bank.
  2. Choose a random name from that letter's list.

When multiple names are needed, prefer distinct starting letters
(and distinct names) so characters are easy to tell apart.
"""

from __future__ import annotations

import random
from typing import Sequence

# Enough variety per letter; Q/X/Z keep short lists rather than merging.
FIRST_NAMES_BY_LETTER: dict[str, tuple[str, ...]] = {
    "A": ("Alex", "Avery", "Amir", "Ava", "Adrian", "Aisha"),
    "B": ("Blake", "Brianna", "Ben", "Bailey", "Brooke", "Brian"),
    "C": ("Casey", "Cameron", "Chloe", "Carlos", "Claire", "Chris"),
    "D": ("Dana", "Diego", "Devon", "Diana", "Drew", "Daniel"),
    "E": ("Elena", "Ethan", "Emma", "Evan", "Eliza", "Eric"),
    "F": ("Finn", "Faith", "Felix", "Fiona", "Frankie"),
    "G": ("Grace", "Gabriel", "Gia", "Grant", "Gwen", "George"),
    "H": ("Harper", "Hassan", "Hannah", "Hugo", "Hazel", "Henry"),
    "I": ("Iris", "Isaac", "Ivy", "Ian", "Isabel"),
    "J": ("Jordan", "Jamie", "Jade", "Julian", "Jasmine", "Jay"),
    "K": ("Kai", "Kayla", "Kevin", "Kim", "Kira", "Kyle"),
    "L": ("Liam", "Lena", "Leo", "Lucia", "Logan", "Lily"),
    "M": ("Morgan", "Maya", "Marcus", "Mia", "Miles", "Maria"),
    "N": ("Noah", "Nina", "Nate", "Nora", "Nia", "Neil"),
    "O": ("Owen", "Olivia", "Omar", "Opal", "Oscar"),
    "P": ("Parker", "Priya", "Paul", "Paige", "Peter", "Piper"),
    "Q": ("Quinn", "Quincy", "Queenie"),
    "R": ("Riley", "Rosa", "Ryan", "Ravi", "Rachel", "Reed"),
    "S": ("Sam", "Sofia", "Sean", "Sara", "Soren", "Skye"),
    "T": ("Taylor", "Tessa", "Theo", "Talia", "Tyler", "Tara"),
    "U": ("Uma", "Uri", "Ursula"),
    "V": ("Vera", "Victor", "Violet", "Vince", "Valerie"),
    "W": ("Wendy", "Will", "Willow", "Wesley", "Wade"),
    "X": ("Xavier", "Xander", "Ximena"),
    "Y": ("Yara", "Yuri", "Yasmin", "Yves"),
    "Z": ("Zara", "Zoe", "Zane"),
}


def letters_with_names() -> tuple[str, ...]:
    """Letters that have at least one name in the bank."""
    return tuple(FIRST_NAMES_BY_LETTER.keys())


def names_for_letter(letter: str) -> tuple[str, ...]:
    """Return names for ``letter`` (case-insensitive). Empty if unknown."""
    return FIRST_NAMES_BY_LETTER.get(letter.upper(), ())


def pick_names(
    count: int = 1,
    *,
    rng: random.Random | None = None,
    exclude: Sequence[str] | None = None,
) -> list[str]:
    """Pick ``count`` first names via letter-then-name sampling.

    Prefers distinct starting letters when possible, then distinct names.
    Falls back to reusing letters (still avoiding duplicate names when it can)
    if ``count`` exceeds the number of available letters.
    """
    if count < 1:
        return []

    chooser = rng if rng is not None else random
    excluded = {n for n in (exclude or ()) if n}
    letters = list(FIRST_NAMES_BY_LETTER.keys())
    used_letters: set[str] = set()
    used_names: set[str] = set(excluded)
    result: list[str] = []

    for _ in range(count):
        preferred = [L for L in letters if L not in used_letters]
        pool_letters = preferred or letters

        # Prefer letters that still have unused names.
        usable = [
            L
            for L in pool_letters
            if any(n not in used_names for n in FIRST_NAMES_BY_LETTER[L])
        ]
        if not usable:
            usable = [
                L
                for L in letters
                if any(n not in used_names for n in FIRST_NAMES_BY_LETTER[L])
            ]
        if not usable:
            usable = letters

        letter = chooser.choice(usable)
        candidates = [n for n in FIRST_NAMES_BY_LETTER[letter] if n not in used_names]
        if not candidates:
            candidates = list(FIRST_NAMES_BY_LETTER[letter])
        name = chooser.choice(candidates)
        result.append(name)
        used_letters.add(letter)
        used_names.add(name)

    return result


def pick_name(
    *,
    rng: random.Random | None = None,
    exclude: Sequence[str] | None = None,
) -> str:
    """Pick a single first name (letter, then name within that letter)."""
    return pick_names(1, rng=rng, exclude=exclude)[0]
