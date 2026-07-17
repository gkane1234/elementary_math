"use client";

import { CurriculumTopicPicker } from "@/components/CurriculumTopicPicker";
import type { QuestionTypeInfo } from "@/lib/types";

type AddTopicPanelProps = {
  types: QuestionTypeInfo[];
  /** Called when the user picks a ready topic from the browser. */
  onSelectType: (typeId: string) => void;
};

/** Full-side curriculum browser. Double-click a ready topic to open options. */
export function AddTopicPanel({ types, onSelectType }: AddTopicPanelProps) {
  if (types.length === 0) {
    return (
      <section className="panel topics-browser-panel topics-browser-panel-fill">
        <h2>Topics</h2>
        <p className="hint">Loading topics…</p>
      </section>
    );
  }

  return (
    <section className="panel topics-browser-panel topics-browser-panel-fill">
      <header className="topics-browser-header">
        <h2>Topics</h2>
        <p className="hint">
          Single-click a topic to select it and view prerequisites. Double-click a ready topic
          to add it. Right-click a prerequisite for add or browse options.
        </p>
      </header>
      <CurriculumTopicPicker
        types={types}
        selectedTypeId=""
        onTypeIdChange={(typeId) => {
          if (typeId) onSelectType(typeId);
        }}
      />
    </section>
  );
}
