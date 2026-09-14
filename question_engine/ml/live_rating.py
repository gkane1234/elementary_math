"""Live adaptive human-rating loop: pairwise Bayesian utility.

Policy:
  - Pairwise A vs B is the primary label (Bradley–Terry on a linear utility).
  - Absolute 1–5 remains optional / legacy.
  - Cold start: stratified generator → type → D until ``MIN_PAIRS`` comparisons
    or ``MIN_TRAIN`` absolute ratings.
  - Once ready: shortlist + UCB picks the most informative (type, D);
    both pair sides share that type and D (different seeds). Posterior
    reweights ``form_id`` at generate time (Thompson / UCB, not difficulty padding).
  - Multi-type campaigns pick generator-first so a shared generator is updated
    by ratings from any topic that uses it. The *model* transfers across
    topics; each on-screen pair is the same ``type_id``.
  - Append-only JSONL + session state under
    ``scripts/output/ml/ratings/live/<session>/``.
  - A generation-process change (``engine_rev``) rotates the live JSONL to
    ``history/`` and cold-starts. Old labels stay on disk.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import time
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping

from question_engine.api.handler import _generate_for_type
from question_engine.core.base import QUESTION_TYPES
from question_engine.ml.effort import has_effort_scorer, score_effort
from question_engine.ml.knob_introspect import (
    has_continuous_difficulty,
    list_continuous_difficulty_types,
)
from question_engine.frameworks.primitives.openstax_form_catalogs import (
    live_quality_form_weights,
)
from question_engine.ml.rating_regressor import (
    MIN_PAIRS,
    MIN_TRAIN,
    extract_skeleton_features,
    is_pair_record,
    pair_sides,
    refit_from_ratings,
)
from question_engine.ml.schema import build_generation_record

ROOT = Path(__file__).resolve().parents[2]
LIVE_ROOT = ROOT / "scripts" / "output" / "ml" / "ratings" / "live"

# Same stratified grid as build_hand_rating_set.py.
DIFFICULTY_GRID: tuple[float, ...] = (0.0, 3.0, 6.0, 8.0, 12.0, 16.0, 20.0, 25.0)

# Default live campaign: every Ready continuous-D topic.
ALL_TOPICS_CAMPAIGN = "all_topics"

# Named subset: skeleton-path derivative rule topics (backward compatible).
SKELETON_DERIV_CAMPAIGN = "skeleton_deriv"
SKELETON_DERIV_TYPE_IDS: tuple[str, ...] = (
    "calc_diff_power_rule",
    "calc_diff_product_rule",
    "calc_diff_quotient_rule",
    "calc_diff_chain_rule",
    "calc_diff_trigonometric",
    "calc_diff_natural_logarithms_and_exponentials",
    "calc_diff_inverse_trigonometric",
    "calc_diff_higher_order_derivatives",
    "calc_diff_general",
)

# Paths whose edits change generation and should reset the live model.
_GEN_REV_PATHS: tuple[str, ...] = (
    "question_engine/frameworks",
    "question_engine/generators",
    "question_engine/catalogs",
    "question_engine/types",
)

_MAX_GENERATE_ATTEMPTS = 5
ACTIVE_SHORTLIST = 6
UCB_KAPPA = 1.0
BEST_OF_CANDIDATES = 3


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _engine_rev() -> str | None:
    """Fingerprint the generation process.

    ``POLY_ENGINE_REV`` / ``GIT_COMMIT`` win (tests + explicit bumps).
    Otherwise ``git HEAD`` plus a short hash of uncommitted ``question_engine``
    generation-path diffs so WIP edits cold-start the live model.
    """
    env = os.environ.get("POLY_ENGINE_REV") or os.environ.get("GIT_COMMIT")
    if env:
        return env.strip()
    try:
        head = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(ROOT),
            stderr=subprocess.DEVNULL,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=3,
        ).strip()
        diff = subprocess.check_output(
            ["git", "diff", "HEAD", "--", *_GEN_REV_PATHS],
            cwd=str(ROOT),
            stderr=subprocess.DEVNULL,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=8,
        )
        status = subprocess.check_output(
            ["git", "status", "--porcelain", "--", *_GEN_REV_PATHS],
            cwd=str(ROOT),
            stderr=subprocess.DEVNULL,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        dirty = f"{diff}\n{status}".strip()
        if not dirty:
            return head or None
        fp = hashlib.sha1(dirty.encode("utf-8", errors="replace")).hexdigest()[:8]
        return f"{head}+{fp}" if head else fp
    except Exception:  # noqa: BLE001
        return None


def generator_key_for_type(type_id: str) -> str:
    """Resolved generator key, or the type_id when a leaf has no shared gen."""
    qt = QUESTION_TYPES.get(type_id)
    if qt is None:
        return str(type_id)
    key = getattr(qt, "_generator_key", None)
    return str(key) if key else str(type_id)


def all_ready_type_ids() -> tuple[str, ...]:
    """Ready continuous-D topics (scaffolds excluded). Learning stays available on WIP leaves."""
    import question_engine.types  # noqa: F401 — register catalogs

    rows = list_continuous_difficulty_types(ready_only=True, include_scaffolds=False)
    return tuple(str(r["type_id"]) for r in rows if r.get("type_id"))


def nearest_grid_bin(difficulty: float, grid: tuple[float, ...] = DIFFICULTY_GRID) -> float:
    """Map a continuous D to the nearest stratified grid anchor."""
    return min(grid, key=lambda g: abs(g - float(difficulty)))


def iter_rated_item_views(ratings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Flatten pair records so coverage / D bins see both sides."""
    out: list[dict[str, Any]] = []
    for row in ratings:
        if is_pair_record(row):
            if row.get("skipped"):
                continue
            sides = pair_sides(row)
            if sides is None:
                continue
            for side in sides:
                view = dict(side)
                if "theta_requested" not in view:
                    raw_d = view.get("difficulty")
                    if raw_d is None:
                        raw_d = (view.get("theta_full") or {}).get("difficulty")
                    if raw_d is not None:
                        view["theta_requested"] = {"difficulty": raw_d}
                if not view.get("type_id"):
                    view["type_id"] = row.get("type_id")
                if not view.get("generator"):
                    view["generator"] = row.get("generator")
                out.append(view)
            continue
        if row.get("rating_1_to_5") is None and row.get("skipped"):
            continue
        out.append(row)
    return out


def bin_counts_from_ratings(
    ratings: list[dict[str, Any]],
    *,
    grid: tuple[float, ...] = DIFFICULTY_GRID,
) -> dict[float, int]:
    counts: Counter[float] = Counter({d: 0 for d in grid})
    for row in iter_rated_item_views(ratings):
        raw = row.get("theta_requested", {}).get("difficulty") if isinstance(row.get("theta_requested"), dict) else None
        if raw is None:
            raw = row.get("difficulty")
        if raw is None:
            continue
        try:
            d = float(raw)
        except (TypeError, ValueError):
            continue
        counts[nearest_grid_bin(d, grid)] += 1
    return {float(k): int(v) for k, v in counts.items()}


def pick_next_difficulty(
    ratings: list[dict[str, Any]],
    *,
    grid: tuple[float, ...] = DIFFICULTY_GRID,
    rng_seed: int | None = None,
) -> float:
    """Prefer under-sampled grid bins; break ties by space-filling then cycle.

    Among bins with the minimum count, choose the one farthest from the mean of
    already-rated difficulties (space-filling). If none rated yet, start at the
    middle of the grid. Optional ``rng_seed`` only affects seed mixing elsewhere.
    """
    del rng_seed  # reserved for future jitter; policy is deterministic for v1 tests
    counts = bin_counts_from_ratings(ratings, grid=grid)
    min_count = min(counts[d] for d in grid)
    underfilled = [d for d in grid if counts[d] == min_count]
    if len(underfilled) == 1:
        return underfilled[0]

    rated_ds: list[float] = []
    for row in iter_rated_item_views(ratings):
        raw = row.get("theta_requested", {}).get("difficulty") if isinstance(row.get("theta_requested"), dict) else None
        if raw is None:
            raw = row.get("difficulty")
        if raw is None:
            continue
        try:
            rated_ds.append(float(raw))
        except (TypeError, ValueError):
            continue

    if not rated_ds:
        # Start mid-ladder (12.0 on the default 8-point grid).
        mid = grid[len(grid) // 2]
        return mid if mid in underfilled else underfilled[len(underfilled) // 2]

    mean_d = sum(rated_ds) / len(rated_ds)
    # Farthest from mean among underfilled; stable secondary sort by D.
    underfilled_sorted = sorted(underfilled, key=lambda d: (-abs(d - mean_d), d))
    return underfilled_sorted[0]


def type_counts_from_ratings(
    ratings: list[dict[str, Any]],
    type_ids: tuple[str, ...] | list[str],
) -> dict[str, int]:
    counts: Counter[str] = Counter({t: 0 for t in type_ids})
    for row in iter_rated_item_views(ratings):
        tid = str(row.get("type_id") or "")
        if tid in counts:
            counts[tid] += 1
    return {k: int(v) for k, v in counts.items()}


def pick_next_type_and_difficulty(
    ratings: list[dict[str, Any]],
    type_ids: tuple[str, ...] | list[str] = SKELETON_DERIV_TYPE_IDS,
    *,
    grid: tuple[float, ...] = DIFFICULTY_GRID,
    generator_of: Callable[[str], str] | None = None,
) -> tuple[str, float]:
    """Balance coverage, then stratified conceptual / continuous D bins.

    When ``generator_of`` is set, pick an under-sampled **generator** first so
    a shared generator is fed by every topic that uses it, then an under-sampled
    type inside that generator, then D.
    """
    ids = tuple(type_ids)
    if not ids:
        raise ValueError("type_ids required")
    if generator_of is not None:
        type_id = _pick_type_generator_first(ratings, ids, generator_of)
    else:
        tcounts = type_counts_from_ratings(ratings, ids)
        min_t = min(tcounts[t] for t in ids)
        under_types = [t for t in ids if tcounts[t] == min_t]
        # Stable: prefer first underfilled type in catalog order for cold start.
        type_id = under_types[0]
    type_rows = [
        r for r in iter_rated_item_views(ratings) if str(r.get("type_id") or "") == type_id
    ]
    difficulty = pick_next_difficulty(type_rows, grid=grid)
    return type_id, difficulty


def generator_counts_from_ratings(
    ratings: list[dict[str, Any]],
    type_ids: tuple[str, ...] | list[str],
    generator_of: Callable[[str], str],
) -> dict[str, int]:
    ids = tuple(type_ids)
    gens = []
    seen: set[str] = set()
    for tid in ids:
        gen = generator_of(tid)
        if gen not in seen:
            seen.add(gen)
            gens.append(gen)
    counts: Counter[str] = Counter({g: 0 for g in gens})
    id_set = set(ids)
    for row in iter_rated_item_views(ratings):
        tid = str(row.get("type_id") or "")
        gen = str(row.get("generator") or "").strip()
        if not gen:
            gen = generator_of(tid) if tid in id_set else ""
        if gen in counts:
            counts[gen] += 1
    return {k: int(v) for k, v in counts.items()}


def _pick_type_generator_first(
    ratings: list[dict[str, Any]],
    type_ids: tuple[str, ...],
    generator_of: Callable[[str], str],
) -> str:
    gcounts = generator_counts_from_ratings(ratings, type_ids, generator_of)
    min_g = min(gcounts[g] for g in gcounts)
    under_gens = [g for g in gcounts if gcounts[g] == min_g]
    # Stable: first underfilled generator in type-list order.
    gen = None
    for tid in type_ids:
        g = generator_of(tid)
        if g in under_gens:
            gen = g
            break
    if gen is None:
        gen = under_gens[0]
    types_for_gen = [t for t in type_ids if generator_of(t) == gen]
    tcounts = type_counts_from_ratings(ratings, types_for_gen)
    min_t = min(tcounts[t] for t in types_for_gen)
    under_types = [t for t in types_for_gen if tcounts[t] == min_t]
    return under_types[0]


def ratings_for_engine_rev(
    ratings: list[dict[str, Any]],
    engine_rev: str | None,
) -> list[dict[str, Any]]:
    """Train only on labels from the current generation fingerprint."""
    if not engine_rev:
        return list(ratings)
    return [r for r in ratings if str(r.get("engine_rev") or "") == str(engine_rev)]


def infer_engine_rev_from_ratings(ratings: list[dict[str, Any]]) -> str | None:
    revs = [str(r.get("engine_rev") or "") for r in ratings if r.get("engine_rev")]
    if not revs:
        return None
    return Counter(revs).most_common(1)[0][0]


def rotate_ratings_if_engine_changed(
    directory: Path,
    state: dict[str, Any],
    ratings_path: Path,
    current_rev: str | None,
    *,
    load_ratings: Callable[[], list[dict[str, Any]]] | None = None,
) -> bool:
    """If ``engine_rev`` changed, archive the live JSONL and cold-start.

    Returns True when a rotation happened. Old file lands in ``history/``.
    """
    stored = state.get("engine_rev")
    if not stored and ratings_path.is_file() and load_ratings is not None:
        stored = infer_engine_rev_from_ratings(load_ratings())
    if stored and current_rev and str(stored) != str(current_rev) and ratings_path.is_file():
        hist = directory / "history"
        hist.mkdir(parents=True, exist_ok=True)
        safe_old = "".join(
            c if c.isalnum() or c in "-_+" else "_" for c in str(stored)
        )[:48]
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        dest = hist / f"ratings.{safe_old}.{stamp}.jsonl"
        ratings_path.replace(dest)
        pending_path = directory / "pending.json"
        if pending_path.is_file():
            pending_path.unlink()
        state["engine_rev"] = current_rev
        state["rotated_from"] = stored
        state["rotated_at"] = _utc_now()
        state["rotated_to"] = str(dest)
        state["pending"] = None
        state["learning_reset"] = True
        return True
    if current_rev and not stored:
        state["engine_rev"] = current_rev
    elif current_rev:
        state["engine_rev"] = current_rev
    state["learning_reset"] = False
    return False


def load_ratings_jsonl(ratings_path: Path) -> list[dict[str, Any]]:
    if not ratings_path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in ratings_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict):
            rows.append(row)
    return rows


def attach_model_prediction(
    item: dict[str, Any],
    ratings: list[dict[str, Any]],
    *,
    min_train: int = MIN_TRAIN,
    min_pairs: int = MIN_PAIRS,
    engine_rev: str | None = None,
    model: Any = None,
) -> dict[str, Any]:
    """Refit Bayesian utility from current-rev ratings and stamp prediction fields."""
    train = ratings_for_engine_rev(ratings, engine_rev if engine_rev is not None else _engine_rev())
    if model is None:
        model = refit_from_ratings(train, min_train=min_train, min_pairs=min_pairs)
    status = model.status_for(item)
    item["predicted_rating"] = status.predicted_rating
    item["predicted_std"] = status.predicted_std
    item["n_train"] = status.n_train
    item["n_pairs"] = status.n_pairs
    item["model_ready"] = status.model_ready
    item["model_message"] = status.message
    item["min_train"] = status.min_train
    item["min_pairs"] = status.min_pairs
    item["engine_rev"] = item.get("engine_rev") or engine_rev or _engine_rev()
    if "skeleton_features" not in item:
        item["skeleton_features"] = extract_skeleton_features(item)
    return item


def _proxy_row(type_id: str, difficulty: float, generator: str) -> dict[str, Any]:
    return {
        "type_id": type_id,
        "generator": generator,
        "difficulty": difficulty,
        "conceptual_difficulty": difficulty,
        "theta_requested": {"difficulty": difficulty},
        "metadata": {
            "generator": generator,
            "conceptual_difficulty": difficulty,
        },
    }


def _training_item_rows(ratings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for row in ratings:
        if is_pair_record(row):
            sides = pair_sides(row)
            if sides:
                items.extend(dict(s) for s in sides)
        else:
            items.append(row)
    return items


def quality_form_weights_from_model(
    model: Any,
    train_rows: list[dict[str, Any]],
    *,
    seed: int | None = None,
) -> dict[str, float]:
    """Thompson-centered form utilities for ``select_form_id`` (empty if cold)."""
    if model is None or not getattr(model, "model_ready", False):
        return {}
    import numpy as np

    rng = np.random.default_rng(seed)
    return model.categorical_quality_scores(
        _training_item_rows(train_rows),
        "form_id",
        thompson=True,
        rng=rng,
    )


def plan_active_shortlist(
    ratings: list[dict[str, Any]],
    type_ids: tuple[str, ...] | list[str],
    *,
    generator_of: Callable[[str], str] | None = None,
    grid: tuple[float, ...] = DIFFICULTY_GRID,
    n_shortlist: int = ACTIVE_SHORTLIST,
    rng_seed: int | None = None,
) -> list[tuple[str, float]]:
    """Plan (type, D) slots: weakly balance generators, mix D. No generate."""
    import random

    ids = tuple(type_ids)
    if not ids:
        raise ValueError("type_ids required")
    rng = random.Random(rng_seed)
    under_gens: set[str] = set()
    if generator_of is not None:
        gcounts = generator_counts_from_ratings(ratings, ids, generator_of)
        if gcounts:
            min_g = min(gcounts.values())
            under_gens = {g for g, c in gcounts.items() if c == min_g}
    n_under = max(1, n_shortlist // 2) if under_gens else 0
    tcounts = type_counts_from_ratings(ratings, ids)
    min_t = min(tcounts[t] for t in ids)
    under_types = [t for t in ids if tcounts[t] == min_t]

    def _pick_type(prefer_under: bool) -> str:
        if generator_of is not None and prefer_under and under_gens:
            cands = [t for t in ids if generator_of(t) in under_gens]
            if cands:
                return rng.choice(cands)
        return rng.choice(under_types if under_types else list(ids))

    slots: list[tuple[str, float]] = []
    for i in range(int(n_shortlist)):
        tid = _pick_type(prefer_under=(i < n_under))
        d = float(rng.choice(list(grid)))
        slots.append((tid, d))
    return slots


def _pick_type_for_pair(
    ratings: list[dict[str, Any]],
    type_ids: tuple[str, ...],
    generator_of: Callable[[str], str] | None,
) -> str:
    """Cold-start type pick: under-sampled generator, then type. No D."""
    if generator_of is not None:
        return _pick_type_generator_first(ratings, type_ids, generator_of)
    tcounts = type_counts_from_ratings(ratings, type_ids)
    min_t = min(tcounts[t] for t in type_ids)
    under_types = [t for t in type_ids if tcounts[t] == min_t]
    return under_types[0]


def pick_active_pair_slots(
    ratings: list[dict[str, Any]],
    type_ids: tuple[str, ...] | list[str],
    model: Any | None,
    *,
    generator_of: Callable[[str], str] | None = None,
    grid: tuple[float, ...] = DIFFICULTY_GRID,
    n_shortlist: int = ACTIVE_SHORTLIST,
    rng_seed: int | None = None,
    restrict_type: str | None = None,
) -> tuple[tuple[str, float], tuple[str, float]]:
    """One (type, D) for both pair sides. Cold = stratified; ready = UCB.

    Comparison UI is same-topic: A and B share ``type_id`` and the same D bin.
    D is chosen from *session* coverage (not a fresh type's empty bins) so
    pairs rotate the grid after the first mid-ladder pick. Seeds differ later.
    """
    ids = tuple(type_ids)
    if restrict_type:
        ids = (restrict_type,) if restrict_type in ids or not ids else (restrict_type,)
    if not ids:
        raise ValueError("type_ids required")

    if model is None or not getattr(model, "model_ready", False):
        type_id = _pick_type_for_pair(ratings, ids, generator_of)
        # Session-level bins so a new type does not reset every pair to mid-grid 12.
        difficulty = pick_next_difficulty(ratings, grid=grid)
        slot = (type_id, float(difficulty))
        return slot, slot

    slots = plan_active_shortlist(
        ratings,
        ids,
        generator_of=generator_of,
        grid=grid,
        n_shortlist=n_shortlist,
        rng_seed=rng_seed,
    )
    scored: list[tuple[str, float, float, float, float]] = []
    for tid, d in slots:
        gen = generator_of(tid) if generator_of else tid
        pred = model.predict_mean_std(_proxy_row(tid, d, gen))
        mean, std = pred if pred is not None else (3.0, 1.0)
        scored.append((tid, d, float(mean), float(std), float(mean + UCB_KAPPA * std)))
    scored.sort(key=lambda x: -x[4])
    a = scored[0]
    slot = (a[0], a[1])
    return slot, slot


def pick_active_single_slot(
    ratings: list[dict[str, Any]],
    type_ids: tuple[str, ...] | list[str],
    model: Any | None,
    *,
    generator_of: Callable[[str], str] | None = None,
    grid: tuple[float, ...] = DIFFICULTY_GRID,
    rng_seed: int | None = None,
    restrict_type: str | None = None,
) -> tuple[str, float]:
    """Max-UCB slot when ready; stratified when cold."""
    if model is None or not getattr(model, "model_ready", False):
        ids = tuple(type_ids)
        if restrict_type:
            ids = (restrict_type,)
        return pick_next_type_and_difficulty(
            ratings, ids, generator_of=generator_of, grid=grid
        )
    a, _ = pick_active_pair_slots(
        ratings,
        type_ids,
        model,
        generator_of=generator_of,
        grid=grid,
        rng_seed=rng_seed,
        restrict_type=restrict_type,
    )
    return a


def generate_live_item(
    type_id: str,
    difficulty: float,
    seed: int,
    *,
    session_name: str,
    campaign_id: str | None = None,
    quality_weights: dict[str, float] | None = None,
) -> dict[str, Any]:
    """Generate one live-rating item. Quality weights tilt form_id, not D costs."""
    settings: dict[str, Any] = {
        "difficulty": difficulty,
        "conceptual_difficulty": difficulty,
        "count": 1,
        "include_answer_key": True,
        "seed": seed,
    }
    if quality_weights:
        settings["live_quality_form_weights"] = dict(quality_weights)
    t0 = time.perf_counter()
    with live_quality_form_weights(quality_weights or None):
        questions = _generate_for_type(type_id, settings)
    elapsed_ms = int((time.perf_counter() - t0) * 1000)
    if not questions:
        raise RuntimeError(f"empty generate for {type_id}")
    question = questions[0]
    gen_settings = (question.metadata or {}).get("generation_settings") or settings

    y_effort = None
    y_mode = None
    effort_feats: dict[str, Any] = {}
    prompt = (question.prompt_latex or question.prompt_text or "").strip()
    answer = (question.answer_latex or question.answer_text or "").strip()
    if has_effort_scorer(type_id):
        y_effort, effort_feats = score_effort(type_id, prompt, answer)
        if isinstance(effort_feats, dict):
            raw_mode = effort_feats.get("form") or effort_feats.get("mode")
            y_mode = str(raw_mode) if raw_mode is not None else None

    record = build_generation_record(
        type_id,
        question,
        gen_settings if isinstance(gen_settings, dict) else settings,
        y_effort=y_effort,
        y_mode=y_mode,
        effort_feats=effort_feats,
    )
    row = record.to_dict()
    meta = row.get("metadata") or {}
    generator = (
        meta.get("generator")
        or (row.get("theta_full") or {}).get("generator")
        or getattr(question, "metadata", {}).get("generator")
    )
    rating_id = f"live_{session_name}_{uuid.uuid4().hex[:12]}"
    item: dict[str, Any] = {
        **row,
        "rating_id": rating_id,
        "generator": generator,
        "theta_requested": {
            "difficulty": difficulty,
            "conceptual_difficulty": difficulty,
            "seed": seed,
            "count": 1,
            "type_id": type_id,
        },
        "theta_full": row.get("theta_full") or {},
        "bin": nearest_grid_bin(difficulty),
        "engine_rev": _engine_rev(),
        "generated_at": _utc_now(),
        "generate_ms": elapsed_ms,
        "session": session_name,
        "rating_1_to_5": None,
        "minutes": None,
        "notes": None,
        "topic_fit_ok": None,
        "latex_ok": None,
        "broken": None,
        "rated_at": None,
    }
    if campaign_id:
        item["campaign"] = campaign_id
    item["skeleton_features"] = extract_skeleton_features(item)
    return item


def _select_best_of(items: list[dict[str, Any]], model: Any) -> dict[str, Any]:
    if not items:
        raise ValueError("no candidates")
    if model is None or not getattr(model, "model_ready", False) or len(items) == 1:
        return items[0]
    best = items[0]
    best_score = float("-inf")
    for it in items:
        pred = model.predict_mean_std(it)
        score = (pred[0] + UCB_KAPPA * pred[1]) if pred is not None else 0.0
        if score > best_score:
            best_score = score
            best = it
    return best


def _form_id_of(item: Mapping[str, Any] | dict[str, Any]) -> str:
    feats = item.get("skeleton_features") if isinstance(item.get("skeleton_features"), dict) else {}
    meta = item.get("metadata") if isinstance(item.get("metadata"), dict) else {}
    return str(
        (feats or {}).get("form_id")
        or meta.get("form_id")
        or item.get("form_id")
        or ""
    )


def _apply_side_flags(item: dict[str, Any], flags: Mapping[str, Any]) -> None:
    if "topic_fit_ok" in flags:
        item["topic_fit_ok"] = flags.get("topic_fit_ok")
    if "latex_ok" in flags:
        item["latex_ok"] = flags.get("latex_ok")
    if "broken" in flags:
        item["broken"] = flags.get("broken")
    if "rating_1_to_5" in flags and flags.get("rating_1_to_5") is not None:
        item["rating_1_to_5"] = flags.get("rating_1_to_5")
    if "notes" in flags and flags.get("notes"):
        item["notes"] = flags.get("notes")


def _session_slug(type_id: str, session: str | None) -> str:
    if session:
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in session.strip())
        return safe or type_id
    return type_id


class LiveRatingSession:
    """Append-only ratings + pending item for one type_id / session folder."""

    def __init__(
        self,
        type_id: str,
        *,
        session: str | None = None,
        root: Path | None = None,
        mix_seeds: bool = True,
    ) -> None:
        if not has_continuous_difficulty(type_id):
            raise ValueError(f"type_id does not expose continuous difficulty: {type_id}")
        self.type_id = type_id
        self.session_name = _session_slug(type_id, session)
        self.root = Path(root) if root else LIVE_ROOT
        self.dir = self.root / self.session_name
        self.dir.mkdir(parents=True, exist_ok=True)
        self.ratings_path = self.dir / "ratings.jsonl"
        self.state_path = self.dir / "session.json"
        self.mix_seeds = mix_seeds
        self._state = self._load_state()
        self._maybe_rotate_engine()

    def _maybe_rotate_engine(self) -> bool:
        rotated = rotate_ratings_if_engine_changed(
            self.dir,
            self._state,
            self.ratings_path,
            _engine_rev(),
            load_ratings=lambda: load_ratings_jsonl(self.ratings_path),
        )
        self._save_state()
        return rotated

    def _load_state(self) -> dict[str, Any]:
        if self.state_path.is_file():
            try:
                data = json.loads(self.state_path.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    return data
            except json.JSONDecodeError:
                pass
        return {
            "type_id": self.type_id,
            "session": self.session_name,
            "seed_counter": 0,
            "pending": None,
            "created_at": _utc_now(),
            "engine_rev": _engine_rev(),
            "policy": "pairwise_bayesian_utility_v2",
            "model": "bayesian_linear_bt_refit_each_submit",
            "min_train": MIN_TRAIN,
            "min_pairs": MIN_PAIRS,
        }

    def _save_state(self) -> None:
        self._state["type_id"] = self.type_id
        self._state["session"] = self.session_name
        self._state["engine_rev"] = self._state.get("engine_rev") or _engine_rev()
        self._state["updated_at"] = _utc_now()
        self.state_path.write_text(
            json.dumps(self._state, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def load_ratings(self) -> list[dict[str, Any]]:
        return load_ratings_jsonl(self.ratings_path)

    def train_ratings(self) -> list[dict[str, Any]]:
        return ratings_for_engine_rev(self.load_ratings(), _engine_rev())

    def coverage(self) -> dict[str, Any]:
        ratings = self.load_ratings()
        train = ratings_for_engine_rev(ratings, _engine_rev())
        counts = bin_counts_from_ratings(train)
        model = refit_from_ratings(train)
        status = model.status_for(None)
        return {
            "type_id": self.type_id,
            "session": self.session_name,
            "n_ratings": len(train),
            "n_archived": max(0, len(ratings) - len(train)),
            "by_difficulty": {str(k): v for k, v in sorted(counts.items())},
            "pending": self._state.get("pending"),
            "dir": str(self.dir),
            "engine_rev": _engine_rev(),
            "learning_reset": bool(self._state.get("learning_reset")),
            "model_ready": status.model_ready,
            "n_train": status.n_train,
            "n_pairs": status.n_pairs,
            "min_train": status.min_train,
            "min_pairs": status.min_pairs,
            "model_message": status.message,
        }

    def _next_seed(self, difficulty: float) -> int:
        counter = int(self._state.get("seed_counter") or 0) + 1
        self._state["seed_counter"] = counter
        # Mix seeds at similar D: counter + difficulty hash + type hash.
        base = (
            counter * 9973
            + int(difficulty * 1000)
            + (hash(self.type_id) % 100_003)
        )
        if self.mix_seeds:
            # Extra salt so consecutive same-D picks diverge.
            base ^= (counter * 7919) & 0x7FFFFFFF
        return abs(base) % 2_000_000_000

    def generate_next(
        self,
        *,
        difficulty: float | None = None,
        seed: int | None = None,
    ) -> dict[str, Any]:
        """Generate the next single item (legacy / CLI ``--rating``)."""
        self._maybe_rotate_engine()
        ratings = self.train_ratings()
        model = refit_from_ratings(ratings)
        if difficulty is None:
            if model.model_ready:
                _, theta_d = pick_active_single_slot(
                    ratings,
                    (self.type_id,),
                    model,
                    rng_seed=int(self._state.get("seed_counter") or 0),
                    restrict_type=self.type_id,
                )
            else:
                theta_d = pick_next_difficulty(ratings)
        else:
            theta_d = float(difficulty)
        qw = quality_form_weights_from_model(
            model, ratings, seed=int(self._state.get("seed_counter") or 0)
        )
        if seed is not None:
            use_seed = int(seed)
            item = generate_live_item(
                self.type_id,
                theta_d,
                use_seed,
                session_name=self.session_name,
                quality_weights=qw,
            )
        else:
            n_try = BEST_OF_CANDIDATES if model.model_ready else 1
            cands: list[dict[str, Any]] = []
            last_err: Exception | None = None
            for _ in range(n_try):
                try:
                    cands.append(
                        generate_live_item(
                            self.type_id,
                            theta_d,
                            self._next_seed(theta_d),
                            session_name=self.session_name,
                            quality_weights=qw,
                        )
                    )
                except Exception as exc:  # noqa: BLE001
                    last_err = exc
            if not cands:
                raise RuntimeError(f"generate failed: {last_err}")
            item = _select_best_of(cands, model)
            use_seed = int((item.get("theta_requested") or {}).get("seed") or 0)
        attach_model_prediction(item, ratings, engine_rev=_engine_rev(), model=model)
        self._store_pending_single(item, theta_d, use_seed)
        return item

    def generate_next_pair(
        self,
        *,
        difficulty: float | None = None,
        seed: int | None = None,
    ) -> dict[str, Any]:
        """Default next action: two candidates for A/B comparison."""
        self._maybe_rotate_engine()
        ratings = self.train_ratings()
        model = refit_from_ratings(ratings)
        (t1, d1), _ = pick_active_pair_slots(
            ratings,
            (self.type_id,),
            model,
            rng_seed=int(self._state.get("seed_counter") or 0),
            restrict_type=self.type_id,
        )
        t1 = self.type_id
        if difficulty is not None:
            d1 = float(difficulty)
        t2, d2 = t1, d1
        qw = quality_form_weights_from_model(
            model, ratings, seed=int(self._state.get("seed_counter") or 0)
        )
        seed_a = int(seed) if seed is not None else self._next_seed(d1)
        seed_b = (int(seed) + 1) if seed is not None else self._next_seed(d2)
        left = generate_live_item(
            t1, d1, seed_a, session_name=self.session_name, quality_weights=qw
        )
        right = generate_live_item(
            t2, d2, seed_b, session_name=self.session_name, quality_weights=qw
        )
        attach_model_prediction(left, ratings, engine_rev=_engine_rev(), model=model)
        attach_model_prediction(right, ratings, engine_rev=_engine_rev(), model=model)
        return self._store_pending_pair(left, right)

    def _store_pending_single(self, item: dict[str, Any], theta_d: float, use_seed: int) -> None:
        self._state["pending"] = {
            "mode": "single",
            "rating_id": item["rating_id"],
            "type_id": self.type_id,
            "difficulty": theta_d,
            "bin": nearest_grid_bin(theta_d),
            "seed": use_seed,
            "generated_at": item["generated_at"],
        }
        pending_path = self.dir / "pending.json"
        pending_path.write_text(
            json.dumps(item, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        self._save_state()

    def _store_pending_pair(self, left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
        pair_id = f"pair_{self.session_name}_{uuid.uuid4().hex[:12]}"
        payload = {
            "mode": "pair",
            "pair_id": pair_id,
            "left": left,
            "right": right,
            "engine_rev": _engine_rev(),
            "session": self.session_name,
        }
        self._state["pending"] = {
            "mode": "pair",
            "pair_id": pair_id,
            "left": {
                "rating_id": left.get("rating_id"),
                "type_id": left.get("type_id"),
                "difficulty": left.get("difficulty"),
                "seed": (left.get("theta_requested") or {}).get("seed"),
            },
            "right": {
                "rating_id": right.get("rating_id"),
                "type_id": right.get("type_id"),
                "difficulty": right.get("difficulty"),
                "seed": (right.get("theta_requested") or {}).get("seed"),
            },
            "generated_at": left.get("generated_at"),
        }
        pending_path = self.dir / "pending.json"
        pending_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        self._save_state()
        return payload

    def _load_pending_item(self) -> dict[str, Any] | None:
        pending_path = self.dir / "pending.json"
        if not pending_path.is_file():
            return None
        try:
            data = json.loads(pending_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None
        return data if isinstance(data, dict) else None

    def submit(
        self,
        *,
        rating_id: str | None = None,
        pair_id: str | None = None,
        winner: str | None = None,
        rating_1_to_5: int | None = None,
        minutes: float | None = None,
        notes: str | None = None,
        topic_fit_ok: bool | None = None,
        latex_ok: bool | None = None,
        broken: bool | None = None,
        left: dict[str, Any] | None = None,
        right: dict[str, Any] | None = None,
        skip: bool = False,
    ) -> dict[str, Any]:
        """Append a pair comparison or a single-item rating."""
        pending_meta = self._state.get("pending")
        pending = self._load_pending_item()
        if pending is None:
            raise ValueError("No pending item to rate — call next first")
        if pending.get("mode") == "pair" or pending.get("pair_id"):
            return self._submit_pair(
                pending,
                pending_meta=pending_meta,
                pair_id=pair_id,
                winner=winner,
                minutes=minutes,
                notes=notes,
                left=left,
                right=right,
                skip=skip,
            )
        return self._submit_single(
            pending,
            pending_meta=pending_meta,
            rating_id=rating_id,
            rating_1_to_5=rating_1_to_5,
            minutes=minutes,
            notes=notes,
            topic_fit_ok=topic_fit_ok,
            latex_ok=latex_ok,
            broken=broken,
            skip=skip,
        )

    def _clear_pending(self) -> None:
        self._state["pending"] = None
        pending_path = self.dir / "pending.json"
        if pending_path.is_file():
            pending_path.unlink()
        self._save_state()

    def _model_submit_payload(self, extra: dict[str, Any]) -> dict[str, Any]:
        train = self.train_ratings()
        model = refit_from_ratings(train)
        status = model.status_for(None)
        extra.update(
            {
                "ok": True,
                "coverage": self.coverage(),
                "model_ready": status.model_ready,
                "n_train": status.n_train,
                "n_pairs": status.n_pairs,
                "min_train": status.min_train,
                "min_pairs": status.min_pairs,
                "model_message": status.message,
            }
        )
        return extra

    def _submit_single(
        self,
        item: dict[str, Any],
        *,
        pending_meta: Any,
        rating_id: str | None,
        rating_1_to_5: int | None,
        minutes: float | None,
        notes: str | None,
        topic_fit_ok: bool | None,
        latex_ok: bool | None,
        broken: bool | None,
        skip: bool,
    ) -> dict[str, Any]:
        if rating_id and item.get("rating_id") != rating_id:
            raise ValueError(
                f"rating_id mismatch: pending={item.get('rating_id')} got={rating_id}"
            )
        if not skip:
            if rating_1_to_5 is None:
                raise ValueError("rating_1_to_5 required unless skip=true")
            score = int(rating_1_to_5)
            if score < 1 or score > 5:
                raise ValueError("rating_1_to_5 must be 1–5")
        else:
            score = None

        out = dict(item)
        out.update(
            {
                "rating_1_to_5": score,
                "minutes": minutes,
                "notes": notes,
                "topic_fit_ok": topic_fit_ok,
                "latex_ok": latex_ok,
                "broken": broken,
                "skipped": bool(skip),
                "rated_at": _utc_now(),
                "engine_rev": out.get("engine_rev") or _engine_rev(),
            }
        )
        with self.ratings_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(out, ensure_ascii=False) + "\n")
        self._state["last_rated_id"] = out["rating_id"]
        self._clear_pending()
        return self._model_submit_payload(
            {"rating_id": out["rating_id"], "pending_was": pending_meta}
        )

    def _submit_pair(
        self,
        pending: dict[str, Any],
        *,
        pending_meta: Any,
        pair_id: str | None,
        winner: str | None,
        minutes: float | None,
        notes: str | None,
        left: dict[str, Any] | None,
        right: dict[str, Any] | None,
        skip: bool,
    ) -> dict[str, Any]:
        left_item = dict(pending.get("left") or {})
        right_item = dict(pending.get("right") or {})
        if not left_item or not right_item:
            raise ValueError("Pending pair is missing left/right items")
        pending_pid = pending.get("pair_id")
        if pair_id and pending_pid and pair_id != pending_pid:
            raise ValueError(f"pair_id mismatch: pending={pending_pid} got={pair_id}")
        left_flags = left or {}
        right_flags = right or {}
        _apply_side_flags(left_item, left_flags)
        _apply_side_flags(right_item, right_flags)
        win = None if skip else str(winner or "").strip().lower()
        if not skip:
            if win not in {"a", "b", "tie"}:
                raise ValueError("winner must be a, b, or tie unless skip=true")
        record = {
            "record_kind": "pair",
            "pair_id": pending_pid,
            "left": left_item,
            "right": right_item,
            "winner": win,
            "minutes": minutes,
            "notes": notes,
            "skipped": bool(skip),
            "rated_at": _utc_now(),
            "engine_rev": pending.get("engine_rev") or _engine_rev(),
            "session": self.session_name,
            "generators": [left_item.get("generator"), right_item.get("generator")],
            "form_ids": [_form_id_of(left_item), _form_id_of(right_item)],
            "type_ids": [left_item.get("type_id"), right_item.get("type_id")],
        }
        with self.ratings_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        self._state["last_rated_id"] = pending_pid
        self._clear_pending()
        return self._model_submit_payload(
            {"pair_id": pending_pid, "winner": win, "pending_was": pending_meta}
        )


class MultiTypeCampaign:
    """Shared live rater across many continuous-D topics.

    One JSONL under ``live/<session>/``. Picks an under-sampled generator, then
    type, then session-level D (cold) or UCB (ready). Each pair is one topic
    at one D (different seeds). Ratings from any topic still update every
    other topic on the same generator. Bayesian utility refits on every
    submit, trained only on the current ``engine_rev`` (generation-process
    change rotates JSONL → ``history/``).
    """

    campaign_id = ALL_TOPICS_CAMPAIGN
    pick_by_generator = True

    def __init__(
        self,
        *,
        session: str | None = None,
        root: Path | None = None,
        type_ids: tuple[str, ...] | list[str] | None = None,
        campaign: str | None = None,
        mix_seeds: bool = True,
    ) -> None:
        self.campaign_id = campaign or self.campaign_id
        self.type_ids = tuple(type_ids) if type_ids is not None else all_ready_type_ids()
        if not self.type_ids:
            raise ValueError("campaign has no continuous-D types")
        for tid in self.type_ids:
            if not has_continuous_difficulty(tid):
                raise ValueError(f"type_id lacks continuous difficulty: {tid}")
        self.session_name = _session_slug(
            self.campaign_id, session or self.campaign_id
        )
        self.root = Path(root) if root else LIVE_ROOT
        self.dir = self.root / self.session_name
        self.dir.mkdir(parents=True, exist_ok=True)
        self.ratings_path = self.dir / "ratings.jsonl"
        self.state_path = self.dir / "session.json"
        self.mix_seeds = mix_seeds
        self._state = self._load_state()
        self._maybe_rotate_engine()

    def _maybe_rotate_engine(self) -> bool:
        rotated = rotate_ratings_if_engine_changed(
            self.dir,
            self._state,
            self.ratings_path,
            _engine_rev(),
            load_ratings=lambda: load_ratings_jsonl(self.ratings_path),
        )
        self._save_state()
        return rotated

    def _load_state(self) -> dict[str, Any]:
        if self.state_path.is_file():
            try:
                data = json.loads(self.state_path.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    return data
            except json.JSONDecodeError:
                pass
        return {
            "campaign": self.campaign_id,
            "session": self.session_name,
            "type_ids": list(self.type_ids),
            "seed_counter": 0,
            "pending": None,
            "created_at": _utc_now(),
            "engine_rev": _engine_rev(),
            "policy": "pairwise_bayesian_utility_v2",
            "model": "bayesian_linear_bt_shared_generator",
            "min_train": MIN_TRAIN,
            "min_pairs": MIN_PAIRS,
        }

    def _save_state(self) -> None:
        self._state["campaign"] = self.campaign_id
        self._state["session"] = self.session_name
        self._state["type_ids"] = list(self.type_ids)
        self._state["engine_rev"] = self._state.get("engine_rev") or _engine_rev()
        self._state["updated_at"] = _utc_now()
        self.state_path.write_text(
            json.dumps(self._state, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def load_ratings(self) -> list[dict[str, Any]]:
        return load_ratings_jsonl(self.ratings_path)

    def train_ratings(self) -> list[dict[str, Any]]:
        return ratings_for_engine_rev(self.load_ratings(), _engine_rev())

    def coverage(self) -> dict[str, Any]:
        ratings = self.load_ratings()
        train = ratings_for_engine_rev(ratings, _engine_rev())
        counts = bin_counts_from_ratings(train)
        by_type = type_counts_from_ratings(train, self.type_ids)
        by_gen = generator_counts_from_ratings(
            train, self.type_ids, generator_key_for_type
        )
        model = refit_from_ratings(train)
        status = model.status_for(None)
        return {
            "campaign": self.campaign_id,
            "session": self.session_name,
            "n_ratings": len(train),
            "n_archived": max(0, len(ratings) - len(train)),
            "n_types": len(self.type_ids),
            "by_difficulty": {str(k): v for k, v in sorted(counts.items())},
            "by_type": {k: v for k, v in by_type.items() if v},
            "by_generator": {k: v for k, v in by_gen.items() if v},
            "pending": self._state.get("pending"),
            "dir": str(self.dir),
            "engine_rev": _engine_rev(),
            "learning_reset": bool(self._state.get("learning_reset")),
            "model_ready": status.model_ready,
            "n_train": status.n_train,
            "n_pairs": status.n_pairs,
            "min_train": status.min_train,
            "min_pairs": status.min_pairs,
            "model_message": status.message,
        }

    def _next_seed(self, type_id: str, difficulty: float) -> int:
        counter = int(self._state.get("seed_counter") or 0) + 1
        self._state["seed_counter"] = counter
        base = (
            counter * 9973
            + int(difficulty * 1000)
            + (hash(type_id) % 100_003)
        )
        if self.mix_seeds:
            base ^= (counter * 7919) & 0x7FFFFFFF
        return abs(base) % 2_000_000_000

    def _gen_of(self) -> Callable[[str], str] | None:
        return generator_key_for_type if self.pick_by_generator else None

    def generate_next(
        self,
        *,
        type_id: str | None = None,
        difficulty: float | None = None,
        seed: int | None = None,
    ) -> dict[str, Any]:
        self._maybe_rotate_engine()
        ratings = self.train_ratings()
        model = refit_from_ratings(ratings)
        last_err: Exception | None = None
        use_type = type_id
        theta_d = float(difficulty) if difficulty is not None else None
        item: dict[str, Any] | None = None
        qw = quality_form_weights_from_model(
            model, ratings, seed=int(self._state.get("seed_counter") or 0)
        )
        for _attempt in range(_MAX_GENERATE_ATTEMPTS):
            if use_type is None or theta_d is None:
                if model.model_ready:
                    pick_t, pick_d = pick_active_single_slot(
                        ratings,
                        self.type_ids,
                        model,
                        generator_of=self._gen_of(),
                        rng_seed=int(self._state.get("seed_counter") or 0),
                        restrict_type=type_id,
                    )
                else:
                    pick_t, pick_d = pick_next_type_and_difficulty(
                        ratings,
                        self.type_ids,
                        generator_of=self._gen_of(),
                    )
                use_type = type_id or pick_t
                theta_d = float(difficulty) if difficulty is not None else pick_d
            if use_type not in self.type_ids:
                raise ValueError(f"type_id not in {self.campaign_id} campaign: {use_type}")
            try:
                if seed is not None:
                    item = generate_live_item(
                        use_type,
                        theta_d,
                        int(seed),
                        session_name=self.session_name,
                        campaign_id=self.campaign_id,
                        quality_weights=qw,
                    )
                else:
                    n_try = BEST_OF_CANDIDATES if model.model_ready else 1
                    cands: list[dict[str, Any]] = []
                    for _ in range(n_try):
                        cands.append(
                            generate_live_item(
                                use_type,
                                theta_d,
                                self._next_seed(use_type, theta_d),
                                session_name=self.session_name,
                                campaign_id=self.campaign_id,
                                quality_weights=qw,
                            )
                        )
                    item = _select_best_of(cands, model)
                break
            except Exception as exc:  # noqa: BLE001 — retry another type in all-topics
                last_err = exc
            if type_id is not None and difficulty is not None and seed is not None:
                break
            if type_id is not None:
                use_type = type_id
                theta_d = float(difficulty) if difficulty is not None else None
                continue
            use_type = None
            theta_d = None
        if item is None:
            raise RuntimeError(
                f"generate failed after {_MAX_GENERATE_ATTEMPTS} attempts: {last_err}"
            )
        assert use_type is not None and theta_d is not None
        attach_model_prediction(item, ratings, engine_rev=_engine_rev(), model=model)
        use_seed = int((item.get("theta_requested") or {}).get("seed") or 0)
        self._store_pending_single(item, use_type, theta_d, use_seed)
        return item

    def generate_next_pair(
        self,
        *,
        type_id: str | None = None,
        difficulty: float | None = None,
        seed: int | None = None,
    ) -> dict[str, Any]:
        self._maybe_rotate_engine()
        ratings = self.train_ratings()
        model = refit_from_ratings(ratings)
        (t1, d1), _ = pick_active_pair_slots(
            ratings,
            self.type_ids,
            model,
            generator_of=self._gen_of(),
            rng_seed=int(self._state.get("seed_counter") or 0),
            restrict_type=type_id,
        )
        if type_id is not None:
            t1 = type_id
        if difficulty is not None:
            d1 = float(difficulty)
        t2, d2 = t1, d1
        if t1 not in self.type_ids:
            raise ValueError(f"type_id not in {self.campaign_id} campaign: {t1}")
        qw = quality_form_weights_from_model(
            model, ratings, seed=int(self._state.get("seed_counter") or 0)
        )
        seed_a = int(seed) if seed is not None else self._next_seed(t1, d1)
        seed_b = (int(seed) + 1) if seed is not None else self._next_seed(t2, d2)
        last_err: Exception | None = None
        left = right = None
        for _attempt in range(_MAX_GENERATE_ATTEMPTS):
            try:
                left = generate_live_item(
                    t1, d1, seed_a,
                    session_name=self.session_name,
                    campaign_id=self.campaign_id,
                    quality_weights=qw,
                )
                right = generate_live_item(
                    t2, d2, seed_b,
                    session_name=self.session_name,
                    campaign_id=self.campaign_id,
                    quality_weights=qw,
                )
                break
            except Exception as exc:  # noqa: BLE001
                last_err = exc
                if type_id is not None and difficulty is not None and seed is not None:
                    break
                (t1, d1), _ = pick_active_pair_slots(
                    ratings,
                    self.type_ids,
                    model,
                    generator_of=self._gen_of(),
                    rng_seed=int(self._state.get("seed_counter") or 0) + _attempt + 1,
                    restrict_type=type_id,
                )
                if type_id is not None:
                    t1 = type_id
                if difficulty is not None:
                    d1 = float(difficulty)
                t2, d2 = t1, d1
                seed_a = self._next_seed(t1, d1)
                seed_b = self._next_seed(t2, d2)
        if left is None or right is None:
            raise RuntimeError(
                f"generate pair failed after {_MAX_GENERATE_ATTEMPTS} attempts: {last_err}"
            )
        attach_model_prediction(left, ratings, engine_rev=_engine_rev(), model=model)
        attach_model_prediction(right, ratings, engine_rev=_engine_rev(), model=model)
        return self._store_pending_pair(left, right)

    def _store_pending_single(
        self, item: dict[str, Any], use_type: str, theta_d: float, use_seed: int
    ) -> None:
        self._state["pending"] = {
            "mode": "single",
            "rating_id": item["rating_id"],
            "type_id": use_type,
            "difficulty": theta_d,
            "bin": nearest_grid_bin(theta_d),
            "seed": use_seed,
            "generated_at": item["generated_at"],
        }
        pending_path = self.dir / "pending.json"
        pending_path.write_text(
            json.dumps(item, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        self._save_state()

    def _store_pending_pair(self, left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
        pair_id = f"pair_{self.session_name}_{uuid.uuid4().hex[:12]}"
        payload = {
            "mode": "pair",
            "pair_id": pair_id,
            "left": left,
            "right": right,
            "engine_rev": _engine_rev(),
            "session": self.session_name,
            "campaign": self.campaign_id,
        }
        self._state["pending"] = {
            "mode": "pair",
            "pair_id": pair_id,
            "left": {
                "rating_id": left.get("rating_id"),
                "type_id": left.get("type_id"),
                "difficulty": left.get("difficulty"),
                "seed": (left.get("theta_requested") or {}).get("seed"),
            },
            "right": {
                "rating_id": right.get("rating_id"),
                "type_id": right.get("type_id"),
                "difficulty": right.get("difficulty"),
                "seed": (right.get("theta_requested") or {}).get("seed"),
            },
            "generated_at": left.get("generated_at"),
        }
        pending_path = self.dir / "pending.json"
        pending_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        self._save_state()
        return payload

    def _load_pending_item(self) -> dict[str, Any] | None:
        pending_path = self.dir / "pending.json"
        if not pending_path.is_file():
            return None
        try:
            data = json.loads(pending_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None
        return data if isinstance(data, dict) else None

    def submit(
        self,
        *,
        rating_id: str | None = None,
        pair_id: str | None = None,
        winner: str | None = None,
        rating_1_to_5: int | None = None,
        minutes: float | None = None,
        notes: str | None = None,
        topic_fit_ok: bool | None = None,
        latex_ok: bool | None = None,
        broken: bool | None = None,
        left: dict[str, Any] | None = None,
        right: dict[str, Any] | None = None,
        skip: bool = False,
    ) -> dict[str, Any]:
        pending_meta = self._state.get("pending")
        pending = self._load_pending_item()
        if pending is None:
            raise ValueError("No pending item to rate — call next first")
        if pending.get("mode") == "pair" or pending.get("pair_id"):
            return self._submit_pair(
                pending,
                pending_meta=pending_meta,
                pair_id=pair_id,
                winner=winner,
                minutes=minutes,
                notes=notes,
                left=left,
                right=right,
                skip=skip,
            )
        return self._submit_single(
            pending,
            pending_meta=pending_meta,
            rating_id=rating_id,
            rating_1_to_5=rating_1_to_5,
            minutes=minutes,
            notes=notes,
            topic_fit_ok=topic_fit_ok,
            latex_ok=latex_ok,
            broken=broken,
            skip=skip,
        )

    def _clear_pending(self) -> None:
        self._state["pending"] = None
        pending_path = self.dir / "pending.json"
        if pending_path.is_file():
            pending_path.unlink()
        self._save_state()

    def _model_submit_payload(self, extra: dict[str, Any]) -> dict[str, Any]:
        train = self.train_ratings()
        model = refit_from_ratings(train)
        status = model.status_for(None)
        extra.update(
            {
                "ok": True,
                "coverage": self.coverage(),
                "model_ready": status.model_ready,
                "n_train": status.n_train,
                "n_pairs": status.n_pairs,
                "min_train": status.min_train,
                "min_pairs": status.min_pairs,
                "model_message": status.message,
            }
        )
        return extra

    def _submit_single(
        self,
        item: dict[str, Any],
        *,
        pending_meta: Any,
        rating_id: str | None,
        rating_1_to_5: int | None,
        minutes: float | None,
        notes: str | None,
        topic_fit_ok: bool | None,
        latex_ok: bool | None,
        broken: bool | None,
        skip: bool,
    ) -> dict[str, Any]:
        if rating_id and item.get("rating_id") != rating_id:
            raise ValueError(
                f"rating_id mismatch: pending={item.get('rating_id')} got={rating_id}"
            )
        if not skip:
            if rating_1_to_5 is None:
                raise ValueError("rating_1_to_5 required unless skip=true")
            score = int(rating_1_to_5)
            if score < 1 or score > 5:
                raise ValueError("rating_1_to_5 must be 1–5")
        else:
            score = None

        out = dict(item)
        out.update(
            {
                "rating_1_to_5": score,
                "minutes": minutes,
                "notes": notes,
                "topic_fit_ok": topic_fit_ok,
                "latex_ok": latex_ok,
                "broken": broken,
                "skipped": bool(skip),
                "rated_at": _utc_now(),
                "engine_rev": out.get("engine_rev") or _engine_rev(),
            }
        )
        if "skeleton_features" not in out:
            out["skeleton_features"] = extract_skeleton_features(out)
        with self.ratings_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(out, ensure_ascii=False) + "\n")
        self._state["last_rated_id"] = out["rating_id"]
        self._clear_pending()
        return self._model_submit_payload(
            {"rating_id": out["rating_id"], "pending_was": pending_meta}
        )

    def _submit_pair(
        self,
        pending: dict[str, Any],
        *,
        pending_meta: Any,
        pair_id: str | None,
        winner: str | None,
        minutes: float | None,
        notes: str | None,
        left: dict[str, Any] | None,
        right: dict[str, Any] | None,
        skip: bool,
    ) -> dict[str, Any]:
        left_item = dict(pending.get("left") or {})
        right_item = dict(pending.get("right") or {})
        if not left_item or not right_item:
            raise ValueError("Pending pair is missing left/right items")
        pending_pid = pending.get("pair_id")
        if pair_id and pending_pid and pair_id != pending_pid:
            raise ValueError(f"pair_id mismatch: pending={pending_pid} got={pair_id}")
        _apply_side_flags(left_item, left or {})
        _apply_side_flags(right_item, right or {})
        win = None if skip else str(winner or "").strip().lower()
        if not skip:
            if win not in {"a", "b", "tie"}:
                raise ValueError("winner must be a, b, or tie unless skip=true")
        record = {
            "record_kind": "pair",
            "pair_id": pending_pid,
            "left": left_item,
            "right": right_item,
            "winner": win,
            "minutes": minutes,
            "notes": notes,
            "skipped": bool(skip),
            "rated_at": _utc_now(),
            "engine_rev": pending.get("engine_rev") or _engine_rev(),
            "session": self.session_name,
            "campaign": self.campaign_id,
            "generators": [left_item.get("generator"), right_item.get("generator")],
            "form_ids": [_form_id_of(left_item), _form_id_of(right_item)],
            "type_ids": [left_item.get("type_id"), right_item.get("type_id")],
        }
        with self.ratings_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        self._state["last_rated_id"] = pending_pid
        self._clear_pending()
        return self._model_submit_payload(
            {"pair_id": pending_pid, "winner": win, "pending_was": pending_meta}
        )


class SkeletonDerivCampaign(MultiTypeCampaign):
    """Backward-compatible subset: calc_diff_* skeleton-path types."""

    campaign_id = SKELETON_DERIV_CAMPAIGN
    pick_by_generator = True

    def __init__(
        self,
        *,
        session: str | None = None,
        root: Path | None = None,
        type_ids: tuple[str, ...] | list[str] | None = None,
        mix_seeds: bool = True,
    ) -> None:
        super().__init__(
            session=session,
            root=root,
            type_ids=tuple(type_ids or SKELETON_DERIV_TYPE_IDS),
            campaign=SKELETON_DERIV_CAMPAIGN,
            mix_seeds=mix_seeds,
        )


def open_live_session(
    type_id: str | None = None,
    *,
    session: str | None = None,
    campaign: str | None = None,
    root: Path | None = None,
) -> LiveRatingSession | MultiTypeCampaign:
    """Factory: all-topics / skeleton-deriv campaign or single-type session."""
    camp = (campaign or "").strip().lower()
    tid = (type_id or "").strip()
    if camp in {ALL_TOPICS_CAMPAIGN, "all", "global"} or tid in {
        ALL_TOPICS_CAMPAIGN,
        "__all_topics__",
    }:
        return MultiTypeCampaign(session=session, root=root, campaign=ALL_TOPICS_CAMPAIGN)
    if camp in {SKELETON_DERIV_CAMPAIGN, "skeleton", "deriv_skeleton"} or tid in {
        SKELETON_DERIV_CAMPAIGN,
        "__skeleton_deriv__",
    }:
        return SkeletonDerivCampaign(session=session, root=root)
    if not tid:
        return MultiTypeCampaign(session=session, root=root, campaign=ALL_TOPICS_CAMPAIGN)
    return LiveRatingSession(tid, session=session, root=root)


def list_types(*, ready_only: bool = True, include_scaffolds: bool = False) -> list[dict[str, Any]]:
    return list_continuous_difficulty_types(
        ready_only=ready_only,
        include_scaffolds=include_scaffolds,
    )


__all__ = [
    "ALL_TOPICS_CAMPAIGN",
    "DIFFICULTY_GRID",
    "LIVE_ROOT",
    "MIN_PAIRS",
    "MIN_TRAIN",
    "SKELETON_DERIV_CAMPAIGN",
    "SKELETON_DERIV_TYPE_IDS",
    "LiveRatingSession",
    "MultiTypeCampaign",
    "SkeletonDerivCampaign",
    "all_ready_type_ids",
    "attach_model_prediction",
    "bin_counts_from_ratings",
    "generator_counts_from_ratings",
    "generator_key_for_type",
    "has_continuous_difficulty",
    "iter_rated_item_views",
    "list_types",
    "nearest_grid_bin",
    "open_live_session",
    "pick_active_pair_slots",
    "pick_active_single_slot",
    "pick_next_difficulty",
    "pick_next_type_and_difficulty",
    "plan_active_shortlist",
    "quality_form_weights_from_model",
    "ratings_for_engine_rev",
    "rotate_ratings_if_engine_changed",
    "type_counts_from_ratings",
]
