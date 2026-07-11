import type { Question, QuestionSet, WorksheetDraft, WorksheetQuestion } from "./types";

export const DEFAULT_SPACING = 1;
export const MIN_SPACING = 0.25;
export const MAX_SPACING = 4;

export function clampSpacing(value: number): number {
  return Math.min(MAX_SPACING, Math.max(MIN_SPACING, value));
}

export function toWorksheetQuestion(question: Question): WorksheetQuestion {
  const metadata = question.metadata ?? {};
  return {
    ...question,
    spacing: DEFAULT_SPACING,
    generation_settings: (metadata.generation_settings as Record<string, unknown>) ?? {},
    instruction_latex: (metadata.instruction_latex as string | null | undefined) ?? null,
  };
}

export function questionSetToDraft(result: QuestionSet): WorksheetDraft {
  return {
    title: result.title,
    columns: result.columns ?? 1,
    questions: result.questions.map(toWorksheetQuestion),
  };
}

export function allSameTopic(questions: Array<{ topic: string }>): boolean {
  if (questions.length === 0) return true;
  return questions.every((question) => question.topic === questions[0].topic);
}

export function allSameInstruction(questions: Array<{ instruction_latex?: string | null }>): boolean {
  if (questions.length === 0) return true;
  const first = questions[0]?.instruction_latex ?? null;
  return questions.every((question) => (question.instruction_latex ?? null) === first);
}

export function sharedHeaderInstruction(
  questions: Array<{ topic: string; instruction_latex?: string | null }>,
): string | null {
  if (questions.length === 0) return null;
  if (!allSameTopic(questions) || !allSameInstruction(questions)) return null;
  return questions[0]?.instruction_latex ?? null;
}

export type InstructionGroup<T extends { instruction_latex?: string | null }> = {
  instruction: string | null;
  questions: T[];
  startIndex: number;
};

/** Group consecutive questions that share the same instruction_latex. */
export function groupQuestionsByInstruction<T extends { instruction_latex?: string | null }>(
  questions: T[],
): InstructionGroup<T>[] {
  if (questions.length === 0) return [];

  const groups: InstructionGroup<T>[] = [];
  let current: InstructionGroup<T> | null = null;

  questions.forEach((question, index) => {
    const instruction = question.instruction_latex ?? null;
    if (!current || current.instruction !== instruction) {
      current = { instruction, questions: [question], startIndex: index };
      groups.push(current);
      return;
    }
    current.questions.push(question);
  });

  return groups;
}

/**
 * Whether to show a full-width section header for this instruction group.
 * Skipped when the worksheet already shows the same instruction in the page header.
 */
export function shouldShowSectionHeader(
  instruction: string | null,
  headerInstruction: string | null,
): boolean {
  if (!instruction) return false;
  if (headerInstruction && instruction === headerInstruction) return false;
  return true;
}

/**
 * Per-question instruction inside a cell — only when not covered by a worksheet
 * or section header (legacy fallback; grouping UI should prefer section headers).
 */
export function shouldShowInstruction(
  question: WorksheetQuestion,
  previous: WorksheetQuestion | null,
  headerInstruction: string | null,
): boolean {
  if (!question.instruction_latex) return false;
  if (headerInstruction && question.instruction_latex === headerInstruction) return false;
  if (!previous) return true;
  return (previous.instruction_latex ?? null) !== question.instruction_latex;
}

export function moveQuestion(
  questions: WorksheetQuestion[],
  fromIndex: number,
  toIndex: number,
): WorksheetQuestion[] {
  if (fromIndex === toIndex) return questions;
  const next = [...questions];
  const [moved] = next.splice(fromIndex, 1);
  next.splice(toIndex, 0, moved);
  return next;
}

export function updateQuestion(
  questions: WorksheetQuestion[],
  questionId: string,
  updater: (question: WorksheetQuestion) => WorksheetQuestion,
): WorksheetQuestion[] {
  return questions.map((question) =>
    question.id === questionId ? updater(question) : question,
  );
}

export function removeQuestion(
  questions: WorksheetQuestion[],
  questionId: string,
): WorksheetQuestion[] {
  return questions.filter((question) => question.id !== questionId);
}
