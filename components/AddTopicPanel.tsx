"use client";

import { useEffect, useMemo, useState } from "react";
import { TopicSettingsFields, topicSettingsFields } from "@/components/TopicSettingsFields";
import { CurriculumTopicPicker } from "@/components/CurriculumTopicPicker";
import {
  buildCurriculumPicker,
  findFirstTopicByTypeId,
  findTopicSelection,
  getDefaultSelection,
} from "@/lib/curriculum-picker";
import { typeIsNotReady } from "@/lib/diagram-readiness";
import type { QuestionTypeInfo, TopicSection } from "@/lib/types";

function defaultTopicValues(type: QuestionTypeInfo | null): Record<string, string | number | boolean> {
  if (!type) return {};
  return Object.fromEntries(
    topicSettingsFields(type.settings).map((field) => [field.key, field.default]),
  );
}

function createSectionId(): string {
  return `section-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
}

function firstReadyTypeId(types: QuestionTypeInfo[]): string {
  const courses = buildCurriculumPicker(undefined, types);
  const defaultSelection = getDefaultSelection(courses);
  const fromCurriculum =
    defaultSelection && findTopicSelection(courses, defaultSelection)?.typeId;
  if (fromCurriculum) return fromCurriculum;
  return types.find((type) => !typeIsNotReady(type))?.id ?? "";
}

type AddTopicPanelProps = {
  types: QuestionTypeInfo[];
  sections: TopicSection[];
  onSectionsChange: (sections: TopicSection[]) => void;
};

export function AddTopicPanel({ types, sections, onSectionsChange }: AddTopicPanelProps) {
  const [selectedTypeId, setSelectedTypeId] = useState("");
  const [count, setCount] = useState(5);
  const [values, setValues] = useState<Record<string, string | number | boolean>>({});

  const courses = useMemo(() => buildCurriculumPicker(undefined, types), [types]);
  const selectedType = useMemo(
    () => types.find((type) => type.id === selectedTypeId) ?? null,
    [types, selectedTypeId],
  );
  const selectedIsReady = useMemo(() => {
    if (!selectedType || typeIsNotReady(selectedType)) return false;
    const mapped = findFirstTopicByTypeId(courses, selectedType.id);
    if (mapped) return mapped.topic.hasGenerator;
    return true;
  }, [courses, selectedType]);

  const fields = useMemo(
    () => topicSettingsFields(selectedType?.settings ?? []),
    [selectedType],
  );

  useEffect(() => {
    if (types.length === 0) return;
    if (!selectedTypeId || !selectedIsReady) {
      const defaultTypeId = firstReadyTypeId(types);
      if (defaultTypeId && defaultTypeId !== selectedTypeId) {
        setSelectedTypeId(defaultTypeId);
      }
    }
  }, [types, selectedTypeId, selectedIsReady]);

  useEffect(() => {
    setValues(defaultTopicValues(selectedType));
  }, [selectedType]);

  if (types.length === 0) {
    return null;
  }

  const handleAdd = () => {
    if (!selectedType || !selectedIsReady) return;
    onSectionsChange([
      ...sections,
      {
        id: createSectionId(),
        type_id: selectedType.id,
        count,
        settings: values,
      },
    ]);
  };

  const handleRemove = (sectionId: string) => {
    onSectionsChange(sections.filter((section) => section.id !== sectionId));
  };

  return (
    <section className="panel">
      <h2>Add question topics</h2>

      <CurriculumTopicPicker
        types={types}
        selectedTypeId={selectedTypeId}
        onTypeIdChange={setSelectedTypeId}
      />

      {selectedType && <p className="description">{selectedType.description}</p>}

      {selectedType && (
        <>
          <label className="field">
            <span>Questions to add</span>
            <input
              type="number"
              min={1}
              max={50}
              value={count}
              onChange={(event) => setCount(Number(event.target.value))}
            />
          </label>

          <TopicSettingsFields
            fields={fields}
            values={values}
            onChange={(key, value) => setValues((current) => ({ ...current, [key]: value }))}
          />
        </>
      )}

      <button
        className="secondary"
        type="button"
        onClick={handleAdd}
        disabled={!selectedType || !selectedIsReady}
      >
        Add to worksheet plan
      </button>

      {sections.length > 0 && (
        <ul className="section-queue">
          {sections.map((section) => {
            const type = types.find((entry) => entry.id === section.type_id);
            return (
              <li key={section.id}>
                <span>
                  {type?.name ?? section.type_id} × {section.count}
                </span>
                <button type="button" onClick={() => handleRemove(section.id)}>
                  Remove
                </button>
              </li>
            );
          })}
        </ul>
      )}
    </section>
  );
}
