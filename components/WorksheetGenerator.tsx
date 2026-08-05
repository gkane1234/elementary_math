"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { useSession } from "next-auth/react";
import { useSearchParams } from "next/navigation";
import { AddTopicModal } from "@/components/AddTopicModal";
import { AddTopicPanel } from "@/components/AddTopicPanel";
import { ExportPdfButton } from "@/components/ExportPdfButton";
import { InteractiveWorksheet } from "@/components/InteractiveWorksheet";
import { PayForPdfButton } from "@/components/PayForPdfButton";
import { SubscribeButton } from "@/components/SubscribeButton";
import { TopicSectionList } from "@/components/TopicSectionList";
import { WorksheetPageLayout } from "@/components/WorksheetPageLayout";
import { WorksheetPageLayoutControls } from "@/components/WorksheetPageLayoutControls";
import { generateProgressive } from "@/lib/api";
import { resolveColumnCount } from "@/lib/columns";
import { fetchEntitlement } from "@/lib/payment";
import {
  continuousReadyTypes,
  progressiveApiSectionsToTopicSections,
} from "@/lib/progressive";
import type { QuestionTypeInfo, TopicSection, WorksheetDraft } from "@/lib/types";
import { questionSetToDraft } from "@/lib/worksheet";
import {
  DEFAULT_PAGE_LAYOUT,
  type FitScales,
  type PageLayoutSettings,
} from "@/lib/worksheet-page-layout";
import {
  WORKSHEET_DIFFICULTY_PRESETS,
  worksheetDifficultyToRamp,
  type WorksheetDifficultyPreset,
} from "@/lib/worksheet-difficulty";
import {
  preserveQuestionEdits,
  reorderQuestionsBySections,
  sectionContentKey,
  sectionOrderKey,
  syncWorksheetFromSections,
} from "@/lib/worksheet-sync";
import { formatTopicLabel } from "@/lib/topic-labels";

const UNLOCK_STORAGE_KEY = "polynomial_unlocked_worksheet";

type RestoredUnlock = {
  worksheetId: string;
  worksheet: WorksheetDraft;
};

type WorksheetMode = "manual" | "progressive";

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
  const { status: sessionStatus } = useSession();
  const searchParams = useSearchParams();
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
  const [addingTypeId, setAddingTypeId] = useState<string | null>(null);
  const [paid, setPaid] = useState(Boolean(restoredUnlock));
  const [worksheetId, setWorksheetId] = useState<string | null>(restoredUnlock?.worksheetId ?? null);
  const [paymentsRequired, setPaymentsRequired] = useState(true);
  const [pdfPriceCents, setPdfPriceCents] = useState(300);
  const [subscriptionPriceCents, setSubscriptionPriceCents] = useState(1000);
  const [subscriptionEnabled, setSubscriptionEnabled] = useState(false);
  const [authConfigured, setAuthConfigured] = useState(false);
  const [subscriberEntitled, setSubscriberEntitled] = useState(false);
  const [stripeConfigured, setStripeConfigured] = useState(false);
  const [stripeKeyError, setStripeKeyError] = useState<string | null>(null);
  const [pageLayout, setPageLayout] = useState<PageLayoutSettings>(DEFAULT_PAGE_LAYOUT);
  const [pageFit, setPageFit] = useState<FitScales | null>(null);

  const [mode, setMode] = useState<WorksheetMode>("manual");
  const [progressiveSeed, setProgressiveSeed] = useState("");
  const [progressiveCount, setProgressiveCount] = useState(10);
  const [progressiveDMin, setProgressiveDMin] = useState(0);
  const [progressiveDMax, setProgressiveDMax] = useState(18);
  const [worksheetDifficulty, setWorksheetDifficulty] =
    useState<WorksheetDifficultyPreset | "custom">("custom");
  const [includeRelated, setIncludeRelated] = useState(true);
  const [progressiveTopics, setProgressiveTopics] = useState<string[]>([]);
  const [rngSeed, setRngSeed] = useState<number | null>(null);

  const worksheetRef = useRef<WorksheetDraft | null>(null);
  const lastContentKeyRef = useRef<string>("");
  const lastSectionsRef = useRef<TopicSection[]>([]);
  const skipNextSectionSyncRef = useRef(false);
  const deepLinkAppliedRef = useRef(false);
  const autoGenerateRef = useRef(false);

  const contentKey = useMemo(() => sectionContentKey(sections), [sections]);
  const orderKey = useMemo(() => sectionOrderKey(sections), [sections]);
  const continuousTypes = useMemo(() => continuousReadyTypes(types), [types]);

  worksheetRef.current = worksheet;

  useEffect(() => {
    if (restoredUnlock) {
      window.sessionStorage.removeItem(UNLOCK_STORAGE_KEY);
    }
  }, [restoredUnlock]);

  useEffect(() => {
    fetch("/api/payments/config", { cache: "no-store" })
      .then((response) => response.json())
      .then(
        (data: {
          enabled: boolean;
          required: boolean;
          configured: boolean;
          keyError?: string | null;
          priceCents: number;
          subscriptionPriceCents?: number;
          subscriptionEnabled?: boolean;
          authConfigured?: boolean;
        }) => {
          setPaymentsRequired(data.required);
          setStripeConfigured(data.configured);
          setStripeKeyError(data.keyError ?? null);
          setPdfPriceCents(data.priceCents);
          setSubscriptionPriceCents(data.subscriptionPriceCents ?? 1000);
          setSubscriptionEnabled(Boolean(data.subscriptionEnabled));
          setAuthConfigured(Boolean(data.authConfigured));
        },
      )
      .catch(() => {
        setPaymentsRequired(true);
        setStripeConfigured(false);
      });
  }, []);

  useEffect(() => {
    if (sessionStatus === "loading") {
      return;
    }

    fetchEntitlement()
      .then((data) => {
        setSubscriberEntitled(data.entitled);
        setAuthConfigured(data.authConfigured);
      })
      .catch(() => {
        setSubscriberEntitled(false);
      });
  }, [sessionStatus]);

  useEffect(() => {
    fetch("/api/question-types", { cache: "no-store" })
      .then(async (response) => {
        if (!response.ok) {
          throw new Error("Failed to load question types (is the Python API running?)");
        }
        const contentType = response.headers.get("content-type") ?? "";
        if (!contentType.includes("application/json")) {
          throw new Error("Question types API returned non-JSON (check Next rewrites / Python API)");
        }
        return response.json();
      })
      .then((data) => setTypes(data.types))
      .catch((err: Error) => setError(err.message));
  }, []);

  useEffect(() => {
    if (deepLinkAppliedRef.current) {
      return;
    }
    const modeParam = searchParams.get("mode");
    if (modeParam !== "progressive") {
      return;
    }
    deepLinkAppliedRef.current = true;
    setMode("progressive");
    const seedParam = searchParams.get("seed");
    if (seedParam) {
      setProgressiveSeed(seedParam);
    }
    const countParam = searchParams.get("count");
    if (countParam) {
      setProgressiveCount(Math.max(1, Number(countParam) || 10));
    }
    const titleParam = searchParams.get("title");
    if (titleParam) {
      setTitle(titleParam);
    }
    const relatedParam = searchParams.get("include_related");
    if (relatedParam === "0" || relatedParam === "false") {
      setIncludeRelated(false);
    }
    const rngParam = searchParams.get("rng_seed");
    if (rngParam) {
      setRngSeed(Number(rngParam) || null);
    }
    const wsDiff = searchParams.get("worksheetDifficulty");
    const knownPresets = new Set<string>([
      ...WORKSHEET_DIFFICULTY_PRESETS,
      "easy",
      "medium",
      "hard",
      "d0-8",
      "d4-14",
      "d10-22",
      "d0-3",
      "d3-20",
      "d8-25",
      "d20-25",
    ]);
    if (wsDiff && knownPresets.has(wsDiff)) {
      const ramp = worksheetDifficultyToRamp(wsDiff);
      setWorksheetDifficulty(ramp.level);
      setProgressiveDMin(ramp.d_min);
      setProgressiveDMax(ramp.d_max);
    } else {
      const dMinParam = searchParams.get("d_min");
      const dMaxParam = searchParams.get("d_max");
      if (dMinParam != null) {
        setProgressiveDMin(Number(dMinParam) || 0);
      }
      if (dMaxParam != null) {
        setProgressiveDMax(Number(dMaxParam) || 0);
      }
      setWorksheetDifficulty("custom");
    }
    if (searchParams.get("auto") === "1") {
      autoGenerateRef.current = true;
    }
  }, [searchParams]);

  useEffect(() => {
    if (!progressiveSeed && continuousTypes.length > 0 && !deepLinkAppliedRef.current) {
      const preferred =
        continuousTypes.find((type) => type.id === "g6_introduction_to_ratios") ??
        continuousTypes.find((type) => type.id === "pa_simplifying_fractions") ??
        continuousTypes[0];
      setProgressiveSeed(preferred.id);
    }
  }, [continuousTypes, progressiveSeed]);

  const totalPlanned = useMemo(
    () =>
      mode === "progressive"
        ? progressiveCount
        : sections.reduce((sum, section) => sum + section.count, 0),
    [mode, progressiveCount, sections],
  );

  const applyColumns = (draft: WorksheetDraft): WorksheetDraft => ({
    ...draft,
    columns: resolveColumnCount(draft.questions.length, maxColumns),
  });

  useEffect(() => {
    if (mode === "progressive") {
      return;
    }

    if (skipNextSectionSyncRef.current) {
      skipNextSectionSyncRef.current = false;
      lastContentKeyRef.current = contentKey;
      lastSectionsRef.current = sections;
      return;
    }

    if (sections.length === 0) {
      if (!paid && !subscriberEntitled) {
        setWorksheet(null);
        setError(null);
        setLoading(false);
        lastContentKeyRef.current = "";
        lastSectionsRef.current = [];
      }
      return;
    }

    if (contentKey !== lastContentKeyRef.current && !paid && !subscriberEntitled) {
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
    const previousSections = lastSectionsRef.current;

    syncWorksheetFromSections(worksheetRef.current, sections, title, maxColumns, previousSections)
      .then((draft) => {
        if (cancelled) return;
        lastContentKeyRef.current = contentKey;
        lastSectionsRef.current = sections;
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
  }, [contentKey, orderKey, mode]);

  useEffect(() => {
    setWorksheet((current) => (current ? { ...current, title } : current));
  }, [title]);

  useEffect(() => {
    setWorksheet((current) => (current ? applyColumns(current) : current));
  }, [maxColumns]);

  const closeTopicModal = () => {
    setTopicModalOpen(false);
    setEditingSectionId(null);
    setAddingTypeId(null);
  };

  const openTopicEditor = (section: TopicSection) => {
    setAddingTypeId(null);
    setEditingSectionId(section.id);
    setTopicModalOpen(true);
  };

  const openTopicAdder = (typeId: string) => {
    if (mode === "progressive") {
      setProgressiveSeed(typeId);
      return;
    }
    setEditingSectionId(null);
    setAddingTypeId(typeId);
    setTopicModalOpen(true);
  };

  const handleProgressiveGenerate = async () => {
    if (!progressiveSeed) {
      setError("Pick a seed topic for progressive practice.");
      return;
    }
    setLoading(true);
    setError(null);
    if (!paid && !subscriberEntitled) {
      setPaid(false);
      setWorksheetId(null);
    }
    try {
      const result = await generateProgressive({
        seeds: [progressiveSeed],
        count: progressiveCount,
        d_min: progressiveDMin,
        d_max: progressiveDMax,
        ...(worksheetDifficulty !== "custom"
          ? { worksheet_difficulty: worksheetDifficulty }
          : {}),
        include_related: includeRelated,
        title,
        ...(rngSeed != null ? { rng_seed: rngSeed } : {}),
      });
      const draft = applyColumns(questionSetToDraft(result));
      setWorksheet(draft);
      setProgressiveTopics(result.progressive?.topics ?? []);
      if (result.sections?.length) {
        skipNextSectionSyncRef.current = true;
        const nextSections = progressiveApiSectionsToTopicSections(result.sections);
        lastContentKeyRef.current = sectionContentKey(nextSections);
        lastSectionsRef.current = nextSections;
        setSections(nextSections);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to generate progressive worksheet");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!autoGenerateRef.current) {
      return;
    }
    if (mode !== "progressive" || !progressiveSeed || loading) {
      return;
    }
    autoGenerateRef.current = false;
    void handleProgressiveGenerate();
    // Intentionally once when deep-link auto=1 and seed is ready.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mode, progressiveSeed]);

  const unlocked = paid || subscriberEntitled;
  const canExport = Boolean(worksheet && worksheet.questions.length > 0 && !loading);
  const exportEnabled = canExport && (!paymentsRequired || unlocked);
  const showPaymentGate = paymentsRequired && !unlocked;

  return (
    <>
      <div className="worksheet-workspace">
        <aside className="left-rail">
          <section className="panel">
            <h2>Worksheet settings</h2>
            <label className="field">
              <span>Mode</span>
              <select
                value={mode}
                onChange={(event) => setMode(event.target.value as WorksheetMode)}
              >
                <option value="manual">Manual topics</option>
                <option value="progressive">Progressive practice</option>
              </select>
            </label>
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

            <WorksheetPageLayoutControls
              settings={pageLayout}
              fit={pageFit}
              onChange={setPageLayout}
            />

            {mode === "progressive" && (
              <div className="progressive-controls">
                <label className="field">
                  <span>Seed topic</span>
                  <select
                    value={progressiveSeed}
                    onChange={(event) => setProgressiveSeed(event.target.value)}
                  >
                    {continuousTypes.map((type) => (
                      <option key={type.id} value={type.id}>
                        {formatTopicLabel(type.id, type.name, { category: type.category })}
                      </option>
                    ))}
                  </select>
                </label>
                <label className="field">
                  <span>Questions</span>
                  <input
                    type="number"
                    min={1}
                    max={40}
                    value={progressiveCount}
                    onChange={(event) =>
                      setProgressiveCount(Math.max(1, Number(event.target.value) || 1))
                    }
                  />
                </label>
                <label className="field">
                  <span>Worksheet difficulty</span>
                  <select
                    value={worksheetDifficulty}
                    onChange={(event) => {
                      const value = event.target.value as WorksheetDifficultyPreset | "custom";
                      setWorksheetDifficulty(value);
                      if (value !== "custom") {
                        const ramp = worksheetDifficultyToRamp(value);
                        setProgressiveDMin(ramp.d_min);
                        setProgressiveDMax(ramp.d_max);
                      }
                    }}
                  >
                    <option value="custom">Custom D range</option>
                    {WORKSHEET_DIFFICULTY_PRESETS.map((level) => {
                      const ramp = worksheetDifficultyToRamp(level);
                      return (
                        <option key={level} value={level}>
                          {ramp.label} (D {ramp.d_min}–{ramp.d_max})
                        </option>
                      );
                    })}
                  </select>
                </label>
                <div className="field-bool-row">
                  <label className="field field-compact">
                    <span>D min</span>
                    <input
                      type="number"
                      min={0}
                      value={progressiveDMin}
                      onChange={(event) => {
                        setWorksheetDifficulty("custom");
                        setProgressiveDMin(Number(event.target.value) || 0);
                      }}
                    />
                  </label>
                  <label className="field field-compact">
                    <span>D max</span>
                    <input
                      type="number"
                      min={0}
                      value={progressiveDMax}
                      onChange={(event) => {
                        setWorksheetDifficulty("custom");
                        setProgressiveDMax(Number(event.target.value) || 0);
                      }}
                    />
                  </label>
                </div>
                <label className="field field-inline">
                  <input
                    type="checkbox"
                    checked={includeRelated}
                    onChange={(event) => setIncludeRelated(event.target.checked)}
                  />
                  <span>Include related topics</span>
                </label>
                <button
                  type="button"
                  className="primary"
                  disabled={loading || !progressiveSeed}
                  onClick={() => void handleProgressiveGenerate()}
                >
                  {loading ? "Generating…" : "Generate progressive worksheet"}
                </button>
                {progressiveTopics.length > 0 && (
                  <p className="plan-summary">
                    Topics:{" "}
                    {progressiveTopics
                      .map((tid) => {
                        const t = continuousTypes.find((x) => x.id === tid);
                        return formatTopicLabel(tid, t?.name, { category: t?.category });
                      })
                      .join(", ")}
                  </p>
                )}
              </div>
            )}

            <div className="settings-export-actions">
              {paymentsRequired ? (
                unlocked ? (
                  <>
                    <ExportPdfButton disabled={!exportEnabled} />
                    {subscriberEntitled && (
                      <p className="plan-summary">Pro subscription — unlimited exports.</p>
                    )}
                    {paid && !subscriberEntitled && worksheetId && (
                      <p className="plan-summary">Worksheet unlocked for export.</p>
                    )}
                  </>
                ) : (
                  <>
                    <PayForPdfButton
                      disabled={!canExport || !stripeConfigured || !worksheet}
                      title={title}
                      worksheet={worksheet!}
                      priceCents={pdfPriceCents}
                      onCheckoutStart={setWorksheetId}
                      onError={setError}
                    />
                    <SubscribeButton
                      disabled={!stripeConfigured || !subscriptionEnabled}
                      priceCents={subscriptionPriceCents}
                      authConfigured={authConfigured}
                      onError={setError}
                    />
                    {!stripeConfigured && (
                      <p className="error">
                        {stripeKeyError ??
                          "Stripe is not configured. Add sk_test_... to STRIPE_SECRET_KEY in .env.local and restart the dev server."}
                      </p>
                    )}
                    {stripeConfigured && !subscriptionEnabled && (
                      <p className="plan-summary">
                        Subscription checkout needs Google auth + STRIPE_SUBSCRIPTION_PRICE_ID.
                      </p>
                    )}
                  </>
                )
              ) : (
                <ExportPdfButton disabled={!exportEnabled} />
              )}

              {error && <p className="error">{error}</p>}
            </div>
          </section>

          <section className="panel action-rail">
            <div className="action-rail-scroll">
              <h2>Questions</h2>
              <p className="plan-summary">
                Planned questions: <strong>{totalPlanned}</strong>
                {mode === "progressive" ? " (progressive ramp)" : ""}
              </p>

              {mode === "manual" ? (
                <TopicSectionList
                  sections={sections}
                  types={types}
                  onSectionsChange={setSections}
                  onEditSection={openTopicEditor}
                  onRemoveSection={(sectionId) => {
                    setSections((current) => current.filter((section) => section.id !== sectionId));
                  }}
                  compact
                />
              ) : (
                <p className="hint">
                  Progressive mode builds a rising-difficulty mix from the seed topic
                  {includeRelated ? " and related family/prereq neighbors" : ""}. Use the
                  curriculum browser to change the seed.
                </p>
              )}
            </div>
          </section>
        </aside>

        <div className="worksheet-main">
          {loading && <p className="worksheet-status interactive-only">Generating worksheet...</p>}
          {showPaymentGate && worksheet && (
            <p className="worksheet-status preview-banner interactive-only">
              Preview mode — pay once or subscribe to unlock the answer key and PDF export.
            </p>
          )}
          <WorksheetPageLayout
            settings={pageLayout}
            contentKey={`${contentKey}|${orderKey}|${worksheet?.questions.length ?? 0}|${maxColumns}|${title}`}
            onFitChange={setPageFit}
          >
            <InteractiveWorksheet
              worksheet={worksheet}
              types={types}
              previewMode={showPaymentGate}
              onChange={(next) => {
                setWorksheet(applyColumns(next));
              }}
              onError={setError}
            />
          </WorksheetPageLayout>
        </div>

        <aside className="right-rail topics-rail">
          <AddTopicPanel types={types} onSelectType={openTopicAdder} />
        </aside>
      </div>

      <AddTopicModal
        open={topicModalOpen}
        types={types}
        sections={sections}
        editingSectionId={editingSectionId}
        addingTypeId={addingTypeId}
        onClose={closeTopicModal}
        onSectionsChange={setSections}
        onSwitchType={(typeId) => {
          setEditingSectionId(null);
          setAddingTypeId(typeId);
          setTopicModalOpen(true);
        }}
      />
    </>
  );
}
