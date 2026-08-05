# Topic-fit QA report — Calculus derivative-rules batch

Scope: Differentiation chapter (classic derivative rules + rates/definition/inverse)

Gallery: `scripts/output/topic_fit/calculus_derivative_rules/`

## Verification table

| Type | Topic? | Method? | Hard harder? | Status |
|------|--------|---------|--------------|--------|
| `calc_diff_power_rule` | Y | Y | Y | Pass |
| `calc_diff_product_rule` | Y | Y | Y | Pass |
| `calc_diff_quotient_rule` | Y | Y | Y | Pass |
| `calc_diff_chain_rule` | Y | Y | Y | Pass |
| `calc_diff_trigonometric` | Y | Y | Y | Pass |
| `calc_diff_inverse_trigonometric` | Y | Y | Y | Pass |
| `calc_diff_natural_logarithms_and_exponentials` | Y | Y | Y | Pass |
| `calc_diff_other_base_logarithms_and_exponentials` | Y | Y | Y | Pass |
| `calc_diff_logarithmic` | Y | Y (log diff technique) | Y | Pass |
| `calc_diff_implicit` | Y | Y | Y | Pass |
| `calc_diff_higher_order_derivatives` | Y | Y | Y | Pass |
| `calc_diff_average_rates_of_change` | Y | Y | Y | Pass |
| `calc_diff_instantaneous_rates_of_change` | Y | Y | Y | Pass |
| `calc_diff_definition_of_the_derivative` | Y | Y | Y | Pass |
| `calc_diff_inverse_functions` | Y | Y | Y | Pass |

Topic-fit auto-flags: 15/15 PASS (`FAIL=0`). Pytest: 57 passed (derivative-rules + pilot).

## Failures found

None.

## Deferred / remaining

| Item | Why |
|------|-----|
| `calc_diff_rules_using_tables` | Already dedicated; not reworked this pass |
| App-of-diff foundations stubs (concavity, extrema, optimization, curve sketching, motion, Newton, graphical comparison) | Outside derivative-rules batch |
| Integration / DE foundations stubs | Outside this batch |
