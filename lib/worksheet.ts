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

export function allSameTopic(questions: WorksheetQuestion[]): boolean {
  if (questions.length === 0) return true;
  return questions.every((question) => question.topic === questions[0].topic);
}

export function sharedHeaderInstruction(questions: WorksheetQuestion[]): string | null {
  if (!allSameTopic(questions)) return null;
  return questions[0]?.instruction_latex ?? null;
}

export function shouldShowInstruction(
  question: WorksheetQuestion,
  previous: WorksheetQuestion | null,
  headerInstruction: string | null,
): boolean {
  if (!question.instruction_latex) return false;
  if (headerInstruction && question.instruction_latex === headerInstruction) return false;
  if (!previous) return true;
  return previous.topic !== question.topic;
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
