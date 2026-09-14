"""A1 equations WP + systems algebra notes (remaining after skeletoned/linear skip).

Writes ``notes/<type_id>.md``. Does not implement engines.
Does not rewrite G6/PA notes or notes that already have openstax.org + old-path.
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

from question_engine.catalogs.algebra_1 import CATALOG
from question_engine.api.handler import _generate_for_type
from question_engine.frameworks.primitives.wp_packaging import looks_like_dumped_equation

OUT = Path(__file__).resolve().parent
MINE_EA = _ROOT / "scripts/output/example_mining/elementary-algebra-2e/stage1"
MINE_IA = _ROOT / "scripts/output/example_mining/intermediate-algebra-2e/stage1"
MINE_PA = _ROOT / "scripts/output/example_mining/prealgebra-2e/stage1"

DS = (0.0, 8.0, 16.0, 22.0)
SEEDS = (101, 207)

TARGET = {
    "mixture_word_problems",
    "distance_rate_time_word_problems",
    "work_word_problems",
    "age_word_problems",
    "coin_word_problems",
    "consecutive_integers_word_problems",
    "percent_word_problems",
    "systems_elimination",
    "systems_substitution",
    "systems_word_problems",
}

DUMP_MARKERS = (
    "the equation is",
    "giving $",
    "satisfy $",
    "reduces to $",
    "uses a proportion",
    "the costs satisfy",
    "the system is",
)

OPT_OUT: dict[str, dict[str, Any]] = {
    "systems_word_problems": {"use_legacy_systems": True},
}

EA = "https://openstax.org/books/elementary-algebra-2e/pages"
IA = "https://openstax.org/books/intermediate-algebra-2e/pages"
PA = "https://openstax.org/books/prealgebra-2e/pages"


def _cite(book: str, section: str, slug: str, mine: str | None = None, extra: list[str] | None = None):
    if book.startswith("Prealgebra"):
        base = PA
    elif book.startswith("Intermediate"):
        base = IA
    else:
        base = EA
    return {
        "book": book,
        "section": section,
        "url": f"{base}/{slug}",
        "mine": mine,
        "extra": extra or [],
    }


META: dict[str, dict[str, Any]] = {
    "mixture_word_problems": {
        "should": (
            "Story first: two concentrations / ticket prices / dry mix. D=0 one easy "
            "percent-mix or ticket frame with small ints. High D: find an amount given "
            "the blend percent. Never dump the equation. Not a systems leaf (EA 5.5)."
        ),
        "cites": [
            _cite(
                "Elementary Algebra 2e",
                "3.3 Solve Mixture Applications",
                "3-3-solve-mixture-applications",
                extra=["Coins / tickets / percent solutions as one linear equation."],
            ),
            _cite(
                "Intermediate Algebra 2e",
                "2.4 Solve Mixture and Uniform Motion Applications",
                "2-4-solve-mixture-and-uniform-motion-applications",
                "2-4-solve-mixture-and-uniform-motion-applications.json",
            ),
        ],
        "engine": (
            "Reuse MixtureProblemFramework + OpenStax story frames (wp_packaging style). "
            "Algebra stays one linear mix equation — not systems."
        ),
    },
    "distance_rate_time_word_problems": {
        "should": (
            "d=rt stories. D=0: one easy missing-piece (find distance or time) with "
            "small ints. High D: round-trip / opposite / catch-up. Several vehicles "
            "(bike / drive / walk / bus / train) — not one Mad-Lib. Never dump $d=rt$."
        ),
        "cites": [
            _cite(
                "Elementary Algebra 2e",
                "3.4 Solve Uniform Motion Applications",
                "3-4-solve-uniform-motion-applications",
                extra=["Opposite direction, same direction, round trip. Several vehicles."],
            ),
            _cite(
                "Intermediate Algebra 2e",
                "2.4 Solve Mixture and Uniform Motion Applications",
                "2-4-solve-mixture-and-uniform-motion-applications",
                "2-4-solve-mixture-and-uniform-motion-applications.json",
            ),
        ],
        "engine": (
            "Reuse DistanceRateTimeFramework + several OpenStax d=rt frames. "
            "Algebra shapes follow old path (missing piece → two-motion)."
        ),
    },
    "work_word_problems": {
        "should": (
            "Together / one-rate / pipes. D=0: two people finish a job in integer hours. "
            "High D: starts-later or three workers. Story first; not a dumped $1/a+1/b=1/t$."
        ),
        "cites": [
            _cite(
                "Elementary Algebra 2e",
                "8.8 Solve Uniform Motion and Work Applications",
                "8-8-solve-uniform-motion-and-work-applications",
                "8-8-solve-uniform-motion-and-work-applications.json",
            ),
        ],
        "engine": (
            "Reuse WorkProblemFramework. Optional later wrap in wp_packaging frames. "
            "Leave on dedicated work core — do not dump onto one-step SolveLinear."
        ),
    },
    "age_word_problems": {
        "should": (
            "Now / in-n-years / n-years-ago. D=0: one is k years older; sum is S. "
            "High D: both-in-the-future. Story, not “the equation is $x+(x+k)=S$”."
        ),
        "cites": [
            _cite(
                "Elementary Algebra 2e",
                "3.1 Use a Problem-Solving Strategy",
                "3-1-use-a-problem-solving-strategy",
                extra=["Number/age translate-then-solve (one equation)."],
            ),
            _cite(
                "Elementary Algebra 2e",
                "5.4 Solve Applications with Systems of Equations",
                "5-4-solve-applications-with-systems-of-equations",
                "5-4-solve-applications-with-systems-of-equations.json",
                extra=["Example 5.37 is an age *system* — keep two-variable ages on systems WP."],
            ),
        ],
        "engine": "Reuse AgeProblemFramework / narrative_wp. One equation, not systems.",
    },
    "coin_word_problems": {
        "should": (
            "Nickels/dimes/quarters value. D=0: two coin types, small counts. High D: "
            "three types or a “k more dimes than nickels” clause. Not a dumped value equation."
        ),
        "cites": [
            _cite(
                "Elementary Algebra 2e",
                "3.3 Solve Mixture Applications",
                "3-3-solve-mixture-applications",
                extra=["Coin/ticket value as a mixture application (0.05n+0.10d=…)."],
            ),
            _cite(
                "Prealgebra 2e",
                "9.2 Solve Money Applications",
                "9-2-solve-money-applications",
                extra=["PA money/tickets/coins — same algebra, simpler numbers at D=0."],
            ),
        ],
        "engine": "Reuse CoinProblemFramework / narrative_wp. Several coin-type frames.",
    },
    "consecutive_integers_word_problems": {
        "should": (
            "D=0: two or three consecutive integers, sum. High D: consecutive even/odd, "
            "or first+last. Translate the phrase; do not dump $n+(n+1)+(n+2)=S$."
        ),
        "cites": [
            _cite(
                "Elementary Algebra 2e",
                "3.1 Use a Problem-Solving Strategy",
                "3-1-use-a-problem-solving-strategy",
                extra=["Consecutive integer number problems (sum of three consecutive…)."],
            ),
            _cite(
                "Intermediate Algebra 2e",
                "2.2 Use a Problem Solving Strategy",
                "2-2-use-a-problem-solving-strategy",
                "2-2-use-a-problem-solving-strategy.json",
            ),
        ],
        "engine": "Reuse ConsecutiveIntegersFramework / narrative_wp. SolveLinear only as reverse algebra after a real stem.",
    },
    "percent_word_problems": {
        "should": (
            "D=0: find the part given percent of a whole (simple interest or discount). "
            "High D: mark-up then tax, or solve for the original. Retail/interest stories, "
            "not “the equation is $0.2x=12$”."
        ),
        "cites": [
            _cite(
                "Elementary Algebra 2e",
                "3.2 Solve Percent Applications",
                "3-2-solve-percent-applications",
                extra=["Percent of, discount, mark-up, simple interest."],
            ),
            _cite(
                "Intermediate Algebra 2e",
                "2.2 Use a Problem Solving Strategy",
                "2-2-use-a-problem-solving-strategy",
                "2-2-use-a-problem-solving-strategy.json",
            ),
        ],
        "engine": "Reuse PercentWordProblemFramework. Keep A1 as EA 3.2 percent applications, not a new engine.",
    },
    "systems_elimination": {
        "should": (
            "D=0: already opposite coeffs ($x+y=5$, $x-y=1$) or one add. High D: multiply "
            "one/both equations first; later no-solution / infinite. Prompt is the system, not a story."
        ),
        "cites": [
            _cite(
                "Elementary Algebra 2e",
                "5.3 Solve Systems of Equations by Elimination",
                "5-3-solve-systems-of-equations-by-elimination",
                "5-3-solve-systems-of-equations-by-elimination.json",
            ),
        ],
        "engine": "Reuse systems_elimination. New LinearSystem skeleton only if later A1 unification needs it — not this notes pass.",
    },
    "systems_substitution": {
        "should": (
            "D=0: one equation already solved for $y$ ($y=x+1$, $x+y=5$). High D: solve a "
            "first equation for a variable, then substitute; fractions later."
        ),
        "cites": [
            _cite(
                "Elementary Algebra 2e",
                "5.2 Solving Systems of Equations by Substitution",
                "5-2-solving-systems-of-equations-by-substitution",
                "5-2-solving-systems-of-equations-by-substitution.json",
            ),
        ],
        "engine": "Reuse systems_substitution (shared with pa_systems_substitution). No new engine this pass.",
    },
    "systems_word_problems": {
        "should": (
            "OpenStax EA 5.4: number, money/tickets, geometry, uniform motion. D=0 one easy "
            "number or tickets frame. Do **not** dump the system into the prompt."
        ),
        "cites": [
            _cite(
                "Elementary Algebra 2e",
                "5.4 Solve Applications with Systems of Equations",
                "5-4-solve-applications-with-systems-of-equations",
                "5-4-solve-applications-with-systems-of-equations.json",
            ),
        ],
        "engine": (
            "Reuse SystemsWP + wp_packaging frames (already the live default). "
            "Old path is use_legacy_systems dump stub — do not revive it."
        ),
        "force_flags": ["UNCLEAR", "LOW_VARIETY"],
        "flag_why": "Old opt-out dumps the system (“costs satisfy cases …”). OpenStax 5.4 has number, money, geometry, motion.",
    },
}


def _mine_path(fname: str) -> Path | None:
    for root in (MINE_EA, MINE_IA, MINE_PA):
        p = root / fname
        if p.exists():
            return p
    return None


def _extract_examples(fname: str, limit: int = 4) -> list[str]:
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
        if len(prompt) > 280:
            prompt = prompt[:277] + "…"
        if title and prompt:
            out.append(f"{title}: {prompt}")
        elif prompt:
            out.append(prompt)
        if len(out) >= limit:
            break
    return out


def _clip(s: str, n: int = 420) -> str:
    s = re.sub(r"\s+", " ", (s or "").strip())
    return s if len(s) <= n else s[: n - 1] + "…"


def sample_type(type_id: str) -> dict[str, Any]:
    extra = dict(OPT_OUT.get(type_id) or {})
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
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
                meta = q.metadata or {}
                prompt = q.prompt_latex or q.prompt_text or ""
                rows.append(
                    {
                        "d": d,
                        "seed": seed,
                        "prompt": prompt,
                        "answer": q.answer_latex or "",
                        "pattern": meta.get("skeleton_pattern") or "",
                        "frame_id": meta.get("frame_id") or "",
                        "has_figure": bool(
                            meta.get("figure")
                            or meta.get("diagram")
                            or meta.get("number_line_spec")
                            or meta.get("coordinate_plane")
                        ),
                    }
                )
            except Exception as exc:  # noqa: BLE001
                errors.append(f"D={d} seed={seed}: {exc}")
                rows.append({"d": d, "seed": seed, "error": str(exc)})
    return {"rows": rows, "errors": errors, "opt_out": extra}


def _flags_for(type_id: str, sampled: dict[str, Any]) -> tuple[list[str], str]:
    meta = META.get(type_id) or {}
    flags = list(meta.get("force_flags") or [])
    why = str(meta.get("flag_why") or "")
    prompts = [str(r.get("prompt") or "") for r in sampled.get("rows") or [] if not r.get("error")]
    blob = "\n".join(prompts).lower()
    dump = any(m in blob for m in DUMP_MARKERS) or any(
        looks_like_dumped_equation(p) for p in prompts if p
    )
    if dump and "UNCLEAR" not in flags:
        flags.append("UNCLEAR")
    if dump and "LOW_VARIETY" not in flags:
        flags.append("LOW_VARIETY")
        if not why:
            why = "Old path looks like an equation-dump stub."
    d0 = [
        re.sub(r"\d+", "N", r.get("prompt") or "")
        for r in sampled.get("rows") or []
        if r.get("d") == 0 and r.get("prompt")
    ]
    if (
        type_id.endswith("word_problems")
        and len(d0) >= 2
        and len(set(d0)) == 1
        and "LOW_VARIETY" not in flags
    ):
        flags.append("LOW_VARIETY")
        if not why:
            why = "One template across seeds at D=0."
    return flags, why


def _has_openstax_notes(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    return "openstax.org" in text and "What old path actually produced" in text


def render_notes(entry, sampled: dict[str, Any]) -> str:
    type_id = entry.id
    meta = META.get(type_id) or {}
    flags, why = _flags_for(type_id, sampled)
    banner = ""
    if flags:
        banner = (
            f"> **{' / '.join(flags)}**"
            + (f" — {why}" if why else "")
            + "\n\n"
        )
    opt = sampled.get("opt_out") or {}
    opt_line = (
        f"Old-path extra settings: `{json.dumps(opt)}`."
        if opt
        else "No skeleton opt-out (old path is the live default)."
    )

    lines = [
        f"# `{type_id}` — {entry.name}",
        "",
        banner.rstrip(),
        "",
        f"- **Course:** Algebra 1 (A1 catalog)",
        f"- **Category:** {entry.category}",
        f"- **Generator:** `{entry.generator}`",
        f"- **Already on skeleton?** {'yes' if type_id == 'systems_word_problems' else 'no'}",
        f"- **{opt_line}**",
        "",
        "## What the question should look like (D=0 vs high D)",
        "",
        meta.get("should") or "Match old-path algebra shapes; copy OpenStax example shapes below.",
        "",
        "## What old path actually produced",
        "",
        "Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).",
        "",
    ]
    by_d: dict[float, list[dict[str, Any]]] = {}
    for row in sampled.get("rows") or []:
        by_d.setdefault(float(row["d"]), []).append(row)
    for d in DS:
        lines.append(f"### D={int(d) if d == int(d) else d}")
        lines.append("")
        for row in by_d.get(d, []):
            if row.get("error"):
                lines.append(f"- seed {row['seed']}: **ERROR** `{row['error']}`")
                continue
            extra = []
            if row.get("pattern"):
                extra.append(f"pattern=`{row['pattern']}`")
            if row.get("frame_id"):
                extra.append(f"frame=`{row['frame_id']}`")
            if row.get("has_figure"):
                extra.append("has_figure")
            tag = f" ({', '.join(extra)})" if extra else ""
            lines.append(f"- seed {row['seed']}{tag}:")
            lines.append(f"  - prompt: `{_clip(row.get('prompt') or '')}`")
            if row.get("answer"):
                lines.append(f"  - answer: `{_clip(str(row['answer']), 200)}`")
        lines.append("")

    if sampled.get("errors"):
        lines.append("Generation errors:")
        for e in sampled["errors"]:
            lines.append(f"- {e}")
        lines.append("")

    lines.extend(["## OpenStax examples + chapter/section cites", ""])
    for c in meta.get("cites") or []:
        lines.append(f"### {c['book']} — {c['section']}")
        lines.append("")
        lines.append(f"- {c['url']}")
        examples = _extract_examples(c["mine"]) if c.get("mine") else []
        if examples:
            lines.append("- Mined examples:")
            for ex in examples:
                lines.append(f"  - {ex}")
        for extra in c.get("extra") or []:
            lines.append(f"- Shape: {extra}")
        if not examples and not c.get("extra"):
            lines.append("- (no local mine items; use the section URL)")
        lines.append("")

    lines.extend(
        [
            "## Variety notes",
            "",
            why or "Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.",
            "",
            "## Proposed engine (reuse vs new)",
            "",
            meta.get("engine") or "TBD after samples — do not implement in this pass.",
            "",
            "_Proposal only. No engine implementation in this notes pass._",
            "",
        ]
    )
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    summary: dict[str, Any] = {
        "written": [],
        "skipped": [],
        "unclear": [],
        "low_variety": [],
        "errors": {},
    }
    by_id = {e.id: e for e in CATALOG}
    for type_id in sorted(TARGET):
        entry = by_id[type_id]
        path = OUT / f"{type_id}.md"
        if _has_openstax_notes(path):
            summary["skipped"].append(type_id)
            continue
        sampled = sample_type(type_id)
        flags, _why = _flags_for(type_id, sampled)
        if "UNCLEAR" in flags:
            summary["unclear"].append(type_id)
        if "LOW_VARIETY" in flags:
            summary["low_variety"].append(type_id)
        if sampled.get("errors"):
            summary["errors"][type_id] = sampled["errors"]
        path.write_text(render_notes(entry, sampled), encoding="utf-8")
        summary["written"].append(type_id)
        print(f"wrote {type_id} flags={flags}", flush=True)

    (OUT / "_a1_eq_wp_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "errors"}, indent=2))


if __name__ == "__main__":
    main()
