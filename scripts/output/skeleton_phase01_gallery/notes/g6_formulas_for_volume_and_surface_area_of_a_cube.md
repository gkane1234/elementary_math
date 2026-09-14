# `g6_formulas_for_volume_and_surface_area_of_a_cube` — Formulas for volume and surface area of a cube

> RED HEADER: **LOW_VARIETY**
>
> Ship samples anyway. Implementation must not treat a green checkbox as success if the old stem is a stub or a single template.

Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0:** `Find the volume of a cube with side 2 cm` or surface area with side 5; `V=s^3` / `S=6s^2`; tiny s.

**High D:** larger integer side. Still a **cube**, not a general rectangular solid (OpenStax 9.6 also has `V=LWH` — that could be a later unlock on this leaf or a skip).

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22, `include_answer_key=True`, seeds 101 and 202. Default path **is** the old path (these leaves are not on equation/poly skeletons). One sample per D below (seed 101).

| D | Prompt (latex) | Answer |
|--:|----------------|--------|
| 0 | `$\text{Find the surface area of a cube with side } 6\text{ cm}.$` | `$216\text{ cm}^{2}$` |
| 8 | `$\text{Find the surface area of a cube with side } 8\text{ cm}.$` | `$384\text{ cm}^{2}$` |
| 16 | `$\text{Find the surface area of a cube with side } 13\text{ cm}.$` | `$1014\text{ cm}^{2}$` |
| 22 | `$\text{Find the surface area of a cube with side } 14\text{ cm}.$` | `$1176\text{ cm}^{2}$` |

Second seed (202) at D=0 and D=22:

- D=0: `$\text{Find the volume of a cube with side } 5\text{ cm}.$` → `$125\text{ cm}^{3}$`
- D=22: `$\text{Find the surface area of a cube with side } 12\text{ cm}.$` → `$864\text{ cm}^{2}$`

## OpenStax examples + chapter/section

**Prealgebra 2e §9.6**: cube as special rectangular solid; `V=s^3`, `S=6s^2`. Also rectangular crate `V=LWH` and paint-the-crate SA. Spheres/cylinders/cones in the same section are **not G6** for this catalog leaf.

## Variety notes

**LOW_VARIETY:** only cube V or SA; difficulty = bigger `s`. No missing-side (`V` given, find `s`), no rectangular non-cube. D=8–22 in this pack were mostly surface area.

## Limitations

- Flags: **LOW_VARIETY**.
- **LOW_VARIETY:** only cube V or SA; difficulty = bigger `s`. No missing-side (`V` given, find `s`), no rectangular non-cube. D=8–22 in this pack were mostly surface area.

## Proposed engine (proposal only)

geometry_basic (`geo_solid_volume_surface`) cube mode. Optional later: rectangular solid `LWH` as a real structure unlock (OpenStax 9.6), not a metadata pad.

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
