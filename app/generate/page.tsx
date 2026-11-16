import type { Metadata } from "next";
import { Suspense } from "react";
import { WorksheetGenerator } from "@/components/WorksheetGenerator";
import { defaultGalleryEntry } from "@/lib/worksheet-gallery";

export const metadata: Metadata = {
  title: "Generator",
  description: "Build a printable math worksheet from a topic, a difficulty, or a progressive ramp.",
};

function GeneratorFallback() {
  const entry = defaultGalleryEntry();
  return (
    <div className="worksheet-stage">
      <section className="panel preview worksheet-page" aria-busy="true">
        <header className="worksheet-header">
          <h2>{entry?.title ?? "Math Practice"}</h2>
          <p className="worksheet-meta">Name: ________________________________ Date: ____________</p>
        </header>
        <p className="worksheet-page-status">Opening the worksheet…</p>
      </section>
    </div>
  );
}

export default function GeneratePage() {
  return (
    <Suspense fallback={<GeneratorFallback />}>
      <WorksheetGenerator />
    </Suspense>
  );
}
