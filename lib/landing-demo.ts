/**
 * Landing-hero worksheet pool.
 *
 * Bands are the five ranges the demo steps through: D 0–5, 5–10, 10–15,
 * 15–20, 20–25. The sheet opens on the second band (D 5–10).
 *
 * `config/landing-demo-types.json` is the types where that step is visible.
 * Each id is a Grade 6 `verified_ramp` topic, or a pre-algebra topic from the
 * first ramp tranche in `scripts/output/topic_fit/`. A type is listed only
 * when the same seed replays the same five questions, and those questions
 * differ between every pair of adjacent bands, for seeds 1, 7, and 101.
 * `question_engine/tests/test_landing_demo_pool.py` rechecks that.
 */

import pool from "@/config/landing-demo-types.json";
import { freshGalleryRngSeed } from "@/lib/worksheet-gallery";

export type DemoType = {
  id: string;
  name: string;
};

export type DemoBand = {
  d_min: number;
  d_max: number;
};

const SCHEDULES = ["intro", "gentle", "moderate", "steep", "intense"] as const;

export const DEMO_QUESTION_COUNT = pool.count;
export const DEMO_BANDS: DemoBand[] = pool.bands;
export const DEMO_START_BAND = pool.start_band;
export const DEMO_TYPES: DemoType[] = pool.types;

export function demoBand(index: number): DemoBand {
  const band = DEMO_BANDS[index];
  if (!band) {
    throw new Error(`Demo band ${index} is outside 0–${DEMO_BANDS.length - 1}`);
  }
  return band;
}

export function demoBandLabel(band: DemoBand): string {
  return `D ${band.d_min}\u2013${band.d_max}`;
}

export function demoBandSchedule(index: number): (typeof SCHEDULES)[number] {
  return SCHEDULES[index] ?? "gentle";
}

export function pickDemoType(exceptId?: string): DemoType {
  const choices = exceptId ? DEMO_TYPES.filter((type) => type.id !== exceptId) : DEMO_TYPES;
  const source = choices.length > 0 ? choices : DEMO_TYPES;
  return source[Math.floor(Math.random() * source.length)];
}

export function freshDemoRngSeed(): number {
  return freshGalleryRngSeed();
}

export function demoProgressiveRequest(type: DemoType, bandIndex: number, rngSeed: number) {
  const band = demoBand(bandIndex);
  return {
    seeds: [type.id],
    count: DEMO_QUESTION_COUNT,
    d_min: band.d_min,
    d_max: band.d_max,
    include_related: false as const,
    max_topics: 1,
    title: type.name,
    rng_seed: rngSeed,
  };
}

/** Generator link for this sheet. Omits worksheetDifficulty so the band is not replaced. */
export function demoGeneratorHref(type: DemoType, bandIndex: number, rngSeed: number): string {
  const band = demoBand(bandIndex);
  const params = new URLSearchParams({
    mode: "progressive",
    seed: type.id,
    count: String(DEMO_QUESTION_COUNT),
    d_min: String(band.d_min),
    d_max: String(band.d_max),
    include_related: "0",
    title: type.name,
    auto: "1",
    rng_seed: String(rngSeed),
  });
  return `/generate?${params.toString()}`;
}
