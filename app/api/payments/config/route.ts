import { NextResponse } from "next/server";
import { getPdfPriceCents, isStripeConfigured, stripeKeyError } from "@/lib/stripe";

export async function GET() {
  const disabled = process.env.STRIPE_PAYMENTS_DISABLED === "true";
  const configured = isStripeConfigured();
  const keyError = stripeKeyError(process.env.STRIPE_SECRET_KEY);
  const priceCents = getPdfPriceCents();

  return NextResponse.json({
    enabled: !disabled && configured,
    required: !disabled,
    configured,
    keyError,
    priceCents,
  });
}
