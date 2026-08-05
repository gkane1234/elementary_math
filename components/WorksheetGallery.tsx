"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import {
  galleryOpenInGeneratorHref,
  listGalleryEntries,
  type GalleryEntry,
} from "@/lib/worksheet-gallery";
import {
  WORKSHEET_DIFFICULTY_PRESETS,
  worksheetDifficultyOptionLabel,
  worksheetDifficultyToRamp,
  type WorksheetDifficultyPreset,
} from "@/lib/worksheet-difficulty";
import { formatTopicLabel } from "@/lib/topic-labels";

function DifficultyBadge({ level }: { level: WorksheetDifficultyPreset | string }) {
  const ramp = worksheetDifficultyToRamp(level);
  return (
    <span className={`gallery-badge gallery-badge--${ramp.schedule}`} title={ramp.description}>
      {ramp.label}
      <span className="gallery-badge-range">
        D {ramp.d_min}–{ramp.d_max}
      </span>
    </span>
  );
}

function GalleryCard({ entry }: { entry: GalleryEntry }) {
  const ramp = worksheetDifficultyToRamp(entry.worksheetDifficulty);
  const openHref = galleryOpenInGeneratorHref(entry);

  return (
    <article className="gallery-card">
      <div className="gallery-card-top">
        <h2 className="gallery-card-title">{entry.title}</h2>
        <DifficultyBadge level={String(entry.worksheetDifficulty)} />
      </div>
      <p className="gallery-card-meta">
        <span>{entry.course}</span>
        <span aria-hidden="true"> · </span>
        <span>{entry.lesson}</span>
      </p>
      <p className="gallery-card-desc">{entry.description}</p>
      <p className="gallery-card-topics">
        <span className="gallery-label">Seed topics</span>
        {entry.seeds.map((s) => formatTopicLabel(s)).join(", ")}
      </p>
      <p className="gallery-card-ramp">
        <span className="gallery-label">D schedule</span>
        {ramp.schedule} ramp · {ramp.d_min} → {ramp.d_max} across {entry.count} questions
      </p>
      <div className="gallery-card-actions">
        <Link className="button" href={`/gallery/${entry.id}`}>
          View example
        </Link>
        <Link className="button secondary" href={openHref}>
          Open in generator
        </Link>
      </div>
    </article>
  );
}

export function WorksheetGallery() {
  const entries = useMemo(() => listGalleryEntries(), []);
  const [courseFilter, setCourseFilter] = useState<string>("all");
  const [diffFilter, setDiffFilter] = useState<string>("all");

  const courses = useMemo(() => {
    const set = new Set(entries.map((e) => e.course));
    return ["all", ...Array.from(set)];
  }, [entries]);

  const filtered = entries.filter((entry) => {
    if (courseFilter !== "all" && entry.course !== courseFilter) return false;
    if (diffFilter !== "all" && String(entry.worksheetDifficulty) !== diffFilter) return false;
    return true;
  });

  return (
    <div className="gallery-page">
      <div className="gallery-intro">
        <p className="gallery-kicker">
          <Link href="/">← Generator</Link>
        </p>
        <h1 className="gallery-heading">Example worksheet gallery</h1>
        <p className="gallery-lede">
          Progressive practice worksheets across courses. Each example uses a{" "}
          <strong>worksheet Level (0–4)</strong> that sets how question difficulties
          ramp across the sheet.
        </p>
        <div className="gallery-mapping">
          <h2>Worksheet difficulty → D ramp</h2>
          <table className="gallery-mapping-table">
            <thead>
              <tr>
                <th>Level</th>
                <th>d_min</th>
                <th>d_max</th>
                <th>Schedule</th>
              </tr>
            </thead>
            <tbody>
              {WORKSHEET_DIFFICULTY_PRESETS.map((level) => {
                const ramp = worksheetDifficultyToRamp(level);
                return (
                  <tr key={level}>
                    <td>
                      <DifficultyBadge level={level} />
                    </td>
                    <td>{ramp.d_min}</td>
                    <td>{ramp.d_max}</td>
                    <td>{ramp.schedule}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
          <p className="hint">
            A numeric slider 0–24 interpolates between Level 0 (D 0–3) and Level 4 (D 20–25).
            Progressive mode expands seed topics into related curriculum neighbors and assigns
            each question D = lerp(d_min, d_max, i/(N−1)).
          </p>
        </div>
      </div>

      <div className="gallery-filters">
        <label>
          Course
          <select value={courseFilter} onChange={(e) => setCourseFilter(e.target.value)}>
            {courses.map((c) => (
              <option key={c} value={c}>
                {c === "all" ? "All courses" : c}
              </option>
            ))}
          </select>
        </label>
        <label>
          Worksheet difficulty
          <select value={diffFilter} onChange={(e) => setDiffFilter(e.target.value)}>
            <option value="all">All levels</option>
            {WORKSHEET_DIFFICULTY_PRESETS.map((level) => (
              <option key={level} value={level}>
                {worksheetDifficultyOptionLabel(level)}
              </option>
            ))}
          </select>
        </label>
      </div>

      <div className="gallery-grid">
        {filtered.map((entry) => (
          <GalleryCard key={entry.id} entry={entry} />
        ))}
      </div>
      {filtered.length === 0 && <p className="hint">No examples match these filters.</p>}
    </div>
  );
}
