# Notes — `a2_trigonometry_arc_length_and_sector_area`

- **Display name:** Arc length and sector area
- **Category:** Algebra 2 — Trigonometry
- **Generator:** `geo_arc_sector`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice arc length and sector area (catalog: geo_arc_sector).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{A circle has radius } 12\text{ cm} \text{ and a central angle of } 60^\circ.\ \text{Find the sector area.}$ | $\frac{60}{360} \cdot \pi \cdot 12^{2}$ | — |
| 0 | 207 | $\text{A circle has radius } 11\text{ cm} \text{ and a central angle of } 180^\circ.\ \text{Find the arc length.}$ | $\frac{180}{360} \cdot 2\pi \cdot 11$ | — |
| 8 | 101 | $\text{A circle has radius } 12\text{ cm} \text{ and a central angle of } 60^\circ.\ \text{Find the sector area.}$ | $\frac{60}{360} \cdot \pi \cdot 12^{2}$ | — |
| 8 | 207 | $\text{A circle has radius } 11\text{ cm} \text{ and a central angle of } 180^\circ.\ \text{Find the arc length.}$ | $\frac{180}{360} \cdot 2\pi \cdot 11$ | — |
| 16 | 101 | $\text{A circle has radius } 12\text{ cm} \text{ and a central angle of } 60^\circ.\ \text{Find the sector area.}$ | $\frac{60}{360} \cdot \pi \cdot 12^{2}$ | — |
| 16 | 207 | $\text{A circle has radius } 11\text{ cm} \text{ and a central angle of } 180^\circ.\ \text{Find the arc length.}$ | $\frac{180}{360} \cdot 2\pi \cdot 11$ | — |
| 22 | 101 | $\text{A circle has radius } 12\text{ cm} \text{ and a central angle of } 60^\circ.\ \text{Find the sector area.}$ | $\frac{60}{360} \cdot \pi \cdot 12^{2}$ | — |
| 22 | 207 | $\text{A circle has radius } 11\text{ cm} \text{ and a central angle of } 180^\circ.\ \text{Find the arc length.}$ | $\frac{180}{360} \cdot 2\pi \cdot 11$ | — |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| College Algebra 2e §5.1 | https://openstax.org/books/college-algebra-2e/pages/5-1-angles | 5.1 Angles |
| College Algebra 2e §7.1 | https://openstax.org/books/college-algebra-2e/pages/7-1-right-triangle-trigonometry | 7.1 Right Triangle Trigonometry |
| College Algebra 2e §7.2 | https://openstax.org/books/college-algebra-2e/pages/7-2-non-right-triangles-law-of-sines | 7.2 Non-right Triangles: Law of Sines |

Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.

## Variety notes / UNCLEAR flag

Not a WP leaf unless the generator is story-based. Algebra shapes follow old path samples above.

## Limitations

- **Difficulty scaling:** D-scaling may be flat — D=0 and D=16 prompts look identical in notes samples.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Existing `geo_arc_sector` hand path until a skeleton exists.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `geo_arc_sector`; equations/WP agent owns solve/WP siblings._
