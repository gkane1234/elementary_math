"""g6_introduction_to_percents is visual shade-the-figure, not percent-of formulas."""

from __future__ import annotations

import random
import re

from question_engine.diagrams.grade6_figures import (
    percent_bar_svg,
    percent_circle_svg,
    percent_grid_svg,
    percent_hundred_grid_svg,
    percent_multi_panel_svg,
)
from question_engine.frameworks.number import IntroductionToPercentsFramework
from question_engine.generators import GENERATORS


def test_percent_figure_svgs_blank_vs_shaded():
    for builder in (percent_hundred_grid_svg, percent_bar_svg, percent_circle_svg):
        blank = builder(37, blank=True)
        shaded = builder(37, blank=False)
        assert "<svg" in blank and "<svg" in shaded
        assert blank != shaded
        assert "#93c5fd" in shaded
        # Blank hundred-grid / bar / circle should not show the fill color as the
        # main shade (circle ticks use gray only).
        if builder is percent_hundred_grid_svg:
            assert blank.count("#93c5fd") == 0


def test_non_hundred_grid_and_multi_panel_svgs():
    blank = percent_grid_svg(40, blank=True, rows=5, cols=5)
    shaded = percent_grid_svg(40, blank=False, rows=5, cols=5)
    assert "5×5" in blank
    assert blank != shaded
    assert shaded.count("#93c5fd") == 10  # 40% of 25 cells

    panels = [
        {"figure": "circle", "percent": 37, "show_ticks": False, "label": "37%"},
        {"figure": "grid", "percent": 61, "rows": 7, "cols": 9, "label": "61%"},
    ]
    multi_blank = percent_multi_panel_svg(panels, blank=True)
    multi_shaded = percent_multi_panel_svg(panels, blank=False)
    assert "<svg" in multi_blank and multi_blank != multi_shaded
    assert "37%" in multi_blank and "61%" in multi_blank


def test_generator_wired_and_not_formula_percents():
    gen = GENERATORS["g6_introduction_to_percents"]
    qs = gen(
        "g6_introduction_to_percents",
        {"difficulty": 0, "count": 8, "seed": 3, "include_answer_key": True},
    )
    assert len(qs) == 8
    for q in qs:
        latex = q.prompt_latex or ""
        text = (q.prompt_text or "").lower()
        assert "Shade the figure to represent" in latex
        assert "what is" not in text
        assert "of what number" not in text
        assert "what percent of" not in text
        meta = q.metadata or {}
        assert meta.get("diagram_svg") and "<svg" in meta["diagram_svg"]
        assert meta.get("answer_diagram_svg") and "<svg" in meta["answer_diagram_svg"]
        assert (meta.get("diagram_spec") or {}).get("kind") == "percent_shade"
        assert (meta.get("stimulus") or {}).get("kind") == "percent_shade"
        pct = (meta.get("stimulus") or {}).get("percent")
        assert isinstance(pct, int) and 1 <= pct <= 100
        assert q.answer_latex == f"{pct}\\%"
        assert pct in {10, 25, 50, 75}
        assert (meta.get("stimulus") or {}).get("figure") == "hundred_grid"


def test_continuous_d_ladder_percent_pools():
    fw = IntroductionToPercentsFramework()
    easy_pcts: set[int] = set()
    mid_pcts: set[int] = set()
    mid_figures: set[str] = set()
    hard40_figures: set[str] = set()
    hard40_grids: set[tuple[int, int]] = set()
    extreme_modes: set[str] = set()
    extreme_figures: set[str] = set()

    for seed in range(40):
        random.seed(seed)
        _l, _t, _a = fw.build_prompt({"difficulty": 0})
        meta = fw.build_question_metadata(
            {"difficulty": 0}, prompt_latex=_l, prompt_text=_t, answer=_a
        )
        easy_pcts.add(int(meta["stimulus"]["percent"]))  # type: ignore[index]

    for seed in range(50):
        random.seed(seed + 100)
        _l, _t, _a = fw.build_prompt({"difficulty": 10})
        meta = fw.build_question_metadata(
            {"difficulty": 10}, prompt_latex=_l, prompt_text=_t, answer=_a
        )
        mid_pcts.add(int(meta["stimulus"]["percent"]))  # type: ignore[index]
        mid_figures.add(str(meta["stimulus"]["figure"]))  # type: ignore[index]

    for seed in range(60):
        random.seed(seed + 200)
        _l, _t, _a = fw.build_prompt({"difficulty": 40})
        meta = fw.build_question_metadata(
            {"difficulty": 40}, prompt_latex=_l, prompt_text=_t, answer=_a
        )
        stim = meta["stimulus"]  # type: ignore[index]
        hard40_figures.add(str(stim["figure"]))
        if stim.get("figure") == "grid":
            hard40_grids.add((int(stim["rows"]), int(stim["cols"])))

    for seed in range(40):
        random.seed(seed + 300)
        _l, _t, _a = fw.build_prompt({"difficulty": 1000})
        meta = fw.build_question_metadata(
            {"difficulty": 1000}, prompt_latex=_l, prompt_text=_t, answer=_a
        )
        stim = meta["stimulus"]  # type: ignore[index]
        extreme_figures.add(str(stim["figure"]))
        if stim.get("figure") == "multi":
            extreme_modes.add("multi")
            assert len(stim.get("percents") or []) >= 2
            assert "each figure" in (_l or "").lower() or "labeled" in (_l or "").lower()

    assert easy_pcts <= {10, 25, 50, 75}
    assert any(p % 5 != 0 for p in mid_pcts)
    assert mid_figures <= {"hundred_grid", "bar"}
    assert "grid" in hard40_figures
    assert any((r, c) != (10, 10) for r, c in hard40_grids)
    assert "multi" in extreme_modes
    assert extreme_figures == {"multi"}


def test_d1000_not_classroom_shade_awkward_single():
    """Extreme D must not look like a normal single shade-46% item."""
    gen = GENERATORS["g6_introduction_to_percents"]
    qs = gen(
        "g6_introduction_to_percents",
        {"difficulty": 1000, "count": 12, "seed": 77, "include_answer_key": True},
    )
    assert len(qs) == 12
    for q in qs:
        stim = (q.metadata or {}).get("stimulus") or {}
        assert stim.get("figure") == "multi"
        assert len(stim.get("percents") or []) >= 2
        assert "Shade each figure" in (q.prompt_latex or "")
        # Answer lists each panel percent — not a lone classroom item.
        assert ";\\," in (q.answer_latex or "") or ";" in (q.answer_latex or "")


def test_catalog_uses_dedicated_generator():
    from question_engine.core.registry import get_catalog_entry

    entry = get_catalog_entry("g6_introduction_to_percents")
    assert entry is not None
    assert entry.generator == "g6_introduction_to_percents"
    assert "shade" in (entry.instruction_text or "").lower()


def test_live_samples_across_d():
    gen = GENERATORS["g6_introduction_to_percents"]
    for d in (0, 5, 10, 20, 40, 1000):
        qs = gen(
            "g6_introduction_to_percents",
            {
                "difficulty": d,
                "count": 5,
                "seed": 40 + d,
                "include_answer_key": True,
            },
        )
        for q in qs:
            assert (q.metadata or {}).get("diagram_svg")
            stim = (q.metadata or {}).get("stimulus") or {}
            if d >= 1000:
                assert stim.get("figure") == "multi"
                continue
            m = re.search(r"(\d+)\\%", q.prompt_latex or "")
            assert m, q.prompt_latex
            pct = int(m.group(1))
            assert q.answer_latex == f"{pct}\\%"
