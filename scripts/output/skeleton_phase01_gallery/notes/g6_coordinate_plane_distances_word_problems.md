# `g6_coordinate_plane_distances_word_problems` — Coordinate plane distances, word problems

> RED HEADER: **UNCLEAR** · **LOW_VARIETY**
>
> Ship samples anyway. Implementation must not treat a green checkbox as success if the old stem is a stub or a single template.

Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0:** short story, two map-like points that share a street (axis-aligned), ask “how many blocks / units apart?” Small positives.

**High D:** still H/V distance in a story (park, school, two buildings). OpenStax-style frames: different settings, not bigger coordinates only. Do **not** use Pythagorean.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22, `include_answer_key=True`, seeds 101 and 202. Default path **is** the old path (these leaves are not on equation/poly skeletons). One sample per D below (seed 101).

| D | Prompt (latex) | Answer |
|--:|----------------|--------|
| 0 | `$\text{Point A is at (4, -2) and point B is at (11, 3) on a coordinate plane. How far apart are the points in units?}$` | `$9$` |
| 8 | `$\text{Point A is at (4, -2) and point B is at (11, 3) on a coordinate plane. How far apart are the points in units?}$` | `$9$` |
| 16 | `$\text{Point A is at (4, -2) and point B is at (11, 3) on a coordinate plane. How far apart are the points in units?}$` | `$9$` |
| 22 | `$\text{Point A is at (4, -2) and point B is at (11, 3) on a coordinate plane. How far apart are the points in units?}$` | `$9$` |

Second seed (202) at D=0 and D=22:

- D=0: `$\text{Point A is at (1, 5) and point B is at (7, 11) on a coordinate plane. How far apart are the points in units?}$` → `$8$`
- D=22: `$\text{Point A is at (1, 5) and point B is at (7, 11) on a coordinate plane. How far apart are the points in units?}$` → `$8$`

## OpenStax examples + chapter/section

No OpenStax Prealgebra word-problem section for coordinate distance. **§11.1** has a campus map (grid sections 2B, 4D) — qualitative location, not distance.

IM Grade 6 Unit 7 has “map” distance along a grid.

**UNCLEAR:** old live samples are not stories. They dump `Point A is at (4, -2) and point B is at (11, 3)… How far apart…` and the points are **not** axis-aligned, while the skill is G6 axis-aligned distance. Answer `9` is neither `|Δx|` (7) nor `|Δy|` (5) nor Euclidean. Treat old path as a stub to replace with OpenStax/IM **frames**, not as gold math.

## Variety notes

**LOW_VARIETY:** seed 101 is the same prompt at D=0, 8, 16, and 22; seed 202 likewise. Two templates total. Difficulty setting is ignored.

## Limitations

- Flags: **UNCLEAR**, **LOW_VARIETY**.
- **LOW_VARIETY:** seed 101 is the same prompt at D=0, 8, 16, and 22; seed 202 likewise. Two templates total. Difficulty setting is ignored.
- Weak / missing OpenStax chapter match for this leaf.

## Proposed engine (proposal only)

WP packaging on a coordinate-distance core (not SolveLinear). Several map/city frames; force axis-aligned points. Do not copy the old diagonal stub.

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
