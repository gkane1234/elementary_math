import uuid

from packages.polynomial_core import create_factorable_polynomial

from question_engine.base import QuestionType, register
from question_engine.factoring_settings import build_factorable_options, shared_factoring_settings
from question_engine.models import Question, SettingField


def _format_factors_latex(factors: list) -> str:
    return "".join(f"({factor.to_latex()})" for factor in factors)


@register
class QuadraticFactoringQuestionType(QuestionType):
    id = "quadratic_factoring"
    name = "Quadratic expressions"
    category = "Algebra 1 — Polynomials"
    subcategory = "Factoring"
    description = "Factor quadratic trinomials with integer coefficients."
    instruction_latex = "\\text{Factor completely.}"
    instruction_text = "Factor completely."

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
            SettingField("coef_min", "Coefficient min", "int", -10, min=-20, max=20),
            SettingField("coef_max", "Coefficient max", "int", 10, min=-20, max=20),
            SettingField("positive_leading_coefficient", "Positive leading coefficient", "bool", True),
            *shared_factoring_settings(),
            SettingField("include_answer_key", "Include answer key", "bool", False),
        ]

    def generate(self, settings: dict) -> list[Question]:
        count = int(settings.get("count", 10))
        include_answer_key = bool(settings.get("include_answer_key", False))

        questions: list[Question] = []
        for _ in range(count):
            options = build_factorable_options(settings, 2, 2)
            result = create_factorable_polynomial(options)
            quadratic = result.polynomial
            known_factors = list(result.factors)

            answer_latex = None
            if include_answer_key:
                answer_latex = _format_factors_latex(known_factors)

            questions.append(
                Question(
                    id=str(uuid.uuid4()),
                    topic=self.id,
                    prompt_latex=quadratic.to_latex(),
                    prompt_text=str(quadratic),
                    answer_latex=answer_latex,
                    metadata={"degree": quadratic.deg(), "factoring_method": result.method},
                )
            )

        return questions
