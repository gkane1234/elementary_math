"""Pre–Grade 6 foundation skills (true roots of the progression DAG).

These are not a separate OpenStax book; they model arithmetic number sense
that Grade 6 units actually require (e.g. ratios need numbers and fractions).
"""

from __future__ import annotations

# (node_id, chapter_index, title)
FOUNDATION_UNITS: list[tuple[str, int, str]] = [
    ("whole_numbers", 1, "Whole Numbers and Operations"),
    ("fractions", 2, "Fraction Meaning and Equivalence"),
    ("decimals", 3, "Decimal Place Value"),
    ("multiplication_and_division_fluency", 4, "Multiplication and Division Fluency"),
]

BOOK_ID = "foundations"
DISPLAY_NAME = "Foundations (Pre–Grade 6)"
