import { NextResponse } from "next/server";
import { getStripe, isStripeConfigured } from "@/lib/stripe";
import { getWorksheet, markWorksheetPaid } from "@/lib/worksheet-store";

export async function GET(request: Request) {
  if (!isStripeConfigured()) {
    return NextResponse.json({ error: "Stripe is not configured" }, { status: 503 });
  }

  const { searchParams } = new URL(request.url);
  const worksheetId = searchParams.get("worksheet_id")?.trim();
  const sessionId = searchParams.get("session_id")?.trim();

  if (!worksheetId || !sessionId) {
    return NextResponse.json({ error: "worksheet_id and session_id are required" }, { status: 400 });
  }

  const stripe = getStripe();
  const session = await stripe.checkout.sessions.retrieve(sessionId);

  if (session.payment_status !== "paid") {
    return NextResponse.json({ error: "Payment not completed" }, { status: 403 });
  }

  if (session.metadata?.worksheet_id !== worksheetId) {
    return NextResponse.json({ error: "Worksheet does not match checkout session" }, { status: 403 });
  }

  let worksheet = await getWorksheet(worksheetId);
  if (!worksheet) {
    return NextResponse.json({ error: "Worksheet not found" }, { status: 404 });
  }

  if (!worksheet.paid) {
    worksheet =
      (await markWorksheetPaid(worksheetId, session.id, session.customer_details?.email)) ?? worksheet;
  }

  if (!worksheet.paid) {
    return NextResponse.json({ error: "Worksheet is not unlocked yet" }, { status: 403 });
  }

  return NextResponse.json({
    paid: true,
    worksheet: worksheet.full_data,
  });
}
