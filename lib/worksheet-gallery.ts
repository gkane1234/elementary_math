/** Gallery catalog + deep-link helpers for example worksheets. */

import galleryConfig from "@/config/worksheet-gallery.json";
import {
  worksheetDifficultyToRamp,
  type WorksheetDifficultyInput,
  type WorksheetDifficultyRamp,
} from "@/lib/worksheet-difficulty";

export type GalleryEntry = {
  id: string;
  title: string;
  description: string;
  course: string;
  lesson: string;
  seeds: string[];
  worksheetDifficulty: WorksheetDifficultyInput;
  count: number;
  seed: number;
  includeRelated?: boolean;
  maxTopics?: number;
};

export type GalleryConfig = {
  version: number;
  difficulty_mapping: Record<string, unknown>;
  entries: GalleryEntry[];
};

export const worksheetGalleryConfig = galleryConfig as GalleryConfig;

export function listGalleryEntries(): GalleryEntry[] {
  return worksheetGalleryConfig.entries;
}

export function getGalleryEntry(id: string): GalleryEntry | undefined {
  return worksheetGalleryConfig.entries.find((entry) => entry.id === id);
}

export function galleryEntryRamp(entry: GalleryEntry): WorksheetDifficultyRamp {
  return worksheetDifficultyToRamp(entry.worksheetDifficulty);
}

/** Worksheet RNG seed for one gallery visit. Slot k still uses this seed + k*1009. */
export function freshGalleryRngSeed(): number {
  return 1 + Math.floor(Math.random() * 1_000_000_000);
}

/** Payload for POST /api/generate. Pass a new `rngSeed` on every open and regenerate. */
export function galleryProgressiveRequest(entry: GalleryEntry, rngSeed: number) {
  const ramp = galleryEntryRamp(entry);
  return {
    seeds: entry.seeds,
    count: entry.count,
    d_min: ramp.d_min,
    d_max: ramp.d_max,
    worksheet_difficulty: entry.worksheetDifficulty,
    include_related: entry.includeRelated !== false,
    max_topics: entry.maxTopics ?? 4,
    title: entry.title,
    rng_seed: rngSeed,
  };
}

/** Build a home-page deep link that opens progressive mode for this gallery entry. */
export function galleryOpenInGeneratorHref(entry: GalleryEntry, options?: { auto?: boolean }): string {
  const ramp = galleryEntryRamp(entry);
  const params = new URLSearchParams({
    mode: "progressive",
    seed: entry.seeds[0] ?? "",
    count: String(entry.count),
    d_min: String(ramp.d_min),
    d_max: String(ramp.d_max),
    worksheetDifficulty: String(entry.worksheetDifficulty),
    include_related: entry.includeRelated === false ? "0" : "1",
    title: entry.title,
  });
  if (options?.auto !== false) {
    params.set("auto", "1");
  }
  if (entry.seed != null) {
    params.set("rng_seed", String(entry.seed));
  }
  return `/?${params.toString()}`;
}
