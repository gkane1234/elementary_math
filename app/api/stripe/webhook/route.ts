import { NextResponse } from "next/server";
import Stripe from "stripe";
import { getStripe } from "@/lib/stripe";
import {
  getSubscriptionByCustomerId,
  upsertSubscription,
  updateSubscriptionByCustomerId,
} from "@/lib/subscription-store";
import { markWorksheetPaid } from "@/lib/worksheet-store";

export const runtime = "nodejs";

function periodEndIso(subscription: Stripe.Subscription): string | null {
  const periodEnd = (subscription as Stripe.Subscription & { current_period_end?: number })
    .current_period_end;
  if (typeof periodEnd !== "number") {
    return null;
  }
  return new Date(periodEnd * 1000).toISOString();
}

async function syncSubscriptionFromStripe(subscription: Stripe.Subscription): Promise<void> {
  const customerId =
    typeof subscription.customer === "string" ? subscription.customer : subscription.customer.id;
  const userId = subscription.metadata?.user_id;
  const existing = await getSubscriptionByCustomerId(customerId);

  if (userId) {
    await upsertSubscription({
      user_id: userId,
      email: existing?.email ?? null,
      stripe_customer_id: customerId,
      stripe_subscription_id: subscription.id,
      status: subscription.status,
      current_period_end: periodEndIso(subscription),
    });
    return;
  }

  if (existing) {
    await updateSubscriptionByCustomerId(customerId, {
      status: subscription.status,
      stripe_subscription_id: subscription.id,
      current_period_end: periodEndIso(subscription),
    });
  }
}

export async function POST(request: Request) {
  const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;
  if (!webhookSecret) {
    return NextResponse.json({ error: "STRIPE_WEBHOOK_SECRET is not configured" }, { status: 503 });
  }

  const signature = request.headers.get("stripe-signature");
  if (!signature) {
    return NextResponse.json({ error: "Missing stripe-signature header" }, { status: 400 });
  }

  const body = await request.text();
  let event: Stripe.Event;

  try {
    event = getStripe().webhooks.constructEvent(body, signature, webhookSecret);
  } catch (error) {
    const message = error instanceof Error ? error.message : "Invalid webhook signature";
    return NextResponse.json({ error: message }, { status: 400 });
  }

  if (event.type === "checkout.session.completed") {
    const session = event.data.object as Stripe.Checkout.Session;

    if (session.mode === "payment") {
      const worksheetId = session.metadata?.worksheet_id;
      if (worksheetId && session.payment_status === "paid") {
        await markWorksheetPaid(worksheetId, session.id, session.customer_details?.email);
      }
    }

    if (session.mode === "subscription") {
      const userId = session.metadata?.user_id ?? session.client_reference_id;
      const customerId =
        typeof session.customer === "string" ? session.customer : session.customer?.id;
      const subscriptionId =
        typeof session.subscription === "string"
          ? session.subscription
          : session.subscription?.id;

      if (userId && customerId && subscriptionId) {
        const subscription = await getStripe().subscriptions.retrieve(subscriptionId);
        await upsertSubscription({
          user_id: userId,
          email: session.customer_details?.email ?? session.customer_email ?? null,
          stripe_customer_id: customerId,
          stripe_subscription_id: subscription.id,
          status: subscription.status,
          current_period_end: periodEndIso(subscription),
        });
      }
    }
  }

  if (
    event.type === "customer.subscription.updated" ||
    event.type === "customer.subscription.deleted"
  ) {
    const subscription = event.data.object as Stripe.Subscription;
    await syncSubscriptionFromStripe(subscription);
  }

  return NextResponse.json({ received: true });
}
