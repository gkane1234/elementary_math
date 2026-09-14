"""Live rating ← Bayesian linear utility on skeleton features.

Cold start: ``model_ready`` is false until at least ``MIN_PAIRS`` pairwise
comparisons **or** ``MIN_TRAIN`` absolute 1–5 ratings. Predictions then come
from a Bayesian linear utility (ridge is the MAP) with posterior mean + std.

Primary signal is pairwise Bradley–Terry / Thurstone:
``P(A ≻ B) = σ(u(A) − u(B))``. Absolute 1–5 ratings remain optional / legacy.

Primary features are expr_skeleton inventory / ``cost_spend`` — not Spec
densify cost pads.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

import numpy as np

# Absolute 1–5: enough signal for a tiny Bayesian linear before surfacing.
MIN_TRAIN: int = 20
# Pairwise is the primary label: fewer comparisons identify a ranking.
MIN_PAIRS: int = 8
# Observation noise for absolute ratings on the 1–5 scale.
_OBS_VAR: float = 1.0
# Intercept prior mean (mid-scale) so pair-only utilities stay on 1–5-ish.
_INTERCEPT_PRIOR_MEAN: float = 3.0
_INTERCEPT_PRIOR_PREC: float = 0.25
# Tie pairs pull u(A) ≈ u(B) instead of a Bernoulli 0.5 that ignores them.
_TIE_PREC: float = 0.5
_NEWTON_MAX_ITER: int = 25
_SCORE_CLIP: float = 4.0

# Feature hashing width for categoricals (form_id, kind, pattern, type_id, …).
_HASH_DIM: int = 64

_FN_CLASSES: tuple[str, ...] = (
    "algebraic",
    "trig",
    "exp",
    "log",
    "roots",
    "invtrig",
    "hyperbolic",
)

_METHODS: tuple[str, ...] = (
    "power",
    "product",
    "quotient",
    "chain",
    "sum",
)


def _safe_float(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, (list, tuple, set, frozenset)):
        return list(value)
    return [value]


def _stable_hash_bucket(token: str, dim: int = _HASH_DIM) -> int:
    """Deterministic bucket (not Python's salted hash)."""
    h = 2166136261
    for ch in token.encode("utf-8"):
        h ^= ch
        h = (h * 16777619) & 0xFFFFFFFF
    return int(h % dim)


def extract_skeleton_features(row: Mapping[str, Any]) -> dict[str, Any]:
    """Pull a compact feature dict from a live-rating / generation row."""
    meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
    structural = (
        row.get("structural_features")
        if isinstance(row.get("structural_features"), dict)
        else {}
    )
    theta = row.get("theta_full") if isinstance(row.get("theta_full"), dict) else {}
    spend = (
        row.get("cost_spend")
        or meta.get("cost_spend")
        or structural.get("cost_spend")
        or {}
    )
    if not isinstance(spend, dict):
        spend = {}
    richness = (
        row.get("richness_knobs")
        or meta.get("richness_knobs")
        or structural.get("richness_knobs")
        or {}
    )
    if not isinstance(richness, dict):
        richness = {}

    def _pick(*keys: str, default: Any = None) -> Any:
        for key in keys:
            for src in (row, meta, structural, theta, spend, richness):
                if isinstance(src, Mapping) and key in src and src[key] is not None:
                    return src[key]
        return default

    form_id = _pick("form_id", "core_form_id", "openstax_form", default="")
    classes = _as_list(_pick("function_classes", default=[]))
    methods = _as_list(_pick("methods_used", default=[]))
    generator = _pick("generator", default="") or row.get("generator") or ""

    feats: dict[str, Any] = {
        "type_id": str(row.get("type_id") or _pick("type_id", default="") or ""),
        "generator": str(generator or ""),
        "catalog_id": str(_pick("catalog_id", default="") or ""),
        "strategy": str(_pick("strategy", default="") or ""),
        "form_id": str(form_id or ""),
        "skeleton_kind": str(_pick("skeleton_kind", default="") or ""),
        "skeleton_pattern": str(_pick("skeleton_pattern", default="") or ""),
        "skeleton_source": str(_pick("skeleton_source", default="") or ""),
        "richness_band": str(_pick("richness_band", default="") or ""),
        "inner_kind": str(
            _pick("inner_kind", default=None) or spend.get("inner_kind") or ""
        ),
        "shared_vs_independent": str(spend.get("shared_vs_independent") or ""),
        "difficulty": _safe_float(
            _pick(
                "conceptual_difficulty",
                "difficulty",
                "d_spend",
                "effective_d",
                default=0.0,
            )
        ),
        "conceptual_difficulty": _safe_float(
            _pick("conceptual_difficulty", "difficulty", "d_spend", default=0.0)
        ),
        "derivative_order": _safe_float(_pick("derivative_order", default=1.0), 1.0),
        "chain_depth": _safe_float(
            _pick("chain_depth", default=None) or spend.get("chain_depth"), 0.0
        ),
        "nest_budget": _safe_float(spend.get("nest_budget", richness.get("nest_budget"))),
        "nest_depth_expr": _safe_float(
            spend.get("nest_depth_expr", _pick("nest_depth", default=0.0))
        ),
        "degree_max": _safe_float(
            spend.get("degree_max", _pick("degree_max", default=0.0))
        ),
        "n_applies": _safe_float(spend.get("n_applies")),
        "n_terms": _safe_float(spend.get("n_terms", _pick("n_terms", default=0.0))),
        "n_factors": _safe_float(
            spend.get("n_factors", _pick("n_factors", default=0.0))
        ),
        "inner_degree": _safe_float(spend.get("inner_degree")),
        "shared_inner": 1.0
        if bool(_pick("shared_inner", default=False))
        else 0.0,
        "function_classes": sorted(str(c) for c in classes),
        "methods_used": sorted(str(m) for m in methods),
    }
    return feats


def _numeric_vector(feats: Mapping[str, Any]) -> list[float]:
    return [
        _safe_float(feats.get("difficulty")),
        _safe_float(feats.get("conceptual_difficulty")),
        _safe_float(feats.get("derivative_order"), 1.0),
        _safe_float(feats.get("chain_depth")),
        _safe_float(feats.get("nest_budget")),
        _safe_float(feats.get("nest_depth_expr")),
        _safe_float(feats.get("degree_max")),
        _safe_float(feats.get("n_applies")),
        _safe_float(feats.get("n_terms")),
        _safe_float(feats.get("n_factors")),
        _safe_float(feats.get("inner_degree")),
        _safe_float(feats.get("shared_inner")),
        *[
            1.0 if c in set(feats.get("function_classes") or []) else 0.0
            for c in _FN_CLASSES
        ],
        *[
            1.0 if m in set(feats.get("methods_used") or []) else 0.0
            for m in _METHODS
        ],
    ]


NUMERIC_FEATURE_NAMES: tuple[str, ...] = (
    "difficulty",
    "conceptual_difficulty",
    "derivative_order",
    "chain_depth",
    "nest_budget",
    "nest_depth_expr",
    "degree_max",
    "n_applies",
    "n_terms",
    "n_factors",
    "inner_degree",
    "shared_inner",
    *[f"fn_{c}" for c in _FN_CLASSES],
    *[f"method_{m}" for m in _METHODS],
)


def _categorical_tokens(feats: Mapping[str, Any]) -> list[str]:
    tokens: list[str] = []
    for key in (
        "generator",
        "form_id",
        "catalog_id",
        "strategy",
        "type_id",
        "skeleton_kind",
        "skeleton_pattern",
        "richness_band",
        "inner_kind",
        "shared_vs_independent",
        "skeleton_source",
    ):
        val = str(feats.get(key) or "").strip()
        if val:
            tokens.append(f"{key}={val}")
    return tokens


def _hashed_categorical_vector(feats: Mapping[str, Any], dim: int = _HASH_DIM) -> list[float]:
    vec = [0.0] * dim
    for token in _categorical_tokens(feats):
        vec[_stable_hash_bucket(token, dim)] += 1.0
    return vec


def row_feature_vector(row: Mapping[str, Any]) -> list[float]:
    feats = extract_skeleton_features(row)
    return _numeric_vector(feats) + _hashed_categorical_vector(feats)


def is_pair_record(row: Mapping[str, Any]) -> bool:
    if row.get("record_kind") == "pair":
        return True
    return bool(
        row.get("pair_id")
        and isinstance(row.get("left"), Mapping)
        and isinstance(row.get("right"), Mapping)
    )


def is_trainable_rating(row: Mapping[str, Any]) -> bool:
    if is_pair_record(row):
        return False
    if row.get("skipped"):
        return False
    if row.get("broken") is True:
        return False
    score = row.get("rating_1_to_5")
    try:
        n = int(score)
    except (TypeError, ValueError):
        return False
    return 1 <= n <= 5


def is_trainable_pair(row: Mapping[str, Any]) -> bool:
    """Pairwise label usable for BT training (neither side broken/skipped)."""
    if not is_pair_record(row):
        return False
    if row.get("skipped"):
        return False
    winner = str(row.get("winner") or "").strip().lower()
    if winner not in {"a", "b", "tie"}:
        return False
    left = row.get("left") if isinstance(row.get("left"), Mapping) else None
    right = row.get("right") if isinstance(row.get("right"), Mapping) else None
    if left is None or right is None:
        return False
    if left.get("broken") is True or right.get("broken") is True:
        return False
    if left.get("skipped") or right.get("skipped"):
        return False
    return True


def pair_sides(row: Mapping[str, Any]) -> tuple[Mapping[str, Any], Mapping[str, Any]] | None:
    if not is_pair_record(row):
        return None
    left = row.get("left")
    right = row.get("right")
    if isinstance(left, Mapping) and isinstance(right, Mapping):
        return left, right
    return None


@dataclass
class RatingModelStatus:
    model_ready: bool
    n_train: int
    n_pairs: int = 0
    min_train: int = MIN_TRAIN
    min_pairs: int = MIN_PAIRS
    predicted_rating: float | None = None
    predicted_std: float | None = None
    message: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "model_ready": self.model_ready,
            "n_train": self.n_train,
            "n_pairs": self.n_pairs,
            "min_train": self.min_train,
            "min_pairs": self.min_pairs,
            "predicted_rating": self.predicted_rating,
            "predicted_std": self.predicted_std,
            "message": self.message,
        }


def _sigmoid(z: np.ndarray | float) -> np.ndarray | float:
    z_arr = np.asarray(z, dtype=float)
    out = np.empty_like(z_arr, dtype=float)
    pos = z_arr >= 0
    out[pos] = 1.0 / (1.0 + np.exp(-z_arr[pos]))
    ez = np.exp(z_arr[~pos])
    out[~pos] = ez / (1.0 + ez)
    if np.isscalar(z):
        return float(out)
    return out


def _standardize_stats(X: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mean = X.mean(axis=0)
    scale = X.std(axis=0)
    scale = np.where(scale < 1e-8, 1.0, scale)
    return mean, scale


def _phi_rows(X: np.ndarray, mean: np.ndarray, scale: np.ndarray) -> np.ndarray:
    xs = (X - mean) / scale
    return np.hstack([np.ones((xs.shape[0], 1)), xs])


def _phi_one(x: np.ndarray, mean: np.ndarray, scale: np.ndarray) -> np.ndarray:
    return np.concatenate([[1.0], (x - mean) / scale])


def _prior_precision(dim: int, alpha: float) -> np.ndarray:
    prec = np.eye(dim) * float(alpha)
    prec[0, 0] = float(_INTERCEPT_PRIOR_PREC)
    return prec


def _prior_mean(dim: int) -> np.ndarray:
    mu = np.zeros(dim)
    mu[0] = float(_INTERCEPT_PRIOR_MEAN)
    return mu


@dataclass
class SkeletonRatingRegressor:
    """Bayesian linear utility: absolute 1–5 + Bradley–Terry pairs.

    Ridge MAP is the posterior mode; we keep the Laplace / Gaussian posterior
    so each item has ``mean`` and ``std``. Pairwise is the primary likelihood.
    """

    min_train: int = MIN_TRAIN
    min_pairs: int = MIN_PAIRS
    alpha: float = 2.0
    n_train: int = 0
    n_pairs: int = 0
    model_ready: bool = False
    coef_: np.ndarray | None = None
    intercept_: float = 0.0
    mean_: np.ndarray | None = None
    scale_: np.ndarray | None = None
    cov_: np.ndarray | None = None
    mu_: np.ndarray | None = None
    feature_dim: int = 0
    last_metrics: dict[str, float] = field(default_factory=dict)

    def fit(self, rows: list[Mapping[str, Any]]) -> "SkeletonRatingRegressor":
        abs_rows = [r for r in rows if is_trainable_rating(r)]
        pair_rows = [r for r in rows if is_trainable_pair(r)]
        self.n_train = len(abs_rows)
        self.n_pairs = len(pair_rows)
        self.model_ready = (
            self.n_pairs >= int(self.min_pairs) or self.n_train >= int(self.min_train)
        )
        self.coef_ = None
        self.intercept_ = 0.0
        self.mean_ = None
        self.scale_ = None
        self.cov_ = None
        self.mu_ = None
        self.last_metrics = {
            "n_train": float(self.n_train),
            "n_pairs": float(self.n_pairs),
        }
        if not self.model_ready:
            return self

        feat_rows: list[Mapping[str, Any]] = list(abs_rows)
        for pr in pair_rows:
            sides = pair_sides(pr)
            if sides is not None:
                feat_rows.extend(sides)
        if not feat_rows:
            self.model_ready = False
            return self

        X_all = np.asarray([row_feature_vector(r) for r in feat_rows], dtype=float)
        self.feature_dim = int(X_all.shape[1])
        mean, scale = _standardize_stats(X_all)
        self.mean_ = mean
        self.scale_ = scale

        X_abs = (
            np.asarray([row_feature_vector(r) for r in abs_rows], dtype=float)
            if abs_rows
            else np.zeros((0, self.feature_dim))
        )
        y_abs = (
            np.asarray([float(int(r["rating_1_to_5"])) for r in abs_rows], dtype=float)
            if abs_rows
            else np.zeros(0)
        )
        deltas: list[np.ndarray] = []
        signs: list[float] = []
        tie_deltas: list[np.ndarray] = []
        for pr in pair_rows:
            sides = pair_sides(pr)
            if sides is None:
                continue
            xa = np.asarray(row_feature_vector(sides[0]), dtype=float)
            xb = np.asarray(row_feature_vector(sides[1]), dtype=float)
            phi_a = _phi_one(xa, mean, scale)
            phi_b = _phi_one(xb, mean, scale)
            delta = phi_a - phi_b
            winner = str(pr.get("winner") or "").strip().lower()
            if winner == "tie":
                tie_deltas.append(delta)
            elif winner == "a":
                deltas.append(delta)
                signs.append(1.0)
            elif winner == "b":
                deltas.append(delta)
                signs.append(-1.0)

        if pair_rows:
            mu, cov = self._fit_joint_newton(
                X_abs, y_abs, deltas, signs, tie_deltas, mean, scale
            )
        else:
            mu, cov = self._fit_abs_closed_form(X_abs, y_abs, mean, scale)

        self.mu_ = mu
        self.cov_ = cov
        self.intercept_ = float(mu[0])
        self.coef_ = mu[1:]
        if abs_rows:
            phi = _phi_rows(X_abs, mean, scale)
            pred = phi @ mu
            resid = y_abs - pred
            self.last_metrics["rmse"] = float(np.sqrt(np.mean(resid**2)))
            self.last_metrics["mae"] = float(np.mean(np.abs(resid)))
        return self

    def _fit_abs_closed_form(
        self,
        X: np.ndarray,
        y: np.ndarray,
        mean: np.ndarray,
        scale: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        phi = _phi_rows(X, mean, scale)
        dim = phi.shape[1]
        prec = _prior_precision(dim, self.alpha)
        mu0 = _prior_mean(dim)
        # Posterior: (ΦᵀΦ / σ² + P₀) μ = Φᵀy / σ² + P₀ μ₀
        a = (phi.T @ phi) / float(_OBS_VAR) + prec
        b = (phi.T @ y) / float(_OBS_VAR) + prec @ mu0
        mu = np.linalg.solve(a, b)
        cov = np.linalg.inv(a)
        cov = 0.5 * (cov + cov.T)
        return mu, cov

    def _fit_joint_newton(
        self,
        X_abs: np.ndarray,
        y_abs: np.ndarray,
        deltas: list[np.ndarray],
        signs: list[float],
        tie_deltas: list[np.ndarray],
        mean: np.ndarray,
        scale: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        if X_abs.shape[0]:
            dim = X_abs.shape[1] + 1
            phi_abs = _phi_rows(X_abs, mean, scale)
        elif deltas:
            dim = int(deltas[0].shape[0])
            phi_abs = np.zeros((0, dim))
        elif tie_deltas:
            dim = int(tie_deltas[0].shape[0])
            phi_abs = np.zeros((0, dim))
        else:
            dim = int(self.feature_dim) + 1
            phi_abs = np.zeros((0, dim))

        prec = _prior_precision(dim, self.alpha)
        mu0 = _prior_mean(dim)
        w = mu0.copy()
        if X_abs.shape[0]:
            # Warm start from absolute closed form when present.
            try:
                w, _ = self._fit_abs_closed_form(X_abs, y_abs, mean, scale)
            except np.linalg.LinAlgError:
                w = mu0.copy()

        d_mat = np.asarray(deltas, dtype=float) if deltas else np.zeros((0, dim))
        s_vec = np.asarray(signs, dtype=float) if signs else np.zeros(0)
        t_mat = np.asarray(tie_deltas, dtype=float) if tie_deltas else np.zeros((0, dim))

        for _ in range(_NEWTON_MAX_ITER):
            g = prec @ (w - mu0)
            h = prec.copy()
            if phi_abs.shape[0]:
                resid = phi_abs @ w - y_abs
                g = g + (phi_abs.T @ resid) / float(_OBS_VAR)
                h = h + (phi_abs.T @ phi_abs) / float(_OBS_VAR)
            if d_mat.shape[0]:
                z = s_vec * (d_mat @ w)
                p = np.asarray(_sigmoid(z), dtype=float)
                # NLL grad for -log σ(s Δ·w): (σ(z) - 1) * s Δ
                g = g + d_mat.T @ ((p - 1.0) * s_vec)
                weights = p * (1.0 - p)
                h = h + d_mat.T @ (d_mat * weights[:, None])
            if t_mat.shape[0]:
                tu = t_mat @ w
                g = g + float(_TIE_PREC) * (t_mat.T @ tu)
                h = h + float(_TIE_PREC) * (t_mat.T @ t_mat)
            h = 0.5 * (h + h.T)
            try:
                step = np.linalg.solve(h, g)
            except np.linalg.LinAlgError:
                h = h + 1e-4 * np.eye(dim)
                step = np.linalg.solve(h, g)
            w = w - step
            if float(np.max(np.abs(step))) < 1e-6:
                break

        try:
            cov = np.linalg.inv(h)
        except np.linalg.LinAlgError:
            cov = np.linalg.pinv(h)
        cov = 0.5 * (cov + cov.T)
        # Jitter if a diagonal went non-positive from numerics.
        diag = np.diag(cov)
        if np.any(diag <= 0):
            cov = cov + (1e-6 - np.minimum(diag, 0.0)).min() * np.eye(dim)
        return w, cov

    def predict_mean_std(self, row: Mapping[str, Any]) -> tuple[float, float] | None:
        if (
            not self.model_ready
            or self.mu_ is None
            or self.cov_ is None
            or self.mean_ is None
            or self.scale_ is None
        ):
            return None
        x = np.asarray(row_feature_vector(row), dtype=float)
        if x.shape[0] != self.feature_dim:
            return None
        phi = _phi_one(x, self.mean_, self.scale_)
        mean = float(phi @ self.mu_)
        var = float(phi @ self.cov_ @ phi)
        std = float(np.sqrt(max(var, 1e-12)))
        return mean, std

    def predict_one(self, row: Mapping[str, Any]) -> float | None:
        pred = self.predict_mean_std(row)
        if pred is None:
            return None
        # Clamp to rating scale for display; model is still linear underneath.
        return float(min(5.0, max(1.0, pred[0])))

    def thompson_weights(self, rng: np.random.Generator | None = None) -> np.ndarray | None:
        if not self.model_ready or self.mu_ is None or self.cov_ is None:
            return None
        gen = rng if rng is not None else np.random.default_rng()
        cov = self.cov_ + 1e-8 * np.eye(self.cov_.shape[0])
        try:
            return gen.multivariate_normal(self.mu_, cov)
        except np.linalg.LinAlgError:
            return self.mu_.copy()

    def utility_with_weights(
        self, row: Mapping[str, Any], weights: np.ndarray
    ) -> float | None:
        if self.mean_ is None or self.scale_ is None:
            return None
        x = np.asarray(row_feature_vector(row), dtype=float)
        if x.shape[0] != self.feature_dim:
            return None
        phi = _phi_one(x, self.mean_, self.scale_)
        if phi.shape[0] != weights.shape[0]:
            return None
        return float(phi @ weights)

    def categorical_quality_scores(
        self,
        rows: list[Mapping[str, Any]],
        key: str = "form_id",
        *,
        thompson: bool = False,
        rng: np.random.Generator | None = None,
    ) -> dict[str, float]:
        """Centered posterior (or Thompson) utility per categorical value.

        Used to reweight ``form_id`` / ``generator`` at generate time. Unseen
        keys stay at 0 after centering so they keep the catalog D-weight.
        """
        if not self.model_ready:
            return {}
        draw = self.thompson_weights(rng) if thompson else None
        buckets: dict[str, list[float]] = {}
        for row in rows:
            feats = extract_skeleton_features(row)
            token = str(feats.get(key) or "").strip()
            if not token:
                continue
            if draw is not None:
                u = self.utility_with_weights(row, draw)
            else:
                pred = self.predict_mean_std(row)
                u = pred[0] if pred is not None else None
            if u is None:
                continue
            buckets.setdefault(token, []).append(float(u))
        if not buckets:
            return {}
        means = {k: float(sum(v) / len(v)) for k, v in buckets.items()}
        center = float(sum(means.values()) / len(means))
        return {k: max(-_SCORE_CLIP, min(_SCORE_CLIP, v - center)) for k, v in means.items()}

    def status_for(self, row: Mapping[str, Any] | None = None) -> RatingModelStatus:
        if not self.model_ready:
            msg = (
                f"Cold start: n/a until {self.min_pairs} pairs or "
                f"{self.min_train} absolute ratings "
                f"(have n_pairs={self.n_pairs}, n_train={self.n_train})."
            )
            return RatingModelStatus(
                model_ready=False,
                n_train=self.n_train,
                n_pairs=self.n_pairs,
                min_train=self.min_train,
                min_pairs=self.min_pairs,
                predicted_rating=None,
                predicted_std=None,
                message=msg,
            )
        pred = self.predict_mean_std(row) if row is not None else None
        rating = float(min(5.0, max(1.0, pred[0]))) if pred is not None else None
        std = float(pred[1]) if pred is not None else None
        return RatingModelStatus(
            model_ready=True,
            n_train=self.n_train,
            n_pairs=self.n_pairs,
            min_train=self.min_train,
            min_pairs=self.min_pairs,
            predicted_rating=rating,
            predicted_std=std,
            message=(
                f"Bayesian utility on {self.n_train} abs + {self.n_pairs} pairs."
            ),
        )


def refit_from_ratings(
    rows: list[Mapping[str, Any]],
    *,
    min_train: int = MIN_TRAIN,
    min_pairs: int = MIN_PAIRS,
    alpha: float = 2.0,
) -> SkeletonRatingRegressor:
    return SkeletonRatingRegressor(
        min_train=min_train, min_pairs=min_pairs, alpha=alpha
    ).fit(rows)


# Public alias: the live model is Bayesian linear + BT, not ridge.
BayesianLinearUtility = SkeletonRatingRegressor


FEATURE_LIST_DOC: tuple[str, ...] = (
    *NUMERIC_FEATURE_NAMES,
    *[f"hash({k})" for k in (
        "generator",
        "form_id",
        "catalog_id",
        "strategy",
        "type_id",
        "skeleton_kind",
        "skeleton_pattern",
        "richness_band",
        "inner_kind",
        "shared_vs_independent",
        "skeleton_source",
    )],
)


__all__ = [
    "FEATURE_LIST_DOC",
    "MIN_PAIRS",
    "MIN_TRAIN",
    "NUMERIC_FEATURE_NAMES",
    "BayesianLinearUtility",
    "RatingModelStatus",
    "SkeletonRatingRegressor",
    "extract_skeleton_features",
    "is_pair_record",
    "is_trainable_pair",
    "is_trainable_rating",
    "pair_sides",
    "refit_from_ratings",
    "row_feature_vector",
]
