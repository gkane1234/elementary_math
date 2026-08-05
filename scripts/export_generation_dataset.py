"""Export GenerationRecord JSONL sweeps for difficulty learning.

Samples (type_id × D × seed) via the same settings path as the worksheet API,
scores effort when a scorer is registered, and writes JSONL.

Usage:
  $env:PYTHONPATH='.'
  python scripts/export_generation_dataset.py --types g6_introduction_to_ratios --n-per 20
  python scripts/export_generation_dataset.py --g6-ratios --n-per 40
  python scripts/export_generation_dataset.py --pre-algebra --out scripts/output/ml/pa_first_tranche.jsonl
  python scripts/export_generation_dataset.py --algebra-1 --n-per 5 --out scripts/output/ml/a1_continuous_stub.jsonl
  python scripts/export_generation_dataset.py --g6-ratios --out scripts/output/ml/g6_ratios.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import question_engine.types  # noqa: F401
from question_engine.api.handler import _resolve_generation_settings
from question_engine.core.base import QUESTION_TYPES
from question_engine.ml.effort import has_effort_scorer, score_effort
from question_engine.ml.schema import build_generation_record

DEFAULT_DIFFS = (0.0, 5.0, 10.0, 15.0, 20.0, 25.0)

G6_RATIO_PERCENT_TYPES = [
    "g6_introduction_to_ratios",
    "g6_equivalent_ratios",
    "g6_part_part_whole_ratios",
    "g6_comparing_ratios",
    "g6_unit_rates_and_equivalent_rates",
    "g6_comparing_rates",
    "g6_converting_units",
    "g6_introduction_to_percents",
    "g6_relating_percents_fractions_and_decimals",
    "g6_finding_percents_with_equivalent_fractions",
    "g6_solving_percent_problems_with_formulas",
]

# First-tranche PA continuous-D types with registered effort scorers.
PA_FIRST_TRANCHE_TYPES = [
    "pa_naming_decimal_places_and_rounding",
    "pa_writing_numbers_with_words",
    "pa_integers_adding_and_subtracting",
    "pa_integers_multiplying",
    "pa_integers_dividing",
    "pa_factoring",
    "pa_greatest_common_factor",
    "pa_least_common_multiple",
    "pa_simplifying_fractions",
    "pa_converting_fractions_and_decimals",
    "pa_fractions_decimals_and_percents",
    "pa_simple_and_compound_interest",
    # Beyond the 12 knob_retargets — continuous schema + scorer ready.
    "pa_squares_and_square_roots",
    # pa_markup_discount_and_tax deferred: wp_percent currently emits equation stubs
]

# Second PA tranche: fraction aliases (OpenStax §4.2/4.4/4.5) + already_continuous algebra.
PA_SECOND_TRANCHE_TYPES = [
    "pa_fractions_add_like",
    "pa_fractions_subtract_like",
    "pa_fractions_add_unlike",
    "pa_fractions_subtract_unlike",
    "pa_fractions_multiply",
    "pa_fractions_divide",
    "pa_equations_one_step_word_problems",
    "pa_equations_two_step_word_problems",
    "pa_equations_multi_step_equations",
    "pa_multi_step_inequalities",
    "pa_checking_for_a_proportion",
    "pa_proportions_word_problems",
    "pa_slope",
    "pa_writing_linear_equations",
    "pa_graphing_systems_of_equations",
    "pa_systems_substitution",
    "pa_systems_word_problems",
    "pa_polynomials_simplifying",
    "pa_polynomials_adding_and_subtracting",
    "pa_polynomials_multiplying",
]

A1_EXPORT_TYPES_PATH = ROOT / "scripts" / "output" / "ml" / "a1_export_types.json"
A2_EXPORT_TYPES_PATH = ROOT / "scripts" / "output" / "ml" / "a2_export_types.json"
PRECALC_EXPORT_TYPES_PATH = ROOT / "scripts" / "output" / "ml" / "precalc_export_types.json"
CALC_EXPORT_TYPES_PATH = ROOT / "scripts" / "output" / "ml" / "calc_export_types.json"


def _load_export_types(path: Path, *, label: str) -> list[str]:
    if not path.is_file():
        raise FileNotFoundError(f"Missing {label} type list: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    ids = data.get("type_ids") if isinstance(data, dict) else data
    if not isinstance(ids, list) or not ids:
        raise ValueError(f"No type_ids in {path}")
    return [str(x) for x in ids]


def _load_a1_export_types() -> list[str]:
    return _load_export_types(A1_EXPORT_TYPES_PATH, label="A1")


def _load_a2_export_types() -> list[str]:
    return _load_export_types(A2_EXPORT_TYPES_PATH, label="A2")


def _load_precalc_export_types() -> list[str]:
    return _load_export_types(PRECALC_EXPORT_TYPES_PATH, label="precalculus")


def _load_calc_export_types() -> list[str]:
    return _load_export_types(CALC_EXPORT_TYPES_PATH, label="calculus")


def _generate_one(
    type_id: str,
    difficulty: float,
    seed: int,
) -> tuple[Any, dict[str, Any]]:
    qt = QUESTION_TYPES[type_id]
    settings = _resolve_generation_settings(
        type_id,
        {
            "difficulty": difficulty,
            "count": 1,
            "include_answer_key": True,
            "seed": seed,
        },
    )
    questions = qt.generate(settings)
    # Match API annotation of generation_settings.
    for q in questions:
        q.metadata = {
            **(q.metadata or {}),
            "generation_settings": {
                k: v for k, v in settings.items() if k not in {"count", "max_columns"}
            },
        }
    if not questions:
        raise RuntimeError(f"No questions generated for {type_id} d={difficulty}")
    return questions[0], settings


def export_records(
    type_ids: list[str],
    *,
    difficulties: list[float],
    n_per: int,
    seed_base: int,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for type_id in type_ids:
        if type_id not in QUESTION_TYPES:
            print(f"skip unknown type: {type_id}", file=sys.stderr)
            continue
        for d in difficulties:
            for i in range(n_per):
                seed = seed_base + int(d * 1000) + i * 17 + (hash(type_id) % 997)
                try:
                    question, settings = _generate_one(type_id, d, seed)
                except Exception as exc:  # noqa: BLE001
                    rows.append(
                        {
                            "type_id": type_id,
                            "difficulty": d,
                            "seed": seed,
                            "error": f"{type(exc).__name__}: {exc}",
                        }
                    )
                    continue
                prompt = (question.prompt_latex or question.prompt_text or "").strip()
                answer = (question.answer_latex or question.answer_text or "").strip()
                y_effort = None
                y_mode = None
                effort_feats: dict[str, Any] = {}
                if has_effort_scorer(type_id):
                    y_effort, effort_feats = score_effort(type_id, prompt, answer)
                    y_mode = None
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
                rows.append(record.to_dict())
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--types", nargs="*", default=[], help="type_id list")
    parser.add_argument(
        "--g6-ratios",
        action="store_true",
        help="Export the first-11 G6 ratio/percent Ready topics",
    )
    parser.add_argument(
        "--pre-algebra",
        action="store_true",
        help="Export PA first+second tranche continuous types with effort scorers",
    )
    parser.add_argument(
        "--algebra-1",
        action="store_true",
        help=(
            "Export continuous-D A1 types from "
            "scripts/output/ml/a1_export_types.json"
        ),
    )
    parser.add_argument(
        "--algebra-2",
        action="store_true",
        help=(
            "Export continuous-D A2 types from "
            "scripts/output/ml/a2_export_types.json"
        ),
    )
    parser.add_argument(
        "--precalculus",
        action="store_true",
        help=(
            "Export continuous-D precalc types from "
            "scripts/output/ml/precalc_export_types.json"
        ),
    )
    parser.add_argument(
        "--calculus",
        action="store_true",
        help=(
            "Export continuous-D calculus types from "
            "scripts/output/ml/calc_export_types.json"
        ),
    )
    parser.add_argument(
        "--diffs",
        type=float,
        nargs="*",
        default=list(DEFAULT_DIFFS),
        help="Difficulty levels to sweep",
    )
    parser.add_argument("--n-per", type=int, default=20, help="Samples per (type, D)")
    parser.add_argument("--seed-base", type=int, default=4000)
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "scripts" / "output" / "ml" / "generation_dataset.jsonl",
    )
    args = parser.parse_args()

    type_ids = list(args.types)
    if args.g6_ratios:
        type_ids.extend(G6_RATIO_PERCENT_TYPES)
    if args.pre_algebra:
        type_ids.extend(PA_FIRST_TRANCHE_TYPES)
        type_ids.extend(PA_SECOND_TRANCHE_TYPES)
    if args.algebra_1:
        type_ids.extend(_load_a1_export_types())
    if args.algebra_2:
        type_ids.extend(_load_a2_export_types())
    if args.precalculus:
        type_ids.extend(_load_precalc_export_types())
    if args.calculus:
        type_ids.extend(_load_calc_export_types())
    type_ids = list(dict.fromkeys(type_ids))
    if not type_ids:
        parser.error(
            "Provide --types and/or --g6-ratios and/or --pre-algebra "
            "and/or --algebra-1 and/or --algebra-2 and/or --precalculus and/or --calculus"
        )

    t0 = time.time()
    rows = export_records(
        type_ids,
        difficulties=[float(d) for d in args.diffs],
        n_per=int(args.n_per),
        seed_base=int(args.seed_base),
    )
    out: Path = args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    n_err = sum(1 for r in rows if "error" in r)
    n_labeled = sum(1 for r in rows if r.get("y_effort") is not None)
    summary = {
        "out": str(out),
        "n_rows": len(rows),
        "n_labeled": n_labeled,
        "n_errors": n_err,
        "types": type_ids,
        "diffs": args.diffs,
        "n_per": args.n_per,
        "elapsed_s": round(time.time() - t0, 2),
    }
    summary_path = out.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if n_err == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
