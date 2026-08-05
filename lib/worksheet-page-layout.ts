/**
 * Letter-page fit helpers for worksheet preview/print.
 *
 * Content height is measured on the print layout; scales map to CSS variables
 * (--ws-space-scale, --ws-font-scale, --ws-gap-scale, --ws-margin-scale).
 */

export type TargetPages = "auto" | 1 | 2 | 3 | 4 | 5 | 6;

export type PageLayoutSettings = {
  showPageBreaks: boolean;
  targetPages: TargetPages;
};

export type FitStatus = "auto" | "tight" | "spread" | "overflow";

export type FitScales = {
  spaceScale: number;
  fontScale: number;
  gapScale: number;
  marginScale: number;
  status: FitStatus;
  estimatedPages: number;
  targetPages: TargetPages;
};

/** Letter at 96dpi. Matches `@page { size: letter; margin: 0.5in }` in globals.css. */
export const LETTER_DPI = 96;
export const LETTER_PAGE_HEIGHT_PX = 11 * LETTER_DPI;
export const LETTER_MARGIN_IN = 0.5;
export const LETTER_MARGIN_PX = LETTER_MARGIN_IN * LETTER_DPI;
export const PAGE_CONTENT_HEIGHT_PX = LETTER_PAGE_HEIGHT_PX - 2 * LETTER_MARGIN_PX;

export const MIN_SPACE_SCALE = 0.35;
export const MAX_SPACE_SCALE = 3;
export const MIN_FONT_SCALE = 0.78;
export const MAX_FONT_SCALE = 1;
export const MIN_GAP_SCALE = 0.4;
export const MAX_GAP_SCALE = 2.25;
export const MIN_MARGIN_SCALE = 0.55;
export const MAX_MARGIN_SCALE = 1;

export const DEFAULT_PAGE_LAYOUT: PageLayoutSettings = {
  showPageBreaks: true,
  targetPages: "auto",
};

export const TARGET_PAGE_OPTIONS: Array<{ value: TargetPages; label: string }> = [
  { value: "auto", label: "Auto" },
  { value: 1, label: "1 page" },
  { value: 2, label: "2 pages" },
  { value: 3, label: "3 pages" },
  { value: 4, label: "4 pages" },
  { value: 5, label: "5 pages" },
  { value: 6, label: "6 pages" },
];

function clamp(value: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, value));
}

export function parseTargetPages(raw: string): TargetPages {
  if (raw === "auto") return "auto";
  const n = Number(raw);
  if (n === 1 || n === 2 || n === 3 || n === 4 || n === 5 || n === 6) return n;
  return "auto";
}

export function estimatePageCount(contentHeightPx: number): number {
  if (contentHeightPx <= 0) return 1;
  return Math.max(1, Math.ceil(contentHeightPx / PAGE_CONTENT_HEIGHT_PX - 1e-6));
}

/**
 * Derive layout scales from natural (unscaled) content height vs target pages.
 * Whitespace scales first; font/margins only when tightening.
 */
export function computeFitScales(
  naturalContentHeightPx: number,
  targetPages: TargetPages,
): FitScales {
  const estimatedPages = estimatePageCount(naturalContentHeightPx);

  if (targetPages === "auto" || naturalContentHeightPx <= 0) {
    return {
      spaceScale: 1,
      fontScale: 1,
      gapScale: 1,
      marginScale: 1,
      status: "auto",
      estimatedPages,
      targetPages,
    };
  }

  const targetHeight = targetPages * PAGE_CONTENT_HEIGHT_PX;
  const ratio = targetHeight / naturalContentHeightPx;

  if (ratio >= 0.98 && ratio <= 1.02) {
    return {
      spaceScale: 1,
      fontScale: 1,
      gapScale: 1,
      marginScale: 1,
      status: "auto",
      estimatedPages: targetPages,
      targetPages,
    };
  }

  if (ratio > 1) {
    // Content short: spread spacing/gaps so material fills toward N pages.
    const spaceScale = clamp(ratio, 1, MAX_SPACE_SCALE);
    const leftover = ratio / spaceScale;
    const gapScale = clamp(leftover, 1, MAX_GAP_SCALE);
    return {
      spaceScale,
      fontScale: 1,
      gapScale,
      marginScale: 1,
      status: "spread",
      estimatedPages: targetPages,
      targetPages,
    };
  }

  // Content tall: tighten spacing, then gaps, then font, then margins.
  let remaining = ratio;
  const spaceScale = clamp(remaining, MIN_SPACE_SCALE, 1);
  remaining = remaining / spaceScale;

  const gapScale = clamp(remaining, MIN_GAP_SCALE, 1);
  remaining = remaining / gapScale;

  const fontScale = clamp(remaining, MIN_FONT_SCALE, 1);
  remaining = remaining / fontScale;

  const marginScale = clamp(remaining, MIN_MARGIN_SCALE, 1);
  remaining = remaining / marginScale;

  const status: FitStatus = remaining < 0.97 ? "overflow" : "tight";

  return {
    spaceScale,
    fontScale,
    gapScale,
    marginScale,
    status,
    estimatedPages: status === "overflow" ? estimatedPages : targetPages,
    targetPages,
  };
}

export function fitScalesToCssVars(scales: FitScales): Record<string, string> {
  return {
    "--ws-space-scale": String(scales.spaceScale),
    "--ws-font-scale": String(scales.fontScale),
    "--ws-gap-scale": String(scales.gapScale),
    "--ws-margin-scale": String(scales.marginScale),
    "--ws-page-content-height": `${PAGE_CONTENT_HEIGHT_PX}px`,
    "--ws-page-margin": `calc(${LETTER_MARGIN_IN}in * var(--ws-margin-scale))`,
  };
}
