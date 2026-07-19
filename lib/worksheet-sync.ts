import { resolveColumnCount } from "./columns";
import { generateFromSections } from "./api";
import type { TopicSection, WorksheetDraft, WorksheetQuestion } from "./types";
import { toWorksheetQuestion } from "./worksheet";

export function sectionContentKey(sections: TopicSection[]): string {
  return JSON.stringify(
    Object.fromEntries(
      sections.map((section) => [
        section.id,
        {
          type_id: section.type_id,
          count: section.count,
          settings: section.settings,
        },
      ]),
    ),
  );
}

export function sectionOrderKey(sections: TopicSection[]): string {
  return sections.map((section) => section.id).join("|");
}

export function settingsEqual(
  left: Record<string, unknown>,
  right: Record<string, string | number | boolean>,
): boolean {
  return JSON.stringify(left) === JSON.stringify(right);
}

function groupQuestionsBySection(
  questions: WorksheetQuestion[],
): Map<string, WorksheetQuestion[]> {
  const groups = new Map<string, WorksheetQuestion[]>();
  for (const question of questions) {
    const sectionId = question.sectionId ?? "";
    const bucket = groups.get(sectionId) ?? [];
    bucket.push(question);
    groups.set(sectionId, bucket);
  }
  return groups;
}

export function reorderQuestionsBySections(
  questions: WorksheetQuestion[],
  sections: TopicSection[],
): WorksheetQuestion[] {
  const groups = groupQuestionsBySection(questions);
  const ordered: WorksheetQuestion[] = [];

  for (const section of sections) {
    ordered.push(...(groups.get(section.id) ?? []));
  }

  for (const [sectionId, sectionQuestions] of groups) {
    if (!sectionId || sections.some((section) => section.id === sectionId)) continue;
    ordered.push(...sectionQuestions);
  }

  return ordered;
}

/** True when this section's type/settings changed vs the previous plan (count changes do not). */
export function sectionRequiresRegenerate(
  section: TopicSection,
  previous: TopicSection | undefined,
): boolean {
  if (!previous) return false;
  return (
    previous.type_id !== section.type_id ||
    !settingsEqual(previous.settings, section.settings)
  );
}

async function generateSectionQuestions(
  section: TopicSection,
  title: string,
  count: number,
): Promise<WorksheetQuestion[]> {
  const result = await generateFromSections({
    title,
    worksheet_settings: {},
    sections: [
      {
        type_id: section.type_id,
        count,
        settings: section.settings,
      },
    ],
  });

  return result.questions.map((question) => ({
    ...toWorksheetQuestion(question),
    sectionId: section.id,
  }));
}

export type SectionSyncPlan =
  | { kind: "keep"; questions: WorksheetQuestion[] }
  | { kind: "append"; questions: WorksheetQuestion[]; generateCount: number }
  | { kind: "trim"; questions: WorksheetQuestion[] }
  | { kind: "regenerate"; generateCount: number };

/**
 * Decide keep / append / trim / regenerate for one section without calling the API.
 * Existing questions are already scoped to this sectionId.
 */
export function planSectionSync(
  section: TopicSection,
  existing: WorksheetQuestion[],
  forceRegenerate = false,
): SectionSyncPlan {
  const kept = existing.filter((question) => question.topic === section.type_id);

  if (forceRegenerate || kept.length === 0) {
    return { kind: "regenerate", generateCount: section.count };
  }

  if (kept.length === section.count) {
    return { kind: "keep", questions: kept };
  }

  if (kept.length < section.count) {
    return {
      kind: "append",
      questions: kept,
      generateCount: section.count - kept.length,
    };
  }

  return { kind: "trim", questions: kept.slice(0, section.count) };
}

/**
 * Keep/append/trim questions for one section.
 * Existing questions are already scoped to this sectionId — do not regenerate
 * them for count-only changes. Full regen only when forceRegenerate is set
 * (type/settings change) or there is nothing to keep.
 */
export async function syncSectionQuestions(
  section: TopicSection,
  existing: WorksheetQuestion[],
  title: string,
  forceRegenerate = false,
): Promise<WorksheetQuestion[]> {
  const plan = planSectionSync(section, existing, forceRegenerate);

  if (plan.kind === "keep" || plan.kind === "trim") {
    return plan.questions;
  }

  if (plan.kind === "append") {
    const extra = await generateSectionQuestions(section, title, plan.generateCount);
    return [...plan.questions, ...extra];
  }

  return generateSectionQuestions(section, title, plan.generateCount);
}

export async function syncWorksheetFromSections(
  current: WorksheetDraft | null,
  sections: TopicSection[],
  title: string,
  maxColumns: string,
  previousSections: TopicSection[] = [],
): Promise<WorksheetDraft> {
  const existingBySection = groupQuestionsBySection(current?.questions ?? []);
  const previousById = new Map(previousSections.map((section) => [section.id, section]));
  const questions: WorksheetQuestion[] = [];

  for (const section of sections) {
    const existing = existingBySection.get(section.id) ?? [];
    const forceRegenerate = sectionRequiresRegenerate(section, previousById.get(section.id));
    const sectionQuestions = await syncSectionQuestions(
      section,
      existing,
      title,
      forceRegenerate,
    );
    questions.push(
      ...sectionQuestions.map((question) => ({
        ...question,
        sectionId: section.id,
      })),
    );
  }

  return {
    title,
    columns: resolveColumnCount(questions.length, maxColumns),
    questions,
  };
}

export function preserveQuestionEdits(
  generated: WorksheetQuestion[],
  previous: WorksheetQuestion[],
): WorksheetQuestion[] {
  const previousById = new Map(previous.map((question) => [question.id, question]));
  return generated.map((question) => {
    const prior = previousById.get(question.id);
    if (!prior) return question;
    return {
      ...question,
      spacing: prior.spacing,
    };
  });
}
