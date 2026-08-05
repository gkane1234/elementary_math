"use client";

import { signIn, useSession } from "next-auth/react";
import { useState } from "react";
import { createSubscriptionCheckout, formatPdfPrice } from "@/lib/payment";

type SubscribeButtonProps = {
  disabled: boolean;
  priceCents: number;
  authConfigured: boolean;
  onError?: (message: string) => void;
};

export function SubscribeButton({
  disabled,
  priceCents,
  authConfigured,
  onError,
}: SubscribeButtonProps) {
  const { data: session, status } = useSession();
  const [loading, setLoading] = useState(false);

  const handleClick = async () => {
    onError?.("");

    if (!authConfigured) {
      onError?.(
        "Auth is not configured. Add AUTH_SECRET, AUTH_GOOGLE_ID, and AUTH_GOOGLE_SECRET to .env.local.",
      );
      return;
    }

    if (status === "loading") {
      return;
    }

    if (!session?.user) {
      await signIn("google", { callbackUrl: "/" });
      return;
    }

    setLoading(true);
    try {
      const checkoutUrl = await createSubscriptionCheckout();
      window.location.assign(checkoutUrl);
    } catch (error) {
      const message = error instanceof Error ? error.message : "Subscription checkout failed";
      onError?.(message);
      setLoading(false);
    }
  };

  const label = session?.user
    ? `Unlimited — ${formatPdfPrice(priceCents)}/mo`
    : `Sign in to subscribe — ${formatPdfPrice(priceCents)}/mo`;

  return (
    <button
      className="secondary"
      type="button"
      onClick={handleClick}
      disabled={disabled || loading || status === "loading"}
    >
      {loading ? "Redirecting to checkout..." : label}
    </button>
  );
}
