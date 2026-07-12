import {
  evaluateGraphFunction,
  extractGraphMetadata,
  type GraphRegion,
  type GraphSpec,
  type NumberLineSpec,
  type QuestionGraphMetadata,
} from "@/lib/graph-metadata";

const WIDTH = 280;
const HEIGHT = 120;
const PLANE_HEIGHT = 220;
const PADDING = 24;

function mapX(value: number, spec: GraphSpec, width: number): number {
  const span = spec.x_max - spec.x_min || 1;
  return PADDING + ((value - spec.x_min) / span) * (width - PADDING * 2);
}

function mapY(value: number, spec: GraphSpec, height: number): number {
  const span = spec.y_max - spec.y_min || 1;
  return height - PADDING - ((value - spec.y_min) / span) * (height - PADDING * 2);
}

/** Liang–Barsky clip of a segment to the axis-aligned view rectangle. */
function clipSegmentToView(
  x0: number,
  y0: number,
  x1: number,
  y1: number,
  spec: GraphSpec,
): [[number, number], [number, number]] | null {
  const xmin = spec.x_min;
  const xmax = spec.x_max;
  const ymin = spec.y_min;
  const ymax = spec.y_max;
  let t0 = 0;
  let t1 = 1;
  const dx = x1 - x0;
  const dy = y1 - y0;
  const checks: Array<[number, number]> = [
    [-dx, x0 - xmin],
    [dx, xmax - x0],
    [-dy, y0 - ymin],
    [dy, ymax - y0],
  ];
  for (const [p, q] of checks) {
    if (p === 0) {
      if (q < 0) return null;
      continue;
    }
    const r = q / p;
    if (p < 0) {
      if (r > t1) return null;
      if (r > t0) t0 = r;
    } else {
      if (r < t0) return null;
      if (r < t1) t1 = r;
    }
  }
  return [
    [x0 + t0 * dx, y0 + t0 * dy],
    [x0 + t1 * dx, y0 + t1 * dy],
  ];
}

/** Parametric / implicit conic markers emitted by conic_sections / polar_graphs. */
function sampleConicPath(fn: string, spec: GraphSpec, width: number, height: number): string[][] | null {
  const normalized = fn.replace(/\s+/g, "");
  const circle = normalized.match(/^circle\((-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)\)$/);
  if (circle) {
    const h = Number(circle[1]);
    const k = Number(circle[2]);
    const r = Number(circle[3]);
    const pts: string[] = [];
    for (let i = 0; i <= 96; i += 1) {
      const t = (2 * Math.PI * i) / 96;
      const x = h + r * Math.cos(t);
      const y = k + r * Math.sin(t);
      if (x < spec.x_min || x > spec.x_max || y < spec.y_min || y > spec.y_max) continue;
      pts.push(`${mapX(x, spec, width)},${mapY(y, spec, height)}`);
    }
    return pts.length > 1 ? [pts] : [];
  }

  const ellipse = normalized.match(
    /^ellipse\((-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)\)$/,
  );
  if (ellipse) {
    const h = Number(ellipse[1]);
    const k = Number(ellipse[2]);
    const a = Number(ellipse[3]);
    const b = Number(ellipse[4]);
    const pts: string[] = [];
    for (let i = 0; i <= 96; i += 1) {
      const t = (2 * Math.PI * i) / 96;
      const x = h + a * Math.cos(t);
      const y = k + b * Math.sin(t);
      if (x < spec.x_min || x > spec.x_max || y < spec.y_min || y > spec.y_max) continue;
      pts.push(`${mapX(x, spec, width)},${mapY(y, spec, height)}`);
    }
    return pts.length > 1 ? [pts] : [];
  }

  const hypH = normalized.match(
    /^hyperbola_h\((-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)\)$/,
  );
  if (hypH) {
    const h = Number(hypH[1]);
    const k = Number(hypH[2]);
    const a = Number(hypH[3]);
    const b = Number(hypH[4]);
    const branches: string[][] = [];
    for (const sign of [-1, 1] as const) {
      const pts: string[] = [];
      for (let i = 0; i <= 48; i += 1) {
        const t = -2 + (4 * i) / 48;
        const x = h + sign * a * Math.cosh(t);
        const y = k + b * Math.sinh(t);
        if (x < spec.x_min || x > spec.x_max || y < spec.y_min || y > spec.y_max) {
          if (pts.length > 1) branches.push(pts.splice(0, pts.length));
          continue;
        }
        pts.push(`${mapX(x, spec, width)},${mapY(y, spec, height)}`);
      }
      if (pts.length > 1) branches.push(pts);
    }
    return branches;
  }

  const hypV = normalized.match(
    /^hyperbola_v\((-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)\)$/,
  );
  if (hypV) {
    const h = Number(hypV[1]);
    const k = Number(hypV[2]);
    const a = Number(hypV[3]);
    const b = Number(hypV[4]);
    const branches: string[][] = [];
    for (const sign of [-1, 1] as const) {
      const pts: string[] = [];
      for (let i = 0; i <= 48; i += 1) {
        const t = -2 + (4 * i) / 48;
        const y = k + sign * a * Math.cosh(t);
        const x = h + b * Math.sinh(t);
        if (x < spec.x_min || x > spec.x_max || y < spec.y_min || y > spec.y_max) {
          if (pts.length > 1) branches.push(pts.splice(0, pts.length));
          continue;
        }
        pts.push(`${mapX(x, spec, width)},${mapY(y, spec, height)}`);
      }
      if (pts.length > 1) branches.push(pts);
    }
    return branches;
  }

  const parV = normalized.match(
    /^parabola_v\((-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)\)$/,
  );
  if (parV) {
    const h = Number(parV[1]);
    const k = Number(parV[2]);
    const p = Number(parV[3]);
    // x^2 = 4p(y - k) with vertex (h, k) → y = (x - h)^2 / (4p) + k
    const segments: string[][] = [];
    let current: string[] = [];
    const steps = 120;
    for (let index = 0; index <= steps; index += 1) {
      const x = spec.x_min + ((spec.x_max - spec.x_min) * index) / steps;
      const y = ((x - h) * (x - h)) / (4 * p) + k;
      if (y < spec.y_min || y > spec.y_max) {
        if (current.length > 1) segments.push(current);
        current = [];
        continue;
      }
      current.push(`${mapX(x, spec, width)},${mapY(y, spec, height)}`);
    }
    if (current.length > 1) segments.push(current);
    return segments;
  }

  const parH = normalized.match(
    /^parabola_h\((-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)\)$/,
  );
  if (parH) {
    const h = Number(parH[1]);
    const k = Number(parH[2]);
    const p = Number(parH[3]);
    const pts: string[] = [];
    for (let i = 0; i <= 80; i += 1) {
      const y = spec.y_min + ((spec.y_max - spec.y_min) * i) / 80;
      const x = h + ((y - k) * (y - k)) / (4 * p);
      if (x < spec.x_min || x > spec.x_max) continue;
      pts.push(`${mapX(x, spec, width)},${mapY(y, spec, height)}`);
    }
    return pts.length > 1 ? [pts] : [];
  }

  return null;
}

/** Build polyline samples for a function, clipped to the visible plane. */
function sampleFunctionPath(fn: string, spec: GraphSpec, width: number, height: number): string[][] {
  const conic = sampleConicPath(fn, spec, width, height);
  if (conic !== null) return conic;

  // Prefer exact endpoint clipping for linear mx+b so the segment spans the view
  // and passes through plotted points without sampling gaps at the y bounds.
  const midX = (spec.x_min + spec.x_max) / 2;
  const yAtMin = evaluateGraphFunction(fn, spec.x_min);
  const yAtMax = evaluateGraphFunction(fn, spec.x_max);
  const yAtMid = evaluateGraphFunction(fn, midX);
  const isLinear =
    yAtMin !== null &&
    yAtMax !== null &&
    yAtMid !== null &&
    Math.abs(yAtMid - (yAtMin + yAtMax) / 2) < 1e-6;

  if (isLinear && yAtMin !== null && yAtMax !== null) {
    const clipped = clipSegmentToView(spec.x_min, yAtMin, spec.x_max, yAtMax, spec);
    if (!clipped) return [];
    const [[cx0, cy0], [cx1, cy1]] = clipped;
    return [
      [
        `${mapX(cx0, spec, width)},${mapY(cy0, spec, height)}`,
        `${mapX(cx1, spec, width)},${mapY(cy1, spec, height)}`,
      ],
    ];
  }

  const segments: string[][] = [];
  let current: string[] = [];
  const steps = 120;
  for (let index = 0; index <= steps; index += 1) {
    const x = spec.x_min + ((spec.x_max - spec.x_min) * index) / steps;
    const y = evaluateGraphFunction(fn, x);
    if (y === null || y < spec.y_min || y > spec.y_max) {
      if (current.length > 1) segments.push(current);
      current = [];
      continue;
    }
    current.push(`${mapX(x, spec, width)},${mapY(y, spec, height)}`);
  }
  if (current.length > 1) segments.push(current);
  return segments;
}

function numberLineAsGraph(spec: NumberLineSpec): GraphSpec {
  return {
    x_min: spec.min_value,
    x_max: spec.max_value,
    y_min: -1,
    y_max: 1,
    functions: [],
    points: [],
  };
}

function NumberLineGraph({ spec }: { spec: NumberLineSpec }) {
  const y = HEIGHT / 2;
  const axis = numberLineAsGraph(spec);
  const startX = mapX(spec.min_value, axis, WIDTH);
  const endX = mapX(spec.max_value, axis, WIDTH);
  const blank = Boolean(spec.blank);
  const showZero = spec.show_zero !== false;
  const zeroInRange = spec.min_value <= 0 && spec.max_value >= 0;

  const boundaryX = mapX(spec.boundary, axis, WIDTH);
  const boundaryHighX =
    spec.boundary_high !== undefined ? mapX(spec.boundary_high, axis, WIDTH) : null;

  const shadeStart =
    spec.direction === "right"
      ? boundaryX
      : spec.direction === "left"
        ? startX
        : boundaryX;
  const shadeEnd =
    spec.direction === "right"
      ? endX
      : spec.direction === "left"
        ? boundaryX
        : (boundaryHighX ?? boundaryX);
  const outside =
    spec.direction === "outside" && boundaryHighX !== null;

  return (
    <svg
      className="question-graph number-line-graph"
      viewBox={`0 0 ${WIDTH} ${HEIGHT}`}
      role="img"
      aria-label={blank ? "Blank number line" : "Number line"}
    >
      <line x1={startX} y1={y} x2={endX} y2={y} className="graph-axis" />
      {!blank && !outside && (
        <polygon
          points={`${shadeStart},${y - 8} ${shadeEnd},${y - 8} ${shadeEnd},${y + 8} ${shadeStart},${y + 8}`}
          className="graph-shade"
        />
      )}
      {!blank && outside && boundaryHighX !== null && (
        <>
          <polygon
            points={`${startX},${y - 8} ${boundaryX},${y - 8} ${boundaryX},${y + 8} ${startX},${y + 8}`}
            className="graph-shade"
          />
          <polygon
            points={`${boundaryHighX},${y - 8} ${endX},${y - 8} ${endX},${y + 8} ${boundaryHighX},${y + 8}`}
            className="graph-shade"
          />
        </>
      )}
      {showZero && zeroInRange && (
        <g>
          <line
            x1={mapX(0, axis, WIDTH)}
            y1={y - 6}
            x2={mapX(0, axis, WIDTH)}
            y2={y + 6}
            className="graph-tick"
          />
          <text x={mapX(0, axis, WIDTH)} y={y + 20} textAnchor="middle" className="graph-label">
            0
          </text>
        </g>
      )}
      {!blank && (
        <circle
          cx={boundaryX}
          cy={y}
          r={5}
          className={spec.inclusive ? "graph-boundary-filled" : "graph-boundary-open"}
        />
      )}
      {!blank && boundaryHighX !== null && (
        <circle
          cx={boundaryHighX}
          cy={y}
          r={5}
          className={
            (spec.inclusive_high ?? spec.inclusive)
              ? "graph-boundary-filled"
              : "graph-boundary-open"
          }
        />
      )}
    </svg>
  );
}

/** Build a polygon for the half-plane y ≷ m x + b clipped to the view box. */
function halfPlanePolygonPoints(
  region: GraphRegion,
  spec: GraphSpec,
  width: number,
  height: number,
): string | null {
  const { m, b, op } = region;
  const xmin = spec.x_min;
  const xmax = spec.x_max;
  const ymin = spec.y_min;
  const ymax = spec.y_max;
  const above = op === ">" || op === ">=";
  const eps = 1e-9;
  const onSide = (x: number, y: number) => {
    const lineY = m * x + b;
    return above ? y >= lineY - eps : y <= lineY + eps;
  };

  const corners: Array<[number, number]> = [
    [xmin, ymin],
    [xmax, ymin],
    [xmax, ymax],
    [xmin, ymax],
  ];
  const edges: Array<[[number, number], [number, number]]> = [
    [corners[0], corners[1]],
    [corners[1], corners[2]],
    [corners[2], corners[3]],
    [corners[3], corners[0]],
  ];

  const hits: Array<[number, number]> = [];
  for (const [[x0, y0], [x1, y1]] of edges) {
    // Segment ∩ line y = mx+b
    const f0 = y0 - (m * x0 + b);
    const f1 = y1 - (m * x1 + b);
    if (Math.abs(f0) < eps) hits.push([x0, y0]);
    if (Math.abs(f1) < eps) hits.push([x1, y1]);
    if (f0 * f1 < 0) {
      const t = f0 / (f0 - f1);
      hits.push([x0 + t * (x1 - x0), y0 + t * (y1 - y0)]);
    }
  }

  const uniq: Array<[number, number]> = [];
  const key = (p: [number, number]) => `${p[0].toFixed(6)},${p[1].toFixed(6)}`;
  const seen = new Set<string>();
  for (const p of [...corners.filter(([x, y]) => onSide(x, y)), ...hits]) {
    const k = key(p);
    if (seen.has(k)) continue;
    seen.add(k);
    uniq.push(p);
  }
  if (uniq.length < 3) return null;

  const cx = uniq.reduce((s, p) => s + p[0], 0) / uniq.length;
  const cy = uniq.reduce((s, p) => s + p[1], 0) / uniq.length;
  uniq.sort((a, b) => Math.atan2(a[1] - cy, a[0] - cx) - Math.atan2(b[1] - cy, b[0] - cx));

  return uniq.map(([x, y]) => `${mapX(x, spec, width)},${mapY(y, spec, height)}`).join(" ");
}

function CoordinatePlaneGraph({
  spec,
  blankRole = false,
}: {
  spec: GraphSpec;
  /** When true (graph_role blank / prompt work plane), never draw curves or points. */
  blankRole?: boolean;
}) {
  const width = WIDTH;
  const height = PLANE_HEIGHT;
  const originX = mapX(0, spec, width);
  const originY = mapY(0, spec, height);
  const showGrid = spec.show_grid !== false;
  const functions = blankRole ? [] : (spec.functions ?? []);
  const points = blankRole ? [] : (spec.points ?? []);
  const regions = blankRole ? [] : (spec.regions ?? []);
  const showPoints = !blankRole && spec.show_points !== false && points.length > 0;
  const blank =
    blankRole ||
    ((functions.length ?? 0) === 0 &&
      (points.length ?? 0) === 0 &&
      (regions.length ?? 0) === 0);

  const xTicks: number[] = [];
  for (let x = Math.ceil(spec.x_min); x <= Math.floor(spec.x_max); x += 1) {
    xTicks.push(x);
  }
  const yTicks: number[] = [];
  for (let y = Math.ceil(spec.y_min); y <= Math.floor(spec.y_max); y += 1) {
    yTicks.push(y);
  }

  const linePaths: { points: string[]; dashed: boolean }[] = [];
  for (let i = 0; i < functions.length; i += 1) {
    const fn = functions[i];
    const region = regions.find(
      (r) =>
        r.kind === "half_plane" &&
        Math.abs(r.m - Number(fn.match(/^(-?\d+(?:\.\d+)?)\*x/)?.[1] ?? NaN)) < 1e-9,
    );
    // Prefer matching by index when regions align with functions.
    const matched = regions[i] ?? region;
    const dashed = matched?.kind === "half_plane" && (matched.op === ">" || matched.op === "<");
    for (const segment of sampleFunctionPath(fn, spec, width, height)) {
      linePaths.push({ points: segment, dashed });
    }
  }

  const shadePolygons = regions
    .filter((r) => r.kind === "half_plane")
    .map((r) => halfPlanePolygonPoints(r, spec, width, height))
    .filter((p): p is string => Boolean(p));

  return (
    <svg
      className="question-graph coordinate-plane-graph"
      viewBox={`0 0 ${width} ${height}`}
      role="img"
      aria-label={blank ? "Blank coordinate plane" : "Coordinate plane"}
    >
      {showGrid &&
        xTicks.map((tick) => {
          const x = mapX(tick, spec, width);
          return (
            <line
              key={`x-grid-${tick}`}
              x1={x}
              y1={PADDING}
              x2={x}
              y2={height - PADDING}
              className="graph-grid"
            />
          );
        })}
      {showGrid &&
        yTicks.map((tick) => {
          const y = mapY(tick, spec, height);
          return (
            <line
              key={`y-grid-${tick}`}
              x1={PADDING}
              y1={y}
              x2={width - PADDING}
              y2={y}
              className="graph-grid"
            />
          );
        })}
      <line
        x1={PADDING}
        y1={originY}
        x2={width - PADDING}
        y2={originY}
        className="graph-axis"
      />
      <line
        x1={originX}
        y1={PADDING}
        x2={originX}
        y2={height - PADDING}
        className="graph-axis"
      />
      {shadePolygons.map((poly, index) => (
        <polygon key={`shade-${index}`} points={poly} className="graph-shade" />
      ))}
      {linePaths.map((line, lineIndex) => (
        <polyline
          key={`graph-line-${lineIndex}`}
          points={line.points.join(" ")}
          className="graph-line"
          fill="none"
          strokeDasharray={line.dashed ? "6 4" : undefined}
        />
      ))}
      {showPoints &&
        points.map(([x, y], index) => (
          <circle
            key={`point-${index}`}
            cx={mapX(x, spec, width)}
            cy={mapY(y, spec, height)}
            r={4}
            className="graph-point"
          />
        ))}
    </svg>
  );
}

type QuestionGraphProps = {
  metadata: QuestionGraphMetadata;
};

export function QuestionGraph({ metadata }: QuestionGraphProps) {
  if (metadata.number_line_spec) {
    return <NumberLineGraph spec={metadata.number_line_spec} />;
  }
  if (metadata.graph_spec) {
    return (
      <CoordinatePlaneGraph
        spec={metadata.graph_spec}
        blankRole={metadata.graph_role === "blank"}
      />
    );
  }
  return null;
}

export function QuestionGraphFromMetadata({
  metadata,
  variant = "prompt",
}: {
  metadata?: Record<string, unknown>;
  /** prompt: blank/stimulus under the question; answer: solution graph on answer key */
  variant?: "prompt" | "answer";
}) {
  const graph = extractGraphMetadata(metadata, variant);
  if (!graph?.number_line_spec && !graph?.graph_spec) return null;
  return <QuestionGraph metadata={graph} />;
}
