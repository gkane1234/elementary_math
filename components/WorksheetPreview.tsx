"use client";

import { QuestionDiagramFromMetadata } from "@/components/QuestionDiagram";
import { QuestionGraphFromMetadata } from "@/components/QuestionGraph";
import { MultipleChoiceOptions } from "@/components/MultipleChoiceOptions";
import {
  InlineLatex,
  InstructionLatex,
  QuestionPrompt,
} from "@/components/QuestionPrompt";
import { columnStartNumber, distributeToColumns } from "@/lib/columns";
import type { Question, QuestionSet } from "@/lib/types";
import {
  correctChoiceLabel,
  getMultipleChoiceChoices,
} from "@/lib/multiple-choice";
import {
  groupQuestionsByInstruction,
  sharedHeaderInstruction,
  shouldShowSectionHeader,
} from "@/lib/worksheet";

type WorksheetPreviewProps = {
  worksheet: QuestionSet | null;
};

function questionInstruction(question: Question): string | null {
  const fromMeta = question.metadata?.instruction_latex;
  return typeof fromMeta === "string" ? fromMeta : null;
}

function QuestionColumns({
  questions,
  columnCount,
  startIndex = 0,
}: {
  questions: Question[];
  columnCount: number;
  startIndex?: number;
}) {
  const columns = distributeToColumns(questions, columnCount);

  return (
    <div
      className="question-columns"
      data-columns={columns.length}
      style={{ gridTemplateColumns: `repeat(${columns.length}, minmax(0, 1fr))` }}
    >
      {columns.map((columnQuestions, columnIndex) => (
        <ol
          key={`column-${startIndex}-${columnIndex}`}
          className="question-list"
          start={startIndex + columnStartNumber(columns, columnIndex)}
        >
          {columnQuestions.map((question) => {
            const index = startIndex + questions.findIndex((entry) => entry.id === question.id);
            const choices = getMultipleChoiceChoices(question.metadata);
            return (
              <li key={question.id} value={index + 1}>
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
  );
}

export function WorksheetPreview({ worksheet }: WorksheetPreviewProps) {
  if (!worksheet) {
    return (
      <section className="panel preview empty">
        <p>Generate a worksheet to preview it here.</p>
      </section>
    );
  }

  const showAnswers = worksheet.questions.some((question) => question.answer_latex);
  const columnCount = worksheet.columns ?? 1;
  const answerColumns = distributeToColumns(worksheet.questions, columnCount);
  const questionsWithInstruction = worksheet.questions.map((question) => ({
    ...question,
    instruction_latex: questionInstruction(question),
  }));
  const headerInstruction =
    worksheet.instruction_latex ?? sharedHeaderInstruction(questionsWithInstruction);
  const instructionGroups = groupQuestionsByInstruction(questionsWithInstruction);

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

      <div className="instruction-groups">
        {instructionGroups.map((group) => (
          <div key={`preview-group-${group.startIndex}`} className="instruction-group">
            {shouldShowSectionHeader(group.instruction, headerInstruction) && group.instruction && (
              <p className="worksheet-section-instruction">
                <InstructionLatex content={group.instruction} />
              </p>
            )}
            <QuestionColumns
              questions={group.questions}
              columnCount={columnCount}
              startIndex={group.startIndex}
            />
          </div>
        ))}
      </div>

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
                      ) : (
                        "—"
                      )}
                      <QuestionGraphFromMetadata metadata={question.metadata} variant="answer" />
                      <QuestionDiagramFromMetadata metadata={question.metadata} />
                    </li>
                  );
                })}
              </ol>
            ))}
          </div>
        </div>
      )}
    </section>
  );
}
