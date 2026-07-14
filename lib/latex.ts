/**
 * Repair instruction LaTeX corrupted when `\t` in `\text{...}` was parsed as a tab.
 */
export function repairInstructionLatex(latex: string | null | undefined): string {
  if (!latex) {
    return "";
  }

  if (latex.charCodeAt(0) === 9 && latex.startsWith("ext", 1)) {
    return `\\text${latex.slice(4)}`;
  }

  if (latex.startsWith("ext{")) {
    return `\\text{${latex.slice(4)}`;
  }

  return latex;
}

const UNSIGNED_NUM = String.raw`\d+(?:\.\d+)?(?:[eE][+-]?\d+)?`;

/**
 * Collapse awkward sign juxtaposition and parenthesize negative slash denominators.
 * Mirrors `packages/polynomial_core/latex.normalize_expression_signs`.
 *
 * Examples: `5+-2` → `5-2`, `2/-1` → `2/(-1)`, `2*x+-3` → `2*x-3`.
 */
export function normalizeExpressionSigns(expr: string | null | undefined): string {
  if (!expr) {
    return "";
  }

  let s = expr;
  for (let i = 0; i < 8; i++) {
    const prev = s;
    s = s.replace(/\+-/g, "-");
    s = s.replace(/-\+/g, "-");
    s = s.replace(/--/g, "+");
    s = s.replace(/\s+\+\s+-/g, " - ");
    s = s.replace(/\s+-\s+\+/g, " - ");
    s = s.replace(/\s+-\s+-/g, " + ");
    s = s.replace(new RegExp(`/(\\s*)-(${UNSIGNED_NUM})(?!\\))`, "g"), "/($1-$2)");
    s = s.replace(new RegExp(`/\\(\\s*-(${UNSIGNED_NUM})\\s*\\)`, "g"), "/(-$1)");
    s = s.replace(
      new RegExp(`(\\\\div|÷|\\\\cdot|\\*)(\\s*)-(${UNSIGNED_NUM})(?!\\))`, "g"),
      "$1$2(-$3)",
    );
    if (s === prev) break;
  }
  return s;
}

/** Parenthesize a negative numeric token for slash division: `-1` → `(-1)`. */
export function parenIfNegative(value: string | number): string {
  const text = String(value).trim();
  if (text.startsWith("-") && !text.startsWith("(")) {
    return `(${text})`;
  }
  return text;
}

/**
 * Upright unit label for math mode (avoids italicized `cm` / `in` / …).
 * Mirrors `packages/polynomial_core/latex.unit_latex`.
 */
export function unitLatex(unit: string, options?: { leadingSpace?: boolean }): string {
  const u = (unit ?? "").trim();
  if (!u) return "";
  const leadingSpace = options?.leadingSpace !== false;
  return leadingSpace ? `\\text{ ${u}}` : `\\text{${u}}`;
}

/**
 * Numeric (or LaTeX) value with an upright unit suffix.
 * Mirrors `packages/polynomial_core/latex.format_with_unit`.
 *
 * Examples: `3\text{ cm}`, `\frac{3}{2}\text{ cm}`, `5\text{ cm}^{2}`.
 */
export function formatWithUnit(
  value: string | number,
  unit: string,
  options?: { power?: number },
): string {
  const body = String(value);
  const suffix = unitLatex(unit);
  const power = options?.power;
  if (!suffix) {
    if (power != null && power !== 1) return `${body}^{${power}}`;
    return body;
  }
  if (power != null && power !== 1) return `${body}${suffix}^{${power}}`;
  return `${body}${suffix}`;
}

/**
 * Plain-text measurement for diagram labels / prompt text.
 * Mirrors `packages/polynomial_core/latex.format_measurement_text`.
 */
export function formatMeasurementText(
  value: string | number,
  unit: string,
  options?: { power?: number },
): string {
  const body = String(value);
  const u = (unit ?? "").trim();
  const power = options?.power;
  if (!u) {
    if (power != null && power !== 1) return `${body}^${power}`;
    return body;
  }
  if (power != null && power !== 1) return `${body} ${u}^${power}`;
  return `${body} ${u}`;
}

/** Format `a/b` with parentheses around a negative denominator. */
export function formatSlashFraction(
  numerator: string | number,
  denominator: string | number,
): string {
  return `${numerator}/${parenIfNegative(denominator)}`;
}

/**
 * KaTeX `\text{...}` joins words with U+00A0 (nbsp), so long prompts never wrap
 * in multi-column worksheets. Replace those with normal spaces after render.
 */
export function enableKatexSoftWrap(root: HTMLElement): void {
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  const nodes: Text[] = [];
  let node: Node | null = walker.nextNode();
  while (node) {
    if (node.nodeValue?.includes("\u00a0")) {
      nodes.push(node as Text);
    }
    node = walker.nextNode();
  }
  for (const textNode of nodes) {
    textNode.nodeValue = textNode.nodeValue!.replace(/\u00a0/g, " ");
  }
}
