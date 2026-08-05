"""Merge exported ratings into items; report + simple recalibration artifacts."""
from __future__ import annotations

import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from question_engine.ml.forward import ForwardEffortModel, train_forward_model
from question_engine.ml.schema import GenerationRecord

DIR = Path(__file__).resolve().parent
ITEMS = DIR / "items.jsonl"
RATINGS = DIR / "calc_derivatives_ratings.json"
FILLED = DIR / "ratings_filled.jsonl"
REPORT_JSON = DIR / "calibration_report.json"
REPORT_MD = DIR / "CALIBRATION.md"
LINEAR_JSON = DIR / "recalibration_linear.json"
FORWARD_JSON = DIR / "human_forward_effort_model.json"


def pearson(x: list[float], y: list[float]) -> float:
    if len(x) < 2:
        return float("nan")
    a = np.asarray(x, dtype=float)
    b = np.asarray(y, dtype=float)
    if a.std() < 1e-12 or b.std() < 1e-12:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def spearman(x: list[float], y: list[float]) -> float:
    if len(x) < 2:
        return float("nan")
    rx = np.argsort(np.argsort(np.asarray(x, dtype=float))).astype(float)
    ry = np.argsort(np.argsort(np.asarray(y, dtype=float))).astype(float)
    return pearson(rx.tolist(), ry.tolist())


def fit_linear(x: list[float], y: list[float]) -> dict[str, float]:
    """y ≈ a*x + b via least squares."""
    a_arr = np.asarray(x, dtype=float)
    b_arr = np.asarray(y, dtype=float)
    if len(a_arr) < 2 or a_arr.std() < 1e-12:
        return {"slope": 0.0, "intercept": float(b_arr.mean() if len(b_arr) else 0.0), "r": float("nan")}
    slope, intercept = np.polyfit(a_arr, b_arr, 1)
    pred = slope * a_arr + intercept
    ss_res = float(((b_arr - pred) ** 2).sum())
    ss_tot = float(((b_arr - b_arr.mean()) ** 2).sum())
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-12 else float("nan")
    return {
        "slope": float(slope),
        "intercept": float(intercept),
        "r": pearson(x, y),
        "r2": r2,
        "mae": float(np.mean(np.abs(b_arr - pred))),
    }


def row_to_record(row: dict[str, Any], y: float) -> GenerationRecord:
    return GenerationRecord(
        type_id=str(row.get("type_id") or ""),
        seed=int(row.get("seed") or 0),
        difficulty=float(row.get("difficulty") or 0.0),
        theta_full=dict(row.get("theta_full") or {}),
        prompt_latex=str(row.get("prompt_latex") or ""),
        prompt_text=str(row.get("prompt_text") or ""),
        answer_latex=str(row.get("answer_latex") or ""),
        answer_text=str(row.get("answer_text") or ""),
        structural_features=dict(row.get("structural_features") or {}),
        y_effort=float(y),
        metadata=dict(row.get("metadata") or {}),
    )


def main() -> None:
    ratings_raw = json.loads(RATINGS.read_text(encoding="utf-8"))
    # Support flat store or wrapped {ratings: ...}
    if isinstance(ratings_raw, dict) and "ratings" in ratings_raw and isinstance(
        ratings_raw["ratings"], dict
    ):
        store = ratings_raw["ratings"]
    else:
        store = ratings_raw

    items = [json.loads(line) for line in ITEMS.read_text(encoding="utf-8").splitlines() if line.strip()]
    item_ids = {r["rating_id"] for r in items}
    store_ids = set(store.keys())

    filled_rows: list[dict[str, Any]] = []
    rated_rows: list[dict[str, Any]] = []
    missing_in_store: list[str] = []
    orphan_ratings = sorted(store_ids - item_ids)

    for row in items:
        rid = row["rating_id"]
        human = store.get(rid)
        if not human:
            missing_in_store.append(rid)
            filled = dict(row)
        else:
            filled = dict(row)
            filled["rating_1_to_5"] = human.get("rating_1_to_5")
            filled["minutes"] = human.get("minutes")
            filled["notes"] = human.get("notes")
            filled["rated_at"] = human.get("rated_at")
        filled_rows.append(filled)
        if filled.get("rating_1_to_5") is not None:
            rated_rows.append(filled)

    with FILLED.open("w", encoding="utf-8") as fh:
        for r in filled_rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    hist = Counter(int(r["rating_1_to_5"]) for r in rated_rows)
    by_pack: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in rated_rows:
        by_pack[str(r.get("pack") or "?")].append(r)

    # Correlations
    h = [float(r["rating_1_to_5"]) for r in rated_rows]
    ye = [float(r["y_effort"]) for r in rated_rows if r.get("y_effort") is not None]
    # align ye with rated that have y_effort
    rated_with_ye = [r for r in rated_rows if r.get("y_effort") is not None]
    h_ye = [float(r["rating_1_to_5"]) for r in rated_with_ye]
    ye = [float(r["y_effort"]) for r in rated_with_ye]
    d = [float(r["difficulty"]) for r in rated_rows]
    h_d = [float(r["rating_1_to_5"]) for r in rated_rows]

    pack_stats = []
    for pack, rows in sorted(by_pack.items()):
        hh = [float(r["rating_1_to_5"]) for r in rows]
        yy = [float(r["y_effort"]) for r in rows if r.get("y_effort") is not None]
        hy = [float(r["rating_1_to_5"]) for r in rows if r.get("y_effort") is not None]
        dd = [float(r["difficulty"]) for r in rows]
        # residual: zscore(human) - zscore(y_effort) mean abs — disagreement
        disagree = float("nan")
        if len(hy) >= 3 and np.std(hy) > 1e-9 and np.std(yy) > 1e-9:
            zh = (np.asarray(hy) - np.mean(hy)) / np.std(hy)
            zy = (np.asarray(yy) - np.mean(yy)) / np.std(yy)
            disagree = float(np.mean(np.abs(zh - zy)))
        pack_stats.append(
            {
                "pack": pack,
                "n_rated": len(rows),
                "mean_rating": float(np.mean(hh)),
                "mean_y_effort": float(np.mean(yy)) if yy else None,
                "mean_difficulty": float(np.mean(dd)),
                "pearson_rating_vs_y_effort": pearson(hy, yy) if len(hy) >= 3 else None,
                "pearson_rating_vs_difficulty": pearson(hh, dd) if len(hh) >= 3 else None,
                "z_disagreement_vs_y_effort": disagree,
                "score_hist": dict(sorted(Counter(int(x) for x in hh).items())),
            }
        )
    pack_stats_sorted = sorted(
        pack_stats,
        key=lambda p: (
            -(p["z_disagreement_vs_y_effort"] if p["z_disagreement_vs_y_effort"] == p["z_disagreement_vs_y_effort"] else -1),
        ),
    )

    # Per-difficulty mean human rating
    by_d: dict[float, list[float]] = defaultdict(list)
    for r in rated_rows:
        by_d[float(r["difficulty"])].append(float(r["rating_1_to_5"]))
    difficulty_means = {
        str(k): {"n": len(v), "mean_rating": float(np.mean(v))} for k, v in sorted(by_d.items())
    }

    linear_rating_from_ye = fit_linear(ye, h_ye)
    linear_ye_from_rating = fit_linear(h_ye, ye)
    linear_rating_from_d = fit_linear(d, h_d)
    linear_d_from_rating = fit_linear(h_d, d)

    LINEAR_JSON.write_text(
        json.dumps(
            {
                "n_rated": len(rated_rows),
                "rating_from_y_effort": linear_rating_from_ye,
                "y_effort_from_rating": linear_ye_from_rating,
                "rating_from_difficulty": linear_rating_from_d,
                "difficulty_from_rating": linear_d_from_rating,
                "note": (
                    "Apply y_effort_from_rating to map human 1..5 → effort units, "
                    "or rating_from_y_effort to rescore rule effort onto the human scale."
                ),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    # Tiny forward model: predict human rating (scaled to ~effort via linear map)
    # Target = mapped effort so existing ForwardEffortModel API stays in effort units.
    forward_metrics: dict[str, Any] = {}
    if len(rated_with_ye) >= 40:
        slope = linear_ye_from_rating["slope"]
        intercept = linear_ye_from_rating["intercept"]
        records = []
        for r in rated_rows:
            human = float(r["rating_1_to_5"])
            y_target = slope * human + intercept
            records.append(row_to_record(r, y_target))
        try:
            model = train_forward_model(records, test_fraction=0.25, seed=0)
            model.save(FORWARD_JSON)
            forward_metrics = {
                "model_kind": model.model_kind,
                "metrics": model.metrics,
                "target": "linear_map(rating_1_to_5 → y_effort units)",
                "path": str(FORWARD_JSON),
            }
        except Exception as e:
            forward_metrics = {"error": str(e)}

    # Unrated / null coverage by pack
    null_by_pack: Counter[str] = Counter()
    for r in filled_rows:
        if r.get("rating_1_to_5") is None:
            null_by_pack[str(r.get("pack") or "?")] += 1

    report = {
        "source_ratings": str(RATINGS),
        "source_items": str(ITEMS),
        "filled_path": str(FILLED),
        "n_items": len(items),
        "n_store_keys": len(store),
        "n_rated": len(rated_rows),
        "n_unrated": len(items) - len(rated_rows),
        "coverage_pct": round(100.0 * len(rated_rows) / max(len(items), 1), 1),
        "score_hist": dict(sorted(hist.items())),
        "orphan_rating_ids": orphan_ratings[:20],
        "missing_from_store_count": len(missing_in_store),
        "visited_null_count": sum(
            1
            for rid, v in store.items()
            if isinstance(v, dict) and v.get("rating_1_to_5") is None and rid in item_ids
        ),
        "unrated_by_pack": dict(sorted(null_by_pack.items())),
        "pearson_rating_vs_y_effort": pearson(h_ye, ye),
        "spearman_rating_vs_y_effort": spearman(h_ye, ye),
        "pearson_rating_vs_difficulty": pearson(h_d, d),
        "spearman_rating_vs_difficulty": spearman(h_d, d),
        "difficulty_means": difficulty_means,
        "packs_most_disagree": pack_stats_sorted[:5],
        "packs_all": pack_stats_sorted,
        "linear_recalibration": {
            "rating_from_y_effort": linear_rating_from_ye,
            "y_effort_from_rating": linear_ye_from_rating,
        },
        "forward_model": forward_metrics,
    }
    REPORT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines = [
        "# Calc derivatives — calibration report",
        "",
        f"Recovered ratings from Cursor browser localStorage → `{RATINGS.name}`.",
        "",
        "## Coverage",
        "",
        f"- Items: **{len(items)}**",
        f"- Rated (1–5): **{len(rated_rows)}** ({report['coverage_pct']}%)",
        f"- Unrated / null: **{report['n_unrated']}**",
        f"- Score histogram: `{dict(sorted(hist.items()))}`",
        "",
        "Unrated by pack:",
        "",
    ]
    for pack, n in sorted(null_by_pack.items(), key=lambda kv: -kv[1]):
        lines.append(f"- `{pack}`: {n}")
    lines += [
        "",
        "## Human vs machine",
        "",
        f"- Pearson(rating, y_effort): **{report['pearson_rating_vs_y_effort']:.3f}**",
        f"- Spearman(rating, y_effort): **{report['spearman_rating_vs_y_effort']:.3f}**",
        f"- Pearson(rating, difficulty): **{report['pearson_rating_vs_difficulty']:.3f}**",
        f"- Spearman(rating, difficulty): **{report['spearman_rating_vs_difficulty']:.3f}**",
        "",
        "### Linear recalibration",
        "",
        f"- `rating ≈ {linear_rating_from_ye['slope']:.4f} * y_effort + {linear_rating_from_ye['intercept']:.4f}` "
        f"(r={linear_rating_from_ye['r']:.3f}, MAE={linear_rating_from_ye['mae']:.3f})",
        f"- `y_effort ≈ {linear_ye_from_rating['slope']:.4f} * rating + {linear_ye_from_rating['intercept']:.4f}` "
        f"(r={linear_ye_from_rating['r']:.3f})",
        "",
        f"Artifacts: `{LINEAR_JSON.name}`, filled rows `{FILLED.name}`.",
        "",
        "### Packs with most disagreement (z-score |human − y_effort|)",
        "",
    ]
    for p in pack_stats_sorted[:5]:
        lines.append(
            f"- **{p['pack']}** n={p['n_rated']} mean_rating={p['mean_rating']:.2f} "
            f"mean_y_effort={p['mean_y_effort']:.2f} "
            f"r(y_effort)={p['pearson_rating_vs_y_effort']} "
            f"z_disagree={p['z_disagreement_vs_y_effort']:.3f}"
            if p["z_disagreement_vs_y_effort"] == p["z_disagreement_vs_y_effort"]
            else f"- **{p['pack']}** n={p['n_rated']} (insufficient)"
        )
    if forward_metrics.get("metrics"):
        lines += [
            "",
            "### Tiny forward model (human→effort-mapped target)",
            "",
            f"- kind: `{forward_metrics.get('model_kind')}`",
            f"- metrics: `{forward_metrics.get('metrics')}`",
            f"- saved: `{FORWARD_JSON.name}`",
        ]
    lines += [
        "",
        "## Next steps",
        "",
        "1. **Finish the 68 nulls** — reopen `rater.html`, filter Unrated, export JSON to "
        f"`{RATINGS.name}` (or re-run extract from browser storage).",
        "2. **OpenStax rating pass** — use `COVERAGE.md` checklist; rate textbook-aligned forms "
        "the generator under-covers (especially packs that disagree most).",
        "3. **Expand campaigns** — build/rate `algebra_1`, `algebra_2`, `precalc_algebraic` "
        "with the same rater pipeline.",
        "4. **Apply recalibration** — use `y_effort_from_rating` to supervise effort scorers, "
        "or fold the human forward model into inverse-D pilots for calc derivative packs.",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"filled={FILLED} rated={len(rated_rows)}/{len(items)}")
    print(f"hist={dict(sorted(hist.items()))}")
    print(
        f"pearson ye={report['pearson_rating_vs_y_effort']:.3f} "
        f"d={report['pearson_rating_vs_difficulty']:.3f}"
    )
    print("top disagree packs:", [p["pack"] for p in pack_stats_sorted[:5]])
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
