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

export type ProgressiveGenerateOptions = {
  seeds: string[];
  count?: number;
  d_min?: number;
  d_max?: number;
  /** Worksheet-level difficulty (level-0…level-4, legacy EMH / d-range aliases, or 0–24); sets d_min/d_max when provided. */
  worksheet_difficulty?: string | number;
  include_related?: boolean;
  max_topics?: number;
  title?: string;
  plan_only?: boolean;
  /** Optional RNG seed applied to each question's settings. */
  rng_seed?: number;
};

export type ProgressivePlan = {
  seeds: string[];
  count: number;
  d_min: number;
  d_max: number;
  include_related: boolean;
  max_topics: number;
  topics: string[];
  difficulties: number[];
};

export type ProgressiveGenerateResult = QuestionSet & {
  progressive?: ProgressivePlan;
  sections?: GenerateSection[];
};

/** Progressive practice: coherent related topics + global difficulty ramp. */
export async function generateProgressive(
  options: ProgressiveGenerateOptions,
): Promise<ProgressiveGenerateResult> {
  const response = await fetch("/api/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      title: options.title ?? "Progressive Practice",
      worksheet_settings: {},
      progressive: {
        seeds: options.seeds,
        count: options.count ?? 10,
        d_min: options.d_min ?? 0,
        d_max: options.d_max ?? 18,
        ...(options.worksheet_difficulty != null
          ? { worksheet_difficulty: options.worksheet_difficulty }
          : {}),
        include_related: options.include_related ?? true,
        max_topics: options.max_topics ?? 4,
        plan_only: options.plan_only ?? false,
        ...(options.rng_seed != null
          ? { base_settings: { seed: options.rng_seed } }
          : {}),
      },
    }),
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
