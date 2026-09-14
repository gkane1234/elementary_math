# `finding_angles` — Finding angles

> **UNCLEAR** — Not in EA TOC. Confirm old path (inverse trig vs geometry angle chase).

- **Course:** Algebra 1
- **Category:** Algebra 1 — Beginning Trigonometry
- **Generator:** `finding_angles`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Find an acute angle from a trig ratio (inverse trig) or complementary in a right triangle. D=0: obvious 30-60-90 if old has it.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Two angles are supplementary. One measures } 148^\circ.\text{ Find the measure of the other angle.}`
  - answer: `32^\circ`
- seed 207:
  - prompt: `\text{Two angles are supplementary. One measures } 108^\circ.\text{ Find the measure of the other angle.}`
  - answer: `72^\circ`

### D=8

- seed 101:
  - prompt: `\text{Vertical angles measure } (4x + 21)^\circ\text{ and } (5x - 1)^\circ.\text{ Find } x.`
  - answer: `22`
- seed 207:
  - prompt: `\text{Vertical angles measure } (4x + 4)^\circ\text{ and } (x + 34)^\circ.\text{ Find } x.`
  - answer: `10`

### D=16

- seed 101:
  - prompt: `\text{Angles measuring } (4x + 10)^\circ\text{ and } (4x - 8)^\circ\text{ are complementary. Find the measure of an angle that is supplementary to the first angle.}`
  - answer: `126^\circ`
- seed 207:
  - prompt: `\text{Angles measuring } (3x - 16)^\circ\text{ and } (x + 2)^\circ\text{ are complementary. Find the measure of an angle that is supplementary to the first angle.}`
  - answer: `118^\circ`

### D=22

- seed 101:
  - prompt: `\text{Angles measuring } (4x + 10)^\circ\text{ and } (4x - 8)^\circ\text{ are complementary. Find the measure of an angle that is supplementary to the first angle.}`
  - answer: `126^\circ`
- seed 207:
  - prompt: `\text{Angles measuring } (3x - 16)^\circ\text{ and } (x + 2)^\circ\text{ are complementary. Find the measure of an angle that is supplementary to the first angle.}`
  - answer: `118^\circ`

## OpenStax examples + chapter/section cites

### Algebra and Trigonometry 2e — 7.2 Right Triangle Trigonometry

- https://openstax.org/books/algebra-and-trigonometry-2e/pages/7-2-right-triangle-trigonometry
- Shape: Solve for θ given sin θ = 3/5 (calculator) or special triangles.

## Variety notes

Not in EA TOC. Confirm old path (inverse trig vs geometry angle chase).

## Limitations

- UNCLEAR / LIMITATIONS: confirm inverse-trig vs geometry angle chase before engine work.

## Proposed engine (reuse vs new)

Reuse finding_angles. Confirm old path is inverse-trig vs angle-sum.

_Proposal only. No engine implementation in this notes pass._
