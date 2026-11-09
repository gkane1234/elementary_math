"use client";

import Link from "next/link";
import { useCallback, useEffect, useRef, useState } from "react";
import { QuestionDiagramFromMetadata } from "@/components/QuestionDiagram";
import { QuestionGraphFromMetadata } from "@/components/QuestionGraph";
import { QuestionPrompt } from "@/components/QuestionPrompt";
import { generateProgressive, type ProgressivePlan } from "@/lib/api";
import { collapseRedundantLeftGroups } from "@/lib/latex";
import { formatDifficulty } from "@/lib/landing";
import {
  DEMO_BANDS,
  DEMO_QUESTION_COUNT,
  DEMO_START_BAND,
  demoBandLabel,
  demoBandSchedule,
  demoGeneratorHref,
  demoProgressiveRequest,
  freshDemoRngSeed,
  pickDemoType,
  type DemoType,
} from "@/lib/landing-demo";
import { formatTopicLabel } from "@/lib/topic-labels";
import type { Question } from "@/lib/types";

type LoadSpec = {
  type: DemoType;
  band: number;
  rngSeed: number;
};

function questionDifficulty(
  question: Question,
  index: number,
  plan: ProgressivePlan | null,
): number | null {
  const settings = question.metadata?.generation_settings;
  if (settings && typeof settings === "object" && "difficulty" in settings) {
    const value = (settings as { difficulty?: unknown }).difficulty;
    if (typeof value === "number") return value;
  }
  const effective = question.metadata?.effective_d;
  if (typeof effective === "number") return effective;
  const planned = plan?.difficulties?.[index];
  return typeof planned === "number" ? planned : null;
}

export function LandingDemo() {
  const [spec, setSpec] = useState<LoadSpec | null>(null);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [plan, setPlan] = useState<ProgressivePlan | null>(null);
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState("Picking a worksheet…");
  const [typeNames, setTypeNames] = useState<Record<string, string>>({});
  const requestId = useRef(0);
  const specRef = useRef<LoadSpec | null>(null);

  const load = useCallback(async (next: LoadSpec, message: string) => {
    const previous = specRef.current;
    const id = ++requestId.current;
    setStatus(message);
    setBusy(true);
    setError(null);
    setSpec(next);
    specRef.current = next;
    try {
      const result = await generateProgressive(
        demoProgressiveRequest(next.type, next.band, next.rngSeed),
      );
      if (id !== requestId.current) return;
      setQuestions((result.questions ?? []).slice(0, DEMO_QUESTION_COUNT));
      setPlan(result.progressive ?? null);
      const band = DEMO_BANDS[next.band];
      setStatus(
        `${demoBandLabel(band)}. Five questions, generated now.`,
      );
    } catch (err) {
      if (id !== requestId.current) return;
      if (previous) {
        setSpec(previous);
        specRef.current = previous;
      }
      setError(err instanceof Error ? err.message : "Generation failed");
      setStatus("Could not generate this sheet.");
    } finally {
      if (id === requestId.current) setBusy(false);
    }
  }, []);

  useEffect(() => {
    void load(
      { type: pickDemoType(), band: DEMO_START_BAND, rngSeed: freshDemoRngSeed() },
      "Picking a worksheet…",
    );
  }, [load]);

  useEffect(() => {
    let cancelled = false;
    fetch("/api/question-types", { cache: "no-store" })
      .then((response) => (response.ok ? response.json() : null))
      .then((data) => {
        if (cancelled || !data?.types) return;
        const names: Record<string, string> = {};
        for (const type of data.types) {
          if (type?.id && type?.name) names[type.id] = type.name;
        }
        setTypeNames(names);
      })
      .catch(() => {
        /* humanized type ids still label the questions */
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const band = spec ? DEMO_BANDS[spec.band] : null;

  function stepBand(delta: number, message: string) {
    if (!spec || busy) return;
    const nextBand = spec.band + delta;
    if (nextBand < 0 || nextBand >= DEMO_BANDS.length) return;
    void load({ ...spec, band: nextBand }, message);
  }

  return (
    <figure
      className="landing-sheet"
      data-demo-type={spec?.type.id ?? ""}
      data-demo-band={band ? `${band.d_min}-${band.d_max}` : ""}
      data-demo-seed={spec ? String(spec.rngSeed) : ""}
      data-demo-busy={busy ? "1" : "0"}
      aria-busy={busy}
    >
      <figcaption className="landing-sheet-top">
        <div>
          <p className="landing-sheet-title">{spec?.type.name ?? "Worksheet"}</p>
          <p className="landing-sheet-note" aria-live="polite">
            {status}
          </p>
        </div>
        {band && spec ? (
          <span className={`gallery-badge gallery-badge--${demoBandSchedule(spec.band)}`}>
            {demoBandLabel(band)}
          </span>
        ) : null}
      </figcaption>

      {error ? <p className="error">{error}</p> : null}

      <ol className={busy && questions.length > 0 ? "landing-questions is-loading" : "landing-questions"}>
        {questions.map((question, index) => {
          const difficulty = questionDifficulty(question, index, plan);
          const prompt = collapseRedundantLeftGroups(question.prompt_latex || question.prompt_text);
          const topicName =
            typeNames[question.topic] ??
            (spec && question.topic === spec.type.id ? spec.type.name : undefined);
          return (
            <li key={question.id || index} className="landing-question" data-latex={prompt}>
              <div className="landing-question-prompt">
                <QuestionPrompt content={prompt} />
                <QuestionGraphFromMetadata metadata={question.metadata} />
                <QuestionDiagramFromMetadata metadata={question.metadata} />
              </div>
              <p className="landing-question-meta">
                {formatTopicLabel(question.topic, topicName)}
                {difficulty != null ? (
                  <>
                    <span aria-hidden="true"> · </span>
                    D {formatDifficulty(difficulty)}
                  </>
                ) : null}
              </p>
            </li>
          );
        })}
      </ol>

      <div className="landing-demo-controls">
        <button
          type="button"
          onClick={() => {
            if (busy) return;
            const type = pickDemoType(spec?.type.id);
            void load(
              { type, band: DEMO_START_BAND, rngSeed: freshDemoRngSeed() },
              "Picking a new worksheet…",
            );
          }}
          disabled={busy}
        >
          New worksheet
        </button>
        <button
          type="button"
          onClick={() => {
            if (!spec || busy) return;
            void load(
              { ...spec, rngSeed: freshDemoRngSeed() },
              "Generating new questions…",
            );
          }}
          disabled={busy || !spec}
        >
          New questions
        </button>
        <button
          type="button"
          onClick={() => stepBand(-1, "Making an easier sheet…")}
          disabled={busy || !spec || spec.band <= 0}
        >
          Easier
        </button>
        <button
          type="button"
          onClick={() => stepBand(1, "Making a harder sheet…")}
          disabled={busy || !spec || spec.band >= DEMO_BANDS.length - 1}
        >
          Harder
        </button>
      </div>

      {spec ? (
        <p className="landing-sheet-link">
          <Link href={demoGeneratorHref(spec.type, spec.band, spec.rngSeed)}>
            Open in the generator
          </Link>
        </p>
      ) : null}
    </figure>
  );
}
