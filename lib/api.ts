import type { GenerateSection, Question, QuestionSet, QuestionTypeInfo } from "./types";

export async function fetchQuestionTypes(): Promise<QuestionTypeInfo[]> {
  const response = await fetch("/api/question-types", { cache: "no-store" });
  if (!response.ok) {
    throw new Error("Failed to load question types");
  }
  const data = await response.json();
  return data.types;
}

export async function generateWorksheet(payload: {
  type_id: string;
  settings: Record<string, unknown>;
  title?: string;
}): Promise<QuestionSet> {
  const response = await fetch("/api/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: "Generation failed" }));
    throw new Error(error.error || "Generation failed");
  }

  return response.json();
}

export async function generateFromSections(payload: {
  title: string;
  worksheet_settings: Record<string, unknown>;
  sections: GenerateSection[];
}): Promise<QuestionSet> {
  const response = await fetch("/api/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: "Generation failed" }));
    throw new Error(error.error || "Generation failed");
  }

  return response.json();
}

export async function regenerateQuestion(payload: {
  type_id: string;
  settings: Record<string, unknown>;
}): Promise<Question> {
  const result = await generateWorksheet({
    type_id: payload.type_id,
    settings: { ...payload.settings, count: 1 },
  });

  if (!result.questions.length) {
    throw new Error("No question was generated");
  }

  return result.questions[0];
}
