"use client";

import Link from "next/link";
import { useCallback, useEffect, useMemo, useState } from "react";
import { InteractiveWorksheet } from "@/components/InteractiveWorksheet";
import { generateProgressive } from "@/lib/api";
import { fetchEntitlement } from "@/lib/payment";
import {
  galleryOpenInGeneratorHref,
  gallerySnapshotPath,
  getGalleryEntry,
} from "@/lib/worksheet-gallery";
import { worksheetDifficultyToRamp } from "@/lib/worksheet-difficulty";
import type { Question, QuestionTypeInfo, WorksheetDraft } from "@/lib/types";
import { questionSetToDraft } from "@/lib/worksheet";
import { formatTopicLabel } from "@/lib/topic-labels";

type SnapshotPayload = {
  id: string;
  title: string;
  description?: string;
  course?: string;
  lesson?: string;
  topics?: string[];
  difficulties?: number[];
  questions?: Question[];
  worksheetDifficulty?: string;
  ramp?: { d_min: number; d_max: number; schedule: string; label: string };
};

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
        /* types optional for static snapshot display */
      });
  }, []);

  const loadSnapshot = useCallback(async () => {
    if (!entry) return;
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(gallerySnapshotPath(entry.id), { cache: "no-store" });
      if (!response.ok) {
        throw new Error(
          "No static snapshot yet — click Regenerate, or run scripts/build_worksheet_gallery.py",
        );
      }
      const data = (await response.json()) as SnapshotPayload;
      const questions = data.questions ?? [];
      setWorksheet(questionsToDraft(data.title || entry.title, questions));
      setTopics(data.topics ?? []);
      setDifficulties(data.difficulties ?? []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load snapshot");
      setWorksheet(null);
    } finally {
      setLoading(false);
    }
  }, [entry]);

  useEffect(() => {
    void loadSnapshot();
  }, [loadSnapshot]);

  const regenerate = async () => {
    if (!entry) return;
    setRegenerating(true);
    setError(null);
    try {
      const ramp = worksheetDifficultyToRamp(entry.worksheetDifficulty);
      const result = await generateProgressive({
        seeds: entry.seeds,
        count: entry.count,
        d_min: ramp.d_min,
        d_max: ramp.d_max,
        worksheet_difficulty: entry.worksheetDifficulty,
        include_related: entry.includeRelated !== false,
        max_topics: entry.maxTopics ?? 4,
        title: entry.title,
        rng_seed: entry.seed,
      });
      setWorksheet(
        questionsToDraft(result.title || entry.title, result.questions ?? []),
      );
      setTopics(result.progressive?.topics ?? []);
      setDifficulties(result.progressive?.difficulties ?? []);
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
            {ramp.label} · D {ramp.d_min}–{ramp.d_max} · {entry.count} questions · seed RNG{" "}
            {entry.seed}
          </p>
          <div className="gallery-card-actions">
            <Link className="button" href={openHref}>
              Open in generator
            </Link>
            <button
              type="button"
              className="button secondary"
              disabled={regenerating}
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
      {loading && <p className="worksheet-status">Loading snapshot…</p>}
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
