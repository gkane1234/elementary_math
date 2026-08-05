/**
 * Client-side mirror of ``structure_moves.approx_max_d`` for settings UI.
 * This is the **conceptual** ceiling only — Spec difficulty is independent
 * and unbounded. Keep weights in sync with
 * question_engine/frameworks/primitives/structure_moves.py.
 */

const PEDAGOGICAL_MAX_D = 25;
const STRUCTURAL_SHARE = 0.72;
const ALLOW_SHARE = 0.28;

const ALLOW_BONUS: Record<string, number> = {
  allow_trig: 3,
  allow_exp: 3,
  allow_log: 2.5,
  allow_roots: 2,
  allow_invtrig: 3,
  allow_triple_product: 2,
  allow_one_sided: 1,
};

/** Leaf → allow_* knobs that participate in approx max (generator_key or type family). */
const LEAF_ALLOW_KEYS: Record<string, string[]> = {
  limit_direct_evaluation: [
    "allow_trig",
    "allow_exp",
    "allow_log",
    "allow_roots",
    "allow_invtrig",
  ],
  limit_removable: ["allow_roots"],
  limit_jump: ["allow_trig", "allow_exp", "allow_log", "allow_roots", "allow_one_sided"],
  limit_essential: ["allow_trig", "allow_exp"],
  limit_continuity: ["allow_trig", "allow_exp", "allow_log", "allow_roots"],
  limit_at_infinity: ["allow_trig", "allow_exp", "allow_log", "allow_invtrig"],
  lhopitals_rule: ["allow_trig", "allow_exp", "allow_log", "allow_invtrig"],
  derivative_power_rule: ["allow_roots"],
  derivative_product_rule: [
    "allow_trig",
    "allow_exp",
    "allow_log",
    "allow_roots",
    "allow_invtrig",
    "allow_triple_product",
  ],
  derivative_quotient_rule: [
    "allow_trig",
    "allow_exp",
    "allow_log",
    "allow_roots",
    "allow_invtrig",
  ],
  derivative_chain_rule: [
    "allow_trig",
    "allow_exp",
    "allow_log",
    "allow_roots",
    "allow_invtrig",
  ],
  derivative_trigonometric: ["allow_trig"],
  derivative_ln_exp: ["allow_exp", "allow_log"],
  derivative_inverse_trig: ["allow_invtrig"],
  derivative_higher_order: ["allow_trig", "allow_exp", "allow_log"],
  derivative_general: [
    "allow_trig",
    "allow_exp",
    "allow_log",
    "allow_roots",
    "allow_invtrig",
    "allow_triple_product",
  ],
  integral_power_rule: ["allow_roots"],
  integral_trigonometric: ["allow_trig"],
  integral_substitution: ["allow_trig", "allow_exp", "allow_log"],
  integration_by_parts: ["allow_trig", "allow_exp", "allow_log"],
  first_fundamental_theorem: ["allow_trig", "allow_exp", "allow_roots"],
  second_fundamental_theorem: ["allow_trig", "allow_exp", "allow_roots"],
};

function normalizeLeaf(typeIdOrKey: string | null | undefined): string | null {
  if (!typeIdOrKey) return null;
  const key = typeIdOrKey.trim();
  if (LEAF_ALLOW_KEYS[key]) return key;
  // type_id like c1_limit_jump → limit_jump if present
  const stripped = key.startsWith("c1_") ? key.slice(3) : key;
  if (LEAF_ALLOW_KEYS[stripped]) return stripped;
  // Heuristic family match
  for (const leaf of Object.keys(LEAF_ALLOW_KEYS)) {
    if (key.includes(leaf) || stripped.includes(leaf)) return leaf;
  }
  return null;
}

export function approxMaxDForSettings(
  typeIdOrGeneratorKey: string | null | undefined,
  values: Record<string, string | number | boolean>,
): number | null {
  const leaf = normalizeLeaf(typeIdOrGeneratorKey);
  if (!leaf) return null;
  const keys = LEAF_ALLOW_KEYS[leaf] ?? [];
  if (keys.length === 0) return PEDAGOGICAL_MAX_D;
  let saturated = 0;
  let bonus = 0;
  for (const k of keys) {
    const w = ALLOW_BONUS[k] ?? 0;
    saturated += w;
    if (Boolean(values[k])) bonus += w;
  }
  const frac = saturated > 0 ? bonus / saturated : 1;
  const scaled = PEDAGOGICAL_MAX_D * (STRUCTURAL_SHARE + ALLOW_SHARE * frac);
  return Math.min(PEDAGOGICAL_MAX_D, Math.max(8, Math.round(scaled * 10) / 10));
}
