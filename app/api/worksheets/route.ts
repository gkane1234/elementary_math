import { NextResponse } from "next/server";
import type { WorksheetDraft } from "@/lib/types";
import { createWorksheet } from "@/lib/worksheet-store";

type SaveWorksheetBody = {
  title?: string;
  worksheet?: WorksheetDraft;
};

export async function POST(request: Request) {
  let body: SaveWorksheetBody;

  try {
    body = (await request.json()) as SaveWorksheetBody;
  } catch {
    return NextResponse.json({ error: "Invalid JSON body" }, { status: 400 });
  }

  if (!body.worksheet || !Array.isArray(body.worksheet.questions) || body.worksheet.questions.length === 0) {
    return NextResponse.json({ error: "Worksheet with questions is required" }, { status: 400 });
  }

  const title = body.title?.trim() || body.worksheet.title || "Math Practice";
  const record = await createWorksheet(title, {
    ...body.worksheet,
    title,
  });

  return NextResponse.json({
    worksheet_id: record.id,
    paid: record.paid,
  });
}
