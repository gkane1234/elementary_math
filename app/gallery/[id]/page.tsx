import type { Metadata } from "next";
import { GalleryExampleViewer } from "@/components/GalleryExampleViewer";
import { listGalleryEntries } from "@/lib/worksheet-gallery";

type Props = { params: Promise<{ id: string }> };

export function generateStaticParams() {
  return listGalleryEntries().map((entry) => ({ id: entry.id }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { id } = await params;
  const entry = listGalleryEntries().find((e) => e.id === id);
  return {
    title: entry ? `${entry.title} · Gallery` : "Gallery example",
    description: entry?.description,
  };
}

export default async function GalleryExamplePage({ params }: Props) {
  const { id } = await params;
  return <GalleryExampleViewer entryId={id} />;
}
