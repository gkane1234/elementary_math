import random
import uuid

from packages.polynomial_core import Polynomial, square_root_latex

from question_engine.base import QuestionType, register
from question_engine.models import Question
from question_engine.settings.generator_profiles import schema_for_generator
from question_engine.settings.params import radical_params_from_settings

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

    def settings_schema(self):
        return schema_for_generator(self.id)

    def generate(self, settings: dict) -> list[Question]:
        count = int(settings.get("count", 10))
        params = radical_params_from_settings(settings)
        include_answer_key = bool(settings.get("include_answer_key", False))

        questions: list[Question] = []
        for _ in range(count):
            if params.require_simplifiable:
                radicand = _create_simplifiable_radicand(params.radicand_min, params.radicand_max)
            else:
                radicand = _create_square_free_radicand(params.radicand_min, params.radicand_max)

            if params.radical_index == 2:
                coeff, simplified_radicand = Polynomial.simplify_square_root(radicand)
                prompt_latex = f"\\sqrt{{{radicand}}}"
                answer_latex = square_root_latex(coeff, simplified_radicand) if include_answer_key else None
            else:
                coeff = 1
                simplified_radicand = radicand
                prompt_latex = f"\\sqrt[{params.radical_index}]{{{radicand}}}"
                answer_latex = prompt_latex if include_answer_key else None

            questions.append(
                Question(
                    id=str(uuid.uuid4()),
                    topic=self.id,
                    prompt_latex=prompt_latex,
                    prompt_text=f"root({radicand})",
                    answer_latex=answer_latex,
                    metadata={
                        "radicand": radicand,
                        "simplified_coefficient": coeff,
                        "radical_index": params.radical_index,
                    },
                )
            )

        return questions
