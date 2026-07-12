"""Thorough QA for Algebra 2, Geometry Review of Algebra, Precalc foundations.

Samples E/M/H for each curriculum-linked Ready type and flags:
- stub / wrong-topic prompts
- identical E/M/H prompts
- missing answers
- missing graph_spec when graphing topic
- alias sharing generator with flat/wrong presets
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import question_engine.types  # noqa: F401
from question_engine.catalogs.algebra_2 import CATALOG as A2
from question_engine.catalogs.geometry import CATALOG as GEO
from question_engine.catalogs.precalculus import CATALOG as PC
from question_engine.core.base import QUESTION_TYPES
from question_engine.core.registry import get_catalog_entry
from question_engine.diagram_readiness import type_requires_diagram
from question_engine.settings.presets import apply_difficulty_presets, lookup_difficulty_preset
from question_engine.type_readiness import type_not_ready

OUT = ROOT / "scripts" / "output" / "qa_a2_geo_pc_report.json"
OUT_TXT = ROOT / "scripts" / "output" / "qa_a2_geo_pc_report.txt"
TIERS = ("easy", "medium", "hard")


def parse_curriculum_type_ids() -> dict[str, set[str]]:
    text = (ROOT / "lib" / "curriculum.ts").read_text(encoding="utf-8")
    lines = text.splitlines()
    course: str | None = None
    chapter: str | None = None
    by_scope: dict[str, set[str]] = defaultdict(set)
    for line in lines:
        cm = re.match(r'\s*id:\s*"(algebra_2|geometry|precalculus|algebra_1|calculus|grade_6|pre_algebra)"', line)
        if cm and "name:" not in line:
            # course-level ids appear before name on next lines; chapter ids also match
            pass
        # Course detection: look for id then name pattern of known courses
        if re.search(r'id:\s*"algebra_2"', line):
            course = "algebra_2"
            chapter = None
        elif re.search(r'id:\s*"geometry"', line) and "type_id" not in line:
            course = "geometry"
            chapter = None
        elif re.search(r'id:\s*"precalculus"', line):
            course = "precalculus"
            chapter = None
        elif re.search(r'id:\s*"(algebra_1|calculus|grade_6|pre_algebra)"', line) and "type_id" not in line:
            course = cm.group(1) if cm else "other"
            chapter = None

        ch = re.search(r'id:\s*"(review_of_algebra|beginning_algebra|functions)"', line)
        if ch and course in ("geometry", "algebra_2", "precalculus"):
            chapter = ch.group(1)

        if course == "geometry" and re.search(r'id:\s*"basics_of_geometry"', line):
            chapter = None

        tm = re.search(r'type_id:\s*"([^"]+)"', line)
        if not tm or course not in ("algebra_2", "geometry", "precalculus"):
            continue
        tid = tm.group(1)
        if course == "algebra_2":
            by_scope["algebra_2"].add(tid)
        elif course == "geometry" and chapter == "review_of_algebra":
            by_scope["geo_review"].add(tid)
        elif course == "precalculus":
            by_scope["precalculus"].add(tid)
    return by_scope


def prompt_sig(q) -> str:
    raw = (q.prompt_latex or q.prompt_text or "").strip()
    # normalize whitespace / seed noise lightly
    raw = re.sub(r"\s+", " ", raw)
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]


def looks_stub(prompt: str, entry) -> bool:
    p = prompt.lower()
    if re.search(r"\bscaffolded\b|placeholder|todo|fixme|not implemented", p):
        return True
    # precalc_foundations often says "Foundations:" or generic evaluate
    if entry.generator == "precalc_foundations":
        if "foundations" in p or "practice problem" in p:
            return True
    return False


def expects_graph(entry) -> bool:
    name = (entry.id + " " + entry.name).lower()
    tokens = (
        "graphing",
        "graph ",
        " graphs",
        "end behavior",
        "vertex",
        "parabola",
        "ellipse",
        "hyperbola",
        "circle graph",
        "transformations of graphs",
    )
    if any(t in name for t in tokens):
        # writing equations often no graph needed
        if "writing" in name and "graph" not in name:
            return False
        return True
    return False


def audit_entry(entry) -> dict:
    qt = QUESTION_TYPES.get(entry.id)
    issues: list[str] = []
    samples: dict[str, dict] = {}
    if qt is None:
        return {"id": entry.id, "generator": entry.generator, "issues": ["not registered"], "samples": {}}

    profile = getattr(qt, "setting_profile", None)
    presets = {
        tier: lookup_difficulty_preset(
            tier,
            type_id=entry.id,
            setting_profile=profile,
        )
        for tier in TIERS
    }
    # Also compare generator-keyed presets when catalog generator differs from type id
    gen = getattr(entry, "generator", None)
    if gen and not str(gen).startswith("hand_written:"):
        gen_presets = {
            tier: lookup_difficulty_preset(tier, type_id=gen, setting_profile=profile)
            for tier in TIERS
        }
    else:
        gen_presets = presets

    # Flat presets across tiers?
    check = gen_presets if gen_presets.get("easy") else presets
    if check["easy"] and check["medium"] and check["hard"]:
        if check["easy"] == check["medium"] == check["hard"]:
            issues.append("identical_presets_EMH")
        elif check["easy"] == check["medium"] or check["medium"] == check["hard"]:
            issues.append("partially_flat_presets")
    elif not (check.get("easy") or check.get("medium") or check.get("hard")):
        # No type/generator-specific presets — may still differ via profile
        pass

    sigs = []
    for tier in TIERS:
        settings = apply_difficulty_presets(
            {
                "count": 1,
                "difficulty_tier": tier,
                "include_answer_key": True,
                "include_diagram": True,
                "include_graph_metadata": True,
            },
            type_id=entry.id,
            setting_profile=getattr(qt, "setting_profile", None),
        )
        try:
            qs = qt.generate(settings)
        except Exception as exc:  # noqa: BLE001
            issues.append(f"{tier}:EXC:{exc}")
            samples[tier] = {"error": str(exc)}
            continue
        if not qs:
            issues.append(f"{tier}:empty")
            samples[tier] = {"empty": True}
            continue
        q = qs[0]
        prompt = (q.prompt_latex or q.prompt_text or "").strip()
        meta = q.metadata or {}
        sig = prompt_sig(q)
        sigs.append(sig)
        row = {
            "prompt": prompt[:220],
            "answer": (q.answer_latex or "")[:120],
            "sig": sig,
            "has_graph": bool(meta.get("graph_spec")),
            "has_diagram": bool(meta.get("diagram_svg")),
            "has_number_line": bool(meta.get("number_line_spec")),
        }
        samples[tier] = row
        if not prompt:
            issues.append(f"{tier}:blank_prompt")
        if looks_stub(prompt, entry):
            issues.append(f"{tier}:stub_prompt")
        if not (q.answer_latex or "").strip():
            issues.append(f"{tier}:missing_answer")
        if expects_graph(entry) and not (
            meta.get("graph_spec") or meta.get("diagram_svg") or meta.get("number_line_spec")
        ):
            issues.append(f"{tier}:missing_graph")

    if len(sigs) == 3 and len(set(sigs)) == 1:
        issues.append("identical_EMH_prompts")
    elif len(sigs) == 3 and len(set(sigs)) == 2:
        issues.append("weak_EMH_diversity")

    # Wrong-topic heuristics for known bad aliases
    gen = entry.generator
    name_l = entry.name.lower()
    id_l = entry.id.lower()
    if gen == "graph_quadratic" and any(
        t in id_l for t in ("rational", "exponential", "trig", "transformation", "polynomial_graphs", "ellipse", "hyperbola", "circle", "log")
    ):
        issues.append("wrong_topic_alias:graph_quadratic")
    if gen == "function_operations" and "vector" in id_l:
        issues.append("wrong_topic_alias:function_operations_for_vectors")
    if gen == "inverse_function_basic" and "matrix" in id_l:
        issues.append("wrong_topic_alias:inverse_fn_for_matrix")
    if gen == "pc_inverses" or (entry.id == "pc_inverses" and "matrix" in name_l):
        pass
    if gen == "precalc_foundations":
        issues.append("uses_precalc_foundations_stub")
    if gen == "stats_counting_principle" and "permutation" in id_l and "probability_with" not in id_l:
        # may still be ok for sample spaces
        pass
    if gen == "sequence_arithmetic_nth_term" and "geometric" in id_l:
        issues.append("wrong_topic_alias:arith_seq_for_geometric")
    if gen == "quadratic_vertex_form_write" and "conic" in id_l and "parabola" not in id_l:
        issues.append("wrong_topic_alias:vertex_write")

    return {
        "id": entry.id,
        "name": entry.name,
        "generator": entry.generator,
        "issues": issues,
        "samples": samples,
        "presets_equal_emh": "identical_presets_EMH" in issues,
    }


def catalog_by_id(cat):
    return {e.id: e for e in cat}


def safe_entry(tid: str, *maps):
    for m in maps:
        if tid in m:
            return m[tid]
    try:
        return get_catalog_entry(tid)
    except KeyError:
        pass
    # Hand-written / registered-only type (no catalog row)
    if tid in QUESTION_TYPES:
        from types import SimpleNamespace

        qt = QUESTION_TYPES[tid]
        return SimpleNamespace(
            id=tid,
            name=getattr(qt, "name", tid) or tid,
            generator=f"hand_written:{tid}",
            instruction_text=getattr(qt, "instruction_text", None),
        )
    return None


def main() -> None:
    scopes = parse_curriculum_type_ids()
    a2_map = catalog_by_id(A2)
    geo_map = catalog_by_id(GEO)
    pc_map = catalog_by_id(PC)
    print("Parsed curriculum scopes:", {k: len(v) for k, v in scopes.items()})

    a2_ids = sorted(scopes["algebra_2"]) or sorted(
        e.id for e in A2 if e.generator != "scaffold" and not type_not_ready(e.id)
    )
    geo_ids = sorted(scopes["geo_review"]) or [
        e.id for e in GEO if e.id.startswith("geo_review_") and e.generator != "scaffold"
    ]
    pc_foundation_ids = sorted(
        e.id
        for e in PC
        if e.generator == "precalc_foundations" and not type_not_ready(e.id)
    )
    pc_linked_ready = sorted(
        tid
        for tid in (scopes["precalculus"] or {e.id for e in PC})
        if tid in QUESTION_TYPES and not type_not_ready(tid)
    )

    targets: list[tuple[str, object]] = []
    seen: set[str] = set()
    skipped: list[str] = []

    def add(scope: str, tid: str, entry):
        if tid in seen:
            return
        if type_requires_diagram(tid) or type_not_ready(tid):
            skipped.append(f"{tid}:not_ready")
            return
        if entry is None:
            entry = safe_entry(tid, a2_map, geo_map, pc_map)
        if entry is None:
            skipped.append(f"{tid}:no_entry")
            return
        if getattr(entry, "generator", None) == "scaffold":
            skipped.append(f"{tid}:scaffold")
            return
        if tid not in QUESTION_TYPES:
            skipped.append(f"{tid}:unregistered")
            return
        seen.add(tid)
        targets.append((scope, entry))

    for tid in a2_ids:
        add("algebra_2", tid, safe_entry(tid, a2_map))
    for tid in geo_ids:
        add("geo_review", tid, safe_entry(tid, geo_map, a2_map))
    for tid in pc_foundation_ids:
        add("pc_foundations", tid, safe_entry(tid, pc_map))
    for tid in pc_linked_ready:
        if tid not in seen:
            add("pc_linked", tid, safe_entry(tid, pc_map, a2_map))
    print(f"Skipped: {len(skipped)} e.g. {skipped[:8]}")

    print(f"Auditing {len(targets)} types…")
    print(f"  algebra_2={sum(1 for s,_ in targets if s=='algebra_2')}")
    print(f"  geo_review={sum(1 for s,_ in targets if s=='geo_review')}")
    print(f"  pc_foundations={sum(1 for s,_ in targets if s=='pc_foundations')}")
    print(f"  pc_linked={sum(1 for s,_ in targets if s=='pc_linked')}")

    rows = []
    for i, (scope, entry) in enumerate(targets, 1):
        row = audit_entry(entry)
        row["scope"] = scope
        rows.append(row)
        if i % 25 == 0:
            bad_n = sum(1 for r in rows if r["issues"])
            print(f"  {i}/{len(targets)} (issues so far={bad_n})")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rows, indent=2), encoding="utf-8")

    # Text summary
    by_issue: dict[str, list[str]] = defaultdict(list)
    lines = [
        f"Audited: {len(rows)}",
        f"With issues: {sum(1 for r in rows if r['issues'])}",
        f"Clean: {sum(1 for r in rows if not r['issues'])}",
        "",
        "## Issue frequency",
    ]
    for r in rows:
        for iss in r["issues"]:
            key = iss.split(":")[0] if iss.startswith("wrong") or ":" not in iss else iss.split(":")[0]
            # group by issue kind
            kind = iss
            for prefix in (
                "identical_EMH_prompts",
                "identical_presets_EMH",
                "partially_flat_presets",
                "weak_EMH_diversity",
                "uses_precalc_foundations_stub",
                "wrong_topic_alias",
                "missing_answer",
                "missing_graph",
                "stub_prompt",
                "blank_prompt",
                "empty",
                "EXC",
                "not registered",
            ):
                if prefix in iss or iss.startswith(prefix):
                    kind = prefix
                    break
            by_issue[kind].append(r["id"])

    for kind, ids in sorted(by_issue.items(), key=lambda x: -len(x[1])):
        lines.append(f"  {kind}: {len(ids)}")

    lines.append("")
    lines.append("## Failures by type")
    for r in sorted(rows, key=lambda x: (0 if x["issues"] else 1, x["scope"], x["id"])):
        if not r["issues"]:
            continue
        lines.append(f"{r['scope']}\t{r['id']}\t{r['generator']}\t{'; '.join(r['issues'])}")

    lines.append("")
    lines.append("## Clean types (first 40)")
    clean = [r for r in rows if not r["issues"]]
    for r in clean[:40]:
        lines.append(f"  OK {r['scope']} {r['id']} ({r['generator']})")

    OUT_TXT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Wrote {OUT_TXT}")
    print(f"With issues: {sum(1 for r in rows if r['issues'])} / {len(rows)}")
    # Print top failures
    for kind, ids in sorted(by_issue.items(), key=lambda x: -len(x[1]))[:12]:
        print(f"  {kind}: {len(ids)} e.g. {ids[:3]}")


if __name__ == "__main__":
    main()
