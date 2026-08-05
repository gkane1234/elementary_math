import type { Metadata } from "next";
import { WorksheetGallery } from "@/components/WorksheetGallery";

export const metadata: Metadata = {
  title: "Example worksheet gallery",
  description:
    "Browse progressive practice worksheets across courses with worksheet-level difficulty ramps.",
};

export default function GalleryPage() {
  return <WorksheetGallery />;
}
