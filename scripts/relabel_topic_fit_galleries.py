"""Batch-update topic_fit gallery titles/h1 (+ gallery.md #) with course prefixes.

Does not re-sample questions. Rebuilds INDEX.md via build_verified_topic_galleries
``--index-only``.

Usage:
  $env:PYTHONPATH='.'
  python scripts/relabel_topic_fit_galleries.py
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import question_engine.types  # noqa: F401
from question_engine.core.base import QUESTION_TYPES
from question_engine.topic_labels import format_topic_label

_naming_spec = importlib.util.spec_from_file_location(
    "topic_fit_naming",
    ROOT / "scripts" / "topic_fit_naming.py",
)
_naming_mod = importlib.util.module_from_spec(_naming_spec)
assert _naming_spec.loader is not None
_naming_spec.loader.exec_module(_naming_mod)
type_id_from_folder = _naming_mod.type_id_from_folder

TOPIC_FIT = ROOT / "scripts" / "output" / "topic_fit"
BY_TOPIC = TOPIC_FIT / "by_topic"

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.DOTALL)
H1_RE = re.compile(r"<h1>(.*?)</h1>", re.DOTALL)
MD_H1_RE = re.compile(r"^# .+$", re.MULTILINE)
MD_H2_TID_RE = re.compile(
    r"^## `([^`]+)` — (.+)$", re.MULTILINE
)


def _label_for(tid: str) -> str:
    qt = QUESTION_TYPES.get(tid)
    name = getattr(qt, "name", None) if qt else None
    return format_topic_label(tid, name)


def _relabel_html(path: Path, label: str) -> bool:
    text = path.read_text(encoding="utf-8")
    new = TITLE_RE.sub(f"<title>{label}</title>", text, count=1)
    new = H1_RE.sub(f"<h1>{label}</h1>", new, count=1)
    if new == text:
        return False
    path.write_text(new, encoding="utf-8")
    return True


def _relabel_md(path: Path, label: str) -> bool:
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    new, n = MD_H1_RE.subn(f"# {label}", text, count=1)
    if n == 0 or new == text:
        return False
    path.write_text(new, encoding="utf-8")
    return True


def _relabel_aggregate_md(path: Path) -> bool:
    """Rewrite ``## `type_id` — Name`` headings to ``## prefix: Name``."""
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")

    def repl(m: re.Match[str]) -> str:
        tid, _name = m.group(1), m.group(2)
        return f"## {_label_for(tid)}\n\n`{tid}`"

    new, n = MD_H2_TID_RE.subn(repl, text)
    # Also rewrite already-relabeled h2 that still need type_id line? skip.
    if n == 0:
        return False
    path.write_text(new, encoding="utf-8")
    return True


def _relabel_aggregate_html(path: Path) -> int:
    """Update h2 sections that still look like ``code — Name``."""
    if not path.is_file():
        return 0
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(
        r"<h2><code>([^<]+)</code>\s*[—\-]\s*([^<]+)</h2>"
    )
    changed = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal changed
        tid = m.group(1)
        label = _label_for(tid)
        changed += 1
        return f"<h2>{label}</h2>\n<p><code>{tid}</code></p>"

    new = pattern.sub(repl, text)
    if changed:
        path.write_text(new, encoding="utf-8")
    return changed


def main() -> int:
    known = frozenset(QUESTION_TYPES.keys())
    html_n = md_n = 0

    if BY_TOPIC.is_dir():
        for folder in sorted(BY_TOPIC.iterdir()):
            if not folder.is_dir():
                continue
            html = folder / "gallery.html"
            if not html.is_file():
                continue
            tid = type_id_from_folder(folder.name, known_ids=known)
            label = _label_for(tid)
            if _relabel_html(html, label):
                html_n += 1
            if _relabel_md(folder / "gallery.md", label):
                md_n += 1

    # Calc continuous single-topic folders (c1_calc_*).
    for folder in sorted(TOPIC_FIT.iterdir()):
        if not folder.is_dir() or folder.name == "by_topic":
            continue
        if not (
            folder.name.startswith("c1_calc_")
            or folder.name.startswith("c2_calc_")
            or folder.name.startswith("c3_calc_")
        ):
            continue
        html = folder / "gallery.html"
        if not html.is_file():
            continue
        tid = type_id_from_folder(folder.name, known_ids=known)
        if tid not in known and folder.name.startswith(("c1_", "c2_", "c3_")):
            # c1_calc_diff_… → calc_diff_…
            for p in ("c1_", "c2_", "c3_"):
                if folder.name.startswith(p):
                    cand = folder.name[len(p) :]
                    if cand in known:
                        tid = cand
                    break
        label = _label_for(tid)
        if _relabel_html(html, label):
            html_n += 1
        if _relabel_md(folder / "gallery.md", label):
            md_n += 1

    # Aggregate calc galleries: section headings.
    for agg in ("c1_calculus_derivative_rules", "c1_calculus_pilot"):
        folder = TOPIC_FIT / agg
        if _relabel_aggregate_md(folder / "gallery.md"):
            md_n += 1
        html_n += _relabel_aggregate_html(folder / "gallery.html")

    # Rebuild INDEX with prefixed topic column.
    bv_spec = importlib.util.spec_from_file_location(
        "build_verified_topic_galleries",
        ROOT / "scripts" / "build_verified_topic_galleries.py",
    )
    bv = importlib.util.module_from_spec(bv_spec)
    assert bv_spec.loader is not None
    bv_spec.loader.exec_module(bv)
    index_path = bv.write_index(
        generated=[],
        skipped_ooo=[],
        failures=[],
        remaining_notes=[
            "Titles/h1 refreshed via `scripts/relabel_topic_fit_galleries.py` "
            "(display prefixes only; type_ids unchanged).",
        ],
    )

    print(f"relabeled html={html_n} md={md_n}")
    print(f"INDEX -> {index_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
