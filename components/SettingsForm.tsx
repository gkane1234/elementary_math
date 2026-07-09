import type { SettingField } from "@/lib/types";

type SettingsFormProps = {
  fields: SettingField[];
  values: Record<string, string | number | boolean>;
  title: string;
  onTitleChange: (title: string) => void;
  onChange: (key: string, value: string | number | boolean) => void;
  onSubmit: () => void;
  loading: boolean;
};

export function SettingsForm({
  fields,
  values,
  title,
  onTitleChange,
  onChange,
  onSubmit,
  loading,
}: SettingsFormProps) {
  return (
    <section className="panel">
      <h2>Worksheet settings</h2>

      <label className="field">
        <span>Worksheet title</span>
        <input
          type="text"
          value={title}
          onChange={(event) => onTitleChange(event.target.value)}
        />
      </label>

      {fields.map((field) => (
        <label className="field" key={field.key}>
          <span>{field.label}</span>
          {field.type === "bool" ? (
            <input
              type="checkbox"
              checked={Boolean(values[field.key])}
              onChange={(event) => onChange(field.key, event.target.checked)}
            />
          ) : field.type === "select" ? (
            <select
              value={String(values[field.key])}
              onChange={(event) => onChange(field.key, event.target.value)}
            >
              {(field.options ?? []).map((option) => (
                <option key={option} value={option}>
                  {option === "auto" ? "Auto (up to 3)" : option}
                </option>
              ))}
            </select>
          ) : (
            <input
              type="number"
              value={Number(values[field.key])}
              min={field.min}
              max={field.max}
              onChange={(event) => onChange(field.key, Number(event.target.value))}
            />
          )}
        </label>
      ))}

      <button className="primary" onClick={onSubmit} disabled={loading}>
        {loading ? "Generating..." : "Generate worksheet"}
      </button>
    </section>
  );
}
