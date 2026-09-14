# Notes — `a2_exponential_and_logarithmic_expressions_writing_logs_in_terms_of_others`

> **LOW_VARIETY** — One template across seeds at D=0.

- **Display name:** Writing logs in terms of others
- **Category:** Algebra 2 — Exponential and Logarithmic Expressions
- **Generator:** `log_change_of_base`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice writing logs in terms of others (catalog: log_change_of_base).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Expand: } \log_{3}\left(7^{5}\right)$ | $5\log_{3}(7)$ | form=exp_requiring_log |
| 0 | 207 | $\text{Expand: } \log_{3}\left(4^{2}\right)$ | $2\log_{3}(4)$ | form=exp_requiring_log |
| 8 | 101 | $\text{Expand: } \log_{5}\left(7^{5}\right)$ | $5\log_{5}(7)$ | form=exp_requiring_log |
| 8 | 207 | $\text{Expand: } \log_{5}\left(4^{2}\right)$ | $2\log_{5}(4)$ | form=log_properties_condense |
| 16 | 101 | $\text{Expand: } \log_{5}\left(7^{5}\right)$ | $5\log_{5}(7)$ | form=exp_requiring_log |
| 16 | 207 | $\text{Expand: } \log_{12}\left(5^{3}\right)$ | $3\log_{12}(5)$ | form=exp_requiring_log |
| 22 | 101 | $\text{Expand: } \log_{5}\left(7^{5}\right)$ | $5\log_{5}(7)$ | form=exp_requiring_log |
| 22 | 207 | $\text{Expand: } \log_{12}\left(5^{3}\right)$ | $3\log_{12}(5)$ | form=exp_requiring_log |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| Intermediate Algebra 2e §10.2 | https://openstax.org/books/intermediate-algebra-2e/pages/10-2-evaluate-and-graph-exponential-functions | 10.2 Evaluate and Graph Exponential Functions — e.g. Example 10.10: On the same coordinate system graph $f (x) = 2^{x}$ and $g (x) = 3^{x} .$; Example 10.11: On the same coordinate system, graph $f (x) = \left(\right. \frac{1}{2} \left.\right)^{x}$ and $g (x) = \left(\right. \frac{1}{3} \left.\right)^{x} .$ |
| Intermediate Algebra 2e §10.3 | https://openstax.org/books/intermediate-algebra-2e/pages/10-3-evaluate-and-graph-logarithmic-functions | 10.3 Evaluate and Graph Logarithmic Functions — e.g. Example 10.18: Convert to logarithmic form: ⓐ $2^{3} = 8 ,$ ⓑ $5^{\frac{1}{2}} = \sqrt{5} ,$ and ⓒ $\left(\right. \frac{1}{2} \left.\right)^{4} = \frac{1}{16} .$; Example 10.19: Convert to exponential form: ⓐ $2 = \log_{8} 64 ,$ ⓑ $0 = \log_{4} 1 ,$ and ⓒ $- 3 = \log_{10} \frac{1}{1000} .$ |
| Intermediate Algebra 2e §10.4 | https://openstax.org/books/intermediate-algebra-2e/pages/10-4-use-the-properties-of-logarithms | 10.4 Use the Properties of Logarithms — e.g. Example 10.28: Evaluate using the properties of logarithms: ⓐ $\log_{8} 1$ and ⓑ $\log_{6} 6 .$; Example 10.29: Evaluate using the properties of logarithms: ⓐ $4^{\log_{4} 9}$ and ⓑ $\log_{3} 3^{5} .$ |

Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.

## Variety notes / UNCLEAR flag

One template across seeds at D=0.
Flags: `LOW_VARIETY`.

## Limitations

Flags for gallery red header: `LOW_VARIETY`.

- **Variety:** one template / Mad-Lib across seeds at easy D — rotate OpenStax-derived frames or algebraic shapes before claiming shipped variety.
- **Difficulty scaling:** Variety thin at fixed D; D may still bump coeffs — check live ladder.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Existing `log_change_of_base` hand path until a skeleton exists.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `log_change_of_base`; equations/WP agent owns solve/WP siblings._
