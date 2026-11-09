import type { Metadata } from "next";
import { Suspense } from "react";
import { WorksheetGenerator } from "@/components/WorksheetGenerator";

export const metadata: Metadata = {
  title: "Generator",
  description: "Build a printable math worksheet from a topic, a difficulty, or a progressive ramp.",
};

export default function GeneratePage() {
  return (
    <Suspense fallback={<p className="worksheet-status">Loading generator…</p>}>
      <WorksheetGenerator />
    </Suspense>
  );
}
