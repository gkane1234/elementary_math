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
    easy: {
      coef_min: -5,
      coef_max: 5,
      integer_only: true,
      steps: 1,
      compound_style: "mixed",
      allow_inclusive: false,
      allow_lt: true,
      allow_gt: true,
      allow_lte: false,
      allow_gte: false,
    },
    medium: {
      coef_min: -12,
      coef_max: 12,
      integer_only: true,
      steps: 2,
      compound_style: "mixed",
      allow_inclusive: true,
      allow_lt: true,
      allow_gt: true,
      allow_lte: true,
      allow_gte: true,
    },
    hard: {
      coef_min: -20,
      coef_max: 20,
      integer_only: false,
      steps: 3,
      compound_style: "mixed",
      allow_inclusive: true,
      allow_lt: true,
      allow_gt: true,
      allow_lte: true,
      allow_gte: true,
    },
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
  // Factoring pedagogy:
  //   easy   — monic quadratics (a = 1) via normal factoring
  //   medium — non-monic quadratics (a ≠ 1) via normal factoring
  //   hard   — non-quadratic techniques (grouping, cubes, substitution)
  polynomial_factoring: {
    easy: {
      coef_min: -5,
      coef_max: 5,
      min_degree: 2,
      max_degree: 2,
      leading_coefficient_one: true,
      monic_only: true,
      factor_normal: true,
      factor_grouping: false,
      factor_substitution: false,
      factor_difference_of_squares: false,
      factor_perfect_square_trinomial: false,
      factor_difference_of_cubes: false,
      factor_sum_of_cubes: false,
      factor_rrt: false,
      require_gcf: false,
      difference_of_squares_only: false,
    },
    medium: {
      coef_min: -10,
      coef_max: 10,
      min_degree: 2,
      max_degree: 2,
      leading_coefficient_one: false,
      monic_only: false,
      factor_normal: true,
      factor_grouping: false,
      factor_substitution: false,
      factor_difference_of_squares: false,
      factor_perfect_square_trinomial: false,
      factor_difference_of_cubes: false,
      factor_sum_of_cubes: false,
      factor_rrt: false,
      require_gcf: false,
      difference_of_squares_only: false,
    },
    hard: {
      coef_min: -12,
      coef_max: 12,
      min_degree: 3,
      max_degree: 4,
      leading_coefficient_one: false,
      monic_only: false,
      factor_normal: false,
      factor_grouping: true,
      factor_substitution: true,
      factor_difference_of_squares: false,
      factor_perfect_square_trinomial: false,
      factor_difference_of_cubes: true,
      factor_sum_of_cubes: true,
      factor_rrt: false,
      require_gcf: false,
      difference_of_squares_only: false,
    },
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
  scientific_notation: {
    easy: {
      sci_exp_min: 1,
      sci_exp_max: 3,
      allow_negative_exponents: false,
      mantissa_decimals: 1,
      sci_write_direction: "to_sci",
      sci_operation: "multiply",
      require_normalization: false,
      sci_exp_diff_min: 0,
      sci_exp_diff_max: 0,
      allow_magnitude_compare: false,
    },
    medium: {
      sci_exp_min: -4,
      sci_exp_max: 6,
      allow_negative_exponents: true,
      mantissa_decimals: 2,
      sci_write_direction: "both",
      sci_operation: "mixed",
      require_normalization: true,
      sci_exp_diff_min: 1,
      sci_exp_diff_max: 2,
      allow_magnitude_compare: false,
    },
    hard: {
      sci_exp_min: -10,
      sci_exp_max: 10,
      allow_negative_exponents: true,
      mantissa_decimals: 3,
      sci_write_direction: "both",
      sci_operation: "mixed",
      require_normalization: true,
      sci_exp_diff_min: 3,
      sci_exp_diff_max: 6,
      allow_magnitude_compare: true,
    },
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
  more_on_slope: {
    easy: {
      slope_min: -3,
      slope_max: 3,
      intercept_min: -5,
      intercept_max: 5,
      coord_min: -5,
      coord_max: 5,
      ask_mode: "mixed",
      allow_from_points: true,
      allow_from_equation: true,
      allow_from_graph: true,
      allow_find_equation: false,
      allow_classify: true,
      allow_parallel_perpendicular: false,
      show_points: false,
    },
    medium: {
      slope_min: -6,
      slope_max: 6,
      intercept_min: -8,
      intercept_max: 8,
      coord_min: -8,
      coord_max: 8,
      ask_mode: "mixed",
      allow_from_points: true,
      allow_from_equation: true,
      allow_from_graph: true,
      allow_find_equation: true,
      allow_classify: true,
      allow_parallel_perpendicular: true,
      show_points: false,
    },
    hard: {
      slope_min: -10,
      slope_max: 10,
      intercept_min: -12,
      intercept_max: 12,
      coord_min: -12,
      coord_max: 12,
      ask_mode: "mixed",
      allow_from_points: true,
      allow_from_equation: true,
      allow_from_graph: true,
      allow_find_equation: true,
      allow_classify: true,
      allow_parallel_perpendicular: true,
      show_points: false,
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
    easy: {
      coef_min: -5,
      coef_max: 5,
      integer_only: true,
      system_coef_min: 1,
      system_coef_max: 5,
      max_coefficient_magnitude: 5,
      prefer_integer_solutions: true,
    },
    medium: {
      coef_min: -10,
      coef_max: 10,
      integer_only: true,
      system_coef_min: 1,
      system_coef_max: 10,
      max_coefficient_magnitude: 10,
      prefer_integer_solutions: true,
    },
    hard: {
      coef_min: -15,
      coef_max: 15,
      integer_only: false,
      system_coef_min: 1,
      system_coef_max: 15,
      max_coefficient_magnitude: 15,
      prefer_integer_solutions: true,
    },
  },
  graphing: {
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
  // Quadratic solve / analyze types (formula, square roots, discriminant, CTS, …):
  //   easy   — monic (a = 1); smaller coeffs; simpler discriminants/roots
  //   medium — a may be ≠ 1; wider integer coeffs
  //   hard   — a often ≠ 1; wider / messier (non-integer allowed)
  quadratic: {
    easy: {
      coef_min: -5,
      coef_max: 5,
      integer_only: true,
      leading_coefficient_one: true,
      monic_only: true,
      ...COMMON_TERMS.easy,
    },
    medium: {
      coef_min: -10,
      coef_max: 10,
      integer_only: true,
      leading_coefficient_one: false,
      monic_only: false,
      ...COMMON_TERMS.medium,
    },
    hard: {
      coef_min: -15,
      coef_max: 15,
      integer_only: false,
      leading_coefficient_one: false,
      monic_only: false,
      ...COMMON_TERMS.hard,
    },
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
  exponential: {
    easy: { exp_base_min: 2, exp_base_max: 5, exp_exponent_max: 3 },
    medium: { exp_base_min: 2, exp_base_max: 8, exp_exponent_max: 4 },
    hard: { exp_base_min: 2, exp_base_max: 12, exp_exponent_max: 5 },
  },
  exponential_graph: {
    easy: {
      exp_base_min: 2,
      exp_base_max: 3,
      allow_decay: false,
      allow_stretch: false,
      allow_vertical_shift: false,
      allow_horizontal_shift: false,
      allow_reflection: false,
      coord_min: -5,
      coord_max: 5,
    },
    medium: {
      exp_base_min: 2,
      exp_base_max: 4,
      allow_decay: true,
      allow_stretch: true,
      allow_vertical_shift: true,
      allow_horizontal_shift: true,
      allow_reflection: false,
      coord_min: -6,
      coord_max: 6,
    },
    hard: {
      exp_base_min: 2,
      exp_base_max: 5,
      allow_decay: true,
      allow_stretch: true,
      allow_vertical_shift: true,
      allow_horizontal_shift: true,
      allow_reflection: true,
      coord_min: -8,
      coord_max: 8,
    },
  },
  absolute_value_graph: {
    easy: {
      allow_shift_h: true,
      allow_shift_k: false,
      allow_stretch: false,
      allow_reflection: false,
      coef_min: 1,
      coef_max: 1,
      integer_only: true,
      coord_min: -5,
      coord_max: 5,
      intercept_min: 0,
      intercept_max: 0,
    },
    medium: {
      allow_shift_h: true,
      allow_shift_k: true,
      allow_stretch: true,
      allow_reflection: true,
      coef_min: -2,
      coef_max: 2,
      integer_only: true,
      coord_min: -6,
      coord_max: 6,
      intercept_min: -5,
      intercept_max: 5,
    },
    hard: {
      allow_shift_h: true,
      allow_shift_k: true,
      allow_stretch: true,
      allow_reflection: true,
      coef_min: -3,
      coef_max: 3,
      integer_only: false,
      coord_min: -8,
      coord_max: 8,
      intercept_min: -8,
      intercept_max: 8,
    },
  },
  // Graphing quadratics (forms + transforms):
  //   easy   — clean vertex; a = 1; one-axis shift; no rewrite
  //   medium — mix vertex / standard / factored; a≠1 sometimes; light messy
  //   hard   — often messy (needs algebra); fractional a; wider h/k
  quadratic_graph: {
    easy: {
      allow_vertex_form: true,
      allow_standard_form: false,
      allow_factored_form: false,
      allow_messy_form: false,
      allow_shift_h: true,
      allow_shift_k: true,
      allow_stretch: false,
      allow_reflection: false,
      coef_min: 1,
      coef_max: 1,
      integer_only: true,
      leading_coefficient_one: true,
      monic_only: true,
      coord_min: -3,
      coord_max: 3,
      intercept_min: -3,
      intercept_max: 3,
    },
    medium: {
      allow_vertex_form: true,
      allow_standard_form: true,
      allow_factored_form: true,
      allow_messy_form: true,
      allow_shift_h: true,
      allow_shift_k: true,
      allow_stretch: true,
      allow_reflection: true,
      coef_min: -2,
      coef_max: 2,
      integer_only: true,
      leading_coefficient_one: false,
      monic_only: false,
      coord_min: -5,
      coord_max: 5,
      intercept_min: -5,
      intercept_max: 5,
    },
    hard: {
      allow_vertex_form: true,
      allow_standard_form: true,
      allow_factored_form: true,
      allow_messy_form: true,
      allow_shift_h: true,
      allow_shift_k: true,
      allow_stretch: true,
      allow_reflection: true,
      coef_min: -3,
      coef_max: 3,
      integer_only: false,
      leading_coefficient_one: false,
      monic_only: false,
      coord_min: -8,
      coord_max: 8,
      intercept_min: -8,
      intercept_max: 8,
    },
  },
  // Solve polynomials by graphing:
  //   easy   — monic (a=1); small integer roots
  //   medium — a ≠ 1 allowed; wider roots; factored prompts ok
  //   hard   — stretch/reflection; optional cubic; wider root range
  polynomial_solve_graph: {
    easy: {
      leading_coefficient_one: true,
      monic_only: true,
      allow_stretch: false,
      allow_reflection: false,
      allow_factored_form: false,
      coef_min: 1,
      coef_max: 1,
      root_min: -3,
      root_max: 3,
      min_degree: 2,
      max_degree: 2,
      integer_only: true,
      coord_min: -5,
      coord_max: 5,
    },
    medium: {
      leading_coefficient_one: false,
      monic_only: false,
      allow_stretch: true,
      allow_reflection: true,
      allow_factored_form: true,
      coef_min: -3,
      coef_max: 3,
      root_min: -5,
      root_max: 5,
      min_degree: 2,
      max_degree: 2,
      integer_only: true,
      coord_min: -8,
      coord_max: 8,
    },
    hard: {
      leading_coefficient_one: false,
      monic_only: false,
      allow_stretch: true,
      allow_reflection: true,
      allow_factored_form: true,
      coef_min: -4,
      coef_max: 4,
      root_min: -7,
      root_max: 7,
      min_degree: 2,
      max_degree: 3,
      integer_only: true,
      coord_min: -10,
      coord_max: 10,
    },
  },
  // Graphing quadratic inequalities (forms + symbols):
  //   easy   — clean vertex or standard; a=1; < / > only
  //   medium — factored / expand / light messy; a≠1; ≤ ≥ unlocked
  //   hard   — messy rewrite + CTS standard; fractional a
  quadratic_inequality_graph: {
    easy: {
      allow_vertex_form: true,
      allow_standard_form: true,
      allow_factored_form: false,
      allow_messy_form: false,
      allow_shift_h: true,
      allow_shift_k: true,
      allow_stretch: false,
      allow_reflection: false,
      coef_min: 1,
      coef_max: 1,
      integer_only: true,
      leading_coefficient_one: true,
      monic_only: true,
      coord_min: -3,
      coord_max: 3,
      intercept_min: -3,
      intercept_max: 3,
      allow_lt: true,
      allow_gt: true,
      allow_lte: false,
      allow_gte: false,
    },
    medium: {
      allow_vertex_form: true,
      allow_standard_form: true,
      allow_factored_form: true,
      allow_messy_form: true,
      allow_shift_h: true,
      allow_shift_k: true,
      allow_stretch: true,
      allow_reflection: true,
      coef_min: -2,
      coef_max: 2,
      integer_only: true,
      leading_coefficient_one: false,
      monic_only: false,
      coord_min: -5,
      coord_max: 5,
      intercept_min: -5,
      intercept_max: 5,
      allow_lt: true,
      allow_gt: true,
      allow_lte: true,
      allow_gte: true,
    },
    hard: {
      allow_vertex_form: true,
      allow_standard_form: true,
      allow_factored_form: true,
      allow_messy_form: true,
      allow_shift_h: true,
      allow_shift_k: true,
      allow_stretch: true,
      allow_reflection: true,
      coef_min: -3,
      coef_max: 3,
      integer_only: false,
      leading_coefficient_one: false,
      monic_only: false,
      coord_min: -8,
      coord_max: 8,
      intercept_min: -8,
      intercept_max: 8,
      allow_lt: true,
      allow_gt: true,
      allow_lte: true,
      allow_gte: true,
    },
  },
  number_sets: {
    easy: {
      ask_mode: "classify",
      include_natural: true,
      include_whole: true,
      include_integer: true,
      include_rational: false,
      include_irrational: false,
      include_real: false,
      allow_negative: true,
      allow_fractions: false,
      allow_irrationals: false,
      num_min: -10,
      num_max: 10,
    },
    medium: {
      ask_mode: "mixed",
      include_natural: true,
      include_whole: true,
      include_integer: true,
      include_rational: true,
      include_irrational: false,
      include_real: true,
      allow_negative: true,
      allow_fractions: true,
      allow_irrationals: false,
      num_min: -12,
      num_max: 12,
    },
    hard: {
      ask_mode: "mixed",
      include_natural: true,
      include_whole: true,
      include_integer: true,
      include_rational: true,
      include_irrational: true,
      include_real: true,
      allow_negative: true,
      allow_fractions: true,
      allow_irrationals: true,
      num_min: -20,
      num_max: 20,
    },
  },
  derivatives: {
    easy: { term_count: 2, power_max: 3, difficulty_tier: "easy" },
    medium: { term_count: 3, power_max: 4, difficulty_tier: "medium" },
    hard: { term_count: 4, power_max: 6, difficulty_tier: "hard" },
  },
  integrals: {
    easy: {
      term_count: 1,
      power_max: 3,
      require_positive_power: true,
      difficulty_tier: "easy",
    },
    medium: {
      term_count: 2,
      power_max: 4,
      require_positive_power: true,
      difficulty_tier: "medium",
    },
    hard: {
      term_count: 3,
      power_max: 5,
      require_positive_power: false,
      difficulty_tier: "hard",
    },
  },
  common_enrichment: { ...COMMON_TERMS },
};

const CONSECUTIVE_INTEGERS_TIERS: TierPresets = {
  easy: {
    difficulty: "easy",
    min_consecutive_count: 2,
    max_consecutive_count: 3,
    allow_consecutive_integers: true,
    allow_consecutive_even: false,
    allow_consecutive_odd: false,
    allow_sum_goal: true,
    allow_sum_first_last_goal: false,
    allow_product_goal: false,
  },
  medium: {
    difficulty: "medium",
    min_consecutive_count: 3,
    max_consecutive_count: 4,
    allow_consecutive_integers: true,
    allow_consecutive_even: true,
    allow_consecutive_odd: true,
    allow_sum_goal: true,
    allow_sum_first_last_goal: true,
    allow_product_goal: false,
  },
  hard: {
    difficulty: "hard",
    min_consecutive_count: 4,
    max_consecutive_count: 5,
    allow_consecutive_integers: true,
    allow_consecutive_even: true,
    allow_consecutive_odd: true,
    allow_sum_goal: true,
    allow_sum_first_last_goal: true,
    allow_product_goal: true,
  },
};

const EXPONENTIAL_GROWTH_DECAY_TIERS: TierPresets = {
  easy: {
    ask_mode: "find_final",
    allow_growth: true,
    allow_decay: true,
    rate_min: 5,
    rate_max: 10,
    periods_min: 2,
    periods_max: 4,
    discrete_only: true,
    allow_how_much_more: false,
    allow_compare: false,
    allow_threshold: false,
    allow_half_life: false,
    allow_fractional_periods: false,
  },
  medium: {
    ask_mode: "mixed",
    allow_growth: true,
    allow_decay: true,
    rate_min: 5,
    rate_max: 20,
    periods_min: 4,
    periods_max: 8,
    discrete_only: true,
    allow_how_much_more: true,
    allow_compare: false,
    allow_threshold: false,
    allow_half_life: false,
    allow_fractional_periods: false,
  },
  hard: {
    ask_mode: "mixed",
    allow_growth: true,
    allow_decay: true,
    rate_min: 3,
    rate_max: 25,
    periods_min: 5,
    periods_max: 12,
    discrete_only: true,
    allow_how_much_more: true,
    allow_compare: true,
    allow_threshold: true,
    allow_half_life: true,
    allow_fractional_periods: true,
  },
};

const DISTANCE_RATE_TIME_TIERS: TierPresets = {
  easy: {
    difficulty: "easy",
    allow_drt_find_missing: true,
    allow_drt_round_trip: false,
    allow_drt_two_segments: false,
    allow_drt_opposite: false,
    allow_drt_same_direction: false,
    allow_distance_mi: true,
    allow_distance_km: true,
    allow_distance_m: true,
    allow_distance_ft: true,
    allow_time_hr: true,
    allow_time_min: true,
  },
  medium: {
    difficulty: "medium",
    allow_drt_find_missing: true,
    allow_drt_round_trip: true,
    allow_drt_two_segments: true,
    allow_drt_opposite: false,
    allow_drt_same_direction: false,
    allow_distance_mi: true,
    allow_distance_km: true,
    allow_distance_m: true,
    allow_distance_ft: true,
    allow_time_hr: true,
    allow_time_min: true,
  },
  hard: {
    difficulty: "hard",
    allow_drt_find_missing: false,
    allow_drt_round_trip: true,
    allow_drt_two_segments: true,
    allow_drt_opposite: true,
    allow_drt_same_direction: true,
    allow_distance_mi: true,
    allow_distance_km: true,
    allow_distance_m: true,
    allow_distance_ft: true,
    allow_time_hr: true,
    allow_time_min: true,
  },
};

const WORK_PROBLEM_TIERS: TierPresets = {
  easy: {
    difficulty: "easy",
    allow_work_together: true,
    allow_work_find_one_rate: true,
    allow_work_three: false,
    allow_work_find_one_time: false,
    allow_work_starts_later: false,
    allow_work_pipes: false,
    allow_work_time_hr: true,
    allow_work_time_min: true,
  },
  medium: {
    difficulty: "medium",
    allow_work_together: false,
    allow_work_find_one_rate: false,
    allow_work_three: true,
    allow_work_find_one_time: true,
    allow_work_starts_later: false,
    allow_work_pipes: false,
    allow_work_time_hr: true,
    allow_work_time_min: true,
  },
  hard: {
    difficulty: "hard",
    allow_work_together: false,
    allow_work_find_one_rate: false,
    allow_work_three: false,
    allow_work_find_one_time: false,
    allow_work_starts_later: true,
    allow_work_pipes: true,
    allow_work_time_hr: true,
    allow_work_time_min: true,
  },
};

const POLYNOMIAL_MULTIPLY_TIERS: TierPresets = {
  easy: {
    coef_min: -5,
    coef_max: 5,
    min_degree: 1,
    max_degree: 2,
    integer_coefficients_only: true,
    allow_monomial_binomial: true,
    allow_binomial_binomial: true,
    allow_trinomial: false,
    leading_coefficient_one: true,
    max_factor_terms: 2,
  },
  medium: {
    coef_min: -9,
    coef_max: 9,
    min_degree: 1,
    max_degree: 3,
    integer_coefficients_only: true,
    allow_monomial_binomial: true,
    allow_binomial_binomial: true,
    allow_trinomial: true,
    leading_coefficient_one: false,
    max_factor_terms: 3,
  },
  hard: {
    coef_min: -12,
    coef_max: 12,
    min_degree: 2,
    max_degree: 5,
    integer_coefficients_only: true,
    allow_monomial_binomial: true,
    allow_binomial_binomial: true,
    allow_trinomial: true,
    leading_coefficient_one: false,
    max_factor_terms: 5,
  },
};

const FACTORING_COMMON_FACTOR_TIERS: TierPresets = {
  // GCF-only: remaining poly stays expanded; difficulty = GCF shape + degree.
  easy: {
    coef_min: -5,
    coef_max: 5,
    min_degree: 1,
    max_degree: 2,
    leading_coefficient_one: true,
    monic_only: true,
  },
  medium: {
    coef_min: -8,
    coef_max: 8,
    min_degree: 2,
    max_degree: 2,
    leading_coefficient_one: false,
    monic_only: false,
  },
  hard: {
    coef_min: -12,
    coef_max: 12,
    min_degree: 2,
    max_degree: 3,
    leading_coefficient_one: false,
    monic_only: false,
  },
};

const QUADRATIC_FACTORING_TIERS: TierPresets = {
  easy: {
    coef_min: -5,
    coef_max: 5,
    min_degree: 2,
    max_degree: 2,
    leading_coefficient_one: true,
    monic_only: true,
    factor_normal: true,
    factor_grouping: false,
    factor_substitution: false,
    factor_difference_of_squares: false,
    factor_perfect_square_trinomial: false,
    factor_difference_of_cubes: false,
    factor_sum_of_cubes: false,
    factor_rrt: false,
    require_gcf: false,
  },
  medium: {
    coef_min: -10,
    coef_max: 10,
    min_degree: 2,
    max_degree: 2,
    leading_coefficient_one: false,
    monic_only: false,
    factor_normal: true,
    factor_grouping: false,
    factor_substitution: false,
    factor_difference_of_squares: false,
    factor_perfect_square_trinomial: false,
    factor_difference_of_cubes: false,
    factor_sum_of_cubes: false,
    factor_rrt: false,
    require_gcf: false,
  },
  hard: {
    coef_min: -15,
    coef_max: 15,
    min_degree: 2,
    max_degree: 2,
    leading_coefficient_one: false,
    monic_only: false,
    factor_normal: true,
    factor_grouping: false,
    factor_substitution: false,
    factor_difference_of_squares: true,
    factor_perfect_square_trinomial: true,
    factor_difference_of_cubes: false,
    factor_sum_of_cubes: false,
    factor_rrt: false,
    require_gcf: false,
  },
};

const FACTORING_GROUPING_TIERS: TierPresets = {
  easy: {
    coef_min: -5,
    coef_max: 5,
    min_degree: 3,
    max_degree: 3,
    leading_coefficient_one: true,
    monic_only: true,
    factor_normal: false,
    factor_grouping: true,
    factor_substitution: false,
    factor_difference_of_squares: false,
    factor_perfect_square_trinomial: false,
    factor_difference_of_cubes: false,
    factor_sum_of_cubes: false,
    factor_rrt: false,
  },
  medium: {
    coef_min: -10,
    coef_max: 10,
    min_degree: 3,
    max_degree: 3,
    leading_coefficient_one: false,
    monic_only: false,
    factor_normal: false,
    factor_grouping: true,
    factor_substitution: false,
    factor_difference_of_squares: false,
    factor_perfect_square_trinomial: false,
    factor_difference_of_cubes: false,
    factor_sum_of_cubes: false,
    factor_rrt: false,
  },
  hard: {
    coef_min: -15,
    coef_max: 15,
    min_degree: 3,
    max_degree: 3,
    leading_coefficient_one: false,
    monic_only: false,
    factor_normal: false,
    factor_grouping: true,
    factor_substitution: false,
    factor_difference_of_squares: false,
    factor_perfect_square_trinomial: false,
    factor_difference_of_cubes: false,
    factor_sum_of_cubes: false,
    factor_rrt: false,
  },
};

const QUADRATIC_SOLVE_BY_GRAPH_TIERS: TierPresets = {
  easy: {
    leading_coefficient_one: true,
    monic_only: true,
    allow_stretch: false,
    allow_reflection: false,
    allow_factored_form: false,
    coef_min: 1,
    coef_max: 1,
    root_min: -3,
    root_max: 3,
    min_degree: 2,
    max_degree: 2,
    integer_only: true,
    coord_min: -5,
    coord_max: 5,
  },
  medium: {
    leading_coefficient_one: false,
    monic_only: false,
    allow_stretch: true,
    allow_reflection: true,
    allow_factored_form: true,
    coef_min: -3,
    coef_max: 3,
    root_min: -5,
    root_max: 5,
    min_degree: 2,
    max_degree: 2,
    integer_only: true,
    coord_min: -8,
    coord_max: 8,
  },
  hard: {
    leading_coefficient_one: false,
    monic_only: false,
    allow_stretch: true,
    allow_reflection: true,
    allow_factored_form: true,
    coef_min: -4,
    coef_max: 4,
    root_min: -7,
    root_max: 7,
    min_degree: 2,
    max_degree: 2,
    integer_only: true,
    coord_min: -10,
    coord_max: 10,
  },
};

const POLYNOMIAL_MULTIPLY_SPECIAL_TIERS: TierPresets = {
  easy: {
    coef_min: -5,
    coef_max: 5,
    leading_coefficient_one: true,
    monic_only: true,
  },
  medium: {
    coef_min: -9,
    coef_max: 9,
    leading_coefficient_one: true,
    monic_only: true,
  },
  hard: {
    coef_min: -12,
    coef_max: 12,
    leading_coefficient_one: false,
    monic_only: false,
  },
};

const FACTORING_EQUATIONS_TIERS: TierPresets = {
  easy: {
    coef_min: -5,
    coef_max: 5,
    leading_coefficient_one: true,
    monic_only: true,
    factor_normal: true,
    factor_grouping: false,
    factor_substitution: false,
    factor_difference_of_squares: false,
    factor_perfect_square_trinomial: false,
    factor_difference_of_cubes: false,
    factor_sum_of_cubes: false,
    factor_rrt: false,
  },
  medium: {
    coef_min: -10,
    coef_max: 10,
    leading_coefficient_one: false,
    monic_only: false,
    factor_normal: true,
    factor_grouping: false,
    factor_substitution: false,
    factor_difference_of_squares: false,
    factor_perfect_square_trinomial: false,
    factor_difference_of_cubes: false,
    factor_sum_of_cubes: false,
    factor_rrt: false,
  },
  hard: {
    coef_min: -15,
    coef_max: 15,
    leading_coefficient_one: false,
    monic_only: false,
    factor_normal: true,
    factor_grouping: false,
    factor_substitution: false,
    factor_difference_of_squares: true,
    factor_perfect_square_trinomial: true,
    factor_difference_of_cubes: false,
    factor_sum_of_cubes: false,
    factor_rrt: false,
  },
};

const SPECIAL_FACTORING_TIERS: TierPresets = {
  easy: {
    coef_min: -5,
    coef_max: 5,
    factor_difference_of_squares: true,
    factor_perfect_square_trinomial: true,
    factor_difference_of_cubes: false,
    factor_sum_of_cubes: false,
    allow_higher_even_powers: false,
    max_even_power: 4,
    require_gcf: false,
    leading_coefficient_one: true,
  },
  medium: {
    coef_min: -10,
    coef_max: 10,
    factor_difference_of_squares: true,
    factor_perfect_square_trinomial: true,
    factor_difference_of_cubes: true,
    factor_sum_of_cubes: true,
    allow_higher_even_powers: false,
    max_even_power: 4,
    require_gcf: false,
    leading_coefficient_one: false,
  },
  hard: {
    coef_min: -12,
    coef_max: 12,
    factor_difference_of_squares: true,
    factor_perfect_square_trinomial: true,
    factor_difference_of_cubes: true,
    factor_sum_of_cubes: true,
    allow_higher_even_powers: true,
    max_even_power: 8,
    require_gcf: false,
    leading_coefficient_one: false,
  },
};

/** Optional per-type overrides (wins over profile presets). */
export const GENERATOR_DIFFICULTY_PRESETS: Record<string, TierPresets> = {
  // Algebra 1 finding_angles: geometry relationships only (no inverse trig).
  // easy   — numeric complementary / supplementary / vertical / adjacent
  // medium — algebraic complementary / supplementary / vertical
  // hard   — triangle angle-sum / multi-step with algebra
  finding_angles: {
    easy: {
      angle_min: 20,
      angle_max: 120,
      coef_min: -3,
      coef_max: 3,
    },
    medium: {
      angle_min: 15,
      angle_max: 160,
      coef_min: -5,
      coef_max: 5,
    },
    hard: {
      angle_min: 10,
      angle_max: 170,
      coef_min: -6,
      coef_max: 6,
    },
  },
  // Always built from linear factors (then expanded).
  // easy   — GCF / obvious linear cancel
  // medium — difference of squares / easy trinomials
  // hard   — higher degree, more canceling; still factorable
  rational_simplification: {
    easy: {
      coef_min: -5,
      coef_max: 5,
      numerator_degree_min: 1,
      numerator_degree_max: 2,
      denominator_degree_min: 1,
      denominator_degree_max: 2,
      leading_coefficient_one: true,
      monic_only: true,
      allow_constant_gcf: true,
      prefer_difference_of_squares: false,
      max_cancel_factors: 1,
    },
    medium: {
      coef_min: -8,
      coef_max: 8,
      numerator_degree_min: 2,
      numerator_degree_max: 3,
      denominator_degree_min: 2,
      denominator_degree_max: 3,
      leading_coefficient_one: true,
      monic_only: true,
      allow_constant_gcf: false,
      prefer_difference_of_squares: true,
      max_cancel_factors: 1,
    },
    hard: {
      coef_min: -9,
      coef_max: 9,
      numerator_degree_min: 3,
      numerator_degree_max: 4,
      denominator_degree_min: 2,
      denominator_degree_max: 4,
      leading_coefficient_one: false,
      monic_only: false,
      allow_constant_gcf: false,
      prefer_difference_of_squares: true,
      max_cancel_factors: 2,
    },
  },
  polynomial_factoring_special_cases: SPECIAL_FACTORING_TIERS,
  consecutive_integers_word_problems: CONSECUTIVE_INTEGERS_TIERS,
  wp_consecutive_integers: CONSECUTIVE_INTEGERS_TIERS,
  distance_rate_time_word_problems: DISTANCE_RATE_TIME_TIERS,
  wp_distance_rate_time: DISTANCE_RATE_TIME_TIERS,
  a2_equations_and_inequalities_distance_rate_time_word_problems: DISTANCE_RATE_TIME_TIERS,
  work_word_problems: WORK_PROBLEM_TIERS,
  wp_work: WORK_PROBLEM_TIERS,
  a2_equations_and_inequalities_work_word_problems: WORK_PROBLEM_TIERS,
  polynomial_factoring_common_factor: FACTORING_COMMON_FACTOR_TIERS,
  quadratic_factoring: QUADRATIC_FACTORING_TIERS,
  polynomial_factoring_grouping: FACTORING_GROUPING_TIERS,
  a2_polynomial_functions_factoring_by_grouping: FACTORING_GROUPING_TIERS,
  polynomial_multiply_special: POLYNOMIAL_MULTIPLY_SPECIAL_TIERS,
  quadratic_factoring_equations: FACTORING_EQUATIONS_TIERS,
  a2_quadratic_functions_and_inequalities_solving_equations_by_factoring: FACTORING_EQUATIONS_TIERS,
  // Adding/subtracting rational expressions:
  //   easy   — exactly 2 terms; LCD is a single monomial/binomial
  //   medium — unlike non-monic binomials (2 terms) OR monic 3-term
  //   hard   — multi-factor LCDs, optional cancel/inflation, more terms
  rational_expression_simplification: {
    easy: {
      coef_min: -4,
      coef_max: 4,
      term_count: 2,
      denominator_degree_min: 1,
      denominator_degree_max: 1,
      leading_coefficient_one: true,
      monic_only: true,
      add_subtract_structure: "shared_lcd",
      max_lcd_factors: 1,
      prefer_simple_factors: true,
      content_primitive_denominators: true,
      allow_polynomial_terms: false,
      allow_full_lcd_terms: false,
      inflation_chance: 0,
      cancel_factor_count: "0",
      factor_rrt: false,
      force_lcd: false,
    },
    medium: {
      coef_min: -5,
      coef_max: 5,
      term_count: 3,
      denominator_degree_min: 1,
      denominator_degree_max: 1,
      leading_coefficient_one: false,
      monic_only: false,
      add_subtract_structure: "auto",
      max_lcd_factors: 2,
      prefer_simple_factors: true,
      content_primitive_denominators: true,
      allow_polynomial_terms: false,
      allow_full_lcd_terms: false,
      inflation_chance: 0,
      cancel_factor_count: "0",
      factor_rrt: false,
      force_lcd: false,
    },
    hard: {
      coef_min: -5,
      coef_max: 5,
      term_count: 3,
      denominator_degree_min: 1,
      denominator_degree_max: 2,
      leading_coefficient_one: false,
      monic_only: false,
      add_subtract_structure: "complex",
      max_lcd_factors: 3,
      prefer_simple_factors: true,
      content_primitive_denominators: true,
      allow_polynomial_terms: true,
      allow_full_lcd_terms: true,
      inflation_chance: 15,
      cancel_factor_count: "random",
      factor_rrt: false,
      force_lcd: false,
    },
  },
  // Solving by square roots:
  //   easy   — monic isolated squares only (x² = k / simple (x±h)²)
  //   medium — vertex form; a may be ≠ 1
  //   hard   — messy vertex (a≠1) and/or complete-the-square first
  quadratic_square_roots: {
    easy: {
      coef_min: -5,
      coef_max: 5,
      integer_only: true,
      leading_coefficient_one: true,
      monic_only: true,
      allow_isolated: true,
      allow_vertex: false,
      allow_complete_square: false,
    },
    medium: {
      coef_min: -8,
      coef_max: 8,
      integer_only: true,
      leading_coefficient_one: false,
      monic_only: false,
      allow_isolated: false,
      allow_vertex: true,
      allow_complete_square: false,
    },
    hard: {
      coef_min: -12,
      coef_max: 12,
      integer_only: false,
      leading_coefficient_one: false,
      monic_only: false,
      allow_isolated: false,
      allow_vertex: true,
      allow_complete_square: true,
    },
  },
  exponential_growth_decay: EXPONENTIAL_GROWTH_DECAY_TIERS,
  a2_exponential_and_logarithmic_expressions_discrete_exponential_growth_and_decay_word_problems:
    EXPONENTIAL_GROWTH_DECAY_TIERS,
  discrete_exponential_growth_and_decay_word_problems: EXPONENTIAL_GROWTH_DECAY_TIERS,
  polynomial_multiply: POLYNOMIAL_MULTIPLY_TIERS,
  pa_polynomials_multiplying: POLYNOMIAL_MULTIPLY_TIERS,
  a2_polynomial_functions_multiplying: POLYNOMIAL_MULTIPLY_TIERS,
  more_on_slope: {
    easy: {
      ask_mode: "mixed",
      allow_from_points: true,
      allow_from_equation: true,
      allow_from_graph: true,
      allow_find_equation: false,
      allow_classify: true,
      allow_parallel_perpendicular: false,
      show_points: false,
      slope_min: -3,
      slope_max: 3,
      intercept_min: -5,
      intercept_max: 5,
      coord_min: -5,
      coord_max: 5,
    },
    medium: {
      ask_mode: "mixed",
      allow_from_points: true,
      allow_from_equation: true,
      allow_from_graph: true,
      allow_find_equation: true,
      allow_classify: true,
      allow_parallel_perpendicular: true,
      show_points: false,
      slope_min: -6,
      slope_max: 6,
      intercept_min: -8,
      intercept_max: 8,
      coord_min: -8,
      coord_max: 8,
    },
    hard: {
      ask_mode: "mixed",
      allow_from_points: true,
      allow_from_equation: true,
      allow_from_graph: true,
      allow_find_equation: true,
      allow_classify: true,
      allow_parallel_perpendicular: true,
      show_points: false,
      slope_min: -10,
      slope_max: 10,
      intercept_min: -12,
      intercept_max: 12,
      coord_min: -12,
      coord_max: 12,
    },
  },
  absolute_value_equations: {
    easy: {
      coef_min: -5,
      coef_max: 5,
      integer_only: true,
      allow_basic: true,
      allow_isolated_right: true,
      allow_simple: true,
      allow_abs_plus_constant: false,
      allow_factored_inside: false,
      allow_coeff_outside: false,
      allow_abs_equals_abs: false,
      allow_abs_equals_linear: false,
    },
    medium: {
      coef_min: -12,
      coef_max: 12,
      integer_only: true,
      allow_basic: false,
      allow_isolated_right: false,
      allow_simple: false,
      allow_abs_plus_constant: true,
      allow_factored_inside: true,
      allow_coeff_outside: false,
      allow_abs_equals_abs: false,
      allow_abs_equals_linear: false,
    },
    hard: {
      coef_min: -20,
      coef_max: 20,
      integer_only: false,
      allow_basic: false,
      allow_isolated_right: false,
      allow_simple: false,
      allow_abs_plus_constant: false,
      allow_factored_inside: false,
      allow_coeff_outside: true,
      allow_abs_equals_abs: true,
      allow_abs_equals_linear: true,
    },
  },
  absolute_value_inequalities: {
    easy: {
      coef_min: -5,
      coef_max: 5,
      integer_only: true,
      allow_simple: true,
      allow_shifted: true,
      allow_linear: false,
      allow_abs_plus_constant: false,
      allow_abs_vs_linear: false,
      allow_lt: true,
      allow_gt: true,
      allow_lte: false,
      allow_gte: false,
    },
    medium: {
      coef_min: -12,
      coef_max: 12,
      integer_only: true,
      allow_simple: false,
      allow_shifted: false,
      allow_linear: true,
      allow_abs_plus_constant: false,
      allow_abs_vs_linear: false,
      allow_lt: true,
      allow_gt: true,
      allow_lte: true,
      allow_gte: true,
    },
    hard: {
      coef_min: -20,
      coef_max: 20,
      integer_only: false,
      allow_simple: false,
      allow_shifted: false,
      allow_linear: true,
      allow_abs_plus_constant: true,
      allow_abs_vs_linear: true,
      allow_lt: true,
      allow_gt: true,
      allow_lte: true,
      allow_gte: true,
    },
  },
  // Adding/subtracting radicals:
  //   easy   — already-simplified like radicals (2√3 + 5√3)
  //   medium — light simplify first (√12 + √3, √18 − √8)
  //   hard   — coefficients + larger perfect squares / more terms
  radical_add_subtract: {
    easy: {
      allow_like_radicals: true,
      allow_unsimplified_radicals: false,
      allow_coeff_unsimplified: false,
      coef_min: 1,
      coef_max: 6,
      min_terms: 2,
      max_terms: 2,
    },
    medium: {
      allow_like_radicals: false,
      allow_unsimplified_radicals: true,
      allow_coeff_unsimplified: false,
      coef_min: 1,
      coef_max: 1,
      min_terms: 2,
      max_terms: 2,
    },
    hard: {
      allow_like_radicals: false,
      allow_unsimplified_radicals: false,
      allow_coeff_unsimplified: true,
      coef_min: 1,
      coef_max: 8,
      min_terms: 3,
      max_terms: 4,
    },
  },
  // Dividing radicals:
  //   easy   — already-reduced quotients (√12/√3, 6√5/2√5)
  //   medium — simplify perfect squares / cancel after rewriting
  //   hard   — rationalize denominator + multi-factor coeffs
  radical_divide: {
    easy: {
      allow_reduced_quotients: true,
      allow_simplify_quotients: false,
      allow_rationalize_divide: false,
      coef_min: 1,
      coef_max: 6,
    },
    medium: {
      allow_reduced_quotients: false,
      allow_simplify_quotients: true,
      allow_rationalize_divide: false,
      coef_min: 1,
      coef_max: 3,
    },
    hard: {
      allow_reduced_quotients: false,
      allow_simplify_quotients: false,
      allow_rationalize_divide: true,
      coef_min: 1,
      coef_max: 8,
    },
  },
  // Multiplying radicals:
  //   easy   — √a · √b
  //   medium — k√a · m√b
  //   hard   — binomial FOIL
  radical_multiply: {
    easy: {
      allow_simple_product: true,
      allow_coeff_product: false,
      allow_binomial_product: false,
      coef_min: 1,
      coef_max: 4,
    },
    medium: {
      allow_simple_product: false,
      allow_coeff_product: true,
      allow_binomial_product: false,
      coef_min: 1,
      coef_max: 6,
    },
    hard: {
      allow_simple_product: false,
      allow_coeff_product: false,
      allow_binomial_product: true,
      coef_min: 1,
      coef_max: 5,
    },
  },
  radical_simplification: {
    easy: {
      radicand_min: 12,
      radicand_max: 96,
      require_simplifiable: true,
      radical_index: 2,
    },
    medium: {
      radicand_min: 48,
      radicand_max: 200,
      require_simplifiable: true,
      radical_index: 2,
    },
    hard: {
      radicand_min: 100,
      radicand_max: 400,
      require_simplifiable: true,
      radical_index: 2,
    },
  },
  complex_fractions: {
    easy: { coef_min: -5, coef_max: 5, difficulty_tier: "easy" },
    medium: { coef_min: -8, coef_max: 8, difficulty_tier: "medium" },
    hard: { coef_min: -10, coef_max: 10, difficulty_tier: "hard" },
  },
  // Rational expression multiply / divide:
  //   easy   — monic linears, one cancel, ÷ only for division
  //   medium — non-monic, 1–2 cancels, ÷ or slash
  //   hard   — expanded polys, 2 cancels, 3 factors, ÷ or complex fraction
  rational_expression_multiply_divide: {
    easy: {
      coef_min: -4,
      coef_max: 4,
      allow_multiply: true,
      allow_divide: true,
      cancel_factor_count: 1,
      max_factor_degree: 1,
      expand_polynomials: false,
      operand_count: 2,
      leading_coefficient_one: true,
      allow_obelus: true,
      allow_complex_fraction: false,
      allow_slash: false,
    },
    medium: {
      coef_min: -8,
      coef_max: 8,
      allow_multiply: true,
      allow_divide: true,
      cancel_factor_count: 2,
      max_factor_degree: 1,
      expand_polynomials: false,
      operand_count: 2,
      leading_coefficient_one: false,
      allow_obelus: true,
      allow_complex_fraction: false,
      allow_slash: true,
    },
    hard: {
      coef_min: -10,
      coef_max: 10,
      allow_multiply: true,
      allow_divide: true,
      cancel_factor_count: 2,
      max_factor_degree: 2,
      expand_polynomials: true,
      operand_count: 3,
      leading_coefficient_one: false,
      allow_obelus: true,
      allow_complex_fraction: true,
      allow_slash: false,
    },
  },
  // Radical equations:
  //   easy   — single radical; move/divide then square; occasional extraneous check
  //   medium — more algebra to isolate; √ = linear with checking
  //   hard   — two radicals (square more than once); nestier; designed extraneous
  radical_equations: {
    easy: {
      coef_min: -6,
      coef_max: 6,
      integer_only: true,
      allow_light_prep: true,
      allow_isolate_algebra: false,
      allow_radical_equals_linear: false,
      allow_two_radicals: false,
    },
    medium: {
      coef_min: -10,
      coef_max: 10,
      integer_only: true,
      allow_light_prep: false,
      allow_isolate_algebra: true,
      allow_radical_equals_linear: true,
      allow_two_radicals: false,
    },
    hard: {
      coef_min: -12,
      coef_max: 12,
      integer_only: true,
      allow_light_prep: false,
      allow_isolate_algebra: false,
      allow_radical_equals_linear: true,
      allow_two_radicals: true,
    },
  },
  // Rational equations:
  //   easy   — single fraction = constant (or simple proportion)
  //   medium — proportions + fraction plus constant
  //   hard   — two rational terms (LCD; extraneous checks)
  rational_equations: {
    easy: {
      coef_min: -6,
      coef_max: 6,
      integer_only: true,
      allow_simple_fraction: true,
      allow_proportion: true,
      allow_fraction_plus_constant: false,
      allow_two_fractions: false,
    },
    medium: {
      coef_min: -10,
      coef_max: 10,
      integer_only: true,
      allow_simple_fraction: false,
      allow_proportion: true,
      allow_fraction_plus_constant: true,
      allow_two_fractions: false,
    },
    hard: {
      coef_min: -12,
      coef_max: 12,
      integer_only: true,
      allow_simple_fraction: false,
      allow_proportion: false,
      allow_fraction_plus_constant: false,
      allow_two_fractions: true,
    },
  },
};

GENERATOR_DIFFICULTY_PRESETS.a2_equations_and_inequalities_absolute_value_equations =
  GENERATOR_DIFFICULTY_PRESETS.absolute_value_equations;
GENERATOR_DIFFICULTY_PRESETS.a2_equations_and_inequalities_absolute_value_inequalities =
  GENERATOR_DIFFICULTY_PRESETS.absolute_value_inequalities;
GENERATOR_DIFFICULTY_PRESETS.a2_quadratic_functions_and_inequalities_solving_equations_by_taking_square_roots =
  GENERATOR_DIFFICULTY_PRESETS.quadratic_square_roots;
GENERATOR_DIFFICULTY_PRESETS.solving_equations_by_taking_square_roots =
  GENERATOR_DIFFICULTY_PRESETS.quadratic_square_roots;
GENERATOR_DIFFICULTY_PRESETS.a2_polynomial_functions_factoring_sum_difference_of_cubes =
  GENERATOR_DIFFICULTY_PRESETS.polynomial_factoring_special_cases;
GENERATOR_DIFFICULTY_PRESETS.a2_quadratic_functions_and_inequalities_factoring_special_case_quadratic_expressions =
  GENERATOR_DIFFICULTY_PRESETS.polynomial_factoring_special_cases;
GENERATOR_DIFFICULTY_PRESETS.a2_polynomial_functions_conjugate_roots_and_factoring =
  GENERATOR_DIFFICULTY_PRESETS.polynomial_factoring_special_cases;
GENERATOR_DIFFICULTY_PRESETS.solve_polynomial_by_graphing =
  PROFILE_DIFFICULTY_PRESETS.polynomial_solve_graph;
GENERATOR_DIFFICULTY_PRESETS.quadratic_solve_by_graphing = QUADRATIC_SOLVE_BY_GRAPH_TIERS;
GENERATOR_DIFFICULTY_PRESETS.a2_quadratic_functions_and_inequalities_solving_equations_by_graphing =
  QUADRATIC_SOLVE_BY_GRAPH_TIERS;
GENERATOR_DIFFICULTY_PRESETS.a2_radical_functions_and_rational_exponents_adding_and_subtracting_radical_expressions =
  {
    easy: {
      ...GENERATOR_DIFFICULTY_PRESETS.radical_add_subtract.easy,
      coef_max: (Number(GENERATOR_DIFFICULTY_PRESETS.radical_add_subtract.easy.coef_max) || 6) + 2,
    },
    medium: {
      ...GENERATOR_DIFFICULTY_PRESETS.radical_add_subtract.medium,
      coef_max: (Number(GENERATOR_DIFFICULTY_PRESETS.radical_add_subtract.medium.coef_max) || 1) + 2,
    },
    hard: {
      ...GENERATOR_DIFFICULTY_PRESETS.radical_add_subtract.hard,
      coef_max: (Number(GENERATOR_DIFFICULTY_PRESETS.radical_add_subtract.hard.coef_max) || 8) + 2,
    },
  };
GENERATOR_DIFFICULTY_PRESETS.geo_review_adding_and_subtracting_square_roots = {
  easy: {
    allow_like_radicals: true,
    allow_unsimplified_radicals: false,
    allow_coeff_unsimplified: false,
    coef_min: 1,
    coef_max: 4,
    min_terms: 2,
    max_terms: 2,
  },
  medium: {
    allow_like_radicals: false,
    allow_unsimplified_radicals: true,
    allow_coeff_unsimplified: false,
    coef_min: 1,
    coef_max: 1,
    min_terms: 2,
    max_terms: 2,
  },
  hard: {
    allow_like_radicals: false,
    allow_unsimplified_radicals: false,
    allow_coeff_unsimplified: true,
    coef_min: 1,
    coef_max: 5,
    min_terms: 2,
    max_terms: 3,
  },
};
GENERATOR_DIFFICULTY_PRESETS.a2_radical_functions_and_rational_exponents_dividing_radical_expressions =
  GENERATOR_DIFFICULTY_PRESETS.radical_divide;
GENERATOR_DIFFICULTY_PRESETS.geo_review_dividing_square_roots = {
  easy: {
    allow_reduced_quotients: true,
    allow_simplify_quotients: false,
    allow_rationalize_divide: false,
    coef_min: 1,
    coef_max: 4,
  },
  medium: {
    allow_reduced_quotients: false,
    allow_simplify_quotients: true,
    allow_rationalize_divide: false,
    coef_min: 1,
    coef_max: 3,
  },
  hard: {
    allow_reduced_quotients: false,
    allow_simplify_quotients: true,
    allow_rationalize_divide: false,
    coef_min: 1,
    coef_max: 5,
  },
};
GENERATOR_DIFFICULTY_PRESETS.a2_radical_functions_and_rational_exponents_multiplying_radical_expressions =
  GENERATOR_DIFFICULTY_PRESETS.radical_multiply;
GENERATOR_DIFFICULTY_PRESETS.geo_review_multiplying_square_roots = {
  easy: {
    allow_simple_product: true,
    allow_coeff_product: false,
    allow_binomial_product: false,
    coef_min: 1,
    coef_max: 3,
  },
  medium: {
    allow_simple_product: false,
    allow_coeff_product: true,
    allow_binomial_product: false,
    coef_min: 1,
    coef_max: 4,
  },
  hard: {
    allow_simple_product: false,
    allow_coeff_product: true,
    allow_binomial_product: false,
    coef_min: 1,
    coef_max: 6,
  },
};
GENERATOR_DIFFICULTY_PRESETS.a2_radical_functions_and_rational_exponents_simplifying_radicals = {
  easy: { radicand_min: 18, radicand_max: 120, require_simplifiable: true, radical_index: 2 },
  medium: { radicand_min: 50, radicand_max: 250, require_simplifiable: true, radical_index: 2 },
  hard: { radicand_min: 120, radicand_max: 500, require_simplifiable: true, radical_index: 2 },
};
GENERATOR_DIFFICULTY_PRESETS.geo_review_simplifying_square_roots = {
  easy: { radicand_min: 8, radicand_max: 50, require_simplifiable: true, radical_index: 2 },
  medium: { radicand_min: 18, radicand_max: 120, require_simplifiable: true, radical_index: 2 },
  hard: { radicand_min: 48, radicand_max: 200, require_simplifiable: true, radical_index: 2 },
};
GENERATOR_DIFFICULTY_PRESETS.a2_rational_expressions_complex_fractions =
  GENERATOR_DIFFICULTY_PRESETS.complex_fractions;
GENERATOR_DIFFICULTY_PRESETS.a2_rational_expressions_multiplying_and_dividing =
  GENERATOR_DIFFICULTY_PRESETS.rational_expression_multiply_divide;
GENERATOR_DIFFICULTY_PRESETS.rational_expressions_multiplying_and_dividing =
  GENERATOR_DIFFICULTY_PRESETS.rational_expression_multiply_divide;
GENERATOR_DIFFICULTY_PRESETS.a2_rational_expressions_adding_and_subtracting =
  GENERATOR_DIFFICULTY_PRESETS.rational_expression_simplification;
GENERATOR_DIFFICULTY_PRESETS.rational_expressions_adding_and_subtracting =
  GENERATOR_DIFFICULTY_PRESETS.rational_expression_simplification;
GENERATOR_DIFFICULTY_PRESETS.a2_rational_expressions_simplifying =
  GENERATOR_DIFFICULTY_PRESETS.rational_simplification;
GENERATOR_DIFFICULTY_PRESETS.rational_expressions_simplifying =
  GENERATOR_DIFFICULTY_PRESETS.rational_simplification;
GENERATOR_DIFFICULTY_PRESETS.a2_radical_functions_and_rational_exponents_radical_equations =
  GENERATOR_DIFFICULTY_PRESETS.radical_equations;
GENERATOR_DIFFICULTY_PRESETS.a2_radical_functions_and_rational_exponents_rational_exponent_equations =
  GENERATOR_DIFFICULTY_PRESETS.radical_equations;
GENERATOR_DIFFICULTY_PRESETS.rational_expressions_equations =
  GENERATOR_DIFFICULTY_PRESETS.rational_equations;
GENERATOR_DIFFICULTY_PRESETS.a2_rational_expressions_equations = {
  easy: {
    coef_min: -8,
    coef_max: 8,
    integer_only: true,
    allow_simple_fraction: true,
    allow_proportion: true,
    allow_fraction_plus_constant: false,
    allow_two_fractions: false,
  },
  medium: {
    coef_min: -12,
    coef_max: 12,
    integer_only: true,
    allow_simple_fraction: false,
    allow_proportion: false,
    allow_fraction_plus_constant: true,
    allow_two_fractions: true,
  },
  hard: {
    coef_min: -15,
    coef_max: 15,
    integer_only: true,
    allow_simple_fraction: false,
    allow_proportion: false,
    allow_fraction_plus_constant: false,
    allow_two_fractions: true,
  },
};
GENERATOR_DIFFICULTY_PRESETS.pc_rational_equations =
  GENERATOR_DIFFICULTY_PRESETS.a2_rational_expressions_equations;

GENERATOR_DIFFICULTY_PRESETS.g6_numeric_expressions_and_order_of_operations = {
  easy: { pemdas_complexity: "basic", num_min: 1, num_max: 5 },
  medium: { pemdas_complexity: "basic", num_min: 2, num_max: 8 },
  hard: { pemdas_complexity: "mixed", num_min: 2, num_max: 9 },
};
const DECIMAL_MULTIPLICATION_TIERS: TierPresets = {
  easy: {
    whole_times_decimal: true,
    decimal_places: 1,
    max_decimal_places: 1,
    allow_negative: false,
  },
  medium: {
    whole_times_decimal: false,
    decimal_places: 2,
    max_decimal_places: 2,
    allow_negative: false,
  },
  hard: {
    whole_times_decimal: false,
    decimal_places: 3,
    max_decimal_places: 3,
    allow_negative: false,
  },
};
GENERATOR_DIFFICULTY_PRESETS.g6_decimal_multiplication = DECIMAL_MULTIPLICATION_TIERS;
GENERATOR_DIFFICULTY_PRESETS.g6_decimal_multiplication_with_equivalent_fractions =
  DECIMAL_MULTIPLICATION_TIERS;
GENERATOR_DIFFICULTY_PRESETS.g6_decimal_multiplication_with_area_diagrams =
  DECIMAL_MULTIPLICATION_TIERS;
const WHOLE_DIVIDE_TO_DECIMAL_TIERS: TierPresets = {
  easy: {
    decimal_places: 1,
    max_decimal_places: 1,
    allow_negative: false,
    num_min: 1,
    num_max: 20,
  },
  medium: {
    decimal_places: 2,
    max_decimal_places: 2,
    allow_negative: false,
    num_min: 1,
    num_max: 50,
  },
  hard: {
    decimal_places: 3,
    max_decimal_places: 3,
    allow_negative: false,
    num_min: 1,
    num_max: 200,
  },
};
GENERATOR_DIFFICULTY_PRESETS.g6_dividing_whole_numbers_that_result_in_decimals =
  WHOLE_DIVIDE_TO_DECIMAL_TIERS;
GENERATOR_DIFFICULTY_PRESETS.g6_distributive_property_numeric = {
  easy: { coef_min: 2, coef_max: 5, allow_negative: false },
  medium: { coef_min: 2, coef_max: 9, allow_negative: false },
  hard: { coef_min: 2, coef_max: 12, allow_negative: false },
};
GENERATOR_DIFFICULTY_PRESETS.g6_distributive_property_algebraic = {
  easy: { coef_min: 2, coef_max: 5, allow_negative: false },
  medium: { coef_min: 2, coef_max: 8, allow_negative: false },
  hard: { coef_min: -5, coef_max: 9, allow_negative: true },
};
GENERATOR_DIFFICULTY_PRESETS.distributive_property_algebraic =
  GENERATOR_DIFFICULTY_PRESETS.g6_distributive_property_algebraic;
GENERATOR_DIFFICULTY_PRESETS.g6_distances_on_the_coordinate_plane = {
  easy: { coord_min: -5, coord_max: 5, integer_coordinates: true, axis_aligned_only: true },
  medium: { coord_min: -8, coord_max: 8, integer_coordinates: true, axis_aligned_only: true },
  hard: { coord_min: -10, coord_max: 10, integer_coordinates: true, axis_aligned_only: true },
};
GENERATOR_DIFFICULTY_PRESETS.g6_fraction_multiply = {
  easy: {
    num_min: 1,
    num_max: 5,
    denom_min: 2,
    denom_max: 6,
    coef_min: 1,
    coef_max: 5,
    allow_negative: false,
    allow_mixed: false,
    require_proper: true,
  },
  medium: {
    num_min: 1,
    num_max: 12,
    denom_min: 2,
    denom_max: 12,
    coef_min: 1,
    coef_max: 12,
    allow_negative: false,
    allow_mixed: true,
    require_proper: false,
  },
  hard: {
    num_min: 5,
    num_max: 50,
    denom_min: 8,
    denom_max: 50,
    coef_min: 5,
    coef_max: 50,
    allow_negative: false,
    allow_mixed: true,
    require_proper: false,
  },
};
GENERATOR_DIFFICULTY_PRESETS.rational_multiply =
  GENERATOR_DIFFICULTY_PRESETS.g6_fraction_multiply;
const FRACTION_DIVIDE_WORD_TIERS: TierPresets = {
  easy: {
    num_min: 2,
    num_max: 12,
    denom_min: 2,
    denom_max: 6,
    coef_min: 2,
    coef_max: 12,
    allow_negative: false,
    allow_mixed: false,
    require_proper: false,
    dividend_form: "whole",
    divisor_form: "whole",
    require_whole_quotient: true,
    require_non_whole_quotient: false,
  },
  medium: {
    num_min: 1,
    num_max: 12,
    denom_min: 2,
    denom_max: 8,
    coef_min: 1,
    coef_max: 12,
    allow_negative: false,
    allow_mixed: true,
    require_proper: false,
    dividend_form: "whole",
    divisor_form: "any",
    require_whole_quotient: false,
    require_non_whole_quotient: false,
  },
  hard: {
    num_min: 1,
    num_max: 15,
    denom_min: 2,
    denom_max: 12,
    coef_min: 1,
    coef_max: 15,
    allow_negative: false,
    allow_mixed: true,
    require_proper: false,
    dividend_form: "fraction",
    divisor_form: "fraction",
    require_whole_quotient: false,
    require_non_whole_quotient: false,
  },
};
GENERATOR_DIFFICULTY_PRESETS.g6_how_many_groups_times = FRACTION_DIVIDE_WORD_TIERS;
GENERATOR_DIFFICULTY_PRESETS.g6_how_much_in_each_group_time = FRACTION_DIVIDE_WORD_TIERS;
GENERATOR_DIFFICULTY_PRESETS.g6_fraction_divide_groups = FRACTION_DIVIDE_WORD_TIERS;
GENERATOR_DIFFICULTY_PRESETS.g6_fraction_divide_each = FRACTION_DIVIDE_WORD_TIERS;
GENERATOR_DIFFICULTY_PRESETS.g6_factoring = {
  easy: {
    prime_factor_count_min: 2,
    prime_factor_count_max: 2,
    prime_max: 7,
    factor_product_max: 50,
  },
  medium: {
    prime_factor_count_min: 2,
    prime_factor_count_max: 4,
    prime_max: 11,
    factor_product_max: 200,
  },
  hard: {
    prime_factor_count_min: 3,
    prime_factor_count_max: 6,
    prime_max: 19,
    factor_product_max: 999,
  },
};
GENERATOR_DIFFICULTY_PRESETS.pa_factoring = GENERATOR_DIFFICULTY_PRESETS.g6_factoring;
const LONG_DIVISION_REMAINDER_TIERS: TierPresets = {
  easy: {
    dividend_min: 10,
    dividend_max: 99,
    divisor_min: 2,
    divisor_max: 9,
    allow_negative: false,
  },
  medium: {
    dividend_min: 100,
    dividend_max: 999,
    divisor_min: 2,
    divisor_max: 9,
    allow_negative: false,
  },
  hard: {
    dividend_min: 1000,
    dividend_max: 10000,
    divisor_min: 2,
    divisor_max: 49,
    allow_negative: false,
  },
};
GENERATOR_DIFFICULTY_PRESETS.g6_long_division_with_remainders =
  LONG_DIVISION_REMAINDER_TIERS;
GENERATOR_DIFFICULTY_PRESETS.g6_shapes_and_perimeter_on_the_coordinate_plane = {
  easy: { coord_min: 0, coord_max: 6, max_side: 4, allow_l_shape: false },
  medium: { coord_min: -3, coord_max: 7, max_side: 5, allow_l_shape: false },
  hard: { coord_min: -5, coord_max: 8, max_side: 6, allow_l_shape: true },
};
GENERATOR_DIFFICULTY_PRESETS.g6_coordinate_perimeter =
  GENERATOR_DIFFICULTY_PRESETS.g6_shapes_and_perimeter_on_the_coordinate_plane;
GENERATOR_DIFFICULTY_PRESETS.g6_equations_tape_diagrams = {
  easy: { tape_style: "uniform", difficulty_tier: "easy" },
  medium: { tape_style: "mixed", difficulty_tier: "medium" },
  hard: { tape_style: "nonuniform", difficulty_tier: "hard" },
};
GENERATOR_DIFFICULTY_PRESETS.pa_integers_adding_and_subtracting = {
  easy: { num_min: -10, num_max: 10, allow_negative: true },
  medium: { num_min: -20, num_max: 20, allow_negative: true },
  hard: { num_min: -50, num_max: 50, allow_negative: true },
};
GENERATOR_DIFFICULTY_PRESETS.pa_integers_multiplying =
  GENERATOR_DIFFICULTY_PRESETS.pa_integers_adding_and_subtracting;
GENERATOR_DIFFICULTY_PRESETS.pa_integers_dividing =
  GENERATOR_DIFFICULTY_PRESETS.pa_integers_adding_and_subtracting;
GENERATOR_DIFFICULTY_PRESETS.find_missing_sides_of_triangles = {
  easy: { side_min: 3, side_max: 12, integer_only: true },
  medium: { side_min: 3, side_max: 20, integer_only: true },
  hard: { side_min: 5, side_max: 30, integer_only: false },
};
GENERATOR_DIFFICULTY_PRESETS.finding_sine_cosine_tangent =
  GENERATOR_DIFFICULTY_PRESETS.find_missing_sides_of_triangles;

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
