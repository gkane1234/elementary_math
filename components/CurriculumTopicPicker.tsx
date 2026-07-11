"use client";

import { useEffect, useMemo, useState } from "react";
import {
  buildCurriculumPicker,
  filterTopics,
  findFirstTopicByTypeId,
  findTopicSelection,
  getDefaultSelection,
  getUnmappedTypes,
  topicStatusLabel,
  type CurriculumSelection,
  type FlatTopicSearchResult,
} from "@/lib/curriculum-picker";
import { formatQuestionTypeLabel, groupQuestionTypes } from "@/lib/question-type-groups";
import type { QuestionTypeInfo } from "@/lib/types";

type CurriculumTopicPickerProps = {
  types: QuestionTypeInfo[];
  selectedTypeId: string;
  onTypeIdChange: (typeId: string) => void;
};

export function CurriculumTopicPicker({
  types,
  selectedTypeId,
  onTypeIdChange,
}: CurriculumTopicPickerProps) {
  const courses = useMemo(() => buildCurriculumPicker(undefined, types), [types]);
  const unmappedTypes = useMemo(() => getUnmappedTypes(types, courses), [types, courses]);
  const unmappedGroups = useMemo(() => groupQuestionTypes(unmappedTypes), [unmappedTypes]);

  const [selection, setSelection] = useState<CurriculumSelection | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [filterCourseId, setFilterCourseId] = useState("");
  const [filterChapterId, setFilterChapterId] = useState("");
  // Default to Ready-only so diagram / unfinished topics are not listed as usable.
  const [readyOnly, setReadyOnly] = useState(true);
  const [useFallback, setUseFallback] = useState(false);

  const selectedTopic = selection ? findTopicSelection(courses, selection) : null;

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

  useEffect(() => {
    if (types.length === 0) return;

    const mapped = findFirstTopicByTypeId(courses, selectedTypeId);
    if (mapped) {
      setSelection((current) => {
        if (current) {
          const currentTopic = findTopicSelection(courses, current);
          if (currentTopic?.typeId === selectedTypeId) {
            return current;
          }
        }
        return {
          courseId: mapped.courseId,
          chapterId: mapped.chapterId,
          topicId: mapped.topicId,
        };
      });
      setUseFallback(false);
      return;
    }

    if (selectedTypeId && unmappedTypes.some((type) => type.id === selectedTypeId)) {
      setUseFallback(true);
      return;
    }

    setSelection((current) => current ?? getDefaultSelection(courses, selectedTypeId));
    setUseFallback(false);
  }, [courses, selectedTypeId, types.length, unmappedTypes]);

  const applySelection = (next: CurriculumSelection) => {
    setSelection(next);
    const topic = findTopicSelection(courses, next);
    if (topic?.typeId && topic.hasGenerator) {
      onTypeIdChange(topic.typeId);
      setUseFallback(false);
      return;
    }
    onTypeIdChange("");
  };

  const handleListPick = (entry: FlatTopicSearchResult) => {
    if (!entry.topic.hasGenerator) return;
    applySelection({
      courseId: entry.courseId,
      chapterId: entry.chapterId,
      topicId: entry.topicId,
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
      return;
    }
    setFilterChapterId(chapterId);
  };

  if (courses.length === 0) {
    return null;
  }

  return (
    <div className="curriculum-picker">
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
          <select value={filterCourseId} onChange={(event) => handleFilterCourseChange(event.target.value)}>
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

      <div className="curriculum-topic-list" role="listbox" aria-label="Topics">
        {filteredTopics.length === 0 ? (
          <p className="curriculum-topic-list-empty">No topics match your search or filters.</p>
        ) : (
          filteredTopics.map((entry) => {
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
                  entry.topic.hasGenerator ? "" : " is-disabled"
                }`}
                disabled={!entry.topic.hasGenerator}
                onClick={() => handleListPick(entry)}
              >
                <span className="curriculum-topic-row-check" aria-hidden="true">
                  {isSelected ? "✓" : ""}
                </span>
                <span className="curriculum-topic-row-main">
                  <span className="curriculum-topic-row-name">{entry.topic.name}</span>
                  <span className="curriculum-topic-row-path">
                    {entry.courseName} › {entry.chapterName}
                  </span>
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
          })
        )}
      </div>

      {selectedTopic && !selectedTopic.hasGenerator && (
        <p className="curriculum-topic-hint">
          This topic is Coming soon — diagrams or a matching generator are not available yet.
        </p>
      )}

      {unmappedTypes.length > 0 && (
        <details className="curriculum-fallback" open={useFallback}>
          <summary>Other question types ({unmappedTypes.length})</summary>
          <label className="field">
            <span>Type not listed in curriculum</span>
            <select
              value={useFallback ? selectedTypeId : ""}
              onChange={(event) => {
                setUseFallback(true);
                onTypeIdChange(event.target.value);
              }}
            >
              <option value="" disabled>
                Select a type…
              </option>
              {unmappedGroups.map((group) => (
                <optgroup key={group.label} label={group.label}>
                  {group.types.map((type) => (
                    <option key={type.id} value={type.id}>
                      {formatQuestionTypeLabel(type)}
                    </option>
                  ))}
                </optgroup>
              ))}
            </select>
          </label>
        </details>
      )}
    </div>
  );
}
