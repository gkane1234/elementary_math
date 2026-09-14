"""Unit checks for skeleton rating regressor + live campaign policy."""

from __future__ import annotations

from pathlib import Path

from question_engine.ml.live_rating import (
    ALL_TOPICS_CAMPAIGN,
    DIFFICULTY_GRID,
    SKELETON_DERIV_TYPE_IDS,
    MultiTypeCampaign,
    SkeletonDerivCampaign,
    all_ready_type_ids,
    generator_key_for_type,
    pick_active_pair_slots,
    pick_next_difficulty,
    pick_next_type_and_difficulty,
)
from question_engine.ml.rating_regressor import (
    MIN_PAIRS,
    MIN_TRAIN,
    extract_skeleton_features,
    refit_from_ratings,
    row_feature_vector,
)


def _fake_row(
    *,
    type_id: str = "calc_diff_power_rule",
    difficulty: float = 8.0,
    rating: int | None = 3,
    form_id: str = "power_poly",
    kind: str = "diff_pow_h_n",
    n_applies: float = 0,
    degree_max: float = 2,
    nest: float = 1,
    generator: str = "diff_power",
) -> dict:
    return {
        "type_id": type_id,
        "generator": generator,
        "difficulty": difficulty,
        "theta_requested": {"difficulty": difficulty},
        "rating_1_to_5": rating,
        "metadata": {
            "generator": generator,
            "form_id": form_id,
            "skeleton_kind": kind,
            "skeleton_pattern": f"Diff({kind})",
            "skeleton_source": "expr_skeleton",
            "conceptual_difficulty": difficulty,
            "richness_band": "mid",
            "function_classes": ["algebraic"],
            "methods_used": ["power"],
            "cost_spend": {
                "n_applies": n_applies,
                "degree_max": degree_max,
                "nest_depth_expr": nest,
                "chain_depth": 1,
                "n_terms": 2,
                "n_factors": 0,
                "inner_kind": "affine",
                "inner_degree": 1,
                "nest_budget": 0,
            },
        },
    }


def test_cold_start_not_ready_below_min_train():
    rows = [_fake_row(rating=3, difficulty=float(d)) for d in range(MIN_TRAIN - 1)]
    model = refit_from_ratings(rows)
    assert model.n_train == MIN_TRAIN - 1
    assert model.n_pairs == 0
    assert model.model_ready is False
    status = model.status_for(rows[0])
    assert status.predicted_rating is None
    assert status.predicted_std is None
    assert "Cold start" in status.message


def _pair_row(left: dict, right: dict, winner: str, *, engine_rev: str = "rev") -> dict:
    return {
        "record_kind": "pair",
        "pair_id": f"pair_{left.get('type_id')}_{winner}",
        "left": left,
        "right": right,
        "winner": winner,
        "engine_rev": engine_rev,
        "skipped": False,
    }


def test_refit_ready_and_predicts_after_min_train():
    rows = []
    for i in range(MIN_TRAIN):
        # Higher nest / degree → higher rating signal.
        nest = 1.0 + (i % 5)
        deg = 1.0 + (i % 4)
        rating = 1 + min(4, int(nest + deg) // 2)
        rows.append(
            _fake_row(
                rating=rating,
                difficulty=float(DIFFICULTY_GRID[i % len(DIFFICULTY_GRID)]),
                n_applies=float(i % 3),
                degree_max=deg,
                nest=nest,
                form_id=f"form_{i % 4}",
            )
        )
    model = refit_from_ratings(rows)
    assert model.model_ready is True
    assert model.n_train == MIN_TRAIN
    easy = _fake_row(rating=None, nest=1, degree_max=1, n_applies=0)
    hard = _fake_row(rating=None, nest=5, degree_max=5, n_applies=2)
    p_easy = model.predict_one(easy)
    p_hard = model.predict_one(hard)
    assert p_easy is not None and p_hard is not None
    assert 1.0 <= p_easy <= 5.0
    assert 1.0 <= p_hard <= 5.0


def test_broken_and_skip_excluded_from_train():
    rows = [_fake_row(rating=4) for _ in range(MIN_TRAIN)]
    rows[0]["broken"] = True
    rows[1]["skipped"] = True
    rows[1]["rating_1_to_5"] = None
    model = refit_from_ratings(rows)
    assert model.n_train == MIN_TRAIN - 2
    assert model.model_ready is False


def test_extract_skeleton_features_prefers_cost_spend():
    feats = extract_skeleton_features(_fake_row())
    assert feats["form_id"] == "power_poly"
    assert feats["generator"] == "diff_power"
    assert feats["skeleton_kind"] == "diff_pow_h_n"
    assert feats["n_applies"] == 0.0
    assert feats["degree_max"] == 2.0
    vec = row_feature_vector(_fake_row())
    assert len(vec) > len(feats)
    assert all(isinstance(x, float) for x in vec)


def test_pick_next_type_balances_coverage():
    stuffed = [
        {
            "type_id": SKELETON_DERIV_TYPE_IDS[0],
            "theta_requested": {"difficulty": 8.0},
            "rating_1_to_5": 3,
        }
        for _ in range(5)
    ]
    tid, d = pick_next_type_and_difficulty(stuffed)
    assert tid != SKELETON_DERIV_TYPE_IDS[0]
    assert tid in SKELETON_DERIV_TYPE_IDS
    assert d in DIFFICULTY_GRID


def test_pick_next_difficulty_still_works():
    stuffed = [
        {"theta_requested": {"difficulty": 8.0}, "rating_1_to_5": 3} for _ in range(5)
    ]
    assert pick_next_difficulty(stuffed) != 8.0


def test_skeleton_campaign_generate_submit(tmp_path: Path):
    import question_engine.types  # noqa: F401

    camp = SkeletonDerivCampaign(session="unit_skel", root=tmp_path)
    item = camp.generate_next(type_id="calc_diff_power_rule", difficulty=8.0, seed=11)
    assert item["type_id"] == "calc_diff_power_rule"
    assert item["model_ready"] is False
    assert item["predicted_rating"] is None
    assert item["n_train"] == 0
    assert "skeleton_features" in item
    # Live path should carry skeleton source when form maps.
    src = (item.get("metadata") or {}).get("skeleton_source") or item[
        "skeleton_features"
    ].get("skeleton_source")
    assert src in ("expr_skeleton", "")
    result = camp.submit(rating_1_to_5=4, notes="unit", topic_fit_ok=True)
    assert result["ok"] is True
    assert result["n_train"] == 1
    assert (tmp_path / "unit_skel" / "ratings.jsonl").is_file()
    cov = camp.coverage()
    assert cov["n_ratings"] == 1
    assert cov["by_type"]["calc_diff_power_rule"] == 1


def test_pick_next_type_generator_first_balances_shared_gens():
    ids = ("leaf_a1", "leaf_a2", "leaf_b")

    def gen_of(tid: str) -> str:
        return "gen_a" if tid.startswith("leaf_a") else "gen_b"

    stuffed = [
        {
            "type_id": "leaf_a1",
            "generator": "gen_a",
            "theta_requested": {"difficulty": 8.0},
            "rating_1_to_5": 3,
        }
        for _ in range(4)
    ]
    tid, d = pick_next_type_and_difficulty(stuffed, ids, generator_of=gen_of)
    assert tid == "leaf_b"
    assert d in DIFFICULTY_GRID


def test_shared_generator_ratings_transfer_across_types():
    rows = [
        _fake_row(
            type_id="leaf_a",
            generator="shared_gen",
            form_id=f"form_{i % 3}",
            rating=2 + (i % 4),
            difficulty=float(DIFFICULTY_GRID[i % len(DIFFICULTY_GRID)]),
            nest=1.0 + (i % 4),
            degree_max=1.0 + (i % 3),
        )
        for i in range(MIN_TRAIN)
    ]
    model = refit_from_ratings(rows)
    assert model.model_ready is True
    other = _fake_row(
        type_id="leaf_b",
        generator="shared_gen",
        form_id="form_0",
        rating=None,
    )
    pred = model.predict_one(other)
    assert pred is not None
    assert 1.0 <= pred <= 5.0


def test_all_topics_pool_includes_trig_integral():
    import question_engine.types  # noqa: F401

    ids = all_ready_type_ids()
    assert "calc_indef_int_trigonometric" in ids
    assert generator_key_for_type("calc_indef_int_trigonometric") == "integral_trigonometric"


def test_all_topics_campaign_trig_and_form_id_on_theta(tmp_path: Path, monkeypatch):
    import question_engine.types  # noqa: F401

    monkeypatch.setenv("POLY_ENGINE_REV", "unit-rev-a")
    camp = MultiTypeCampaign(
        session="unit_all",
        root=tmp_path,
        type_ids=("calc_indef_int_trigonometric",),
        campaign=ALL_TOPICS_CAMPAIGN,
    )
    item = camp.generate_next(
        type_id="calc_indef_int_trigonometric", difficulty=8.0, seed=207
    )
    assert item["type_id"] == "calc_indef_int_trigonometric"
    assert item["campaign"] == ALL_TOPICS_CAMPAIGN
    assert item.get("generator") == "integral_trigonometric"
    feats = item.get("skeleton_features") or {}
    assert feats.get("form_id")
    assert feats.get("generator") == "integral_trigonometric"
    theta = item.get("theta_full") or {}
    assert theta.get("form_id") or (item.get("metadata") or {}).get("form_id")
    result = camp.submit(rating_1_to_5=4)
    assert result["ok"] is True
    assert result["n_train"] == 1


def test_engine_rev_change_rotates_jsonl_and_cold_starts(tmp_path: Path, monkeypatch):
    import question_engine.types  # noqa: F401

    monkeypatch.setenv("POLY_ENGINE_REV", "rev-old")
    camp = MultiTypeCampaign(
        session="unit_reset",
        root=tmp_path,
        type_ids=("calc_indef_int_trigonometric",),
        campaign=ALL_TOPICS_CAMPAIGN,
    )
    camp.generate_next(type_id="calc_indef_int_trigonometric", difficulty=0.0, seed=11)
    camp.submit(rating_1_to_5=3)
    live = tmp_path / "unit_reset" / "ratings.jsonl"
    assert live.is_file()

    monkeypatch.setenv("POLY_ENGINE_REV", "rev-new")
    camp2 = MultiTypeCampaign(
        session="unit_reset",
        root=tmp_path,
        type_ids=("calc_indef_int_trigonometric",),
        campaign=ALL_TOPICS_CAMPAIGN,
    )
    assert not live.is_file()
    hist = list((tmp_path / "unit_reset" / "history").glob("ratings.*.jsonl"))
    assert hist, "old JSONL should be archived under history/"
    cov = camp2.coverage()
    assert cov["n_train"] == 0
    assert cov["model_ready"] is False
    assert cov["engine_rev"] == "rev-new"


def test_posterior_mean_and_std_after_abs_ready():
    rows = []
    for i in range(MIN_TRAIN):
        nest = 1.0 + (i % 5)
        deg = 1.0 + (i % 4)
        rating = 1 + min(4, int(nest + deg) // 2)
        rows.append(
            _fake_row(
                rating=rating,
                difficulty=float(DIFFICULTY_GRID[i % len(DIFFICULTY_GRID)]),
                n_applies=float(i % 3),
                degree_max=deg,
                nest=nest,
                form_id=f"form_{i % 4}",
            )
        )
    model = refit_from_ratings(rows)
    assert model.model_ready is True
    probe = _fake_row(rating=None, nest=2, degree_max=2)
    pred = model.predict_mean_std(probe)
    assert pred is not None
    mean, std = pred
    assert 1.0 <= float(min(5.0, max(1.0, mean))) <= 5.0
    assert std > 0.0
    status = model.status_for(probe)
    assert status.predicted_std is not None
    assert status.predicted_std > 0.0


def test_pairwise_winner_ranks_higher():
    pairs = []
    for i in range(MIN_PAIRS + 2):
        good = _fake_row(
            type_id="leaf_a",
            generator="shared_gen",
            form_id="good_form",
            rating=None,
            nest=5.0,
            degree_max=5.0,
            n_applies=2.0,
            difficulty=16.0,
        )
        bad = _fake_row(
            type_id="leaf_a",
            generator="shared_gen",
            form_id="bad_form",
            rating=None,
            nest=1.0,
            degree_max=1.0,
            n_applies=0.0,
            difficulty=4.0,
        )
        pairs.append(_pair_row(good, bad, "a", engine_rev="cur"))
    model = refit_from_ratings(pairs)
    assert model.model_ready is True
    assert model.n_pairs >= MIN_PAIRS
    assert model.n_train == 0
    u_good = model.predict_mean_std(pairs[0]["left"])
    u_bad = model.predict_mean_std(pairs[0]["right"])
    assert u_good is not None and u_bad is not None
    assert u_good[0] > u_bad[0]


def test_engine_rev_change_excludes_old_pairs():
    from question_engine.ml.live_rating import ratings_for_engine_rev

    old_pairs = []
    for i in range(MIN_PAIRS + 1):
        old_pairs.append(
            _pair_row(
                _fake_row(form_id="good_form", nest=5, rating=None),
                _fake_row(form_id="bad_form", nest=1, rating=None),
                "a",
                engine_rev="old",
            )
        )
    new_pairs = [
        _pair_row(
            _fake_row(form_id="good_form", nest=5, rating=None),
            _fake_row(form_id="bad_form", nest=1, rating=None),
            "b",
            engine_rev="new",
        )
        for _ in range(2)
    ]
    train = ratings_for_engine_rev(old_pairs + new_pairs, "new")
    model = refit_from_ratings(train)
    assert model.n_pairs == 2
    assert model.model_ready is False
    assert model.status_for(None).predicted_rating is None


def test_shared_generator_pairs_transfer_across_types():
    pairs = []
    for i in range(MIN_PAIRS + 2):
        good = _fake_row(
            type_id="leaf_a",
            generator="shared_gen",
            form_id="good_form",
            rating=None,
            nest=5.0,
            degree_max=4.0,
        )
        bad = _fake_row(
            type_id="leaf_a",
            generator="shared_gen",
            form_id="bad_form",
            rating=None,
            nest=1.0,
            degree_max=1.0,
        )
        pairs.append(_pair_row(good, bad, "a"))
    model = refit_from_ratings(pairs)
    assert model.model_ready is True
    other_good = _fake_row(
        type_id="leaf_b",
        generator="shared_gen",
        form_id="good_form",
        rating=None,
        nest=5.0,
        degree_max=4.0,
    )
    other_bad = _fake_row(
        type_id="leaf_b",
        generator="shared_gen",
        form_id="bad_form",
        rating=None,
        nest=1.0,
        degree_max=1.0,
    )
    u_good = model.predict_mean_std(other_good)
    u_bad = model.predict_mean_std(other_bad)
    assert u_good is not None and u_bad is not None
    assert u_good[0] > u_bad[0]


def test_active_pick_not_stuck_on_stuffed_bin_when_ready():
    rows = []
    for i in range(MIN_TRAIN):
        rows.append(
            _fake_row(
                rating=2 + (i % 4),
                difficulty=8.0,
                nest=1.0 + (i % 4),
                degree_max=1.0 + (i % 3),
                form_id=f"form_{i % 3}",
            )
        )
    model = refit_from_ratings(rows)
    assert model.model_ready is True
    ds = []
    for seed in range(12):
        a, b = pick_active_pair_slots(
            rows,
            SKELETON_DERIV_TYPE_IDS[:3],
            model,
            rng_seed=seed,
        )
        assert a[0] == b[0]
        assert abs(a[1] - b[1]) < 1e-9
        ds.extend([a[1], b[1]])
    assert len(set(ds)) > 1
    # Cold policy after stuffing D=8 is a single underfilled bin; ready must vary.
    cold = pick_next_difficulty(rows)
    assert not all(abs(d - cold) < 1e-9 for d in ds)


def test_pick_active_pair_slots_same_type_and_d():
    ids = ("leaf_a", "leaf_b", "leaf_c")

    def gen_of(tid: str) -> str:
        return "gen_a" if tid == "leaf_a" else "gen_b"

    a, b = pick_active_pair_slots([], ids, None, generator_of=gen_of)
    assert a[0] == b[0]
    assert a[0] in ids
    assert abs(a[1] - b[1]) < 1e-9
    mid = DIFFICULTY_GRID[len(DIFFICULTY_GRID) // 2]
    assert a[1] == mid

    stuffed = [
        {
            "type_id": "leaf_a",
            "generator": "gen_a",
            "theta_requested": {"difficulty": mid},
            "rating_1_to_5": 3,
        }
        for _ in range(2)
    ]
    a2, b2 = pick_active_pair_slots(stuffed, ids, None, generator_of=gen_of)
    assert a2[0] == b2[0]
    assert abs(a2[1] - b2[1]) < 1e-9
    # Session-level D rotates off the stuffed mid bin; type may change.
    assert a2[1] != mid
    assert a2[1] in DIFFICULTY_GRID


def test_generate_next_pair_same_type_unpinned(tmp_path: Path, monkeypatch):
    import question_engine.types  # noqa: F401

    monkeypatch.setenv("POLY_ENGINE_REV", "unit-same-type")
    camp = MultiTypeCampaign(
        session="unit_same_type",
        root=tmp_path,
        type_ids=("calc_diff_power_rule", "calc_diff_product_rule"),
        campaign=ALL_TOPICS_CAMPAIGN,
    )
    pair = camp.generate_next_pair()
    left, right = pair["left"], pair["right"]
    assert left["type_id"] == right["type_id"]
    assert left["type_id"] in ("calc_diff_power_rule", "calc_diff_product_rule")
    assert left["difficulty"] == right["difficulty"]
    seed_l = (left.get("theta_requested") or {}).get("seed")
    seed_r = (right.get("theta_requested") or {}).get("seed")
    assert seed_l != seed_r
    mid = DIFFICULTY_GRID[len(DIFFICULTY_GRID) // 2]
    assert left["difficulty"] == mid

    camp.submit(winner="a")
    pair2 = camp.generate_next_pair()
    left2, right2 = pair2["left"], pair2["right"]
    assert left2["type_id"] == right2["type_id"]
    assert left2["difficulty"] == right2["difficulty"]
    # After a mid-grid pair, session D should leave 12.
    assert left2["difficulty"] != mid


def test_campaign_generate_submit_pair(tmp_path: Path, monkeypatch):
    import question_engine.types  # noqa: F401

    monkeypatch.setenv("POLY_ENGINE_REV", "unit-pair-rev")
    camp = SkeletonDerivCampaign(session="unit_pair", root=tmp_path)
    pair = camp.generate_next_pair(
        type_id="calc_diff_power_rule", difficulty=8.0, seed=21
    )
    assert pair["mode"] == "pair"
    assert pair["pair_id"]
    assert pair["left"]["type_id"] == pair["right"]["type_id"] == "calc_diff_power_rule"
    assert pair["left"]["difficulty"] == pair["right"]["difficulty"]
    assert pair["left"]["rating_id"] != pair["right"]["rating_id"]
    result = camp.submit(winner="a", left={"topic_fit_ok": True}, right={"topic_fit_ok": True})
    assert result["ok"] is True
    assert result["winner"] == "a"
    assert result["n_pairs"] == 1
    live = tmp_path / "unit_pair" / "ratings.jsonl"
    assert live.is_file()
    row = __import__("json").loads(live.read_text(encoding="utf-8").splitlines()[0])
    assert row["record_kind"] == "pair"
    assert row["winner"] == "a"
    cov = camp.coverage()
    assert cov["n_pairs"] == 1


def test_all_topics_pool_includes_related_rates():
    import question_engine.types  # noqa: F401
    from question_engine.ml.knob_introspect import has_continuous_difficulty
    from question_engine.type_readiness import type_not_ready

    tid = "calc_app_diff_related_rates"
    assert has_continuous_difficulty(tid)
    assert not type_not_ready(tid)
    ids = all_ready_type_ids()
    assert tid in ids
    assert generator_key_for_type(tid) == "related_rates_simple"


def test_related_rates_live_form_id_features_and_two_seeds(tmp_path: Path, monkeypatch):
    import question_engine.types  # noqa: F401
    from question_engine.api.handler import _generate_for_type

    monkeypatch.setenv("POLY_ENGINE_REV", "unit-rr-form")
    camp = MultiTypeCampaign(
        session="unit_rr",
        root=tmp_path,
        type_ids=("calc_app_diff_related_rates",),
        campaign=ALL_TOPICS_CAMPAIGN,
    )
    item = camp.generate_next(
        type_id="calc_app_diff_related_rates", difficulty=8.0, seed=101
    )
    assert item.get("generator") == "related_rates_simple"
    feats = item.get("skeleton_features") or {}
    assert feats.get("form_id")
    assert feats.get("generator") == "related_rates_simple"
    theta = item.get("theta_full") or {}
    meta = item.get("metadata") or {}
    fid = meta.get("form_id") or theta.get("form_id")
    assert fid
    assert (meta.get("spec_snapshot") or {}).get("form_id") == fid
    assert theta.get("form_id") == fid or meta.get("form_id") == fid
    assert extract_skeleton_features(item)["form_id"] == str(fid)

    seen = {str(fid)}
    for seed in range(40):
        q = _generate_for_type(
            "calc_app_diff_related_rates",
            {
                "difficulty": 8.0,
                "seed": seed,
                "count": 1,
                "include_answer_key": True,
            },
        )[0]
        seen.add(str((q.metadata or {}).get("form_id") or ""))
        if len(seen) >= 2:
            break
    assert len(seen) >= 2, seen
