"use client";

import { useState, type DragEvent, type MouseEvent } from "react";
import { QuestionDiagramFromMetadata } from "@/components/QuestionDiagram";
import { QuestionGraphFromMetadata } from "@/components/QuestionGraph";
import { hasAnswerDiagram } from "@/lib/diagram-metadata";
import { MultipleChoiceOptions } from "@/components/MultipleChoiceOptions";
import {
  InlineLatex,
  InstructionLatex,
  QuestionPrompt,
} from "@/components/QuestionPrompt";
import { QuestionContextMenu } from "@/components/QuestionContextMenu";
import { QuestionSettingsModal } from "@/components/QuestionSettingsModal";
import { columnStartNumber, distributeToColumns, insertAtIndex } from "@/lib/columns";
import { regenerateQuestion } from "@/lib/api";
import {
  correctChoiceLabel,
  getMultipleChoiceChoices,
} from "@/lib/multiple-choice";
import type { QuestionTypeInfo, WorksheetDraft, WorksheetQuestion } from "@/lib/types";
import {
  clampSpacing,
  groupQuestionsByInstruction,
  removeQuestion,
  sharedHeaderInstruction,
  shouldShowSectionHeader,
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

function allowDrop(event: DragEvent) {
  event.preventDefault();
  event.dataTransfer.dropEffect = "move";
}

type QuestionItemProps = {
  question: WorksheetQuestion;
  number: number;
  selected: boolean;
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
  const choices = getMultipleChoiceChoices(question.metadata);

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
          <div className="question-prompt-row">
            <span className="question-number">{number}.</span>
            <QuestionPrompt content={question.prompt_latex} />
          </div>
          <QuestionGraphFromMetadata metadata={question.metadata} />
          <QuestionDiagramFromMetadata metadata={question.metadata} />
          {choices ? (
            <MultipleChoiceOptions
              choices={choices}
              questionId={question.id}
              interactive
            />
          ) : null}
        </div>
      </div>
    </div>
  );
}

function SectionInstruction({ content }: { content: string }) {
  return (
    <p className="worksheet-section-instruction">
      <InstructionLatex content={content} />
    </p>
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
  const headerInstruction = sharedHeaderInstruction(worksheet.questions);
  const instructionGroups = groupQuestionsByInstruction(worksheet.questions);
  const answerColumns = distributeToColumns(worksheet.questions, columnCount);
  const showAnswers =
    !previewMode &&
    worksheet.questions.some(
      (question) =>
        Boolean(question.answer_latex) || hasAnswerDiagram(question.metadata),
    );
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
            <InstructionLatex content={headerInstruction} />
          </p>
        )}
      </header>

      <p className="interactive-hint interactive-only">
        Drag a question card to reorder. Right-click for settings, regenerate, or spacing.
      </p>

      <div
        className="question-grid interactive-only"
        data-columns={columnCount}
        style={{
          gridTemplateColumns: `repeat(${columnCount}, minmax(0, 1fr))`,
        }}
        onDragOver={allowDrop}
        onDrop={handleDrop}
      >
        {instructionGroups.flatMap((group) => {
          const header =
            shouldShowSectionHeader(group.instruction, headerInstruction) && group.instruction ? (
              <div
                key={`section-${group.startIndex}`}
                className="worksheet-section-header"
              >
                <SectionInstruction content={group.instruction} />
              </div>
            ) : null;

          const items = group.questions.map((question, groupIndex) => {
            const index = group.startIndex + groupIndex;
            return (
              <QuestionItem
                key={question.id}
                question={question}
                number={index + 1}
                selected={selectedId === question.id}
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
          });

          return header ? [header, ...items] : items;
        })}
      </div>

      <div className="print-only instruction-groups">
        {instructionGroups.map((group) => {
          const columns = distributeToColumns(group.questions, columnCount);
          return (
            <div key={`print-group-${group.startIndex}`} className="instruction-group">
              {shouldShowSectionHeader(group.instruction, headerInstruction) && group.instruction && (
                <SectionInstruction content={group.instruction} />
              )}
              <div
                className="question-columns"
                data-columns={columns.length}
                style={{ gridTemplateColumns: `repeat(${columns.length}, minmax(0, 1fr))` }}
              >
                {columns.map((columnQuestions, columnIndex) => (
                  <ol
                    key={`print-column-${group.startIndex}-${columnIndex}`}
                    className="question-list"
                    start={group.startIndex + columnStartNumber(columns, columnIndex)}
                  >
                    {columnQuestions.map((question) => {
                      const index = worksheet.questions.findIndex((entry) => entry.id === question.id);
                      const choices = getMultipleChoiceChoices(question.metadata);
                      return (
                        <li
                          key={`print-${question.id}`}
                          value={index + 1}
                          style={{ marginBottom: `${question.spacing * 2.25}rem` }}
                        >
                          <QuestionPrompt content={question.prompt_latex} />
                          <QuestionGraphFromMetadata metadata={question.metadata} />
                          <QuestionDiagramFromMetadata metadata={question.metadata} />
                          {choices ? (
                            <MultipleChoiceOptions
                              choices={choices}
                              questionId={question.id}
                            />
                          ) : null}
                        </li>
                      );
                    })}
                  </ol>
                ))}
              </div>
            </div>
          );
        })}
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
            data-columns={answerColumns.length}
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
                  const choices = getMultipleChoiceChoices(question.metadata);
                  const letter = choices ? correctChoiceLabel(choices) : null;
                  return (
                    <li key={`${question.id}-answer`} value={index + 1}>
                      {letter ? (
                        <span>
                          {letter}
                          {question.answer_latex ? (
                            <>
                              {") "}
                              <InlineLatex content={question.answer_latex} />
                            </>
                          ) : null}
                        </span>
                      ) : question.answer_latex ? (
                        <InlineLatex content={question.answer_latex} />
                      ) : hasAnswerDiagram(question.metadata) ? null : (
                        "—"
                      )}
                      <QuestionGraphFromMetadata metadata={question.metadata} variant="answer" />
                      <QuestionDiagramFromMetadata metadata={question.metadata} variant="answer" />
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
