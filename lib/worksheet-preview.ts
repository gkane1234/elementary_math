import type { WorksheetDraft } from "@/lib/types";

export function toPreviewWorksheet(worksheet: WorksheetDraft): WorksheetDraft {
  return {
    ...worksheet,
    questions: worksheet.questions.map((question) => ({
      ...question,
      answer_latex: null,
    })),
  };
}
