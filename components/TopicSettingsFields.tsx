import type { SettingField } from "@/lib/types";
import { applyDifficultyPresetToSettings } from "@/lib/difficulty-presets";

const WORKSHEET_LEVEL_KEYS = new Set(["count", "max_columns"]);

/** Soft visual range for the optional difficulty slider (typed values may exceed this). */
const SOFT_DIFFICULTY_SLIDER_MAX = 24;

/** Shared enrichment groups rendered after question-specific settings. */
const COMMON_GROUPS = new Set(["answer", "signs", "presentation"]);

/** Deeper MC controls — only shown when the MC toggle is checked. */
const MC_DETAIL_KEYS = new Set(["multiple_choice_ratio"]);

const CANCEL_FACTOR_COUNT_LABELS: Record<string, string> = {
  random: "Random",
  "0": "None",
  "1": "1 factor",
  "2": "2 factors",
  "3": "3 factors",
  "4": "All (up to 4)",
};

/** Human labels for Layer 0 number profile lane ids (incl. auto override). */
const NUMBER_PROFILE_LABELS: Record<string, string> = {
  auto: "Auto (from difficulty + constraints)",
  friendly_wholes: "Friendly wholes",
  signed_small: "Signed small integers",
  unit_fractions: "Unit fractions",
  simple_rations: "Simple rationals",
  difficult_rations: "Difficult rationals",
  friendly_decimals: "Friendly decimals",
  awkward_decimals: "Awkward decimals",
};

/** Human labels for Layer 0 variable lane ids. */
const VARIABLE_LANE_LABELS: Record<string, string> = {
  auto: "Auto (from difficulty + constraints)",
  none: "None (don't lock)",
  only_x: "Only x",
  xyz: "x, y, z",
  abctuvwxyz: "Common algebra letters",
  whole_alphabet: "Whole alphabet a–z",
  greek: "Greek letters",
};

export function topicSettingsFields(fields: SettingField[]): SettingField[] {
  return fields.filter((field) => !WORKSHEET_LEVEL_KEYS.has(field.key));
}

type TopicSettingsFieldsProps = {
  fields: SettingField[];
  values: Record<string, string | number | boolean>;
  onChange: (key: string, value: string | number | boolean) => void;
  /** Replace many settings at once (used when difficulty presets apply). */
  onValuesChange?: (values: Record<string, string | number | boolean>) => void;
  typeId?: string | null;
  settingProfile?: string | null;
};

function fieldValue(
  values: Record<string, string | number | boolean>,
  field: SettingField,
): string | number | boolean {
  const current = values[field.key];
  if (current !== undefined && current !== null) return current;
  return field.default;
}

function numberFieldValue(
  values: Record<string, string | number | boolean>,
  field: SettingField,
): number {
  const raw = fieldValue(values, field);
  const parsed = typeof raw === "number" ? raw : Number(raw);
  return Number.isFinite(parsed) ? parsed : Number(field.default);
}

function isFieldVisible(
  field: SettingField,
  values: Record<string, string | number | boolean>,
): boolean {
  if (!MC_DETAIL_KEYS.has(field.key)) return true;
  return Boolean(values.multiple_choice ?? false);
}

function optionLabel(field: SettingField, option: string): string {
  if (field.key === "cancel_factor_count") {
    return CANCEL_FACTOR_COUNT_LABELS[option] ?? option;
  }
  if (field.key === "number_profile") {
    return NUMBER_PROFILE_LABELS[option] ?? option.replaceAll("_", " ");
  }
  if (
    field.key === "variable_lane" ||
    field.key === "max_variable_lane" ||
    field.key === "lock_variable"
  ) {
    return VARIABLE_LANE_LABELS[option] ?? option.replaceAll("_", " ");
  }
  if (field.key === "answer_format" && option === "auto") return "Auto";
  if (option === "auto") return "Auto (up to 3)";
  return option;
}

function renderBoolField(
  field: SettingField,
  values: Record<string, string | number | boolean>,
  onChange: (key: string, value: string | number | boolean) => void,
) {
  return (
    <label className="field field-inline" key={field.key}>
      <input
        type="checkbox"
        checked={Boolean(fieldValue(values, field))}
        onChange={(event) => onChange(field.key, event.target.checked)}
      />
      <span>{field.label}</span>
    </label>
  );
}

function renderRangeField(
  field: SettingField,
  values: Record<string, string | number | boolean>,
  onChange: (key: string, value: string | number | boolean) => void,
) {
  const value = numberFieldValue(values, field);
  const min = field.min ?? 0;
  const max = field.max ?? 100;
  const suffix =
    field.key === "inflation_chance" || field.key === "multiple_choice_ratio" ? "%" : "";

  return (
    <label className="field field-range" key={field.key}>
      <span>
        {field.label}: {value}
        {suffix}
      </span>
      <input
        type="range"
        value={value}
        min={min}
        max={max}
        step={1}
        onChange={(event) => onChange(field.key, Number(event.target.value))}
      />
    </label>
  );
}

/** Primary difficulty control: free number entry + optional soft-range slider. */
function renderDifficultyField(
  field: SettingField,
  values: Record<string, string | number | boolean>,
  onChange: (key: string, value: string | number | boolean) => void,
) {
  const value = numberFieldValue(values, field);
  const min = field.min ?? 0;
  const softMax = field.max ?? SOFT_DIFFICULTY_SLIDER_MAX;
  const sliderValue = Math.min(Math.max(value, min), softMax);

  return (
    <div className="field field-difficulty" key={field.key}>
      <label className="field-difficulty-label">
        <span>{field.label}</span>
        <input
          type="number"
          value={Number.isFinite(value) ? value : min}
          min={min}
          step={1}
          onChange={(event) => {
            const next = Number(event.target.value);
            if (!Number.isFinite(next)) {
              onChange(field.key, min);
              return;
            }
            onChange(field.key, Math.max(min, next));
          }}
        />
      </label>
      <input
        type="range"
        aria-label={`${field.label} (quick adjust)`}
        value={sliderValue}
        min={min}
        max={softMax}
        step={1}
        onChange={(event) => onChange(field.key, Number(event.target.value))}
      />
      {value > softMax ? (
        <p className="settings-hint">
          Above the typical 0–{softMax} range; generation will use {value} as entered.
        </p>
      ) : (
        <p className="settings-hint">
          Type any non-negative number, or use the slider for the common 0–{softMax} range.
        </p>
      )}
    </div>
  );
}

/** Empty string / blank = no prereq cap (unlimited). Explicit ≥0 numbers apply a cap. */
function isPrereqCapUncapped(raw: string | number | boolean | undefined | null): boolean {
  if (raw === undefined || raw === null || raw === "") return true;
  if (typeof raw === "boolean") return true;
  if (typeof raw === "string") {
    const text = raw.trim().toLowerCase();
    return text === "" || text === "none" || text === "uncapped" || text === "unlimited";
  }
  return !Number.isFinite(Number(raw));
}

function optionalPrereqCapValue(
  values: Record<string, string | number | boolean>,
  field: SettingField,
): number | null {
  const raw = values[field.key];
  if (raw === undefined || raw === null) {
    return isPrereqCapUncapped(field.default) ? null : Number(field.default);
  }
  if (isPrereqCapUncapped(raw)) return null;
  const parsed = typeof raw === "number" ? raw : Number(raw);
  if (!Number.isFinite(parsed)) return null;
  return Math.max(field.min ?? 0, parsed);
}

/** Prerequisite cap: default uncapped; soft slider + typed value like main difficulty. */
function renderPrereqCapField(
  field: SettingField,
  values: Record<string, string | number | boolean>,
  onChange: (key: string, value: string | number | boolean) => void,
) {
  const min = field.min ?? 0;
  const softMax = field.max ?? SOFT_DIFFICULTY_SLIDER_MAX;
  const cap = optionalPrereqCapValue(values, field);
  const uncapped = cap === null;
  const sliderValue = uncapped ? softMax : Math.min(Math.max(cap, min), softMax);

  return (
    <div className="field field-difficulty" key={field.key}>
      <label className="field-difficulty-label">
        <span>{field.label}</span>
        <input
          type="number"
          value={uncapped ? "" : cap}
          min={min}
          step={1}
          placeholder="No cap"
          onChange={(event) => {
            const text = event.target.value;
            if (text.trim() === "") {
              onChange(field.key, "");
              return;
            }
            const next = Number(text);
            if (!Number.isFinite(next)) {
              onChange(field.key, "");
              return;
            }
            onChange(field.key, Math.max(min, next));
          }}
        />
      </label>
      <input
        type="range"
        aria-label={`${field.label} (quick adjust)`}
        value={sliderValue}
        min={min}
        max={softMax}
        step={1}
        onChange={(event) => onChange(field.key, Number(event.target.value))}
      />
      {uncapped ? (
        <p className="settings-hint">
          No cap (default). Type a non-negative number or use the slider to set a limit.
        </p>
      ) : cap > softMax ? (
        <p className="settings-hint">
          Cap is above the typical 0–{softMax} range; generation will use {cap}.{" "}
          <button type="button" className="link-button" onClick={() => onChange(field.key, "")}>
            Clear cap
          </button>
        </p>
      ) : (
        <p className="settings-hint">
          Cap set to {cap}.{" "}
          <button type="button" className="link-button" onClick={() => onChange(field.key, "")}>
            Clear cap
          </button>
        </p>
      )}
    </div>
  );
}

function renderCompactField(
  field: SettingField,
  values: Record<string, string | number | boolean>,
  onChange: (key: string, value: string | number | boolean) => void,
) {
  return (
    <label className="field field-compact" key={field.key}>
      <span>{field.label}</span>
      {field.type === "select" ? (
        <select
          value={String(fieldValue(values, field))}
          onChange={(event) => onChange(field.key, event.target.value)}
        >
          {(field.options ?? []).map((option) => (
            <option key={option} value={option}>
              {optionLabel(field, option)}
            </option>
          ))}
        </select>
      ) : (
        <input
          type="number"
          value={numberFieldValue(values, field)}
          min={field.min}
          max={field.max}
          onChange={(event) => onChange(field.key, Number(event.target.value))}
        />
      )}
    </label>
  );
}

function partitionFields(fields: SettingField[]) {
  const difficulty: SettingField[] = [];
  const prereqCaps: SettingField[] = [];
  const layer0: SettingField[] = [];
  const layer0Advanced: SettingField[] = [];
  const specific: SettingField[] = [];
  const common: SettingField[] = [];
  const hasContinuousDifficulty = fields.some((field) => field.key === "difficulty");

  for (const field of fields) {
    // On the primitive-difficulty experiment, hide legacy EMH when a continuous slider exists.
    if (hasContinuousDifficulty && field.key === "difficulty_tier") {
      continue;
    }
    if (field.group === "difficulty" || field.key === "difficulty_tier" || field.key === "difficulty") {
      difficulty.push(field);
      continue;
    }
    if (field.group === "prereq_caps" || field.key.startsWith("prereq_cap_")) {
      prereqCaps.push(field);
      continue;
    }
    if (field.group === "layer0_advanced") {
      layer0Advanced.push(field);
      continue;
    }
    if (field.group === "layer0") {
      layer0.push(field);
      continue;
    }
    if (COMMON_GROUPS.has(field.group ?? "") || field.key === "include_answer_key") {
      common.push(field);
      continue;
    }
    specific.push(field);
  }

  return {
    difficulty,
    prereqCaps,
    layer0,
    layer0Advanced,
    specific,
    common,
    hasContinuousDifficulty,
  };
}

function renderFieldBlock(
  fields: SettingField[],
  values: Record<string, string | number | boolean>,
  onChange: (key: string, value: string | number | boolean) => void,
  sectionKey: string,
) {
  const visible = fields.filter((field) => isFieldVisible(field, values));
  if (visible.length === 0) return null;

  const difficultyFields = visible.filter((field) => field.key === "difficulty");
  const compactFields = visible.filter(
    (field) =>
      field.key !== "difficulty" && (field.type === "int" || field.type === "select"),
  );
  const rangeFields = visible.filter(
    (field) => field.key !== "difficulty" && field.type === "range",
  );
  const boolFields = visible.filter((field) => field.type === "bool");

  return (
    <div className="settings-fields-section" key={sectionKey}>
      {difficultyFields.map((field) => renderDifficultyField(field, values, onChange))}
      {compactFields.length > 0 && (
        <div className="settings-compact-grid">
          {compactFields.map((field) => renderCompactField(field, values, onChange))}
        </div>
      )}
      {boolFields.length > 0 && (
        <div className="field-bool-row">
          {boolFields.map((field) => renderBoolField(field, values, onChange))}
        </div>
      )}
      {rangeFields.map((field) => renderRangeField(field, values, onChange))}
    </div>
  );
}

export function TopicSettingsFields({
  fields,
  values,
  onChange,
  onValuesChange,
  typeId,
  settingProfile,
}: TopicSettingsFieldsProps) {
  const handleFieldChange = (key: string, value: string | number | boolean) => {
    if (key === "difficulty_tier" && onValuesChange) {
      onValuesChange(
        applyDifficultyPresetToSettings(values, value, {
          typeId,
          settingProfile,
          allowedKeys: fields.map((field) => field.key),
        }),
      );
      return;
    }
    onChange(key, value);
  };

  const {
    difficulty,
    prereqCaps,
    layer0,
    layer0Advanced,
    specific,
    common,
    hasContinuousDifficulty,
  } = partitionFields(fields);

  return (
    <>
      {renderFieldBlock(difficulty, values, handleFieldChange, "difficulty")}
      {prereqCaps.length > 0 && (
        <div className="settings-fields-section" key="prereq-caps">
          <div className="settings-section-label">Prerequisite difficulty caps</div>
          <p className="settings-hint">
            Defaults are uncapped. Set a cap only when you want to limit that
            shared primitive wherever it appears. Number form and variable pool
            still follow overall difficulty plus the constraints below.
          </p>
          {prereqCaps.map((field) => renderPrereqCapField(field, values, handleFieldChange))}
        </div>
      )}
      {layer0.length > 0 && (
        <details className="settings-fields-section" key="layer0" open>
          <summary>Number &amp; variable constraints</summary>
          <p className="settings-hint">
            Difficulty picks number and variable lanes; constraints filter which
            pools are allowed (e.g. integers only, only x, no Greek). Lock a
            letter to force that variable for the whole item.
          </p>
          {renderFieldBlock(layer0, values, handleFieldChange, "layer0-inner")}
          {layer0Advanced.length > 0 && (
            <details className="settings-fields-section" key="layer0-advanced">
              <summary>Advanced: force number / variable lane</summary>
              <p className="settings-hint">
                Leave on Auto unless debugging. Forcing a lane overrides
                difficulty-based selection.
              </p>
              {renderFieldBlock(
                layer0Advanced,
                values,
                handleFieldChange,
                "layer0-advanced-inner",
              )}
            </details>
          )}
        </details>
      )}
      {/* Black-box: hide legacy specific knobs when continuous difficulty is active */}
      {!hasContinuousDifficulty &&
        renderFieldBlock(specific, values, handleFieldChange, "specific")}
      {renderFieldBlock(common, values, handleFieldChange, "common")}
    </>
  );
}
