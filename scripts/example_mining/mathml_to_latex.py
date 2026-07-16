"""MathML → LaTeX via the `mathml-to-latex` package (with OpenStax cleanup).

OpenStax pages embed Presentation MathML plus Content MathML annotations.
We strip annotations before converting, then apply light post-cleanup for
common OpenStax fencing / lim patterns.
"""

from __future__ import annotations

import re

from bs4 import BeautifulSoup
from mathml_to_latex.converter import MathMLToLaTeX

_CONVERTER = MathMLToLaTeX()

# OpenStax often encodes f(x) as mo+mi+mo with empty \left(\right. wrappers.
_FENCE_FUNC = re.compile(
    r"\\left\(\s*\\right\.\s*([^\\{}]+?)\s*\\left\.\s*\\right\)"
)
_LIM_UNDERSET = re.compile(
    r"\\underset\{([^}]+)\}\{\\text\{lim\}\}"
)
_ABS_FENCE = re.compile(
    r"\\left\|\s*\\right\.\s*(.*?)\s*\\left\.\s*\\right\|"
)


def _presentation_only(mathml: str) -> str:
    soup = BeautifulSoup(mathml, "html.parser")
    math = soup.find("math")
    if math is None:
        return mathml.strip()
    for ann in math.select("annotation, annotation-xml"):
        ann.decompose()
    for sem in list(math.select("semantics")):
        sem.unwrap()
    return str(math)


def _cleanup_latex(latex: str) -> str:
    s = latex
    s = _LIM_UNDERSET.sub(r"\\lim_{\1}", s)
    s = _FENCE_FUNC.sub(r"(\1)", s)
    s = _ABS_FENCE.sub(r"\\left|\1\\right|", s)
    s = s.replace(r"\rightarrow", r"\to")
    for name in ("sin", "cos", "tan", "sec", "csc", "cot", "ln", "log", "exp"):
        s = s.replace(rf"\text{{{name}}}", rf"\{name}")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def mathml_to_latex(mathml: str) -> str:
    """Convert a <math>…</math> fragment to LaTeX."""
    cleaned = mathml.strip()
    if not cleaned:
        return ""
    try:
        presentation = _presentation_only(cleaned)
        raw = _CONVERTER.convert(presentation)
    except Exception:
        return ""
    return _cleanup_latex(raw)
