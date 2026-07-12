"""Print verification table for critical A2/geo/PC types."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import question_engine.types  # noqa: F401
from question_engine.core.base import QUESTION_TYPES
from question_engine.core.registry import get_catalog_entry
from question_engine.settings.presets import apply_difficulty_presets

CRITICAL = [
    ("A2", "a2_complex_numbers_absolute_value"),
    ("A2", "a2_conic_sections_ellipses_writing_equations"),
    ("A2", "a2_conic_sections_classifying"),
    ("A2", "a2_sequences_and_series_arithmetic_and_geometric_mean"),
    ("A2", "a2_sequences_and_series_arithmetic_series"),
    ("A2", "a2_sequences_and_series_geometric_series"),
    ("A2", "a2_probability_and_statistics_permutations"),
    ("A2", "a2_probability_and_statistics_combinations"),
    ("A2", "a2_matrices_inverses"),
    ("A2", "direct_inverse_variation"),
    ("A2", "continuous_relations"),
    ("A2", "writing_linear_equations"),
    ("A2", "a2_linear_relations_and_functions_graphing_linear_equations"),
    ("Geo", "geo_review_simplifying_square_roots"),
    ("Geo", "geo_review_multiplying_square_roots"),
    ("Geo", "multi_step_equations"),
    ("PC", "pc_vectors_operations"),
    ("PC", "pc_3d_vectors_operations"),
    ("PC", "pc_transformations_of_graphs"),
    ("PC", "pc_polynomial_graphs_real_zeros_and_end_behavior"),
    ("PC", "pc_graphs_of_rational_functions"),
    ("PC", "pc_inverses"),
]


def main() -> None:
    print("| Scope | Type | Generator | Verdict | Notes |")
    print("|---|---|---|---|---|")
    for scope, tid in CRITICAL:
        entry = get_catalog_entry(tid)
        qt = QUESTION_TYPES[tid]
        notes: list[str] = []
        prompts: list[str] = []
        ok = True
        for tier in ("easy", "medium", "hard"):
            settings = apply_difficulty_presets(
                {
                    "count": 1,
                    "difficulty_tier": tier,
                    "include_answer_key": True,
                    "include_graph_metadata": True,
                },
                type_id=tid,
                setting_profile=getattr(qt, "setting_profile", None),
            )
            try:
                q = qt.generate(settings)[0]
            except Exception as exc:  # noqa: BLE001
                ok = False
                notes.append(f"{tier}:EXC {exc}")
                continue
            prompt = (q.prompt_latex or q.prompt_text or "").strip()
            prompts.append(prompt)
            if not prompt:
                ok = False
                notes.append(f"{tier}:blank")
            if not (q.answer_latex or "").strip():
                ok = False
                notes.append(f"{tier}:no_ans")
        if len(prompts) == 3 and len(set(prompts)) == 1:
            notes.append("identical prompt text across E/M/H")
        verdict = "PASS" if ok else "FAIL"
        if ok and notes:
            verdict = "PASS*"
        note_s = "; ".join(notes) if notes else ""
        print(f"| {scope} | `{tid}` | `{entry.generator}` | {verdict} | {note_s} |")


if __name__ == "__main__":
    main()
