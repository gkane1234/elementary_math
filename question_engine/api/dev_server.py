from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import question_engine.types  # noqa: F401
from question_engine.api.handler import handle_generate, handle_question_types


class DevAPIHandler(BaseHTTPRequestHandler):
    def _send(self, status: int, body: str):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path.rstrip("/").endswith("question-types"):
            status, _, body = handle_question_types()
            self._send(status, body)
            return
        self._send(404, json.dumps({"error": "Not found"}))

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8") if length else "{}"
        try:
            payload = json.loads(raw or "{}")
        except json.JSONDecodeError:
            self._send(400, json.dumps({"error": "Invalid JSON body"}))
            return

        if self.path.rstrip("/").endswith("generate"):
            status, _, body = handle_generate(payload)
            self._send(status, body)
            return
        self._send(404, json.dumps({"error": "Not found"}))

    def log_message(self, format, *args):
        return


def main():
    port = 5328
    server = HTTPServer(("127.0.0.1", port), DevAPIHandler)
    print(f"Dev API running at http://127.0.0.1:{port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
