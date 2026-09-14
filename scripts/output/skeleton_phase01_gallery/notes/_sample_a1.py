"""Steps 1–3 for already-skeletoned A1 leaves that still need notes.

Live old-path + default samples. Writes ``notes/<gallery-slug>.md``.
Does not implement engines. Skip if the slug file already has an openstax.org cite
and an old-path section.
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
from question_engine.catalogs.algebra_1 import CATALOG

OUT = Path(__file__).resolve().parent
MINE_EA = _ROOT / "scripts/output/example_mining/elementary-algebra-2e/stage1"
MINE_IA = _ROOT / "scripts/output/example_mining/intermediate-algebra-2e/stage1"

DS = (0.0, 8.0, 16.0, 22.0)
SEEDS = (101, 207)

EA = "https://openstax.org/books/elementary-algebra-2e/pages"
IA = "https://openstax.org/books/intermediate-algebra-2e/pages"

# Already-on-skeleton A1 leaves whose notes were missing at inventory time.
BACKFILL: dict[str, dict[str, Any]] = {
    "absolute_value_equations": {
        "slug": "abs_eq",
        "opt_out": {"use_sample_absolute_value_equation": True},
        "family": "solve",
        "engine": "AbsEquation / equation_skeleton (already wired). Opt-out: `use_sample_absolute_value_equation`.",
        "skill": "Solve an absolute-value equation by splitting $|inner|=k$.",
        "d0": r"$|x|=k$ or $|x+b|=k$ with $a=1$; small positive $k$.",
        "high": r"$|ax+b|=k$ with $|a|\ge 2$; numeric hardness before extra nesting.",
        "must_not": "Inequalities, graphs of $y=|x|$, or quadratic inners.",
        "cites": [
            (
                "OpenStax Intermediate Algebra 2e §2.7",
                f"{IA}/2-7-solve-absolute-value-inequalities",
                r"$|x|=k$; $|x+b|=k$; later $|ax+b|=k$. Same section also covers inequalities — keep this leaf equations-only.",
                "2-7-solve-absolute-value-inequalities.json",
            ),
        ],
    },
    "literal_equations": {
        "slug": "literal",
        "opt_out": {"use_sample_literal_equation": True},
        "family": "solve",
        "engine": "Reuse SolveLiteral / equation_skeleton (already wired). Opt-out: `use_sample_literal_equation`.",
        "skill": "Solve a formula for a specified variable.",
        "d0": r"One-step isolate: $d=rt$, $A=\ell w$, $C=\pi d$.",
        "high": "Multi-term formulas; fractions; isolate a var that is not already alone.",
        "must_not": "Numeric linear equations in one unknown; word-problem stories.",
        "cites": [
            (
                "OpenStax Elementary Algebra 2e §2.6",
                f"{EA}/2-6-solve-a-formula-for-a-specific-variable",
                r"Solve $d=rt$ for $t$; $A=\tfrac12 bh$ for $h$; $P=2L+2W$ for $W$.",
                "2-6-solve-a-formula-for-a-specific-variable.json",
            ),
        ],
    },
    "compound_inequalities": {
        "slug": "compound_ineq",
        "opt_out": {"use_sample_compound_inequality": True},
        "family": "solve",
        "engine": "Reuse CompoundInequality (already wired). Opt-out: `use_sample_compound_inequality`.",
        "skill": "Solve a compound inequality and graph the solution on a number line.",
        "d0": r"Already isolated: $-1<x<2$ or $x<-1$ or $x>1$ (prompt ≈ answer) on a blank number line.",
        "high": "Solve a linear compound first, then graph the isolated form.",
        "must_not": "Single (non-compound) inequalities; abs-value compounds belong on the abs-ineq leaf.",
        "cites": [
            (
                "OpenStax Intermediate Algebra 2e §2.6",
                f"{IA}/2-6-solve-compound-inequalities",
                "And vs or; isolated three-part; then linear sides to isolate.",
                "2-6-solve-compound-inequalities.json",
            ),
        ],
    },
    "absolute_value_inequalities": {
        "slug": "abs_ineq",
        "opt_out": {"use_sample_absolute_value_inequality": True},
        "family": "solve",
        "engine": "Reuse AbsInequality / equation_skeleton (already wired). Opt-out: `use_sample_absolute_value_inequality`.",
        "skill": "Solve an absolute-value inequality; write a compound and graph it.",
        "d0": r"$|x|<k$ or $|x+b|<k$ with $a=1$.",
        "high": r"$|ax+b|\ge k$ with $|a|\ge 2$; number line on the answer.",
        "must_not": "Abs-value *equations*; quadratic inners.",
        "cites": [
            (
                "OpenStax Intermediate Algebra 2e §2.7",
                f"{IA}/2-7-solve-absolute-value-inequalities",
                r"Less-than → and; greater-than → or. $|x|<2$ then $|ax+b|\ge k$.",
                "2-7-solve-absolute-value-inequalities.json",
            ),
        ],
    },
    "polynomial_multiply": {
        "slug": "multiply",
        "opt_out": {"use_factor_poly": True},
        "family": "other",
        "engine": "Reuse FactorProduct multiply task / poly_skeleton (already wired). Opt-out: `use_factor_poly`.",
        "skill": "Multiply polynomials (distribute / FOIL) and write the expanded product.",
        "d0": "Monomial×binomial or two linear binomials.",
        "high": "Binomial×trinomial; larger coeffs. Special-product identities stay on the special-multiply leaf.",
        "must_not": "Factoring prompts; PolyAddSub.",
        "cites": [
            (
                "OpenStax Elementary Algebra 2e §6.3",
                f"{EA}/6-3-multiply-polynomials",
                "Monomial×poly; FOIL two binomials; then (binomial)(trinomial).",
                "6-3-multiply-polynomials.json",
            ),
        ],
    },
    "polynomial_multiply_special": {
        "slug": "multiply_special",
        "opt_out": {"use_factor_poly": True},
        "family": "other",
        "engine": "Reuse FactorProduct special multiply / poly_skeleton (already wired). Opt-out: `use_factor_poly`.",
        "skill": "Multiply special products: $(a\\pm b)^2$ and difference of squares.",
        "d0": r"$(x\pm b)^2$ or $(x-a)(x+a)$ with small ints.",
        "high": r"$(ax\pm b)^2$; larger coeffs. Keep the identity visible — not a generic FOIL mixer.",
        "must_not": "Generic multiply; factoring the result as the prompt.",
        "cites": [
            (
                "OpenStax Elementary Algebra 2e §6.4",
                f"{EA}/6-4-special-products",
                r"$(a+b)^2$, $(a-b)^2$, $(a-b)(a+b)$.",
                None,
            ),
        ],
    },
    "polynomial_factoring_special_cases": {
        "slug": "factor_special",
        "opt_out": {"use_factor_poly": True},
        "family": "other",
        "engine": "Reuse FactorProduct special factor / poly_skeleton (already wired). Opt-out: `use_factor_poly`.",
        "skill": "Factor difference of squares or a perfect-square trinomial.",
        "d0": r"$x^2-c^2$ or $x^2\pm 2bx+b^2$ (a=1).",
        "high": r"$a^2x^2-c^2$ / non-monic perfect squares. Cubes are A2, not this A1 leaf.",
        "must_not": "Generic $x^2+bx+c$ that is not a special product; grouping four-terms.",
        "cites": [
            (
                "OpenStax Elementary Algebra 2e §7.4",
                f"{EA}/7-4-factor-special-products",
                "Difference of squares; perfect-square trinomials.",
                "7-4-factor-special-products.json",
            ),
        ],
    },
    "polynomial_factoring_grouping": {
        "slug": "factor_grouping",
        "opt_out": {"use_factor_poly": True},
        "family": "other",
        "engine": "Reuse FactorProduct grouping / poly_skeleton (already wired). Opt-out: `use_factor_poly`.",
        "skill": "Factor a four-term polynomial by grouping.",
        "d0": "Four terms, degree ≤2 in each pair; small ints; GCF of each pair is obvious.",
        "high": "Larger coeffs; degree up to 3. Not a quadratic trinomial.",
        "must_not": "Monic $x^2+bx+c$; GCF-only binomials.",
        "cites": [
            (
                "OpenStax Elementary Algebra 2e §7.1",
                f"{EA}/7-1-greatest-common-factor-and-factor-by-grouping",
                "Four-term grouping after (optional) monomial GCF.",
                None,
            ),
        ],
    },
    "quadratic_factoring": {
        "slug": "factor_quadratic",
        "opt_out": {"use_factor_poly": True},
        "family": "other",
        "engine": "Reuse FactorProduct quadratic / poly_skeleton (already wired). Opt-out: `use_factor_poly`.",
        "skill": "Factor a quadratic trinomial.",
        "d0": r"Monic $x^2+bx+c$ with small factor pairs.",
        "high": r"$a\neq 1$ (ac method); unsimplified stems later. Always degree 2.",
        "must_not": "Four-term grouping; solve-by-factoring equations (that is `quadratic_factoring_equations`).",
        "cites": [
            (
                "OpenStax Elementary Algebra 2e §7.2",
                f"{EA}/7-2-factor-trinomials-of-the-form-x2-bx-c",
                r"$x^2+bx+c$ with $a=1$.",
                None,
            ),
            (
                "OpenStax Elementary Algebra 2e §7.3",
                f"{EA}/7-3-factor-trinomials-of-the-form-ax2-bx-c",
                r"$ax^2+bx+c$ with $a\neq 1$.",
                None,
            ),
        ],
    },
    "polynomial_factoring_general_strategy": {
        "slug": "factor_all_techniques",
        "opt_out": {"use_factor_poly": True},
        "family": "other",
        "engine": "Reuse FactorProduct all-techniques mixer / poly_skeleton (already wired). Opt-out: `use_factor_poly`.",
        "skill": "Choose a factoring method and factor completely (GCF, trinomial, special, grouping).",
        "d0": "GCF-only or a simple monic trinomial — one obvious method.",
        "high": "D-weighted mix; GCF then a pattern; grouping. Still A1 methods (no cubes-only A2).",
        "must_not": "A dedicated single-method leaf’s exclusive shape at every D (mixer must actually mix at high D).",
        "cites": [
            (
                "OpenStax Elementary Algebra 2e §7.5",
                f"{EA}/7-5-general-strategy-for-factoring-polynomials",
                "Choose method / factor completely — GCF first, then pattern.",
                None,
            ),
        ],
    },
    "quadratic_factoring_equations": {
        "slug": "factor_equations",
        "opt_out": {"use_factor_poly": True},
        "family": "other",
        "engine": "Reuse FactorProduct solve-by-factoring / poly_skeleton (already wired). Opt-out: `use_factor_poly`.",
        "skill": "Solve a quadratic equation by factoring (zero-product property).",
        "d0": r"Monic $x^2+bx+c=0$ already set to zero.",
        "high": r"$a\neq 1$; rearrange to $=0$ first; unsimplified stems later. Always degree 2.",
        "must_not": "Grouping four-terms; quadratic formula; graphing.",
        "cites": [
            (
                "OpenStax Elementary Algebra 2e §7.6",
                f"{EA}/7-6-quadratic-equations",
                r"Set $=0$, factor, zero-product. $x^2+7x+12=0$ then $a\neq 1$.",
                "7-6-quadratic-equations.json",
            ),
        ],
    },
    "rational_simplification": {
        "slug": "simplify_cancel",
        "opt_out": {"use_constructive_rational": True},
        "family": "other",
        "engine": "Reuse SimplifyCancel / rational_skeleton (already wired). Opt-out: `use_constructive_rational`.",
        "skill": "Simplify a single rational expression and state excluded values.",
        "d0": "Cancel a linear common factor; monomial or simple binomial dens.",
        "high": "Quadratic factors; more excluded values. Not add/subtract unlike dens.",
        "must_not": "Add/subtract two rationals; complex fractions (A2 leaf).",
        "cites": [
            (
                "OpenStax Elementary Algebra 2e §8.1",
                f"{EA}/8-1-simplify-rational-expressions",
                "Factor numerator and denominator; cancel; state $x\neq$ excluded.",
                "8-1-simplify-rational-expressions.json",
            ),
        ],
    },
    "rational_expression_simplification": {
        "slug": "add_sub_cancel",
        "opt_out": {"use_constructive_rational": True},
        "family": "other",
        "engine": "Reuse AddSubCancel / rational_skeleton (already wired). Opt-out: `use_constructive_rational`.",
        "skill": "Add or subtract rational expressions and simplify.",
        "d0": "Like denominators, linear; combine numerators.",
        "high": "Unlike dens / LCD of polynomials; cancel after combining.",
        "must_not": "Single-fraction simplify-only; multiply/divide.",
        "cites": [
            (
                "OpenStax Elementary Algebra 2e §8.3",
                f"{EA}/8-3-add-and-subtract-rational-expressions-with-a-common-denominator",
                "Common denominator; combine numerators.",
                "8-3-add-and-subtract-rational-expressions-with-a-common-denominator.json",
            ),
            (
                "OpenStax Elementary Algebra 2e §8.4",
                f"{EA}/8-4-add-and-subtract-rational-expressions-with-unlike-denominators",
                "LCD of polynomial dens; then simplify.",
                None,
            ),
        ],
    },
    "rational_expression_multiply_divide": {
        "slug": "mul_div_cancel",
        "opt_out": {"use_hand_muldiv": True},
        "family": "other",
        "engine": "Reuse MulDivCancel / rational_skeleton (already wired). Opt-out: `use_hand_muldiv` (or `use_constructive_rational`).",
        "skill": "Multiply or divide rational expressions and cancel.",
        "d0": "Linear×linear with an obvious cancel; or divide by taking a reciprocal.",
        "high": "Quadratic factors; cancel across operands. Remain degree ≤ 2.",
        "must_not": "Add/subtract; complex fractions.",
        "cites": [
            (
                "OpenStax Elementary Algebra 2e §8.2",
                f"{EA}/8-2-multiply-and-divide-rational-expressions",
                "Factor, cancel across ×; divide = multiply by reciprocal.",
                "8-2-multiply-and-divide-rational-expressions.json",
            ),
        ],
    },
    "rational_expressions_equations": {
        "slug": "eq_cancel",
        "opt_out": {"use_hand_rational_equations": True},
        "family": "other",
        "engine": "Reuse EqCancel / rational_skeleton (already wired). Opt-out: `use_hand_rational_equations`.",
        "skill": "Solve a rational equation; check extraneous solutions.",
        "d0": "A proportion (two fractions).",
        "high": "One linear denominator, then LCD, then extraneous check.",
        "must_not": "Simplify-an-expression (no equation); mixture/DRT story dumps.",
        "cites": [
            (
                "OpenStax Elementary Algebra 2e §8.6",
                f"{EA}/8-6-solve-rational-equations",
                "Clear dens; proportion first; extraneous values.",
                None,
            ),
            (
                "OpenStax Elementary Algebra 2e §8.7",
                f"{EA}/8-7-solve-proportion-and-similar-figure-applications",
                "Proportion shape at D=0 — applications stay on WP leaves.",
                "8-7-solve-proportion-and-similar-figure-applications.json",
            ),
        ],
    },
}

_CATALOG = {e.id: e for e in CATALOG}


def _mine_path(fname: str) -> Path | None:
    for root in (MINE_EA, MINE_IA):
        p = root / fname
        if p.exists():
            return p
    return None


def _extract_examples(fname: str, limit: int = 3) -> list[str]:
    path = _mine_path(fname)
    if path is None:
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    out: list[str] = []
    for item in data.get("items") or []:
        if item.get("kind") != "example":
            continue
        title = (item.get("title") or "").strip()
        prompt = re.sub(r"\s+", " ", (item.get("prompt_text") or "").strip())
        if "If you missed" in prompt:
            continue
        if len(prompt) > 220:
            prompt = prompt[:217] + "…"
        if title and prompt:
            out.append(f"{title}: {prompt}")
        elif prompt:
            out.append(prompt)
        if len(out) >= limit:
            break
    return out


def _math(s: str) -> str:
    s = (s or "").strip()
    s = re.sub(r"\s+", " ", s)
    if not s:
        return "_(empty)_"
    if "$" in s:
        return s
    return f"${s}$"


def _clip(s: str, n: int = 360) -> str:
    s = re.sub(r"\s+", " ", (s or "").strip())
    return s if len(s) <= n else s[: n - 1] + "…"


def _meta_bits(q) -> str:
    meta = getattr(q, "metadata", None) or {}
    bits = []
    fid = meta.get("form_id") or ""
    pat = meta.get("skeleton_pattern") or ""
    if fid:
        bits.append(f"form_id={fid}")
    if pat:
        bits.append(f"pattern={pat}")
    if meta.get("number_line_spec") or meta.get("figure") or meta.get("diagram"):
        bits.append("has_figure")
    return ", ".join(bits)


def sample_one(type_id: str, extra: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for d in DS:
        for seed in SEEDS:
            settings = {
                "difficulty": d,
                "seed": seed,
                "count": 1,
                "include_answer_key": True,
                **extra,
            }
            try:
                qs = _generate_for_type(type_id, settings)
                q = qs[0]
                rows.append(
                    {
                        "d": d,
                        "seed": seed,
                        "prompt": q.prompt_latex or q.prompt_text or "",
                        "answer": q.answer_latex or "",
                        "bits": _meta_bits(q),
                    }
                )
            except Exception as exc:  # noqa: BLE001
                rows.append({"d": d, "seed": seed, "error": str(exc)})
    return rows


def _rows_md(rows: list[dict[str, Any]]) -> list[str]:
    lines: list[str] = []
    for row in rows:
        d = row["d"]
        dlab = int(d) if d == int(d) else d
        if row.get("error"):
            lines.append(f"- **D={dlab} seed={row['seed']}:** **ERROR** `{_clip(row['error'], 200)}`")
            continue
        extra = f" — {row['bits']}" if row.get("bits") else ""
        lines.append(
            f"- **D={dlab} seed={row['seed']}:** {_math(_clip(row.get('prompt') or ''))} "
            f"→ {_math(_clip(str(row.get('answer') or ''), 200))}{extra}"
        )
    return lines


def _has_filled_notes(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    return "openstax.org" in text and "What old path actually produced" in text


def render_notes(type_id: str, spec: dict[str, Any], old: list[dict], default: list[dict]) -> str:
    entry = _CATALOG[type_id]
    slug = spec["slug"]
    opt = spec["opt_out"]
    opt_key = next(iter(opt))
    flags: list[str] = []
    dumpish = any(
        "the equation is" in ((r.get("prompt") or "").lower())
        for r in old
        if not r.get("error")
    )
    if dumpish:
        flags.append("LOW_VARIETY")
    flag_block = "- " + ", ".join(f"`{f}`" for f in flags) if flags else "- _(none)_"
    aliases = [type_id]
    cites_md: list[str] = []
    for cite, url, shape, mine in spec["cites"]:
        cites_md.append(f"| {cite} | {url} | {shape} |")
        if mine:
            # Shape cites only — do not dump mined example wording (copyright).

    lines = [
        f"# Notes — `{slug}` (`{type_id}`)",
        "",
        f"Also covers: {', '.join(f'`{a}`' for a in aliases)}",
        "",
        "Flags:",
        "",
        flag_block,
        "",
        "---",
        "",
        "## What the question should look like (D=0 vs high D)",
        "",
        f"- **Skill:** {spec['skill']}",
        f"- **D=0:** {spec['d0']}",
        f"- **High D (≈16–22):** {spec['high']}",
        f"- **Must not:** {spec['must_not']}",
        "",
        "## What old path actually produced (real latex, D=0/8/16/22)",
        "",
        f"Live `_generate_for_type` with `{opt_key}=True`.",
        "",
        * _rows_md(old),
        "",
        f"Opt-out flag used: `{opt_key}=True`",
        "",
        "## Current default (same D/seeds)",
        "",
        * _rows_md(default),
        "",
        "## OpenStax examples + chapter/section cites",
        "",
        "Paraphrase stems; cite book + chapter/section + URL. Do not dump copyrighted problem text wholesale.",
        "",
        "| Cite | URL | What to copy (shape / frame, not wording) |",
        "|------|-----|-------------------------------------------|",
        *cites_md,
        "",
        "Local HTML (if mined): `textbooks/openstax/html/elementary-algebra-2e/` or `intermediate-algebra-2e/`.",
        "",
        "## Variety notes / UNCLEAR flag",
        "",
        "Not a WP. Algebra shapes follow the old path; default is the live skeleton.",
        "Flag UNCLEAR only if old path is a dump stub or the skill is wrong.",
        "",
        "## Proposed engine (reuse vs new) — proposal only",
        "",
        f"- **Reuse:** {spec['engine']}",
        "- **New:** not this pass (already on skeleton).",
        "- **Not this pass:** do not re-implement generators.",
        "",
        f"Suggested family from `A1_INDEX.md`: `{spec['family']}`",
        "",
        f"_Catalog:_ {entry.category} — {entry.name}. Generator `{entry.generator}`.",
        "",
    ]
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def main() -> None:
    summary: dict[str, Any] = {"written": [], "skipped": [], "errors": {}}
    samples: dict[str, Any] = {}
    for type_id, spec in BACKFILL.items():
        path = OUT / f"{spec['slug']}.md"
        if _has_filled_notes(path):
            summary["skipped"].append(type_id)
            continue
        old = sample_one(type_id, spec["opt_out"])
        default = sample_one(type_id, {})
        errs = [r["error"] for r in old + default if r.get("error")]
        if errs:
            summary["errors"][type_id] = errs
        samples[type_id] = {"slug": spec["slug"], "old": old, "default": default}
        path.write_text(render_notes(type_id, spec, old, default), encoding="utf-8")
        summary["written"].append({"type_id": type_id, "path": path.name})
        print(f"wrote {path.name} ({type_id})", flush=True)

    (OUT / "_a1_backfill_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2)[:2000])


if __name__ == "__main__":
    main()
