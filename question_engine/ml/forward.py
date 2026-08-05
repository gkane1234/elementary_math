"""Forward effort model: f(θ, type_id) → y_effort.

Prefers sklearn GradientBoostingRegressor when available; falls back to a
numpy ridge regressor so the pilot runs without optional deps.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

from .features import build_design_matrix, record_feature_dict
from .schema import GenerationRecord


def _try_sklearn_gbr(**kwargs: Any):
    try:
        from sklearn.ensemble import GradientBoostingRegressor

        return GradientBoostingRegressor(**kwargs)
    except ImportError:
        return None


@dataclass
class ForwardEffortModel:
    """Trained forward model with feature schema for save/load."""

    feature_names: list[str]
    model_kind: str
    estimator: Any = None
    ridge_coef: list[float] | None = None
    ridge_intercept: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)

    def predict_rows(self, X: list[list[float]]) -> list[float]:
        if not X:
            return []
        arr = np.asarray(X, dtype=float)
        if self.model_kind == "gbr" and self.estimator is not None:
            return [float(v) for v in self.estimator.predict(arr)]
        coef = np.asarray(self.ridge_coef or [0.0] * arr.shape[1], dtype=float)
        preds = arr @ coef + self.ridge_intercept
        return [float(v) for v in preds]

    def predict_records(self, records: list[GenerationRecord]) -> list[float | None]:
        X, _, _, kept = build_design_matrix(records, feature_names=self.feature_names)
        out: list[float | None] = [None] * len(records)
        if X:
            preds = self.predict_rows(X)
            for idx, pred in zip(kept, preds):
                out[idx] = pred
        name_index = {n: i for i, n in enumerate(self.feature_names)}
        for i, rec in enumerate(records):
            if out[i] is not None:
                continue
            feats = record_feature_dict(rec)
            row = [0.0] * len(self.feature_names)
            for key, val in feats.items():
                if isinstance(val, str) or key == "type_id":
                    col = f"{key}={val}"
                    if col in name_index:
                        row[name_index[col]] = 1.0
                elif key in name_index:
                    row[name_index[key]] = float(val)
            out[i] = self.predict_rows([row])[0]
        return out

    def to_dict(self) -> dict[str, Any]:
        return {
            "feature_names": self.feature_names,
            "model_kind": self.model_kind,
            "metrics": self.metrics,
            "ridge_coef": self.ridge_coef,
            "ridge_intercept": self.ridge_intercept,
        }

    def save(self, path: Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        meta_path = path.with_suffix(".json")
        meta_path.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")
        if self.model_kind == "gbr" and self.estimator is not None:
            import pickle

            with path.with_suffix(".pkl").open("wb") as fh:
                pickle.dump(self.estimator, fh)

    @classmethod
    def load(cls, path: Path) -> "ForwardEffortModel":
        path = Path(path)
        meta_path = path if path.suffix == ".json" else path.with_suffix(".json")
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        estimator = None
        if meta.get("model_kind") == "gbr":
            import pickle

            pkl = meta_path.with_suffix(".pkl")
            if pkl.exists():
                with pkl.open("rb") as fh:
                    estimator = pickle.load(fh)
        return cls(
            feature_names=list(meta["feature_names"]),
            model_kind=meta["model_kind"],
            estimator=estimator,
            ridge_coef=meta.get("ridge_coef"),
            ridge_intercept=float(meta.get("ridge_intercept") or 0.0),
            metrics=dict(meta.get("metrics") or {}),
        )


def _pearson(y_true: list[float], y_pred: list[float]) -> float:
    if len(y_true) < 2:
        return 0.0
    yt = np.asarray(y_true, dtype=float)
    yp = np.asarray(y_pred, dtype=float)
    yt = yt - yt.mean()
    yp = yp - yp.mean()
    denom = float(np.linalg.norm(yt) * np.linalg.norm(yp))
    if denom < 1e-12:
        return 0.0
    return float(np.dot(yt, yp) / denom)


def _rmse(y_true: list[float], y_pred: list[float]) -> float:
    if not y_true:
        return 0.0
    err = np.asarray(y_true, dtype=float) - np.asarray(y_pred, dtype=float)
    return float(math.sqrt(float(np.mean(err * err))))


def _fit_ridge(X: np.ndarray, y: np.ndarray, *, l2: float = 1.0) -> tuple[np.ndarray, float]:
    if X.size == 0:
        return np.zeros(0), float(y.mean()) if len(y) else 0.0
    x_mean = X.mean(axis=0)
    y_mean = float(y.mean())
    Xc = X - x_mean
    yc = y - y_mean
    n_features = X.shape[1]
    xtx = Xc.T @ Xc + l2 * np.eye(n_features)
    xty = Xc.T @ yc
    try:
        coef = np.linalg.solve(xtx, xty)
    except np.linalg.LinAlgError:
        coef = np.linalg.pinv(xtx) @ xty
    intercept = y_mean - float(x_mean @ coef)
    return coef, intercept


def train_forward_model(
    records: list[GenerationRecord],
    *,
    prefer_gbr: bool = True,
    test_fraction: float = 0.2,
    seed: int = 0,
    n_estimators: int = 120,
    max_depth: int = 3,
) -> ForwardEffortModel:
    """Train f(θ) → effort on labeled GenerationRecords."""
    X, y, names, _kept = build_design_matrix(records)
    if len(y) < 8:
        raise ValueError(f"Need at least 8 labeled records; got {len(y)}")

    rng = np.random.default_rng(seed)
    idx = np.arange(len(y))
    rng.shuffle(idx)
    n_test = max(1, int(round(len(y) * test_fraction)))
    test_idx = idx[:n_test]
    train_idx = idx[n_test:]
    if len(train_idx) < 4:
        train_idx = idx
        test_idx = idx[: max(1, len(idx) // 5)]

    X_arr = np.asarray(X, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    X_train, y_train = X_arr[train_idx], y_arr[train_idx]
    X_test, y_test = X_arr[test_idx], y_arr[test_idx]

    gbr = (
        _try_sklearn_gbr(
            n_estimators=n_estimators,
            max_depth=max_depth,
            learning_rate=0.08,
            random_state=seed,
        )
        if prefer_gbr
        else None
    )

    if gbr is not None:
        gbr.fit(X_train, y_train)
        pred_test = [float(v) for v in gbr.predict(X_test)]
        return ForwardEffortModel(
            feature_names=names,
            model_kind="gbr",
            estimator=gbr,
            metrics={
                "n_train": float(len(train_idx)),
                "n_test": float(len(test_idx)),
                "rmse": _rmse(list(y_test), pred_test),
                "pearson_r": _pearson(list(y_test), pred_test),
            },
        )

    coef, intercept = _fit_ridge(X_train, y_train, l2=1.0)
    pred_test = list(X_test @ coef + intercept)
    return ForwardEffortModel(
        feature_names=names,
        model_kind="ridge",
        ridge_coef=[float(c) for c in coef],
        ridge_intercept=float(intercept),
        metrics={
            "n_train": float(len(train_idx)),
            "n_test": float(len(test_idx)),
            "rmse": _rmse(list(y_test), pred_test),
            "pearson_r": _pearson(list(y_test), pred_test),
        },
    )
