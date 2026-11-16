import type { TopicSection, WorksheetDraft } from "@/lib/types";

export const WORKSHEET_PRESET_STORAGE_KEY = "elementary_math.worksheet_presets";

export type SavedWorksheetPreset = {
  id: string;
  title: string;
  savedAt: string;
  worksheet: WorksheetDraft;
  sections: TopicSection[];
  topics: string[];
};

export function topicsOnWorksheet(
  worksheet: WorksheetDraft | null,
  sections: readonly TopicSection[] = [],
): string[] {
  const topics: string[] = [];
  const seen = new Set<string>();
  const add = (topic: string | null | undefined) => {
    const value = topic?.trim() ?? "";
    if (!value || seen.has(value)) return;
    seen.add(value);
    topics.push(value);
  };
  for (const section of sections) add(section.type_id);
  for (const question of worksheet?.questions ?? []) add(question.topic);
  return topics;
}

export function presetsIncludingTopic(
  presets: readonly SavedWorksheetPreset[],
  typeId: string,
): SavedWorksheetPreset[] {
  const topic = typeId.trim();
  if (!topic) return [];
  return presets.filter((preset) => preset.topics.includes(topic));
}

export function upsertPreset(
  presets: readonly SavedWorksheetPreset[],
  preset: SavedWorksheetPreset,
): SavedWorksheetPreset[] {
  const index = presets.findIndex((entry) => entry.id === preset.id);
  if (index === -1) return [preset, ...presets];
  return presets.map((entry) => (entry.id === preset.id ? preset : entry));
}

export function removePreset(
  presets: readonly SavedWorksheetPreset[],
  id: string,
): SavedWorksheetPreset[] {
  return presets.filter((entry) => entry.id !== id);
}

export function readSavedPresets(storage: Storage | null): SavedWorksheetPreset[] {
  if (!storage) return [];
  try {
    const raw = storage.getItem(WORKSHEET_PRESET_STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw) as unknown;
    if (!Array.isArray(parsed)) return [];
    return parsed.filter(isSavedPreset);
  } catch {
    return [];
  }
}

export function writeSavedPresets(
  storage: Storage | null,
  presets: readonly SavedWorksheetPreset[],
): void {
  if (!storage) return;
  storage.setItem(WORKSHEET_PRESET_STORAGE_KEY, JSON.stringify(presets));
}

export function newPresetId(): string {
  const bytes = new Uint8Array(8);
  crypto.getRandomValues(bytes);
  return `saved_${Array.from(bytes, (byte) => byte.toString(16).padStart(2, "0")).join("")}`;
}

function isSavedPreset(value: unknown): value is SavedWorksheetPreset {
  if (!value || typeof value !== "object") return false;
  const preset = value as Partial<SavedWorksheetPreset>;
  return (
    typeof preset.id === "string" &&
    typeof preset.title === "string" &&
    typeof preset.savedAt === "string" &&
    Array.isArray(preset.topics) &&
    Array.isArray(preset.sections) &&
    Boolean(preset.worksheet) &&
    typeof preset.worksheet === "object" &&
    Array.isArray((preset.worksheet as WorksheetDraft).questions)
  );
}
