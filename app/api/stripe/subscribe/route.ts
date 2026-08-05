import { NextResponse } from "next/server";
import { auth, isAuthConfigured } from "@/auth";
import {
  getAppOrigin,
  getStripe,
  getSubscriptionPriceId,
  isStripeConfigured,
  isSubscriptionConfigured,
  stripeKeyError,
} from "@/lib/stripe";
import { getSubscriptionByUserId, isEntitled } from "@/lib/subscription-store";

export async function POST(request: Request) {
  if (process.env.STRIPE_PAYMENTS_DISABLED === "true") {
    return NextResponse.json({ error: "Payments are temporarily disabled" }, { status: 503 });
  }

  if (!isAuthConfigured()) {
    return NextResponse.json(
      { error: "Auth is not configured. Set AUTH_SECRET, AUTH_GOOGLE_ID, and AUTH_GOOGLE_SECRET." },
      { status: 503 },
    );
  }

  const keyError = stripeKeyError(process.env.STRIPE_SECRET_KEY);
  if (keyError) {
    return NextResponse.json({ error: keyError }, { status: 503 });
  }

  if (!isStripeConfigured() || !isSubscriptionConfigured()) {
    return NextResponse.json(
      { error: "Subscription billing is not configured. Set STRIPE_SUBSCRIPTION_PRICE_ID." },
      { status: 503 },
    );
  }

  const session = await auth();
  const userId = session?.user?.id;
  const email = session?.user?.email;

  if (!userId || !email) {
    return NextResponse.json({ error: "Sign in required" }, { status: 401 });
  }

  const existing = await getSubscriptionByUserId(userId);
  if (existing && isEntitled(existing.status)) {
    return NextResponse.json({ error: "You already have an active subscription" }, { status: 409 });
  }

  const origin = getAppOrigin(request);
  const stripe = getStripe();
  const priceId = getSubscriptionPriceId();
  if (!priceId) {
    return NextResponse.json({ error: "STRIPE_SUBSCRIPTION_PRICE_ID is not configured" }, { status: 503 });
  }

  let customerId = existing?.stripe_customer_id;
  if (!customerId) {
    const customer = await stripe.customers.create({
      email,
      metadata: { user_id: userId },
    });
    customerId = customer.id;
  }

  const checkoutSession = await stripe.checkout.sessions.create({
    mode: "subscription",
    customer: customerId,
    client_reference_id: userId,
    line_items: [{ price: priceId, quantity: 1 }],
    metadata: {
      user_id: userId,
    },
    subscription_data: {
      metadata: {
        user_id: userId,
      },
    },
    success_url: `${origin}/success?session_id={CHECKOUT_SESSION_ID}&type=subscription`,
    cancel_url: `${origin}/cancel?type=subscription`,
  });

  if (!checkoutSession.url) {
    return NextResponse.json({ error: "Failed to create checkout session" }, { status: 500 });
  }

  return NextResponse.json({ url: checkoutSession.url });
}
