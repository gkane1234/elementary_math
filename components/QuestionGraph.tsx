import {
  evaluateGraphFunction,
  extractGraphMetadata,
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

/** Build polyline samples for a function, clipped to the visible plane. */
function sampleFunctionPath(fn: string, spec: GraphSpec, width: number, height: number): string[] {
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
      `${mapX(cx0, spec, width)},${mapY(cy0, spec, height)}`,
      `${mapX(cx1, spec, width)},${mapY(cy1, spec, height)}`,
    ];
  }

  const linePoints: string[] = [];
  const steps = 80;
  for (let index = 0; index <= steps; index += 1) {
    const x = spec.x_min + ((spec.x_max - spec.x_min) * index) / steps;
    const y = evaluateGraphFunction(fn, x);
    if (y === null || y < spec.y_min || y > spec.y_max) continue;
    linePoints.push(`${mapX(x, spec, width)},${mapY(y, spec, height)}`);
  }
  return linePoints;
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

  return (
    <svg
      className="question-graph number-line-graph"
      viewBox={`0 0 ${WIDTH} ${HEIGHT}`}
      role="img"
      aria-label={blank ? "Blank number line" : "Number line"}
    >
      <line x1={startX} y1={y} x2={endX} y2={y} className="graph-axis" />
      {!blank && (
        <polygon
          points={`${shadeStart},${y - 8} ${shadeEnd},${y - 8} ${shadeEnd},${y + 8} ${shadeStart},${y + 8}`}
          className="graph-shade"
        />
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
        <circle cx={boundaryHighX} cy={y} r={5} className="graph-boundary-open" />
      )}
    </svg>
  );
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
  const showPoints = !blankRole && spec.show_points !== false && points.length > 0;
  const blank =
    blankRole || ((functions.length ?? 0) === 0 && (points.length ?? 0) === 0);

  const xTicks: number[] = [];
  for (let x = Math.ceil(spec.x_min); x <= Math.floor(spec.x_max); x += 1) {
    xTicks.push(x);
  }
  const yTicks: number[] = [];
  for (let y = Math.ceil(spec.y_min); y <= Math.floor(spec.y_max); y += 1) {
    yTicks.push(y);
  }

  const linePaths: string[][] = [];
  for (const fn of functions) {
    const linePoints = sampleFunctionPath(fn, spec, width, height);
    if (linePoints.length > 1) {
      linePaths.push(linePoints);
    }
  }

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
      {linePaths.map((linePoints, lineIndex) => (
        <polyline
          key={`graph-line-${lineIndex}`}
          points={linePoints.join(" ")}
          className="graph-line"
          fill="none"
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
