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

function sectionMatchesQuestion(
  question: WorksheetQuestion,
  section: TopicSection,
): boolean {
  return (
    question.topic === section.type_id &&
    settingsEqual(question.generation_settings, section.settings)
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

async function syncSectionQuestions(
  section: TopicSection,
  existing: WorksheetQuestion[],
  title: string,
): Promise<WorksheetQuestion[]> {
  const matching = existing.filter((question) => sectionMatchesQuestion(question, section));

  if (matching.length === section.count && matching.length > 0) {
    return matching;
  }

  if (
    matching.length > 0 &&
    matching.length < section.count &&
    matching.every((question) => sectionMatchesQuestion(question, section))
  ) {
    const extra = await generateSectionQuestions(
      section,
      title,
      section.count - matching.length,
    );
    return [...matching, ...extra];
  }

  if (matching.length > section.count) {
    return matching.slice(0, section.count);
  }

  return generateSectionQuestions(section, title, section.count);
}

export async function syncWorksheetFromSections(
  current: WorksheetDraft | null,
  sections: TopicSection[],
  title: string,
  maxColumns: string,
): Promise<WorksheetDraft> {
  const existingBySection = groupQuestionsBySection(current?.questions ?? []);
  const questions: WorksheetQuestion[] = [];

  for (const section of sections) {
    const existing = existingBySection.get(section.id) ?? [];
    const sectionQuestions = await syncSectionQuestions(section, existing, title);
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
