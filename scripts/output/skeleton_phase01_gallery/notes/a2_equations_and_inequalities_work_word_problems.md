# Notes — `a2_equations_and_inequalities_work_word_problems`


- **Course:** Algebra 2 (A2 catalog)
- **Category:** Algebra 2 — Equations and Inequalities
- **Generator:** `wp_work`
- **Suggested family:** `wp`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Two workers together / find missing rate; integer hours.
- **D=0:** Two workers together / find missing rate; integer hours.
- **High D (≈16–22):** Three workers; pipes + drain; partial work then join.
- **Must not:** Dump $1/a+1/b=1/t$; d=rt on this leaf.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out: `none (wp_work live default)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Press #1 takes 4 hr to print an issue. Working with Press #2, they finish in 3 hr. How many hr would Press #2 need working alone?}$ | $12 hr$ | pattern=WorkWP |
| 0 | 207 | $\text{Aisha can clean a pool in 12 hr and Maya can finish the same pool in 6 hr. Working together, how many hr will it take them to finish cleaning?}$ | $4 hr$ | pattern=WorkWP |
| 8 | 101 | $\text{Owen and Wade can mow a lawn in 3 and 10 hr. With Gwen helping, the three finish in 2 hr. How many hr would Gwen need alone?}$ | $15 hr$ | pattern=WorkWP |
| 8 | 207 | $\text{Aisha, Maya, and Yves can finish a job in 3, 10, and 15 hr respectively. Working together, how many hr will it take them to finish the job?}$ | $2 hr$ | pattern=WorkWP |
| 16 | 101 | $\text{Pipe A fills a tank in 3 hr, pipe B fills it in 6 hr, and a drain empties it in 6 hr. With all three open, how many hr to fill the tank?}$ | $3 hr$ | pattern=WorkWP |
| 16 | 207 | $\text{Aisha can finish a job in 10 hr and Maya can finish the same job in 5 hr. Aisha works alone for 4 hr, then Maya joins. How many hr from the start until the job is done?}$ | $6 hr$ | pattern=WorkWP |
| 22 | 101 | $\text{Pipe A fills a tank in 3 hr, pipe B fills it in 6 hr, and a drain empties it in 6 hr. With all three open, how many hr to fill the tank?}$ | $3 hr$ | pattern=WorkWP |
| 22 | 207 | $\text{Aisha can finish a job in 10 hr and Maya can finish the same job in 5 hr. Aisha works alone for 4 hr, then Maya joins. How many hr from the start until the job is done?}$ | $6 hr$ | pattern=WorkWP |

Opt-out flag used: `none (wp_work live default)`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §8.8 | https://openstax.org/books/elementary-algebra-2e/pages/8-8-solve-uniform-motion-and-work-applications | Work: together, alone, pipes |
| OpenStax Intermediate Algebra 2e §2.4 | https://openstax.org/books/intermediate-algebra-2e/pages/2-4-solve-mixture-and-uniform-motion-applications | IA applications (work half) |

## Variety notes / UNCLEAR flag

Old path shapes recorded above; OpenStax frames win for WP stories.

## Limitations

- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** WorkWP (wp_packaging) — same as A1 `work_word_problems`.
- **New:** only if no honest match (see benchmark-old-path skip).
- **Not this pass:** notes only — no generator implementation.
