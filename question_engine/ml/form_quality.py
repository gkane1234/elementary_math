"""Topic-fit scores for catalog forms, separate from effort.

A 1–5 rating is centered on 3 and stored per topic, form, and difficulty band.
Generate-time sampling reads a shrunk score, ``sum / (count + 4)``, and passes
it to ``select_form_id`` as ``live_quality_form_weights``. Effort labels are
not read and are not written here.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

SHRINK_PRIOR = 4
_BANDS = ("low", "mid", "high")


def difficulty_band(difficulty: float) -> str:
    """Bands match the edit cap: under 6, 6–12, and 12 and above."""
    d = float(difficulty)
    if d < 6:
        return "low"
    if d < 12:
        return "mid"
    return "high"


def default_store_path() -> Path:
    raw = os.environ.get("FORM_QUALITY_PATH")
    if raw:
        return Path(raw)
    return Path("scripts/output/ml/form_quality/scores.json")


def _key(type_id: str, form_id: str, band: str) -> str:
    return f"{type_id}|{form_id}|{band}"


def _empty() -> dict[str, Any]:
    return {"version": 1, "rows": {}}


class FormQualityStore:
    """JSON store of topic-fit counts. One file, one row per form and band."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = Path(path) if path is not None else default_store_path()

    def load(self) -> dict[str, Any]:
        if not self.path.is_file():
            return _empty()
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return _empty()
        if not isinstance(data, dict) or not isinstance(data.get("rows"), dict):
            return _empty()
        return data

    def _save(self, data: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def record(
        self,
        *,
        type_id: str,
        form_id: str,
        difficulty: float,
        rating_1_to_5: int,
    ) -> dict[str, Any]:
        """Add one topic-fit rating. ``rating_1_to_5`` is centered on 3."""
        score = int(rating_1_to_5)
        if score < 1 or score > 5:
            raise ValueError("rating_1_to_5 must be 1–5")
        form = str(form_id or "").strip()
        topic = str(type_id or "").strip()
        if not form or not topic:
            raise ValueError("type_id and form_id are required")
        band = difficulty_band(difficulty)
        data = self.load()
        row = data["rows"].get(_key(topic, form, band)) or {
            "type_id": topic,
            "form_id": form,
            "band": band,
            "count": 0,
            "centered_sum": 0.0,
        }
        row["count"] = int(row["count"]) + 1
        row["centered_sum"] = float(row["centered_sum"]) + (score - 3)
        data["rows"][_key(topic, form, band)] = row
        self._save(data)
        return row

    def weights(self, type_id: str, difficulty: float) -> dict[str, float]:
        """Shrunk topic-fit scores for forms in this topic and difficulty band."""
        band = difficulty_band(difficulty)
        topic = str(type_id or "").strip()
        out: dict[str, float] = {}
        for row in self.load()["rows"].values():
            if not isinstance(row, dict):
                continue
            if row.get("type_id") != topic or row.get("band") != band:
                continue
            form = str(row.get("form_id") or "")
            count = int(row.get("count") or 0)
            if not form or count <= 0:
                continue
            centered = float(row.get("centered_sum") or 0.0)
            out[form] = centered / (count + SHRINK_PRIOR)
        return out


def record_from_rated_item(item: dict[str, Any], store: FormQualityStore | None = None) -> dict[str, Any] | None:
    """Record a 1–5 topic-fit rating from a live-rating item. Skip items with no form."""
    rating = item.get("rating_1_to_5")
    if rating is None:
        return None
    requested = item.get("theta_requested") if isinstance(item.get("theta_requested"), dict) else {}
    meta = item.get("metadata") if isinstance(item.get("metadata"), dict) else {}
    feats = item.get("skeleton_features") if isinstance(item.get("skeleton_features"), dict) else {}
    type_id = str(requested.get("type_id") or item.get("topic") or item.get("type_id") or "")
    form_id = str(feats.get("form_id") or meta.get("form_id") or item.get("form_id") or "")
    if not type_id or not form_id:
        return None
    difficulty = requested.get("conceptual_difficulty", requested.get("difficulty", item.get("difficulty", 6)))
    try:
        d = float(difficulty)
    except (TypeError, ValueError):
        d = 6.0
    return (store or FormQualityStore()).record(
        type_id=type_id,
        form_id=form_id,
        difficulty=d,
        rating_1_to_5=int(rating),
    )
