export type SettingField = {
  key: string;
  label: string;
  type: "int" | "range" | "select" | "bool";
  default: string | number | boolean;
  min?: number;
  max?: number;
  options?: string[];
  group?: string;
};

export type QuestionTypeInfo = {
  id: string;
  name: string;
  description: string;
  category: string;
  subcategory?: string | null;
  instruction_latex?: string | null;
  instruction_text?: string | null;
  settings: SettingField[];
};

export type Question = {
  id: string;
  topic: string;
  prompt_latex: string;
  prompt_text: string;
  answer_latex?: string | null;
  metadata?: Record<string, unknown>;
};

export type QuestionSet = {
  title: string;
  questions: Question[];
  settings_snapshot?: Record<string, unknown>;
  instruction_latex?: string | null;
  instruction_text?: string | null;
  columns?: number;
};

export type TopicSection = {
  id: string;
  type_id: string;
  count: number;
  settings: Record<string, string | number | boolean>;
};

export type WorksheetQuestion = Question & {
  spacing: number;
  generation_settings: Record<string, unknown>;
  instruction_latex?: string | null;
  sectionId?: string;
};

export type WorksheetDraft = {
  title: string;
  columns: number;
  questions: WorksheetQuestion[];
};

export type GenerateSection = {
  type_id: string;
  count: number;
  settings: Record<string, unknown>;
};

export type CurriculumTopic = {
  id: string;
  name: string;
  /** Canonical question type registry id when a generator exists. */
  type_id?: string | null;
  topics?: CurriculumTopic[];
};

export type CurriculumLevel = {
  id: string;
  name: string;
  topics: CurriculumTopic[];
};
