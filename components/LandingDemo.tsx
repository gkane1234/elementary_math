"use client";

import Link from "next/link";
import { useCallback, useEffect, useRef, useState } from "react";
import { QuestionDiagramFromMetadata } from "@/components/QuestionDiagram";
import { QuestionGraphFromMetadata } from "@/components/QuestionGraph";
import { QuestionPrompt } from "@/components/QuestionPrompt";
import { generateProgressive, type ProgressivePlan } from "@/lib/api";
import { collapseRedundantLeftGroups } from "@/lib/latex";
import { formatDifficulty } from "@/lib/landing";
import { formatTopicLabel } from "@/lib/topic-labels";
import type { Question } from "@/lib/types";
import {
  freshGalleryRngSeed,
  galleryOpenInGeneratorHref,
  galleryProgressiveRequest,
  listGalleryEntries,
  type GalleryEntry,
} from "@/lib/worksheet-gallery";
import {
  WORKSHEET_DIFFICULTY_PRESETS,
  worksheetDifficultyToRamp,
  type WorksheetDifficultyPreset,
} from "@/lib/worksheet-difficulty";

const DEMO_COUNT = 3;

type LoadSpec = {
  entry: GalleryEntry;
  level: WorksheetDifficultyPreset;
  rngSeed: number;
};

function levelOf(entry: GalleryEntry): WorksheetDifficultyPreset {
  return worksheetDifficultyToRamp(entry.worksheetDifficulty).level;
}

function pickEntry(exceptId?: string): GalleryEntry {
  const entries = listGalleryEntries();
  const pool = exceptId ? entries.filter((entry) => entry.id !== exceptId) : entries;
  const source = pool.length > 0 ? pool : entries;
  return source[Math.floor(Math.random() * source.length)];
}

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

function demoEntry(spec: LoadSpec): GalleryEntry {
  return {
    ...spec.entry,
    worksheetDifficulty: spec.level,
    count: DEMO_COUNT,
    seed: spec.rngSeed,
  };
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
        galleryProgressiveRequest(demoEntry(next), next.rngSeed),
      );
      if (id !== requestId.current) return;
      setQuestions((result.questions ?? []).slice(0, DEMO_COUNT));
      setPlan(result.progressive ?? null);
      const ramp = worksheetDifficultyToRamp(next.level);
      setStatus(`${ramp.label}, D ${ramp.d_min}–${ramp.d_max}. Three questions, generated now.`);
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
    const entry = pickEntry();
    void load(
      { entry, level: levelOf(entry), rngSeed: freshGalleryRngSeed() },
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

  const levelIndex = spec ? WORKSHEET_DIFFICULTY_PRESETS.indexOf(spec.level) : -1;
  const ramp = spec ? worksheetDifficultyToRamp(spec.level) : null;

  function stepLevel(delta: number, message: string) {
    if (!spec || busy) return;
    const nextIndex = levelIndex + delta;
    if (nextIndex < 0 || nextIndex >= WORKSHEET_DIFFICULTY_PRESETS.length) return;
    void load(
      { ...spec, level: WORKSHEET_DIFFICULTY_PRESETS[nextIndex] },
      message,
    );
  }

  return (
    <figure
      className="landing-sheet"
      data-demo-entry={spec?.entry.id ?? ""}
      data-demo-level={spec?.level ?? ""}
      data-demo-seed={spec ? String(spec.rngSeed) : ""}
      data-demo-busy={busy ? "1" : "0"}
      aria-busy={busy}
    >
      <figcaption className="landing-sheet-top">
        <div>
          <p className="landing-sheet-title">{spec?.entry.title ?? "Worksheet"}</p>
          <p className="landing-sheet-note" aria-live="polite">
            {status}
          </p>
        </div>
        {ramp ? (
          <span className={`gallery-badge gallery-badge--${ramp.schedule}`}>
            {ramp.label}
            <span className="gallery-badge-range">
              D {ramp.d_min}–{ramp.d_max}
            </span>
          </span>
        ) : null}
      </figcaption>

      {error ? <p className="error">{error}</p> : null}

      <ol className={busy && questions.length > 0 ? "landing-questions is-loading" : "landing-questions"}>
        {questions.map((question, index) => {
          const difficulty = questionDifficulty(question, index, plan);
          const prompt = collapseRedundantLeftGroups(question.prompt_latex || question.prompt_text);
          return (
            <li key={question.id || index} className="landing-question" data-latex={prompt}>
              <div className="landing-question-prompt">
                <QuestionPrompt content={prompt} />
                <QuestionGraphFromMetadata metadata={question.metadata} />
                <QuestionDiagramFromMetadata metadata={question.metadata} />
              </div>
              <p className="landing-question-meta">
                {formatTopicLabel(question.topic, typeNames[question.topic])}
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
          onClick={() => stepLevel(-1, "Making an easier sheet…")}
          disabled={busy || !spec || levelIndex <= 0}
        >
          Too hard
        </button>
        <button
          type="button"
          onClick={() => stepLevel(1, "Making a harder sheet…")}
          disabled={busy || !spec || levelIndex < 0 || levelIndex >= WORKSHEET_DIFFICULTY_PRESETS.length - 1}
        >
          Harder
        </button>
        <button
          type="button"
          onClick={() => {
            if (!spec || busy) return;
            void load(
              { ...spec, rngSeed: freshGalleryRngSeed() },
              "Generating new questions…",
            );
          }}
          disabled={busy || !spec}
        >
          New questions
        </button>
        <button
          type="button"
          onClick={() => {
            if (busy) return;
            const entry = pickEntry(spec?.entry.id);
            void load(
              { entry, level: levelOf(entry), rngSeed: freshGalleryRngSeed() },
              "Picking another worksheet…",
            );
          }}
          disabled={busy}
        >
          Another worksheet
        </button>
      </div>

      {spec ? (
        <p className="landing-sheet-link">
          <Link href={galleryOpenInGeneratorHref(demoEntry(spec))}>Open in the generator</Link>
        </p>
      ) : null}
    </figure>
  );
}
