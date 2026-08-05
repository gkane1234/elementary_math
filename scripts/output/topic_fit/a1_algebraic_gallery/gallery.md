# Algebra 1 algebraic gallery

Generated: 2026-08-02T17:31:48.704220+00:00

Live samples via `_generate_for_type` (D = 0, 3, 6, 8, 12, 16, 20, 25; 3 seeds each). No Easy/Medium/Hard labels — continuous **D=** only.

Open [gallery.html](gallery.html) in a browser for KaTeX (local `_assets/katex`).

- topics ok: **8** · skipped missing: **0**
- samples ok: **192** · errors: **0**
- metadata: `tricks_required`, `spec_snapshot` pack, form/shape when present

## Structure inventory

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **7** · samples: **192**

| Structure / family | Count |
|--------|------:|
| `(unlabeled)` | 72 |
| `construct_poly:construct_poly` | 24 |
| `factor_gcf:factor_gcf` | 24 |
| `radical_add_subtract:structured_radical_add` | 24 |
| `polynomial_add_subtract:+` | 14 |
| `polynomial_multiply:distribute` | 12 |
| `polynomial_multiply:foil` | 12 |
| `polynomial_add_subtract:-` | 10 |

## Topics

- [A1 simplify polynomials](#poly_simplify) — `simplify_polynomials`
- [A1 multiply polynomials](#poly_multiply) — `polynomial_multiply`
- [A1 add/subtract polynomials](#poly_add_subtract) — `polynomial_add_subtract`
- [A1 quadratic factoring](#quadratic_factoring) — `quadratic_factoring`
- [A1 factor GCF](#factor_gcf) — `polynomial_factoring_common_factor`
- [A1 simplify rational expressions](#rational_simplify) — `rational_simplification`
- [A1 add/subtract rational expressions](#rational_add) — `rational_expression_simplification`
- [A1 add/subtract radicals](#radical_add) — `radical_add_subtract`

## A1 simplify polynomials

<a id="poly_simplify"></a>

`simplify_polynomials` · pack `poly_simplify` · topic label: a1: Simplifying polynomials · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **1** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `construct_poly:construct_poly` | 24 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $3x^{2} + 3x - 2$ | $3x^{2} + 3x - 2$ | `—` | `spec_pack=structured_construct_poly · methods=algebraic · form=construct_poly · shape=construct_poly · D=0` |
| 0 | $2x^{2} + 2$ | $2x^{2} + 2$ | `—` | `spec_pack=structured_construct_poly · methods=algebraic · form=construct_poly · shape=construct_poly · D=0` |
| 0 | $1 + 3x^{2}$ | $3x^{2} + 1$ | `—` | `spec_pack=structured_construct_poly · methods=algebraic · form=construct_poly · shape=construct_poly · D=0` |
| 3 | $2\left(x^{2} + x\right)$ | $2x^{2} + 2x$ | `—` | `spec_pack=structured_construct_poly · methods=algebraic · form=construct_poly · shape=construct_poly · D=3` |
| 3 | $-3x^{2} - 2 - 1$ | $-3x^{2} - 3$ | `—` | `spec_pack=structured_construct_poly · methods=algebraic · form=construct_poly · shape=construct_poly · D=3` |
| 3 | $3 + 2x^{2}$ | $2x^{2} + 3$ | `—` | `spec_pack=structured_construct_poly · methods=algebraic · form=construct_poly · shape=construct_poly · D=3` |
| 6 | $3 + 3x^{3} - x^{3} - x$ | $2x^{3} - x + 3$ | `—` | `spec_pack=structured_construct_poly · methods=algebraic · form=construct_poly · shape=construct_poly · D=6` |
| 6 | $2x - 3x^{3}$ | $-3x^{3} + 2x$ | `—` | `spec_pack=structured_construct_poly · methods=algebraic · form=construct_poly · shape=construct_poly · D=6` |
| 6 | $-x^{2} + 2x^{2} + 1 + x^{3}$ | $x^{3} + x^{2} + 1$ | `—` | `spec_pack=structured_construct_poly · methods=algebraic · form=construct_poly · shape=construct_poly · D=6` |
| 8 | $x^{2} + 1 - 2x^{2} + 2x^{3}$ | $2x^{3} - x^{2} + 1$ | `—` | `spec_pack=structured_construct_poly · methods=algebraic · form=construct_poly · shape=construct_poly · D=8` |
| 8 | $-3x^{2} + x + 2x^{2} + 2x^{3}$ | $2x^{3} - x^{2} + x$ | `—` | `spec_pack=structured_construct_poly · methods=algebraic · form=construct_poly · shape=construct_poly · D=8` |
| 8 | $3x + 2x^{3} - x^{3} - 1$ | $x^{3} + 3x - 1$ | `—` | `spec_pack=structured_construct_poly · methods=algebraic · form=construct_poly · shape=construct_poly · D=8` |
| 12 | $5x^{4} - 3x^{4}$ | $2x^{4}$ | `—` | `spec_pack=structured_construct_poly · methods=algebraic · form=construct_poly · shape=construct_poly · D=12` |
| 12 | $3y^{4} + 4 - 3y + 7y$ | $3y^{4} + 4y + 4$ | `—` | `spec_pack=structured_construct_poly · methods=algebraic · form=construct_poly · shape=construct_poly · D=12` |
| 12 | $x^{3} + 4x + 4 - 3x^{4} + 4x^{4}$ | $x^{4} + x^{3} + 4x + 4$ | `—` | `spec_pack=structured_construct_poly · methods=algebraic · form=construct_poly · shape=construct_poly · D=12` |
| 16 | $5\left(t^{4} + 2\right) - 4t^{4} + 3t^{3} + 6t^{2} - 11$ | $t^{4} + 3t^{3} + 6t^{2} - 1$ | `—` | `spec_pack=structured_construct_poly · methods=algebraic · form=construct_poly · shape=construct_poly · D=16` |
| 16 | $-5y^{4} + y^{3} - 6y^{2} + 5y + 3y^{4}$ | $-2y^{4} + y^{3} - 6y^{2} + 5y$ | `—` | `spec_pack=structured_construct_poly · methods=algebraic · form=construct_poly · shape=construct_poly · D=16` |
| 16 | $7 - 1 - x + 8x + 9x^{3} + 7x^{4}$ | $7x^{4} + 9x^{3} + 7x + 6$ | `—` | `spec_pack=structured_construct_poly · methods=algebraic · form=construct_poly · shape=construct_poly · D=16` |
| 20 | $c + 3c^{4} - 2c^{4} + c^{4} + 2c^{3} + 3c^{2}$ | $2c^{4} + 2c^{3} + 3c^{2} + c$ | `—` | `spec_pack=structured_construct_poly · methods=algebraic · form=construct_poly · shape=construct_poly · D=20` |
| 20 | $-x^{4} + 4x^{4}$ | $3x^{4}$ | `—` | `spec_pack=structured_construct_poly · methods=algebraic · form=construct_poly · shape=construct_poly · D=20` |
| 20 | $2\left(x^{4} + 1\right)$ | $2x^{4} + 2$ | `—` | `spec_pack=structured_construct_poly · methods=algebraic · form=construct_poly · shape=construct_poly · D=20` |
| 25 | $-3z^{3} + z^{2} + 3z + 4 + 2z^{3} + 2\left(2z^{4} - 1\right)$ | $4z^{4} - z^{3} + z^{2} + 3z + 2$ | `—` | `spec_pack=structured_construct_poly · methods=algebraic · form=construct_poly · shape=construct_poly · D=25` |
| 25 | $2x^{3} + 5x^{4} - x^{2} - 3x - 1 - 2x^{4}$ | $3x^{4} + 2x^{3} - x^{2} - 3x - 1$ | `—` | `spec_pack=structured_construct_poly · methods=algebraic · form=construct_poly · shape=construct_poly · D=25` |
| 25 | $\phi^{3} - 3\phi^{2} + 4 + 22\phi^{4} + 4\phi$ | $4\phi^{4} + \phi^{3} - 3\phi^{2} + 4\phi + 4$ | `—` | `spec_pack=structured_construct_poly · methods=algebraic · form=construct_poly · shape=construct_poly · D=25` |

## A1 multiply polynomials

<a id="poly_multiply"></a>

`polynomial_multiply` · pack `poly_multiply` · topic label: a1: Multiplying · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **2** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `polynomial_multiply:distribute` | 12 |
| `polynomial_multiply:foil` | 12 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\text{Multiply: } \left(2x\right)\left(x + 3\right)$ | $2x^{2} + 6x$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form=distribute · shape=distribute · D=0` |
| 0 | $\text{Multiply: } \left(x\right)\left(2x - 1\right)$ | $2x^{2} - x$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form=distribute · shape=distribute · D=0` |
| 0 | $\text{Multiply: } \left(x\right)\left(x + 2\right)$ | $x^{2} + 2x$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form=distribute · shape=distribute · D=0` |
| 3 | $\text{Multiply: } \left(2x + 1\right)\left(2x\right)$ | $4x^{2} + 2x$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form=distribute · shape=distribute · D=3` |
| 3 | $\text{Multiply: } \left(3x + 1\right)\left(x + 1\right)$ | $3x^{2} + 4x + 1$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form=foil · shape=foil · D=3` |
| 3 | $\text{Multiply: } \left(3x + 3\right)\left(2x\right)$ | $6x^{2} + 6x$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form=distribute · shape=distribute · D=3` |
| 6 | $\text{Multiply: } \left(3x^{2} + 4\right)\left(4x + 3\right)$ | $12x^{3} + 9x^{2} + 16x + 12$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form=foil · shape=foil · D=6` |
| 6 | $\text{Multiply: } \left(2x^{2} + 1\right)\left(-x + 1\right)$ | $-2x^{3} + 2x^{2} - x + 1$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form=foil · shape=foil · D=6` |
| 6 | $\text{Multiply: } \left(z + 3\right)\left(2z\right)$ | $2z^{2} + 6z$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form=distribute · shape=distribute · D=6` |
| 8 | $\text{Multiply: } \left(x^{2} + x + 1\right)\left(3x\right)$ | $3x^{3} + 3x^{2} + 3x$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form=distribute · shape=distribute · D=8` |
| 8 | $\text{Multiply: } \left(2x + 2\right)\left(x^{2} + 3\right)$ | $2x^{3} + 2x^{2} + 6x + 6$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form=foil · shape=foil · D=8` |
| 8 | $\text{Multiply: } \left(-x - 4\right)\left(2x^{2} + 2\right)$ | $-2x^{3} - 8x^{2} - 2x - 8$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form=foil · shape=foil · D=8` |
| 12 | $\text{Multiply: } \left(x^{2} - 2\right)\left(3x + 4\right)$ | $3x^{3} + 4x^{2} - 6x - 8$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form=foil · shape=foil · D=12` |
| 12 | $\text{Multiply: } \left(2x + 2\right)\left(x^{2} + 3\right)$ | $2x^{3} + 2x^{2} + 6x + 6$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form=foil · shape=foil · D=12` |
| 12 | $\text{Multiply: } \left(2x + 1\right)\left(-2x + 2\right)$ | $-4x^{2} + 2x + 2$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form=foil · shape=foil · D=12` |
| 16 | $\text{Multiply: } \left(x^{2} - 1\right)\left(x + 3\right)$ | $x^{3} + 3x^{2} - x - 3$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form=foil · shape=foil · D=16` |
| 16 | $\text{Multiply: } \left(-2c^{2} + 3\right)\left(-3c + 4\right)$ | $6c^{3} - 8c^{2} - 9c + 12$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form=distribute · shape=distribute · D=16` |
| 16 | $\text{Multiply: } \left(x + 2\right)\left(4x + 4\right)$ | $4x^{2} + 12x + 8$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form=foil · shape=foil · D=16` |
| 20 | $\text{Multiply: } \left(\gamma + 6\right)\left(6\gamma + 4\right)$ | $6\gamma^{2} + 40\gamma + 24$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form=foil · shape=foil · D=20` |
| 20 | $\text{Multiply: } \left(3r^{2} + 3\right)\left(r^{2} - r + 1\right)$ | $3r^{4} - 3r^{3} + 6r^{2} - 3r + 3$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form=distribute · shape=distribute · D=20` |
| 20 | $\text{Multiply: } \left(x^{3}\right)\left(3x + 4\right)$ | $3x^{4} + 4x^{3}$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form=distribute · shape=distribute · D=20` |
| 25 | $\text{Multiply: } \left(3x^{2} + 3\right)\left(4x^{2} + 2\right)$ | $12x^{4} + 18x^{2} + 6$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form=foil · shape=foil · D=25` |
| 25 | $\text{Multiply: } \left(4k^{2} + 2k + 3\right)\left(4k^{2}\right)$ | $16k^{4} + 8k^{3} + 12k^{2}$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form=distribute · shape=distribute · D=25` |
| 25 | $\text{Multiply: } \left(v + 7\right)\left(7v^{2} + 6v + 5\right)$ | $7v^{3} + 55v^{2} + 47v + 35$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form=distribute · shape=distribute · D=25` |

## A1 add/subtract polynomials

<a id="poly_add_subtract"></a>

`polynomial_add_subtract` · pack `poly_add_subtract` · topic label: a1: Adding and subtracting · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **2** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `polynomial_add_subtract:+` | 14 |
| `polynomial_add_subtract:-` | 10 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\text{Simplify: } \left(3x^{2} - 1\right) + \left(3x^{2} - 1\right)$ | $6x^{2} - 2$ | `—` | `spec_pack=structured_polynomial_add_subtract · methods=algebraic · form=+ · shape=+ · D=0` |
| 0 | $\text{Simplify: } \left(x^{2} + 3\right) + \left(2x^{2} + 1\right)$ | $3x^{2} + 4$ | `—` | `spec_pack=structured_polynomial_add_subtract · methods=algebraic · form=+ · shape=+ · D=0` |
| 0 | $\text{Simplify: } \left(2x^{2} + 3\right) + \left(3x + 1\right)$ | $2x^{2} + 3x + 4$ | `—` | `spec_pack=structured_polynomial_add_subtract · methods=algebraic · form=+ · shape=+ · D=0` |
| 3 | $\text{Simplify: } \left(x^{2} - x\right) + \left(3x^{2} + 2\right)$ | $4x^{2} - x + 2$ | `—` | `spec_pack=structured_polynomial_add_subtract · methods=algebraic · form=+ · shape=+ · D=3` |
| 3 | $\text{Simplify: } \left(3x^{2} + 3\right) - \left(x^{2} + 1\right)$ | $2x^{2} + 2$ | `—` | `spec_pack=structured_polynomial_add_subtract · methods=algebraic · form=- · shape=- · D=3` |
| 3 | $\text{Simplify: } \left(-2x^{2} - 1\right) - \left(x^{2} + 3\right)$ | $-3x^{2} - 4$ | `—` | `spec_pack=structured_polynomial_add_subtract · methods=algebraic · form=- · shape=- · D=3` |
| 6 | $\text{Simplify: } \left(3x^{2} + 3\right) - \left(x^{2} + 2\right)$ | $2x^{2} + 1$ | `—` | `spec_pack=structured_polynomial_add_subtract · methods=algebraic · form=- · shape=- · D=6` |
| 6 | $\text{Simplify: } \left(3x^{3} - 3x + 1\right) + \left(x^{2} + 2x\right)$ | $3x^{3} + x^{2} - x + 1$ | `—` | `spec_pack=structured_polynomial_add_subtract · methods=algebraic · form=+ · shape=+ · D=6` |
| 6 | $\text{Simplify: } \left(3x^{2} + 1\right) - \left(2x^{2} + 2\right)$ | $x^{2} - 1$ | `—` | `spec_pack=structured_polynomial_add_subtract · methods=algebraic · form=- · shape=- · D=6` |
| 8 | $\text{Simplify: } \left(2x^{3} + 3x^{2} + 2x\right) + \left(-3x^{3} + 2\right)$ | $-x^{3} + 3x^{2} + 2x + 2$ | `—` | `spec_pack=structured_polynomial_add_subtract · methods=algebraic · form=+ · shape=+ · D=8` |
| 8 | $\text{Simplify: } \left(3x^{3} + x^{2}\right) + \left(3x^{3} + 3x\right)$ | $6x^{3} + x^{2} + 3x$ | `—` | `spec_pack=structured_polynomial_add_subtract · methods=algebraic · form=+ · shape=+ · D=8` |
| 8 | $\text{Simplify: } \left(3x^{3} - 2x^{2} - x\right) + \left(3x^{3} + 1\right)$ | $6x^{3} - 2x^{2} - x + 1$ | `—` | `spec_pack=structured_polynomial_add_subtract · methods=algebraic · form=+ · shape=+ · D=8` |
| 12 | $\text{Simplify: } \left(2z^{3} + 3z^{2} + 2z\right) - \left(z^{3} - 3z^{2}\right)$ | $z^{3} + 6z^{2} + 2z$ | `—` | `spec_pack=structured_polynomial_add_subtract · methods=algebraic · form=- · shape=- · D=12` |
| 12 | $\text{Simplify: } \left(y^{3} + y + 3\right) - \left(-y^{2} + 1\right)$ | $y^{3} + y^{2} + y + 2$ | `—` | `spec_pack=structured_polynomial_add_subtract · methods=algebraic · form=- · shape=- · D=12` |
| 12 | $\text{Simplify: } \left(x^{3} + 2x^{2} + x\right) + \left(4x^{3} + 1\right)$ | $5x^{3} + 2x^{2} + x + 1$ | `—` | `spec_pack=structured_polynomial_add_subtract · methods=algebraic · form=+ · shape=+ · D=12` |
| 16 | $\text{Simplify: } \left(x^{4} + 3x^{3} + 2x + 2\right) - \left(4x^{4} + 4x^{2} + 2\right)$ | $-3x^{4} + 3x^{3} - 4x^{2} + 2x$ | `—` | `spec_pack=structured_polynomial_add_subtract · methods=algebraic · form=- · shape=- · D=16` |
| 16 | $\text{Simplify: } \left(-x^{4} - 3x^{3} + 2x^{2} + x\right) + \left(3x^{4} + 3x^{3} - 2\right)$ | $2x^{4} + 2x^{2} + x - 2$ | `—` | `spec_pack=structured_polynomial_add_subtract · methods=algebraic · form=+ · shape=+ · D=16` |
| 16 | $\text{Simplify: } \left(2z^{3} + 2z^{2} - 3z + 3\right) + \left(3z^{2} + 2z - 1\right)$ | $2z^{3} + 5z^{2} - z + 2$ | `—` | `spec_pack=structured_polynomial_add_subtract · methods=algebraic · form=+ · shape=+ · D=16` |
| 20 | $\text{Simplify: } \left(6q^{2} + 3\right) - \left(11q^{2} - 11\right)$ | $-5q^{2} + 14$ | `—` | `spec_pack=structured_polynomial_add_subtract · methods=algebraic · form=- · shape=- · D=20` |
| 20 | $\text{Simplify: } \left(-y^{4} + 2y^{3} + y^{2} - 2\right) - \left(3y^{4} + 2y^{2} + 1\right)$ | $-4y^{4} + 2y^{3} - y^{2} - 3$ | `—` | `spec_pack=structured_polynomial_add_subtract · methods=algebraic · form=- · shape=- · D=20` |
| 20 | $\text{Simplify: } \left(5y^{3} - 2y^{2} + 6y + 2\right) - \left(2y^{3} - 6y^{2} + 2\right)$ | $3y^{3} + 4y^{2} + 6y$ | `—` | `spec_pack=structured_polynomial_add_subtract · methods=algebraic · form=- · shape=- · D=20` |
| 25 | $\text{Simplify: } \left(-2x^{4} - 6x^{2} - 5x + 1\right) + \left(x^{4} + 2x - 1\right)$ | $-x^{4} - 6x^{2} - 3x$ | `—` | `spec_pack=structured_polynomial_add_subtract · methods=algebraic · form=+ · shape=+ · D=25` |
| 25 | $\text{Simplify: } \left(2v^{4} + 2v^{2} + v + 3\right) + \left(4v^{4} - 3v^{2} + 1\right)$ | $6v^{4} - v^{2} + v + 4$ | `—` | `spec_pack=structured_polynomial_add_subtract · methods=algebraic · form=+ · shape=+ · D=25` |
| 25 | $\text{Simplify: } \left(7h^{3} + 6h^{2} + 4\right) + \left(3h^{2} - 6\right)$ | $7h^{3} + 9h^{2} - 2$ | `—` | `spec_pack=structured_polynomial_add_subtract · methods=algebraic · form=+ · shape=+ · D=25` |

## A1 quadratic factoring

<a id="quadratic_factoring"></a>

`quadratic_factoring` · pack `quadratic_factoring` · topic label: a1: Quadratic expressions · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **0** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `(unlabeled)` | 24 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $x^{2}+7x+12$ | $(x+4)(x+3)$ | `—` | `pack=quadratic_factoring · D=0` |
| 0 | $x^{2}+5x+4$ | $(x+4)(x+1)$ | `—` | `pack=quadratic_factoring · D=0` |
| 0 | $x^{2}-5x+6$ | $(x-2)(x-3)$ | `—` | `pack=quadratic_factoring · D=0` |
| 3 | $x^{2}-7x+12$ | $(x-3)(x-4)$ | `—` | `pack=quadratic_factoring · D=3` |
| 3 | $x^{2}+2x$ | $(x+2)(x)$ | `—` | `pack=quadratic_factoring · D=3` |
| 3 | $x^{2}-4x$ | $(x)(x-4)$ | `—` | `pack=quadratic_factoring · D=3` |
| 6 | $6x^{2}+66x+108$ | $(6x+12)(x+9)$ | `—` | `pack=quadratic_factoring · D=6` |
| 6 | $3x^{2}+45x+150$ | $(3x+15)(x+10)$ | `—` | `pack=quadratic_factoring · D=6` |
| 6 | $2x^{2}-4x-70$ | $(2x+10)(x-7)$ | `—` | `pack=quadratic_factoring · D=6` |
| 8 | $4x^{2}-16x+16$ | $(4x-8)(x-2)$ | `—` | `pack=quadratic_factoring · D=8` |
| 8 | $4x^{2}+4x-24$ | $(4x+12)(x-2)$ | `—` | `pack=quadratic_factoring · D=8` |
| 8 | $5x^{2}-30x-35$ | $(5x+5)(x-7)$ | `—` | `pack=quadratic_factoring · D=8` |
| 12 | $9x^{2}-25$ | $(3x+5)(3x-5)$ | `—` | `pack=quadratic_factoring · D=12` |
| 12 | $4x^{2}-144$ | $(2x-12)(2x+12)$ | `—` | `pack=quadratic_factoring · D=12` |
| 12 | $9x^{2}-144$ | $(3x-12)(3x+12)$ | `—` | `pack=quadratic_factoring · D=12` |
| 16 | $6x^{2}+6x-120$ | $(6x+30)(x-4)$ | `—` | `pack=quadratic_factoring · D=16` |
| 16 | $9x^{2}-42x+49$ | $(3x-7)(3x-7)$ | `—` | `pack=quadratic_factoring · D=16` |
| 16 | $4x^{2}-56x+196$ | $(2x-14)(2x-14)$ | `—` | `pack=quadratic_factoring · D=16` |
| 20 | $9x^{2}-16$ | $(3x+4)(3x-4)$ | `—` | `pack=quadratic_factoring · D=20` |
| 20 | $5x^{2}+30x+40$ | $(5x+20)(x+2)$ | `—` | `pack=quadratic_factoring · D=20` |
| 20 | $2x^{2}+24x+54$ | $(2x+6)(x+9)$ | `—` | `pack=quadratic_factoring · D=20` |
| 25 | $16x^{2}-36$ | $(4x-6)(4x+6)$ | `—` | `pack=quadratic_factoring · D=25` |
| 25 | $6x^{2}-144x+810$ | $(6x-54)(x-15)$ | `—` | `pack=quadratic_factoring · D=25` |
| 25 | $5x^{2}-5x-10$ | $(5x-10)(x+1)$ | `—` | `pack=quadratic_factoring · D=25` |

## A1 factor GCF

<a id="factor_gcf"></a>

`polynomial_factoring_common_factor` · pack `factor_gcf` · topic label: a1: Common factor only · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **1** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `factor_gcf:factor_gcf` | 24 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\text{Factor: } 6x + 3$ | $3\left(2x + 1\right)$ | `—` | `spec_pack=structured_factor_gcf · methods=factor · form=factor_gcf · shape=factor_gcf · D=0` |
| 0 | $\text{Factor: } 3x + 6$ | $3\left(x + 2\right)$ | `—` | `spec_pack=structured_factor_gcf · methods=factor · form=factor_gcf · shape=factor_gcf · D=0` |
| 0 | $\text{Factor: } 6x + 3$ | $3\left(2x + 1\right)$ | `—` | `spec_pack=structured_factor_gcf · methods=factor · form=factor_gcf · shape=factor_gcf · D=0` |
| 3 | $\text{Factor: } 4 + 4x + 2x^{2}$ | $2\left(x^{2} + 2x + 2\right)$ | `—` | `spec_pack=structured_factor_gcf · methods=factor · form=factor_gcf · shape=factor_gcf · D=3` |
| 3 | $\text{Factor: } 3 + 3x$ | $3\left(x + 1\right)$ | `—` | `spec_pack=structured_factor_gcf · methods=factor · form=factor_gcf · shape=factor_gcf · D=3` |
| 3 | $\text{Factor: } 2x + 4x^{2} + 4$ | $2\left(2x^{2} + x + 2\right)$ | `—` | `spec_pack=structured_factor_gcf · methods=factor · form=factor_gcf · shape=factor_gcf · D=3` |
| 6 | $\text{Factor: } 7x^{2} + 21x$ | $7x\left(x + 3\right)$ | `—` | `spec_pack=structured_factor_gcf · methods=factor · form=factor_gcf · shape=factor_gcf · D=6` |
| 6 | $\text{Factor: } -4x^{2} - 6 + 4x$ | $2\left(-2x^{2} + 2x - 3\right)$ | `—` | `spec_pack=structured_factor_gcf · methods=factor · form=factor_gcf · shape=factor_gcf · D=6` |
| 6 | $\text{Factor: } 12x + 4x^{2} - 8$ | $4\left(x^{2} + 3x - 2\right)$ | `—` | `spec_pack=structured_factor_gcf · methods=factor · form=factor_gcf · shape=factor_gcf · D=6` |
| 8 | $\text{Factor: } 2u + 2$ | $2\left(u + 1\right)$ | `—` | `spec_pack=structured_factor_gcf · methods=factor · form=factor_gcf · shape=factor_gcf · D=8` |
| 8 | $\text{Factor: } 30x + 6x^{2}$ | $6x\left(x + 5\right)$ | `—` | `spec_pack=structured_factor_gcf · methods=factor · form=factor_gcf · shape=factor_gcf · D=8` |
| 8 | $\text{Factor: } 16x^{2} + 64x$ | $8x\left(2x + 8\right)$ | `—` | `spec_pack=structured_factor_gcf · methods=factor · form=factor_gcf · shape=factor_gcf · D=8` |
| 12 | $\text{Factor: } 54x^{2} + 36x$ | $9x\left(6x + 4\right)$ | `—` | `spec_pack=structured_factor_gcf · methods=factor · form=factor_gcf · shape=factor_gcf · D=12` |
| 12 | $\text{Factor: } 4y - 8y^{2} + 2$ | $2\left(-4y^{2} + 2y + 1\right)$ | `—` | `spec_pack=structured_factor_gcf · methods=factor · form=factor_gcf · shape=factor_gcf · D=12` |
| 12 | $\text{Factor: } 36x^{2} + 36x$ | $9x\left(4x + 4\right)$ | `—` | `spec_pack=structured_factor_gcf · methods=factor · form=factor_gcf · shape=factor_gcf · D=12` |
| 16 | $\text{Factor: } 26x + 14x^{2}$ | $2x\left(7x + 13\right)$ | `—` | `spec_pack=structured_factor_gcf · methods=factor · form=factor_gcf · shape=factor_gcf · D=16` |
| 16 | $\text{Factor: } 12x^{2}$ | $12x\left(x\right)$ | `—` | `spec_pack=structured_factor_gcf · methods=factor · form=factor_gcf · shape=factor_gcf · D=16` |
| 16 | $\text{Factor: } 96x + 24x^{2}$ | $12x\left(2x + 8\right)$ | `—` | `spec_pack=structured_factor_gcf · methods=factor · form=factor_gcf · shape=factor_gcf · D=16` |
| 20 | $\text{Factor: } 10x^{2} + 65x$ | $5x\left(2x + 13\right)$ | `—` | `spec_pack=structured_factor_gcf · methods=factor · form=factor_gcf · shape=factor_gcf · D=20` |
| 20 | $\text{Factor: } 18x + 15x^{2}$ | $3x\left(5x + 6\right)$ | `—` | `spec_pack=structured_factor_gcf · methods=factor · form=factor_gcf · shape=factor_gcf · D=20` |
| 20 | $\text{Factor: } 56x + 35x^{2}$ | $7x\left(5x + 8\right)$ | `—` | `spec_pack=structured_factor_gcf · methods=factor · form=factor_gcf · shape=factor_gcf · D=20` |
| 25 | $\text{Factor: } 6\phi^{2} + 36\phi$ | $6\phi\left(\phi + 6\right)$ | `—` | `spec_pack=structured_factor_gcf · methods=factor · form=factor_gcf · shape=factor_gcf · D=25` |
| 25 | $\text{Factor: } -30x + 50x^{2}$ | $10x\left(5x - 3\right)$ | `—` | `spec_pack=structured_factor_gcf · methods=factor · form=factor_gcf · shape=factor_gcf · D=25` |
| 25 | $\text{Factor: } 63x^{2} - 18x$ | $9x\left(7x - 2\right)$ | `—` | `spec_pack=structured_factor_gcf · methods=factor · form=factor_gcf · shape=factor_gcf · D=25` |

## A1 simplify rational expressions

<a id="rational_simplify"></a>

`rational_simplification` · pack `rational_simplify` · topic label: a1: Simplifying and excluded values · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **0** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `(unlabeled)` | 24 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\frac{x+3}{x^{2}+4x+3}$ | $\frac{1}{x+1},\; x \neq -3$ | `—` | `pack=rational_simplify · D=0` |
| 0 | $\frac{2x-10}{2x^{2}-18x+40}$ | $\frac{1}{x-4},\; x \neq 5$ | `—` | `pack=rational_simplify · D=0` |
| 0 | $\frac{5x+20}{5x+20}$ | $1,\; x \neq -4$ | `—` | `pack=rational_simplify · D=0` |
| 3 | $\frac{5x^{2}-30x+40}{5x^{2}-45x+100}$ | $\frac{x-2}{x-5},\; x \neq 4$ | `—` | `pack=rational_simplify · D=3` |
| 3 | $\frac{x^{2}+x}{x^{2}+4x}$ | $\frac{x+1}{x+4},\; x \neq 0$ | `—` | `pack=rational_simplify · D=3` |
| 3 | $\frac{x}{x}$ | $1,\; x \neq 0$ | `—` | `pack=rational_simplify · D=3` |
| 6 | $\frac{x^{3}-7x^{2}+7x+15}{x^{2}+x-30}$ | $\frac{x^{2}-2x-3}{x+6},\; x \neq 5$ | `—` | `pack=rational_simplify · D=6` |
| 6 | $\frac{x^{2}+5x+4}{x^{3}+10x^{2}+27x+18}$ | $\frac{x+4}{x^{2}+9x+18},\; x \neq -1$ | `—` | `pack=rational_simplify · D=6` |
| 6 | $\frac{x^{3}+5x^{2}-9x-45}{x^{3}-x^{2}-22x+40}$ | $\frac{x^{2}-9}{x^{2}-6x+8},\; x \neq -5$ | `—` | `pack=rational_simplify · D=6` |
| 8 | $\frac{x^{3}-4x}{x^{3}-4x^{2}-5x}$ | $\frac{x^{2}-4}{x^{2}-4x-5},\; x \neq 0$ | `—` | `pack=rational_simplify · D=8` |
| 8 | $\frac{x^{2}-1}{x^{2}-2x-3}$ | $\frac{x-1}{x-3},\; x \neq -1$ | `—` | `pack=rational_simplify · D=8` |
| 8 | $\frac{x^{3}-2x^{2}-25x+50}{x^{3}-2x^{2}-9x+18}$ | $\frac{x^{2}-25}{x^{2}-9},\; x \neq 2$ | `—` | `pack=rational_simplify · D=8` |
| 12 | $\frac{x^{3}-7x^{2}+10x}{x^{3}+3x^{2}-10x}$ | $\frac{x-5}{x+5},\; x \neq 0, 2$ | `—` | `pack=rational_simplify · D=12` |
| 12 | $\frac{x^{3}+x^{2}-30x-72}{2x^{4}+16x^{3}+34x^{2}-4x-48}$ | $\frac{x-6}{2x^{2}+2x-4},\; x \neq -4, -3$ | `—` | `pack=rational_simplify · D=12` |
| 12 | $\frac{2x^{3}+18x^{2}+52x+48}{8x^{4}+48x^{3}+56x^{2}-48x-64}$ | $\frac{x+3}{4x^{2}-4},\; x \neq -4, -2$ | `—` | `pack=rational_simplify · D=12` |
| 16 | $\frac{3x^{3}+6x^{2}-75x-150}{x^{2}-3x-10}$ | $3x+15,\; x \neq -2, 5$ | `—` | `pack=rational_simplify · D=16` |
| 16 | $\frac{x^{3}-2x^{2}-5x+6}{x^{2}-x-6}$ | $x-1,\; x \neq -2, 3$ | `—` | `pack=rational_simplify · D=16` |
| 16 | $\frac{2x^{4}-2x^{3}-48x^{2}+8x+160}{x^{3}-x^{2}-20x}$ | $\frac{2x^{2}-8}{x},\; x \neq -4, 5$ | `—` | `pack=rational_simplify · D=16` |
| 20 | $\frac{3x^{4}+9x^{3}-24x^{2}-36x+48}{x^{2}+6x+8}$ | $3x^{2}-9x+6,\; x \neq -4, -2$ | `—` | `pack=rational_simplify · D=20` |
| 20 | $\frac{x^{3}-4x^{2}-4x+16}{x^{2}-4}$ | $x-4,\; x \neq -2, 2$ | `—` | `pack=rational_simplify · D=20` |
| 20 | $\frac{6x^{4}-12x^{3}-126x^{2}-108x}{6x^{4}-36x^{3}-96x^{2}+576x}$ | $\frac{x^{2}+4x+3}{x^{2}-16},\; x \neq 0, 6$ | `—` | `pack=rational_simplify · D=20` |
| 25 | $\frac{x^{3}-13x^{2}+54x-72}{2x^{3}-20x^{2}+54x-36}$ | $\frac{x-4}{2x-2},\; x \neq 3, 6$ | `—` | `pack=rational_simplify · D=25` |
| 25 | $\frac{4x^{4}-12x^{3}-32x^{2}+48x+64}{2x^{2}-6x-8}$ | $2x^{2}-8,\; x \neq -1, 4$ | `—` | `pack=rational_simplify · D=25` |
| 25 | $\frac{4x^{4}-40x^{3}-4x^{2}+1000x-2400}{2x^{2}-22x+60}$ | $2x^{2}+2x-40,\; x \neq 5, 6$ | `—` | `pack=rational_simplify · D=25` |

## A1 add/subtract rational expressions

<a id="rational_add"></a>

`rational_expression_simplification` · pack `rational_add` · topic label: a1: Adding and subtracting rational expressions · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **0** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `(unlabeled)` | 24 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\frac{-1}{x+1} + \frac{-1}{x+1}$ | $\frac{-2}{x+1}$ | `—` | `pack=rational_add · D=0` |
| 0 | $\frac{2}{x-3} + \frac{1}{3x-9}$ | $\frac{7}{3x-9}$ | `—` | `pack=rational_add · D=0` |
| 0 | $\frac{-4}{3x-12} + \frac{-3}{x-4}$ | $\frac{-13}{3x-12}$ | `—` | `pack=rational_add · D=0` |
| 3 | $\frac{-3}{x+3} + \frac{2}{x+3}$ | $\frac{-1}{x+3}$ | `—` | `pack=rational_add · D=3` |
| 3 | $\frac{2}{x+4} + \frac{-4}{x+4}$ | $\frac{-2}{x+4}$ | `—` | `pack=rational_add · D=3` |
| 3 | $\frac{2}{x+1} + \frac{1}{x+1}$ | $\frac{3}{x+1}$ | `—` | `pack=rational_add · D=3` |
| 6 | $\frac{-48x^{2}-4x+40}{(4x+5)(4x-1)(4x-3)} + \frac{3}{4x-1}$ | $\frac{5}{(4x+5)(4x-3)},\; x \neq \frac{1}{4}$ | `—` | `pack=rational_add · D=6` |
| 6 | $\frac{-16x-7}{12x^{2}+13x+3} + \frac{1}{3x+1}$ | $\frac{-4}{4x+3},\; x \neq -\frac{1}{3}$ | `—` | `pack=rational_add · D=6` |
| 6 | $\frac{-60x^{2}+29x+59}{(2x-3)(3x+2)(4x-5)} + \frac{5}{2x-3}$ | $\frac{-3}{(3x+2)(4x-5)},\; x \neq \frac{3}{2}$ | `—` | `pack=rational_add · D=6` |
| 8 | $\frac{-3}{3x-4} + \frac{15x-21}{6x^{2}-17x+12}$ | $\frac{3}{2x-3},\; x \neq \frac{4}{3}$ | `—` | `pack=rational_add · D=8` |
| 8 | $\frac{-18x^{2}-12x-12}{(3x-2)(2x+1)(3x+2)} + \frac{3}{3x-2}$ | $\frac{3}{(2x+1)(3x+2)},\; x \neq \frac{2}{3}$ | `—` | `pack=rational_add · D=8` |
| 8 | $\frac{-3}{4x+3} + \frac{-3x-12}{12x^{2}+5x-3}$ | $\frac{-3}{3x-1},\; x \neq -\frac{3}{4}$ | `—` | `pack=rational_add · D=8` |
| 12 | $\frac{-33x^{2}+6x+6}{(4x+3)(3x-1)(2x-1)} + \frac{3x-3}{8x^{2}+2x-3}$ | $\frac{-3}{3x-1},\; x \neq -\frac{3}{4}, \frac{1}{2}$ | `—` | `pack=rational_add · D=12` |
| 12 | $\frac{-3}{4x+3} + \frac{-11x-18}{12x^{2}+5x-3}$ | $\frac{-5}{3x-1},\; x \neq -\frac{3}{4}, \frac{5}{3}$ | `—` | `pack=rational_add · D=12` |
| 12 | $\frac{2}{6x^{2}+11x-10} + \frac{10x^{2}+57x-40}{(2x-5)(3x-2)(2x+5)(2x-1)}$ | $\frac{3}{(2x-5)(2x-1)},\; x \neq -\frac{5}{2}, \frac{2}{3}$ | `—` | `pack=rational_add · D=12` |
| 16 | $\frac{-5}{12x^{2}-5x-3} + \frac{-36x^{2}+113x-87}{(3x+1)(4x-3)(2x-5)} + \frac{4x^{2}+x+2}{(3x+1)(4x-3)(2x-5)}$ | $\frac{-4}{3x+1},\; x \neq \frac{3}{4}, \frac{5}{2}$ | `—` | `pack=rational_add · D=16` |
| 16 | $\frac{x+1}{12x^{2}+35x+25} + \frac{-4x^{2}+16x+30}{(3x+5)(4x+5)(4x-5)}$ | $\frac{5}{(4x+5)(4x-5)},\; x \neq -\frac{5}{3}, -\frac{1}{2}$ | `—` | `pack=rational_add · D=16` |
| 16 | $\frac{54x^{2}+89x-5}{(2x+1)(2x+5)(4x-1)(3x+2)(3x-5)} + \frac{-5}{(2x+5)(4x-1)(3x-5)}$ | $\frac{3}{(2x+1)(3x+2)(3x-5)},\; x \neq -\frac{5}{2}, \frac{1}{4}$ | `—` | `pack=rational_add · D=16` |
| 20 | $\frac{-4}{(4x+1)(3x+5)(4x-3)(3x+1)(2x-5)(3x-4)} + \frac{-36x^{2}-21x+2}{(4x+1)(3x+5)(4x-3)(3x+1)(2x-5)(3x-4)} + \frac{-3}{(4x+1)(3x+5)(4x-3)(3x+1)(2x-5)(3x-4)} + \frac{2}{(4x+1)(3x+5)(4x-3)(3x+1)(2x-5)(3x-4)}$ | $\frac{-3}{(3x+5)(4x-3)(2x-5)(3x-4)},\; x \neq -\frac{1}{3}, -\frac{1}{4}$ | `—` | `pack=rational_add · D=20` |
| 20 | $\frac{-4}{2x+5} + \frac{-5}{3x+5} + \frac{-5}{4x+3} + \frac{26x+37}{8x^{2}+26x+15}$ | $\frac{-5}{3x+5},\; x \neq -\frac{5}{2}, -\frac{3}{4}$ | `—` | `pack=rational_add · D=20` |
| 20 | $\frac{7x-23}{12x^{2}-23x+5} + \frac{2}{3x-5}$ | $\frac{5}{4x-1},\; x \neq -\frac{5}{3}, \frac{5}{3}$ | `—` | `pack=rational_add · D=20` |
| 25 | $\frac{36x^{2}+7x-8}{(4x+1)(4x-1)(3x+2)} + \frac{2}{12x^{2}+5x-2}$ | $\frac{3}{4x+1},\; x \neq -\frac{2}{3}, \frac{1}{4}$ | `—` | `pack=rational_add · D=25` |
| 25 | $\frac{2x-17}{8x^{2}+18x-5} + \frac{-2}{2x+5}$ | $\frac{-3}{4x-1},\; x \neq -\frac{5}{2}, \frac{3}{4}$ | `—` | `pack=rational_add · D=25` |
| 25 | $\frac{5x-3}{(3x-4)(4x+5)(3x+2)(3x-2)(2x+1)} + \frac{-2x^{2}-8x-9}{(3x-4)(4x+5)(3x+2)(4x+1)(3x-2)(2x+1)}$ | $\frac{3}{(4x+5)(3x+2)(4x+1)(3x-2)},\; x \neq -\frac{1}{2}, \frac{4}{3}$ | `—` | `pack=rational_add · D=25` |

## A1 add/subtract radicals

<a id="radical_add"></a>

`radical_add_subtract` · pack `radical_add` · topic label: a1: Adding and subtracting · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **1** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `radical_add_subtract:structured_radical_add` | 24 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $2\sqrt{14} - \sqrt{14}$ | $\sqrt{14}$ | `—` | `spec_pack=structured_radical_add · methods=radical_combine · form=structured_radical_add · shape=structured_radical_add · D=0` |
| 0 | $\sqrt{5} + 2\sqrt{5}$ | $3\sqrt{5}$ | `—` | `spec_pack=structured_radical_add · methods=radical_combine · form=structured_radical_add · shape=structured_radical_add · D=0` |
| 0 | $2\sqrt{3} + 4\sqrt{3}$ | $6\sqrt{3}$ | `—` | `spec_pack=structured_radical_add · methods=radical_combine · form=structured_radical_add · shape=structured_radical_add · D=0` |
| 3 | $4\sqrt{13} - 5\sqrt{13}$ | $-\sqrt{13}$ | `—` | `spec_pack=structured_radical_add · methods=radical_combine · form=structured_radical_add · shape=structured_radical_add · D=3` |
| 3 | $2\sqrt{14} + 2\sqrt{14}$ | $4\sqrt{14}$ | `—` | `spec_pack=structured_radical_add · methods=radical_combine · form=structured_radical_add · shape=structured_radical_add · D=3` |
| 3 | $\sqrt{15} + 2\sqrt{15}$ | $3\sqrt{15}$ | `—` | `spec_pack=structured_radical_add · methods=radical_combine · form=structured_radical_add · shape=structured_radical_add · D=3` |
| 6 | $\sqrt{99} + \sqrt{176}$ | $7\sqrt{11}$ | `—` | `spec_pack=structured_radical_add · methods=radical_combine · form=structured_radical_add · shape=structured_radical_add · D=6` |
| 6 | $\sqrt{2} - 2\sqrt{2}$ | $-\sqrt{2}$ | `—` | `spec_pack=structured_radical_add · methods=radical_combine · form=structured_radical_add · shape=structured_radical_add · D=6` |
| 6 | $\sqrt{6} - 2\sqrt{6}$ | $-\sqrt{6}$ | `—` | `spec_pack=structured_radical_add · methods=radical_combine · form=structured_radical_add · shape=structured_radical_add · D=6` |
| 8 | $4\sqrt{245} + \sqrt{245} - \sqrt{245}$ | $28\sqrt{5}$ | `—` | `spec_pack=structured_radical_add · methods=radical_combine · form=structured_radical_add · shape=structured_radical_add · D=8` |
| 8 | $\sqrt{112} + \sqrt{28} - \sqrt{63}$ | $3\sqrt{7}$ | `—` | `spec_pack=structured_radical_add · methods=radical_combine · form=structured_radical_add · shape=structured_radical_add · D=8` |
| 8 | $\sqrt{72} + \sqrt{98} - \sqrt{72}$ | $7\sqrt{2}$ | `—` | `spec_pack=structured_radical_add · methods=radical_combine · form=structured_radical_add · shape=structured_radical_add · D=8` |
| 12 | $5\sqrt{160} - \sqrt{490} + 2\sqrt{160}$ | $21\sqrt{10}$ | `—` | `spec_pack=structured_radical_add · methods=radical_combine · form=structured_radical_add · shape=structured_radical_add · D=12` |
| 12 | $\sqrt{112} - \sqrt{7} - \sqrt{112}$ | $-\sqrt{7}$ | `—` | `spec_pack=structured_radical_add · methods=radical_combine · form=structured_radical_add · shape=structured_radical_add · D=12` |
| 12 | $5\sqrt{125} - 6\sqrt{20} - 6\sqrt{20}$ | $\sqrt{5}$ | `—` | `spec_pack=structured_radical_add · methods=radical_combine · form=structured_radical_add · shape=structured_radical_add · D=12` |
| 16 | $5\sqrt{44} - \sqrt{44} - 8\sqrt{176}$ | $-24\sqrt{11}$ | `—` | `spec_pack=structured_radical_add · methods=radical_combine · form=structured_radical_add · shape=structured_radical_add · D=16` |
| 16 | $\sqrt{112} + 5\sqrt{112} - 8\sqrt{63} + 2\sqrt{63}$ | $6\sqrt{7}$ | `—` | `spec_pack=structured_radical_add · methods=radical_combine · form=structured_radical_add · shape=structured_radical_add · D=16` |
| 16 | $7\sqrt{175} + 2\sqrt{112} + 3\sqrt{28} - 7\sqrt{252}$ | $7\sqrt{7}$ | `—` | `spec_pack=structured_radical_add · methods=radical_combine · form=structured_radical_add · shape=structured_radical_add · D=16` |
| 20 | $\sqrt{60} + 7\sqrt{240} + \sqrt{135}$ | $33\sqrt{15}$ | `—` | `spec_pack=structured_radical_add · methods=radical_combine · form=structured_radical_add · shape=structured_radical_add · D=20` |
| 20 | $5\sqrt{135} - 7\sqrt{240} + 7\sqrt{60} - \sqrt{540} - \sqrt{135}$ | $-8\sqrt{15}$ | `—` | `spec_pack=structured_radical_add · methods=radical_combine · form=structured_radical_add · shape=structured_radical_add · D=20` |
| 20 | $2\sqrt{275} + \sqrt{44} - 2\sqrt{396} + 2\sqrt{176} - 8\sqrt{396}$ | $-40\sqrt{11}$ | `—` | `spec_pack=structured_radical_add · methods=radical_combine · form=structured_radical_add · shape=structured_radical_add · D=20` |
| 25 | $8\sqrt{45} - 4\sqrt{125} - 6\sqrt{125}$ | $-26\sqrt{5}$ | `—` | `spec_pack=structured_radical_add · methods=radical_combine · form=structured_radical_add · shape=structured_radical_add · D=25` |
| 25 | $10\sqrt{468} - \sqrt{208} + 8\sqrt{468} - \sqrt{468}$ | $98\sqrt{13}$ | `—` | `spec_pack=structured_radical_add · methods=radical_combine · form=structured_radical_add · shape=structured_radical_add · D=25` |
| 25 | $10\sqrt{135} + \sqrt{240} + 9\sqrt{60}$ | $52\sqrt{15}$ | `—` | `spec_pack=structured_radical_add · methods=radical_combine · form=structured_radical_add · shape=structured_radical_add · D=25` |
