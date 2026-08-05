"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { fetchEntitlement, unlockWorksheet } from "@/lib/payment";
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
  const [mode, setMode] = useState<"payment" | "subscription">("payment");

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const sessionId = params.get("session_id");
    const worksheetId = params.get("worksheet_id");
    const type = params.get("type");

    if (type === "subscription") {
      setMode("subscription");
      setMessage("Confirming your subscription...");

      if (!sessionId) {
        setStatus("error");
        setMessage("Missing subscription details. Return to the worksheet and try again.");
        return;
      }

      let cancelled = false;
      let attempts = 0;

      const pollEntitlement = async () => {
        try {
          const result = await fetchEntitlement();
          if (cancelled) {
            return;
          }

          if (result.entitled) {
            setStatus("ready");
            setMessage("Subscription active. You can export unlimited worksheets.");
            return;
          }

          attempts += 1;
          if (attempts < 8) {
            window.setTimeout(pollEntitlement, 1500);
            return;
          }

          setStatus("error");
          setMessage("Subscription not confirmed yet. Refresh in a moment or return home.");
        } catch (error) {
          if (cancelled) {
            return;
          }

          attempts += 1;
          if (attempts < 8) {
            window.setTimeout(pollEntitlement, 1500);
            return;
          }

          const detail = error instanceof Error ? error.message : "Subscription could not be confirmed";
          setStatus("error");
          setMessage(detail);
        }
      };

      pollEntitlement();
      return () => {
        cancelled = true;
      };
    }

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

  const stored = status === "ready" && mode === "payment" ? readStoredUnlock() : null;

  return (
    <section className="panel payment-status">
      <h2>
        {status === "ready"
          ? mode === "subscription"
            ? "Subscription active"
            : "Worksheet unlocked"
          : "Processing payment"}
      </h2>
      <p>{message}</p>

      {status === "loading" && <p className="worksheet-status">This usually takes a few seconds.</p>}

      {status === "ready" && (
        <div className="payment-actions">
          <Link className="primary button-link" href="/">
            Return to worksheet
          </Link>
          {stored && (
            <p className="plan-summary">
              Unlocked: <strong>{stored.worksheet.title}</strong>
            </p>
          )}
          {mode === "subscription" && (
            <p className="plan-summary">Pro unlocks answer keys and PDF export on every worksheet.</p>
          )}
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
