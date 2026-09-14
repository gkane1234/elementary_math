"""AddSubCancel gallery — goal vs cancels vs 2D kernel knobs.

Live default for A1/A2 ± rationals (see primitive_rational.rational_add_subtract).
Opt out with use_constructive_rational=True.

Generates:
  scripts/output/addsub_cancel_gallery/index.html
  scripts/output/addsub_cancel_gallery/gallery.html
  scripts/output/addsub_cancel_gallery/samples.json

Open gallery.html in a browser (KaTeX).
"""

from __future__ import annotations

import json
from html import escape
from pathlib import Path
from typing import Any

from question_engine.frameworks.primitives.rational_skeleton import (
    generate_add_sub_cancel_question,
)

OUT = Path(__file__).resolve().parent
KATEX = "../topic_fit/_assets/katex"

# Grid: k × D-band × kernel force (with auto rows too)
LADDER: list[dict[str, Any]] = []


def _cells() -> list[dict[str, Any]]:
    cells: list[dict[str, Any]] = []
    seed = 100
    # Low D — prefer simple factors / K=0 often
    for k in (0, 1, 2):
        for i in range(3):
            cells.append(
                {
                    "label": f"low D · k={k} · auto kernel",
                    "settings": {
                        "difficulty": 2.0 + 0.5 * i,
                        "seed": seed,
                        "n_factors": 2 if k < 2 or True else 2,
                        "cancel_factor_count": k,
                        "allow_nonmonic": False,
                    },
                }
            )
            seed += 1
    # Mid D — leading a≠1 bias, simple kernel options
    for k in (0, 1, 2):
        for mode in ("zero", "constant", "a0", "full"):
            if k == 0 and mode == "zero":
                pass
            cells.append(
                {
                    "label": f"mid D · k={k} · kernel={mode}",
                    "settings": {
                        "difficulty": 9.0,
                        "seed": seed,
                        "n_factors": 2,
                        "cancel_factor_count": k,
                        "allow_nonmonic": True,
                        "kernel_mode": mode,
                    },
                }
            )
            seed += 1
    # High D — uglier factors, expanded dens, 2D kernel variety
    for k in (0, 1, 2):
        for i in range(4):
            cells.append(
                {
                    "label": f"high D · k={k} · auto",
                    "settings": {
                        "difficulty": 16.0 + i,
                        "seed": seed,
                        "n_factors": 2,
                        "cancel_factor_count": k,
                        "allow_nonmonic": True,
                        "dens_style": "expanded" if i % 2 else "auto",
                    },
                }
            )
            seed += 1
    # Goal showcase: linear/linear like x/(x+2)
    for i in range(6):
        cells.append(
            {
                "label": "goal showcase · prefer linear num",
                "settings": {
                    "difficulty": 4.0 + i,
                    "seed": seed,
                    "n_factors": 2,
                    "cancel_factor_count": 1,
                    "prefer_linear_goal": True,
                    "kernel_mode": "constant",
                    "allow_nonmonic": i >= 3,
                },
            }
        )
        seed += 1
    return cells


def _factor_tex(f: dict) -> str:
    from fractions import Fraction as F

    aF, bF = F(f.get("a", "1")), F(f.get("b", "0"))
    if aF == 1:
        lead = "x"
    elif aF == -1:
        lead = "-x"
    else:
        lead = f"{aF}x"
    if bF == 0:
        return lead
    sign = "+" if bF > 0 else "-"
    return f"{lead} {sign} {abs(bF)}"


def build_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for cell in _cells():
        try:
            r = generate_add_sub_cancel_question(cell["settings"])
            dbg = r.debug_dict()
            rows.append(
                {
                    "ok": True,
                    "label": cell["label"],
                    "settings": cell["settings"],
                    "prompt": r.prompt_latex,
                    "answer": r.answer_latex,
                    "debug": dbg,
                }
            )
        except Exception as exc:  # noqa: BLE001 — gallery should show failures
            rows.append(
                {
                    "ok": False,
                    "label": cell["label"],
                    "settings": cell["settings"],
                    "error": str(exc),
                }
            )
    return rows


def _debug_panel(dbg: dict[str, Any]) -> str:
    kern = dbg.get("kernel") or {}
    cancels = dbg.get("cancel_factors") or []
    remain = dbg.get("remain_factors") or []
    facs = (dbg.get("factors") or {}).get("factors") or []

    def flist(fs: list) -> str:
        if not fs:
            return "(none)"
        return ", ".join(f"${_factor_tex(f)}$" for f in fs)

    rows = [
        ("pattern", dbg.get("pattern")),
        ("D", dbg.get("effective_d")),
        ("goal mode", dbg.get("goal_mode")),
        ("clear factor M", dbg.get("clear_factor", 1)),
        ("scaling", dbg.get("scaling_convention")),
        ("goal / answer", f"${dbg.get('goal_latex', '')}$"),
        ("goal num (scaled)", dbg.get("goal_num")),
        ("goal num (pre-M)", dbg.get("goal_num_unscaled")),
        ("k cancels", dbg.get("cancel_count")),
        ("cancel factors", flist(cancels)),
        ("remain (goal den)", flist(remain)),
        (
            "excluded (cancel only)",
            dbg.get("excluded_values") if dbg.get("excluded_values") else "(none)",
        ),
        ("all factors", flist(facs)),
        ("factor bias", (dbg.get("factors") or {}).get("bias_label")),
        ("dens_style", dbg.get("dens_style")),
        ("package", dbg.get("package_mode")),
        (
            "kernel (a, b)",
            f"$a={kern.get('a', 0)},\\; b={kern.get('b', 0)}$ "
            f"(dim={kern.get('dim')}, $K={kern.get('latex', '0')}$)",
        ),
        ("R num (scaled)", dbg.get("r_num")),
        ("R den", dbg.get("r_den")),
        ("poly part", dbg.get("poly_part")),
        (
            "PF nums (cleared)",
            ", ".join(
                f"{t.get('kind')}: {{{', '.join(f'{k}:{v}' for k,v in (t.get('num') or {}).items())}}}"
                for t in (dbg.get("terms") or [])
            )
            or "(none)",
        ),
    ]
    lis = "".join(
        f"<div class='kv'><span class='k'>{escape(str(k))}</span>"
        f"<span class='v'>{v if isinstance(v, str) and v.startswith('$') else escape(str(v))}</span></div>"
        for k, v in rows
    )
    return f"<div class='debug'>{lis}</div>"


def render_html(rows: list[dict[str, Any]]) -> str:
    cards = []
    for i, row in enumerate(rows, 1):
        if not row.get("ok"):
            cards.append(
                f"<div class='card fail'><header><span class='n'>#{i}</span> "
                f"{escape(row.get('label',''))}</header>"
                f"<pre>{escape(row.get('error',''))}</pre></div>"
            )
            continue
        dbg = row["debug"]
        cards.append(
            f"<div class='card'>"
            f"<header><span class='n'>#{i}</span> "
            f"<strong>{escape(row['label'])}</strong> "
            f"<span class='tag'>k={dbg.get('cancel_count')}</span> "
            f"<span class='tag'>{escape(str(dbg.get('package_mode')))}</span> "
            f"<span class='tag'>K dim={dbg.get('kernel',{}).get('dim')}</span> "
            f"<span class='tag'>M={dbg.get('clear_factor', 1)}</span> "
            f"<span class='tag'>{escape(str((dbg.get('factors') or {}).get('bias_label','')))}</span>"
            f"</header>"
            f"<div class='math'><div class='lab'>Prompt</div>$${row['prompt']}$$</div>"
            f"<div class='math'><div class='lab'>Answer (M·G)</div>$${row['answer']}$$</div>"
            f"{_debug_panel(dbg)}"
            f"</div>"
        )
    body = "\n".join(cards)
    ok_n = sum(1 for r in rows if r.get("ok"))
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<title>AddSubCancel — factor sampler + 2D kernel</title>
<style>
body {{ font-family: Georgia, "Iowan Old Style", serif; margin: 1.25rem 1.75rem;
  background: #f7f5f0; color: #1a1a1a; }}
h1 {{ font-size: 1.35rem; margin-bottom: 0.35rem; }}
.sub {{ color: #555; font-size: 0.9rem; margin-bottom: 1rem; max-width: 48rem; }}
.card {{ background: #fff; border: 1px solid #d8d2c4; padding: 0.75rem 1rem;
  margin-bottom: 0.85rem; max-width: 54rem; }}
.card.fail {{ border-color: #c44; }}
header {{ display: flex; flex-wrap: wrap; gap: 0.45rem; align-items: baseline;
  font-size: 0.88rem; margin-bottom: 0.45rem; }}
.n {{ color: #666; }}
.tag {{ background: #efebe3; padding: 0.1rem 0.4rem; font-size: 0.78rem; }}
.math {{ margin: 0.4rem 0; }}
.lab {{ font-size: 0.75rem; color: #666; text-transform: uppercase; letter-spacing: 0.04em; }}
.debug {{ margin-top: 0.55rem; padding-top: 0.45rem; border-top: 1px dashed #d8d2c4;
  font-size: 0.82rem; }}
.kv {{ display: grid; grid-template-columns: 9.5rem 1fr; gap: 0.25rem 0.75rem; margin: 0.15rem 0; }}
.k {{ color: #666; }}
.v {{ word-break: break-word; }}
code {{ font-size: 0.85em; }}
</style>
<link rel="stylesheet" href="{KATEX}/katex.min.css"/>
<script defer src="{KATEX}/katex.min.js"></script>
<script defer src="{KATEX}/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{{delimiters:[{{left:'$$',right:'$$',display:true}},{{left:'$',right:'$',display:false}}],throwOnError:false}});"></script>
</head><body>
<h1>AddSubCancel — universal factor sampler + 2D residual kernel</h1>
<p class="sub">
<strong>Live default</strong> for A1/A2 add/subtract rational expressions
(<code>rational_expression_simplification</code> /
<code>a2_rational_expressions_adding_and_subtracting</code>).
Opt out with <code>use_constructive_rational=True</code>.
Kernel is multidimensional: $K(x)/D=(a+bx)/D$. Low D biases $K=0$ / simple
($b=0$ or $a=0$); factor hardness is constraint-box + D bias (not cancel count).
Caps: $k\\in\\{{0,1,2\\}}$, $\\deg D\\le 2$.
When PF/kernel numerators are fractional, clear factor $M=\\mathrm{{lcm}}$ of
denominators scales the packaged sum and answer to $M\\cdot G$ (integer coeffs).
Excluded values on the answer are <em>cancelled-factor roots only</em>
(removable holes); poles that remain in the final denominator are omitted.
Generated {ok_n}/{len(rows)} samples. Open this file in a browser.
</p>
{body}
</body></html>
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = build_rows()
    (OUT / "samples.json").write_text(
        json.dumps(rows, indent=2, default=str), encoding="utf-8"
    )
    (OUT / "gallery.html").write_text(render_html(rows), encoding="utf-8")
    (OUT / "index.html").write_text(
        """<!DOCTYPE html><html><head><meta charset="utf-8"/>
<title>AddSubCancel gallery</title></head><body>
<h1>AddSubCancel gallery</h1>
<p><a href="gallery.html">gallery.html</a> (KaTeX) ·
<a href="samples.json">samples.json</a></p>
<p>Regenerate: <code>python scripts/output/addsub_cancel_gallery/gen_examples.py</code></p>
</body></html>
""",
        encoding="utf-8",
    )
    ok = sum(1 for r in rows if r.get("ok"))
    print(f"Wrote {ok}/{len(rows)} samples -> {OUT}")


if __name__ == "__main__":
    main()
