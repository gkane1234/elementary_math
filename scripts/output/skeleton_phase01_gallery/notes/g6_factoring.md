# Notes — `g6_factoring` (`g6_factoring`)

- **Display name:** Factoring
- **Catalog chapter:** Grade 6 — Common Factors and Common Multiples
- **Generator key:** `g6_factoring`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** `LOW_VARIETY`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Factoring
- **D=0:** Prime factorization of a two-prime product ($10=2\cdot 5$).
- **High D (≈16–22):** Higher powers and three distinct primes ($360=2^3\cdot 3^2\cdot 5$).
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Factor.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `\text{Write the prime factorization of } 10` | `2 \cdot 5` | D=0 easy |
| 8 | 41 | `\text{Write the prime factorization of } 105` | `3 \cdot 5 \cdot 7` | mid |
| 16 | 41 | `\text{Write the prime factorization of } 225` | `3^{2} \cdot 5^{2}` | high D |
| 22 | 41 | `\text{Write the prime factorization of } 300` | `2^{2} \cdot 3 \cdot 5^{2}` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_factoring/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§2.5 Prime Factorization and the LCM** — https://openstax.org/books/prealgebra-2e/pages/2-5-prime-factorization-and-the-least-common-multiple | | |
| Ex 2.48: prime factorization of $48$ by factor tree; Ex 2.50: $120$ by ladder. | | |
| OpenStax Prealgebra 2e **§2.4 Find Multiples and Factors** also lists *all* factors / prime vs composite / divisibility — we do not. | | |

## Variety notes / UNCLEAR flag

**LOW_VARIETY** vs OpenStax 2.4+2.5: only 'write the prime factorization'. Missing: all factor pairs, prime/composite, divisibility tests (Ex 2.40–2.45).

## Limitations

- Flags: **UNCLEAR**, **LOW_VARIETY**.
- **LOW_VARIETY** vs OpenStax 2.4+2.5: only 'write the prime factorization'. Missing: all factor pairs, prime/composite, divisibility tests (Ex 2.40–2.45).

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse existing **number** `g6_factoring`. Do not invent a poly-GCF engine (that's A1). Optional extra 2.4 modes later.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
