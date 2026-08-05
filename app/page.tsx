import { Suspense } from "react";
import { WorksheetGenerator } from "@/components/WorksheetGenerator";

export default function HomePage() {
  return (
    <Suspense fallback={<p className="worksheet-status">Loading generator…</p>}>
      <WorksheetGenerator />
    </Suspense>
  );
}
