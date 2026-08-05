"""Wrap topic-fit gallery.md files in KaTeX-ready gallery.html.

Cursor/VS Code markdown preview does not render `$...$` math. Open the sibling
`gallery.html` in a browser instead (file:// works; KaTeX is local under
``scripts/output/topic_fit/_assets/katex/``).

Usage:
  python scripts/render_topic_fit_gallery_html.py
  python scripts/render_topic_fit_gallery_html.py scripts/output/topic_fit/ooo_audit
  python scripts/render_topic_fit_gallery_html.py --all-missing
  python scripts/render_topic_fit_gallery_html.py --relink-katex
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPIC_FIT = ROOT / "scripts" / "output" / "topic_fit"

import importlib.util

_katex_spec = importlib.util.spec_from_file_location(
    "topic_fit_katex", ROOT / "scripts" / "topic_fit_katex.py"
)
_katex_mod = importlib.util.module_from_spec(_katex_spec)
assert _katex_spec.loader is not None
_katex_spec.loader.exec_module(_katex_mod)
katex_head_html = _katex_mod.katex_head_html
ensure_katex_vendor = _katex_mod.ensure_katex_vendor
relink_all_topic_fit_galleries = _katex_mod.relink_all_topic_fit_galleries

CSS = """\
:root { color-scheme: light; }
body { font-family: Georgia, "Times New Roman", serif; margin: 1.5rem 2rem; line-height: 1.45;
       color: #1a1a1a; background: #faf9f7; max-width:.72rem; }
h1 { font-size: 1.75rem; margin-bottom: 0.25rem; }
h2 { margin-top: 2rem; border-bottom: 1px solid #ccc; padding-bottom: 0.25rem; }
h3 { margin-top: 1.25rem; }
p, li { max-width: 52rem; }
code { font-family: ui-monospace, Consolas, monospace; font-size: 0.85em;
       background: #eee; padding: 0.05rem 0.25rem; border-radius: 3px; }
pre { background: #f0eeea; padding: 0.75rem 1rem; overflow-x: auto; border-radius: 4px; }
pre code { background: none; padding: 0; }
table { border-collapse: collapse; width: 100%; font-size: 0.88rem; margin: 0.5rem 0 1.5rem; }
th, td { border: 1px solid #ccc; padding: 0.4rem 0.5rem; vertical-align: top; }
th { background: #e8e6e1; text-align: left; }
a { color: #1a4a7a; }
.banner { background: #eef2f7; border: 1px solid #c5d0de; padding: 0.5rem 0.75rem;
          margin-bottom: 1rem; border-radius: 4px; font-size: 0.9rem; }
/* If katex.css fails to load, MathML text duplicates the HTML render
   (looks like "Find ddx … Find d/dx …"). Match KaTeX's sr-only clip. */
.katex .katex-mathml {
  position: absolute !important;
  clip: rect(1px, 1px, 1px, 1px) !important;
  -webkit-clip-path: inset(50%) !important;
  clip-path: inset(50%) !important;
  padding: 0 !important;
  border: 0 !important;
  height: 1px !important;
  width: 1px !important;
  overflow: hidden !important;
  white-space: nowrap !important;
}
""".replace("max-width:.72rem", "max-width: 72rem")

_MATH_RE = re.compile(r"\$\$.+?\$\$|\$[^$\n]+?\$", re.DOTALL)
_HEADER_RE = re.compile(r"^(#{1,3})\s+(.+)$")
_TABLE_SEP_RE = re.compile(r"^\|?[\s:|-]+\|[\s:|-]*\|?$")
_TOKEN_RE = re.compile(r"(\[([^\]]+)\]\(([^)]+)\)|\*\*([^*]+)\*\*|`([^`]+)`)")


def _protect_math(text: str) -> tuple[str, list[str]]:
    slots: list[str] = []

    def repl(m: re.Match[str]) -> str:
        slots.append(m.group(0))
        return f"\x00MATH{len(slots) - 1}\x00"

    return _MATH_RE.sub(repl, text), slots


def _restore_math(text: str, slots: list[str]) -> str:
    for i, raw in enumerate(slots):
        text = text.replace(f"\x00MATH{i}\x00", raw)
    return text


def _looks_like_latex(s: str) -> bool:
    """True for bare TeX often wrongly wrapped in markdown backticks."""
    s = (s or "").strip()
    if not s or s.startswith("http"):
        return False
    if s.startswith("$") and s.endswith("$"):
        return True
    return "\\" in s


def format_inline(text: str) -> str:
    """Escape HTML except math; apply links / bold / code.

    Backtick-wrapped strings that look like LaTeX (e.g. ``\\text{...}``) are
    emitted as ``$...$`` so KaTeX auto-render picks them up. KaTeX skips
    ``<code>`` by default, and bare TeX without math delimiters never renders.
    """
    text, math = _protect_math(text)
    parts: list[str] = []
    pos = 0
    for m in _TOKEN_RE.finditer(text):
        parts.append(html.escape(text[pos : m.start()]))
        if m.group(2) is not None:
            parts.append(
                f'<a href="{html.escape(m.group(3), quote=True)}">'
                f"{html.escape(m.group(2))}</a>"
            )
        elif m.group(4) is not None:
            parts.append(f"<strong>{html.escape(m.group(4))}</strong>")
        else:
            code = m.group(5)
            if _looks_like_latex(code):
                body = code.strip()
                if body.startswith("$") and body.endswith("$"):
                    parts.append(body)
                else:
                    parts.append(f"${body}$")
            else:
                parts.append(f"<code>{html.escape(code)}</code>")
        pos = m.end()
    parts.append(html.escape(text[pos:]))
    return _restore_math("".join(parts), math)


def _is_table_row(line: str) -> bool:
    s = line.strip()
    return s.startswith("|") and s.count("|") >= 2


def _parse_table_row(line: str) -> list[str]:
    """Split a markdown table row on `|`, but not inside ``$...$`` math."""
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    cells: list[str] = []
    buf: list[str] = []
    in_math = False
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "$":
            # toggle on single $; $$ handled by toggling twice (still fine)
            in_math = not in_math
            buf.append(ch)
            i += 1
            continue
        if ch == "|" and not in_math:
            cells.append("".join(buf).strip())
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    cells.append("".join(buf).strip())
    return cells


def md_to_body_html(md: str) -> str:
    lines = md.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i = 0
    para: list[str] = []

    def flush_para() -> None:
        nonlocal para
        if para:
            out.append("<p>" + format_inline(" ".join(para)) + "</p>")
            para = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            flush_para()
            i += 1
            continue

        if stripped.startswith("```"):
            flush_para()
            i += 1
            code_lines: list[str] = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            out.append(
                "<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>"
            )
            continue

        hm = _HEADER_RE.match(stripped)
        if hm:
            flush_para()
            level = len(hm.group(1))
            out.append(f"<h{level}>{format_inline(hm.group(2))}</h{level}>")
            i += 1
            continue

        if _is_table_row(stripped) and i + 1 < len(lines) and _TABLE_SEP_RE.match(
            lines[i + 1].strip()
        ):
            flush_para()
            headers = _parse_table_row(stripped)
            i += 2
            rows: list[list[str]] = []
            while i < len(lines) and _is_table_row(lines[i]):
                rows.append(_parse_table_row(lines[i]))
                i += 1
            out.append("<table><thead><tr>")
            for h in headers:
                out.append(f"<th>{format_inline(h)}</th>")
            out.append("</tr></thead><tbody>")
            for row in rows:
                while len(row) < len(headers):
                    row.append("")
                out.append("<tr>")
                for cell in row[: len(headers)]:
                    out.append(f"<td>{format_inline(cell)}</td>")
                out.append("</tr>")
            out.append("</tbody></table>")
            continue

        if stripped.startswith("- ") or stripped.startswith("* "):
            flush_para()
            out.append("<ul>")
            while i < len(lines) and (
                lines[i].strip().startswith("- ") or lines[i].strip().startswith("* ")
            ):
                item = lines[i].strip()[2:]
                out.append(f"<li>{format_inline(item)}</li>")
                i += 1
            out.append("</ul>")
            continue

        para.append(stripped)
        i += 1

    flush_para()
    return "\n".join(out)


def wrap_gallery_html(
    md_text: str,
    title: str | None = None,
    *,
    html_path: Path | None = None,
) -> str:
    body = md_to_body_html(md_text)
    if not title:
        m = re.search(r"^#\s+(.+)$", md_text, re.MULTILINE)
        title = m.group(1).strip() if m else "Gallery"
    title_esc = html.escape(title)
    katex = katex_head_html(html_path) if html_path is not None else katex_head_html(depth=2)
    return (
        "<!DOCTYPE html>\n"
        '<html lang="en"><head><meta charset="utf-8"/>\n'
        f"<title>{title_esc}</title>\n"
        f"<style>\n{CSS}\n</style>\n"
        f"{katex}"
        "</head><body>\n"
        '<p class="banner">KaTeX-rendered view of <code>gallery.md</code>. '
        "Open this file in a browser (not the Cursor markdown preview).</p>\n"
        f"{body}\n"
        "</body></html>\n"
    )


def render_one(md_path: Path, *, force: bool = False) -> Path | None:
    md_path = md_path.resolve()
    if md_path.is_dir():
        md_path = md_path / "gallery.md"
    if md_path.name != "gallery.md" or not md_path.is_file():
        raise SystemExit(f"Expected gallery.md file or folder, got {md_path}")
    html_path = md_path.with_name("gallery.html")
    if html_path.exists() and not force:
        return None
    md_text = md_path.read_text(encoding="utf-8")
    html_path.write_text(
        wrap_gallery_html(md_text, html_path=html_path), encoding="utf-8"
    )
    return html_path


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="gallery.md files or audit folders",
    )
    ap.add_argument(
        "--all-missing",
        action="store_true",
        help="Render every topic_fit gallery.md that lacks gallery.html",
    )
    ap.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing gallery.html",
    )
    ap.add_argument(
        "--include-timestamps",
        action="store_true",
        help="With --all-missing, also render dated snapshot folders",
    )
    ap.add_argument(
        "--relink-katex",
        action="store_true",
        help="Rewrite CDN KaTeX URLs in existing gallery.html to local _assets",
    )
    args = ap.parse_args()

    if args.relink_katex:
        ensure_katex_vendor()
        updated = relink_all_topic_fit_galleries()
        for p in updated:
            print(f"relinked {p}")
        print(f"relinked {len(updated)} gallery.html file(s)")
        return

    targets: list[Path] = []
    if args.all_missing:
        for md in sorted(TOPIC_FIT.rglob("gallery.md")):
            if not args.include_timestamps and re.match(r"^\d{8}T", md.parent.name):
                continue
            if not md.with_name("gallery.html").exists() or args.force:
                targets.append(md)
    elif args.paths:
        targets = list(args.paths)
    else:
        targets = [TOPIC_FIT / "ooo_audit"]

    # Default / explicit paths: write if missing; --force overwrites.
    # Never overwrite richer audit HTML unless --force.
    force = args.force
    written: list[Path] = []
    kept: list[Path] = []
    for t in targets:
        result = render_one(t, force=force)
        if result is None:
            kept.append(Path(t))
        else:
            written.append(result)

    for p in written:
        print(f"wrote {p}")
    for p in kept:
        html_p = (p / "gallery.html") if p.is_dir() else p.with_name("gallery.html")
        if not html_p.exists() and p.name == "gallery.md":
            html_p = p.with_name("gallery.html")
        print(f"kept existing {html_p if html_p.exists() else p}")

    if not written and not kept:
        print("nothing to do", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
