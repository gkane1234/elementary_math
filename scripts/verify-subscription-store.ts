/**
 * Lightweight verification for subscription entitlement helpers.
 * Run: npx --yes tsx scripts/verify-subscription-store.ts
 */
import {
  getSubscriptionByUserId,
  isEntitled,
  upsertSubscription,
  updateSubscriptionByCustomerId,
} from "../lib/subscription-store";

async function main() {
  process.env.WORKSHEET_STORE_FILE = "true";

  if (!isEntitled("active") || !isEntitled("trialing") || isEntitled("canceled")) {
    throw new Error("isEntitled status mapping failed");
  }

  const userId = `user_verify_${Date.now()}`;
  const customerId = `cus_verify_${Date.now()}`;

  await upsertSubscription({
    user_id: userId,
    email: "verify@example.com",
    stripe_customer_id: customerId,
    stripe_subscription_id: "sub_verify",
    status: "active",
    current_period_end: new Date(Date.now() + 30 * 86400000).toISOString(),
  });

  const loaded = await getSubscriptionByUserId(userId);
  if (!loaded || !isEntitled(loaded.status) || loaded.stripe_customer_id !== customerId) {
    throw new Error("upsert/getByUserId failed");
  }

  await updateSubscriptionByCustomerId(customerId, { status: "canceled" });
  const canceled = await getSubscriptionByUserId(userId);
  if (!canceled || isEntitled(canceled.status)) {
    throw new Error("cancel update failed");
  }

  console.log("subscription-store verification ok");
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
