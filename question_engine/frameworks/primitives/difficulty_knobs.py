"""Load / reload continuous-difficulty knobs from ``difficulty_knobs.json``.

Single source of truth for lane thresholds, log scales, unlocks, and constructive
parameters. Edit the JSON by hand or via ``python scripts/difficulty_knobs_server.py``.
"""

from __future__ import annotations

import json
import threading
from copy import deepcopy
from pathlib import Path
from typing import Any

_KNOBS_PATH = Path(__file__).with_name("difficulty_knobs.json")
_lock = threading.RLock()
_cache: dict[str, Any] | None = None
_cache_mtime: float | None = None


def knobs_path() -> Path:
    return _KNOBS_PATH


def load_knobs(*, force: bool = False) -> dict[str, Any]:
    """Return the knob dict (cached). Re-reads when the file mtime changes."""
    global _cache, _cache_mtime
    with _lock:
        try:
            mtime = _KNOBS_PATH.stat().st_mtime
        except OSError:
            mtime = None
        if (
            _cache is not None
            and not force
            and mtime is not None
            and _cache_mtime is not None
            and mtime <= _cache_mtime
        ):
            return _cache
        raw = json.loads(_KNOBS_PATH.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise ValueError("difficulty_knobs.json must be a JSON object")
        _cache = raw
        _cache_mtime = mtime
        return _cache


def reload_knobs() -> dict[str, Any]:
    return load_knobs(force=True)


def save_knobs(data: dict[str, Any]) -> None:
    """Write knobs to disk and refresh cache (debug UI / tooling)."""
    global _cache, _cache_mtime
    with _lock:
        text = json.dumps(data, indent=2, sort_keys=False) + "\n"
        _KNOBS_PATH.write_text(text, encoding="utf-8")
        _cache = deepcopy(data)
        try:
            _cache_mtime = _KNOBS_PATH.stat().st_mtime
        except OSError:
            _cache_mtime = None


def knobs() -> dict[str, Any]:
    return load_knobs()


def section(name: str) -> dict[str, Any]:
    return dict(knobs().get(name) or {})


def fget(section_name: str, key: str, default: float) -> float:
    sec = knobs().get(section_name) or {}
    try:
        return float(sec.get(key, default))
    except (TypeError, ValueError):
        return float(default)


def iget(section_name: str, key: str, default: int) -> int:
    return int(fget(section_name, key, float(default)))


def number_lane_min_d(profile: str) -> float:
    sec = section("number_lanes")
    entry = sec.get(profile) or {}
    if isinstance(entry, dict) and "min_d" in entry:
        return float(entry["min_d"])
    # Fallback to historical defaults
    defaults = {
        "friendly_wholes": 0.0,
        "signed_small": 0.0,
        "unit_fractions": 3.0,
        "simple_rations": 4.0,
        "friendly_decimals": 4.0,
        "difficult_rations": 8.0,
        "awkward_decimals": 10.0,
    }
    return float(defaults.get(profile, 0.0))


def variable_lane_min_d(lane: str) -> float:
    sec = section("variable_lanes")
    entry = sec.get(lane) or {}
    if isinstance(entry, dict) and "min_d" in entry:
        return float(entry["min_d"])
    defaults = {
        "only_x": 0.0,
        "xyz": 3.0,
        "abctuvwxyz": 6.0,
        "whole_alphabet": 10.0,
        "greek": 12.0,
    }
    return float(defaults.get(lane, 0.0))


def all_number_lane_min_d() -> dict[str, float]:
    sec = section("number_lanes")
    out: dict[str, float] = {}
    for key, val in sec.items():
        if isinstance(val, dict) and "min_d" in val:
            out[key] = float(val["min_d"])
    return out


def all_variable_lane_min_d() -> dict[str, float]:
    sec = section("variable_lanes")
    out: dict[str, float] = {}
    for key, val in sec.items():
        if isinstance(val, dict) and "min_d" in val:
            out[key] = float(val["min_d"])
    return out


def flatten_knobs(data: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Flat list of editable numeric/bool knobs for the debug UI."""
    data = data if data is not None else knobs()
    rows: list[dict[str, Any]] = []

    def walk(prefix: str, obj: Any) -> None:
        if isinstance(obj, dict):
            if set(obj.keys()) <= {"min_d"} or (
                "min_d" in obj and all(k in {"min_d", "label"} for k in obj)
            ):
                rows.append(
                    {
                        "path": f"{prefix}.min_d" if prefix else "min_d",
                        "value": obj.get("min_d"),
                        "type": "number",
                    }
                )
                return
            for k, v in obj.items():
                if k.startswith("_"):
                    continue
                walk(f"{prefix}.{k}" if prefix else k, v)
        elif isinstance(obj, bool):
            rows.append({"path": prefix, "value": obj, "type": "bool"})
        elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
            rows.append({"path": prefix, "value": obj, "type": "number"})
        elif isinstance(obj, str):
            rows.append({"path": prefix, "value": obj, "type": "string"})
        elif isinstance(obj, list) and all(isinstance(x, str) for x in obj):
            rows.append({"path": prefix, "value": obj, "type": "string_list"})

    walk("", data)
    return rows


def apply_flat_updates(updates: dict[str, Any]) -> dict[str, Any]:
    """Apply ``{"a.b.c": value}`` paths onto a deep copy of knobs and save."""
    data = deepcopy(knobs())
    for path, value in updates.items():
        parts = [p for p in str(path).split(".") if p]
        if not parts:
            continue
        cur: Any = data
        for part in parts[:-1]:
            nxt = cur.get(part)
            if not isinstance(nxt, dict):
                cur[part] = {}
            cur = cur[part]
        cur[parts[-1]] = value
    save_knobs(data)
    return data
