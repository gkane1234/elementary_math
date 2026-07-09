"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { unlockWorksheet } from "@/lib/payment";
import type { WorksheetDraft } from "@/lib/types";

const STORAGE_KEY = "polynomial_unlocked_worksheet";

type StoredUnlock = {
  worksheetId: string;
  sessionId: string;
  worksheet: WorksheetDraft;
};

function readStoredUnlock(): StoredUnlock | null {
  if (typeof window === "undefined") {
    return null;
  }

  const raw = window.sessionStorage.getItem(STORAGE_KEY);
  if (!raw) {
    return null;
  }

  try {
    return JSON.parse(raw) as StoredUnlock;
  } catch {
    return null;
  }
}

function writeStoredUnlock(value: StoredUnlock) {
  window.sessionStorage.setItem(STORAGE_KEY, JSON.stringify(value));
}

export default function SuccessPage() {
  const [status, setStatus] = useState<"loading" | "ready" | "error">("loading");
  const [message, setMessage] = useState("Confirming your payment...");

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const sessionId = params.get("session_id");
    const worksheetId = params.get("worksheet_id");

    if (!sessionId || !worksheetId) {
      setStatus("error");
      setMessage("Missing payment details. Return to the worksheet and try again.");
      return;
    }

    let cancelled = false;
    let attempts = 0;

    const pollUnlock = async () => {
      try {
        const result = await unlockWorksheet(worksheetId, sessionId);
        if (cancelled) {
          return;
        }

        writeStoredUnlock({
          worksheetId,
          sessionId,
          worksheet: result.worksheet,
        });

        setStatus("ready");
        setMessage("Payment confirmed. Your worksheet is unlocked.");
      } catch (error) {
        if (cancelled) {
          return;
        }

        attempts += 1;
        if (attempts < 8) {
          window.setTimeout(pollUnlock, 1500);
          return;
        }

        const detail = error instanceof Error ? error.message : "Payment could not be confirmed";
        setStatus("error");
        setMessage(detail);
      }
    };

    pollUnlock();

    return () => {
      cancelled = true;
    };
  }, []);

  const stored = status === "ready" ? readStoredUnlock() : null;

  return (
    <section className="panel payment-status">
      <h2>{status === "ready" ? "Worksheet unlocked" : "Processing payment"}</h2>
      <p>{message}</p>

      {status === "loading" && <p className="worksheet-status">This usually takes a few seconds.</p>}

      {status === "ready" && stored && (
        <div className="payment-actions">
          <Link className="primary button-link" href="/">
            Return to worksheet
          </Link>
          <p className="plan-summary">
            Unlocked: <strong>{stored.worksheet.title}</strong>
          </p>
        </div>
      )}

      {status === "error" && (
        <div className="payment-actions">
          <Link className="secondary button-link" href="/">
            Back to worksheet
          </Link>
        </div>
      )}
    </section>
  );
}
