# Topic-fit sample gallery

Review prompts for **topic / method / difficulty shape** — not answer correctness.

## `polynomial_naming` — Naming

- generator: `polynomial_naming`
- auto status: **PASS**

### easy

- `3x-1`
- `3x^{2}+x+2`

### medium

- `9x^{3}-4x^{2}+7x+9`
- `5x^{3}-2x^{2}-2x+7`

### hard

- `8x^{2}-9x+12`
- `7x^{5}+10x^{4}-19x^{3}+x^{2}-3x+3`

## `polynomial_add_subtract` — Adding and subtracting

- generator: `polynomial_add_subtract`
- auto status: **PASS**

### easy

- `(x+2) + (3x-3)`
- `(3x^{2}+3x-1) + (x^{2}+2x+2)`

### medium

- `(5x^{2}+4x-3) - (5x^{2}-4x+2)`
- `(5x^{2}+7x-4) + (9x^{2}-8x-7)`

### hard

- `(4x^{5}-17x^{4}+19x^{3}-14x^{2}-19x+10) + (6x^{5}-18x^{4}+7x^{3}+4x^{2}+20x-17)`
- `(7x^{2}+14x-17) + (10x^{2}-14x+14)`

## `polynomial_multiply` — Multiplying

- generator: `polynomial_multiply`
- auto status: **PASS**

### easy

- `(x-2)(x-3)`
- `(x-1)(x+1)`

### medium

- `(2x^{3}-x^{2}+4)(4x^{2}+5x+9)`
- `(3x^{3}-8x+1)(9x)`

### hard

- `(11x^{4})(8x^{5}+10x^{2}-4)`
- `(6x^{3}+2x+9)(6x^{3}-6x^{2}+10x-15)`

## `polynomial_multiply_special` — Multiplying special cases

- generator: `polynomial_multiply_special`
- auto status: **PASS**

### easy

- `(x + 1)(x - 3)`
- `(x + 1)(x - 2)`

### medium

- `(x + 6)(x - 2)`
- `(x + 6)(x - 6)`

### hard

- `(3x + 5)(3x - 5)`
- `(4x - 2)^2`

## `polynomial_factoring_common_factor` — Common factor only

- generator: `polynomial_factoring_common_factor`
- auto status: **PASS**

### easy

- `2x^{2}-6x+6`
- `3x^{2}+3x+3`

### medium

- `21x^{3}+9x^{2}-9x`
- `8x^{2}-16x+14`

### hard

- `24x^{4}-34x^{3}+16x^{2}+30x`
- `52x^{2}-56x+44`

## `quadratic_factoring` — Quadratic expressions

- generator: `quadratic_factoring`
- auto status: **PASS**

### easy

- `x^{2}+2x-8`
- `x^{2}-4x+3`

### medium

- `2x^{2}+26x+44`
- `6x^{2}-18x+12`

### hard

- `2x^{2}-38x+176`
- `4x^{2}+68x+280`

## `polynomial_factoring_special_cases` — Special cases

- generator: `polynomial_factoring_special_cases`
- auto status: **PASS**

### easy

- `x^{2}-4`
- `x^{2}-6x+9`

### medium

- `16x^{2}-1`
- `4x^{2}-9`

### hard

- `125x^{3}-64`
- `27x^{3}-64`

## `polynomial_factoring_grouping` — By grouping

- generator: `polynomial_factoring_grouping`
- auto status: **PASS**

### easy

- `x^{3}-3x^{2}-x+3`
- `x^{3}+x^{2}+2x+2`

### medium

- `4x^{3}-24x^{2}-2x+12`
- `2x^{3}-14x^{2}-2x+14`

### hard

- `2x^{3}-24x^{2}+5x-60`
- `2x^{3}-8x^{2}-5x+20`

## `quadratic_solve_by_graphing` — Solving equations by graphing

- generator: `solve_polynomial_by_graphing`
- auto status: **PASS**

### easy

- `x^{2} - 1 = 0`
- `x^{2} + x - 2 = 0`

### medium

- `3x^{2} - 3x - 6 = 0`
- `-3x^{2} + 3x + 36 = 0`

### hard

- `-4(x + 4)(x - 4) = 0`
- `4x^{2} + 20x = 0`

## `quadratic_square_roots` — Solving equations by taking square roots

- generator: `quadratic_square_roots`
- auto status: **PASS**

### easy

- `x^{2} = 9`
- `x^{2} = 9`

### medium

- `6(x - 5)^{2} - 54 = 0`
- `(x - 4)^{2} = 16`

### hard

- `5(x + 2)^{2} = 50`
- `5x^{2} - 10x - 20 = 0`

## `quadratic_factoring_equations` — Solving equations by factoring

- generator: `quadratic_factoring_equations`
- auto status: **PASS**

### easy

- `x^{2}+14x+49 = 0`
- `x^{2}+8x+15 = 0`

### medium

- `4x^{2}-44x+40 = 0`
- `3x^{2}+21x-180 = 0`

### hard

- `16x^{2}-80x+100 = 0`
- `9x^{2}+78x+169 = 0`

## `quadratic_formula` — Solving equations with the Quadratic Formula

- generator: `quadratic_formula`
- auto status: **PASS**

### easy

- `x^{2} + x - 6 = 0`
- `x^{2} + 2x - 3 = 0`

### medium

- `3x^{2} + 54x + 240 = 0`
- `3x^{2} + 24x = 0`

### hard

- `4x^{2} + 15x - 8 = 0`
- `3x^{2} + 8x + 14 = 0`

## `quadratic_discriminant` — Understanding the discriminant

- generator: `quadratic_discriminant`
- auto status: **PASS**

### easy

- `\text{Find the discriminant of } x^{2} + 2x - 1.`
- `\text{Find the discriminant of } x^{2} + 3x + 1.`

### medium

- `\text{Find the discriminant of } 3x^{2} + 3x + 3.`
- `\text{Find the discriminant of } 2x^{2} - 7x - 1.`

### hard

- `\text{Find the discriminant of } 4x^{2} - 12x + 8.`
- `\text{Find the discriminant of } 2x^{2} + 16x + 19.`

## `quadratic_completing_square_constant` — Completing the square by finding the constant

- generator: `quadratic_completing_square_constant`
- auto status: **PASS**

### easy

- `x^{2} + 2x + c \text{ is a perfect square trinomial. Find } c.`
- `x^{2} + 2x + c \text{ is a perfect square trinomial. Find } c.`

### medium

- `x^{2} + 10x + c \text{ is a perfect square trinomial. Find } c.`
- `x^{2} - 8x + c \text{ is a perfect square trinomial. Find } c.`

### hard

- `x^{2} - 17x + c \text{ is a perfect square trinomial. Find } c.`
- `x^{2} - 21x + c \text{ is a perfect square trinomial. Find } c.`

## `quadratic_completing_square_solve` — Solving equations by completing the square

- generator: `quadratic_completing_square_solve`
- auto status: **PASS**

### easy

- `x^{2} + 4x + 4 = 0`
- `x^{2} - 6x + 8 = 0`

### medium

- `4x^{2} - 24x - 160 = 0`
- `4x^{2} + 48x - 52 = 0`

### hard

- `3x^{2} - 6x - 24 = 0`
- `4x^{2} - 56x + 248 = 0`
