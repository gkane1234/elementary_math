"""Shared LaTeX/text rendering helpers for Layer-1 algebra primitives."""

from __future__ import annotations

from fractions import Fraction

from question_engine.generators.utils import frac_latex


def num_latex(value: Fraction) -> str:
    return frac_latex(value)


def coeff_times_var(coeff: Fraction, var_latex: str) -> str:
    """Render ``coeff * var`` without a leading ``+``."""
    if coeff == 0:
        return "0"
    if coeff == 1:
        return var_latex
    if coeff == -1:
        return f"-{var_latex}"
    return f"{num_latex(coeff)}{var_latex}"


def join_signed_terms(parts: list[tuple[Fraction, str]]) -> tuple[str, str]:
    """Join (coeff, atom_latex) terms with +/−. Empty → ('0','0').

    ``atom_latex`` is the variable part (e.g. ``x``, ``x^{2}``) or ``""`` for a constant.
    """
    cleaned: list[tuple[Fraction, str]] = [(c, a) for c, a in parts if c != 0]
    if not cleaned:
        return "0", "0"

    def piece(c: Fraction, atom: str) -> str:
        if not atom:
            return num_latex(c)
        return coeff_times_var(c, atom)

    first_c, first_a = cleaned[0]
    latex = piece(first_c, first_a)
    text = latex
    for c, a in cleaned[1:]:
        body = piece(abs(c), a) if a else num_latex(abs(c))
        if c < 0:
            latex = f"{latex} - {body}"
            text = f"{text} - {body}"
        else:
            latex = f"{latex} + {body}"
            text = f"{text} + {body}"
    return latex, text


def sample_integerish(ctx, *, exclude_zero: bool = False, prefer_positive: bool = False):
    """Sample a number; retry until integer if fractions sneak in (GCF / steps)."""
    for _ in range(24):
        n = ctx.sample_number(exclude_zero=exclude_zero)
        if prefer_positive and n.value < 0:
            continue
        if n.value.denominator == 1:
            return n
    # Fallback: force friendly wholes via temporary override on numbers settings.
    from question_engine.frameworks.primitives.numbers import sample_number
    from question_engine.frameworks.primitives.registry import PRIM_NUMBERS

    settings = {
        **ctx.settings_for(PRIM_NUMBERS),
        "number_profile": "friendly_wholes" if prefer_positive else "signed_small",
        "integers_only": True,
        "exclude_zero": exclude_zero,
    }
    if prefer_positive:
        settings["allow_negatives"] = False
    return sample_number(
        ctx.effective_d(PRIM_NUMBERS),
        settings=settings,
        rng=ctx.rng,
        exclude_zero=exclude_zero,
    )
