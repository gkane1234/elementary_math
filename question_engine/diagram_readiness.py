"""Types that must not show as curriculum-picker Ready until diagrams render.

Keep this set minimal: only types whose student experience still lacks a
usable rendered figure (or still uses a wrong stand-in).
"""

from __future__ import annotations

REQUIRES_DIAGRAM_TYPE_IDS: frozenset[str] = frozenset(
    {
        # Grade 6 decimal / percent “with diagrams” topics still lack true
        # place-value / area / percent-bar models (wired stand-ins are plain
        # arithmetic).
        "g6_decimal_addition_with_diagrams",
        "g6_decimal_subtraction_with_diagrams",
        "g6_decimal_multiplication_with_area_diagrams",
        "g6_solving_percent_problems_with_diagrams",
        # Box-plot “drawing” still uses the interpret-basics stand-in.
        "g6_drawing_box_plots",
        "scatter_plots",
        # Tip-to-tail vector diagram UI.
        "pc_vectors_diagrams",
        # Composite rhombus/kite + right-triangle figure not yet composed.
        "geo_trig_rhombuses_and_kites_with_right_triangles",
        # Need interactive sketch / multi-graph comparison UI.
        "calc_app_diff_curve_sketching",
        "calc_app_diff_graphical_comparison_of_f_f_prime_and_f_double_prime",
    }
)


def type_requires_diagram(type_id: str) -> bool:
    return type_id in REQUIRES_DIAGRAM_TYPE_IDS
