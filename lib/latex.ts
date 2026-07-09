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
