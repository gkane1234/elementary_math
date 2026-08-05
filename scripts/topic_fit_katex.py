"""Local KaTeX for topic_fit gallery.html (works under file:// in Firefox).

Vendors katex.min.css/js + auto-render + fonts under
``scripts/output/topic_fit/_assets/katex/`` from ``node_modules/katex/dist``.
Galleries use relative href/src so double-click open needs no network.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPIC_FIT = ROOT / "scripts" / "output" / "topic_fit"
KATEX_VENDOR = TOPIC_FIT / "_assets" / "katex"
NODE_KATEX_DIST = ROOT / "node_modules" / "katex" / "dist"

CDN_DIST_RE = re.compile(
    r"https://cdn\.jsdelivr\.net/npm/katex@[^/]+/dist/",
    re.IGNORECASE,
)

_AUTO_RENDER_ONLOAD = (
    "renderMathInElement(document.body,{delimiters:["
    "{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}"
    "],throwOnError:false});"
    "document.documentElement.setAttribute('data-math-ready','1');"
)


def ensure_katex_vendor(*, force: bool = False) -> Path:
    """Copy KaTeX dist assets into topic_fit/_assets/katex if missing."""
    marker = KATEX_VENDOR / "katex.min.js"
    if marker.is_file() and not force:
        return KATEX_VENDOR
    if not NODE_KATEX_DIST.is_dir():
        raise FileNotFoundError(
            f"KaTeX not found at {NODE_KATEX_DIST}. Run `npm install` first."
        )
    KATEX_VENDOR.mkdir(parents=True, exist_ok=True)
    for name in ("katex.min.css", "katex.min.js"):
        shutil.copy2(NODE_KATEX_DIST / name, KATEX_VENDOR / name)
    contrib_src = NODE_KATEX_DIST / "contrib" / "auto-render.min.js"
    contrib_dst = KATEX_VENDOR / "contrib"
    contrib_dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(contrib_src, contrib_dst / "auto-render.min.js")
    fonts_src = NODE_KATEX_DIST / "fonts"
    fonts_dst = KATEX_VENDOR / "fonts"
    if fonts_dst.exists():
        shutil.rmtree(fonts_dst)
    shutil.copytree(fonts_src, fonts_dst)
    return KATEX_VENDOR


def katex_rel_prefix(html_path: Path) -> str:
    """Posix-relative path from gallery.html's directory to the vendor folder."""
    html_path = html_path.resolve()
    ensure_katex_vendor()
    rel = Path(
        __import__("os").path.relpath(KATEX_VENDOR.resolve(), html_path.parent)
    ).as_posix()
    return rel


def katex_head_html(html_path: Path | None = None, *, depth: int | None = None) -> str:
    """Return <link>/<script> tags pointing at local KaTeX."""
    if html_path is not None:
        prefix = katex_rel_prefix(html_path)
    elif depth is not None:
        ensure_katex_vendor()
        prefix = "/".join([".."] * depth) + "/_assets/katex"
    else:
        ensure_katex_vendor()
        prefix = "../_assets/katex"
    return (
        f'<link rel="stylesheet" href="{prefix}/katex.min.css"/>\n'
        f'<script defer src="{prefix}/katex.min.js"></script>\n'
        f'<script defer src="{prefix}/contrib/auto-render.min.js"\n'
        f'  onload="{_AUTO_RENDER_ONLOAD}"></script>\n'
    )


def rewrite_katex_cdn_to_local(html_text: str, html_path: Path) -> str:
    """Replace jsDelivr KaTeX CDN URLs with relative local vendor paths."""
    if "cdn.jsdelivr.net/npm/katex" not in html_text.lower():
        return html_text
    prefix = katex_rel_prefix(html_path)
    return CDN_DIST_RE.sub(prefix.rstrip("/") + "/", html_text)


def relink_all_topic_fit_galleries(*, force_vendor: bool = False) -> list[Path]:
    """Rewrite CDN KaTeX URLs in every topic_fit gallery.html."""
    ensure_katex_vendor(force=force_vendor)
    updated: list[Path] = []
    for html_path in sorted(TOPIC_FIT.rglob("gallery.html")):
        text = html_path.read_text(encoding="utf-8")
        new = rewrite_katex_cdn_to_local(text, html_path)
        if new != text:
            html_path.write_text(new, encoding="utf-8")
            updated.append(html_path)
    return updated


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--relink",
        action="store_true",
        help="Rewrite CDN URLs in existing topic_fit gallery.html files",
    )
    ap.add_argument(
        "--force-vendor",
        action="store_true",
        help="Re-copy KaTeX from node_modules even if already vendored",
    )
    args = ap.parse_args()
    ensure_katex_vendor(force=args.force_vendor)
    print(f"vendored {KATEX_VENDOR}")
    if args.relink:
        for p in relink_all_topic_fit_galleries():
            print(f"relinked {p.relative_to(ROOT)}")
