# `direct_inverse_variation` — Direct and inverse variation

> **Shipped VariationEq** — was inverse-only / D-flat; now direct+inverse packaging (EA §8.9). Opt out: `use_legacy_variation=True`.

- **Course:** Algebra 1
- **Category:** Algebra 1 — Direct and inverse variation
- **Generator:** `direct_inverse_variation`
- **Already on skeleton?** yes (`VariationEq` / variation_packaging)
- **Opt-out:** `use_legacy_variation=True` (old DirectVariationFramework path)

## What the question should look like (D=0 vs high D)

- **Skill:** Write $y=kx$ or $y=k/x$ (and story forms $d=kt$, $C=kn$, $P=k/V$).
- **D=0:** Direct or inverse with small $k$; rate story unlocked early.
- **High D:** Larger $k$; cost / pressure frames at higher format tier.
- **Must not:** Inverse-only Mad-Lib; joint variation; dump “the equation is …”.

## What old path actually produced (legacy / opt-out)

Live `_generate_for_type` with `use_legacy_variation=True` (seeds 101 and 207) — **inverse-only, flat across D**.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | If $y$ varies inversely with $x$ and $y=\frac{5}{6}$ when $x=6$, write the equation. | $y=\frac{5}{x}$ | inverse only |
| 0 | 207 | Write an inverse variation equation with $k=12$. | $y=\frac{12}{x}$ | inverse only |
| 8–22 | 101/207 | same inverse shapes | same | D-flat |

## Current default (VariationEq packaging)

Live `_generate_for_type` default (no opt-out). Fixed seeds 101/207 can land inverse; rotate seeds for direct/rate.

| D | seed | frame_id | prompt (abbrev) | answer |
|---|------|----------|-----------------|--------|
| 0 | 101 | `var_inverse_k` | Write inverse with $k=5$ | $y=\frac{5}{x}$ |
| 0 | 207 | `var_inverse_point` | Inverse; $y=\frac{3}{2}$ when $x=2$ | $y=\frac{3}{x}$ |
| 0 | 102 | `var_direct_rate` | Name travels … write $d$ as function of $t$ | $d=kt$ |
| 0 | 116 | `var_direct_point` | Direct; $y=8$ when $x=4$ | $y=2x$ |
| 16 | 101 | `var_inverse_k` | Write inverse with $k=9$ | $y=\frac{9}{x}$ |

Across 30 seeds at D=0: both `direct` and `inverse`; frames include `var_direct_k`, `var_direct_point`, `var_direct_rate`, `var_inverse_k`, `var_inverse_point`.

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 8.9 Use Direct and Inverse Variation

- https://openstax.org/books/elementary-algebra-2e/pages/8-9-use-direct-and-inverse-variation
- Shapes: given-$k$ and given-point direct/inverse; story rate/cost; pressure inverse.

## Variety notes

Default rotates direct (k, point, rate, cost) and inverse (k, point, pressure). Legacy inverse-only path via `use_legacy_variation=True`.

## Limitations

- Shipped: VariationEq packaging (direct + inverse + rate/cost frames). Opt out: `use_legacy_variation=True`.
- LIMITATIONS: EA §8.9 story density still thinner than OpenStax worked examples (calories, gallons, beam load); joint variation not in scope.
- D scaling is numeric_tier / format_tier unlocks (cost, pressure), not coefficient inflation alone.
- Fixed gallery seeds can look inverse-heavy — variety is across seeds, not within one seed.

## Proposed engine (reuse vs new)

**Shipped:** `sample_variation_packaged` via `primitive_a2._variation` (same as A2 alias). Do not re-bind `DirectVariationFramework` on the A1 type module.
