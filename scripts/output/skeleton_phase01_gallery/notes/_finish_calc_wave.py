"""Finish Calc wave: Limitations on all notes, missing notes, gallery sections.

Run from repo root:
  python scripts/output/skeleton_phase01_gallery/notes/_finish_calc_wave.py
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any

os.environ["QE_LOG_GENERATED"] = "0"

_ROOT = Path(__file__).resolve().parents[4]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from question_engine.api.handler import _generate_for_type
from question_engine.catalogs.calculus import CATALOG

NOTES = Path(__file__).resolve().parent
OUT = NOTES.parent
GEN = OUT / "gen_examples.py"

DS = (0.0, 8.0, 16.0, 22.0)
SEEDS = (101, 207)

# Catalog leaves still on calculus_foundations (honest gold not locked).
STUB_UNCLEAR = {
    "calc_app_diff_intervals_of_concavity",
    "calc_app_diff_relative_extrema",
    "calc_app_diff_absolute_extrema",
    "calc_app_diff_optimization",
    "calc_app_diff_curve_sketching",
    "calc_app_diff_graphical_comparison_of_f_f_prime_and_f_double_prime",
    "calc_app_diff_motion_along_a_line",
    "calc_app_diff_newtons_method",
    "calc_app_int_motion_along_a_line_revisited",
    "calc_diff_eq_introduction",
}

# Shipped this wave (were deferred from gallery; generators honest or just fleshed).
NEWLY_SHIPPED = {
    "calc_app_diff_slope_tangent_and_normal_lines",
    "calc_app_diff_rolles_theorem",
    "calc_app_diff_mean_value_theorem",
    "calc_app_diff_intervals_of_increase_and_decrease",
    "calc_app_diff_differentials",
    "calc_app_diff_linear_approximations",
    "calc_def_int_approximating_area_under_a_curve",
    "calc_def_int_area_under_a_curve_by_limit_of_sums",
    "calc_def_int_riemann_sum_tables",
    "calc_def_int_mean_value_theorem",
    "calc_app_int_area_between_curves",
    "calc_app_int_volume_by_slicing_disks_and_washers",
    "calc_app_int_volume_by_cylinders",
    "calc_app_int_volume_of_solids_with_known_cross_sections",
    "calc_diff_eq_slope_fields",
    "calc_diff_eq_separable",
    "calc_diff_eq_exponential_growth_and_decay",
    # also missing-note Diff leaves that already have generators
    "calc_diff_average_rates_of_change",
    "calc_diff_definition_of_the_derivative",
    "calc_diff_instantaneous_rates_of_change",
    "calc_diff_rules_using_tables",
    "calc_diff_other_base_logarithms_and_exponentials",
    "calc_diff_logarithmic",
    "calc_diff_inverse_functions",
    "calc_app_diff_limits_in_form_of_definition_of_derivative",
}

LIMITATIONS_BY_FAMILY: dict[str, str] = {
    "limits": (
        "LimitSpec packs ship. Remaining gaps: form_id metadata sometimes mismatches "
        "latex (e.g. `direct_sqrt` stamp on rational plug-in); one-sided / piecewise "
        "story variety thinner than OpenStax §2.2–2.4 exercise banks; no dedicated "
        "limit-skeleton patterns beyond packs."
    ),
    "diff_skel": (
        "Live on Diff `expr_skeleton` + derivatives.json forms. Gaps: allow_* checkboxes "
        "gate class unlocks; some leaves still stamp soft patterns; OpenStax mixed-rule "
        "drill richer than general pack at mid-D."
    ),
    "diff_other": (
        "Dedicated constructive / Mad-Lib-meta generators (not expr_skeleton gallery "
        "topics). Gaps: table/figure UX still text-only; logarithmic / inverse-function "
        "depth vs OpenStax §3.8–3.9 limited; implicit remains Mad-Lib (see that leaf)."
    ),
    "integral": (
        "Reuse `integrals.py` / FTC / Riemann constructive cores. Gaps: curve families "
        "still thin vs OpenStax §5–6 (mostly poly); trig-sub / PFD / multi-trick are "
        "catalog-shaped but not full textbook exercise breadth."
    ),
    "app_shipped": (
        "Constructive app generators with continuous-D structure knobs. Gaps: story "
        "frame banks thinner than OpenStax for related rates / growth; volumes mostly "
        "axis-of-rotation textbook templates; no interactive figures."
    ),
    "stub": (
        "`calculus_foundations` fallback — NOT honest gold for this leaf. Needs "
        "dedicated sign-chart / closed-interval / optimization-frame / sketch / "
        "graph-match / motion / Newton / DE-intro generators before clearing UNCLEAR."
    ),
}


def _family_for(tid: str, gen: str) -> str:
    if tid in STUB_UNCLEAR or gen == "calculus_foundations":
        return "stub"
    if tid.startswith("calc_limits_") or tid.startswith("calc_continuity_") or tid == "calc_app_diff_lhopitals_rule":
        return "limits"
    if tid in {
        "calc_diff_power_rule",
        "calc_diff_product_rule",
        "calc_diff_quotient_rule",
        "calc_diff_chain_rule",
        "calc_diff_trigonometric",
        "calc_diff_inverse_trigonometric",
        "calc_diff_natural_logarithms_and_exponentials",
        "calc_diff_general",
        "calc_diff_higher_order_derivatives",
    }:
        return "diff_skel"
    if tid.startswith("calc_diff_") and not tid.startswith("calc_diff_eq_"):
        return "diff_other"
    if tid.startswith("calc_indef_") or tid.startswith("calc_def_") or tid.startswith("calc_app_int_"):
        if tid in STUB_UNCLEAR:
            return "stub"
        return "integral" if tid.startswith(("calc_indef_", "calc_def_")) else "app_shipped"
    if tid.startswith("calc_app_diff_"):
        return "stub" if tid in STUB_UNCLEAR else "app_shipped"
    if tid.startswith("calc_diff_eq_"):
        return "stub" if tid in STUB_UNCLEAR else "app_shipped"
    return "app_shipped"


def _sample_rows(tid: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for d in DS:
        for seed in SEEDS:
            try:
                qs = _generate_for_type(
                    tid,
                    {
                        "difficulty": d,
                        "count": 1,
                        "include_answer_key": True,
                        "seed": seed,
                    },
                )
            except Exception as exc:  # noqa: BLE001
                rows.append(
                    {
                        "d": d,
                        "seed": seed,
                        "prompt": f"(error: {exc})",
                        "answer": "",
                        "shape": "error",
                    }
                )
                continue
            q = qs[0] if qs else None
            if q is None:
                rows.append({"d": d, "seed": seed, "prompt": "(empty)", "answer": "", "shape": ""})
                continue
            pl = getattr(q, "prompt_latex", None) or ""
            al = getattr(q, "answer_latex", None) or ""
            meta = getattr(q, "metadata", None) or {}
            if hasattr(meta, "get"):
                form = meta.get("form_id") or meta.get("skeleton_pattern") or ""
            else:
                form = ""
            rows.append(
                {
                    "d": d,
                    "seed": seed,
                    "prompt": pl,
                    "answer": al,
                    "shape": str(form),
                }
            )
    return rows


def _tex_cell(s: str) -> str:
    s = (s or "").replace("\n", " ").strip()
    if not s:
        return ""
    if s.startswith("$") or s.startswith(r"\text") or s.startswith(r"\int") or s.startswith(r"\lim") or s.startswith(r"\frac"):
        return f"${s}$" if not s.startswith("$") else s
    return f"${s}$"


def _limitations_block(tid: str, gen: str, *, status: str) -> str:
    fam = _family_for(tid, gen)
    body = LIMITATIONS_BY_FAMILY[fam]
    lines = [
        "## Limitations",
        "",
        f"- **Status:** {status}",
        f"- **Generator:** `{gen}`",
        f"- **Remaining limits:** {body}",
    ]
    if tid in STUB_UNCLEAR:
        lines.append("- **Flags:** `UNCLEAR` / `NOT_IMPLEMENTED` — red-header gallery samples only.")
    elif tid == "calc_diff_implicit":
        lines.append("- **Flags:** `UNCLEAR` / `LOW_VARIETY` — Mad-Lib implicit; catalog form stub.")
    return "\n".join(lines) + "\n"


def _ensure_limitations(path: Path, tid: str, gen: str, status: str) -> None:
    text = path.read_text(encoding="utf-8")
    block = _limitations_block(tid, gen, status=status)
    if re.search(r"^## Limitations\s*$", text, re.M):
        # Replace existing Limitations section through next ## or EOF
        text2 = re.sub(
            r"^## Limitations\n(?:.*?)(?=^## |\Z)",
            block + "\n",
            text,
            count=1,
            flags=re.M | re.S,
        )
        path.write_text(text2, encoding="utf-8")
        return
    # Insert after header / first ---
    if "\n---\n" in text:
        pre, post = text.split("\n---\n", 1)
        text = pre + "\n---\n\n" + block + "\n" + post.lstrip("\n")
    else:
        text = block + "\n" + text
    path.write_text(text, encoding="utf-8")


def _write_missing_note(entry) -> Path:
    tid = entry.id
    gen = str(entry.generator or "")
    fam = _family_for(tid, gen)
    status = (
        "stub / NOT_IMPLEMENTED"
        if fam == "stub"
        else ("shipped (Diff skeleton)" if fam == "diff_skel" else "shipped (constructive)")
    )
    rows = _sample_rows(tid)
    unclear = tid in STUB_UNCLEAR or tid == "calc_diff_implicit"
    flags = ""
    if unclear:
        flags = "\n\n> **UNCLEAR** — see Limitations.\n"
        if tid == "calc_diff_implicit":
            flags = "\n\n> **UNCLEAR / LOW_VARIETY** — Mad-Lib implicit.\n"

    openstax = {
        "calc_diff_average_rates_of_change": ("3.4", "3-4-derivatives-as-rates-of-change", "avg rate [a,b]"),
        "calc_diff_definition_of_the_derivative": ("3.1", "3-1-defining-the-derivative", "limit definition f'(a)"),
        "calc_diff_instantaneous_rates_of_change": ("3.4", "3-4-derivatives-as-rates-of-change", "f'(a) as instantaneous rate"),
        "calc_diff_rules_using_tables": ("3.3", "3-3-differentiation-rules", "product/quotient/chain from table"),
        "calc_diff_other_base_logarithms_and_exponentials": ("3.9", "3-9-derivatives-of-exponential-and-logarithmic-functions", "a^x / log_a"),
        "calc_diff_logarithmic": ("3.9", "3-9-derivatives-of-exponential-and-logarithmic-functions", "logarithmic differentiation"),
        "calc_diff_inverse_functions": ("3.7", "3-7-derivatives-of-inverse-functions", "(f^{-1})'(a)=1/f'(b)"),
        "calc_app_diff_limits_in_form_of_definition_of_derivative": (
            "3.1",
            "3-1-defining-the-derivative",
            "recognize lim h→0 as f'(a)",
        ),
    }
    sec, slug, shape = openstax.get(
        tid,
        ("3.3", "3-3-differentiation-rules", "match OpenStax skill for this leaf"),
    )
    table_lines = [
        "| D | seed | prompt_latex | answer_latex | shape notes |",
        "|---|------|--------------|--------------|-------------|",
    ]
    for r in rows:
        table_lines.append(
            f"| {int(r['d']) if float(r['d']).is_integer() else r['d']} | {r['seed']} | "
            f"{_tex_cell(r['prompt'])} | {_tex_cell(r['answer'])} | {r['shape'] or '—'} |"
        )

    md = f"""# Notes — `{tid}`

- **Display name:** {entry.name}
- **Category:** {entry.category}
- **Generator:** `{gen}`
- **Suggested family:** diff / other
{flags}
---

{_limitations_block(tid, gen, status=status)}

## What the question should look like (D=0 vs high D)

- **Skill:** {entry.name} — match OpenStax shape below.
- **D=0:** As simple as live easy samples.
- **High D (≈16–22):** Numeric / structure unlocks via continuous D (not metadata pads).
- **Must not:** Wrong-topic dump; Diff skeleton on non-Diff leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` (default path).

{chr(10).join(table_lines)}

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §{sec} | https://openstax.org/books/calculus-volume-1/pages/{slug} | {shape} |

Local HTML / mine: `scripts/output/example_mining/calculus-volume-1/stage1/`

## Variety notes / UNCLEAR flag

{"Flags: `UNCLEAR`." if unclear else "Shapes follow live samples; OpenStax frames win for story variety when applicable."}

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** current catalog generator `{gen}`.
- **Not this pass:** gallery stub + Limitations; flesh only if gold locked.
"""
    path = NOTES / f"{tid}.md"
    path.write_text(md, encoding="utf-8")
    return path


def _refresh_live_samples_in_note(path: Path, tid: str) -> None:
    """Update old-path table for newly fleshed leaves."""
    if tid not in {
        "calc_app_int_area_between_curves",
        "calc_def_int_approximating_area_under_a_curve",
        "calc_diff_eq_exponential_growth_and_decay",
    }:
        return
    rows = _sample_rows(tid)
    table_lines = [
        "| D | seed | prompt_latex | answer_latex | shape notes |",
        "|---|------|--------------|--------------|-------------|",
    ]
    for r in rows:
        table_lines.append(
            f"| {int(r['d']) if float(r['d']).is_integer() else r['d']} | {r['seed']} | "
            f"{_tex_cell(r['prompt'])} | {_tex_cell(r['answer'])} | {r['shape'] or '—'} |"
        )
    table = "\n".join(table_lines)
    text = path.read_text(encoding="utf-8")
    text2, n = re.subn(
        r"(\| D \| seed \| prompt_latex \| answer_latex \| shape notes \|\n\|---\|.*?\n)(?:\|.*\n)+",
        r"\1" + "\n".join(table_lines[2:]) + "\n",
        text,
        count=1,
        flags=re.M,
    )
    if n:
        path.write_text(text2, encoding="utf-8")
    else:
        # fallback: leave as-is
        pass


def _patch_gen_examples() -> None:
    text = GEN.read_text(encoding="utf-8")
    # Expand shipped list + unclear titles for remaining stubs; add NEWLY_SHIPPED.
    marker = "CALC_INTEGRAL_APP_SHIPPED: list[tuple[str, str, str]] = ["
    if marker not in text:
        raise SystemExit("CALC_INTEGRAL_APP_SHIPPED marker missing")

    extra_shipped = [
        (
            "calc_app_diff_slope_tangent_and_normal_lines",
            "App — tangent / normal lines",
            "Pilot <code>tangent_normal_line</code>. OpenStax Vol 1 §3.1 / §4.2.",
        ),
        (
            "calc_app_diff_rolles_theorem",
            "App — Rolle's Theorem",
            "Find c with f'(c)=0. OpenStax Vol 1 §4.4.",
        ),
        (
            "calc_app_diff_mean_value_theorem",
            "App — Mean Value Theorem (diff)",
            "Find c with f'(c)=(f(b)-f(a))/(b-a). OpenStax Vol 1 §4.4.",
        ),
        (
            "calc_app_diff_intervals_of_increase_and_decrease",
            "App — intervals of increase/decrease",
            "Quadratic sign-chart style. OpenStax Vol 1 §4.5.",
        ),
        (
            "calc_app_diff_differentials",
            "App — differentials",
            "dy = f'(x) dx. OpenStax Vol 1 §4.2.",
        ),
        (
            "calc_app_diff_linear_approximations",
            "App — linear approximations",
            "L(x)=f(a)+f'(a)(x-a). OpenStax Vol 1 §4.2.",
        ),
        (
            "calc_def_int_approximating_area_under_a_curve",
            "Riemann — approximate area",
            "Left/right/mid + linear/quad curves. OpenStax Vol 1 §5.1.",
        ),
        (
            "calc_def_int_area_under_a_curve_by_limit_of_sums",
            "Area by limit of sums",
            "Reuse area_under_curve / limit-of-sums path. OpenStax Vol 1 §5.2.",
        ),
        (
            "calc_def_int_riemann_sum_tables",
            "Riemann sums from tables",
            "Left/right/mid from value tables. OpenStax Vol 1 §5.1.",
        ),
        (
            "calc_def_int_mean_value_theorem",
            "Integral MVT — average value",
            "Average value of f on [a,b]. OpenStax Vol 1 §5.4 / §6.x.",
        ),
        (
            "calc_app_int_area_between_curves",
            "App — area between curves",
            "∫(top−bottom); D unlocks. OpenStax Vol 1 §6.1.",
        ),
        (
            "calc_app_int_volume_by_slicing_disks_and_washers",
            "App — disk / washer volumes",
            "Rotate about x-axis. OpenStax Vol 1 §6.2.",
        ),
        (
            "calc_app_int_volume_by_cylinders",
            "App — shell method volumes",
            "Rotate about y-axis. OpenStax Vol 1 §6.3.",
        ),
        (
            "calc_app_int_volume_of_solids_with_known_cross_sections",
            "App — known cross sections",
            "Square / equilateral / semicircle. OpenStax Vol 1 §6.2.",
        ),
        (
            "calc_diff_eq_slope_fields",
            "DE — slope field interpret",
            "Evaluate y' at a point. OpenStax Vol 2 §4.1–4.2.",
        ),
        (
            "calc_diff_eq_separable",
            "DE — separable",
            "IVP poly / exp / homogeneous. OpenStax Vol 2 §4.3.",
        ),
        (
            "calc_diff_eq_exponential_growth_and_decay",
            "DE — continuous growth/decay",
            "y'=ky models (not Algebra discrete %). OpenStax Vol 1 §6.8.",
        ),
        (
            "calc_diff_average_rates_of_change",
            "Diff — average rate of change",
            "Δf/Δx on [a,b]. OpenStax Vol 1 §3.4.",
        ),
        (
            "calc_diff_definition_of_the_derivative",
            "Diff — definition of the derivative",
            "Limit definition. OpenStax Vol 1 §3.1.",
        ),
        (
            "calc_diff_instantaneous_rates_of_change",
            "Diff — instantaneous rate",
            "f'(a) as rate. OpenStax Vol 1 §3.4.",
        ),
        (
            "calc_diff_rules_using_tables",
            "Diff — rules from tables",
            "Product/quotient/chain from tabulated values. OpenStax Vol 1 §3.3.",
        ),
        (
            "calc_diff_other_base_logarithms_and_exponentials",
            "Diff — other-base log/exp",
            "a^x / log_a. OpenStax Vol 1 §3.9.",
        ),
        (
            "calc_diff_logarithmic",
            "Diff — logarithmic differentiation",
            "OpenStax Vol 1 §3.9.",
        ),
        (
            "calc_diff_inverse_functions",
            "Diff — inverse functions",
            "(f^{-1})'. OpenStax Vol 1 §3.7.",
        ),
        (
            "calc_app_diff_limits_in_form_of_definition_of_derivative",
            "App — limits as definition of derivative",
            "Recognize lim as f'(a). OpenStax Vol 1 §3.1.",
        ),
    ]

    # Insert extra tuples before closing of CALC_INTEGRAL_APP_SHIPPED if not present
    for tid, title, blurb in extra_shipped:
        if f'"{tid}"' in text and tid in text[text.find(marker) : text.find("CALC_UNCLEAR_TITLES")]:
            continue
        # append before the closing ] of CALC_INTEGRAL_APP_SHIPPED
        close_idx = text.find("\n]\n\nCALC_UNCLEAR_TITLES")
        if close_idx < 0:
            raise SystemExit("cannot find end of CALC_INTEGRAL_APP_SHIPPED")
        entry = (
            f'    (\n'
            f'        "{tid}",\n'
            f'        "{title}",\n'
            f'        "{blurb}",\n'
            f'    ),\n'
        )
        # avoid dup
        if f'"{tid}"' in text[text.find(marker):close_idx]:
            continue
        text = text[:close_idx] + "\n" + entry + text[close_idx:]

    # Update _calc_sec engine mapping for new types
    engine_patch = '''
def _build_calc_integral_sections() -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    for tid, title, blurb in CALC_INTEGRAL_APP_SHIPPED:
        eng = "integrals"
        if "related_rates" in tid:
            eng = "related_rates_frames"
        elif tid == "calc_app_int_area_under_a_curve":
            eng = "area_under_curve"
        elif tid == "calc_app_int_area_between_curves":
            eng = "area_between_curves"
        elif "volume" in tid:
            eng = "volumes"
        elif "riemann" in tid or tid == "calc_def_int_approximating_area_under_a_curve":
            eng = "riemann"
        elif tid.startswith("calc_diff_eq_"):
            eng = "diff_eq"
        elif tid.startswith("calc_app_diff_") or tid.startswith("calc_diff_"):
            eng = "calc_apps"
        elif tid == "calc_def_int_mean_value_theorem":
            eng = "def_int_mvt"
        elif tid == "calc_def_int_area_under_a_curve_by_limit_of_sums":
            eng = "area_under_curve"
        sections.append(_calc_sec(tid, title, blurb, engine=eng))
    for tid in sorted(CALC_UNCLEAR):
        title = CALC_UNCLEAR_TITLES.get(tid, f"{tid} (UNCLEAR)")
        sections.append(
            _calc_sec(
                tid,
                title,
                "UNCLEAR gold — red-header live samples of existing generator only. "
                f"See <code>notes/{tid}.md</code>.",
                engine="calculus_foundations",
            )
        )
    return sections
'''
    text2, n = re.subn(
        r"def _build_calc_integral_sections\(\) -> list\[dict\[str, Any\]\]:.*?(?=\n\nSECTIONS\.extend\(_build_calc_integral_sections\(\)\))",
        engine_patch.strip() + "\n",
        text,
        count=1,
        flags=re.S,
    )
    if n != 1:
        print("warn: _build_calc_integral_sections replace count", n)
        text2 = text

    # Update SKIPPED_NOTE deferred line
    text2 = re.sub(
        r"Calc deferred this wave \(volumes / Riemann / DE separable·growth·slope / "
        r"area-between / integral MVT / differentials·linear approx / Rolle·MVT·tangent\): "
        r"see <code>notes/CALC_INDEX\.md</code>\.",
        "Calc apps formerly deferred (volumes / Riemann / DE / area-between / Rolle·MVT / …) "
        "are gallery-wired; remaining UNCLEAR = <code>calculus_foundations</code> stubs — "
        "see <code>notes/CALC_INDEX.md</code>.",
        text2,
        count=1,
    )

    # Red-header flags: include NOT_IMPLEMENTED
    text2 = text2.replace(
        r'_NOTES_FLAG_RE = re.compile(r"\b(UNCLEAR|LOW_VARIETY)\b")',
        r'_NOTES_FLAG_RE = re.compile(r"\b(UNCLEAR|LOW_VARIETY|NOT_IMPLEMENTED)\b")',
    )

    GEN.write_text(text2, encoding="utf-8")
    print("patched gen_examples.py")


def main() -> None:
    by_id = {e.id: e for e in CATALOG}
    summary: dict[str, Any] = {
        "limitations_written": [],
        "notes_created": [],
        "shipped": sorted(NEWLY_SHIPPED),
        "stub_unclear": sorted(STUB_UNCLEAR),
    }

    for entry in CATALOG:
        tid = entry.id
        gen = str(entry.generator or "")
        path = NOTES / f"{tid}.md"
        if not path.is_file():
            _write_missing_note(entry)
            summary["notes_created"].append(tid)
            path = NOTES / f"{tid}.md"
        fam = _family_for(tid, gen)
        if fam == "stub":
            status = "stub / NOT_IMPLEMENTED (calculus_foundations)"
        elif fam == "diff_skel":
            status = "shipped — Diff expr_skeleton"
        elif tid in NEWLY_SHIPPED:
            status = "shipped — constructive (gallery-wired this wave)"
        else:
            status = "shipped — live generator"
        _ensure_limitations(path, tid, gen, status)
        _refresh_live_samples_in_note(path, tid)
        summary["limitations_written"].append(tid)

        # Ensure UNCLEAR / NOT_IMPLEMENTED token present for stubs
        if tid in STUB_UNCLEAR:
            text = path.read_text(encoding="utf-8")
            if "NOT_IMPLEMENTED" not in text:
                text = text.replace(
                    "> **UNCLEAR**",
                    "> **UNCLEAR / NOT_IMPLEMENTED**",
                    1,
                )
                if "UNCLEAR" not in text[:400]:
                    text = text.replace(
                        f"# Notes — `{tid}`\n",
                        f"# Notes — `{tid}`\n\n> **UNCLEAR / NOT_IMPLEMENTED** — foundations stub.\n\n",
                        1,
                    )
                path.write_text(text, encoding="utf-8")

    _patch_gen_examples()

    # Write status index
    status_md = NOTES / "CALC_STATUS.md"
    status_md.write_text(
        "# Calculus shipped vs stub (2026-08-20 wave)\n\n"
        f"- Catalog leaves: **{len(CATALOG)}**\n"
        f"- Newly gallery-wired / fleshed: **{len(NEWLY_SHIPPED)}**\n"
        f"- Still stub (`calculus_foundations` / UNCLEAR): **{len(STUB_UNCLEAR)}**\n\n"
        "## Newly shipped (this wave)\n\n"
        + "\n".join(f"- `{t}`" for t in sorted(NEWLY_SHIPPED))
        + "\n\n## Stub-only (red-header)\n\n"
        + "\n".join(f"- `{t}`" for t in sorted(STUB_UNCLEAR))
        + "\n",
        encoding="utf-8",
    )
    (NOTES / "_calc_finish_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps({k: (len(v) if isinstance(v, list) else v) for k, v in summary.items()}, indent=2))


if __name__ == "__main__":
    main()
