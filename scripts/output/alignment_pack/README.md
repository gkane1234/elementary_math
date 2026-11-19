# Published vs generated

Open `index.html` (or `spotlight.html` for a short visual pass).

632 wired leaves. Verdict counts: {"off": 182, "partial": 387, "weak_reference": 12, "close": 51}.
Visual leaves (name or a generated figure): 262.

## What a row is

- **Published:** two items at easy, medium, and hard when the source has an exercise ladder
  (OpenStax section order, or Open Up practice-problem order). Illustrative Mathematics
  geometry tasks are a task set, not a numbered ladder; the note says so.
- **Generated:** live `_generate_for_type` at easy / medium / hard, seeds 101 and 207,
  with diagrams and graph metadata turned on.
- **Verdict:** `close`, `partial`, `off`, `weak_reference`, or `generate_failed`.
  Hard must stay on the same skill. Fractions, negatives, and larger coefficients
  count as earlier prerequisites.

## Sources (consulted 2026-11-19)

| Source | License | Used for |
| --- | --- | --- |
| OpenStax Prealgebra, Elementary Algebra, Intermediate Algebra, Precalculus, Calculus Volumes 1–3 | CC BY-NC-SA 4.0 | Algebra, prealgebra, precalculus, calculus, and computational geometry |
| Open Up Resources Grade 6 (Illustrative Mathematics lessons) | CC BY 4.0 (Open Up Resources and Illustrative Mathematics) | Grade 6, including hanger, tape, area, and data figures |
| Illustrative Mathematics task PDFs | CC BY-NC-SA 4.0 (Illustrative Mathematics) | Geometry figures and proofs, and a fallback when an OpenStax section match is weak |

Foundations leaves have no `type_id`, so they are listed and not generated.

Regenerate:

```
QE_LOG_GENERATED=0 PYTHONPATH=. python scripts/build_alignment_pack.py
```

Downloaded pages and PDFs stay in `textbooks/alignment_cache/` (gitignored). The HTML pack quotes short excerpts and stores the figures it shows.
