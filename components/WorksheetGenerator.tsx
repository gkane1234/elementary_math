"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { AddTopicModal } from "@/components/AddTopicModal";
import { ExportPdfButton } from "@/components/ExportPdfButton";
import { InteractiveWorksheet } from "@/components/InteractiveWorksheet";
import { PayForPdfButton } from "@/components/PayForPdfButton";
import { TopicSectionList } from "@/components/TopicSectionList";
import { resolveColumnCount } from "@/lib/columns";
import type { QuestionTypeInfo, TopicSection, WorksheetDraft } from "@/lib/types";
import {
  preserveQuestionEdits,
  reorderQuestionsBySections,
  sectionContentKey,
  sectionOrderKey,
  syncWorksheetFromSections,
} from "@/lib/worksheet-sync";

const UNLOCK_STORAGE_KEY = "polynomial_unlocked_worksheet";

type RestoredUnlock = {
  worksheetId: string;
  worksheet: WorksheetDraft;
};

function readRestoredUnlock(): RestoredUnlock | null {
  if (typeof window === "undefined") {
    return null;
  }

  const raw = window.sessionStorage.getItem(UNLOCK_STORAGE_KEY);
  if (!raw) {
    return null;
  }

  try {
    return JSON.parse(raw) as RestoredUnlock;
  } catch {
    window.sessionStorage.removeItem(UNLOCK_STORAGE_KEY);
    return null;
  }
}

export function WorksheetGenerator() {
  const restoredUnlock = useMemo(() => readRestoredUnlock(), []);
  const [types, setTypes] = useState<QuestionTypeInfo[]>([]);
  const [sections, setSections] = useState<TopicSection[]>([]);
  const [title, setTitle] = useState(restoredUnlock?.worksheet.title ?? "Math Practice");
  const [maxColumns, setMaxColumns] = useState<string>("auto");
  const [worksheet, setWorksheet] = useState<WorksheetDraft | null>(restoredUnlock?.worksheet ?? null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [topicModalOpen, setTopicModalOpen] = useState(false);
  const [editingSectionId, setEditingSectionId] = useState<string | null>(null);
  const [paid, setPaid] = useState(Boolean(restoredUnlock));
  const [worksheetId, setWorksheetId] = useState<string | null>(restoredUnlock?.worksheetId ?? null);
  const [paymentsRequired, setPaymentsRequired] = useState(true);
  const [paymentsEnabled, setPaymentsEnabled] = useState(false);
  const [pdfPriceCents, setPdfPriceCents] = useState(300);
  const [stripeConfigured, setStripeConfigured] = useState(false);
  const [stripeKeyError, setStripeKeyError] = useState<string | null>(null);

  const worksheetRef = useRef<WorksheetDraft | null>(null);
  const lastContentKeyRef = useRef<string>("");

  const contentKey = useMemo(() => sectionContentKey(sections), [sections]);
  const orderKey = useMemo(() => sectionOrderKey(sections), [sections]);

  worksheetRef.current = worksheet;

  useEffect(() => {
    if (restoredUnlock) {
      window.sessionStorage.removeItem(UNLOCK_STORAGE_KEY);
    }
  }, [restoredUnlock]);

  useEffect(() => {
    fetch("/api/payments/config", { cache: "no-store" })
      .then((response) => response.json())
      .then((data: { enabled: boolean; required: boolean; configured: boolean; keyError?: string | null; priceCents: number }) => {
        setPaymentsRequired(data.required);
        setPaymentsEnabled(data.enabled);
        setStripeConfigured(data.configured);
        setStripeKeyError(data.keyError ?? null);
        setPdfPriceCents(data.priceCents);
      })
      .catch(() => {
        setPaymentsRequired(true);
        setPaymentsEnabled(false);
        setStripeConfigured(false);
      });
  }, []);

  useEffect(() => {
    fetch("/api/question-types", { cache: "no-store" })
      .then((response) => response.json())
      .then((data) => setTypes(data.types))
      .catch((err: Error) => setError(err.message));
  }, []);

  const totalPlanned = useMemo(
    () => sections.reduce((sum, section) => sum + section.count, 0),
    [sections],
  );

  const applyColumns = (draft: WorksheetDraft): WorksheetDraft => ({
    ...draft,
    columns: resolveColumnCount(draft.questions.length, maxColumns),
  });

  useEffect(() => {
    if (sections.length === 0) {
      if (!paid) {
        setWorksheet(null);
        setError(null);
        setLoading(false);
        lastContentKeyRef.current = "";
      }
      return;
    }

    if (contentKey !== lastContentKeyRef.current && !paid) {
      setPaid(false);
      setWorksheetId(null);
    }

    if (contentKey === lastContentKeyRef.current && worksheetRef.current) {
      setWorksheet((current) =>
        current
          ? applyColumns({
              ...current,
              questions: reorderQuestionsBySections(current.questions, sections),
            })
          : current,
      );
      return;
    }

    let cancelled = false;
    setLoading(true);
    setError(null);

    const previousQuestions = worksheetRef.current?.questions ?? [];

    syncWorksheetFromSections(worksheetRef.current, sections, title, maxColumns)
      .then((draft) => {
        if (cancelled) return;
        lastContentKeyRef.current = contentKey;
        setWorksheet(
          applyColumns({
            ...draft,
            title,
            questions: preserveQuestionEdits(draft.questions, previousQuestions),
          }),
        );
      })
      .catch((err: Error) => {
        if (cancelled) return;
        setError(err.message || "Failed to generate worksheet");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [contentKey, orderKey]);

  useEffect(() => {
    setWorksheet((current) => (current ? { ...current, title } : current));
  }, [title]);

  useEffect(() => {
    setWorksheet((current) => (current ? applyColumns(current) : current));
  }, [maxColumns]);

  const openTopicEditor = (section?: TopicSection) => {
    setEditingSectionId(section?.id ?? null);
    setTopicModalOpen(true);
  };

  const canExport = Boolean(worksheet && worksheet.questions.length > 0 && !loading);
  const exportEnabled = canExport && (!paymentsRequired || paid);
  const showPaymentGate = paymentsRequired && !paid;

  return (
    <>
      <div className="worksheet-workspace">
        <aside className="left-rail">
          <section className="panel">
            <h2>Worksheet settings</h2>
            <label className="field">
              <span>Worksheet title</span>
              <input type="text" value={title} onChange={(event) => setTitle(event.target.value)} />
            </label>
            <label className="field">
              <span>Columns</span>
              <select value={maxColumns} onChange={(event) => setMaxColumns(event.target.value)}>
                <option value="auto">Auto (up to 3)</option>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
              </select>
            </label>
            <button className="secondary" type="button" onClick={() => openTopicEditor()}>
              Add question topics...
            </button>
          </section>
        </aside>

        <div className="worksheet-main">
          {loading && <p className="worksheet-status interactive-only">Generating worksheet...</p>}
          {showPaymentGate && worksheet && (
            <p className="worksheet-status preview-banner interactive-only">
              Preview mode — purchase to unlock the answer key and PDF export.
            </p>
          )}
          <InteractiveWorksheet
            worksheet={worksheet}
            types={types}
            previewMode={showPaymentGate}
            onChange={(next) => {
              setWorksheet(applyColumns(next));
            }}
            onError={setError}
          />
        </div>

        <aside className="right-rail">
          <section className="panel action-rail">
            <div className="action-rail-scroll">
              <h2>Actions</h2>
              <p className="plan-summary">
                Planned questions: <strong>{totalPlanned}</strong>
              </p>

              <TopicSectionList
                sections={sections}
                types={types}
                onSectionsChange={setSections}
                onEditSection={openTopicEditor}
                compact
              />

              <button className="secondary" type="button" onClick={() => openTopicEditor()}>
                Edit topics
              </button>
            </div>

            <div className="action-rail-actions">
              {paymentsRequired ? (
                paid ? (
                  <ExportPdfButton disabled={!exportEnabled} />
                ) : (
                  <>
                    <PayForPdfButton
                      disabled={!canExport || !stripeConfigured}
                      title={title}
                      worksheet={worksheet!}
                      priceCents={pdfPriceCents}
                      onCheckoutStart={setWorksheetId}
                      onError={setError}
                    />
                    {!stripeConfigured && (
                      <p className="error">
                        {stripeKeyError ??
                          "Stripe is not configured. Add sk_test_... to STRIPE_SECRET_KEY in .env.local and restart the dev server."}
                      </p>
                    )}
                  </>
                )
              ) : (
                <ExportPdfButton disabled={!exportEnabled} />
              )}

              {paymentsRequired && paid && worksheetId && (
                <p className="plan-summary">Worksheet unlocked for export.</p>
              )}

              {error && <p className="error">{error}</p>}
            </div>
          </section>
        </aside>
      </div>

      <AddTopicModal
        open={topicModalOpen}
        types={types}
        sections={sections}
        editingSectionId={editingSectionId}
        onClose={() => {
          setTopicModalOpen(false);
          setEditingSectionId(null);
        }}
        onSectionsChange={setSections}
        onEditingSectionIdChange={setEditingSectionId}
      />
    </>
  );
}
