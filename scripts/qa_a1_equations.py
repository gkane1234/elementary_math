"""Thorough QA for Algebra 1 equations/inequalities/graphing/slope/systems."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import question_engine.types  # noqa: F401
from question_engine.core.base import QUESTION_TYPES
from question_engine.settings.presets import apply_difficulty_presets

TYPE_IDS = [
    "one_step_equations",
    "two_step_equations",
    "multi_step_equations",
    "absolute_value_equations",
    "literal_equations",
    "graphing_single_variable_inequalities",
    "one_step_inequalities",
    "two_step_inequalities",
    "multi_step_inequalities",
    "compound_inequalities",
    "absolute_value_inequalities",
    "slope",
    "more_on_slope",
    "graphing_linear_equations",
    "writing_linear_equations",
    "graphing_linear_inequalities",
    "graphing_absolute_value_equations",
    "systems_graphing",
    "systems_elimination",
    "systems_substitution",
    "graphing_systems_of_inequalities",
]

N = 6
TIERS = ("easy", "medium", "hard")
OUT = ROOT / "scripts" / "output" / "a1_eq_qa_samples.json"


def strip_latex(s: str) -> str:
    if not s:
        return ""
    return re.sub(r"\\[a-zA-Z]+|[{}$]", " ", s)


def features(q) -> dict:
    p = q.prompt_latex or q.prompt_text or ""
    a = q.answer_latex or ""
    meta = getattr(q, "metadata", None) or {}
    if not isinstance(meta, dict):
        meta = {}
    graph_spec = meta.get("answer_graph_spec") or meta.get("graph_spec") or {}
    nl_ans = meta.get("answer_number_line_spec")
    nl_prompt = meta.get("number_line_spec")
    funcs = graph_spec.get("functions") if isinstance(graph_spec, dict) else None
    nums = [
        abs(float(x))
        for x in re.findall(r"-?\d+(?:\.\d+)?", strip_latex(p))
        if x not in ("",)
    ]
    return {
        "prompt": p,
        "answer": a,
        "prompt_len": len(p),
        "has_abs": bool(
            re.search(r"\\(?:left)?\||\\lvert|absolute", p, re.I)
            or "|" in p
        ),
        "has_compound_and_or": bool(re.search(r"\b(and|or)\b", p, re.I)),
        "has_frac": r"\frac" in p,
        "paren_count": p.count("("),
        "graph_role": meta.get("graph_role"),
        "has_answer_graph": bool(
            (isinstance(graph_spec, dict) and (graph_spec.get("functions") or graph_spec.get("points") or graph_spec.get("regions")))
            or nl_ans
        ),
        "has_prompt_graph_content": bool(
            (isinstance(meta.get("graph_spec"), dict) and (
                meta["graph_spec"].get("functions")
                or meta["graph_spec"].get("points")
                or meta["graph_spec"].get("regions")
            ))
            or (isinstance(nl_prompt, dict) and not nl_prompt.get("blank", False) and (
                nl_prompt.get("rays") or nl_prompt.get("segments") or nl_prompt.get("points")
            ))
        ),
        "functions": funcs,
        "nl_answer": nl_ans,
        "max_num": max(nums) if nums else 0,
        "num_count": len(nums),
        "extra": {
            k: meta.get(k)
            for k in (
                "form",
                "mode",
                "variant",
                "question_mode",
                "slope_mode",
                "system_mode",
                "compound_type",
                "inequality_form",
                "problem_type",
                "kind",
            )
            if k in meta
        },
        "meta_keys": sorted(meta.keys()),
        "bad_1x": bool(re.search(r"(?<![0-9])1x(?![0-9])|(?<![0-9])-1x(?![0-9])|0x", a + p)),
        "answer_has_y_eq": "y =" in a or r"y=" in a.replace(" ", "") or "y =" in a,
    }


def main() -> None:
    results: dict = {}
    for tid in TYPE_IDS:
        qt = QUESTION_TYPES.get(tid)
        if not qt:
            results[tid] = {"error": "not registered"}
            continue
        profile = getattr(qt, "setting_profile", None)
        tier_samples: dict = {}
        for tier in TIERS:
            samples = []
            for _ in range(N):
                settings = apply_difficulty_presets(
                    {
                        "count": 1,
                        "difficulty_tier": tier,
                        "include_answer_key": True,
                        "include_diagram": True,
                        "include_graph_metadata": True,
                    },
                    type_id=tid,
                    setting_profile=profile,
                )
                try:
                    qs = qt.generate(settings)
                    if not qs:
                        samples.append({"error": "empty"})
                        continue
                    samples.append(features(qs[0]))
                except Exception as exc:  # noqa: BLE001
                    samples.append({"error": str(exc)})
            tier_samples[tier] = samples
        results[tid] = {"profile": profile, "name": getattr(qt, "name", tid), "samples": tier_samples}

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print(f"wrote {OUT}")

    for tid, data in results.items():
        print(f"\n==== {tid} profile={data.get('profile')} ====")
        if "error" in data:
            print(" ERROR", data["error"])
            continue
        for tier in TIERS:
            samples = data["samples"][tier]
            errs = [s for s in samples if "error" in s]
            ok = [s for s in samples if "error" not in s]
            max_nums = sorted(s["max_num"] for s in ok)
            abs_c = sum(1 for s in ok if s["has_abs"])
            frac_c = sum(1 for s in ok if s["has_frac"])
            ans_graphs = sum(1 for s in ok if s.get("has_answer_graph"))
            prompt_content = sum(1 for s in ok if s.get("has_prompt_graph_content"))
            bad_1x = sum(1 for s in ok if s.get("bad_1x"))
            roles = {s.get("graph_role") for s in ok}
            modes = {json.dumps(s.get("extra"), sort_keys=True) for s in ok}
            print(
                f" {tier}: n={len(ok)} err={len(errs)} "
                f"max_num={max_nums[0] if max_nums else '-'}..{max_nums[-1] if max_nums else '-'} "
                f"abs={abs_c} frac={frac_c} ans_g={ans_graphs} prompt_g_content={prompt_content} "
                f"bad1x={bad_1x} roles={roles}"
            )
            print(f"   modes: {modes}")
            for i, s in enumerate(ok[:2]):
                p = s["prompt"][:100].replace("\n", " ")
                a = s["answer"][:80].replace("\n", " ")
                print(f"   P{i}: {p}")
                print(f"   A{i}: {a}")


if __name__ == "__main__":
    main()
