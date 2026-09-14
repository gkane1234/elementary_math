# Notes — `a2_systems_of_equations_and_inequalities_graphing_systems_of_linear_inequalities`

> **UNCLEAR / NOT_IMPLEMENTED** — see Limitations.



- **Course:** Algebra 2 (A2 catalog)
- **Category:** Algebra 2 — Systems of Equations and Inequalities
- **Generator:** `graph_system_inequalities`
- **Suggested family:** `systems`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Two half-planes: $y>x$ and $y\le k$.
- **D=0:** Two half-planes: $y>x$ and $y\le k$.
- **High D (≈16–22):** Mixed solid/dashed; steeper slopes ($y>2x$, $y\le -2x$).
- **Must not:** Algebraic elimination on this leaf.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out: `none (live systems skeleton)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Graph the system: } \begin{cases} y > x \\ y \le 2 \end{cases}$ | $\begin{cases} y > x \\ y \le 2 \end{cases}$ | pattern=GraphSystemIneq |
| 0 | 207 | $\text{Graph the system: } \begin{cases} y > x \\ y \le 3 \end{cases}$ | $\begin{cases} y > x \\ y \le 3 \end{cases}$ | pattern=GraphSystemIneq |
| 8 | 101 | $\text{Graph the system: } \begin{cases} y > x \\ y \le 3 \end{cases}$ | $\begin{cases} y > x \\ y \le 3 \end{cases}$ | pattern=GraphSystemIneq |
| 8 | 207 | $\text{Graph the system: } \begin{cases} y > x \\ y \le 4 \end{cases}$ | $\begin{cases} y > x \\ y \le 4 \end{cases}$ | pattern=GraphSystemIneq |
| 16 | 101 | $\text{Graph the system: } \begin{cases} y > 2x \\ y \le -2x \end{cases}$ | $\begin{cases} y > 2x \\ y \le -2x \end{cases}$ | pattern=GraphSystemIneq |
| 16 | 207 | $\text{Graph the system: } \begin{cases} y \ge 3x \\ y < 2x \end{cases}$ | $\begin{cases} y \ge 3x \\ y < 2x \end{cases}$ | pattern=GraphSystemIneq |
| 22 | 101 | $\text{Graph the system: } \begin{cases} y > 2x \\ y \le -2x \end{cases}$ | $\begin{cases} y > 2x \\ y \le -2x \end{cases}$ | pattern=GraphSystemIneq |
| 22 | 207 | $\text{Graph the system: } \begin{cases} y \ge 3x \\ y < 2x \end{cases}$ | $\begin{cases} y \ge 3x \\ y < 2x \end{cases}$ | pattern=GraphSystemIneq |

Opt-out flag used: `none (live systems skeleton)`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §5.6 | https://openstax.org/books/elementary-algebra-2e/pages/5-6-graph-systems-of-linear-inequalities | Two inequalities; shade intersection |
| OpenStax Intermediate Algebra 2e §4.6 | https://openstax.org/books/intermediate-algebra-2e/pages/4-6-graph-systems-of-linear-inequalities | IA systems of inequalities |

## Variety notes / UNCLEAR flag

Old path shapes recorded above; OpenStax frames win for WP stories.

## Limitations

Flags for gallery red header: `NOT_IMPLEMENTED`, `UNCLEAR`.

- **Not implemented on an algebraic skeleton** — graph / figure engine outside SolveLinear / poly / rational cores; leave leaf until a graph core can match OpenStax shapes honestly (`benchmark-old-path` skip).
- **Why stubbed:** live old path may still sample, but gold (transforms, asymptotes, focus/directrix, amplitude/period, shading) is not locked — red-header gallery only.
- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** GraphSystemIneq (systems / linear_forms).
- **New:** only if no honest match (see benchmark-old-path skip).
- **Not this pass:** notes only — no generator implementation.
