export type MultipleChoiceOption = {
  id: string;
  latex: string;
  correct: boolean;
};

const LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function normalizeChoice(raw: unknown, index: number): MultipleChoiceOption | null {
  if (typeof raw === "string") {
    return {
      id: LETTERS[index]?.toLowerCase() ?? String(index),
      latex: raw,
      correct: false,
    };
  }
  if (!isRecord(raw) || typeof raw.latex !== "string") return null;
  const id =
    typeof raw.id === "string" && raw.id.trim()
      ? raw.id.trim()
      : (LETTERS[index]?.toLowerCase() ?? String(index));
  return {
    id,
    latex: raw.latex,
    correct: Boolean(raw.correct),
  };
}

/** Parse MC choices from question metadata (new object shape or legacy string list). */
export function getMultipleChoiceChoices(
  metadata?: Record<string, unknown> | null,
): MultipleChoiceOption[] | null {
  if (!metadata) return null;
  const raw = metadata.choices;
  if (!Array.isArray(raw) || raw.length === 0) return null;

  const choices = raw
    .map((entry, index) => normalizeChoice(entry, index))
    .filter((entry): entry is MultipleChoiceOption => entry !== null);

  if (choices.length === 0) return null;

  // Legacy: choices were plain strings with correct_index.
  if (choices.every((choice) => !choice.correct) && typeof metadata.correct_index === "number") {
    const index = metadata.correct_index;
    if (index >= 0 && index < choices.length) {
      choices[index] = { ...choices[index], correct: true };
    }
  }

  if (metadata.answer_mode === "multiple_choice" || choices.some((choice) => choice.correct)) {
    return choices;
  }

  // If enrichment only attached choices without flags, still treat as MC.
  return choices;
}

export function choiceLetter(choice: MultipleChoiceOption, index: number): string {
  const fromId = choice.id.trim().toUpperCase();
  if (/^[A-Z]$/.test(fromId)) return fromId;
  return LETTERS[index] ?? String(index + 1);
}

export function correctChoiceLabel(choices: MultipleChoiceOption[]): string | null {
  const index = choices.findIndex((choice) => choice.correct);
  if (index < 0) return null;
  return choiceLetter(choices[index], index);
}
