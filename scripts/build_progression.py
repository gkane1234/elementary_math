"""Build cross-section progression graphs from mirrored OpenStax HTML + Grade 6 curriculum.

Usage:
  $env:PYTHONPATH='.'
  python scripts/build_progression.py --books calculus-volume-1
  python scripts/build_progression.py --preset g6-prealg-alg1
  python scripts/build_progression.py --preset calculus
  python scripts/build_progression.py --preset full
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.example_mining.progression import (  # noqa: E402
    build_book_progression,
    build_foundations_progression,
    build_geometry_progression,
    build_grade_6_progression,
    build_progression_output,
    progression_to_markdown,
)
from scripts.example_mining.prerequisite_loader import (  # noqa: E402
    build_prerequisite_edges,
    load_prerequisite_map,
)

DEFAULT_HTML_ROOT = ROOT / "textbooks" / "openstax" / "html"
DEFAULT_OUT = ROOT / "scripts" / "output" / "example_mining" / "progression"

BOOK_DISPLAY = {
    "foundations_math": "Foundations Math",
    "grade_6_math": "Grade 6 Math",
    "geometry": "Geometry",
    "prealgebra-2e": "Pre-Algebra (OpenStax Prealgebra 2e)",
    "elementary-algebra-2e": "Algebra 1 (OpenStax Elementary Algebra 2e)",
    "intermediate-algebra-2e": "Algebra 2 (OpenStax Intermediate Algebra 2e)",
    "precalculus-2e": "Precalculus (OpenStax Precalculus 2e)",
    "calculus-volume-1": "Calculus I (OpenStax Calculus Vol. 1)",
    "calculus-volume-2": "Calculus II (OpenStax Calculus Vol. 2)",
    "calculus-volume-3": "Calculus III (OpenStax Calculus Vol. 3)",
}

PRESETS = {
    "g6-prealg-alg1": ["grade_6_math", "prealgebra-2e", "elementary-algebra-2e"],
    "calculus": ["calculus-volume-1", "calculus-volume-2", "calculus-volume-3"],
    "full": [
        "foundations_math",
        "grade_6_math",
        "prealgebra-2e",
        "elementary-algebra-2e",
        "geometry",
        "intermediate-algebra-2e",
        "precalculus-2e",
        "calculus-volume-1",
        "calculus-volume-2",
        "calculus-volume-3",
    ],
}


def _load_book(book: str, html_root: Path):
    if book == "foundations_math":
        print(f"Building progression for {book} (curriculum units) …")
        return build_foundations_progression()
    if book == "grade_6_math":
        print(f"Building progression for {book} (curriculum units) …")
        return build_grade_6_progression()
    if book == "geometry":
        print(f"Building progression for {book} (curriculum units) …")
        return build_geometry_progression()
    if not (html_root / book).is_dir():
        print(f"Skip missing mirror: {book}", file=sys.stderr)
        return None
    print(f"Building progression for {book} …")
    return build_book_progression(book, BOOK_DISPLAY.get(book, book), html_root)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--books", default=None, help="Comma-separated book/course slugs")
    p.add_argument("--preset", choices=sorted(PRESETS), default=None)
    p.add_argument("--html-root", type=Path, default=DEFAULT_HTML_ROOT)
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    p.add_argument("--name", default=None, help="Output basename (default derived)")
    args = p.parse_args(argv)

    if args.books:
        books = [b.strip() for b in args.books.split(",") if b.strip()]
    elif args.preset:
        books = PRESETS[args.preset]
    else:
        print("Provide --books or --preset", file=sys.stderr)
        return 1

    progs = []
    for book in books:
        prog = _load_book(book, args.html_root)
        if prog is not None:
            progs.append(prog)

    if not progs:
        print("No books processed.", file=sys.stderr)
        return 1

    args.out.mkdir(parents=True, exist_ok=True)
    basename = args.name or (args.preset or "_".join(b.replace("-", "") for b in books))

    output = build_progression_output(progs)
    maps = {book: load_prerequisite_map(book) for book in books}
    maps = {k: v for k, v in maps.items() if v}
    prereq_edges, prereq_reasons = build_prerequisite_edges(maps)

    json_path = args.out / f"{basename}.json"
    md_path = args.out / f"{basename}.md"
    json_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(
        progression_to_markdown(progs, prereq_edges, prereq_reasons, maps),
        encoding="utf-8",
    )

    if output["validation_warnings"]:
        print("Prerequisite validation warnings:", file=sys.stderr)
        for w in output["validation_warnings"]:
            print(f"  - {w}", file=sys.stderr)

    total_nodes = sum(len(pr["nodes"]) for pr in output["books"])
    print(f"Books: {len(progs)}  Sections/units: {total_nodes}")
    print(f"Prerequisite edges: {len(output['prerequisite_edges'])}")
    print(f"Reading-order edges: {len(output['reading_order_edges'])}")
    print(f"Wrote {md_path.relative_to(ROOT)}")
    print(f"Wrote {json_path.relative_to(ROOT)}")

    # Keep the topic-picker index in sync when building the full spine.
    if args.preset == "full" or "foundations_math" in books:
        from scripts.export_prerequisite_browser import main as export_browser

        export_code = export_browser()
        if export_code != 0:
            return export_code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
