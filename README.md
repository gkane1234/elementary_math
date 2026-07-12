# Math Worksheet Generator

Generate printable math worksheets from randomized questions.

## Phase 1 MVP

- Quadratic factoring worksheets
- Schema-driven settings UI
- KaTeX preview
- Browser print-to-PDF export
- Python question engine + serverless API

## Local development

Open two terminals from the project root.

**Terminal 1 — Python API**

```powershell
python -m question_engine.dev_server
```

**Terminal 2 — Next.js frontend**

```powershell
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

In development, Next.js rewrites `/api/*` requests to the Python dev server on port `5328`.

## Test the Python engine directly

```powershell
python -m question_engine.cli question-types
```

```powershell
echo '{"type_id":"quadratic_factoring","settings":{"count":3,"include_answer_key":true}}' | python -m question_engine.cli generate
```

## Deploy to Vercel

This app uses **Vercel Services** (Next.js frontend + FastAPI Python API).

1. Push this repo to GitHub
2. Import the project in Vercel
3. In **Project Settings → General → Framework Preset**, choose **Services**
4. Deploy

Python API entrypoint: [`backend/main.py`](backend/main.py)  
Routing is configured in [`vercel.json`](vercel.json) (`/api/generate` and `/api/question-types` → Python).

## Project layout

- [`packages/polynomial_core/`](packages/polynomial_core/) — extracted polynomial library
- [`question_engine/`](question_engine/) — question models, registry, generators
- [`api/`](api/) — Vercel Python serverless endpoints
- [`app/`](app/) — Next.js UI
- [`components/`](components/) — settings form, preview, PDF export

See [`ARCHITECTURE.md`](ARCHITECTURE.md) for the full plan, including Stripe integration in Phase 2.
