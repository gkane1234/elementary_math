#!/usr/bin/env python3
"""Local live adaptive human-rating loop (pairwise Bayesian utility).

Default next action generates two candidates (A/B). Choose A better / B better
/ tie. The model is a Bayesian linear utility with uncertainty; once ready it
picks informative pairs and reweights form_id at generate time.

Usage:
  $env:PYTHONPATH='.'
  python scripts/live_rating_server.py
  # open http://127.0.0.1:8777/
  # default UI campaign = all_topics

  # CLI smoke (all-topics campaign, pairwise):
  python scripts/live_rating_server.py --next --campaign all_topics --session smoke_all
  python scripts/live_rating_server.py --submit --campaign all_topics --session smoke_all --winner a
  python scripts/live_rating_server.py --coverage --campaign all_topics --session smoke_all

  # Single-item (legacy --rating):
  python scripts/live_rating_server.py --next --single --campaign all_topics --session smoke_abs
  python scripts/live_rating_server.py --submit --campaign all_topics --session smoke_abs --rating 3

API:
  GET  /api/types
  GET  /api/coverage?type_id=&session=&campaign=
  GET|POST /api/next   pair=1 (default) → {pair, coverage}; pair=0 → {item, coverage}
  POST /api/submit     winner=a|b|tie (pair) or rating_1_to_5 (single)

``/api/next`` stamps ``predicted_rating``, ``predicted_std``, ``n_train``,
``n_pairs``, ``model_ready``.
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
    ALL_TOPICS_CAMPAIGN,
    LIVE_ROOT,
    MIN_PAIRS,
    MIN_TRAIN,
    SKELETON_DERIV_CAMPAIGN,
    SKELETON_DERIV_TYPE_IDS,
    LiveRatingSession,
    MultiTypeCampaign,
    list_types,
    open_live_session,
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
    skel_types_js = json.dumps(list(SKELETON_DERIV_TYPE_IDS))
    min_train = int(MIN_TRAIN)
    min_pairs = int(MIN_PAIRS)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Polynomial — live rater (all topics)</title>
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
.pred {{ margin:0.5rem 0 0.75rem; padding:0.55rem 0.7rem; border-radius:4px; background:#e8f0ea; font-size:0.92rem; }}
.pred.cold {{ background:#f3ebe3; color:var(--warn); }}
.prompt-block {{ margin:0.85rem 0 1rem; padding:0.7rem 0.8rem 0.85rem; border:1px solid var(--line);
  border-radius:5px; background:#fff; }}
.prompt-label {{ margin:0 0 0.4rem; font-size:0.78rem; font-weight:700; letter-spacing:0.06em;
  text-transform:uppercase; color:var(--accent); }}
.prompt {{ font-size:1.2rem; margin:0.15rem 0 0.55rem; min-height:2.2rem; }}
.prompt-fallback-note {{ margin:0 0 0.45rem; font-size:0.82rem; color:var(--warn); }}
.prompt-raw {{ margin:0.35rem 0 0; font-size:0.82rem; color:var(--muted); }}
.prompt-raw summary {{ cursor:pointer; }}
.prompt-raw pre {{ margin:0.4rem 0 0; padding:0.45rem 0.55rem; background:#efe9df; border-radius:4px;
  overflow:auto; white-space:pre-wrap; word-break:break-word; font-family:Consolas, "Courier New", monospace;
  font-size:0.8rem; color:var(--ink); }}
.answer {{ margin:0.5rem 0 1rem; padding:0.6rem 0.75rem; background:#f0ebe3; border-radius:4px; }}
.answer summary {{ cursor:pointer; color:var(--muted); }}
.rate-row {{ display:flex; flex-wrap:wrap; gap:0.5rem; align-items:center; margin:0.75rem 0; }}
.flags {{ display:flex; flex-wrap:wrap; gap:0.75rem 1rem; font-size:0.9rem; color:var(--muted); margin:0.5rem 0; }}
.flags label {{ display:flex; align-items:center; gap:0.3rem; }}
.flags-hint {{ width:100%; font-size:0.78rem; color:var(--muted); margin:0; }}
textarea {{ width:100%; min-height:3.5rem; border:1px solid var(--line); border-radius:4px; padding:0.45rem; background:#fff; }}
.nav {{ display:flex; justify-content:space-between; gap:0.75rem; margin-top:1rem; }}
.coverage {{ font-size:0.82rem; color:var(--muted); margin-top:0.75rem; font-variant-numeric: tabular-nums; }}
.toast {{ position:fixed; bottom:1rem; right:1rem; background:#1a1a1a; color:#fff; padding:0.5rem 0.75rem;
  border-radius:4px; font-size:0.85rem; opacity:0; transition:opacity 0.2s; pointer-events:none; }}
.toast.show {{ opacity:0.92; }}
.status {{ color:var(--muted); font-size:0.85rem; }}
.status.err {{ color:var(--warn); }}
.skel-hint {{ font-size:0.78rem; color:var(--muted); margin-top:0.35rem; }}
.pair-grid {{ display:grid; grid-template-columns: 1fr 1fr; gap:0.85rem; }}
@media (max-width: 820px) {{ .pair-grid {{ grid-template-columns: 1fr; }} }}
.side-card {{ border:1px solid var(--line); border-radius:5px; padding:0.65rem 0.75rem 0.8rem; background:#fff; }}
.side-card.chosen {{ outline:2px solid var(--accent); }}
.side-label {{ margin:0 0 0.35rem; font-size:0.78rem; font-weight:700; letter-spacing:0.06em;
  text-transform:uppercase; color:var(--accent); }}
.winner-row {{ display:flex; flex-wrap:wrap; gap:0.5rem; justify-content:center; margin:1rem 0 0.5rem; }}
button.winner-btn {{ min-width:7.2rem; background:#fff; color:var(--ink); border-color:var(--line); }}
button.winner-btn.active {{ background:var(--accent); color:#fff; border-color:var(--accent); }}
details.abs-rate {{ margin-top:0.65rem; font-size:0.85rem; color:var(--muted); }}
details.abs-rate summary {{ cursor:pointer; }}
</style>
</head>
<body>
<header>
  <h1>Polynomial — live rater</h1>
  <p>Pairwise A vs B · Bayesian utility with uncertainty · generation reweights preferred forms. Cold start until {min_pairs} pairs or {min_train} absolute ratings. Generation-process change resets the model.</p>
  <div class="toolbar">
    <label>Campaign
      <select id="campaign">
        <option value="all_topics" selected>all_topics (every Ready leaf)</option>
        <option value="skeleton_deriv">skeleton_deriv (calc_diff_* only)</option>
        <option value="single">single type_id</option>
      </select>
    </label>
    <label>type_id
      <input id="typeFilter" type="text" list="typeList" placeholder="(campaign picks)" style="width:14rem"/>
      <datalist id="typeList"></datalist>
    </label>
    <label>Session <input id="session" type="text" placeholder="all_topics" style="width:10rem"/></label>
    <button type="button" id="btnLoadTypes" class="secondary">Refresh types</button>
    <button type="button" id="btnNext">Load next</button>
    <span class="status" id="status"></span>
  </div>
</header>
<main>
  <div class="card" id="card">
    <div class="meta" id="meta"><em>Load next to start the all-topics campaign (A vs B).</em></div>
    <div class="pred cold" id="pred">Model: cold start — predicted rating n/a</div>
    <div class="pair-grid" id="pairGrid">
      <section class="side-card" id="sideA">
        <h2 class="side-label">A</h2>
        <div class="meta" id="metaA"></div>
        <section class="prompt-block">
          <h3 class="prompt-label">Prompt</h3>
          <div class="prompt" id="promptA"></div>
          <p class="prompt-fallback-note" id="promptFallbackNoteA" hidden></p>
          <details class="prompt-raw" open>
            <summary>Raw prompt (LaTeX / text)</summary>
            <pre id="promptRawA"></pre>
          </details>
        </section>
        <details class="answer"><summary>Show answer</summary><div id="answerA"></div></details>
        <div class="flags">
          <p class="flags-hint">Check only if A is wrong. Unchecked = fine.</p>
          <label><input type="checkbox" id="flagTopicFitA"/> incorrect topic fit</label>
          <label><input type="checkbox" id="flagLatexA"/> latex broken</label>
          <label><input type="checkbox" id="flagBrokenA"/> broken / bad gen</label>
        </div>
        <details class="abs-rate">
          <summary>Optional absolute 1–5 (A)</summary>
          <div class="rate-row" id="scoresA"><span>A rating:</span></div>
        </details>
        <div class="skel-hint" id="skelHintA"></div>
      </section>
      <section class="side-card" id="sideB">
        <h2 class="side-label">B</h2>
        <div class="meta" id="metaB"></div>
        <section class="prompt-block">
          <h3 class="prompt-label">Prompt</h3>
          <div class="prompt" id="promptB"></div>
          <p class="prompt-fallback-note" id="promptFallbackNoteB" hidden></p>
          <details class="prompt-raw" open>
            <summary>Raw prompt (LaTeX / text)</summary>
            <pre id="promptRawB"></pre>
          </details>
        </section>
        <details class="answer"><summary>Show answer</summary><div id="answerB"></div></details>
        <div class="flags">
          <p class="flags-hint">Check only if B is wrong. Unchecked = fine.</p>
          <label><input type="checkbox" id="flagTopicFitB"/> incorrect topic fit</label>
          <label><input type="checkbox" id="flagLatexB"/> latex broken</label>
          <label><input type="checkbox" id="flagBrokenB"/> broken / bad gen</label>
        </div>
        <details class="abs-rate">
          <summary>Optional absolute 1–5 (B)</summary>
          <div class="rate-row" id="scoresB"><span>B rating:</span></div>
        </details>
        <div class="skel-hint" id="skelHintB"></div>
      </section>
    </div>
    <div class="winner-row" id="winners">
      <button type="button" class="winner-btn" data-winner="a">A better</button>
      <button type="button" class="winner-btn" data-winner="tie">Tie</button>
      <button type="button" class="winner-btn" data-winner="b">B better</button>
    </div>
    <div class="rate-row">
      <label>Minutes <input id="minutes" type="number" min="0" step="0.5" style="width:5rem"/></label>
    </div>
    <label for="notes">Notes</label>
    <textarea id="notes" placeholder="Optional pedagogy / latex / topic flags"></textarea>
    <div class="nav">
      <button type="button" class="secondary" id="btnSkip">Skip</button>
      <button type="button" id="btnSubmit" disabled>Submit &amp; next</button>
    </div>
    <div class="coverage" id="coverage"></div>
    <div class="skel-hint" id="skelHint"></div>
  </div>
</main>
<div class="toast" id="toast"></div>
<script>
const STORAGE_KEY = "poly_live_rater_pair_v2";
const SKELETON_TYPES = {skel_types_js};
const MIN_TRAIN = {min_train};
const MIN_PAIRS = {min_pairs};
let types = [];
let current = null;
let currentWinner = null;
let currentScoreA = null;
let currentScoreB = null;

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

function campaignMode() {{
  return document.getElementById("campaign").value;
}}
function typeId() {{
  return (document.getElementById("typeFilter").value || "").trim();
}}
function sessionName() {{
  const raw = (document.getElementById("session").value || "").trim();
  if (raw) return raw;
  if (campaignMode() === "all_topics") return "all_topics";
  if (campaignMode() === "skeleton_deriv") return "skeleton_deriv";
  return null;
}}

function fillTypes(list) {{
  types = list || [];
  const dl = document.getElementById("typeList");
  dl.innerHTML = "";
  const prefer = new Set(SKELETON_TYPES);
  const ordered = [...types].sort((a,b) => {{
    const ap = prefer.has(a.type_id) ? 0 : 1;
    const bp = prefer.has(b.type_id) ? 0 : 1;
    return ap - bp || String(a.type_id).localeCompare(String(b.type_id));
  }});
  for (const t of ordered) {{
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
  let typePart = "";
  if (cov.by_generator) {{
    const gkeys = Object.keys(cov.by_generator).filter(k => cov.by_generator[k] > 0);
    if (gkeys.length)
      typePart += " · gens " + gkeys.slice(0, 8).map(k => k + "=" + cov.by_generator[k]).join(",");
  }}
  if (cov.by_type) {{
    const tkeys = Object.keys(cov.by_type).filter(k => cov.by_type[k] > 0);
    typePart += " · types " + tkeys.slice(0, 8).map(k => k.replace("calc_diff_", "") + "=" + cov.by_type[k]).join(",");
    if (tkeys.length > 8) typePart += "…";
  }}
  const modelBit = cov.model_ready
    ? (" · model ready abs=" + (cov.n_train || 0) + " pairs=" + (cov.n_pairs || 0))
    : (" · cold abs=" + (cov.n_train || 0) + "/" + (cov.min_train || MIN_TRAIN) +
       " pairs=" + (cov.n_pairs || 0) + "/" + (cov.min_pairs || MIN_PAIRS));
  const resetBit = cov.learning_reset ? " · reset (new gen rev)" : "";
  const revBit = cov.engine_rev ? (" · rev " + cov.engine_rev) : "";
  document.getElementById("coverage").textContent =
    "Rated " + (cov.n_ratings || 0) + " · " + parts.join(" · ") + typePart + modelBit + resetBit + revBit +
    (cov.dir ? " · " + cov.dir : "");
}}

function showPred(left, right) {{
  const el = document.getElementById("pred");
  const src = left || right;
  if (!src) {{
    el.className = "pred cold";
    el.textContent = "Model: —";
    return;
  }}
  if (src.model_ready) {{
    el.className = "pred";
    const bits = [];
    if (left && left.predicted_rating != null)
      bits.push("A " + Number(left.predicted_rating).toFixed(2) +
        (left.predicted_std != null ? " ±" + Number(left.predicted_std).toFixed(2) : ""));
    if (right && right.predicted_rating != null)
      bits.push("B " + Number(right.predicted_rating).toFixed(2) +
        (right.predicted_std != null ? " ±" + Number(right.predicted_std).toFixed(2) : ""));
    el.textContent = (bits.length ? ("Predicted: " + bits.join(" · ")) : (src.model_message || "Model ready")) +
      " · abs=" + (src.n_train || 0) + " pairs=" + (src.n_pairs || 0);
  }} else {{
    el.className = "pred cold";
    el.textContent = src.model_message ||
      ("Cold start: n/a until " + (src.min_pairs || MIN_PAIRS) + " pairs or " +
       (src.min_train || MIN_TRAIN) + " abs (have pairs=" + (src.n_pairs || 0) +
       ", abs=" + (src.n_train || 0) + ").");
  }}
}}

function skelBits(it) {{
  if (!it) return "";
  const sf = it.skeleton_features || {{}};
  const bits = [
    sf.generator ? ("gen " + sf.generator) : null,
    sf.form_id ? ("form " + sf.form_id) : null,
    sf.skeleton_kind ? ("kind " + sf.skeleton_kind) : null,
    sf.richness_band ? ("band " + sf.richness_band) : null,
    sf.n_applies != null ? ("n_applies " + sf.n_applies) : null,
    sf.degree_max != null ? ("deg " + sf.degree_max) : null,
    sf.nest_depth_expr != null ? ("nest " + sf.nest_depth_expr) : null,
  ].filter(Boolean);
  return bits.length ? ("Skeleton: " + bits.join(" · ")) : "";
}}

function itemMetaHtml(it) {{
  if (!it) return "";
  return [
    "<span>type <code>" + it.type_id + "</code></span>",
    "<span>D <code>" + it.difficulty + "</code></span>",
    "<span>bin <code>" + it.bin + "</code></span>",
    it.generator ? "<span>gen <code>" + it.generator + "</code></span>" : "",
    (it.metadata && it.metadata.skeleton_source) ? "<span>skel <code>" + it.metadata.skeleton_source + "</code></span>" : "",
    it.engine_rev ? "<span>rev <code>" + it.engine_rev + "</code></span>" : "",
    it.rating_id ? "<span>id <code>" + it.rating_id + "</code></span>" : ""
  ].filter(Boolean).join("");
}}

function fillPrompt(it, suffix) {{
  const latex = ((it && it.prompt_latex) || "").trim();
  const text = ((it && it.prompt_text) || "").trim();
  const rawPrompt = latex || text;
  document.getElementById("prompt" + suffix).innerHTML = wrapMath(rawPrompt);
  const note = document.getElementById("promptFallbackNote" + suffix);
  if (!latex && text) {{
    note.hidden = false;
    note.textContent = "prompt_latex is empty — showing prompt_text";
  }} else if (!latex && !text) {{
    note.hidden = false;
    note.textContent = "prompt_latex and prompt_text are empty";
  }} else {{
    note.hidden = true;
    note.textContent = "";
  }}
  document.getElementById("promptRaw" + suffix).textContent = rawPrompt || "(empty)";
  document.getElementById("answer" + suffix).innerHTML = wrapMath((it && (it.answer_latex || it.answer_text)) || "");
}}

function resetFlags() {{
  ["A", "B"].forEach(s => {{
    document.getElementById("flagTopicFit" + s).checked = false;
    document.getElementById("flagLatex" + s).checked = false;
    document.getElementById("flagBroken" + s).checked = false;
  }});
  document.getElementById("minutes").value = "";
  document.getElementById("notes").value = "";
  currentWinner = null;
  currentScoreA = null;
  currentScoreB = null;
  document.querySelectorAll("button.winner-btn").forEach(b => b.classList.remove("active"));
  document.querySelectorAll("button.score").forEach(b => b.classList.remove("active"));
  document.getElementById("sideA").classList.remove("chosen");
  document.getElementById("sideB").classList.remove("chosen");
}}

function showPair(payload) {{
  const left = payload && payload.left;
  const right = payload && payload.right;
  current = payload;
  resetFlags();
  document.getElementById("btnSubmit").disabled = !left || !right;
  if (!left || !right) {{
    document.getElementById("meta").innerHTML = "<em>No pair.</em>";
    showPred(null, null);
    return;
  }}
  document.getElementById("meta").innerHTML =
    "<span>pair <code>" + (payload.pair_id || "") + "</code></span>";
  document.getElementById("metaA").innerHTML = itemMetaHtml(left);
  document.getElementById("metaB").innerHTML = itemMetaHtml(right);
  fillPrompt(left, "A");
  fillPrompt(right, "B");
  document.getElementById("skelHintA").textContent = skelBits(left);
  document.getElementById("skelHintB").textContent = skelBits(right);
  showPred(left, right);
  document.querySelectorAll("details.answer").forEach(el => {{ el.open = false; }});
  renderMath();
  const prefs = loadPrefs();
  prefs.lastType = left.type_id;
  prefs.lastSession = sessionName();
  prefs.lastCampaign = campaignMode();
  prefs.lastPair = {{ pair_id: payload.pair_id }};
  savePrefs(prefs);
}}

async function refreshTypes() {{
  setStatus("Loading types…");
  const data = await api("GET", "/api/types");
  fillTypes(data.types || []);
  setStatus((data.types || []).length + " types");
}}

async function loadNext() {{
  const mode = campaignMode();
  if (mode === "single" && !typeId()) {{ setStatus("Enter a type_id", true); return; }}
  setStatus("Generating…");
  document.getElementById("btnNext").disabled = true;
  try {{
    const body = {{}};
    const sess = sessionName();
    if (sess) body.session = sess;
    if (mode === "all_topics" || mode === "skeleton_deriv") {{
      body.campaign = mode;
      if (typeId()) body.type_id = typeId();
    }} else {{
      body.type_id = typeId();
    }}
    const data = await api("POST", "/api/next", body);
    if (data.pair) showPair(data.pair);
    else if (data.item) showPair({{ pair_id: data.item.rating_id, left: data.item, right: data.item }});
    showCoverage(data.coverage);
    setStatus("Ready");
    toast("Next pair");
  }} catch (e) {{
    setStatus(String(e.message || e), true);
  }} finally {{
    document.getElementById("btnNext").disabled = false;
  }}
}}

function sideFlags(suffix, score) {{
  return {{
    topic_fit_ok: !document.getElementById("flagTopicFit" + suffix).checked,
    latex_ok: !document.getElementById("flagLatex" + suffix).checked,
    broken: document.getElementById("flagBroken" + suffix).checked,
    rating_1_to_5: score
  }};
}}

async function submit(skip) {{
  if (!current) return;
  if (!skip && !currentWinner) {{ setStatus("Pick A better, B better, or Tie", true); return; }}
  const minutesRaw = document.getElementById("minutes").value;
  const body = {{
    session: sessionName(),
    pair_id: current.pair_id,
    winner: skip ? null : currentWinner,
    minutes: minutesRaw === "" ? null : Number(minutesRaw),
    notes: document.getElementById("notes").value || null,
    left: sideFlags("A", currentScoreA),
    right: sideFlags("B", currentScoreB),
    skip: !!skip
  }};
  if (campaignMode() === "all_topics" || campaignMode() === "skeleton_deriv")
    body.campaign = campaignMode();
  else body.type_id = typeId() || (current.left && current.left.type_id);
  setStatus(skip ? "Skipping…" : "Saving…");
  try {{
    const data = await api("POST", "/api/submit", body);
    showCoverage(data.coverage);
    toast(skip ? "Skipped" : "Saved · refit");
    const prefs = loadPrefs();
    prefs.lastSubmit = {{ pair_id: body.pair_id, winner: body.winner, at: new Date().toISOString() }};
    savePrefs(prefs);
    await loadNext();
  }} catch (e) {{
    setStatus(String(e.message || e), true);
  }}
}}

function bindScores(rowId, assign) {{
  const scores = document.getElementById(rowId);
  for (let s = 1; s <= 5; s++) {{
    const b = document.createElement("button");
    b.type = "button";
    b.className = "score";
    b.dataset.score = String(s);
    b.textContent = String(s);
    b.addEventListener("click", () => {{
      assign(s);
      scores.querySelectorAll("button.score").forEach(x =>
        x.classList.toggle("active", Number(x.dataset.score) === s));
    }});
    scores.appendChild(b);
  }}
}}
bindScores("scoresA", (s) => {{ currentScoreA = s; }});
bindScores("scoresB", (s) => {{ currentScoreB = s; }});

document.querySelectorAll("button.winner-btn").forEach(b => {{
  b.addEventListener("click", () => {{
    currentWinner = b.dataset.winner;
    document.querySelectorAll("button.winner-btn").forEach(x =>
      x.classList.toggle("active", x.dataset.winner === currentWinner));
    document.getElementById("sideA").classList.toggle("chosen", currentWinner === "a");
    document.getElementById("sideB").classList.toggle("chosen", currentWinner === "b");
  }});
}});

document.getElementById("btnLoadTypes").addEventListener("click", () => refreshTypes().catch(e => setStatus(String(e.message||e), true)));
document.getElementById("btnNext").addEventListener("click", () => loadNext());
document.getElementById("btnSubmit").addEventListener("click", () => submit(false));
document.getElementById("btnSkip").addEventListener("click", () => submit(true));
document.getElementById("campaign").addEventListener("change", () => {{
  const prefs = loadPrefs();
  prefs.lastCampaign = campaignMode();
  savePrefs(prefs);
}});

document.addEventListener("keydown", (e) => {{
  if (e.target && (e.target.tagName === "TEXTAREA" || e.target.tagName === "INPUT" || e.target.tagName === "SELECT")) return;
  const k = (e.key || "").toLowerCase();
  if (k === "a" || k === "b" || k === "t") {{
    currentWinner = k === "t" ? "tie" : k;
    document.querySelectorAll("button.winner-btn").forEach(x =>
      x.classList.toggle("active", x.dataset.winner === currentWinner));
    document.getElementById("sideA").classList.toggle("chosen", currentWinner === "a");
    document.getElementById("sideB").classList.toggle("chosen", currentWinner === "b");
  }} else if (e.key === "Enter") {{
    submit(false);
  }}
}});

(async function init() {{
  const prefs = loadPrefs();
  if (prefs.lastCampaign) document.getElementById("campaign").value = prefs.lastCampaign;
  if (prefs.lastType) document.getElementById("typeFilter").value = prefs.lastType;
  if (prefs.lastSession) document.getElementById("session").value = prefs.lastSession;
  else if (campaignMode() === "all_topics") document.getElementById("session").value = "all_topics";
  else if (campaignMode() === "skeleton_deriv") document.getElementById("session").value = "skeleton_deriv";
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


def _session_from_request(body: dict[str, Any], qs: dict[str, list[str]]) -> LiveRatingSession | MultiTypeCampaign:
    type_id = (body.get("type_id") or (qs.get("type_id") or [None])[0] or "").strip() or None
    campaign = body.get("campaign")
    if campaign is None:
        campaign = (qs.get("campaign") or [None])[0]
    if campaign is not None:
        campaign = str(campaign).strip() or None
    session = body.get("session")
    if session is None:
        session = (qs.get("session") or [None])[0]
    if session is not None:
        session = str(session).strip() or None
    # Default browser open → all-topics when neither type nor campaign set.
    if not type_id and not campaign:
        campaign = ALL_TOPICS_CAMPAIGN
    return open_live_session(type_id, session=session, campaign=campaign)


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
                self._json(
                    200,
                    {
                        "types": types,
                        "n": len(types),
                        "skeleton_deriv_types": list(SKELETON_DERIV_TYPE_IDS),
                        "min_train": MIN_TRAIN,
                        "min_pairs": MIN_PAIRS,
                        "default_campaign": ALL_TOPICS_CAMPAIGN,
                    },
                )
                return
            if path == "/api/coverage":
                sess = _session_from_request({}, qs)
                self._json(200, sess.coverage())
                return
            if path == "/api/next":
                sess = _session_from_request({}, qs)
                difficulty = (qs.get("difficulty") or [None])[0]
                seed = (qs.get("seed") or [None])[0]
                pair_mode = (qs.get("pair") or ["1"])[0] != "0"
                kwargs: dict[str, Any] = {
                    "difficulty": float(difficulty) if difficulty is not None else None,
                    "seed": int(seed) if seed is not None else None,
                }
                if isinstance(sess, MultiTypeCampaign):
                    type_override = (qs.get("type_id") or [None])[0]
                    if type_override:
                        kwargs["type_id"] = type_override
                if pair_mode:
                    pair = sess.generate_next_pair(**kwargs)
                    self._json(200, {"pair": pair, "coverage": sess.coverage()})
                else:
                    item = sess.generate_next(**kwargs)
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
                pair_mode = body.get("pair", True)
                kwargs: dict[str, Any] = {
                    "difficulty": float(difficulty) if difficulty is not None else None,
                    "seed": int(seed) if seed is not None else None,
                }
                if isinstance(sess, MultiTypeCampaign):
                    # Optional pin; campaign still owns the session folder.
                    raw_tid = str(body.get("type_id") or "").strip()
                    if raw_tid and raw_tid not in {
                        SKELETON_DERIV_CAMPAIGN,
                        "__skeleton_deriv__",
                        ALL_TOPICS_CAMPAIGN,
                        "__all_topics__",
                    }:
                        kwargs["type_id"] = raw_tid
                if pair_mode:
                    pair = sess.generate_next_pair(**kwargs)
                    self._json(200, {"pair": pair, "coverage": sess.coverage()})
                else:
                    item = sess.generate_next(**kwargs)
                    self._json(200, {"item": item, "coverage": sess.coverage()})
                return
            if path == "/api/submit":
                sess = _session_from_request(body, {})
                minutes = body.get("minutes")
                result = sess.submit(
                    rating_id=body.get("rating_id"),
                    pair_id=body.get("pair_id"),
                    winner=body.get("winner"),
                    rating_1_to_5=body.get("rating_1_to_5"),
                    minutes=float(minutes) if minutes is not None and minutes != "" else None,
                    notes=body.get("notes"),
                    topic_fit_ok=body.get("topic_fit_ok"),
                    latex_ok=body.get("latex_ok"),
                    broken=body.get("broken"),
                    left=body.get("left") if isinstance(body.get("left"), dict) else None,
                    right=body.get("right") if isinstance(body.get("right"), dict) else None,
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
    sess = open_live_session(args.type_id, session=args.session, campaign=args.campaign)
    kwargs: dict[str, Any] = {
        "difficulty": args.difficulty,
        "seed": args.seed,
    }
    if isinstance(sess, MultiTypeCampaign) and args.type_id and args.type_id not in {
        SKELETON_DERIV_CAMPAIGN,
        "__skeleton_deriv__",
        ALL_TOPICS_CAMPAIGN,
        "__all_topics__",
    }:
        kwargs["type_id"] = args.type_id
    want_pair = not bool(getattr(args, "single", False))
    if want_pair:
        pair = sess.generate_next_pair(**kwargs)
        left = pair.get("left") or {}
        right = pair.get("right") or {}
        lite = {
            "pair_id": pair.get("pair_id"),
            "mode": "pair",
            "left": {
                "rating_id": left.get("rating_id"),
                "type_id": left.get("type_id"),
                "difficulty": left.get("difficulty"),
                "predicted_rating": left.get("predicted_rating"),
                "predicted_std": left.get("predicted_std"),
                "prompt_latex": (left.get("prompt_latex") or "")[:200],
            },
            "right": {
                "rating_id": right.get("rating_id"),
                "type_id": right.get("type_id"),
                "difficulty": right.get("difficulty"),
                "predicted_rating": right.get("predicted_rating"),
                "predicted_std": right.get("predicted_std"),
                "prompt_latex": (right.get("prompt_latex") or "")[:200],
            },
            "model_ready": left.get("model_ready"),
            "n_train": left.get("n_train"),
            "n_pairs": left.get("n_pairs"),
            "model_message": left.get("model_message"),
            "coverage": sess.coverage(),
        }
        print(json.dumps(lite, indent=2, ensure_ascii=False))
        return 0
    item = sess.generate_next(**kwargs)
    lite = {
        "rating_id": item["rating_id"],
        "type_id": item["type_id"],
        "difficulty": item["difficulty"],
        "bin": item["bin"],
        "seed": item["seed"],
        "predicted_rating": item.get("predicted_rating"),
        "predicted_std": item.get("predicted_std"),
        "model_ready": item.get("model_ready"),
        "n_train": item.get("n_train"),
        "n_pairs": item.get("n_pairs"),
        "model_message": item.get("model_message"),
        "skeleton_features": item.get("skeleton_features"),
        "prompt_latex": (item.get("prompt_latex") or "")[:200],
        "coverage": sess.coverage(),
    }
    print(json.dumps(lite, indent=2, ensure_ascii=False))
    return 0


def _cli_submit(args: argparse.Namespace) -> int:
    sess = open_live_session(args.type_id, session=args.session, campaign=args.campaign)
    result = sess.submit(
        rating_id=args.rating_id,
        pair_id=getattr(args, "pair_id", None),
        winner=getattr(args, "winner", None),
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
    parser = argparse.ArgumentParser(description="Live adaptive human-rating loop (pairwise Bayesian utility)")
    parser.add_argument("--host", default=HOST)
    parser.add_argument("--port", type=int, default=PORT)
    parser.add_argument("--list-types", action="store_true")
    parser.add_argument("--include-scaffolds", action="store_true")
    parser.add_argument("--next", action="store_true", help="CLI: generate next pair (default) or item")
    parser.add_argument("--single", action="store_true", help="CLI --next: one item instead of a pair")
    parser.add_argument("--submit", action="store_true", help="CLI: submit pair winner or rating")
    parser.add_argument("--coverage", action="store_true")
    parser.add_argument("--type-id", default=None)
    parser.add_argument(
        "--campaign",
        default=None,
        help=f"'{ALL_TOPICS_CAMPAIGN}' (default) or '{SKELETON_DERIV_CAMPAIGN}'",
    )
    parser.add_argument("--session", default=None)
    parser.add_argument("--difficulty", type=float, default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--rating-id", default=None)
    parser.add_argument("--pair-id", default=None)
    parser.add_argument("--winner", choices=["a", "b", "tie"], default=None)
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
        print(
            json.dumps(
                {
                    "n": len(types),
                    "types": types[:50],
                    "truncated": len(types) > 50,
                    "skeleton_deriv_types": list(SKELETON_DERIV_TYPE_IDS),
                    "default_campaign": ALL_TOPICS_CAMPAIGN,
                    "min_train": MIN_TRAIN,
                    "min_pairs": MIN_PAIRS,
                },
                indent=2,
            )
        )
        return

    if args.demo_policy:
        # Show that after stuffing one band, next prefers underfilled bins.
        fake = [{"difficulty": 8.0, "theta_requested": {"difficulty": 8.0}, "rating_1_to_5": 3}] * 4
        nxt = pick_next_difficulty(fake)
        print(json.dumps({"after_four_at_8": nxt, "expected_not_8": nxt != 8.0}, indent=2))
        return

    if args.coverage:
        if not args.type_id and not args.campaign:
            args.campaign = ALL_TOPICS_CAMPAIGN
        sess = open_live_session(args.type_id, session=args.session, campaign=args.campaign)
        print(json.dumps(sess.coverage(), indent=2))
        return

    if args.next:
        if not args.type_id and not args.campaign:
            args.campaign = ALL_TOPICS_CAMPAIGN
        raise SystemExit(_cli_next(args))

    if args.submit:
        if not args.type_id and not args.campaign:
            args.campaign = ALL_TOPICS_CAMPAIGN
        raise SystemExit(_cli_submit(args))

    katex_root = _ensure_katex_vendor()
    Handler.katex_root = katex_root
    print(f"Live ratings root: {LIVE_ROOT}", flush=True)
    print(
        f"Default campaign: {ALL_TOPICS_CAMPAIGN} "
        f"(min_pairs={MIN_PAIRS}, min_train={MIN_TRAIN})",
        flush=True,
    )
    print(f"Open http://{args.host}:{args.port}/", flush=True)
    if katex_root:
        print(f"KaTeX assets: {katex_root}", flush=True)
    ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
