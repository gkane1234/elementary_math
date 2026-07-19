"""Layer 0 — variable lanes selected from difficulty + constraints.

Mental model
------------
Topic difficulty ``D`` is the single primary knob. Constraints (only-x, allow
greek, lock letter, …) filter which lanes may appear. The system then picks a
lane from the eligible pool (biased toward harder / recently unlocked lanes as
D rises) and samples a letter *within* that lane.

Lane eligibility thresholds (min effective_D to enter the pool)
--------------------------------------------------------------
| min_D | lane            | letter pool |
|-------|-----------------|-------------|
| 0     | only_x          | x |
| 3     | xyz             | x, y, z |
| 6     | abctuvwxyz      | common school algebra letters |
| 10    | whole_alphabet  | a–z |
| 12    | greek           | common Greek variables (α β γ …) |

Optional ``variable_lane`` / ``force_variable_lane`` forces a lane (debug/audit);
omit or set to ``auto`` for the default D+constraints path.

Legacy: ``allow_other_letters=False`` forces the only_x lane (same as ``only_x``).

Greek letter set (documented choices)
-------------------------------------
Included: α β γ δ θ λ μ ξ ρ σ τ φ ψ ω
Excluded: π (almost always the constant), ε (often a small positive), ι (looks
like i). These stay out of the pool even at high D.
"""

from __future__ import annotations

import random
import string
from dataclasses import dataclass
from typing import Any, Literal

VariableLaneId = Literal[
    "only_x",
    "xyz",
    "abctuvwxyz",
    "whole_alphabet",
    "greek",
]

VARIABLE_LANES: tuple[VariableLaneId, ...] = (
    "only_x",
    "xyz",
    "abctuvwxyz",
    "whole_alphabet",
    "greek",
)

LANE_ALIASES: dict[str, VariableLaneId] = {
    "x_only": "only_x",
    "only-x": "only_x",
    "x": "only_x",
    "xyz_only": "xyz",
    "common": "abctuvwxyz",
    "common_algebra": "abctuvwxyz",
    "school": "abctuvwxyz",
    "alphabet": "whole_alphabet",
    "a_z": "whole_alphabet",
    "az": "whole_alphabet",
    "greek_letters": "greek",
}

# Minimum effective_D for a lane to enter the auto-selection pool (live from knobs).
class _VarLaneMinDProxy(dict):
    def __getitem__(self, key: VariableLaneId) -> float:  # type: ignore[override]
        from question_engine.frameworks.primitives.difficulty_knobs import variable_lane_min_d

        return variable_lane_min_d(str(key))

    def get(self, key, default=None):  # type: ignore[override]
        try:
            return self[key]
        except Exception:
            return default


LANE_MIN_D: dict[VariableLaneId, float] = _VarLaneMinDProxy()  # type: ignore[assignment]

# Common school algebra letters (user sketch a,b,c,t,u,v,w,x,y,z plus frequent extras).
COMMON_ALGEBRA_LETTERS: tuple[str, ...] = (
    "a",
    "b",
    "c",
    "h",
    "k",
    "m",
    "n",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
)

# Unicode Greek → KaTeX command (no leading backslash stored twice).
GREEK_LETTER_LATEX: dict[str, str] = {
    "α": r"\alpha",
    "β": r"\beta",
    "γ": r"\gamma",
    "δ": r"\delta",
    "θ": r"\theta",
    "λ": r"\lambda",
    "μ": r"\mu",
    "ξ": r"\xi",
    "ρ": r"\rho",
    "σ": r"\sigma",
    "τ": r"\tau",
    "φ": r"\phi",
    "ψ": r"\psi",
    "ω": r"\omega",
}

GREEK_LETTERS: tuple[str, ...] = tuple(GREEK_LETTER_LATEX.keys())

LANE_POOLS: dict[VariableLaneId, tuple[str, ...]] = {
    "only_x": ("x",),
    "xyz": ("x", "y", "z"),
    "abctuvwxyz": COMMON_ALGEBRA_LETTERS,
    "whole_alphabet": tuple(string.ascii_lowercase),
    "greek": GREEK_LETTERS,
}

# Legacy export — common Latin letters used as lock options / older callers.
DEFAULT_VARIABLES: tuple[str, ...] = (
    "x",
    "y",
    "z",
    "n",
    "t",
    "a",
    "b",
    "k",
    "m",
)

# Soft per-letter cost hint (lane min_D dominates selection).
VARIABLE_COST: dict[str, float] = {
    "x": 0.0,
    "y": 1.0,
    "z": 1.0,
    "n": 1.5,
    "t": 1.5,
    "a": 2.0,
    "b": 2.0,
    "k": 2.5,
    "m": 2.5,
}
for _ch in string.ascii_lowercase:
    VARIABLE_COST.setdefault(_ch, 3.0)
for _g in GREEK_LETTERS:
    VARIABLE_COST[_g] = 4.0

LANE_CATALOG: dict[VariableLaneId, dict[str, str]] = {
    "only_x": {
        "label": "Only x",
        "summary": "Always the letter x.",
        "design_intent": "Default early-algebra lane. One familiar unknown.",
        "contrast": "vs xyz (adds y, z).",
        "min_d": "0",
    },
    "xyz": {
        "label": "x, y, z",
        "summary": "Classic Cartesian / multi-variable intro letters.",
        "design_intent": "Small pool for two- and three-variable comfort.",
        "contrast": "vs only_x; vs broader school letter set.",
        "min_d": "3",
    },
    "abctuvwxyz": {
        "label": "Common algebra letters",
        "summary": "School set: a–c, h, k, m–n, p–z (no d–g, i–j, l, o).",
        "design_intent": (
            "Usual classroom variables without the full alphabet noise "
            "(skips letters that look like digits/ops: i, l, o)."
        ),
        "contrast": "vs whole_alphabet (a–z); vs xyz (tiny pool).",
        "min_d": "6",
    },
    "whole_alphabet": {
        "label": "Whole alphabet",
        "summary": "Any lowercase Latin letter a–z.",
        "design_intent": "Full Latin pool when letter variety itself is the skill friction.",
        "contrast": "vs abctuvwxyz (curated); vs greek.",
        "min_d": "10",
    },
    "greek": {
        "label": "Greek letters",
        "summary": "Common Greek variables (α β γ δ θ λ μ … ω); not π/ε/ι.",
        "design_intent": (
            "Top-of-progression pool. Prefers letters used as unknowns/parameters "
            "in secondary math. Excludes π (constant), ε (often 'small positive'), "
            "ι (confusable with i)."
        ),
        "contrast": "vs Latin lanes; requires allow_greek (default on).",
        "min_d": "12",
    },
}

VARIABLE_SETTINGS_SCHEMA = {
    "only_x": {
        "type": "bool",
        "default": False,
        "description": "Force the only_x lane (ignore wider pools).",
    },
    "allow_greek": {
        "type": "bool",
        "default": True,
        "description": "If false, greek lane never enters the eligible pool.",
    },
    "max_variable_lane": {
        "type": "enum_or_null",
        "values": ["auto", *VARIABLE_LANES],
        "default": "auto",
        "description": "Cap progression: only lanes at or below this id may be selected.",
    },
    "lock_variable": {
        "type": "enum_or_null",
        "values": [None, "none", *DEFAULT_VARIABLES, *GREEK_LETTERS],
        "default": None,
        "description": "If set to a letter, always use that letter (bypasses lane sampling).",
    },
    # Legacy → maps to only_x when False.
    "allow_other_letters": {
        "type": "bool",
        "default": True,
        "description": "Legacy: False forces only_x (same as only_x=True).",
    },
    # Override only — prefer auto lane selection from D + constraints.
    "variable_lane": {
        "type": "enum",
        "values": ["auto", *VARIABLE_LANES],
        "default": "auto",
        "catalog": LANE_CATALOG,
        "doc": "Force a lane for debug/audit; 'auto' selects from D + constraints.",
    },
}


@dataclass(frozen=True)
class VariableConstraints:
    only_x: bool = False
    allow_greek: bool = True
    max_variable_lane: VariableLaneId | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "only_x": self.only_x,
            "allow_greek": self.allow_greek,
            "max_variable_lane": self.max_variable_lane,
        }


@dataclass(frozen=True)
class VariableLaneSelection:
    profile: VariableLaneId
    source: Literal["auto", "force", "lock"]
    effective_d: float
    eligible: tuple[VariableLaneId, ...]
    constraints: VariableConstraints
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
class SampledVariable:
    name: str
    effective_d: float
    cost: float
    locked: bool
    latex: str = ""
    profile: VariableLaneId = "only_x"
    lane: VariableLaneSelection | None = None

    def __post_init__(self) -> None:
        if not self.latex:
            object.__setattr__(self, "latex", variable_latex(self.name))


def variable_latex(name: str) -> str:
    """LaTeX fragment for embedding a variable in math mode."""
    key = str(name).strip()
    if key in GREEK_LETTER_LATEX:
        return GREEK_LETTER_LATEX[key]
    # Already a command like \alpha
    if key.startswith("\\"):
        return key
    # Map greek command names without slash
    bare = {v.lstrip("\\"): v for v in GREEK_LETTER_LATEX.values()}
    if key in bare:
        return bare[key]
    return key


def normalize_lane_id(raw: str | None) -> VariableLaneId:
    key = str(raw or "only_x").strip().lower().replace(" ", "_")
    if key in LANE_ALIASES:
        return LANE_ALIASES[key]
    if key in VARIABLE_LANES:
        return key  # type: ignore[return-value]
    return "only_x"


def _lane_rank(lane: VariableLaneId) -> int:
    return VARIABLE_LANES.index(lane)


def resolve_variable_constraints(settings: dict[str, Any] | None) -> VariableConstraints:
    """Normalize variable-domain constraints from settings."""
    settings = settings or {}
    only_x = bool(settings.get("only_x", False))
    # Legacy: allow_other_letters=False → only x.
    if "allow_other_letters" in settings and settings.get("allow_other_letters") is False:
        only_x = True

    allow_greek = bool(settings.get("allow_greek", True))
    if settings.get("no_greek") is True:
        allow_greek = False

    max_lane: VariableLaneId | None = None
    raw_max = settings.get("max_variable_lane")
    if raw_max is not None:
        text = str(raw_max).strip().lower()
        if text not in {"", "auto", "none", "default"}:
            max_lane = normalize_lane_id(text)

    return VariableConstraints(
        only_x=only_x,
        allow_greek=allow_greek,
        max_variable_lane=max_lane,
    )


def _forced_lane(settings: dict[str, Any] | None) -> VariableLaneId | None:
    settings = settings or {}
    for key in ("force_variable_lane", "variable_lane"):
        raw = settings.get(key)
        if raw is None:
            continue
        text = str(raw).strip().lower()
        if text in {"", "auto", "none", "default"}:
            continue
        return normalize_lane_id(text)
    return None


def _normalize_lock(raw: Any) -> str | None:
    if raw is None:
        return None
    text = str(raw).strip()
    if text.lower() in {"", "none", "auto", "null", "default"}:
        return None
    # Accept \alpha / alpha / α
    if text.startswith("\\"):
        for uni, cmd in GREEK_LETTER_LATEX.items():
            if cmd == text:
                return uni
        return text.lstrip("\\")  # fall through as bare name
    bare = {v.lstrip("\\"): k for k, v in GREEK_LETTER_LATEX.items()}
    if text in bare:
        return bare[text]
    return text


def eligible_variable_lanes(
    effective_d: float,
    constraints: VariableConstraints,
) -> list[VariableLaneId]:
    """Lanes allowed by D thresholds and constraints (ordered by VARIABLE_LANES)."""
    d = max(0.0, float(effective_d))
    out: list[VariableLaneId] = []
    for lid in VARIABLE_LANES:
        if d + 1e-9 < LANE_MIN_D[lid]:
            continue
        if constraints.only_x and lid != "only_x":
            continue
        if lid == "greek" and not constraints.allow_greek:
            continue
        if constraints.max_variable_lane is not None:
            if _lane_rank(lid) > _lane_rank(constraints.max_variable_lane):
                continue
        out.append(lid)
    if not out:
        out = ["only_x"]
    return out


def _lane_weight(lane: VariableLaneId, effective_d: float) -> float:
    """Bias toward harder (higher min_D) lanes as D rises — same spirit as numbers."""
    from question_engine.frameworks.primitives.difficulty_knobs import fget

    min_d = LANE_MIN_D[lane]
    power = fget("variable_lanes", "weight_hardness_power", 2.2)
    offset = fget("variable_lanes", "weight_staleness_offset", 3.0)
    hardness = (1.0 + min_d) ** power
    staleness = max(0.0, effective_d - min_d - offset)
    return hardness / (1.0 + 0.35 * staleness)


def select_variable_lane(
    effective_d: float,
    *,
    settings: dict[str, Any] | None = None,
    rng: random.Random | None = None,
) -> VariableLaneSelection:
    """Choose a variable lane from D + constraints (or force override)."""
    rng = rng or random.Random()
    settings = settings or {}
    constraints = resolve_variable_constraints(settings)
    d = max(0.0, float(effective_d))

    forced = _forced_lane(settings)
    if forced is not None:
        return VariableLaneSelection(
            profile=forced,
            source="force",
            effective_d=d,
            eligible=(forced,),
            constraints=constraints,
            note=f"forced lane={forced}",
        )

    pool = eligible_variable_lanes(d, constraints)
    weights = [_lane_weight(p, d) for p in pool]
    chosen = rng.choices(pool, weights=weights, k=1)[0]
    return VariableLaneSelection(
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


def _lane_for_locked_letter(name: str) -> VariableLaneId:
    """Pick the narrowest lane that contains the locked letter (metadata only)."""
    for lid in VARIABLE_LANES:
        if name in LANE_POOLS[lid]:
            return lid
    if name in GREEK_LETTERS:
        return "greek"
    return "whole_alphabet"


def sample_variable(
    effective_d: float,
    *,
    settings: dict[str, Any] | None = None,
    rng: random.Random | None = None,
) -> SampledVariable:
    """Sample a variable: pick lane from D+constraints (unless forced/locked), then draw."""
    rng = rng or random.Random()
    settings = dict(settings or {})
    d = max(0.0, float(effective_d))
    constraints = resolve_variable_constraints(settings)

    lock = _normalize_lock(settings.get("lock_variable"))
    if lock:
        profile = _lane_for_locked_letter(lock)
        lane = VariableLaneSelection(
            profile=profile,
            source="lock",
            effective_d=d,
            eligible=(profile,),
            constraints=constraints,
            note=f"lock_variable={lock}",
        )
        return SampledVariable(
            name=lock,
            latex=variable_latex(lock),
            effective_d=effective_d,
            cost=float(VARIABLE_COST.get(lock, LANE_MIN_D.get(profile, 0.0))),
            locked=True,
            profile=profile,
            lane=lane,
        )

    lane = select_variable_lane(effective_d, settings=settings, rng=rng)
    profile = lane.profile
    pool = LANE_POOLS[profile]
    if not pool:
        pool = ("x",)
    name = rng.choice(pool)
    return SampledVariable(
        name=name,
        latex=variable_latex(name),
        effective_d=effective_d,
        cost=float(LANE_MIN_D[profile]),
        locked=False,
        profile=profile,
        lane=lane,
    )


def audit_variable_lane_selection(
    *,
    difficulties: tuple[float, ...] = (0, 2, 4, 6, 8, 10, 12, 14),
    constraint_sets: dict[str, dict[str, Any]] | None = None,
    n_per: int = 8,
    seed: int = 1,
) -> list[dict[str, Any]]:
    """Audit auto variable lane selection: for each D × constraint set, record lanes + letters."""
    if constraint_sets is None:
        constraint_sets = {
            "default": {},
            "only_x": {"only_x": True},
            "no_greek": {"allow_greek": False},
            "max_xyz": {"max_variable_lane": "xyz"},
            "max_common": {"max_variable_lane": "abctuvwxyz"},
            "legacy_no_other_letters": {"allow_other_letters": False},
        }
    rows: list[dict[str, Any]] = []
    for cname, csettings in constraint_sets.items():
        constraints = resolve_variable_constraints(csettings)
        for d in difficulties:
            eligible = eligible_variable_lanes(d, constraints)
            rng = random.Random(seed + int(17 * d) + hash(cname) % 991)
            for i in range(n_per):
                sample = sample_variable(d, settings=csettings, rng=rng)
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
                        "name": sample.name,
                        "latex": sample.latex,
                        "index": i,
                    }
                )
    return rows
