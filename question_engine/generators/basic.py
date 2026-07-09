import math
import random
import uuid
from fractions import Fraction
from typing import Callable

from packages.polynomial_core import Polynomial, create_factorable_polynomial, square_root_latex

from ..settings.common_settings import standard_question_settings
from ..settings.factoring_settings import build_factorable_options
from ..settings.enrichment import merge_enrichment_metadata
from ..settings.params import allowed_rational_operations, polynomial_params_from_settings, radical_params_from_settings
from ..core.metadata import scaffold_metadata
from ..core.models import Question, SettingField
from .utils import _frac_latex, _make_questions, _random_fraction


def _discrete_relations(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        x = random.randint(-5, 5)
        m = random.randint(-4, 4)
        b = random.randint(-6, 6)
        y = m * x + b
        prompt = f"\\text{{If }} y = {m}x + {b}, \\text{{ find }} y \\text{{ when }} x = {x}."
        answer = str(y) if include_answer_key else None
        return prompt, f"y when x={x}", answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _continuous_relations(topic: str, settings: dict) -> list[Question]:
    return _discrete_relations(topic, settings)


def _evaluating_graphing_functions(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        x = random.randint(-4, 4)
        a = random.randint(-3, 3)
        b = random.randint(-6, 6)
        value = a * x * x + b
        fn = f"f(x) = {a}x^2 + {b}" if a != 0 else f"f(x) = {b}"
        prompt = f"\\text{{Given }} {fn}, \\text{{ find }} f({x})."
        answer = str(value) if include_answer_key else None
        return prompt, f"f({x})", answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _writing_linear_equations(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        m = random.randint(-5, 5)
        while m == 0:
            m = random.randint(-5, 5)
        b = random.randint(-8, 8)
        x1, y1 = random.randint(-4, 4), random.randint(-8, 8)
        prompt = (
            f"\\text{{Write the equation of the line with slope {m} "
            f"through }} ({x1}, {y1})."
        )
        sign = "+" if b >= 0 else "-"
        answer = f"y = {m}x {sign} {abs(b)}" if include_answer_key else None
        return prompt, "Write linear equation", answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _direct_inverse_variation(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        k = random.randint(2, 12)
        if random.choice([True, False]):
            prompt = f"\\text{{Write a direct variation equation with }} k = {k}."
            answer = f"y = {k}x" if include_answer_key else None
        else:
            prompt = f"\\text{{Write an inverse variation equation with }} k = {k}."
            answer = f"y = \\frac{{{k}}}{{x}}" if include_answer_key else None
        return prompt, "Variation equation", answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _systems(topic: str, settings: dict, method: str) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        x = random.randint(-5, 5)
        y = random.randint(-5, 5)
        a1, b1 = random.randint(1, 4), random.randint(1, 4)
        a2, b2 = random.randint(1, 4), random.randint(-4, -1)
        c1 = a1 * x + b1 * y
        c2 = a2 * x + b2 * y
        prompt = f"\\begin{{cases}} {a1}x + {b1}y = {c1} \\\\ {a2}x + {b2}y = {c2} \\end{{cases}}"
        answer = f"(x, y) = ({x}, {y})" if include_answer_key else None
        return prompt, f"system ({method})", answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _exponential_growth_decay(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 5))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        initial = random.randint(50, 500)
        rate = random.choice([0.05, 0.1, 0.15, 0.2])
        years = random.randint(2, 6)
        growth = random.choice([True, False])
        factor = 1 + rate if growth else 1 - rate
        final = round(initial * (factor**years), 2)
        kind = "growth" if growth else "decay"
        prompt = (
            f"\\text{{A population of {initial} changes by {int(rate * 100)}\\% "
            f"{kind} per year. Find the value after {years} years.}}"
        )
        answer = str(final) if include_answer_key else None
        return prompt, f"exponential {kind}", answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _polynomial_add_subtract(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = polynomial_params_from_settings(settings)
    ops = allowed_rational_operations(settings)

    def build() -> tuple[str, str, str | None]:
        degree = random.randint(params.min_degree, params.max_degree)
        p = Polynomial.random_polynomial(
            degree, params.coef_min, params.coef_max, positive_leading=params.positive_leading
        )
        q = Polynomial.random_polynomial(
            degree, params.coef_min, params.coef_max, positive_leading=params.positive_leading
        )
        op = random.choice(ops)
        result = p + q if op == "+" else p - q
        prompt = f"({p.to_latex()}) {op} ({q.to_latex()})"
        answer = result.to_latex() if include_answer_key else None
        return prompt, f"({p}) {op} ({q})", answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _polynomial_multiply(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = polynomial_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        p = Polynomial.random_polynomial(
            random.randint(params.min_degree, params.max_degree),
            params.coef_min,
            params.coef_max,
            positive_leading=params.positive_leading,
        )
        q = Polynomial.random_polynomial(
            random.randint(params.min_degree, params.max_degree),
            params.coef_min,
            params.coef_max,
            positive_leading=params.positive_leading,
        )
        result = p * q
        prompt = f"({p.to_latex()})({q.to_latex()})"
        answer = result.to_latex() if include_answer_key else None
        return prompt, f"({p})({q})", answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _polynomial_multiply_special(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        a = random.randint(2, 9)
        b = random.randint(1, 8)
        pattern = random.choice(["square", "sum_diff"])
        if pattern == "square":
            prompt = f"(x + {a})^2"
            answer = f"x^2 + {2 * a}x + {a * a}" if include_answer_key else None
        else:
            op = random.choice(["+", "-"])
            prompt = f"(x + {a})(x {op} {b})"
            if op == "+":
                answer = f"x^2 + {a + b}x + {a * b}" if include_answer_key else None
            else:
                answer = f"x^2 + {a - b}x - {a * b}" if include_answer_key else None
        return prompt, prompt, answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _polynomial_factoring(topic: str, settings: dict, method_overrides: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = polynomial_params_from_settings(settings)
    merged = {**settings, **method_overrides}

    questions: list[Question] = []
    for _ in range(count):
        options = build_factorable_options(merged, params.min_degree, params.max_degree)
        result = create_factorable_polynomial(options)
        poly = result.polynomial
        factors = "".join(f"({factor.to_latex()})" for factor in result.factors)
        questions.append(
            Question(
                id=str(uuid.uuid4()),
                topic=topic,
                prompt_latex=poly.to_latex(),
                prompt_text=str(poly),
                answer_latex=factors if include_answer_key else None,
                metadata=merge_enrichment_metadata(
                    settings,
                    {"factoring_method": result.method},
                    answer=factors if include_answer_key else None,
                ),
            )
        )
    return questions


def _quadratic_square_roots(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = polynomial_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        root = random.randint(2, max(3, params.coef_max))
        a = random.randint(1, max(1, min(5, params.coef_max)))
        c = a * root * root
        prompt = f"{a}x^2 = {c}"
        answer = f"x = \\pm {root}" if include_answer_key else None
        return prompt, prompt, answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _quadratic_factoring_equations(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    questions: list[Question] = []
    for _ in range(count):
        options = build_factorable_options(settings, 2, 2)
        result = create_factorable_polynomial(options)
        poly = result.polynomial
        roots = [str(-factor.coef(0) // factor.coef(1)) for factor in result.factors if factor.deg() == 1]
        answer = ", ".join(f"x = {root}" for root in roots) if include_answer_key else None
        questions.append(
            Question(
                id=str(uuid.uuid4()),
                topic=topic,
                prompt_latex=f"{poly.to_latex()} = 0",
                prompt_text=f"{poly} = 0",
                answer_latex=answer,
                metadata=merge_enrichment_metadata(settings, {"factoring_method": result.method}, answer=answer),
            )
        )
    return questions


def _quadratic_formula(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = polynomial_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        a = random.randint(1, max(1, min(3, params.coef_max)))
        b = random.randint(params.coef_min, params.coef_max)
        c = random.randint(params.coef_min, params.coef_max)
        prompt = f"{a}x^2 + {b}x + {c} = 0"
        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            answer = "\\text{no real solutions}" if include_answer_key else None
        else:
            root = math.sqrt(discriminant)
            x1 = (-b + root) / (2 * a)
            x2 = (-b - root) / (2 * a)
            answer = f"x = {x1:.3g}, {x2:.3g}" if include_answer_key else None
        return prompt, prompt, answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _quadratic_discriminant(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = polynomial_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        a = random.randint(1, max(1, min(4, params.coef_max)))
        b = random.randint(params.coef_min, params.coef_max)
        c = random.randint(params.coef_min, params.coef_max)
        d = b * b - 4 * a * c
        prompt = f"\\text{{Find the discriminant of }} {a}x^2 + {b}x + {c}."
        if not include_answer_key:
            answer = None
        elif d > 0:
            answer = f"D = {d}; \\text{{two real roots}}"
        elif d == 0:
            answer = "D = 0; \\text{one real root}"
        else:
            answer = f"D = {d}; \\text{{no real roots}}"
        return prompt, f"discriminant of {a}x^2+{b}x+{c}", answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _quadratic_completing_square_constant(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = polynomial_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        h = random.randint(params.coef_min, params.coef_max)
        k = random.randint(params.coef_min, params.coef_max)
        c = h * h + k
        prompt = f"x^2 + {2 * h}x + c \\text{{ is a perfect square trinomial. Find }} c."
        answer = str(c) if include_answer_key else None
        return prompt, f"find c for square with h={h}", answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _quadratic_completing_square_solve(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = polynomial_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        h = random.randint(params.coef_min, params.coef_max)
        k = random.randint(params.coef_min, params.coef_max)
        b = 2 * h
        c = h * h + k
        prompt = f"x^2 + {b}x + {c} = 0"
        if k == 0:
            answer = f"x = {-h}" if include_answer_key else None
        elif k > 0:
            answer = f"x = {-h} \\pm {math.sqrt(k):.3g}" if include_answer_key else None
        else:
            answer = "\\text{no real solutions}" if include_answer_key else None
        return prompt, prompt, answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _radical_distance_formula(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        x1, y1 = random.randint(-6, 6), random.randint(-6, 6)
        x2, y2 = random.randint(-6, 6), random.randint(-6, 6)
        dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        prompt = f"\\text{{Find the distance between }} ({x1}, {y1}) \\text{{ and }} ({x2}, {y2})."
        answer = f"{dist:.3g}" if include_answer_key else None
        return prompt, f"distance ({x1},{y1}) to ({x2},{y2})", answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _radical_midpoint_formula(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        x1, y1 = random.randint(-8, 8), random.randint(-8, 8)
        x2, y2 = random.randint(-8, 8), random.randint(-8, 8)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        prompt = f"\\text{{Find the midpoint of }} ({x1}, {y1}) \\text{{ and }} ({x2}, {y2})."
        answer = f"\\left({mx:g}, {my:g}\\right)" if include_answer_key else None
        return prompt, f"midpoint ({x1},{y1}) to ({x2},{y2})", answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _radical_add_subtract(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = radical_params_from_settings(settings)
    ops = allowed_rational_operations(settings)

    def build() -> tuple[str, str, str | None]:
        r = random.randint(max(2, params.radicand_min // 10), min(30, params.radicand_max // 5))
        a = random.randint(2, 6)
        b = random.randint(1, 5)
        op = random.choice(ops)
        prompt = f"{a}\\sqrt{{{r}}} {op} {b}\\sqrt{{{r}}}"
        coeff = a + b if op == "+" else a - b
        answer = f"{coeff}\\sqrt{{{r}}}" if include_answer_key else None
        return prompt, prompt, answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _radical_multiply(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = radical_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        lo = max(2, int(params.radicand_min ** 0.5))
        hi = max(lo + 1, min(20, int(params.radicand_max ** 0.5)))
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        prompt = f"\\sqrt{{{a}}} \\cdot \\sqrt{{{b}}}"
        product = a * b
        coeff, simplified = Polynomial.simplify_square_root(product)
        answer = square_root_latex(coeff, simplified) if include_answer_key else None
        return prompt, f"sqrt({a}) * sqrt({b})", answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _radical_divide(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = radical_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        lo = max(2, int(params.radicand_min ** 0.5))
        hi = max(lo + 1, min(20, int(params.radicand_max ** 0.5)))
        a = random.randint(lo, hi * 2)
        b = random.randint(lo, hi)
        prompt = f"\\frac{{\\sqrt{{{a}}}}}{{\\sqrt{{{b}}}}}"
        coeff, simplified = Polynomial.simplify_square_root(Fraction(a, b).limit_denominator().numerator)
        answer = (
            f"\\frac{{{square_root_latex(1, simplified)}}}{{{math.sqrt(b):.0f}}}"
            if include_answer_key
            else None
        )
        return prompt, f"sqrt({a})/sqrt({b})", answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _radical_equations(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        x = random.randint(2, 12)
        a = random.randint(1, 5)
        rhs = math.sqrt(a * x)
        prompt = f"\\sqrt{{{a}x}} = {rhs:.3g}"
        answer = f"x = {x}" if include_answer_key else None
        return prompt, prompt, answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _rational_expression_multiply_divide(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        p = Polynomial.random_polynomial(1, -6, 6, positive_leading=True)
        q = Polynomial.random_polynomial(1, -6, 6, positive_leading=True)
        r = Polynomial.random_polynomial(1, -6, 6, positive_leading=True)
        s = Polynomial.random_polynomial(1, -6, 6, positive_leading=True)
        op = random.choice(["\\cdot", "\\div"])
        if op == "\\cdot":
            num = p * r
            den = q * s
            prompt = f"\\frac{{{p.to_latex()}}}{{{q.to_latex()}}} {op} \\frac{{{r.to_latex()}}}{{{s.to_latex()}}}"
        else:
            num = p * s
            den = q * r
            prompt = f"\\frac{{{p.to_latex()}}}{{{q.to_latex()}}} {op} \\frac{{{r.to_latex()}}}{{{s.to_latex()}}}"
        answer = f"\\frac{{{num.to_latex()}}}{{{den.to_latex()}}}" if include_answer_key else None
        return prompt, "rational multiply/divide", answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _scaffold(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    questions: list[Question] = []
    for index in range(count):
        a = random.randint(2, 12)
        b = random.randint(2, 12)
        prompt_latex = f"{a} + {b}"
        questions.append(
            Question(
                id=str(uuid.uuid4()),
                topic=topic,
                prompt_latex=prompt_latex,
                prompt_text=f"{a} + {b}",
                answer_latex=str(a + b) if include_answer_key else None,
                metadata=scaffold_metadata(),
            )
        )
    return questions


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "scaffold": _scaffold,
    "exponential_growth_decay": _exponential_growth_decay,
    "polynomial_add_subtract": _polynomial_add_subtract,
    "polynomial_multiply": _polynomial_multiply,
    "polynomial_multiply_special": _polynomial_multiply_special,
    "polynomial_factoring_common_factor": lambda topic, settings: _polynomial_factoring(
        topic,
        settings,
        {
            "factor_normal": True,
            "factor_grouping": False,
            "factor_substitution": False,
            "factor_difference_of_squares": False,
            "factor_difference_of_cubes": False,
            "factor_sum_of_cubes": False,
            "factor_rrt": False,
        },
    ),
    "polynomial_factoring_special_cases": lambda topic, settings: _polynomial_factoring(
        topic,
        settings,
        {
            "factor_normal": False,
            "factor_grouping": False,
            "factor_substitution": False,
            "factor_difference_of_squares": True,
            "factor_difference_of_cubes": True,
            "factor_sum_of_cubes": True,
            "factor_rrt": False,
        },
    ),
    "polynomial_factoring_grouping": lambda topic, settings: _polynomial_factoring(
        topic,
        settings,
        {
            "factor_normal": False,
            "factor_grouping": True,
            "factor_substitution": False,
            "factor_difference_of_squares": False,
            "factor_difference_of_cubes": False,
            "factor_sum_of_cubes": False,
            "factor_rrt": False,
        },
    ),
    "quadratic_square_roots": _quadratic_square_roots,
    "quadratic_factoring_equations": _quadratic_factoring_equations,
    "quadratic_formula": _quadratic_formula,
    "quadratic_discriminant": _quadratic_discriminant,
    "quadratic_completing_square_constant": _quadratic_completing_square_constant,
    "quadratic_completing_square_solve": _quadratic_completing_square_solve,
    "radical_distance_formula": _radical_distance_formula,
    "radical_midpoint_formula": _radical_midpoint_formula,
    "radical_add_subtract": _radical_add_subtract,
    "radical_multiply": _radical_multiply,
    "radical_divide": _radical_divide,
    "radical_equations": _radical_equations,
    "rational_expression_multiply_divide": _rational_expression_multiply_divide,
}
