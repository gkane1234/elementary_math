# Stage 1 inventory — `4-9-newtons-method`

- **Book:** `calculus-volume-1`
- **Title:** 4.9 Newton’s Method
- **Source:** https://openstax.org/books/calculus-volume-1/pages/4-9-newtons-method
- **Local:** `textbooks/openstax/html/calculus-volume-1/4-9-newtons-method.html`
- **Extracted:** 2026-07-28T21:56:34.511834+00:00
- **Items:** 67

## Learning objectives

- 4.9.1 Describe the steps of Newton’s method.
- 4.9.2 Explain what an iterative process means.
- 4.9.3 Recognize when Newton’s method does not work.
- 4.9.4 Apply iterative processes to various situations.

## Counts by kind

- `checkpoint`: 4
- `example`: 4
- `section_exercise`: 59

## Items (document order)

### 1. [example] Example 4.46

- **Near heading:** Describing Newton’s Method
- **Has solution:** True
- **Anchor:** `fs-id1165043423917`
- **Prompt:** Finding a Root of a Polynomial Use Newton’s method to approximate a root of $f (x) = x^{3} - 3 x + 1$ in the interval $\left[\right. 1 , 2 \left]\right. .$ Let $x_{0} = 2$ and find $x_{1} , x_{2} , x_{3} , x_{4} ,$ and $x_{5} .$
- **LaTeX bits:**
  - `$f (x) = x^{3} - 3 x + 1$`
  - `$\left[\right. 1 , 2 \left]\right. .$`
  - `$x_{0} = 2$`
  - `$x_{1} , x_{2} , x_{3} , x_{4} ,$`
  - `$x_{5} .$`

### 2. [checkpoint] Checkpoint 4.45

- **Near heading:** Finding a Root of a Polynomial
- **Has solution:** False
- **Anchor:** `fs-id1165043433379`
- **Prompt:** Letting $x_{0} = 0 ,$ let’s use Newton’s method to approximate the root of $f (x) = x^{3} - 3 x + 1$ over the interval $\left[\right. 0 , 1 \left]\right.$ by calculating $x_{1}$ and $x_{2} .$
- **LaTeX bits:**
  - `$x_{0} = 0 ,$`
  - `$f (x) = x^{3} - 3 x + 1$`
  - `$\left[\right. 0 , 1 \left]\right.$`
  - `$x_{1}$`
  - `$x_{2} .$`

### 3. [example] Example 4.47

- **Near heading:** Finding a Root of a Polynomial
- **Has solution:** True
- **Anchor:** `fs-id1165042936506`
- **Prompt:** Finding a Square Root Use Newton’s method to approximate $\sqrt{2}$ ( Figure 4.79 ). Let $f (x) = x^{2} - 2 ,$ let $x_{0} = 2 ,$ and calculate $x_{1} , x_{2} , x_{3} , x_{4} , x_{5} .$ (We note that since $f (x) = x^{2} - 2$ has a zero at $\sqrt{2} ,$ the initial value $x_{0} = 2$ is a reasonable choice to approximate $\sqrt{2} . \left.\right)$
- **LaTeX bits:**
  - `$\sqrt{2}$`
  - `$f (x) = x^{2} - 2 ,$`
  - `$x_{0} = 2 ,$`
  - `$x_{1} , x_{2} , x_{3} , x_{4} , x_{5} .$`
  - `$f (x) = x^{2} - 2$`
  - `$\sqrt{2} ,$`
  - `$x_{0} = 2$`
  - `$\sqrt{2} . \left.\right)$`

### 4. [checkpoint] Checkpoint 4.46

- **Near heading:** Finding a Square Root
- **Has solution:** False
- **Anchor:** `fs-id1165043098719`
- **Prompt:** Use Newton’s method to approximate $\sqrt{3}$ by letting $f (x) = x^{2} - 3$ and $x_{0} = 3 .$ Find $x_{1}$ and $x_{2} .$
- **LaTeX bits:**
  - `$\sqrt{3}$`
  - `$f (x) = x^{2} - 3$`
  - `$x_{0} = 3 .$`
  - `$x_{1}$`
  - `$x_{2} .$`

### 5. [example] Example 4.48

- **Near heading:** Failures of Newton’s Method
- **Has solution:** True
- **Anchor:** `fs-id1165043091063`
- **Prompt:** When Newton’s Method Fails Consider the function $f (x) = x^{3} - 2 x + 2 .$ Let $x_{0} = 0 .$ Show that the sequence $x_{1} , x_{2} ,\ldots$ fails to approach a root of $f .$
- **LaTeX bits:**
  - `$f (x) = x^{3} - 2 x + 2 .$`
  - `$x_{0} = 0 .$`
  - `$x_{1} , x_{2} ,\ldots$`
  - `$f .$`

### 6. [checkpoint] Checkpoint 4.47

- **Near heading:** When Newton’s Method Fails
- **Has solution:** False
- **Anchor:** `fs-id1165043428456`
- **Prompt:** For $f (x) = x^{3} - 2 x + 2 ,$ let $x_{0} = −1.5$ and find $x_{1}$ and $x_{2} .$
- **LaTeX bits:**
  - `$f (x) = x^{3} - 2 x + 2 ,$`
  - `$x_{0} = −1.5$`
  - `$x_{1}$`
  - `$x_{2} .$`

### 7. [example] Example 4.49

- **Near heading:** Other Iterative Processes
- **Has solution:** True
- **Anchor:** `fs-id1165043210088`
- **Prompt:** Finding a Limit for an Iterative Process Let $F (x) = \frac{1}{2} x + 4$ and let $x_{0} = 0 .$ For all $n \geq 1 ,$ let $x_{n} = F \left(\right. x_{n - 1} \left.\right) .$ Find the values $x_{1} , x_{2} , x_{3} , x_{4} , x_{5} .$ Make a conjecture about what happens to this list of numbers $x_{1} , x_{2} , x_{3} \ldots , x_{n} ,\ldots$ as $n \to \infty .$ If the list of numbers $x_{1} , x_{2} , x_{3} ,\ldots$ approaches a finite number $x \star ,$ then $x \star$ satisfies $x \star = F \left(\right. x \star \left.\right) ,$ and $x \star$ is called a fixed point of $F .$
- **LaTeX bits:**
  - `$F (x) = \frac{1}{2} x + 4$`
  - `$x_{0} = 0 .$`
  - `$n \geq 1 ,$`
  - `$x_{n} = F \left(\right. x_{n - 1} \left.\right) .$`
  - `$x_{1} , x_{2} , x_{3} , x_{4} , x_{5} .$`
  - `$x_{1} , x_{2} , x_{3} \ldots , x_{n} ,\ldots$`
  - `$n \to \infty .$`
  - `$x_{1} , x_{2} , x_{3} ,\ldots$`
  - `$x \star ,$`
  - `$x \star$`
  - `$x \star = F \left(\right. x \star \left.\right) ,$`
  - `$x \star$`
  - _…+1 more_

### 8. [checkpoint] Checkpoint 4.48

- **Near heading:** Finding a Limit for an Iterative Process
- **Has solution:** False
- **Anchor:** `fs-id1165042954795`
- **Prompt:** Consider the function $F (x) = \frac{1}{3} x + 6 .$ Let $x_{0} = 0$ and let $x_{n} = F \left(\right. x_{n - 1} \left.\right)$ for $n \geq 2 .$ Find $x_{1} , x_{2} , x_{3} , x_{4} , x_{5} .$ Make a conjecture about what happens to the list of numbers $x_{1} , x_{2} , x_{3} ,\ldots x_{n} ,\ldots$ as $n \to \infty .$
- **LaTeX bits:**
  - `$F (x) = \frac{1}{3} x + 6 .$`
  - `$x_{0} = 0$`
  - `$x_{n} = F \left(\right. x_{n - 1} \left.\right)$`
  - `$n \geq 2 .$`
  - `$x_{1} , x_{2} , x_{3} , x_{4} , x_{5} .$`
  - `$x_{1} , x_{2} , x_{3} ,\ldots x_{n} ,\ldots$`
  - `$n \to \infty .$`

### 9. [section_exercise] fs-id1165043395265

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043395265`
- **Prompt:** 406 . $f (x) = x^{2} + 1$
- **LaTeX bits:**
  - `$f (x) = x^{2} + 1$`

### 10. [section_exercise] fs-id1165042320000

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165042320000`
- **Prompt:** 407 . $f (x) = x^{3} + 2 x + 1$
- **LaTeX bits:**
  - `$f (x) = x^{3} + 2 x + 1$`

### 11. [section_exercise] fs-id1165043250239

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043250239`
- **Prompt:** 408 . $f (x) = \sin x$
- **LaTeX bits:**
  - `$f (x) = \sin x$`

### 12. [section_exercise] fs-id1165043390900

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043390900`
- **Prompt:** 409 . $f (x) = e^{x}$
- **LaTeX bits:**
  - `$f (x) = e^{x}$`

### 13. [section_exercise] fs-id1165043430597

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043430597`
- **Prompt:** 410 . $f (x) = x^{3} + 3 x e^{x}$
- **LaTeX bits:**
  - `$f (x) = x^{3} + 3 x e^{x}$`

### 14. [section_exercise] fs-id1165042706893

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165042706893`
- **Prompt:** 411 . $f (x) = x^{2} - 4 ,$ with $x_{0} = 0$
- **LaTeX bits:**
  - `$f (x) = x^{2} - 4 ,$`
  - `$x_{0} = 0$`

### 15. [section_exercise] fs-id1165042708723

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165042708723`
- **Prompt:** 412 . $f (x) = x^{2} - 4 x + 3 ,$ with $x_{0} = 2$
- **LaTeX bits:**
  - `$f (x) = x^{2} - 4 x + 3 ,$`
  - `$x_{0} = 2$`

### 16. [section_exercise] fs-id1165042710979

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165042710979`
- **Prompt:** 413 . What is the value of $\text{``} c \\"$ for Newton’s method?
- **LaTeX bits:**
  - `$\text{``} c \\"$`

### 17. [section_exercise] fs-id1165042330022

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165042330022`
- **Prompt:** 414 . $x_{n + 1} = x_{n} ^{2} - \frac{1}{2}$
- **LaTeX bits:**
  - `$x_{n + 1} = x_{n} ^{2} - \frac{1}{2}$`

### 18. [section_exercise] fs-id1165042328680

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165042328680`
- **Prompt:** 415 . $x_{n + 1} = 2 x_{n} \left(\right. 1 - x_{n} \left.\right)$
- **LaTeX bits:**
  - `$x_{n + 1} = 2 x_{n} \left(\right. 1 - x_{n} \left.\right)$`

### 19. [section_exercise] fs-id1165042583690

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165042583690`
- **Prompt:** 416 . $x_{n + 1} = \sqrt{x_{n}}$
- **LaTeX bits:**
  - `$x_{n + 1} = \sqrt{x_{n}}$`

### 20. [section_exercise] fs-id1165043393828

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043393828`
- **Prompt:** 417 . $x_{n + 1} = \frac{1}{\sqrt{x_{n}}}$
- **LaTeX bits:**
  - `$x_{n + 1} = \frac{1}{\sqrt{x_{n}}}$`

### 21. [section_exercise] fs-id1165043286618

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043286618`
- **Prompt:** 418 . $x_{n + 1} = 3 x_{n} \left(\right. 1 - x_{n} \left.\right)$
- **LaTeX bits:**
  - `$x_{n + 1} = 3 x_{n} \left(\right. 1 - x_{n} \left.\right)$`

### 22. [section_exercise] fs-id1165042319140

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165042319140`
- **Prompt:** 419 . $x_{n + 1} = x_{n} ^{2} + x_{n} - 2$
- **LaTeX bits:**
  - `$x_{n + 1} = x_{n} ^{2} + x_{n} - 2$`

### 23. [section_exercise] fs-id1165043131639

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043131639`
- **Prompt:** 420 . $x_{n + 1} = \frac{1}{2} x_{n} - 1$
- **LaTeX bits:**
  - `$x_{n + 1} = \frac{1}{2} x_{n} - 1$`

### 24. [section_exercise] fs-id1165043327548

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043327548`
- **Prompt:** 421 . $x_{n + 1} = \left|\right. x_{n} \left|\right.$
- **LaTeX bits:**
  - `$x_{n + 1} = \left|\right. x_{n} \left|\right.$`

### 25. [section_exercise] fs-id1165042609041

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165042609041`
- **Prompt:** 422 . $x^{2} - 10 = 0$
- **LaTeX bits:**
  - `$x^{2} - 10 = 0$`

### 26. [section_exercise] fs-id1165043379909

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043379909`
- **Prompt:** 423 . $x^{4} - 100 = 0$
- **LaTeX bits:**
  - `$x^{4} - 100 = 0$`

### 27. [section_exercise] fs-id1165042372001

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165042372001`
- **Prompt:** 424 . $x^{2} - x = 0$
- **LaTeX bits:**
  - `$x^{2} - x = 0$`

### 28. [section_exercise] fs-id1165043078171

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043078171`
- **Prompt:** 425 . $x^{3} - x = 0$
- **LaTeX bits:**
  - `$x^{3} - x = 0$`

### 29. [section_exercise] fs-id1165043327755

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043327755`
- **Prompt:** 426 . $x + 5 \cos (x) = 0$
- **LaTeX bits:**
  - `$x + 5 \cos (x) = 0$`

### 30. [section_exercise] fs-id1165043298557

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043298557`
- **Prompt:** 427 . $x + \tan (x) = 0 ,$ choose $x_{0} \in \left(\right. - \frac{\pi}{2} , \frac{\pi}{2} \left.\right)$
- **LaTeX bits:**
  - `$x + \tan (x) = 0 ,$`
  - `$x_{0} \in \left(\right. - \frac{\pi}{2} , \frac{\pi}{2} \left.\right)$`

### 31. [section_exercise] fs-id1165043398519

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043398519`
- **Prompt:** 428 . $\frac{1}{1 - x} = 2$
- **LaTeX bits:**
  - `$\frac{1}{1 - x} = 2$`

### 32. [section_exercise] fs-id1165042639363

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165042639363`
- **Prompt:** 429 . $1 + x + x^{2} + x^{3} + x^{4} = 2$
- **LaTeX bits:**
  - `$1 + x + x^{2} + x^{3} + x^{4} = 2$`

### 33. [section_exercise] fs-id1165043395050

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043395050`
- **Prompt:** 430 . $x^{3} + (x + 1)^{3} = 10^{3}$
- **LaTeX bits:**
  - `$x^{3} + (x + 1)^{3} = 10^{3}$`

### 34. [section_exercise] fs-id1165042660241

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165042660241`
- **Prompt:** 431 . $x = \sin^{2} (x)$
- **LaTeX bits:**
  - `$x = \sin^{2} (x)$`

### 35. [section_exercise] fs-id1165043321501

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043321501`
- **Prompt:** 432 . $\sin x$
- **LaTeX bits:**
  - `$\sin x$`

### 36. [section_exercise] fs-id1165043194445

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043194445`
- **Prompt:** 433 . $\tan (x)$ on $x = \left(\right. \frac{\pi}{2} , \frac{3 \pi}{2} \left.\right)$
- **LaTeX bits:**
  - `$\tan (x)$`
  - `$x = \left(\right. \frac{\pi}{2} , \frac{3 \pi}{2} \left.\right)$`

### 37. [section_exercise] fs-id1165043276362

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043276362`
- **Prompt:** 434 . $e^{x} - 2$
- **LaTeX bits:**
  - `$e^{x} - 2$`

### 38. [section_exercise] fs-id1165042705973

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165042705973`
- **Prompt:** 435 . $\ln (x) + 2$
- **LaTeX bits:**
  - `$\ln (x) + 2$`

### 39. [section_exercise] fs-id1165042708278

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165042708278`
- **Prompt:** 436 . To find candidates for maxima and minima, we need to find the critical points $f^{'} (x) = 0 .$ Show that to solve for the critical points of a function $f (x) ,$ Newton’s method is given by $x_{n + 1} = x_{n} - \frac{f^{'} \left(\right. x_{n} \left.\right)}{f^{''} \left(\right. x_{n} \left.\right)} .$
- **LaTeX bits:**
  - `$f^{'} (x) = 0 .$`
  - `$f (x) ,$`
  - `$x_{n + 1} = x_{n} - \frac{f^{'} \left(\right. x_{n} \left.\right)}{f^{''} \left(\right. x_{n} \left.\right)} .$`

### 40. [section_exercise] fs-id1165042318840

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165042318840`
- **Prompt:** 437 . What additional restrictions are necessary on the function $f ?$
- **LaTeX bits:**
  - `$f ?$`

### 41. [section_exercise] fs-id1165043425469

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043425469`
- **Prompt:** 438 . Minimum of $f (x) = x^{2} + 2 x + 4$
- **LaTeX bits:**
  - `$f (x) = x^{2} + 2 x + 4$`

### 42. [section_exercise] fs-id1165043393663

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043393663`
- **Prompt:** 439 . Minimum of $f (x) = 3 x^{3} + 2 x^{2} - 16$
- **LaTeX bits:**
  - `$f (x) = 3 x^{3} + 2 x^{2} - 16$`

### 43. [section_exercise] fs-id1165042709569

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165042709569`
- **Prompt:** 440 . Minimum of $f (x) = x^{2} e^{x}$
- **LaTeX bits:**
  - `$f (x) = x^{2} e^{x}$`

### 44. [section_exercise] fs-id1165043327319

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043327319`
- **Prompt:** 441 . Maximum of $f (x) = x + \frac{1}{x}$
- **LaTeX bits:**
  - `$f (x) = x + \frac{1}{x}$`

### 45. [section_exercise] fs-id1165042407298

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165042407298`
- **Prompt:** 442 . Maximum of $f (x) = x^{3} + 10 x^{2} + 15 x - 2$
- **LaTeX bits:**
  - `$f (x) = x^{3} + 10 x^{2} + 15 x - 2$`

### 46. [section_exercise] fs-id1165042364609

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165042364609`
- **Prompt:** 443 . Maximum of $f (x) = \frac{\sqrt{x} - \sqrt[3]{x}}{x}$
- **LaTeX bits:**
  - `$f (x) = \frac{\sqrt{x} - \sqrt[3]{x}}{x}$`

### 47. [section_exercise] fs-id1165043431672

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043431672`
- **Prompt:** 444 . Minimum of $f (x) = x^{2} \sin x ,$ closest non-zero minimum to $x = 0$
- **LaTeX bits:**
  - `$f (x) = x^{2} \sin x ,$`
  - `$x = 0$`

### 48. [section_exercise] fs-id1165043426178

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043426178`
- **Prompt:** 445 . Minimum of $f (x) = x^{4} + x^{3} + 3 x^{2} + 12 x + 6$
- **LaTeX bits:**
  - `$f (x) = x^{4} + x^{3} + 3 x^{2} + 12 x + 6$`

### 49. [section_exercise] fs-id1165043427439

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043427439`
- **Prompt:** 446 . Newton’s method, $x^{2} + 2 = 0$
- **LaTeX bits:**
  - `$x^{2} + 2 = 0$`

### 50. [section_exercise] fs-id1165042461106

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165042461106`
- **Prompt:** 447 . Newton’s method, $0 = e^{x}$
- **LaTeX bits:**
  - `$0 = e^{x}$`

### 51. [section_exercise] fs-id1165042374586

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165042374586`
- **Prompt:** 448 . Newton’s method, $0 = 1 + x^{2}$ starting at $x_{0} = 0$
- **LaTeX bits:**
  - `$0 = 1 + x^{2}$`
  - `$x_{0} = 0$`

### 52. [section_exercise] fs-id1165042705923

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165042705923`
- **Prompt:** 449 . Solving $x_{n + 1} = − x_{n} ^{3}$ starting at $x_{0} = −1$
- **LaTeX bits:**
  - `$x_{n + 1} = − x_{n} ^{3}$`
  - `$x_{0} = −1$`

### 53. [section_exercise] fs-id1165043333903

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043333903`
- **Prompt:** 450 . Find a root to $0 = x^{2} - x - 3$ accurate to three decimal places.
- **LaTeX bits:**
  - `$0 = x^{2} - x - 3$`

### 54. [section_exercise] fs-id1165042450785

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165042450785`
- **Prompt:** 451 . Find a root to $0 = \sin x + 3 x$ accurate to four decimal places.
- **LaTeX bits:**
  - `$0 = \sin x + 3 x$`

### 55. [section_exercise] fs-id1165043094076

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043094076`
- **Prompt:** 452 . Find a root to $0 = e^{x} - 2$ accurate to four decimal places.
- **LaTeX bits:**
  - `$0 = e^{x} - 2$`

### 56. [section_exercise] fs-id1165043174650

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043174650`
- **Prompt:** 453 . Find a root to $\ln (x + 2) = \frac{1}{2}$ accurate to four decimal places.
- **LaTeX bits:**
  - `$\ln (x + 2) = \frac{1}{2}$`

### 57. [section_exercise] fs-id1165043394928

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043394928`
- **Prompt:** 454 . Why would you use the secant method over Newton’s method? What are the necessary restrictions on $f ?$
- **LaTeX bits:**
  - `$f ?$`

### 58. [section_exercise] fs-id1165043251688

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043251688`
- **Prompt:** 455 . $f (x) = x^{2} + 2 x + 1 , x_{0} = 1$
- **LaTeX bits:**
  - `$f (x) = x^{2} + 2 x + 1 , x_{0} = 1$`

### 59. [section_exercise] fs-id1165042645634

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165042645634`
- **Prompt:** 456 . $f (x) = x^{2} , x_{0} = 1$
- **LaTeX bits:**
  - `$f (x) = x^{2} , x_{0} = 1$`

### 60. [section_exercise] fs-id1165043183794

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043183794`
- **Prompt:** 457 . $f (x) = \sin x , x_{0} = 1$
- **LaTeX bits:**
  - `$f (x) = \sin x , x_{0} = 1$`

### 61. [section_exercise] fs-id1165042632602

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165042632602`
- **Prompt:** 458 . $f (x) = e^{x} - 1 , x_{0} = 2$
- **LaTeX bits:**
  - `$f (x) = e^{x} - 1 , x_{0} = 2$`

### 62. [section_exercise] fs-id1165042545815

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165042545815`
- **Prompt:** 459 . $f (x) = x^{3} + 2 x + 4 , x_{0} = 0$
- **LaTeX bits:**
  - `$f (x) = x^{3} + 2 x + 4 , x_{0} = 0$`

### 63. [section_exercise] fs-id1165043393688

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043393688`
- **Prompt:** 460 . Use Newton’s method to solve for the eccentric anomaly $E$ when the mean anomaly $M = \frac{\pi}{3}$ and the eccentricity of the orbit $\epsilon = 0.25 ;$ round to three decimals.
- **LaTeX bits:**
  - `$E$`
  - `$M = \frac{\pi}{3}$`
  - `$\epsilon = 0.25 ;$`

### 64. [section_exercise] fs-id1165042320304

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165042320304`
- **Prompt:** 461 . Use Newton’s method to solve for the eccentric anomaly $E$ when the mean anomaly $M = \frac{3 \pi}{2}$ and the eccentricity of the orbit $\epsilon = 0.8 ;$ round to three decimals.
- **LaTeX bits:**
  - `$E$`
  - `$M = \frac{3 \pi}{2}$`
  - `$\epsilon = 0.8 ;$`

### 65. [section_exercise] fs-id1165042710933

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165042710933`
- **Prompt:** 462 . Use Newton’s method to determine the interest rate if the interest was compounded annually.

### 66. [section_exercise] fs-id1165043317181

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043317181`
- **Prompt:** 463 . Use Newton’s method to determine the interest rate if the interest was compounded continuously.

### 67. [section_exercise] fs-id1165043423992

- **Near heading:** Section 4.9 Exercises
- **Has solution:** False
- **Anchor:** `fs-id1165043423992`
- **Prompt:** 464 . The total cost for printing $x$ books can be given by the equation $C (x) = 1000 + 12 x + \left(\right. \frac{1}{2} \left.\right) x^{2 / 3} .$ Use Newton’s method to find the break-even point if the printer sells each book for $\$ 2 0 .$
- **LaTeX bits:**
  - `$x$`
  - `$C (x) = 1000 + 12 x + \left(\right. \frac{1}{2} \left.\right) x^{2 / 3} .$`
  - `$\$ 2 0 .$`

---

_Stage 1 only: inventory. No family tags or EMH yet._
