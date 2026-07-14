export type NumberLineSpec = {
  min_value: number;
  max_value: number;
  boundary: number;
  boundary_high?: number;
  direction: "left" | "right" | "both" | "outside";
  inclusive: boolean;
  inclusive_high?: boolean;
  tick_interval: number;
  /** When true (default), mark and label 0. Unit ticks are never drawn. */
  show_zero?: boolean;
  /** When true, render axes/ticks only (no shading or boundary markers). */
  blank?: boolean;
};

export type GraphRegion = {
  kind: "half_plane";
  m: number;
  b: number;
  op: ">" | ">=" | "<" | "<=";
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
  /** Half-plane shades for linear inequality answer keys. */
  regions?: GraphRegion[];
};

export type GraphRole = "blank" | "stimulus";

export type QuestionGraphMetadata = {
  /** Prompt graph: blank plane/line or stimulus with solution drawn. */
  number_line_spec?: NumberLineSpec;
  graph_spec?: GraphSpec;
  /** Solution graph for answer key (when prompt is blank). */
  answer_number_line_spec?: NumberLineSpec;
  answer_graph_spec?: GraphSpec;
  graph_role?: GraphRole;
};

/** Axes/grid/bounds only — strip curves and markers that would reveal the solution. */
export function blankCoordinatePlane(spec: GraphSpec): GraphSpec {
  return {
    ...spec,
    functions: [],
    points: [],
    show_points: false,
    regions: [],
  };
}

export function extractGraphMetadata(
  metadata: Record<string, unknown> | undefined,
  variant: "prompt" | "answer" = "prompt",
): QuestionGraphMetadata | null {
  if (!metadata) return null;

  if (variant === "answer") {
    const answerNumberLine = metadata.answer_number_line_spec as NumberLineSpec | undefined;
    const answerGraph = metadata.answer_graph_spec as GraphSpec | undefined;
    if (!answerNumberLine && !answerGraph) return null;
    return {
      number_line_spec: answerNumberLine,
      graph_spec: answerGraph,
      graph_role: "stimulus",
    };
  }

  const numberLine = metadata.number_line_spec as NumberLineSpec | undefined;
  let graphSpec = metadata.graph_spec as GraphSpec | undefined;
  const graphRole = metadata.graph_role as GraphRole | undefined;
  if (!numberLine && !graphSpec) return null;

  // Defense in depth: blank student-work prompts never draw solution paths.
  if (graphRole === "blank" && graphSpec) {
    graphSpec = blankCoordinatePlane(graphSpec);
  }

  return {
    number_line_spec: numberLine,
    graph_spec: graphSpec,
    answer_number_line_spec: metadata.answer_number_line_spec as NumberLineSpec | undefined,
    answer_graph_spec: metadata.answer_graph_spec as GraphSpec | undefined,
    graph_role: graphRole,
  };
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
  // m*x+b — also accept legacy "+-b" from older emitters (prefer normalized `m*x-b`)
  const linear = normalized.match(/^(-?\d+(?:\.\d+)?(?:e[+-]?\d+)?)\*x\+(-?\d+(?:\.\d+)?(?:e[+-]?\d+)?)$/i);
  if (linear) {
    return Number(linear[1]) * x + Number(linear[2]);
  }
  // m*x-b
  const linearMinus = normalized.match(/^(-?\d+(?:\.\d+)?(?:e[+-]?\d+)?)\*x-(-?\d+(?:\.\d+)?(?:e[+-]?\d+)?)$/i);
  if (linearMinus) {
    return Number(linearMinus[1]) * x - Number(linearMinus[2]);
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
  const cubicMatch = normalized.match(
    /^(-?\d+(?:\.\d+)?)\*x\^3\+(-?\d+(?:\.\d+)?)\*x\^2\+(-?\d+(?:\.\d+)?)\*x\+(-?\d+(?:\.\d+)?)$/,
  );
  if (cubicMatch) {
    const a = Number(cubicMatch[1]);
    const b = Number(cubicMatch[2]);
    const c = Number(cubicMatch[3]);
    const d = Number(cubicMatch[4]);
    return ((a * x + b) * x + c) * x + d;
  }
  const quadMatch = normalized.match(
    /^(-?\d+(?:\.\d+)?)\*x\^2\+(-?\d+(?:\.\d+)?)\*x\+(-?\d+(?:\.\d+)?)$/,
  );
  if (quadMatch) {
    const a = Number(quadMatch[1]);
    const b = Number(quadMatch[2]);
    const c = Number(quadMatch[3]);
    return a * x * x + b * x + c;
  }

  // a*b^(x-h)+k — base may be decimal or (p/q); optional a*, (x±h), ±k
  const expMatch = normalized.match(
    /^(-?\d+(?:\.\d+)?)?\*?(?:\((\d+)\/(\d+)\)|(\d+(?:\.\d+)?))\^(?:\((x([+-]\d+(?:\.\d+)?)?)\)|(x))([+-]\d+(?:\.\d+)?)?$/,
  );
  if (expMatch) {
    const scale = expMatch[1] !== undefined ? Number(expMatch[1]) : 1;
    const fracNum = expMatch[2];
    const fracDen = expMatch[3];
    const decimalBase = expMatch[4];
    const base =
      fracNum !== undefined && fracDen !== undefined
        ? Number(fracNum) / Number(fracDen)
        : Number(decimalBase);
    const shiftRaw = expMatch[6];
    const shift = shiftRaw !== undefined ? Number(shiftRaw) : 0;
    const tail = expMatch[8] !== undefined ? Number(expMatch[8]) : 0;
    if (!(base > 0) || !Number.isFinite(scale) || !Number.isFinite(tail)) return null;
    const value = scale * base ** (x + shift) + tail;
    return Number.isFinite(value) ? value : null;
  }

  // a*sqrt(x±h)+k
  const sqrtMatch = normalized.match(
    /^(-?\d+(?:\.\d+)?)?\*?sqrt\(x([+-]\d+(?:\.\d+)?)?\)([+-]\d+(?:\.\d+)?)?$/,
  );
  if (sqrtMatch) {
    const scale = sqrtMatch[1] !== undefined ? Number(sqrtMatch[1]) : 1;
    const shift = sqrtMatch[2] !== undefined ? Number(sqrtMatch[2]) : 0;
    const tail = sqrtMatch[3] !== undefined ? Number(sqrtMatch[3]) : 0;
    const inside = x + shift;
    if (inside < 0) return null;
    const value = scale * Math.sqrt(inside) + tail;
    return Number.isFinite(value) ? value : null;
  }

  // a*log(base,x±h)+k
  const logMatch = normalized.match(
    /^(-?\d+(?:\.\d+)?)?\*?log\((\d+(?:\.\d+)?),x([+-]\d+(?:\.\d+)?)?\)([+-]\d+(?:\.\d+)?)?$/,
  );
  if (logMatch) {
    const scale = logMatch[1] !== undefined ? Number(logMatch[1]) : 1;
    const base = Number(logMatch[2]);
    const shift = logMatch[3] !== undefined ? Number(logMatch[3]) : 0;
    const tail = logMatch[4] !== undefined ? Number(logMatch[4]) : 0;
    const arg = x + shift;
    if (!(base > 0) || base === 1 || arg <= 0) return null;
    const value = scale * (Math.log(arg) / Math.log(base)) + tail;
    return Number.isFinite(value) ? value : null;
  }

  // a/(x±h)+k  or  a/x+k
  const rationalMatch = normalized.match(
    /^(-?\d+(?:\.\d+)?)\/(?:\(x([+-]\d+(?:\.\d+)?)?\)|x)([+-]\d+(?:\.\d+)?)?$/,
  );
  if (rationalMatch) {
    const scale = Number(rationalMatch[1]);
    const shift = rationalMatch[2] !== undefined ? Number(rationalMatch[2]) : 0;
    const tail = rationalMatch[3] !== undefined ? Number(rationalMatch[3]) : 0;
    const denom = x + shift;
    if (Math.abs(denom) < 1e-12) return null;
    const value = scale / denom + tail;
    return Number.isFinite(value) ? value : null;
  }

  return null;
}
