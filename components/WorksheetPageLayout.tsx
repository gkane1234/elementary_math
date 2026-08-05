"use client";

import { useEffect, useLayoutEffect, useState, type ReactNode } from "react";
import {
  MAX_GAP_SCALE,
  MAX_SPACE_SCALE,
  MIN_FONT_SCALE,
  MIN_GAP_SCALE,
  MIN_SPACE_SCALE,
  PAGE_CONTENT_HEIGHT_PX,
  computeFitScales,
  fitScalesToCssVars,
  type FitScales,
  type PageLayoutSettings,
  type TargetPages,
} from "@/lib/worksheet-page-layout";

type WorksheetPageLayoutProps = {
  settings: PageLayoutSettings;
  /** Bump when worksheet content changes so we remeasure. */
  contentKey: string;
  onFitChange?: (fit: FitScales) => void;
  children: ReactNode;
};

function nextFrame(): Promise<void> {
  return new Promise((resolve) => {
    requestAnimationFrame(() => resolve());
  });
}

function clamp(value: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, value));
}

function refineScales(
  scales: FitScales,
  actualHeight: number,
  targetPages: Exclude<TargetPages, "auto">,
): FitScales {
  const targetHeight = targetPages * PAGE_CONTENT_HEIGHT_PX;
  if (actualHeight <= 0) return scales;
  const ratio = targetHeight / actualHeight;
  if (ratio >= 0.97 && ratio <= 1.03) {
    return { ...scales, status: scales.status === "auto" ? "auto" : scales.status, estimatedPages: targetPages };
  }

  if (ratio > 1) {
    const spaceScale = clamp(scales.spaceScale * ratio, 1, MAX_SPACE_SCALE);
    const gapScale = clamp(scales.gapScale * Math.sqrt(ratio), 1, MAX_GAP_SCALE);
    return {
      ...scales,
      spaceScale,
      gapScale,
      fontScale: 1,
      marginScale: 1,
      status: "spread",
      estimatedPages: targetPages,
      targetPages,
    };
  }

  const spaceScale = clamp(scales.spaceScale * ratio, MIN_SPACE_SCALE, 1);
  const gapScale = clamp(scales.gapScale * ratio, MIN_GAP_SCALE, 1);
  const fontScale = clamp(scales.fontScale * Math.min(1, ratio / 0.92), MIN_FONT_SCALE, 1);
  const stillShort = spaceScale <= MIN_SPACE_SCALE + 0.02 && fontScale <= MIN_FONT_SCALE + 0.02 && ratio < 0.97;
  return {
    ...scales,
    spaceScale,
    gapScale,
    fontScale,
    status: stillShort ? "overflow" : "tight",
    estimatedPages: stillShort ? Math.ceil(actualHeight / PAGE_CONTENT_HEIGHT_PX) : targetPages,
    targetPages,
  };
}

/**
 * Applies fit-to-N-pages CSS variables on #worksheet-preview and draws screen
 * page-break markers over the print layout. Print/PDF picks up the same vars.
 */
export function WorksheetPageLayout({
  settings,
  contentKey,
  onFitChange,
  children,
}: WorksheetPageLayoutProps) {
  const [fit, setFit] = useState<FitScales>(() => computeFitScales(0, settings.targetPages));

  useEffect(() => {
    onFitChange?.(fit);
  }, [fit, onFitChange]);

  useLayoutEffect(() => {
    const preview = document.getElementById("worksheet-preview");
    if (!preview) return;

    let cancelled = false;

    preview.dataset.showPageBreaks = settings.showPageBreaks ? "true" : "false";
    preview.dataset.targetPages = String(settings.targetPages);

    const applyScales = (scales: FitScales) => {
      const vars = fitScalesToCssVars(scales);
      for (const [key, value] of Object.entries(vars)) {
        preview.style.setProperty(key, value);
      }
      if (!cancelled) setFit(scales);
    };

    const ensureOverlay = (measureRoot: HTMLElement): HTMLElement => {
      let overlay = measureRoot.querySelector(
        ":scope > .worksheet-page-break-overlay",
      ) as HTMLElement | null;
      if (!overlay) {
        overlay = document.createElement("div");
        overlay.className = "worksheet-page-break-overlay interactive-only";
        overlay.setAttribute("aria-hidden", "true");
        measureRoot.appendChild(overlay);
      }
      return overlay;
    };

    const placeMarkers = (measureRoot: HTMLElement, scaledHeight: number) => {
      const overlay = ensureOverlay(measureRoot);
      overlay.replaceChildren();

      if (!settings.showPageBreaks || scaledHeight <= 0) {
        overlay.hidden = true;
        return;
      }

      overlay.hidden = false;
      overlay.style.height = `${scaledHeight}px`;

      const pageCount = Math.max(1, Math.ceil(scaledHeight / PAGE_CONTENT_HEIGHT_PX - 1e-6));
      for (let page = 1; page < pageCount; page += 1) {
        const marker = document.createElement("div");
        marker.className = "worksheet-page-break-marker";
        marker.style.top = `${page * PAGE_CONTENT_HEIGHT_PX}px`;
        const label = document.createElement("span");
        label.textContent = `Page ${page} ↑  ·  Page ${page + 1} ↓`;
        marker.appendChild(label);
        overlay.appendChild(marker);
      }
    };

    const measureHeight = (measureRoot: HTMLElement) =>
      Math.max(measureRoot.scrollHeight, measureRoot.offsetHeight);

    const runMeasure = async () => {
      const measureRoot = preview.querySelector(".worksheet-print-measure") as HTMLElement | null;
      if (!measureRoot || cancelled) return;

      applyScales(computeFitScales(0, "auto"));
      await nextFrame();
      if (cancelled) return;

      const naturalHeight = measureHeight(measureRoot);
      let scales = computeFitScales(naturalHeight, settings.targetPages);
      applyScales(scales);
      await nextFrame();
      if (cancelled) return;

      if (settings.targetPages !== "auto") {
        for (let i = 0; i < 3; i += 1) {
          const actual = measureHeight(measureRoot);
          const next = refineScales(scales, actual, settings.targetPages);
          const changed =
            Math.abs(next.spaceScale - scales.spaceScale) > 0.02 ||
            Math.abs(next.gapScale - scales.gapScale) > 0.02 ||
            Math.abs(next.fontScale - scales.fontScale) > 0.01;
          scales = next;
          applyScales(scales);
          await nextFrame();
          if (cancelled) return;
          if (!changed) break;
        }
      }

      placeMarkers(measureRoot, measureHeight(measureRoot));
    };

    void runMeasure();
    const t1 = window.setTimeout(() => void runMeasure(), 350);
    const t2 = window.setTimeout(() => void runMeasure(), 1000);

    return () => {
      cancelled = true;
      window.clearTimeout(t1);
      window.clearTimeout(t2);
    };
  }, [settings.showPageBreaks, settings.targetPages, contentKey]);

  return <div className="worksheet-page-layout-root">{children}</div>;
}
