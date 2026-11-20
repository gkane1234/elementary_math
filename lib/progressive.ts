/** Client helpers for progressive practice mode (mirrors question_engine.progressive rules). */

import type { QuestionTypeInfo, TopicSection } from "@/lib/types";

export type ProgressivePairing = "lesson" | "drill" | "spiral";
export type ProgressiveScope = "topic" | "unit" | "adjacent";
export type ProgressiveStyle = "ramp" | "straight";

export type ProgressiveTemplateFields = {
  pairing?: ProgressivePairing;
  scope?: ProgressiveScope;
  topics?: string[];
  style?: ProgressiveStyle;
  ramp_each_topic?: boolean;
};

const PHASE_LABELS: Record<string, string> = {
  warmup: "Warm-up",
  focus: "Topics",
  drill: "Procedure drill",
  stretch: "Follow-on",
};

/** Collapse a slot phase list to "Warm-up → Topics → Procedure drill → Follow-on". */
export function summarizePhaseOrder(phases: readonly string[]): string {
  const runs: string[] = [];
  for (const phase of phases) {
    const label = PHASE_LABELS[phase] ?? phase;
    if (runs.length === 0 || runs[runs.length - 1] !== label) {
      runs.push(label);
    }
  }
  return runs.join(" → ");
}

/** Fields the progressive API echoes for Grade 6 and Geometry templates. */
export function progressiveTemplatePayload(
  fields: ProgressiveTemplateFields,
): ProgressiveTemplateFields {
  const payload: ProgressiveTemplateFields = {};
  if (fields.pairing) payload.pairing = fields.pairing;
  if (fields.scope) payload.scope = fields.scope;
  if (fields.style) payload.style = fields.style;
  if (fields.topics) payload.topics = fields.topics;
  if (fields.ramp_each_topic != null) payload.ramp_each_topic = fields.ramp_each_topic;
  return payload;
}

export function typeHasContinuousDifficulty(type: QuestionTypeInfo): boolean {
  return type.settings.some(
    (field) =>
      field.key === "difficulty" &&
      (field.type === "int" || field.type === "range"),
  );
}

export function continuousReadyTypes(types: QuestionTypeInfo[]): QuestionTypeInfo[] {
  return types.filter(
    (type) =>
      !type.not_ready &&
      !type.requires_diagram &&
      !type.incorrect_implementation &&
      typeHasContinuousDifficulty(type),
  );
}

export function createProgressiveSectionId(index: number): string {
  return `progressive-${Date.now()}-${index}-${Math.random().toString(36).slice(2, 6)}`;
}

/** Map API progressive sections into TopicSection rows for the sidebar. */
export function progressiveApiSectionsToTopicSections(
  apiSections: Array<{ type_id: string; count: number; settings: Record<string, unknown> }>,
): TopicSection[] {
  return apiSections.map((section, index) => ({
    id: createProgressiveSectionId(index),
    type_id: section.type_id,
    count: section.count,
    settings: Object.fromEntries(
      Object.entries(section.settings).filter(
        ([, value]) =>
          typeof value === "string" ||
          typeof value === "number" ||
          typeof value === "boolean",
      ),
    ) as Record<string, string | number | boolean>,
  }));
}
