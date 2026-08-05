"use client";

import {
  DEFAULT_PAGE_LAYOUT,
  TARGET_PAGE_OPTIONS,
  parseTargetPages,
  type FitScales,
  type PageLayoutSettings,
  type TargetPages,
} from "@/lib/worksheet-page-layout";

type WorksheetPageLayoutControlsProps = {
  settings: PageLayoutSettings;
  fit?: FitScales | null;
  onChange: (next: PageLayoutSettings) => void;
};

function statusMessage(fit: FitScales | null | undefined): string | null {
  if (!fit) return null;
  if (fit.targetPages === "auto") {
    return `About ${fit.estimatedPages} page${fit.estimatedPages === 1 ? "" : "s"} at current spacing.`;
  }
  if (fit.status === "overflow") {
    return `Still overflows ${fit.targetPages} page${fit.targetPages === 1 ? "" : "s"} at minimum size — reduce question count or use more columns.`;
  }
  if (fit.status === "tight") {
    return `Tightened spacing/size to fit ${fit.targetPages} page${fit.targetPages === 1 ? "" : "s"}.`;
  }
  if (fit.status === "spread") {
    return `Spaced content to fill ${fit.targetPages} page${fit.targetPages === 1 ? "" : "s"}.`;
  }
  return null;
}

export function WorksheetPageLayoutControls({
  settings = DEFAULT_PAGE_LAYOUT,
  fit = null,
  onChange,
}: WorksheetPageLayoutControlsProps) {
  const hint = statusMessage(fit);

  return (
    <div className="worksheet-page-layout-controls">
      <label className="field field-inline">
        <input
          type="checkbox"
          checked={settings.showPageBreaks}
          onChange={(event) =>
            onChange({ ...settings, showPageBreaks: event.target.checked })
          }
        />
        <span>Show page breaks</span>
      </label>

      <label className="field">
        <span>Target pages</span>
        <select
          value={String(settings.targetPages)}
          onChange={(event) =>
            onChange({
              ...settings,
              targetPages: parseTargetPages(event.target.value) as TargetPages,
            })
          }
        >
          {TARGET_PAGE_OPTIONS.map((option) => (
            <option key={String(option.value)} value={String(option.value)}>
              {option.label}
            </option>
          ))}
        </select>
      </label>

      {hint && <p className="settings-hint worksheet-page-layout-hint">{hint}</p>}
    </div>
  );
}
