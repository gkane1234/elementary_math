/**
 * Difficulty-tier presets that update domain settings when Easy / Medium / Hard
 * is selected in the topic settings UI.
 *
 * Structure mirrors `question_engine/settings/presets.py`:
 *   PROFILE_DIFFICULTY_PRESETS[profile][tier] = { settingKey: value }
 *
 * To add presets for a new question type:
 * 1. Prefer adding under that type's `setting_profile` in PROFILE_DIFFICULTY_PRESETS.
 * 2. For a one-off type, add an entry in GENERATOR_DIFFICULTY_PRESETS keyed by type id.
 * 3. Keep the Python presets module in sync so API generate behaves the same.
 */

export type DifficultyTier = "easy" | "medium" | "hard";

export type PresetValues = Record<string, string | number | boolean>;

export type TierPresets = Record<DifficultyTier, PresetValues>;

const COMMON_TERMS: TierPresets = {
  easy: { min_terms: 2, max_terms: 3 },
  medium: { min_terms: 2, max_terms: 4 },
  hard: { min_terms: 3, max_terms: 6 },
};

export const PROFILE_DIFFICULTY_PRESETS: Record<string, TierPresets> = {
  equation: {
    easy: { coef_min: -5, coef_max: 5, integer_only: true },
    medium: { coef_min: -12, coef_max: 12, integer_only: true },
    hard: { coef_min: -20, coef_max: 20, integer_only: false },
  },
  inequality: {
    easy: { coef_min: -5, coef_max: 5, integer_only: true },
    medium: { coef_min: -12, coef_max: 12, integer_only: true },
    hard: { coef_min: -20, coef_max: 20, integer_only: false },
  },
  compound_inequality: {
    easy: { coef_min: -5, coef_max: 5, integer_only: true },
    medium: { coef_min: -12, coef_max: 12, integer_only: true },
    hard: { coef_min: -20, coef_max: 20, integer_only: false },
  },
  polynomial: {
    easy: {
      coef_min: -5,
      coef_max: 5,
      min_degree: 1,
      max_degree: 2,
      integer_coefficients_only: true,
    },
    medium: {
      coef_min: -10,
      coef_max: 10,
      min_degree: 1,
      max_degree: 3,
      integer_coefficients_only: true,
    },
    hard: {
      coef_min: -15,
      coef_max: 15,
      min_degree: 2,
      max_degree: 5,
      integer_coefficients_only: false,
    },
  },
  polynomial_factoring: {
    easy: { coef_min: -5, coef_max: 5, min_degree: 2, max_degree: 2 },
    medium: { coef_min: -10, coef_max: 10, min_degree: 2, max_degree: 3 },
    hard: { coef_min: -15, coef_max: 15, min_degree: 2, max_degree: 4 },
  },
  polynomial_division: {
    easy: {
      coef_min: -5,
      coef_max: 5,
      numerator_degree_min: 2,
      numerator_degree_max: 3,
      denominator_degree_min: 1,
      denominator_degree_max: 1,
      divide_cleanly: true,
    },
    medium: {
      coef_min: -10,
      coef_max: 10,
      numerator_degree_min: 2,
      numerator_degree_max: 4,
      denominator_degree_min: 1,
      denominator_degree_max: 2,
      divide_cleanly: true,
    },
    hard: {
      coef_min: -15,
      coef_max: 15,
      numerator_degree_min: 3,
      numerator_degree_max: 5,
      denominator_degree_min: 1,
      denominator_degree_max: 2,
      divide_cleanly: false,
    },
  },
  number: {
    easy: {
      num_min: -5,
      num_max: 5,
      denom_min: 2,
      denom_max: 6,
      allow_negative: false,
      ...COMMON_TERMS.easy,
    },
    medium: {
      num_min: -10,
      num_max: 10,
      denom_min: 2,
      denom_max: 12,
      allow_negative: true,
      ...COMMON_TERMS.medium,
    },
    hard: {
      num_min: -20,
      num_max: 20,
      denom_min: 2,
      denom_max: 20,
      allow_negative: true,
      ...COMMON_TERMS.hard,
    },
  },
  rational: {
    easy: {
      num_min: -5,
      num_max: 5,
      denom_min: 2,
      denom_max: 6,
      coef_min: -5,
      coef_max: 5,
      allow_negative: false,
      allow_obelus: true,
      allow_complex_fraction: false,
      allow_slash: false,
      ...COMMON_TERMS.easy,
    },
    medium: {
      num_min: -10,
      num_max: 10,
      denom_min: 2,
      denom_max: 12,
      coef_min: -10,
      coef_max: 10,
      allow_negative: true,
      allow_obelus: true,
      allow_complex_fraction: false,
      allow_slash: true,
      ...COMMON_TERMS.medium,
    },
    hard: {
      num_min: -20,
      num_max: 20,
      denom_min: 2,
      denom_max: 20,
      coef_min: -15,
      coef_max: 15,
      allow_negative: true,
      allow_obelus: true,
      allow_complex_fraction: true,
      allow_slash: true,
      ...COMMON_TERMS.hard,
    },
  },
  percent: {
    easy: {
      percent_min: 5,
      percent_max: 50,
      base_min: 10,
      base_max: 100,
      round_to_whole: true,
      allow_decimal_percents: false,
    },
    medium: {
      percent_min: 5,
      percent_max: 75,
      base_min: 10,
      base_max: 200,
      round_to_whole: false,
      allow_decimal_percents: false,
    },
    hard: {
      percent_min: 1,
      percent_max: 99,
      base_min: 10,
      base_max: 500,
      round_to_whole: false,
      allow_decimal_percents: true,
    },
  },
  decimal: {
    easy: { decimal_places: 1, allow_negative: false },
    medium: { decimal_places: 2, allow_negative: false },
    hard: { decimal_places: 3, allow_negative: true },
  },
  ratio: {
    easy: { ratio_part_min: 1, ratio_part_max: 8 },
    medium: { ratio_part_min: 2, ratio_part_max: 15 },
    hard: { ratio_part_min: 2, ratio_part_max: 30 },
  },
  unit_rate: {
    easy: {
      unit_rate_min: 2,
      unit_rate_max: 8,
      unit_rate_multiplier_min: 2,
      unit_rate_multiplier_max: 5,
    },
    medium: {
      unit_rate_min: 2,
      unit_rate_max: 12,
      unit_rate_multiplier_min: 2,
      unit_rate_multiplier_max: 10,
    },
    hard: {
      unit_rate_min: 2,
      unit_rate_max: 25,
      unit_rate_multiplier_min: 3,
      unit_rate_multiplier_max: 15,
    },
  },
  proportion: {
    easy: { ratio_part_min: 1, ratio_part_max: 8 },
    medium: { ratio_part_min: 2, ratio_part_max: 12 },
    hard: { ratio_part_min: 2, ratio_part_max: 25 },
  },
  integer: {
    easy: { num_min: -10, num_max: 10, allow_negative: true },
    medium: { num_min: -20, num_max: 20, allow_negative: true },
    hard: { num_min: -50, num_max: 50, allow_negative: true },
  },
  factor: {
    easy: { factor_min: 4, factor_max: 30 },
    medium: { factor_min: 4, factor_max: 60 },
    hard: { factor_min: 6, factor_max: 120 },
  },
  order_of_operations: {
    easy: { pemdas_complexity: "basic", num_min: 2, num_max: 6 },
    medium: { pemdas_complexity: "mixed", num_min: 2, num_max: 9 },
    hard: { pemdas_complexity: "exponent", num_min: 2, num_max: 12 },
  },
  distributive: {
    easy: { coef_min: -5, coef_max: 5, allow_negative: false },
    medium: { coef_min: -9, coef_max: 9, allow_negative: true },
    hard: { coef_min: -15, coef_max: 15, allow_negative: true },
  },
  linear: {
    easy: {
      slope_min: -3,
      slope_max: 3,
      intercept_min: -5,
      intercept_max: 5,
      coord_min: -5,
      coord_max: 5,
    },
    medium: {
      slope_min: -6,
      slope_max: 6,
      intercept_min: -8,
      intercept_max: 8,
      coord_min: -8,
      coord_max: 8,
    },
    hard: {
      slope_min: -10,
      slope_max: 10,
      intercept_min: -12,
      intercept_max: 12,
      coord_min: -12,
      coord_max: 12,
    },
  },
  coordinate_plane: {
    easy: { coord_min: -5, coord_max: 5 },
    medium: { coord_min: -8, coord_max: 8 },
    hard: { coord_min: -12, coord_max: 12 },
  },
  number_line: {
    easy: { number_line_min: -8, number_line_max: 8 },
    medium: { number_line_min: -12, number_line_max: 12 },
    hard: { number_line_min: -20, number_line_max: 20 },
  },
  systems: {
    easy: { coef_min: -5, coef_max: 5, integer_only: true },
    medium: { coef_min: -10, coef_max: 10, integer_only: true },
    hard: { coef_min: -15, coef_max: 15, integer_only: false },
  },
  quadratic: {
    easy: { coef_min: -5, coef_max: 5, integer_only: true, ...COMMON_TERMS.easy },
    medium: { coef_min: -10, coef_max: 10, integer_only: true, ...COMMON_TERMS.medium },
    hard: { coef_min: -15, coef_max: 15, integer_only: false, ...COMMON_TERMS.hard },
  },
  radical: {
    easy: { coef_min: 1, coef_max: 10, ...COMMON_TERMS.easy },
    medium: { coef_min: 1, coef_max: 20, ...COMMON_TERMS.medium },
    hard: { coef_min: 1, coef_max: 40, ...COMMON_TERMS.hard },
  },
  geometry: {
    easy: { side_min: 3, side_max: 12, angle_min: 20, angle_max: 120 },
    medium: { side_min: 3, side_max: 20, angle_min: 10, angle_max: 170 },
    hard: { side_min: 5, side_max: 40, angle_min: 5, angle_max: 175 },
  },
  geometry_basic: {
    easy: { side_min: 3, side_max: 12 },
    medium: { side_min: 3, side_max: 20 },
    hard: { side_min: 5, side_max: 40 },
  },
  geometry_angles: {
    easy: { angle_min: 20, angle_max: 120 },
    medium: { angle_min: 10, angle_max: 170 },
    hard: { angle_min: 5, angle_max: 175 },
  },
  geometry_triangles: {
    easy: { side_min: 3, side_max: 12, angle_min: 20, angle_max: 120 },
    medium: { side_min: 3, side_max: 20, angle_min: 10, angle_max: 170 },
    hard: { side_min: 5, side_max: 40, angle_min: 5, angle_max: 175 },
  },
  geometry_circles: {
    easy: { side_min: 3, side_max: 12 },
    medium: { side_min: 3, side_max: 20 },
    hard: { side_min: 5, side_max: 40 },
  },
  word_problem: {
    easy: { difficulty: "easy", ...COMMON_TERMS.easy },
    medium: { difficulty: "medium", ...COMMON_TERMS.medium },
    hard: { difficulty: "hard", ...COMMON_TERMS.hard },
  },
  common_enrichment: { ...COMMON_TERMS },
};

/** Optional per-type overrides (wins over profile presets). */
export const GENERATOR_DIFFICULTY_PRESETS: Record<string, TierPresets> = {};

function normalizeTier(tier: string | number | boolean): DifficultyTier | null {
  const value = String(tier).trim().toLowerCase();
  if (value === "easy" || value === "medium" || value === "hard") {
    return value;
  }
  return null;
}

export function lookupDifficultyPreset(
  tier: string | number | boolean,
  options?: { typeId?: string | null; settingProfile?: string | null },
): PresetValues {
  const normalized = normalizeTier(tier);
  if (!normalized) return {};

  const typeId = options?.typeId ?? null;
  if (typeId) {
    const generatorPresets = GENERATOR_DIFFICULTY_PRESETS[typeId];
    if (generatorPresets?.[normalized]) {
      return { ...generatorPresets[normalized] };
    }
  }

  const profile = options?.settingProfile ?? null;
  if (profile) {
    const profilePresets = PROFILE_DIFFICULTY_PRESETS[profile];
    if (profilePresets?.[normalized]) {
      return { ...profilePresets[normalized] };
    }
  }

  return { ...(PROFILE_DIFFICULTY_PRESETS.common_enrichment?.[normalized] ?? {}) };
}

/**
 * Apply a difficulty preset onto current settings.
 * Only keys present in `allowedKeys` (usually the type's settings schema) are written.
 */
export function applyDifficultyPresetToSettings(
  values: Record<string, string | number | boolean>,
  tier: string | number | boolean,
  options?: {
    typeId?: string | null;
    settingProfile?: string | null;
    allowedKeys?: Iterable<string>;
  },
): Record<string, string | number | boolean> {
  const normalized = normalizeTier(tier);
  if (!normalized) {
    return { ...values, difficulty_tier: String(tier) };
  }

  const preset = lookupDifficultyPreset(normalized, {
    typeId: options?.typeId,
    settingProfile: options?.settingProfile,
  });

  const allowed = options?.allowedKeys ? new Set(options.allowedKeys) : null;
  const applied: Record<string, string | number | boolean> = {
    difficulty_tier: normalized,
  };

  for (const [key, value] of Object.entries(preset)) {
    if (allowed && !allowed.has(key)) continue;
    applied[key] = value;
  }

  return { ...values, ...applied };
}
