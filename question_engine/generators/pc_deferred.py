"""Named Precalc engines for former ``precalc_foundations`` stub leaves.

Shapes follow live old-path notes + OpenStax cites in
``scripts/output/skeleton_phase01_gallery/notes/pc_*.md``.
``pc_3d_vectors_operations`` is add/subtract (not cross product).
"""

from __future__ import annotations

import math
import random
from fractions import Fraction
from typing import Any, Callable

from question_engine.core.models import Question
from question_engine.generators.utils import _make_questions, frac_latex

Generator = Callable[[str, dict], list[Question]]

_RADIAN_LABELS: dict[int, str] = {
    0: "0",
    30: r"\frac{\pi}{6}",
    45: r"\frac{\pi}{4}",
    60: r"\frac{\pi}{3}",
    90: r"\frac{\pi}{2}",
    120: r"\frac{2\pi}{3}",
    135: r"\frac{3\pi}{4}",
    150: r"\frac{5\pi}{6}",
    180: r"\pi",
    210: r"\frac{7\pi}{6}",
    225: r"\frac{5\pi}{4}",
    240: r"\frac{4\pi}{3}",
    270: r"\frac{3\pi}{2}",
    300: r"\frac{5\pi}{3}",
    315: r"\frac{7\pi}{4}",
    330: r"\frac{11\pi}{6}",
    360: r"2\pi",
}


def _d(settings: dict) -> float:
    try:
        return float(settings.get("difficulty") or 0)
    except (TypeError, ValueError):
        return 0.0


def _span(settings: dict, *, lo: int = 2, mid: int = 4, hi: int = 6) -> int:
    d = _d(settings)
    if d < 8:
        return lo
    if d < 16:
        return mid
    return hi


def _meta(engine: str, **extra: Any) -> dict[str, Any]:
    return {
        "primitive_engine": engine,
        "generator": engine,
        "function_classes": ["algebraic"],
        **extra,
    }


def _with_meta(build_fn, engine: str, topic: str, settings: dict, **extra: Any):
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        prompt, topic_key, answer, meta = build_fn(keyed)
        last["meta"] = _meta(engine, **{**extra, **(meta or {})})
        return prompt, topic_key, answer

    def metadata_builder(_p: str, _t: str, _a: str | None) -> dict[str, Any]:
        return dict(last.get("meta") or {})

    return _make_questions(
        topic,
        count,
        keyed,
        build,
        metadata_builder=metadata_builder,
        settings=settings,
    )


# --- Functions -----------------------------------------------------------------


def pc_continuity(topic: str, settings: dict) -> list[Question]:
    """Continuity at a point from piecewise (OpenStax PC §1.3)."""

    def build_fn(keyed: bool):
        span = _span(settings, lo=3, mid=4, hi=6)
        c = random.randint(-span, span)
        # D=0: continuous match; higher D: sometimes jump discontinuity.
        continuous = _d(settings) < 8 or random.random() < 0.45
        right = c if continuous else c + random.choice([-2, -1, 1, 2])
        prompt = (
            rf"f(x)=\begin{{cases}}x+{c},&x<0\\{right},&x\ge0\end{{cases}}."
            rf"\quad\text{{Is }}f\text{{ continuous at }}0?"
        )
        answer = "Yes" if continuous else "No"
        return prompt, "continuity", answer if keyed else None, {
            "methods_used": ["continuity"],
            "continuous": continuous,
        }

    return _with_meta(build_fn, "pc_continuity", topic, settings)


def pc_extrema_intervals(topic: str, settings: dict) -> list[Question]:
    """Local extrema + increase intervals on quadratics (OpenStax PC §1.3)."""

    def build_fn(keyed: bool):
        d = _d(settings)
        a = random.choice([1, 2, 3] if d < 8 else [1, 2, 3, 4, -1, -2])
        h = 0 if d < 8 else random.randint(-2, 2)
        k = 0 if d < 12 else random.randint(-3, 3)
        if h == 0 and k == 0:
            fx = rf"{a}x^2" if a != 1 else r"x^2"
            if a == -1:
                fx = r"-x^2"
            elif a < 0:
                fx = rf"{a}x^2"
        elif h == 0:
            fx = rf"{a}x^2+{k}" if k >= 0 else rf"{a}x^2-{abs(k)}"
            if a == 1:
                fx = rf"x^2+{k}" if k >= 0 else rf"x^2-{abs(k)}"
            elif a == -1:
                fx = rf"-x^2+{k}" if k >= 0 else rf"-x^2-{abs(k)}"
        else:
            # a(x-h)^2 + k
            inner = rf"x-{h}" if h > 0 else rf"x+{abs(h)}"
            core = rf"({inner})^2"
            lead = "" if a == 1 else ("-" if a == -1 else str(a))
            fx = rf"{lead}{core}"
            if k > 0:
                fx = rf"{fx}+{k}"
            elif k < 0:
                fx = rf"{fx}-{abs(k)}"
        if a > 0:
            ext = rf"\text{{minimum }}{k}\text{{ at }}x={h}"
            inc = rf"\text{{increasing on }}({h},\infty)"
        else:
            ext = rf"\text{{maximum }}{k}\text{{ at }}x={h}"
            inc = rf"\text{{increasing on }}(-\infty,{h})"
        prompt = rf"\text{{Find the extrema and intervals of increase for }}f(x)={fx}."
        answer = rf"{ext};\ {inc}"
        return prompt, "extrema intervals", answer if keyed else None, {
            "methods_used": ["extrema"],
        }

    return _with_meta(build_fn, "pc_extrema_intervals", topic, settings)


def pc_power_functions(topic: str, settings: dict) -> list[Question]:
    """Evaluate power f(x)=x^n (OpenStax PC §3.3)."""

    def build_fn(keyed: bool):
        d = _d(settings)
        n = random.randint(2, 4 if d < 8 else (5 if d < 16 else 6))
        m_hi = 4 if d < 8 else (6 if d < 16 else 8)
        m = random.randint(2, m_hi)
        # Keep answers from exploding at high n.
        if n >= 5:
            m = random.randint(2, 4)
        prompt = rf"\text{{Evaluate }}f(x)=x^{{{n}}}\text{{ at }}x={m}."
        return prompt, "power function", str(m**n) if keyed else None, {
            "methods_used": ["evaluate"],
        }

    return _with_meta(build_fn, "pc_power_functions", topic, settings)


def pc_piecewise_functions(topic: str, settings: dict) -> list[Question]:
    """Evaluate piecewise at a point (OpenStax PC §1.5)."""

    def build_fn(keyed: bool):
        from question_engine.settings.params import piecewise_structure_from_continuous

        structure = piecewise_structure_from_continuous(settings)
        if structure is None:
            c = random.randint(-3, 4)
            bp = random.randint(-2, 2)
            x0 = random.randint(-3, 3)
            prompt = (
                rf"f(x)=\begin{{cases}}x+{c},&x<{bp}\\{c},&x\ge{bp}\end{{cases}}."
                rf"\quad\text{{Evaluate }}f({x0})."
            )
            value = str(x0 + c if x0 < bp else c)
            return prompt, "piecewise evaluate", value if keyed else None, {
                "methods_used": ["piecewise"],
            }

        span = int(structure["coef_span"])
        bp_span = int(structure["breakpoint_span"])
        c = random.randint(-span, span)
        bp = random.randint(-bp_span, bp_span)
        x0 = random.randint(-bp_span - 1, bp_span + 1)
        if structure["piece_count"] >= 3:
            c2 = random.randint(-span, span)
            left = bp - 1
            right = bp + 1
            use_linear_right = bool(structure["allow_quadratic_piece"])
            right_expr = rf"{c2}x" if use_linear_right else str(c2)
            if x0 < left:
                value = str(x0 + c)
            elif x0 < right:
                value = str(c)
            else:
                value = str(c2 * x0 if use_linear_right else c2)
            prompt = (
                rf"f(x)=\begin{{cases}}x+{c},&x<{left}\\{c},&"
                rf"{left}\le x<{right}\\{right_expr},&x\ge{right}\end{{cases}}."
                rf"\quad\text{{Evaluate }}f({x0})."
            )
        elif structure["allow_quadratic_piece"] and random.random() < 0.5:
            a = random.randint(1, max(1, span // 2))
            value = str(a * x0 * x0 + c if x0 < bp else c)
            prompt = (
                rf"f(x)=\begin{{cases}}{a}x^2+{c},&x<{bp}\\{c},&x\ge{bp}"
                rf"\end{{cases}}.\quad\text{{Evaluate }}f({x0})."
            )
        else:
            value = str(x0 + c if x0 < bp else c)
            prompt = (
                rf"f(x)=\begin{{cases}}x+{c},&x<{bp}\\{c},&x\ge{bp}"
                rf"\end{{cases}}.\quad\text{{Evaluate }}f({x0})."
            )
        return prompt, "piecewise evaluate", value if keyed else None, {
            "methods_used": ["piecewise"],
        }

    return _with_meta(build_fn, "pc_piecewise_functions", topic, settings)


# --- Polynomial / rational -----------------------------------------------------


def pc_complex_zeros(topic: str, settings: dict) -> list[Question]:
    """Complex zeros of x^2 + k^2 = 0 (OpenStax PC §3.6-ish FTA)."""

    def build_fn(keyed: bool):
        k = random.randint(2, _span(settings, lo=4, mid=6, hi=9))
        prompt = rf"\text{{Find the zeros of }}x^2+{k * k}=0."
        return prompt, "complex zeros", rf"x=\pm {k}i" if keyed else None, {
            "methods_used": ["complex_zeros"],
        }

    return _with_meta(build_fn, "pc_complex_zeros", topic, settings)


def pc_polynomial_inequalities(topic: str, settings: dict) -> list[Question]:
    """Sign-chart poly inequality (OpenStax PC §3.8 style)."""

    def build_fn(keyed: bool):
        n = random.randint(2, _span(settings, lo=5, mid=7, hi=9))
        m = random.randint(2, _span(settings, lo=5, mid=7, hi=9))
        # Keep roots distinct and ordered: -m < n
        op = ">" if _d(settings) < 12 or random.random() < 0.6 else ">="
        prompt = rf"(x-{n})(x+{m}){op}0."
        if op == ">":
            answer = rf"x<-{m}\text{{ or }}x>{n}"
        else:
            answer = rf"x\le -{m}\text{{ or }}x\ge {n}"
        return prompt, "polynomial inequality", answer if keyed else None, {
            "methods_used": ["sign_chart"],
        }

    return _with_meta(build_fn, "pc_polynomial_inequalities", topic, settings)


def pc_rational_inequalities(topic: str, settings: dict) -> list[Question]:
    """Critical points on rational inequality (OpenStax PC §3.7)."""

    def build_fn(keyed: bool):
        n = random.randint(2, _span(settings, lo=5, mid=7, hi=9))
        m = random.randint(2, _span(settings, lo=5, mid=7, hi=9))
        op = ">" if _d(settings) < 12 or random.random() < 0.6 else ">="
        prompt = rf"\frac{{x-{n}}}{{x+{m}}}{op}0."
        # Same critical-point solution shape as old path for > ;
        # for >= include endpoints except the vertical asymptote x=-m.
        if op == ">":
            answer = rf"x<-{m}\text{{ or }}x>{n}"
        else:
            answer = rf"x<-{m}\text{{ or }}x\ge {n}"
        return prompt, "rational inequality", answer if keyed else None, {
            "methods_used": ["sign_chart"],
        }

    return _with_meta(build_fn, "pc_rational_inequalities", topic, settings)


# --- Trig / parametric ---------------------------------------------------------


def pc_angles_and_angle_measure(topic: str, settings: dict) -> list[Question]:
    """Degree ↔ radian conversion / coterminal (OpenStax PC §5.1)."""

    def build_fn(keyed: bool):
        degs = [30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]
        if _d(settings) < 8:
            degs = [30, 45, 60, 90, 120, 135, 150, 180]
        deg = random.choice(degs)
        mode = "to_rad"
        if _d(settings) >= 8 and random.random() < 0.35:
            mode = "coterminal"
        if mode == "coterminal":
            turns = random.choice([-1, 1, 2])
            given = deg + 360 * turns
            prompt = rf"\text{{Find a coterminal angle between }}0^\circ\text{{ and }}360^\circ\text{{ for }}{given}^\circ."
            answer = rf"{deg}^\circ"
        else:
            prompt = rf"\text{{Convert }}{deg}^\circ\text{{ to radians.}}"
            answer = _RADIAN_LABELS[deg]
        return prompt, "angle measure", answer if keyed else None, {
            "methods_used": ["angle_measure"],
            "mode": mode,
        }

    return _with_meta(build_fn, "pc_angles_and_angle_measure", topic, settings)


def pc_parametric_equations(topic: str, settings: dict) -> list[Question]:
    """Point at t or eliminate parameter (OpenStax PC §8.6)."""

    def build_fn(keyed: bool):
        t = random.randint(1, _span(settings, lo=4, mid=6, hi=8))
        a = 1 if _d(settings) < 10 else random.randint(1, 3)
        b = 2 if _d(settings) < 10 else random.randint(1, 4)
        c = 1 if _d(settings) < 12 else random.randint(-3, 3)
        if _d(settings) >= 16 and random.random() < 0.4:
            # Eliminate parameter for x=t, y=at+b style
            prompt = rf"x={a}t,\ y={b}t+{c}.\quad\text{{Eliminate the parameter.}}"
            # y = (b/a)x + c
            if a == 1:
                answer = rf"y={b}x+{c}" if c >= 0 else rf"y={b}x-{abs(c)}"
            else:
                answer = rf"y=\frac{{{b}}}{{{a}}}x+{c}" if c >= 0 else rf"y=\frac{{{b}}}{{{a}}}x-{abs(c)}"
            mode = "eliminate"
        else:
            prompt = rf"x=t^2,\ y={b}t+{c}.\quad\text{{Find }}(x,y)\text{{ when }}t={t}."
            y = b * t + c
            answer = f"({t * t}, {y})"
            mode = "evaluate_t"
        return prompt, "parametric", answer if keyed else None, {
            "methods_used": ["parametric"],
            "mode": mode,
        }

    return _with_meta(build_fn, "pc_parametric_equations", topic, settings)


def pc_projectile_motion(topic: str, settings: dict) -> list[Question]:
    """Time of max height from h(t)=-16t^2+vt (OpenStax PC §8.6)."""

    def build_fn(keyed: bool):
        v = random.randint(3, _span(settings, lo=6, mid=8, hi=10))
        linear = 32 * v
        if _d(settings) >= 14 and random.random() < 0.4:
            # Ask for max height value
            prompt = rf"h(t)=-16t^2+{linear}t.\quad\text{{Find the maximum height.}}"
            tmax = v
            hmax = -16 * tmax * tmax + linear * tmax
            answer = str(hmax)
            mode = "max_height"
        else:
            prompt = rf"h(t)=-16t^2+{linear}t.\quad\text{{Find the time of maximum height.}}"
            answer = str(v)
            mode = "time_max"
        return prompt, "projectile", answer if keyed else None, {
            "methods_used": ["projectile"],
            "mode": mode,
        }

    return _with_meta(build_fn, "pc_projectile_motion", topic, settings)


# --- Vectors / 3D / systems ----------------------------------------------------


def pc_3d_points(topic: str, settings: dict) -> list[Question]:
    """Distance in 3D (OpenStax PC §9.8 / vectors chapter)."""

    def build_fn(keyed: bool):
        nice = [(3, 4, 12), (2, 3, 6), (1, 2, 2), (4, 4, 7), (1, 4, 8), (2, 6, 9)]
        if _d(settings) < 8 or random.random() < 0.55:
            x, y, z = random.choice(nice)
        else:
            span = _span(settings, lo=4, mid=6, hi=8)
            x, y, z = (random.randint(1, span) for _ in range(3))
        dist_sq = x * x + y * y + z * z
        root = int(math.isqrt(dist_sq))
        ans = str(root) if root * root == dist_sq else rf"\sqrt{{{dist_sq}}}"
        prompt = rf"\text{{Find the distance from }}(0,0,0)\text{{ to }}({x},{y},{z})."
        return prompt, "3d distance", ans if keyed else None, {
            "methods_used": ["distance_3d"],
        }

    return _with_meta(build_fn, "pc_3d_points", topic, settings)


def vector_3d_operations(topic: str, settings: dict) -> list[Question]:
    """3D vector add / subtract — OpenStax PC §9.8 (not cross product)."""

    def build_fn(keyed: bool):
        span = _span(settings, lo=3, mid=5, hi=7)
        a = [random.randint(-span, span) for _ in range(3)]
        b = [random.randint(-span, span) for _ in range(3)]
        op = "add" if (_d(settings) < 8 or random.random() < 0.55) else "subtract"
        if op == "add":
            prompt = (
                rf"\text{{Find }}\langle {a[0]},{a[1]},{a[2]}\rangle+"
                rf"\langle {b[0]},{b[1]},{b[2]}\rangle."
            )
            c = [a[i] + b[i] for i in range(3)]
        else:
            prompt = (
                rf"\text{{Find }}\langle {a[0]},{a[1]},{a[2]}\rangle-"
                rf"\langle {b[0]},{b[1]},{b[2]}\rangle."
            )
            c = [a[i] - b[i] for i in range(3)]
        answer = rf"\langle {c[0]},{c[1]},{c[2]}\rangle"
        return prompt, f"3d vector {op}", answer if keyed else None, {
            "methods_used": ["vector_ops"],
            "op": op,
        }

    return _with_meta(build_fn, "vector_3d_operations", topic, settings)


def cross_products(topic: str, settings: dict) -> list[Question]:
    """3D cross product components (OpenStax PC vectors)."""

    def build_fn(keyed: bool):
        span = _span(settings, lo=3, mid=4, hi=6)
        a = [random.randint(-span, span) for _ in range(3)]
        b = [random.randint(-span, span) for _ in range(3)]
        cx = a[1] * b[2] - a[2] * b[1]
        cy = a[2] * b[0] - a[0] * b[2]
        cz = a[0] * b[1] - a[1] * b[0]
        prompt = (
            rf"\text{{Find }}({a[0]},{a[1]},{a[2]})\times({b[0]},{b[1]},{b[2]})."
        )
        answer = rf"({cx},{cy},{cz})"
        return prompt, "cross product", answer if keyed else None, {
            "methods_used": ["cross_product"],
        }

    return _with_meta(build_fn, "cross_products", topic, settings)


def pc_multivariable_systems(topic: str, settings: dict) -> list[Question]:
    """3×3 linear system with simple integer solution (row ops)."""

    def build_fn(keyed: bool):
        z = random.randint(1, _span(settings, lo=3, mid=4, hi=5))
        x = random.randint(1, _span(settings, lo=3, mid=4, hi=5))
        y = x  # keeps x-y=0 equation from old path
        s = x + y + z
        if _d(settings) >= 14 and random.random() < 0.4:
            y = random.randint(1, 4)
            if y == x:
                y = x + 1
            s = x + y + z
            prompt = (
                rf"\text{{Solve }}x+y+z={s},\ x-y={x - y},\ z={z}."
            )
        else:
            prompt = rf"\text{{Solve }}x+y+z={s},\ x-y=0,\ z={z}."
        answer = rf"({x},{y},{z})"
        return prompt, "multivariable system", answer if keyed else None, {
            "methods_used": ["row_ops"],
        }

    return _with_meta(build_fn, "pc_multivariable_systems", topic, settings)


# --- Discrete / series / calc intro --------------------------------------------


def pc_mathematical_induction(topic: str, settings: dict) -> list[Question]:
    """Verify base case for sum formula (OpenStax discrete induction intro)."""

    def build_fn(keyed: bool):
        n0 = 1 if _d(settings) < 8 else random.choice([1, 2, 3])
        if n0 == 1:
            answer = "1=1"
        elif n0 == 2:
            answer = r"1+2=3"
        else:
            answer = r"1+2+3=6"
        prompt = (
            rf"\text{{Verify the base case }}n={n0}\text{{ for }}"
            rf"\sum_{{k=1}}^n k=\frac{{n(n+1)}}2."
        )
        return prompt, "induction base", answer if keyed else None, {
            "methods_used": ["induction"],
        }

    return _with_meta(build_fn, "pc_mathematical_induction", topic, settings)


def pc_power_series(topic: str, settings: dict) -> list[Question]:
    """Radius of convergence for geometric series ∑(cx)^n."""

    def build_fn(keyed: bool):
        c = random.choice([1, 2, 3] if _d(settings) < 10 else [1, 2, 3, 4, 5])
        prompt = (
            rf"\text{{Find the radius of convergence of }}"
            rf"\sum_{{n=0}}^{{\infty}}({c}x)^n."
        )
        answer = frac_latex(Fraction(1, c))
        return prompt, "power series radius", answer if keyed else None, {
            "methods_used": ["power_series"],
        }

    return _with_meta(build_fn, "pc_power_series", topic, settings)


def pc_motion_along_a_line(topic: str, settings: dict) -> list[Question]:
    """Velocity from s(t) (OpenStax / calc intro motion)."""

    def build_fn(keyed: bool):
        n = random.randint(2, _span(settings, lo=5, mid=7, hi=9))
        t0 = 2 if _d(settings) < 10 else random.randint(1, 4)
        if _d(settings) >= 14 and random.random() < 0.35:
            # a(t) from s(t)=t^2+nt → a=2
            prompt = rf"s(t)=t^2+{n}t.\quad\text{{Find }}a({t0})."
            answer = "2"
            mode = "acceleration"
        else:
            prompt = rf"s(t)=t^2+{n}t.\quad\text{{Find }}v({t0})."
            answer = str(2 * t0 + n)
            mode = "velocity"
        return prompt, "motion line", answer if keyed else None, {
            "methods_used": ["motion"],
            "mode": mode,
        }

    return _with_meta(build_fn, "pc_motion_along_a_line", topic, settings)


GENERATORS: dict[str, Generator] = {
    "pc_continuity": pc_continuity,
    "pc_extrema_intervals": pc_extrema_intervals,
    "pc_power_functions": pc_power_functions,
    "pc_piecewise_functions": pc_piecewise_functions,
    "pc_complex_zeros": pc_complex_zeros,
    "pc_polynomial_inequalities": pc_polynomial_inequalities,
    "pc_rational_inequalities": pc_rational_inequalities,
    "pc_angles_and_angle_measure": pc_angles_and_angle_measure,
    "pc_parametric_equations": pc_parametric_equations,
    "pc_projectile_motion": pc_projectile_motion,
    "pc_3d_points": pc_3d_points,
    "vector_3d_operations": vector_3d_operations,
    "cross_products": cross_products,
    "pc_multivariable_systems": pc_multivariable_systems,
    "pc_mathematical_induction": pc_mathematical_induction,
    "pc_power_series": pc_power_series,
    "pc_motion_along_a_line": pc_motion_along_a_line,
}
