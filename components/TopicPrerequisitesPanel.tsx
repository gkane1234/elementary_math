"use client";

import { useMemo } from "react";
import {
  buildCurriculumPicker,
  findFirstTopicByTypeId,
  type CurriculumSelection,
} from "@/lib/curriculum-picker";
import {
  findJumpTargetInChapter,
  getPrerequisiteEntry,
  getPrerequisitesForSelection,
  type PrerequisiteEntry,
  type PrerequisiteRef,
} from "@/lib/prerequisites";
import type { QuestionTypeInfo } from "@/lib/types";

type TopicPrerequisitesPanelProps = {
  types: QuestionTypeInfo[];
  /** Active question type (from topic options modal). */
  typeId: string | null;
  /**
   * Optional chapter being browsed for drill-down when the target has no ready generator.
   * When set, takes precedence over typeId for which prerequisites are shown.
   */
  browseSelection?: CurriculumSelection | null;
  onNavigateToType: (typeId: string) => void;
  onBrowseChapter: (selection: CurriculumSelection) => void;
};

function resolveEntry(
  types: QuestionTypeInfo[],
  typeId: string | null,
  browseSelection: CurriculumSelection | null | undefined,
): { entry: PrerequisiteEntry | null; label: string } {
  const courses = buildCurriculumPicker(undefined, types);

  if (browseSelection) {
    const course = courses.find((c) => c.id === browseSelection.courseId);
    const chapter = course?.chapters.find((c) => c.id === browseSelection.chapterId);
    const topic = chapter?.topics.find((t) => t.id === browseSelection.topicId);
    const label = [course?.name, chapter?.name, topic?.name].filter(Boolean).join(" › ");
    return {
      entry: getPrerequisitesForSelection(browseSelection),
      label: label || "Selected chapter",
    };
  }

  if (!typeId) {
    return { entry: null, label: "" };
  }

  const mapped = findFirstTopicByTypeId(courses, typeId);
  if (!mapped) {
    return { entry: null, label: "" };
  }

  const course = courses.find((c) => c.id === mapped.courseId);
  const chapter = course?.chapters.find((c) => c.id === mapped.chapterId);
  const label = [course?.name, chapter?.name, mapped.topic.name].filter(Boolean).join(" › ");
  return {
    entry: getPrerequisiteEntry(mapped.courseId, mapped.chapterId),
    label,
  };
}

export function TopicPrerequisitesPanel({
  types,
  typeId,
  browseSelection = null,
  onNavigateToType,
  onBrowseChapter,
}: TopicPrerequisitesPanelProps) {
  const courses = useMemo(() => buildCurriculumPicker(undefined, types), [types]);
  const { entry, label } = useMemo(
    () => resolveEntry(types, typeId, browseSelection),
    [types, typeId, browseSelection],
  );

  if (!typeId && !browseSelection) {
    return null;
  }

  const browsePrerequisite = (req: PrerequisiteRef) => {
    const jump = findJumpTargetInChapter(
      courses,
      req.courseId,
      req.chapterId,
      req.topicId,
    );
    if (!jump) return;

    onBrowseChapter({
      courseId: jump.courseId,
      chapterId: jump.chapterId,
      topicId: jump.topicId,
    });
  };

  const openPrerequisite = (req: PrerequisiteRef) => {
    if (req.typeId) {
      onNavigateToType(req.typeId);
      return;
    }
    const jump = findJumpTargetInChapter(
      courses,
      req.courseId,
      req.chapterId,
      req.topicId,
    );
    if (!jump) return;

    if (jump.hasGenerator && jump.typeId) {
      onNavigateToType(jump.typeId);
      return;
    }

    browsePrerequisite(req);
  };

  return (
    <section className="topic-options-prereqs" aria-label="Prerequisites">
      <div className="topic-options-prereqs-header">
        <h3>Prerequisites</h3>
        {label ? <p className="topic-options-prereqs-path">{label}</p> : null}
      </div>

      {entry && entry.requires.length > 0 ? (
        <>
          {entry.reason ? <p className="topic-options-prereqs-reason">{entry.reason}</p> : null}
          <ul className="topic-options-prereqs-list">
            {entry.requires.map((req) => {
              const jump = findJumpTargetInChapter(
                courses,
                req.courseId,
                req.chapterId,
                req.topicId,
              );
              const courseName =
                courses.find((course) => course.id === req.courseId)?.name ?? req.courseId;
              return (
                <li key={req.key}>
                  <button
                    type="button"
                    className="topic-options-prereq-link"
                    disabled={!jump}
                    onClick={() => browsePrerequisite(req)}
                    onDoubleClick={() => openPrerequisite(req)}
                    onContextMenu={(event) => {
                      event.preventDefault();
                      browsePrerequisite(req);
                    }}
                  >
                    <span className="topic-options-prereq-title">{req.title}</span>
                    <span className="topic-options-prereq-meta">
                      {courseName}
                      {jump?.hasGenerator ? " · ready" : jump ? " · view prerequisites" : ""}
                    </span>
                  </button>
                </li>
              );
            })}
          </ul>
          <p className="topic-options-prereqs-hint">
            Single-click or right-click to browse prerequisites. Double-click a ready topic to
            open its options.
          </p>
        </>
      ) : (
        <p className="topic-options-prereqs-empty">
          No curated prerequisites for this topic yet
          {browseSelection ? " (foundation topic)" : ""}.
        </p>
      )}
    </section>
  );
}
