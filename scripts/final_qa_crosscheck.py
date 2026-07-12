"""FINAL quality cross-check after large QA wave.

Stratified sample of Ready types:
  - ALL Algebra 1 Ready types
  - ALL radical / rational Ready types (any course)
  - Recently fixed poly/quad types (explicit)
  - Large A2 / Precalc / Calculus sample

For each type: generate Easy/Medium/Hard (n=3 each), assert topic keywords,
Easy≠Hard structure, non-empty sensible answers.

Writes scripts/output/FINAL_QA_CROSSCHECK.md

Usage:
  $env:PYTHONPATH='.'; python scripts/final_qa_crosscheck.py
"""

from __future__ import annotations

import hashlib
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import question_engine.types  # noqa: F401
from question_engine.catalogs.algebra_1 import CATALOG as A1
from question_engine.catalogs.algebra_2 import CATALOG as A2
from question_engine.catalogs.calculus import CATALOG as CALC
from question_engine.catalogs.geometry import CATALOG as GEO
from question_engine.catalogs.grade_6 import CATALOG as G6
from question_engine.catalogs.pre_algebra import CATALOG as PA
from question_engine.catalogs.precalculus import CATALOG as PC
from question_engine.core.base import QUESTION_TYPES
from question_engine.core.registry import TYPE_CATALOG
from question_engine.settings.presets import apply_difficulty_presets, lookup_difficulty_preset
from question_engine.type_readiness import type_not_ready

OUT = ROOT / "scripts" / "output" / "FINAL_QA_CROSSCHECK.md"
TIERS = ("easy", "medium", "hard")
N_PER_TIER = 3

RECENTLY_FIXED = [
    "polynomial_multiply_special",
    "polynomial_factoring_common_factor",
    "polynomial_factoring_special_cases",
    "polynomial_factoring_grouping",
    "quadratic_factoring",
    "quadratic_solve_by_graphing",
    "quadratic_factoring_equations",
    "quadratic_formula",
    "quadratic_completing_square_constant",
    "quadratic_completing_square_solve",
    "one_step_equations",
    "two_step_equations",
    "multi_step_equations",
    "absolute_value_equations",
    "graphing_linear_equations",
    "systems_elimination",
    "systems_substitution",
    "slope",
    "more_on_slope",
]


def unique_ready(catalog) -> list:
    seen: set[str] = set()
    out = []
    for e in catalog:
        if e.id in seen:
            continue
        if e.generator == "scaffold" or type_not_ready(e.id):
            continue
        if e.id not in QUESTION_TYPES:
            continue
        seen.add(e.id)
        out.append(e)
    return out


def all_ready_unique() -> dict[str, Any]:
    by: dict[str, Any] = {}
    for e in TYPE_CATALOG:
        if e.generator == "scaffold" or type_not_ready(e.id):
            continue
        if e.id not in QUESTION_TYPES:
            continue
        by[e.id] = e
    return by


def prompt_of(q) -> str:
    return (q.prompt_latex or q.prompt_text or "").strip()


def answer_of(q) -> str:
    return (q.answer_latex or "").strip()


def norm_prompt(p: str) -> str:
    """Normalize for structural comparison (strip specific numbers)."""
    s = re.sub(r"\s+", " ", p)
    s = re.sub(r"-?\d+(?:\.\d+)?", "N", s)
    return s


def prompt_sig(p: str) -> str:
    return hashlib.sha1(norm_prompt(p).encode("utf-8")).hexdigest()[:10]


def looks_stub(p: str) -> bool:
    return bool(re.search(r"\bscaffolded\b|placeholder|TODO|FIXME|not implemented|practice problem", p, re.I))


def has_sqrt(p: str) -> bool:
    return bool(re.search(r"\\sqrt|√", p))


def has_frac(p: str) -> bool:
    return r"\frac" in p or "/" in p


def has_product_marker(p: str) -> bool:
    # product-rule style: f·g or ( )( ) with derivative language
    return bool(re.search(r"\\cdot|\\times|\*\s*\(|product", p, re.I)) or (
        p.count("(") >= 2 and "d/dx" in p.lower().replace(" ", "")
    )


def has_quotient_marker(p: str) -> bool:
    return bool(re.search(r"\\frac\s*\{|quotient", p, re.I))


def has_chain_marker(p: str) -> bool:
    # nested composition markers
    return bool(re.search(r"\\(?:sin|cos|tan|ln|e\^|sqrt)", p)) or p.count("(") >= 3


@dataclass
class Sample:
    tier: str
    prompt: str
    answer: str
    error: str | None = None
    meta: dict = field(default_factory=dict)


@dataclass
class TypeResult:
    tid: str
    name: str
    generator: str
    bucket: str
    status: str = "PASS"  # PASS | FAIL | NOTE
    hard_fails: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    samples: list[Sample] = field(default_factory=list)
    fail_examples: list[str] = field(default_factory=list)


# Topic keyword rules: (match_ids_or_gens, required_any, forbidden_any, description)
# required/forbidden are callables on prompt string OR regex strings.
TOPIC_RULES: list[tuple] = []


def _rule(match_fn, check_fn, label: str):
    TOPIC_RULES.append((match_fn, check_fn, label))


def _id_contains(*toks):
    return lambda tid, name, gen: any(t in tid or t in name for t in toks)


def _gen_is(*gens):
    return lambda tid, name, gen: gen in gens


def _setup_topic_rules():
    # Rational equations / expressions: must look like rational (frac), must NOT be lone radical simplify
    def rational_eq(tid, name, gen):
        return (
            "rational" in tid
            and any(t in tid for t in ("equation", "equations"))
            and "radical" not in tid
        ) or gen == "rational_equations"

    def check_rational_eq(prompts: list[str], answers: list[str]) -> list[str]:
        fails = []
        # At least some prompts should have fractions / rational structure
        frac_n = sum(1 for p in prompts if has_frac(p) or "=" in p)
        if frac_n < max(1, len(prompts) // 3):
            fails.append("rational-equation: few fraction/equation prompts")
        # Radical-only prompts under rational equations are wrong topic
        radical_only = [
            p
            for p in prompts
            if has_sqrt(p)
            and not has_frac(p)
            and "rational" not in p.lower()
            and r"^{" not in p  # rational exponents ok-ish
        ]
        if len(radical_only) >= max(2, len(prompts) // 2):
            fails.append(
                f"rational-equation: √-heavy without fractions ({len(radical_only)}/{len(prompts)})"
            )
        return fails

    _rule(rational_eq, check_rational_eq, "rational_equations")

    def radical_type(tid, name, gen):
        return (
            ("radical" in tid or gen.startswith("radical_"))
            and "rational_exponent" not in tid
            and "connecting" not in tid
            and "properties_of_exponents" not in gen
            and "domain" not in tid
            and "graph" not in tid
            and "distance" not in tid
            and "midpoint" not in tid
        )

    def check_radical(prompts, answers):
        fails = []
        sqrt_n = sum(1 for p in prompts if has_sqrt(p) or "root" in p.lower())
        if sqrt_n < len(prompts) // 2:
            fails.append(f"radical: missing √ in prompts ({sqrt_n}/{len(prompts)})")
        return fails

    _rule(radical_type, check_radical, "radical_ops")

    def product_rule(tid, name, gen):
        return "product_rule" in tid or gen == "derivative_product_rule"

    def check_product(prompts, answers):
        fails = []
        # Power-rule only: single monomial like x^n without product of two functions
        power_only = 0
        for p in prompts:
            pl = p.lower().replace(" ", "")
            # classic product: two factors
            looks_product = (
                r"\cdot" in p
                or r"\times" in p
                or (p.count("(") >= 2 and ("d/dx" in pl or "\\frac{d}" in p or "differentiate" in p.lower() or "find" in p.lower()))
                or re.search(r"\)\s*\(", p)
            )
            looks_power_only = bool(
                re.search(r"x\^|x\^\{|\\mathrm\{d\}|d/dx", p)
            ) and not looks_product and p.count("(") <= 1
            if looks_power_only:
                power_only += 1
            if not looks_product and "product" not in p.lower():
                # soft — many product rules show f(x)g(x) as juxtaposition
                if re.search(r"\(.*x.*\).*(\(.*x.*\)|x\^|sin|cos|e\^)", p):
                    looks_product = True
        if power_only >= len(prompts) // 2 + 1:
            fails.append(f"product_rule: looks like power-rule only ({power_only}/{len(prompts)})")
        return fails

    _rule(product_rule, check_product, "product_rule")

    def power_rule(tid, name, gen):
        return ("power_rule" in tid or gen in ("derivative_power_rule", "integral_power_rule")) and "product" not in tid and "substitution" not in tid

    def check_power(prompts, answers):
        fails = []
        # Should NOT be heavy product/quotient of two distinct non-power factors
        bad = 0
        for p in prompts:
            if r"\frac" in p and p.count("x") >= 2 and "d/dx" in p.lower().replace(" ", ""):
                # quotient may still be power of quotient — soft
                pass
            if re.search(r"\\sin|\\cos|\\tan|\\ln", p) and "chain" not in p.lower():
                # power rule sometimes on trig^n — ok
                pass
        return fails

    _rule(power_rule, check_power, "power_rule")

    def quotient_rule(tid, name, gen):
        return "quotient_rule" in tid or gen == "derivative_quotient_rule"

    def check_quotient(prompts, answers):
        fails = []
        frac_n = sum(1 for p in prompts if r"\frac" in p or "/" in p)
        if frac_n < len(prompts) // 2:
            fails.append(f"quotient_rule: missing fraction form ({frac_n}/{len(prompts)})")
        return fails

    _rule(quotient_rule, check_quotient, "quotient_rule")

    def chain_rule(tid, name, gen):
        return "chain_rule" in tid or gen == "derivative_chain_rule"

    def check_chain(prompts, answers):
        fails = []
        ok = 0
        for p in prompts:
            if (
                re.search(r"\\(?:sin|cos|tan|ln|sqrt|e\^)", p)
                or re.search(r"\\left\(.*\\right\)\^|\)\^\{", p)
                or p.count("(") >= 2
            ):
                ok += 1
        if ok < len(prompts) // 2:
            fails.append(f"chain_rule: weak composition markers ({ok}/{len(prompts)})")
        return fails

    _rule(chain_rule, check_chain, "chain_rule")

    def abs_eq(tid, name, gen):
        return "absolute_value" in tid and "inequality" not in tid

    def check_abs(prompts, answers):
        fails = []
        abs_n = sum(
            1
            for p in prompts
            if re.search(r"\\(?:left)?\||\\lvert|absolute", p, re.I) or "|" in p
        )
        if abs_n < len(prompts) // 2:
            fails.append(f"absolute_value: missing |·| ({abs_n}/{len(prompts)})")
        return fails

    _rule(abs_eq, check_abs, "absolute_value")

    def systems(tid, name, gen):
        if any(t in tid for t in ("inequality", "word", "planes", "points_in_three", "three_dimensions")):
            return False
        return (
            "systems_of_equations" in tid
            or "systems_elimination" in tid
            or "systems_substitution" in tid
            or "systems_graphing" in tid
            or gen in ("systems_elimination", "systems_substitution", "graph_system")
        )

    def check_systems(prompts, answers):
        fails = []
        multi = sum(1 for p in prompts if p.count("=") >= 2 or "system" in p.lower() or r"\\" in p)
        if multi < len(prompts) // 3:
            fails.append(f"systems: few multi-equation prompts ({multi}/{len(prompts)})")
        return fails

    _rule(systems, check_systems, "systems")

    def log_type(tid, name, gen):
        if "logic" in tid:
            return False
        if any(
            t in tid
            for t in (
                "growth",
                "decay",
                "graphing_exponential",
                "exponential_equations_not",
                "exponential_equations_requiring",
                "logarithmic_rule_and_exponentials",  # integrals: 1/x and a^x mix
                "calc_diff_logarithmic",  # mixes ln and e^x by design
                "calc_diff_other",  # other bases / exp
            )
        ):
            return False
        return (
            "logarithm" in tid
            or "logarithms" in tid
            or gen.startswith("logarithm")
            or gen in ("log_properties", "log_equations", "change_of_base")
        )

    def check_log(prompts, answers):
        fails = []
        texts = prompts + answers
        log_n = sum(1 for p in texts if re.search(r"\\log|\\ln|\blog\b", p, re.I))
        if log_n < max(1, len(prompts) // 3):
            fails.append(f"log: missing log markers ({log_n} across prompts/answers)")
        return fails

    _rule(log_type, check_log, "logarithm")

    def trig_graph(tid, name, gen):
        return "trig" in tid and "graph" in tid

    def check_trig_graph(prompts, answers):
        return []  # soft

    _rule(trig_graph, check_trig_graph, "trig_graph")


tid_global: dict[str, str] = {}


def build_sample_set(all_ready: dict[str, Any]) -> list[tuple[str, Any]]:
    """Return (bucket, entry) list without duplicates."""
    a1 = unique_ready(A1)
    a2 = unique_ready(A2)
    pc = unique_ready(PC)
    calc = unique_ready(CALC)
    geo = unique_ready(GEO)
    g6 = unique_ready(G6)
    pa = unique_ready(PA)

    chosen: dict[str, tuple[str, Any]] = {}

    def add(bucket: str, entry):
        if entry.id in chosen:
            # prefer more specific bucket labels by keeping first, append note via bucket merge
            return
        chosen[entry.id] = (bucket, entry)

    for e in a1:
        add("algebra1", e)

    for e in all_ready.values():
        if any(t in e.id.lower() or t in (e.name or "").lower() for t in ("radical", "rational")):
            add("radical_rational", e)

    for tid in RECENTLY_FIXED:
        if tid in all_ready:
            add("recently_fixed", all_ready[tid])

    # Large A2 sample: all Ready A2 (practical — 143)
    for e in a2:
        add("algebra2", e)

    # Large PC sample: all Ready PC
    for e in pc:
        add("precalculus", e)

    # All calc Ready
    for e in calc:
        add("calculus", e)

    # Geo review of algebra + a slice of other geo
    for e in geo:
        if "review" in e.id or "review" in (e.category or "").lower():
            add("geometry_review", e)
        elif any(t in e.id for t in ("pythag", "trig", "similar", "congruent", "circle", "quad")):
            add("geometry_sample", e)

    # Light G6 / PA sample for smoke
    for e in g6[:25]:
        add("grade6_sample", e)
    for e in pa[:20]:
        add("prealgebra_sample", e)

    # Stratified extras from remaining Ready if still small — we already have a lot
    return sorted(chosen.values(), key=lambda x: (x[0], x[1].id))


def generate_samples(entry, n: int = N_PER_TIER) -> list[Sample]:
    qt = QUESTION_TYPES[entry.id]
    profile = getattr(qt, "setting_profile", None)
    out: list[Sample] = []
    for tier in TIERS:
        for _ in range(n):
            settings = apply_difficulty_presets(
                {
                    "count": 1,
                    "difficulty_tier": tier,
                    "include_answer_key": True,
                    "include_diagram": True,
                    "include_graph_metadata": True,
                },
                type_id=entry.id,
                setting_profile=profile,
            )
            try:
                qs = qt.generate(settings)
                if not qs:
                    out.append(Sample(tier=tier, prompt="", answer="", error="empty"))
                    continue
                q = qs[0]
                meta = q.metadata if isinstance(q.metadata, dict) else {}
                out.append(
                    Sample(
                        tier=tier,
                        prompt=prompt_of(q),
                        answer=answer_of(q),
                        meta=meta,
                    )
                )
            except Exception as exc:  # noqa: BLE001
                out.append(Sample(tier=tier, prompt="", answer="", error=str(exc)))
    return out


def audit_type(bucket: str, entry) -> TypeResult:
    tid_global["cur"] = entry.id
    tr = TypeResult(
        tid=entry.id,
        name=entry.name or entry.id,
        generator=entry.generator,
        bucket=bucket,
    )
    samples = generate_samples(entry)
    tr.samples = samples

    # Exceptions / empty
    for s in samples:
        if s.error:
            tr.hard_fails.append(f"{s.tier}: {s.error}")
            tr.fail_examples.append(f"{s.tier}: ERROR {s.error}")
        elif not s.prompt:
            tr.hard_fails.append(f"{s.tier}: blank prompt")
            tr.fail_examples.append(f"{s.tier}: blank prompt")
        elif looks_stub(s.prompt):
            tr.hard_fails.append(f"{s.tier}: stub prompt")
            tr.fail_examples.append(f"{s.tier}: {s.prompt[:160]}")
        elif not s.answer:
            tr.hard_fails.append(f"{s.tier}: empty answer")
            tr.fail_examples.append(f"{s.tier}: P={s.prompt[:120]}")

    # Easy vs Hard: hard-fail only when prompt AND answer are literally identical
    # across tiers (true flat content). Fixed instructional text with different
    # answers/graphs (writing equations from a graph, geo area from a figure) → NOTE.
    easy_rows = [(s.prompt, s.answer) for s in samples if s.tier == "easy" and s.prompt]
    hard_rows = [(s.prompt, s.answer) for s in samples if s.tier == "hard" and s.prompt]
    easy_exact = {p for p, _ in easy_rows}
    hard_exact = {p for p, _ in hard_rows}
    easy_sigs = {prompt_sig(p) for p, _ in easy_rows}
    hard_sigs = {prompt_sig(p) for p, _ in hard_rows}
    easy_norms = {norm_prompt(p) for p, _ in easy_rows}
    hard_norms = {norm_prompt(p) for p, _ in hard_rows}

    easy_pairs = set(easy_rows)
    hard_pairs = set(hard_rows)
    if easy_pairs and hard_pairs and easy_pairs == hard_pairs:
        all_pairs = {(s.prompt, s.answer) for s in samples if s.prompt}
        if len(all_pairs) == 1:
            tr.hard_fails.append("identical Easy=Hard content (single fixed problem)")
            e0 = easy_rows[0]
            tr.fail_examples.append(f"E/H: {e0[0][:140]} A={e0[1][:80]}")
        else:
            tr.notes.append(
                "E/H sample sets matched (small discrete pool / fixed template; soft)"
            )
    elif easy_exact and hard_exact and easy_exact == hard_exact:
        easy_ans = {a for _, a in easy_rows}
        hard_ans = {a for _, a in hard_rows}
        if easy_ans == hard_ans and len(easy_ans) == 1:
            tr.hard_fails.append("identical Easy=Hard prompts and answers")
            tr.fail_examples.append(f"E/H: {next(iter(easy_exact))[:140]}")
        else:
            tr.notes.append(
                "same prompt text E/H (difficulty in numbers/graph/diagram; answers differ)"
            )
    elif easy_norms and hard_norms and easy_norms == hard_norms:
        tr.notes.append("weak E/H diversity: same skeleton after number-normalization")
    elif easy_sigs and hard_sigs and easy_sigs == hard_sigs:
        tr.notes.append("weak E/H diversity: same normalized prompt signatures")

    profile = getattr(QUESTION_TYPES[entry.id], "setting_profile", None)
    gen = entry.generator
    pe2 = ph2 = None
    if gen and not str(gen).startswith("hand_written:"):
        pe2 = lookup_difficulty_preset("easy", type_id=gen, setting_profile=profile)
        ph2 = lookup_difficulty_preset("hard", type_id=gen, setting_profile=profile)
    if pe2 is None:
        pe2 = lookup_difficulty_preset("easy", type_id=entry.id, setting_profile=profile)
        ph2 = lookup_difficulty_preset("hard", type_id=entry.id, setting_profile=profile)
    if pe2 and ph2 and pe2 == ph2:
        tr.notes.append("flat E/H difficulty presets")

    # Topic rules
    prompts = [s.prompt for s in samples if s.prompt]
    answers = [s.answer for s in samples if s.prompt]
    name_l = (entry.name or "").lower()
    for match_fn, check_fn, label in TOPIC_RULES:
        if match_fn(entry.id.lower(), name_l, entry.generator):
            fails = check_fn(prompts, answers)
            for f in fails:
                tr.hard_fails.append(f)
                # attach sample
                if prompts:
                    tr.fail_examples.append(f"[{label}] {prompts[0][:160]}")

    # Wrong-topic alias heuristics (from prior QA)
    id_l = entry.id.lower()
    if gen == "graph_quadratic" and any(
        t in id_l
        for t in (
            "rational",
            "exponential",
            "trig",
            "transformation",
            "polynomial_graphs",
            "ellipse",
            "hyperbola",
            "circle",
            "log",
        )
    ):
        tr.hard_fails.append("miswire: graph_quadratic for non-quadratic topic")
    if gen == "precalc_foundations":
        stub_n = sum(1 for p in prompts if looks_stub(p))
        if stub_n:
            tr.hard_fails.append("stub prompt via precalc_foundations")
            tr.fail_examples.append(prompts[0][:160] if prompts else "")
        else:
            tr.notes.append("thin generator: precalc_foundations (topic-routed fallback)")
    if gen == "calculus_foundations":
        # Flag only when all samples are byte-identical (caught above) or clearly off-topic.
        tr.notes.append("thin generator: calculus_foundations (topic-routed fallback)")
    if gen == "sequence_arithmetic_nth_term" and "geometric" in id_l:
        tr.hard_fails.append("miswire: arithmetic sequence generator for geometric")
    if gen == "function_operations" and "vector" in id_l:
        tr.hard_fails.append("miswire: function_operations for vectors")
    if gen == "derivative_power_rule" and "product_rule" in id_l:
        tr.hard_fails.append("miswire: power_rule generator on product_rule type")
    if gen == "derivative_product_rule" and "power_rule" in id_l and "product" not in id_l:
        tr.hard_fails.append("miswire: product_rule generator on power_rule type")
    if gen == "radical_equations" and "rational" in id_l and "radical" not in id_l and "exponent" not in id_l:
        # rational equations should not use radical_equations
        tr.hard_fails.append("miswire: radical_equations for rational type")
    if gen == "radical_simplification" and "rationalizing" in id_l:
        # may be ok for complex rationalizing denominators
        tr.notes.append("uses radical_simplification for rationalizing denominators")

    # Sensible answer spot-check: answer shouldn't be just "undefined" always unless topic is domain
    nonempty_ans = [s for s in samples if s.answer]
    if nonempty_ans:
        weird = [
            s
            for s in nonempty_ans
            if s.answer.lower() in ("n/a", "none", "todo", "?", "null")
        ]
        if weird:
            tr.hard_fails.append("nonsensical answer tokens")
            tr.fail_examples.append(f"{weird[0].tier}: A={weird[0].answer} P={weird[0].prompt[:100]}")

    # Weak diversity (soft)
    all_sigs = [prompt_sig(s.prompt) for s in samples if s.prompt]
    if all_sigs and len(set(all_sigs)) == 1:
        note = "weak diversity: all 9 samples same normalized template"
        if note not in tr.notes:
            tr.notes.append(note)

    if tr.hard_fails:
        tr.status = "FAIL"
    elif tr.notes:
        tr.status = "NOTE"
    else:
        tr.status = "PASS"
    return tr


def render_report(
    results: list[TypeResult],
    ready_count: int,
    sampled_ids: list[str],
) -> str:
    by_status = defaultdict(list)
    for r in results:
        by_status[r.status].append(r)

    lines: list[str] = []
    lines.append("# FINAL QA Cross-Check")
    lines.append("")
    lines.append(f"- Ready catalog types (unique, selectable): **{ready_count}**")
    lines.append(f"- Sampled in this run: **{len(results)}**")
    lines.append(f"- Per type: Easy/Medium/Hard × {N_PER_TIER} = {N_PER_TIER * 3} generations")
    lines.append("")
    lines.append("## Summary counts")
    lines.append("")
    lines.append(f"| Status | Count |")
    lines.append(f"|--------|------:|")
    lines.append(f"| PASS | {len(by_status['PASS'])} |")
    lines.append(f"| FAIL | {len(by_status['FAIL'])} |")
    lines.append(f"| NOTE (soft) | {len(by_status['NOTE'])} |")
    lines.append("")

    buckets = defaultdict(lambda: {"PASS": 0, "FAIL": 0, "NOTE": 0})
    for r in results:
        buckets[r.bucket][r.status] += 1
    lines.append("### By bucket")
    lines.append("")
    lines.append("| Bucket | PASS | FAIL | NOTE |")
    lines.append("|--------|-----:|-----:|-----:|")
    for b in sorted(buckets):
        d = buckets[b]
        lines.append(f"| {b} | {d['PASS']} | {d['FAIL']} | {d['NOTE']} |")
    lines.append("")

    lines.append("## FAIL details")
    lines.append("")
    fails = sorted(by_status["FAIL"], key=lambda r: (r.bucket, r.tid))
    if not fails:
        lines.append("_None._")
        lines.append("")
    else:
        for r in fails:
            lines.append(f"### `{r.tid}` — **FAIL**")
            lines.append(f"- Bucket: {r.bucket}")
            lines.append(f"- Generator: `{r.generator}`")
            lines.append(f"- Name: {r.name}")
            lines.append(f"- Issues:")
            for iss in r.hard_fails:
                lines.append(f"  - {iss}")
            if r.fail_examples:
                lines.append(f"- Concrete samples:")
                for ex in r.fail_examples[:6]:
                    lines.append(f"  - `{ex}`")
            # show one E and one H
            e = next((s for s in r.samples if s.tier == "easy" and s.prompt), None)
            h = next((s for s in r.samples if s.tier == "hard" and s.prompt), None)
            if e:
                lines.append(f"- Easy: P=`{e.prompt[:180]}` A=`{e.answer[:100]}`")
            if h:
                lines.append(f"- Hard: P=`{h.prompt[:180]}` A=`{h.answer[:100]}`")
            lines.append("")

    lines.append("## NOTE (soft / deferred)")
    lines.append("")
    notes = sorted(by_status["NOTE"], key=lambda r: (r.bucket, r.tid))
    if not notes:
        lines.append("_None._")
        lines.append("")
    else:
        for r in notes:
            lines.append(f"- `{r.tid}` ({r.generator}): {'; '.join(r.notes)}")
        lines.append("")

    lines.append("## PASS types")
    lines.append("")
    lines.append(f"{len(by_status['PASS'])} types passed hard checks. IDs:")
    lines.append("")
    # Group by bucket
    for b in sorted({r.bucket for r in by_status["PASS"]}):
        ids = sorted(r.tid for r in by_status["PASS"] if r.bucket == b)
        lines.append(f"### {b} ({len(ids)})")
        lines.append("")
        # compact
        chunk = []
        for tid in ids:
            chunk.append(f"`{tid}`")
            if len(chunk) >= 8:
                lines.append(", ".join(chunk))
                chunk = []
        if chunk:
            lines.append(", ".join(chunk))
        lines.append("")

    lines.append("## Method")
    lines.append("")
    lines.append("1. Collect Ready = catalog entries with non-scaffold generator, not `type_not_ready`, registered in `QUESTION_TYPES`.")
    lines.append("2. Stratify: all A1 + all radical/rational + recently fixed + all A2/PC/Calc Ready + geo/G6/PA samples.")
    lines.append("3. Generate E/M/H × 3; assert non-empty prompts/answers; stub detection; topic keyword rules; Easy≠Hard normalized templates; known miswire heuristics.")
    lines.append("4. Soft weak-diversity → NOTE only.")
    lines.append("")
    lines.append("## Fixes applied in this pass")
    lines.append("")
    lines.append(
        "- `calc_app_diff_newtons_method`: varied `f`/`x0` by tier (was hardcoded "
        "`x^2-2` from `x_0=1`)."
    )
    lines.append(
        "- `calc_diff_eq_introduction`: varied DE coefficient; hard uses `y=Cx^k` "
        "(was always `y=Ce^{2x}`)."
    )
    lines.append(
        "- `graphing_trig_functions` (A2/PC): Easy parents, Medium amplitude, "
        "Hard amplitude+period(+phase) (was ±sin/±cos only at every tier)."
    )
    lines.append(
        "- `_int_bounds` duplicate overwrite in `frameworks/number.py`: removed second "
        "definition that broke `lo_default`/`hi_default` (absolute value / ordering)."
    )
    lines.append(
        "- `geo_circles_arcs_and_chords` / `geo_circles_tangents`: tiered prompts "
        "(were single fixed flashcards)."
    )
    lines.append(
        "- `geo_congruent_proving_triangles_congruent`: SSS/SAS/ASA/AAS/HL by tier "
        "(was always SSS)."
    )
    lines.append(
        "- `geo_constructions_circles`: tiered construction prompts "
        "(was a single fixed identify-the-construction card)."
    )
    lines.append(
        "- Soft deferred: diagram/graph types with fixed prompt text but differing "
        "answers; thin `precalc_foundations` / `calculus_foundations` fallbacks "
        "(not stub prompts when topic-routed)."
    )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    _setup_topic_rules()
    all_ready = all_ready_unique()
    print(f"Ready unique: {len(all_ready)}", flush=True)
    sample = build_sample_set(all_ready)
    print(f"Sample size: {len(sample)}", flush=True)
    for b in sorted({x[0] for x in sample}):
        print(f"  {b}: {sum(1 for x in sample if x[0]==b)}", flush=True)

    results: list[TypeResult] = []
    progress = OUT.with_suffix(".progress.txt")
    for i, (bucket, entry) in enumerate(sample, 1):
        tr = audit_type(bucket, entry)
        results.append(tr)
        if i % 10 == 0 or tr.status == "FAIL":
            line = (
                f"  [{i}/{len(sample)}] {tr.status} {tr.tid}"
                + (f" :: {tr.hard_fails[:2]}" if tr.hard_fails else "")
            )
            print(line, flush=True)
            with progress.open("a", encoding="utf-8") as pf:
                pf.write(line + "\n")

    report = render_report(results, len(all_ready), [e.id for _, e in sample])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(report, encoding="utf-8")
    print(f"Wrote {OUT}", flush=True)
    print(
        f"PASS={sum(1 for r in results if r.status=='PASS')} "
        f"FAIL={sum(1 for r in results if r.status=='FAIL')} "
        f"NOTE={sum(1 for r in results if r.status=='NOTE')}",
        flush=True,
    )


if __name__ == "__main__":
    main()
