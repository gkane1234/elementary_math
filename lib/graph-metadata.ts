export type NumberLineSpec = {
  min_value: number;
  max_value: number;
  boundary: number;
  boundary_high?: number;
  direction: "left" | "right" | "both";
  inclusive: boolean;
  tick_interval: number;
};

export type GraphSpec = {
  x_min: number;
  x_max: number;
  y_min: number;
  y_max: number;
  functions: string[];
  points: [number, number][];
  show_grid?: boolean;
  show_points?: boolean;
};

export type QuestionGraphMetadata = {
  number_line_spec?: NumberLineSpec;
  graph_spec?: GraphSpec;
};

export function extractGraphMetadata(
  metadata: Record<string, unknown> | undefined,
): QuestionGraphMetadata | null {
  if (!metadata) return null;
  const numberLine = metadata.number_line_spec as NumberLineSpec | undefined;
  const graphSpec = metadata.graph_spec as GraphSpec | undefined;
  if (!numberLine && !graphSpec) return null;
  return { number_line_spec: numberLine, graph_spec: graphSpec };
}

export function isNumberLineGraph(metadata: QuestionGraphMetadata): boolean {
  return Boolean(metadata.number_line_spec);
}

export function isCoordinatePlaneGraph(metadata: QuestionGraphMetadata): boolean {
  const spec = metadata.graph_spec;
  if (!spec) return false;
  if (metadata.number_line_spec) return false;
  const hasPlane =
    (spec.points?.length ?? 0) > 0 ||
    (spec.functions?.length ?? 0) > 0 ||
    spec.y_max - spec.y_min > 2;
  return hasPlane;
}

export function evaluateLinearFunction(expression: string, x: number): number | null {
  const normalized = expression.replace(/\s+/g, "");
  const linear = normalized.match(/^(-?\d+(?:\.\d+)?)\*x\+(-?\d+(?:\.\d+)?)$/);
  if (linear) {
    return Number(linear[1]) * x + Number(linear[2]);
  }
  const absMatch = normalized.match(/^(-?\d+(?:\.\d+)?)?\*?abs\(x([+-]\d+(?:\.\d+)?)?\)([+-]\d+(?:\.\d+)?)?$/);
  if (absMatch) {
    const scale = absMatch[1] ? Number(absMatch[1]) : 1;
    const shift = absMatch[2] ? Number(absMatch[2]) : 0;
    const tail = absMatch[3] ? Number(absMatch[3]) : 0;
    return scale * Math.abs(x + shift) + tail;
  }
  return null;
}

export function evaluateGraphFunction(expression: string, x: number): number | null {
  const normalized = expression.replace(/\s+/g, "");
  const linear = evaluateLinearFunction(normalized, x);
  if (linear !== null) return linear;
  const quadMatch = normalized.match(
    /^(-?\d+(?:\.\d+)?)\*x\^2\+(-?\d+(?:\.\d+)?)\*x\+(-?\d+(?:\.\d+)?)$/,
  );
  if (!quadMatch) return null;
  const a = Number(quadMatch[1]);
  const b = Number(quadMatch[2]);
  const c = Number(quadMatch[3]);
  return a * x * x + b * x + c;
}
