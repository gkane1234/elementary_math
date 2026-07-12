"""Deferred Coming-soon types (intentionally not Ready).



These remain demoted after this session because they need Tier-3 UI or

true specialized models — not because they are forgotten scaffolds.

"""



DEFERRED = [

    (

        "g6_decimal_*_with_diagrams / area models",

        "Math is now decimal arithmetic (not fraction stand-ins); true place-value/area diagram UI still deferred.",

    ),

    (

        "scatter_plots",

        "Association/prediction text questions Ready; interactive scatter SVG still deferred.",

    ),

    (

        "g6_isometric_sketching / volume with isometric drawings",

        "Needs isometric drawing surface.",

    ),

    (

        "pc_vectors_diagrams",

        "Needs tip-to-tail vector diagram composition.",

    ),

    (

        "geo_trig_rhombuses_and_kites_with_right_triangles",

        "Needs composite rhombus/kite + right-triangle figure.",

    ),

    (

        "calc_app_diff_curve_sketching",

        "Needs interactive curve-sketching UI (critical points / asymptotes / sign charts).",

    ),

    (

        "calc_app_diff_graphical_comparison_of_f_f_prime_and_f_double_prime",

        "Needs multi-graph comparison UI for f / f' / f''.",

    ),

]



# Remaining thin calculus_foundations / precalc_foundations topics that are

# still Ready but only lightly covered (not wrong-topic). Polish later.

FOUNDATIONS_THIN = [

    (

        "calc_diff_instantaneous_rates_of_change / inverse_functions / "

        "slope_tangent / concavity / extrema / optimization / motion / "

        "differentials / newton / log-exp substitution / trig-with-sub / "

        "diff_eq_introduction / motion revisited",

        "Still on calculus_foundations with correct but thin single-pattern prompts.",

    ),

    (

        "pc_continuity / extrema / piecewise / power / parametric / projectile / "

        "induction / power_series / multivariable / partial fractions / "

        "rational & polynomial inequalities / limits at kinks/essential",

        "Still on precalc_foundations; topic-matched but shallow EMH diversity.",

    ),

]



# Polynomial / quadratic QA follow-ups (resolved this pass).

# Evidence: scripts/output/POLY_QUAD_QA.md

POLY_QUAD_RESOLVED = [

    (

        "polynomial_factoring_grouping non-monic leading",

        "Fixed: _generate_grouping uses _leading_coefficient so medium/hard a≠1.",

    ),

    (

        "quadratic_formula unreduced radical answers",

        "Fixed: content-reduces (-b ± c√d)/(2a) by gcd(|b|,|c|,|2a|).",

    ),

]



# Plane inequality shading — implemented (not deferred).

PLANE_SHADE_NOTE = (

    "graphing_linear_inequalities / graphing_systems_of_inequalities now emit "

    "GraphSpec.regions half_plane overlays; QuestionGraph + render_graph_svg shade them. "

    "Systems use overlapping translucent half-planes (not computed intersection polygons)."

)


