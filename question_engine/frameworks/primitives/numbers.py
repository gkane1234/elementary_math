"""Layer 0 — number lanes selected from difficulty + constraints.

Mental model
------------
Topic difficulty ``D`` is the single primary knob. Constraints (integers only,
allow negatives / fractions / decimals, …) filter which lanes may appear.
The system then picks a lane from the eligible pool (biased toward harder
lanes as D rises) and samples a value *within* that lane at effective D.

Lane eligibility thresholds (min effective_D to enter the pool)
--------------------------------------------------------------
| min_D | lanes (still subject to constraints) |
|-------|--------------------------------------|
| 0     | friendly_wholes; signed_small if allow_negatives |
| 3     | unit_fractions (if fractions allowed) |
| 4     | simple_rations (fractions); friendly_decimals (decimals) |
| 8     | difficult_rations (fractions) |
| 10    | awkward_decimals (decimals) |

Optional ``number_profile`` / ``force_number_profile`` forces a lane (debug/audit);
omit or set to ``auto`` for the default D+constraints path.

Aliases: ``simple_rationals``→simple_rations, ``difficult_rationals``/``ugly_rations``→difficult_rations.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
from typing import Any, Literal

from question_engine.frameworks.niceness import (
    NicenessError,
    bounds_for_difficulty,
    fraction_is_nice,
    int_is_nice,
)
from question_engine.generators.utils import frac_latex

NumberProfileId = Literal[
    "friendly_wholes",
    "signed_small",
    "unit_fractions",
    "simple_rations",
    "difficult_rations",
    "friendly_decimals",
    "awkward_decimals",
]

NUMBER_PROFILES: tuple[NumberProfileId, ...] = (
    "friendly_wholes",
    "signed_small",
    "unit_fractions",
    "simple_rations",
    "difficult_rations",
    "friendly_decimals",
    "awkward_decimals",
)

PROFILE_ALIASES: dict[str, NumberProfileId] = {
    "simple_rationals": "simple_rations",
    "simple_rational": "simple_rations",
    "difficult_rationals": "difficult_rations",
    "difficult_rational": "difficult_rations",
    "ugly_rations": "difficult_rations",
    "ugly_rationals": "difficult_rations",
    "decimals": "friendly_decimals",
    "wholes": "friendly_wholes",
    "integers": "signed_small",
}

# Minimum effective_D for a lane to enter the auto-selection pool.
# Values live in difficulty_knobs.json — LANE_MIN_D is a live view.
def _lane_min_d_map() -> dict[NumberProfileId, float]:
    from question_engine.frameworks.primitives.difficulty_knobs import all_number_lane_min_d

    raw = all_number_lane_min_d()
    return {pid: float(raw.get(pid, 0.0)) for pid in NUMBER_PROFILES}  # type: ignore[misc]


class _LaneMinDProxy(dict):
    """Dict-like proxy so ``LANE_MIN_D[profile]`` always reads current knobs."""

    def __getitem__(self, key: NumberProfileId) -> float:  # type: ignore[override]
        from question_engine.frameworks.primitives.difficulty_knobs import number_lane_min_d

        return number_lane_min_d(str(key))

    def get(self, key, default=None):  # type: ignore[override]
        try:
            return self[key]
        except Exception:
            return default

    def items(self):  # type: ignore[override]
        return _lane_min_d_map().items()

    def keys(self):  # type: ignore[override]
        return _lane_min_d_map().keys()

    def values(self):  # type: ignore[override]
        return _lane_min_d_map().values()

    def __contains__(self, key: object) -> bool:
        return key in NUMBER_PROFILES


LANE_MIN_D: dict[NumberProfileId, float] = _LaneMinDProxy()  # type: ignore[assignment]

INTEGER_LANES: frozenset[NumberProfileId] = frozenset({"friendly_wholes", "signed_small"})
FRACTION_LANES: frozenset[NumberProfileId] = frozenset(
    {"unit_fractions", "simple_rations", "difficult_rations"}
)
DECIMAL_LANES: frozenset[NumberProfileId] = frozenset(
    {"friendly_decimals", "awkward_decimals"}
)

# Design intent for auditors / UI catalog (keep summaries short; design_intent richer).
PROFILE_CATALOG: dict[NumberProfileId, dict[str, str]] = {
    "friendly_wholes": {
        "label": "Friendly wholes",
        "summary": "Non-negative whole numbers; classroom-small at low D.",
        "design_intent": (
            "Default early-arithmetic lane. Never negative, never fractional. "
            "Low D stays in a small span (about 0–6); higher D widens the span only."
        ),
        "contrast": "vs signed_small (adds negatives); vs rationals/decimals (other forms).",
        "min_d": "0",
    },
    "signed_small": {
        "label": "Signed small integers",
        "summary": "Small integers including negatives.",
        "design_intent": (
            "Integer-introduction lane. Same magnitude growth as wholes but centered "
            "on zero so negatives appear naturally."
        ),
        "contrast": "vs friendly_wholes (no negatives); still no fractions/decimals.",
        "min_d": "0 (requires allow_negatives)",
    },
    "unit_fractions": {
        "label": "Unit fractions",
        "summary": "Only 1/n forms (fraction meaning / unit parts).",
        "design_intent": (
            "Strict 1/n only — for meaning-of-fractions and unit-fraction skills. "
            "D only raises the largest allowed denominator."
        ),
        "contrast": "vs simple_rations (general p/q); never improper or multi-numerator.",
        "min_d": "3",
    },
    "simple_rations": {
        "label": "Simple rationals",
        "summary": "Small p/q, usually reduced; mild dens.",
        "design_intent": (
            "Friendly fraction-ops lane. Dens stay modest; Fraction reduction means "
            "students usually see already-simplified forms. Occasional negatives when allowed."
        ),
        "contrast": (
            "vs difficult_rations (larger dens + often unreduced display); "
            "vs unit_fractions (only 1/n)."
        ),
        "min_d": "4",
    },
    "difficult_rations": {
        "label": "Difficult rationals",
        "summary": "Larger dens; often shown unreduced so students must simplify.",
        "design_intent": (
            "Harder fraction-ops lane. Larger numerators/denominators; at D≥2 a majority "
            "of draws inflate by 2–4 so latex shows an unreduced form (value stored reduced)."
        ),
        "contrast": "vs simple_rations (smaller, usually reduced); intentionally 'ugly' display.",
        "min_d": "8",
    },
    "friendly_decimals": {
        "label": "Friendly decimals",
        "summary": "Tenths/hundredths that still look clean (0.5, 1.25, …).",
        "design_intent": (
            "Clean decimal lane: 1–2 places. Low D biases toward .5 / .25 / .75 style values; "
            "higher D allows slightly larger magnitudes but still readable places."
        ),
        "contrast": "vs awkward_decimals (messier places / more digits).",
        "min_d": "4",
    },
    "awkward_decimals": {
        "label": "Awkward decimals",
        "summary": "Messier place values / more digits as D grows.",
        "design_intent": (
            "Messy decimal lane: 2–3 places, avoids tidy trailing zeros, more negatives. "
            "Use when you want place-value friction without switching to fraction form."
        ),
        "contrast": "vs friendly_decimals (clean tenths/hundredths).",
        "min_d": "10",
    },
}

NUMBER_SETTINGS_SCHEMA = {
    "integers_only": {
        "type": "bool",
        "default": False,
        "doc": "Restrict lanes to whole/signed integers (no fractions or decimals).",
    },
    "allow_negatives": {"type": "bool", "default": True},
    "allow_fractions": {"type": "bool", "default": True},
    "allow_decimals": {"type": "bool", "default": True},
    "exclude_zero": {"type": "bool", "default": False},
    # Override only — prefer auto lane selection from D + constraints.
    "number_profile": {
        "type": "enum",
        "values": ["auto", *NUMBER_PROFILES],
        "default": "auto",
        "catalog": PROFILE_CATALOG,
        "doc": "Force a lane for debug/audit; 'auto' selects from D + constraints.",
    },
}


@dataclass(frozen=True)
class NumberConstraints:
    integers_only: bool = False
    allow_negatives: bool = True
    allow_fractions: bool = True
    allow_decimals: bool = True
    exclude_zero: bool = False

    def as_dict(self) -> dict[str, bool]:
        return {
            "integers_only": self.integers_only,
            "allow_negatives": self.allow_negatives,
            "allow_fractions": self.allow_fractions,
            "allow_decimals": self.allow_decimals,
            "exclude_zero": self.exclude_zero,
        }


@dataclass(frozen=True)
class LaneSelection:
    profile: NumberProfileId
    source: Literal["auto", "force"]
    effective_d: float
    eligible: tuple[NumberProfileId, ...]
    constraints: NumberConstraints
    note: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "profile": self.profile,
            "source": self.source,
            "effective_d": self.effective_d,
            "eligible": list(self.eligible),
            "constraints": self.constraints.as_dict(),
            "note": self.note,
        }


@dataclass(frozen=True)
class SampledNumber:
    value: Fraction
    profile: NumberProfileId
    effective_d: float
    latex: str
    cost_hint: float = 0.0
    display: str = "fraction"  # fraction | decimal | integer
    # For difficult_rations: raw unreduced pair used in latex (None → use value).
    display_num: int | None = None
    display_den: int | None = None
    lane: LaneSelection | None = None


def normalize_profile_id(raw: str | None) -> NumberProfileId:
    key = str(raw or "friendly_wholes").strip()
    if key in PROFILE_ALIASES:
        return PROFILE_ALIASES[key]
    if key in NUMBER_PROFILES:
        return key  # type: ignore[return-value]
    return "friendly_wholes"


def resolve_constraints(settings: dict[str, Any] | None) -> NumberConstraints:
    """Normalize number-domain constraints from settings."""
    settings = settings or {}
    integers_only = bool(settings.get("integers_only", False))
    domain = str(settings.get("number_domain", "")).strip().lower()
    if domain in {"integers", "integer", "wholes", "whole", "int"}:
        integers_only = True

    allow_fractions = bool(settings.get("allow_fractions", True)) and not integers_only
    allow_decimals = bool(settings.get("allow_decimals", True)) and not integers_only
    # Legacy / compact aliases
    if settings.get("no_fractions") is True:
        allow_fractions = False
    if settings.get("no_decimals") is True:
        allow_decimals = False

    return NumberConstraints(
        integers_only=integers_only,
        allow_negatives=bool(settings.get("allow_negatives", True)),
        allow_fractions=allow_fractions,
        allow_decimals=allow_decimals,
        exclude_zero=bool(settings.get("exclude_zero", False)),
    )


def _forced_profile(settings: dict[str, Any] | None) -> NumberProfileId | None:
    settings = settings or {}
    for key in ("force_number_profile", "number_profile"):
        raw = settings.get(key)
        if raw is None:
            continue
        text = str(raw).strip().lower()
        if text in {"", "auto", "none", "default"}:
            continue
        return normalize_profile_id(text)
    return None


def eligible_lanes(
    effective_d: float,
    constraints: NumberConstraints,
) -> list[NumberProfileId]:
    """Lanes allowed by D thresholds and constraints (ordered by NUMBER_PROFILES)."""
    d = max(0.0, float(effective_d))
    out: list[NumberProfileId] = []
    for pid in NUMBER_PROFILES:
        if d + 1e-9 < LANE_MIN_D[pid]:
            continue
        if pid in INTEGER_LANES:
            if pid == "signed_small" and not constraints.allow_negatives:
                continue
            out.append(pid)
            continue
        if pid in FRACTION_LANES:
            if not constraints.allow_fractions:
                continue
            out.append(pid)
            continue
        if pid in DECIMAL_LANES:
            if not constraints.allow_decimals:
                continue
            out.append(pid)
    if not out:
        # Always keep a safe fallback.
        out = ["friendly_wholes"]
    return out


def _lane_weight(profile: NumberProfileId, effective_d: float) -> float:
    """Bias toward harder (higher min_D) lanes as D rises.

    Soft lanes stay available but get down-weighted once much easier than D,
    so ~D=10+ draws mostly difficult_rations / awkward_decimals when allowed.
    """
    min_d = LANE_MIN_D[profile]
    from question_engine.frameworks.primitives.difficulty_knobs import fget

    # Base: harder unlock threshold → higher weight.
    power = fget("number_lanes", "weight_hardness_power", 2.2)
    offset = fget("number_lanes", "weight_staleness_offset", 3.0)
    hardness = (1.0 + min_d) ** power
    # Mild preference for the "frontier" near current D; stale easy lanes fade.
    staleness = max(0.0, effective_d - min_d - offset)
    return hardness / (1.0 + 0.35 * staleness)


def select_lane(
    effective_d: float,
    *,
    settings: dict[str, Any] | None = None,
    rng: random.Random | None = None,
) -> LaneSelection:
    """Choose a number lane from D + constraints (or force override)."""
    rng = rng or random.Random()
    settings = settings or {}
    constraints = resolve_constraints(settings)
    d = max(0.0, float(effective_d))

    forced = _forced_profile(settings)
    if forced is not None:
        return LaneSelection(
            profile=forced,
            source="force",
            effective_d=d,
            eligible=(forced,),
            constraints=constraints,
            note=f"forced profile={forced}",
        )

    pool = eligible_lanes(d, constraints)
    weights = [_lane_weight(p, d) for p in pool]
    chosen = rng.choices(pool, weights=weights, k=1)[0]
    return LaneSelection(
        profile=chosen,
        source="auto",
        effective_d=d,
        eligible=tuple(pool),
        constraints=constraints,
        note=(
            f"auto from D={d:g} eligible={list(pool)} "
            f"constraints={constraints.as_dict()}"
        ),
    )


def sample_number(
    effective_d: float,
    *,
    settings: dict[str, Any] | None = None,
    rng: random.Random | None = None,
    exclude_zero: bool | None = None,
) -> SampledNumber:
    """Sample a number: pick lane from D+constraints (unless forced), then draw in-lane."""
    rng = rng or random.Random()
    settings = dict(settings or {})
    lane = select_lane(effective_d, settings=settings, rng=rng)
    profile = lane.profile
    constraints = lane.constraints
    if exclude_zero is None:
        exclude_zero = constraints.exclude_zero
    allow_negatives = constraints.allow_negatives
    bounds = bounds_for_difficulty(effective_d, profile=profile)

    last_err = "unknown"
    for _ in range(48):
        try:
            value, display, raw_pair = _draw_profile(
                profile,
                effective_d,
                bounds,
                rng,
                exclude_zero=exclude_zero,
                allow_negatives=allow_negatives,
            )
        except NicenessError as exc:
            last_err = str(exc)
            continue
        if exclude_zero and value == 0:
            continue
        if profile in {"friendly_wholes", "signed_small"}:
            if value.denominator != 1 or not int_is_nice(int(value), bounds):
                continue
        elif not fraction_is_nice(value, bounds):
            continue
        latex = _latex_for(value, profile, display, raw_pair=raw_pair)
        disp_num = disp_den = None
        if raw_pair is not None:
            disp_num, disp_den = raw_pair
        return SampledNumber(
            value=value,
            profile=profile,
            effective_d=effective_d,
            latex=latex,
            cost_hint=_cost_hint(value, profile, effective_d),
            display=display,
            display_num=disp_num,
            display_den=disp_den,
            lane=lane,
        )
    raise NicenessError(
        f"failed to sample nice number for profile={profile} d={effective_d}: {last_err}"
    )


def _draw_profile(
    profile: NumberProfileId,
    effective_d: float,
    bounds,
    rng: random.Random,
    *,
    exclude_zero: bool,
    allow_negatives: bool = True,
) -> tuple[Fraction, str, tuple[int, int] | None]:
    """Return (value, display_mode, optional_unreduced_pair)."""
    d = max(0.0, effective_d)
    span = max(1, min(bounds.max_abs_int, int(3 + d)))

    if profile == "friendly_wholes":
        lo, hi = 0, span
        if exclude_zero:
            lo = 1
        return Fraction(rng.randint(lo, max(lo, hi))), "integer", None

    if profile == "signed_small":
        if not allow_negatives:
            lo = 1 if exclude_zero else 0
            return Fraction(rng.randint(lo, max(lo, span))), "integer", None
        n = rng.randint(-span, span)
        if exclude_zero and n == 0:
            n = rng.choice([-1, 1])
        return Fraction(n), "integer", None

    if profile == "unit_fractions":
        den_hi = min(bounds.max_denominator, max(2, int(3 + d)))
        den = rng.randint(2, den_hi)
        return Fraction(1, den), "fraction", None

    if profile == "simple_rations":
        # Keep dens mild; prefer already-reduced look (no inflate).
        den_hi = min(bounds.max_denominator, max(2, int(3 + 0.5 * d)))
        den = rng.randint(2, den_hi)
        num_hi = min(bounds.max_abs_int, max(1, den + int(d)))
        num = rng.randint(1, num_hi)
        # Bias toward proper-ish fractions at low D.
        if d < 4 and num >= den and rng.random() < 0.7:
            num = rng.randint(1, max(1, den - 1))
        if allow_negatives and rng.random() < 0.25:
            num = -num
        return Fraction(num, den), "fraction", None

    if profile == "difficult_rations":
        den_hi = min(bounds.max_denominator, max(4, int(6 + d)))
        den = rng.randint(4, den_hi)
        num_hi = min(bounds.max_abs_int, max(den + 1, int(10 + 2 * d)))
        num = rng.randint(1, num_hi)
        # Prefer unreduced display: inflate by k so gcd(num,den)>1.
        raw_pair: tuple[int, int] | None = None
        if d >= 2 and rng.random() < 0.75:
            k = rng.choice([2, 3, 4] if d >= 6 else [2, 3])
            num *= k
            den *= k
            # Cap inflated den against niceness-ish ceiling
            if den > bounds.max_denominator * 2:
                num //= k
                den //= k
            else:
                raw_pair = (num, den)
        if allow_negatives and rng.random() < 0.4:
            num = -abs(num)
            if raw_pair is not None:
                raw_pair = (-abs(raw_pair[0]), raw_pair[1])
        value = Fraction(num, den)
        if raw_pair is None and abs(num) > 0 and den > 1 and math.gcd(abs(num), den) > 1:
            raw_pair = (num, den)
        # If still reduced (coprime), optionally force an inflate for audit distinctness.
        if raw_pair is None and d >= 4 and value.denominator > 1 and rng.random() < 0.5:
            k = 2
            raw_pair = (value.numerator * k, value.denominator * k)
        return value, "fraction", raw_pair

    if profile == "friendly_decimals":
        # Tenths or hundredths that look clean.
        places = 1 if d < 4 else rng.choice([1, 2])
        scale = 10**places
        max_units = min(bounds.max_abs_int, max(3, int(4 + d)))
        units = rng.randint(0 if not exclude_zero else 1, max_units * scale)
        if exclude_zero and units == 0:
            units = rng.randint(1, max(1, scale))
        # Bias toward .5 / .25 / .75 at low D.
        if d < 5 and places == 2 and rng.random() < 0.55:
            candidates = [25, 50, 75, 125, 150, 250, 100, 200]
            units = rng.choice(candidates)
            units = min(units, max_units * scale)
            units = max(1 if exclude_zero else 0, units)
        elif d < 5 and places == 1 and rng.random() < 0.45:
            units = rng.choice([5, 10, 15, 20, 25]) % (max_units * scale + 1)
            units = max(1 if exclude_zero else 0, units)
        if allow_negatives and rng.random() < 0.2:
            units = -units
        return Fraction(units, scale), "decimal", None

    # awkward_decimals — messier place values; avoid tidy trailing zeros.
    places = 2 if d < 6 else rng.choice([2, 3])
    scale = 10**places
    max_units = min(bounds.max_abs_int * scale, max(scale, int((5 + 2 * d) * scale // 2)))
    units = rng.randint(1, max(1, max_units))
    if units % 10 == 0 and rng.random() < 0.75:
        units += rng.choice([1, 3, 7, 9])
    # Prefer non-.00 / non-.50 endings
    if places >= 2 and units % 25 == 0 and rng.random() < 0.6:
        units += rng.choice([1, 2, 3, 7])
    if allow_negatives and rng.random() < 0.4:
        units = -units
    return Fraction(units, scale), "decimal", None


def _latex_for(
    value: Fraction,
    profile: NumberProfileId,
    display: str,
    *,
    raw_pair: tuple[int, int] | None = None,
) -> str:
    if display == "integer" or (
        value.denominator == 1 and profile in {"friendly_wholes", "signed_small"}
    ):
        return str(value.numerator)
    if display == "decimal" or profile in {"friendly_decimals", "awkward_decimals"}:
        dec = Decimal(value.numerator) / Decimal(value.denominator)
        places = 3 if profile == "awkward_decimals" else 2
        q = Decimal(10) ** -places
        s = str(dec.quantize(q, rounding=ROUND_HALF_UP))
        if "." in s:
            s = s.rstrip("0").rstrip(".")
        return s
    if raw_pair is not None:
        num, den = raw_pair
        if den == 1:
            return str(num)
        if num < 0:
            return f"-\\frac{{{abs(num)}}}{{{den}}}"
        return f"\\frac{{{num}}}{{{den}}}"
    return frac_latex(value)


def _cost_hint(value: Fraction, profile: NumberProfileId, effective_d: float) -> float:
    base = {
        "friendly_wholes": 0.0,
        "signed_small": 0.5,
        "unit_fractions": 1.0,
        "simple_rations": 1.5,
        "difficult_rations": 2.5,
        "friendly_decimals": 1.0,
        "awkward_decimals": 2.0,
    }
    c = float(base.get(profile, 0))
    if abs(value.numerator) > 9 or value.denominator > 6:
        c += 0.5
    return min(c, max(0.0, effective_d))


def audit_samples(
    profile: NumberProfileId,
    *,
    difficulties: tuple[float, ...] = (0, 3, 6, 10, 14),
    n_per: int = 10,
    seed: int = 0,
) -> list[dict[str, Any]]:
    """Generate sample draws for a forced profile (legacy per-lane audit)."""
    rows: list[dict[str, Any]] = []
    meta = PROFILE_CATALOG[profile]
    for d in difficulties:
        rng = random.Random(seed + int(10 * d) + hash(profile) % 997)
        for i in range(n_per):
            sample = sample_number(d, settings={"number_profile": profile}, rng=rng)
            rows.append(
                {
                    "profile": profile,
                    "label": meta["label"],
                    "summary": meta["summary"],
                    "design_intent": meta.get("design_intent", ""),
                    "contrast": meta.get("contrast", ""),
                    "difficulty": d,
                    "latex": sample.latex,
                    "value": str(sample.value),
                    "display": sample.display,
                    "display_num": sample.display_num,
                    "display_den": sample.display_den,
                    "index": i,
                    "lane_source": "force",
                }
            )
    return rows


def audit_lane_selection(
    *,
    difficulties: tuple[float, ...] = (0, 2, 4, 6, 8, 10, 12, 14),
    constraint_sets: dict[str, dict[str, Any]] | None = None,
    n_per: int = 8,
    seed: int = 1,
) -> list[dict[str, Any]]:
    """Audit auto lane selection: for each D × constraint set, record lanes + samples."""
    if constraint_sets is None:
        constraint_sets = {
            "default": {},
            "integers_only": {"integers_only": True},
            "no_decimals": {"allow_decimals": False},
            "no_fractions": {"allow_fractions": False},
            "positives_only": {"allow_negatives": False},
            "integers_no_negatives": {"integers_only": True, "allow_negatives": False},
        }
    rows: list[dict[str, Any]] = []
    for cname, csettings in constraint_sets.items():
        constraints = resolve_constraints(csettings)
        for d in difficulties:
            eligible = eligible_lanes(d, constraints)
            rng = random.Random(seed + int(17 * d) + hash(cname) % 991)
            for i in range(n_per):
                sample = sample_number(d, settings=csettings, rng=rng)
                lane = sample.lane
                rows.append(
                    {
                        "constraint_set": cname,
                        "constraints": constraints.as_dict(),
                        "difficulty": d,
                        "eligible": list(eligible),
                        "selected": sample.profile,
                        "lane_source": lane.source if lane else "auto",
                        "lane_note": lane.note if lane else "",
                        "latex": sample.latex,
                        "value": str(sample.value),
                        "display": sample.display,
                        "index": i,
                    }
                )
    return rows
