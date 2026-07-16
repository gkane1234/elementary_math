import prerequisiteIndex from "@/lib/data/prerequisite-index.json";
import type { CurriculumSelection, PickerCourse } from "@/lib/curriculum-picker";

export type PrerequisiteRef = {
  key: string;
  courseId: string;
  chapterId: string;
  title: string;
};

export type PrerequisiteEntry = {
  key: string;
  courseId: string;
  chapterId: string;
  title: string;
  reason: string;
  requires: PrerequisiteRef[];
};

type PrerequisiteIndex = {
  version: number;
  entries: Record<string, PrerequisiteEntry>;
  nodeToCurriculumKey?: Record<string, string>;
};

const INDEX = prerequisiteIndex as PrerequisiteIndex;

export function chapterPrerequisiteKey(courseId: string, chapterId: string): string {
  return `${courseId}:${chapterId}`;
}

export function getPrerequisiteEntry(
  courseId: string,
  chapterId: string,
): PrerequisiteEntry | null {
  return INDEX.entries[chapterPrerequisiteKey(courseId, chapterId)] ?? null;
}

export function getPrerequisitesForSelection(
  selection: CurriculumSelection | null,
): PrerequisiteEntry | null {
  if (!selection) return null;
  return getPrerequisiteEntry(selection.courseId, selection.chapterId);
}

/** First selectable topic in a chapter (ready preferred). */
export function findJumpTargetInChapter(
  courses: PickerCourse[],
  courseId: string,
  chapterId: string,
): (CurriculumSelection & { topicName: string; hasGenerator: boolean }) | null {
  const course = courses.find((entry) => entry.id === courseId);
  const chapter = course?.chapters.find((entry) => entry.id === chapterId);
  if (!course || !chapter || chapter.topics.length === 0) return null;

  const ready = chapter.topics.find((topic) => topic.hasGenerator);
  const topic = ready ?? chapter.topics[0];
  return {
    courseId: course.id,
    chapterId: chapter.id,
    topicId: topic.id,
    topicName: topic.name,
    hasGenerator: topic.hasGenerator,
  };
}
