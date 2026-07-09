import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import question_engine.types  # noqa: F401
from question_engine.api.handler import handle_generate, handle_question_types


def main() -> int:
    if len(sys.argv) < 2:
        print(json.dumps({"error": "command required"}))
        return 1

    command = sys.argv[1]
    if command == "question-types":
        _, _, body = handle_question_types()
        print(body)
        return 0

    if command == "generate":
        payload = json.loads(sys.stdin.read() or "{}")
        status, _, body = handle_generate(payload)
        print(body)
        return 0 if status == 200 else 1

    print(json.dumps({"error": f"unknown command: {command}"}))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
