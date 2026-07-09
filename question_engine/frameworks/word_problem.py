"""Word-problem template framework — narrative prompts with numeric slots.

Template pattern
----------------
``WordProblemTemplate`` holds a LaTeX/plain template with ``{slot}`` placeholders.
A companion ``variable_slots`` dict maps slot names to sampler callables that
read worksheet settings and return display + answer values. This mirrors how
catalog entries declare ``instruction_text`` while deferring numeric generation.

Catalog mapping (16 dedicated + scattered proportion/system types)
------------------------------------------------------------------
| Template family        | Example catalog IDs                                      |
|------------------------|----------------------------------------------------------|
| Equation word problems | ``pa_equations_one_step_word_problems``, ``g6_equations_word_problems`` |
| Proportion / ratio     | ``pa_proportions_word_problems``, Grade 6 ratio topics   |
| Geometry context       | ``pa_similar_figures_word_problems``                     |
| Systems                | ``pa_systems_word_problems``                             |
| Inequality context     | ``g6_inequalities_word_problems``                        |
| Work / DRT / mixture   | ``a2_equations_and_inequalities_*_word_problems``        |

Tier 2 plan: register templates per subcategory; reuse ``NumberFramework`` and
``EquationFramework`` samplers inside slot functions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from .base import QuestionFramework

SlotSampler = Callable[[dict], tuple[str, str | None]]


@dataclass
class WordProblemTemplate:
    """Declarative word-problem shell with injectable numeric slots."""

    template_latex: str
    template_text: str
    variable_slots: dict[str, SlotSampler] = field(default_factory=dict)
    answer_slot: str | None = None

    def render(self, settings: dict) -> tuple[str, str, str | None]:
        """Fill slots and return (prompt_latex, prompt_text, answer)."""
        values: dict[str, str] = {}
        answer: str | None = None
        for name, sampler in self.variable_slots.items():
            display, slot_answer = sampler(settings)
            values[name] = display
            if self.answer_slot == name and slot_answer is not None:
                answer = slot_answer
        latex = self.template_latex.format(**values)
        text = self.template_text.format(**values)
        return latex, text, answer


class WordProblemFramework(QuestionFramework):
    """Batch generation wrapper around a ``WordProblemTemplate``.

  Settings (via ``word_problem_settings()``):
  - ``difficulty`` — easy | medium | hard (controls coefficient / context ranges)
  - ``units`` — optional unit label appended to numeric answers
  """

    def __init__(self, template: WordProblemTemplate | None = None):
        self.template = template

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {
            "difficulty": settings.get("difficulty", "medium"),
            "units": settings.get("units", ""),
            "template_latex": self.template.template_latex if self.template else None,
        }

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        if self.template is None:
            raise NotImplementedError(
                "WordProblemFramework requires a WordProblemTemplate instance."
            )
        return self.template.render(settings)
