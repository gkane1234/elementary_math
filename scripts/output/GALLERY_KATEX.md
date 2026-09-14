# KaTeX snippets for `scripts/output` galleries

Working reference: `addsub_cancel_gallery/gallery.html` (single-level) and `diff_skeleton_gallery/` (index + nested topics).

Assets are **local** under `topic_fit/_assets/katex/` — adjust `{katex_rel}` for file depth.

## Head — flat gallery (`<gallery>/gallery.html`)

Replace `{katex_rel}` with `../topic_fit/_assets/katex`.

```html
<link rel="stylesheet" href="../topic_fit/_assets/katex/katex.min.css"/>
<script defer src="../topic_fit/_assets/katex/katex.min.js"></script>
<script defer src="../topic_fit/_assets/katex/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false});"></script>
```

## Head — nested per-type page (`<gallery>/<slug>/gallery.html`)

Replace `{katex_rel}` with `../../topic_fit/_assets/katex`.

```html
<link rel="stylesheet" href="../../topic_fit/_assets/katex/katex.min.css"/>
<script defer src="../../topic_fit/_assets/katex/katex.min.js"></script>
<script defer src="../../topic_fit/_assets/katex/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false});"></script>
```

## Head — index only (`<gallery>/index.html`)

Same as flat gallery: `../topic_fit/_assets/katex`.

## Card body (Python template)

Engine returns bare TeX; wrap for display math:

```python
f"<div class='math'><div class='lab'>Prompt</div>$${row['prompt_latex']}$$</div>"
f"<div class='math'><div class='lab'>Answer</div>$${row.get('answer_latex', '')}$$</div>"
```

## `gen_examples.py` constants (index + nested pages)

```python
KATEX = "../../topic_fit/_assets/katex"       # <slug>/gallery.html
KATEX_INDEX = "../topic_fit/_assets/katex"    # index.html
```

Rule file with full checklist: `.cursor/rules/gallery-html-katex.mdc`.

## NOTES.md on section pages (`skeleton_phase01_gallery`)

`gen_examples.py` prepends topic notes to each `<slug>/gallery.html` when a file exists:

| Location | Example |
|---|---|
| `notes/<type_id>.md` | `notes/g6_equations_word_problems.md` (preferred for catalog stubs) |
| `notes/<slug>.md` | `notes/one_step.md` |
| `<slug>/NOTES.md` | `one_step/NOTES.md` |

Also checks gallery aliases. Start from `notes/_TEMPLATE.md` (includes a required **Limitations** section).

Red header tokens (word boundary): `UNCLEAR`, `LOW_VARIETY`, `LIMITATIONS`, `NOT_IMPLEMENTED`. Header appears above the notes, then the notes body, then example cards (0–N if live generate partially/fails — stub pages still write).

Any catalog `type_id` can get a section page even when not in `SECTIONS`:

```bash
python scripts/output/skeleton_phase01_gallery/gen_examples.py --type-id verbal_expressions
python scripts/output/skeleton_phase01_gallery/gen_examples.py --ensure-stubs   # all missing catalog ids
```

Do not hand-edit `gallery.html` for notes — regenerate the section (`--only <slug>` / `--type-id` is enough; it does not rewrite other sections or `index.html`).
