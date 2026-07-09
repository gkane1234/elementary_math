"""One-step equations — framework-backed example type."""

from question_engine.core.base import QuestionType, register
from question_engine.core.registry import get_catalog_entry
from question_engine.frameworks.base import QuestionFramework
from question_engine.frameworks.equation import OneStepEquationsFramework
from question_engine.settings.domains.equation import equation_coef_settings

_ENTRY = get_catalog_entry("one_step_equations")
_FRAMEWORK = OneStepEquationsFramework()


@register
class OneStepEquationsQuestionType(QuestionType):
    id = _ENTRY.id
    name = _ENTRY.name
    category = _ENTRY.category
    subcategory = _ENTRY.subcategory
    description = _ENTRY.description
    instruction_latex = _ENTRY.instruction_latex
    instruction_text = _ENTRY.instruction_text

    def settings_schema(self):
        return QuestionFramework.framework_settings(equation_coef_settings())

    def generate(self, settings: dict):
        return _FRAMEWORK.generate_batch(self.id, settings)
