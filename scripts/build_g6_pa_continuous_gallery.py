"""HTML gallery for G6/PA number-lane continuous-difficulty topics.

Samples 5 questions at D ∈ {0, 5, 10, 20, 40} plus 1 extreme sample at
D = 1000 (unreasonable / unbounded scaling) via the worksheet generate
settings path. Output:

  scripts/output/topic_fit/g6_pa_continuous/gallery.html

Usage:
  $env:PYTHONPATH='.'
  python scripts/build_g6_pa_continuous_gallery.py
"""

from __future__ import annotations

import html
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import question_engine.types  # noqa: F401
from question_engine.api.handler import _resolve_generation_settings
from question_engine.core.base import QUESTION_TYPES
from question_engine.generators import GENERATORS

OUT = ROOT / "scripts" / "output" / "topic_fit" / "g6_pa_continuous"
# Classroom ladder + one extreme unbounded sample.
DIFFS = (0, 5, 10, 20, 40)
EXTREME_D = 1000
N = 5
N_EXTREME = 1

# Topics where D=1000 escalates structure (not raw magnitude) — annotate in gallery.
STRUCTURAL_EXTREME_NOTES: dict[str, str] = {
    "g6_introduction_to_percents": (
        "Shade-% plateaus as a skill; extreme D escalates structure "
        "(multi-panel + non-100 / hostile figures), not a harder single classroom shade-%."
    ),
}

# Continuous-D number-lane topics from this pass (+ related OOO leaves).
# Skips geometry-diagram / stats-viz / Tier-3 diagram UX topics.
TOPICS: tuple[tuple[str, str], ...] = (
    # Near-zero OOO alias + sibling already on continuous OOO
    ("g6_numeric_expressions_with_exponents", "Numeric expressions with exponents"),
    ("g6_numeric_expressions_and_order_of_operations", "Numeric expressions / order of operations"),
    # Ratios / rates
    ("g6_introduction_to_ratios", "Introduction to ratios"),
    ("g6_equivalent_ratios", "Equivalent ratios"),
    ("g6_part_part_whole_ratios", "Part-part-whole ratios"),
    ("g6_comparing_ratios", "Comparing ratios"),
    ("g6_unit_rates_and_equivalent_rates", "Unit rates and equivalent rates"),
    ("g6_comparing_rates", "Comparing rates"),
    ("g6_converting_units", "Converting units"),
    # Percents / FDP
    ("g6_introduction_to_percents", "Introduction to percents"),
    ("g6_relating_percents_fractions_and_decimals", "Relating percents, fractions, decimals"),
    ("g6_finding_percents_with_equivalent_fractions", "Finding percents with equivalent fractions"),
    ("g6_solving_percent_problems_with_formulas", "Solving percent problems with formulas"),
    ("pa_fractions_decimals_and_percents", "Fractions, decimals, and percents"),
    ("pa_converting_fractions_and_decimals", "Converting fractions and decimals"),
    ("pa_simplifying_fractions", "Simplifying fractions"),
    # Fraction ops (word-problem aliases disabled from curriculum picker)
    ("g6_dividing_fractions", "Dividing fractions"),
    # Decimals / division
    ("g6_decimal_addition", "Decimal addition"),
    ("g6_decimal_subtraction", "Decimal subtraction"),
    ("g6_decimal_multiplication", "Decimal multiplication"),
    ("g6_long_division_with_remainders", "Long division with remainders"),
    ("g6_dividing_whole_numbers_that_result_in_decimals", "Whole ÷ whole → decimal"),
    ("g6_dividing_decimals_by_whole_numbers", "Dividing decimals by whole numbers"),
    ("g6_dividing_whole_numbers_by_decimals", "Dividing whole numbers by decimals"),
    ("g6_dividing_decimals_by_decimals", "Dividing decimals by decimals"),
    ("pa_naming_decimal_places_and_rounding", "Place value and rounding"),
    # Factors / integers / abs / order
    ("g6_factoring", "Prime factorization"),
    ("pa_factoring", "Prime factorization (PA)"),
    ("pa_greatest_common_factor", "Greatest common factor"),
    ("pa_least_common_multiple", "Least common multiple"),
    ("g6_gcf_and_lcm_word_problems", "GCF and LCM word problems"),
    # g6_opposites_of_numbers disabled from curriculum picker (catalog/generators kept)
    ("g6_comparing_numbers", "Comparing numbers"),
    ("g6_ordering_numbers", "Ordering numbers"),
    ("g6_absolute_values", "Absolute values"),
    ("g6_comparing_with_absolute_values", "Comparing with absolute values"),
    ("g6_ordering_with_absolute_values", "Ordering with absolute values"),
    ("pa_integers_adding_and_subtracting", "Integers: adding and subtracting"),
    ("pa_integers_multiplying", "Integers: multiplying"),
    ("pa_integers_dividing", "Integers: dividing"),
    ("pa_writing_numbers_with_words", "Writing numbers with words"),
    # Interest (already continuous word-problem D; same set)
    ("pa_simple_and_compound_interest", "Simple and compound interest"),
)


def _generator_for(tid: str):
    if tid in GENERATORS:
        return GENERATORS[tid]
    try:
        from question_engine.core.registry import get_catalog_entry

        family = get_catalog_entry(tid).generator
    except Exception:
        family = None
    if family and family in GENERATORS:
        return GENERATORS[family]
    qt = QUESTION_TYPES.get(tid)
    if qt is not None:
        family = getattr(qt, "generator", None) or tid
        if family in GENERATORS:
            return GENERATORS[family]
    raise KeyError(tid)


def _d_heading(d: int) -> str:
    if d == EXTREME_D:
        return f"D = {d} <span class='extreme'>(extreme / unreasonable)</span>"
    return f"D = {d}"


def _append_samples(
    parts: list[str],
    *,
    tid: str,
    gen,
    d: int,
    count: int,
    failures: list[str],
) -> None:
    parts.append(f"<h3>{_d_heading(d)}</h3>")
    try:
        settings = _resolve_generation_settings(
            tid,
            {
                "difficulty": d,
                "count": count,
                "seed": 40 + d * 13 + (hash(tid) % 997),
                "include_answer_key": True,
            },
        )
        qs = gen(tid, settings)
    except Exception as exc:  # noqa: BLE001 — gallery should continue
        msg = f"{tid} D={d}: {exc}"
        failures.append(msg)
        parts.append(f"<p class='err'>{html.escape(msg)}</p>")
        return
    for i, q in enumerate(qs):
        prompt = q.prompt_latex or q.prompt_text or ""
        answer = q.answer_latex or q.answer_text or ""
        # Extreme D can produce huge integers; keep HTML/KaTeX usable.
        if d >= EXTREME_D and len(prompt) > 400:
            prompt = prompt[:400] + "\\ldots"
        if d >= EXTREME_D and len(answer) > 200:
            answer = answer[:200] + "\\ldots"
        card_cls = "card extreme-card" if d == EXTREME_D else "card"
        parts.append(f"<div class='{card_cls}'>")
        label = f"D={d}"
        if d == EXTREME_D:
            label += " · extreme / unreasonable"
        parts.append(
            f"<div class='meta'>#{i + 1} · topic=<code>{html.escape(tid)}</code> · "
            f"{html.escape(label)}</div>"
        )
        parts.append(f"<div>$${html.escape(prompt)}$$</div>")
        svg = (q.metadata or {}).get("diagram_svg")
        if isinstance(svg, str) and svg.lstrip().startswith("<svg"):
            parts.append(f"<div class='meta'>stimulus</div>{svg}")
        if answer:
            parts.append(f"<div class='ans'>→ $${html.escape(answer)}$$</div>")
        parts.append("</div>")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    parts = [
        "<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'/>",
        "<title>G6 / PA continuous difficulty</title>",
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css"/>',
        "<script defer src='https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js'></script>",
        "<script defer src='https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js'",
        " onload=\"renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}]})\"></script>",
        "<style>body{font-family:Georgia,serif;max-width:980px;margin:2rem auto;padding:0 1rem;background:#f7f4ef}",
        "h1{font-size:1.6rem}h2{margin-top:2.2rem;border-bottom:1px solid #ccc;padding-bottom:.25rem}",
        "h3{color:#444;margin-top:1.1rem}.card{background:#fff;border:1px solid #ddd;border-radius:6px;padding:.75rem 1rem;margin:.5rem 0}",
        ".ans{color:#1a5c2e}.meta{font-size:.8rem;color:#666}.toc a{margin-right:.75rem;line-height:1.8}",
        ".err{color:#8a1f1f;background:#fdeeee;padding:.5rem;border-radius:4px}",
        ".extreme{color:#8a3b12;font-weight:normal;font-size:.85em}",
        ".extreme-card{border-color:#d4a574;background:#fff8f0}</style></head><body>",
        "<h1>G6 / PA number-lane continuous difficulty</h1>",
        f"<p class='meta'>Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} · "
        f"{len(TOPICS)} topics · {N} examples at each of D = {', '.join(str(d) for d in DIFFS)} · "
        f"{N_EXTREME} example at D = {EXTREME_D} (extreme / unreasonable)</p>",
        "<p class='meta'>D = 40 is difficult but doable. D = 1000 proves unbounded scaling "
        "(essentially impossible). Diagram / geometry-fraction / stats-viz topics were skipped.</p>",
        "<nav class='toc'><strong>Topics:</strong><br/>",
    ]
    for tid, title in TOPICS:
        parts.append(f"<a href='#{html.escape(tid)}'>{html.escape(title)}</a>")
    parts.append("</nav>")

    failures: list[str] = []
    for tid, title in TOPICS:
        parts.append(f"<h2 id='{html.escape(tid)}'>{html.escape(title)}</h2>")
        parts.append(f"<p class='meta'><code>{html.escape(tid)}</code></p>")
        note = STRUCTURAL_EXTREME_NOTES.get(tid)
        if note:
            parts.append(f"<p class='meta extreme'>{html.escape(note)}</p>")
        try:
            gen = _generator_for(tid)
        except KeyError:
            msg = f"No generator for {tid}"
            failures.append(msg)
            parts.append(f"<p class='err'>{html.escape(msg)}</p>")
            continue
        for d in DIFFS:
            _append_samples(
                parts, tid=tid, gen=gen, d=d, count=N, failures=failures
            )
        _append_samples(
            parts,
            tid=tid,
            gen=gen,
            d=EXTREME_D,
            count=N_EXTREME,
            failures=failures,
        )

    if failures:
        parts.append("<h2>Failures</h2><ul>")
        for msg in failures:
            parts.append(f"<li class='err'>{html.escape(msg)}</li>")
        parts.append("</ul>")

    parts.append("</body></html>")
    path = OUT / "gallery.html"
    path.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {path} ({len(TOPICS)} topics, {len(failures)} failures)")
    if failures:
        for msg in failures[:20]:
            print(" FAIL", msg)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
