import { NextResponse } from "next/server";
import { auth, isAuthConfigured } from "@/auth";
import { getSubscriptionByUserId, isEntitled } from "@/lib/subscription-store";

export async function GET() {
  if (process.env.STRIPE_PAYMENTS_DISABLED === "true") {
    return NextResponse.json({
      entitled: true,
      signedIn: false,
      authConfigured: isAuthConfigured(),
      status: null,
      reason: "payments_disabled",
    });
  }

  if (!isAuthConfigured()) {
    return NextResponse.json({
      entitled: false,
      signedIn: false,
      authConfigured: false,
      status: null,
    });
  }

  const session = await auth();
  const userId = session?.user?.id;
  if (!userId) {
    return NextResponse.json({
      entitled: false,
      signedIn: false,
      authConfigured: true,
      status: null,
    });
  }

  const subscription = await getSubscriptionByUserId(userId);
  const status = subscription?.status ?? null;

  return NextResponse.json({
    entitled: isEntitled(status),
    signedIn: true,
    authConfigured: true,
    status,
    currentPeriodEnd: subscription?.current_period_end ?? null,
  });
}
