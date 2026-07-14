"""Additional geometry frameworks — angles, polygons, special triangles, circles."""

from __future__ import annotations

import math
import random
from typing import Any

from packages.polynomial_core import format_linear_latex, format_with_unit, unit_latex

from .base import QuestionFramework
from .geometry import (
    GeometryFramework,
    _ANGLE_LABELS,
    _TRIANGLE_LABELS,
    _angle_symbol,
    _bounds,
    _diagram_enabled,
    _figure_metadata,
    _format_angle,
    _measurement_unit,
    _pythagorean_triple,
    _random_angle,
    _random_radius,
    _random_side,
)
from ..diagrams import (
    adjacent_angles_figure,
    angle_figure,
    circle_figure,
    complementary_angles_figure,
    kite_figure,
    parallel_lines_transversal_figure,
    parallelogram_figure,
    right_triangle_figure,
    segment_figure,
    supplementary_angles_figure,
    trapezoid_figure,
    triangle_figure,
    vertical_angles_figure,
)
from ..generators.utils import random_int_range


def _difficulty_tier(settings: dict) -> str:
    tier = str(settings.get("difficulty_tier") or "medium").strip().lower()
    if tier in {"easy", "medium", "hard"}:
        return tier
    return "medium"


def _coef_bound(settings: dict, default: int = 4) -> int:
    lo = abs(int(settings.get("coef_min", -default)))
    hi = abs(int(settings.get("coef_max", default)))
    return max(1, min(6, lo or default, hi or default))


def _linear_expr_for_value(value: int, x: int, coef_bound: int) -> tuple[int, int]:
    """Return ``(a, b)`` so ``a*x + b == value`` with small classroom coefficients."""
    candidates: list[tuple[int, int]] = []
    for a in range(1, coef_bound + 1):
        b = value - a * x
        if abs(b) <= 40:
            candidates.append((a, b))
        b_neg = value - (-a) * x
        if abs(b_neg) <= 40:
            candidates.append((-a, b_neg))
    if not candidates:
        a = random.randint(1, max(1, coef_bound))
        return a, value - a * x
    return random.choice(candidates)


def _expr_latex(a: int, b: int) -> str:
    return format_linear_latex(a, b, variable="x")


class AngleAdditionFramework(GeometryFramework):
    """Angle Addition Postulate: find a whole or part from a multi-ray figure."""

    def __init__(self) -> None:
        super().__init__(figure_type="composite")
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        symbol = _angle_symbol(settings)
        tier = _difficulty_tier(settings)

        if tier == "easy":
            n = 2
            mode = random.choice(["find_total", "find_part"])
        elif tier == "medium":
            n = random.choice([2, 3])
            mode = random.choice(["find_total", "find_part", "find_span"])
        else:
            n = random.choice([3, 4])
            mode = random.choice(["find_span", "find_part", "find_span", "find_total"])

        cap = 160 if tier == "easy" else 175
        pieces: list[int] = []
        for _attempt in range(12):
            pieces = []
            remaining = random.randint(max(40, 20 * n), cap)
            ok = True
            for i in range(n - 1):
                left = n - i
                hi = remaining - 12 * (left - 1)
                if hi < 12:
                    ok = False
                    break
                pieces.append(
                    random.randint(12, max(12, min(hi, remaining // left + 15)))
                )
                remaining -= pieces[-1]
            if not ok:
                continue
            pieces.append(remaining)
            if pieces[-1] >= 12:
                break
        else:
            pieces = [20] * (n - 1) + [30]

        tip_count = n + 1
        labels = random.sample(_ANGLE_LABELS, tip_count + 1)
        vertex = labels[0]
        tips = labels[1:]

        if mode == "find_total":
            ask_start, ask_end = 0, n
            answer_val = sum(pieces)
            piece_marks = [f"{p}\u00b0" for p in pieces]
            span_marks = [(0, n, "?")]
            given_bits = [
                f"m\\angle {tips[i]}{vertex}{tips[i + 1]} = {pieces[i]}{symbol}"
                for i in range(n)
            ]
            prompt = (
                f"\\text{{In the diagram, }} "
                + "\\text{{ and }} ".join(given_bits)
                + f".\\ \\text{{Find }} m\\angle {tips[0]}{vertex}{tips[-1]}."
            )
        elif mode == "find_part":
            miss = random.randrange(n)
            ask_start, ask_end = miss, miss + 1
            answer_val = pieces[miss]
            piece_marks = [
                "?" if i == miss else f"{p}\u00b0" for i, p in enumerate(pieces)
            ]
            span_marks = [(0, n, f"{sum(pieces)}\u00b0")]
            labeled = [
                f"m\\angle {tips[i]}{vertex}{tips[i + 1]} = {pieces[i]}{symbol}"
                for i in range(n)
                if i != miss
            ]
            prompt = (
                f"\\text{{In the diagram, }} m\\angle {tips[0]}{vertex}{tips[-1]}"
                f" = {sum(pieces)}{symbol}"
            )
            if labeled:
                prompt += "\\text{{ and }} " + "\\text{{, }} ".join(labeled)
            prompt += (
                f".\\ \\text{{Find }} m\\angle {tips[miss]}{vertex}{tips[miss + 1]}."
            )
        else:
            max_start = n - 2
            ask_start = random.randint(0, max(0, max_start))
            ask_end = random.randint(ask_start + 2, n)
            answer_val = sum(pieces[ask_start:ask_end])
            piece_marks = [f"{p}\u00b0" for p in pieces]
            span_marks = [(ask_start, ask_end, "?")]
            if tier == "hard" and ask_end - ask_start < n and random.random() < 0.55:
                span_marks.append((0, n, f"{sum(pieces)}\u00b0"))
            prompt = (
                f"\\text{{Use the diagram to find }} "
                f"m\\angle {tips[ask_start]}{vertex}{tips[ask_end]}."
            )

        fig = adjacent_angles_figure(
            [float(p) for p in pieces],
            tip_labels=tips,
            vertex_label=vertex,
            piece_labels=piece_marks,
            span_marks=span_marks,
            kind="angle_addition",
        )
        answer = f"{answer_val}{symbol}"
        self._last = {
            "figure": fig,
            "labels": [tips[ask_start], vertex, tips[ask_end], *tips],
            "angle": answer_val,
            "pieces": pieces,
            "ask_span": (ask_start, ask_end),
            "mode": mode,
        }
        return prompt, "angle addition", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_question_metadata(self, settings: dict, **_: Any) -> dict[str, Any]:
        last = self._last
        if not last:
            return {}
        return _figure_metadata(
            settings,
            figure_type="composite",
            labels=last["labels"],
            dimensions={"angle_deg": float(last["angle"])},
            diagram=last.get("figure") if _diagram_enabled(settings) else None,
        )


class SegmentAdditionFramework(GeometryFramework):
    """Segment Addition Postulate."""

    def __init__(self) -> None:
        super().__init__(figure_type="composite")
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        unit = _measurement_unit(settings)
        a_len = _random_side(settings)
        b_len = _random_side(settings)
        total = a_len + b_len
        p, q, r = random.sample(_ANGLE_LABELS, 3)
        if random.choice([True, False]):
            prompt = (
                f"\\text{{Point }} {q} \\text{{ is on }} \\overline{{{p}{r}}}.\\ "
                f"{p}{q} = {a_len}\\text{{ {unit}}} \\text{{ and }} "
                f"{q}{r} = {b_len}\\text{{ {unit}}}.\\ "
                f"\\text{{Find }} {p}{r}."
            )
            answer = f"{total}\\text{{ {unit}}}"
        else:
            prompt = (
                f"\\text{{Point }} {q} \\text{{ is on }} \\overline{{{p}{r}}}.\\ "
                f"{p}{r} = {total}\\text{{ {unit}}} \\text{{ and }} "
                f"{p}{q} = {a_len}\\text{{ {unit}}}.\\ "
                f"\\text{{Find }} {q}{r}."
            )
            answer = f"{b_len}\\text{{ {unit}}}"
        self._last = {
            "figure": segment_figure(float(total), labels=(p, r), unit=unit),
            "labels": [p, r],
            "length": total,
        }
        return prompt, "segment addition", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_question_metadata(self, settings: dict, **_: Any) -> dict[str, Any]:
        last = self._last
        if not last:
            return {}
        return _figure_metadata(
            settings,
            figure_type="composite",
            labels=last["labels"],
            dimensions={"length": float(last["length"])},
            diagram=last.get("figure") if _diagram_enabled(settings) else None,
        )


class AngleRelationshipsFramework(GeometryFramework):
    """Complementary, supplementary, or vertical angles — from relationship diagrams."""

    def __init__(self) -> None:
        super().__init__(figure_type="composite")
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        symbol = _angle_symbol(settings)
        kind = random.choice(["complementary", "supplementary", "vertical"])
        if kind == "complementary":
            angle = random.randint(15, 75)
            other = 90 - angle
            labels = tuple(random.sample(_ANGLE_LABELS, 4))
            fig = complementary_angles_figure(float(angle), labels=labels)
            prompt = (
                f"\\text{{The diagram shows complementary angles. "
                f"Find the measure of the unmarked angle.}}"
            )
            answer = f"{other}{symbol}"
            meta_labels = list(labels)
        elif kind == "supplementary":
            angle = random.randint(25, 155)
            other = 180 - angle
            labels = tuple(random.sample(_ANGLE_LABELS, 4))
            fig = supplementary_angles_figure(float(angle), labels=labels)
            prompt = (
                f"\\text{{The diagram shows supplementary angles on a straight line. "
                f"Find the measure of the unmarked angle.}}"
            )
            answer = f"{other}{symbol}"
            meta_labels = list(labels)
        else:
            angle = random.randint(25, 155)
            if abs(angle - 90) < 8:
                angle = 70 if angle < 90 else 110
            labels5 = tuple(random.sample(_ANGLE_LABELS, 5))
            fig = vertical_angles_figure(float(angle), labels=labels5)
            prompt = (
                f"\\text{{The diagram shows vertical angles formed by intersecting lines. "
                f"Find the measure of the unmarked angle.}}"
            )
            answer = f"{angle}{symbol}"
            meta_labels = list(labels5)
        self._last = {
            "figure": fig,
            "labels": meta_labels,
            "angle": angle,
            "kind": kind,
        }
        return prompt, f"angle relationship {kind}", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_question_metadata(self, settings: dict, **_: Any) -> dict[str, Any]:
        last = self._last
        if not last:
            return {}
        return _figure_metadata(
            settings,
            figure_type="composite",
            labels=last["labels"],
            dimensions={"angle_deg": float(last["angle"])},
            diagram=last.get("figure") if _diagram_enabled(settings) else None,
        )


class AlgebraFindingAnglesFramework(GeometryFramework):
    """Algebra 1 angle relationships — no inverse trig.

    Easy: numeric complementary / supplementary / vertical / adjacent on a line.
    Medium: algebraic expressions for complementary or supplementary angles.
    Hard: triangle angle-sum (and multi-step) with algebraic expressions.
    """

    def __init__(self) -> None:
        super().__init__(figure_type="composite")
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        tier = _difficulty_tier(settings)
        if tier == "easy":
            return self._build_easy(settings)
        if tier == "hard":
            return self._build_hard(settings)
        return self._build_medium(settings)

    def _build_easy(self, settings: dict) -> tuple[str, str, str | None]:
        symbol = _angle_symbol(settings)
        kind = random.choice(
            ["complementary", "supplementary", "vertical", "adjacent_line"]
        )
        vertex, p1, p2 = random.sample(_ANGLE_LABELS, 3)
        if kind == "complementary":
            angle = random.randint(15, 75)
            other = 90 - angle
            prompt = (
                f"\\text{{Two angles are complementary. One measures }} {angle}{symbol}."
                f"\\text{{ Find the measure of the other angle.}}"
            )
            answer = f"{other}{symbol}"
        elif kind == "supplementary":
            angle = random.randint(20, 160)
            other = 180 - angle
            prompt = (
                f"\\text{{Two angles are supplementary. One measures }} {angle}{symbol}."
                f"\\text{{ Find the measure of the other angle.}}"
            )
            answer = f"{other}{symbol}"
        elif kind == "vertical":
            angle = random.randint(20, 160)
            prompt = (
                f"\\text{{Vertical angles are congruent. If }} m\\angle {p1}{vertex}{p2}"
                f" = {angle}{symbol},\\text{{ find the measure of its vertical angle.}}"
            )
            answer = f"{angle}{symbol}"
        else:
            angle = random.randint(20, 160)
            other = 180 - angle
            prompt = (
                f"\\text{{Adjacent angles on a straight line are supplementary. "
                f"If one measures }} {angle}{symbol},"
                f"\\text{{ find the measure of the adjacent angle.}}"
            )
            answer = f"{other}{symbol}"
        self._last = {
            "figure": angle_figure(p1, vertex, p2, float(angle), show_measure=True),
            "labels": [p1, vertex, p2],
            "angle": angle,
            "figure_type": "composite",
        }
        return prompt, f"finding angles easy {kind}", answer

    def _build_medium(self, settings: dict) -> tuple[str, str, str | None]:
        symbol = _angle_symbol(settings)
        coef_bound = _coef_bound(settings, default=4)
        kind = random.choice(["complementary", "supplementary", "vertical"])
        ask = random.choice(["x", "measure"])
        x = random.randint(5, 25)
        vertex, p1, p2 = random.sample(_ANGLE_LABELS, 3)

        if kind == "vertical":
            measure = random.randint(25, 140)
            a1, b1 = _linear_expr_for_value(measure, x, coef_bound)
            a2, b2 = _linear_expr_for_value(measure, x, coef_bound)
            for _ in range(12):
                if (a1, b1) != (a2, b2):
                    break
                a2, b2 = _linear_expr_for_value(measure, x, coef_bound)
            e1, e2 = _expr_latex(a1, b1), _expr_latex(a2, b2)
            if ask == "x":
                prompt = (
                    f"\\text{{Vertical angles measure }} ({e1}){symbol}"
                    f"\\text{{ and }} ({e2}){symbol}."
                    f"\\text{{ Find }} x."
                )
                answer = str(x)
            else:
                prompt = (
                    f"\\text{{Vertical angles measure }} ({e1}){symbol}"
                    f"\\text{{ and }} ({e2}){symbol}."
                    f"\\text{{ Find the measure of each angle.}}"
                )
                answer = f"{measure}{symbol}"
            self._last = {
                "figure": angle_figure(p1, vertex, p2, float(measure), show_measure=False),
                "labels": [p1, vertex, p2],
                "angle": measure,
                "figure_type": "composite",
            }
            return prompt, "finding angles medium vertical", answer

        total = 90 if kind == "complementary" else 180
        lo, hi = (15, 75) if kind == "complementary" else (25, 155)
        m1 = random.randint(lo, hi)
        m2 = total - m1
        a1, b1 = _linear_expr_for_value(m1, x, coef_bound)
        a2, b2 = _linear_expr_for_value(m2, x, coef_bound)
        e1, e2 = _expr_latex(a1, b1), _expr_latex(a2, b2)
        relation = "complementary" if kind == "complementary" else "supplementary"
        if ask == "x":
            prompt = (
                f"\\text{{The angles }} ({e1}){symbol}\\text{{ and }} ({e2}){symbol}"
                f"\\text{{ are {relation}. Find }} x."
            )
            answer = str(x)
        else:
            which = random.choice([1, 2])
            target = m1 if which == 1 else m2
            prompt = (
                f"\\text{{The angles }} ({e1}){symbol}\\text{{ and }} ({e2}){symbol}"
                f"\\text{{ are {relation}. Find the measure of the "
                f"{'first' if which == 1 else 'second'} angle.}}"
            )
            answer = f"{target}{symbol}"
        self._last = {
            "figure": angle_figure(p1, vertex, p2, float(m1), show_measure=False),
            "labels": [p1, vertex, p2],
            "angle": m1,
            "figure_type": "composite",
        }
        return prompt, f"finding angles medium {kind}", answer

    def _build_hard(self, settings: dict) -> tuple[str, str, str | None]:
        symbol = _angle_symbol(settings)
        coef_bound = _coef_bound(settings, default=5)
        mode = random.choice(["triangle_algebra", "triangle_mixed", "multi_step"])
        labels = list(_TRIANGLE_LABELS)
        x = random.randint(5, 30)

        if mode == "multi_step":
            m1 = random.randint(20, 70)
            m2 = 90 - m1
            a1, b1 = _linear_expr_for_value(m1, x, coef_bound)
            a2, b2 = _linear_expr_for_value(m2, x, coef_bound)
            e1, e2 = _expr_latex(a1, b1), _expr_latex(a2, b2)
            ask_first = random.choice([True, False])
            ask_measure = m1 if ask_first else m2
            which = "first" if ask_first else "second"
            supplement = 180 - ask_measure
            prompt = (
                f"\\text{{Angles measuring }} ({e1}){symbol}\\text{{ and }} ({e2}){symbol}"
                f"\\text{{ are complementary. Find the measure of an angle that is "
                f"supplementary to the {which} angle.}}"
            )
            answer = f"{supplement}{symbol}"
            self._last = {
                "figure": angle_figure("A", "B", "C", float(ask_measure), show_measure=False),
                "labels": ["A", "B", "C"],
                "angle": ask_measure,
                "figure_type": "composite",
            }
            return prompt, "finding angles hard multi-step", answer

        a_ang = random.randint(20, 80)
        b_ang = random.randint(20, 80)
        while a_ang + b_ang >= 160:
            b_ang = random.randint(20, 80)
        c_ang = 180 - a_ang - b_ang
        angle_map = {"A": a_ang, "B": b_ang, "C": c_ang}
        angles = (a_ang, b_ang, c_ang)

        if mode == "triangle_mixed":
            known_label = random.choice(labels)
            alg_labels = [lab for lab in labels if lab != known_label]
            exprs: dict[str, str] = {}
            for lab in alg_labels:
                aa, bb = _linear_expr_for_value(angle_map[lab], x, coef_bound)
                exprs[lab] = _expr_latex(aa, bb)
            ask = random.choice(["x", "measure"])
            parts = [
                f"m\\angle {known_label} = {angle_map[known_label]}{symbol}",
            ]
            for lab in alg_labels:
                parts.append(f"m\\angle {lab} = ({exprs[lab]}){symbol}")
            random.shuffle(parts)
            if ask == "x":
                prompt = (
                    f"\\text{{In }} \\triangle {''.join(labels)},\\ "
                    f"{parts[0]},\\ {parts[1]},\\text{{ and }} {parts[2]}."
                    f"\\text{{ Find }} x."
                )
                answer = str(x)
            else:
                target = random.choice(alg_labels)
                prompt = (
                    f"\\text{{In }} \\triangle {''.join(labels)},\\ "
                    f"{parts[0]},\\ {parts[1]},\\text{{ and }} {parts[2]}."
                    f"\\text{{ Find }} m\\angle {target}."
                )
                answer = f"{angle_map[target]}{symbol}"
        else:
            exprs = {}
            for lab in labels:
                aa, bb = _linear_expr_for_value(angle_map[lab], x, coef_bound)
                exprs[lab] = _expr_latex(aa, bb)
            ask = random.choice(["x", "measure"])
            prompt = (
                f"\\text{{In }} \\triangle {''.join(labels)},\\ "
                f"m\\angle A = ({exprs['A']}){symbol},\\ "
                f"m\\angle B = ({exprs['B']}){symbol},\\text{{ and }} "
                f"m\\angle C = ({exprs['C']}){symbol}."
            )
            if ask == "x":
                prompt += f"\\text{{ Find }} x."
                answer = str(x)
            else:
                target = random.choice(labels)
                prompt += f"\\text{{ Find }} m\\angle {target}."
                answer = f"{angle_map[target]}{symbol}"

        self._last = {
            "figure": triangle_figure(labels, angles, missing=None),
            "labels": labels,
            "angle": c_ang,
            "figure_type": "triangle",
        }
        return prompt, f"finding angles hard {mode}", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_question_metadata(self, settings: dict, **_: Any) -> dict[str, Any]:
        last = self._last
        if not last:
            return {}
        return _figure_metadata(
            settings,
            figure_type=last.get("figure_type", "composite"),
            labels=last["labels"],
            dimensions={"angle_deg": float(last["angle"])},
            diagram=last.get("figure") if _diagram_enabled(settings) else None,
        )


class ExteriorAngleFramework(GeometryFramework):
    """Exterior Angle Theorem."""

    def __init__(self) -> None:
        super().__init__(figure_type="triangle")
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        symbol = _angle_symbol(settings)
        a = _random_angle(settings)
        b = _random_angle(settings)
        while a + b >= 170:
            b = _random_angle(settings)
        exterior = a + b
        labels = list(_TRIANGLE_LABELS)
        prompt = (
            f"\\text{{In }} \\triangle {''.join(labels)},\\ "
            f"m\\angle {labels[0]} = {a}{symbol} \\text{{ and }} "
            f"m\\angle {labels[1]} = {b}{symbol}.\\ "
            f"\\text{{Find the exterior angle at }} {labels[2]}."
        )
        answer = f"{exterior}{symbol}"
        fig = triangle_figure(labels, (a, b, 180 - a - b), missing=labels[2])
        self._last = {"figure": fig, "labels": labels, "angles": (a, b, exterior)}
        return prompt, "exterior angle theorem", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_question_metadata(self, settings: dict, **_: Any) -> dict[str, Any]:
        last = self._last
        if not last:
            return {}
        return _figure_metadata(
            settings,
            figure_type="triangle",
            labels=last["labels"],
            dimensions={"exterior": float(last["angles"][2])},
            diagram=last.get("figure") if _diagram_enabled(settings) else None,
        )


class ClassifyingTrianglesFramework(GeometryFramework):
    """Classify triangles by sides or angles."""

    def __init__(self) -> None:
        super().__init__(figure_type="triangle")
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        mode = random.choice(["sides", "angles"])
        labels = list(_TRIANGLE_LABELS)
        if mode == "sides":
            kind = random.choice(["equilateral", "isosceles", "scalene"])
            if kind == "equilateral":
                s = _random_side(settings)
                sides = (s, s, s)
                angles = (60, 60, 60)
            elif kind == "isosceles":
                a = _random_side(settings)
                b = _random_side(settings)
                while b == a:
                    b = _random_side(settings)
                sides = (a, a, b)
                angles = (70, 70, 40)
            else:
                a, b, c = _random_side(settings), _random_side(settings), _random_side(settings)
                while len({a, b, c}) < 3 or a + b <= c:
                    c = _random_side(settings)
                sides = (a, b, c)
                angles = (50, 60, 70)
            prompt = (
                f"\\text{{Classify }} \\triangle {''.join(labels)} "
                f"\\text{{ by its sides.}}"
            )
            answer = kind
            fig = triangle_figure(
                labels,
                angles,
                side_labels={
                    f"{labels[1]}{labels[2]}": str(sides[0]),
                    f"{labels[0]}{labels[2]}": str(sides[1]),
                    f"{labels[0]}{labels[1]}": str(sides[2]),
                },
            )
        else:
            kind = random.choice(["acute", "right", "obtuse"])
            if kind == "right":
                angles = (90, 35, 55)
            elif kind == "obtuse":
                angles = (120, 30, 30)
            else:
                angles = (50, 60, 70)
            prompt = (
                f"\\text{{Classify }} \\triangle {''.join(labels)} "
                f"\\text{{ by its angles.}}"
            )
            answer = kind
            fig = triangle_figure(labels, angles)
        self._last = {"figure": fig, "labels": labels}
        return prompt, f"classify triangle {answer}", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_question_metadata(self, settings: dict, **_: Any) -> dict[str, Any]:
        last = self._last
        if not last:
            return {}
        return _figure_metadata(
            settings,
            figure_type="triangle",
            labels=last["labels"],
            dimensions={},
            diagram=last.get("figure") if _diagram_enabled(settings) else None,
        )


class IsoscelesTriangleFramework(GeometryFramework):
    """Base angles of isosceles / equilateral triangles."""

    def __init__(self) -> None:
        super().__init__(figure_type="triangle")
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        symbol = _angle_symbol(settings)
        labels = list(_TRIANGLE_LABELS)
        vertex_angle = random.randint(20, 100)
        base = (180 - vertex_angle) // 2
        prompt = (
            f"\\triangle {''.join(labels)} \\text{{ is isosceles with }} "
            f"{labels[0]}{labels[1]} = {labels[0]}{labels[2]}.\\ "
            f"m\\angle {labels[0]} = {vertex_angle}{symbol}.\\ "
            f"\\text{{Find }} m\\angle {labels[1]}."
        )
        answer = f"{base}{symbol}"
        fig = triangle_figure(labels, (vertex_angle, base, base), missing=labels[1])
        self._last = {"figure": fig, "labels": labels}
        return prompt, "isosceles triangle", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_question_metadata(self, settings: dict, **_: Any) -> dict[str, Any]:
        last = self._last
        if not last:
            return {}
        return _figure_metadata(
            settings,
            figure_type="triangle",
            labels=last["labels"],
            dimensions={},
            diagram=last.get("figure") if _diagram_enabled(settings) else None,
        )


class ParallelTransversalFramework(GeometryFramework):
    """Parallel lines cut by a transversal — find an angle."""

    def __init__(self) -> None:
        super().__init__(figure_type="composite")
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        symbol = _angle_symbol(settings)
        angle = random.randint(35, 145)
        relation = random.choice(
            ["corresponding", "alternate interior", "same-side interior"]
        )
        if relation == "same-side interior":
            answer_val = 180 - angle
        else:
            answer_val = angle
        prompt = (
            f"\\text{{Two parallel lines are cut by a transversal. "
            f"One angle measures }} {angle}{symbol}.\\ "
            f"\\text{{Find the {relation} angle.}}"
        )
        answer = f"{answer_val}{symbol}"
        self._last = {
            "figure": parallel_lines_transversal_figure(float(angle), show_measure=True),
            "angle": angle,
        }
        return prompt, f"parallel transversal {relation}", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_question_metadata(self, settings: dict, **_: Any) -> dict[str, Any]:
        last = self._last
        if not last:
            return {}
        return _figure_metadata(
            settings,
            figure_type="composite",
            labels=["P"],
            dimensions={"angle_deg": float(last["angle"])},
            diagram=last.get("figure") if _diagram_enabled(settings) else None,
        )


class TriangleInequalityFramework(GeometryFramework):
    """Determine whether three lengths form a triangle."""

    def __init__(self) -> None:
        super().__init__(figure_type="triangle")
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        a = _random_side(settings)
        b = _random_side(settings)
        if random.choice([True, False]):
            c = random.randint(1, a + b - 1)
            forms = True
        else:
            c = a + b + random.randint(1, 5)
            forms = False
        prompt = (
            f"\\text{{Can sides of lengths }} {a},\\ {b},\\ \\text{{ and }} {c} "
            f"\\text{{ form a triangle?}}"
        )
        answer = "yes" if forms else "no"
        labels = list(_TRIANGLE_LABELS)
        fig = triangle_figure(labels, (50, 60, 70)) if forms else None
        self._last = {"figure": fig, "labels": labels, "forms": forms}
        return prompt, "triangle inequality", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_question_metadata(self, settings: dict, **_: Any) -> dict[str, Any]:
        last = self._last
        if not last or not last.get("forms"):
            return {}
        return _figure_metadata(
            settings,
            figure_type="triangle",
            labels=last["labels"],
            dimensions={},
            diagram=last.get("figure") if _diagram_enabled(settings) else None,
        )


class SpecialRightTriangleFramework(GeometryFramework):
    """45-45-90 and 30-60-90 triangles."""

    def __init__(self) -> None:
        super().__init__(figure_type="triangle")
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        unit = _measurement_unit(settings)
        labels = list(_TRIANGLE_LABELS)
        kind = random.choice(["45-45-90", "30-60-90"])
        if kind == "45-45-90":
            leg = _random_side(settings)
            prompt = (
                f"\\text{{In a }} 45^\\circ\\text{{-}}45^\\circ\\text{{-}}90^\\circ "
                f"\\text{{ triangle, a leg is }} {leg}\\text{{ {unit}}}.\\ "
                f"\\text{{Find the hypotenuse.}}"
            )
            answer = f"{leg}\\sqrt{{2}}\\text{{ {unit}}}"
            fig = right_triangle_figure(
                float(leg),
                float(leg),
                labels=(labels[0], labels[1], labels[2]),
                side_labels={
                    f"{labels[1]}{labels[2]}": f"{leg} {unit}",
                    f"{labels[0]}{labels[2]}": f"{leg} {unit}",
                    f"{labels[0]}{labels[1]}": "?",
                },
            )
        else:
            short = _random_side(settings)
            prompt = (
                f"\\text{{In a }} 30^\\circ\\text{{-}}60^\\circ\\text{{-}}90^\\circ "
                f"\\text{{ triangle, the shorter leg is }} {short}\\text{{ {unit}}}.\\ "
                f"\\text{{Find the hypotenuse.}}"
            )
            answer = f"{2 * short}\\text{{ {unit}}}"
            fig = right_triangle_figure(
                float(short),
                float(short) * 1.7,
                labels=(labels[0], labels[1], labels[2]),
                side_labels={
                    f"{labels[1]}{labels[2]}": f"{short} {unit}",
                    f"{labels[0]}{labels[1]}": "?",
                },
                angle_labels={labels[0]: "30°", labels[1]: "60°"},
            )
        self._last = {"figure": fig, "labels": labels}
        return prompt, f"special right {kind}", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_question_metadata(self, settings: dict, **_: Any) -> dict[str, Any]:
        last = self._last
        if not last:
            return {}
        return _figure_metadata(
            settings,
            figure_type="triangle",
            labels=last["labels"],
            dimensions={},
            diagram=last.get("figure") if _diagram_enabled(settings) else None,
        )


class PolygonInteriorAngleFramework(GeometryFramework):
    """Sum of interior angles or one angle of a regular polygon."""

    def __init__(self) -> None:
        super().__init__(figure_type="composite")
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        symbol = _angle_symbol(settings)
        n = random.choice([3, 4, 5, 6, 8, 10])
        total = (n - 2) * 180
        if random.choice([True, False]):
            prompt = (
                f"\\text{{Find the sum of the interior angles of a regular }} "
                f"{n}\\text{{-gon.}}"
            )
            answer = f"{total}{symbol}"
        else:
            each = total // n
            prompt = (
                f"\\text{{Find the measure of one interior angle of a regular }} "
                f"{n}\\text{{-gon.}}"
            )
            answer = f"{each}{symbol}"
        self._last = {"n": n}
        return prompt, f"polygon interior n={n}", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_question_metadata(self, settings: dict, **_: Any) -> dict[str, Any]:
        return {}


class ParallelogramAreaFramework(GeometryFramework):
    """Area of a parallelogram."""

    def __init__(self) -> None:
        super().__init__(figure_type="parallelogram")
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        unit = _measurement_unit(settings)
        base = _random_side(settings)
        height = _random_side(settings)
        area = base * height
        prompt = "\\text{{Find the area of the parallelogram.}}"
        answer = f"{area}\\text{{ {unit}}}^2"
        self._last = {
            "figure": parallelogram_figure(float(base), float(height), unit=unit),
            "base": base,
            "height": height,
        }
        return prompt, f"parallelogram area {base}x{height}", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_question_metadata(self, settings: dict, **_: Any) -> dict[str, Any]:
        last = self._last
        if not last:
            return {}
        return _figure_metadata(
            settings,
            figure_type="parallelogram",
            labels=["A", "B", "C", "D"],
            dimensions={"base": float(last["base"]), "height": float(last["height"])},
            diagram=last.get("figure") if _diagram_enabled(settings) else None,
        )


class TrapezoidAreaFramework(GeometryFramework):
    """Area of a trapezoid."""

    def __init__(self) -> None:
        super().__init__(figure_type="trapezoid")
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        unit = _measurement_unit(settings)
        b1 = _random_side(settings)
        b2 = _random_side(settings)
        h = _random_side(settings)
        area = (b1 + b2) * h / 2
        prompt = "\\text{{Find the area of the trapezoid.}}"
        answer = f"{area:g}\\text{{ {unit}}}^2"
        self._last = {
            "figure": trapezoid_figure(float(b1), float(b2), float(h), unit=unit),
            "b1": b1,
            "b2": b2,
            "h": h,
        }
        return prompt, f"trapezoid area", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_question_metadata(self, settings: dict, **_: Any) -> dict[str, Any]:
        last = self._last
        if not last:
            return {}
        return _figure_metadata(
            settings,
            figure_type="trapezoid",
            labels=["A", "B", "C", "D"],
            dimensions={
                "base1": float(last["b1"]),
                "base2": float(last["b2"]),
                "height": float(last["h"]),
            },
            diagram=last.get("figure") if _diagram_enabled(settings) else None,
        )


class KiteAreaFramework(GeometryFramework):
    """Area of a kite from diagonals."""

    def __init__(self) -> None:
        super().__init__(figure_type="composite")
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        unit = _measurement_unit(settings)
        d1 = _random_side(settings)
        d2 = _random_side(settings)
        area = d1 * d2 / 2
        prompt = "\\text{{Find the area of the kite.}}"
        answer = f"{area:g}\\text{{ {unit}}}^2"
        self._last = {
            "figure": kite_figure(float(d1), float(d2), unit=unit),
            "d1": d1,
            "d2": d2,
        }
        return prompt, "kite area", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_question_metadata(self, settings: dict, **_: Any) -> dict[str, Any]:
        last = self._last
        if not last:
            return {}
        return _figure_metadata(
            settings,
            figure_type="composite",
            labels=["A", "B", "C", "D"],
            dimensions={"d1": float(last["d1"]), "d2": float(last["d2"])},
            diagram=last.get("figure") if _diagram_enabled(settings) else None,
        )


class CentralArcAngleFramework(GeometryFramework):
    """Central angle equals intercepted arc measure."""

    def __init__(self) -> None:
        super().__init__(figure_type="circle")
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        symbol = _angle_symbol(settings)
        measure = random.randint(40, 160)
        prompt = (
            f"\\text{{A central angle measures }} {measure}{symbol}.\\ "
            f"\\text{{Find the measure of its intercepted arc.}}"
        )
        answer = f"{measure}{symbol}"
        from ..diagrams import circle_figure

        self._last = {"figure": circle_figure(5, show_radius_length=False), "m": measure}
        return prompt, "central arc angle", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_question_metadata(self, settings: dict, **_: Any) -> dict[str, Any]:
        last = self._last
        if not last:
            return {}
        return _figure_metadata(
            settings,
            figure_type="circle",
            labels=["O", "A"],
            dimensions={"arc": float(last["m"])},
            diagram=last.get("figure") if _diagram_enabled(settings) else None,
        )


class InscribedAngleFramework(GeometryFramework):
    """Inscribed angle is half the intercepted arc."""

    def __init__(self) -> None:
        super().__init__(figure_type="circle")
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        symbol = _angle_symbol(settings)
        arc = random.choice([40, 60, 80, 100, 120, 140])
        if random.choice([True, False]):
            prompt = (
                f"\\text{{An inscribed angle intercepts an arc of }} {arc}{symbol}.\\ "
                f"\\text{{Find the inscribed angle.}}"
            )
            answer = f"{arc // 2}{symbol}"
        else:
            angle = arc // 2
            prompt = (
                f"\\text{{An inscribed angle measures }} {angle}{symbol}.\\ "
                f"\\text{{Find the intercepted arc.}}"
            )
            answer = f"{arc}{symbol}"
        from ..diagrams import circle_figure

        self._last = {"figure": circle_figure(5, show_radius_length=False), "arc": arc}
        return prompt, "inscribed angle", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_question_metadata(self, settings: dict, **_: Any) -> dict[str, Any]:
        last = self._last
        if not last:
            return {}
        return _figure_metadata(
            settings,
            figure_type="circle",
            labels=["O", "A"],
            dimensions={"arc": float(last["arc"])},
            diagram=last.get("figure") if _diagram_enabled(settings) else None,
        )


class ArcLengthSectorFramework(GeometryFramework):
    """Arc length or sector area."""

    def __init__(self) -> None:
        super().__init__(figure_type="circle")
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        unit = _measurement_unit(settings)
        r = random.randint(3, 12)
        central = random.choice([45, 60, 90, 120, 180])
        from ..diagrams import circle_figure

        if random.choice([True, False]):
            prompt = (
                f"\\text{{A circle has radius }} {r}\\text{{ {unit}}} "
                f"\\text{{ and a central angle of }} {central}^\\circ.\\ "
                f"\\text{{Find the arc length.}}"
            )
            # (theta/360)*2*pi*r
            answer = f"\\frac{{{central}}}{{360}} \\cdot 2\\pi \\cdot {r}"
        else:
            prompt = (
                f"\\text{{A circle has radius }} {r}\\text{{ {unit}}} "
                f"\\text{{ and a central angle of }} {central}^\\circ.\\ "
                f"\\text{{Find the sector area.}}"
            )
            answer = f"\\frac{{{central}}}{{360}} \\cdot \\pi \\cdot {r}^{{2}}"
        self._last = {"figure": circle_figure(float(r), unit=unit), "r": r}
        return prompt, "arc length / sector", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_question_metadata(self, settings: dict, **_: Any) -> dict[str, Any]:
        last = self._last
        if not last:
            return {}
        return _figure_metadata(
            settings,
            figure_type="circle",
            labels=["O", "A"],
            dimensions={"radius": float(last["r"])},
            diagram=last.get("figure") if _diagram_enabled(settings) else None,
        )


class SolidVolumeSurfaceFramework(GeometryFramework):
    """Volume or surface area of rectangular prism / cube / cylinder (text)."""

    def __init__(self) -> None:
        super().__init__(figure_type="prism")
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        unit = _measurement_unit(settings)
        shape = random.choice(["cube", "rectangular prism", "cylinder"])
        if shape == "cube":
            s = _random_side(settings)
            if random.choice([True, False]):
                prompt = (
                    f"\\text{{Find the volume of a cube with side }} "
                    f"{format_with_unit(s, unit)}."
                )
                answer = format_with_unit(s ** 3, unit, power=3)
            else:
                prompt = (
                    f"\\text{{Find the surface area of a cube with side }} "
                    f"{format_with_unit(s, unit)}."
                )
                answer = format_with_unit(6 * s * s, unit, power=2)
        elif shape == "rectangular prism":
            l, w, h = _random_side(settings), _random_side(settings), _random_side(settings)
            if random.choice([True, False]):
                prompt = (
                    f"\\text{{Find the volume of a }} {l}\\times{w}\\times{h}"
                    f"{unit_latex(unit)} \\text{{ rectangular prism.}}"
                )
                answer = format_with_unit(l * w * h, unit, power=3)
            else:
                sa = 2 * (l * w + l * h + w * h)
                prompt = (
                    f"\\text{{Find the surface area of a }} {l}\\times{w}\\times{h}"
                    f"{unit_latex(unit)} \\text{{ rectangular prism.}}"
                )
                answer = format_with_unit(sa, unit, power=2)
        else:
            r = random.randint(2, 10)
            h = _random_side(settings)
            prompt = (
                f"\\text{{Find the volume of a cylinder with radius }} "
                f"{format_with_unit(r, unit)} "
                f"\\text{{ and height }} {format_with_unit(h, unit)}."
            )
            answer = f"{r * r}\\pi \\cdot {h}{unit_latex(unit)}^{{3}}"
        return prompt, f"solid {shape}", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}



# ---------------------------------------------------------------------------
# Geometric transformations on the coordinate plane (shapes, not functions)
# ---------------------------------------------------------------------------

_Point = tuple[int, int]


def _format_vertices_latex(labels: list[str], points: list[_Point]) -> str:
    return ",\\ ".join(f"{lab}({x}, {y})" for lab, (x, y) in zip(labels, points))


def _format_image_vertices_latex(labels: list[str], points: list[_Point]) -> str:
    return ",\\ ".join(f"{lab}'({x}, {y})" for lab, (x, y) in zip(labels, points))


def _translate_points(points: list[_Point], dx: int, dy: int) -> list[_Point]:
    return [(x + dx, y + dy) for x, y in points]


def _reflect_over_x(points: list[_Point]) -> list[_Point]:
    return [(x, -y) for x, y in points]


def _reflect_over_y(points: list[_Point]) -> list[_Point]:
    return [(-x, y) for x, y in points]


def _reflect_over_yx(points: list[_Point]) -> list[_Point]:
    return [(y, x) for x, y in points]


def _rotate_90_ccw(points: list[_Point]) -> list[_Point]:
    return [(-y, x) for x, y in points]


def _rotate_90_cw(points: list[_Point]) -> list[_Point]:
    return [(y, -x) for x, y in points]


def _rotate_180(points: list[_Point]) -> list[_Point]:
    return [(-x, -y) for x, y in points]


def _dilate_from_origin(points: list[_Point], k: int) -> list[_Point]:
    return [(k * x, k * y) for x, y in points]


def _points_in_bounds(points: list[_Point], lo: int, hi: int) -> bool:
    return all(lo <= x <= hi and lo <= y <= hi for x, y in points)


def _translation_action(dx: int, dy: int) -> str:
    parts: list[str] = []
    if dx:
        units = "unit" if abs(dx) == 1 else "units"
        direction = "right" if dx > 0 else "left"
        parts.append(f"{abs(dx)} {units} {direction}")
    if dy:
        units = "unit" if abs(dy) == 1 else "units"
        direction = "up" if dy > 0 else "down"
        parts.append(f"{abs(dy)} {units} {direction}")
    joined = " and ".join(parts) if parts else "0 units"
    return f"\\text{{translated {joined}}}"


def _random_transform_triangle(lo: int, hi: int) -> list[_Point]:
    for _ in range(40):
        pts = [
            (random.randint(lo, hi), random.randint(lo, hi)),
            (random.randint(lo, hi), random.randint(lo, hi)),
            (random.randint(lo, hi), random.randint(lo, hi)),
        ]
        if len(set(pts)) < 3:
            continue
        (x1, y1), (x2, y2), (x3, y3) = pts
        if (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1) == 0:
            continue
        return pts
    return [(1, 1), (3, 1), (2, 3)]


def _random_transform_rectangle(lo: int, hi: int, *, square: bool = False) -> list[_Point]:
    span = max(2, hi - lo)
    side_cap = min(3, span)
    w = random.randint(1, side_cap)
    h = w if square else random.randint(1, side_cap)
    if not square and w == h and side_cap >= 2:
        h = 1 if w != 1 else 2
    x = random.randint(lo, hi - w)
    y = random.randint(lo, hi - h)
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]


def _random_transform_parallelogram(lo: int, hi: int) -> list[_Point]:
    for _ in range(40):
        ax = random.randint(lo, hi - 3)
        ay = random.randint(lo, hi - 3)
        w = random.randint(2, 3)
        dx = random.randint(1, 2)
        dy = random.randint(2, 3)
        pts = [(ax, ay), (ax + w, ay), (ax + w + dx, ay + dy), (ax + dx, ay + dy)]
        if _points_in_bounds(pts, lo, hi) and len(set(pts)) == 4:
            return pts
    return [(-2, -1), (1, -1), (2, 2), (-1, 2)]


def _pick_plane_figure(
    lo: int, hi: int, *, tier: str
) -> tuple[str, list[str], list[_Point]]:
    if tier == "easy":
        choices = ("triangle", "triangle", "square", "rectangle")
    elif tier == "hard":
        choices = ("triangle", "parallelogram", "rectangle", "quadrilateral")
    else:
        choices = ("triangle", "square", "rectangle", "parallelogram")
    kind = random.choice(choices)
    if kind == "triangle":
        return "triangle", ["A", "B", "C"], _random_transform_triangle(lo, hi)
    if kind == "square":
        return "square", ["A", "B", "C", "D"], _random_transform_rectangle(lo, hi, square=True)
    if kind == "parallelogram":
        return "parallelogram", ["A", "B", "C", "D"], _random_transform_parallelogram(lo, hi)
    if kind == "quadrilateral":
        return "quadrilateral", ["A", "B", "C", "D"], _random_transform_parallelogram(lo, hi)
    return "rectangle", ["A", "B", "C", "D"], _random_transform_rectangle(lo, hi)


class GeometricTransformationsFramework(QuestionFramework):
    """Graph translations, reflections, rotations, and dilations of plane figures.

    Not function transformations — triangles / squares / quadrilaterals on a
    coordinate plane. Easy: translations. Medium: reflections / rotations.
    Hard: dilations and compositions.
    """

    instruction_latex = r"\text{Graph the transformation.}"
    instruction_text = "Graph the transformation."

    def __init__(self) -> None:
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        from ..diagrams.grade6_figures import coordinate_transform_svg

        tier = _difficulty_tier(settings)
        lo, hi = _bounds(settings, "coord_min", "coord_max", -6, 6)
        pre_lo = max(lo, -4)
        pre_hi = min(hi, 4)
        if pre_hi - pre_lo < 3:
            pre_lo, pre_hi = -3, 3

        shape_name, labels, preimage = _pick_plane_figure(pre_lo, pre_hi, tier=tier)
        image: list[_Point] = list(preimage)
        kind = "translation"
        action = r"\text{translated}"

        if tier == "easy":
            kind = "translation"
            for _attempt in range(40):
                dx = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
                dy = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
                cand = _translate_points(preimage, dx, dy)
                if _points_in_bounds(cand, lo, hi):
                    image = cand
                    action = _translation_action(dx, dy)
                    break
            else:
                image = _translate_points(preimage, 2, 3)
                action = _translation_action(2, 3)

        elif tier == "medium":
            options: list[tuple[str, str, Any]] = [
                ("reflection_x", r"\text{reflected across the }x\text{-axis}", _reflect_over_x),
                ("reflection_y", r"\text{reflected across the }y\text{-axis}", _reflect_over_y),
                ("reflection_yx", r"\text{reflected across the line }y=x", _reflect_over_yx),
                (
                    "rotation_90",
                    r"\text{rotated }90^\circ\text{ counterclockwise about the origin}",
                    _rotate_90_ccw,
                ),
                (
                    "rotation_90_cw",
                    r"\text{rotated }90^\circ\text{ clockwise about the origin}",
                    _rotate_90_cw,
                ),
                (
                    "rotation_180",
                    r"\text{rotated }180^\circ\text{ about the origin}",
                    _rotate_180,
                ),
            ]
            # Dilations / compositions are hard (grade progression).
            random.shuffle(options)
            for kind, action, fn in options:
                cand = fn(preimage)
                if _points_in_bounds(cand, lo, hi) and cand != preimage:
                    image = cand
                    break
            else:
                kind = "translation"
                image = _translate_points(preimage, 2, -1)
                action = _translation_action(2, -1)

        else:  # hard — dilations and compositions
            if random.random() < 0.45:
                kind = "dilation"
                for _attempt in range(25):
                    k = random.choice([2, 3])
                    shape_name, labels, compact = _pick_plane_figure(-2, 2, tier="hard")
                    if any(p == (0, 0) for p in compact):
                        continue
                    cand = _dilate_from_origin(compact, k)
                    if _points_in_bounds(cand, lo, hi) and cand != compact:
                        preimage = compact
                        image = cand
                        action = (
                            f"\\text{{dilated by a factor of }} {k}"
                            r"\text{ centered at the origin}"
                        )
                        break
                else:
                    preimage = [(1, 1), (2, 1), (1, 2)]
                    labels = ["A", "B", "C"]
                    shape_name = "triangle"
                    image = _dilate_from_origin(preimage, 2)
                    action = r"\text{dilated by a factor of }2\text{ centered at the origin}"
            else:
                kind = "composition"
                dx = random.choice([-3, -2, -1, 1, 2, 3])
                dy = random.choice([-3, -2, -1, 1, 2, 3])
                mid = _translate_points(preimage, dx, dy)
                t_part = _translation_action(dx, dy)
                second = random.choice(["reflect_y", "reflect_x", "rotate_180", "dilate"])
                if second == "reflect_y":
                    image = _reflect_over_y(mid)
                    action = f"{t_part}\\text{{, then reflected across the }}y\\text{{-axis}}"
                elif second == "reflect_x":
                    image = _reflect_over_x(mid)
                    action = f"{t_part}\\text{{, then reflected across the }}x\\text{{-axis}}"
                elif second == "dilate":
                    shape_name, labels, compact = _pick_plane_figure(-2, 2, tier="hard")
                    mid = _dilate_from_origin(compact, 2)
                    image = _translate_points(mid, dx, dy)
                    preimage = compact
                    action = (
                        r"\text{dilated by a factor of }2\text{ centered at the origin, then }"
                        + _translation_action(dx, dy)
                    )
                else:
                    image = _rotate_180(mid)
                    action = (
                        f"{t_part}\\text{{, then rotated }}"
                        r"180^\circ\text{ about the origin}"
                    )

        verts = _format_vertices_latex(labels, preimage)
        image_verts = _format_image_vertices_latex(labels, image)
        image_labels = [f"{lab}'" for lab in labels]
        use_stimulus = bool(settings.get("show_preimage_graph", True)) and random.random() < 0.6

        if use_stimulus:
            if shape_name == "triangle":
                prompt = (
                    rf"\triangle {''.join(labels)}\text{{ shown on the coordinate plane is }} "
                    f"{action}\\text{{. Graph the image.}}"
                )
            else:
                prompt = (
                    f"\\text{{The {shape_name} shown on the coordinate plane is }} {action}"
                    f"\\text{{. Graph the image.}}"
                )
            prompt_mode = "stimulus"
            prompt_svg = coordinate_transform_svg(preimage, labels=labels)
        else:
            if shape_name == "triangle":
                prompt = (
                    rf"\triangle {''.join(labels)}\text{{ has vertices }} {verts}"
                    f"\\text{{. The figure is }} {action}"
                    f"\\text{{. Graph the image.}}"
                )
            else:
                prompt = (
                    f"\\text{{A {shape_name} has vertices }} {verts}"
                    f"\\text{{. The figure is }} {action}"
                    f"\\text{{. Graph the image.}}"
                )
            prompt_mode = "blank"
            prompt_svg = coordinate_transform_svg(preimage, blank=True)

        answer_svg = coordinate_transform_svg(
            preimage,
            image=image,
            labels=labels,
            image_labels=image_labels,
        )
        self._last = {
            "preimage": preimage,
            "image": image,
            "labels": labels,
            "shape": shape_name,
            "kind": kind,
            "prompt_mode": prompt_mode,
            "diagram_svg": prompt_svg,
            "answer_diagram_svg": answer_svg,
        }
        return prompt, f"{kind} of {shape_name}", image_verts

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_question_metadata(
        self,
        settings: dict,
        *,
        prompt_latex: str,
        prompt_text: str,
        answer: str | None,
    ) -> dict[str, Any]:
        from .graphing import (
            CoordinatePlaneSpec,
            blank_graph_spec,
            coordinate_plane_spec_to_graph_spec,
            include_graph_metadata,
            origin_centered_bounds,
        )
        from ..core.metadata import question_metadata

        last = self._last
        if not last:
            return {}
        preimage: list[_Point] = last["preimage"]
        image: list[_Point] = last["image"]
        features = [(float(x), float(y)) for x, y in preimage + image]
        x_min, x_max, y_min, y_max = origin_centered_bounds(features, settings=settings)
        answer_spec = CoordinatePlaneSpec(
            points=[(float(x), float(y)) for x, y in image],
            show_grid=True,
            show_points=True,
            x_min=x_min,
            x_max=x_max,
            y_min=y_min,
            y_max=y_max,
        )
        pre_spec = CoordinatePlaneSpec(
            points=[(float(x), float(y)) for x, y in preimage],
            show_grid=True,
            show_points=True,
            x_min=x_min,
            x_max=x_max,
            y_min=y_min,
            y_max=y_max,
        )
        meta: dict[str, Any] = {
            "kind": "geometric_transformation",
            "diagram_svg": last.get("diagram_svg"),
            "answer_diagram_svg": last.get("answer_diagram_svg"),
            "coordinate_points": [
                {"x": x, "y": y, "label": lab}
                for lab, (x, y) in zip(last["labels"], preimage)
            ],
            "image_points": [
                {"x": x, "y": y, "label": f"{lab}'"}
                for lab, (x, y) in zip(last["labels"], image)
            ],
            "transform_kind": last.get("kind"),
        }
        if not include_graph_metadata(settings):
            return meta
        answer_gs = coordinate_plane_spec_to_graph_spec(answer_spec, settings)
        if last.get("prompt_mode") == "stimulus":
            pre_gs = coordinate_plane_spec_to_graph_spec(pre_spec, settings)
            meta.update(
                question_metadata(
                    graph_spec=pre_gs,
                    answer_graph_spec=answer_gs,
                    graph_role="stimulus",
                )
            )
        else:
            meta.update(
                question_metadata(
                    graph_spec=blank_graph_spec(answer_gs),
                    answer_graph_spec=answer_gs,
                    graph_role="blank",
                )
            )
        return meta


class RemainingGeometryFramework(GeometryFramework):
    """Diagram-backed generators for the remaining Geometry catalog topics.

    Each mode deliberately asks one well-scoped, automatically gradable
    question.  Construction modes assess the object produced by standard
    compass-and-straightedge steps rather than requiring an interactive
    construction surface.
    """

    def __init__(self, mode: str) -> None:
        super().__init__(figure_type="composite")
        self.mode = mode
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        unit = _measurement_unit(settings)
        symbol = _angle_symbol(settings)
        labels = ["A", "B", "C"]
        mode = self.mode

        if mode == "notation":
            a, b = random.sample(_ANGLE_LABELS, 2)
            self._last = {"figure": segment_figure(1, labels=(a, b), show_length=False), "labels": [a, b]}
            return f"\\text{{Name the segment shown.}}", f"segment {a}{b}", f"\\overline{{{a}{b}}}"
        if mode == "congruence":
            sides = random.choice([(5, 6, 7), (4, 4, 6), (3, 4, 5)])
            self._last = {"figure": triangle_figure(labels, (55, 60, 65)), "labels": labels}
            return (
                f"\\triangle ABC\\text{{ has side lengths }} {sides[0]}, {sides[1]}, {sides[2]}"
                f"\\text{{ and }}\\triangle DEF\\text{{ has corresponding side lengths }}"
                f"{sides[0]}, {sides[1]}, {sides[2]}.\\ \\text{{Are the triangles congruent?}}",
                "congruent triangles by SSS",
                "yes",
            )
        if mode == "congruence_proof":
            self._last = {"figure": triangle_figure(labels, (50, 60, 70)), "labels": labels}
            tier = str(settings.get("difficulty_tier") or "medium").lower()
            if tier == "hard":
                prompts = [
                    (
                        r"\text{In right }\triangle ABC\text{ and right }\triangle DEF,"
                        r"\ \overline{AC}\cong\overline{DF}\text{ (hypotenuses) and }"
                        r"\overline{BC}\cong\overline{EF}\text{ (a leg). "
                        r"Which congruence theorem applies?}",
                        "HL",
                    ),
                    (
                        r"\text{Two triangles have }\angle A\cong\angle D,\ "
                        r"\overline{AB}\cong\overline{DE},\text{ and }"
                        r"\angle B\cong\angle E.\text{ Which congruence theorem applies?}",
                        "ASA",
                    ),
                    (
                        r"\text{Two triangles have }\angle A\cong\angle D,\ "
                        r"\angle B\cong\angle E,\text{ and }"
                        r"\overline{BC}\cong\overline{EF}.\text{ Which congruence theorem applies?}",
                        "AAS",
                    ),
                ]
                prompt, answer = random.choice(prompts)
                return prompt, "congruence theorem", answer
            if tier == "medium":
                prompts = [
                    (
                        r"\text{Two triangles have two pairs of congruent sides and the "
                        r"included angles congruent. Which congruence theorem applies?}",
                        "SAS",
                    ),
                    (
                        r"\text{Two triangles have two pairs of congruent angles and the "
                        r"included sides congruent. Which congruence theorem applies?}",
                        "ASA",
                    ),
                ]
                prompt, answer = random.choice(prompts)
                return prompt, "congruence theorem", answer
            return (
                r"\text{Two triangles have three pairs of corresponding congruent sides. "
                r"Which congruence theorem proves the triangles congruent?}",
                "congruence theorem",
                "SSS",
            )
        if mode == "midsegment":
            base = _random_side(settings)
            self._last = {"figure": triangle_figure(labels, (50, 60, 70)), "labels": labels}
            return (
                f"\\text{{A midsegment of a triangle is parallel to a side of length }} {base}\\text{{ {unit}}}. "
                "\\text{Find the length of the midsegment.}",
                "triangle midsegment",
                f"{base / 2:g}\\text{{ {unit}}}",
            )
        if mode == "angle_bisector":
            angle = random.choice([40, 60, 80, 100, 120])
            self._last = {"figure": angle_figure("A", "B", "C", angle, show_measure=True), "labels": ["A", "B", "C"]}
            return (
                f"\\text{{Ray }} BD\\text{{ bisects }} \\angle ABC,\\text{{ which measures }} {angle}{symbol}. "
                "\\text{Find }m\\angle ABD.",
                "angle bisector",
                f"{angle // 2}{symbol}",
            )
        if mode == "medians":
            self._last = {"figure": triangle_figure(labels, (50, 60, 70)), "labels": labels}
            return (
                "\\text{In }\\triangle ABC,\\ D\\text{ is the midpoint of }\\overline{BC}. "
                "\\text{Name the median from }A.",
                "triangle median",
                "\\overline{AD}",
            )
        if mode == "centroid":
            x1, y1 = random.randint(-6, 4), random.randint(-4, 5)
            x2, y2 = x1 + random.choice([3, 6, 9]), y1 + random.choice([0, 3, 6])
            x3, y3 = x1 + random.choice([0, 3, 6]), y1 + random.choice([3, 6, 9])
            cx, cy = (x1 + x2 + x3) / 3, (y1 + y2 + y3) / 3
            self._last = {"figure": triangle_figure(labels, (50, 60, 70)), "labels": labels}
            return (
                f"\\text{{Find the centroid of a triangle with vertices }} ({x1},{y1}),\\ ({x2},{y2}),\\ ({x3},{y3}).",
                "triangle centroid",
                f"({cx:g}, {cy:g})",
            )
        if mode == "quadrilateral_classifying":
            kind = random.choice(["rectangle", "rhombus", "trapezoid", "parallelogram"])
            if kind == "trapezoid":
                fig = trapezoid_figure(8, 5, 4, show_dimensions=False)
            else:
                fig = parallelogram_figure(8, 4, show_dimensions=False, kind=kind)
            self._last = {"figure": fig, "labels": ["A", "B", "C", "D"]}
            return f"\\text{{Classify the {kind} shown by its most specific name.}}", f"classify {kind}", kind
        if mode == "regular_polygon_area":
            apothem, perimeter = random.choice([(4, 30), (5, 36), (6, 40)])
            self._last = {"figure": parallelogram_figure(6, 4, show_dimensions=False, kind="regular_polygon"), "labels": ["A", "B", "C", "D"]}
            return (
                f"\\text{{A regular polygon has apothem }} {apothem}\\text{{ {unit}}} "
                f"\\text{{and perimeter }} {perimeter}\\text{{ {unit}}}.\\ \\text{{Find its area.}}",
                "regular polygon area",
                f"{apothem * perimeter / 2:g}\\text{{ {unit}}}^2",
            )
        if mode == "similar_polygons":
            from ..diagrams import similar_figures_pair_figure

            scale = random.choice([2, 3, 4])
            side = _random_side(settings)
            other = _random_side(settings)
            while other == side:
                other = _random_side(settings)
            style = str(settings.get("prompt_style", "diagram")).strip().lower()
            use_diagram = style not in {
                "description_only",
                "description",
                "text",
                "text_only",
            } and _diagram_enabled(settings)
            if "include_figure" in settings:
                use_diagram = bool(settings["include_figure"]) and _diagram_enabled(settings)

            task = random.choice(["scale_factor", "missing_side", "scale_factor"])
            if task == "scale_factor":
                answer = str(scale)
                if use_diagram:
                    fig = similar_figures_pair_figure(
                        shape="rectangle",
                        small_labels=("A", "B", "C", "D"),
                        large_labels=("E", "F", "G", "H"),
                        small_side_labels={
                            "AB": f"{side} {unit}",
                            "AD": f"{other} {unit}",
                        },
                        large_side_labels={
                            "EF": f"{side * scale} {unit}",
                            "EH": f"{other * scale} {unit}",
                        },
                        aspect=(3.0, 2.0),
                        scale_factor=float(scale),
                        kind="similar_polygons",
                    )
                    prompt = (
                        r"ABCD \sim EFGH.\ "
                        r"\text{The polygons are similar. Find the scale factor "
                        r"from }ABCD\text{ to }EFGH."
                    )
                else:
                    fig = None
                    prompt = (
                        f"\\text{{Two polygons have corresponding side lengths }} {side}\\text{{ and }} {side * scale}"
                        f"\\text{{ and all corresponding angles are congruent. Find the scale factor from the first to the second.}}"
                    )
            else:
                answer = f"{other * scale}\\text{{ {unit}}}"
                if use_diagram:
                    fig = similar_figures_pair_figure(
                        shape="rectangle",
                        small_labels=("A", "B", "C", "D"),
                        large_labels=("E", "F", "G", "H"),
                        small_side_labels={
                            "AB": f"{side} {unit}",
                            "AD": f"{other} {unit}",
                        },
                        large_side_labels={
                            "EF": f"{side * scale} {unit}",
                            "EH": "?",
                        },
                        aspect=(3.0, 2.0),
                        scale_factor=float(scale),
                        kind="similar_polygons",
                    )
                    prompt = r"ABCD \sim EFGH.\ \text{Find the length of } EH."
                else:
                    fig = None
                    prompt = (
                        f"\\text{{Two similar polygons have corresponding sides }} {side}\\text{{ {unit} and }} "
                        f"{side * scale}\\text{{ {unit}. A second side of the smaller is }} {other}\\text{{ {unit}. "
                        f"Find the corresponding larger side.}}"
                    )
            self._last = {
                "figure": fig,
                "labels": ["A", "B", "C", "D", "E", "F", "G", "H"],
            }
            return (
                prompt,
                "similar polygons",
                answer,
            )
        if mode == "proportional_parts":
            small, ratio = _random_side(settings), random.choice([2, 3, 4])
            self._last = {"figure": triangle_figure(labels, (50, 60, 70)), "labels": labels}
            return (
                f"\\text{{A segment parallel to one side of a triangle creates similar triangles. "
                f"If a corresponding small side is }} {small}\\text{{ {unit}}} "
                f"\\text{{and the scale factor is }} {ratio}\\text{{, find the larger side.}}",
                "proportional parts",
                f"{small * ratio}\\text{{ {unit}}}",
            )
        if mode == "circle_chords":
            r = _random_radius(settings)
            self._last = {"figure": circle_figure(r, unit=unit), "labels": ["O", "A"]}
            # Vary by difficulty: conceptual vs numeric chord-distance relations.
            tier = str(settings.get("difficulty_tier") or "medium").lower()
            if tier == "hard":
                # Perpendicular from center to chord: half-chord / radius → distance
                half = random.choice([3, 4, 5, 6, 8, 9])
                # Choose radius so distance is a Pythagorean integer when possible
                triples = [(3, 4, 5), (5, 12, 13), (6, 8, 10), (9, 12, 15)]
                a, b, c = random.choice(triples)
                # a = half chord, b = distance, c = radius (or swap a/b)
                if random.random() < 0.5:
                    half, dist, rad = a, b, c
                else:
                    half, dist, rad = b, a, c
                return (
                    rf"\text{{A chord of length }}{2 * half}\text{{ {unit} }} "
                    rf"\text{{is in a circle of radius }}{rad}\text{{ {unit}. }} "
                    rf"\text{{How far is the chord from the center?}}",
                    "chord distance from center",
                    f"{dist}\\text{{ {unit}}}",
                )
            if tier == "medium":
                return (
                    rf"\text{{A diameter of a circle is }}{2 * r}\text{{ {unit}. }} "
                    rf"\text{{A chord of length }}{r}\text{{ {unit} }} "
                    rf"\text{{is perpendicular to a radius at its midpoint. "
                    rf"Is the midpoint of the chord the center of the circle?}}",
                    "chord midpoint vs center",
                    r"\text{No}",
                )
            return (
                r"\text{Two congruent chords of a circle intercept what kind of arcs?}",
                "congruent chords arcs",
                "congruent arcs",
            )
        if mode == "tangents":
            r = _random_radius(settings)
            self._last = {"figure": circle_figure(r, unit=unit), "labels": ["O", "A"]}
            tier = str(settings.get("difficulty_tier") or "medium").lower()
            if tier == "hard":
                # Two tangents from external point are equal
                a = random.randint(5, 12)
                return (
                    rf"\text{{Two tangent segments from an external point to a circle "
                    rf"measure }}{a}\text{{ {unit} }} "
                    rf"\text{{and }}x\text{{ {unit}. Find }}x.",
                    "two tangents theorem",
                    f"{a}\\text{{ {unit}}}",
                )
            if tier == "medium":
                return (
                    rf"\text{{A tangent segment and a radius meet at the point of tangency. "
                    rf"If the radius is }}{r}\text{{ {unit} }} "
                    rf"\text{{and the tangent segment is }}{r + 3}\text{{ {unit}, }} "
                    rf"\text{{what is the measure of the angle between them?}}",
                    "radius-tangent angle",
                    r"90^\circ",
                )
            return (
                r"\text{What is the relationship between a radius and a tangent at the point of tangency?}",
                "radius tangent relationship",
                "perpendicular",
            )
        if mode == "secant_tangent":
            outside, whole = random.choice([(3, 12), (4, 16), (5, 20)])
            other_whole = outside * whole // random.choice([2, 3, 4])
            while outside * whole % other_whole:
                other_whole += 1
            other_outside = outside * whole / other_whole
            self._last = {"figure": circle_figure(5, unit=unit), "labels": ["O", "A"]}
            return (
                f"\\text{{Two secants from an external point have outside and whole lengths }} {outside}, {whole}"
                f"\\text{{ and }} x, {other_whole}.\\ \\text{{Find }}x.",
                "secant segment theorem",
                f"{other_outside:g}",
            )
        if mode == "circle_segments":
            a, b = random.choice([(3, 12), (4, 9), (5, 8)])
            self._last = {"figure": circle_figure(5, unit=unit), "labels": ["O", "A"]}
            return (
                f"\\text{{Two chords intersect inside a circle. One chord has segments }} {a}\\text{{ and }} {b}"
                "\\text{; the other has segments }6\\text{ and }x.\\ \\text{Find }x.",
                "intersecting chords",
                f"{a * b / 6:g}",
            )
        if mode == "circle_equation_using":
            h, k, r = random.randint(-5, 5), random.randint(-5, 5), _random_radius(settings)
            self._last = {"figure": circle_figure(r, unit=unit), "labels": ["O", "A"]}
            return (
                f"\\text{{For }} (x-({h}))^2+(y-({k}))^2={r*r},\\text{{ find the radius.}}",
                "circle equation radius",
                str(r),
            )
        if mode == "circle_equation_writing":
            h, k, r = random.randint(-5, 5), random.randint(-5, 5), _random_radius(settings)
            self._last = {"figure": circle_figure(r, unit=unit), "labels": ["O", "A"]}
            return (
                f"\\text{{Write the equation of the circle with center }} ({h},{k}) "
                f"\\text{{and radius }} {r}.",
                "circle standard equation",
                f"(x-({h}))^2+(y-({k}))^2={r*r}",
            )
        if mode == "transformations":
            raise RuntimeError(
                "geo_transformations uses GeometricTransformationsFramework; "
                "do not call RemainingGeometryFramework('transformations')."
            )

        construction_answers = {
            "construction_segments": ("segment congruent to the given segment", segment_figure(1, show_length=False)),
            "construction_perpendicular": ("a perpendicular line", angle_figure("A", "B", "C", 90, show_measure=False)),
            "construction_angles": ("an angle congruent to the given angle", angle_figure("A", "B", "C", 60, show_measure=False)),
            "construction_triangles": ("a triangle congruent to the given triangle", triangle_figure(labels, (50, 60, 70))),
            "construction_medians": ("a median", triangle_figure(labels, (50, 60, 70))),
            "construction_altitudes": ("an altitude", triangle_figure(labels, (50, 60, 70))),
            "construction_bisectors": ("an angle bisector", angle_figure("A", "B", "C", 60, show_measure=False)),
            "construction_circles": ("a circle with the given center and radius", circle_figure(5, unit=unit)),
        }
        if mode == "construction_circles":
            tier = str(settings.get("difficulty_tier") or "medium").lower()
            r = _random_radius(settings)
            self._last = {"figure": circle_figure(r, unit=unit), "labels": ["O", "A"]}
            if tier == "hard":
                return (
                    rf"\text{{Using compass and straightedge, you copy a segment of length }}"
                    rf"{r}\text{{ {unit} }} "
                    rf"\text{{as a radius from center }}O.\text{{ What figure is constructed?}}",
                    "construction circles",
                    r"\text{a circle with center }O\text{ and radius }" + f"{r}\\text{{ {unit}}}",
                )
            if tier == "medium":
                return (
                    r"\text{Which construction step creates all points at a fixed distance "
                    r"from a given center?}",
                    "construction circles",
                    r"\text{drawing a circle with the compass}",
                )
            return (
                r"\text{Identify the result of the standard construction shown: "
                r"a circle with the given center and radius.}",
                "construction circles",
                r"\text{a circle with the given center and radius}",
            )
        answer, figure = construction_answers[mode]
        self._last = {"figure": figure, "labels": labels}
        return (
            f"\\text{{Identify the result of the standard construction shown: }}\\ {answer}.",
            f"construction {mode}",
            answer,
        )

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_question_metadata(self, settings: dict, **_: Any) -> dict[str, Any]:
        last = self._last
        if not last:
            return {}
        fig = last.get("figure")
        if fig is None:
            return {}
        return _figure_metadata(
            settings,
            figure_type="composite",
            labels=last["labels"],
            dimensions={},
            diagram=fig if _diagram_enabled(settings) else None,
        )
