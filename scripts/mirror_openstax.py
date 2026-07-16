"""Mirror OpenStax book pages to local HTML (MathML preserved).

Discovers page slugs from embedded TOC JSON on any book page, then
politely downloads each page under textbooks/openstax/html/<book-slug>/.

Usage:
  $env:PYTHONPATH='.'
  python scripts/mirror_openstax.py --book calculus-volume-1 --chapter 2
  python scripts/mirror_openstax.py --book calculus-volume-1 --chapter 2 --dry-run
  python scripts/mirror_openstax.py --book elementary-algebra-2e
  python scripts/mirror_openstax.py --book calculus-volume-1 --pages 2-4-continuity,2-key-concepts

OpenStax content is CC BY-NC-SA. Keep textbooks/ out of git; cite the
canonical URL when mining. Be polite: default wait is 1.0s between requests.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "textbooks" / "openstax" / "html"
USER_AGENT = "PolynomialLocalMirror/1.0 (+local research; polite crawl)"

PAGE_SLUG_RE = re.compile(
    r'"slug"\s*:\s*"('
    r"(?:\d+-\d+-[a-z0-9-]+)"  # numbered sections: 2-4-continuity
    r"|(?:\d+-introduction(?:-[a-z0-9-]*)?)"  # 2-introduction, 1-introduction-to-functions
    r"|(?:\d+-key-(?:terms|equations|concepts))"
    r"|(?:\d+-review-exercises)"
    r"|(?:preface)"
    r"|(?:answer-key)"
    r"|(?:index)"
    r')"',
)


def fetch_text(url: str, timeout: float = 45.0) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, errors="replace")


def book_page_url(book: str, slug: str) -> str:
    return f"https://openstax.org/books/{book}/pages/{slug}"


def discover_slugs(book: str, seed_slug: str = "1-introduction") -> list[str]:
    """Pull unique content page slugs from TOC JSON embedded in a book page."""
    seeds = [seed_slug]
    for alt in ("1-introduction", "preface", "1-introduction-to-functions"):
        if alt not in seeds:
            seeds.append(alt)
    html = None
    last_err: Exception | None = None
    for seed in seeds:
        try:
            html = fetch_text(book_page_url(book, seed))
            break
        except Exception as e:
            last_err = e
            continue
    if html is None:
        raise RuntimeError(f"Could not fetch TOC seed for {book}: {last_err}")
    found = set(PAGE_SLUG_RE.findall(html))
    return sorted(found, key=_slug_sort_key)


def _slug_sort_key(slug: str) -> tuple:
    parts = slug.split("-")
    chapter = int(parts[0]) if parts and parts[0].isdigit() else 999
    if slug.endswith("-introduction") or (len(parts) == 2 and parts[1] == "introduction"):
        return (chapter, 0, 0, slug)
    if len(parts) >= 2 and parts[1].isdigit():
        return (chapter, 1, int(parts[1]), slug)
    # review block after sections
    review_order = {
        "key-terms": 91,
        "key-equations": 92,
        "key-concepts": 93,
        "review-exercises": 94,
    }
    for name, order in review_order.items():
        if slug == f"{chapter}-{name}" or slug.endswith(f"-{name}"):
            return (chapter, 2, order, slug)
    return (chapter, 3, 0, slug)


def filter_chapter(slugs: list[str], chapter: int) -> list[str]:
    prefix = f"{chapter}-"
    return [s for s in slugs if s.startswith(prefix)]


def mirror_pages(
    book: str,
    slugs: list[str],
    out_dir: Path,
    *,
    wait: float,
    dry_run: bool,
    force: bool,
) -> list[dict]:
    book_dir = out_dir / book
    book_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict] = []
    for i, slug in enumerate(slugs):
        url = book_page_url(book, slug)
        dest = book_dir / f"{slug}.html"
        row = {
            "slug": slug,
            "url": url,
            "path": str(dest.relative_to(ROOT)).replace("\\", "/"),
            "status": "pending",
            "bytes": 0,
            "fetched_at": None,
        }
        if dest.exists() and not force:
            row["status"] = "skipped_exists"
            row["bytes"] = dest.stat().st_size
            results.append(row)
            print(f"[{i + 1}/{len(slugs)}] skip {slug} (exists)")
            continue
        if dry_run:
            row["status"] = "dry_run"
            results.append(row)
            print(f"[{i + 1}/{len(slugs)}] dry-run {url}")
            continue
        try:
            if i > 0 and wait > 0:
                time.sleep(wait)
            html = fetch_text(url)
            dest.write_text(html, encoding="utf-8")
            row["status"] = "fetched"
            row["bytes"] = len(html.encode("utf-8"))
            row["fetched_at"] = datetime.now(timezone.utc).isoformat()
            has_math = "<math" in html.lower()
            print(
                f"[{i + 1}/{len(slugs)}] ok {slug} "
                f"({row['bytes']} bytes, mathml={has_math})"
            )
        except urllib.error.HTTPError as e:
            row["status"] = f"http_{e.code}"
            print(f"[{i + 1}/{len(slugs)}] FAIL {slug}: HTTP {e.code}", file=sys.stderr)
        except Exception as e:
            row["status"] = f"error:{type(e).__name__}"
            print(f"[{i + 1}/{len(slugs)}] FAIL {slug}: {e}", file=sys.stderr)
        results.append(row)
    return results


def write_manifest(book_dir: Path, book: str, results: list[dict], chapter: int | None) -> Path:
    path = book_dir / "manifest.json"
    prev: dict = {}
    if path.exists():
        try:
            prev = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            prev = {}
    pages = {p["slug"]: p for p in prev.get("pages", [])}
    for row in results:
        pages[row["slug"]] = row
    payload = {
        "book": book,
        "base_url": f"https://openstax.org/books/{book}/pages/",
        "license": "CC BY-NC-SA (OpenStax)",
        "attribution": f"Access for free at https://openstax.org/books/{book}/pages/1-introduction",
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "last_run": {
            "chapter": chapter,
            "page_count": len(results),
            "fetched": sum(1 for r in results if r["status"] == "fetched"),
            "skipped": sum(1 for r in results if r["status"] == "skipped_exists"),
        },
        "pages": sorted(pages.values(), key=lambda p: _slug_sort_key(p["slug"])),
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument(
        "--book",
        required=True,
        help="OpenStax book slug, e.g. calculus-volume-1, elementary-algebra-2e",
    )
    p.add_argument(
        "--chapter",
        type=int,
        default=None,
        help="Only mirror pages for this chapter number (e.g. 2)",
    )
    p.add_argument(
        "--pages",
        default=None,
        help="Comma-separated page slugs (skips TOC discovery filter)",
    )
    p.add_argument(
        "--seed",
        default="1-introduction",
        help="Seed page used to discover TOC slugs (default: 1-introduction)",
    )
    p.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help=f"Output root (default: {DEFAULT_OUT})",
    )
    p.add_argument("--wait", type=float, default=1.0, help="Seconds between fetches (default: 1.0)")
    p.add_argument("--dry-run", action="store_true", help="List URLs only; do not write HTML")
    p.add_argument("--force", action="store_true", help="Re-download even if file exists")
    p.add_argument(
        "--list-only",
        action="store_true",
        help="Discover and print slugs, then exit",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    book = args.book.strip().strip("/")

    if args.pages:
        slugs = [s.strip() for s in args.pages.split(",") if s.strip()]
    else:
        print(f"Discovering TOC from {book_page_url(book, args.seed)} …")
        try:
            slugs = discover_slugs(book, args.seed)
        except Exception as e:
            print(f"Failed to discover TOC: {e}", file=sys.stderr)
            return 1
        print(f"Found {len(slugs)} page slugs in book TOC")
        if args.chapter is not None:
            slugs = filter_chapter(slugs, args.chapter)
            print(f"Chapter {args.chapter}: {len(slugs)} pages")

    if not slugs:
        print("No pages to mirror.", file=sys.stderr)
        return 1

    if args.list_only:
        for s in slugs:
            print(f"  {s}\t{book_page_url(book, s)}")
        return 0

    results = mirror_pages(
        book,
        slugs,
        args.out,
        wait=args.wait,
        dry_run=args.dry_run,
        force=args.force,
    )
    if not args.dry_run:
        manifest = write_manifest(args.out / book, book, results, args.chapter)
        print(f"Wrote {manifest.relative_to(ROOT)}")
    fetched = sum(1 for r in results if r["status"] == "fetched")
    skipped = sum(1 for r in results if r["status"] == "skipped_exists")
    failed = sum(1 for r in results if r["status"] not in {"fetched", "skipped_exists", "dry_run"})
    print(f"Done: fetched={fetched} skipped={skipped} failed={failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
