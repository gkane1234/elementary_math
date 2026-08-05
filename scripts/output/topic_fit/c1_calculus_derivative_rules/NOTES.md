# Calculus derivative-rules batch

## What changed

- New module `question_engine/generators/calculus_derivative_rules.py` overrides
  thin derivative builders with ordering/family variety.
- New/fixed wirings:
  - `instantaneous_rate_of_change` (was `calculus_foundations`)
  - `derivative_inverse_functions` (was `calculus_foundations`)
  - `derivative_logarithmic` (was miswired to plain `derivative_ln_exp`)

## Variety examples

| Rule | Seed pattern | Added variants |
|------|--------------|----------------|
| Power | ∑ a_k x^k | reversed terms, x^{-n} vs 1/x^n, fractional powers, factored x(x+b) |
| Product | (ax+b)(cx+d) | · vs juxtaposition, factor order, x sin x / x e^x |
| Quotient | (ax+b)/(cx+d) | frac vs ( )( )^{-1}; sin/x; linear over quadratic |
| Chain | (ax+b)^n | b+ax inner; e^{inner}/exp; √; sin(a x^n); nested powers |
| Trig | sin x | cot/sec/csc; k·x vs kx; products; sin²x |
| Inv trig | arcsin x | sin^{-1} notation; arcsin(ax+b); arctan(x^k) |
| Ln/exp | ln(x^n), e^{kx} | exp(); e^{b+ax}; ln\|ax+b\|; e^{x²} |
| Other base | a^x, log_a x | a^{kx}; log_a(ax+b); x·a^x product |
| Log diff | — | products/quotients of powers; x^x; (sin x)^x |
| Implicit | x²+y²=a | term order; xy; ellipses; cubes; sin/cos |
| Rates / definition | x² | reciprocal/sqrt/trig/exp; limit forms h vs x→a |

## Regenerate

```powershell
$env:PYTHONPATH='.'
python scripts/build_calculus_derivative_rules_gallery.py
python -m pytest question_engine/tests/test_calculus_derivative_rules.py -q
```
