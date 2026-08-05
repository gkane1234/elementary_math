/**
 * Display labels for question type_ids: short course prefix + human name.
 *
 * Internal type_ids are unchanged (g6_*, pa_*, geo_*, a2_*, pc_*, calc_*, unprefixed A1).
 * UI / gallery / INDEX surfaces use formatTopicLabel → e.g. "a1: Slope", "g6: Decimal addition".
 *
 * Prefixes: g6 | pa | a1 | ge | a2 | pc | c1 | c2 | c3
 */

export type TopicCoursePrefix =
  | "g6"
  | "pa"
  | "a1"
  | "ge"
  | "a2"
  | "pc"
  | "c1"
  | "c2"
  | "c3";

const TYPE_ID_PREFIX_TO_COURSE: Array<{ prefix: string; course: TopicCoursePrefix }> = [
  { prefix: "g6_", course: "g6" },
  { prefix: "pa_", course: "pa" },
  { prefix: "geo_", course: "ge" },
  { prefix: "a2_", course: "a2" },
  { prefix: "pc_", course: "pc" },
];

const CATEGORY_TO_COURSE: Array<{ needle: string; course: TopicCoursePrefix }> = [
  { needle: "Grade 6", course: "g6" },
  { needle: "Pre-Algebra", course: "pa" },
  { needle: "Algebra 1", course: "a1" },
  { needle: "Geometry", course: "ge" },
  { needle: "Algebra 2", course: "a2" },
  { needle: "Precalculus", course: "pc" },
];

/** Calculus Vol 1 / 2 / 3 → c1 / c2 / c3 from type_id shape (catalog is mostly Vol 1 + DE). */
export function calcVolumePrefix(typeId: string): "c1" | "c2" | "c3" {
  if (!typeId.startsWith("calc_")) return "c1";
  // OpenStax Vol 2 spine (DE); no c3 leaves in live catalog yet.
  if (typeId.startsWith("calc_diff_eq_")) return "c2";
  if (
    typeId.includes("_multivariable") ||
    typeId.includes("_vector") ||
    typeId.includes("_parametric") ||
    typeId.includes("_polar")
  ) {
    return "c3";
  }
  // Limits, continuity, differentiation, apps of diff, integration, apps of int → Vol 1.
  return "c1";
}

function courseFromCategory(category?: string | null): TopicCoursePrefix | null {
  if (!category) return null;
  const head = category.split("—")[0]?.trim() ?? category;
  for (const { needle, course } of CATEGORY_TO_COURSE) {
    if (head === needle || head.startsWith(needle)) return course;
  }
  if (head === "Calculus" || head.startsWith("Calculus")) return null;
  return null;
}

/** Map type_id (+ optional catalog category) → short course prefix. */
export function coursePrefixForTypeId(
  typeId: string,
  options?: { category?: string | null },
): TopicCoursePrefix {
  if (typeId.startsWith("calc_")) {
    return calcVolumePrefix(typeId);
  }
  for (const { prefix, course } of TYPE_ID_PREFIX_TO_COURSE) {
    if (typeId.startsWith(prefix)) return course;
  }
  const fromCat = courseFromCategory(options?.category);
  if (fromCat) return fromCat;
  // Unprefixed catalog leaves are Algebra 1.
  return "a1";
}

/** Strip known course/type prefixes from a type_id for a readable fallback title. */
export function humanizeTypeId(typeId: string): string {
  let rest = typeId;
  for (const p of ["g6_", "pa_", "geo_", "a2_", "pc_", "calc_"]) {
    if (rest.startsWith(p)) {
      rest = rest.slice(p.length);
      break;
    }
  }
  return rest
    .split("_")
    .filter(Boolean)
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ");
}

function looksLikeTypeId(value: string): boolean {
  return /^[a-z][a-z0-9]*(?:_[a-z0-9]+)+$/.test(value);
}

/**
 * Prefer authored catalog/curriculum `name`; never show a bare type_id as the title part.
 * Format: `{prefix}: {Name}` — e.g. `g6: Introduction to ratios`, `a1: Slope`.
 */
export function formatTopicLabel(
  typeId: string,
  name?: string | null,
  options?: { category?: string | null },
): string {
  const prefix = coursePrefixForTypeId(typeId, options);
  const raw = (name ?? "").trim();
  const title =
    raw && raw !== typeId && !looksLikeTypeId(raw) ? raw : humanizeTypeId(typeId);
  return `${prefix}: ${title}`;
}
