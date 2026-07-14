/** Geometry diagram metadata emitted by ``question_engine.diagrams``. */

export type DiagramSpec = {
  kind?: string;
  labels?: string[];
  segments?: [string, string][];
  angles?: Array<string | number>;
  points?: Record<string, { x: number; y: number; label?: string | null }>;
};

export type QuestionDiagramMetadata = {
  diagram_svg?: string;
  diagram_latex?: string;
  diagram_spec?: DiagramSpec;
};

export function extractDiagramMetadata(
  metadata: Record<string, unknown> | undefined,
  variant: "prompt" | "answer" = "prompt",
): QuestionDiagramMetadata | null {
  if (!metadata) return null;

  if (variant === "answer") {
    const answerSvg = metadata.answer_diagram_svg;
    if (typeof answerSvg === "string" && answerSvg.trim()) {
      return { diagram_svg: answerSvg };
    }
    // Fall back to stimulus diagram when there is no separate answer figure.
  }

  const svg = metadata.diagram_svg;
  const latex = metadata.diagram_latex;
  const spec = metadata.diagram_spec as DiagramSpec | undefined;
  if (typeof svg !== "string" && typeof latex !== "string" && !spec) {
    return null;
  }
  return {
    diagram_svg: typeof svg === "string" ? svg : undefined,
    diagram_latex: typeof latex === "string" ? latex : undefined,
    diagram_spec: spec,
  };
}

export function hasRenderableDiagram(
  metadata: Record<string, unknown> | undefined,
  variant: "prompt" | "answer" = "prompt",
): boolean {
  const diagram = extractDiagramMetadata(metadata, variant);
  return Boolean(diagram?.diagram_svg);
}

export function hasAnswerDiagram(
  metadata: Record<string, unknown> | undefined,
): boolean {
  const svg = metadata?.answer_diagram_svg;
  return typeof svg === "string" && svg.trim().length > 0;
}
