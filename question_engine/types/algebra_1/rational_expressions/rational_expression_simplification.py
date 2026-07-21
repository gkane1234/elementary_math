import random
import uuid

from packages.polynomial_core import (
    build_rational_expression_problem,
    excluded_values_from_factors,
    rational_excluded_values_latex,
    sum_of_fractions_latex,
    term_prompt_text,
)

from question_engine.base import QuestionType, register
from question_engine.factoring_settings import build_factorable_options
from question_engine.frameworks.primitives.rational_cancel import (
    ALL_AVAILABLE_CANCEL,
    apply_continuous_rational_structure,
    clamp_cancel_to_available,
    is_all_available_cancel,
    resolve_rational_cancel_count,
    sample_all_available_factor_count,
)
from question_engine.latex_helpers import polynomial_fraction_latex
from question_engine.models import Question
from question_engine.settings.enrichment import merge_enrichment_metadata, random_term_count
from question_engine.settings.generator_profiles import schema_for_generator


def _resolve_add_subtract_structure(settings: dict) -> dict:
    """Apply Easy/Medium/Hard structural rules onto a copy of settings."""
    resolved = dict(settings)
    structure = str(resolved.get("add_subtract_structure", "auto")).strip().lower()
    tier = str(resolved.get("difficulty_tier", "")).strip().lower()

    if structure == "auto":
        if tier == "easy":
            structure = "shared_lcd"
        elif tier == "medium":
            structure = random.choice(["unlike_binomials", "multi_term"])
        elif tier == "hard":
            structure = "complex"
        else:
            structure = "complex"

    if structure == "shared_lcd":
        resolved.update(
            {
                "term_count": 2,
                "max_lcd_factors": 1,
                "leading_coefficient_one": True,
                "monic_only": True,
                "denominator_degree_min": 1,
                "denominator_degree_max": 1,
                "allow_polynomial_terms": False,
                "allow_full_lcd_terms": False,
                "inflation_chance": 0,
                "prefer_simple_factors": True,
                "content_primitive_denominators": True,
                "force_shared_lcd": True,
                "allow_monomial_lcd": True,
                "factor_rrt": False,
                # Single-factor LCD cannot cancel a factor and still leave a
                # denominator; builder rejects cancel>=1 when max_lcd_factors=1.
                "cancel_factor_count": 0,
            }
        )
    elif structure == "unlike_binomials":
        # Medium variant: 2 terms, non-monic binomial denominators.
        resolved.update(
            {
                "term_count": 2,
                "max_lcd_factors": 2,
                "leading_coefficient_one": False,
                "monic_only": False,
                "denominator_degree_min": 1,
                "denominator_degree_max": 1,
                "allow_polynomial_terms": False,
                "allow_full_lcd_terms": False,
                "inflation_chance": 0,
                "prefer_simple_factors": True,
                "content_primitive_denominators": True,
                "force_shared_lcd": False,
                "allow_monomial_lcd": False,
                "factor_rrt": False,
            }
        )
        resolved.setdefault("cancel_factor_count", 1)
    elif structure == "multi_term":
        # Medium variant: 3 monic terms, still simple factoring.
        resolved.update(
            {
                "term_count": 3,
                "max_lcd_factors": 2,
                "leading_coefficient_one": True,
                "monic_only": True,
                "denominator_degree_min": 1,
                "denominator_degree_max": 1,
                "allow_polynomial_terms": False,
                "allow_full_lcd_terms": False,
                "inflation_chance": 0,
                "prefer_simple_factors": True,
                "content_primitive_denominators": True,
                "force_shared_lcd": False,
                "allow_monomial_lcd": False,
                "factor_rrt": False,
            }
        )
        resolved.setdefault("cancel_factor_count", 1)
    else:
        # complex / hard — keep caller values; fill sensible defaults.
        resolved.setdefault("max_lcd_factors", 4)
        resolved.setdefault("prefer_simple_factors", True)
        resolved.setdefault("content_primitive_denominators", True)
        resolved.setdefault("force_shared_lcd", False)
        resolved.setdefault("allow_monomial_lcd", False)

    resolved["add_subtract_structure"] = structure
    return resolved


@register
class RationalExpressionSimplificationQuestionType(QuestionType):
    id = "rational_expression_simplification"
    name = "Adding and subtracting rational expressions"
    category = "Algebra 1 — Rational Expressions"
    description = (
        "Combine a sum of rational terms by finding a common denominator, "
        "then simplify to a single fraction."
    )
    instruction_latex = "\\text{Combine and simplify.}"
    instruction_text = "Combine and simplify."

    def settings_schema(self):
        return schema_for_generator(self.id)

    def generate(self, settings: dict) -> list[Question]:
        count = int(settings.get("count", 5))
        include_answer_key = bool(settings.get("include_answer_key", False))
        include_solution_details = bool(settings.get("include_solution_details", True))

        questions: list[Question] = []
        for _ in range(count):
            structured = _resolve_add_subtract_structure(settings)
            # Continuous D overrides EMH plateaus for LCD / term counts.
            structured = apply_continuous_rational_structure(structured)
            term_count = int(structured.get("term_count", random_term_count(structured, default=3)))
            term_count = min(term_count, int(structured.get("max_rational_terms", max(term_count, 5))))
            denominator_degree_min = int(structured.get("denominator_degree_min", 2))
            denominator_degree_max = int(structured.get("denominator_degree_max", 3))
            use_random_partial_solution = bool(structured.get("use_random_partial_solution", True))
            allow_polynomial_terms = bool(structured.get("allow_polynomial_terms", True))
            force_lcd = bool(structured.get("force_lcd", False))
            allow_full_lcd_terms = bool(structured.get("allow_full_lcd_terms", True)) or force_lcd
            if force_lcd:
                allow_polynomial_terms = False
            allow_unlike_denominators = bool(structured.get("allow_unlike_denominators", True))
            inflation_chance = max(
                0.0, min(1.0, int(structured.get("inflation_chance", 15)) / 100.0)
            )
            max_inflation_degree = int(structured.get("max_inflation_degree", 2))

            max_lcd_factors = int(structured.get("max_lcd_factors", 4))
            prefer_simple_factors = bool(structured.get("prefer_simple_factors", True))
            content_primitive = bool(structured.get("content_primitive_denominators", True))
            force_shared_lcd = bool(structured.get("force_shared_lcd", False))
            allow_monomial_lcd = bool(structured.get("allow_monomial_lcd", False))

            base_options = build_factorable_options(
                structured,
                denominator_degree_min,
                denominator_degree_max,
            )
            if not allow_unlike_denominators:
                base_options = build_factorable_options(
                    {**structured, "factor_rrt": False},
                    denominator_degree_min,
                    denominator_degree_max,
                )

            solution = None
            cancel_factor_count = 0
            requested_cancel = 0
            for _attempt in range(80):
                if force_lcd:
                    # Cancelled-LCD construction path never emits a full-LCD term.
                    cancel_factor_count = 0
                    requested_cancel = 0
                    builder_cancel: int | str = 0
                else:
                    requested_cancel = resolve_rational_cancel_count(structured)
                    if is_all_available_cancel(requested_cancel):
                        # Cap LCD size for "all available" — cancel every factor
                        # in a normal problem, do not grow to continuous D max.
                        max_lcd_factors = sample_all_available_factor_count(
                            structured, default=max_lcd_factors
                        )
                        structured["max_lcd_factors"] = max_lcd_factors
                        cancel_factor_count = max_lcd_factors
                        builder_cancel = ALL_AVAILABLE_CANCEL
                    else:
                        # Capacity: leave at least one LCD factor when a polynomial
                        # answer is disallowed; otherwise every LCD factor may cancel.
                        if allow_polynomial_terms:
                            available = max_lcd_factors
                        else:
                            available = max(0, max_lcd_factors - 1)
                        cancel_factor_count = clamp_cancel_to_available(
                            requested_cancel, available
                        )
                        builder_cancel = cancel_factor_count
                try:
                    candidate = build_rational_expression_problem(
                        base_options,
                        term_count=term_count,
                        use_random_partial_solution=use_random_partial_solution,
                        allow_polynomial_terms=allow_polynomial_terms,
                        allow_full_lcd_terms=allow_full_lcd_terms,
                        inflation_chance=inflation_chance,
                        max_inflation_degree=max_inflation_degree,
                        cancel_factor_count=builder_cancel,
                        max_lcd_factors=max_lcd_factors,
                        prefer_simple_factors=prefer_simple_factors,
                        content_primitive=content_primitive,
                        allow_empty_denominators=allow_polynomial_terms,
                        force_shared_lcd=force_shared_lcd,
                        allow_monomial_lcd=allow_monomial_lcd,
                    )
                except (ValueError, RuntimeError):
                    continue
                if force_lcd and candidate.full_lcd_numerator is None:
                    continue
                if not allow_unlike_denominators:
                    denominators = [
                        term.denominator
                        for term in candidate.display_terms
                        if term.denominator is not None
                    ]
                    if denominators and len({str(d) for d in denominators}) > 1:
                        continue
                if len(candidate.display_terms) < 2:
                    continue
                if max_lcd_factors <= 1 and candidate.lcd.deg() > 1:
                    continue
                solution = candidate
                cancel_factor_count = len(candidate.cancelled_lcd_factors)
                break

            if solution is None:
                raise RuntimeError("Unable to build rational expression problem")

            structured["cancel_factor_count"] = cancel_factor_count

            answer_latex = None
            excluded: list[int] = []
            if include_answer_key:
                from packages.polynomial_core.rational import _scale_fraction_to_integers

                answer_numerator = solution.final_numerator or solution.simplified_numerator
                answer_denominator = solution.final_denominator or solution.simplified_denominator
                answer_numerator, answer_denominator = _scale_fraction_to_integers(
                    answer_numerator,
                    answer_denominator,
                )
                if (
                    answer_denominator.deg() == 0
                    and abs(float(answer_denominator.coef_list()[0]) - 1) < 1e-10
                ):
                    answer_latex = answer_numerator.to_latex()
                else:
                    answer_latex = polynomial_fraction_latex(
                        answer_numerator,
                        answer_denominator,
                    )
                # Excluded values from original LCD / display dens — collect per
                # linear factor so canceled non-monic roots are not dropped.
                factor_pool = list(solution.lcd_factors) + list(solution.cancelled_lcd_factors)
                for term in solution.display_terms:
                    factor_pool.extend(term.denominator_factors)
                excluded_fracs = excluded_values_from_factors(factor_pool)
                note = rational_excluded_values_latex(excluded_fracs)
                if note:
                    answer_latex = f"{answer_latex},\\; {note}"
                excluded = [
                    int(v) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"
                    for v in excluded_fracs
                ]
            metadata = merge_enrichment_metadata(
                structured,
                {
                    "term_count": len(solution.display_terms),
                    "numerator_degree": solution.simplified_numerator.deg(),
                    "denominator_degree": solution.simplified_denominator.deg(),
                    "combined_numerator_degree": solution.combined_numerator.deg(),
                    "combined_denominator_degree": solution.combined_denominator.deg(),
                    "has_polynomial_term": solution.polynomial_term is not None,
                    "has_full_lcd_term": solution.full_lcd_numerator is not None,
                    "has_degree_inflation": solution.inflation_factor.deg() > 0,
                    "cancel_factor_count": cancel_factor_count,
                    "requested_cancel_factor_count": requested_cancel,
                    "cancelled_lcd_factor_count": len(solution.cancelled_lcd_factors),
                    "inflation_chance": inflation_chance,
                    "max_inflation_degree": max_inflation_degree,
                    "force_lcd": force_lcd,
                    "allow_unlike_denominators": allow_unlike_denominators,
                    "add_subtract_structure": structured.get("add_subtract_structure"),
                    "max_lcd_factors": max_lcd_factors,
                    "lcd_degree": solution.lcd.deg(),
                    "excluded_values": excluded,
                },
                answer=answer_latex,
            )
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
