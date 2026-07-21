"""Word-problem template framework — narrative prompts with numeric slots."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Callable

from .base import QuestionFramework
from ..generators.utils import random_int_range
from ..word_problems.names import pick_name, pick_names

SlotSampler = Callable[[dict], tuple[str, str | None]]

_LETTERS = ("A", "B", "C", "D")


@dataclass
class WordProblemTemplate:
    """Declarative word-problem shell with injectable numeric slots."""

    template_latex: str
    template_text: str
    variable_slots: dict[str, SlotSampler] = field(default_factory=dict)
    answer_slot: str | None = None

    def render(self, settings: dict) -> tuple[str, str, str | None]:
        values: dict[str, str] = {}
        answer: str | None = None
        for name, sampler in self.variable_slots.items():
            display, slot_answer = sampler(settings)
            values[name] = display
            if self.answer_slot == name and slot_answer is not None:
                answer = slot_answer
        latex = self.template_latex.format(**values)
        text = self.template_text.format(**values)
        return latex, text, answer


def _topic_d(settings: dict) -> float:
    """Continuous difficulty (0–24+); shims legacy easy/medium/hard strings."""
    from .difficulty_budget import settings_difficulty

    return settings_difficulty(settings, default=8.0)


def _band_from_d(d: float) -> str:
    from .difficulty_budget import difficulty_band

    return difficulty_band(d)


def _difficulty_range(settings: dict) -> tuple[int, int]:
    raw = settings.get("difficulty", "medium")
    try:
        d = float(raw)
        if d <= 4.0:
            return 2, 12
        if d <= 11.0:
            return 5, 30
        return 10, 60
    except (TypeError, ValueError):
        pass
    difficulty = str(raw).strip().lower()
    if difficulty == "easy":
        return 2, 12
    if difficulty == "hard":
        return 10, 50
    return 5, 25


def _pick_names(settings: dict, count: int = 1) -> list[str]:
    """Resolve ``name_style`` into ``count`` display labels for a problem."""
    style = str(settings.get("name_style", "names"))
    if style == "letters":
        return [_LETTERS[i % len(_LETTERS)] for i in range(count)]
    if style == "person_a_b":
        return [f"Person {chr(ord('A') + i)}" for i in range(count)]
    return pick_names(count)


def _pick_name(settings: dict, *, index: int = 0) -> str:
    style = str(settings.get("name_style", "names"))
    if style == "letters":
        return _LETTERS[index % len(_LETTERS)]
    if style == "person_a_b":
        return "Person A" if index == 0 else "Person B"
    return pick_name()


def _format_answer(value: float | int, settings: dict) -> str:
    if bool(settings.get("integer_only_answers", True)):
        value = int(round(value))
        return str(value)
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.1f}".rstrip("0").rstrip(".")


def _append_units(answer: str, settings: dict) -> str:
    units = str(settings.get("answer_units", ""))
    if not units:
        return answer
    if units == "dollars":
        return f"\\${answer}" if answer.startswith("\\") else f"${answer}"
    return f"{answer} {units}"


def _unit_label(settings: dict, default: str) -> str:
    if not bool(settings.get("show_unit_labels", True)):
        return ""
    units = str(settings.get("answer_units", ""))
    return units or default


def _random_value(settings: dict, *, lo: int | None = None, hi: int | None = None) -> int:
    default_lo, default_hi = _difficulty_range(settings)
    minimum = lo if lo is not None else default_lo
    maximum = hi if hi is not None else default_hi
    return random_int_range(minimum, maximum)


def _tier(settings: dict) -> str:
    raw = settings.get("difficulty_tier") or settings.get("difficulty") or "medium"
    try:
        return _band_from_d(float(raw))
    except (TypeError, ValueError):
        pass
    value = str(raw).strip().lower()
    return value if value in {"easy", "medium", "hard"} else "medium"


def _as_decimal(value: int | float | str | Decimal) -> Decimal:
    return value if isinstance(value, Decimal) else Decimal(str(value))


def _round_money(amount: Decimal) -> Decimal:
    """Round half-up to cents — matches typical calculator money mode."""
    return _as_decimal(amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _format_money(amount: Decimal) -> str:
    return f"{_round_money(amount):.2f}"


def _display_money(amount: Decimal) -> str:
    """Prompt dollars: omit trailing .00 for whole-dollar prices."""
    rounded = _round_money(amount)
    if rounded == rounded.to_integral_value():
        return str(int(rounded))
    return f"{rounded:.2f}"


def _display_rate(rate: Decimal) -> str:
    normalized = _as_decimal(rate).normalize()
    if normalized == normalized.to_integral_value():
        return str(int(normalized))
    text = format(normalized, "f")
    return text.rstrip("0").rstrip(".") if "." in text else text


def _percent_of(price: Decimal, rate: Decimal) -> Decimal:
    return _round_money(price * rate / Decimal(100))


def _apply_rate_factor(price: Decimal, factor: Decimal) -> Decimal:
    return _round_money(price * factor)


class WordProblemFramework(QuestionFramework):
    """Batch generation wrapper around a word-problem template or subclass."""

    problem_kind: str = "generic"

    def __init__(self, template: WordProblemTemplate | None = None):
        self.template = template

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {
            "difficulty": settings.get("difficulty", "medium"),
            "answer_units": settings.get("answer_units", ""),
            "problem_kind": self.problem_kind,
            "max_steps": int(settings.get("max_steps", 2)),
        }

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        if self.template is None:
            raise NotImplementedError(
                f"{self.__class__.__name__} requires build_prompt or a WordProblemTemplate."
            )
        latex, text, answer = self.template.render(settings)
        if answer is not None:
            answer = _append_units(answer, settings)
        return latex, text, answer


# Distance / speed / time packs: distance unit always matches speed unit.
_DRT_UNIT_PACKS: tuple[tuple[str, str, str, str, str], ...] = (
    # (distance, time, speed_label, distance_toggle, time_toggle)
    ("mi", "hr", "mi/hr", "allow_distance_mi", "allow_time_hr"),
    ("mi", "min", "mi/min", "allow_distance_mi", "allow_time_min"),
    ("km", "hr", "km/hr", "allow_distance_km", "allow_time_hr"),
    ("km", "min", "km/min", "allow_distance_km", "allow_time_min"),
    # m/s and ft/s use seconds so rates stay coherent (no mi with km/h mix-ups).
    ("m", "s", "m/s", "allow_distance_m", ""),
    ("ft", "s", "ft/s", "allow_distance_ft", ""),
)

_DRT_VARIANT_KEYS: tuple[tuple[str, str, bool], ...] = (
    ("find_missing", "allow_drt_find_missing", True),
    ("round_trip", "allow_drt_round_trip", False),
    ("two_segments", "allow_drt_two_segments", False),
    ("opposite", "allow_drt_opposite", False),
    ("same_direction", "allow_drt_same_direction", False),
)

_WORK_VARIANT_KEYS: tuple[tuple[str, str, bool], ...] = (
    ("together", "allow_work_together", True),
    ("find_one_rate", "allow_work_find_one_rate", True),
    ("three", "allow_work_three", False),
    ("find_one_time", "allow_work_find_one_time", False),
    ("starts_later", "allow_work_starts_later", False),
    ("pipes", "allow_work_pipes", False),
)


def _pick_drt_units(settings: dict) -> tuple[str, str, str]:
    """Return (distance_unit, time_unit, speed_label) from enabled toggles.

    Classroom default: mi/hr and km/hr. Meter/foot and per-minute packs are
    opt-in via settings (not on by default).
    """
    packs: list[tuple[str, str, str]] = []
    # Keys whose default is False unless explicitly enabled.
    opt_in_false = {"allow_distance_m", "allow_distance_ft", "allow_time_min"}
    for distance, time_u, speed, dist_key, time_key in _DRT_UNIT_PACKS:
        dist_default = dist_key not in opt_in_false
        if not bool(settings.get(dist_key, dist_default)):
            continue
        if time_key:
            time_default = time_key not in opt_in_false
            if not bool(settings.get(time_key, time_default)):
                continue
        packs.append((distance, time_u, speed))
    if not packs:
        packs = [("mi", "hr", "mi/hr")]
    return random.choice(packs)


def _drt_rate_bounds(settings: dict, *, time_unit: str) -> tuple[int, int]:
    d = _topic_d(settings)
    band = _band_from_d(d)
    if time_unit == "s":
        if band == "easy":
            return 2, 8
        if band == "hard":
            return 5, 20
        return 3, 12
    if time_unit == "min":
        if band == "easy":
            return 1, 5
        if band == "hard":
            return 2, 12
        return 1, 8
    # hours — classroom DRT typically uses mph / km/h
    if band == "easy":
        return 20, 55
    if band == "hard":
        return 35, 95
    return 25, 75


def _drt_time_bounds(settings: dict) -> tuple[int, int]:
    band = _band_from_d(_topic_d(settings))
    if band == "easy":
        return 2, 5
    if band == "hard":
        return 3, 12
    return 2, 8


def _drt_variants_for_d(d: float) -> list[str]:
    """Core DRT skills from curriculum examples: d=rt, round-trip, catch-up.

    two_segments / opposite stay available only when explicitly allowed in settings
    (genuine DRT, but outside the example families we prioritize).
    """
    out = ["find_missing"]
    if d >= 3.0:
        out.append("round_trip")
    if d >= 6.0:
        out.append("same_direction")
    return out


def _enabled_drt_variants(settings: dict) -> list[str]:
    """Prefer example families; honor explicit structure toggles when set."""
    d = _topic_d(settings)
    core = _drt_variants_for_d(d)
    # Explicit allows for non-core structures (never invent them from D alone).
    extra: list[str] = []
    if bool(settings.get("allow_drt_two_segments", False)):
        extra.append("two_segments")
    if bool(settings.get("allow_drt_opposite", False)):
        extra.append("opposite")

    # If the caller narrowed structure toggles, respect that filter.
    flagged = [
        name
        for name, key, default in _DRT_VARIANT_KEYS
        if bool(settings.get(key, default))
    ]
    nondefault_on = any(
        bool(settings.get(key, False))
        for _, key, default in _DRT_VARIANT_KEYS
        if not default
    )
    if nondefault_on or (flagged and flagged != ["find_missing"]):
        allowed = set(flagged)
        chosen = [name for name in (*core, *extra) if name in allowed]
        return chosen or list(allowed) or ["find_missing"]
    return [*core, *extra] or ["find_missing"]


def _enabled_variants(
    settings: dict,
    keys: tuple[tuple[str, str, bool], ...],
    *,
    fallback: str,
) -> list[str]:
    enabled = [
        name
        for name, key, default in keys
        if bool(settings.get(key, default))
    ]
    return enabled or [fallback]


def _integer_pair_product_sum(lo: int, hi: int) -> tuple[int, int] | None:
    """Pick distinct a, b in [lo, hi] so ab/(a+b) is an integer."""
    candidates: list[tuple[int, int]] = []
    for a in range(lo, hi + 1):
        for b in range(lo, hi + 1):
            if a == b:
                continue
            total = a + b
            if total and (a * b) % total == 0:
                candidates.append((a, b))
    if not candidates:
        return None
    return random.choice(candidates)


def _integer_triple_together(lo: int, hi: int) -> tuple[int, int, int, int] | None:
    """Pick a,b,c so 1/a+1/b+1/c = 1/t for integer t."""
    candidates: list[tuple[int, int, int, int]] = []
    for a in range(lo, hi + 1):
        for b in range(a + 1, hi + 1):
            for c in range(b + 1, hi + 1):
                # t = 1 / (1/a + 1/b + 1/c) = abc / (bc + ac + ab)
                num = a * b * c
                den = b * c + a * c + a * b
                if den and num % den == 0:
                    t = num // den
                    if t >= 1:
                        candidates.append((a, b, c, t))
    if not candidates:
        return None
    return random.choice(candidates)


class DistanceRateTimeFramework(WordProblemFramework):
    """Genuine d = r·t word problems: basic missing piece, round-trip, catch-up."""

    problem_kind = "distance_rate_time"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        # Prefer mi/hr classroom units for round-trip / catch-up story frames.
        distance_u, time_u, speed_u = _pick_drt_units(settings)
        show_units = bool(settings.get("show_unit_labels", True))
        variant_family = random.choice(_enabled_drt_variants(settings))
        rate_lo, rate_hi = _drt_rate_bounds(settings, time_unit=time_u)
        time_lo, time_hi = _drt_time_bounds(settings)

        if variant_family == "find_missing":
            return self._find_missing(
                settings,
                distance_u=distance_u,
                time_u=time_u,
                speed_u=speed_u,
                show_units=show_units,
                rate_lo=rate_lo,
                rate_hi=rate_hi,
                time_lo=time_lo,
                time_hi=time_hi,
            )
        if variant_family == "round_trip":
            return self._round_trip(
                settings,
                distance_u=distance_u,
                time_u=time_u,
                speed_u=speed_u,
                show_units=show_units,
                rate_lo=rate_lo,
                rate_hi=rate_hi,
            )
        if variant_family == "two_segments":
            return self._two_segments(
                settings,
                distance_u=distance_u,
                time_u=time_u,
                speed_u=speed_u,
                show_units=show_units,
                rate_lo=rate_lo,
                rate_hi=rate_hi,
                time_lo=time_lo,
                time_hi=time_hi,
            )
        if variant_family == "opposite":
            return self._opposite(
                settings,
                distance_u=distance_u,
                time_u=time_u,
                speed_u=speed_u,
                show_units=show_units,
                rate_lo=rate_lo,
                rate_hi=rate_hi,
            )
        return self._same_direction(
            settings,
            distance_u=distance_u,
            time_u=time_u,
            speed_u=speed_u,
            show_units=show_units,
            rate_lo=rate_lo,
            rate_hi=rate_hi,
        )

    def _find_missing(
        self,
        settings: dict,
        *,
        distance_u: str,
        time_u: str,
        speed_u: str,
        show_units: bool,
        rate_lo: int,
        rate_hi: int,
        time_lo: int,
        time_hi: int,
    ) -> tuple[str, str, str | None]:
        name = _pick_name(settings)
        ask = random.choice(["find_time", "find_distance", "find_rate"])
        rate = _random_value(settings, lo=rate_lo, hi=rate_hi)
        time = _random_value(settings, lo=time_lo, hi=time_hi)
        distance = rate * time

        if ask == "find_time":
            answer = _format_answer(time, settings)
            unit_suffix = f" {time_u}" if show_units else ""
            latex = (
                rf"\text{{{name} travels {distance} {distance_u} at {rate} {speed_u}. "
                rf"How many {time_u} does the trip take?}}"
            )
            text = (
                f"{name} travels {distance} {distance_u} at {rate} {speed_u}. "
                f"How many {time_u} does the trip take?"
            )
            return latex, text, f"{answer}{unit_suffix}" if show_units else answer

        if ask == "find_distance":
            answer = _format_answer(distance, settings)
            unit_suffix = f" {distance_u}" if show_units else ""
            latex = (
                rf"\text{{{name} travels at {rate} {speed_u} for {time} {time_u}. "
                rf"How many {distance_u} does {name} travel?}}"
            )
            text = (
                f"{name} travels at {rate} {speed_u} for {time} {time_u}. "
                f"How many {distance_u} does {name} travel?"
            )
            return latex, text, f"{answer}{unit_suffix}" if show_units else answer

        answer = _format_answer(rate, settings)
        unit_suffix = f" {speed_u}" if show_units else ""
        latex = (
            rf"\text{{{name} travels {distance} {distance_u} in {time} {time_u}. "
            rf"What is the average speed in {speed_u}?}}"
        )
        text = (
            f"{name} travels {distance} {distance_u} in {time} {time_u}. "
            f"What is the average speed in {speed_u}?"
        )
        return latex, text, f"{answer}{unit_suffix}" if show_units else answer

    def _round_trip(
        self,
        settings: dict,
        *,
        distance_u: str,
        time_u: str,
        speed_u: str,
        show_units: bool,
        rate_lo: int,
        rate_hi: int,
    ) -> tuple[str, str, str | None]:
        """Round-trip: same distance both ways; find missing speed or time."""
        name = _pick_name(settings)
        d = _topic_d(settings)
        band = _band_from_d(d)
        # Prefer hour-based classroom wording when units allow.
        if band == "easy":
            asks = ["find_speed_there", "find_time_there", "find_total_time"]
        else:
            asks = ["find_speed_there", "find_time_there"]
        ask = random.choice(asks)

        # Build integer rates/times with equal distances: r1*t1 = r2*t2.
        t_there = random.randint(2, 5 if band != "hard" else 8)
        t_back = random.randint(2, 5 if band != "hard" else 8)
        while t_back == t_there:
            t_back = random.randint(2, 6)
        # Choose k so both speeds land in range: r_there = k*t_back, r_back = k*t_there.
        max_k = min(rate_hi // t_back, rate_hi // t_there)
        min_k = max(
            1,
            (rate_lo + t_back - 1) // t_back,
            (rate_lo + t_there - 1) // t_there,
        )
        if max_k < min_k:
            t_there, t_back = 2, 3
            max_k = min(rate_hi // t_back, rate_hi // t_there)
            min_k = max(1, (rate_lo + t_back - 1) // t_back, (rate_lo + t_there - 1) // t_there)
        k = random.randint(min_k, max(min_k, max_k))
        r_there = k * t_back
        r_back = k * t_there
        if r_there == r_back:
            t_back = t_there + 1
            r_there = k * t_back
        distance = k * t_there * t_back

        if ask == "find_speed_there":
            # Given: time there, time back, speed back → speed there
            answer = _format_answer(r_there, settings)
            unit_suffix = f" {speed_u}" if show_units else ""
            latex = (
                rf"\text{{{name} drives to a destination in {t_there} {time_u} and "
                rf"returns in {t_back} {time_u} at {r_back} {speed_u}. "
                rf"What was {name}'s speed on the way there?}}"
            )
            text = (
                f"{name} drives to a destination in {t_there} {time_u} and "
                f"returns in {t_back} {time_u} at {r_back} {speed_u}. "
                f"What was {name}'s speed on the way there?"
            )
            return latex, text, f"{answer}{unit_suffix}" if show_units else answer

        if ask == "find_time_there":
            # Given: speed there, speed back, time back → time there
            answer = _format_answer(t_there, settings)
            unit_suffix = f" {time_u}" if show_units else ""
            latex = (
                rf"\text{{{name} drives to a destination at {r_there} {speed_u} and "
                rf"returns at {r_back} {speed_u}, taking {t_back} {time_u} on the way back. "
                rf"How long did the trip there take?}}"
            )
            text = (
                f"{name} drives to a destination at {r_there} {speed_u} and "
                f"returns at {r_back} {speed_u}, taking {t_back} {time_u} on the way back. "
                f"How long did the trip there take?"
            )
            return latex, text, f"{answer}{unit_suffix}" if show_units else answer

        # find_total_time — both speeds and one-way distance known
        total = t_there + t_back
        answer = _format_answer(total, settings)
        unit_suffix = f" {time_u}" if show_units else ""
        latex = (
            rf"\text{{{name} drives {distance} {distance_u} at {r_there} {speed_u}, "
            rf"then returns the same distance at {r_back} {speed_u}. "
            rf"How many {time_u} does the round trip take?}}"
        )
        text = (
            f"{name} drives {distance} {distance_u} at {r_there} {speed_u}, "
            f"then returns the same distance at {r_back} {speed_u}. "
            f"How many {time_u} does the round trip take?"
        )
        return latex, text, f"{answer}{unit_suffix}" if show_units else answer

    def _two_segments(
        self,
        settings: dict,
        *,
        distance_u: str,
        time_u: str,
        speed_u: str,
        show_units: bool,
        rate_lo: int,
        rate_hi: int,
        time_lo: int,
        time_hi: int,
    ) -> tuple[str, str, str | None]:
        name = _pick_name(settings)
        rate1 = _random_value(settings, lo=rate_lo, hi=rate_hi)
        rate2 = _random_value(settings, lo=rate_lo, hi=rate_hi)
        while rate2 == rate1:
            rate2 = _random_value(settings, lo=rate_lo, hi=rate_hi)
        t1 = _random_value(settings, lo=time_lo, hi=max(time_lo + 1, time_hi - 1))
        t2 = _random_value(settings, lo=time_lo, hi=time_hi)
        d1, d2 = rate1 * t1, rate2 * t2
        total = d1 + d2
        answer = _format_answer(total, settings)
        unit_suffix = f" {distance_u}" if show_units else ""
        latex = (
            rf"\text{{{name} travels at {rate1} {speed_u} for {t1} {time_u}, then "
            rf"at {rate2} {speed_u} for {t2} {time_u}. "
            rf"How many {distance_u} does {name} travel in all?}}"
        )
        text = (
            f"{name} travels at {rate1} {speed_u} for {t1} {time_u}, then "
            f"at {rate2} {speed_u} for {t2} {time_u}. "
            f"How many {distance_u} does {name} travel in all?"
        )
        return latex, text, f"{answer}{unit_suffix}" if show_units else answer

    def _opposite(
        self,
        settings: dict,
        *,
        distance_u: str,
        time_u: str,
        speed_u: str,
        show_units: bool,
        rate_lo: int,
        rate_hi: int,
    ) -> tuple[str, str, str | None]:
        a_name, b_name = _pick_names(settings, 2)
        rate_a = _random_value(settings, lo=rate_lo, hi=rate_hi)
        rate_b = _random_value(settings, lo=rate_lo, hi=rate_hi)
        while rate_b == rate_a:
            rate_b = _random_value(settings, lo=rate_lo, hi=rate_hi)
        meet_time = _random_value(settings, lo=2, hi=6)
        distance = (rate_a + rate_b) * meet_time
        ask = random.choice(["time", "distance"])
        if ask == "time":
            answer = _format_answer(meet_time, settings)
            unit_suffix = f" {time_u}" if show_units else ""
            latex = (
                rf"\text{{{a_name} and {b_name} leave the same place at the same time "
                rf"and travel in opposite directions at {rate_a} {speed_u} and "
                rf"{rate_b} {speed_u}. They are {distance} {distance_u} apart when they "
                rf"stop. How many {time_u} did they travel?}}"
            )
            text = (
                f"{a_name} and {b_name} leave the same place at the same time "
                f"and travel in opposite directions at {rate_a} {speed_u} and "
                f"{rate_b} {speed_u}. They are {distance} {distance_u} apart when they "
                f"stop. How many {time_u} did they travel?"
            )
            return latex, text, f"{answer}{unit_suffix}" if show_units else answer

        answer = _format_answer(distance, settings)
        unit_suffix = f" {distance_u}" if show_units else ""
        latex = (
            rf"\text{{{a_name} and {b_name} leave the same place at the same time "
            rf"and travel in opposite directions at {rate_a} {speed_u} and "
            rf"{rate_b} {speed_u} for {meet_time} {time_u}. "
            rf"How many {distance_u} apart are they?}}"
        )
        text = (
            f"{a_name} and {b_name} leave the same place at the same time "
            f"and travel in opposite directions at {rate_a} {speed_u} and "
            f"{rate_b} {speed_u} for {meet_time} {time_u}. "
            f"How many {distance_u} apart are they?"
        )
        return latex, text, f"{answer}{unit_suffix}" if show_units else answer

    def _same_direction(
        self,
        settings: dict,
        *,
        distance_u: str,
        time_u: str,
        speed_u: str,
        show_units: bool,
        rate_lo: int,
        rate_hi: int,
    ) -> tuple[str, str, str | None]:
        """Catch-up: slower traveler leaves first; faster catches up later."""
        a_name, b_name = _pick_names(settings, 2)
        d = _topic_d(settings)
        band = _band_from_d(d)
        # Asks matching textbook catch-up frames.
        if band == "easy":
            asks = ["find_catch_time", "find_slow_speed", "find_leader_total_time"]
        else:
            asks = ["find_slow_speed", "find_leader_total_time"]
        ask = random.choice(asks)

        # Clean integers: slow*(head+catch) = fast*catch
        # ⇒ slow = fast*catch/(head+catch), leader_total = head+catch = fast*catch/slow
        head = random.randint(1, 3 if band == "easy" else 5)
        catch = random.randint(2, 4 if band == "easy" else 7)
        # Pick fast and factor so slow is an integer in range.
        for _ in range(40):
            fast = _random_value(settings, lo=max(rate_lo + 5, rate_lo), hi=rate_hi)
            total_leader = head + catch
            if (fast * catch) % total_leader != 0:
                continue
            slow = (fast * catch) // total_leader
            if rate_lo <= slow < fast:
                break
        else:
            # Guaranteed clean fallback: catch=head, fast=2*slow
            head = 2
            catch = 2
            slow = max(rate_lo, min(rate_hi - 10, 30))
            fast = 2 * slow

        if ask == "find_slow_speed":
            # Slow left earlier; after catch hours the fast one catches up → find slow speed
            answer = _format_answer(slow, settings)
            unit_suffix = f" {speed_u}" if show_units else ""
            vehicle = random.choice(["train", "bus", "car"])
            latex = (
                rf"\text{{A slow {vehicle} leaves a station traveling at an unknown speed. "
                rf"{head} {time_u} later a faster {vehicle} leaves the same station at "
                rf"{fast} {speed_u} and catches up after {catch} {time_u}. "
                rf"What is the slow {vehicle}'s speed?}}"
            )
            text = (
                f"A slow {vehicle} leaves a station traveling at an unknown speed. "
                f"{head} {time_u} later a faster {vehicle} leaves the same station at "
                f"{fast} {speed_u} and catches up after {catch} {time_u}. "
                f"What is the slow {vehicle}'s speed?"
            )
            return latex, text, f"{answer}{unit_suffix}" if show_units else answer

        if ask == "find_leader_total_time":
            # Jose left first slower; Rob catches after T → how long has Jose been driving?
            leader_total = head + catch
            answer = _format_answer(leader_total, settings)
            unit_suffix = f" {time_u}" if show_units else ""
            latex = (
                rf"\text{{{a_name} leaves traveling at {slow} {speed_u}. {b_name} leaves "
                rf"later from the same place at {fast} {speed_u} in the same direction and "
                rf"catches up {catch} {time_u} after starting. "
                rf"How long had {a_name} been traveling when caught?}}"
            )
            text = (
                f"{a_name} leaves traveling at {slow} {speed_u}. {b_name} leaves "
                f"later from the same place at {fast} {speed_u} in the same direction and "
                f"catches up {catch} {time_u} after starting. "
                f"How long had {a_name} been traveling when caught?"
            )
            return latex, text, f"{answer}{unit_suffix}" if show_units else answer

        # find_catch_time — both speeds and head start known
        answer = _format_answer(catch, settings)
        unit_suffix = f" {time_u}" if show_units else ""
        latex = (
            rf"\text{{{a_name} leaves traveling at {slow} {speed_u}. {b_name} leaves "
            rf"from the same place {head} {time_u} later at {fast} {speed_u} "
            rf"in the same direction. How many {time_u} after {b_name} starts does "
            rf"{b_name} catch up to {a_name}?}}"
        )
        text = (
            f"{a_name} leaves traveling at {slow} {speed_u}. {b_name} leaves "
            f"from the same place {head} {time_u} later at {fast} {speed_u} "
            f"in the same direction. How many {time_u} after {b_name} starts does "
            f"{b_name} catch up to {a_name}?"
        )
        return latex, text, f"{answer}{unit_suffix}" if show_units else answer


class WorkProblemFramework(WordProblemFramework):
    problem_kind = "work"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        time_u = self._pick_time_unit(settings)
        show_units = bool(settings.get("show_unit_labels", True))
        variant = random.choice(
            _enabled_variants(settings, _WORK_VARIANT_KEYS, fallback="together")
        )
        if variant == "together":
            return self._together(settings, time_u=time_u, show_units=show_units)
        if variant == "find_one_rate":
            return self._find_one_rate(settings, time_u=time_u, show_units=show_units)
        if variant == "three":
            return self._three(settings, time_u=time_u, show_units=show_units)
        if variant == "find_one_time":
            return self._find_one_time(settings, time_u=time_u, show_units=show_units)
        if variant == "starts_later":
            return self._starts_later(settings, time_u=time_u, show_units=show_units)
        return self._pipes(settings, time_u=time_u, show_units=show_units)

    @staticmethod
    def _pick_time_unit(settings: dict) -> str:
        options: list[str] = []
        if bool(settings.get("allow_work_time_hr", True)):
            options.append("hr")
        if bool(settings.get("allow_work_time_min", True)):
            options.append("min")
        return random.choice(options or ["hr"])

    @staticmethod
    def _time_bounds(settings: dict) -> tuple[int, int]:
        difficulty = str(settings.get("difficulty", "medium"))
        if difficulty == "easy":
            return 2, 12
        if difficulty == "hard":
            return 4, 24
        return 3, 18

    def _together(
        self, settings: dict, *, time_u: str, show_units: bool
    ) -> tuple[str, str, str | None]:
        a_name, b_name = _pick_names(settings, 2)
        lo, hi = self._time_bounds(settings)
        pair = _integer_pair_product_sum(lo, hi) or (3, 6)
        a_time, b_time = pair
        together = (a_time * b_time) // (a_time + b_time)
        answer = _format_answer(together, settings)
        unit_suffix = f" {time_u}" if show_units else ""
        latex = (
            rf"\text{{{a_name} can finish a job in {a_time} {time_u} and {b_name} "
            rf"can finish the same job in {b_time} {time_u}. Working together, "
            rf"how many {time_u} will it take them to finish the job?}}"
        )
        text = (
            f"{a_name} can finish a job in {a_time} {time_u} and {b_name} "
            f"can finish the same job in {b_time} {time_u}. Working together, "
            f"how many {time_u} will it take them to finish the job?"
        )
        return latex, text, f"{answer}{unit_suffix}" if show_units else answer

    def _find_one_rate(
        self, settings: dict, *, time_u: str, show_units: bool
    ) -> tuple[str, str, str | None]:
        a_name, b_name = _pick_names(settings, 2)
        lo, hi = self._time_bounds(settings)
        pair = _integer_pair_product_sum(lo, hi) or (4, 12)
        a_time, b_time = pair
        together = (a_time * b_time) // (a_time + b_time)
        answer = _format_answer(b_time, settings)
        unit_suffix = f" {time_u}" if show_units else ""
        latex = (
            rf"\text{{{a_name} can finish a job in {a_time} {time_u}. Working with "
            rf"{b_name}, they finish in {together} {time_u}. How many {time_u} would "
            rf"it take {b_name} working alone?}}"
        )
        text = (
            f"{a_name} can finish a job in {a_time} {time_u}. Working with "
            f"{b_name}, they finish in {together} {time_u}. How many {time_u} would "
            f"it take {b_name} working alone?"
        )
        return latex, text, f"{answer}{unit_suffix}" if show_units else answer

    def _three(
        self, settings: dict, *, time_u: str, show_units: bool
    ) -> tuple[str, str, str | None]:
        a_name, b_name, c_name = _pick_names(settings, 3)
        lo, hi = self._time_bounds(settings)
        triple = _integer_triple_together(lo, min(hi, 16))
        if triple is None:
            a_time, b_time, c_time, together = 4, 6, 12, 2
        else:
            a_time, b_time, c_time, together = triple
        answer = _format_answer(together, settings)
        unit_suffix = f" {time_u}" if show_units else ""
        latex = (
            rf"\text{{{a_name}, {b_name}, and {c_name} can finish a job in "
            rf"{a_time}, {b_time}, and {c_time} {time_u} respectively. Working "
            rf"together, how many {time_u} will it take them?}}"
        )
        text = (
            f"{a_name}, {b_name}, and {c_name} can finish a job in "
            f"{a_time}, {b_time}, and {c_time} {time_u} respectively. Working "
            f"together, how many {time_u} will it take them?"
        )
        return latex, text, f"{answer}{unit_suffix}" if show_units else answer

    def _find_one_time(
        self, settings: dict, *, time_u: str, show_units: bool
    ) -> tuple[str, str, str | None]:
        a_name, b_name, c_name = _pick_names(settings, 3)
        lo, hi = self._time_bounds(settings)
        triple = _integer_triple_together(lo, min(hi, 20))
        if triple is None:
            a_time, b_time, c_time, together = 6, 8, 24, 3
        else:
            a_time, b_time, c_time, together = triple
        answer = _format_answer(c_time, settings)
        unit_suffix = f" {time_u}" if show_units else ""
        latex = (
            rf"\text{{{a_name} and {b_name} can finish a job in {a_time} and "
            rf"{b_time} {time_u}. With {c_name} helping, the three finish in "
            rf"{together} {time_u}. How many {time_u} would {c_name} need alone?}}"
        )
        text = (
            f"{a_name} and {b_name} can finish a job in {a_time} and "
            f"{b_time} {time_u}. With {c_name} helping, the three finish in "
            f"{together} {time_u}. How many {time_u} would {c_name} need alone?"
        )
        return latex, text, f"{answer}{unit_suffix}" if show_units else answer

    def _starts_later(
        self, settings: dict, *, time_u: str, show_units: bool
    ) -> tuple[str, str, str | None]:
        a_name, b_name = _pick_names(settings, 2)
        # Prefer clean integer totals from a small curated set.
        a_time, b_time, delay, total = random.choice(
            [
                (6, 3, 3, 4),
                (8, 8, 2, 5),
                (6, 6, 2, 4),
                (10, 5, 4, 6),
                (12, 6, 6, 8),
            ]
        )
        answer = _format_answer(total, settings)
        unit_suffix = f" {time_u}" if show_units else ""
        latex = (
            rf"\text{{{a_name} can finish a job in {a_time} {time_u} and {b_name} "
            rf"in {b_time} {time_u}. {a_name} works alone for {delay} {time_u}, then "
            rf"{b_name} joins. How many {time_u} from the start until the job is done?}}"
        )
        text = (
            f"{a_name} can finish a job in {a_time} {time_u} and {b_name} "
            f"in {b_time} {time_u}. {a_name} works alone for {delay} {time_u}, then "
            f"{b_name} joins. How many {time_u} from the start until the job is done?"
        )
        return latex, text, f"{answer}{unit_suffix}" if show_units else answer

    def _pipes(
        self, settings: dict, *, time_u: str, show_units: bool
    ) -> tuple[str, str, str | None]:
        fill_a, fill_b, drain, total = random.choice(
            [
                (4, 6, 12, 3),
                (6, 8, 24, 4),
                (3, 4, 12, 2),
                (3, 6, 6, 3),
                (8, 8, 8, 8),
            ]
        )
        answer = _format_answer(total, settings)
        unit_suffix = f" {time_u}" if show_units else ""
        latex = (
            rf"\text{{Pipe A fills a tank in {fill_a} {time_u}, pipe B fills it in "
            rf"{fill_b} {time_u}, and a drain empties it in {drain} {time_u}. "
            rf"With all three open, how many {time_u} to fill the tank?}}"
        )
        text = (
            f"Pipe A fills a tank in {fill_a} {time_u}, pipe B fills it in "
            f"{fill_b} {time_u}, and a drain empties it in {drain} {time_u}. "
            f"With all three open, how many {time_u} to fill the tank?"
        )
        return latex, text, f"{answer}{unit_suffix}" if show_units else answer


class AgeProblemFramework(WordProblemFramework):
    problem_kind = "age"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        older, younger = _pick_names(settings, 2)
        diff = _random_value(settings, lo=2, hi=8)
        younger_age = _random_value(settings, lo=8, hi=20)
        older_age = younger_age + diff
        total = younger_age + older_age
        answer = _format_answer(younger_age, settings)
        year_unit = _unit_label(settings, "years") or "years"
        latex = (
            rf"\text{{{older} is {diff} {year_unit} older than {younger}. "
            rf"The sum of their ages is {total} {year_unit}. How old is {younger}?}}"
        )
        text = (
            f"{older} is {diff} {year_unit} older than {younger}. "
            f"The sum of their ages is {total} {year_unit}. How old is {younger}?"
        )
        return latex, text, _append_units(answer, settings)


_COUNT_WORDS = {2: "two", 3: "three", 4: "four", 5: "five"}


def _consecutive_count(settings: dict) -> int:
    lo = int(settings.get("min_consecutive_count", 2))
    hi = int(settings.get("max_consecutive_count", 4))
    lo = max(2, min(5, lo))
    hi = max(2, min(5, hi))
    if lo > hi:
        lo, hi = hi, lo
    return random.randint(lo, hi)


def _consecutive_parity(settings: dict) -> str:
    options: list[str] = []
    if bool(settings.get("allow_consecutive_integers", True)):
        options.append("any")
    if bool(settings.get("allow_consecutive_even", False)):
        options.append("even")
    if bool(settings.get("allow_consecutive_odd", False)):
        options.append("odd")
    if not options:
        options = ["any"]
    return random.choice(options)


def _consecutive_goal(settings: dict) -> str:
    options: list[str] = []
    if bool(settings.get("allow_sum_goal", True)):
        options.append("sum")
    if bool(settings.get("allow_sum_first_last_goal", False)):
        options.append("sum_first_last")
    if bool(settings.get("allow_product_goal", False)):
        options.append("product")
    if not options:
        options = ["sum"]
    return random.choice(options)


def _consecutive_phrase(count: int, parity: str) -> str:
    word = _COUNT_WORDS.get(count, str(count))
    if parity == "even":
        return f"{word} consecutive even integers"
    if parity == "odd":
        return f"{word} consecutive odd integers"
    return f"{word} consecutive integers"


def _consecutive_start(settings: dict, *, count: int, parity: str, step: int) -> int:
    """Pick a starting integer sized for the difficulty tier."""
    lo, hi = _difficulty_range(settings)
    # Keep products of first/last from exploding on hard tiers.
    if parity != "any":
        lo = max(lo, 2)
        hi = max(hi, lo + 2)
    start = _random_value(settings, lo=lo, hi=hi)
    if parity == "even" and start % 2:
        start += 1
    elif parity == "odd" and start % 2 == 0:
        start += 1
    # Prefer positive sequences for readability unless hard allows negatives.
    if start <= 0 and str(settings.get("difficulty", "medium")) != "hard":
        start = step if parity != "odd" else 1
        if parity == "even":
            start = 2
    # Avoid a trailing zero-only edge when count is large and start is tiny.
    if start + (count - 1) * step == 0:
        start += step
    return start


class ConsecutiveIntegersFramework(WordProblemFramework):
    problem_kind = "consecutive_integers"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        count = _consecutive_count(settings)
        parity = _consecutive_parity(settings)
        goal = _consecutive_goal(settings)
        step = 1 if parity == "any" else 2
        start = _consecutive_start(settings, count=count, parity=parity, step=step)
        values = [start + i * step for i in range(count)]
        phrase = _consecutive_phrase(count, parity)
        first, last = values[0], values[-1]

        if goal == "sum_first_last":
            clue = first + last
            latex = (
                rf"\text{{The sum of the first and last of {phrase} is {clue}. "
                rf"Find the smallest integer.}}"
            )
            text = (
                f"The sum of the first and last of {phrase} is {clue}. "
                f"Find the smallest integer."
            )
        elif goal == "product":
            clue = first * last
            latex = (
                rf"\text{{The product of the first and last of {phrase} is {clue}. "
                rf"Find the smallest integer.}}"
            )
            text = (
                f"The product of the first and last of {phrase} is {clue}. "
                f"Find the smallest integer."
            )
        else:
            clue = sum(values)
            # Slight wording variety so tiers don't read identically.
            if count >= 4 and random.random() < 0.5:
                latex = (
                    rf"\text{{Find the smallest of {phrase} whose sum is {clue}.}}"
                )
                text = f"Find the smallest of {phrase} whose sum is {clue}."
            else:
                latex = (
                    rf"\text{{The sum of {phrase} is {clue}. Find the smallest integer.}}"
                )
                text = f"The sum of {phrase} is {clue}. Find the smallest integer."

        answer = _format_answer(start, settings)
        return latex, text, answer


class CoinProblemFramework(WordProblemFramework):
    problem_kind = "coin"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        total_coins = _random_value(settings, lo=12, hi=30)
        quarters = _random_value(settings, lo=4, hi=total_coins - 4)
        nickels = total_coins - quarters
        total_cents = quarters * 25 + nickels * 5
        answer = _format_answer(quarters, settings)
        dollars = total_cents / 100
        dollar_text = f"\\${dollars:.2f}" if dollars == int(dollars) else f"\\${dollars:.2f}"
        latex = (
            rf"\text{{A jar contains {total_coins} coins, all quarters and nickels, "
            rf"worth {dollar_text} in total. How many quarters are in the jar?}}"
        )
        text = (
            f"A jar contains {total_coins} coins, all quarters and nickels, "
            f"worth ${dollars:.2f} in total. How many quarters are in the jar?"
        )
        return latex, text, _append_units(answer, settings)


class MixtureProblemFramework(WordProblemFramework):
    """Weighted-average mixtures: percent/concentration or cost per unit.

    Skill: combine two amounts with two rates → mixture rate
    ``(a1·r1 + a2·r2) / (a1 + a2)``. Story frames match classroom examples
    (soil/sand, nuts/peanuts, alcohol solutions, spice cost blends).
    """

    problem_kind = "mixture"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        d = _topic_d(settings)
        band = _band_from_d(d)
        variant = self._pick_variant(settings, d)
        if variant == "cost":
            return self._cost_mixture(settings, band)
        return self._percent_mixture(settings, band)

    @staticmethod
    def _pick_variant(settings: dict, d: float) -> str:
        allow_pct = bool(settings.get("allow_mixture_percent", True))
        allow_cost = bool(settings.get("allow_mixture_cost", True))
        options: list[str] = []
        if allow_pct:
            options.append("percent")
        if allow_cost and d >= 4.0:
            options.append("cost")
        if not options:
            options = ["percent"]
        return random.choice(options)

    @staticmethod
    def _sample_amounts(band: str) -> tuple[int, int]:
        if band == "easy":
            choices = [2, 3, 4, 5, 6, 8, 10]
        elif band == "hard":
            choices = list(range(4, 25))
        else:
            choices = [3, 4, 5, 6, 8, 10, 12, 15]
        a1 = random.choice(choices)
        a2 = random.choice([c for c in choices if c != a1] or choices)
        return a1, a2

    @staticmethod
    def _sample_percents(band: str) -> tuple[int, int]:
        if band == "easy":
            pool = [10, 20, 25, 30, 40, 50, 60, 75]
        elif band == "hard":
            pool = [10, 12, 15, 18, 20, 25, 30, 35, 40, 45, 50, 60, 70]
        else:
            pool = [10, 15, 20, 25, 30, 40, 50, 60, 75]
        p1 = random.choice(pool)
        p2 = random.choice([p for p in pool if p != p1] or pool)
        return p1, p2

    def _percent_mixture(
        self, settings: dict, band: str
    ) -> tuple[str, str, str | None]:
        """Two amounts + two percents → concentration of the mixture."""
        # Retry until mixture percent is a clean value at low/medium D.
        for _ in range(60):
            a1, a2 = self._sample_amounts(band)
            p1, p2 = self._sample_percents(band)
            total = a1 + a2
            pure = a1 * p1 + a2 * p2
            if band != "hard" and pure % total != 0:
                continue
            mix = pure / total
            if band == "hard":
                # Allow one-decimal percents when not integer.
                if abs(mix - round(mix)) < 1e-9:
                    mix_disp = str(int(round(mix)))
                else:
                    mix = round(mix, 1)
                    mix_disp = f"{mix:.1f}".rstrip("0").rstrip(".")
            else:
                mix_disp = str(int(round(mix)))
            break
        else:
            a1, a2, p1, p2, mix_disp = 4, 6, 20, 50, "38"

        frame = random.choice(["soil", "nuts", "alcohol"])
        name = _pick_name(settings)

        if frame == "soil":
            latex = (
                rf"\text{{{name} mixes {a1} cubic yards of soil that is {p1}\% sand with "
                rf"{a2} cubic yards of soil that is {p2}\% sand. "
                rf"What percent of the mixture is sand?}}"
            )
            text = (
                f"{name} mixes {a1} cubic yards of soil that is {p1}% sand with "
                f"{a2} cubic yards of soil that is {p2}% sand. "
                f"What percent of the mixture is sand?"
            )
        elif frame == "nuts":
            latex = (
                rf"\text{{{name} mixes {a1} lb of nuts that are {p1}\% peanuts with "
                rf"{a2} lb of nuts that are {p2}\% peanuts. "
                rf"What percent of the new mixture is peanuts?}}"
            )
            text = (
                f"{name} mixes {a1} lb of nuts that are {p1}% peanuts with "
                f"{a2} lb of nuts that are {p2}% peanuts. "
                f"What percent of the new mixture is peanuts?"
            )
        else:
            unit = "fl oz"
            latex = (
                rf"\text{{{name} mixes {a1} {unit} of a {p1}\% alcohol solution with "
                rf"{a2} {unit} of a {p2}\% alcohol solution. "
                rf"What is the concentration of the new mixture?}}"
            )
            text = (
                f"{name} mixes {a1} {unit} of a {p1}% alcohol solution with "
                f"{a2} {unit} of a {p2}% alcohol solution. "
                f"What is the concentration of the new mixture?"
            )

        answer = f"{mix_disp}\\%"
        return latex, text, answer

    def _cost_mixture(
        self, settings: dict, band: str
    ) -> tuple[str, str, str | None]:
        """Two weights + two $/unit prices → cost per unit of the blend."""
        name = _pick_name(settings)
        for _ in range(60):
            w1, w2 = self._sample_amounts(band)
            if band == "easy":
                c1 = random.choice([2, 3, 4, 5, 6, 8])
                c2 = random.choice([x for x in (3, 4, 5, 6, 8, 10) if x != c1])
            elif band == "hard":
                c1 = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 12])
                c2 = random.choice([3, 4, 5, 6, 7, 8, 9, 10, 11, 14])
                if c2 == c1:
                    c2 = c1 + 2
            else:
                c1 = random.choice([2, 3, 4, 5, 6, 8, 10])
                c2 = random.choice([x for x in (3, 4, 5, 6, 8, 9, 12) if x != c1])
            total_w = w1 + w2
            total_cost = w1 * c1 + w2 * c2
            if band != "hard" and total_cost % total_w != 0:
                continue
            unit_cost = total_cost / total_w
            if band == "hard" and abs(unit_cost - round(unit_cost, 2)) > 1e-9:
                continue
            break
        else:
            w1, w2, c1, c2, unit_cost = 3, 5, 4, 8, 6.5

        if abs(unit_cost - round(unit_cost)) < 1e-9:
            cost_disp = str(int(round(unit_cost)))
        else:
            cost_disp = f"{unit_cost:.2f}".rstrip("0").rstrip(".")

        # Cinnamon / spice blend frame (classroom cost-mixture style).
        brand_a = random.choice(["Indonesian", "Sri Lankan", "Vietnamese"])
        brand_b = random.choice(["Thai", "Indian", "Mexican"])
        while brand_b == brand_a:
            brand_b = random.choice(["Thai", "Indian", "Mexican", "Chinese"])
        product = random.choice(["cinnamon", "coffee", "tea"])

        latex = (
            rf"\text{{{name} blends {w1} lb of {brand_a} {product} costing "
            rf"\${c1} per lb with {w2} lb of {brand_b} {product} costing "
            rf"\${c2} per lb. What is the cost per pound of the mixture?}}"
        )
        text = (
            f"{name} blends {w1} lb of {brand_a} {product} costing "
            f"${c1} per lb with {w2} lb of {brand_b} {product} costing "
            f"${c2} per lb. What is the cost per pound of the mixture?"
        )
        return latex, text, f"\\${cost_disp}"


class PerimeterAreaFramework(WordProblemFramework):
    problem_kind = "perimeter_area"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        unit = _unit_label(settings, "ft") or "ft"
        variant = random.choice(["perimeter", "area"])

        if variant == "perimeter":
            width = _random_value(settings, lo=4, hi=15)
            diff = _random_value(settings, lo=2, hi=6)
            length = width + diff
            perimeter = 2 * (length + width)
            answer = _format_answer(width, settings)
            latex = (
                rf"\text{{A rectangle has length {diff} {unit} more than its width. "
                rf"If the perimeter is {perimeter} {unit}, what is the width in {unit}?}}"
            )
            text = (
                f"A rectangle has length {diff} {unit} more than its width. "
                f"If the perimeter is {perimeter} {unit}, what is the width in {unit}?"
            )
        else:
            width = _random_value(settings, lo=3, hi=10)
            diff = _random_value(settings, lo=2, hi=5)
            length = width + diff
            area = length * width
            answer = _format_answer(length, settings)
            latex = (
                rf"\text{{A rectangle has width {width} {unit} and area {area} {unit}^2. "
                rf"What is the length in {unit}?}}"
            )
            text = (
                f"A rectangle has width {width} {unit} and area {area} {unit}^2. "
                f"What is the length in {unit}?"
            )

        return latex, text, _append_units(answer, settings)


class PercentWordProblemFramework(WordProblemFramework):
    """Markup / discount / tax / tip money percents.

    Easy/Medium are calculator-appropriate: sensible prices and retail rates,
    with answers keyed to half-up-to-cents arithmetic (not integer truncation).
    Hard may use decimal rates, awkward cents, or discount-then-tax.
    """

    problem_kind = "percent"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        name = _pick_name(settings)
        tier = _tier(settings)
        variant = self._pick_variant(settings)
        if (
            tier == "hard"
            and bool(settings.get("allow_multi_step", True))
            and variant in {"discount", "tax"}
            and random.random() < 0.45
        ):
            return self._build_discount_then_tax(name, settings)

        price = self._sample_price(settings, tier)
        rate = self._sample_rate(settings, tier, variant)
        price_disp = _display_money(price)
        rate_disp = _display_rate(rate)

        if variant == "discount":
            answer = _apply_rate_factor(price, (Decimal(100) - rate) / Decimal(100))
            latex = (
                rf"\text{{{name} buys an item priced at \${price_disp}. "
                rf"It is on sale for {rate_disp}\% off. What is the sale price?}}"
            )
            text = (
                f"{name} buys an item priced at ${price_disp}. "
                f"It is on sale for {rate_disp}% off. What is the sale price?"
            )
        elif variant == "tax":
            answer = _apply_rate_factor(price, (Decimal(100) + rate) / Decimal(100))
            latex = (
                rf"\text{{A \${price_disp} purchase has {rate_disp}\% sales tax added. "
                rf"What is the total cost?}}"
            )
            text = (
                f"A ${price_disp} purchase has {rate_disp}% sales tax added. "
                f"What is the total cost?"
            )
        elif variant == "markup":
            answer = _apply_rate_factor(price, (Decimal(100) + rate) / Decimal(100))
            latex = (
                rf"\text{{A store marks up a \${price_disp} item by {rate_disp}\%. "
                rf"What is the selling price?}}"
            )
            text = (
                f"A store marks up a ${price_disp} item by {rate_disp}%. "
                f"What is the selling price?"
            )
        else:  # tip
            if random.random() < 0.5:
                answer = _percent_of(price, rate)
                latex = (
                    rf"\text{{{name} leaves a {rate_disp}\% tip on a \${price_disp} bill. "
                    rf"How much is the tip?}}"
                )
                text = (
                    f"{name} leaves a {rate_disp}% tip on a ${price_disp} bill. "
                    f"How much is the tip?"
                )
            else:
                answer = _apply_rate_factor(price, (Decimal(100) + rate) / Decimal(100))
                latex = (
                    rf"\text{{{name} leaves a {rate_disp}\% tip on a \${price_disp} bill. "
                    rf"What is the total, including tip?}}"
                )
                text = (
                    f"{name} leaves a {rate_disp}% tip on a ${price_disp} bill. "
                    f"What is the total, including tip?"
                )

        money = _format_money(answer)
        if str(settings.get("answer_units", "")):
            return latex, text, _append_units(money, settings)
        return latex, text, f"\\${money}"

    @staticmethod
    def _pick_variant(settings: dict) -> str:
        flags = (
            ("discount", bool(settings.get("allow_discount", True))),
            ("tax", bool(settings.get("allow_tax", True))),
            ("markup", bool(settings.get("allow_markup", True))),
            ("tip", bool(settings.get("allow_tip", True))),
        )
        allowed = [name for name, on in flags if on]
        if not allowed:
            allowed = ["discount", "tax", "markup"]
        return random.choice(allowed)

    @staticmethod
    def _sample_price(settings: dict, tier: str) -> Decimal:
        allow_cents = bool(settings.get("allow_price_cents", tier != "easy"))
        if tier == "easy":
            return Decimal(random.randint(15, 120))
        if tier == "medium":
            dollars = random.randint(20, 180)
            if allow_cents and random.random() < 0.55:
                cents = random.choice([50, 95, 99])
                return Decimal(dollars) + Decimal(cents) / Decimal(100)
            return Decimal(dollars)
        dollars = random.randint(25, 250)
        if allow_cents and random.random() < 0.75:
            cents = random.choice([19, 25, 49, 50, 75, 89, 95, 99])
            return Decimal(dollars) + Decimal(cents) / Decimal(100)
        return Decimal(dollars)

    @staticmethod
    def _sample_rate(settings: dict, tier: str, variant: str) -> Decimal:
        allow_decimal = bool(settings.get("allow_decimal_rates", tier == "hard"))
        if variant == "tax":
            if tier == "easy":
                choices: list[Decimal | int | float] = [5, 6, 7, 8, 10]
            elif tier == "medium":
                choices = (
                    [5, 6, 7, 7.5, 8, 8.25, 9, 10]
                    if allow_decimal
                    else [5, 6, 7, 8, 9, 10]
                )
            else:
                choices = (
                    [4.75, 5.5, 6.25, 7.25, 7.5, 8.25, 8.875, 9.5]
                    if allow_decimal
                    else [5, 6, 7, 8, 9, 11, 12]
                )
        elif variant == "tip":
            if tier == "easy":
                choices = [10, 15, 18, 20]
            elif tier == "medium":
                choices = [15, 18, 20, 22]
            else:
                choices = (
                    [17.5, 18, 18.5, 20, 22.5]
                    if allow_decimal
                    else [15, 18, 20, 22, 25]
                )
        else:  # discount / markup
            if tier == "easy":
                choices = [10, 15, 20, 25]
            elif tier == "medium":
                choices = [8, 10, 12, 15, 20, 25, 30]
            else:
                choices = (
                    [7.5, 12.5, 15, 17.5, 22.5, 33]
                    if allow_decimal
                    else [8, 12, 15, 18, 22, 35]
                )
        return _as_decimal(random.choice(choices))

    def _build_discount_then_tax(
        self, name: str, settings: dict
    ) -> tuple[str, str, str | None]:
        """Hard multi-step: percent off, then sales tax on the sale price."""
        price = self._sample_price(settings, "hard")
        discount = self._sample_rate(settings, "hard", "discount")
        tax = self._sample_rate(settings, "hard", "tax")
        sale = _apply_rate_factor(price, (Decimal(100) - discount) / Decimal(100))
        total = _apply_rate_factor(sale, (Decimal(100) + tax) / Decimal(100))
        price_disp = _display_money(price)
        disc_disp = _display_rate(discount)
        tax_disp = _display_rate(tax)
        latex = (
            rf"\text{{{name} buys an item priced at \${price_disp}. "
            rf"It is {disc_disp}\% off, and then {tax_disp}\% sales tax is added. "
            rf"What is the final price?}}"
        )
        text = (
            f"{name} buys an item priced at ${price_disp}. "
            f"It is {disc_disp}% off, and then {tax_disp}% sales tax is added. "
            f"What is the final price?"
        )
        money = _format_money(total)
        if str(settings.get("answer_units", "")):
            return latex, text, _append_units(money, settings)
        return latex, text, f"\\${money}"



_COMPOUND_FREQ: dict[int, str] = {
    1: "annually",
    2: "semiannually",
    4: "quarterly",
    12: "monthly",
}


def _money_display(amount: float) -> str:
    """Format a dollar amount for prompts/keys (whole dollars omit cents when exact)."""
    cents = int(round(amount * 100))
    if cents % 100 == 0:
        return str(cents // 100)
    return f"{cents / 100:.2f}"


def _money_answer(amount: float) -> str:
    return f"\\${_money_display(amount)}"


# G6 / Pre-Algebra interest: plug into I=Prt / A=P(1+rt) or A=P(1+r/n)^{nt} only.
# Never solve for rate (precalc), time (logs / rearrange), or principal.
_INTEREST_FORWARD_ASKS = ("interest", "amount")


class InterestWordProblemFramework(WordProblemFramework):
    """Simple interest (I = Prt) and compound interest word problems.

    PA / G6 skill is forward plug-in only: given P, r, t (and n for compound),
    find interest earned or future value. Continuous D scales magnitudes.
    """

    problem_kind = "interest"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        d = _topic_d(settings)
        band = _band_from_d(d)
        name = _pick_name(settings)
        kind = self._pick_kind(settings, band)
        if kind == "simple":
            return self._simple(settings, name, band, d)
        return self._compound(settings, name, band, d)

    def _pick_kind(self, settings: dict, band: str) -> str:
        forced = str(settings.get("interest_kind", "mixed")).lower()
        if forced in ("simple", "compound"):
            return forced
        if band == "easy":
            return "simple" if random.random() < 0.75 else "compound"
        if band == "hard":
            return "simple" if random.random() < 0.35 else "compound"
        return "simple" if random.random() < 0.5 else "compound"

    @staticmethod
    def _forward_ask(band: str) -> str:
        """Only interest earned or ending balance — never reverse for r / t / P."""
        if band == "easy":
            return random.choice(["interest", "interest", "amount"])
        return random.choice(list(_INTEREST_FORWARD_ASKS))

    @staticmethod
    def _principal_scale(d: float) -> float:
        """Continuous D inflates principal magnitude beyond band baselines."""
        # d≈0 → 1×; d≈8 → ~1.3×; d≈20 → ~2×; keeps answers calculator-friendly.
        return 1.0 + max(0.0, d) / 20.0

    def _simple_params(self, band: str, d: float) -> tuple[int, float, int]:
        """Return (principal dollars, rate percent, time years) with nice I when easy."""
        scale = self._principal_scale(d)
        if band == "easy":
            for _ in range(60):
                base = random.choice(
                    [100, 200, 250, 400, 500, 800, 1000, 1200, 1500, 2000]
                )
                p = int(round(base * scale / 50.0) * 50) or base
                r = float(random.choice([2, 3, 4, 5, 6, 8, 10]))
                t = random.choice([1, 2, 3, 4, 5])
                if (p * int(r) * t) % 100 == 0:
                    return p, r, t
            return 1000, 5.0, 2
        if band == "hard":
            for _ in range(60):
                base = random.choice(
                    [750, 1250, 1800, 2400, 3500, 4500, 5000, 7500, 10000]
                )
                p = int(round(base * scale / 50.0) * 50) or base
                r = float(random.choice([2.5, 3.5, 4.5, 5.5, 6.5, 7, 7.5, 8.5, 9]))
                t = random.choice([2, 3, 4, 5, 6, 8, 10])
                if d >= 16.0:
                    t = random.choice([4, 5, 6, 8, 10, 12])
                interest = p * (r / 100.0) * t
                if abs(interest * 100 - round(interest * 100)) < 1e-6:
                    return p, r, t
            return 5000, 5.0, 4
        base = random.choice([300, 450, 600, 800, 1000, 1500, 2000, 2500, 3000])
        p = int(round(base * scale / 50.0) * 50) or base
        r = float(random.choice([3, 4, 5, 6, 7, 8, 9, 10, 12]))
        t = random.choice([1, 2, 3, 4, 5, 6])
        return p, r, t

    def _simple(
        self, settings: dict, name: str, band: str, d: float
    ) -> tuple[str, str, str | None]:
        p, r, t = self._simple_params(band, d)
        rate_decimal = float(r) / 100
        interest = p * rate_decimal * t
        amount = p + interest
        years = "year" if t == 1 else "years"
        rate_show = int(r) if float(r).is_integer() else r
        find = self._forward_ask(band)

        if find == "interest":
            latex = (
                rf"\text{{{name} invests \${_money_display(p)} at {rate_show}\% "
                rf"simple interest for {t} {years}. How much interest is earned?}}"
            )
            text = (
                f"{name} invests ${_money_display(p)} at {rate_show}% "
                f"simple interest for {t} {years}. How much interest is earned?"
            )
            return latex, text, _money_answer(interest)

        # find == "amount" — A = P(1 + rt)
        latex = (
            rf"\text{{{name} deposits \${_money_display(p)} in an account that earns "
            rf"{rate_show}\% simple interest for {t} {years}. "
            rf"What is the account balance at the end of the term?}}"
        )
        text = (
            f"{name} deposits ${_money_display(p)} in an account that earns "
            f"{rate_show}% simple interest for {t} {years}. "
            f"What is the account balance at the end of the term?"
        )
        return latex, text, _money_answer(amount)

    def _compound_params(
        self, band: str, d: float
    ) -> tuple[int, int, int, int]:
        """Return (P, r_percent, t_years, n_compounds_per_year)."""
        scale = self._principal_scale(d)
        if band == "easy":
            base = random.choice([500, 800, 1000, 1200, 1500, 2000])
            p = int(round(base * scale / 50.0) * 50) or base
            r = random.choice([2, 3, 4, 5, 6, 8, 10])
            t = random.choice([1, 2, 3])
            n = 1  # annual compounding for easy
            return p, r, t, n
        if band == "hard":
            base = random.choice([1000, 1500, 2000, 2500, 3500, 5000, 8000])
            p = int(round(base * scale / 50.0) * 50) or base
            r = random.choice([3, 4, 5, 6, 7, 8, 9, 12])
            t = random.choice([3, 4, 5, 6, 8, 10])
            if d >= 16.0:
                t = random.choice([5, 6, 8, 10, 12])
            n = random.choice([2, 4, 12])
            return p, r, t, n
        base = random.choice([800, 1000, 1200, 1500, 2000, 2500, 3000])
        p = int(round(base * scale / 50.0) * 50) or base
        r = random.choice([3, 4, 5, 6, 8, 10])
        t = random.choice([2, 3, 4, 5])
        n = random.choice([1, 1, 2, 4])  # mostly annual / semiannual / quarterly
        return p, r, t, n

    def _compound(
        self, settings: dict, name: str, band: str, d: float
    ) -> tuple[str, str, str | None]:
        p, r, t, n = self._compound_params(band, d)
        amount = p * (1 + r / (100 * n)) ** (n * t)
        interest = amount - p
        years = "year" if t == 1 else "years"
        freq = _COMPOUND_FREQ[n]
        find = self._forward_ask(band)

        if n == 1:
            latex_core = (
                rf"{name} invests \${_money_display(p)} in an account that pays "
                rf"{r}\% interest compounded annually for {t} {years}."
            )
            text_core = (
                f"{name} invests ${_money_display(p)} in an account that pays "
                f"{r}% interest compounded annually for {t} {years}."
            )
        else:
            latex_core = (
                rf"{name} invests \${_money_display(p)} at {r}\% interest "
                rf"compounded {freq} for {t} {years}."
            )
            text_core = (
                f"{name} invests ${_money_display(p)} at {r}% interest "
                f"compounded {freq} for {t} {years}."
            )

        if find == "interest":
            latex = rf"\text{{{latex_core} How much interest is earned?}}"
            text = f"{text_core} How much interest is earned?"
            return latex, text, _money_answer(interest)

        latex = rf"\text{{{latex_core} What is the balance at the end of the term?}}"
        text = f"{text_core} What is the balance at the end of the term?"
        return latex, text, _money_answer(amount)


class ProportionWordProblemFramework(WordProblemFramework):
    problem_kind = "proportion"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        unit_count = _random_value(settings, lo=2, hi=6)
        unit_price_cents = random.choice([50, 75, 100, 125, 150, 200])
        target_count = unit_count + _random_value(settings, lo=2, hi=6)
        cost_cents = unit_price_cents * target_count // unit_count
        answer = _format_answer(cost_cents / 100, settings)
        items = random.choice(["apples", "notebooks", "markers", "bottles of water"])
        latex = (
            rf"\text{{If {unit_count} {items} cost \${unit_price_cents / 100:.2f}, "
            rf"how much do {target_count} {items} cost at the same rate?}}"
        )
        text = (
            f"If {unit_count} {items} cost ${unit_price_cents / 100:.2f}, "
            f"how much do {target_count} {items} cost at the same rate?"
        )
        return latex, text, f"\\${answer}"


class OneStepEquationWordFramework(WordProblemFramework):
    problem_kind = "one_step_equation"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        name = _pick_name(settings)
        op = random.choice(["subtract", "add", "multiply", "divide"])

        if op == "subtract":
            # start - spent = left → solve for start
            spent = _random_value(settings, lo=5, hi=20)
            left = _random_value(settings, lo=10, hi=60)
            start = left + spent
            answer = _format_answer(start, settings)
            latex = (
                rf"\text{{{name} had some money, spent \${spent}, and has \${left} left. "
                rf"How much did {name} start with?}}"
            )
            text = (
                f"{name} had some money, spent ${spent}, and has ${left} left. "
                f"How much did {name} start with?"
            )
        elif op == "add":
            # start + received = total → solve for start (keep start positive)
            received = _random_value(settings, lo=5, hi=20)
            start = _random_value(settings, lo=5, hi=40)
            total = start + received
            answer = _format_answer(start, settings)
            latex = (
                rf"\text{{{name} had some money, received \${received}, and now has \${total}. "
                rf"How much did {name} start with?}}"
            )
            text = (
                f"{name} had some money, received ${received}, and now has ${total}. "
                f"How much did {name} start with?"
            )
        elif op == "multiply":
            # factor * each = total → solve for each (exact product)
            factor = random.choice([2, 3, 4, 5])
            each = _random_value(settings, lo=5, hi=20)
            total = each * factor
            answer = _format_answer(each, settings)
            latex = (
                rf"\text{{{name} collected {factor} equal donations totaling \${total}. "
                rf"How much was each donation?}}"
            )
            text = (
                f"{name} collected {factor} equal donations totaling ${total}. "
                f"How much was each donation?"
            )
        else:
            # total shared equally among factor → each = total / factor (not the total)
            factor = random.choice([2, 3, 4, 5])
            each = _random_value(settings, lo=10, hi=60)
            total = each * factor
            answer = _format_answer(each, settings)
            latex = (
                rf"\text{{{name} shared \${total} equally among {factor} friends. "
                rf"How much did each friend receive?}}"
            )
            text = (
                f"{name} shared ${total} equally among {factor} friends. "
                f"How much did each friend receive?"
            )

        return latex, text, f"\\${answer}"


class TwoStepEquationWordFramework(WordProblemFramework):
    problem_kind = "two_step_equation"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        for _ in range(40):
            coeff = random.choice([2, 3, 4, 5])
            constant = _random_value(settings, lo=3, hi=15)
            number = _random_value(settings, lo=4, hi=20)
            result = coeff * number - constant
            if result <= 0:
                continue
            answer = _format_answer(number, settings)
            latex = (
                rf"\text{{{constant} less than {coeff} times a number is {result}. "
                rf"Find the number.}}"
            )
            text = f"{constant} less than {coeff} times a number is {result}. Find the number."
            return latex, text, answer

        number = 5
        answer = _format_answer(number, settings)
        latex = r"\text{7 less than 3 times a number is 8. Find the number.}"
        text = "7 less than 3 times a number is 8. Find the number."
        return latex, text, answer


class SystemsWordProblemFramework(WordProblemFramework):
    problem_kind = "systems"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        adult_price = random.choice([10, 12, 15])
        child_price = adult_price - random.choice([2, 4])
        child_count = _random_value(settings, lo=20, hi=60)
        adult_count = _random_value(settings, lo=20, hi=60)
        total_tickets = adult_count + child_count
        total_revenue = adult_count * adult_price + child_count * child_price
        answer = _format_answer(adult_count, settings)
        latex = (
            rf"\text{{Adult tickets cost \${adult_price} and child tickets cost \${child_price}. "
            rf"{total_tickets} tickets were sold for a total of \${total_revenue}. "
            rf"How many adult tickets were sold?}}"
        )
        text = (
            f"Adult tickets cost ${adult_price} and child tickets cost ${child_price}. "
            f"{total_tickets} tickets were sold for a total of ${total_revenue}. "
            f"How many adult tickets were sold?"
        )
        return latex, text, answer


class InequalityWordProblemFramework(WordProblemFramework):
    problem_kind = "inequality"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        name = _pick_name(settings)
        tests_taken = random.choice([3, 4, 5])
        current_total = _random_value(settings, lo=60, hi=90) * tests_taken // 3
        goal = current_total + _random_value(settings, lo=15, hi=40)
        needed = math.ceil((goal - current_total))
        answer = _format_answer(needed, settings)
        latex = (
            rf"\text{{{name} has scored a total of {current_total} points on {tests_taken} tests "
            rf"and wants at least {goal} points after one more test. "
            rf"What is the minimum score needed on the next test?}}"
        )
        text = (
            f"{name} has scored a total of {current_total} points on {tests_taken} tests "
            f"and wants at least {goal} points after one more test. "
            f"What is the minimum score needed on the next test?"
        )
        return latex, text, answer


class GcfLcmWordFramework(WordProblemFramework):
    problem_kind = "gcf_lcm"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        from question_engine.frameworks.difficulty_budget import settings_difficulty
        from question_engine.word_problems.things import (
            SAME_LETTER_MIN_DIFFICULTY,
            pick_things,
        )

        variant = random.choice(["lcm", "gcf"])
        require_gt_one = bool(settings.get("require_gcf_greater_than_one", True))
        prefer_same_letter = False
        if "difficulty" in settings and settings["difficulty"] is not None:
            d = settings_difficulty(settings, default=0.0)
            prefer_same_letter = d >= SAME_LETTER_MIN_DIFFICULTY - 1e-9
        item_a, item_b = pick_things(2, prefer_same_first_letter=prefer_same_letter)

        if variant == "lcm":
            a = random.choice([6, 8, 9, 10, 12])
            b_choices = [n for n in (8, 10, 12, 15, 18) if n != a]
            b = random.choice(b_choices)
            value = math.lcm(a, b)
            answer = _format_answer(value, settings)
            text = (
                f"{item_a.capitalize()} come in packs of {a} and {item_b} come in packs of {b}. "
                f"What is the least number of each needed so there are no leftovers?"
            )
            latex = rf"\text{{{text}}}"
        else:
            g_lo = 2 if require_gt_one else 1
            g = random.randint(g_lo, 6)
            multipliers = [2, 3, 4, 5, 6, 7, 8, 9]
            m1 = random.choice(multipliers)
            m2 = random.choice([m for m in multipliers if m != m1 and math.gcd(m1, m) == 1])
            count_a, count_b = m1 * g, m2 * g
            answer = _format_answer(g, settings)
            text = (
                f"You have {count_a} {item_a} and {count_b} {item_b}. "
                f"What is the greatest number of identical bags you can make?"
            )
            latex = rf"\text{{{text}}}"
        return latex, text, answer


class NumberLineWordFramework(WordProblemFramework):
    problem_kind = "number_line"

    def __init__(self, template: WordProblemTemplate | None = None) -> None:
        super().__init__(template)
        self._last_start: float | None = None
        self._last_end: float | None = None

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        start = _random_value(settings, lo=-15, hi=10)
        change = _random_value(settings, lo=3, hi=20)
        if random.choice([True, False]):
            end = start + change
            latex = (
                rf"\text{{The temperature was {start}\textdegree{{}}F and rose {change}\textdegree{{}}F. "
                rf"What is the new temperature?}}"
            )
            text = f"The temperature was {start}°F and rose {change}°F. What is the new temperature?"
        else:
            end = start - change
            latex = (
                rf"\text{{The temperature was {start}\textdegree{{}}F and dropped {change}\textdegree{{}}F. "
                rf"What is the new temperature?}}"
            )
            text = f"The temperature was {start}°F and dropped {change}°F. What is the new temperature?"
        self._last_start = float(start)
        self._last_end = float(end)
        answer = _format_answer(end, settings)
        return latex, text, answer

    def build_question_metadata(
        self,
        settings: dict,
        *,
        prompt_latex: str,
        prompt_text: str,
        answer: str | None,
    ) -> dict[str, Any]:
        from .graphing import (
            NumberLineSpec,
            _number_line_bounds,
            _number_line_show_zero,
            include_graph_metadata,
            metadata_from_number_line_spec,
        )

        if not include_graph_metadata(settings) or self._last_end is None:
            return {}
        extras = (self._last_end,)
        if self._last_start is not None:
            extras = (self._last_start, self._last_end)
        lo, hi, tick = _number_line_bounds(settings, *extras)
        # Blank prompt line for student work; answer key marks the final value.
        spec = NumberLineSpec(
            min_value=lo,
            max_value=hi,
            boundary=self._last_end,
            direction="both",
            inclusive=True,
            tick_interval=tick,
            show_zero=_number_line_show_zero(settings),
        )
        return metadata_from_number_line_spec(spec, prompt="blank")


class CoordinateDistanceWordFramework(WordProblemFramework):
    problem_kind = "coordinate_distance"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        x1 = _random_value(settings, lo=-5, hi=5)
        y1 = _random_value(settings, lo=-5, hi=5)
        dx = _random_value(settings, lo=3, hi=8)
        dy = _random_value(settings, lo=3, hi=8)
        x2, y2 = x1 + dx, y1 + dy
        distance = math.sqrt(dx * dx + dy * dy)
        answer = _format_answer(distance, settings)
        unit = _unit_label(settings, "units") or "units"
        latex = (
            rf"\text{{Point A is at ({x1}, {y1}) and point B is at ({x2}, {y2}) on a coordinate plane. "
            rf"How far apart are the points in {unit}?}}"
        )
        text = (
            f"Point A is at ({x1}, {y1}) and point B is at ({x2}, {y2}) on a coordinate plane. "
            f"How far apart are the points in {unit}?"
        )
        return latex, text, _append_units(answer, settings)


class SimilarFiguresWordFramework(WordProblemFramework):
    problem_kind = "similar_figures"

    def __init__(self) -> None:
        super().__init__()
        self._last: dict[str, Any] = {}

    @staticmethod
    def _use_diagram(settings: dict) -> bool:
        style = str(settings.get("prompt_style", "diagram")).strip().lower()
        if style in {"description_only", "description", "text", "text_only"}:
            return False
        if "include_figure" in settings:
            return bool(settings["include_figure"])
        if "include_diagram" in settings:
            return bool(settings["include_diagram"])
        return True

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        from ..diagrams import similar_figures_pair_figure

        ratio = random.choice([2, 3, 4])
        small_side = _random_value(settings, lo=3, hi=10)
        other_small = _random_value(settings, lo=3, hi=10)
        while other_small == small_side:
            other_small = _random_value(settings, lo=3, hi=10)
        large_side = small_side * ratio
        other_large = other_small * ratio
        unit = _unit_label(settings, "cm") or "cm"
        shape = random.choice(["triangle", "rectangle"])
        task = random.choice(["missing_side", "missing_side", "scale_factor"])
        use_diagram = self._use_diagram(settings)

        if shape == "triangle":
            small_labels = ("A", "B", "C")
            large_labels = ("D", "E", "F")
            angles = random.choice([(50, 60, 70), (40, 70, 70), (45, 55, 80)])
            aspect = (3.0, 2.0)
            corresponding = ("AB", "DE")
            other_pair = ("BC", "EF")
            similar_stmt_latex = r"\triangle ABC \sim \triangle DEF"
            similar_stmt_text = "Triangle ABC ~ triangle DEF"
        else:
            small_labels = ("A", "B", "C", "D")
            large_labels = ("E", "F", "G", "H")
            angles = (50.0, 60.0, 70.0)
            aspect = random.choice([(3.0, 2.0), (5.0, 3.0), (4.0, 2.0)])
            corresponding = ("AB", "EF")
            other_pair = ("AD", "EH")
            similar_stmt_latex = r"ABCD \sim EFGH"
            similar_stmt_text = "Quadrilateral ABCD ~ EFGH"

        fig = None
        if use_diagram:
            if task == "scale_factor":
                small_side_labels = {
                    corresponding[0]: f"{small_side} {unit}",
                    other_pair[0]: f"{other_small} {unit}",
                }
                large_side_labels = {
                    corresponding[1]: f"{large_side} {unit}",
                    other_pair[1]: f"{other_large} {unit}",
                }
                answer = str(ratio)
                latex = (
                    rf"{similar_stmt_latex}.\ "
                    rf"\text{{The figures are similar. Find the scale factor from the smaller to the larger.}}"
                )
                text = (
                    f"{similar_stmt_text}. "
                    "The figures are similar. Find the scale factor from the smaller to the larger."
                )
            else:
                small_side_labels = {
                    corresponding[0]: f"{small_side} {unit}",
                    other_pair[0]: f"{other_small} {unit}",
                }
                large_side_labels = {
                    corresponding[1]: f"{large_side} {unit}",
                    other_pair[1]: "?",
                }
                answer = _append_units(_format_answer(other_large, settings), settings)
                missing = other_pair[1]
                latex = (
                    rf"{similar_stmt_latex}.\ "
                    rf"\text{{Find the length of }} {missing}."
                )
                text = f"{similar_stmt_text}. Find the length of {missing}."
            fig = similar_figures_pair_figure(
                shape=shape,  # type: ignore[arg-type]
                small_labels=small_labels,
                large_labels=large_labels,
                small_side_labels=small_side_labels,
                large_side_labels=large_side_labels,
                angles=angles,
                aspect=aspect,
                scale_factor=float(ratio),
            )
            self._last = {"figure": fig, "task": task, "shape": shape}
            return latex, text, answer

        # description_only
        self._last = {"figure": None, "task": task, "shape": shape}
        if task == "scale_factor":
            answer = str(ratio)
            latex = (
                rf"\text{{Two similar {shape}s have corresponding sides of length }} "
                rf"{small_side}\text{{ {unit} and }} {large_side}\text{{ {unit}. "
                rf"Find the scale factor from the smaller to the larger.}}"
            )
            text = (
                f"Two similar {shape}s have corresponding sides of length "
                f"{small_side} {unit} and {large_side} {unit}. "
                "Find the scale factor from the smaller to the larger."
            )
            return latex, text, answer

        answer = _append_units(_format_answer(large_side, settings), settings)
        latex = (
            rf"\text{{Two similar {shape}s have a scale factor of {ratio}:1. "
            rf"The smaller {shape} has a side of {small_side} {unit}. "
            rf"What is the corresponding side in the larger {shape}?}}"
        )
        text = (
            f"Two similar {shape}s have a scale factor of {ratio}:1. "
            f"The smaller {shape} has a side of {small_side} {unit}. "
            f"What is the corresponding side in the larger {shape}?"
        )
        return latex, text, answer

    def build_question_metadata(
        self,
        settings: dict,
        *,
        prompt_latex: str,
        prompt_text: str,
        answer: str | None,
    ) -> dict[str, Any]:
        fig = (self._last or {}).get("figure")
        if fig is None or not self._use_diagram(settings):
            return {}
        return fig.to_metadata()
