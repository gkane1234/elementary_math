"""Geometry / stats / variation / number-sets / graphing effort scorers.

Kept separate from ``effort.py`` to reduce merge contention. Registered via
``register_geo_stats_scorers`` from ``effort.py``.
"""

from __future__ import annotations

import re
from typing import Any, Callable

EffortScorer = Callable[[str, str], tuple[float, dict[str, Any]]]


def _clip(e: float) -> float:
    return round(min(max(e, 0.0), 25.0), 1)


def effort_classify_angles(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Acute / right / obtuse / straight classification from a diagram."""
    ans = (answer or "").lower()
    feats: dict[str, Any] = {"task": "classify"}
    e = 2.0
    if "straight" in ans:
        e = 3.5
        feats["class"] = "straight"
    elif "right" in ans:
        e = 2.5
        feats["class"] = "right"
    elif "obtuse" in ans:
        e = 3.0
        feats["class"] = "obtuse"
    else:
        feats["class"] = "acute"
    return _clip(e), feats


def effort_angle_measure(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Draw / read angle measures."""
    feats: dict[str, Any] = {"task": "measure"}
    e = 3.0
    m = re.search(r"(\d+)\s*\^?\\?circ", prompt) or re.search(r"(\d+)\s*°", prompt)
    if m:
        deg = int(m.group(1))
        feats["measure"] = deg
        if deg in {30, 45, 60, 90, 120, 180}:
            e = 2.5
        elif deg % 5 != 0:
            e = 5.0
        else:
            e = 3.5 + (1.0 if deg > 90 else 0.0)
    if "using the diagram" in prompt.lower() or "find" in prompt.lower():
        e += 1.0
        feats["from_diagram"] = True
    return _clip(e), feats


def effort_angle_relationships(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Complementary / supplementary / vertical unmarked measures."""
    p = prompt.lower()
    feats: dict[str, Any] = {}
    e = 4.0
    if "complementary" in p:
        feats["relation"] = "complementary"
        e = 4.0
    elif "supplementary" in p or "straight" in p:
        feats["relation"] = "supplementary"
        e = 4.5
    elif "vertical" in p:
        feats["relation"] = "vertical"
        e = 5.0
    else:
        feats["relation"] = "mixed"
        e = 5.5
    if re.search(r"\d+\s*x|x\s*[+\-]", prompt):
        e += 3.0
        feats["algebra"] = True
    return _clip(e), feats


def effort_angle_addition(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Angle addition postulate / multi-ray fans."""
    feats: dict[str, Any] = {"task": "angle_addition"}
    e = 5.0
    # Count angle names as a proxy for piece complexity.
    names = re.findall(r"\\angle\s*[A-Z]{2,3}|m\\angle", prompt)
    feats["angle_refs"] = len(names)
    e += 1.0 * max(0, len(names) - 1)
    if re.search(r"\d+\s*x|[a-z]\s*[+\-]", prompt):
        e += 2.5
        feats["algebra"] = True
    return _clip(e), feats


def effort_finding_angles(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Triangle sum / supplementary algebra for unknown angles."""
    p = prompt.lower()
    feats: dict[str, Any] = {}
    e = 5.0
    if "triangle" in p:
        feats["setting"] = "triangle"
        e = 6.0
    elif "supplementary" in p or "complementary" in p:
        feats["setting"] = "pair"
        e = 5.0
    else:
        feats["setting"] = "other"
    linear = len(re.findall(r"\([^)]*x[^)]*\)", prompt))
    feats["linear_exprs"] = linear
    e += 2.0 * max(0, linear - 1)
    if linear >= 3:
        e += 1.5
    return _clip(e), feats


def effort_sets_of_numbers(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Natural / whole / integer / rational / irrational / real classification."""
    feats: dict[str, Any] = {}
    e = 3.0
    if "which of the following" in prompt.lower():
        feats["mode"] = "pick"
        e = 4.0
    elif "true or false" in prompt.lower():
        feats["mode"] = "membership"
        e = 3.5
    else:
        feats["mode"] = "classify"
        e = 3.0
    if r"\sqrt" in prompt or "sqrt" in prompt.lower() or prompt.strip() in {"e", r"\pi", "pi"}:
        e += 2.0
        feats["irrational_present"] = True
    if r"\frac" in prompt or "/" in prompt:
        e += 1.0
        feats["fraction_present"] = True
    ans = answer or ""
    if "irrational" in ans.lower():
        e += 1.0
    if ans.count(",") >= 2:
        e += 0.5
        feats["multi_set"] = True
    return _clip(e), feats


def effort_variation(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Direct / inverse variation equation writing."""
    p = prompt.lower()
    feats: dict[str, Any] = {}
    e = 3.5
    if "inversely" in p or "inverse" in p:
        feats["kind"] = "inverse"
        e = 5.0
    else:
        feats["kind"] = "direct"
        e = 3.5
    if "when" in p and "varies" in p:
        e += 2.0
        feats["from_point"] = True
    if re.search(r"k\s*=", prompt):
        feats["given_k"] = True
    return _clip(e), feats


def effort_center_spread(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Mean / median / mode / range of a data set."""
    p = prompt.lower()
    feats: dict[str, Any] = {}
    e = 3.0
    if "mean" in p:
        feats["measure"] = "mean"
        e = 5.0
    elif "median" in p:
        feats["measure"] = "median"
        e = 4.0
    elif "mode" in p:
        feats["measure"] = "mode"
        e = 3.0
    elif "range" in p:
        feats["measure"] = "range"
        e = 2.5
    else:
        feats["measure"] = "other"
        e = 4.0
    nums = re.findall(r"\d+(?:\.\d+)?", prompt)
    # Exclude the measure word's incidental digits; count braced/list numbers.
    n = max(0, len(nums) - 0)
    # Heuristic: data lists are usually 5–12 numbers.
    if n >= 5:
        feats["n"] = n
        e += 0.4 * max(0, n - 5)
    if "." in (answer or ""):
        e += 1.0
        feats["non_integer"] = True
    return _clip(e), feats


def effort_box_plot_read(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Interpret five-number summary / IQR / range from a box plot."""
    p = prompt.lower()
    feats: dict[str, Any] = {}
    e = 3.0
    if "interquartile" in p or "iqr" in p:
        feats["ask"] = "iqr"
        e = 5.5
    elif "median" in p:
        feats["ask"] = "median"
        e = 3.5
    elif "range" in p:
        feats["ask"] = "range"
        e = 4.0
    elif "quartile" in p or "q1" in p or "q3" in p:
        feats["ask"] = "quartile"
        e = 4.5
    else:
        feats["ask"] = "other"
        e = 4.0
    if "draw" in p:
        e += 2.0
        feats["draw"] = True
    return _clip(e), feats


def effort_graph_linear(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Graph slope-intercept lines / linear inequalities."""
    feats: dict[str, Any] = {}
    e = 3.0
    p = prompt.replace(" ", "")
    if "\\ge" in prompt or "\\le" in prompt or ">=" in prompt or "<=" in prompt or "inequality" in prompt.lower():
        e += 2.0
        feats["inequality"] = True
    m = re.search(r"y\s*=\s*(-?\d*)\s*x", prompt) or re.search(r"y=(-?\d*)x", p)
    if m:
        coef = m.group(1)
        slope = int(coef) if coef not in {"", "+", "-"} else (1 if coef != "-" else -1)
        feats["slope"] = slope
        e += 0.5 * min(4, abs(slope))
    if re.search(r"[+\-]\s*\d+\s*$", prompt) or re.search(r"[+\-]\d+$", p):
        e += 0.5
        feats["intercept"] = True
    return _clip(e), feats


def effort_calc_tangent_line(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Tangent / normal line to a curve at a point."""
    feats: dict[str, Any] = {}
    e = 8.0
    if "normal" in prompt.lower():
        e += 2.0
        feats["normal"] = True
    else:
        feats["tangent"] = True
    if r"\sin" in prompt or r"\cos" in prompt:
        e += 3.0
        feats["trig"] = True
    if r"e^{" in prompt or r"\ln" in prompt:
        e += 3.5
        feats["exp_ln"] = True
    if r"\sqrt" in prompt:
        e += 2.5
        feats["radical"] = True
    if r"\frac" in prompt or "^{-" in prompt:
        e += 2.0
        feats["rational"] = True
    powers = [int(x) for x in re.findall(r"\^\{(\d+)\}", prompt)]
    if powers:
        e += 1.0 * max(0, max(powers) - 2)
        feats["max_power"] = max(powers)
    return _clip(e), feats


def effort_calc_related_rates(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    p = prompt.lower()
    feats: dict[str, Any] = {}
    e = 10.0
    if "elevation angle" in p or "angle of elevation" in p or "camera" in p:
        feats["shape"] = "angle"
        e = 19.0
    elif "bicycl" in p or "intersection" in p or "helicopter" in p or (
        "airplane a" in p and "airplane b" in p
    ):
        feats["shape"] = "two_rate"
        e = 18.0
    elif "shadow" in p or "lamp" in p:
        feats["shape"] = "shadow"
        e = 17.0
    elif "ladder" in p:
        feats["shape"] = "ladder"
        e = 16.0
    elif "gravel" in p or "conical tank" in p or "cone keeps" in p or "cone" in p:
        feats["shape"] = "cone"
        e = 15.0
    elif "balloon" in p or "sphere" in p:
        feats["shape"] = "sphere"
        e = 14.0
    else:
        feats["shape"] = "circle"
        e = 10.0
    return _clip(e), feats


def effort_calc_riemann(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    feats: dict[str, Any] = {"task": "riemann"}
    e = 8.0
    m = re.search(r"(\d+)\s*(?:equal intervals|intervals)", prompt)
    if m:
        n = int(m.group(1))
        feats["n"] = n
        e += 1.5 * max(0, n - 2)
    if "midpoint" in prompt.lower():
        e += 1.0
        feats["midpoint"] = True
    return _clip(e), feats


def effort_segment_addition(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Segment addition / midpoint / length on a line."""
    feats: dict[str, Any] = {"task": "segment"}
    e = 3.5
    nums = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", prompt)]
    feats["n_nums"] = len(nums)
    e += 0.4 * max(0, len(nums) - 2)
    if re.search(r"\d+\s*x|[a-z]\s*[+\-]", prompt):
        e += 2.5
        feats["algebra"] = True
    if "midpoint" in prompt.lower():
        e += 1.5
        feats["midpoint"] = True
    return _clip(e), feats


def effort_circle_measure(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Circumference / area / arc length / sector area."""
    p = prompt.lower()
    feats: dict[str, Any] = {}
    e = 4.0
    if "sector" in p:
        feats["ask"] = "sector"
        e = 7.0
    elif "arc length" in p or "length of the arc" in p:
        feats["ask"] = "arc_length"
        e = 6.5
    elif "circumference" in p:
        feats["ask"] = "circumference"
        e = 4.0
    elif "area" in p:
        feats["ask"] = "area"
        e = 5.0
    else:
        feats["ask"] = "other"
        e = 5.0
    if "diameter" in p:
        e += 0.5
        feats["given"] = "diameter"
    if "central angle" in p or re.search(r"\d+\s*\^?\\?circ", prompt):
        e += 1.0
    if r"\pi" in prompt or "pi" in p:
        feats["exact_pi"] = True
    return _clip(e), feats


def effort_circle_angles(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Central / inscribed / tangent–chord / secant angle measures."""
    p = prompt.lower()
    feats: dict[str, Any] = {}
    e = 5.0
    if "inscribed" in p:
        feats["kind"] = "inscribed"
        e = 6.5
    elif "tangent" in p and "secant" in p:
        feats["kind"] = "secant_tangent"
        e = 8.0
    elif "tangent" in p:
        feats["kind"] = "tangent"
        e = 7.0
    elif "central" in p or "arc" in p:
        feats["kind"] = "central_arc"
        e = 5.5
    else:
        feats["kind"] = "other"
    if re.search(r"\d+\s*x|[a-z]\s*[+\-]", prompt):
        e += 2.0
        feats["algebra"] = True
    return _clip(e), feats


def effort_circle_equation(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Write / use circle equations (x-h)^2+(y-k)^2=r^2."""
    feats: dict[str, Any] = {"task": "circle_eq"}
    e = 5.0
    if "write" in prompt.lower() or "equation" in prompt.lower():
        e = 6.0
    if re.search(r"center|radius", prompt.lower()):
        e += 0.5
    if re.search(r"[+\-]\s*\d+", prompt) and prompt.count("^") >= 2:
        e += 2.0
        feats["expanded_or_complete_square"] = True
    return _clip(e), feats


def effort_parallel_transversal(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Corresponding / alternate / consecutive angles with parallels."""
    p = prompt.lower()
    feats: dict[str, Any] = {}
    e = 5.0
    for key, bump in (
        ("corresponding", 0.0),
        ("alternate interior", 0.5),
        ("alternate exterior", 0.5),
        ("consecutive", 1.0),
        ("same-side", 1.0),
        ("co-interior", 1.0),
    ):
        if key in p:
            feats["relation"] = key
            e = 5.0 + bump
            break
    else:
        feats["relation"] = "generic"
        e = 5.5
    if re.search(r"\d+\s*x|[a-z]\s*[+\-]", prompt):
        e += 2.5
        feats["algebra"] = True
    return _clip(e), feats


def effort_coordinate_geo(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Distance / midpoint / slope / plot points on the plane."""
    p = prompt.lower()
    feats: dict[str, Any] = {}
    e = 4.0
    if "distance" in p:
        feats["ask"] = "distance"
        e = 5.5
    elif "midpoint" in p:
        feats["ask"] = "midpoint"
        e = 4.5
    elif "slope" in p:
        feats["ask"] = "slope"
        e = 4.0
    elif "plot" in p or "graph" in p or "coordinate" in p:
        feats["ask"] = "plot"
        e = 3.5
    else:
        feats["ask"] = "other"
    pts = re.findall(r"\(-?\d+\s*,\s*-?\d+\)", prompt)
    feats["n_points"] = len(pts)
    e += 0.5 * max(0, len(pts) - 2)
    if any("-" in (t or "") for t in pts):
        e += 0.5
        feats["neg_coords"] = True
    return _clip(e), feats


def effort_triangle_classify_sum(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Classify triangles / angle sum / exterior angle / isosceles."""
    p = prompt.lower()
    feats: dict[str, Any] = {}
    e = 4.0
    if "exterior" in p:
        feats["task"] = "exterior"
        e = 6.0
    elif "classify" in p:
        feats["task"] = "classify"
        e = 3.5
    elif "isosceles" in p or "equilateral" in p:
        feats["task"] = "special"
        e = 5.5
    elif "perimeter" in p:
        feats["task"] = "perimeter"
        e = 4.5
    elif "congruent" in p or "prove" in p:
        feats["task"] = "congruence"
        e = 8.0
    else:
        feats["task"] = "angle_sum"
        e = 5.0
    if re.search(r"\d+\s*x|[a-z]\s*[+\-]", prompt):
        e += 2.0
        feats["algebra"] = True
    return _clip(e), feats


def effort_triangle_properties(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Midsegment / median / altitude / bisector / inequality."""
    p = prompt.lower()
    feats: dict[str, Any] = {}
    e = 5.5
    for key, base in (
        ("midsegment", 5.0),
        ("centroid", 6.5),
        ("median", 6.0),
        ("altitude", 6.0),
        ("bisector", 6.5),
        ("inequality", 7.0),
    ):
        if key in p:
            feats["property"] = key
            e = base
            break
    else:
        feats["property"] = "other"
    if re.search(r"\d+\s*x|[a-z]\s*[+\-]", prompt):
        e += 2.0
        feats["algebra"] = True
    return _clip(e), feats


def effort_quad_classify_measure(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Classify quads / angle / side / diagonal properties."""
    p = prompt.lower()
    feats: dict[str, Any] = {}
    e = 4.0
    for name in (
        "rhombus",
        "kite",
        "trapezoid",
        "parallelogram",
        "rectangle",
        "square",
    ):
        if name in p:
            feats["figure"] = name
            break
    if "classify" in p:
        e = 3.5
        feats["task"] = "classify"
    elif "area" in p:
        e = 5.5
        feats["task"] = "area"
        if "regular" in p or "polygon" in p:
            e = 7.0
    elif "angle" in p:
        e = 5.0
        feats["task"] = "angles"
    else:
        feats["task"] = "property"
        e = 5.5
    if re.search(r"\d+\s*x|[a-z]\s*[+\-]", prompt):
        e += 2.0
        feats["algebra"] = True
    return _clip(e), feats


def effort_pythagorean(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Pythagorean theorem / multi-step / special right triangles."""
    p = prompt.lower()
    feats: dict[str, Any] = {}
    e = 5.0
    if "45" in prompt and "30" not in prompt:
        feats["kind"] = "45_45_90"
        e = 5.5
    elif "30" in prompt or "60" in prompt:
        feats["kind"] = "30_60_90"
        e = 6.5
    elif "multi" in p or "two right" in p or "diagram" in p:
        feats["kind"] = "multi_step"
        e = 8.0
    else:
        feats["kind"] = "basic"
        e = 5.0
    if r"\sqrt" in prompt or "sqrt" in p:
        e += 1.5
        feats["radical"] = True
    return _clip(e), feats


def effort_right_trig(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """SOH-CAH-TOA ratios / solve triangles / angle measures."""
    p = prompt.lower()
    feats: dict[str, Any] = {}
    e = 5.0
    if r"\sin" in prompt or "sin" in p:
        feats["fn"] = "sin"
    elif r"\cos" in prompt or "cos" in p:
        feats["fn"] = "cos"
    elif r"\tan" in prompt or "tan" in p:
        feats["fn"] = "tan"
        e += 0.5
    if "find the angle" in p or "measure" in p and "angle" in p:
        feats["ask"] = "angle"
        e = 6.5
    elif "solve" in p:
        feats["ask"] = "solve"
        e = 7.5
    else:
        feats["ask"] = "ratio"
        e = 5.0
    if r"\frac" in (answer or "") or "/" in (answer or ""):
        e += 0.5
    if "multi" in p or "word" in p:
        e += 2.0
    return _clip(e), feats


def effort_similarity(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Similar polygons / triangles / proportional parts."""
    p = prompt.lower()
    feats: dict[str, Any] = {}
    e = 5.5
    if "proportional" in p or "parallel" in p:
        feats["kind"] = "proportional_parts"
        e = 7.0
    elif "right" in p:
        feats["kind"] = "similar_right"
        e = 6.5
    elif "polygon" in p:
        feats["kind"] = "polygons"
        e = 5.5
    else:
        feats["kind"] = "triangles"
        e = 5.5
    if "word" in p:
        e += 1.5
    nums = re.findall(r"\d+(?:\.\d+)?", prompt)
    if len(nums) >= 4:
        e += 1.0
        feats["multi_lengths"] = True
    return _clip(e), feats


def effort_solid_volume_area(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Identify / compute volume or surface area of solids."""
    p = prompt.lower()
    feats: dict[str, Any] = {}
    e = 5.0
    for shape in ("sphere", "cone", "cylinder", "pyramid", "prism", "cube"):
        if shape in p:
            feats["shape"] = shape
            break
    if "surface" in p:
        feats["ask"] = "sa"
        e = 6.5
    elif "volume" in p:
        feats["ask"] = "volume"
        e = 5.5
    elif "similar" in p:
        feats["ask"] = "similar_solids"
        e = 7.5
    else:
        feats["ask"] = "identify"
        e = 4.0
    return _clip(e), feats


def effort_area_plane_figure(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """G6/PA/geo plane-figure area (parallelogram, triangle, trapezoid, kite)."""
    p = prompt.lower()
    feats: dict[str, Any] = {}
    e = 4.0
    for name, base in (
        ("trapezoid", 5.5),
        ("kite", 5.0),
        ("triangle", 4.5),
        ("parallelogram", 4.0),
        ("rhombus", 5.0),
        ("rectangle", 3.5),
        ("square", 3.0),
    ):
        if name in p:
            feats["figure"] = name
            e = base
            break
    if "understanding" in p or "formula" in p:
        e -= 0.5
        feats["concept"] = True
    if "perimeter" in p:
        e = max(3.0, e - 0.5)
        feats["ask"] = "perimeter"
    else:
        feats["ask"] = "area"
    return _clip(e), feats


def effort_decimal_ops(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Decimal + − × ÷ (place-value complexity via digit/decimal counts)."""
    feats: dict[str, Any] = {"task": "decimal"}
    e = 3.0
    p = prompt.replace(" ", "")
    if "/" in prompt or "\\div" in prompt or "÷" in prompt:
        feats["op"] = "div"
        e = 5.5
    elif "*" in p or "\\times" in prompt or "×" in prompt:
        feats["op"] = "mul"
        e = 5.0
    elif "-" in p and not p.startswith("-"):
        feats["op"] = "sub"
        e = 3.5
    else:
        feats["op"] = "add"
        e = 3.0
    decimals = re.findall(r"\d+\.\d+", prompt)
    feats["n_decimals"] = len(decimals)
    max_places = max((len(d.split(".")[1]) for d in decimals), default=0)
    feats["max_places"] = max_places
    e += 0.6 * max_places + 0.4 * max(0, len(decimals) - 1)
    if "diagram" in prompt.lower() or "area" in prompt.lower():
        e += 1.0
        feats["diagram"] = True
    return _clip(e), feats


def effort_abs_compare(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Absolute value evaluate / compare."""
    feats: dict[str, Any] = {}
    e = 3.0
    if "compar" in prompt.lower() or "<" in prompt or ">" in prompt:
        feats["task"] = "compare"
        e = 4.5
    else:
        feats["task"] = "evaluate"
        e = 3.0
    if prompt.count("|") >= 4 or prompt.count(r"\left|") >= 2:
        e += 1.5
        feats["multi"] = True
    if "-" in prompt:
        e += 0.5
    return _clip(e), feats


def effort_number_line_plot(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Plot / locate numbers on a number line."""
    feats: dict[str, Any] = {"task": "number_line"}
    e = 3.0
    if r"\frac" in prompt:
        e = 4.5
        feats["fraction"] = True
    elif "." in prompt:
        e = 3.5
        feats["decimal"] = True
    if "word" in prompt.lower():
        e += 1.5
        feats["word"] = True
    return _clip(e), feats


def effort_dot_histogram(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Interpret / draw dot plots and histograms."""
    p = prompt.lower()
    feats: dict[str, Any] = {}
    e = 4.0
    if "histogram" in p:
        feats["chart"] = "histogram"
        e = 5.0
    else:
        feats["chart"] = "dot"
        e = 4.0
    if "draw" in p or "create" in p:
        e += 1.5
        feats["draw"] = True
    if "how many" in p or "frequency" in p or "mode" in p:
        e += 0.5
    return _clip(e), feats


def effort_g6_expression(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Evaluate / combine like terms / simple algebraic expressions."""
    feats: dict[str, Any] = {}
    e = 3.5
    if "combin" in prompt.lower() or "like terms" in prompt.lower() or "simplify" in prompt.lower():
        feats["task"] = "like_terms"
        e = 4.5
    elif "evaluat" in prompt.lower() or "=" in prompt and "when" in prompt.lower():
        feats["task"] = "evaluate"
        e = 4.0
    else:
        feats["task"] = "expression"
        e = 3.5
    terms = len(re.findall(r"[+\-]", prompt))
    e += 0.4 * max(0, terms - 1)
    if r"\frac" in prompt:
        e += 1.5
    return _clip(e), feats


def effort_compare_order(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Compare / order integers, decimals, fractions."""
    feats: dict[str, Any] = {"task": "compare"}
    e = 3.0
    if "order" in prompt.lower() or "least" in prompt.lower() or "greatest" in prompt.lower():
        feats["task"] = "order"
        e = 4.5
    if r"\frac" in prompt:
        e += 1.5
        feats["fraction"] = True
    if "." in prompt:
        e += 0.5
        feats["decimal"] = True
    if "-" in prompt:
        e += 0.5
        feats["negative"] = True
    return _clip(e), feats


def effort_divisibility(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    feats: dict[str, Any] = {"task": "divisibility"}
    e = 2.5
    nums = [int(x) for x in re.findall(r"\d+", prompt)]
    if nums:
        feats["n"] = max(nums)
        e += min(4.0, 0.02 * max(nums))
    return _clip(e), feats


def effort_transformation(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    p = prompt.lower()
    feats: dict[str, Any] = {}
    e = 5.0
    if "dilat" in p:
        feats["kind"] = "dilation"
        e = 7.0
    elif "rotat" in p:
        feats["kind"] = "rotation"
        e = 6.5
    elif "reflect" in p:
        feats["kind"] = "reflection"
        e = 5.5
    else:
        feats["kind"] = "translation"
        e = 5.0
    pts = re.findall(r"\(-?\d+\s*,\s*-?\d+\)", prompt)
    e += 0.3 * max(0, len(pts) - 2)
    return _clip(e), feats


def effort_function_ops(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """(f±g)(a) / (fg)(a) / composition."""
    p = prompt.lower()
    feats: dict[str, Any] = {}
    e = 5.0
    if "circ" in p or r"\circ" in prompt or "(f \\circ" in prompt or "composition" in p:
        feats["op"] = "compose"
        e = 8.0
    elif "f - g" in p or "(f-g)" in p.replace(" ", ""):
        feats["op"] = "subtract"
        e = 6.0
    elif "f + g" in p or "(f+g)" in p.replace(" ", ""):
        feats["op"] = "add"
        e = 5.5
    elif "f \\cdot g" in prompt or "(fg)" in p.replace(" ", "") or "product" in p:
        feats["op"] = "multiply"
        e = 6.5
    else:
        feats["op"] = "other"
        e = 6.0
    if "x^{2}" in prompt or "x^2" in prompt:
        e += 1.5
        feats["quadratic"] = True
    return _clip(e), feats


def effort_scatter_plot(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Association label vs linear-model prediction from a scatter description."""
    p = prompt.lower()
    feats: dict[str, Any] = {}
    e = 3.5
    if "predict" in p or re.search(r"y\s*=", prompt):
        feats["task"] = "predict"
        e = 5.5
        nums = [abs(int(x)) for x in re.findall(r"-?\d+", prompt)]
        if nums:
            feats["max_coef"] = max(nums)
            e += 0.2 * max(0, feats["max_coef"] - 5)
    elif "association" in p or "trend" in p:
        feats["task"] = "association"
        e = 3.5
        if "no clear" in p or "none" in (answer or "").lower():
            e += 0.5
            feats["none"] = True
        elif "negative" in p:
            e += 0.3
    else:
        feats["task"] = "other"
        e = 4.0
    return _clip(e), feats


def effort_geo_notation(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Name segment / ray / line / angle from a basic diagram."""
    ans = (answer or "").lower()
    p = prompt.lower()
    feats: dict[str, Any] = {"task": "notation"}
    e = 2.0
    if "angle" in p or r"\angle" in (answer or "") or "angle" in ans:
        feats["object"] = "angle"
        e = 3.0
    elif "ray" in p or r"\overrightarrow" in (answer or ""):
        feats["object"] = "ray"
        e = 2.5
    elif "line" in p and "segment" not in p:
        feats["object"] = "line"
        e = 2.5
    else:
        feats["object"] = "segment"
        e = 2.0
    return _clip(e), feats


def effort_construction(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Identify compass-and-straightedge construction results from figure/prompt."""
    blob = f"{prompt} {answer}".lower()
    feats: dict[str, Any] = {"task": "construction"}
    ladder = (
        ("altitude", 7.0),
        ("median", 6.5),
        ("bisector", 6.0),
        ("congruent to the given triangle", 5.5),
        ("triangle congruent", 5.5),
        ("perpendicular", 4.5),
        ("circle", 5.0),
        ("congruent to the given angle", 4.5),
        ("angle congruent", 4.5),
        ("segment congruent", 3.5),
        ("congruent to the given segment", 3.5),
    )
    e = 4.0
    feats["kind"] = "other"
    for key, base in ladder:
        if key in blob:
            feats["kind"] = key.split()[0]
            e = base
            break
    if "compass" in blob or "straightedge" in blob:
        e += 1.5
        feats["tools_named"] = True
    if "fixed distance" in blob or "radius" in blob:
        e += 1.0
        feats["radius_cue"] = True
    nums = [abs(int(x)) for x in re.findall(r"-?\d+", prompt)]
    if nums and max(nums) >= 5:
        e += 0.5
        feats["measure"] = max(nums)
    return _clip(e), feats


def effort_g6_fraction_measure(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Area/volume with fractional side lengths (rect / triangle / prism)."""
    p = prompt.lower()
    feats: dict[str, Any] = {}
    e = 4.0
    if "prism" in p or "volume" in p:
        feats["shape"] = "prism"
        e = 6.5
    elif "triangle" in p:
        feats["shape"] = "triangle"
        e = 5.5
    elif "rectangle" in p:
        feats["shape"] = "rectangle"
        e = 4.5
    else:
        feats["shape"] = "other"
    fracs = re.findall(r"\\frac\{(\d+)\}\{(\d+)\}", prompt)
    feats["n_fracs"] = len(fracs)
    e += 1.2 * len(fracs)
    dens = [int(d) for _, d in fracs]
    if dens:
        feats["max_den"] = max(dens)
        e += 0.35 * max(0, feats["max_den"] - 2)
        if any(d not in {2, 3, 4, 5, 10} for d in dens):
            e += 1.0
            feats["awkward_den"] = True
    if not fracs:
        e = max(3.0, e - 2.0)
        feats["all_whole"] = True
    return _clip(e), feats


def effort_g6_grid_polygon(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Count unit squares for polygons / shaded regions on a grid."""
    p = prompt.lower()
    feats: dict[str, Any] = {}
    e = 4.0
    shaded = "shaded" in p
    if shaded:
        feats["shaded"] = True
        e += 1.0
    shape_bases = (
        ("l-shaped", 7.5),
        ("irregular", 7.0),
        ("trapezoid", 6.5),
        ("parallelogram", 5.5),
        ("triangle", 5.0),
        ("rectangle", 4.0),
        ("square", 3.5),
    )
    feats["shape"] = "polygon"
    for key, base in shape_bases:
        if key in p:
            feats["shape"] = key
            e = base + (1.0 if shaded else 0.0)
            break
    if r"\frac" in (answer or "") or "/2" in (answer or "").replace(" ", ""):
        e += 1.5
        feats["half_unit"] = True
    m = re.search(r"(\d+)", answer or "")
    if m:
        area_n = int(m.group(1))
        feats["area_num"] = area_n
        e += 0.15 * max(0, area_n - 6)
    return _clip(e), feats


def effort_g6_isometric(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Volume / surface area from an isometric rectangular-prism drawing."""
    p = prompt.lower()
    feats: dict[str, Any] = {}
    e = 5.0
    if "surface" in p:
        feats["ask"] = "surface_area"
        e = 7.0
    else:
        feats["ask"] = "volume"
        e = 5.0
    m = re.search(r"(\d+)", answer or "")
    if m:
        val = int(m.group(1))
        feats["value"] = val
        e += 0.12 * max(0, val - 8)
    return _clip(e), feats


GEO_STATS_SCORERS: dict[str, EffortScorer] = {
    # Geometry angles
    "geo_basics_classifying_angles": effort_classify_angles,
    "geo_basics_basic_angle_terminology": effort_classify_angles,
    "geo_basics_angles_and_their_measures": effort_angle_measure,
    "pa_drawing_and_measuring_angles": effort_angle_measure,
    "geo_basics_angle_relationships": effort_angle_relationships,
    "pa_angle_relationships": effort_angle_relationships,
    "geo_basics_angle_addition_postulate": effort_angle_addition,
    "finding_angles": effort_finding_angles,
    # Segments
    "geo_basics_line_segments_and_their_measures": effort_segment_addition,
    "geo_basics_segment_addition_postulate": effort_segment_addition,
    # Circles
    "geo_circles_circumference_and_area": effort_circle_measure,
    "geo_circles_arc_length_and_sector_area": effort_circle_measure,
    "pa_circles": effort_circle_measure,
    "a2_trigonometry_arc_length_and_sector_area": effort_circle_measure,
    "geo_circles_naming_arcs_and_central_angles": effort_circle_angles,
    "geo_circles_measures_of_arcs_and_central_angles": effort_circle_angles,
    "geo_circles_arcs_and_chords": effort_circle_angles,
    "geo_circles_inscribed_angles": effort_circle_angles,
    "geo_circles_tangents": effort_circle_angles,
    "geo_circles_secant_and_tangent_angles": effort_circle_angles,
    "geo_circles_segment_measures": effort_circle_angles,
    "geo_circles_using_equations_of_circles": effort_circle_equation,
    "geo_circles_writing_equations_of_circles": effort_circle_equation,
    # Parallel / coordinate
    "geo_parallel_parallel_lines_and_transversals": effort_parallel_transversal,
    "geo_parallel_points_of_the_coordinate_plane": effort_coordinate_geo,
    "geo_parallel_slope_and_lines": effort_coordinate_geo,
    "geo_parallel_distance_formula": effort_coordinate_geo,
    "geo_parallel_graphing_linear_equations": effort_graph_linear,
    "geo_parallel_writing_linear_equations": effort_graph_linear,
    "g6_points_on_the_coordinate_plane": effort_coordinate_geo,
    "g6_distances_on_the_coordinate_plane": effort_coordinate_geo,
    "g6_shapes_and_perimeter_on_the_coordinate_plane": effort_coordinate_geo,
    "g6_coordinate_plane_distances_word_problems": effort_coordinate_geo,
    "pa_plotting_points": effort_coordinate_geo,
    # Triangles / congruence / properties
    "geo_congruent_classifying_triangles": effort_triangle_classify_sum,
    "geo_congruent_triangle_angle_sum": effort_triangle_classify_sum,
    "geo_congruent_triangle_perimeter": effort_triangle_classify_sum,
    "geo_congruent_exterior_angle_theorem": effort_triangle_classify_sum,
    "geo_congruent_isosceles_and_equilateral_triangles": effort_triangle_classify_sum,
    "geo_congruent_triangles_and_congruence": effort_triangle_classify_sum,
    "geo_congruent_proving_triangles_congruent": effort_triangle_classify_sum,
    "geo_properties_midsegment": effort_triangle_properties,
    "geo_properties_angle_bisectors": effort_triangle_properties,
    "geo_properties_medians": effort_triangle_properties,
    "geo_properties_centroid": effort_triangle_properties,
    "geo_properties_triangle_inequality_theorem": effort_triangle_properties,
    "geo_properties_inequalities_in_one_triangle": effort_triangle_properties,
    # Quads / area
    "geo_quadrilaterals_classifying": effort_quad_classify_measure,
    "geo_quadrilaterals_angles": effort_quad_classify_measure,
    "geo_quadrilaterals_parallelograms": effort_quad_classify_measure,
    "geo_quadrilaterals_trapezoids": effort_quad_classify_measure,
    "geo_quadrilaterals_rhombuses": effort_quad_classify_measure,
    "geo_quadrilaterals_kites": effort_quad_classify_measure,
    "geo_quadrilaterals_area_of_triangles_and_quadrilaterals": effort_quad_classify_measure,
    "geo_quadrilaterals_polygon_basics": effort_quad_classify_measure,
    "geo_quadrilaterals_area_of_regular_polygons": effort_quad_classify_measure,
    "pa_quadrilaterals": effort_quad_classify_measure,
    "pa_area_of_triangles_and_quadrilaterals": effort_area_plane_figure,
    "pa_plane_figures_triangles": effort_area_plane_figure,
    "g6_parallelograms": effort_area_plane_figure,
    "g6_parallelograms_understanding_area_formula": effort_area_plane_figure,
    "g6_triangles": effort_area_plane_figure,
    "g6_triangles_understanding_area_formula": effort_area_plane_figure,
    "g6_trapezoids": effort_area_plane_figure,
    "g6_kites": effort_area_plane_figure,
    # Right triangle / trig / similarity
    "geo_right_pythagorean_theorem": effort_pythagorean,
    "geo_right_multi_step_pythagorean_theorem_problems": effort_pythagorean,
    "geo_right_special_right_triangles": effort_pythagorean,
    "geo_right_multi_step_special_right_triangle_problems": effort_pythagorean,
    "pythagorean_theorem": effort_pythagorean,
    "geo_trig_finding_trig_ratios": effort_right_trig,
    "geo_trig_finding_angle_measures": effort_right_trig,
    "geo_trig_solving_right_triangles": effort_right_trig,
    "geo_trig_multi_step_trig_problems": effort_right_trig,
    "geo_trig_rhombuses_and_kites_with_right_triangles": effort_right_trig,
    "geo_trig_trigonometry_and_area": effort_right_trig,
    "a2_trigonometry_right_triangle_trig_finding_ratios": effort_right_trig,
    "a2_trigonometry_right_triangle_trig_finding_angle_measures": effort_right_trig,
    "a2_trigonometry_right_triangle_trig_angles_and_sides": effort_right_trig,
    "geo_similarity_similar_polygons": effort_similarity,
    "geo_similarity_similar_triangles": effort_similarity,
    "geo_similarity_similar_right_triangles": effort_similarity,
    "geo_similarity_proportional_parts_in_triangles_and_parallel_lines": effort_similarity,
    "pa_similar_figures": effort_similarity,
    "pa_similar_figures_word_problems": effort_similarity,
    # Solids
    "geo_solid_figures_identifying_volume_and_area": effort_solid_volume_area,
    "geo_similar_solids": effort_solid_volume_area,
    "pa_classifying_volume_and_surface_area": effort_solid_volume_area,
    "g6_formulas_for_volume_and_surface_area_of_a_cube": effort_solid_volume_area,
    # Number sets / variation
    "sets_of_numbers": effort_sets_of_numbers,
    "direct_inverse_variation": effort_variation,
    "a2_direct_and_inverse_variation_direct_and_inverse_variation": effort_variation,
    # Stats charts
    "center_and_spread": effort_center_spread,
    "g6_data_center_and_spread": effort_center_spread,
    "g6_interpreting_box_plots": effort_box_plot_read,
    "g6_drawing_box_plots": effort_box_plot_read,
    "g6_interpreting_dot_plots": effort_dot_histogram,
    "g6_drawing_dot_plots": effort_dot_histogram,
    "g6_interpreting_histograms": effort_dot_histogram,
    "g6_drawing_histograms": effort_dot_histogram,
    # Graphing (parseable slope-intercept stems)
    "graphing_linear_equations": effort_graph_linear,
    "graphing_linear_inequalities": effort_graph_linear,
    "a2_linear_relations_and_functions_graphing_linear_equations": effort_graph_linear,
    "a2_linear_relations_and_functions_graphing_linear_inequalities": effort_graph_linear,
    # Calc sketch-backed leaves
    "calc_app_diff_slope_tangent_and_normal_lines": effort_calc_tangent_line,
    "calc_app_diff_related_rates": effort_calc_related_rates,
    "calc_def_int_approximating_area_under_a_curve": effort_calc_riemann,
    # G6 number / expression
    "g6_decimal_addition": effort_decimal_ops,
    "g6_decimal_subtraction": effort_decimal_ops,
    "g6_decimal_multiplication": effort_decimal_ops,
    "g6_decimal_addition_with_diagrams": effort_decimal_ops,
    "g6_decimal_subtraction_with_diagrams": effort_decimal_ops,
    "g6_decimal_multiplication_with_area_diagrams": effort_decimal_ops,
    "g6_decimal_multiplication_with_equivalent_fractions": effort_decimal_ops,
    "g6_dividing_decimals_by_decimals": effort_decimal_ops,
    "g6_dividing_decimals_by_whole_numbers": effort_decimal_ops,
    "g6_dividing_whole_numbers_by_decimals": effort_decimal_ops,
    "g6_dividing_whole_numbers_that_result_in_decimals": effort_decimal_ops,
    "g6_long_division_with_remainders": effort_decimal_ops,
    "g6_absolute_values": effort_abs_compare,
    "g6_comparing_with_absolute_values": effort_abs_compare,
    "g6_numbers_on_a_number_line": effort_number_line_plot,
    "g6_number_line_word_problems": effort_number_line_plot,
    "g6_evaluating_algebraic_expressions": effort_g6_expression,
    "g6_combining_like_terms": effort_g6_expression,
    "g6_distributive_property_algebraic": effort_g6_expression,
    "g6_distributive_property_area_diagrams_numeric": effort_g6_expression,
    "g6_distributive_property_area_diagrams_algebraic": effort_g6_expression,
    "g6_writing_numeric_expressions": effort_g6_expression,
    "g6_numeric_expressions_with_exponents": effort_g6_expression,
    "g6_comparing_numbers": effort_compare_order,
    "g6_ordering_numbers": effort_compare_order,
    "g6_ordering_with_absolute_values": effort_compare_order,
    "g6_opposites_of_numbers": effort_abs_compare,
    "g6_classifying_and_naming": effort_compare_order,
    "pa_divisibility": effort_divisibility,
    "pa_transformations": effort_transformation,
    "geo_transformations_translations_rotations_reflections_and_dilations": effort_transformation,
    "a2_general_functions_operations": effort_function_ops,
    "pc_functions_operations": effort_function_ops,
    # A1 leftovers / visualizing / scatter
    "scatter_plots": effort_scatter_plot,
    "visualizing_data": effort_dot_histogram,
    # Geo constructions + notation
    "geo_basics_geometric_diagrams_and_notation": effort_geo_notation,
    "geo_constructions_line_segments": effort_construction,
    "geo_constructions_perpendicular_segments": effort_construction,
    "geo_constructions_angles": effort_construction,
    "geo_constructions_triangles": effort_construction,
    "geo_constructions_medians_of_a_triangle": effort_construction,
    "geo_constructions_altitudes_of_a_triangle": effort_construction,
    "geo_constructions_angle_bisectors": effort_construction,
    "geo_constructions_circles": effort_construction,
    # G6 fraction solids / grid / isometric
    "g6_rectangles_with_fraction_side_lengths": effort_g6_fraction_measure,
    "g6_triangles_with_fraction_side_lengths": effort_g6_fraction_measure,
    "g6_right_rectangular_prisms_with_fraction_side_lengths": effort_g6_fraction_measure,
    "g6_polygons_on_a_grid_or_coordinate_plane": effort_g6_grid_polygon,
    "g6_polygons_and_shaded_regions": effort_g6_grid_polygon,
    "g6_volume_and_surface_area_using_isometric_drawings": effort_g6_isometric,
}


def register_geo_stats_scorers(register: Callable[[str, EffortScorer], None]) -> None:
    for type_id, scorer in GEO_STATS_SCORERS.items():
        register(type_id, scorer)
