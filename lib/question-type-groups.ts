import { formatTopicLabel } from "./topic-labels";
import type { QuestionTypeInfo } from "./types";

export type QuestionTypeGroup = {
  label: string;
  types: QuestionTypeInfo[];
};

function groupLabel(type: QuestionTypeInfo): string {
  if (type.subcategory) {
    return `${type.category} — ${type.subcategory}`;
  }
  return type.category;
}

export function groupQuestionTypes(types: QuestionTypeInfo[]): QuestionTypeGroup[] {
  const groups = new Map<string, QuestionTypeInfo[]>();

  for (const type of types) {
    const label = groupLabel(type);
    const existing = groups.get(label) ?? [];
    existing.push(type);
    groups.set(label, existing);
  }

  return Array.from(groups.entries()).map(([label, groupedTypes]) => ({
    label,
    types: groupedTypes,
  }));
}

export function formatQuestionTypeLabel(type: QuestionTypeInfo): string {
  return formatTopicLabel(type.id, type.name, { category: type.category });
}
