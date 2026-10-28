import { useId } from "react";

const WATERMARK_LABEL = "Polynomial Preview";
/** Tile pitch for the repeating diagonal stamp. Large enough for the full label. */
const PATTERN_WIDTH = 340;
const PATTERN_HEIGHT = 168;

/**
 * Presentation-only overlay for unpaid / non-subscriber worksheet previews.
 * Pointer-events none; does not affect generation or editing.
 *
 * A single SVG pattern tiles across the overlay. The previous start-aligned
 * grid packed every stamp at the top of a rotated box, so print/PDF only
 * showed a strip along the top of the page.
 */
export function WorksheetWatermark() {
  const patternId = `worksheet-watermark-${useId().replace(/[^a-zA-Z0-9_-]/g, "")}`;

  return (
    <div
      className="worksheet-preview-watermark"
      aria-hidden="true"
      data-watermark="polynomial-preview"
    >
      <svg
        className="worksheet-preview-watermark__svg"
        xmlns="http://www.w3.org/2000/svg"
        width="100%"
        height="100%"
        focusable="false"
      >
        <defs>
          <pattern
            id={patternId}
            patternUnits="userSpaceOnUse"
            width={PATTERN_WIDTH}
            height={PATTERN_HEIGHT}
            patternTransform="rotate(-28)"
          >
            <text
              x="6"
              y="28"
              fill="#1f2937"
              fontFamily="Segoe UI, Tahoma, Geneva, Verdana, sans-serif"
              fontSize="16"
              fontWeight="700"
              letterSpacing="1.4"
            >
              {WATERMARK_LABEL.toUpperCase()}
            </text>
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill={`url(#${patternId})`} />
      </svg>
    </div>
  );
}
