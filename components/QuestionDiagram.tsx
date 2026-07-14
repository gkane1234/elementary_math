import {
  extractDiagramMetadata,
  type QuestionDiagramMetadata,
} from "@/lib/diagram-metadata";

type QuestionDiagramProps = {
  metadata: QuestionDiagramMetadata;
};

/** Renders server-emitted SVG from the geometry diagram DSL. */
export function QuestionDiagram({ metadata }: QuestionDiagramProps) {
  const svg = metadata.diagram_svg;
  if (!svg) return null;

  return (
    <div
      className="question-diagram"
      role="img"
      aria-label="Geometry diagram"
      dangerouslySetInnerHTML={{ __html: svg }}
    />
  );
}

export function QuestionDiagramFromMetadata({
  metadata,
  variant = "prompt",
}: {
  metadata?: Record<string, unknown>;
  /** prompt: blank/stimulus under the question; answer: solution diagram on answer key */
  variant?: "prompt" | "answer";
}) {
  const diagram = extractDiagramMetadata(metadata, variant);
  if (!diagram?.diagram_svg) return null;
  return <QuestionDiagram metadata={diagram} />;
}
