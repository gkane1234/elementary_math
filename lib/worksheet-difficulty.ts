/** Worksheet-level difficulty → per-question D ramp bands (mirrors Python). */

/** Preset ids shown in UI (Level 0–4). Legacy ids still accepted as input. */
export type WorksheetDifficultyPreset =
  | "level-0"
  | "level-1"
  | "level-2"
  | "level-3"
  | "level-4";

export type WorksheetDifficultyInput = WorksheetDifficultyPreset | number | string;

export type WorksheetDifficultySchedule =
  | "intro"
  | "gentle"
  | "moderate"
  | "steep"
  | "intense";

export type WorksheetDifficultyRamp = {
  level: WorksheetDifficultyPreset;
  label: string;
  d_min: number;
  d_max: number;
  schedule: WorksheetDifficultySchedule;
  description: string;
  slider?: number;
};

const NAMED: Record<WorksheetDifficultyPreset, WorksheetDifficultyRamp> = {
  "level-0": {
    level: "level-0",
    label: "Level 0",
    d_min: 0,
    d_max: 3,
    schedule: "intro",
    description: "Introductory band: most items at very low D.",
  },
  "level-1": {
    level: "level-1",
    label: "Level 1",
    d_min: 0,
    d_max: 8,
    schedule: "gentle",
    description: "Most items at low D with a gentle ramp.",
  },
  "level-2": {
    level: "level-2",
    label: "Level 2",
    d_min: 3,
    d_max: 20,
    schedule: "moderate",
    description: "Mid-band difficulties with a moderate ramp.",
  },
  "level-3": {
    level: "level-3",
    label: "Level 3",
    d_min: 8,
    d_max: 25,
    schedule: "steep",
    description: "High-band difficulties with a steep ramp.",
  },
  "level-4": {
    level: "level-4",
    label: "Level 4",
    d_min: 20,
    d_max: 25,
    schedule: "intense",
    description: "Sustained high-D practice near the top of the band.",
  },
};

/**
 * Legacy / prior-preset aliases → Level ids (API / old deep links only).
 *
 * | Alias | Maps to | Notes |
 * |-------|---------|-------|
 * | easy, e | level-1 | former easy → D 0–8 |
 * | medium, m | level-2 | former medium ≈ mid band |
 * | hard, h | level-3 | former hard ≈ high band |
 * | d0-8 | level-1 | exact former preset |
 * | d4-14 | level-2 | closest mid band (was 4–14) |
 * | d10-22 | level-3 | closest high band (was 10–22) |
 * | d0-3, d3-20, d8-25, d20-25 | level-0…4 | range-id synonyms |
 */
const LEGACY_ALIASES: Record<string, WorksheetDifficultyPreset> = {
  easy: "level-1",
  e: "level-1",
  medium: "level-2",
  m: "level-2",
  hard: "level-3",
  h: "level-3",
  "d0-8": "level-1",
  "d4-14": "level-2",
  "d10-22": "level-3",
  "d0-3": "level-0",
  "d3-20": "level-2",
  "d8-25": "level-3",
  "d20-25": "level-4",
};

const SCHEDULE_BY_BUCKET: WorksheetDifficultySchedule[] = [
  "intro",
  "gentle",
  "moderate",
  "steep",
  "intense",
];

function lerp(a: number, b: number, t: number): number {
  return a + (b - a) * t;
}

/** Map Level preset, legacy alias, or a 0–24 slider to { d_min, d_max, schedule }. */
export function worksheetDifficultyToRamp(
  level: WorksheetDifficultyInput,
): WorksheetDifficultyRamp {
  if (typeof level === "string") {
    const key = level.trim().toLowerCase();
    if (key in NAMED) return { ...NAMED[key as WorksheetDifficultyPreset] };
    if (key in LEGACY_ALIASES) return { ...NAMED[LEGACY_ALIASES[key]] };
    const asNum = Number(key);
    if (!Number.isFinite(asNum)) {
      throw new Error(
        `Unknown worksheet difficulty "${level}"; use level-0…level-4 or 0–24.`,
      );
    }
    return worksheetDifficultyToRamp(asNum);
  }

  const clamped = Math.max(0, Math.min(24, Number(level)));
  const t = clamped / 24;
  const low = NAMED["level-0"];
  const high = NAMED["level-4"];
  const d_min = Math.round(lerp(low.d_min, high.d_min, t) * 10000) / 10000;
  const d_max = Math.round(lerp(low.d_max, high.d_max, t) * 10000) / 10000;
  const bucket = Math.min(4, Math.floor(t * 5));
  const named = WORKSHEET_DIFFICULTY_PRESETS[bucket];
  const schedule = SCHEDULE_BY_BUCKET[bucket];
  return {
    level: named,
    slider: clamped,
    label: `D ${clamped}`,
    d_min,
    d_max,
    schedule,
    description: `Continuous worksheet D=${clamped} → questions ramp from ${d_min} to ${d_max} (${schedule}).`,
  };
}

export const WORKSHEET_DIFFICULTY_PRESETS: WorksheetDifficultyPreset[] = [
  "level-0",
  "level-1",
  "level-2",
  "level-3",
  "level-4",
];

/** @deprecated Use WORKSHEET_DIFFICULTY_PRESETS */
export const WORKSHEET_DIFFICULTY_LEVELS = WORKSHEET_DIFFICULTY_PRESETS;

/** @deprecated Use WorksheetDifficultyPreset */
export type WorksheetDifficultyLevel = WorksheetDifficultyPreset;

export function worksheetDifficultyLabel(level: WorksheetDifficultyInput): string {
  return worksheetDifficultyToRamp(level).label;
}

/** UI option text: e.g. "Level 2 (D 3–20)". */
export function worksheetDifficultyOptionLabel(
  level: WorksheetDifficultyInput,
): string {
  const ramp = worksheetDifficultyToRamp(level);
  if (ramp.slider !== undefined) return ramp.label;
  return `${ramp.label} (D ${ramp.d_min}–${ramp.d_max})`;
}
