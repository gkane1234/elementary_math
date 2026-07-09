"use client";

import { useEffect, useMemo, useState } from "react";
import {
  buildCurriculumPicker,
  findFirstTopicByTypeId,
  findTopicSelection,
  flattenTopicsForSearch,
  getDefaultSelection,
  getUnmappedTypes,
  topicStatusLabel,
  type CurriculumSelection,
  type PickerTopic,
} from "@/lib/curriculum-picker";
import { formatQuestionTypeLabel, groupQuestionTypes } from "@/lib/question-type-groups";
import type { QuestionTypeInfo } from "@/lib/types";

type CurriculumTopicPickerProps = {
  types: QuestionTypeInfo[];
  selectedTypeId: string;
  onTypeIdChange: (typeId: string) => void;
};

function topicOptionLabel(topic: PickerTopic): string {
  if (topic.status === "ready") return topic.name;
  return `${topic.name} (${topicStatusLabel(topic.status)})`;
}

export function CurriculumTopicPicker({
  types,
  selectedTypeId,
  onTypeIdChange,
}: CurriculumTopicPickerProps) {
  const courses = useMemo(() => buildCurriculumPicker(undefined, types), [types]);
  const searchIndex = useMemo(() => flattenTopicsForSearch(courses), [courses]);
  const unmappedTypes = useMemo(() => getUnmappedTypes(types, courses), [types, courses]);
  const unmappedGroups = useMemo(() => groupQuestionTypes(unmappedTypes), [unmappedTypes]);

  const [selection, setSelection] = useState<CurriculumSelection | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [useFallback, setUseFallback] = useState(false);

  const selectedCourse = courses.find((course) => course.id === selection?.courseId) ?? null;
  const selectedChapter =
    selectedCourse?.chapters.find((chapter) => chapter.id === selection?.chapterId) ?? null;
  const selectedTopic = selection ? findTopicSelection(courses, selection) : null;

  const searchResults = useMemo(() => {
    const query = searchQuery.trim().toLowerCase();
    if (!query) return [];
    return searchIndex
      .filter((entry) => entry.topic.name.toLowerCase().includes(query))
      .slice(0, 12);
  }, [searchIndex, searchQuery]);

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

  const handleCourseChange = (courseId: string) => {
    const course = courses.find((entry) => entry.id === courseId);
    const chapter = course?.chapters[0];
    const topic = chapter?.topics[0];
    if (!course || !chapter || !topic) return;
    applySelection({ courseId, chapterId: chapter.id, topicId: topic.id });
    setSearchQuery("");
  };

  const handleChapterChange = (chapterId: string) => {
    if (!selection) return;
    const chapter = selectedCourse?.chapters.find((entry) => entry.id === chapterId);
    const topic = chapter?.topics[0];
    if (!chapter || !topic) return;
    applySelection({ ...selection, chapterId, topicId: topic.id });
    setSearchQuery("");
  };

  const handleTopicChange = (topicId: string) => {
    if (!selection) return;
    applySelection({ ...selection, topicId });
    setSearchQuery("");
  };

  const handleSearchPick = (entry: (typeof searchResults)[number]) => {
    setSearchQuery("");
    setSelection({
      courseId: entry.courseId,
      chapterId: entry.chapterId,
      topicId: entry.topicId,
    });
    if (entry.topic.typeId && entry.topic.hasGenerator) {
      onTypeIdChange(entry.topic.typeId);
      setUseFallback(false);
    }
  };

  if (courses.length === 0) {
    return null;
  }

  return (
    <div className="curriculum-picker">
      <label className="field">
        <span>Search topics</span>
        <input
          type="search"
          placeholder="Filter by topic name…"
          value={searchQuery}
          onChange={(event) => setSearchQuery(event.target.value)}
        />
      </label>

      {searchQuery.trim() && (
        <ul className="curriculum-search-results">
          {searchResults.length === 0 ? (
            <li className="curriculum-search-empty">No topics match your search.</li>
          ) : (
            searchResults.map((entry) => (
              <li key={`${entry.courseId}-${entry.chapterId}-${entry.topicId}`}>
                <button
                  type="button"
                  className={`curriculum-search-option${entry.topic.hasGenerator ? "" : " is-disabled"}`}
                  disabled={!entry.topic.hasGenerator}
                  onClick={() => handleSearchPick(entry)}
                >
                  <span className="curriculum-search-topic">{entry.topic.name}</span>
                  <span className="curriculum-search-path">
                    {entry.courseName} › {entry.chapterName}
                  </span>
                  {!entry.topic.hasGenerator && (
                    <span className="topic-status-badge">{topicStatusLabel(entry.topic.status)}</span>
                  )}
                </button>
              </li>
            ))
          )}
        </ul>
      )}

      <div className="curriculum-picker-cascade">
        <label className="field">
          <span>Course</span>
          <select
            value={selection?.courseId ?? ""}
            onChange={(event) => handleCourseChange(event.target.value)}
          >
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
            value={selection?.chapterId ?? ""}
            onChange={(event) => handleChapterChange(event.target.value)}
            disabled={!selectedCourse}
          >
            {(selectedCourse?.chapters ?? []).map((chapter) => (
              <option key={chapter.id} value={chapter.id}>
                {chapter.name}
              </option>
            ))}
          </select>
        </label>

        <label className="field">
          <span>Topic</span>
          <select
            value={selection?.topicId ?? ""}
            onChange={(event) => handleTopicChange(event.target.value)}
            disabled={!selectedChapter}
          >
            {(selectedChapter?.topics ?? []).map((topic) => (
              <option key={topic.id} value={topic.id} disabled={!topic.hasGenerator}>
                {topicOptionLabel(topic)}
              </option>
            ))}
          </select>
        </label>
      </div>

      {selectedTopic && !selectedTopic.hasGenerator && (
        <p className="curriculum-topic-hint">
          This topic is not available for worksheet generation yet.
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
