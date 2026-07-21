"use client";

import { useEffect, useMemo, useState } from "react";
import { Modal } from "@/components/Modal";
import { TopicExamplePreview } from "@/components/TopicExamplePreview";
import { TopicPrerequisitesPanel } from "@/components/TopicPrerequisitesPanel";
import { TopicSettingsFields, topicSettingsFields } from "@/components/TopicSettingsFields";
import type { CurriculumSelection } from "@/lib/curriculum-picker";
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

type AddTopicModalProps = {
  open: boolean;
  types: QuestionTypeInfo[];
  sections: TopicSection[];
  /** When set, modal edits this existing section. */
  editingSectionId: string | null;
  /** When set (and not editing), modal adds a new section of this type. */
  addingTypeId: string | null;
  onClose: () => void;
  onSectionsChange: (sections: TopicSection[]) => void;
  /** Switch the modal to another ready topic (prerequisite drill-down). */
  onSwitchType?: (typeId: string) => void;
};

/** Topic options modal: add a new topic block or edit an existing one. */
export function AddTopicModal({
  open,
  types,
  sections,
  editingSectionId,
  addingTypeId,
  onClose,
  onSectionsChange,
  onSwitchType,
}: AddTopicModalProps) {
  const [count, setCount] = useState(5);
  const [values, setValues] = useState<Record<string, string | number | boolean>>({});
  const [browseSelection, setBrowseSelection] = useState<CurriculumSelection | null>(null);

  const editingSection = useMemo(
    () => sections.find((entry) => entry.id === editingSectionId) ?? null,
    [sections, editingSectionId],
  );

  const typeId = editingSection?.type_id ?? addingTypeId;
  const selectedType = useMemo(
    () => (typeId ? types.find((type) => type.id === typeId) ?? null : null),
    [types, typeId],
  );
  const selectedIsReady = Boolean(selectedType && !typeIsNotReady(selectedType));
  const isEditing = Boolean(editingSection);
  const isBrowsingOnly = Boolean(browseSelection);

  const fields = useMemo(
    () => topicSettingsFields(selectedType?.settings ?? []),
    [selectedType],
  );

  useEffect(() => {
    if (!open) {
      setBrowseSelection(null);
      return;
    }
    // Reset browse drill-down whenever the active type changes from outside.
    setBrowseSelection(null);
  }, [open, typeId]);

  useEffect(() => {
    if (!open || !selectedType) return;

    if (editingSection) {
      setCount(editingSection.count);
      setValues({ ...defaultTopicValues(selectedType), ...editingSection.settings });
      return;
    }

    setCount(5);
    setValues(defaultTopicValues(selectedType));
  }, [open, selectedType, editingSection]);

  const handleConfirm = () => {
    if (!selectedType || !selectedIsReady || isBrowsingOnly) return;

    if (editingSection) {
      onSectionsChange(
        sections.map((entry) =>
          entry.id === editingSection.id
            ? { ...entry, count, settings: values }
            : entry,
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

    onClose();
  };

  const handleNavigateToType = (nextTypeId: string) => {
    setBrowseSelection(null);
    onSwitchType?.(nextTypeId);
  };

  const modalOpen = open && Boolean(selectedType || browseSelection);
  const showExample =
    modalOpen && Boolean(selectedType) && selectedIsReady && !isBrowsingOnly;
  const title = isBrowsingOnly
    ? "Topic prerequisites"
    : isEditing
      ? "Edit topic block"
      : "Topic options";

  return (
    <Modal
      open={modalOpen}
      title={title}
      onClose={onClose}
      stickyFooter={
        showExample && selectedType ? (
          <TopicExamplePreview
            active
            typeId={selectedType.id}
            settings={values}
          />
        ) : null
      }
      footer={
        isBrowsingOnly ? (
          <button
            className="secondary"
            type="button"
            onClick={() => setBrowseSelection(null)}
          >
            Back to topic options
          </button>
        ) : (
          <button
            className="primary"
            type="button"
            onClick={handleConfirm}
            disabled={!selectedType || !selectedIsReady}
          >
            {isEditing ? "Save changes" : "Add to worksheet"}
          </button>
        )
      }
    >
      {selectedType && !isBrowsingOnly && (
        <>
          <p className="description">
            <strong>{selectedType.name}</strong>
            {selectedType.description ? ` — ${selectedType.description}` : null}
          </p>

          <label className="field">
            <span>Questions</span>
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
            typeId={selectedType.id}
            settingProfile={selectedType.setting_profile}
            onChange={(key, value) => setValues((current) => ({ ...current, [key]: value }))}
            onValuesChange={setValues}
          />
        </>
      )}

      <TopicPrerequisitesPanel
        types={types}
        typeId={isBrowsingOnly ? null : typeId}
        browseSelection={browseSelection}
        onNavigateToType={handleNavigateToType}
        onBrowseChapter={setBrowseSelection}
      />
    </Modal>
  );
}
