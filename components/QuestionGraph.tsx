import {
  evaluateGraphFunction,
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

function NumberLineGraph({ spec }: { spec: NumberLineSpec }) {
  const y = HEIGHT / 2;
  const startX = mapX(spec.min_value, {
    x_min: spec.min_value,
    x_max: spec.max_value,
    y_min: -1,
    y_max: 1,
    functions: [],
    points: [],
  }, WIDTH);
  const endX = mapX(spec.max_value, {
    x_min: spec.min_value,
    x_max: spec.max_value,
    y_min: -1,
    y_max: 1,
    functions: [],
    points: [],
  }, WIDTH);
  const boundaryX = mapX(spec.boundary, {
    x_min: spec.min_value,
    x_max: spec.max_value,
    y_min: -1,
    y_max: 1,
    functions: [],
    points: [],
  }, WIDTH);
  const boundaryHighX =
    spec.boundary_high !== undefined
      ? mapX(spec.boundary_high, {
          x_min: spec.min_value,
          x_max: spec.max_value,
          y_min: -1,
          y_max: 1,
          functions: [],
          points: [],
        }, WIDTH)
      : null;

  const ticks: number[] = [];
  for (let value = spec.min_value; value <= spec.max_value; value += spec.tick_interval) {
    ticks.push(value);
  }

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
      aria-label="Number line"
    >
      <line x1={startX} y1={y} x2={endX} y2={y} className="graph-axis" />
      <polygon
        points={`${shadeStart},${y - 8} ${shadeEnd},${y - 8} ${shadeEnd},${y + 8} ${shadeStart},${y + 8}`}
        className="graph-shade"
      />
      {ticks.map((tick) => {
        const x = mapX(tick, {
          x_min: spec.min_value,
          x_max: spec.max_value,
          y_min: -1,
          y_max: 1,
          functions: [],
          points: [],
        }, WIDTH);
        return (
          <g key={tick}>
            <line x1={x} y1={y - 6} x2={x} y2={y + 6} className="graph-tick" />
            <text x={x} y={y + 20} textAnchor="middle" className="graph-label">
              {tick}
            </text>
          </g>
        );
      })}
      <circle
        cx={boundaryX}
        cy={y}
        r={5}
        className={spec.inclusive ? "graph-boundary-filled" : "graph-boundary-open"}
      />
      {boundaryHighX !== null && (
        <circle cx={boundaryHighX} cy={y} r={5} className="graph-boundary-open" />
      )}
    </svg>
  );
}

function CoordinatePlaneGraph({ spec }: { spec: GraphSpec }) {
  const width = WIDTH;
  const height = PLANE_HEIGHT;
  const originX = mapX(0, spec, width);
  const originY = mapY(0, spec, height);
  const showGrid = spec.show_grid !== false;
  const showPoints = spec.show_points !== false;

  const xTicks: number[] = [];
  for (let x = Math.ceil(spec.x_min); x <= Math.floor(spec.x_max); x += 1) {
    xTicks.push(x);
  }
  const yTicks: number[] = [];
  for (let y = Math.ceil(spec.y_min); y <= Math.floor(spec.y_max); y += 1) {
    yTicks.push(y);
  }

  const linePaths: string[][] = [];
  for (const fn of spec.functions) {
    const linePoints: string[] = [];
    const steps = 40;
    for (let index = 0; index <= steps; index += 1) {
      const x = spec.x_min + ((spec.x_max - spec.x_min) * index) / steps;
      const y = evaluateGraphFunction(fn, x);
      if (y === null || y < spec.y_min || y > spec.y_max) continue;
      linePoints.push(`${mapX(x, spec, width)},${mapY(y, spec, height)}`);
    }
    if (linePoints.length > 1) {
      linePaths.push(linePoints);
    }
  }

  return (
    <svg
      className="question-graph coordinate-plane-graph"
      viewBox={`0 0 ${width} ${height}`}
      role="img"
      aria-label="Coordinate plane"
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
        spec.points.map(([x, y], index) => (
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
    return <CoordinatePlaneGraph spec={metadata.graph_spec} />;
  }
  return null;
}

export function QuestionGraphFromMetadata({
  metadata,
}: {
  metadata?: Record<string, unknown>;
}) {
  const graph = metadata
    ? {
        number_line_spec: metadata.number_line_spec as NumberLineSpec | undefined,
        graph_spec: metadata.graph_spec as GraphSpec | undefined,
      }
    : null;
  if (!graph?.number_line_spec && !graph?.graph_spec) return null;
  return <QuestionGraph metadata={graph} />;
}
