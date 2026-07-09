import uuid

from packages.polynomial_core import (
    build_rational_expression_problem,
    sum_of_fractions_latex,
    term_prompt_text,
)

from question_engine.base import QuestionType, register
from question_engine.factoring_settings import build_factorable_options, shared_factoring_settings
from question_engine.latex_helpers import polynomial_fraction_latex
from question_engine.models import Question, SettingField


@register
class RationalExpressionSimplificationQuestionType(QuestionType):
    id = "rational_expression_simplification"
    name = "Adding and subtracting"
    category = "Algebra 1 — Rational Expressions"
    description = (
        "Combine a sum of rational terms by finding a common denominator, "
        "then simplify to a single fraction."
    )
    instruction_latex = "\\text{Combine and simplify.}"
    instruction_text = "Combine and simplify."

    def settings_schema(self) -> list[SettingField]:
        return [
            SettingField("count", "Number of questions", "int", 5, min=1, max=50),
            SettingField(
                "max_columns",
                "Columns (auto-fit up to 3)",
                "select",
                "auto",
                options=["auto", "1", "2", "3"],
            ),
            SettingField("term_count", "Number of rational terms", "int", 3, min=2, max=5),
            SettingField("denominator_degree_min", "LCD factor degree min", "int", 2, min=1, max=6),
            SettingField("denominator_degree_max", "LCD factor degree max", "int", 3, min=1, max=6),
            SettingField("coef_min", "Coefficient min", "int", -6, min=-20, max=20),
            SettingField("coef_max", "Coefficient max", "int", 6, min=-20, max=20),
            SettingField("positive_leading_coefficient", "Positive leading coefficients", "bool", True),
            SettingField(
                "use_random_partial_solution",
                "Use random partial-fraction numerators",
                "bool",
                True,
            ),
            SettingField(
                "allow_polynomial_terms",
                "Allow terms with no denominator",
                "bool",
                True,
            ),
            SettingField(
                "allow_full_lcd_terms",
                "Allow terms over the full LCD",
                "bool",
                True,
            ),
            SettingField(
                "inflation_chance",
                "Degree inflation chance (%)",
                "range",
                15,
                min=0,
                max=100,
            ),
            SettingField(
                "max_inflation_degree",
                "Max inflation factor degree",
                "int",
                2,
                min=1,
                max=4,
            ),
            SettingField(
                "cancel_factor_count",
                "LCD factors to cancel in final answer",
                "select",
                "random",
                options=["random", "0", "1", "2", "3", "4"],
            ),
            *shared_factoring_settings(),
            SettingField("include_answer_key", "Include answer key", "bool", False),
            SettingField(
                "include_solution_details",
                "Include complete solution details in metadata",
                "bool",
                True,
            ),
        ]

    def generate(self, settings: dict) -> list[Question]:
        count = int(settings.get("count", 5))
        term_count = int(settings.get("term_count", 3))
        denominator_degree_min = int(settings.get("denominator_degree_min", 2))
        denominator_degree_max = int(settings.get("denominator_degree_max", 3))
        include_answer_key = bool(settings.get("include_answer_key", False))
        include_solution_details = bool(settings.get("include_solution_details", True))
        use_random_partial_solution = bool(settings.get("use_random_partial_solution", True))
        allow_polynomial_terms = bool(settings.get("allow_polynomial_terms", True))
        allow_full_lcd_terms = bool(settings.get("allow_full_lcd_terms", True))
        inflation_chance = max(0.0, min(1.0, int(settings.get("inflation_chance", 15)) / 100.0))
        max_inflation_degree = int(settings.get("max_inflation_degree", 2))
        cancel_factor_count = settings.get("cancel_factor_count", "random")

        base_options = build_factorable_options(
            settings,
            denominator_degree_min,
            denominator_degree_max,
        )

        questions: list[Question] = []
        for _ in range(count):
            solution = build_rational_expression_problem(
                base_options,
                term_count=term_count,
                use_random_partial_solution=use_random_partial_solution,
                allow_polynomial_terms=allow_polynomial_terms,
                allow_full_lcd_terms=allow_full_lcd_terms,
                inflation_chance=inflation_chance,
                max_inflation_degree=max_inflation_degree,
                cancel_factor_count=cancel_factor_count,
            )

            answer_latex = None
            if include_answer_key:
                answer_numerator = solution.final_numerator or solution.simplified_numerator
                answer_denominator = solution.final_denominator or solution.simplified_denominator
                answer_latex = polynomial_fraction_latex(
                    answer_numerator,
                    answer_denominator,
                )

            metadata = {
                "term_count": len(solution.display_terms),
                "numerator_degree": solution.simplified_numerator.deg(),
                "denominator_degree": solution.simplified_denominator.deg(),
                "combined_numerator_degree": solution.combined_numerator.deg(),
                "combined_denominator_degree": solution.combined_denominator.deg(),
                "has_polynomial_term": solution.polynomial_term is not None,
                "has_full_lcd_term": solution.full_lcd_numerator is not None,
                "has_degree_inflation": solution.inflation_factor.deg() > 0,
                "cancelled_lcd_factor_count": len(solution.cancelled_lcd_factors),
                "inflation_chance": inflation_chance,
                "max_inflation_degree": max_inflation_degree,
            }
            if include_solution_details:
                metadata["solution"] = solution.to_dict()

            questions.append(
                Question(
                    id=str(uuid.uuid4()),
                    topic=self.id,
                    prompt_latex=sum_of_fractions_latex(list(solution.display_terms)),
                    prompt_text=" + ".join(term_prompt_text(term) for term in solution.display_terms),
                    answer_latex=answer_latex,
                    metadata=metadata,
                )
            )

        return questions
