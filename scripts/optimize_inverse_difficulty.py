"""Inverse difficulty pilot: g(target_effort) → θ* via forward model search.

Usage:
  $env:PYTHONPATH='.'
  python scripts/optimize_inverse_difficulty.py \\
    --model scripts/output/ml/forward_effort_model.json \\
    --type-id g6_introduction_to_ratios
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from question_engine.ml.forward import ForwardEffortModel
from question_engine.ml.inverse import optimize_difficulty_ladder, optimize_theta


DEFAULT_TARGETS = [2.0, 5.0, 8.0, 12.0, 16.0, 20.0]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--model",
        type=Path,
        default=ROOT / "scripts" / "output" / "ml" / "forward_effort_model.json",
    )
    parser.add_argument("--type-id", default="g6_introduction_to_ratios")
    parser.add_argument("--target", type=float, default=None, help="Single target effort")
    parser.add_argument(
        "--targets",
        type=float,
        nargs="*",
        default=None,
        help="Effort ladder targets",
    )
    parser.add_argument("--n-candidates", type=int, default=200)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "scripts" / "output" / "ml" / "inverse_difficulty.json",
    )
    args = parser.parse_args()

    model = ForwardEffortModel.load(args.model)
    if args.target is not None:
        targets = [float(args.target)]
        results = [
            optimize_theta(
                model,
                args.type_id,
                float(args.target),
                n_candidates=int(args.n_candidates),
                seed=int(args.seed),
                vary_extra_bounds=False,
            )
        ]
    else:
        targets = [float(t) for t in (args.targets or DEFAULT_TARGETS)]
        results = optimize_difficulty_ladder(
            model,
            args.type_id,
            targets,
            n_candidates=int(args.n_candidates),
            seed=int(args.seed),
        )

    payload = {
        "type_id": args.type_id,
        "model_kind": model.model_kind,
        "model_metrics": model.metrics,
        "targets": targets,
        "results": [
            {
                "target_effort": r.target_effort,
                "predicted_effort": r.predicted_effort,
                "abs_error": r.abs_error,
                "theta": r.theta,
                "suggested_difficulty": r.theta.get("difficulty"),
            }
            for r in results
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
