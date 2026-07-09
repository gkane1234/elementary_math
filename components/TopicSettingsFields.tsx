import type { SettingField } from "@/lib/types";

const WORKSHEET_LEVEL_KEYS = new Set(["count", "max_columns"]);

const GROUP_LABELS: Record<string, string> = {
  factoring: "Factoring",
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
  const suffix = field.key === "inflation_chance" ? "%" : "";

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

export function TopicSettingsFields({ fields, values, onChange }: TopicSettingsFieldsProps) {
  const boolFields = fields.filter((field) => field.type === "bool" && !field.group);
  const otherFields = fields.filter((field) => field.type !== "bool" && !field.group);
  const { grouped } = groupFields(fields.filter((field) => field.group));

  return (
    <>
      {boolFields.length > 0 && (
        <div className="field-bool-row">
          {boolFields.map((field) => renderBoolField(field, values, onChange))}
        </div>
      )}

      {otherFields.map((field) => renderOtherField(field, values, onChange))}

      {Array.from(grouped.entries()).map(([groupKey, groupFieldsList]) => {
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
      })}
    </>
  );
}
