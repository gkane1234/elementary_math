"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
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
import { WorksheetPresetRail } from "@/components/WorksheetPresetRail";
import {
  generateProgressive,
  type ProgressiveGenerateResult,
  type ProgressivePlan,
} from "@/lib/api";
import { resolveColumnCount } from "@/lib/columns";
import { fetchEntitlement } from "@/lib/payment";
import {
  continuousReadyTypes,
  progressiveApiSectionsToTopicSections,
  summarizePhaseOrder,
  type ProgressivePairing,
  type ProgressiveScope,
  type ProgressiveStyle,
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
import {
  defaultGalleryEntry,
  galleryEntryRamp,
  galleryProgressiveRequest,
  getGalleryEntry,
  listGalleryEntries,
  worksheetsIncludingTopic,
} from "@/lib/worksheet-gallery";
import {
  courseOfType,
  scopeTopicChoices,
  spiralSuggestionText,
} from "@/lib/worksheet-template";
import {
  newPresetId,
  presetsIncludingTopic,
  readSavedPresets,
  removePreset,
  topicsOnWorksheet,
  upsertPreset,
  writeSavedPresets,
  type SavedWorksheetPreset,
} from "@/lib/worksheet-presets";

const openingEntry = defaultGalleryEntry();
const openingRamp = openingEntry ? galleryEntryRamp(openingEntry) : null;

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
  const opensFromLink = searchParams.get("mode") === "progressive";
  const [types, setTypes] = useState<QuestionTypeInfo[]>([]);
  const [sections, setSections] = useState<TopicSection[]>([]);
  const [title, setTitle] = useState(
    restoredUnlock?.worksheet.title ??
      (opensFromLink ? searchParams.get("title") : null) ??
      openingEntry?.title ??
      "Math Practice",
  );
  const [maxColumns, setMaxColumns] = useState<string>("auto");
  const [worksheet, setWorksheet] = useState<WorksheetDraft | null>(restoredUnlock?.worksheet ?? null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [topicModalOpen, setTopicModalOpen] = useState(false);
  const [editingSectionId, setEditingSectionId] = useState<string | null>(null);
  const [addingTypeId, setAddingTypeId] = useState<string | null>(null);
  const [paid, setPaid] = useState(Boolean(restoredUnlock));
  const [worksheetId, setWorksheetId] = useState<string | null>(restoredUnlock?.worksheetId ?? null);
  const [paymentsRequired, setPaymentsRequired] = useState<boolean | null>(null);
  const [pdfPriceCents, setPdfPriceCents] = useState(300);
  const [subscriptionPriceCents, setSubscriptionPriceCents] = useState(1000);
  const [subscriptionEnabled, setSubscriptionEnabled] = useState(false);
  const [authConfigured, setAuthConfigured] = useState(false);
  const [subscriberEntitled, setSubscriberEntitled] = useState(false);
  const [stripeConfigured, setStripeConfigured] = useState(false);
  const [stripeKeyError, setStripeKeyError] = useState<string | null>(null);
  const [pageLayout, setPageLayout] = useState<PageLayoutSettings>(DEFAULT_PAGE_LAYOUT);
  const [pageFit, setPageFit] = useState<FitScales | null>(null);

  const [mode, setMode] = useState<WorksheetMode>(
    restoredUnlock || opensFromLink ? "manual" : "progressive",
  );
  const [progressiveSeed, setProgressiveSeed] = useState(
    opensFromLink ? (searchParams.get("seed") ?? "") : (openingEntry?.seeds[0] ?? ""),
  );
  const [progressiveCount, setProgressiveCount] = useState(openingEntry?.count ?? 10);
  const [progressiveDMin, setProgressiveDMin] = useState(openingRamp?.d_min ?? 0);
  const [progressiveDMax, setProgressiveDMax] = useState(openingRamp?.d_max ?? 18);
  const [worksheetDifficulty, setWorksheetDifficulty] = useState<
    WorksheetDifficultyPreset | "custom"
  >(openingRamp?.level ?? "custom");
  const [selectedGalleryId, setSelectedGalleryId] = useState(
    restoredUnlock || opensFromLink ? "" : (openingEntry?.id ?? ""),
  );
  const [browsedTypeId, setBrowsedTypeId] = useState("");
  const [galleryTopics, setGalleryTopics] = useState<Record<string, string[]>>({});
  const [savedPresets, setSavedPresets] = useState<SavedWorksheetPreset[]>([]);
  const [includeRelated, setIncludeRelated] = useState(true);
  const [progressiveTopics, setProgressiveTopics] = useState<string[]>([]);
  const [progressivePlan, setProgressivePlan] = useState<ProgressivePlan | null>(null);
  const [rngSeed, setRngSeed] = useState<number | null>(null);
  const [pairing, setPairing] = useState<ProgressivePairing>(openingEntry?.pairing ?? "lesson");
  const [scope, setScope] = useState<ProgressiveScope>(openingEntry?.scope ?? "topic");
  const [difficultyStyle, setDifficultyStyle] = useState<ProgressiveStyle>(
    openingEntry?.style ?? "ramp",
  );
  const [rampEachTopic, setRampEachTopic] = useState(Boolean(openingEntry?.rampEachTopic));
  const [checkedTopics, setCheckedTopics] = useState<string[]>([]);
  const [topicPin, setTopicPin] = useState<string[] | null>(null);

  const worksheetRef = useRef<WorksheetDraft | null>(null);
  const lastContentKeyRef = useRef<string>("");
  const lastSectionsRef = useRef<TopicSection[]>([]);
  const skipNextSectionSyncRef = useRef(false);
  const deepLinkAppliedRef = useRef(false);
  const autoGenerateRef = useRef(false);
  const openedDefaultRef = useRef(false);
  const galleryRequestRef = useRef(0);

  const contentKey = useMemo(() => sectionContentKey(sections), [sections]);
  const orderKey = useMemo(() => sectionOrderKey(sections), [sections]);
  const continuousTypes = useMemo(() => continuousReadyTypes(types), [types]);
  const templateCourse = useMemo(() => courseOfType(progressiveSeed), [progressiveSeed]);
  const selectableTypeIds = useMemo(
    () => new Set(continuousTypes.map((type) => type.id)),
    [continuousTypes],
  );
  const checklist = useMemo(() => {
    if (!templateCourse || scope === "topic") return [];
    return scopeTopicChoices(progressiveSeed, scope).filter((choice) =>
      selectableTypeIds.has(choice.typeId),
    );
  }, [templateCourse, progressiveSeed, scope, selectableTypeIds]);
  const checklistKey = checklist.map((choice) => choice.typeId).join("|");
  const spiralHint = templateCourse ? spiralSuggestionText(progressiveSeed, pairing) : null;

  useEffect(() => {
    if (!templateCourse || scope === "topic") return;
    const ids = checklist.map((choice) => choice.typeId);
    if (topicPin) {
      if (ids.length === 0) return;
      const allowed = new Set(ids);
      setCheckedTopics(topicPin.filter((id) => allowed.has(id)));
      return;
    }
    setCheckedTopics(ids);
  }, [templateCourse, progressiveSeed, scope, checklistKey, topicPin, checklist]);

  worksheetRef.current = worksheet;

  useEffect(() => {
    if (restoredUnlock) {
      window.sessionStorage.removeItem(UNLOCK_STORAGE_KEY);
    }
  }, [restoredUnlock]);

  useEffect(() => {
    setSavedPresets(readSavedPresets(window.localStorage));
  }, []);

  const persistPresets = (next: SavedWorksheetPreset[]) => {
    setSavedPresets(next);
    writeSavedPresets(window.localStorage, next);
  };

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
    const matchedGallery = listGalleryEntries().find(
      (entry) =>
        entry.seeds[0] === (seedParam ?? "") && (!titleParam || entry.title === titleParam),
    );
    if (matchedGallery) {
      setSelectedGalleryId(matchedGallery.id);
    }
    const relatedParam = searchParams.get("include_related");
    if (relatedParam === "0" || relatedParam === "false") {
      setIncludeRelated(false);
    }
    const pairingParam = searchParams.get("pairing");
    if (pairingParam === "lesson" || pairingParam === "drill" || pairingParam === "spiral") {
      setPairing(pairingParam);
    }
    const scopeParam = searchParams.get("scope");
    if (scopeParam === "topic" || scopeParam === "unit" || scopeParam === "adjacent") {
      setScope(scopeParam);
    }
    const styleParam = searchParams.get("style");
    if (styleParam === "ramp" || styleParam === "straight") {
      setDifficultyStyle(styleParam);
    }
    const rampEachParam = searchParams.get("ramp_each_topic");
    if (rampEachParam === "1" || rampEachParam === "true") {
      setRampEachTopic(true);
    } else if (rampEachParam === "0" || rampEachParam === "false") {
      setRampEachTopic(false);
    }
    const topicsParam = searchParams.get("topics");
    if (topicsParam) {
      setTopicPin(topicsParam.split(",").map((id) => id.trim()).filter(Boolean));
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

  const applyProgressiveResult = (result: ProgressiveGenerateResult) => {
    const draft = applyColumns(questionSetToDraft(result));
    setWorksheet(draft);
    setProgressivePlan(result.progressive ?? null);
    setProgressiveTopics(result.progressive?.topics ?? []);
    if (result.title) {
      setTitle(result.title);
    }
    if (result.sections?.length) {
      skipNextSectionSyncRef.current = true;
      const nextSections = progressiveApiSectionsToTopicSections(result.sections);
      lastContentKeyRef.current = sectionContentKey(nextSections);
      lastSectionsRef.current = nextSections;
      setSections(nextSections);
    }
  };

  const loadGalleryEntry = async (entryId: string) => {
    const entry = getGalleryEntry(entryId);
    if (!entry) return;
    const ramp = galleryEntryRamp(entry);
    const requestId = galleryRequestRef.current + 1;
    galleryRequestRef.current = requestId;
    setSelectedGalleryId(entry.id);
    setMode("progressive");
    setProgressiveSeed(entry.seeds[0] ?? "");
    setProgressiveCount(entry.count);
    setWorksheetDifficulty(ramp.level);
    setProgressiveDMin(ramp.d_min);
    setProgressiveDMax(ramp.d_max);
    setIncludeRelated(entry.includeRelated !== false);
    setPairing(entry.pairing ?? "lesson");
    setScope(entry.scope ?? "topic");
    setDifficultyStyle(entry.style ?? "ramp");
    setRampEachTopic(Boolean(entry.rampEachTopic));
    setTopicPin(entry.topics ?? null);
    setTitle(entry.title);
    setRngSeed(entry.seed);
    setWorksheet({ title: entry.title, questions: [], columns: 1 });
    setLoading(true);
    setError(null);
    if (!subscriberEntitled) {
      setPaid(false);
      setWorksheetId(null);
    }
    try {
      const result = await generateProgressive(galleryProgressiveRequest(entry, entry.seed));
      if (galleryRequestRef.current !== requestId) return;
      applyProgressiveResult(result);
    } catch (err) {
      if (galleryRequestRef.current !== requestId) return;
      setError(err instanceof Error ? err.message : "Failed to open worksheet");
    } finally {
      if (galleryRequestRef.current === requestId) setLoading(false);
    }
  };

  const handleProgressiveGenerate = async () => {
    if (!progressiveSeed) {
      setError("Pick a seed topic for progressive practice.");
      return;
    }
    if (templateCourse && scope !== "topic" && checkedTopics.length === 0) {
      setError("Check at least one topic.");
      return;
    }
    const named = getGalleryEntry(selectedGalleryId);
    if (!named || named.seeds[0] !== progressiveSeed || named.title !== title) {
      setSelectedGalleryId("");
    }
    const requestId = galleryRequestRef.current + 1;
    galleryRequestRef.current = requestId;
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
        ...(templateCourse
          ? {
              pairing,
              scope,
              style: difficultyStyle,
              ramp_each_topic: rampEachTopic,
              ...(scope !== "topic" ? { topics: checkedTopics } : {}),
            }
          : {}),
        ...(rngSeed != null ? { rng_seed: rngSeed } : {}),
      });
      if (galleryRequestRef.current !== requestId) return;
      applyProgressiveResult(result);
    } catch (err) {
      if (galleryRequestRef.current !== requestId) return;
      setError(err instanceof Error ? err.message : "Failed to generate progressive worksheet");
    } finally {
      if (galleryRequestRef.current === requestId) setLoading(false);
    }
  };

  useEffect(() => {
    if (openedDefaultRef.current || restoredUnlock) return;
    if (searchParams.get("mode") === "progressive") return;
    const entry = defaultGalleryEntry();
    if (!entry) return;
    openedDefaultRef.current = true;
    void loadGalleryEntry(entry.id);
    // Open the catalog sheet once, as soon as the generator mounts.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchParams, restoredUnlock]);

  useEffect(() => {
    let cancelled = false;
    void Promise.all(
      listGalleryEntries().map(async (entry) => {
        try {
          const result = await generateProgressive({
            ...galleryProgressiveRequest(entry, entry.seed),
            plan_only: true,
          });
          return [entry.id, result.progressive?.topics ?? []] as const;
        } catch {
          return [entry.id, [] as string[]] as const;
        }
      }),
    ).then((pairs) => {
      if (cancelled) return;
      const next: Record<string, string[]> = {};
      for (const [id, topics] of pairs) {
        if (topics.length > 0) next[id] = [...topics];
      }
      setGalleryTopics(next);
    });
    return () => {
      cancelled = true;
    };
  }, []);

  const loadSavedPreset = (presetId: string) => {
    const preset = savedPresets.find((entry) => entry.id === presetId);
    if (!preset) return;
    galleryRequestRef.current += 1;
    skipNextSectionSyncRef.current = true;
    lastContentKeyRef.current = sectionContentKey(preset.sections);
    lastSectionsRef.current = preset.sections;
    setSelectedGalleryId(preset.id);
    setMode("manual");
    setTitle(preset.worksheet.title || preset.title);
    setSections(preset.sections);
    setWorksheet(applyColumns({ ...preset.worksheet, title: preset.worksheet.title || preset.title }));
    setProgressiveTopics(preset.topics);
    setLoading(false);
    setError(null);
    if (!subscriberEntitled) {
      setPaid(false);
      setWorksheetId(null);
    }
  };

  const saveCurrentPreset = () => {
    if (!worksheet || worksheet.questions.length === 0) return;
    const current = savedPresets.find((entry) => entry.id === selectedGalleryId);
    const preset: SavedWorksheetPreset = {
      id: current?.id ?? newPresetId(),
      title: worksheet.title || title || "Saved worksheet",
      savedAt: new Date().toISOString(),
      worksheet: { ...worksheet, title: worksheet.title || title || "Saved worksheet" },
      sections,
      topics: topicsOnWorksheet(worksheet, sections),
    };
    persistPresets(upsertPreset(savedPresets, preset));
    setSelectedGalleryId(preset.id);
  };

  const deleteSavedPreset = (presetId: string) => {
    persistPresets(removePreset(savedPresets, presetId));
    if (selectedGalleryId === presetId) setSelectedGalleryId("");
  };

  const handleBrowseType = useCallback((typeId: string | null) => {
    setBrowsedTypeId((current) => {
      const next = typeId ?? "";
      return current === next ? current : next;
    });
  }, []);

  const softwareMatches = useMemo(
    () => worksheetsIncludingTopic(browsedTypeId, galleryTopics),
    [browsedTypeId, galleryTopics],
  );
  const savedMatches = useMemo(
    () => presetsIncludingTopic(savedPresets, browsedTypeId),
    [savedPresets, browsedTypeId],
  );
  const catalogSheets = useMemo(() => listGalleryEntries(), []);
  const browsedType = types.find((type) => type.id === browsedTypeId);
  const browsedLabel = browsedType
    ? formatTopicLabel(browsedType.id, browsedType.name, { category: browsedType.category })
    : "";

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
  const exportEnabled = canExport && (paymentsRequired !== true || unlocked);
  const showPaymentGate = paymentsRequired === true && !unlocked;

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
              <input
                type="text"
                value={title}
                onChange={(event) => {
                  const next = event.target.value;
                  setTitle(next);
                  const named = getGalleryEntry(selectedGalleryId);
                  if (named && named.title !== next) setSelectedGalleryId("");
                }}
              />
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
                    onChange={(event) => {
                      setTopicPin(null);
                      setSelectedGalleryId("");
                      setProgressiveSeed(event.target.value);
                    }}
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
                {templateCourse && (
                  <>
                    <label className="field">
                      <span>Scope</span>
                      <select
                        value={scope}
                        onChange={(event) => {
                          setTopicPin(null);
                          setSelectedGalleryId("");
                          setScope(event.target.value as ProgressiveScope);
                        }}
                      >
                        <option value="topic">One topic</option>
                        <option value="unit">This unit</option>
                        <option value="adjacent">This unit and the next</option>
                      </select>
                    </label>
                    <label className="field">
                      <span>Pairing</span>
                      <select
                        value={pairing}
                        onChange={(event) => {
                          setSelectedGalleryId("");
                          setPairing(event.target.value as ProgressivePairing);
                        }}
                      >
                        <option value="lesson">Lesson</option>
                        <option value="drill">Procedure drill</option>
                        <option value="spiral">Spiral</option>
                      </select>
                    </label>
                    <label className="field">
                      <span>Difficulty shape</span>
                      <select
                        value={difficultyStyle}
                        onChange={(event) => {
                          setSelectedGalleryId("");
                          setDifficultyStyle(event.target.value as ProgressiveStyle);
                        }}
                      >
                        <option value="ramp">Easy to hard</option>
                        <option value="straight">Flat</option>
                      </select>
                    </label>
                    {difficultyStyle === "ramp" && (
                      <label className="field field-inline">
                        <input
                          type="checkbox"
                          checked={rampEachTopic}
                          onChange={(event) => {
                            setSelectedGalleryId("");
                            setRampEachTopic(event.target.checked);
                          }}
                        />
                        <span>Ramp each topic</span>
                      </label>
                    )}
                    {scope !== "topic" && (
                      <fieldset className="topic-checklist">
                        <legend>Topics</legend>
                        {checklist.map((choice) => (
                          <label key={choice.typeId}>
                            <input
                              type="checkbox"
                              checked={checkedTopics.includes(choice.typeId)}
                              onChange={(event) => {
                                setSelectedGalleryId("");
                                const next = event.target.checked;
                                setCheckedTopics((current) => {
                                  if (next) {
                                    return current.includes(choice.typeId)
                                      ? current
                                      : [...current, choice.typeId];
                                  }
                                  return current.filter((id) => id !== choice.typeId);
                                });
                              }}
                            />
                            <span>{choice.name}</span>
                          </label>
                        ))}
                      </fieldset>
                    )}
                    {spiralHint && pairing !== "spiral" && (
                      <p className="spiral-hint">{spiralHint}</p>
                    )}
                    <p className="plan-summary">
                      Template:{" "}
                      {scope === "topic"
                        ? "one topic"
                        : scope === "unit"
                          ? "this unit"
                          : "this unit and the next"}
                      , {pairing === "lesson" ? "lesson" : pairing === "drill" ? "procedure drill" : "spiral"}
                      , {difficultyStyle === "ramp" ? "easy to hard" : "flat"}
                      {scope !== "topic" ? `, ${checkedTopics.length} checked` : ""}
                      {difficultyStyle === "ramp" && rampEachTopic ? ", ramp each topic" : ""}
                    </p>
                  </>
                )}
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
                {progressivePlan?.phases && progressivePlan.phases.length > 0 && templateCourse && (
                  <p className="plan-summary">
                    Order: {summarizePhaseOrder(progressivePlan.phases)}
                  </p>
                )}
                {progressivePlan?.omitted_topics && progressivePlan.omitted_topics.length > 0 && (
                  <p className="plan-summary">
                    Not placed:{" "}
                    {progressivePlan.omitted_topics
                      .map((tid) => {
                        const t = continuousTypes.find((x) => x.id === tid);
                        return formatTopicLabel(tid, t?.name, { category: t?.category });
                      })
                      .join(", ")}
                  </p>
                )}
              </div>
            )}

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
                  onSectionsChange={(next) => {
                    setSelectedGalleryId("");
                    setSections(next);
                  }}
                  onEditSection={openTopicEditor}
                  onRemoveSection={(sectionId) => {
                    setSelectedGalleryId("");
                    setSections((current) => current.filter((section) => section.id !== sectionId));
                  }}
                  compact
                />
              ) : (
                <p className="hint">
                  {templateCourse
                    ? "This course uses a worksheet template: lesson order, an optional procedure drill, then one follow-on skill. Easy to hard is the default. Flat difficulty, spiral, and the topic checklist are customizations."
                    : `Progressive mode builds a rising-difficulty mix from the seed topic${
                        includeRelated ? " and related family/prereq neighbors" : ""
                      }. Use the curriculum browser to change the seed.`}
                </p>
              )}
            </div>
          </section>
        </aside>

        <div className="worksheet-stage">
          <div className="worksheet-stage-bar interactive-only">
            <label className="field worksheet-picker">
              <span>Worksheet</span>
              <select
                aria-label="Worksheet"
                value={selectedGalleryId}
                onChange={(event) => {
                  const id = event.target.value;
                  if (!id) {
                    setSelectedGalleryId("");
                    return;
                  }
                  if (savedPresets.some((preset) => preset.id === id)) {
                    loadSavedPreset(id);
                    return;
                  }
                  void loadGalleryEntry(id);
                }}
              >
                <option value="">Custom</option>
                {savedPresets.length > 0 && (
                  <optgroup label="Saved">
                    {savedPresets.map((preset) => (
                      <option key={preset.id} value={preset.id}>
                        {preset.title}
                      </option>
                    ))}
                  </optgroup>
                )}
                <optgroup label="Included">
                  {catalogSheets.map((entry) => (
                    <option key={entry.id} value={entry.id}>
                      {entry.title}
                    </option>
                  ))}
                </optgroup>
              </select>
            </label>

            <div className="worksheet-stage-pay">
              {paymentsRequired && !unlocked && (
                <p className="worksheet-pay-note">
                  Pay for this worksheet, or subscribe for every worksheet.
                </p>
              )}
              {paymentsRequired ? (
                unlocked ? (
                  <>
                    <ExportPdfButton disabled={!exportEnabled} />
                    {subscriberEntitled && (
                      <p className="plan-summary">Pro subscription — unlimited exports.</p>
                    )}
                    {paid && !subscriberEntitled && worksheetId && (
                      <p className="plan-summary">This worksheet is unlocked.</p>
                    )}
                  </>
                ) : (
                  <>
                    {worksheet && worksheet.questions.length > 0 ? (
                      <PayForPdfButton
                        disabled={!canExport || !stripeConfigured}
                        title={title}
                        worksheet={worksheet}
                        priceCents={pdfPriceCents}
                        onCheckoutStart={setWorksheetId}
                        onError={setError}
                      />
                    ) : (
                      <button className="primary" type="button" disabled>
                        Pay for this worksheet
                      </button>
                    )}
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
            </div>
          </div>

          {showPaymentGate && worksheet && worksheet.questions.length > 0 && (
            <p className="worksheet-status preview-banner interactive-only">
              Preview — pay for this worksheet or subscribe to unlock the answer key and PDF.
            </p>
          )}
          {loading && (
            <p className="worksheet-status interactive-only">Building this page…</p>
          )}
          {error && <p className="error interactive-only">{error}</p>}

          <WorksheetPageLayout
            settings={pageLayout}
            contentKey={`${contentKey}|${orderKey}|${worksheet?.questions.length ?? 0}|${maxColumns}|${title}`}
            onFitChange={setPageFit}
          >
            <InteractiveWorksheet
              worksheet={worksheet}
              types={types}
              pageTitle={title}
              loading={loading}
              previewMode={showPaymentGate && Boolean(worksheet && worksheet.questions.length > 0)}
              onChange={(next) => {
                setWorksheet(applyColumns(next));
              }}
              onError={setError}
            />
          </WorksheetPageLayout>
        </div>

        <aside className="right-rail topics-rail">
          <WorksheetPresetRail
            topicLabel={browsedLabel}
            softwareMatches={softwareMatches}
            savedMatches={savedMatches}
            savedPresets={savedPresets}
            canSave={Boolean(worksheet && worksheet.questions.length > 0 && !loading)}
            onSave={saveCurrentPreset}
            onLoadSoftware={(id) => void loadGalleryEntry(id)}
            onLoadSaved={loadSavedPreset}
            onRemoveSaved={deleteSavedPreset}
          />
          <AddTopicPanel
            types={types}
            onSelectType={openTopicAdder}
            onBrowseTypeId={handleBrowseType}
          />
        </aside>
      </div>

      <AddTopicModal
        open={topicModalOpen}
        types={types}
        sections={sections}
        editingSectionId={editingSectionId}
        addingTypeId={addingTypeId}
        onClose={closeTopicModal}
        onSectionsChange={(next) => {
          setSelectedGalleryId("");
          setSections(next);
        }}
        onSwitchType={(typeId) => {
          setEditingSectionId(null);
          setAddingTypeId(typeId);
          setTopicModalOpen(true);
        }}
      />
    </>
  );
}
