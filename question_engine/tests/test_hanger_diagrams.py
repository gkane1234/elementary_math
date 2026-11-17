"""Hanger diagrams are vertical balance mobiles, not a row of blocks."""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET

from question_engine.api.handler import _generate_for_type
from question_engine.diagrams.grade6_figures import hanger_svg

_NS = "http://www.w3.org/2000/svg"


def _root(svg: str) -> ET.Element:
    return ET.fromstring(svg)


def _view_box(root: ET.Element) -> tuple[float, float]:
    box = root.attrib["viewBox"].split()
    return float(box[2]), float(box[3])


def _rects(root: ET.Element, kind: str) -> list[dict[str, float]]:
    found = []
    for node in root.findall(f".//{{{_NS}}}rect"):
        if node.attrib.get("data-kind") != kind:
            continue
        found.append(
            {
                "x": float(node.attrib["x"]),
                "y": float(node.attrib["y"]),
                "w": float(node.attrib["width"]),
                "h": float(node.attrib["height"]),
            }
        )
    return found


def _texts(root: ET.Element, kind: str) -> list[str]:
    return [
        (node.text or "").strip()
        for node in root.findall(f".//{{{_NS}}}text")
        if node.attrib.get("data-kind") == kind
    ]


def _lines(root: ET.Element, cls: str) -> list[dict[str, float]]:
    found = []
    for node in root.findall(f".//{{{_NS}}}line"):
        if node.attrib.get("class") != cls:
            continue
        found.append(
            {
                "x1": float(node.attrib["x1"]),
                "y1": float(node.attrib["y1"]),
                "x2": float(node.attrib["x2"]),
                "y2": float(node.attrib["y2"]),
                "side": node.attrib.get("data-side", ""),
            }
        )
    return found


def _overlaps(a: dict[str, float], b: dict[str, float]) -> bool:
    return not (
        a["x"] + a["w"] <= b["x"] + 0.5
        or b["x"] + b["w"] <= a["x"] + 0.5
        or a["y"] + a["h"] <= b["y"] + 0.5
        or b["y"] + b["h"] <= a["y"] + 0.5
    )


def test_equation_hanger_is_a_vertical_chain():
    svg = hanger_svg(3, 15)
    assert "x blocks" not in svg
    root = _root(svg)
    width, height = _view_box(root)
    squares = _rects(root, "x")
    totals = _rects(root, "total")
    assert len(squares) == 3
    assert len(totals) == 1
    assert _texts(root, "x") == ["x", "x", "x"]
    assert _texts(root, "total") == ["15"]

    xs = {round(sq["x"], 1) for sq in squares}
    assert len(xs) == 1
    ys = [sq["y"] for sq in squares]
    assert ys == sorted(ys)
    assert ys[1] - ys[0] >= squares[0]["h"]
    assert all(abs(sq["w"] - sq["h"]) < 0.2 for sq in squares)

    total = totals[0]
    assert total["x"] > squares[0]["x"] + squares[0]["w"]
    assert not _overlaps(squares[-1], total)
    assert total["h"] > squares[0]["h"]

    beam = _lines(root, "hanger-beam")
    hook = _lines(root, "hanger-hook")
    strings = _lines(root, "hanger-string")
    links = _lines(root, "hanger-link")
    assert len(beam) == 1 and len(hook) == 1
    assert abs(beam[0]["y1"] - beam[0]["y2"]) < 0.2
    assert abs(hook[0]["x1"] - hook[0]["x2"]) < 0.2
    assert hook[0]["y1"] < hook[0]["y2"] - 8
    mid_x = (beam[0]["x1"] + beam[0]["x2"]) / 2
    mid_y = (beam[0]["y1"] + beam[0]["y2"]) / 2
    assert abs(hook[0]["x2"] - mid_x) < 0.6
    assert abs(hook[0]["y2"] - mid_y) < 0.6
    assert len(strings) == 2
    assert all(abs(seg["x1"] - seg["x2"]) < 0.2 for seg in strings)
    assert len(links) == 2
    assert all(abs(seg["x1"] - seg["x2"]) < 0.2 for seg in links)

    left = next(seg for seg in strings if seg["side"] == "left")
    right = next(seg for seg in strings if seg["side"] == "right")
    assert abs(left["x1"] - (squares[0]["x"] + squares[0]["w"] / 2)) < 0.6
    assert abs(left["y2"] - squares[0]["y"]) < 0.6
    assert abs(right["x1"] - (total["x"] + total["w"] / 2)) < 0.6
    assert abs(right["y2"] - total["y"]) < 0.6
    assert abs(left["y1"] - right["y1"]) < 0.6

    for node in list(root.iter()):
        for key in ("x", "y", "x1", "y1", "x2", "y2"):
            if key in node.attrib and node.attrib[key].replace(".", "", 1).isdigit():
                value = float(node.attrib[key])
                limit = width if key.startswith("x") else height
                assert -0.5 <= value <= limit + 0.5


def test_many_squares_stay_in_one_column():
    svg = hanger_svg(9, 153)
    root = _root(svg)
    squares = _rects(root, "x")
    total = _rects(root, "total")[0]
    assert len(squares) == 9
    assert _texts(root, "total") == ["153"]
    assert len({round(sq["x"], 1) for sq in squares}) == 1
    assert all(not _overlaps(sq, total) for sq in squares)
    assert squares[0]["x"] + squares[0]["w"] < total["x"]


def test_inequality_lowers_the_greater_side():
    le = _root(hanger_svg(3, 15, inequality=True, relation="\\le"))
    ge = _root(hanger_svg(4, 32, inequality=True, relation="\\ge"))
    le_beam = _lines(le, "hanger-beam")[0]
    ge_beam = _lines(ge, "hanger-beam")[0]
    # Beam is drawn left to right. Positive slope in SVG lowers the right end.
    assert le_beam["x2"] > le_beam["x1"]
    assert le_beam["y2"] > le_beam["y1"] + 8
    assert ge_beam["y1"] > ge_beam["y2"] + 8

    le_strings = _lines(le, "hanger-string")
    left = next(seg for seg in le_strings if seg["side"] == "left")
    right = next(seg for seg in le_strings if seg["side"] == "right")
    assert right["y1"] > left["y1"] + 8
    assert abs(left["x1"] - left["x2"]) < 0.2
    assert abs(right["x1"] - right["x2"]) < 0.2
    # Weights still hang straight down, under the lowered end.
    squares = _rects(le, "x")
    total = _rects(le, "total")[0]
    assert total["y"] > squares[0]["y"] + 8


def test_live_hanger_questions_match_the_diagram():
    eq = _generate_for_type(
        "g6_equations_hanger_diagrams",
        {
            "difficulty": 0,
            "seed": 101,
            "count": 1,
            "include_answer_key": True,
        },
    )[0]
    assert eq.prompt_latex
    match = re.search(r"(\d+)x\s*=\s*(\d+)", eq.prompt_latex)
    assert match, eq.prompt_latex
    parts, total = int(match.group(1)), int(match.group(2))
    root = _root(eq.metadata["diagram_svg"])
    assert len(_rects(root, "x")) == parts
    assert _texts(root, "total") == [str(total)]
    beam = _lines(root, "hanger-beam")[0]
    assert abs(beam["y1"] - beam["y2"]) < 0.2
    assert "x blocks" not in eq.metadata["diagram_svg"]

    ineq = _generate_for_type(
        "g6_inequalities_hanger_diagrams",
        {
            "difficulty": 22,
            "seed": 101,
            "count": 1,
            "include_answer_key": True,
        },
    )[0]
    imatch = re.search(r"(\d+)x\s*(\\le|\\ge)\s*(\d+)", ineq.prompt_latex or "")
    assert imatch, ineq.prompt_latex
    iroot = _root(ineq.metadata["diagram_svg"])
    assert len(_rects(iroot, "x")) == int(imatch.group(1))
    assert _texts(iroot, "total") == [imatch.group(3)]
    ibeam = _lines(iroot, "hanger-beam")[0]
    if imatch.group(2) == "\\le":
        assert ibeam["y2"] > ibeam["y1"] + 8
    else:
        assert ibeam["y1"] > ibeam["y2"] + 8
