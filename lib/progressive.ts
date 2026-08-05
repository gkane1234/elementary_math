/** Client helpers for progressive practice mode (mirrors question_engine.progressive rules). */

import type { QuestionTypeInfo, TopicSection } from "@/lib/types";

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
