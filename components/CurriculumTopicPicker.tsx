"use client";

import { useEffect, useMemo, useState } from "react";
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

  const [selection, setSelection] = useState<CurriculumSelection | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [filterCourseId, setFilterCourseId] = useState("");
  const [filterChapterId, setFilterChapterId] = useState("");
  const [readyOnly, setReadyOnly] = useState(true);
  const [useFallback, setUseFallback] = useState(false);

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
    () => getPrerequisitesForSelection(selection),
    [selection],
  );

  const selectedTopic = useMemo(
    () => (selection ? findTopicSelection(courses, selection) : null),
    [courses, selection],
  );

  const selectedChapterName = useMemo(() => {
    if (!selection) return null;
    const course = courses.find((entry) => entry.id === selection.courseId);
    return course?.chapters.find((entry) => entry.id === selection.chapterId)?.name ?? null;
  }, [courses, selection]);

  useEffect(() => {
    if (types.length === 0) return;

    const mapped = findFirstTopicByTypeId(courses, selectedTypeId);
    if (mapped) {
      setSelection({
        courseId: mapped.courseId,
        chapterId: mapped.chapterId,
        topicId: mapped.topicId,
      });
      setUseFallback(false);
      return;
    }

    if (selectedTypeId && unmappedTypes.some((type) => type.id === selectedTypeId)) {
      setSelection(null);
      setUseFallback(true);
      return;
    }

    if (!selectedTypeId) {
      setSelection(null);
      setUseFallback(false);
    }
  }, [courses, selectedTypeId, types.length, unmappedTypes]);

  const applySelection = (next: CurriculumSelection, updateType = true) => {
    setSelection(next);
    setFilterCourseId(next.courseId);
    setFilterChapterId(next.chapterId);
    setSearchQuery("");
    const topic = findTopicSelection(courses, next);
    if (!updateType) return;
    if (topic?.typeId && topic.hasGenerator) {
      onTypeIdChange(topic.typeId);
      setUseFallback(false);
      return;
    }
    onTypeIdChange("");
  };

  const handleListPick = (entry: FlatTopicSearchResult) => {
    // Allow browsing Coming soon / Preview topics to inspect prerequisites,
    // but only change the worksheet type when a generator is ready.
    applySelection(
      {
        courseId: entry.courseId,
        chapterId: entry.chapterId,
        topicId: entry.topicId,
      },
      entry.topic.hasGenerator,
    );
    setUseFallback(false);
  };

  const handlePrerequisiteJump = (courseId: string, chapterId: string) => {
    const target = findJumpTargetInChapter(courses, courseId, chapterId);
    if (!target) return;
    if (!target.hasGenerator) {
      setReadyOnly(false);
    }
    applySelection(
      {
        courseId: target.courseId,
        chapterId: target.chapterId,
        topicId: target.topicId,
      },
      target.hasGenerator,
    );
    setUseFallback(false);
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

      {selection && (
        <div className="curriculum-prereq-panel" aria-live="polite">
          <div className="curriculum-prereq-header">
            <h3>Prerequisites</h3>
            <p className="curriculum-prereq-current">
              {selectedChapterName ?? "Selected chapter"}
              {selectedTopic ? ` › ${selectedTopic.name}` : ""}
            </p>
          </div>
          {prerequisiteEntry && prerequisiteEntry.requires.length > 0 ? (
            <>
              {prerequisiteEntry.reason ? (
                <p className="curriculum-prereq-reason">{prerequisiteEntry.reason}</p>
              ) : null}
              <ul className="curriculum-prereq-list">
                {prerequisiteEntry.requires.map((req) => {
                  const jump = findJumpTargetInChapter(courses, req.courseId, req.chapterId);
                  const courseName =
                    courses.find((course) => course.id === req.courseId)?.name ?? req.courseId;
                  return (
                    <li key={req.key}>
                      <button
                        type="button"
                        className="curriculum-prereq-link"
                        disabled={!jump}
                        onClick={() => handlePrerequisiteJump(req.courseId, req.chapterId)}
                      >
                        <span className="curriculum-prereq-link-title">{req.title}</span>
                        <span className="curriculum-prereq-link-path">
                          {courseName}
                          {jump ? " · browse" : ""}
                        </span>
                      </button>
                    </li>
                  );
                })}
              </ul>
              <p className="curriculum-prereq-hint">
                Click a prerequisite to open that chapter and see its prerequisites.
              </p>
            </>
          ) : (
            <p className="curriculum-prereq-empty">
              No curated prerequisites for this chapter yet (it may be a foundation topic).
            </p>
          )}
        </div>
      )}

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
                      onClick={() => handleListPick(entry)}
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
                  const isSelected = useFallback && selectedTypeId === type.id;
                  return (
                    <button
                      key={type.id}
                      type="button"
                      role="option"
                      aria-selected={isSelected}
                      className={`curriculum-topic-row${isSelected ? " is-selected" : ""}`}
                      onClick={() => {
                        setSelection(null);
                        setUseFallback(true);
                        onTypeIdChange(type.id);
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
    </div>
  );
}
