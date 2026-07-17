"use client";

import { useEffect, useMemo, useState, type MouseEvent } from "react";
import {
  buildCurriculumPicker,
  filterTopics,
  filterUnmappedTypes,
  findFirstTopicByTypeId,
  findTopicSelection,
  getUnmappedTypes,
  topicStatusLabel,
  type CurriculumSelection,
  type FlatTopicSearchResult,
} from "@/lib/curriculum-picker";
import {
  findJumpTargetInChapter,
  getPrerequisitesForSelection,
} from "@/lib/prerequisites";
import { formatQuestionTypeLabel } from "@/lib/question-type-groups";
import type { QuestionTypeInfo } from "@/lib/types";

type CurriculumTopicPickerProps = {
  types: QuestionTypeInfo[];
  selectedTypeId: string;
  onTypeIdChange: (typeId: string) => void;
};

type TopicGroup = {
  key: string;
  label: string;
  entries: FlatTopicSearchResult[];
};

type PrereqHistoryEntry = {
  selection: CurriculumSelection;
  /** Prerequisite key entered from this view (restored on Back). */
  enteredKey: string;
};

type PrereqContextMenuState = {
  x: number;
  y: number;
  courseId: string;
  chapterId: string;
  /** Highlight / history key for this menu target. */
  prereqKey: string;
  title: string;
  canAdd: boolean;
  /** Specific curriculum topic when drilling into a skill-level prerequisite. */
  topicId?: string;
  typeId?: string | null;
};

function selectionKey(selection: CurriculumSelection): string {
  return `${selection.courseId}:${selection.chapterId}:${selection.topicId}`;
}

function groupFilteredTopics(entries: FlatTopicSearchResult[]): TopicGroup[] {
  const groups: TopicGroup[] = [];
  const indexByKey = new Map<string, number>();

  for (const entry of entries) {
    const key = `${entry.courseId}:${entry.chapterId}`;
    const label = `${entry.courseName} › ${entry.chapterName}`;
    const existing = indexByKey.get(key);
    if (existing === undefined) {
      indexByKey.set(key, groups.length);
      groups.push({ key, label, entries: [entry] });
    } else {
      groups[existing].entries.push(entry);
    }
  }

  return groups;
}

export function CurriculumTopicPicker({
  types,
  selectedTypeId,
  onTypeIdChange,
}: CurriculumTopicPickerProps) {
  const courses = useMemo(() => buildCurriculumPicker(undefined, types), [types]);
  const unmappedTypes = useMemo(() => getUnmappedTypes(types, courses), [types, courses]);

  /** Highlighted row in the topic list. */
  const [selection, setSelection] = useState<CurriculumSelection | null>(null);
  /** Topic whose prerequisites are shown (may differ while browsing the prereq chain). */
  const [prereqView, setPrereqView] = useState<CurriculumSelection | null>(null);
  const [prereqHistory, setPrereqHistory] = useState<PrereqHistoryEntry[]>([]);
  const [highlightedPrereqKey, setHighlightedPrereqKey] = useState<string | null>(null);
  const [prereqMenu, setPrereqMenu] = useState<PrereqContextMenuState | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [filterCourseId, setFilterCourseId] = useState("");
  const [filterChapterId, setFilterChapterId] = useState("");
  const [readyOnly, setReadyOnly] = useState(true);
  const [useFallback, setUseFallback] = useState(false);
  /** Local highlight for unmapped types (selection does not open the add modal). */
  const [focusedUnmappedId, setFocusedUnmappedId] = useState<string | null>(null);

  const filterCourse = courses.find((course) => course.id === filterCourseId) ?? null;
  const chapterFilterOptions = useMemo(() => {
    const chapters: { id: string; name: string; courseId: string; courseName: string }[] = [];
    const sourceCourses = filterCourse ? [filterCourse] : courses;
    for (const course of sourceCourses) {
      for (const chapter of course.chapters) {
        chapters.push({
          id: chapter.id,
          name: chapter.name,
          courseId: course.id,
          courseName: course.name,
        });
      }
    }
    return chapters;
  }, [courses, filterCourse]);

  const filteredTopics = useMemo(
    () =>
      filterTopics(courses, searchQuery, {
        courseId: filterCourseId || undefined,
        chapterId: filterChapterId || undefined,
        readyOnly,
      }),
    [courses, searchQuery, filterCourseId, filterChapterId, readyOnly],
  );

  const topicGroups = useMemo(() => groupFilteredTopics(filteredTopics), [filteredTopics]);

  const filteredUnmapped = useMemo(
    () =>
      filterUnmappedTypes(unmappedTypes, {
        query: searchQuery,
        readyOnly,
        courseId: filterCourseId || undefined,
      }),
    [unmappedTypes, searchQuery, readyOnly, filterCourseId],
  );

  const prerequisiteEntry = useMemo(
    () => getPrerequisitesForSelection(prereqView),
    [prereqView],
  );

  const prereqViewTopic = useMemo(
    () => (prereqView ? findTopicSelection(courses, prereqView) : null),
    [courses, prereqView],
  );

  const prereqViewChapterName = useMemo(() => {
    if (!prereqView) return null;
    const course = courses.find((entry) => entry.id === prereqView.courseId);
    return course?.chapters.find((entry) => entry.id === prereqView.chapterId)?.name ?? null;
  }, [courses, prereqView]);

  useEffect(() => {
    if (types.length === 0) return;

    const mapped = findFirstTopicByTypeId(courses, selectedTypeId);
    if (mapped) {
      const next = {
        courseId: mapped.courseId,
        chapterId: mapped.chapterId,
        topicId: mapped.topicId,
      };
      setSelection(next);
      setPrereqView(next);
      setPrereqHistory([]);
      setHighlightedPrereqKey(null);
      setUseFallback(false);
      setFocusedUnmappedId(null);
      return;
    }

    if (selectedTypeId && unmappedTypes.some((type) => type.id === selectedTypeId)) {
      setSelection(null);
      setPrereqView(null);
      setPrereqHistory([]);
      setHighlightedPrereqKey(null);
      setUseFallback(true);
      setFocusedUnmappedId(selectedTypeId);
      return;
    }

    if (!selectedTypeId) {
      setUseFallback(false);
    }
  }, [courses, selectedTypeId, types.length, unmappedTypes]);

  const resetPrereqBrowse = (next: CurriculumSelection) => {
    setPrereqView(next);
    setPrereqHistory([]);
    setHighlightedPrereqKey(null);
    setPrereqMenu(null);
  };

  /** Select a topic for browsing prerequisites without opening the add-topic dialog. */
  const selectForBrowse = (next: CurriculumSelection) => {
    setSelection(next);
    setUseFallback(false);
    setFocusedUnmappedId(null);
    resetPrereqBrowse(next);
  };

  const openAddTopic = (typeId: string) => {
    if (!typeId) return;
    onTypeIdChange(typeId);
  };

  const handleListSelect = (entry: FlatTopicSearchResult) => {
    selectForBrowse({
      courseId: entry.courseId,
      chapterId: entry.chapterId,
      topicId: entry.topicId,
    });
  };

  const handleListOpen = (entry: FlatTopicSearchResult) => {
    handleListSelect(entry);
    if (entry.topic.hasGenerator && entry.topic.typeId) {
      openAddTopic(entry.topic.typeId);
    }
  };

  const handlePrerequisiteHighlight = (prereqKey: string) => {
    setHighlightedPrereqKey(prereqKey);
  };

  const handlePrerequisiteDrill = (
    courseId: string,
    chapterId: string,
    prereqKey: string,
    preferredTopicId?: string,
  ) => {
    const target = findJumpTargetInChapter(courses, courseId, chapterId, preferredTopicId);
    if (!target || !prereqView) return;

    setHighlightedPrereqKey(prereqKey);

    const next: CurriculumSelection = {
      courseId: target.courseId,
      chapterId: target.chapterId,
      topicId: target.topicId,
    };

    if (selectionKey(prereqView) === selectionKey(next)) {
      return;
    }

    if (!target.hasGenerator) {
      setReadyOnly(false);
    }

    setPrereqHistory((history) => [
      ...history,
      { selection: prereqView, enteredKey: prereqKey },
    ]);
    setPrereqView(next);
    setHighlightedPrereqKey(null);
  };

  const handlePrerequisiteOpen = (
    courseId: string,
    chapterId: string,
    prereqKey: string,
    preferredTopicId?: string,
  ) => {
    const target = findJumpTargetInChapter(courses, courseId, chapterId, preferredTopicId);
    if (!target) return;
    setHighlightedPrereqKey(prereqKey);
    const topic = findTopicSelection(courses, {
      courseId: target.courseId,
      chapterId: target.chapterId,
      topicId: target.topicId,
    });
    if (topic?.hasGenerator && topic.typeId) {
      openAddTopic(topic.typeId);
    }
  };

  const openPrereqMenu = (
    event: MouseEvent,
    courseId: string,
    chapterId: string,
    prereqKey: string,
    title: string,
    options?: { topicId?: string; typeId?: string | null; canAdd?: boolean },
  ) => {
    event.preventDefault();
    setHighlightedPrereqKey(prereqKey);

    let canAdd = options?.canAdd;
    if (canAdd === undefined) {
      const jump = findJumpTargetInChapter(courses, courseId, chapterId);
      if (!jump) return;
      const topic = findTopicSelection(courses, {
        courseId: jump.courseId,
        chapterId: jump.chapterId,
        topicId: jump.topicId,
      });
      canAdd = Boolean(topic?.hasGenerator && topic.typeId);
    }

    setPrereqMenu({
      x: event.clientX,
      y: event.clientY,
      courseId,
      chapterId,
      prereqKey,
      title,
      canAdd: Boolean(canAdd),
      topicId: options?.topicId,
      typeId: options?.typeId,
    });
  };

  const closePrereqMenu = () => setPrereqMenu(null);

  const handlePrereqBack = () => {
    setPrereqHistory((history) => {
      if (history.length === 0) return history;
      const previous = history[history.length - 1];
      setPrereqView(previous.selection);
      setHighlightedPrereqKey(previous.enteredKey);
      return history.slice(0, -1);
    });
  };

  const handleFilterCourseChange = (courseId: string) => {
    setFilterCourseId(courseId);
    if (!courseId) {
      setFilterChapterId("");
      return;
    }

    const course = courses.find((entry) => entry.id === courseId);
    const separator = filterChapterId.indexOf(":");
    const chapterId =
      separator === -1
        ? filterChapterId
        : filterChapterId.slice(0, separator) === courseId
          ? filterChapterId.slice(separator + 1)
          : "";

    if (!chapterId || !course?.chapters.some((chapter) => chapter.id === chapterId)) {
      setFilterChapterId("");
    }
  };

  if (courses.length === 0 && unmappedTypes.length === 0) {
    return null;
  }

  const listEmpty = filteredTopics.length === 0 && filteredUnmapped.length === 0;
  const canGoBack = prereqHistory.length > 0;

  return (
    <div className="curriculum-picker">
      <div className="curriculum-picker-controls">
        <div className="curriculum-picker-toolbar">
          <label className="field curriculum-picker-search">
            <span className="sr-only">Search topics</span>
            <input
              type="search"
              placeholder="Search topics…"
              value={searchQuery}
              onChange={(event) => setSearchQuery(event.target.value)}
              aria-label="Search topics"
            />
          </label>

          <label className="field field-inline curriculum-picker-ready-only">
            <input
              type="checkbox"
              checked={readyOnly}
              onChange={(event) => setReadyOnly(event.target.checked)}
            />
            <span>Ready only</span>
          </label>
        </div>

        <div className="curriculum-picker-filters">
          <label className="field">
            <span>Course</span>
            <select
              value={filterCourseId}
              onChange={(event) => handleFilterCourseChange(event.target.value)}
            >
              <option value="">All courses</option>
              {courses.map((course) => (
                <option key={course.id} value={course.id}>
                  {course.name}
                </option>
              ))}
            </select>
          </label>

          <label className="field">
            <span>Chapter</span>
            <select
              value={filterChapterId}
              onChange={(event) => setFilterChapterId(event.target.value)}
            >
              <option value="">All chapters</option>
              {chapterFilterOptions.map((chapter) => {
                const value = filterCourse ? chapter.id : `${chapter.courseId}:${chapter.id}`;
                return (
                  <option key={`${chapter.courseId}:${chapter.id}`} value={value}>
                    {filterCourse ? chapter.name : `${chapter.courseName} › ${chapter.name}`}
                  </option>
                );
              })}
            </select>
          </label>
        </div>
      </div>

      <div className="curriculum-topic-list" role="listbox" aria-label="Topics">
        {listEmpty ? (
          <p className="curriculum-topic-list-empty">No topics match your search or filters.</p>
        ) : (
          <>
            {topicGroups.map((group) => (
              <div key={group.key} className="curriculum-topic-group">
                <div className="curriculum-topic-section-header" role="presentation">
                  {group.label}
                </div>
                {group.entries.map((entry) => {
                  const isSelected =
                    selection?.courseId === entry.courseId &&
                    selection.chapterId === entry.chapterId &&
                    selection.topicId === entry.topicId;

                  return (
                    <button
                      key={`${entry.courseId}-${entry.chapterId}-${entry.topicId}`}
                      type="button"
                      role="option"
                      aria-selected={isSelected}
                      className={`curriculum-topic-row${isSelected ? " is-selected" : ""}${
                        entry.topic.hasGenerator ? "" : " is-browse-only"
                      }`}
                      onClick={() => handleListSelect(entry)}
                      onDoubleClick={() => handleListOpen(entry)}
                      onContextMenu={(event) => {
                        event.preventDefault();
                        handleListSelect(entry);
                      }}
                    >
                      <span className="curriculum-topic-row-check" aria-hidden="true">
                        {isSelected ? "✓" : ""}
                      </span>
                      <span className="curriculum-topic-row-main">
                        <span className="curriculum-topic-row-name">{entry.topic.name}</span>
                      </span>
                      <span
                        className={`topic-status-badge${
                          entry.topic.status === "ready" ? " is-ready" : ""
                        }`}
                      >
                        {topicStatusLabel(entry.topic.status)}
                      </span>
                    </button>
                  );
                })}
              </div>
            ))}

            {filteredUnmapped.length > 0 && (
              <div className="curriculum-topic-group">
                <div className="curriculum-topic-section-header" role="presentation">
                  Other question types
                </div>
                {filteredUnmapped.map((type) => {
                  const isSelected = useFallback && focusedUnmappedId === type.id;
                  return (
                    <button
                      key={type.id}
                      type="button"
                      role="option"
                      aria-selected={isSelected}
                      className={`curriculum-topic-row${isSelected ? " is-selected" : ""}`}
                      onClick={() => {
                        setSelection(null);
                        setPrereqView(null);
                        setPrereqHistory([]);
                        setHighlightedPrereqKey(null);
                        setUseFallback(true);
                        setFocusedUnmappedId(type.id);
                      }}
                      onDoubleClick={() => {
                        setSelection(null);
                        setPrereqView(null);
                        setPrereqHistory([]);
                        setHighlightedPrereqKey(null);
                        setUseFallback(true);
                        setFocusedUnmappedId(type.id);
                        openAddTopic(type.id);
                      }}
                      onContextMenu={(event) => {
                        event.preventDefault();
                        setSelection(null);
                        setPrereqView(null);
                        setPrereqHistory([]);
                        setHighlightedPrereqKey(null);
                        setUseFallback(true);
                        setFocusedUnmappedId(type.id);
                      }}
                    >
                      <span className="curriculum-topic-row-check" aria-hidden="true">
                        {isSelected ? "✓" : ""}
                      </span>
                      <span className="curriculum-topic-row-main">
                        <span className="curriculum-topic-row-name">
                          {formatQuestionTypeLabel(type)}
                        </span>
                        <span className="curriculum-topic-row-path">
                          {type.subcategory
                            ? `${type.category} — ${type.subcategory}`
                            : type.category}
                        </span>
                      </span>
                    </button>
                  );
                })}
              </div>
            )}
          </>
        )}
      </div>

      {prereqView && (
        <div className="curriculum-prereq-panel" aria-live="polite">
          <div className="curriculum-prereq-header">
            <div className="curriculum-prereq-header-row">
              <h3>Prerequisites</h3>
              <div className="curriculum-prereq-back-slot">
                {canGoBack ? (
                  <button
                    type="button"
                    className="curriculum-prereq-back"
                    onClick={handlePrereqBack}
                  >
                    ← Back
                  </button>
                ) : null}
              </div>
            </div>
            <p className="curriculum-prereq-current">
              {prereqViewChapterName ?? "Selected chapter"}
              {prereqViewTopic ? ` › ${prereqViewTopic.name}` : ""}
            </p>
          </div>

          {prerequisiteEntry && prerequisiteEntry.requires.length > 0 ? (
            <div className="curriculum-prereq-section">
              <h4 className="curriculum-prereq-section-title">
                {prerequisiteEntry.topicId
                  ? "Required skills beforehand"
                  : "Required beforehand"}
              </h4>
              {prerequisiteEntry.reason ? (
                <p className="curriculum-prereq-reason">{prerequisiteEntry.reason}</p>
              ) : null}
              <ul className="curriculum-prereq-list">
                {prerequisiteEntry.requires.map((req) => {
                  const jump = findJumpTargetInChapter(
                    courses,
                    req.courseId,
                    req.chapterId,
                    req.topicId,
                  );
                  const courseName =
                    courses.find((course) => course.id === req.courseId)?.name ?? req.courseId;
                  const isHighlighted = highlightedPrereqKey === req.key;
                  return (
                    <li key={req.key}>
                      <button
                        type="button"
                        className={`curriculum-prereq-link${isHighlighted ? " is-selected" : ""}`}
                        disabled={!jump}
                        aria-pressed={isHighlighted}
                        onClick={() => handlePrerequisiteHighlight(req.key)}
                        onDoubleClick={() =>
                          handlePrerequisiteOpen(
                            req.courseId,
                            req.chapterId,
                            req.key,
                            req.topicId,
                          )
                        }
                        onContextMenu={(event) =>
                          openPrereqMenu(
                            event,
                            req.courseId,
                            req.chapterId,
                            req.key,
                            req.title,
                            {
                              topicId: req.topicId ?? jump?.topicId,
                              typeId: req.typeId ?? jump?.typeId,
                              canAdd: Boolean(jump?.hasGenerator && jump.typeId),
                            },
                          )
                        }
                      >
                        <span className="curriculum-prereq-link-title">{req.title}</span>
                        <span className="curriculum-prereq-link-path">
                          {courseName}
                          {jump?.hasGenerator ? " · ready" : jump ? " · browse" : ""}
                        </span>
                      </button>
                    </li>
                  );
                })}
              </ul>
            </div>
          ) : (
            <p className="curriculum-prereq-empty">
              No curated prerequisites for this chapter yet (it may be a foundation topic).
              {canGoBack ? " Use Back to return to the previous topic." : ""}
            </p>
          )}

          <p className="curriculum-prereq-hint">
            Single-click to highlight. Right-click for options. Double-click a ready topic to
            add it. Use Back to return.
          </p>
        </div>
      )}

      {prereqMenu ? (
        <>
          <button
            className="context-backdrop"
            type="button"
            aria-label="Close menu"
            onClick={closePrereqMenu}
          />
          <menu
            className="context-menu"
            style={{ top: prereqMenu.y, left: prereqMenu.x }}
            aria-label={`Options for ${prereqMenu.title}`}
          >
            <button
              type="button"
              disabled={!prereqMenu.canAdd}
              onClick={() => {
                if (prereqMenu.typeId) {
                  openAddTopic(prereqMenu.typeId);
                } else {
                  handlePrerequisiteOpen(
                    prereqMenu.courseId,
                    prereqMenu.chapterId,
                    prereqMenu.prereqKey,
                    prereqMenu.topicId,
                  );
                }
                closePrereqMenu();
              }}
            >
              Add topic…
            </button>
            <button
              type="button"
              onClick={() => {
                handlePrerequisiteDrill(
                  prereqMenu.courseId,
                  prereqMenu.chapterId,
                  prereqMenu.prereqKey,
                  prereqMenu.topicId,
                );
                closePrereqMenu();
              }}
            >
              Look into prerequisites
            </button>
          </menu>
        </>
      ) : null}
    </div>
  );
}
