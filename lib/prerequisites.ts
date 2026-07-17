import prerequisiteIndex from "@/lib/data/prerequisite-index.json";
import type { CurriculumSelection, PickerCourse } from "@/lib/curriculum-picker";

export type PrerequisiteRef = {
  key: string;
  courseId: string;
  chapterId: string;
  title: string;
  /** Present on topic-level refs. */
  topicId?: string;
  typeId?: string;
};

export type PrerequisiteEntry = {
  key: string;
  courseId: string;
  chapterId: string;
  title: string;
  reason: string;
  requires: PrerequisiteRef[];
  /** Present on topic-level entries. */
  topicId?: string;
  typeId?: string;
};

type PrerequisiteIndex = {
  version: number;
  entries: Record<string, PrerequisiteEntry>;
  topicEntries?: Record<string, PrerequisiteEntry>;
  typeIdToTopicKey?: Record<string, string>;
  nodeToCurriculumKey?: Record<string, string>;
};

const INDEX = prerequisiteIndex as PrerequisiteIndex;

export function chapterPrerequisiteKey(courseId: string, chapterId: string): string {
  return `${courseId}:${chapterId}`;
}

export function topicPrerequisiteKey(
  courseId: string,
  chapterId: string,
  topicId: string,
): string {
  return `${courseId}:${chapterId}:${topicId}`;
}

export function getPrerequisiteEntry(
  courseId: string,
  chapterId: string,
): PrerequisiteEntry | null {
  return INDEX.entries[chapterPrerequisiteKey(courseId, chapterId)] ?? null;
}

export function getTopicPrerequisiteEntry(
  courseId: string,
  chapterId: string,
  topicId: string,
): PrerequisiteEntry | null {
  const topicEntries = INDEX.topicEntries;
  if (!topicEntries) return null;
  return topicEntries[topicPrerequisiteKey(courseId, chapterId, topicId)] ?? null;
}

export function getTopicPrerequisiteByTypeId(typeId: string): PrerequisiteEntry | null {
  const key = INDEX.typeIdToTopicKey?.[typeId];
  if (!key || !INDEX.topicEntries) return null;
  return INDEX.topicEntries[key] ?? null;
}

/**
 * Prefer topic/leaf skill deps when authored; otherwise fall back to chapter overview.
 */
export function getPrerequisitesForSelection(
  selection: CurriculumSelection | null,
): PrerequisiteEntry | null {
  if (!selection) return null;
  const topicEntry = getTopicPrerequisiteEntry(
    selection.courseId,
    selection.chapterId,
    selection.topicId,
  );
  if (topicEntry) return topicEntry;
  return getPrerequisiteEntry(selection.courseId, selection.chapterId);
}

/** First selectable topic in a chapter (ready preferred). */
export function findJumpTargetInChapter(
  courses: PickerCourse[],
  courseId: string,
  chapterId: string,
  preferredTopicId?: string,
): (CurriculumSelection & { topicName: string; hasGenerator: boolean; typeId: string | null }) | null {
  const course = courses.find((entry) => entry.id === courseId);
  const chapter = course?.chapters.find((entry) => entry.id === chapterId);
  if (!course || !chapter || chapter.topics.length === 0) return null;

  const preferred = preferredTopicId
    ? chapter.topics.find((topic) => topic.id === preferredTopicId)
    : undefined;
  const ready = chapter.topics.find((topic) => topic.hasGenerator);
  const topic = preferred ?? ready ?? chapter.topics[0];
  return {
    courseId: course.id,
    chapterId: chapter.id,
    topicId: topic.id,
    topicName: topic.name,
    hasGenerator: topic.hasGenerator,
    typeId: topic.typeId,
  };
}
