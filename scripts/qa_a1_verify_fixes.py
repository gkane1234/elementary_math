"""Post-fix smoke checks for Algebra 1 equation/graphing QA."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import question_engine.types  # noqa: F401
from question_engine.core.base import QUESTION_TYPES
from question_engine.settings.presets import apply_difficulty_presets, lookup_difficulty_preset

FOCUS = [
    "literal_equations",
    "two_step_equations",
    "two_step_inequalities",
    "multi_step_equations",
    "multi_step_inequalities",
    "one_step_inequalities",
    "graphing_linear_equations",
    "systems_elimination",
    "systems_substitution",
    "systems_graphing",
    "writing_linear_equations",
    "graphing_single_variable_inequalities",
    "absolute_value_equations",
    "slope",
]


def main() -> None:
    print("graphing hard", lookup_difficulty_preset("hard", setting_profile="graphing"))
    print("systems hard", lookup_difficulty_preset("hard", setting_profile="systems"))

    for tid in FOCUS:
        qt = QUESTION_TYPES[tid]
        print(f"\n==== {tid} ====")
        for tier in ("easy", "medium", "hard"):
            settings = apply_difficulty_presets(
                {
                    "count": 6,
                    "difficulty_tier": tier,
                    "include_answer_key": True,
                    "include_graph_metadata": True,
                },
                type_id=tid,
                setting_profile=getattr(qt, "setting_profile", None),
            )
            qs = qt.generate(settings)
            issues: list[str] = []
            max_abs_coef = 0
            for q in qs:
                p = q.prompt_latex or ""
                a = q.answer_latex or ""
                if ">=" in a or "<=" in a:
                    issues.append(f"ascii:{a}")
                if "+ 0" in p or "- 0" in p:
                    issues.append(f"plus0:{p}")
                nums = [abs(int(n)) for n in re.findall(r"-?\d+", p)]
                if nums:
                    max_abs_coef = max(max_abs_coef, max(nums))
                if tid == "two_step_equations":
                    compact = p.replace(" ", "")
                    if re.match(r"^-?\d*x=", compact) and not re.search(r"[+-]\d", compact[1:]):
                        issues.append(f"onestepish:{p}")
                if tid == "literal_equations" and "Solve for" not in p:
                    issues.append(f"no-solve-for:{p}")
            print(
                f" {tier}: slope={settings.get('slope_min')}..{settings.get('slope_max')} "
                f"coef={settings.get('coef_min')}..{settings.get('coef_max')} "
                f"max_num~{max_abs_coef}"
            )
            for q in qs[:2]:
                print(f"  P: {(q.prompt_latex or '')[:110]}")
                print(f"  A: {(q.answer_latex or '')[:90]}")
            if issues:
                print(f"  ISSUES ({len(issues)}): {issues[:5]}")


if __name__ == "__main__":
    main()
