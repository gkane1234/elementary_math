# Topic-fit sample gallery

Review prompts for **topic / method / difficulty shape** — not answer correctness.

## `polynomial_naming` — Naming

- generator: `polynomial_naming`
- auto status: **PASS**

### easy

- `3x^{2}-2x-2`
- `x^{2}-3x-2`
- `x^{2}+2x+1`

### medium

- `5x^{3}+3x^{2}-2x-7`
- `8x^{3}-6x^{2}+6x-9`
- `7x^{3}-3x^{2}+3x-8`

### hard

- `15x^{5}+14x^{4}-12x^{3}+2x^{2}+21x-6`
- `11x^{5}+3x^{4}-9x^{3}+16x^{2}+20x+7`
- `19x^{2}-7x+14`

## `polynomial_add_subtract` — Adding and subtracting

- generator: `polynomial_add_subtract`
- auto status: **PASS**

### easy

- `(3x^{2}+3x+2) + (2x^{2}-3x+1)`
- `(2x^{2}-2x-3) + (3x^{2}-x-2)`
- `(2x-3) + (2x-1)`

### medium

- `(9x^{3}+5x^{2}-8x+3) - (10x^{3}+3x^{2}-4x-10)`
- `(2x^{2}+8x+6) + (10x^{2}-3x-9)`
- `(2x^{2}-10x-4) + (6x^{2}-2x+10)`

### hard

- `(22x^{5}-17x^{4}-21x^{3}+17x^{2}+22x+17) + (10x^{5}-10x^{4}+15x^{3}-4x^{2}-15x-7)`
- `(13x^{2}+17x+10) + (15x^{2}-12x-12)`
- `(4x^{2}+8x+15) + (3x^{2}-4x-1)`

## `polynomial_multiply` — Multiplying

- generator: `polynomial_multiply`
- auto status: **PASS**

### easy

- `(x)(x-2)`
- `(x^{2})(x-3)`
- `(x-2)(x^{2})`

### medium

- `(6x-7)(5x)`
- `(3x^{2}+3x-9)(9x^{3})`
- `(3x^{2}-6)(2x^{3})`

### hard

- `(10x^{4})(9x^{2}+4x+6)`
- `(9x^{5}+x^{2}+1)(17x^{4}+6x^{2}+12x-6)`
- `(15x^{4}+14x^{3}-9x^{2}-17)(9x^{4}+17x^{3}+14)`

## `polynomial_multiply_special` — Multiplying special cases

- generator: `polynomial_multiply_special`
- auto status: **PASS**

### easy

- `(x + 2)(x - 2)`
- `(x + 5)(x - 1)`
- `(x + 4)(x - 4)`

### medium

- `(x - 1)^2`
- `(x + 4)^2`
- `(x + 5)(x + 4)`

### hard

- `(6x + 3)(6x - 3)`
- `(6x + 4)(6x - 4)`
- `(3x + 1)^2`

## `polynomial_factoring_common_factor` — Common factor only

- generator: `polynomial_factoring_common_factor`
- auto status: **PASS**

### easy

- `2x^{2}+2x+4`
- `3x^{2}-6`
- `2x^{2}+4x+4`

### medium

- `3x^{3}+6x^{2}+3x`
- `25x^{2}-15x+15`
- `30x^{3}-20x^{2}+15x`

### hard

- `63x^{2}+56x-21`
- `16x^{3}-28x^{2}-44x+36`
- `15x^{2}+70x-5`

## `quadratic_factoring` — Quadratic expressions

- generator: `quadratic_factoring`
- auto status: **PASS**

### easy

- `x^{2}+4x-5`
- `x^{2}+2x-15`
- `x^{2}-6x+8`

### medium

- `6x^{2}-90x+336`
- `2x^{2}+8x-24`
- `5x^{2}+25x-70`

### hard

- `4x^{2}-44x+121`
- `16x^{2}+112x+196`
- `16x^{2}-81`

## `polynomial_factoring_special_cases` — Special cases

- generator: `polynomial_factoring_special_cases`
- auto status: **PASS**

### easy

- `x^{2}+2x+1`
- `x^{2}-2x+1`
- `x^{2}-2x+1`

### medium

- `9x^{2}-6x+1`
- `16x^{2}-9`
- `4x^{2}+4x+1`

### hard

- `25x^{2}-4`
- `5x^{3}-135`
- `x^{8}-1`

## `polynomial_factoring_grouping` — By grouping

- generator: `polynomial_factoring_grouping`
- auto status: **PASS**

### easy

- `x^{3}+x^{2}+5x+5`
- `x^{3}-2x^{2}-5x+10`
- `x^{3}-3x^{2}-x+3`

### medium

- `2x^{3}-16x^{2}+x-8`
- `2x^{3}+20x^{2}+6x+60`
- `3x^{3}+27x^{2}+6x+54`

### hard

- `3x^{3}-39x^{2}-3x+39`
- `2x^{3}-16x^{2}+3x-24`
- `2x^{3}+22x^{2}-7x-77`

## `quadratic_solve_by_graphing` — Solving equations by graphing

- generator: `solve_polynomial_by_graphing`
- auto status: **PASS**

### easy

- `x^{2} - 4x + 3 = 0`
- `x^{2} + 5x + 6 = 0`
- `x^{2} - 4 = 0`

### medium

- `3x^{2} - 3 = 0`
- `2x^{2} + 6x = 0`
- `2(x + 3)(x - 4) = 0`

### hard

- `-4x^{2} - 4x + 8 = 0`
- `3(x + 6)(x - 2) = 0`
- `-2(x + 5)(x - 7) = 0`

## `quadratic_square_roots` — Solving equations by taking square roots

- generator: `quadratic_square_roots`
- auto status: **PASS**

### easy

- `x^{2} = 9`
- `(x + 2)^{2} = 9`
- `(x + 2)^{2} = 9`

### medium

- `2(x - 1)^{2} = 8`
- `(x - 2)^{2} - 4 = 0`
- `5(x + 3)^{2} - 80 = 0`

### hard

- `6(x + 2)^{2} - 60 = 0`
- `3x^{2} - 36x + 78 = 0`
- `6(x - 3)^{2} = 42`

## `quadratic_factoring_equations` — Solving equations by factoring

- generator: `quadratic_factoring_equations`
- auto status: **PASS**

### easy

- `x^{2}-6x+9 = 0`
- `x^{2}-x-6 = 0`
- `x^{2}+6x+9 = 0`

### medium

- `3x^{2}+15x-72 = 0`
- `3x^{2}+66x+363 = 0`
- `4x^{2}-20x-96 = 0`

### hard

- `16x^{2}-144 = 0`
- `4x^{2}-144 = 0`
- `16x^{2}-32x+16 = 0`

## `quadratic_formula` — Solving equations with the Quadratic Formula

- generator: `quadratic_formula`
- auto status: **PASS**

### easy

- `x^{2} + 3x = 0`
- `x^{2} + 2x + 1 = 0`
- `x^{2} - 1 = 0`

### medium

- `2x^{2} - 2x - 4 = 0`
- `2x^{2} + 10x - 28 = 0`
- `4x^{2} - 24x = 0`

### hard

- `4x^{2} - 10x + 1 = 0`
- `2x^{2} - 14x - 4 = 0`
- `3x^{2} - 3x + 10 = 0`

## `quadratic_discriminant` — Understanding the discriminant

- generator: `quadratic_discriminant`
- auto status: **PASS**

### easy

- `\text{Find the discriminant of } x^{2} + x - 2.`
- `\text{Find the discriminant of } x^{2} + 3x - 3.`
- `\text{Find the discriminant of } x^{2} + x - 1.`

### medium

- `\text{Find the discriminant of } 4x^{2} - 5x + 7.`
- `\text{Find the discriminant of } 4x^{2} + 2x + 6.`
- `\text{Find the discriminant of } 2x^{2} - 3x - 6.`

### hard

- `\text{Find the discriminant of } 2x^{2} - 12x + 9.`
- `\text{Find the discriminant of } 4x^{2} + 20x - 13.`
- `\text{Find the discriminant of } 2x^{2} + 16x + 21.`

## `quadratic_completing_square_constant` — Completing the square by finding the constant

- generator: `quadratic_completing_square_constant`
- auto status: **NOTE**
- auto notes: weak E/H diversity: same skeleton after number-normalization

### easy

- `x^{2} - 6x + c \text{ is a perfect square trinomial. Find } c.`
- `x^{2} + 6x + c \text{ is a perfect square trinomial. Find } c.`
- `x^{2} - 4x + c \text{ is a perfect square trinomial. Find } c.`

### medium

- `x^{2} - 12x + c \text{ is a perfect square trinomial. Find } c.`
- `x^{2} + 2x + c \text{ is a perfect square trinomial. Find } c.`
- `x^{2} - 4x + c \text{ is a perfect square trinomial. Find } c.`

### hard

- `x^{2} - 12x + c \text{ is a perfect square trinomial. Find } c.`
- `x^{2} - 20x + c \text{ is a perfect square trinomial. Find } c.`
- `x^{2} + 6x + c \text{ is a perfect square trinomial. Find } c.`

## `quadratic_completing_square_solve` — Solving equations by completing the square

- generator: `quadratic_completing_square_solve`
- auto status: **PASS**

### easy

- `x^{2} + 6x + 5 = 0`
- `x^{2} - 6x = 0`
- `x^{2} - 2x - 8 = 0`

### medium

- `2x^{2} - 24x + 72 = 0`
- `3x^{2} + 42x = 0`
- `2x^{2} + 24x + 72 = 0`

### hard

- `4x^{2} + 64x + 309 = 0`
- `2x^{2} - 20x + 75 = 0`
- `4x^{2} + 48x + 142 = 0`
