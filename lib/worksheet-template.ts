/** Grade 6 and Geometry worksheet template helpers.

Both courses are read from `lib/curriculum.ts`. Other courses have no template
course id, so the generator keeps the older related-topic controls.
*/

import { CURRICULUM } from "@/lib/curriculum";
import type { ProgressivePairing, ProgressiveScope } from "@/lib/progressive";

export type TemplateCourseId = "grade_6_math" | "geometry";

export type ScopeTopic = {
  typeId: string;
  name: string;
  chapterId: string;
  chapterName: string;
};

type Placement = ScopeTopic & {
  courseId: TemplateCourseId;
  chapterIndex: number;
};

function isTemplateCourse(courseId: string): courseId is TemplateCourseId {
  return courseId === "grade_6_math" || courseId === "geometry";
}

function placements(typeId: string): Placement[] {
  const hits: Placement[] = [];
  for (const course of CURRICULUM) {
    if (!isTemplateCourse(course.id)) continue;
    const courseId = course.id;
    course.topics.forEach((chapter, chapterIndex) => {
      for (const leaf of chapter.topics ?? []) {
        if (leaf.type_id !== typeId) continue;
        hits.push({
          courseId,
          chapterIndex,
          chapterId: chapter.id,
          chapterName: chapter.name,
          typeId,
          name: leaf.name,
        });
      }
    });
  }
  return hits;
}

function placementFor(typeId: string): Placement | null {
  const hits = placements(typeId);
  return (
    hits.find((hit) => hit.courseId === "grade_6_math") ??
    hits.find((hit) => hit.courseId === "geometry") ??
    null
  );
}

/** Template course for a leaf, or null when the seed stays on the old expander. */
export function courseOfType(typeId: string): TemplateCourseId | null {
  return placementFor(typeId)?.courseId ?? null;
}

function leavesInChapters(typeId: string, chapterIndexes: number[]): ScopeTopic[] {
  const place = placementFor(typeId);
  if (!place) return [];
  const course = CURRICULUM.find((level) => level.id === place.courseId);
  if (!course) return [];
  const out: ScopeTopic[] = [];
  const seen = new Set<string>();
  for (const index of chapterIndexes) {
    const chapter = course.topics[index];
    if (!chapter) continue;
    for (const leaf of chapter.topics ?? []) {
      if (!leaf.type_id || seen.has(leaf.type_id)) continue;
      seen.add(leaf.type_id);
      out.push({
        typeId: leaf.type_id,
        name: leaf.name,
        chapterId: chapter.id,
        chapterName: chapter.name,
      });
    }
  }
  return out;
}

/** Leaves the checklist shows for a scope. One topic returns that leaf only. */
export function scopeTopicChoices(typeId: string, scope: ProgressiveScope): ScopeTopic[] {
  const place = placementFor(typeId);
  if (!place) return [];
  if (scope === "topic") {
    return [
      {
        typeId: place.typeId,
        name: place.name,
        chapterId: place.chapterId,
        chapterName: place.chapterName,
      },
    ];
  }
  const indexes = [place.chapterIndex];
  if (scope === "adjacent") indexes.push(place.chapterIndex + 1);
  return leavesInChapters(typeId, indexes);
}

/** Type ids for a scope, curriculum order. Geometry leaves are included. */
export function unitTopicIdsForScope(typeId: string, scope: ProgressiveScope): string[] {
  return scopeTopicChoices(typeId, scope).map((topic) => topic.typeId);
}

/**
 * Hint naming the previous unit. Null for the first unit in the course.
 * Choosing spiral is still explicit; this does not switch pairing.
 */
export function spiralSuggestionText(
  typeId: string,
  pairing?: ProgressivePairing,
): string | null {
  const place = placementFor(typeId);
  if (!place || place.chapterIndex <= 0) return null;
  const course = CURRICULUM.find((level) => level.id === place.courseId);
  const previous = course?.topics[place.chapterIndex - 1];
  if (!previous) return null;
  if (pairing === "spiral") {
    return `Spiral review starts from ${previous.name}.`;
  }
  return `Spiral review of ${previous.name} is available. Choose Spiral to use it.`;
}
