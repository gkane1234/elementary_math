"""Topic-fit heuristics for question QA.

Focus: prompts match the curriculum topic / method / difficulty shape.
Does NOT verify mathematical correctness of answer keys.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from typing import Any, Callable

from question_engine.catalogs.base import TypeCatalogEntry
from question_engine.core.base import QUESTION_TYPES
from question_engine.core.registry import TYPE_CATALOG
from question_engine.settings.presets import lookup_difficulty_preset
from question_engine.type_readiness import type_not_ready

# ---------------------------------------------------------------------------
# Family presets (type_id lists)
# ---------------------------------------------------------------------------

POLY_QUAD_TYPE_IDS: tuple[str, ...] = (
    "polynomial_naming",
    "polynomial_add_subtract",
    "polynomial_multiply",
    "polynomial_multiply_special",
    "polynomial_factoring_common_factor",
    "quadratic_factoring",
    "polynomial_factoring_special_cases",
    "polynomial_factoring_grouping",
    "quadratic_solve_by_graphing",
    "quadratic_square_roots",
    "quadratic_factoring_equations",
    "quadratic_formula",
    "quadratic_discriminant",
    "quadratic_completing_square_constant",
    "quadratic_completing_square_solve",
)

A1_EQUATIONS_TYPE_IDS: tuple[str, ...] = (
    "one_step_equations",
    "two_step_equations",
    "multi_step_equations",
    "absolute_value_equations",
    "systems_elimination",
    "systems_substitution",
    "systems_graphing",
)

RADICAL_RATIONAL_TYPE_IDS: tuple[str, ...] = (
    "radical_simplification",
    "radical_add_subtract",
    "radical_multiply",
    "radical_divide",
    "radical_equations",
    "radical_distance_formula",
    "radical_midpoint_formula",
    "rational_simplification",
    "rational_expression_multiply_divide",
    "rational_expression_simplification",
    "rational_expressions_equations",
)

GRAPHING_LINEAR_TYPE_IDS: tuple[str, ...] = (
    "graphing_linear_equations",
    "slope",
    "more_on_slope",
    "graph_linear_inequality",
    "graph_inequality_number_line",
)

FAMILIES: dict[str, tuple[str, ...]] = {
    "poly_quad": POLY_QUAD_TYPE_IDS,
    "a1_equations": A1_EQUATIONS_TYPE_IDS,
    "radical_rational": RADICAL_RATIONAL_TYPE_IDS,
    "graphing_linear": GRAPHING_LINEAR_TYPE_IDS,
}


# ---------------------------------------------------------------------------
# Prompt helpers
# ---------------------------------------------------------------------------


def prompt_of(q: Any) -> str:
    return (getattr(q, "prompt_latex", None) or getattr(q, "prompt_text", None) or "").strip()


def norm_prompt(p: str) -> str:
    s = re.sub(r"\s+", " ", p)
    s = re.sub(r"-?\d+(?:\.\d+)?", "N", s)
    return s


def prompt_sig(p: str) -> str:
    return hashlib.sha1(norm_prompt(p).encode("utf-8")).hexdigest()[:10]


def looks_stub(prompt: str, generator: str | None = None) -> bool:
    p = prompt.lower()
    if re.search(r"\bscaffolded\b|placeholder|todo|fixme|not implemented|practice problem", p):
        return True
    if generator == "precalc_foundations" and ("foundations" in p or "practice problem" in p):
        return True
    return False


def has_sqrt(p: str) -> bool:
    return bool(re.search(r"\\sqrt|√", p))


def has_frac(p: str) -> bool:
    return r"\frac" in p or "/" in p


# ---------------------------------------------------------------------------
# Topic keyword rules (prompt structure only)
# ---------------------------------------------------------------------------

TopicMatchFn = Callable[[str, str, str], bool]
TopicCheckFn = Callable[[list[str]], list[str]]

TOPIC_RULES: list[tuple[TopicMatchFn, TopicCheckFn, str]] = []


def _rule(match_fn: TopicMatchFn, check_fn: TopicCheckFn, label: str) -> None:
    TOPIC_RULES.append((match_fn, check_fn, label))


def _setup_topic_rules() -> None:
    if TOPIC_RULES:
        return

    def rational_eq(tid: str, name: str, gen: str) -> bool:
        return (
            "rational" in tid
            and any(t in tid for t in ("equation", "equations"))
            and "radical" not in tid
        ) or gen == "rational_equations"

    def check_rational_eq(prompts: list[str]) -> list[str]:
        fails: list[str] = []
        frac_n = sum(1 for p in prompts if has_frac(p) or "=" in p)
        if frac_n < max(1, len(prompts) // 3):
            fails.append("rational-equation: few fraction/equation prompts")
        radical_only = [
            p
            for p in prompts
            if has_sqrt(p)
            and not has_frac(p)
            and "rational" not in p.lower()
            and r"^{" not in p
        ]
        if len(radical_only) >= max(2, len(prompts) // 2):
            fails.append(
                f"rational-equation: √-heavy without fractions ({len(radical_only)}/{len(prompts)})"
            )
        return fails

    _rule(rational_eq, check_rational_eq, "rational_equations")

    def radical_type(tid: str, name: str, gen: str) -> bool:
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

    def check_radical(prompts: list[str]) -> list[str]:
        fails: list[str] = []
        sqrt_n = sum(1 for p in prompts if has_sqrt(p) or "root" in p.lower())
        if sqrt_n < len(prompts) // 2:
            fails.append(f"radical: missing √ in prompts ({sqrt_n}/{len(prompts)})")
        return fails

    _rule(radical_type, check_radical, "radical_ops")

    def product_rule(tid: str, name: str, gen: str) -> bool:
        return "product_rule" in tid or gen == "derivative_product_rule"

    def check_product(prompts: list[str]) -> list[str]:
        fails: list[str] = []
        power_only = 0
        for p in prompts:
            pl = p.lower().replace(" ", "")
            looks_product = (
                r"\cdot" in p
                or r"\times" in p
                or (
                    p.count("(") >= 2
                    and (
                        "d/dx" in pl
                        or "\\frac{d}" in p
                        or "differentiate" in p.lower()
                        or "find" in p.lower()
                    )
                )
                or re.search(r"\)\s*\(", p)
            )
            looks_power_only = bool(re.search(r"x\^|x\^\{|\\mathrm\{d\}|d/dx", p)) and (
                not looks_product and p.count("(") <= 1
            )
            if looks_power_only:
                power_only += 1
            if not looks_product and "product" not in p.lower():
                if re.search(r"\(.*x.*\).*(\(.*x.*\)|x\^|sin|cos|e\^)", p):
                    looks_product = True
        if power_only >= len(prompts) // 2 + 1:
            fails.append(f"product_rule: looks like power-rule only ({power_only}/{len(prompts)})")
        return fails

    _rule(product_rule, check_product, "product_rule")

    def quotient_rule(tid: str, name: str, gen: str) -> bool:
        return "quotient_rule" in tid or gen == "derivative_quotient_rule"

    def check_quotient(prompts: list[str]) -> list[str]:
        fails: list[str] = []
        frac_n = sum(1 for p in prompts if r"\frac" in p or "/" in p)
        if frac_n < len(prompts) // 2:
            fails.append(f"quotient_rule: missing fraction form ({frac_n}/{len(prompts)})")
        return fails

    _rule(quotient_rule, check_quotient, "quotient_rule")

    def chain_rule(tid: str, name: str, gen: str) -> bool:
        return "chain_rule" in tid or gen == "derivative_chain_rule"

    def check_chain(prompts: list[str]) -> list[str]:
        fails: list[str] = []
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

    def abs_eq(tid: str, name: str, gen: str) -> bool:
        return "absolute_value" in tid and "inequality" not in tid

    def check_abs(prompts: list[str]) -> list[str]:
        fails: list[str] = []
        abs_n = sum(
            1
            for p in prompts
            if re.search(r"\\(?:left)?\||\\lvert|absolute", p, re.I) or "|" in p
        )
        if abs_n < len(prompts) // 2:
            fails.append(f"absolute_value: missing |·| ({abs_n}/{len(prompts)})")
        return fails

    _rule(abs_eq, check_abs, "absolute_value")

    def systems(tid: str, name: str, gen: str) -> bool:
        if any(
            t in tid
            for t in ("inequality", "word", "planes", "points_in_three", "three_dimensions")
        ):
            return False
        return (
            "systems_of_equations" in tid
            or "systems_elimination" in tid
            or "systems_substitution" in tid
            or "systems_graphing" in tid
            or gen in ("systems_elimination", "systems_substitution", "graph_system")
        )

    def check_systems(prompts: list[str]) -> list[str]:
        fails: list[str] = []
        multi = sum(
            1 for p in prompts if p.count("=") >= 2 or "system" in p.lower() or r"\\" in p
        )
        if multi < len(prompts) // 3:
            fails.append(f"systems: few multi-equation prompts ({multi}/{len(prompts)})")
        return fails

    _rule(systems, check_systems, "systems")

    def log_type(tid: str, name: str, gen: str) -> bool:
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
                "logarithmic_rule_and_exponentials",
                "calc_diff_logarithmic",
                "calc_diff_other",
            )
        ):
            return False
        return (
            "logarithm" in tid
            or "logarithms" in tid
            or gen.startswith("logarithm")
            or gen in ("log_properties", "log_equations", "change_of_base")
        )

    def check_log(prompts: list[str]) -> list[str]:
        fails: list[str] = []
        log_n = sum(1 for p in prompts if re.search(r"\\log|\\ln|\blog\b", p, re.I))
        if log_n < max(1, len(prompts) // 3):
            fails.append(f"log: missing log markers ({log_n}/{len(prompts)})")
        return fails

    _rule(log_type, check_log, "logarithm")


_setup_topic_rules()


# ---------------------------------------------------------------------------
# Miswire heuristics
# ---------------------------------------------------------------------------


def check_miswire(type_id: str, generator: str) -> tuple[list[str], list[str]]:
    """Known wrong-generator / alias patterns (topic wiring)."""
    fails: list[str] = []
    notes: list[str] = []
    id_l = type_id.lower()
    gen = generator

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
        fails.append("miswire: graph_quadratic for non-quadratic topic")
    if gen == "sequence_arithmetic_nth_term" and "geometric" in id_l:
        fails.append("miswire: arithmetic sequence generator for geometric")
    if gen == "function_operations" and "vector" in id_l:
        fails.append("miswire: function_operations for vectors")
    if gen == "inverse_function_basic" and "matrix" in id_l:
        fails.append("miswire: inverse_fn for matrix")
    if gen == "derivative_power_rule" and "product_rule" in id_l:
        fails.append("miswire: power_rule generator on product_rule type")
    if gen == "derivative_product_rule" and "power_rule" in id_l and "product" not in id_l:
        fails.append("miswire: product_rule generator on power_rule type")
    if (
        gen == "radical_equations"
        and "rational" in id_l
        and "radical" not in id_l
        and "exponent" not in id_l
    ):
        fails.append("miswire: radical_equations for rational type")
    if gen == "quadratic_vertex_form_write" and "conic" in id_l and "parabola" not in id_l:
        fails.append("miswire: vertex_write for non-parabola conic")
    if gen == "precalc_foundations":
        notes.append("thin generator: precalc_foundations")
    if gen == "calculus_foundations":
        notes.append("thin generator: calculus_foundations")
    if gen == "radical_simplification" and "rationalizing" in id_l:
        notes.append("uses radical_simplification for rationalizing denominators")

    return fails, notes

# ---------------------------------------------------------------------------
# Catalog / resolve
# ---------------------------------------------------------------------------


def ready_catalog_entries() -> dict[str, TypeCatalogEntry]:
    """Ready, non-scaffold, registered types keyed by id."""
    by: dict[str, TypeCatalogEntry] = {}
    for e in TYPE_CATALOG:
        if e.generator == "scaffold" or type_not_ready(e.id):
            continue
        if e.id not in QUESTION_TYPES:
            continue
        by[e.id] = e
    return by


def _synthetic_entry(type_id: str) -> TypeCatalogEntry | None:
    """Build a catalog-like entry for ids registered only as QuestionTypes."""
    qt = QUESTION_TYPES.get(type_id)
    if qt is None:
        return None
    return TypeCatalogEntry(
        id=type_id,
        name=getattr(qt, "name", None) or type_id,
        category=getattr(qt, "category", None) or "uncatalogued",
        generator=type_id,
        description=getattr(qt, "description", None) or "",
        instruction_latex=getattr(qt, "instruction_latex", None) or "",
        instruction_text=getattr(qt, "instruction_text", None) or "",
    )


def resolve_type_ids(
    *,
    family: str | None = None,
    type_ids: list[str] | None = None,
    prefix: str | None = None,
    ready_only: bool = True,
) -> list[TypeCatalogEntry]:
    """Resolve catalog entries for a sample run."""
    ready = ready_catalog_entries()
    catalog_by_id = {e.id: e for e in TYPE_CATALOG}

    selected: list[str] = []
    if family:
        if family not in FAMILIES:
            known = ", ".join(sorted(FAMILIES))
            raise ValueError(f"Unknown family {family!r}. Known: {known}")
        selected.extend(FAMILIES[family])
    if type_ids:
        selected.extend(type_ids)
    if prefix:
        source_ids = set(ready if ready_only else catalog_by_id)
        source_ids.update(tid for tid in QUESTION_TYPES if tid.startswith(prefix))
        selected.extend(sorted(tid for tid in source_ids if tid.startswith(prefix)))

    if not selected and not family and not type_ids and not prefix:
        selected = list(ready.keys())

    # Dedupe preserving order
    seen: set[str] = set()
    ordered: list[str] = []
    for tid in selected:
        if tid in seen:
            continue
        seen.add(tid)
        ordered.append(tid)

    out: list[TypeCatalogEntry] = []
    for tid in ordered:
        entry = ready.get(tid) if ready_only else catalog_by_id.get(tid)
        if entry is None:
            entry = catalog_by_id.get(tid)
        if entry is None:
            entry = _synthetic_entry(tid)
        if entry is None:
            continue
        if entry.generator == "scaffold":
            continue
        if ready_only and tid in catalog_by_id and type_not_ready(tid):
            # Explicit family / --type-id still included via synthetic/catalog path above
            # only when registered; skip denylisted catalog types unless requested.
            if not family and not type_ids:
                continue
        if tid not in QUESTION_TYPES:
            continue
        out.append(entry)
    return out


# ---------------------------------------------------------------------------
# Evaluate topic fit for one type's samples
# ---------------------------------------------------------------------------


@dataclass
class TopicFitResult:
    type_id: str
    name: str
    generator: str
    status: str = "PASS"  # PASS | FAIL | NOTE
    hard_fails: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def evaluate_topic_fit(
    entry: TypeCatalogEntry,
    prompts_by_tier: dict[str, list[str]],
    *,
    errors_by_tier: dict[str, list[str]] | None = None,
    scaffolded_by_tier: dict[str, list[bool]] | None = None,
) -> TopicFitResult:
    """Score topic-fit heuristics for one type given sampled prompts.

    Does not inspect or require answers.
    """
    tr = TopicFitResult(
        type_id=entry.id,
        name=entry.name or entry.id,
        generator=entry.generator,
    )
    errors_by_tier = errors_by_tier or {}
    scaffolded_by_tier = scaffolded_by_tier or {}

    all_prompts: list[str] = []
    for tier, prompts in prompts_by_tier.items():
        for i, p in enumerate(prompts):
            errs = errors_by_tier.get(tier, [])
            if i < len(errs) and errs[i]:
                tr.hard_fails.append(f"{tier}: {errs[i]}")
                continue
            if not p:
                tr.hard_fails.append(f"{tier}: blank prompt")
                continue
            scaf = scaffolded_by_tier.get(tier, [])
            if (i < len(scaf) and scaf[i]) or looks_stub(p, entry.generator):
                tr.hard_fails.append(f"{tier}: stub/scaffold prompt")
            all_prompts.append(p)

    # Easy vs Hard diversity (within-topic hardness signal)
    easy = [p for p in prompts_by_tier.get("easy", []) if p]
    hard = [p for p in prompts_by_tier.get("hard", []) if p]
    if easy and hard:
        easy_exact = set(easy)
        hard_exact = set(hard)
        easy_norms = {norm_prompt(p) for p in easy}
        hard_norms = {norm_prompt(p) for p in hard}
        if easy_exact == hard_exact and len(easy_exact) == 1:
            tr.hard_fails.append("identical Easy=Hard content (single fixed problem)")
        elif easy_exact == hard_exact:
            tr.notes.append("E/H sample sets matched (small discrete pool; soft)")
        elif easy_norms == hard_norms:
            tr.notes.append("weak E/H diversity: same skeleton after number-normalization")

    profile = getattr(QUESTION_TYPES.get(entry.id), "setting_profile", None)
    gen = entry.generator
    pe = ph = None
    if gen and not str(gen).startswith("hand_written:"):
        pe = lookup_difficulty_preset("easy", type_id=gen, setting_profile=profile)
        ph = lookup_difficulty_preset("hard", type_id=gen, setting_profile=profile)
    if pe is None:
        pe = lookup_difficulty_preset("easy", type_id=entry.id, setting_profile=profile)
        ph = lookup_difficulty_preset("hard", type_id=entry.id, setting_profile=profile)
    if pe and ph and pe == ph:
        tr.notes.append("flat E/H difficulty presets")

    name_l = (entry.name or "").lower()
    for match_fn, check_fn, label in TOPIC_RULES:
        if match_fn(entry.id.lower(), name_l, entry.generator):
            for f in check_fn(all_prompts):
                tr.hard_fails.append(f)

    mw_fails, mw_notes = check_miswire(entry.id, entry.generator)
    tr.hard_fails.extend(mw_fails)
    tr.notes.extend(mw_notes)

    if all_prompts and len({prompt_sig(p) for p in all_prompts}) == 1:
        note = "weak diversity: all samples same normalized template"
        if note not in tr.notes:
            tr.notes.append(note)

    if tr.hard_fails:
        tr.status = "FAIL"
    elif tr.notes:
        tr.status = "NOTE"
    else:
        tr.status = "PASS"
    return tr
