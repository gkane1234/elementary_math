/** Gallery catalog + deep-link helpers for example worksheets. */

import galleryConfig from "@/config/worksheet-gallery.json";
import geometryGalleryConfig from "@/config/worksheet-gallery-geometry.json";
import type { ProgressivePairing, ProgressiveScope, ProgressiveStyle } from "@/lib/progressive";
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
  pairing?: ProgressivePairing;
  scope?: ProgressiveScope;
  topics?: string[];
  style?: ProgressiveStyle;
  rampEachTopic?: boolean;
};

export type GalleryConfig = {
  version: number;
  difficulty_mapping: Record<string, unknown>;
  entries: GalleryEntry[];
};

function asGalleryEntries(value: { entries?: unknown }): GalleryEntry[] {
  if (!Array.isArray(value.entries)) return [];
  return value.entries as GalleryEntry[];
}

/** Main catalog first. Geometry templates append when that file has entries. */
export function mergeGalleryEntries(main: GalleryEntry[], extra: GalleryEntry[]): GalleryEntry[] {
  const seen = new Set(main.map((entry) => entry.id));
  const merged = [...main];
  for (const entry of extra) {
    if (!entry?.id || seen.has(entry.id)) continue;
    seen.add(entry.id);
    merged.push(entry);
  }
  return merged;
}

export const worksheetGalleryConfig: GalleryConfig = {
  ...(galleryConfig as GalleryConfig),
  entries: mergeGalleryEntries(
    asGalleryEntries(galleryConfig),
    asGalleryEntries(geometryGalleryConfig),
  ),
};

export function listGalleryEntries(): GalleryEntry[] {
  return worksheetGalleryConfig.entries;
}

/** First catalog sheet. The generator opens on this page. */
export function defaultGalleryEntry(): GalleryEntry | undefined {
  return worksheetGalleryConfig.entries[0];
}

/**
 * Catalog sheets that include `typeId`: the seed counts, and so does any
 * topic the progressive plan actually places on the sheet.
 */
export function worksheetsIncludingTopic(
  typeId: string,
  plannedTopicsById: Readonly<Record<string, readonly string[]>> = {},
): GalleryEntry[] {
  const topic = typeId.trim();
  if (!topic) return [];
  return listGalleryEntries().filter((entry) => {
    if (entry.seeds.includes(topic)) return true;
    return plannedTopicsById[entry.id]?.includes(topic) ?? false;
  });
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
    ...(entry.pairing ? { pairing: entry.pairing } : {}),
    ...(entry.scope ? { scope: entry.scope } : {}),
    ...(entry.topics?.length ? { topics: entry.topics } : {}),
    ...(entry.style ? { style: entry.style } : {}),
    ...(entry.rampEachTopic != null ? { ramp_each_topic: entry.rampEachTopic } : {}),
  };
}

/** Build a generator deep link that opens progressive mode for this gallery entry. */
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
  if (entry.pairing) params.set("pairing", entry.pairing);
  if (entry.scope) params.set("scope", entry.scope);
  if (entry.style) params.set("style", entry.style);
  if (entry.rampEachTopic != null) {
    params.set("ramp_each_topic", entry.rampEachTopic ? "1" : "0");
  }
  if (entry.topics?.length) params.set("topics", entry.topics.join(","));
  return `/generate?${params.toString()}`;
}
