/**
 * Portfolio landing copy and frozen examples.
 *
 * Derivative rows are the saved gallery snapshot
 * `public/gallery/snapshots/calc-derivatives-level-3.json`
 * (generated_at 2026-08-05, seed 1010).
 *
 * Factoring prompts are from the question engine:
 * type `quadratic_factoring`, seed 1, difficulty 0 / 8 / 22.
 *
 * Model figures are the README status snapshot (601 scored catalog types;
 * forward-model correlations for Algebra 1, Algebra 2, Precalculus, Calculus).
 */

export const GENERATOR_PATH = "/generate";

export const COURSES = [
  "Grade 6",
  "Pre-Algebra",
  "Algebra 1",
  "Algebra 2",
  "Geometry",
  "Precalculus",
  "Calculus",
] as const;

export type SheetQuestion = {
  number: number;
  typeId: string;
  name: string;
  difficulty: number;
  promptLatex: string;
};

export const DERIVATIVE_SHEET = {
  id: "calc-derivatives-level-3",
  title: "Calculus: Derivatives Intro",
  level: "level-3" as const,
  questions: [
    {
      number: 1,
      typeId: "calc_limits_by_direct_evaluation",
      name: "By direct evaluation",
      difficulty: 8,
      promptLatex: "\\lim_{x \\to 5} -\\left(\\left(4x + 3\\right)\\right)",
    },
    {
      number: 2,
      typeId: "calc_limits_by_direct_evaluation",
      name: "By direct evaluation",
      difficulty: 9.8889,
      promptLatex: "\\lim_{x \\to 5} -\\left(\\left(4x + 3\\right)\\right)",
    },
    {
      number: 3,
      typeId: "calc_limits_by_direct_evaluation",
      name: "By direct evaluation",
      difficulty: 11.7778,
      promptLatex: "\\lim_{x \\to -4} -\\left(\\left(3x^{5} + 4x\\right)\\right)",
    },
    {
      number: 4,
      typeId: "calc_limits_at_removable_discontinuities",
      name: "At removable discontinuities",
      difficulty: 13.6667,
      promptLatex: "\\lim_{x \\to 1} \\frac{x^{3} + 3x^{2} - x - 3}{x-1}",
    },
    {
      number: 5,
      typeId: "calc_limits_by_direct_evaluation",
      name: "By direct evaluation",
      difficulty: 15.5556,
      promptLatex: "\\lim_{x \\to 5} \\frac{3x^{3} + 4}{-3x + 2}",
    },
    {
      number: 6,
      typeId: "calc_diff_average_rates_of_change",
      name: "Average rates of change",
      difficulty: 17.4444,
      promptLatex:
        "\\text{Find the average rate of change of }f(x)=x - 2\\text{ on }[1,5].",
    },
    {
      number: 7,
      typeId: "calc_limits_by_direct_evaluation",
      name: "By direct evaluation",
      difficulty: 19.3333,
      promptLatex: "\\lim_{x \\to 5} -\\frac{2x^{3} + 3}{6x + 6}",
    },
    {
      number: 8,
      typeId: "calc_diff_definition_of_the_derivative",
      name: "Definition of the derivative",
      difficulty: 21.2222,
      promptLatex: "\\lim_{h\\to 0}\\frac{4(5+h)^{2}-100}{h}",
    },
    {
      number: 9,
      typeId: "calc_limits_by_direct_evaluation",
      name: "By direct evaluation",
      difficulty: 23.1111,
      promptLatex: "\\lim_{x \\to 5} -\\frac{-6x^{3} - 1}{5x + 5}",
    },
    {
      number: 10,
      typeId: "calc_limits_at_removable_discontinuities",
      name: "At removable discontinuities",
      difficulty: 25,
      promptLatex: "\\lim_{x \\to 1} \\frac{x^{3} + 8x^{2} - x - 8}{x-1}",
    },
  ] satisfies SheetQuestion[],
};

/** Questions shown on the hero sheet. Numbers match DERIVATIVE_SHEET. */
export const HERO_QUESTION_NUMBERS = [1, 4, 8] as const;

export const FACTORING_SAMPLE = {
  typeId: "quadratic_factoring",
  name: "Quadratic expressions",
  seed: 1,
  instruction: "Factor.",
  samples: [
    { difficulty: 0, promptLatex: "x^{2} - 9x + 20" },
    { difficulty: 8, promptLatex: "3x^{2} - 32x + 20" },
    { difficulty: 22, promptLatex: "-16z + 15 + 2z^{2} - z^{2}" },
  ],
};

export const CATALOG_TYPES_SCORED = 601;

export const EFFORT_FLOW = [
  "Catalog",
  "Generate",
  "Score effort",
  "Record",
  "Forward model",
  "Inverse search",
] as const;

export const EFFORT_MODELS = [
  { course: "Algebra 1", labeled: "73 types, 6,570 rows", correlation: "0.91" },
  { course: "Algebra 2", labeled: "145 types, 13,050 rows", correlation: "0.91" },
  { course: "Precalculus", labeled: "93 types, 8,370 rows", correlation: "0.94" },
  { course: "Calculus", labeled: "64 types, 5,760 rows", correlation: "0.93" },
] as const;

export const QA_CONCERNS = [
  {
    title: "Correctness",
    body: "The generator computes the answer key. That key is what unit tests and spot checks compare against.",
  },
  {
    title: "Effort",
    body: "A scorer on every catalog type, then a model that predicts effort from the parameters that built the question.",
  },
  {
    title: "Topic fit",
    body: "A separate review that the item is the right skill and method, not only that the key is right.",
  },
] as const;

export const PRODUCT_SHELL = [
  { title: "Sign-in", body: "Google sign-in through Auth.js." },
  { title: "Preview", body: "Watermarked until the worksheet is unlocked." },
  {
    title: "Payment",
    body: "Stripe Checkout for one PDF, or a subscription with a customer portal.",
  },
  { title: "Print", body: "The browser print dialog. No server-side LaTeX." },
] as const;

export function formatDifficulty(value: number): string {
  const rounded = Math.round(value * 10) / 10;
  return Number.isInteger(rounded) ? String(rounded) : rounded.toFixed(1);
}

const GENERATOR_QUERY_KEYS = ["mode", "seed", "auto"] as const;

function queryValuePresent(value: string | string[] | undefined): boolean {
  if (Array.isArray(value)) return value.some((item) => item.length > 0);
  return typeof value === "string" && value.length > 0;
}

/**
 * Old gallery and bookmark links used `/?mode=progressive&…`.
 * Send those to the generator and leave a normal visit on the landing page.
 */
export function generatorRedirectPath(
  search: Record<string, string | string[] | undefined>,
): string | null {
  const opensGenerator = GENERATOR_QUERY_KEYS.some((key) => queryValuePresent(search[key]));
  if (!opensGenerator) return null;

  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(search)) {
    if (typeof value === "string") params.append(key, value);
    else if (Array.isArray(value)) {
      for (const item of value) params.append(key, item);
    }
  }
  const qs = params.toString();
  return qs ? `${GENERATOR_PATH}?${qs}` : GENERATOR_PATH;
}
