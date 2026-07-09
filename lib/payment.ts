import type { WorksheetDraft } from "@/lib/types";

export type SaveWorksheetResponse = {
  worksheet_id: string;
  paid: boolean;
};

export type CheckoutResponse = {
  url: string;
};

export type UnlockResponse = {
  paid: boolean;
  worksheet: WorksheetDraft;
};

export async function saveWorksheetForPayment(
  title: string,
  worksheet: WorksheetDraft,
): Promise<SaveWorksheetResponse> {
  const response = await fetch("/api/worksheets", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, worksheet }),
  });

  if (!response.ok) {
    const payload = (await response.json().catch(() => null)) as { error?: string } | null;
    throw new Error(payload?.error ?? "Failed to save worksheet");
  }

  return response.json() as Promise<SaveWorksheetResponse>;
}

export async function createCheckoutSession(worksheetId: string): Promise<string> {
  const response = await fetch("/api/stripe/checkout", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ worksheet_id: worksheetId }),
  });

  if (!response.ok) {
    const payload = (await response.json().catch(() => null)) as { error?: string } | null;
    throw new Error(payload?.error ?? "Failed to start checkout");
  }

  const data = (await response.json()) as CheckoutResponse;
  if (!data.url) {
    throw new Error("Checkout session did not return a redirect URL");
  }

  return data.url;
}

export async function unlockWorksheet(
  worksheetId: string,
  sessionId: string,
): Promise<UnlockResponse> {
  const params = new URLSearchParams({
    worksheet_id: worksheetId,
    session_id: sessionId,
  });

  const response = await fetch(`/api/worksheets/unlock?${params.toString()}`, {
    cache: "no-store",
  });

  if (!response.ok) {
    const payload = (await response.json().catch(() => null)) as { error?: string } | null;
    throw new Error(payload?.error ?? "Payment not confirmed yet");
  }

  return response.json() as Promise<UnlockResponse>;
}

export function formatPdfPrice(cents: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(cents / 100);
}
