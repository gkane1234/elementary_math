"""Train a forward effort model f(θ) → y_effort from GenerationRecord JSONL.

Usage:
  $env:PYTHONPATH='.'
  python scripts/train_forward_effort_model.py --data scripts/output/ml/g6_ratios.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from question_engine.ml.forward import train_forward_model
from question_engine.ml.schema import GenerationRecord


def load_records(path: Path) -> list[GenerationRecord]:
    records: list[GenerationRecord] = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if "error" in row:
                continue
            records.append(
                GenerationRecord(
                    type_id=row["type_id"],
                    seed=row.get("seed"),
                    difficulty=row.get("difficulty"),
                    theta_full=row.get("theta_full") or {},
                    prompt_latex=row.get("prompt_latex") or "",
                    prompt_text=row.get("prompt_text") or "",
                    answer_latex=row.get("answer_latex") or "",
                    answer_text=row.get("answer_text") or "",
                    structural_features=row.get("structural_features") or {},
                    y_effort=row.get("y_effort"),
                    y_mode=row.get("y_mode"),
                    effort_feats=row.get("effort_feats") or {},
                    qa_flags=row.get("qa_flags") or [],
                    metadata=row.get("metadata") or {},
                )
            )
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data",
        type=Path,
        default=ROOT / "scripts" / "output" / "ml" / "generation_dataset.jsonl",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "scripts" / "output" / "ml" / "forward_effort_model",
    )
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--no-gbr", action="store_true", help="Force ridge fallback")
    args = parser.parse_args()

    records = load_records(args.data)
    labeled = [r for r in records if r.y_effort is not None]
    print(f"loaded {len(records)} records, {len(labeled)} labeled")
    if len(labeled) < 8:
        print("Need at least 8 labeled records", file=sys.stderr)
        return 1

    model = train_forward_model(
        labeled,
        prefer_gbr=not args.no_gbr,
        seed=int(args.seed),
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    model.save(args.out)
    print(json.dumps({"model_kind": model.model_kind, "metrics": model.metrics}, indent=2))
    print(f"wrote {args.out.with_suffix('.json')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
