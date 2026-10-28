"use client";

import Link from "next/link";
import { useCallback, useEffect, useMemo, useState } from "react";
import { InteractiveWorksheet } from "@/components/InteractiveWorksheet";
import { generateProgressive, type ProgressiveGenerateResult } from "@/lib/api";
import { fetchEntitlement } from "@/lib/payment";
import {
  freshGalleryRngSeed,
  galleryOpenInGeneratorHref,
  galleryProgressiveRequest,
  getGalleryEntry,
} from "@/lib/worksheet-gallery";
import { worksheetDifficultyToRamp } from "@/lib/worksheet-difficulty";
import type { Question, QuestionTypeInfo, WorksheetDraft } from "@/lib/types";
import { questionSetToDraft } from "@/lib/worksheet";
import { formatTopicLabel } from "@/lib/topic-labels";

function questionsToDraft(title: string, questions: Question[]): WorksheetDraft {
  return questionSetToDraft({
    title,
    questions,
    columns: questions.length <= 6 ? 1 : 2,
  });
}

export function GalleryExampleViewer({ entryId }: { entryId: string }) {
  const entry = useMemo(() => getGalleryEntry(entryId), [entryId]);
  const [types, setTypes] = useState<QuestionTypeInfo[]>([]);
  const [worksheet, setWorksheet] = useState<WorksheetDraft | null>(null);
  const [topics, setTopics] = useState<string[]>([]);
  const [difficulties, setDifficulties] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);
  const [regenerating, setRegenerating] = useState(false);
  const [activeSeed, setActiveSeed] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [previewMode, setPreviewMode] = useState(true);

  useEffect(() => {
    fetchEntitlement()
      .then((data) => {
        setPreviewMode(!(data.entitled && data.reason !== "payments_disabled"));
      })
      .catch(() => setPreviewMode(true));
  }, []);

  useEffect(() => {
    fetch("/api/question-types", { cache: "no-store" })
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error("Failed to load types"))))
      .then((data) => setTypes(data.types ?? []))
      .catch(() => {
        /* topic labels still render if the type catalog is unavailable */
      });
  }, []);

  const applyGenerated = useCallback(
    (result: ProgressiveGenerateResult) => {
      if (!entry) return;
      setWorksheet(questionsToDraft(result.title || entry.title, result.questions ?? []));
      setTopics(result.progressive?.topics ?? []);
      setDifficulties(result.progressive?.difficulties ?? []);
    },
    [entry],
  );

  const generateExample = useCallback(async () => {
    if (!entry) {
      throw new Error("Unknown gallery example");
    }
    const rngSeed = freshGalleryRngSeed();
    const result = await generateProgressive(galleryProgressiveRequest(entry, rngSeed));
    return { result, rngSeed };
  }, [entry]);

  useEffect(() => {
    if (!entry) {
      setLoading(false);
      return;
    }
    let cancelled = false;
    setLoading(true);
    setError(null);
    setWorksheet(null);
    setActiveSeed(null);
    setTopics([]);
    setDifficulties([]);
    generateExample()
      .then(({ result, rngSeed }) => {
        if (cancelled) return;
        applyGenerated(result);
        setActiveSeed(rngSeed);
      })
      .catch((err: unknown) => {
        if (cancelled) return;
        setError(err instanceof Error ? err.message : "Generation failed");
        setWorksheet(null);
        setActiveSeed(null);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [entry, generateExample, applyGenerated]);

  const regenerate = async () => {
    if (!entry || loading) return;
    setRegenerating(true);
    setError(null);
    try {
      const { result, rngSeed } = await generateExample();
      applyGenerated(result);
      setActiveSeed(rngSeed);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Regeneration failed");
    } finally {
      setRegenerating(false);
    }
  };

  if (!entry) {
    return (
      <div className="gallery-page">
        <p className="error">Unknown gallery example: {entryId}</p>
        <Link href="/gallery">← Back to gallery</Link>
      </div>
    );
  }

  const ramp = worksheetDifficultyToRamp(entry.worksheetDifficulty);
  const openHref = galleryOpenInGeneratorHref(entry);

  return (
    <div className="gallery-page gallery-detail">
      <p className="gallery-kicker">
        <Link href="/gallery">← Gallery</Link>
      </p>
      <header className="gallery-detail-header">
        <div>
          <h1 className="gallery-heading">{entry.title}</h1>
          <p className="gallery-card-meta">
            {entry.course} · {entry.lesson}
          </p>
          <p className="gallery-lede">{entry.description}</p>
        </div>
        <div className="gallery-detail-side">
          <p>
            <span className={`gallery-badge gallery-badge--${ramp.schedule}`}>
              {ramp.label}
              <span className="gallery-badge-range">
                D {ramp.d_min}–{ramp.d_max}
              </span>
            </span>
          </p>
          <p className="hint">
            {ramp.label} · D {ramp.d_min}–{ramp.d_max} · {entry.count} questions
            {activeSeed != null ? ` · seed ${activeSeed}` : " · new seed each visit"}
          </p>
          <div className="gallery-card-actions">
            <Link className="button" href={openHref}>
              Open in generator
            </Link>
            <button
              type="button"
              className="button secondary"
              disabled={loading || regenerating}
              onClick={() => void regenerate()}
            >
              {regenerating ? "Regenerating…" : "Regenerate via API"}
            </button>
          </div>
        </div>
      </header>

      {(topics.length > 0 || difficulties.length > 0) && (
        <div className="gallery-plan">
          {topics.length > 0 && (
            <p>
              <span className="gallery-label">Coherent topics</span>
              {topics.map((tid) => formatTopicLabel(tid)).join(", ")}
            </p>
          )}
          {difficulties.length > 0 && (
            <p>
              <span className="gallery-label">D ramp</span>
              {difficulties.map((d) => (Number.isInteger(d) ? d : d.toFixed(1))).join(" → ")}
            </p>
          )}
        </div>
      )}

      {error && <p className="error">{error}</p>}
      {loading && <p className="worksheet-status">Generating worksheet…</p>}
      {regenerating && <p className="worksheet-status">Regenerating worksheet…</p>}
      {previewMode && worksheet && (
        <p className="worksheet-status preview-banner">
          Preview watermark — subscribe or unlock in the generator for clean export.
        </p>
      )}
      {worksheet && (
        <InteractiveWorksheet
          worksheet={worksheet}
          types={types}
          previewMode={previewMode}
          onChange={setWorksheet}
          onError={setError}
        />
      )}
    </div>
  );
}
