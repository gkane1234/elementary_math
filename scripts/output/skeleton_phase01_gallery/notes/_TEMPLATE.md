# Notes — `<gallery-slug>` (`<type_id>`)

Copy this file to `notes/<slug>.md` or `notes/<type_id>.md` (or `<slug>/NOTES.md`).
Fill from a **live old-path generate**, not from memory. Process:
`.cursor/rules/topic-notes-process.mdc`.

Flags (optional; gallery shows a **red header** if any is present as a whole word):

- `UNCLEAR` — gold look not locked (old path is a dump stub, wrong skill, or we do not know).
- `LOW_VARIETY` — old path is one Mad-Lib / one vehicle; OpenStax frames should win for stories.
- `LIMITATIONS` — known gaps remain (variety, D-scaling, OpenStax coverage, diagram missing, …).
- `NOT_IMPLEMENTED` — no honest skeleton/engine yet; gallery may be notes-only / 0 live samples.

**Every notes file must include a Limitations section** (even if the bullet is “none”).

---

## What the question should look like (D=0 vs high D)

- **Skill:** _one sentence: what the student does_
- **D=0:** _as simple as old easy — shapes, not a dump_
- **High D (≈16–22):** _numeric hardness first, then format unlocks_
- **Must not:** _wrong-topic shapes, equation dump in a WP, mixture/systems on a one-step leaf, …_

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with the opt-out flag (see `benchmark-old-path.mdc`). Paste **real**
`prompt_latex` / `answer_latex`. Never invent TeX.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 |  | `$…$` | `$…$` | _term count, a=1 vs a≠1, parens, graph vs solve, story vs dump_ |
| 8 |  | `$…$` | `$…$` |  |
| 16 |  | `$…$` | `$…$` |  |
| 22 |  | `$…$` | `$…$` |  |

Opt-out flag used: `_e.g. use_sample_linear_equation=True_`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL. Do not dump copyrighted problem text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| _e.g. OpenStax Elementary Algebra 2e §2.6_ | https://openstax.org/… | _d=rt; several vehicles (bike/drive/walk/bus/train)_ |
| _e.g. OpenStax Prealgebra 2e §8.1_ | https://openstax.org/… |  |

Local HTML (if mined): `textbooks/openstax/html/<book>/…`

## Variety notes / UNCLEAR flag

- Story variety: several OpenStax-derived frames at the same D, or not a WP.
- If old is the dump stub (“the equation is $x+1=3$”) or a single-vehicle Mad-Lib, set
  `LOW_VARIETY` and/or `UNCLEAR` here and say what OpenStax should replace.
- WP algebra shapes still follow the old path (`word-problem-frames.mdc`).

_Remove this paragraph and write the actual notes. Leave `UNCLEAR` / `LOW_VARIETY` in the file
only when they still apply._

## Limitations

**Required on every notes file.** Leave the token `LIMITATIONS` and/or `NOT_IMPLEMENTED`
in this section when the gap still applies (red gallery header). Cover what is true:

- Variety (one Mad-Lib / one frame / dump stub)
- Difficulty scaling (D flat across seeds; format unlock without numeric hardness)
- OpenStax coverage (no cite, wrong chapter, missing frame types)
- Diagram / stimulus missing (type name says diagram but no SVG)
- Wrong skill / miswire / deferred engine
- Other (graphing outside algebraic cores, scaffold-only, …)

- **Status:** `_none | LIMITATIONS | NOT_IMPLEMENTED_`
- **Notes:** _one short paragraph or bullets_

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** _existing skeleton / pattern / core, e.g. SolveLinear + wp_packaging_
- **New:** _only if no honest match; otherwise leave the leaf (benchmark-old-path skip)_
- **Not this pass:** do not implement here — index + notes first.

Suggested family from `G6_PA_INDEX.md`: `_number | affine | solve | wp | proportion | geometry | other_`
