"""Rational simplification — delegates to OpenStax form-catalog primitive generator."""

from question_engine.base import QuestionType, register
from question_engine.generators import GENERATORS
from question_engine.settings.generator_profiles import schema_for_generator


@register
class RationalSimplificationQuestionType(QuestionType):
    id = "rational_simplification"
    name = "Simplifying and excluded values"
    category = "Algebra 1 — Rational Expressions"
    description = (
        "Simplify rational expressions by canceling common polynomial factors "
        "and state excluded values (OpenStax §8.1 form catalog)."
    )
    instruction_latex = r"\text{Simplify. State any excluded values.}"
    instruction_text = "Simplify. State any excluded values."

    def settings_schema(self):
        return schema_for_generator(self.id)

    def generate(self, settings: dict):
        return GENERATORS["rational_simplification"](self.id, settings)
