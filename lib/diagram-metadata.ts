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
): QuestionDiagramMetadata | null {
  if (!metadata) return null;
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
): boolean {
  const diagram = extractDiagramMetadata(metadata);
  return Boolean(diagram?.diagram_svg);
}
