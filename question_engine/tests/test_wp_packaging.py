"""Story packaging for one-/two-step / inequality / proportion word problems."""

from __future__ import annotations

import re

from question_engine.api.handler import _generate_for_type
from question_engine.frameworks.primitives.openstax_form_catalogs import (
    implemented_forms,
    load_form_catalog,
)
from question_engine.frameworks.primitives.wp_packaging import (
    looks_like_dumped_equation,
    use_wp_packaging,
)


def _qs(type_id: str, d: float, seed: int, extra: dict | None = None):
    settings = {
        "difficulty": d,
        "seed": seed,
        "count": 1,
        "include_answer_key": True,
        "integers_only": True,
        "only_x": True,
        **(extra or {}),
    }
    qs = _generate_for_type(type_id, settings)
    assert qs, (type_id, d, seed)
    return qs[0]


def test_applications_catalog_loads():
    cat = load_form_catalog("algebra1_linear_applications")
    assert cat["catalog_id"] == "algebra1_linear_applications"
    ids = {str(f["form_id"]) for f in implemented_forms(cat)}
    assert {
        "number_one_step",
        "money_spent",
        "money_received",
        "money_shared",
        "count_tickets",
        "number_two_step",
        "money_two_step",
        "compare_twice",
        "earnings_two_step",
        "ineq_score",
        "ineq_budget",
        "prop_recipe",
        "prop_unit_rate",
        "write_rate",
        "write_cost",
        "sys_number",
        "sys_tickets",
    } <= ids


def test_use_wp_packaging_default_and_opt_out():
    assert use_wp_packaging({}, "one_step") is True
    assert use_wp_packaging({"use_sample_linear_equation": True}, "one_step") is False
    assert use_wp_packaging({"use_wp_packaging": False}, "one_step") is False
    assert use_wp_packaging({"use_sample_linear_inequality": True}, "inequality") is False
    assert use_wp_packaging({}, "inequality") is True


def test_d0_one_step_is_real_story_not_dumped_equation():
    for type_id in (
        "g6_equations_word_problems",
        "pa_equations_one_step_word_problems",
    ):
        for seed in range(12):
            q = _qs(type_id, 0.0, seed)
            prompt = (q.prompt_latex or "") + " " + (q.prompt_text or "")
            assert not looks_like_dumped_equation(prompt), prompt
            assert "the equation is" not in prompt.lower()
            assert re.search(r"\$[0-9]*x", prompt) is None
            meta = q.metadata or {}
            assert meta.get("frame_id")
            assert meta.get("skeleton_pattern") == "SolveLinear"
            assert meta.get("species") == "one" or meta.get("n_ops") == 1
            assert int(meta.get("n_ops") or 0) == 1
            assert q.answer_latex


def test_opt_out_keeps_old_stub():
    q = _qs(
        "pa_equations_one_step_word_problems",
        0.0,
        3,
        extra={"use_sample_linear_equation": True},
    )
    prompt = (q.prompt_latex or "") + " " + (q.prompt_text or "")
    assert looks_like_dumped_equation(prompt) or "the equation is" in prompt.lower()


def test_two_step_stays_two_step():
    for seed in range(10):
        q = _qs("pa_equations_two_step_word_problems", 0.0, seed)
        meta = q.metadata or {}
        prompt = (q.prompt_latex or "") + " " + (q.prompt_text or "")
        assert not looks_like_dumped_equation(prompt), prompt
        assert meta.get("skeleton_pattern") == "SolveLinear"
        assert meta.get("species") == "two" or int(meta.get("n_ops") or 0) == 2
        assert int(meta.get("n_ops") or 0) == 2
        assert meta.get("frame_id") in {
            "number_two_step",
            "money_two_step",
            "compare_twice",
            "earnings_two_step",
        }
        two_fact = (
            "times a number" in prompt.lower()
            or "each" in prompt.lower()
            or "less than" in prompt.lower()
            or "more than twice" in prompt.lower()
            or "together earn" in prompt.lower()
        )
        assert two_fact, prompt


def test_g6_equation_wp_never_two_step():
    for d in (0.0, 8.0, 16.0):
        for seed in range(8):
            q = _qs("g6_equations_word_problems", d, seed)
            meta = q.metadata or {}
            assert int(meta.get("n_ops") or 0) == 1, (d, seed, q.prompt_text, meta)
            assert meta.get("species") == "one"
            assert meta.get("frame_id") in {
                "number_one_step",
                "money_spent",
                "money_received",
                "money_shared",
                "money_donations",
                "count_tickets",
                "count_groups",
            }
            prompt = (q.prompt_text or "") + (q.prompt_latex or "")
            assert "times a number and" not in prompt.lower()


def test_inequality_d0_no_flip_and_not_two_step_budget():
    flipped = []
    for seed in range(16):
        q = _qs("g6_inequalities_word_problems", 0.0, seed)
        meta = q.metadata or {}
        prompt = (q.prompt_latex or "") + " " + (q.prompt_text or "")
        assert not looks_like_dumped_equation(prompt), prompt
        assert meta.get("skeleton_pattern") == "SolveInequality"
        assert meta.get("flipped") in {False, None, "false"}
        flipped.append(bool(meta.get("flipped")))
        assert int(meta.get("n_ops") or 1) == 1
        assert meta.get("frame_id") != "ineq_budget"
        assert "each and a" not in prompt.lower()
        assert "rents a car" not in prompt.lower()
        assert "phone plan" not in prompt.lower()
        assert q.answer_latex
        assert (
            "<" in (q.answer_latex or "")
            or ">" in (q.answer_latex or "")
            or "le" in (q.answer_latex or "")
            or "ge" in (q.answer_latex or "")
        )
    assert not any(flipped)


def test_inequality_d0_points_story_matches_answer():
    """Add-points stories must invert to the keyed boundary."""
    hits = 0
    for seed in range(30):
        q = _qs("g6_inequalities_word_problems", 0.0, seed)
        text = q.prompt_text or ""
        m = re.search(
            r"already has (\d+) points and needs (?:at least|more than|at most|less than) (\d+) points",
            text,
        )
        if not m:
            continue
        have, need = int(m.group(1)), int(m.group(2))
        ans = q.answer_latex or ""
        bound = re.search(r"(-?\\frac\{\d+\}\{\d+\}|-?\d+)", ans)
        assert bound, (text, ans)
        assert abs(float(bound.group(1).replace(r"\frac", "")) - (need - have)) < 1e-9 or (
            abs(int(bound.group(1)) - (need - have)) < 1e-9
        )
        hits += 1
    assert hits >= 1


def test_live_generate_for_type_smoke():
    for type_id, pat in (
        ("g6_equations_word_problems", "SolveLinear"),
        ("pa_equations_one_step_word_problems", "SolveLinear"),
        ("pa_equations_two_step_word_problems", "SolveLinear"),
        ("g6_inequalities_word_problems", "SolveInequality"),
        ("pa_proportions_word_problems", "ProportionRate"),
    ):
        for d in (0.0, 8.0, 16.0):
            q = _qs(type_id, d, 101)
            meta = q.metadata or {}
            assert q.prompt_latex, (type_id, d)
            assert q.answer_latex, (type_id, d)
            assert meta.get("skeleton_pattern") == pat, (
                type_id,
                d,
                meta.get("skeleton_pattern"),
            )
            assert meta.get("frame_id"), (type_id, d, meta)
            prompt = (q.prompt_latex or "") + " " + (q.prompt_text or "")
            assert not looks_like_dumped_equation(prompt), (type_id, d, prompt)


def test_one_step_answers_match_money_stories():
    """Spent/left and share stories key the unknown, not a given."""
    seen = {"spent": 0, "received": 0, "each": 0}
    for seed in range(40):
        q = _qs("pa_equations_one_step_word_problems", 0.0, seed)
        text = q.prompt_text or ""
        ans = (q.answer_latex or "").replace(r"\$", "").replace("$", "").replace("\\", "")
        ans = ans.split("text")[0].strip()
        if "spent" in text and "left" in text:
            m = re.search(r"spent \$(\d+), and has \$(\d+) left", text)
            assert m, text
            spent, left = int(m.group(1)), int(m.group(2))
            assert abs(float(ans) - (left + spent)) < 1e-9
            seen["spent"] += 1
        elif "received" in text and "start with" in text:
            m = re.search(r"received \$(\d+), and now has \$(\d+)", text)
            assert m, text
            rec, total = int(m.group(1)), int(m.group(2))
            assert abs(float(ans) - (total - rec)) < 1e-9
            seen["received"] += 1
        elif "donations totaling" in text:
            m = re.search(r"collected (\d+) equal donations totaling \$(\d+)", text)
            assert m, text
            n, total = int(m.group(1)), int(m.group(2))
            assert total % n == 0
            assert abs(float(ans) - total / n) < 1e-9
            seen["each"] += 1
        elif "shared" in text and "equally" in text:
            m = re.search(r"shared \$(\d+) equally among (\d+) friends", text)
            assert m, text
            total, n = int(m.group(1)), int(m.group(2))
            assert total % n == 0
            assert abs(float(ans) - total / n) < 1e-9
            seen["each"] += 1
    assert sum(seen.values()) >= 1, seen


def _frame_key(q) -> str:
    meta = q.metadata or {}
    fid = str(meta.get("frame_id") or "")
    if fid:
        return fid
    return str(meta.get("frame_variant") or "unknown")


def test_one_step_wp_rotates_frames_across_seeds():
    """OpenStax IA §2.2: number, spent, received, shares, tickets — ≥4 frames."""
    keys = {_frame_key(_qs("pa_equations_one_step_word_problems", 0.0, seed)) for seed in range(48)}
    assert len(keys) >= 4, keys
    moneyish = keys & {
        "money_spent",
        "money_received",
        "money_shared",
        "money_donations",
        "count_tickets",
    }
    assert moneyish, keys
    assert "number_one_step" in keys, keys


def test_two_step_wp_rotates_number_and_money():
    """IA §2.2 number / twice-more / earnings plus unit+fee — all 4 frames."""
    keys = {_frame_key(_qs("pa_equations_two_step_word_problems", 0.0, seed)) for seed in range(48)}
    assert len(keys) >= 4, keys
    assert "money_two_step" in keys, keys
    assert "number_two_step" in keys, keys
    assert "compare_twice" in keys, keys
    assert "earnings_two_step" in keys, keys


def test_ineq_wp_rotates_frames_across_seeds():
    """EA §2.7 score / height / checkout / points — ≥4 frames at D=0."""
    keys = {_frame_key(_qs("g6_inequalities_word_problems", 0.0, seed)) for seed in range(48)}
    assert len(keys) >= 4, keys
    assert "ineq_budget" not in keys
    assert keys & {"ineq_score", "ineq_height", "ineq_checkout", "ineq_points", "ineq_lost", "ineq_tickets"}


def test_proportion_wp_rotates_recipe_and_unit_rate():
    keys = {_frame_key(_qs("pa_proportions_word_problems", 0.0, seed)) for seed in range(48)}
    assert len(keys) >= 4, keys
    assert "prop_recipe" in keys, keys
    assert "prop_unit_rate" in keys, keys
    assert "prop_calories" in keys, keys
    assert "prop_dosage" in keys, keys
    for seed in range(12):
        q = _qs("pa_proportions_word_problems", 0.0, seed)
        prompt = (q.prompt_latex or "") + " " + (q.prompt_text or "")
        assert not looks_like_dumped_equation(prompt), prompt
        assert "scale a recipe" not in prompt.lower()


def test_write_rate_rotates_vehicles_and_asks():
    """EA §2.6: ≥3 vehicles; all three asks (d/t/r) across D."""
    vehicles: set[str] = set()
    asks: set[str] = set()
    d0_asks: set[str] = set()
    for seed in range(36):
        q0 = _qs("g6_constant_rate_equations", 0.0, seed)
        meta0 = q0.metadata or {}
        vehicles.add(str(meta0.get("vehicle") or ""))
        d0_asks.add(str(meta0.get("ask") or ""))
        prompt = (q0.prompt_text or "") + (q0.prompt_latex or "")
        assert "Write an equation" in prompt
        assert not looks_like_dumped_equation(prompt)
        q16 = _qs("g6_constant_rate_equations", 16.0, 200 + seed)
        meta16 = q16.metadata or {}
        vehicles.add(str(meta16.get("vehicle") or ""))
        asks.add(str(meta16.get("ask") or ""))
    vehicles.discard("")
    asks.discard("")
    d0_asks.discard("")
    assert len(vehicles) >= 3, vehicles
    assert vehicles <= {"bike", "car", "walk", "bus", "train"}
    assert d0_asks == {"distance"}, d0_asks
    assert {"distance", "time", "rate"} <= asks, asks


def test_write_other_rotates_frames_not_pencils_only():
    """D=0 is cost/tickets; square invert + triangle show at high D (EA §2.6)."""
    d0 = {_frame_key(_qs("g6_equations_for_other_relationships", 0.0, seed)) for seed in range(36)}
    assert d0 <= {"write_cost", "write_tickets"}, d0
    assert "write_cost" in d0, d0
    assert "write_tickets" in d0, d0
    hi = {
        _frame_key(_qs("g6_equations_for_other_relationships", 16.0, seed))
        for seed in range(36)
    }
    assert "write_triangle" in hi, hi
    assert "write_square_invert" in hi or "write_square" in hi, hi
    prompts = [
        (_qs("g6_equations_for_other_relationships", 0.0, seed).prompt_text or "").lower()
        for seed in range(24)
    ]
    assert any("pencil" not in p and "write an equation" in p for p in prompts)


def test_similar_figures_wp_rotates_shape_and_scale_with_d():
    """EA §8.7: D=0 triangles; higher D mixes quads and scale."""
    d0_frames = set()
    d0_scales = set()
    d0_missing = set()
    for seed in range(24):
        q = _qs("pa_similar_figures", 0.0, seed, extra={"prompt_style": "diagram"})
        meta = q.metadata or {}
        d0_frames.add(str(meta.get("frame_id") or ""))
        d0_scales.add(int(meta.get("scale_factor") or 0))
        d0_missing.add(str(meta.get("missing_side") or ""))
        assert str(meta.get("shape") or "") == "triangle"
        assert int(meta.get("scale_factor") or 0) == 2
        assert str(meta.get("ask") or "") == "missing_side"
        prompt = (q.prompt_latex or "") + " " + (q.prompt_text or "")
        assert not looks_like_dumped_equation(prompt), prompt
    assert d0_frames == {"similar_triangles"}, d0_frames
    assert d0_scales == {2}
    assert len(d0_missing) >= 2, d0_missing

    hi_frames = set()
    hi_shapes = set()
    hi_scales = set()
    hi_missing = set()
    for seed in range(36):
        q = _qs("pa_similar_figures", 16.0, 200 + seed, extra={"prompt_style": "diagram"})
        meta = q.metadata or {}
        hi_frames.add(str(meta.get("frame_id") or ""))
        hi_shapes.add(str(meta.get("shape") or ""))
        hi_scales.add(int(meta.get("scale_factor") or 0))
        if meta.get("ask") == "missing_side":
            hi_missing.add(str(meta.get("missing_side") or ""))
    assert "similar_quad" in hi_frames, hi_frames
    assert "similar_triangles" in hi_frames, hi_frames
    assert hi_shapes >= {"triangle", "rectangle"}, hi_shapes
    assert max(hi_scales) >= 3, hi_scales
    assert len(hi_missing) >= 2, hi_missing


def test_ineq_wp_high_d_rotates_budget_vehicles():
    """IA §2.5 car / phone / tablets — not bike-only, not folders-only."""
    keys = set()
    variants = set()
    for seed in range(40):
        q = _qs("g6_inequalities_word_problems", 16.0, seed)
        meta = q.metadata or {}
        keys.add(str(meta.get("frame_id") or ""))
        variants.add(str(meta.get("frame_variant") or ""))
    assert "ineq_budget" in keys, keys
    budgetish = variants & {"car_rental", "tablets", "phone", "unit_plus_fee"}
    assert len(budgetish) >= 2, variants


def test_systems_wp_is_story_not_dump():
    for type_id in ("pa_systems_word_problems", "systems_word_problems"):
        for seed in range(16):
            q = _qs(type_id, 0.0, seed)
            prompt = (q.prompt_latex or "") + " " + (q.prompt_text or "")
            assert not looks_like_dumped_equation(prompt), prompt
            assert "costs satisfy" not in prompt.lower()
            assert r"\begin{cases}" not in prompt
            meta = q.metadata or {}
            assert meta.get("skeleton_pattern") == "SystemsWP"
            assert meta.get("frame_id") in {"sys_number", "sys_tickets"}, meta
            assert q.answer_latex


def test_systems_wp_opt_out_keeps_dump():
    for type_id in ("pa_systems_word_problems", "systems_word_problems"):
        q = _qs(
            type_id,
            0.0,
            3,
            extra={"use_legacy_systems": True},
        )
        prompt = (q.prompt_latex or "") + " " + (q.prompt_text or "")
        assert looks_like_dumped_equation(prompt) or "costs satisfy" in prompt.lower()


def test_systems_wp_high_d_unlocks_geometry_or_motion():
    for type_id in ("pa_systems_word_problems", "systems_word_problems"):
        keys = {_frame_key(_qs(type_id, 16.0, seed)) for seed in range(24)}
        assert keys & {"sys_geometry", "sys_motion"}, keys
        assert keys & {"sys_number", "sys_tickets"}, keys
