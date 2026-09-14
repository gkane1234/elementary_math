"""Print-time display rules for rational summands.

Semantic AST / packaging (PF atoms, kernel, goal, M-clear) decides *what*
the student must do. This module only rewrites **presentation** of an
already-chosen ``(num, den_factors)`` pair at print time.

Intent gate
-----------
``display_intent``:

- ``None`` / missing / ``atomic_pf_term`` — apply the active rule preset
  (default polish).
- ``complex_fraction_skill`` — nested form *is* the exercise; skip
  **structure-changing** rules (e.g. absorb).
- ``as_built`` — print structured pieces as given; skip **all** rules.

``display_normalize`` is the master on/off switch (default True).

Presets / rule lists
--------------------
``display_preset`` (default ``standard_rational``) or an explicit
``display_rules`` list selects which named rules run, in order.

**Not writing rules (out of scope forever here):**

- Distributing a leading dens coef into a linear (``q(x+2) → qx+2q``).
- Classroom M-clear of fractional PF numerators (semantic package scale).
- Regex rewrites of stored ``prompt_latex``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Literal, Mapping, Sequence

DisplayIntent = Literal["atomic_pf_term", "complex_fraction_skill", "as_built"]

# Missing / None intent polishes the same as atomic_pf_term.
DEFAULT_DISPLAY_INTENT: DisplayIntent | None = None

# ---------------------------------------------------------------------------
# Named rules (ordered presets list them left→right)
# ---------------------------------------------------------------------------

ABSORB_NESTED_NUMERIC_COEFF = "absorb_nested_numeric_coeff"
FACTOR_JUXTAPOSITION = "factor_juxtaposition"
OMIT_COEFF_1 = "omit_coeff_1"

DisplayRule = Literal[
    "absorb_nested_numeric_coeff",
    "factor_juxtaposition",
    "omit_coeff_1",
]

# Rules that change nested vs flat fraction shape.
STRUCTURE_CHANGING_RULES: frozenset[str] = frozenset({ABSORB_NESTED_NUMERIC_COEFF})

OPT_OUT_INTENTS: frozenset[str] = frozenset({"complex_fraction_skill", "as_built"})

ALL_RULES: tuple[str, ...] = (
    ABSORB_NESTED_NUMERIC_COEFF,
    FACTOR_JUXTAPOSITION,
    OMIT_COEFF_1,
)

DISPLAY_PRESETS: dict[str, tuple[str, ...]] = {
    # Safe classroom standardization for PF / ± / kernel atoms.
    "standard_rational": (
        ABSORB_NESTED_NUMERIC_COEFF,
        FACTOR_JUXTAPOSITION,
        OMIT_COEFF_1,
    ),
    "none": (),
    "as_built": (),
}

DEFAULT_DISPLAY_PRESET = "standard_rational"


@dataclass(frozen=True)
class AbsorbedConstantNum:
    """``(p/q) / Π dens`` → ``p / (q · Π dens)`` for display (value-preserving)."""

    num: dict[int, Fraction]  # constant integer numerator {0: p}
    leading_den_coef: int  # positive q absorbed into den product


@dataclass(frozen=True)
class DisplayRuleConfig:
    """Resolved print-time policy for one fraction render."""

    display_normalize: bool = True
    display_intent: DisplayIntent | str | None = None
    active_rules: tuple[str, ...] = ()
    preset: str = DEFAULT_DISPLAY_PRESET

    def allows(self, rule: str) -> bool:
        return rule in self.active_rules


@dataclass(frozen=True)
class FractionDisplayPlan:
    """Structured pieces after display rules (before LaTeX assembly)."""

    num: dict[int, Fraction]
    leading_den_coef: int
    applied_rules: tuple[str, ...]
    config: DisplayRuleConfig


def resolve_display_intent(raw: object) -> DisplayIntent | str | None:
    """Normalize settings value; empty/None stays None (default polish)."""
    if raw is None:
        return None
    text = str(raw).strip()
    if not text:
        return None
    if text in {"atomic_pf_term", "complex_fraction_skill", "as_built"}:
        return text  # type: ignore[return-value]
    return text


def resolve_display_preset(raw: object) -> str:
    if raw is None or str(raw).strip() == "":
        return DEFAULT_DISPLAY_PRESET
    name = str(raw).strip()
    return name if name in DISPLAY_PRESETS else DEFAULT_DISPLAY_PRESET


def resolve_rule_list(
    *,
    display_rules: Sequence[str] | None = None,
    display_preset: object = None,
) -> tuple[str, ...]:
    """Explicit ``display_rules`` wins; else preset membership (ordered)."""
    if display_rules is not None:
        allowed = set(ALL_RULES)
        return tuple(r for r in display_rules if r in allowed)
    preset = resolve_display_preset(display_preset)
    return DISPLAY_PRESETS.get(preset, DISPLAY_PRESETS[DEFAULT_DISPLAY_PRESET])


def intent_skips_all_rules(display_intent: DisplayIntent | str | None) -> bool:
    return display_intent == "as_built"


def intent_skips_structure_rules(display_intent: DisplayIntent | str | None) -> bool:
    return display_intent in OPT_OUT_INTENTS


def resolve_display_config(
    *,
    display_normalize: bool = True,
    display_intent: DisplayIntent | str | None = None,
    display_rules: Sequence[str] | None = None,
    display_preset: object = None,
    settings: Mapping[str, object] | None = None,
) -> DisplayRuleConfig:
    """Build active rule list from settings and intent gate.

    Default: ``display_normalize=True``, missing intent, preset
    ``standard_rational`` → polish (same as ``atomic_pf_term``).
    """
    if settings is not None:
        if "display_normalize" in settings:
            display_normalize = bool(settings.get("display_normalize"))
        if display_intent is None and "display_intent" in settings:
            display_intent = resolve_display_intent(settings.get("display_intent"))
        if display_rules is None and settings.get("display_rules") is not None:
            raw_rules = settings.get("display_rules")
            if isinstance(raw_rules, (list, tuple)):
                display_rules = [str(r) for r in raw_rules]
        if display_preset is None and "display_preset" in settings:
            display_preset = settings.get("display_preset")

    intent = resolve_display_intent(display_intent)
    preset = resolve_display_preset(display_preset)
    candidates = resolve_rule_list(
        display_rules=display_rules, display_preset=preset
    )

    if not display_normalize or intent_skips_all_rules(intent):
        active: tuple[str, ...] = ()
    elif intent_skips_structure_rules(intent):
        active = tuple(r for r in candidates if r not in STRUCTURE_CHANGING_RULES)
    else:
        # None / atomic_pf_term / unknown → full candidate set
        active = candidates

    return DisplayRuleConfig(
        display_normalize=bool(display_normalize),
        display_intent=intent,
        active_rules=active,
        preset=preset,
    )


def should_absorb_nested_numeric(
    *,
    display_normalize: bool,
    display_intent: DisplayIntent | str | None,
) -> bool:
    """Backward-compatible gate: absorb when normalize on and intent not opt-out."""
    cfg = resolve_display_config(
        display_normalize=display_normalize,
        display_intent=display_intent,
    )
    return cfg.allows(ABSORB_NESTED_NUMERIC_COEFF)


def try_absorb_constant_rational_num(
    num: dict[int, Fraction],
    den_factors: tuple,
) -> AbsorbedConstantNum | None:
    """Absorb constant ``p/q`` into den when ``q > 1`` and dens are present.

    Only constant numerators. Poly nums and integer nums are left alone.
    Does **not** distribute ``q(ax+b)`` into ``qax+qb``.
    """
    if not den_factors:
        return None
    if not num or set(num.keys()) != {0}:
        return None
    c = Fraction(num[0])
    if c.denominator == 1:
        return None
    # Fraction is always reduced with positive denominator.
    return AbsorbedConstantNum(
        num={0: Fraction(c.numerator)},
        leading_den_coef=int(c.denominator),
    )


def format_leading_coef_times_den(leading: int, den_latex: str) -> str:
    """``factor_juxtaposition`` (+ ``omit_coeff_1``): never distribute into poly.

    Multi-factor dens are already ``\\left(...\\right)\\left(...\\right)`` —
    prepend ``q``. Single ungrouped linears get ``q\\left(linear\\right)``.
    Leading ``1`` is omitted.
    """
    if leading == 1:
        return den_latex
    body = den_latex.strip()
    if "\\left(" in body:
        return f"{leading}{body}"
    return rf"{leading}\left({body}\right)"


def plan_fraction_display(
    num: dict[int, Fraction],
    den_factors: tuple,
    *,
    config: DisplayRuleConfig | None = None,
    display_normalize: bool = True,
    display_intent: DisplayIntent | str | None = None,
    display_rules: Sequence[str] | None = None,
    display_preset: object = None,
    settings: Mapping[str, object] | None = None,
) -> FractionDisplayPlan:
    """Apply ordered display rules to structured ``(num, dens)``; no LaTeX yet."""
    cfg = config or resolve_display_config(
        display_normalize=display_normalize,
        display_intent=display_intent,
        display_rules=display_rules,
        display_preset=display_preset,
        settings=settings,
    )
    render_num = num
    leading_q = 1
    applied: list[str] = []

    # Ordered: absorb first, then juxtaposition/omit apply at den assembly.
    if cfg.allows(ABSORB_NESTED_NUMERIC_COEFF):
        absorbed = try_absorb_constant_rational_num(num, den_factors)
        if absorbed is not None:
            render_num = absorbed.num
            leading_q = absorbed.leading_den_coef
            applied.append(ABSORB_NESTED_NUMERIC_COEFF)

    if leading_q != 1 and cfg.allows(FACTOR_JUXTAPOSITION):
        applied.append(FACTOR_JUXTAPOSITION)

    return FractionDisplayPlan(
        num=render_num,
        leading_den_coef=leading_q,
        applied_rules=tuple(applied),
        config=cfg,
    )


def apply_leading_den_coef(
    leading: int,
    den_latex: str,
    *,
    config: DisplayRuleConfig,
) -> str:
    """Apply juxtaposition / omit-1 when formatting ``q · den_body``."""
    if leading == 1:
        return den_latex
    if config.allows(FACTOR_JUXTAPOSITION) or config.allows(OMIT_COEFF_1):
        return format_leading_coef_times_den(leading, den_latex)
    # Rules off but absorb somehow left a leading coef: still juxtapose safely
    # (never distribute) so value/display stay consistent.
    return format_leading_coef_times_den(leading, den_latex)


def config_from_settings(settings: Mapping[str, object] | None) -> DisplayRuleConfig:
    return resolve_display_config(settings=settings or {})
