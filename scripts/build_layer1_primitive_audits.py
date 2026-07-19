"""Audit galleries for Layer-1 algebra primitives (and refresh variable audit).

Writes under scripts/output/topic_fit/:
  ooo_audit/
  evaluate_linear_expressions_audit/
  combine_like_terms_audit/
  expand_simplify_audit/
  equations_audit/
  inequalities_audit/
  multistep_equations_audit/
  multistep_inequalities_audit/
  factor_gcf_audit/

Each folder gets gallery.html (KaTeX), gallery.md, samples.json.

Also re-runs variable lane audit via build_variable_lane_audit.

Usage:
  $env:PYTHONPATH='.'
  python scripts/build_layer1_primitive_audits.py
"""

from __future__ import annotations

import html
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from question_engine.generators import GENERATORS

OUT_ROOT = ROOT / "scripts" / "output" / "topic_fit"
DIFFICULTIES = (0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0)
# Wide range so evaluate / expand / multi-step log growth is visible.
EVALUATE_DIFFICULTIES = (0.0, 1.0, 2.0, 3.0, 5.0, 8.0, 10.0, 14.0, 18.0, 22.0, 24.0)
EXPAND_DIFFICULTIES = EVALUATE_DIFFICULTIES
MULTISTEP_DIFFICULTIES = (0.0, 1.0, 2.0, 4.0, 6.0, 8.0, 10.0, 14.0, 18.0, 22.0, 24.0)
N_PER = 4

CONSTRAINT_VARIANTS: dict[str, dict[str, Any]] = {
    "default": {},
    "integers_only": {"integers_only": True},
    "lock_x": {"lock_variable": "x", "integers_only": True},
}


def _base_settings(d: float, extra: dict[str, Any]) -> dict[str, Any]:
    return {
        "count": N_PER,
        "include_answer_key": True,
        "difficulty": d,
        **extra,
    }


def _sample_generator(
    gen_key: str,
    *,
    difficulties: tuple[float, ...] = DIFFICULTIES,
    variants: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    gen = GENERATORS[gen_key]
    variants = variants or CONSTRAINT_VARIANTS
    rows: list[dict[str, Any]] = []
    for vname, vsettings in variants.items():
        for d in difficulties:
            qs = gen(gen_key, _base_settings(d, vsettings))
            for i, q in enumerate(qs):
                meta = q.metadata or {}
                rows.append(
                    {
                        "constraint_set": vname,
                        "constraints": vsettings,
                        "difficulty": d,
                        "index": i,
                        "prompt_latex": q.prompt_latex,
                        "prompt_text": q.prompt_text,
                        "answer_latex": q.answer_latex,
                        "spend": meta.get("spend"),
                        "upgrades": meta.get("upgrades"),
                        "n_terms": meta.get("n_terms"),
                        "n_parens": meta.get("n_parens"),
                        "nest_depth": meta.get("nest_depth"),
                        "n_ops": meta.get("n_ops"),
                        "n_groups": meta.get("n_groups"),
                        "n_lone": meta.get("n_lone"),
                        "nested": meta.get("nested"),
                        "op_pool": meta.get("op_pool"),
                        "steps": meta.get("steps"),
                        "flipped": meta.get("flipped"),
                        "primitive_engine": meta.get("primitive_engine"),
                        "sample_log": meta.get("sample_log"),
                    }
                )
    return rows


def _html_escape(s: str) -> str:
    return html.escape(s, quote=True)


def _build_html(
    title: str,
    lede: str,
    rows: list[dict[str, Any]],
    *,
    d_notes: list[tuple[str, str]] | None = None,
) -> str:
    by_variant: dict[str, list[dict]] = {}
    for r in rows:
        by_variant.setdefault(r["constraint_set"], []).append(r)

    parts = [
        "<!DOCTYPE html>",
        '<html lang="en"><head><meta charset="utf-8"/>',
        f"<title>{_html_escape(title)}</title>",
        "<style>",
        """
    :root { color-scheme: light; }
    body { font-family: Georgia, "Times New Roman", serif; margin: 1.5rem 2rem; line-height: 1.45;
           color: #1a1a1a; background: #faf9f7; }
    h1 { font-size: 1.75rem; margin-bottom: 0.25rem; }
    h2 { margin-top: 2rem; border-bottom: 1px solid #ccc; padding-bottom: 0.25rem; }
    .lede { max-width: 52rem; color: #444; }
    .code { font-family: ui-monospace, Consolas, monospace; font-size: 0.85em; }
    .samples { font-family: "Cambria Math", "Times New Roman", serif; font-size: 1.0rem; }
    table.compare { border-collapse: collapse; width: 100%; font-size: 0.88rem; margin: 0.5rem 0 1.5rem; }
    table.compare th, table.compare td { border: 1px solid #ccc; padding: 0.4rem 0.5rem; vertical-align: top; }
    table.compare th { background: #e8e6e1; }
    .pill { display: inline-block; background: #eef2f7; border: 1px solid #c5d0de;
            border-radius: 3px; padding: 0.05rem 0.35rem; margin: 0.1rem; font-size: 0.8rem; }
    .ans { color: #255; }
    .notes { border-collapse: collapse; font-size: 0.9rem; margin-bottom: 1rem; }
    .notes th, .notes td { border: 1px solid #ccc; padding: 0.3rem 0.5rem; }
        """,
        "</style>",
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css"/>',
        '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>',
        (
            '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" '
            "onload=\"renderMathInElement(document.body,{delimiters:["
            "{left:'$',right:'$',display:false},{left:'$$',right:'$$',display:true}]})\"></script>"
        ),
        "</head><body>",
        f"<h1>{_html_escape(title)}</h1>",
        f'<p class="lede">{lede}</p>',
    ]
    if d_notes:
        parts.append("<h2>Difficulty behavior</h2>")
        parts.append(
            '<table class="notes"><thead><tr><th>D range</th><th>What changes</th></tr></thead><tbody>'
        )
        for rng, note in d_notes:
            parts.append(
                f'<tr><td class="code">{_html_escape(rng)}</td>'
                f"<td>{_html_escape(note)}</td></tr>"
            )
        parts.append("</tbody></table>")

    for vname, vrows in by_variant.items():
        constraints = vrows[0].get("constraints") or {}
        parts.append(f"<h2>{_html_escape(vname)}</h2>")
        parts.append(f'<p class="code">{_html_escape(json.dumps(constraints))}</p>')
        parts.append(
            '<table class="compare"><thead><tr>'
            "<th>D</th><th>Spend / upgrades</th><th>Samples (prompt → answer)</th>"
            "</tr></thead><tbody>"
        )
        by_d: dict[float, list[dict]] = {}
        for r in vrows:
            by_d.setdefault(float(r["difficulty"]), []).append(r)
        for d in sorted(by_d):
            samples = by_d[d]
            meta_bits = []
            spend = samples[0].get("spend")
            if spend:
                meta_bits.append(
                    " ".join(
                        f'<span class="pill code">{_html_escape(k)}={v}</span>'
                        for k, v in spend.items()
                    )
                )
            ups = samples[0].get("upgrades") or []
            if ups:
                meta_bits.append(
                    "upgrades: "
                    + " ".join(
                        f'<span class="pill">{_html_escape(str(u))}</span>' for u in ups
                    )
                )
            for key in ("n_terms", "n_parens", "nest_depth", "n_ops", "n_groups", "n_lone"):
                if samples[0].get(key) is not None:
                    meta_bits.append(
                        f'<span class="pill code">{key}={_html_escape(str(samples[0][key]))}</span>'
                    )
            if samples[0].get("nested"):
                meta_bits.append('<span class="pill">nested</span>')
            steps = samples[0].get("steps")
            if steps:
                meta_bits.append(
                    f'<span class="pill">steps={_html_escape(str(steps))}</span>'
                )
            if samples[0].get("flipped"):
                meta_bits.append('<span class="pill">flipped</span>')
            sample_html = []
            for s in samples:
                pl = s.get("prompt_latex") or ""
                al = s.get("answer_latex") or ""
                sample_html.append(
                    f'<div class="samples">${pl}$ '
                    f'<span class="ans">→ ${al}$</span></div>'
                )
            parts.append(
                f"<tr><td>{d:g}</td><td>{'<br/>'.join(meta_bits) or '—'}</td>"
                f"<td>{''.join(sample_html)}</td></tr>"
            )
        parts.append("</tbody></table>")

    parts.append("</body></html>")
    return "\n".join(parts)


def _build_md(title: str, lede: str, rows: list[dict[str, Any]]) -> str:
    lines = [f"# {title}", "", lede, ""]
    by_variant: dict[str, list[dict]] = {}
    for r in rows:
        by_variant.setdefault(r["constraint_set"], []).append(r)
    for vname, vrows in by_variant.items():
        lines.append(f"## {vname}")
        lines.append("")
        lines.append(f"`{json.dumps(vrows[0].get('constraints') or {})}`")
        lines.append("")
        lines.append("| D | Prompt | Answer | Upgrades |")
        lines.append("|--:|--------|--------|----------|")
        for r in vrows:
            ups = ", ".join(r.get("upgrades") or []) or "—"
            pl = (r.get("prompt_latex") or "").replace("|", "\\|")
            al = (r.get("answer_latex") or "").replace("|", "\\|")
            lines.append(f"| {r['difficulty']:g} | ${pl}$ | ${al}$ | {ups} |")
        lines.append("")
    return "\n".join(lines)


def write_audit(
    folder: str,
    title: str,
    lede: str,
    rows: list[dict[str, Any]],
    *,
    d_notes: list[tuple[str, str]] | None = None,
) -> Path:
    out = OUT_ROOT / folder
    out.mkdir(parents=True, exist_ok=True)
    (out / "samples.json").write_text(
        json.dumps(rows, indent=2, default=str), encoding="utf-8"
    )
    (out / "gallery.md").write_text(_build_md(title, lede, rows), encoding="utf-8")
    (out / "gallery.html").write_text(
        _build_html(title, lede, rows, d_notes=d_notes), encoding="utf-8"
    )
    return out


def main() -> None:
    written: list[Path] = []

    written.append(
        write_audit(
            "ooo_audit",
            "Order of operations audit",
            "Shared expression-structure engine (numeric mode). Leaf count / nesting "
            "grow with D; association (left/right/balanced/chain) and paren placement "
            "vary across seeds. Optional small squares when D ≥ 3.",
            _sample_generator(
                "order_of_operations",
                difficulties=EVALUATE_DIFFICULTIES,
                variants={
                    "default": {"integers_only": True},
                    "friendly": {"integers_only": True, "number_profile": "friendly_wholes"},
                },
            ),
            d_notes=[
                ("0–1.5", "1–2 leaves; +/− primarily"),
                ("1.5–4", "more ops; × unlocks; varied paren association"),
                ("4+", "deeper nests; occasional squares; richer trees"),
            ],
        )
    )

    written.append(
        write_audit(
            "evaluate_linear_expressions_audit",
            "Evaluate linear expressions audit",
            "Affine (degree-1) expressions only. Term count grows as "
            "<code>n_terms = 1 + floor(log2(1 + D/1.5))</code> with no hard cap; "
            "parentheses via <code>n_parens = floor(log2(1 + D/3))</code> (budget often "
            "concentrated for deeper nesting); ×/÷-by-constant unlock with D. Numbers and "
            "the unknown come from Layer 0 lanes.",
            _sample_generator(
                "g6_evaluating_algebraic_expressions",
                difficulties=EVALUATE_DIFFICULTIES,
            ),
            d_notes=[
                ("0–1.5", "1 term (e.g. ax); +/− only"),
                ("1.5–4.5", "2 terms; × unlocks at D≥2"),
                ("4.5–10.5", "3 terms; ÷ unlocks at D≥4; more parens"),
                ("10.5+", "4+ terms; deeper nested parens and scale ops grow without a hard cap"),
            ],
        )
    )

    written.append(
        write_audit(
            "combine_like_terms_audit",
            "Combine like terms audit",
            "D buys more like terms, negatives, and (at high D) a second variable family.",
            _sample_generator("g6_combining_like_terms"),
            d_notes=[
                ("0–3", "Few ax terms + constant"),
                ("4–8", "More terms and negatives"),
                ("10+", "many_terms / second_variable possible"),
            ],
        )
    )

    written.append(
        write_audit(
            "expand_simplify_audit",
            "Expand then simplify audit",
            "Shared expression-structure engine (algebraic, prefer_distribute). "
            "Linear only: distribute then combine to <code>Ax+B</code>. Leaf/group "
            "count grows as <code>1 + floor(log2(1 + D/1.5))</code>; nesting via "
            "shared nest budget. Same structural DNA as OOO (numeric) and "
            "multi-step equation sides.",
            _sample_generator(
                "expand_simplify",
                difficulties=EXPAND_DIFFICULTIES,
            ),
            d_notes=[
                ("0–1.5", "1 distributed group (+ optional lone constants); no nesting"),
                ("1.5–4", "2 groups — must expand then combine; still flat"),
                ("4–12", "nest_extra ≥ 1 → forms like k(m(ax+b)+c); more groups/lones"),
                ("12+", "deeper nests (nest_extra ≥ 2) and/or more nested groups"),
            ],
        )
    )

    eq_rows = _sample_generator(
        "one_step_equations",
        variants={
            "one_step": {"integers_only": True},
            "one_step_lock_x": {"integers_only": True, "lock_variable": "x"},
        },
    )
    eq_rows2 = _sample_generator(
        "two_step_equations",
        variants={
            "two_step": {"integers_only": True},
            "two_step_lock_x": {"integers_only": True, "lock_variable": "x"},
        },
    )
    for r in eq_rows2:
        r["constraint_set"] = f"two_step/{r['constraint_set']}"
    for r in eq_rows:
        r["constraint_set"] = f"one_step/{r['constraint_set']}"
    written.append(
        write_audit(
            "equations_audit",
            "Equations audit (one- and two-step)",
            "Forced step count by catalog leaf; D drives number/variable complexity.",
            eq_rows + eq_rows2,
            d_notes=[
                ("one_step leaf", "Always one inverse operation"),
                ("two_step leaf", "Always ax + b = c form"),
                ("higher D", "Harder number lanes + negative coeffs"),
            ],
        )
    )

    written.append(
        write_audit(
            "multistep_equations_audit",
            "Multi-step equations audit",
            "Composes shared expand/simplify expressions on each side "
            "(<code>LHS = RHS</code>). Op count grows as "
            "<code>n_ops = 3 + floor(log2(1 + D/2))</code>; expression structure "
            "(groups / nesting) scales with the same D via "
            "<code>sample_linear_expression_to_simplify</code>.",
            _sample_generator(
                "multi_step_equations",
                difficulties=MULTISTEP_DIFFICULTIES,
                variants={
                    "default": {"integers_only": True},
                    "lock_x": {"integers_only": True, "lock_variable": "x"},
                },
            ),
            d_notes=[
                ("0–2", "3 ops: simplify-expression = constant"),
                ("2–6", "4+ ops: variables on both sides (two simplify-expressions)"),
                ("6+", "richer groups / nesting on each side; unbounded"),
            ],
        )
    )

    ineq_rows = _sample_generator(
        "one_step_inequalities",
        variants={
            "one_step": {"integers_only": True},
            "one_step_lock_x": {"integers_only": True, "lock_variable": "x"},
        },
    )
    ineq_rows2 = _sample_generator(
        "two_step_inequalities",
        variants={
            "two_step": {"integers_only": True},
            "two_step_lock_x": {"integers_only": True, "lock_variable": "x"},
        },
    )
    for r in ineq_rows:
        r["constraint_set"] = f"one_step/{r['constraint_set']}"
    for r in ineq_rows2:
        r["constraint_set"] = f"two_step/{r['constraint_set']}"
    written.append(
        write_audit(
            "inequalities_audit",
            "Inequalities audit (one- and two-step)",
            "Same as equations with inequality ops; negative coeffs flip the relation.",
            ineq_rows + ineq_rows2,
            d_notes=[
                ("low D", "Add/subtract one-step"),
                ("mid D", "Multiply/divide; flip when coefficient negative"),
                ("high D", "Harder lanes + non-strict ops"),
            ],
        )
    )

    written.append(
        write_audit(
            "multistep_inequalities_audit",
            "Multi-step inequalities audit",
            "Mirrors multi-step equations with the same "
            "<code>n_ops = 3 + floor(log2(1 + D/2))</code> formula; "
            "flips the inequality when the net variable coefficient is negative.",
            _sample_generator(
                "multi_step_inequalities",
                difficulties=MULTISTEP_DIFFICULTIES,
                variants={
                    "default": {"integers_only": True},
                    "lock_x": {"integers_only": True, "lock_variable": "x"},
                },
            ),
            d_notes=[
                ("0–2", "3 ops: distribute form"),
                ("2–6", "4 ops: both sides"),
                ("6–14", "5 ops: distribute + both sides"),
                ("14+", "6+ ops; flip when leading coeff &lt; 0"),
            ],
        )
    )

    written.append(
        write_audit(
            "factor_gcf_audit",
            "Factor GCF / reverse distributive audit",
            "Reverse of distributive: factor a numeric (or variable) GCF from a sum.",
            _sample_generator("factor_gcf"),
            d_notes=[
                ("0–3", "Two-term numeric GCF, e.g. 6x+9 → 3(2x+3)"),
                ("4–7", "Three terms and/or signed inner terms"),
                ("8+", "variable_gcf: factor gx from ax² + bx […]"),
            ],
        )
    )

    for path in written:
        print(f"Wrote {path}")

    var_script = ROOT / "scripts" / "build_variable_lane_audit.py"
    if var_script.exists():
        env = dict(os.environ)
        env["PYTHONPATH"] = str(ROOT)
        subprocess.run(
            [sys.executable, str(var_script)],
            cwd=str(ROOT),
            check=True,
            env=env,
        )
        print(f"Refreshed {OUT_ROOT / 'variable_lane_audit'}")

    print("Done.")


if __name__ == "__main__":
    main()
