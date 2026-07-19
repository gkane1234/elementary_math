#!/usr/bin/env python3
"""Tiny local debug UI for difficulty_knobs.json.

Usage:
  python scripts/difficulty_knobs_server.py
  open http://127.0.0.1:8765/

GET  /           → HTML editor
GET  /api/knobs  → JSON
PUT  /api/knobs  → replace whole JSON body
POST /api/knobs  → { "updates": { "path.to.key": value } } partial apply
POST /api/reload → re-read from disk into process cache
"""

from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from question_engine.frameworks.primitives import difficulty_knobs as dk  # noqa: E402

HOST = "127.0.0.1"
PORT = 8765

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>Difficulty knobs (debug)</title>
<style>
  :root { --bg:#0f1419; --card:#1a2332; --fg:#e7ecf3; --muted:#8b9bb4; --accent:#5b9fd4; --ok:#3d9a6a; }
  * { box-sizing: border-box; }
  body { font-family: ui-sans-serif, system-ui, sans-serif; background: var(--bg); color: var(--fg); margin: 0; padding: 1.25rem 1.5rem 3rem; }
  h1 { font-size: 1.25rem; font-weight: 600; margin: 0 0 .25rem; }
  p.sub { color: var(--muted); margin: 0 0 1.25rem; font-size: .9rem; }
  .toolbar { display: flex; gap: .5rem; flex-wrap: wrap; margin-bottom: 1rem; align-items: center; }
  button, .file { background: var(--accent); color: #041018; border: 0; border-radius: 6px; padding: .45rem .85rem; font-weight: 600; cursor: pointer; font-size: .85rem; }
  button.secondary { background: #2a3548; color: var(--fg); }
  button:disabled { opacity: .5; cursor: wait; }
  #status { color: var(--muted); font-size: .85rem; }
  #status.ok { color: var(--ok); }
  #status.err { color: #e07070; }
  table { width: 100%; border-collapse: collapse; background: var(--card); border-radius: 8px; overflow: hidden; }
  th, td { text-align: left; padding: .45rem .65rem; border-bottom: 1px solid #2a3548; font-size: .85rem; }
  th { color: var(--muted); font-weight: 500; }
  tr:hover td { background: #1f2b3d; }
  input[type=number], input[type=text] { width: 100%; max-width: 14rem; background: #0f1419; color: var(--fg); border: 1px solid #2a3548; border-radius: 4px; padding: .3rem .45rem; }
  input[type=checkbox] { transform: scale(1.15); }
  code.path { font-size: .78rem; color: #a8c5e2; }
  details { margin-top: 1.25rem; }
  summary { cursor: pointer; color: var(--muted); }
  textarea { width: 100%; min-height: 16rem; background: #0f1419; color: var(--fg); border: 1px solid #2a3548; border-radius: 6px; padding: .75rem; font-family: ui-monospace, monospace; font-size: .78rem; }
</style>
</head>
<body>
  <h1>Difficulty knobs</h1>
  <p class="sub">Source: <code>question_engine/frameworks/primitives/difficulty_knobs.json</code> — edits save to disk and reload the Python cache.</p>
  <div class="toolbar">
    <button id="reload">Reload from disk</button>
    <button id="save" class="secondary">Save changes</button>
    <span id="status"></span>
  </div>
  <table>
    <thead><tr><th>Path</th><th>Value</th></tr></thead>
    <tbody id="rows"></tbody>
  </table>
  <details>
    <summary>Raw JSON</summary>
    <textarea id="raw" spellcheck="false"></textarea>
    <div class="toolbar" style="margin-top:.5rem">
      <button id="saveRaw">Save raw JSON</button>
    </div>
  </details>
<script>
let knobs = {};
let flat = [];

async function api(method, path, body) {
  const opts = { method, headers: { 'Content-Type': 'application/json' } };
  if (body !== undefined) opts.body = JSON.stringify(body);
  const r = await fetch(path, opts);
  const text = await r.text();
  let data;
  try { data = JSON.parse(text); } catch { data = { error: text }; }
  if (!r.ok) throw new Error(data.error || r.statusText);
  return data;
}

function setStatus(msg, cls) {
  const el = document.getElementById('status');
  el.textContent = msg;
  el.className = cls || '';
}

function render() {
  const tb = document.getElementById('rows');
  tb.innerHTML = '';
  for (const row of flat) {
    const tr = document.createElement('tr');
    const tdP = document.createElement('td');
    tdP.innerHTML = '<code class="path">' + row.path + '</code>';
    const tdV = document.createElement('td');
    let input;
    if (row.type === 'bool') {
      input = document.createElement('input');
      input.type = 'checkbox';
      input.checked = !!row.value;
      input.dataset.path = row.path;
      input.dataset.type = 'bool';
    } else if (row.type === 'string_list') {
      input = document.createElement('input');
      input.type = 'text';
      input.value = (row.value || []).join(', ');
      input.dataset.path = row.path;
      input.dataset.type = 'string_list';
    } else {
      input = document.createElement('input');
      input.type = 'number';
      input.step = 'any';
      input.value = row.value;
      input.dataset.path = row.path;
      input.dataset.type = 'number';
    }
    tdV.appendChild(input);
    tr.appendChild(tdP);
    tr.appendChild(tdV);
    tb.appendChild(tr);
  }
  document.getElementById('raw').value = JSON.stringify(knobs, null, 2);
}

function collectUpdates() {
  const updates = {};
  document.querySelectorAll('#rows input').forEach(inp => {
    const path = inp.dataset.path;
    const type = inp.dataset.type;
    if (type === 'bool') updates[path] = inp.checked;
    else if (type === 'string_list') updates[path] = inp.value.split(',').map(s => s.trim()).filter(Boolean);
    else {
      const v = parseFloat(inp.value);
      updates[path] = Number.isFinite(v) ? v : inp.value;
    }
  });
  return updates;
}

async function load() {
  setStatus('Loading…');
  const data = await api('GET', '/api/knobs');
  knobs = data.knobs;
  flat = data.flat;
  render();
  setStatus('Loaded', 'ok');
}

document.getElementById('reload').onclick = async () => {
  try {
    await api('POST', '/api/reload');
    await load();
  } catch (e) { setStatus(String(e.message || e), 'err'); }
};

document.getElementById('save').onclick = async () => {
  try {
    setStatus('Saving…');
    const data = await api('POST', '/api/knobs', { updates: collectUpdates() });
    knobs = data.knobs;
    flat = data.flat;
    render();
    setStatus('Saved to disk', 'ok');
  } catch (e) { setStatus(String(e.message || e), 'err'); }
};

document.getElementById('saveRaw').onclick = async () => {
  try {
    setStatus('Saving raw…');
    const parsed = JSON.parse(document.getElementById('raw').value);
    const data = await api('PUT', '/api/knobs', parsed);
    knobs = data.knobs;
    flat = data.flat;
    render();
    setStatus('Raw JSON saved', 'ok');
  } catch (e) { setStatus(String(e.message || e), 'err'); }
};

load().catch(e => setStatus(String(e.message || e), 'err'));
</script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: bytes, content_type: str = "application/json") -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, code: int, payload: dict) -> None:
        self._send(code, json.dumps(payload).encode("utf-8"))

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw.decode("utf-8") or "{}")

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path in {"/", "/index.html"}:
            self._send(200, HTML.encode("utf-8"), "text/html; charset=utf-8")
            return
        if path == "/api/knobs":
            data = dk.load_knobs(force=True)
            self._json(
                200,
                {
                    "path": str(dk.knobs_path()),
                    "knobs": data,
                    "flat": dk.flatten_knobs(data),
                },
            )
            return
        self._json(404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        try:
            if path == "/api/reload":
                data = dk.reload_knobs()
                self._json(200, {"ok": True, "knobs": data, "flat": dk.flatten_knobs(data)})
                return
            if path == "/api/knobs":
                body = self._read_json()
                updates = body.get("updates") or {}
                data = dk.apply_flat_updates(updates)
                self._json(200, {"ok": True, "knobs": data, "flat": dk.flatten_knobs(data)})
                return
            self._json(404, {"error": "not found"})
        except Exception as exc:  # noqa: BLE001
            self._json(400, {"error": str(exc)})

    def do_PUT(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        try:
            if path == "/api/knobs":
                body = self._read_json()
                if not isinstance(body, dict):
                    raise ValueError("body must be a JSON object")
                dk.save_knobs(body)
                data = dk.reload_knobs()
                self._json(200, {"ok": True, "knobs": data, "flat": dk.flatten_knobs(data)})
                return
            self._json(404, {"error": "not found"})
        except Exception as exc:  # noqa: BLE001
            self._json(400, {"error": str(exc)})

    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


def main() -> None:
    print(f"Difficulty knobs file: {dk.knobs_path()}")
    print(f"Open http://{HOST}:{PORT}/")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
