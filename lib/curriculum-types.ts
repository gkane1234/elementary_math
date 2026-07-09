import { CURRICULUM } from "@/lib/curriculum";
import type { CurriculumLevel, CurriculumTopic } from "@/lib/types";

export type CurriculumTopicRef = {
  courseId: string;
  courseName: string;
  path: string[];
  topicId: string;
  topicName: string;
  typeId: string;
};

function walkTopics(
  course: CurriculumLevel,
  topics: CurriculumTopic[],
  chapterPath: string[],
  chapterNames: string[],
  onLeaf: (topic: CurriculumTopic, path: string[], names: string[]) => void,
): void {
  for (const topic of topics) {
    if (topic.topics?.length) {
      walkTopics(course, topic.topics, [...chapterPath, topic.id], [...chapterNames, topic.name], onLeaf);
      continue;
    }
    onLeaf(topic, [...chapterPath, topic.id], [...chapterNames, topic.name]);
  }
}

/** Leaf curriculum topics that link to a real question generator via type_id. */
export function getTopicsWithGenerators(curriculum: CurriculumLevel[]): CurriculumTopicRef[] {
  const refs: CurriculumTopicRef[] = [];

  for (const course of curriculum) {
    walkTopics(course, course.topics, [], [], (topic, _path, names) => {
      if (!topic.type_id) return;
      refs.push({
        courseId: course.id,
        courseName: course.name,
        path: [course.id, ...names.slice(0, -1), topic.id],
        topicId: topic.id,
        topicName: topic.name,
        typeId: topic.type_id,
      });
    });
  }

  return refs;
}

/** Build type_id → curriculum references (deduped by course + topic id). */
export function buildTypeIdIndex(
  curriculum: CurriculumLevel[],
): Map<string, CurriculumTopicRef[]> {
  const index = new Map<string, CurriculumTopicRef[]>();
  for (const ref of getTopicsWithGenerators(curriculum)) {
    const existing = index.get(ref.typeId) ?? [];
    existing.push(ref);
    index.set(ref.typeId, existing);
  }
  return index;
}

/** All curriculum paths where a question type appears. */
export function findCurriculumReferences(
  curriculum: CurriculumLevel[],
  typeId: string,
): CurriculumTopicRef[] {
  return buildTypeIdIndex(curriculum).get(typeId) ?? [];
}

/** Exported mapping from type_id to human-readable curriculum paths. */
export function getTypeIdToCurriculumPaths(
  curriculum: CurriculumLevel[],
): Record<string, string[]> {
  const index = buildTypeIdIndex(curriculum);
  const result: Record<string, string[]> = {};

  for (const [typeId, refs] of index.entries()) {
    result[typeId] = refs.map(
      (ref) => `${ref.courseName} › ${ref.path.slice(1, -1).join(" › ") || ref.topicName} › ${ref.topicName}`,
    );
  }

  return result;
}

/** Pre-built index from the default curriculum tree. */
export const TYPE_ID_TO_CURRICULUM_PATHS = getTypeIdToCurriculumPaths(CURRICULUM);
