# Worksheet page breaks & fit-to-N-pages

## How to use

In **Worksheet settings** (left rail):

1. **Show page breaks** — toggles a print-layout preview under the interactive grid with dashed page markers and a repeating page-height guide. Markers are screen-only; print/PDF uses real page breaks.
2. **Target pages** — `Auto` keeps natural spacing. Choose `1`–`6` to tighten or spread layout toward that page count (questions only; answer key still starts on a new page).

Hint text under the controls reports estimated pages, tighten/spread, or overflow.

## Implementation

| Piece | Role |
| --- | --- |
| `components/WorksheetPageLayoutControls.tsx` | Settings UI |
| `components/WorksheetPageLayout.tsx` | Measures print layout, sets CSS vars, draws markers |
| `lib/worksheet-page-layout.ts` | Letter page constants + fit scale math |
| `app/globals.css` | `--ws-*-scale` vars, screen print preview, print styles |

Fit uses client-side height vs letter content height (11in − 1in margins ≈ 960px at 96dpi). Scales: space → gap → font → margin (tighten); space/gap (spread).

## Limitations

- Approximation: KaTeX/images and `break-inside: avoid` can shift real print breaks vs preview markers.
- `@page` margin stays 0.5in in print; margin scale mainly affects screen preview padding.
- Overflow past min scales is not auto-fixed — reduce questions or increase columns.
- Does not auto-change column count (use the Columns control).
