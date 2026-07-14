# Topic-fit QA — reference

## Sample pack schema (`samples.jsonl`)

One JSON object per line:

| Field | Meaning |
|-------|---------|
| `type_id`, `name`, `generator` | Catalog identity |
| `tier` | `easy` / `medium` / `hard` |
| `sample_index` | 0-based within tier |
| `prompt_latex`, `prompt_text` | Student-facing prompt |
| `instruction_latex` | Shared instruction if present |
| `answer_latex` | Included for context only — **do not score correctness** |
| `error` | Generation error string, or null |
| `metadata_flags` | `scaffolded`, `has_graph`, `has_diagram`, `has_number_line`, `has_choices` |

## Auto flags (`auto_flags.json`)

Per-type `status`: `PASS` | `NOTE` | `FAIL`.

Hard fails include stub/blank prompts, topic keyword mismatches, known miswires, identical Easy=Hard single problem.

Notes include weak E/H diversity, flat difficulty presets, thin foundation generators.

Treat as **pre-flags**; human/agent judgment still required for Method? and Hard harder?.

## Known miswire patterns

| Generator | Bad when type_id suggests |
|-----------|---------------------------|
| `graph_quadratic` | rational, exponential, trig, ellipse, hyperbola, … |
| `sequence_arithmetic_nth_term` | geometric |
| `function_operations` | vector |
| `inverse_function_basic` | matrix |
| `derivative_power_rule` | product_rule |
| `derivative_product_rule` | power_rule (and not product) |
| `radical_equations` | rational (without radical/exponent) |
| `quadratic_vertex_form_write` | conic that is not parabola |
| `g6_integer_multiply` / other arithmetic | `g6_properties_of_addition_and_multiplication` (identify-property) |
| `precalc_foundations` / `calculus_foundations` | thin fallback — scrutinize topic |

Identify-property types also get a light **answer-shape** check: answers that are bare operation names (`multiplication`) or numeric products fail, because that usually means the type is still wired to compute-the-product generation.

## Family type lists

Defined in `question_engine/qa/topic_fit.py` → `FAMILIES`:

- `poly_quad` — polynomials + quadratic solve methods
- `a1_equations` — one/two/multi-step, abs value, systems
- `radical_rational` — radical + rational expression/equation types
- `graphing_linear` — linear graphing / slope / inequalities

## Code entry points

- Heuristics: `question_engine/qa/topic_fit.py`
- CLI: `scripts/topic_fit_sample.py`
- Report template: `scripts/output/topic_fit/_TEMPLATE.md`
- Prior example narrative: `scripts/output/POLY_QUAD_QA.md` (includes answer bugs; for topic-fit, focus on Topic?/Method? columns)
