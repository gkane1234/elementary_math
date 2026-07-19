"""Shared algebraic presentation: commute / flip operands + multiply notation.

Schoolbook default is left-to-right order with juxtaposition. Variants unlock
via ``difficulty_knobs.json`` → ``presentation``:

* **Addition / multiplication** — true commute (swap or shuffle operands/factors).
* **Subtraction** — value-preserving rewrite ``a - b`` ↔ ``-(b - a)`` (higher ``min_d``).
* **Division** — value-preserving rewrite ``a/b`` ↔ ``1/(b/a)`` (higher ``min_d``).
* **Explicit multiply** — ``*`` / ``\\cdot`` instead of juxtaposition (mid ``min_d``).
* **Clutter** — identity/redundant traps (``*1``, ``/1``, ``^{1}``, ``^{0}``, extra
  parens, weird monomial order, trivial cancel). Soft ``amount`` scale; **0 = off**.
* **Strangeness** — mix multiply/divide glyphs *within one expression* once
  ``strange_mode`` is sampled on. Distinct from clutter (noise vs inconsistent
  conventions).

Resolve one ``PresentationStyle`` per expression so glyph/order choices stay
consistent (unless strangeness intentionally mixes them).
"""

from __future__ import annotations

import math
import random
import re
from dataclasses import dataclass, replace
from fractions import Fraction
from typing import Any, Mapping, Sequence, TypeVar

from question_engine.frameworks.primitives._algebra_render import (
    coeff_times_var,
    join_signed_terms,
    num_latex,
    sample_integerish,
)
from question_engine.frameworks.primitives.difficulty_knobs import section

T = TypeVar("T")

# Extensible clutter trap ids → default relative weights.
DEFAULT_CLUTTER_OPS: dict[str, float] = {
    "unnecessary_parens": 1.0,
    "mul_by_1": 1.0,
    "weird_monomial": 1.0,
    "div_by_1": 1.0,
    "pow_1": 1.0,
    "pow_0": 1.0,
    "trivial_cancel": 1.0,
}

# Heinous bases for ``(…)ⁿ`` identity clutter (value 1 when n=0).
_HEINOUS_BASES: tuple[tuple[str, str], ...] = (
    (r"(17-16)", "(17-16)"),
    (r"(3+4\cdot 2)", "(3+4*2)"),
    (r"\frac{8}{4}", "(8/4)"),
    (r"(9-7+1)", "(9-7+1)"),
)

_MUL_GLYPHS_STRANGE = ("juxtapose", "*", "cdot", "times")
_DIV_STYLES_STRANGE = ("frac", "slash", "div")


@dataclass(frozen=True)
class PresentationStyle:
    """Resolved once per expression for consistent rendering."""

    commute_add: bool = False
    commute_mul: bool = False
    flip_subtraction: bool = False
    flip_division: bool = False
    explicit_multiply: bool = False
    multiply_symbol: str = "*"  # "*" | "cdot" | "\\cdot"
    # Clutter: soft intensity after D-gating (0 = never apply).
    clutter_amount: float = 0.0
    clutter_ops: tuple[tuple[str, float], ...] = ()
    # Strangeness: mix glyphs when strange_mode is on.
    strangeness_amount: float = 0.0
    strange_mode: bool = False

    # Back-compat aliases used by early call sites / tests
    @property
    def commute_summands(self) -> bool:
        return self.commute_add

    @property
    def commute_factors(self) -> bool:
        return self.commute_mul

    @property
    def mul_latex(self) -> str:
        sym = self.multiply_symbol.strip()
        if sym in {"cdot", "\\cdot", "·"}:
            return "\\cdot"
        return "*"

    @property
    def mul_text(self) -> str:
        return "*"

    def clutter_op_weights(self) -> dict[str, float]:
        if self.clutter_ops:
            return {k: float(w) for k, w in self.clutter_ops if float(w) > 0}
        return {k: float(w) for k, w in DEFAULT_CLUTTER_OPS.items() if float(w) > 0}

    @staticmethod
    def schoolbook() -> PresentationStyle:
        return PresentationStyle()


def _chance(obj: dict[str, Any], key: str, default: float) -> float:
    try:
        return float(obj.get(key, default))
    except (TypeError, ValueError):
        return float(default)


def _gate(
    sec: dict[str, Any],
    key: str,
    *,
    d: float,
    default_min_d: float,
    default_chance: float,
    default_enabled: bool = True,
) -> tuple[bool, float, float, bool]:
    """Return (enabled, min_d, chance, fired_defaults_unused) config for a gated knob."""
    raw = sec.get(key) or {}
    if not isinstance(raw, dict):
        return default_enabled, default_min_d, default_chance, True
    enabled = bool(raw.get("enabled", default_enabled))
    min_d = _chance(raw, "min_d", default_min_d)
    chance = _chance(raw, "chance", default_chance)
    return enabled, min_d, chance, True


def _bernoulli_gated(
    rng: random.Random,
    d: float,
    *,
    enabled: bool,
    min_d: float,
    chance: float,
    force: bool | None = None,
) -> bool:
    if force is not None:
        return bool(force)
    return bool(enabled and float(d) >= min_d and rng.random() < chance)


def _d_factor(d: float, min_d: float) -> float:
    """Topic-D scale in ~[0.35, 1.325] once ``d >= min_d``."""
    return 0.35 + 0.65 * min(1.5, max(0.0, (float(d) - float(min_d)) / 12.0))


def _soft_intensity(amount: float, d: float, min_d: float) -> float:
    """Map soft ``amount`` × D into intensity; **amount≤0 or d<min_d → 0**."""
    if float(amount) <= 0.0 or float(d) < float(min_d):
        return 0.0
    return float(amount) * _d_factor(d, min_d)


def clutter_site_chance(style: PresentationStyle) -> float:
    """Per render-site probability of applying one clutter trap."""
    if style.clutter_amount <= 0:
        return 0.0
    return 1.0 - math.exp(-style.clutter_amount)


def _parse_amount_block(
    sec: dict[str, Any],
    key: str,
    ov: Mapping[str, Any],
    *,
    d: float,
) -> tuple[float, float, dict[str, float]]:
    """Return (intensity, raw_amount, ops_weights) for clutter / strangeness blocks."""
    raw = sec.get(key) if isinstance(sec.get(key), dict) else {}
    block: dict[str, Any] = dict(raw or {})
    ov_block = ov.get(key)
    if isinstance(ov_block, dict):
        block.update(ov_block)
    elif ov_block is not None and key == "clutter":
        # Allow ``clutter: 0`` style force-off.
        try:
            block["amount"] = float(ov_block)
        except (TypeError, ValueError):
            pass

    amount = _chance(block, "amount", 0.0)
    min_d = _chance(block, "min_d", 0.0)
    intensity = _soft_intensity(amount, d, min_d)

    ops: dict[str, float] = dict(DEFAULT_CLUTTER_OPS)
    ops_raw = block.get("ops")
    if isinstance(ops_raw, dict):
        ops = {}
        for name, weight in ops_raw.items():
            if str(name).startswith("_"):
                continue
            try:
                w = float(weight)
            except (TypeError, ValueError):
                continue
            if w > 0:
                ops[str(name)] = w
    return intensity, amount, ops


def resolve_presentation(
    rng: random.Random,
    d: float = 0.0,
    *,
    overrides: dict[str, Any] | None = None,
) -> PresentationStyle:
    """Sample presentation knobs for difficulty ``d``."""
    sec = section("presentation")
    ov = dict(overrides or {})

    add_chance = _chance(sec, "commute_add_chance", _chance(sec, "commute_summands_chance", 0.45))
    mul_chance = _chance(sec, "commute_mul_chance", _chance(sec, "commute_factors_chance", 0.45))
    if "commute_add_chance" in ov:
        add_chance = float(ov["commute_add_chance"])
    if "commute_summands_chance" in ov:
        add_chance = float(ov["commute_summands_chance"])
    if "commute_mul_chance" in ov:
        mul_chance = float(ov["commute_mul_chance"])
    if "commute_factors_chance" in ov:
        mul_chance = float(ov["commute_factors_chance"])

    if "commute_add" in ov:
        commute_add = bool(ov["commute_add"])
    elif "commute_summands" in ov:
        commute_add = bool(ov["commute_summands"])
    else:
        commute_add = rng.random() < add_chance

    if "commute_mul" in ov:
        commute_mul = bool(ov["commute_mul"])
    elif "commute_factors" in ov:
        commute_mul = bool(ov["commute_factors"])
    else:
        commute_mul = rng.random() < mul_chance

    sub_en, sub_min, sub_ch, _ = _gate(
        sec, "flip_subtraction", d=d, default_min_d=10.0, default_chance=0.2
    )
    div_en, div_min, div_ch, _ = _gate(
        sec, "flip_division", d=d, default_min_d=12.0, default_chance=0.15
    )
    em_en, em_min, em_ch, _ = _gate(
        sec, "explicit_multiply", d=d, default_min_d=8.0, default_chance=0.35
    )

    em = sec.get("explicit_multiply") if isinstance(sec.get("explicit_multiply"), dict) else {}
    symbol = str((em or {}).get("symbol", "*") or "*")

    sub_force = ov.get("flip_subtraction")
    if isinstance(sub_force, dict):
        if "force" in sub_force:
            flip_sub = bool(sub_force["force"])
        else:
            if "enabled" in sub_force:
                sub_en = bool(sub_force["enabled"])
            if "min_d" in sub_force:
                sub_min = float(sub_force["min_d"])
            if "chance" in sub_force:
                sub_ch = float(sub_force["chance"])
            flip_sub = _bernoulli_gated(
                rng, d, enabled=sub_en, min_d=sub_min, chance=sub_ch
            )
    elif sub_force is not None:
        flip_sub = bool(sub_force)
    else:
        flip_sub = _bernoulli_gated(rng, d, enabled=sub_en, min_d=sub_min, chance=sub_ch)

    div_force = ov.get("flip_division")
    if isinstance(div_force, dict):
        if "force" in div_force:
            flip_div = bool(div_force["force"])
        else:
            if "enabled" in div_force:
                div_en = bool(div_force["enabled"])
            if "min_d" in div_force:
                div_min = float(div_force["min_d"])
            if "chance" in div_force:
                div_ch = float(div_force["chance"])
            flip_div = _bernoulli_gated(
                rng, d, enabled=div_en, min_d=div_min, chance=div_ch
            )
    elif div_force is not None:
        flip_div = bool(div_force)
    else:
        flip_div = _bernoulli_gated(rng, d, enabled=div_en, min_d=div_min, chance=div_ch)

    em_force = ov.get("explicit_multiply")
    if isinstance(em_force, dict):
        if "symbol" in em_force:
            symbol = str(em_force["symbol"])
        if "force" in em_force:
            explicit = bool(em_force["force"])
        else:
            if "enabled" in em_force:
                em_en = bool(em_force["enabled"])
            if "min_d" in em_force:
                em_min = float(em_force["min_d"])
            if "chance" in em_force:
                em_ch = float(em_force["chance"])
            explicit = _bernoulli_gated(
                rng, d, enabled=em_en, min_d=em_min, chance=em_ch
            )
    elif em_force is not None:
        explicit = bool(em_force)
    else:
        explicit = _bernoulli_gated(rng, d, enabled=em_en, min_d=em_min, chance=em_ch)

    if "multiply_symbol" in ov:
        symbol = str(ov["multiply_symbol"])

    clutter_intensity, _clutter_raw, clutter_ops = _parse_amount_block(
        sec, "clutter", ov, d=d
    )
    strange_intensity, _strange_raw, _ = _parse_amount_block(
        sec, "strangeness", ov, d=d
    )

    # Sample strange_mode once: soft amount → Bernoulli with intensity-shaped chance.
    if "strange_mode" in ov:
        strange_mode = bool(ov["strange_mode"])
    elif strange_intensity <= 0:
        strange_mode = False
    else:
        strange_mode = rng.random() < (1.0 - math.exp(-strange_intensity))

    ops_tuple = tuple(sorted((k, float(v)) for k, v in clutter_ops.items()))

    return PresentationStyle(
        commute_add=commute_add,
        commute_mul=commute_mul,
        flip_subtraction=flip_sub,
        flip_division=flip_div,
        explicit_multiply=explicit,
        multiply_symbol=symbol,
        clutter_amount=clutter_intensity,
        clutter_ops=ops_tuple,
        strangeness_amount=strange_intensity,
        strange_mode=strange_mode,
    )


def presentation_for_ctx(
    ctx: Any,
    *,
    d: float | None = None,
    primitive_id: str | None = None,
    overrides: dict[str, Any] | None = None,
    reuse: bool = True,
) -> PresentationStyle:
    """Resolve style from a ``PrimitiveContext``; optionally reuse for the item."""
    if reuse:
        cached = getattr(ctx, "_presentation_style", None)
        if isinstance(cached, PresentationStyle) and overrides is None:
            return cached

    if d is not None:
        eff = float(d)
    elif primitive_id is not None:
        eff = float(ctx.effective_d(primitive_id))
    else:
        eff = float(getattr(ctx, "topic_d", 0.0) or 0.0)

    settings_ov: dict[str, Any] = {}
    settings = getattr(ctx, "settings", None)
    if isinstance(settings, dict) and isinstance(settings.get("presentation"), dict):
        settings_ov.update(settings["presentation"])
    # Also allow flat settings on build_context input via prereq-less key on plan — skip.
    if overrides:
        settings_ov.update(overrides)

    style = resolve_presentation(ctx.rng, eff, overrides=settings_ov or None)
    try:
        ctx._presentation_style = style
    except Exception:
        pass
    return style


def order_commutative(
    items: Sequence[T],
    *,
    commute: bool,
    rng: random.Random,
) -> list[T]:
    """Schoolbook order, or commute when requested (swap pair / shuffle longer)."""
    out = list(items)
    if not commute or len(out) <= 1:
        return out
    if len(out) == 2:
        return [out[1], out[0]]
    rng.shuffle(out)
    return out


def join_signed_display(
    terms: Sequence[tuple[str, str, Fraction]],
) -> tuple[str, str]:
    """Join ``(latex, text, signed_value)`` with schoolbook +/− spelling."""
    if not terms:
        return "0", "0"
    first_l, first_t, _first_v = terms[0]
    latex, text = first_l, first_t
    for t_l, t_t, t_v in terms[1:]:
        if t_v < 0:
            bare_l = t_l[1:] if t_l.startswith("-") else t_l
            bare_t = t_t[1:] if t_t.startswith("-") else t_t
            latex = f"{latex} - {bare_l}"
            text = f"{text} - {bare_t}"
        else:
            latex = f"{latex} + {t_l}"
            text = f"{text} + {t_t}"
    return latex, text


@dataclass(frozen=True)
class DisplayPiece:
    latex: str
    text: str


# Alias used by distributive / product helpers
FactorPiece = DisplayPiece


# --- Clutter transforms (value-preserving) ------------------------------------


def _pick_clutter_op(style: PresentationStyle, rng: random.Random) -> str | None:
    weights = style.clutter_op_weights()
    if not weights:
        return None
    names = list(weights.keys())
    ws = [weights[n] for n in names]
    return rng.choices(names, weights=ws, k=1)[0]


def _apply_clutter_op(
    piece: DisplayPiece,
    op: str,
    rng: random.Random,
) -> DisplayPiece:
    """Apply one identity/clutter trap. Unknown ops are no-ops (extensible)."""
    if op == "unnecessary_parens":
        return DisplayPiece(
            latex=rf"\left({piece.latex}\right)",
            text=f"({piece.text})",
        )
    if op == "mul_by_1":
        if rng.random() < 0.5:
            return DisplayPiece(
                latex=rf"1\cdot {piece.latex}",
                text=f"1*{piece.text}",
            )
        return DisplayPiece(
            latex=rf"{piece.latex}\cdot 1",
            text=f"{piece.text}*1",
        )
    if op == "div_by_1":
        return DisplayPiece(
            latex=rf"\frac{{{piece.latex}}}{{1}}",
            text=f"({piece.text})/1",
        )
    if op == "pow_1":
        return DisplayPiece(
            latex=rf"\left({piece.latex}\right)^{{1}}",
            text=f"({piece.text})^1",
        )
    if op == "pow_0":
        base_l, base_t = rng.choice(_HEINOUS_BASES)
        # Multiply by (heinous)^0 ≡ 1.
        if rng.random() < 0.5:
            return DisplayPiece(
                latex=rf"{piece.latex}\cdot {base_l}^{{0}}",
                text=f"{piece.text}*{base_t}^0",
            )
        return DisplayPiece(
            latex=rf"{base_l}^{{0}}\cdot {piece.latex}",
            text=f"{base_t}^0*{piece.text}",
        )
    if op == "trivial_cancel":
        k = rng.randint(2, 9)
        if rng.random() < 0.5:
            return DisplayPiece(
                latex=rf"\frac{{{piece.latex}\cdot {k}}}{{{k}}}",
                text=f"({piece.text}*{k})/{k}",
            )
        return DisplayPiece(
            latex=rf"{piece.latex}\cdot \frac{{{k}}}{{{k}}}",
            text=f"{piece.text}*({k}/{k})",
        )
    if op == "weird_monomial":
        return _weird_monomial(piece, rng)
    return piece


_MONOMIAL_RE = re.compile(
    r"^(?P<sign>-?)(?P<coef>\d+(?:/\d+)?)(?P<vars>[A-Za-z\\].*)$"
)
_MONOMIAL_TEXT_RE = re.compile(
    r"^(?P<sign>-?)(?P<coef>\d+(?:/\d+)?)(?P<vars>[A-Za-z].*)$"
)


def _weird_monomial(piece: DisplayPiece, rng: random.Random) -> DisplayPiece:
    """Non-schoolbook coeff/var order, e.g. ``3x`` → ``x3``."""
    ml = _MONOMIAL_RE.match(piece.latex.strip())
    mt = _MONOMIAL_TEXT_RE.match(piece.text.strip())
    if not ml or not mt:
        # Fallback: wrap with mul-by-1 style noise that still looks "off".
        return DisplayPiece(
            latex=rf"{piece.latex}\cdot 1",
            text=f"{piece.text}*1",
        )
    sign, coef, vars_l = ml.group("sign"), ml.group("coef"), ml.group("vars")
    _, _, vars_t = mt.group("sign"), mt.group("coef"), mt.group("vars")
    mode = rng.choice(["var_then_coef", "coef_mid", "split_stars"])
    if mode == "var_then_coef":
        return DisplayPiece(
            latex=f"{sign}{vars_l}{coef}",
            text=f"{sign}{vars_t}{coef}",
        )
    if mode == "coef_mid" and len(vars_t) >= 2 and vars_t.isalpha():
        # e.g. xy with coeff → x3y style
        mid = rng.randint(1, len(vars_t) - 1)
        return DisplayPiece(
            latex=f"{sign}{vars_l[:mid]}{coef}{vars_l[mid:]}",
            text=f"{sign}{vars_t[:mid]}{coef}{vars_t[mid:]}",
        )
    # Explicit but odd: var * coef
    return DisplayPiece(
        latex=f"{sign}{vars_l}\\cdot {coef}",
        text=f"{sign}{vars_t}*{coef}",
    )


def maybe_clutter(
    piece: DisplayPiece,
    style: PresentationStyle,
    rng: random.Random,
) -> DisplayPiece:
    """With site chance, apply one clutter trap (value-preserving)."""
    p = clutter_site_chance(style)
    if p <= 0 or rng.random() >= p:
        return piece
    op = _pick_clutter_op(style, rng)
    if op is None:
        return piece
    return _apply_clutter_op(piece, op, rng)


def maybe_clutter_result(
    latex: str,
    text: str,
    style: PresentationStyle,
    rng: random.Random,
) -> tuple[str, str]:
    """Optionally clutter a finished (latex, text) pair."""
    out = maybe_clutter(DisplayPiece(latex, text), style, rng)
    return out.latex, out.text


# --- Multiply / divide glyph helpers (strangeness) ----------------------------


def _mul_sep(glyph: str) -> tuple[str, str]:
    """Return (latex_sep, text_sep) for a multiply glyph token."""
    if glyph == "juxtapose":
        return "", ""
    if glyph == "cdot":
        return " \\cdot ", "*"
    if glyph == "times":
        return " \\times ", "*"
    # "*" and default
    return " * ", "*"


def _pick_mul_glyph(style: PresentationStyle, rng: random.Random) -> str:
    if style.strange_mode:
        return rng.choice(_MUL_GLYPHS_STRANGE)
    if style.explicit_multiply:
        sym = style.multiply_symbol.strip()
        if sym in {"cdot", "\\cdot", "·"}:
            return "cdot"
        return "*"
    return "juxtapose"


def _join_factors_strange(
    factors: Sequence[DisplayPiece],
    rng: random.Random,
) -> tuple[str, str]:
    """Join factors using mixed multiply glyphs across the product."""
    if not factors:
        return "1", "1"
    if len(factors) == 1:
        return factors[0].latex, factors[0].text

    glyphs = [rng.choice(_MUL_GLYPHS_STRANGE) for _ in range(len(factors) - 1)]
    # Encourage real mixing when there are ≥2 joins.
    if len(glyphs) >= 2 and len(set(glyphs)) == 1:
        alt = [g for g in _MUL_GLYPHS_STRANGE if g != glyphs[0]]
        glyphs[1] = rng.choice(alt)

    latex = factors[0].latex
    text = factors[0].text
    for i, f in enumerate(factors[1:]):
        sep_l, sep_t = _mul_sep(glyphs[i])
        if sep_l == "":
            latex = f"{latex}{f.latex}"
            text = f"{text}{f.text}"
        else:
            latex = f"{latex}{sep_l}{f.latex}"
            text = f"{text}{sep_t}{f.text}"
    return latex, text


def render_addition(
    left: DisplayPiece,
    right: DisplayPiece,
    style: PresentationStyle,
    rng: random.Random,
) -> tuple[str, str]:
    """``a + b`` with optional commute + clutter."""
    a, b = order_commutative([left, right], commute=style.commute_add, rng=rng)
    a = maybe_clutter(a, style, rng)
    b = maybe_clutter(b, style, rng)
    return maybe_clutter_result(f"{a.latex} + {b.latex}", f"{a.text} + {b.text}", style, rng)


def render_subtraction(
    left: DisplayPiece,
    right: DisplayPiece,
    style: PresentationStyle,
    rng: random.Random | None = None,
) -> tuple[str, str]:
    """``a - b``, or ``-(b - a)`` when ``flip_subtraction`` is set."""
    # rng optional for back-compat with older call sites that omit it.
    _rng = rng if rng is not None else random.Random(0)
    if style.flip_subtraction:
        latex = f"-\\left({right.latex} - {left.latex}\\right)"
        text = f"-({right.text} - {left.text})"
    else:
        latex = f"{left.latex} - {right.latex}"
        text = f"{left.text} - {right.text}"
    if style.clutter_amount > 0:
        return maybe_clutter_result(latex, text, style, _rng)
    return latex, text


def render_product(
    factors: Sequence[DisplayPiece],
    style: PresentationStyle,
    rng: random.Random,
) -> tuple[str, str]:
    """Multiply factors with optional commute + juxtaposition / explicit / strange glyphs."""
    ordered = order_commutative(list(factors), commute=style.commute_mul, rng=rng)
    # Clutter: sometimes inject ×1 before joining.
    if (
        style.clutter_amount > 0
        and "mul_by_1" in style.clutter_op_weights()
        and rng.random() < clutter_site_chance(style) * 0.5
    ):
        one = DisplayPiece("1", "1")
        if rng.random() < 0.5:
            ordered = [one, *ordered]
        else:
            ordered = [*ordered, one]

    if not ordered:
        return "1", "1"
    if len(ordered) == 1:
        only = maybe_clutter(ordered[0], style, rng)
        return only.latex, only.text

    ordered = [maybe_clutter(f, style, rng) for f in ordered]

    if style.strange_mode:
        latex, text = _join_factors_strange(ordered, rng)
        return maybe_clutter_result(latex, text, style, rng)

    glyph = _pick_mul_glyph(style, rng)
    if glyph == "juxtapose":
        # Bare "-3" after a factor reads as subtraction: (x+1)-3. Wrap signed factors.
        safe_l = [_juxtapose_factor_latex(f.latex, i > 0) for i, f in enumerate(ordered)]
        safe_t = [_juxtapose_factor_text(f.text, i > 0) for i, f in enumerate(ordered)]
        latex = "".join(safe_l)
        text = "".join(safe_t)
    else:
        sep_l, sep_t = _mul_sep(glyph)
        latex = sep_l.join(f.latex for f in ordered)
        text = sep_t.join(f.text for f in ordered)
    return maybe_clutter_result(latex, text, style, rng)


def _juxtapose_factor_latex(latex: str, needs_wrap_if_signed: bool) -> str:
    s = latex.strip()
    if needs_wrap_if_signed and s.startswith("-") and not (
        s.startswith("\\left(") or s.startswith("(")
    ):
        return f"\\left({s}\\right)"
    return latex


def _juxtapose_factor_text(text: str, needs_wrap_if_signed: bool) -> str:
    s = text.strip()
    if needs_wrap_if_signed and s.startswith("-") and not s.startswith("("):
        return f"({s})"
    return text


def render_division(
    numer: DisplayPiece,
    denom: DisplayPiece,
    style: PresentationStyle,
    rng: random.Random | None = None,
) -> tuple[str, str]:
    """``a/b``, or ``1/(b/a)`` when ``flip_division`` is set (same value).

    With ``strange_mode``, mix ``\\frac``, ``/``, and ``\\div`` across calls.
    """
    _rng = rng if rng is not None else random.Random(0)
    n = maybe_clutter(numer, style, _rng) if style.clutter_amount > 0 else numer
    d = maybe_clutter(denom, style, _rng) if style.clutter_amount > 0 else denom

    if style.flip_division:
        latex = rf"\frac{{1}}{{\frac{{{d.latex}}}{{{n.latex}}}}}"
        text = f"1/({d.text}/{n.text})"
        return maybe_clutter_result(latex, text, style, _rng) if style.clutter_amount > 0 else (
            latex,
            text,
        )

    if style.strange_mode:
        kind = _rng.choice(_DIV_STYLES_STRANGE)
        if kind == "slash":
            latex, text = f"{n.latex}/{d.latex}", f"{n.text}/{d.text}"
        elif kind == "div":
            latex = f"{n.latex} \\div {d.latex}"
            text = f"{n.text} \\div {d.text}"
        else:
            latex = rf"\frac{{{n.latex}}}{{{d.latex}}}"
            text = f"{n.text}/{d.text}"
        return maybe_clutter_result(latex, text, style, _rng) if style.clutter_amount > 0 else (
            latex,
            text,
        )

    latex = rf"\frac{{{n.latex}}}{{{d.latex}}}"
    text = f"{n.text}/{d.text}"
    return maybe_clutter_result(latex, text, style, _rng) if style.clutter_amount > 0 else (
        latex,
        text,
    )


def render_scaled_sum(
    outer: DisplayPiece,
    summands: Sequence[tuple[str, str, Fraction]],
    style: PresentationStyle,
    rng: random.Random,
) -> tuple[str, str]:
    """Render ``outer * (sum…)`` with add-commute + mul-commute + multiply glyph."""
    ordered = order_commutative(summands, commute=style.commute_add, rng=rng)
    inner_l, inner_t = join_signed_display(ordered)
    group = DisplayPiece(
        latex=f"\\left({inner_l}\\right)",
        text=f"({inner_t})",
    )
    return render_product([outer, group], style, rng)


def expand_scaled_sum_latex(
    outer_latex: str,
    summands: Sequence[tuple[str, Fraction]],
) -> str:
    """Answer-key expansion ``a·b + a·c`` (always ``\\cdot``)."""
    parts: list[str] = []
    for term_l, term_v in summands:
        body = term_l[1:] if term_v < 0 and term_l.startswith("-") else term_l
        if term_v < 0:
            parts.append(f"- {outer_latex}\\cdot {body}")
        else:
            parts.append(f"{outer_latex}\\cdot {body}")
    if not parts:
        return "0"
    out = parts[0]
    for p in parts[1:]:
        if p.startswith("- "):
            out = f"{out} - {p[2:]}"
        else:
            out = f"{out} + {p}"
    return out


# --- Cancel clutter (value-preserving +k−k / +kx−kx / distrib pairs) ----------
#
# Shared by constructive affine presentation (and clients like distributive).
# Soft intensity from ``presentation.cancel_clutter``; topic sections (e.g.
# ``distributive.cancel_clutter``) may override. amount≤0 → off.

_CANCEL_KINDS: tuple[str, ...] = (
    "numeric",  # +k − k
    "affine",  # +kx − kx
    "distrib_expanded",  # a(x+b) vs (ax+ab)
    "distrib_commute",  # a(x+b) vs a(b+x)
)


def cancel_clutter_intensity(
    d: float,
    *,
    overrides: dict[str, Any] | None = None,
    settings: dict[str, Any] | None = None,
) -> float:
    """Soft intensity for cancel clutter; **amount≤0 or d<min_d → 0**."""
    block = _resolve_cancel_clutter_block(overrides=overrides, settings=settings)
    amount = _chance(block, "amount", 0.0)
    min_d = _chance(block, "min_d", 10.0)
    return _soft_intensity(amount, d, min_d)


def cancel_clutter_chance(intensity: float) -> float:
    """Probability of injecting ≥1 cancel group given soft intensity."""
    if intensity <= 0:
        return 0.0
    return 1.0 - math.exp(-intensity)


def _resolve_cancel_clutter_block(
    *,
    overrides: dict[str, Any] | None = None,
    settings: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Merge presentation defaults ← constructive ← distributive ← settings/overrides."""
    block: dict[str, Any] = {}

    def _apply_ov(ov: Any) -> None:
        if isinstance(ov, dict):
            block.update(ov)
        elif ov is not None:
            try:
                block["amount"] = float(ov)
            except (TypeError, ValueError):
                pass

    for sec_name in ("presentation", "constructive", "distributive"):
        sec = section(sec_name)
        raw = sec.get("cancel_clutter") if isinstance(sec.get("cancel_clutter"), dict) else None
        if raw:
            _apply_ov(raw)

    settings = settings or {}
    for key in ("presentation", "constructive", "distributive"):
        nested = settings.get(key)
        if isinstance(nested, dict):
            _apply_ov(nested.get("cancel_clutter"))
    if "cancel_clutter" in settings:
        _apply_ov(settings.get("cancel_clutter"))
    if overrides:
        if "cancel_clutter" in overrides:
            _apply_ov(overrides.get("cancel_clutter"))
        elif "amount" in overrides or "min_d" in overrides:
            _apply_ov(overrides)
    return block


def _is_bare_sum(text: str) -> bool:
    """True for unparenthesized top-level sums like ``3x + 6`` (not ``3(x + 2)``)."""
    s = text.strip()
    if s.startswith("("):
        return False
    depth = 0
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        elif depth == 0 and i + 2 < len(s) and s[i : i + 3] in {" + ", " - "}:
            return True
        i += 1
    return False


def _paren_if_sum(latex: str, text: str) -> tuple[str, str]:
    if _is_bare_sum(text):
        return f"\\left({latex}\\right)", f"({text})"
    return latex, text


def _sample_nonzero_coef_latex(ctx: Any, *, min_abs: int = 1) -> tuple[Fraction, str]:
    """Integer coefficient with ``|value| >= min_abs`` → (value, latex)."""
    for _ in range(16):
        k = sample_integerish(ctx, exclude_zero=True, prefer_positive=True)
        if abs(k.value) >= min_abs:
            return k.value, k.latex
    forced = Fraction(ctx.rng.choice([2, 3, 4, 5]))
    return forced, num_latex(forced)


def _sample_cancel_group(
    ctx: Any,
    style: PresentationStyle,
    var_latex: str,
    var_text: str,
) -> tuple[str, DisplayPiece]:
    """Return (kind, parenthesized zero-sum group)."""
    kind = ctx.rng.choice(_CANCEL_KINDS)
    if kind == "numeric":
        _val, body = _sample_nonzero_coef_latex(ctx, min_abs=1)
        left_l, left_t = body, body
        right_l, right_t = body, body
    elif kind == "affine":
        coef, _ = _sample_nonzero_coef_latex(ctx, min_abs=1)
        coef = abs(coef)
        body_l = coeff_times_var(coef, var_latex)
        body_t = coeff_times_var(coef, var_text)
        left_l, left_t = body_l, body_t
        right_l, right_t = body_l, body_t
    elif kind == "distrib_commute":
        a_val, a_l = _sample_nonzero_coef_latex(ctx, min_abs=2)
        b = sample_integerish(ctx, exclude_zero=True)
        style_fixed = replace(style, commute_add=False)
        outer = DisplayPiece(a_l, a_l)
        s1 = [(var_latex, var_text, Fraction(1)), (b.latex, b.latex, b.value)]
        s2 = [(b.latex, b.latex, b.value), (var_latex, var_text, Fraction(1))]
        left_l, left_t = render_scaled_sum(outer, s1, style_fixed, ctx.rng)
        right_l, right_t = render_scaled_sum(outer, s2, style_fixed, ctx.rng)
        _ = a_val  # sampled for |a|≥2; latex already on outer
    else:  # distrib_expanded
        a_val, a_l = _sample_nonzero_coef_latex(ctx, min_abs=2)
        b = sample_integerish(ctx, exclude_zero=True)
        style_fixed = replace(style, commute_add=False)
        outer = DisplayPiece(a_l, a_l)
        summands = [(var_latex, var_text, Fraction(1)), (b.latex, b.latex, b.value)]
        dist_l, dist_t = render_scaled_sum(outer, summands, style_fixed, ctx.rng)
        exp_l, _ = join_signed_terms([(a_val, var_latex), (a_val * b.value, "")])
        exp_t_plain, _ = join_signed_terms([(a_val, var_text), (a_val * b.value, "")])
        exp_l, exp_t = _paren_if_sum(exp_l, exp_t_plain)
        left_l, left_t = dist_l, dist_t
        right_l, right_t = exp_l, exp_t

    # Vary which canceling side appears first (still sums to 0).
    if style.commute_add and ctx.rng.random() < 0.5:
        left_l, right_l = right_l, left_l
        left_t, right_t = right_t, left_t

    # Subtrahend that is a bare top-level sum needs parens so minus binds correctly.
    if _is_bare_sum(right_t):
        right_l, right_t = f"\\left({right_l}\\right)", f"({right_t})"

    group = DisplayPiece(
        latex=f"\\left({left_l} - {right_l}\\right)",
        text=f"({left_t} - {right_t})",
    )
    return kind, group


def maybe_inject_cancel_clutter(
    ctx: Any,
    style: PresentationStyle,
    *,
    var_latex: str,
    var_text: str,
    core_latex: str,
    core_text: str,
    d: float,
    settings: dict[str, Any] | None = None,
) -> tuple[str, str, tuple[str, ...]]:
    """Optionally append zero-sum cancel groups; commute with the core chunk.

    Returns ``(latex, text, tags)`` where tags look like ``cancel:numeric``.
    Intensity comes from knobs/settings; callers gate with ``ExpressionScope``.
    """
    settings = settings if settings is not None else (
        ctx.settings if isinstance(getattr(ctx, "settings", None), dict) else {}
    )
    intensity = cancel_clutter_intensity(d, settings=settings)
    if intensity <= 0 or ctx.rng.random() >= cancel_clutter_chance(intensity):
        return core_latex, core_text, ()

    n_groups = 1
    if intensity >= 1.0 and ctx.rng.random() < min(0.45, intensity / 3.0):
        n_groups = 2

    terms: list[tuple[str, str, Fraction]] = [
        (core_latex, core_text, Fraction(1)),
    ]
    tags: list[str] = []
    for _ in range(n_groups):
        kind, group = _sample_cancel_group(ctx, style, var_latex, var_text)
        terms.append((group.latex, group.text, Fraction(1)))
        tags.append(f"cancel:{kind}")

    ordered = order_commutative(terms, commute=style.commute_add, rng=ctx.rng)
    latex, text = join_signed_display(ordered)
    return latex, text, tuple(tags)
