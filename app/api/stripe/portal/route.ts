import { NextResponse } from "next/server";
import { auth, isAuthConfigured } from "@/auth";
import { getAppOrigin, getStripe, isStripeConfigured, stripeKeyError } from "@/lib/stripe";
import { getSubscriptionByUserId } from "@/lib/subscription-store";

export async function POST(request: Request) {
  if (!isAuthConfigured()) {
    return NextResponse.json({ error: "Auth is not configured" }, { status: 503 });
  }

  const keyError = stripeKeyError(process.env.STRIPE_SECRET_KEY);
  if (keyError) {
    return NextResponse.json({ error: keyError }, { status: 503 });
  }

  if (!isStripeConfigured()) {
    return NextResponse.json({ error: "Stripe is not configured" }, { status: 503 });
  }

  const session = await auth();
  const userId = session?.user?.id;
  if (!userId) {
    return NextResponse.json({ error: "Sign in required" }, { status: 401 });
  }

  const subscription = await getSubscriptionByUserId(userId);
  if (!subscription?.stripe_customer_id) {
    return NextResponse.json({ error: "No billing account found" }, { status: 404 });
  }

  const origin = getAppOrigin(request);
  const portalSession = await getStripe().billingPortal.sessions.create({
    customer: subscription.stripe_customer_id,
    return_url: origin,
  });

  if (!portalSession.url) {
    return NextResponse.json({ error: "Failed to create portal session" }, { status: 500 });
  }

  return NextResponse.json({ url: portalSession.url });
}
