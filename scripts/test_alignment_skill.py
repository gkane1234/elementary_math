"""Skill-gate checks for the alignment pack. Uses the local textbook cache."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.alignment_skill import (
    expression_shapes,
    filename_score,
    has_abs,
    has_ineq,
    in_topic_not_generated,
    item_matches,
    question_form,
    section_slug_score,
    skill_profile,
)

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "textbooks" / "alignment_cache"


def profile(name: str, type_id: str, stems: list[str]):
    samples = [
        {"instruction_latex": "", "prompt_latex": stem, "prompt_text": "", "error": None, "tier": "easy"}
        for stem in stems
    ]
    return skill_profile({"name": name, "type_id": type_id}, {"samples": samples})


def keep(text: str, prof, **kwargs) -> bool:
    return item_matches(text, prof, **kwargs)


def main() -> None:
    assert has_ineq(r"\left|x\right|<1")
    assert not has_ineq(r"\left|x\right|=2")
    assert not has_ineq(r"$\left|\right. x \left|\right. = 6$")
    assert has_ineq(r"$\left|\right. x \left|\right. < 5$")
    assert has_abs(r"\left|x - 1\right| = 2")
    assert "quotient" in expression_shapes(r"\frac{d}{dx}\left(\frac{x}{2x}\right)")
    assert "quotient" not in expression_shapes(r"f(x) = x^{7} + 10")
    assert "chain" in expression_shapes(r"y = 3 u - 6 , u = 2 x^{2}")
    assert "chain" in expression_shapes(r"\frac{d}{dx}\left(\left(3x + 3\right)^{2}\right)")
    assert "product" in expression_shapes(r"\frac{d}{dx}\left(x\left(2x\right)\right)")
    plain = expression_shapes(r"\frac{d}{dx}\left(x^{2}\right)")
    assert "power" in plain and "chain" not in plain and "quotient" not in plain

    rect = profile(
        "Rectangles with fraction side lengths",
        "g6_rectangles_with_fraction_side_lengths",
        [r"Find the area of the rectangle with base \frac{1}{2} cm and height \frac{3}{4} cm."],
    )
    lesson = json.loads((CACHE / "our_parsed" / "u4-l13.json").read_text())
    kept = []
    for block in lesson["blocks"]:
        if block["kind"] != "practice":
            continue
        alt = " ".join(img.get("alt") or "" for img in block.get("images") or [])
        if keep(block["text"], rect, source_text=lesson["title"], alt=alt):
            kept.append(block["index"])
    assert kept == [1, 2, 3, 4], kept

    hanger = profile(
        "Equations with hanger diagrams",
        "g6_equations_hanger_diagrams",
        [r"Use the diagram to solve 3x = 15."],
    )
    hang = json.loads((CACHE / "our_parsed" / "u6-l3.json").read_text())
    hang_kept = []
    for block in hang["blocks"]:
        if block["kind"] != "practice":
            continue
        alt = " ".join(img.get("alt") or "" for img in block.get("images") or [])
        if keep(block["text"], hanger, source_text=hang["title"], alt=alt):
            hang_kept.append(block["index"])
    assert hang_kept == [1, 2, 3, 4], hang_kept
    assert 6 not in hang_kept and 7 not in hang_kept

    eqs = profile(
        "Absolute value equations",
        "absolute_value_equations",
        [r"Solve: \left|x - 1\right| = 2"],
    )
    ineqs = profile(
        "Absolute value inequalities",
        "absolute_value_inequalities",
        [r"Solve: \left|x - 1\right| < 1"],
    )
    eq_item = r"438 . $\left|\right. 2 x - 3 \left|\right. - 4 = 1$"
    ineq_item = r"462 . $\left|\right. 2 x + 3 \left|\right. + 5 < 4$"
    story = "Miguel routinely overshoots the weight of his tortillas by 0.5 gram."
    assert keep(eq_item, eqs, source_text="Solve Absolute Value Inequalities")
    assert not keep(ineq_item, eqs, source_text="Solve Absolute Value Inequalities")
    assert not keep(story, eqs, source_text="Solve Absolute Value Inequalities")
    assert keep(ineq_item, ineqs, source_text="Solve Absolute Value Inequalities")
    assert not keep(eq_item, ineqs, source_text="Solve Absolute Value Inequalities")

    factor = profile(
        "Quadratic factoring",
        "quadratic_factoring",
        [r"Factor. x^{2} - 4"],
    )
    assert keep(r"63 . $x^{2} + 4 x + 3$", factor, heading="Practice Makes Perfect", source_text="Factor Trinomials of the Form x2 + bx + c")
    assert not keep(
        "Consecutive integers Deirdre is thinking of two consecutive integers whose product is 56.",
        factor,
        heading="Everyday Math",
        source_text="Factor Trinomials",
    )
    assert not keep(r"Multiply: $(x + 4)(x + 5)$.", factor, heading="Be Prepared 7.4", source_text="Factor Trinomials")

    quot = profile(
        "Quotient rule",
        "calc_diff_quotient_rule",
        [r"Find \frac{d}{dx}\left(\frac{x}{2x}\right)"],
    )
    assert keep(r"Find $h'(2)$ if $h(x) = \frac{f(x)}{g(x)}$.", quot, source_text="Differentiation Rules")
    assert not keep(r"$f(x) = x^{7} + 10$", quot, source_text="Differentiation Rules")

    chain = profile(
        "Chain rule",
        "calc_diff_chain_rule",
        [r"Find \frac{d}{dx}\left(\left(3x + 3\right)^{2}\right)"],
    )
    assert keep(r"$y = 3 u - 6 , u = 2 x^{2}$", chain, source_text="The Chain Rule")
    assert keep(r"$y = \sqrt{6 + \sec \pi x^{2}}$", chain, source_text="The Chain Rule")
    assert not keep(
        "The daily temperature in degrees Fahrenheit of Phoenix in the summer can be modeled by the function T(t).",
        chain,
        source_text="The Chain Rule",
    )

    graph = profile(
        "Graphing linear equations",
        "graphing_linear_equations",
        [r"Graph: y = 2x"],
    )
    assert keep(r"Graph $y = 2x + 3$", graph, source_text="Graph Linear Equations in Two Variables")
    assert not keep(r"$y = x^{2} + 3$", graph, source_text="Graphing Quadratic Equations")
    assert not keep(
        "A rancher is going to fence three sides of a corral next to a river.",
        graph,
        source_text="Graphing Quadratic Equations",
    )

    poly = profile(
        "Graphing polynomial functions",
        "a2_polynomial_functions_graphing",
        [r"Graph the following functions. y = x^2"],
    )
    assert keep(r"$f(x) = x^{3}(x - 1)^{3}(x + 2)$", poly, heading="Algebraic", source_text="Graphs of Polynomial Functions")
    assert not keep(
        "What is the difference between an x-intercept and a zero of a polynomial function?",
        poly,
        heading="Verbal",
        source_text="Graphs of Polynomial Functions",
    )

    rate = profile(
        "Constant rate equations",
        "g6_constant_rate_equations",
        [r"Julian drives at 2 miles per hour. Write an equation for the distance d after 6 hours."],
    )
    assert keep("A car is traveling down a road at a constant speed of 50 miles per hour.", rate, source_text="Two Related Quantities")
    assert not keep("Find a solution to each equation: 2^x = 8 and x^2 = 100.", rate, source_text="Two Related Quantities")

    div = profile(
        "Dividing fractions",
        "g6_dividing_fractions",
        [r"Divide. \frac{1}{12} \div \frac{1}{12}"],
    )
    assert keep(r"Find each quotient. a. 5 \div \frac{1}{10}", div, source_text="Dividing by Unit and Non-Unit Fractions")
    assert not keep(
        "It takes one week for a crew of workers to pave a road. At that rate, how long will it take?",
        div,
        source_text="Dividing by Unit and Non-Unit Fractions",
    )

    prove = profile(
        "Proving triangles congruent",
        "geo_congruent_proving_triangles_congruent",
        ["Two triangles have three pairs of corresponding congruent sides. Which congruence theorem proves the triangles congruent?"],
    )
    assert filename_score("HSG-CO.B_Are_the_Triangles_Congruent.pdf", prove) > 0
    assert filename_score("HSG-CO.D.12_Bisecting_an_angle.pdf", prove) == 0
    assert filename_score("HSG-CO.A.3_Seven_Circles_II.pdf", prove) == 0
    assert filename_score("HSA-CED.A.3_Dimes_and_Quarters.pdf", prove) == 0

    coins = profile(
        "Coin word problems",
        "coin_word_problems",
        ["Taylor has 10 coins in a pocket, all quarters and dimes. The coins are worth 1.90. How many quarters are there?"],
    )
    assert filename_score("HSA-CED.A.3_Dimes_and_Quarters.pdf", coins) > 0
    assert filename_score("HSG-MG.A_Coins_in_a_circular_pattern.pdf", coins) == 0
    ages = profile(
        "Age word problems",
        "age_word_problems",
        ["The father is 10 years older than his son. The sum of their ages is 36 years. How old is his son?"],
    )
    assert filename_score("HSF-IF.A.1_Your_Father.pdf", ages) == 0
    assert filename_score("7.SP.A.1_Mr_Briggs_s_Class_Likes_Math.pdf", coins) == 0

    extrema = profile(
        "Absolute extrema",
        "calc_app_diff_absolute_extrema",
        [r"Find the absolute extrema of f(x)=x^{2} on [0,3]."],
    )
    assert section_slug_score("4-3-maxima-and-minima", extrema) > 0
    assert section_slug_score("2-7-solve-absolute-value-inequalities", extrema) == 0
    assert section_slug_score("4-2-graph-linear-equations-in-two-variables", graph) > 0
    assert section_slug_score("10-5-graphing-quadratic-equations-in-two-variables", graph) == 0
    assert section_slug_score("1-3-add-and-subtract-integers", profile("Center and spread", "center_and_spread", ["Find the median of the data set."])) == 0

    rect_topic = {"name": "Rectangles with fraction side lengths", "type_id": "g6_rectangles_with_fraction_side_lengths"}
    rect_samples = [
        {
            "instruction_latex": r"\text{Find the area.}",
            "prompt_latex": r"\text{Find the area of the rectangle with base } \frac{11}{8}\text{ cm} \text{ and height } \frac{4}{3}\text{ cm}.",
            "error": None,
        }
    ]
    rect_cards = [
        {"text": "Find the unknown side length of the rectangle if its area is 11 m 2 . Check your answer by multiplying it by the given side length ( 3\\frac 23 )."},
        {"text": "A television screen has length 16\\frac12 inches, width w inches, and area 462 square inches. Select all equations that represent the relationship of the side lengths and area."},
        {"text": "The area of a rectangle is 17\\frac12 in 2 and its shorter side is 3\\frac12 in. What is the length of the longer side?"},
        {"text": "It takes 1 1/4 minutes to fill a 3-gallon bucket with a hose."},
    ]
    gap = in_topic_not_generated(rect_topic, rect_samples, rect_cards)
    assert "find the missing side given the area and one side" in gap["missing"], gap
    assert any("select equations" in item for item in gap["missing"]), gap
    assert "hose" not in gap["note"] and "gallon" not in gap["note"], gap["note"]
    assert any("find the area given both side lengths" in item for item in gap["generated"]), gap

    factor_gap = in_topic_not_generated(
        {"name": "Quadratic factoring", "type_id": "quadratic_factoring"},
        [{"instruction_latex": r"\text{Factor.}", "prompt_latex": r"x^{2} - 4", "error": None}],
        [{"text": r"63 . $x^{2} + 4 x + 3$"}],
    )
    assert factor_gap["missing"] == [], factor_gap

    abs_gap = in_topic_not_generated(
        {"name": "Absolute value equations", "type_id": "absolute_value_equations"},
        [{"instruction_latex": r"\text{Solve.}", "prompt_latex": r"\text{Solve: } \left|x - 1\right| = 2", "error": None}],
        [{"text": r"438 . $\left|\right. 2 x - 3 \left|\right. - 4 = 1$"}],
    )
    assert abs_gap["missing"] == [], abs_gap
    assert "none seen" in abs_gap["note"]
    cong = question_form(
        r"Prove the triangles are congruent. In right \triangle ABC and right \triangle DEF, "
        r"\overline{AC}\cong\overline{DF} (hypotenuses) and \overline{BC}\cong\overline{EF} (a leg). "
        r"Which congruence theorem applies?"
    )
    assert cong is not None and cong.ask == "prove", cong
    assert "right triangle" not in cong.label

    print("alignment skill gate: ok")
    print("rectangle kept", kept)
    print("hanger kept", hang_kept)


if __name__ == "__main__":
    main()
