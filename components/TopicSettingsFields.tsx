import type { SettingField } from "@/lib/types";
import { applyDifficultyPresetToSettings } from "@/lib/difficulty-presets";

const WORKSHEET_LEVEL_KEYS = new Set(["count", "max_columns"]);

/** Groups rendered before other domain groups (after ungrouped fields). */
const PINNED_GROUP_ORDER = ["difficulty"];

const GROUP_LABELS: Record<string, string> = {
  polynomial: "Polynomial",
  equation: "Equation",
  inequality: "Inequality",
  number: "Numbers",
  linear: "Linear",
  radical: "Radicals",
  rational: "Rational expressions",
  division: "Division notation",
  factoring: "Factoring",
  exponential: "Exponential",
  trigonometry: "Trigonometry",
  logarithm: "Logarithms",
  sequence: "Sequences",
  limits: "Limits",
  derivatives: "Derivatives",
  integrals: "Integrals",
  expression: "Expressions",
  systems: "Systems",
  variation: "Variation",
  relations: "Relations",
  word_problem: "Word problem",
  geometry: "Geometry",
  difficulty: "Difficulty",
  answer: "Answer",
  signs: "Signs",
  terms: "Terms",
  presentation: "Presentation",
};

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

function renderOtherField(
  field: SettingField,
  values: Record<string, string | number | boolean>,
  onChange: (key: string, value: string | number | boolean) => void,
) {
  if (field.type === "range") {
    return renderRangeField(field, values, onChange);
  }

  return (
    <label className="field" key={field.key}>
      <span>{field.label}</span>
      {field.type === "select" ? (
        <select
          value={String(fieldValue(values, field))}
          onChange={(event) => onChange(field.key, event.target.value)}
        >
          {(field.options ?? []).map((option) => (
            <option key={option} value={option}>
              {field.key === "cancel_factor_count"
                ? (CANCEL_FACTOR_COUNT_LABELS[option] ?? option)
                : field.key === "answer_format" && option === "auto"
                  ? "Auto"
                  : field.key === "answer_format" && option === "multiple_choice"
                    ? "Multiple choice"
                    : option === "auto"
                      ? "Auto (up to 3)"
                      : option}
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

function groupFields(fields: SettingField[]) {
  const grouped = new Map<string, SettingField[]>();
  const ungrouped: SettingField[] = [];

  for (const field of fields) {
    if (!field.group) {
      ungrouped.push(field);
      continue;
    }
    const bucket = grouped.get(field.group) ?? [];
    bucket.push(field);
    grouped.set(field.group, bucket);
  }

  return { grouped, ungrouped };
}

function orderedGroupEntries(grouped: Map<string, SettingField[]>) {
  const remaining = new Map(grouped);
  const ordered: Array<[string, SettingField[]]> = [];

  for (const key of PINNED_GROUP_ORDER) {
    const fields = remaining.get(key);
    if (!fields) continue;
    ordered.push([key, fields]);
    remaining.delete(key);
  }

  for (const entry of remaining.entries()) {
    ordered.push(entry);
  }

  return ordered;
}

function renderGroupSection(
  groupKey: string,
  groupFieldsList: SettingField[],
  values: Record<string, string | number | boolean>,
  onChange: (key: string, value: string | number | boolean) => void,
) {
  const boolGroupFields = groupFieldsList.filter((field) => field.type === "bool");
  const otherGroupFields = groupFieldsList.filter((field) => field.type !== "bool");

  return (
    <section className="settings-group" key={groupKey}>
      <h3 className="settings-group-title">{GROUP_LABELS[groupKey] ?? groupKey}</h3>
      {otherGroupFields.map((field) => renderOtherField(field, values, onChange))}
      {boolGroupFields.length > 0 && (
        <div className="field-bool-row settings-group-bools">
          {boolGroupFields.map((field) => renderBoolField(field, values, onChange))}
        </div>
      )}
    </section>
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

  const difficultyFields = fields.filter((field) => field.group === "difficulty");
  const remainingFields = fields.filter((field) => field.group !== "difficulty");

  const boolFields = remainingFields.filter((field) => field.type === "bool" && !field.group);
  const otherFields = remainingFields.filter((field) => field.type !== "bool" && !field.group);
  const { grouped } = groupFields(remainingFields.filter((field) => field.group));

  return (
    <>
      {difficultyFields.length > 0 &&
        renderGroupSection("difficulty", difficultyFields, values, handleFieldChange)}

      {boolFields.length > 0 && (
        <div className="field-bool-row">
          {boolFields.map((field) => renderBoolField(field, values, handleFieldChange))}
        </div>
      )}

      {otherFields.map((field) => renderOtherField(field, values, handleFieldChange))}

      {orderedGroupEntries(grouped).map(([groupKey, groupFieldsList]) =>
        renderGroupSection(groupKey, groupFieldsList, values, handleFieldChange),
      )}
    </>
  );
}
