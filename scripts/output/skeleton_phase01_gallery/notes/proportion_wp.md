# Notes — `proportion_wp` (`pa_proportions_word_problems`)

Also covers: `pa_proportions_word_problems`

Flags:

- `UNCLEAR`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Scale a recipe / unit rate / calories / dosage with a proportion — story, not $a/b=x/c$ dumped.
- **D=0:** One of: recipe, unit-rate cost, calories, dosage. Small integers.
- **High D (≈16–22):** Same frames; harder numbers; unknown not dumped as algebra.
- **Must not:** “uses a proportion $a/b=x/c$ to scale a recipe”.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_sample_linear_equation=True`.

- **D=0 seed=101:** $\text{Sam uses a proportion } \frac{2}{3} = \frac{x}{4} \text{ to scale a recipe. Find } x.$ → $x = \frac{8}{3}$
- **D=0 seed=207:** $\text{Alex uses a proportion } \frac{2}{3} = \frac{x}{4} \text{ to scale a recipe. Find } x.$ → $x = \frac{8}{3}$
- **D=8 seed=101:** $\text{Riley uses a proportion } \frac{4}{10} = \frac{x - 1}{6} \text{ to scale a recipe. Find } x.$ → $x = \frac{17}{5}$
- **D=8 seed=207:** $\text{Jordan uses a proportion } \frac{12}{28} = \frac{x + 1}{9} \text{ to scale a recipe. Find } x.$ → $x = \frac{20}{7}$
- **D=16 seed=101:** $\text{Riley uses a proportion } \frac{24}{60} = \frac{x + 1}{10} \text{ to scale a recipe. Find } x.$ → $x = 3$
- **D=16 seed=207:** $\text{Jordan uses a proportion } \frac{24}{56} = \frac{x + 1}{15} \text{ to scale a recipe. Find } x.$ → $x = \frac{38}{7}$
- **D=22 seed=101:** $\text{Riley uses a proportion } \frac{32}{80} = \frac{x + 1}{12} \text{ to scale a recipe. Find } x.$ → $x = \frac{19}{5}$
- **D=22 seed=207:** $\text{Jordan uses a proportion } \frac{72}{168} = \frac{x + 1}{21} \text{ to scale a recipe. Find } x.$ → $x = 8$

## Current default (same D/seeds)

- **D=0 seed=101:** $\text{A pediatrician prescribes 5 milliliters of medicine for every 25 pounds of a child's weight. If Zara weighs 75 pounds, how many milliliters should be prescribed?}$ → $15\text{ ml}$ — frame_id=prop_dosage
- **D=0 seed=207:** $\text{A pediatrician prescribes 15 milliliters of medicine for every 5 pounds of a child's weight. If Lena weighs 15 pounds, how many milliliters should be prescribed?}$ → $45\text{ ml}$ — frame_id=prop_dosage
- **D=8 seed=101:** $\text{Zara's recipe for 4 dozen cookies uses 28 cups of flour. How many cups are needed for 9 dozen cookies?}$ → $63\text{ cups}$ — frame_id=prop_recipe
- **D=8 seed=207:** $\text{If 2 folders cost \$8, how much do 4 folders cost at the same rate?}$ → $\16$ — frame_id=prop_unit_rate
- **D=16 seed=101:** $\text{If 4 cups cost \$20, how much do 9 cups cost at the same rate?}$ → $\45$ — frame_id=prop_unit_rate
- **D=16 seed=207:** $\text{A 2-ounce chocolate shake has 36 calories. How many calories are in a 4-ounce chocolate shake?}$ → $72\text{ calories}$ — frame_id=prop_calories
- **D=22 seed=101:** $\text{A pediatrician prescribes 5 milliliters of medicine for every 25 pounds of a child's weight. If Kim weighs 75 pounds, how many milliliters should be prescribed?}$ → $15\text{ ml}$ — frame_id=prop_dosage
- **D=22 seed=207:** $\text{A pediatrician prescribes 15 milliliters of medicine for every 5 pounds of a child's weight. If Lena weighs 30 pounds, how many milliliters should be prescribed?}$ → $90\text{ ml}$ — frame_id=prop_dosage

## OpenStax examples + chapter/section cites

- **OpenStax Elementary Algebra 2e §8.7** — Recipe #406 oatmeal cookies; unit-rate cost; calories; acetaminophen dosage — https://openstax.org/books/elementary-algebra-2e/pages/8-7-solve-proportion-and-similar-figure-applications

Local mining: `scripts/output/example_mining/` (EA 2e Ch. 2 / 6 / 7 / 8.7; PA 2e Ch. 3–6).

## Variety notes

**UNCLEAR** — old path dumps a proportion into a fake recipe sentence. Default rotates EA §8.7 `prop_recipe`, `prop_calories`, `prop_unit_rate`, and `prop_dosage` across seeds and D.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** ProportionRate + `wp_packaging` (wired; recipe/calories rotate).
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `G6_PA_INDEX.md`: `wp`
