import type { SettingField } from "@/lib/types";
import { applyDifficultyPresetToSettings } from "@/lib/difficulty-presets";

const WORKSHEET_LEVEL_KEYS = new Set(["count", "max_columns"]);

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
  const specific: SettingField[] = [];
  const common: SettingField[] = [];

  for (const field of fields) {
    if (field.group === "difficulty" || field.key === "difficulty_tier") {
      difficulty.push(field);
      continue;
    }
    if (COMMON_GROUPS.has(field.group ?? "") || field.key === "include_answer_key") {
      common.push(field);
      continue;
    }
    specific.push(field);
  }

  return { difficulty, specific, common };
}

function renderFieldBlock(
  fields: SettingField[],
  values: Record<string, string | number | boolean>,
  onChange: (key: string, value: string | number | boolean) => void,
  sectionKey: string,
) {
  const visible = fields.filter((field) => isFieldVisible(field, values));
  if (visible.length === 0) return null;

  const compactFields = visible.filter(
    (field) => field.type === "int" || field.type === "select",
  );
  const rangeFields = visible.filter((field) => field.type === "range");
  const boolFields = visible.filter((field) => field.type === "bool");

  return (
    <div className="settings-fields-section" key={sectionKey}>
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

  const { difficulty, specific, common } = partitionFields(fields);

  return (
    <>
      {renderFieldBlock(difficulty, values, handleFieldChange, "difficulty")}
      {renderFieldBlock(specific, values, handleFieldChange, "specific")}
      {renderFieldBlock(common, values, handleFieldChange, "common")}
    </>
  );
}
