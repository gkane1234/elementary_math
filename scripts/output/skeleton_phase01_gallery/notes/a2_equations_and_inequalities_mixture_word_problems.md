# Notes — `a2_equations_and_inequalities_mixture_word_problems`


- **Course:** Algebra 2 (A2 catalog)
- **Category:** Algebra 2 — Equations and Inequalities
- **Generator:** `wp_mixture`
- **Suggested family:** `wp`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Blend two concentrations; find mixture percent.
- **D=0:** Blend two concentrations; find mixture percent.
- **High D (≈16–22):** Larger volumes; nuts/soil/alcohol variety.
- **Must not:** Dump equation; systems (EA §5.5).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out: `none (MixtureWP live default)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Quinn mixes 6 fl oz of a 75\% alcohol solution with 4 fl oz of a 10\% alcohol solution. What is the concentration of the new mixture?}$ | $49\%$ | pattern=MixtureWP |
| 0 | 207 | $\text{Finn mixes 2 cubic yards of soil that is 50\% sand with 3 cubic yards of soil that is 25\% sand. What percent of the mixture is sand?}$ | $35\%$ | pattern=MixtureWP |
| 8 | 101 | $\text{Lena mixes 6 fl oz of a 15\% alcohol solution with 4 fl oz of a 75\% alcohol solution. What is the concentration of the new mixture?}$ | $39\%$ | pattern=MixtureWP |
| 8 | 207 | $\text{Parker mixes 3 fl oz of a 40\% alcohol solution with 12 fl oz of a 20\% alcohol solution. What is the concentration of the new mixture?}$ | $24\%$ | pattern=MixtureWP |
| 16 | 101 | $\text{Quinn mixes 21 fl oz of a 35\% alcohol solution with 15 fl oz of a 10\% alcohol solution. What is the concentration of the new mixture?}$ | $24.6\%$ | pattern=MixtureWP |
| 16 | 207 | $\text{Casey mixes 4 lb of nuts that are 15\% peanuts with 16 lb of nuts that are 70\% peanuts. What percent of the new mixture is peanuts?}$ | $59\%$ | pattern=MixtureWP |
| 22 | 101 | $\text{Quinn mixes 21 fl oz of a 35\% alcohol solution with 15 fl oz of a 10\% alcohol solution. What is the concentration of the new mixture?}$ | $24.6\%$ | pattern=MixtureWP |
| 22 | 207 | $\text{Casey mixes 4 lb of nuts that are 15\% peanuts with 16 lb of nuts that are 70\% peanuts. What percent of the new mixture is peanuts?}$ | $59\%$ | pattern=MixtureWP |

Opt-out flag used: `none (MixtureWP live default)`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §3.3 | https://openstax.org/books/elementary-algebra-2e/pages/3-3-solve-mixture-applications | Percent mix, tickets |
| OpenStax Intermediate Algebra 2e §2.4 | https://openstax.org/books/intermediate-algebra-2e/pages/2-4-solve-mixture-and-uniform-motion-applications | IA mixture half |

## Variety notes / UNCLEAR flag

Old path shapes recorded above; OpenStax frames win for WP stories.

## Limitations

- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** MixtureWP (wp_packaging).
- **New:** only if no honest match (see benchmark-old-path skip).
- **Not this pass:** notes only — no generator implementation.
