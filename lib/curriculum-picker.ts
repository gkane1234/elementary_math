import { CURRICULUM } from "@/lib/curriculum";
import {
  INCORRECT_IMPLEMENTATION_TYPE_IDS,
  REQUIRES_DIAGRAM_TYPE_IDS,
  typeIsNotReady,
} from "@/lib/diagram-readiness";
import type { CurriculumLevel, CurriculumTopic, QuestionTypeInfo } from "@/lib/types";

export type TopicPickerStatus = "ready" | "preview" | "coming_soon";

export type PickerTopic = {
  id: string;
  name: string;
  typeId: string | null;
  status: TopicPickerStatus;
  hasGenerator: boolean;
};

export type PickerChapter = {
  id: string;
  name: string;
  topics: PickerTopic[];
};

export type PickerCourse = {
  id: string;
  name: string;
  chapters: PickerChapter[];
};

export type CurriculumSelection = {
  courseId: string;
  chapterId: string;
  topicId: string;
};

export type FlatTopicSearchResult = CurriculumSelection & {
  courseName: string;
  chapterName: string;
  topic: PickerTopic;
};

function topicStatus(
  typeId: string | null | undefined,
  availableTypeIds: Set<string>,
  notReadyIds: Set<string>,
): TopicPickerStatus {
  if (!typeId) return "coming_soon";
  // Diagram / incorrect-implementation demotions are Coming soon (not selectable).
  if (notReadyIds.has(typeId)) return "coming_soon";
  if (!availableTypeIds.has(typeId)) return "preview";
  return "ready";
}

function makePickerTopic(
  topic: CurriculumTopic,
  availableTypeIds: Set<string>,
  notReadyIds: Set<string>,
): PickerTopic {
  const typeId = topic.type_id ?? null;
  const status = topicStatus(typeId, availableTypeIds, notReadyIds);
  return {
    id: topic.id,
    name: topic.name,
    typeId,
    status,
    hasGenerator: status === "ready",
  };
}

function collectLeaves(
  topics: CurriculumTopic[],
  availableTypeIds: Set<string>,
  notReadyIds: Set<string>,
): PickerTopic[] {
  const leaves: PickerTopic[] = [];
  for (const topic of topics) {
    if (topic.topics?.length) {
      leaves.push(...collectLeaves(topic.topics, availableTypeIds, notReadyIds));
      continue;
    }
    leaves.push(makePickerTopic(topic, availableTypeIds, notReadyIds));
  }
  return leaves;
}

function buildChapters(
  courseTopics: CurriculumTopic[],
  availableTypeIds: Set<string>,
  notReadyIds: Set<string>,
): PickerChapter[] {
  return courseTopics.map((chapter) => ({
    id: chapter.id,
    name: chapter.name,
    topics: collectLeaves(chapter.topics ?? [], availableTypeIds, notReadyIds),
  }));
}

export function buildCurriculumPicker(
  curriculum: CurriculumLevel[] = CURRICULUM,
  types: QuestionTypeInfo[] = [],
): PickerCourse[] {
  // Ready = wired generator that is not demoted (diagram gap, wrong implementation, etc.).
  // Block via API flags and/or the frontend denylists (defense in depth).
  const notReadyIds = new Set<string>([
    ...REQUIRES_DIAGRAM_TYPE_IDS,
    ...INCORRECT_IMPLEMENTATION_TYPE_IDS,
  ]);
  for (const type of types) {
    if (typeIsNotReady(type)) notReadyIds.add(type.id);
  }

  const availableTypeIds = new Set(
    types.filter((type) => !typeIsNotReady(type)).map((type) => type.id),
  );

  return curriculum.map((course) => ({
    id: course.id,
    name: course.name,
    chapters: buildChapters(course.topics, availableTypeIds, notReadyIds),
  }));
}

export function findFirstTopicByTypeId(
  courses: PickerCourse[],
  typeId: string,
): (CurriculumSelection & { topic: PickerTopic }) | null {
  for (const course of courses) {
    for (const chapter of course.chapters) {
      for (const topic of chapter.topics) {
        if (topic.typeId === typeId) {
          return {
            courseId: course.id,
            chapterId: chapter.id,
            topicId: topic.id,
            topic,
          };
        }
      }
    }
  }
  return null;
}

export function findTopicSelection(
  courses: PickerCourse[],
  selection: CurriculumSelection,
): PickerTopic | null {
  const course = courses.find((entry) => entry.id === selection.courseId);
  const chapter = course?.chapters.find((entry) => entry.id === selection.chapterId);
  return chapter?.topics.find((entry) => entry.id === selection.topicId) ?? null;
}

export function getDefaultSelection(
  courses: PickerCourse[],
  preferredTypeId?: string,
): CurriculumSelection | null {
  if (preferredTypeId) {
    const match = findFirstTopicByTypeId(courses, preferredTypeId);
    if (match?.topic.hasGenerator) {
      return {
        courseId: match.courseId,
        chapterId: match.chapterId,
        topicId: match.topicId,
      };
    }
  }

  for (const course of courses) {
    for (const chapter of course.chapters) {
      const readyTopic = chapter.topics.find((topic) => topic.hasGenerator);
      if (readyTopic) {
        return {
          courseId: course.id,
          chapterId: chapter.id,
          topicId: readyTopic.id,
        };
      }
    }
  }

  const firstCourse = courses[0];
  const firstChapter = firstCourse?.chapters[0];
  const firstTopic = firstChapter?.topics[0];
  if (!firstCourse || !firstChapter || !firstTopic) return null;

  return {
    courseId: firstCourse.id,
    chapterId: firstChapter.id,
    topicId: firstTopic.id,
  };
}

export function flattenTopicsForSearch(courses: PickerCourse[]): FlatTopicSearchResult[] {
  const results: FlatTopicSearchResult[] = [];
  for (const course of courses) {
    for (const chapter of course.chapters) {
      for (const topic of chapter.topics) {
        results.push({
          courseId: course.id,
          courseName: course.name,
          chapterId: chapter.id,
          chapterName: chapter.name,
          topicId: topic.id,
          topic,
        });
      }
    }
  }
  return results;
}

export type TopicFilterOptions = {
  courseId?: string;
  chapterId?: string;
  readyOnly?: boolean;
};

export function filterTopics(
  courses: PickerCourse[],
  query: string,
  filters: TopicFilterOptions = {},
): FlatTopicSearchResult[] {
  const normalizedQuery = query.trim().toLowerCase();
  return flattenTopicsForSearch(courses).filter((entry) => {
    if (filters.readyOnly && !entry.topic.hasGenerator) return false;
    if (filters.courseId && entry.courseId !== filters.courseId) return false;
    if (filters.chapterId) {
      const separator = filters.chapterId.indexOf(":");
      if (separator !== -1) {
        const courseId = filters.chapterId.slice(0, separator);
        const chapterId = filters.chapterId.slice(separator + 1);
        if (entry.courseId !== courseId || entry.chapterId !== chapterId) return false;
      } else if (entry.chapterId !== filters.chapterId) {
        return false;
      }
    }
    if (normalizedQuery && !entry.topic.name.toLowerCase().includes(normalizedQuery)) return false;
    return true;
  });
}

export function getUnmappedTypes(types: QuestionTypeInfo[], courses: PickerCourse[]): QuestionTypeInfo[] {
  const mapped = new Set<string>();
  for (const course of courses) {
    for (const chapter of course.chapters) {
      for (const topic of chapter.topics) {
        if (topic.typeId) mapped.add(topic.typeId);
      }
    }
  }
  // Hide demoted types from the fallback selector too.
  return types.filter((type) => !mapped.has(type.id) && !typeIsNotReady(type));
}

export function topicStatusLabel(status: TopicPickerStatus): string {
  switch (status) {
    case "ready":
      return "Ready";
    case "preview":
      return "Preview";
    case "coming_soon":
      return "Coming soon";
  }
}
