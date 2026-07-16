# Local OpenStax HTML mirrors

Polite local cache of OpenStax book pages for example mining. **Not committed** (see root `.gitignore`).

OpenStax textbooks are [CC BY-NC-SA](https://creativecommons.org/licenses/by-nc-sa/4.0/). Cite the canonical URL when mining; paraphrase into cards — do not republish exercise banks.

## Books in this curriculum set

| Book slug | Course mapping |
|-----------|----------------|
| `prealgebra-2e` | Pre-Algebra |
| `elementary-algebra-2e` | Algebra 1 |
| `intermediate-algebra-2e` | Algebra 2 |
| `precalculus-2e` | Precalculus |
| `calculus-volume-1` | Calculus |
| `calculus-volume-2` | Calculus |
| `calculus-volume-3` | Calculus |

```powershell
python scripts/mirror_openstax.py --book prealgebra-2e
python scripts/mirror_openstax.py --book elementary-algebra-2e
python scripts/mirror_openstax.py --book intermediate-algebra-2e
python scripts/mirror_openstax.py --book precalculus-2e
python scripts/mirror_openstax.py --book calculus-volume-1
python scripts/mirror_openstax.py --book calculus-volume-2
python scripts/mirror_openstax.py --book calculus-volume-3
```

## Mirror a chapter

```powershell
$env:PYTHONPATH='.'
python scripts/mirror_openstax.py --book calculus-volume-1 --chapter 2 --list-only
python scripts/mirror_openstax.py --book calculus-volume-1 --chapter 2
```

Example URLs this covers (Calculus Volume 1, Chapter 2):

- Introduction → `…/pages/2-introduction`
- 2.1–2.5 sections → `…/pages/2-4-continuity`, etc.
- Chapter Review → `…/pages/2-key-terms`, `2-key-equations`, `2-key-concepts`, `2-review-exercises`

(`2-chapter-review` is a TOC folder only — no HTML page; the script skips it.)

## Layout

```
textbooks/openstax/html/<book-slug>/
  2-introduction.html
  2-1-a-preview-of-calculus.html
  …
  manifest.json
```

HTML keeps **MathML** (`<math>…</math>`), which later mining can convert to LaTeX.

## Whole book

```powershell
python scripts/mirror_openstax.py --book calculus-volume-1
python scripts/mirror_openstax.py --book elementary-algebra-2e
```

Default wait between requests: **1 second**. Re-runs skip existing files unless `--force`.
