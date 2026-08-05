"""Quadratic factoring — delegates to OpenStax form-catalog primitive generator."""

from question_engine.base import QuestionType, register
from question_engine.generators import GENERATORS
from question_engine.settings.generator_profiles import schema_for_generator


@register
class QuadraticFactoringQuestionType(QuestionType):
    id = "quadratic_factoring"
    name = "Quadratic expressions"
    category = "Algebra 1 — Polynomials"
    subcategory = "Factoring"
    description = (
        "Factors-first quadratic trinomials (OpenStax §7.2–7.3 form catalog); "
        "unsimplified stems at high D."
    )
    instruction_latex = "\\text{Factor.}"
    instruction_text = "Factor."

    def settings_schema(self):
        return schema_for_generator(self.id)

    def generate(self, settings: dict):
        return GENERATORS["quadratic_factoring"](self.id, settings)
