"use client";

import { useEffect, useMemo, useState } from "react";
import { Modal } from "@/components/Modal";
import { TopicSettingsFields, topicSettingsFields } from "@/components/TopicSettingsFields";
import { regenerateQuestion } from "@/lib/api";
import type { QuestionTypeInfo, WorksheetQuestion } from "@/lib/types";
import { toWorksheetQuestion } from "@/lib/worksheet";

type QuestionSettingsModalProps = {
  open: boolean;
  question: WorksheetQuestion | null;
  types: QuestionTypeInfo[];
  onClose: () => void;
  onSave: (question: WorksheetQuestion) => void;
};

export function QuestionSettingsModal({
  open,
  question,
  types,
  onClose,
  onSave,
}: QuestionSettingsModalProps) {
  const [values, setValues] = useState<Record<string, string | number | boolean>>({});
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const questionType = useMemo(
    () => types.find((type) => type.id === question?.topic) ?? null,
    [types, question],
  );

  const fields = useMemo(
    () => topicSettingsFields(questionType?.settings ?? []),
    [questionType],
  );

  useEffect(() => {
    if (!open || !question) return;
    setValues({ ...question.generation_settings } as Record<string, string | number | boolean>);
    setError(null);
  }, [open, question]);

  const handleSave = async () => {
    if (!question) return;
    setSaving(true);
    setError(null);
    try {
      const regenerated = await regenerateQuestion({
        type_id: question.topic,
        settings: values,
      });
      const next = toWorksheetQuestion(regenerated);
      onSave({
        ...next,
        id: question.id,
        spacing: question.spacing,
        sectionId: question.sectionId,
        generation_settings: values,
        instruction_latex: questionType?.instruction_latex ?? next.instruction_latex,
      });
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update question");
    } finally {
      setSaving(false);
    }
  };

  return (
    <Modal
      open={open}
      title="Edit question settings"
      onClose={onClose}
      footer={
        <button className="primary" type="button" onClick={handleSave} disabled={saving || !question}>
          {saving ? "Regenerating..." : "Save and regenerate"}
        </button>
      }
    >
      {questionType && <p className="description">{questionType.name}</p>}
      <TopicSettingsFields
        fields={fields}
        values={values}
        typeId={questionType?.id}
        settingProfile={questionType?.setting_profile}
        onChange={(key, value) => setValues((current) => ({ ...current, [key]: value }))}
        onValuesChange={setValues}
      />
      {error && <p className="error">{error}</p>}
    </Modal>
  );
}
