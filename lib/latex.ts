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
