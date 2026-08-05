# Stage 1 inventory — `2-5-the-precise-definition-of-a-limit`

- **Book:** `calculus-volume-1`
- **Title:** 2.5 The Precise Definition of a Limit
- **Source:** https://openstax.org/books/calculus-volume-1/pages/2-5-the-precise-definition-of-a-limit
- **Local:** `textbooks/openstax/html/calculus-volume-1/2-5-the-precise-definition-of-a-limit.html`
- **Extracted:** 2026-07-28T21:56:18.163876+00:00
- **Items:** 42

## Learning objectives

- 2.5.1 Describe the epsilon-delta definition of a limit.
- 2.5.2 Apply the epsilon-delta definition to find the limit of a function.
- 2.5.3 Describe the epsilon-delta definitions of one-sided limits and infinite limits.
- 2.5.4 Use the epsilon-delta definition to prove the limit laws.

## Counts by kind

- `checkpoint`: 4
- `example`: 6
- `section_exercise`: 32

## Items (document order)

### 1. [example] Example 2.39

- **Near heading:** Definition
- **Has solution:** True
- **Anchor:** `fs-id1170572333023`
- **Prompt:** Proving a Statement about the Limit of a Specific Function Prove that $\lim_{x \to 1} (2 x + 1) = 3 .$
- **LaTeX bits:**
  - `$\lim_{x \to 1} (2 x + 1) = 3 .$`
  - `$\left|\right. (2 x + 1) - 3 \left|\right.$`
  - `$0 < \left|\right. x - 1 \left|\right. < \delta$`
  - `$\left|\right. (2 x + 1) - 3 \left|\right.$`
  - `$0 < \left|\right. x - 1 \left|\right. < \delta$`
  - `$\left|\right. (2 x + 1) - 3 \left|\right. < \epsilon$`
  - `$0 < \left|\right. x - 1 \left|\right. < \delta & \Rightarrow \left|\right. x - 1 \left|\right. < \delta \\ & \Rightarrow - \delta < x - 1 < \delta \\ & \Rightarrow - \frac{\epsilon}{2} < x - 1 < \frac{\epsilon}{2} \\ & \Rightarrow - \epsilon < 2 x - 2 < \epsilon \\ & \Rightarrow \left|\right. 2 x - 2 \left|\right. < \epsilon \\ & \Rightarrow \left|\right. (2 x + 1) - 3 \left|\right. < \epsilon .$`
  - `$\lim_{x \to 1} (2 x + 1) = 3 .$`
  - `$\epsilon > 0 .$`
  - `$\delta = \epsilon / 2 .$`
  - `$0 < \left|\right. x - 1 \left|\right. < \delta .$`
  - `$\left|\right. (2 x + 1) - 3 \left|\right. & = \left|\right. 2 x - 2 \left|\right. \\ & = \left|\right. 2 (x - 1) \left|\right. \\ & = \left|\right. 2 \left|\right. \left|\right. x - 1 \left|\right. \\ & = 2 \left|\right. x - 1 \left|\right. \\ & < 2 \cdot \delta \\ & = 2 \cdot \frac{\epsilon}{2} \\ & = \epsilon .$`
  - _…+1 more_

### 2. [example] Example 2.40

- **Near heading:** Proving That lim x → a f ( x ) = L lim x → a f ( x ) = L for a Specific Function f ( x ) f ( x )
- **Has solution:** True
- **Anchor:** `fs-id1170571597356`
- **Prompt:** Proving a Statement about a Limit Complete the proof that $\lim_{x \to −1} (4 x + 1) = −3$ by filling in the blanks. Let _____. Choose $\delta = _______.$ Assume $0 < \left|\right. x - _______ \mid < \delta .$ Thus, $\left|\right. ________ - ________ \left|\right. = _____________________________________ \epsilon .$
- **LaTeX bits:**
  - `$\lim_{x \to −1} (4 x + 1) = −3$`
  - `$\delta = _______.$`
  - `$0 < \left|\right. x - _______ \mid < \delta .$`
  - `$\left|\right. ________ - ________ \left|\right. = _____________________________________ \epsilon .$`

### 3. [checkpoint] Checkpoint 2.27

- **Near heading:** Proving a Statement about a Limit
- **Has solution:** False
- **Anchor:** `fs-id1170571712674`
- **Prompt:** Complete the proof that $\lim_{x \to 2} (3 x - 2) = 4$ by filling in the blanks. Let _______. Choose $\delta = _______ .$ Assume $0 < \left|\right. x - ____ \left|\right. < ____ .$ Thus, $\left|\right. _______ - ____ \left|\right. = ______________________________ \epsilon .$ Therefore, $\lim_{x \to 2} (3 x - 2) = 4 .$
- **LaTeX bits:**
  - `$\lim_{x \to 2} (3 x - 2) = 4$`
  - `$\delta = _______ .$`
  - `$0 < \left|\right. x - ____ \left|\right. < ____ .$`
  - `$\left|\right. _______ - ____ \left|\right. = ______________________________ \epsilon .$`
  - `$\lim_{x \to 2} (3 x - 2) = 4 .$`

### 4. [example] Example 2.41

- **Near heading:** Proving a Statement about a Limit
- **Has solution:** True
- **Anchor:** `fs-id1170571657118`
- **Prompt:** Proving a Statement about the Limit of a Specific Function (Geometric Approach) Prove that $\lim_{x \to 2} x^{2} = 4.$
- **LaTeX bits:**
  - `$\lim_{x \to 2} x^{2} = 4.$`

### 5. [checkpoint] Checkpoint 2.28

- **Near heading:** Proving a Statement about the Limit of a Specific Function (Geometric Approach)
- **Has solution:** False
- **Anchor:** `fs-id1170572332174`
- **Prompt:** Find δ corresponding to $\epsilon > 0$ for a proof that $\lim_{x \to 9} \sqrt{x} = 3 .$
- **LaTeX bits:**
  - `$\epsilon > 0$`
  - `$\lim_{x \to 9} \sqrt{x} = 3 .$`

### 6. [example] Example 2.42

- **Near heading:** Proving a Statement about the Limit of a Specific Function (Geometric Approach)
- **Has solution:** True
- **Anchor:** `fs-id1170571690430`
- **Prompt:** Proving a Statement about the Limit of a Specific Function (Algebraic Approach) Prove that $\lim_{x \to −1} \left(\right. x^{2} - 2 x + 3 \left.\right) = 6 .$
- **LaTeX bits:**
  - `$\lim_{x \to −1} \left(\right. x^{2} - 2 x + 3 \left.\right) = 6 .$`

### 7. [checkpoint] Checkpoint 2.29

- **Near heading:** Proving a Statement about the Limit of a Specific Function (Algebraic Approach)
- **Has solution:** False
- **Anchor:** `fs-id1170572243112`
- **Prompt:** Complete the proof that $\lim_{x \to 1} x^{2} = 1 .$ Let $\epsilon > 0 ;$ choose $\delta = \text{min} \left{\right. 1 , \epsilon / 3 \left.\right} ;$ assume $0 < \left|\right. x - 1 \left|\right. < \delta .$ Since $\left|\right. x - 1 \left|\right. < 1 ,$ we may conclude that $−1 < x - 1 < 1 .$ Thus, $1 < x + 1 < 3 .$ Hence, $\left|\right. x + 1 \left|\right. < 3 .$
- **LaTeX bits:**
  - `$\lim_{x \to 1} x^{2} = 1 .$`
  - `$\epsilon > 0 ;$`
  - `$\delta = \text{min} \left{\right. 1 , \epsilon / 3 \left.\right} ;$`
  - `$0 < \left|\right. x - 1 \left|\right. < \delta .$`
  - `$\left|\right. x - 1 \left|\right. < 1 ,$`
  - `$−1 < x - 1 < 1 .$`
  - `$1 < x + 1 < 3 .$`
  - `$\left|\right. x + 1 \left|\right. < 3 .$`

### 8. [example] Example 2.43

- **Near heading:** Proof
- **Has solution:** True
- **Anchor:** `fs-id1170572550055`
- **Prompt:** Showing That a Limit Does Not Exist Show that $\lim_{x \to 0} \frac{\left|\right. x \left|\right.}{x}$ does not exist. The graph of $f (x) = \left|\right. x \left|\right. / x$ is shown here:
- **LaTeX bits:**
  - `$\lim_{x \to 0} \frac{\left|\right. x \left|\right.}{x}$`
  - `$f (x) = \left|\right. x \left|\right. / x$`

### 9. [example] Example 2.44

- **Near heading:** Definition
- **Has solution:** True
- **Anchor:** `fs-id1170572330921`
- **Prompt:** Proving a Statement about a Limit From the Right Prove that $\underset{x \to 4^{+}}{\text{lim}} \sqrt{x - 4} = 0 .$
- **LaTeX bits:**
  - `$\underset{x \to 4^{+}}{\text{lim}} \sqrt{x - 4} = 0 .$`

### 10. [checkpoint] Checkpoint 2.30

- **Near heading:** Proving a Statement about a Limit From the Right
- **Has solution:** False
- **Anchor:** `fs-id1170571711155`
- **Prompt:** Find $\delta$ corresponding to ε for a proof that $\underset{x \to 1^{-}}{\text{lim}} \sqrt{1 - x} = 0 .$
- **LaTeX bits:**
  - `$\delta$`
  - `$\underset{x \to 1^{-}}{\text{lim}} \sqrt{1 - x} = 0 .$`

### 11. [section_exercise] fs-id1170572551886

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170572551886`
- **Prompt:** 176 . $\lim_{x \to a} f (x) = N$
- **LaTeX bits:**
  - `$\lim_{x \to a} f (x) = N$`

### 12. [section_exercise] fs-id1170572233832

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170572233832`
- **Prompt:** 177 . $\lim_{t \to b} g (t) = M$
- **LaTeX bits:**
  - `$\lim_{t \to b} g (t) = M$`

### 13. [section_exercise] fs-id1170571636309

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170571636309`
- **Prompt:** 178 . $\lim_{x \to c} h (x) = L$
- **LaTeX bits:**
  - `$\lim_{x \to c} h (x) = L$`

### 14. [section_exercise] fs-id1170572294410

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170572294410`
- **Prompt:** 179 . $\lim_{x \to a} \varphi (x) = A$
- **LaTeX bits:**
  - `$\lim_{x \to a} \varphi (x) = A$`

### 15. [section_exercise] fs-id1170571699048

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170571699048`
- **Prompt:** 180 . If $0 < \left|\right. x - 2 \left|\right. < \delta ,$ then $\left|\right. f (x) - 2 \left|\right. < 1 .$
- **LaTeX bits:**
  - `$0 < \left|\right. x - 2 \left|\right. < \delta ,$`
  - `$\left|\right. f (x) - 2 \left|\right. < 1 .$`

### 16. [section_exercise] fs-id1170572338483

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170572338483`
- **Prompt:** 181 . If $0 < \left|\right. x - 2 \left|\right. < \delta ,$ then $\left|\right. f (x) - 2 \left|\right. < 0.5 .$
- **LaTeX bits:**
  - `$0 < \left|\right. x - 2 \left|\right. < \delta ,$`
  - `$\left|\right. f (x) - 2 \left|\right. < 0.5 .$`

### 17. [section_exercise] fs-id1170572624813

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170572624813`
- **Prompt:** 182 . If $0 < \left|\right. x - 3 \left|\right. < \delta ,$ then $\left|\right. f (x) + 1 \left|\right. < 1 .$
- **LaTeX bits:**
  - `$0 < \left|\right. x - 3 \left|\right. < \delta ,$`
  - `$\left|\right. f (x) + 1 \left|\right. < 1 .$`

### 18. [section_exercise] fs-id1170571637496

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170571637496`
- **Prompt:** 183 . If $0 < \left|\right. x - 3 \left|\right. < \delta ,$ then $\left|\right. f (x) + 1 \left|\right. < 2 .$
- **LaTeX bits:**
  - `$0 < \left|\right. x - 3 \left|\right. < \delta ,$`
  - `$\left|\right. f (x) + 1 \left|\right. < 2 .$`

### 19. [section_exercise] fs-id1170572618071

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170572618071`
- **Prompt:** 184 . $\epsilon = 1.5$
- **LaTeX bits:**
  - `$\epsilon = 1.5$`

### 20. [section_exercise] fs-id1170572618102

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170572618102`
- **Prompt:** 185 . $\epsilon = 3$
- **LaTeX bits:**
  - `$\epsilon = 3$`

### 21. [section_exercise] fs-id1170572601177

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170572601177`
- **Prompt:** 186 . $\left|\right. \sin (2 x) - \frac{1}{2} \left|\right. < 0.1 ,$ whenever $\left|\right. x - \frac{\pi}{12} \left|\right. < \delta$
- **LaTeX bits:**
  - `$\left|\right. \sin (2 x) - \frac{1}{2} \left|\right. < 0.1 ,$`
  - `$\left|\right. x - \frac{\pi}{12} \left|\right. < \delta$`

### 22. [section_exercise] fs-id1170571599654

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170571599654`
- **Prompt:** 187 . $\left|\right. \sqrt{x - 4} - 2 \left|\right. < 0.1 , \text{whenever} \left|\right. x - 8 \left|\right. < \delta$
- **LaTeX bits:**
  - `$\left|\right. \sqrt{x - 4} - 2 \left|\right. < 0.1 , \text{whenever} \left|\right. x - 8 \left|\right. < \delta$`

### 23. [section_exercise] fs-id1170572551803

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170572551803`
- **Prompt:** 188 . $\lim_{x \to 2} (5 x + 8) = 18$
- **LaTeX bits:**
  - `$\lim_{x \to 2} (5 x + 8) = 18$`

### 24. [section_exercise] fs-id1170572448375

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170572448375`
- **Prompt:** 189 . $\lim_{x \to 3} \frac{x^{2} - 9}{x - 3} = 6$
- **LaTeX bits:**
  - `$\lim_{x \to 3} \frac{x^{2} - 9}{x - 3} = 6$`

### 25. [section_exercise] fs-id1170571610972

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170571610972`
- **Prompt:** 190 . $\lim_{x \to 2} \frac{2 x^{2} - 3 x - 2}{x - 2} = 5$
- **LaTeX bits:**
  - `$\lim_{x \to 2} \frac{2 x^{2} - 3 x - 2}{x - 2} = 5$`

### 26. [section_exercise] fs-id1170572337116

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170572337116`
- **Prompt:** 191 . $\lim_{x \to 0} x^{4} = 0$
- **LaTeX bits:**
  - `$\lim_{x \to 0} x^{4} = 0$`

### 27. [section_exercise] fs-id1170572163828

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170572163828`
- **Prompt:** 192 . $\lim_{x \to 2} \left(\right. x^{2} + 2 x \left.\right) = 8$
- **LaTeX bits:**
  - `$\lim_{x \to 2} \left(\right. x^{2} + 2 x \left.\right) = 8$`

### 28. [section_exercise] fs-id1170571599727

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170571599727`
- **Prompt:** 193 . $\underset{x \to 5^{-}}{\text{lim}} \sqrt{5 - x} = 0$
- **LaTeX bits:**
  - `$\underset{x \to 5^{-}}{\text{lim}} \sqrt{5 - x} = 0$`

### 29. [section_exercise] fs-id1170572217461

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170572217461`
- **Prompt:** 194 . $\underset{x \to 0^{+}}{\text{lim}} f (x) = −2 , \text{where} f (x) = \left{\right. 8 x - 3 , \text{if} x < 0 \\ 4 x - 2 , \text{if} x \geq 0 .$
- **LaTeX bits:**
  - `$\underset{x \to 0^{+}}{\text{lim}} f (x) = −2 , \text{where} f (x) = \left{\right. 8 x - 3 , \text{if} x < 0 \\ 4 x - 2 , \text{if} x \geq 0 .$`

### 30. [section_exercise] fs-id1170571547600

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170571547600`
- **Prompt:** 195 . $\underset{x \to 1^{-}}{\text{lim}} f (x) = 3 , \text{where} f (x) = \left{\right. 5 x - 2 , \text{if} x < 1 \\ 7 x - 1 , \text{if} x \geq 1 .$
- **LaTeX bits:**
  - `$\underset{x \to 1^{-}}{\text{lim}} f (x) = 3 , \text{where} f (x) = \left{\right. 5 x - 2 , \text{if} x < 1 \\ 7 x - 1 , \text{if} x \geq 1 .$`

### 31. [section_exercise] fs-id1170571733891

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170571733891`
- **Prompt:** 196 . $\lim_{x \to 0} \frac{1}{x^{2}} = \infty$
- **LaTeX bits:**
  - `$\lim_{x \to 0} \frac{1}{x^{2}} = \infty$`

### 32. [section_exercise] fs-id1170572233865

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170572233865`
- **Prompt:** 197 . $\lim_{x \to −1} \frac{3}{(x + 1)^{2}} = \infty$
- **LaTeX bits:**
  - `$\lim_{x \to −1} \frac{3}{(x + 1)^{2}} = \infty$`

### 33. [section_exercise] fs-id1170572331909

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170572331909`
- **Prompt:** 198 . $\lim_{x \to 2} - \frac{1}{(x - 2)^{2}} = − \infty$
- **LaTeX bits:**
  - `$\lim_{x \to 2} - \frac{1}{(x - 2)^{2}} = − \infty$`

### 34. [section_exercise] fs-id1170571652896

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170571652896`
- **Prompt:** 199 . An engineer is using a machine to cut a flat square of Aerogel of area 144 cm 2 . If there is a maximum error tolerance in the area of 8 cm 2 , how accurately must the engineer cut on the side, assuming all sides have the same length? How do these numbers relate to $\delta ,$ ε , a , and L ?
- **LaTeX bits:**
  - `$\delta ,$`

### 35. [section_exercise] fs-id1170572551905

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170572551905`
- **Prompt:** 200 . Use the precise definition of limit to prove that the following limit does not exist: $\lim_{x \to 1} \frac{\left|\right. x - 1 \left|\right.}{x - 1} .$
- **LaTeX bits:**
  - `$\lim_{x \to 1} \frac{\left|\right. x - 1 \left|\right.}{x - 1} .$`

### 36. [section_exercise] fs-id1170572626566

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170572626566`
- **Prompt:** 201 . Using precise definitions of limits, prove that $\lim_{x \to 0} f (x)$ does not exist, given that $f (x)$ is the ceiling function. ( Hint : Try any $\delta < 1 .)$
- **LaTeX bits:**
  - `$\lim_{x \to 0} f (x)$`
  - `$f (x)$`
  - `$\delta < 1 .)$`

### 37. [section_exercise] fs-id1170571699078

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170571699078`
- **Prompt:** 202 . Using precise definitions of limits, prove that $\lim_{x \to 0} f (x)$ does not exist: $f (x) = \left{\right. 1 \text{if} x \text{is rational} \\ 0 \text{if} x \text{is irrational} .$ ( Hint : Think about how you can always choose a rational number $0 < r < d ,$ but $\left|\right. f (r) - 0 \left|\right. = 1 .)$
- **LaTeX bits:**
  - `$\lim_{x \to 0} f (x)$`
  - `$f (x) = \left{\right. 1 \text{if} x \text{is rational} \\ 0 \text{if} x \text{is irrational} .$`
  - `$0 < r < d ,$`
  - `$\left|\right. f (r) - 0 \left|\right. = 1 .)$`

### 38. [section_exercise] fs-id1170572444404

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170572444404`
- **Prompt:** 203 . Using precise definitions of limits, determine $\lim_{x \to 0} f (x)$ for $f (x) = \left{\right. x \text{if} x \text{is rational} \\ 0 \text{if} x \text{is irrational} .$ ( Hint : Break into two cases, x rational and x irrational.)
- **LaTeX bits:**
  - `$\lim_{x \to 0} f (x)$`
  - `$f (x) = \left{\right. x \text{if} x \text{is rational} \\ 0 \text{if} x \text{is irrational} .$`

### 39. [section_exercise] fs-id1170571661071

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170571661071`
- **Prompt:** 204 . Using the function from the previous exercise, use the precise definition of limits to show that $\lim_{x \to a} f (x)$ does not exist for $a \neq 0 .$
- **LaTeX bits:**
  - `$\lim_{x \to a} f (x)$`
  - `$a \neq 0 .$`

### 40. [section_exercise] fs-id1170571653079

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170571653079`
- **Prompt:** 205 . $\lim_{x \to a} \left(\right. f (x) + g (x) \left.\right) = L + M$
- **LaTeX bits:**
  - `$\lim_{x \to a} \left(\right. f (x) + g (x) \left.\right) = L + M$`

### 41. [section_exercise] fs-id1170571613536

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170571613536`
- **Prompt:** 206 . $\lim_{x \to a} \left[\right. c f (x) \left]\right. = c L$ for any real constant c ( Hint : Consider two cases: $c = 0$ and $c \neq 0 .)$
- **LaTeX bits:**
  - `$\lim_{x \to a} \left[\right. c f (x) \left]\right. = c L$`
  - `$c = 0$`
  - `$c \neq 0 .)$`

### 42. [section_exercise] fs-id1170571712568

- **Near heading:** Section 2.5 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1170571712568`
- **Prompt:** 207 . $\lim_{x \to a} \left[\right. f (x) g (x) \left]\right. = L M .$ ( Hint : $\left|\right. f (x) g (x) - L M \left|\right. =$ $\left|\right. f (x) g (x) - f (x) M + f (x) M - L M \left|\right. \leq \left|\right. f (x) \left|\right. \left|\right. g (x) - M \left|\right. + \left|\right. M \left|\right. \left|\right. f (x) - L \left|\right. .)$
- **LaTeX bits:**
  - `$\lim_{x \to a} \left[\right. f (x) g (x) \left]\right. = L M .$`
  - `$\left|\right. f (x) g (x) - L M \left|\right. =$`
  - `$\left|\right. f (x) g (x) - f (x) M + f (x) M - L M \left|\right. \leq \left|\right. f (x) \left|\right. \left|\right. g (x) - M \left|\right. + \left|\right. M \left|\right. \left|\right. f (x) - L \left|\right. .)$`

---

_Stage 1 only: inventory. No family tags or EMH yet._
