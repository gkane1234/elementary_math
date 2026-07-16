"use client";

import { useState, type DragEvent, type MouseEvent } from "react";
import type { QuestionTypeInfo, TopicSection } from "@/lib/types";
import { moveSection } from "@/lib/sections";

type TopicSectionListProps = {
  sections: TopicSection[];
  types: QuestionTypeInfo[];
  onSectionsChange: (sections: TopicSection[]) => void;
  onEditSection: (section: TopicSection) => void;
  onRemoveSection?: (sectionId: string) => void;
  onDuplicateSection?: (section: TopicSection) => void;
  compact?: boolean;
};

function createSectionId(): string {
  return `section-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
}

export function duplicateTopicSection(section: TopicSection): TopicSection {
  return {
    ...section,
    id: createSectionId(),
    settings: { ...section.settings },
  };
}

function allowDrop(event: DragEvent) {
  event.preventDefault();
  event.dataTransfer.dropEffect = "move";
}

export function TopicSectionList({
  sections,
  types,
  onSectionsChange,
  onEditSection,
  onRemoveSection,
  onDuplicateSection,
  compact = false,
}: TopicSectionListProps) {
  const [dragIndex, setDragIndex] = useState<number | null>(null);
  const [dropIndex, setDropIndex] = useState<number | null>(null);
  const [contextMenu, setContextMenu] = useState<{
    x: number;
    y: number;
    sectionId: string;
  } | null>(null);

  if (sections.length === 0) {
    return <p className="plan-empty">No topics added yet.</p>;
  }

  const handleDragOver = (event: DragEvent, index: number) => {
    allowDrop(event);
    const rect = event.currentTarget.getBoundingClientRect();
    const insertAfter = event.clientY > rect.top + rect.height * 0.55;
    setDropIndex(insertAfter ? index + 1 : index);
  };

  const handleDrop = () => {
    if (dragIndex === null || dropIndex === null) return;
    onSectionsChange(moveSection(sections, dragIndex, dropIndex));
    setDragIndex(null);
    setDropIndex(null);
  };

  return (
    <>
      <ol className={`topic-section-list${compact ? " compact" : ""}`}>
        {sections.map((section, index) => {
          const type = types.find((entry) => entry.id === section.type_id);
          return (
            <li
              key={section.id}
              className={`topic-section-item${dragIndex === index ? " dragging" : ""}${dropIndex === index ? " drop-before" : ""}${dropIndex === index + 1 ? " drop-after" : ""}`}
              draggable={sections.length > 1}
              onDragStart={(event) => {
                event.dataTransfer.effectAllowed = "move";
                event.dataTransfer.setData("text/plain", section.id);
                setDragIndex(index);
              }}
              onDragEnd={() => {
                setDragIndex(null);
                setDropIndex(null);
              }}
              onDragOver={(event) => handleDragOver(event, index)}
              onDrop={(event) => {
                event.preventDefault();
                handleDrop();
              }}
              onContextMenu={(event: MouseEvent) => {
                event.preventDefault();
                setContextMenu({
                  x: event.clientX,
                  y: event.clientY,
                  sectionId: section.id,
                });
              }}
            >
              <span className="topic-drag-handle" aria-hidden="true">
                ⋮⋮
              </span>
              <button
                type="button"
                className="topic-section-label"
                onClick={() => onEditSection(section)}
              >
                <strong>{type?.name ?? section.type_id}</strong>
              </button>
              <span className="topic-section-count" title="Question count">
                {section.count}
              </span>
              {onRemoveSection && (
                <button
                  type="button"
                  className="topic-remove"
                  aria-label="Remove topic"
                  title="Remove topic"
                  onClick={() => onRemoveSection(section.id)}
                >
                  ×
                </button>
              )}
            </li>
          );
        })}
      </ol>

      {contextMenu && (
        <>
          <button
            className="context-backdrop"
            type="button"
            aria-label="Close menu"
            onClick={() => setContextMenu(null)}
          />
          <menu className="context-menu" style={{ top: contextMenu.y, left: contextMenu.x }}>
            <button
              type="button"
              onClick={() => {
                const section = sections.find((entry) => entry.id === contextMenu.sectionId);
                if (section) onEditSection(section);
                setContextMenu(null);
              }}
            >
              Edit settings...
            </button>
            <button
              type="button"
              onClick={() => {
                const section = sections.find((entry) => entry.id === contextMenu.sectionId);
                if (!section) {
                  setContextMenu(null);
                  return;
                }
                if (onDuplicateSection) {
                  onDuplicateSection(section);
                } else {
                  const index = sections.findIndex((entry) => entry.id === section.id);
                  const copy = duplicateTopicSection(section);
                  const next = [...sections];
                  next.splice(index + 1, 0, copy);
                  onSectionsChange(next);
                }
                setContextMenu(null);
              }}
            >
              Duplicate
            </button>
            {onRemoveSection && (
              <button
                type="button"
                className="danger"
                onClick={() => {
                  onRemoveSection(contextMenu.sectionId);
                  setContextMenu(null);
                }}
              >
                Remove topic
              </button>
            )}
          </menu>
        </>
      )}
    </>
  );
}

export function WorksheetPlanOutline({
  sections,
  types,
  totalPlanned,
}: {
  sections: TopicSection[];
  types: QuestionTypeInfo[];
  totalPlanned: number;
}) {
  if (sections.length === 0) {
    return (
      <div className="worksheet-plan-outline empty">
        <h3>Worksheet plan</h3>
        <p>No topics added yet.</p>
      </div>
    );
  }

  return (
    <div className="worksheet-plan-outline">
      <h3>Worksheet plan</h3>
      <p className="plan-summary">
        <strong>{totalPlanned}</strong> question{totalPlanned === 1 ? "" : "s"} total
      </p>
      <ol className="worksheet-plan-steps">
        {sections.map((section, index) => {
          const type = types.find((entry) => entry.id === section.type_id);
          return (
            <li key={section.id}>
              <span className="plan-step-index">{index + 1}.</span>
              <span>
                {type?.name ?? section.type_id} × {section.count}
              </span>
            </li>
          );
        })}
      </ol>
    </div>
  );
}
