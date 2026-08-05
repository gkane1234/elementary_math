"""Build a hand-rating package (JSONL + HTML rater) for a course campaign.

Default campaign: calculus derivatives (Spec packs). Gap packs
(other_base / logarithmic / implicit) use ``calc_diff_gaps`` so the rated
``calc_derivatives`` set is not overwritten. Sibling campaigns
(algebra_1 / algebra_2 / precalc_algebraic) read pack plans from CAMPAIGN.json.

Usage:
  $env:PYTHONPATH='.'
  python scripts/build_hand_rating_set.py --campaign calc_derivatives
  python scripts/build_hand_rating_set.py --campaign calc_derivatives --smoke
  python scripts/build_hand_rating_set.py --campaign calc_diff_gaps --smoke
  python scripts/build_hand_rating_set.py --campaign algebra_1 --smoke
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import question_engine.types  # noqa: F401
from question_engine.api.handler import _generate_for_type
from question_engine.ml.effort import has_effort_scorer, score_effort
from question_engine.ml.features import record_feature_dict
from question_engine.ml.schema import build_generation_record

import importlib.util

_katex_spec = importlib.util.spec_from_file_location(
    "topic_fit_katex", ROOT / "scripts" / "topic_fit_katex.py"
)
_katex_mod = importlib.util.module_from_spec(_katex_spec)
assert _katex_spec.loader is not None
_katex_spec.loader.exec_module(_katex_mod)

RATINGS_ROOT = ROOT / "scripts" / "output" / "ml" / "ratings"

DIFFICULTIES = (0.0, 3.0, 6.0, 8.0, 12.0, 16.0, 20.0, 25.0)

# Stratified pack plan → ~360 items (8 D × n_per_d per pack).
CALC_DERIVATIVE_PACKS: list[dict[str, Any]] = [
    {
        "pack": "power",
        "type_id": "calc_diff_power_rule",
        "generator": "derivative_power_rule",
        "n_per_d": 6,
        "openstax": "3.3 power / sum / negative exponents",
    },
    {
        "pack": "product",
        "type_id": "calc_diff_product_rule",
        "generator": "derivative_product_rule",
        "n_per_d": 5,
        "openstax": "3.3 product rule",
    },
    {
        "pack": "quotient",
        "type_id": "calc_diff_quotient_rule",
        "generator": "derivative_quotient_rule",
        "n_per_d": 5,
        "openstax": "3.3 quotient rule",
    },
    {
        "pack": "chain",
        "type_id": "calc_diff_chain_rule",
        "generator": "derivative_chain_rule",
        "n_per_d": 6,
        "openstax": "3.6 chain rule",
    },
    {
        "pack": "trig",
        "type_id": "calc_diff_trigonometric",
        "generator": "derivative_trigonometric",
        "n_per_d": 5,
        "openstax": "3.5 trig derivatives",
    },
    {
        "pack": "ln_exp",
        "type_id": "calc_diff_natural_logarithms_and_exponentials",
        "generator": "derivative_ln_exp",
        "n_per_d": 5,
        "openstax": "3.9 ln / exp",
    },
    {
        "pack": "invtrig",
        "type_id": "calc_diff_inverse_trigonometric",
        "generator": "derivative_inverse_trig",
        "n_per_d": 4,
        "openstax": "3.7 / invtrig forms (OpenStax + extensions)",
    },
    {
        "pack": "general",
        "type_id": "calc_diff_general",
        "generator": "derivative_general",
        "n_per_d": 5,
        "openstax": "mixed rules (combined textbook exercises)",
    },
    {
        "pack": "higher_order",
        "type_id": "calc_diff_higher_order_derivatives",
        "generator": "derivative_higher_order",
        "n_per_d": 4,
        "openstax": "higher-order (Spec path; order≥2)",
    },
]

# Separate campaign — do not merge into rated calc_derivatives items.jsonl.
CALC_GAP_PACKS: list[dict[str, Any]] = [
    {
        "pack": "other_base",
        "type_id": "calc_diff_other_base_logarithms_and_exponentials",
        "generator": "derivative_other_base",
        "n_per_d": 4,
        "openstax": "3.9 other-base a^x / log_a (structured pack)",
    },
    {
        "pack": "logarithmic",
        "type_id": "calc_diff_logarithmic",
        "generator": "derivative_logarithmic",
        "n_per_d": 4,
        "openstax": "logarithmic differentiation (structured pack)",
    },
    {
        "pack": "implicit",
        "type_id": "calc_diff_implicit",
        "generator": "derivative_implicit",
        "n_per_d": 4,
        "openstax": "implicit differentiation (structured pack)",
    },
]

SCAFFOLD_CAMPAIGNS = (
    "algebra_1",
    "algebra_2",
    "precalc_algebraic",
    "calc_limits",
    "calc_integrals",
)

ALL_CAMPAIGNS = ("calc_derivatives", "calc_diff_gaps", *SCAFFOLD_CAMPAIGNS)

# Default expression-ish leaves for non-calc campaigns (override via CAMPAIGN.json packs).
_DEFAULT_CAMPAIGN_PACKS: dict[str, list[dict[str, Any]]] = {
    "algebra_1": [
        {
            "pack": "poly_simplify",
            "type_id": "simplify_polynomials",
            "generator": "simplify_polynomials",
            "n_per_d": 3,
            "openstax": "A1 simplify polynomials",
        },
        {
            "pack": "quadratic_factoring",
            "type_id": "quadratic_factoring",
            "generator": "quadratic_factoring",
            "n_per_d": 3,
            "openstax": "A1 quadratic factoring",
        },
        {
            "pack": "rational_simplify",
            "type_id": "rational_simplification",
            "generator": "rational_simplification",
            "n_per_d": 3,
            "openstax": "A1 simplify rationals",
        },
    ],
    "algebra_2": [
        {
            "pack": "rational_simplify",
            "type_id": "a2_rational_expressions_simplifying",
            "generator": "rational_simplification",
            "n_per_d": 3,
            "openstax": "A2 rational expressions simplifying",
        },
        {
            "pack": "rational_add",
            "type_id": "a2_rational_expressions_adding_and_subtracting",
            "generator": "rational_expression_simplification",
            "n_per_d": 3,
            "openstax": "A2 rational add/subtract",
        },
        {
            "pack": "function_ops",
            "type_id": "a2_general_functions_operations",
            "generator": "function_operations",
            "n_per_d": 3,
            "openstax": "A2 function operations",
        },
    ],
    "precalc_algebraic": [
        {
            "pack": "log_props",
            "type_id": "pc_properties_of_logarithms",
            "generator": "log_change_of_base",
            "n_per_d": 3,
            "openstax": "Precalc properties of logarithms",
        },
        {
            "pack": "power_rule",
            "type_id": "pc_power_rule_for_differentiation",
            "generator": "derivative_power_rule",
            "n_per_d": 3,
            "openstax": "Precalc intro-calc power rule",
        },
        {
            "pack": "pfd",
            "type_id": "pc_partial_fraction_decomposition",
            "generator": "partial_fraction_decomposition",
            "n_per_d": 3,
            "openstax": "Precalc PFD (construct_pfd)",
        },
    ],
    "calc_limits": [
        {
            "pack": "direct",
            "type_id": "calc_limits_by_direct_evaluation",
            "generator": "limit_direct_evaluation",
            "n_per_d": 3,
            "openstax": "Calc 1 algebraic limits (direct)",
        },
        {
            "pack": "removable",
            "type_id": "calc_limits_at_removable_discontinuities",
            "generator": "limit_removable",
            "n_per_d": 3,
            "openstax": "Calc 1 removable",
        },
        {
            "pack": "infinity",
            "type_id": "calc_limits_at_infinity",
            "generator": "limit_at_infinity",
            "n_per_d": 3,
            "openstax": "Calc 1 limits at infinity",
        },
        {
            "pack": "lhopital",
            "type_id": "calc_app_diff_lhopitals_rule",
            "generator": "lhopitals_rule",
            "n_per_d": 3,
            "openstax": "Calc 1 L'Hôpital",
        },
    ],
    "calc_integrals": [
        {
            "pack": "power",
            "type_id": "calc_indef_int_power_rule",
            "generator": "integral_power_rule",
            "n_per_d": 3,
            "openstax": "Calc 1 power-rule integrals",
        },
        {
            "pack": "u_sub",
            "type_id": "calc_indef_int_power_rule_with_substitution",
            "generator": "integral_substitution",
            "n_per_d": 3,
            "openstax": "Calc 1 derivative-backed u-sub",
        },
        {
            "pack": "pfd",
            "type_id": "calc_indef_int_partial_fractions",
            "generator": "integral_partial_fractions",
            "n_per_d": 3,
            "openstax": "Calc 1 PFD via partial_fractions facade",
        },
        {
            "pack": "multi_u_pfd",
            "type_id": "calc_indef_int_multi_trick",
            "generator": "integral_multi_trick",
            "n_per_d": 3,
            "openstax": "Calc 1 u_sub→pfd pipeline",
        },
        {
            "pack": "linear_approx",
            "type_id": "calc_app_diff_linear_approximations",
            "generator": "linear_approximation",
            "n_per_d": 2,
            "openstax": "Calc 1 linear approximations",
        },
    ],
}


def _seed_for(pack: str, type_id: str, d: float, i: int, seed_base: int) -> int:
    return (
        seed_base
        + int(d * 1000)
        + i * 17
        + (hash(f"{pack}:{type_id}") % 9973)
    ) % 2_000_000_000


def _generate_row(
    *,
    rating_id: str,
    pack: str,
    type_id: str,
    generator_hint: str,
    difficulty: float,
    seed: int,
    openstax: str,
) -> dict[str, Any]:
    try:
        questions = _generate_for_type(
            type_id,
            {
                "difficulty": difficulty,
                "count": 1,
                "include_answer_key": True,
                "seed": seed,
            },
        )
    except Exception as exc:  # noqa: BLE001
        return {
            "rating_id": rating_id,
            "pack": pack,
            "type_id": type_id,
            "generator": generator_hint,
            "seed": seed,
            "difficulty": difficulty,
            "openstax_ref": openstax,
            "error": f"{type(exc).__name__}: {exc}",
            "rating_1_to_5": None,
            "minutes": None,
            "notes": None,
        }

    question = questions[0]
    settings = (question.metadata or {}).get("generation_settings") or {
        "difficulty": difficulty,
        "seed": seed,
    }
    y_effort = None
    y_mode = None
    effort_feats: dict[str, Any] = {}
    prompt = (question.prompt_latex or question.prompt_text or "").strip()
    answer = (question.answer_latex or question.answer_text or "").strip()
    if has_effort_scorer(type_id):
        y_effort, effort_feats = score_effort(type_id, prompt, answer)
        if isinstance(effort_feats, dict):
            raw_mode = effort_feats.get("form") or effort_feats.get("mode")
            y_mode = str(raw_mode) if raw_mode is not None else None

    record = build_generation_record(
        type_id,
        question,
        settings,
        y_effort=y_effort,
        y_mode=y_mode,
        effort_feats=effort_feats,
    )
    row = record.to_dict()
    meta = row.get("metadata") or {}
    generator = meta.get("generator") or row.get("theta_full", {}).get("generator") or generator_hint
    row.update(
        {
            "rating_id": rating_id,
            "pack": pack,
            "generator": generator,
            "openstax_ref": openstax,
            "spec_snapshot": meta.get("spec_snapshot")
            or (row.get("structural_features") or {}).get("spec_snapshot"),
            "function_classes": meta.get("function_classes"),
            "methods_used": meta.get("methods_used"),
            "effort_features": meta.get("effort_features"),
            "shape_id": meta.get("shape_id"),
            "structure_id": meta.get("structure_id"),
            "chain_depth": meta.get("chain_depth"),
            "feature_preview": {
                k: v
                for k, v in record_feature_dict(record).items()
                if k.startswith(("allow_", "require_", "spec_", "ast_ef_", "function_classes", "methods_used"))
                or k in {"difficulty", "chain_depth", "derivative_order", "generator", "shape_id"}
            },
        }
    )
    # Ensure human fields present (null until rated).
    row["rating_1_to_5"] = None
    row["minutes"] = None
    row["notes"] = None
    return row


def generate_pack_rows(
    packs: list[dict[str, Any]],
    *,
    seed_base: int,
    smoke: bool,
    rating_id_prefix: str,
) -> list[dict[str, Any]]:
    diffs = DIFFICULTIES
    active = packs
    if smoke:
        active = packs[: min(3, len(packs))]
        diffs = (0.0, 12.0, 25.0)
    rows: list[dict[str, Any]] = []
    n = 0
    for pack_cfg in active:
        n_per = 1 if smoke else int(pack_cfg["n_per_d"])
        for d in diffs:
            for i in range(n_per):
                n += 1
                seed = _seed_for(pack_cfg["pack"], pack_cfg["type_id"], d, i, seed_base)
                rating_id = (
                    f"{rating_id_prefix}_{pack_cfg['pack']}_d{int(d):02d}_{i:02d}_s{seed}"
                )
                row = _generate_row(
                    rating_id=rating_id,
                    pack=pack_cfg["pack"],
                    type_id=pack_cfg["type_id"],
                    generator_hint=pack_cfg["generator"],
                    difficulty=float(d),
                    seed=seed,
                    openstax=str(pack_cfg.get("openstax") or ""),
                )
                rows.append(row)
                if n % 25 == 0:
                    print(f"  … {n} items", flush=True)
    return rows


def generate_calc_derivatives(*, seed_base: int, smoke: bool) -> list[dict[str, Any]]:
    return generate_pack_rows(
        CALC_DERIVATIVE_PACKS,
        seed_base=seed_base,
        smoke=smoke,
        rating_id_prefix="calc_deriv",
    )


def generate_calc_gaps(*, seed_base: int, smoke: bool) -> list[dict[str, Any]]:
    return generate_pack_rows(
        CALC_GAP_PACKS,
        seed_base=seed_base,
        smoke=smoke,
        rating_id_prefix="calc_gap",
    )


def _load_campaign_packs(campaign: str, out_dir: Path) -> list[dict[str, Any]]:
    """Load packs from CAMPAIGN.json when present; else defaults."""
    stub = out_dir / "CAMPAIGN.json"
    if stub.is_file():
        try:
            data = json.loads(stub.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {}
        packs = data.get("packs") if isinstance(data, dict) else None
        if isinstance(packs, list) and packs:
            out: list[dict[str, Any]] = []
            for p in packs:
                if not isinstance(p, dict) or not p.get("type_id"):
                    continue
                out.append(
                    {
                        "pack": str(p.get("pack") or p["type_id"]),
                        "type_id": str(p["type_id"]),
                        "generator": str(p.get("generator") or p["type_id"]),
                        "n_per_d": int(p.get("n_per_d") or 3),
                        "openstax": str(p.get("openstax") or ""),
                    }
                )
            if out:
                return out
    return list(_DEFAULT_CAMPAIGN_PACKS.get(campaign) or [])


def write_coverage_checklist(out_dir: Path) -> None:
    text = """# OpenStax Calc Vol 1 — derivatives coverage checklist

Grounded in stage-1 mining under
`scripts/output/example_mining/calculus-volume-1/stage1/` and generator packs
in `question_engine/frameworks/primitives/derivatives.py` /
`poly_expression.py`.

| Form / skill (OpenStax-informed) | Pack / type_id | Status |
|----------------------------------|----------------|--------|
| Constant / constant-multiple / power | `power` / `calc_diff_power_rule` | Covered |
| Sum / difference of powers | `power` | Covered |
| Negative integer exponents | `power` (D unlock + `allow_negative_exponents` Spec) | Covered (D-gated) |
| Fractional / root exponents | `power` (`allow_roots` / fractional Spec) | Covered (D-gated) |
| Irrational exponents (π, e, √2) | Spec `allow_irrational_exponents` | Partial — unlocks at high D; sparse in rating sweep |
| Product rule (poly × poly) | `product` | Covered |
| Product with specials | `product` / `trig` / `ln_exp` / `general` | Covered when allow_* on |
| Quotient rule | `quotient` | Covered (legacy atom path; `spec_snapshot.pack=legacy_quotient`) |
| Chain rule algebraic `(ax+b)^n` | `chain` | Covered |
| Chain with trig / ln / exp | `chain`, `trig`, `ln_exp` | Covered |
| Nested chain depth ≥2 | `chain` / `general` (D≥~14) | Covered (D-gated) |
| Trig derivatives (sin/cos/tan…) | `trig` | Covered |
| Trig × product / quotient | `trig` | Covered when methods allowed |
| Inverse trig | `invtrig` | Covered |
| Natural ln / exp | `ln_exp` | Covered |
| Other-base log / exp (aˣ, log_a) | `calc_diff_other_base_…` | Structured pack — use `calc_diff_gaps` campaign |
| Logarithmic differentiation | `calc_diff_logarithmic` | Structured pack — use `calc_diff_gaps` campaign |
| Implicit differentiation | `calc_diff_implicit` | Structured pack — use `calc_diff_gaps` campaign |
| Higher-order derivatives | `higher_order` | Covered via Spec (order≥2; soft trig/exp) |
| Definition of derivative | `calc_diff_definition_…` | Gap — out of scope for this pack |
| Rates of change / tables | rates / tables leaves | Gap — out of scope |
| Function powers e.g. tan²(x) | Spec `allow_fn_power` via chain/general/trig | Covered (D≥6) |
| Exotic / mixed general | `general` | Covered |
| Hyperbolic | allow_hyperbolic | Gap — rarely unlocked; not stratified here |

## Gaps intentionally left open

1. **definition / rates / tables** — separate campaigns later (thin Mad-Libs still).
2. **other_base / logarithmic / implicit** — generator ML plumbing ready; build via
   `python scripts/build_hand_rating_set.py --campaign calc_diff_gaps` (does **not**
   overwrite rated `calc_derivatives` items).
3. **Irrational / hyperbolic / deep exotic** — present in knobs but low density at
   default allow-lists; optional follow-up sweep with forced knobs.
4. Full pre-algebra Spec unification is **not** required for this rating push.
5. **higher_order** Spec migration: existing rated Mad-Libs rows keep join keys
   (`rating_id` / type / seed / D) as historical labels; live regen may differ.

## Seed join note

Spec sampling sorts frozenset/class token iteration so `PYTHONHASHSEED` cannot
reshuffle prompts for the same `(type_id, seed, difficulty)`. Rebuild the JSONL
after generator changes before rating if prompts must match live regen.
"""
    (out_dir / "COVERAGE.md").write_text(text, encoding="utf-8")


def write_readme(out_dir: Path, *, n_rows: int, n_err: int, strat: dict[str, Any]) -> None:
    text = f"""# Calc derivatives — hand rating package

Generated for human effort / quality ratings. Machine fields are complete;
human fields start null.

## Files

| File | Role |
|------|------|
| `rater.html` | Open locally (KaTeX). Enter ratings; autosaves to localStorage; export JSON. |
| `items.jsonl` | Full machine rows (θ, Spec snapshot, prompts, metadata). |
| `items.json` | Same rows as a JSON array (loaded by the rater). |
| `INDEX.json` | Stratification counts + regenerate hints. |
| `COVERAGE.md` | OpenStax form checklist vs generator packs / gaps. |
| `README.md` | This file. |

## How to rate

1. Open `rater.html` in a desktop browser (double-click / file://).
2. For each item, enter **rating 1–5** (effort/quality for ML — see scale below),
   optional **minutes**, and optional **notes**.
3. Progress autosaves in **localStorage** under key `poly_rating_calc_derivatives`.
4. Click **Export ratings JSON** to download `calc_derivatives_ratings.json`
   (merge of rating_id → human fields). Click **Export full JSONL** to download
   items with ratings filled in.
5. Keep `items.jsonl` immutable as the machine source of truth; store exported
   ratings beside it (e.g. `ratings_filled.jsonl`).

### Suggested 1–5 scale

| Score | Meaning |
|-------|---------|
| 1 | Trivial / under-topic / broken |
| 2 | Easy for the claimed D / thin |
| 3 | On-level |
| 4 | Solid challenge for claimed D |
| 5 | Hard / dense / high cognitive load (still fair) |

Use notes for pedagogy flags (wrong topic, ugly latex, answer suspect, etc.).

## Stratification

- **Items:** {n_rows} ({n_err} generation errors)
- **Difficulties:** {strat.get("difficulties")}
- **Per pack:** see `INDEX.json`

## Regenerate / join later

Each row carries:

- `type_id`, `generator`, `seed`, continuous `difficulty`
- `theta_full` (resolved allow_*/require_* + Spec-merged exponent knobs)
- `spec_snapshot` when Spec packs ran
- `function_classes`, `methods_used`, `effort_features`, structure inventory

```powershell
$env:PYTHONPATH='.'
python -c "from question_engine.api.handler import _generate_for_type; print(_generate_for_type('TYPE', {{'difficulty': D, 'count': 1, 'include_answer_key': True, 'seed': SEED}})[0].prompt_latex)"
```

## Later courses

Sibling scaffolds (empty until built):

- `../algebra_1/`
- `../algebra_2/`
- `../precalc_algebraic/`

Rebuild this campaign:

```powershell
$env:PYTHONPATH='.'
python scripts/build_hand_rating_set.py --campaign calc_derivatives
```
"""
    (out_dir / "README.md").write_text(text, encoding="utf-8")


def write_index(
    out_dir: Path,
    rows: list[dict[str, Any]],
    *,
    elapsed_s: float,
    campaign: str,
    packs: list[dict[str, Any]],
) -> dict[str, Any]:
    by_pack = Counter(r.get("pack") for r in rows if "error" not in r)
    by_d = Counter(r.get("difficulty") for r in rows if "error" not in r)
    index = {
        "campaign": campaign,
        "n_rows": len(rows),
        "n_ok": sum(1 for r in rows if "error" not in r),
        "n_errors": sum(1 for r in rows if "error" in r),
        "difficulties": list(DIFFICULTIES),
        "by_pack": dict(by_pack),
        "by_difficulty": {str(k): v for k, v in sorted(by_d.items(), key=lambda kv: float(kv[0] or 0))},
        "packs": [
            {
                "pack": p["pack"],
                "type_id": p["type_id"],
                "generator": p["generator"],
                "n_per_d": p["n_per_d"],
                "openstax": p.get("openstax"),
            }
            for p in packs
        ],
        "rating_schema": {
            "rating_1_to_5": "int 1..5 or null",
            "minutes": "float minutes or null",
            "notes": "optional string",
        },
        "join_keys": [
            "rating_id",
            "type_id",
            "generator",
            "seed",
            "difficulty",
            "theta_full",
            "spec_snapshot",
        ],
        "elapsed_s": elapsed_s,
        "paths": {
            "jsonl": "items.jsonl",
            "json": "items.json",
            "rater": "rater.html",
            "coverage": "COVERAGE.md",
        },
    }
    (out_dir / "INDEX.json").write_text(json.dumps(index, indent=2), encoding="utf-8")
    return index


def write_rater_html(
    out_dir: Path,
    items: list[dict[str, Any]],
    *,
    campaign: str = "calc_derivatives",
) -> None:
    html_path = out_dir / "rater.html"
    katex = _katex_mod.katex_head_html(html_path)
    # Embed items as JSON for offline use.
    payload = []
    for r in items:
        if "error" in r:
            continue
        payload.append(
            {
                "rating_id": r["rating_id"],
                "pack": r.get("pack"),
                "type_id": r.get("type_id"),
                "generator": r.get("generator"),
                "seed": r.get("seed"),
                "difficulty": r.get("difficulty"),
                "prompt_latex": r.get("prompt_latex") or "",
                "answer_latex": r.get("answer_latex") or "",
                "function_classes": r.get("function_classes"),
                "methods_used": r.get("methods_used"),
                "shape_id": r.get("shape_id"),
                "chain_depth": r.get("chain_depth"),
                "y_effort": r.get("y_effort"),
                "openstax_ref": r.get("openstax_ref"),
            }
        )
    items_json = json.dumps(payload, ensure_ascii=False)
    # Escape for script tag safety
    items_json = items_json.replace("</", "<\\/")
    storage_key = f"poly_rating_{campaign}"
    title = campaign.replace("_", " ")

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{title} — hand rater</title>
{katex}
<style>
:root {{ color-scheme: light; --ink:#1a1a1a; --muted:#5a5a5a; --line:#cfc8bc; --bg:#f7f4ee; --card:#fffdf8; --accent:#1f4d3a; }}
* {{ box-sizing: border-box; }}
body {{ margin:0; font-family: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
  color: var(--ink); background: linear-gradient(165deg, #efe8dc 0%, #f7f4ee 40%, #e7eef0 100%); min-height:100vh; }}
header {{ padding: 1rem 1.25rem; border-bottom: 1px solid var(--line); background: rgba(255,253,248,0.92);
  position: sticky; top:0; z-index:5; backdrop-filter: blur(6px); }}
header h1 {{ margin:0; font-size:1.35rem; letter-spacing:0.02em; }}
header p {{ margin:0.25rem 0 0; color:var(--muted); font-size:0.92rem; }}
.toolbar {{ display:flex; flex-wrap:wrap; gap:0.5rem 0.75rem; align-items:center; margin-top:0.75rem; }}
.toolbar label {{ font-size:0.85rem; color:var(--muted); }}
select, input[type="number"], input[type="text"], textarea, button {{
  font: inherit; font-size:0.92rem; }}
select, input[type="number"], input[type="text"] {{
  border:1px solid var(--line); border-radius:4px; padding:0.3rem 0.45rem; background:#fff; }}
button {{ border:1px solid var(--accent); background:var(--accent); color:#f6fff9; border-radius:4px;
  padding:0.35rem 0.7rem; cursor:pointer; }}
button.secondary {{ background:#fff; color:var(--accent); }}
button.score {{ min-width:2.2rem; background:#fff; color:var(--ink); border-color:var(--line); }}
button.score.active {{ background:var(--accent); color:#fff; border-color:var(--accent); }}
button:disabled {{ opacity:0.45; cursor:default; }}
main {{ max-width: 52rem; margin: 0 auto; padding: 1.25rem; }}
.card {{ background: var(--card); border:1px solid var(--line); border-radius:6px; padding:1rem 1.1rem 1.2rem;
  box-shadow: 0 1px 0 rgba(0,0,0,0.03); }}
.meta {{ display:flex; flex-wrap:wrap; gap:0.35rem 0.75rem; font-size:0.82rem; color:var(--muted); margin-bottom:0.75rem; }}
.meta code {{ color:var(--ink); background:#efe9df; padding:0.05rem 0.3rem; border-radius:3px; }}
.prompt {{ font-size:1.15rem; margin:0.75rem 0; min-height:2.5rem; }}
.answer {{ margin:0.5rem 0 1rem; padding:0.6rem 0.75rem; background:#f0ebe3; border-radius:4px; }}
.answer summary {{ cursor:pointer; color:var(--muted); }}
.rate-row {{ display:flex; flex-wrap:wrap; gap:0.5rem; align-items:center; margin:0.75rem 0; }}
textarea {{ width:100%; min-height:3.5rem; border:1px solid var(--line); border-radius:4px; padding:0.45rem; background:#fff; }}
.nav {{ display:flex; justify-content:space-between; gap:0.75rem; margin-top:1rem; }}
.progress {{ font-variant-numeric: tabular-nums; }}
.toast {{ position:fixed; bottom:1rem; right:1rem; background:#1a1a1a; color:#fff; padding:0.5rem 0.75rem;
  border-radius:4px; font-size:0.85rem; opacity:0; transition:opacity 0.2s; pointer-events:none; }}
.toast.show {{ opacity:0.92; }}
</style>
</head>
<body>
<header>
  <h1>Polynomial — {title} rater</h1>
  <p>Rate effort/quality 1–5. Autosaves locally. Export when done.</p>
  <div class="toolbar">
    <label>Pack <select id="packFilter"><option value="">All packs</option></select></label>
    <label>Jump <input id="jump" type="number" min="1" value="1" style="width:4.5rem"/></label>
    <span class="progress" id="progress">0 / 0 rated</span>
    <button type="button" class="secondary" id="btnPrev">Prev</button>
    <button type="button" id="btnNext">Next</button>
    <button type="button" class="secondary" id="btnExport">Export ratings JSON</button>
    <button type="button" class="secondary" id="btnExportFull">Export full JSONL</button>
    <button type="button" class="secondary" id="btnClear" title="Clear localStorage for this campaign">Clear saved</button>
  </div>
</header>
<main>
  <div class="card" id="card">
    <div class="meta" id="meta"></div>
    <div class="prompt" id="prompt"></div>
    <details class="answer"><summary>Show answer</summary><div id="answer"></div></details>
    <div class="rate-row" id="scores">
      <span>Rating:</span>
    </div>
    <div class="rate-row">
      <label>Minutes <input id="minutes" type="number" min="0" step="0.5" style="width:5rem"/></label>
    </div>
    <label for="notes">Notes</label>
    <textarea id="notes" placeholder="Optional pedagogy / latex / topic flags"></textarea>
    <div class="nav">
      <button type="button" class="secondary" id="btnSkip">Skip / clear rating</button>
      <button type="button" id="btnSaveNext">Save &amp; next</button>
    </div>
  </div>
</main>
<div class="toast" id="toast"></div>
<script>
const STORAGE_KEY = "{storage_key}";
const ITEMS = {items_json};
const FULL_BY_ID = Object.fromEntries(ITEMS.map(x => [x.rating_id, x]));

function loadStore() {{
  try {{ return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{{}}"); }}
  catch (e) {{ return {{}}; }}
}}
function saveStore(store) {{
  localStorage.setItem(STORAGE_KEY, JSON.stringify(store));
}}

let store = loadStore();
let pack = "";
let idx = 0;
let currentScore = null;

const packFilter = document.getElementById("packFilter");
const packs = [...new Set(ITEMS.map(i => i.pack))].sort();
for (const p of packs) {{
  const opt = document.createElement("option");
  opt.value = p; opt.textContent = p;
  packFilter.appendChild(opt);
}}

function filtered() {{
  return pack ? ITEMS.filter(i => i.pack === pack) : ITEMS;
}}

function toast(msg) {{
  const el = document.getElementById("toast");
  el.textContent = msg;
  el.classList.add("show");
  setTimeout(() => el.classList.remove("show"), 1400);
}}

function renderMath() {{
  if (window.renderMathInElement) {{
    renderMathInElement(document.getElementById("card"), {{
      delimiters: [
        {{left: "$$", right: "$$", display: true}},
        {{left: "$", right: "$", display: false}}
      ],
      throwOnError: false
    }});
  }}
}}

function wrapMath(tex) {{
  const t = (tex || "").trim();
  if (!t) return "<em>(empty)</em>";
  if (t.startsWith("$$") || t.startsWith("$")) return t;
  return "$" + t + "$";
}}

function updateProgress() {{
  const list = filtered();
  let rated = 0;
  for (const it of list) {{
    const r = store[it.rating_id];
    if (r && r.rating_1_to_5 != null) rated++;
  }}
  document.getElementById("progress").textContent =
    rated + " / " + list.length + " rated · #" + (list.length ? (idx+1) : 0);
  document.getElementById("jump").max = Math.max(1, list.length);
  document.getElementById("jump").value = list.length ? (idx+1) : 1;
}}

function showItem() {{
  const list = filtered();
  if (!list.length) return;
  idx = Math.max(0, Math.min(idx, list.length - 1));
  const it = list[idx];
  const saved = store[it.rating_id] || {{}};
  currentScore = saved.rating_1_to_5 != null ? saved.rating_1_to_5 : null;
  document.getElementById("meta").innerHTML = [
    "<span>Pack <code>" + it.pack + "</code></span>",
    "<span>D <code>" + it.difficulty + "</code></span>",
    "<span>seed <code>" + it.seed + "</code></span>",
    "<span>type <code>" + it.type_id + "</code></span>",
    "<span>gen <code>" + (it.generator || "") + "</code></span>",
    "<span>classes <code>" + JSON.stringify(it.function_classes || []) + "</code></span>",
    "<span>methods <code>" + JSON.stringify(it.methods_used || []) + "</code></span>",
    it.y_effort != null ? "<span>y_effort <code>" + it.y_effort + "</code></span>" : "",
    it.openstax_ref ? "<span>" + it.openstax_ref + "</span>" : ""
  ].filter(Boolean).join("");
  document.getElementById("prompt").innerHTML = wrapMath(it.prompt_latex);
  document.getElementById("answer").innerHTML = wrapMath(it.answer_latex);
  document.getElementById("minutes").value = saved.minutes != null ? saved.minutes : "";
  document.getElementById("notes").value = saved.notes || "";
  document.querySelectorAll("button.score").forEach(btn => {{
    btn.classList.toggle("active", Number(btn.dataset.score) === currentScore);
  }});
  const ans = document.querySelector("details.answer");
  if (ans) ans.open = false;
  updateProgress();
  renderMath();
}}

const scores = document.getElementById("scores");
for (let s = 1; s <= 5; s++) {{
  const b = document.createElement("button");
  b.type = "button";
  b.className = "score";
  b.dataset.score = String(s);
  b.textContent = String(s);
  b.addEventListener("click", () => {{
    currentScore = s;
    document.querySelectorAll("button.score").forEach(x =>
      x.classList.toggle("active", Number(x.dataset.score) === currentScore));
  }});
  scores.appendChild(b);
}}

function persistCurrent(clear) {{
  const list = filtered();
  if (!list.length) return;
  const it = list[idx];
  if (clear) {{
    delete store[it.rating_id];
    saveStore(store);
    currentScore = null;
    document.getElementById("minutes").value = "";
    document.getElementById("notes").value = "";
    document.querySelectorAll("button.score").forEach(x => x.classList.remove("active"));
    updateProgress();
    toast("Cleared");
    return;
  }}
  const minutesRaw = document.getElementById("minutes").value;
  store[it.rating_id] = {{
    rating_id: it.rating_id,
    rating_1_to_5: currentScore,
    minutes: minutesRaw === "" ? null : Number(minutesRaw),
    notes: document.getElementById("notes").value || null,
    rated_at: new Date().toISOString()
  }};
  saveStore(store);
  updateProgress();
}}

packFilter.addEventListener("change", () => {{
  pack = packFilter.value;
  idx = 0;
  showItem();
}});
document.getElementById("btnPrev").addEventListener("click", () => {{ persistCurrent(false); idx--; showItem(); }});
document.getElementById("btnNext").addEventListener("click", () => {{ persistCurrent(false); idx++; showItem(); }});
document.getElementById("btnSaveNext").addEventListener("click", () => {{ persistCurrent(false); idx++; showItem(); toast("Saved"); }});
document.getElementById("btnSkip").addEventListener("click", () => {{ persistCurrent(true); }});
document.getElementById("jump").addEventListener("change", () => {{
  persistCurrent(false);
  idx = Math.max(0, Number(document.getElementById("jump").value) - 1);
  showItem();
}});

document.getElementById("btnExport").addEventListener("click", () => {{
  persistCurrent(false);
  const blob = new Blob([JSON.stringify(store, null, 2)], {{type: "application/json"}});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "{campaign}_ratings.json";
  a.click();
  toast("Exported ratings JSON");
}});

document.getElementById("btnExportFull").addEventListener("click", async () => {{
  persistCurrent(false);
  // Merge into lightweight rows for JSONL download
  const lines = ITEMS.map(it => {{
    const r = store[it.rating_id] || {{}};
    return JSON.stringify({{
      ...it,
      rating_1_to_5: r.rating_1_to_5 != null ? r.rating_1_to_5 : null,
      minutes: r.minutes != null ? r.minutes : null,
      notes: r.notes || null,
      rated_at: r.rated_at || null
    }});
  }});
  const blob = new Blob([lines.join("\\n") + "\\n"], {{type: "application/x-ndjson"}});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "{campaign}_rated_lite.jsonl";
  a.click();
  toast("Exported lite JSONL");
}});

document.getElementById("btnClear").addEventListener("click", () => {{
  if (confirm("Clear all saved ratings for {campaign}?")) {{
    store = {{}};
    localStorage.removeItem(STORAGE_KEY);
    showItem();
    toast("Cleared localStorage");
  }}
}});

document.addEventListener("keydown", (e) => {{
  if (e.target && (e.target.tagName === "TEXTAREA" || e.target.tagName === "INPUT")) return;
  if (e.key >= "1" && e.key <= "5") {{
    currentScore = Number(e.key);
    document.querySelectorAll("button.score").forEach(x =>
      x.classList.toggle("active", Number(x.dataset.score) === currentScore));
  }} else if (e.key === "ArrowRight") {{ persistCurrent(false); idx++; showItem(); }}
  else if (e.key === "ArrowLeft") {{ persistCurrent(false); idx--; showItem(); }}
  else if (e.key === "Enter") {{ persistCurrent(false); idx++; showItem(); toast("Saved"); }}
}});

// Wait briefly for KaTeX auto-render onload, then draw.
setTimeout(showItem, 50);
</script>
</body>
</html>
"""
    html_path.write_text(doc, encoding="utf-8")


def scaffold_other_campaigns() -> None:
    for name in SCAFFOLD_CAMPAIGNS:
        d = RATINGS_ROOT / name
        d.mkdir(parents=True, exist_ok=True)
        readme = d / "README.md"
        if not readme.exists():
            readme.write_text(
                f"""# {name} — hand rating campaign

Edit `CAMPAIGN.json` packs, then:

```powershell
$env:PYTHONPATH='.'
python scripts/build_hand_rating_set.py --campaign {name}
python scripts/build_hand_rating_set.py --campaign {name} --smoke
```

Join keys (same schema as calc): `type_id`, `generator`, `seed`, `difficulty`,
`theta_full`, Spec snapshot / structural metadata when available.

See `scripts/output/ml/ML_TRAINING_READINESS.md` for course readiness.
""",
                encoding="utf-8",
            )
        stub = d / "CAMPAIGN.json"
        default_packs = _DEFAULT_CAMPAIGN_PACKS.get(name) or []
        if not stub.exists():
            stub.write_text(
                json.dumps(
                    {
                        "campaign": name,
                        "status": "ready_to_build",
                        "rating_schema": {
                            "rating_1_to_5": "int 1..5 or null",
                            "minutes": "float or null",
                            "notes": "string or null",
                        },
                        "packs": default_packs,
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
        else:
            # Backfill packs key when older scaffolds omit it.
            try:
                data = json.loads(stub.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                data = {}
            if isinstance(data, dict) and not data.get("packs") and default_packs:
                data["packs"] = default_packs
                data["status"] = data.get("status") or "ready_to_build"
                stub.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _write_campaign_bundle(
    out_dir: Path,
    rows: list[dict[str, Any]],
    *,
    campaign: str,
    packs: list[dict[str, Any]],
    elapsed_s: float,
) -> dict[str, Any]:
    jsonl_path = out_dir / "items.jsonl"
    with jsonl_path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    (out_dir / "items.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    if campaign == "calc_derivatives":
        write_coverage_checklist(out_dir)
        write_readme(
            out_dir,
            n_rows=len(rows),
            n_err=sum(1 for r in rows if "error" in r),
            strat={"difficulties": list(DIFFICULTIES)},
        )
    else:
        (out_dir / "README.md").write_text(
            f"""# {campaign} — hand rating package

Generated for human effort / quality ratings. Machine fields are complete;
human fields start null.

Join keys: `rating_id`, `type_id`, `generator`, `seed`, `difficulty`,
`theta_full`, `spec_snapshot` when present.

```powershell
$env:PYTHONPATH='.'
python scripts/build_hand_rating_set.py --campaign {campaign}
```
""",
            encoding="utf-8",
        )
    index = write_index(
        out_dir, rows, elapsed_s=elapsed_s, campaign=campaign, packs=packs
    )
    write_rater_html(out_dir, rows, campaign=campaign)
    summary = {
        "campaign": campaign,
        "out_dir": str(out_dir),
        "n_rows": len(rows),
        "n_ok": index["n_ok"],
        "n_errors": index["n_errors"],
        "by_pack": index["by_pack"],
        "elapsed_s": elapsed_s,
        "rater": str(out_dir / "rater.html"),
        "jsonl": str(jsonl_path),
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--campaign",
        default="calc_derivatives",
        choices=list(ALL_CAMPAIGNS),
    )
    parser.add_argument("--seed-base", type=int, default=91000)
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Tiny subset for plumbing checks",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Override output directory",
    )
    args = parser.parse_args()

    scaffold_other_campaigns()
    campaign = str(args.campaign)
    out_dir = args.out_dir or (RATINGS_ROOT / campaign)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating {campaign} -> {out_dir}")
    t0 = time.time()
    if campaign == "calc_derivatives":
        packs = CALC_DERIVATIVE_PACKS
        rows = generate_calc_derivatives(
            seed_base=int(args.seed_base), smoke=bool(args.smoke)
        )
    elif campaign == "calc_diff_gaps":
        packs = CALC_GAP_PACKS
        rows = generate_calc_gaps(
            seed_base=int(args.seed_base), smoke=bool(args.smoke)
        )
    else:
        packs = _load_campaign_packs(campaign, out_dir)
        if not packs:
            print(f"No packs configured for {campaign}; edit {out_dir / 'CAMPAIGN.json'}")
            return 1
        rows = generate_pack_rows(
            packs,
            seed_base=int(args.seed_base),
            smoke=bool(args.smoke),
            rating_id_prefix=campaign.replace("-", "_")[:24],
        )
    elapsed = round(time.time() - t0, 2)
    summary = _write_campaign_bundle(
        out_dir, rows, campaign=campaign, packs=packs, elapsed_s=elapsed
    )
    print(json.dumps(summary, indent=2))
    return 0 if summary["n_errors"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
