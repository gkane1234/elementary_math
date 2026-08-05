#!/usr/bin/env python3
"""Local live adaptive human-rating loop (v1).

Stratified continuous-D → generate → rate → append JSONL → next.

Usage:
  $env:PYTHONPATH='.'
  python scripts/live_rating_server.py
  # open http://127.0.0.1:8777/

  # CLI smoke:
  python scripts/live_rating_server.py --list-types
  python scripts/live_rating_server.py --next --type-id g6_introduction_to_ratios --session smoke_g6
  python scripts/live_rating_server.py --submit --session smoke_g6 --type-id g6_introduction_to_ratios --rating 3 --minutes 1 --notes "fake"
  python scripts/live_rating_server.py --coverage --session smoke_g6 --type-id g6_introduction_to_ratios

API:
  GET  /api/types
  GET  /api/coverage?type_id=&session=
  GET|POST /api/next   body/query: type_id, session?, difficulty?, seed?
  POST /api/submit     body: type_id, session?, rating_id?, rating_1_to_5, minutes?, notes?,
                             topic_fit_ok?, latex_ok?, broken?, skip?

v2 (not here): uncertainty BO, inverse human model, pairwise, full knob registry.
"""

from __future__ import annotations

import argparse
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import question_engine.types  # noqa: F401 — register catalogs

from question_engine.ml.live_rating import (  # noqa: E402
    LIVE_ROOT,
    LiveRatingSession,
    list_types,
    pick_next_difficulty,
)

HOST = "127.0.0.1"
PORT = 8777


def _katex_head() -> str:
    """Prefer local KaTeX when vendored; fall back to CDN for the live server."""
    try:
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "topic_fit_katex", ROOT / "scripts" / "topic_fit_katex.py"
        )
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            # Serve via /assets/katex/… from this process.
            return (
                '<link rel="stylesheet" href="/assets/katex/katex.min.css"/>\n'
                '<script defer src="/assets/katex/katex.min.js"></script>\n'
                '<script defer src="/assets/katex/contrib/auto-render.min.js"></script>\n'
            )
    except Exception:  # noqa: BLE001
        pass
    return (
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css"/>\n'
        '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>\n'
        '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>\n'
    )


def _ensure_katex_vendor() -> Path | None:
    try:
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "topic_fit_katex", ROOT / "scripts" / "topic_fit_katex.py"
        )
        if not spec or not spec.loader:
            return None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return Path(mod.ensure_katex_vendor())
    except Exception:  # noqa: BLE001
        return None


def build_html() -> str:
    katex = _katex_head()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Polynomial — live rater (v1)</title>
{katex}
<style>
:root {{ color-scheme: light; --ink:#1a1a1a; --muted:#5a5a5a; --line:#cfc8bc; --bg:#f7f4ee; --card:#fffdf8; --accent:#1f4d3a; --warn:#8a4b2a; }}
* {{ box-sizing: border-box; }}
body {{ margin:0; font-family: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
  color: var(--ink); background: linear-gradient(165deg, #efe8dc 0%, #f7f4ee 40%, #e7eef0 100%); min-height:100vh; }}
header {{ padding: 1rem 1.25rem; border-bottom: 1px solid var(--line); background: rgba(255,253,248,0.92);
  position: sticky; top:0; z-index:5; backdrop-filter: blur(6px); }}
header h1 {{ margin:0; font-size:1.35rem; letter-spacing:0.02em; }}
header p {{ margin:0.25rem 0 0; color:var(--muted); font-size:0.92rem; }}
.toolbar {{ display:flex; flex-wrap:wrap; gap:0.5rem 0.75rem; align-items:center; margin-top:0.75rem; }}
.toolbar label {{ font-size:0.85rem; color:var(--muted); }}
select, input[type="number"], input[type="text"], textarea, button {{ font: inherit; font-size:0.92rem; }}
select, input[type="number"], input[type="text"] {{
  border:1px solid var(--line); border-radius:4px; padding:0.3rem 0.45rem; background:#fff; }}
button {{ border:1px solid var(--accent); background:var(--accent); color:#f6fff9; border-radius:4px;
  padding:0.35rem 0.7rem; cursor:pointer; }}
button.secondary {{ background:#fff; color:var(--accent); }}
button.score {{ min-width:2.2rem; background:#fff; color:var(--ink); border-color:var(--line); }}
button.score.active {{ background:var(--accent); color:#fff; border-color:var(--accent); }}
button:disabled {{ opacity:0.45; cursor:default; }}
main {{ max-width: 52rem; margin: 0 auto; padding: 1.25rem; }}
.card {{ background: var(--card); border:1px solid var(--line); border-radius:6px; padding:1rem 1.1rem 1.2rem;
  box-shadow: 0 1px 0 rgba(0,0,0,0.03); }}
.meta {{ display:flex; flex-wrap:wrap; gap:0.35rem 0.75rem; font-size:0.82rem; color:var(--muted); margin-bottom:0.75rem; }}
.meta code {{ color:var(--ink); background:#efe9df; padding:0.05rem 0.3rem; border-radius:3px; }}
.prompt {{ font-size:1.15rem; margin:0.75rem 0; min-height:2.5rem; }}
.answer {{ margin:0.5rem 0 1rem; padding:0.6rem 0.75rem; background:#f0ebe3; border-radius:4px; }}
.answer summary {{ cursor:pointer; color:var(--muted); }}
.rate-row {{ display:flex; flex-wrap:wrap; gap:0.5rem; align-items:center; margin:0.75rem 0; }}
.flags {{ display:flex; flex-wrap:wrap; gap:0.75rem 1rem; font-size:0.9rem; color:var(--muted); margin:0.5rem 0; }}
.flags label {{ display:flex; align-items:center; gap:0.3rem; }}
textarea {{ width:100%; min-height:3.5rem; border:1px solid var(--line); border-radius:4px; padding:0.45rem; background:#fff; }}
.nav {{ display:flex; justify-content:space-between; gap:0.75rem; margin-top:1rem; }}
.coverage {{ font-size:0.82rem; color:var(--muted); margin-top:0.75rem; font-variant-numeric: tabular-nums; }}
.toast {{ position:fixed; bottom:1rem; right:1rem; background:#1a1a1a; color:#fff; padding:0.5rem 0.75rem;
  border-radius:4px; font-size:0.85rem; opacity:0; transition:opacity 0.2s; pointer-events:none; }}
.toast.show {{ opacity:0.92; }}
.status {{ color:var(--muted); font-size:0.85rem; }}
.status.err {{ color:var(--warn); }}
</style>
</head>
<body>
<header>
  <h1>Polynomial — live rater (v1)</h1>
  <p>Stratified continuous-D · rate → append → next. No GP/BO yet.</p>
  <div class="toolbar">
    <label>type_id
      <input id="typeFilter" type="text" list="typeList" placeholder="filter…" style="width:14rem"/>
      <datalist id="typeList"></datalist>
    </label>
    <label>Session <input id="session" type="text" placeholder="(defaults to type_id)" style="width:10rem"/></label>
    <button type="button" id="btnLoadTypes" class="secondary">Refresh types</button>
    <button type="button" id="btnNext">Load next</button>
    <span class="status" id="status"></span>
  </div>
</header>
<main>
  <div class="card" id="card">
    <div class="meta" id="meta"><em>Pick a type_id and Load next.</em></div>
    <div class="prompt" id="prompt"></div>
    <details class="answer"><summary>Show answer</summary><div id="answer"></div></details>
    <div class="rate-row" id="scores"><span>Rating:</span></div>
    <div class="rate-row">
      <label>Minutes <input id="minutes" type="number" min="0" step="0.5" style="width:5rem"/></label>
    </div>
    <div class="flags">
      <label><input type="checkbox" id="flagTopicFit"/> topic_fit ok</label>
      <label><input type="checkbox" id="flagLatex"/> latex ok</label>
      <label><input type="checkbox" id="flagBroken"/> broken</label>
    </div>
    <label for="notes">Notes</label>
    <textarea id="notes" placeholder="Optional pedagogy / latex / topic flags"></textarea>
    <div class="nav">
      <button type="button" class="secondary" id="btnSkip">Skip</button>
      <button type="button" id="btnSubmit" disabled>Submit &amp; next</button>
    </div>
    <div class="coverage" id="coverage"></div>
  </div>
</main>
<div class="toast" id="toast"></div>
<script>
const STORAGE_KEY = "poly_live_rater_v1";
let types = [];
let current = null;
let currentScore = null;

function loadPrefs() {{
  try {{ return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{{}}"); }}
  catch (e) {{ return {{}}; }}
}}
function savePrefs(p) {{
  localStorage.setItem(STORAGE_KEY, JSON.stringify(p));
}}

function toast(msg) {{
  const el = document.getElementById("toast");
  el.textContent = msg;
  el.classList.add("show");
  setTimeout(() => el.classList.remove("show"), 1400);
}}

function setStatus(msg, err) {{
  const el = document.getElementById("status");
  el.textContent = msg || "";
  el.className = "status" + (err ? " err" : "");
}}

async function api(method, path, body) {{
  const opts = {{ method, headers: {{ "Content-Type": "application/json" }} }};
  if (body !== undefined) opts.body = JSON.stringify(body);
  const r = await fetch(path, opts);
  const text = await r.text();
  let data;
  try {{ data = JSON.parse(text); }} catch {{ data = {{ error: text }}; }}
  if (!r.ok) throw new Error(data.error || r.statusText);
  return data;
}}

function wrapMath(tex) {{
  const t = (tex || "").trim();
  if (!t) return "<em>(empty)</em>";
  if (t.startsWith("$$") || t.startsWith("$")) return t;
  return "$" + t + "$";
}}

function renderMath() {{
  if (window.renderMathInElement) {{
    renderMathInElement(document.getElementById("card"), {{
      delimiters: [
        {{left: "$$", right: "$$", display: true}},
        {{left: "$", right: "$", display: false}}
      ],
      throwOnError: false
    }});
  }}
}}

function typeId() {{
  return (document.getElementById("typeFilter").value || "").trim();
}}
function sessionName() {{
  return (document.getElementById("session").value || "").trim() || null;
}}

function fillTypes(list) {{
  types = list || [];
  const dl = document.getElementById("typeList");
  dl.innerHTML = "";
  for (const t of types) {{
    const opt = document.createElement("option");
    opt.value = t.type_id;
    opt.label = (t.category || "") + " / " + (t.name || t.type_id);
    dl.appendChild(opt);
  }}
}}

function showCoverage(cov) {{
  if (!cov) {{ document.getElementById("coverage").textContent = ""; return; }}
  const bins = cov.by_difficulty || {{}};
  const parts = Object.keys(bins).sort((a,b)=>Number(a)-Number(b)).map(k => "D" + k + "=" + bins[k]);
  document.getElementById("coverage").textContent =
    "Rated " + (cov.n_ratings || 0) + " · " + parts.join(" · ") +
    (cov.dir ? " · " + cov.dir : "");
}}

function showItem(it) {{
  current = it;
  currentScore = null;
  document.querySelectorAll("button.score").forEach(b => b.classList.remove("active"));
  document.getElementById("minutes").value = "";
  document.getElementById("notes").value = "";
  document.getElementById("flagTopicFit").checked = false;
  document.getElementById("flagLatex").checked = false;
  document.getElementById("flagBroken").checked = false;
  document.getElementById("btnSubmit").disabled = !it;
  if (!it) {{
    document.getElementById("meta").innerHTML = "<em>No item.</em>";
    document.getElementById("prompt").innerHTML = "";
    document.getElementById("answer").innerHTML = "";
    return;
  }}
  document.getElementById("meta").innerHTML = [
    "<span>type <code>" + it.type_id + "</code></span>",
    "<span>D <code>" + it.difficulty + "</code></span>",
    "<span>bin <code>" + it.bin + "</code></span>",
    "<span>seed <code>" + it.seed + "</code></span>",
    it.generator ? "<span>gen <code>" + it.generator + "</code></span>" : "",
    it.y_effort != null ? "<span>y_effort <code>" + it.y_effort + "</code></span>" : "",
    it.engine_rev ? "<span>rev <code>" + it.engine_rev + "</code></span>" : "",
    "<span>id <code>" + it.rating_id + "</code></span>"
  ].filter(Boolean).join("");
  document.getElementById("prompt").innerHTML = wrapMath(it.prompt_latex || it.prompt_text || "");
  document.getElementById("answer").innerHTML = wrapMath(it.answer_latex || it.answer_text || "");
  const ans = document.querySelector("details.answer");
  if (ans) ans.open = false;
  renderMath();
  // LocalStorage backup of last item (offline recovery aid).
  const prefs = loadPrefs();
  prefs.lastType = it.type_id;
  prefs.lastSession = sessionName();
  prefs.lastItem = {{ rating_id: it.rating_id, difficulty: it.difficulty, seed: it.seed }};
  savePrefs(prefs);
}}

async function refreshTypes() {{
  setStatus("Loading types…");
  const data = await api("GET", "/api/types");
  fillTypes(data.types || []);
  setStatus((data.types || []).length + " types");
}}

async function loadNext() {{
  const tid = typeId();
  if (!tid) {{ setStatus("Enter a type_id", true); return; }}
  setStatus("Generating…");
  document.getElementById("btnNext").disabled = true;
  try {{
    const body = {{ type_id: tid }};
    const sess = sessionName();
    if (sess) body.session = sess;
    const data = await api("POST", "/api/next", body);
    showItem(data.item);
    showCoverage(data.coverage);
    setStatus("Ready");
    toast("Next item");
  }} catch (e) {{
    setStatus(String(e.message || e), true);
  }} finally {{
    document.getElementById("btnNext").disabled = false;
  }}
}}

async function submit(skip) {{
  if (!current) return;
  if (!skip && currentScore == null) {{ setStatus("Pick a rating 1–5", true); return; }}
  const minutesRaw = document.getElementById("minutes").value;
  const body = {{
    type_id: typeId(),
    session: sessionName(),
    rating_id: current.rating_id,
    rating_1_to_5: skip ? null : currentScore,
    minutes: minutesRaw === "" ? null : Number(minutesRaw),
    notes: document.getElementById("notes").value || null,
    topic_fit_ok: document.getElementById("flagTopicFit").checked ? true : null,
    latex_ok: document.getElementById("flagLatex").checked ? true : null,
    broken: document.getElementById("flagBroken").checked ? true : null,
    skip: !!skip
  }};
  // Only send flag true when checked; leave null otherwise (unchecked ≠ false).
  if (!document.getElementById("flagTopicFit").checked) body.topic_fit_ok = null;
  if (!document.getElementById("flagLatex").checked) body.latex_ok = null;
  if (!document.getElementById("flagBroken").checked) body.broken = null;
  setStatus(skip ? "Skipping…" : "Saving…");
  try {{
    const data = await api("POST", "/api/submit", body);
    showCoverage(data.coverage);
    toast(skip ? "Skipped" : "Saved");
    // Backup last rating locally.
    const prefs = loadPrefs();
    prefs.lastSubmit = {{ rating_id: body.rating_id, rating_1_to_5: body.rating_1_to_5, at: new Date().toISOString() }};
    savePrefs(prefs);
    await loadNext();
  }} catch (e) {{
    setStatus(String(e.message || e), true);
  }}
}}

const scores = document.getElementById("scores");
for (let s = 1; s <= 5; s++) {{
  const b = document.createElement("button");
  b.type = "button";
  b.className = "score";
  b.dataset.score = String(s);
  b.textContent = String(s);
  b.addEventListener("click", () => {{
    currentScore = s;
    document.querySelectorAll("button.score").forEach(x =>
      x.classList.toggle("active", Number(x.dataset.score) === currentScore));
  }});
  scores.appendChild(b);
}}

document.getElementById("btnLoadTypes").addEventListener("click", () => refreshTypes().catch(e => setStatus(String(e.message||e), true)));
document.getElementById("btnNext").addEventListener("click", () => loadNext());
document.getElementById("btnSubmit").addEventListener("click", () => submit(false));
document.getElementById("btnSkip").addEventListener("click", () => submit(true));

document.addEventListener("keydown", (e) => {{
  if (e.target && (e.target.tagName === "TEXTAREA" || e.target.tagName === "INPUT")) return;
  if (e.key >= "1" && e.key <= "5") {{
    currentScore = Number(e.key);
    document.querySelectorAll("button.score").forEach(x =>
      x.classList.toggle("active", Number(x.dataset.score) === currentScore));
  }} else if (e.key === "Enter") {{
    submit(false);
  }}
}});

(async function init() {{
  const prefs = loadPrefs();
  if (prefs.lastType) document.getElementById("typeFilter").value = prefs.lastType;
  if (prefs.lastSession) document.getElementById("session").value = prefs.lastSession;
  try {{
    await refreshTypes();
  }} catch (e) {{
    setStatus(String(e.message || e), true);
  }}
}})();
</script>
</body>
</html>
"""


def _session_from_request(body: dict[str, Any], qs: dict[str, list[str]]) -> LiveRatingSession:
    type_id = (body.get("type_id") or (qs.get("type_id") or [None])[0] or "").strip()
    if not type_id:
        raise ValueError("type_id required")
    session = body.get("session")
    if session is None:
        session = (qs.get("session") or [None])[0]
    if session is not None:
        session = str(session).strip() or None
    return LiveRatingSession(type_id, session=session)


class Handler(BaseHTTPRequestHandler):
    katex_root: Path | None = None

    def _send(self, code: int, body: bytes, content_type: str = "application/json") -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, code: int, payload: dict[str, Any]) -> None:
        self._send(code, json.dumps(payload, ensure_ascii=False).encode("utf-8"))

    def _read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b"{}"
        data = json.loads(raw.decode("utf-8") or "{}")
        return data if isinstance(data, dict) else {}

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        if path in {"/", "/index.html"}:
            html = build_html().encode("utf-8")
            self._send(200, html, "text/html; charset=utf-8")
            return

        if path.startswith("/assets/katex/") and self.katex_root:
            rel = path[len("/assets/katex/") :]
            target = (self.katex_root / rel).resolve()
            try:
                target.relative_to(self.katex_root.resolve())
            except ValueError:
                self._json(404, {"error": "not found"})
                return
            if not target.is_file():
                self._json(404, {"error": "not found"})
                return
            data = target.read_bytes()
            ctype = "application/octet-stream"
            if target.suffix == ".css":
                ctype = "text/css; charset=utf-8"
            elif target.suffix == ".js":
                ctype = "application/javascript; charset=utf-8"
            elif target.suffix == ".woff2":
                ctype = "font/woff2"
            elif target.suffix == ".woff":
                ctype = "font/woff"
            elif target.suffix == ".ttf":
                ctype = "font/ttf"
            self._send(200, data, ctype)
            return

        try:
            if path == "/api/types":
                ready_only = (qs.get("ready_only") or ["1"])[0] != "0"
                include_scaffolds = (qs.get("include_scaffolds") or ["0"])[0] == "1"
                types = list_types(ready_only=ready_only, include_scaffolds=include_scaffolds)
                self._json(200, {"types": types, "n": len(types)})
                return
            if path == "/api/coverage":
                sess = _session_from_request({}, qs)
                self._json(200, sess.coverage())
                return
            if path == "/api/next":
                sess = _session_from_request({}, qs)
                difficulty = (qs.get("difficulty") or [None])[0]
                seed = (qs.get("seed") or [None])[0]
                item = sess.generate_next(
                    difficulty=float(difficulty) if difficulty is not None else None,
                    seed=int(seed) if seed is not None else None,
                )
                self._json(200, {"item": item, "coverage": sess.coverage()})
                return
            self._json(404, {"error": "not found"})
        except Exception as exc:  # noqa: BLE001
            self._json(400, {"error": str(exc)})

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path
        try:
            body = self._read_json()
            if path == "/api/next":
                sess = _session_from_request(body, {})
                difficulty = body.get("difficulty")
                seed = body.get("seed")
                item = sess.generate_next(
                    difficulty=float(difficulty) if difficulty is not None else None,
                    seed=int(seed) if seed is not None else None,
                )
                self._json(200, {"item": item, "coverage": sess.coverage()})
                return
            if path == "/api/submit":
                sess = _session_from_request(body, {})
                minutes = body.get("minutes")
                result = sess.submit(
                    rating_id=body.get("rating_id"),
                    rating_1_to_5=body.get("rating_1_to_5"),
                    minutes=float(minutes) if minutes is not None and minutes != "" else None,
                    notes=body.get("notes"),
                    topic_fit_ok=body.get("topic_fit_ok"),
                    latex_ok=body.get("latex_ok"),
                    broken=body.get("broken"),
                    skip=bool(body.get("skip")),
                )
                self._json(200, result)
                return
            self._json(404, {"error": "not found"})
        except Exception as exc:  # noqa: BLE001
            self._json(400, {"error": str(exc)})

    def log_message(self, fmt: str, *args: Any) -> None:
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


def _cli_next(args: argparse.Namespace) -> int:
    sess = LiveRatingSession(args.type_id, session=args.session)
    item = sess.generate_next(
        difficulty=args.difficulty,
        seed=args.seed,
    )
    lite = {
        "rating_id": item["rating_id"],
        "type_id": item["type_id"],
        "difficulty": item["difficulty"],
        "bin": item["bin"],
        "seed": item["seed"],
        "prompt_latex": (item.get("prompt_latex") or "")[:200],
        "coverage": sess.coverage(),
    }
    print(json.dumps(lite, indent=2, ensure_ascii=False))
    return 0


def _cli_submit(args: argparse.Namespace) -> int:
    sess = LiveRatingSession(args.type_id, session=args.session)
    result = sess.submit(
        rating_id=args.rating_id,
        rating_1_to_5=args.rating,
        minutes=args.minutes,
        notes=args.notes,
        topic_fit_ok=args.topic_fit_ok,
        latex_ok=args.latex_ok,
        broken=args.broken,
        skip=bool(args.skip),
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Live adaptive human-rating loop (v1)")
    parser.add_argument("--host", default=HOST)
    parser.add_argument("--port", type=int, default=PORT)
    parser.add_argument("--list-types", action="store_true")
    parser.add_argument("--include-scaffolds", action="store_true")
    parser.add_argument("--next", action="store_true", help="CLI: generate next item")
    parser.add_argument("--submit", action="store_true", help="CLI: submit rating for pending")
    parser.add_argument("--coverage", action="store_true")
    parser.add_argument("--type-id", default=None)
    parser.add_argument("--session", default=None)
    parser.add_argument("--difficulty", type=float, default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--rating-id", default=None)
    parser.add_argument("--rating", type=int, default=None)
    parser.add_argument("--minutes", type=float, default=None)
    parser.add_argument("--notes", default=None)
    parser.add_argument("--topic-fit-ok", action="store_true", default=None)
    parser.add_argument("--latex-ok", action="store_true", default=None)
    parser.add_argument("--broken", action="store_true", default=None)
    parser.add_argument("--skip", action="store_true")
    parser.add_argument(
        "--demo-policy",
        action="store_true",
        help="Print next D after fake ratings at one band (no generate)",
    )
    args = parser.parse_args()

    if args.list_types:
        types = list_types(ready_only=True, include_scaffolds=args.include_scaffolds)
        print(json.dumps({"n": len(types), "types": types[:50], "truncated": len(types) > 50}, indent=2))
        return

    if args.demo_policy:
        # Show that after stuffing one band, next prefers underfilled bins.
        fake = [{"difficulty": 8.0, "theta_requested": {"difficulty": 8.0}, "rating_1_to_5": 3}] * 4
        nxt = pick_next_difficulty(fake)
        print(json.dumps({"after_four_at_8": nxt, "expected_not_8": nxt != 8.0}, indent=2))
        return

    if args.coverage:
        if not args.type_id:
            parser.error("--type-id required with --coverage")
        sess = LiveRatingSession(args.type_id, session=args.session)
        print(json.dumps(sess.coverage(), indent=2))
        return

    if args.next:
        if not args.type_id:
            parser.error("--type-id required with --next")
        raise SystemExit(_cli_next(args))

    if args.submit:
        if not args.type_id:
            parser.error("--type-id required with --submit")
        raise SystemExit(_cli_submit(args))

    katex_root = _ensure_katex_vendor()
    Handler.katex_root = katex_root
    print(f"Live ratings root: {LIVE_ROOT}", flush=True)
    print(f"Open http://{args.host}:{args.port}/", flush=True)
    if katex_root:
        print(f"KaTeX assets: {katex_root}", flush=True)
    ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
