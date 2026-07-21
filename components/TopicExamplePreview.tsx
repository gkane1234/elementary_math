"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { QuestionDiagramFromMetadata } from "@/components/QuestionDiagram";
import { QuestionGraphFromMetadata } from "@/components/QuestionGraph";
import { MultipleChoiceOptions } from "@/components/MultipleChoiceOptions";
import { InlineLatex, QuestionPrompt } from "@/components/QuestionPrompt";
import { regenerateQuestion } from "@/lib/api";
import { hasAnswerDiagram } from "@/lib/diagram-metadata";
import {
  correctChoiceLabel,
  getMultipleChoiceChoices,
} from "@/lib/multiple-choice";
import type { Question } from "@/lib/types";

const DEBOUNCE_MS = 350;

function isTypingTarget(target: EventTarget | null): boolean {
  if (!(target instanceof HTMLElement)) return false;
  const tag = target.tagName;
  if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return true;
  if (target.isContentEditable) return true;
  return Boolean(target.closest("[contenteditable='true']"));
}

function settingsKey(settings: Record<string, string | number | boolean>): string {
  return JSON.stringify(settings);
}

type TopicExamplePreviewProps = {
  active: boolean;
  typeId: string | null;
  settings: Record<string, string | number | boolean>;
};

/** Live sample question for the topic options modal (auto-refreshes; R regenerates). */
export function TopicExamplePreview({
  active,
  typeId,
  settings,
}: TopicExamplePreviewProps) {
  const [question, setQuestion] = useState<Question | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const requestIdRef = useRef(0);
  const settingsRef = useRef(settings);
  settingsRef.current = settings;
  const settingsSnapshot = settingsKey(settings);

  const loadExample = useCallback(async () => {
    if (!active || !typeId) return;

    const requestId = ++requestIdRef.current;
    setLoading(true);
    setError(null);

    try {
      const next = await regenerateQuestion({
        type_id: typeId,
        settings: {
          ...settingsRef.current,
          count: 1,
          include_answer_key: true,
        },
      });
      if (requestId !== requestIdRef.current) return;
      setQuestion(next);
    } catch (err) {
      if (requestId !== requestIdRef.current) return;
      setQuestion(null);
      setError(err instanceof Error ? err.message : "Failed to generate example");
    } finally {
      if (requestId === requestIdRef.current) {
        setLoading(false);
      }
    }
  }, [active, typeId]);

  useEffect(() => {
    if (!active || !typeId) {
      requestIdRef.current += 1;
      setQuestion(null);
      setError(null);
      setLoading(false);
      return;
    }

    const timer = window.setTimeout(() => {
      void loadExample();
    }, DEBOUNCE_MS);

    return () => window.clearTimeout(timer);
  }, [active, typeId, settingsSnapshot, loadExample]);

  useEffect(() => {
    if (!active || !typeId) return;

    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key !== "r" && event.key !== "R") return;
      if (event.metaKey || event.ctrlKey || event.altKey) return;
      if (isTypingTarget(event.target)) return;
      if (loading) return;

      event.preventDefault();
      event.stopImmediatePropagation();
      void loadExample();
    };

    // Capture so worksheet R does not also fire while this modal is open.
    window.addEventListener("keydown", onKeyDown, true);
    return () => window.removeEventListener("keydown", onKeyDown, true);
  }, [active, typeId, loading, loadExample]);

  if (!active || !typeId) return null;

  const choices = question ? getMultipleChoiceChoices(question.metadata) : null;
  const letter = choices ? correctChoiceLabel(choices) : null;
  const showAnswer =
    Boolean(question?.answer_latex) ||
    (question ? hasAnswerDiagram(question.metadata) : false) ||
    Boolean(letter);

  return (
    <section className="topic-example-preview" aria-live="polite">
      <div className="topic-example-preview-header">
        <h3>Example</h3>
        <div className="topic-example-preview-actions">
          <span className="hint topic-example-preview-hint">Press R to regenerate</span>
          <button
            className="secondary"
            type="button"
            onClick={() => void loadExample()}
            disabled={loading}
          >
            {loading ? "Generating…" : "Regenerate"}
          </button>
        </div>
      </div>

      {error ? <p className="error">{error}</p> : null}

      {!error && !question && loading ? (
        <p className="hint">Generating example…</p>
      ) : null}

      {question ? (
        <div className={`topic-example-preview-body${loading ? " is-loading" : ""}`}>
          <div className="question-prompt-row">
            <QuestionPrompt content={question.prompt_latex} />
          </div>
          <QuestionGraphFromMetadata metadata={question.metadata} />
          <QuestionDiagramFromMetadata metadata={question.metadata} />
          {choices ? (
            <MultipleChoiceOptions
              choices={choices}
              questionId={`topic-example-${question.id}`}
            />
          ) : null}
          {showAnswer ? (
            <div className="topic-example-preview-answer">
              <span className="topic-example-preview-answer-label">Answer</span>
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
            </div>
          ) : null}
        </div>
      ) : null}
    </section>
  );
}
