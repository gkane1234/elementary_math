import random
import uuid

from packages.polynomial_core import Polynomial, square_root_latex

from question_engine.base import QuestionType, register
from question_engine.models import Question, SettingField

_SQUARE_FREE_BASES = (2, 3, 5, 6, 7, 10, 11, 13, 14, 15, 17, 19, 21, 22, 23, 26, 29, 30)


def _normalize_range(min_value: int, max_value: int) -> tuple[int, int]:
    if min_value > max_value:
        return max_value, min_value
    return min_value, max_value


def _is_perfect_square(value: int) -> bool:
    if value < 0:
        return False
    root = int(value**0.5)
    return root * root == value


def _create_simplifiable_radicand(radicand_min: int, radicand_max: int) -> int:
    min_value, max_value = _normalize_range(radicand_min, radicand_max)

    for _ in range(200):
        outer = random.randint(2, 12)
        inner_square = random.randint(2, 8) ** 2
        inner = random.choice(_SQUARE_FREE_BASES)
        radicand = outer * outer * inner_square * inner
        if min_value <= radicand <= max_value and not _is_perfect_square(radicand):
            return radicand

    outer = random.randint(2, 8)
    inner = random.choice(_SQUARE_FREE_BASES)
    radicand = outer * outer * 4 * inner
    return max(min_value, min(max_value, radicand))


def _create_square_free_radicand(radicand_min: int, radicand_max: int) -> int:
    min_value, max_value = _normalize_range(radicand_min, radicand_max)

    for _ in range(200):
        candidate = random.randint(min_value, max_value)
        coeff, simplified = Polynomial.simplify_square_root(candidate)
        if simplified == candidate and not _is_perfect_square(candidate):
            return candidate

    for candidate in range(min_value, max_value + 1):
        coeff, simplified = Polynomial.simplify_square_root(candidate)
        if simplified == candidate and not _is_perfect_square(candidate):
            return candidate

    return max(min_value, 2)


@register
class RadicalSimplificationQuestionType(QuestionType):
    id = "radical_simplification"
    name = "Simplifying single radicals"
    category = "Algebra 1 — Radical Expressions"
    description = "Simplify square roots by factoring out perfect squares."
    instruction_latex = "\\text{Simplify.}"
    instruction_text = "Simplify."

    def settings_schema(self) -> list[SettingField]:
        return [
            SettingField("count", "Number of questions", "int", 10, min=1, max=50),
            SettingField(
                "max_columns",
                "Columns (auto-fit up to 3)",
                "select",
                "auto",
                options=["auto", "1", "2", "3"],
            ),
            SettingField("radicand_min", "Radicand min", "int", 12, min=2, max=1000),
            SettingField("radicand_max", "Radicand max", "int", 300, min=2, max=1000),
            SettingField("require_simplifiable", "Require simplifiable radicals", "bool", True),
            SettingField("include_answer_key", "Include answer key", "bool", False),
        ]

    def generate(self, settings: dict) -> list[Question]:
        count = int(settings.get("count", 10))
        radicand_min = int(settings.get("radicand_min", 12))
        radicand_max = int(settings.get("radicand_max", 300))
        require_simplifiable = bool(settings.get("require_simplifiable", True))
        include_answer_key = bool(settings.get("include_answer_key", False))

        questions: list[Question] = []
        for _ in range(count):
            if require_simplifiable:
                radicand = _create_simplifiable_radicand(radicand_min, radicand_max)
            else:
                radicand = _create_square_free_radicand(radicand_min, radicand_max)

            coeff, simplified_radicand = Polynomial.simplify_square_root(radicand)
            answer_latex = None
            if include_answer_key:
                answer_latex = square_root_latex(coeff, simplified_radicand)

            questions.append(
                Question(
                    id=str(uuid.uuid4()),
                    topic=self.id,
                    prompt_latex=f"\\sqrt{{{radicand}}}",
                    prompt_text=f"sqrt({radicand})",
                    answer_latex=answer_latex,
                    metadata={"radicand": radicand, "simplified_coefficient": coeff},
                )
            )

        return questions
