import { NextResponse } from "next/server";
import { isAuthConfigured } from "@/auth";
import {
  getPdfPriceCents,
  getSubscriptionPriceCents,
  isStripeConfigured,
  isSubscriptionConfigured,
  stripeKeyError,
} from "@/lib/stripe";

export async function GET() {
  const disabled = process.env.STRIPE_PAYMENTS_DISABLED === "true";
  const configured = isStripeConfigured();
  const keyError = stripeKeyError(process.env.STRIPE_SECRET_KEY);
  const priceCents = getPdfPriceCents();
  const subscriptionPriceCents = getSubscriptionPriceCents();
  const subscriptionConfigured = isSubscriptionConfigured();
  const authConfigured = isAuthConfigured();

  return NextResponse.json({
    enabled: !disabled && configured,
    required: !disabled,
    configured,
    keyError,
    priceCents,
    subscriptionPriceCents,
    subscriptionEnabled: !disabled && subscriptionConfigured && authConfigured,
    subscriptionConfigured,
    authConfigured,
  });
}
