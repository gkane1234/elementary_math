"use client";

import { useEffect, useRef } from "react";
import katex from "katex";
import { columnStartNumber, distributeToColumns } from "@/lib/columns";
import type { Question, QuestionSet } from "@/lib/types";

type WorksheetPreviewProps = {
  worksheet: QuestionSet | null;
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

function QuestionColumns({
  questions,
  columnCount,
}: {
  questions: Question[];
  columnCount: number;
}) {
  const columns = distributeToColumns(questions, columnCount);

  return (
    <div
      className="question-columns"
      style={{ gridTemplateColumns: `repeat(${columns.length}, minmax(0, 1fr))` }}
    >
      {columns.map((columnQuestions, columnIndex) => (
        <ol
          key={`column-${columnIndex}`}
          className="question-list"
          start={columnStartNumber(columns, columnIndex)}
        >
          {columnQuestions.map((question) => {
            const index = questions.findIndex((entry) => entry.id === question.id);
            return (
              <li key={question.id} value={index + 1}>
                <Latex content={question.prompt_latex} />
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

  return (
    <section className="panel preview" id="worksheet-preview">
      <header className="worksheet-header">
        <h2>{worksheet.title}</h2>
        <p className="worksheet-meta">Name: ________________________________ Date: ____________</p>
        {worksheet.instruction_latex && (
          <p className="worksheet-instruction">
            <Latex content={worksheet.instruction_latex} />
          </p>
        )}
      </header>

      <QuestionColumns questions={worksheet.questions} columnCount={columnCount} />

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
                      {question.answer_latex ? (
                        <Latex content={question.answer_latex} />
                      ) : (
                        "—"
                      )}
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
