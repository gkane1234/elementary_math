"use client";

import { useState } from "react";
import type { WorksheetDraft } from "@/lib/types";
import { createCheckoutSession, formatPdfPrice, saveWorksheetForPayment } from "@/lib/payment";

type PayForPdfButtonProps = {
  disabled: boolean;
  title: string;
  worksheet: WorksheetDraft;
  priceCents: number;
  onCheckoutStart?: (worksheetId: string) => void;
  onError?: (message: string) => void;
};

export function PayForPdfButton({
  disabled,
  title,
  worksheet,
  priceCents,
  onCheckoutStart,
  onError,
}: PayForPdfButtonProps) {
  const [loading, setLoading] = useState(false);

  const handleClick = async () => {
    setLoading(true);
    onError?.("");

    try {
      const saved = await saveWorksheetForPayment(title, worksheet);
      onCheckoutStart?.(saved.worksheet_id);
      const checkoutUrl = await createCheckoutSession(saved.worksheet_id);
      window.location.assign(checkoutUrl);
    } catch (error) {
      const message = error instanceof Error ? error.message : "Checkout failed";
      onError?.(message);
      setLoading(false);
    }
  };

  return (
    <button className="primary" type="button" onClick={handleClick} disabled={disabled || loading}>
      {loading ? "Redirecting to checkout..." : `Download PDF — ${formatPdfPrice(priceCents)}`}
    </button>
  );
}
