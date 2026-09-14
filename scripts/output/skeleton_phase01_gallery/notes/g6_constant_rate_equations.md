# Notes — `write_rate` (`g6_constant_rate_equations`)

Also covers: `g6_constant_rate_equations`

Flags:

- `LOW_VARIETY`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Write $d=rt$ (or $t=d/r$, $r=d/t$) for a constant-rate trip, then evaluate.
- **D=0:** $d=r\cdot t$ with a named vehicle (bike/car/walk/bus/train).
- **High D (≈16–22):** Ask for time or rate; larger numbers.
- **Must not:** Bike-only Mad-Lib because old code was bike-only.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_sample_linear_equation=True`.

- **D=0 seed=101:** $\text{A bike travels at } 6 \text{ miles per hour. Write an equation for the distance } d \text{ after } 3 \text{ hours, then find } d.$ → $d = 6\cdot 3;\; d = 18$
- **D=0 seed=207:** $\text{A bike travels at } 6 \text{ miles per hour. Write an equation for the distance } d \text{ after } 3 \text{ hours, then find } d.$ → $d = 6\cdot 3;\; d = 18$
- **D=8 seed=101:** $\text{A bike travels at } 12 \text{ miles per hour and covers } 48 \text{ miles at a constant rate. Write an equation for the time } t \text{ in hours, then find } t.$ → $t = 48\div 12;\; t = 4$
- **D=8 seed=207:** $\text{A bike travels at } 11 \text{ miles per hour and covers } 88 \text{ miles at a constant rate. Write an equation for the time } t \text{ in hours, then find } t.$ → $t = 88\div 11;\; t = 8$
- **D=16 seed=101:** $\text{A bike travels at } 24 \text{ miles per hour and covers } 168 \text{ miles at a constant rate. Write an equation for the time } t \text{ in hours, then find } t.$ → $t = 168\div 24;\; t = 7$
- **D=16 seed=207:** $\text{A bike travels at } 22 \text{ miles per hour. Write an equation for the distance } d \text{ after } 7 \text{ hours, then find } d.$ → $d = 22\cdot 7;\; d = 154$
- **D=22 seed=101:** $\text{A bike travels at } 13 \text{ miles per hour and covers } 117 \text{ miles at a constant rate. Write an equation for the time } t \text{ in hours, then find } t.$ → $t = 117\div 13;\; t = 9$
- **D=22 seed=207:** $\text{A bike travels at } 13 \text{ miles per hour. Write an equation for the distance } d \text{ after } 11 \text{ hours, then find } d.$ → $d = 13\cdot 11;\; d = 143$

## Current default (same D/seeds)

- **D=0 seed=101:** $\text{Julian drives at }2\text{ miles per hour. Write an equation for the distance d after }6\text{ hours, then find d.}$ → $d = 2\cdot 6;\; d = 12$ — frame_id=write_rate, vehicle=car, steps=one
- **D=0 seed=207:** $\text{Casey rides a bus at }3\text{ miles per hour. Write an equation for the distance d after }3\text{ hours, then find d.}$ → $d = 3\cdot 3;\; d = 9$ — frame_id=write_rate, vehicle=bus, steps=one
- **D=8 seed=101:** $\text{Julian drives at }3\text{ miles per hour and covers }33\text{ miles at a constant rate. Write an equation for the time t in hours, then find t.}$ → $t = 33\div 3;\; t = 11$ — frame_id=write_rate, vehicle=car, steps=one
- **D=8 seed=207:** $\text{Casey rides a bus at }4\text{ miles per hour. Write an equation for the distance d after }4\text{ hours, then find d.}$ → $d = 4\cdot 4;\; d = 16$ — frame_id=write_rate, vehicle=bus, steps=one
- **D=16 seed=101:** $\text{Julian drives and covers }55\text{ miles in }11\text{ hours at a constant rate. Write an equation for the speed r in mph, then find r.}$ → $r = 55\div 11;\; r = 5$ — frame_id=write_rate, vehicle=car, steps=one
- **D=16 seed=207:** $\text{Casey rides a bus at }7\text{ miles per hour and covers }28\text{ miles at a constant rate. Write an equation for the time t in hours, then find t.}$ → $t = 28\div 7;\; t = 4$ — frame_id=write_rate, vehicle=bus, steps=one
- **D=22 seed=101:** $\text{Julian drives and covers }105\text{ miles in }21\text{ hours at a constant rate. Write an equation for the speed r in mph, then find r.}$ → $r = 105\div 21;\; r = 5$ — frame_id=write_rate, vehicle=car, steps=one
- **D=22 seed=207:** $\text{Casey rides a bus at }7\text{ miles per hour and covers }42\text{ miles at a constant rate. Write an equation for the time t in hours, then find t.}$ → $t = 42\div 7;\; t = 6$ — frame_id=write_rate, vehicle=bus, steps=one

## OpenStax examples + chapter/section cites

- **OpenStax Elementary Algebra 2e §2.6** — Jamal bike / Lindsay drove / Trinh walked / Megan bus / Aisha train — https://openstax.org/books/elementary-algebra-2e/pages/2-6-solve-a-formula-for-a-specific-variable

Local mining: `scripts/output/example_mining/` (EA 2e Ch. 2 / 6 / 7 / 8.7; PA 2e Ch. 3–6).

## Variety notes

**LOW_VARIETY** — old path is **bike-only** at every seed. Default rotates car/bus/bike/train (OpenStax richer than the old Mad-Lib).

## Limitations

- Flags: **LOW_VARIETY**.
- **LOW_VARIETY** — old path is **bike-only** at every seed. Default rotates car/bus/bike/train (OpenStax richer than the old Mad-Lib).
- Story variety thin (one Mad-Lib / single vehicle) vs OpenStax frames.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** SolveLinear one-step + `wp_packaging` write_rate frames (already wired).
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `G6_PA_INDEX.md`: `wp`
