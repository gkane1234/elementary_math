"""Stage 1: extract inspectable question inventories from local OpenStax HTML.

Usage:
  $env:PYTHONPATH='.'
  python scripts/mine_openstax_section.py --book calculus-volume-1 --slugs 2-1-a-preview-of-calculus,2-2-the-limit-of-a-function,2-3-the-limit-laws
  python scripts/mine_openstax_section.py --book calculus-volume-1 --chapter 2 --sections 1-3
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.example_mining.openstax_html_parse import (  # noqa: E402
    inventory_to_markdown,
    parse_section_html,
)

DEFAULT_HTML_ROOT = ROOT / "textbooks" / "openstax" / "html"
DEFAULT_OUT = ROOT / "scripts" / "output" / "example_mining"


def resolve_slugs(book_dir: Path, chapter: int, sections: str) -> list[str]:
    """Map --sections 1-3 to slug files like 2-1-..., 2-2-..., 2-3-..."""
    m = re.fullmatch(r"(\d+)\s*-\s*(\d+)", sections.strip())
    if not m:
        raise ValueError("--sections must look like 1-3")
    lo, hi = int(m.group(1)), int(m.group(2))
    if lo > hi:
        lo, hi = hi, lo
    wanted = set(range(lo, hi + 1))
    found: list[tuple[int, str]] = []
    for path in sorted(book_dir.glob(f"{chapter}-*.html")):
        slug = path.stem
        parts = slug.split("-")
        # N-M-title
        if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
            sec = int(parts[1])
            if sec in wanted:
                found.append((sec, slug))
    found.sort()
    return [s for _, s in found]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--book", required=True, help="OpenStax book slug, e.g. calculus-volume-1")
    p.add_argument("--slugs", default=None, help="Comma-separated page slugs")
    p.add_argument("--chapter", type=int, default=None, help="Chapter number (with --sections)")
    p.add_argument("--sections", default=None, help="Section range like 1-3 (requires --chapter)")
    p.add_argument("--html-root", type=Path, default=DEFAULT_HTML_ROOT)
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = p.parse_args(argv)

    book_dir = args.html_root / args.book
    if not book_dir.is_dir():
        print(f"Missing mirrored book: {book_dir}", file=sys.stderr)
        return 1

    if args.slugs:
        slugs = [s.strip() for s in args.slugs.split(",") if s.strip()]
    elif args.chapter is not None and args.sections:
        slugs = resolve_slugs(book_dir, args.chapter, args.sections)
    else:
        print("Provide --slugs or both --chapter and --sections", file=sys.stderr)
        return 1

    if not slugs:
        print("No matching section HTML files found.", file=sys.stderr)
        return 1

    out_dir = args.out / args.book / "stage1"
    out_dir.mkdir(parents=True, exist_ok=True)

    index_rows: list[dict] = []
    for slug in slugs:
        path = book_dir / f"{slug}.html"
        if not path.exists():
            print(f"MISSING {path}", file=sys.stderr)
            continue
        print(f"Extracting {slug} …")
        inv = parse_section_html(path, book=args.book, slug=slug)
        json_path = out_dir / f"{slug}.json"
        md_path = out_dir / f"{slug}.md"
        json_path.write_text(json.dumps(inv.to_dict(), indent=2) + "\n", encoding="utf-8")
        md_path.write_text(inventory_to_markdown(inv), encoding="utf-8")
        counts: dict[str, int] = {}
        for it in inv.items:
            counts[it.kind] = counts.get(it.kind, 0) + 1
        index_rows.append(
            {
                "slug": slug,
                "title": inv.title,
                "items": len(inv.items),
                "counts": counts,
                "json": str(json_path.relative_to(ROOT)).replace("\\", "/"),
                "md": str(md_path.relative_to(ROOT)).replace("\\", "/"),
            }
        )
        print(f"  -> {len(inv.items)} items; wrote {md_path.relative_to(ROOT)}")

    index_path = out_dir / "INDEX.md"
    lines = [
        f"# Stage 1 inventories — `{args.book}`",
        "",
        "Inspect these markdown files before Stage 2 (family tagging / EMH).",
        "",
        "| Section | Items | Breakdown | Markdown |",
        "|---------|------:|-----------|----------|",
    ]
    for row in index_rows:
        breakdown = ", ".join(f"{k}={v}" for k, v in sorted(row["counts"].items()))
        lines.append(
            f"| `{row['slug']}` | {row['items']} | {breakdown} | [{row['slug']}.md]({Path(row['md']).name}) |"
        )
    lines.append("")
    lines.append("## What to check")
    lines.append("")
    lines.append("1. Are examples / checkpoints / section exercises classified correctly?")
    lines.append("2. Is the prompt text readable (math roughly intact as `$...$`)?")
    lines.append("3. Are learning objectives present?")
    lines.append("4. Anything duplicated, empty, or clearly truncated?")
    lines.append("")
    index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {index_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
