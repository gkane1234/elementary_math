"use client";

import { useEffect, useRef, useState, type DragEvent, type MouseEvent } from "react";
import katex from "katex";
import { QuestionContextMenu } from "@/components/QuestionContextMenu";
import { QuestionSettingsModal } from "@/components/QuestionSettingsModal";
import { columnStartNumber, distributeToColumns, insertAtIndex } from "@/lib/columns";
import { regenerateQuestion } from "@/lib/api";
import type { QuestionTypeInfo, WorksheetDraft, WorksheetQuestion } from "@/lib/types";
import {
  clampSpacing,
  removeQuestion,
  sharedHeaderInstruction,
  shouldShowInstruction,
  toWorksheetQuestion,
  updateQuestion,
} from "@/lib/worksheet";

type InteractiveWorksheetProps = {
  worksheet: WorksheetDraft | null;
  types: QuestionTypeInfo[];
  previewMode?: boolean;
  onChange: (worksheet: WorksheetDraft) => void;
  onError?: (message: string) => void;
};

type ContextMenuState = {
  x: number;
  y: number;
  questionId: string;
};

function Latex({ content }: { content: string }) {
  const ref = useRef<HTMLSpanElement>(null);

  useEffect(() => {
    if (!ref.current) return;
    katex.render(content, ref.current, {
      throwOnError: false,
      displayMode: false,
    });
  }, [content]);

  return <span ref={ref} />;
}

function allowDrop(event: DragEvent) {
  event.preventDefault();
  event.dataTransfer.dropEffect = "move";
}

type QuestionItemProps = {
  question: WorksheetQuestion;
  number: number;
  selected: boolean;
  showInstruction: boolean;
  dropBefore: boolean;
  dropAfter: boolean;
  dragging: boolean;
  onSelect: () => void;
  onContextMenu: (event: MouseEvent) => void;
  onDragStart: (event: DragEvent) => void;
  onDragEnd: () => void;
  onDragOver: (event: DragEvent) => void;
  onDrop: (event: DragEvent) => void;
};

function QuestionItem({
  question,
  number,
  selected,
  showInstruction,
  dropBefore,
  dropAfter,
  dragging,
  onSelect,
  onContextMenu,
  onDragStart,
  onDragEnd,
  onDragOver,
  onDrop,
}: QuestionItemProps) {
  return (
    <div
      className={`question-item interactive-only${selected ? " selected" : ""}${dragging ? " dragging" : ""}${dropBefore ? " drop-before" : ""}${dropAfter ? " drop-after" : ""}`}
      style={{ marginBottom: `${question.spacing * 2.25}rem` }}
      draggable
      onClick={onSelect}
      onContextMenu={onContextMenu}
      onDragStart={onDragStart}
      onDragEnd={onDragEnd}
      onDragOver={onDragOver}
      onDrop={onDrop}
    >
      <div className="question-item-row">
        <span className="drag-handle" aria-hidden="true">
          ⋮⋮
        </span>
        <div className="question-content">
          {showInstruction && question.instruction_latex && (
            <p className="question-instruction">
              <Latex content={question.instruction_latex} />
            </p>
          )}
          <span className="question-number">{number}.</span>
          <Latex content={question.prompt_latex} />
        </div>
      </div>
    </div>
  );
}

export function InteractiveWorksheet({
  worksheet,
  types,
  previewMode = false,
  onChange,
  onError,
}: InteractiveWorksheetProps) {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [dragIndex, setDragIndex] = useState<number | null>(null);
  const [dropIndex, setDropIndex] = useState<number | null>(null);
  const [contextMenu, setContextMenu] = useState<ContextMenuState | null>(null);
  const [settingsQuestionId, setSettingsQuestionId] = useState<string | null>(null);
  const [busyId, setBusyId] = useState<string | null>(null);

  if (!worksheet || worksheet.questions.length === 0) {
    return (
      <section className="panel preview empty">
        <p>Add topics and build a worksheet to start editing.</p>
        <p className="hint">Right-click a question to edit or regenerate. Drag to reorder.</p>
      </section>
    );
  }

  const columnCount = worksheet.columns;
  const columns = distributeToColumns(worksheet.questions, columnCount);
  const headerInstruction = sharedHeaderInstruction(worksheet.questions);
  const answerColumns = distributeToColumns(worksheet.questions, columnCount);
  const showAnswers = !previewMode && worksheet.questions.some((question) => question.answer_latex);
  const selectedQuestion = worksheet.questions.find((question) => question.id === selectedId) ?? null;
  const settingsQuestion = worksheet.questions.find((question) => question.id === settingsQuestionId) ?? null;

  const patchWorksheet = (questions: WorksheetQuestion[]) => {
    onChange({ ...worksheet, questions });
  };

  const handleDragOver = (event: DragEvent, index: number) => {
    allowDrop(event);
    const rect = event.currentTarget.getBoundingClientRect();
    const insertAfter = event.clientY > rect.top + rect.height * 0.55;
    setDropIndex(insertAfter ? index + 1 : index);
  };

  const handleDrop = (event: DragEvent) => {
    event.preventDefault();
    if (dragIndex === null || dropIndex === null) return;
    patchWorksheet(insertAtIndex(worksheet.questions, dragIndex, dropIndex));
    setDragIndex(null);
    setDropIndex(null);
  };

  const handleRegenerate = async (questionId: string) => {
    const question = worksheet.questions.find((entry) => entry.id === questionId);
    if (!question) return;

    setBusyId(questionId);
    setContextMenu(null);
    try {
      const regenerated = await regenerateQuestion({
        type_id: question.topic,
        settings: question.generation_settings,
      });
      const next = toWorksheetQuestion(regenerated);
      patchWorksheet(
        updateQuestion(worksheet.questions, questionId, (current) => ({
          ...next,
          id: current.id,
          spacing: current.spacing,
          sectionId: current.sectionId,
          generation_settings: current.generation_settings,
        })),
      );
    } catch (err) {
      onError?.(err instanceof Error ? err.message : "Failed to regenerate question");
    } finally {
      setBusyId(null);
    }
  };

  const handleSpacing = (questionId: string, delta: number) => {
    patchWorksheet(
      updateQuestion(worksheet.questions, questionId, (question) => ({
        ...question,
        spacing: clampSpacing(question.spacing + delta),
      })),
    );
    setContextMenu(null);
  };

  const handleRemove = (questionId: string) => {
    patchWorksheet(removeQuestion(worksheet.questions, questionId));
    setContextMenu(null);
    if (selectedId === questionId) setSelectedId(null);
  };

  return (
    <section className="panel preview" id="worksheet-preview">
      <header className="worksheet-header">
        <h2>{worksheet.title}</h2>
        <p className="worksheet-meta">Name: ________________________________ Date: ____________</p>
        {headerInstruction && (
          <p className="worksheet-instruction">
            <Latex content={headerInstruction} />
          </p>
        )}
      </header>

      <p className="interactive-hint interactive-only">
        Drag a question card to reorder. Right-click for settings, regenerate, or spacing.
      </p>

      <div
        className="question-grid interactive-only"
        style={{
          gridTemplateColumns: `repeat(${columnCount}, minmax(0, 1fr))`,
        }}
        onDragOver={allowDrop}
        onDrop={handleDrop}
      >
        {worksheet.questions.map((question, index) => {
          const previous = index > 0 ? worksheet.questions[index - 1] : null;
          return (
            <QuestionItem
              key={question.id}
              question={question}
              number={index + 1}
              selected={selectedId === question.id}
              showInstruction={shouldShowInstruction(question, previous, headerInstruction)}
              dropBefore={dropIndex === index}
              dropAfter={dropIndex === index + 1}
              dragging={dragIndex === index}
              onSelect={() => setSelectedId(question.id)}
              onContextMenu={(event) => {
                event.preventDefault();
                setSelectedId(question.id);
                setContextMenu({
                  x: event.clientX,
                  y: event.clientY,
                  questionId: question.id,
                });
              }}
              onDragStart={(event) => {
                event.dataTransfer.effectAllowed = "move";
                event.dataTransfer.setData("text/plain", question.id);
                setDragIndex(index);
              }}
              onDragEnd={() => {
                setDragIndex(null);
                setDropIndex(null);
              }}
              onDragOver={(event) => handleDragOver(event, index)}
              onDrop={handleDrop}
            />
          );
        })}
      </div>

      <div
        className="question-columns print-only"
        style={{ gridTemplateColumns: `repeat(${columns.length}, minmax(0, 1fr))` }}
      >
        {columns.map((columnQuestions, columnIndex) => (
          <ol
            key={`print-column-${columnIndex}`}
            className="question-list"
            start={columnStartNumber(columns, columnIndex)}
          >
            {columnQuestions.map((question) => {
              const index = worksheet.questions.findIndex((entry) => entry.id === question.id);
              const previous = index > 0 ? worksheet.questions[index - 1] : null;
              return (
                <li
                  key={`print-${question.id}`}
                  value={index + 1}
                  style={{ marginBottom: `${question.spacing * 2.25}rem` }}
                >
                  {shouldShowInstruction(question, previous, headerInstruction) && question.instruction_latex && (
                    <p className="question-instruction">
                      <Latex content={question.instruction_latex} />
                    </p>
                  )}
                  <Latex content={question.prompt_latex} />
                </li>
              );
            })}
          </ol>
        ))}
      </div>

      {selectedQuestion && (
        <div className="selection-toolbar interactive-only">
          <span>Question {worksheet.questions.findIndex((q) => q.id === selectedQuestion.id) + 1}</span>
          <button type="button" onClick={() => setSettingsQuestionId(selectedQuestion.id)}>
            Edit settings
          </button>
          <button type="button" onClick={() => handleRegenerate(selectedQuestion.id)} disabled={busyId === selectedQuestion.id}>
            Regenerate
          </button>
          <button type="button" onClick={() => handleSpacing(selectedQuestion.id, 0.25)}>
            More space
          </button>
          <button type="button" onClick={() => handleSpacing(selectedQuestion.id, -0.25)}>
            Less space
          </button>
          <button type="button" onClick={() => handleRemove(selectedQuestion.id)}>
            Remove
          </button>
        </div>
      )}

      {showAnswers && (
        <div className="answer-key page-break">
          <h3>Answer Key</h3>
          <div
            className="question-columns"
            style={{ gridTemplateColumns: `repeat(${answerColumns.length}, minmax(0, 1fr))` }}
          >
            {answerColumns.map((columnQuestions, columnIndex) => (
              <ol
                key={`answer-column-${columnIndex}`}
                className="question-list answer-list"
                start={columnStartNumber(answerColumns, columnIndex)}
              >
                {columnQuestions.map((question) => {
                  const index = worksheet.questions.findIndex((entry) => entry.id === question.id);
                  return (
                    <li key={`${question.id}-answer`} value={index + 1}>
                      {question.answer_latex ? <Latex content={question.answer_latex} /> : "—"}
                    </li>
                  );
                })}
              </ol>
            ))}
          </div>
        </div>
      )}

      {contextMenu && (
        <QuestionContextMenu
          x={contextMenu.x}
          y={contextMenu.y}
          onClose={() => setContextMenu(null)}
          onEditSettings={() => {
            setSettingsQuestionId(contextMenu.questionId);
            setContextMenu(null);
          }}
          onRegenerate={() => handleRegenerate(contextMenu.questionId)}
          onIncreaseSpace={() => handleSpacing(contextMenu.questionId, 0.25)}
          onDecreaseSpace={() => handleSpacing(contextMenu.questionId, -0.25)}
          onRemove={() => handleRemove(contextMenu.questionId)}
        />
      )}

      <QuestionSettingsModal
        open={settingsQuestionId !== null}
        question={settingsQuestion}
        types={types}
        onClose={() => setSettingsQuestionId(null)}
        onSave={(updated) => {
          patchWorksheet(
            updateQuestion(worksheet.questions, updated.id, () => updated),
          );
        }}
      />
    </section>
  );
}
