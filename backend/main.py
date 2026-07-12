"""FastAPI entrypoint for Vercel Services (Python worksheet API)."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import Response

import question_engine.types  # noqa: F401 — register question types
from question_engine.api_handler import handle_generate, handle_question_types

app = FastAPI(title="Elementary Math API")


def _from_handler(status: int, headers: dict[str, str], body: str) -> Response:
    return Response(
        content=body,
        status_code=status,
        media_type=headers.get("Content-Type", "application/json"),
    )


@app.post("/api/generate")
async def generate(request: Request) -> Response:
    payload = await request.json()
    return _from_handler(*handle_generate(payload))


@app.get("/api/question-types")
async def question_types() -> Response:
    return _from_handler(*handle_question_types())
