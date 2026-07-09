import { NextResponse } from "next/server";
import { getStripe, getAppOrigin, getPdfPriceCents, isStripeConfigured, stripeKeyError } from "@/lib/stripe";
import { getWorksheet } from "@/lib/worksheet-store";

type CheckoutBody = {
  worksheet_id?: string;
};

export async function POST(request: Request) {
  const keyError = stripeKeyError(process.env.STRIPE_SECRET_KEY);
  if (keyError) {
    return NextResponse.json({ error: keyError }, { status: 503 });
  }

  if (!isStripeConfigured()) {
    return NextResponse.json({ error: "Stripe is not configured" }, { status: 503 });
  }

  let body: CheckoutBody;

  try {
    body = (await request.json()) as CheckoutBody;
  } catch {
    return NextResponse.json({ error: "Invalid JSON body" }, { status: 400 });
  }

  const worksheetId = body.worksheet_id?.trim();
  if (!worksheetId) {
    return NextResponse.json({ error: "worksheet_id is required" }, { status: 400 });
  }

  const worksheet = await getWorksheet(worksheetId);
  if (!worksheet) {
    return NextResponse.json({ error: "Worksheet not found" }, { status: 404 });
  }

  if (worksheet.paid) {
    return NextResponse.json({ error: "Worksheet is already paid" }, { status: 409 });
  }

  const origin = getAppOrigin(request);
  const stripe = getStripe();
  const priceCents = getPdfPriceCents();

  const session = await stripe.checkout.sessions.create({
    mode: "payment",
    line_items: [
      {
        quantity: 1,
        price_data: {
          currency: "usd",
          unit_amount: priceCents,
          product_data: {
            name: "Math Worksheet PDF",
            description: worksheet.title,
          },
        },
      },
    ],
    metadata: {
      worksheet_id: worksheetId,
    },
    success_url: `${origin}/success?session_id={CHECKOUT_SESSION_ID}&worksheet_id=${worksheetId}`,
    cancel_url: `${origin}/cancel?worksheet_id=${worksheetId}`,
  });

  if (!session.url) {
    return NextResponse.json({ error: "Failed to create checkout session" }, { status: 500 });
  }

  return NextResponse.json({ url: session.url });
}
