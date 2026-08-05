const WATERMARK_LABEL = "Polynomial Preview";
const TILE_COUNT = 48;

/**
 * Presentation-only overlay for unpaid / non-subscriber worksheet previews.
 * Pointer-events none; does not affect generation or editing.
 */
export function WorksheetWatermark() {
  return (
    <div
      className="worksheet-preview-watermark"
      aria-hidden="true"
      data-watermark="polynomial-preview"
    >
      <div className="worksheet-preview-watermark__pattern">
        {Array.from({ length: TILE_COUNT }, (_, index) => (
          <span key={index} className="worksheet-preview-watermark__tile">
            {WATERMARK_LABEL}
          </span>
        ))}
      </div>
    </div>
  );
}
