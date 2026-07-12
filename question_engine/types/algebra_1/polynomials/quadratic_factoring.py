import uuid

from packages.polynomial_core import create_factorable_polynomial

from question_engine.base import QuestionType, register
from question_engine.factoring_settings import build_factorable_options
from question_engine.models import Question
from question_engine.settings.enrichment import merge_enrichment_metadata
from question_engine.settings.generator_profiles import schema_for_generator


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

    def settings_schema(self):
        return schema_for_generator(self.id)

    def generate(self, settings: dict) -> list[Question]:
        count = int(settings.get("count", 10))
        include_answer_key = bool(settings.get("include_answer_key", False))
        deg_min = int(settings.get("min_degree", 2))
        deg_max = int(settings.get("max_degree", 2))
        if deg_max < deg_min:
            deg_min, deg_max = deg_max, deg_min

        questions: list[Question] = []
        for _ in range(count):
            options = build_factorable_options(settings, deg_min, deg_max)
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
                    metadata=merge_enrichment_metadata(
                        settings,
                        {"degree": quadratic.deg(), "factoring_method": result.method},
                        answer=answer_latex,
                    ),
                )
            )

        return questions
