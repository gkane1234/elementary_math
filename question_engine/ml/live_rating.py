"""Live adaptive human-rating loop (v1): stratified continuous-D sampling.

Policy (v1 — no GP / BO / multi-knob uncertainty):
  - Space-filling on a fixed continuous-difficulty grid (same anchors as
    ``scripts/build_hand_rating_set.py``).
  - Prefer under-sampled D bins; mix seeds at the chosen D.
  - Append-only JSONL ratings + session state under
    ``scripts/output/ml/ratings/live/<session>/``.

v2 stubs (not implemented): uncertainty sampling, inverse human model, pairwise.
"""

from __future__ import annotations

import json
import os
import subprocess
import time
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from question_engine.api.handler import _generate_for_type
from question_engine.ml.effort import has_effort_scorer, score_effort
from question_engine.ml.knob_introspect import (
    has_continuous_difficulty,
    list_continuous_difficulty_types,
)
from question_engine.ml.schema import build_generation_record

ROOT = Path(__file__).resolve().parents[2]
LIVE_ROOT = ROOT / "scripts" / "output" / "ml" / "ratings" / "live"

# Same stratified grid as build_hand_rating_set.py.
DIFFICULTY_GRID: tuple[float, ...] = (0.0, 3.0, 6.0, 8.0, 12.0, 16.0, 20.0, 25.0)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _engine_rev() -> str | None:
    env = os.environ.get("POLY_ENGINE_REV") or os.environ.get("GIT_COMMIT")
    if env:
        return env.strip()
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(ROOT),
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=3,
        )
        return out.strip() or None
    except Exception:  # noqa: BLE001
        return None


def nearest_grid_bin(difficulty: float, grid: tuple[float, ...] = DIFFICULTY_GRID) -> float:
    """Map a continuous D to the nearest stratified grid anchor."""
    return min(grid, key=lambda g: abs(g - float(difficulty)))


def bin_counts_from_ratings(
    ratings: list[dict[str, Any]],
    *,
    grid: tuple[float, ...] = DIFFICULTY_GRID,
) -> dict[float, int]:
    counts: Counter[float] = Counter({d: 0 for d in grid})
    for row in ratings:
        if row.get("rating_1_to_5") is None and row.get("skipped"):
            continue
        raw = row.get("theta_requested", {}).get("difficulty")
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
    for row in ratings:
        raw = row.get("theta_requested", {}).get("difficulty")
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
            "policy": "stratified_continuous_d_v1",
            "v2_note": "Uncertainty BO / multi-knob introspection deferred.",
        }

    def _save_state(self) -> None:
        self._state["type_id"] = self.type_id
        self._state["session"] = self.session_name
        self._state["updated_at"] = _utc_now()
        self.state_path.write_text(
            json.dumps(self._state, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def load_ratings(self) -> list[dict[str, Any]]:
        if not self.ratings_path.is_file():
            return []
        rows: list[dict[str, Any]] = []
        for line in self.ratings_path.read_text(encoding="utf-8").splitlines():
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

    def coverage(self) -> dict[str, Any]:
        ratings = self.load_ratings()
        counts = bin_counts_from_ratings(ratings)
        return {
            "type_id": self.type_id,
            "session": self.session_name,
            "n_ratings": len(ratings),
            "by_difficulty": {str(k): v for k, v in sorted(counts.items())},
            "pending": self._state.get("pending"),
            "dir": str(self.dir),
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
        """Generate the next item (stratified D unless difficulty overridden)."""
        ratings = self.load_ratings()
        theta_d = (
            float(difficulty)
            if difficulty is not None
            else pick_next_difficulty(ratings)
        )
        use_seed = int(seed) if seed is not None else self._next_seed(theta_d)
        settings = {
            "difficulty": theta_d,
            "count": 1,
            "include_answer_key": True,
            "seed": use_seed,
        }
        t0 = time.perf_counter()
        questions = _generate_for_type(self.type_id, settings)
        elapsed_ms = int((time.perf_counter() - t0) * 1000)
        question = questions[0]
        gen_settings = (question.metadata or {}).get("generation_settings") or settings

        y_effort = None
        y_mode = None
        effort_feats: dict[str, Any] = {}
        prompt = (question.prompt_latex or question.prompt_text or "").strip()
        answer = (question.answer_latex or question.answer_text or "").strip()
        if has_effort_scorer(self.type_id):
            y_effort, effort_feats = score_effort(self.type_id, prompt, answer)
            if isinstance(effort_feats, dict):
                raw_mode = effort_feats.get("form") or effort_feats.get("mode")
                y_mode = str(raw_mode) if raw_mode is not None else None

        record = build_generation_record(
            self.type_id,
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
        rating_id = f"live_{self.session_name}_{uuid.uuid4().hex[:12]}"
        item = {
            **row,
            "rating_id": rating_id,
            "generator": generator,
            "theta_requested": {
                "difficulty": theta_d,
                "seed": use_seed,
                "count": 1,
            },
            "theta_full": row.get("theta_full") or {},
            "bin": nearest_grid_bin(theta_d),
            "engine_rev": _engine_rev(),
            "generated_at": _utc_now(),
            "generate_ms": elapsed_ms,
            "session": self.session_name,
            # Human fields null until submit.
            "rating_1_to_5": None,
            "minutes": None,
            "notes": None,
            "topic_fit_ok": None,
            "latex_ok": None,
            "broken": None,
            "rated_at": None,
        }
        self._state["pending"] = {
            "rating_id": rating_id,
            "type_id": self.type_id,
            "difficulty": theta_d,
            "bin": nearest_grid_bin(theta_d),
            "seed": use_seed,
            "generated_at": item["generated_at"],
        }
        # Keep a compact pending payload for submit linking (full item on disk).
        pending_path = self.dir / "pending.json"
        pending_path.write_text(
            json.dumps(item, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        self._save_state()
        return item

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
        rating_1_to_5: int | None = None,
        minutes: float | None = None,
        notes: str | None = None,
        topic_fit_ok: bool | None = None,
        latex_ok: bool | None = None,
        broken: bool | None = None,
        skip: bool = False,
    ) -> dict[str, Any]:
        """Append a rating for the pending (or matching) item."""
        pending_meta = self._state.get("pending")
        item = self._load_pending_item()
        if item is None:
            raise ValueError("No pending item to rate — call next first")
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

        self._state["pending"] = None
        self._state["last_rated_id"] = out["rating_id"]
        self._save_state()
        pending_path = self.dir / "pending.json"
        if pending_path.is_file():
            pending_path.unlink()
        return {
            "ok": True,
            "rating_id": out["rating_id"],
            "coverage": self.coverage(),
            "pending_was": pending_meta,
        }


def list_types(*, ready_only: bool = True, include_scaffolds: bool = False) -> list[dict[str, Any]]:
    return list_continuous_difficulty_types(
        ready_only=ready_only,
        include_scaffolds=include_scaffolds,
    )


__all__ = [
    "DIFFICULTY_GRID",
    "LIVE_ROOT",
    "LiveRatingSession",
    "bin_counts_from_ratings",
    "has_continuous_difficulty",
    "list_types",
    "nearest_grid_bin",
    "pick_next_difficulty",
]
