"use client";

import { useEffect, useMemo, useState } from "react";
import { Modal } from "@/components/Modal";
import { TopicSettingsFields, topicSettingsFields } from "@/components/TopicSettingsFields";
import { TopicSectionList, WorksheetPlanOutline } from "@/components/TopicSectionList";
import { CurriculumTopicPicker } from "@/components/CurriculumTopicPicker";
import { buildCurriculumPicker, findTopicSelection, getDefaultSelection } from "@/lib/curriculum-picker";
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

type AddTopicModalProps = {
  open: boolean;
  types: QuestionTypeInfo[];
  sections: TopicSection[];
  editingSectionId?: string | null;
  onClose: () => void;
  onSectionsChange: (sections: TopicSection[]) => void;
  onEditingSectionIdChange?: (sectionId: string | null) => void;
};

export function AddTopicModal({
  open,
  types,
  sections,
  editingSectionId: editingSectionIdProp = null,
  onClose,
  onSectionsChange,
  onEditingSectionIdChange,
}: AddTopicModalProps) {
  const [selectedTypeId, setSelectedTypeId] = useState(types[0]?.id ?? "");
  const [count, setCount] = useState(5);
  const [values, setValues] = useState<Record<string, string | number | boolean>>({});
  const [editingSectionId, setEditingSectionId] = useState<string | null>(null);

  const activeEditingId = editingSectionIdProp ?? editingSectionId;

  const selectedType = useMemo(
    () => types.find((type) => type.id === selectedTypeId) ?? null,
    [types, selectedTypeId],
  );

  const fields = useMemo(
    () => topicSettingsFields(selectedType?.settings ?? []),
    [selectedType],
  );

  const totalPlanned = sections.reduce((sum, section) => sum + section.count, 0);

  const setEditing = (sectionId: string | null) => {
    setEditingSectionId(sectionId);
    onEditingSectionIdChange?.(sectionId);
  };

  useEffect(() => {
    if (!open) return;
    if (types.length > 0 && !selectedTypeId) {
      const courses = buildCurriculumPicker(undefined, types);
      const defaultSelection = getDefaultSelection(courses);
      const defaultTypeId =
        (defaultSelection && findTopicSelection(courses, defaultSelection)?.typeId) ?? types[0]?.id ?? "";
      if (defaultTypeId) setSelectedTypeId(defaultTypeId);
    }
  }, [open, types, selectedTypeId]);

  useEffect(() => {
    if (!open || !editingSectionIdProp) return;
    const section = sections.find((entry) => entry.id === editingSectionIdProp);
    if (!section) return;
    const type = types.find((entry) => entry.id === section.type_id) ?? null;
    setEditingSectionId(section.id);
    setSelectedTypeId(section.type_id);
    setCount(section.count);
    setValues({ ...defaultTopicValues(type), ...section.settings });
  }, [open, editingSectionIdProp, sections, types]);

  useEffect(() => {
    if (!open || activeEditingId) return;
    setValues(defaultTopicValues(selectedType));
  }, [open, selectedType, activeEditingId]);

  const resetForm = () => {
    setEditing(null);
    setCount(5);
    setValues(defaultTopicValues(selectedType));
  };

  const applySectionChange = () => {
    if (!selectedType) return false;

    if (activeEditingId) {
      onSectionsChange(
        sections.map((section) =>
          section.id === activeEditingId
            ? { ...section, type_id: selectedType.id, count, settings: values }
            : section,
        ),
      );
    } else {
      onSectionsChange([
        ...sections,
        {
          id: createSectionId(),
          type_id: selectedType.id,
          count,
          settings: values,
        },
      ]);
    }

    return true;
  };

  const handleAddAndContinue = () => {
    if (!applySectionChange()) return;
    resetForm();
  };

  const handleAddAndClose = () => {
    if (!applySectionChange()) return;
    resetForm();
    onClose();
  };

  const handleEditSection = (section: TopicSection) => {
    const type = types.find((entry) => entry.id === section.type_id) ?? null;
    setEditing(section.id);
    setSelectedTypeId(section.type_id);
    setCount(section.count);
    setValues({ ...defaultTopicValues(type), ...section.settings });
  };

  const handleRemove = (sectionId: string) => {
    onSectionsChange(sections.filter((section) => section.id !== sectionId));
    if (activeEditingId === sectionId) {
      resetForm();
    }
  };

  return (
    <Modal
      open={open}
      title={activeEditingId ? "Edit topic block" : "Add question topics"}
      onClose={() => {
        resetForm();
        onClose();
      }}
      footer={
        <>
          {!activeEditingId && (
            <button className="secondary" type="button" onClick={handleAddAndContinue} disabled={!selectedType}>
              Add and continue
            </button>
          )}
          <button className="primary" type="button" onClick={handleAddAndClose} disabled={!selectedType}>
            {activeEditingId ? "Save changes" : "Add to worksheet plan"}
          </button>
        </>
      }
    >
      <WorksheetPlanOutline sections={sections} types={types} totalPlanned={totalPlanned} />

      {sections.length > 0 && (
        <TopicSectionList
          sections={sections}
          types={types}
          onSectionsChange={onSectionsChange}
          onEditSection={handleEditSection}
          onRemoveSection={handleRemove}
        />
      )}

      <hr className="modal-divider" />

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
    </Modal>
  );
}
