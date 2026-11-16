"use client";

import type { GalleryEntry } from "@/lib/worksheet-gallery";
import type { SavedWorksheetPreset } from "@/lib/worksheet-presets";

type WorksheetPresetRailProps = {
  topicLabel: string;
  softwareMatches: GalleryEntry[];
  savedMatches: SavedWorksheetPreset[];
  savedPresets: SavedWorksheetPreset[];
  canSave: boolean;
  onSave: () => void;
  onLoadSoftware: (id: string) => void;
  onLoadSaved: (id: string) => void;
  onRemoveSaved: (id: string) => void;
};

export function WorksheetPresetRail({
  topicLabel,
  softwareMatches,
  savedMatches,
  savedPresets,
  canSave,
  onSave,
  onLoadSoftware,
  onLoadSaved,
  onRemoveSaved,
}: WorksheetPresetRailProps) {
  const showingTopic = topicLabel.length > 0;
  const topicRows = showingTopic ? softwareMatches.length + savedMatches.length : 0;

  return (
    <section className="preset-rail interactive-only" aria-label="Worksheet presets">
      <div className="preset-rail-header">
        <h2>Worksheets</h2>
        <button type="button" className="preset-save" disabled={!canSave} onClick={onSave}>
          Save preset
        </button>
      </div>

      {showingTopic && topicRows > 0 && (
        <div className="preset-group">
          <h3>Includes {topicLabel}</h3>
          <ul className="preset-list">
            {softwareMatches.map((entry) => (
              <li key={entry.id}>
                <PresetRow
                  title={entry.title}
                  kind="Included"
                  onLoad={() => onLoadSoftware(entry.id)}
                />
              </li>
            ))}
            {savedMatches.map((preset) => (
              <li key={preset.id}>
                <PresetRow
                  title={preset.title}
                  kind="Saved"
                  onLoad={() => onLoadSaved(preset.id)}
                  onRemove={() => onRemoveSaved(preset.id)}
                />
              </li>
            ))}
          </ul>
        </div>
      )}

      {showingTopic && topicRows === 0 && (
        <p className="hint preset-empty">No worksheet includes this topic.</p>
      )}

      {!showingTopic && savedPresets.length > 0 && (
        <div className="preset-group">
          <h3>Saved</h3>
          <ul className="preset-list">
            {savedPresets.map((preset) => (
              <li key={preset.id}>
                <PresetRow
                  title={preset.title}
                  kind="Saved"
                  onLoad={() => onLoadSaved(preset.id)}
                  onRemove={() => onRemoveSaved(preset.id)}
                />
              </li>
            ))}
          </ul>
        </div>
      )}

      {!showingTopic && savedPresets.length === 0 && (
        <p className="hint preset-empty">
          Save this page, or load an included worksheet from the menu.
        </p>
      )}
    </section>
  );
}

function PresetRow({
  title,
  kind,
  onLoad,
  onRemove,
}: {
  title: string;
  kind: string;
  onLoad: () => void;
  onRemove?: () => void;
}) {
  return (
    <div className="preset-row">
      <span className="preset-row-title">
        <span className="preset-kind">{kind}</span>
        {title}
      </span>
      <span className="preset-row-actions">
        <button type="button" onClick={onLoad}>
          Load
        </button>
        {onRemove && (
          <button type="button" onClick={onRemove}>
            Remove
          </button>
        )}
      </span>
    </div>
  );
}
