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
}: {
  metadata?: Record<string, unknown>;
}) {
  const diagram = extractDiagramMetadata(metadata);
  if (!diagram?.diagram_svg) return null;
  return <QuestionDiagram metadata={diagram} />;
}
