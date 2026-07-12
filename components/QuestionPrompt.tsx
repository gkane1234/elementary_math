"use client";

import { useEffect, useRef } from "react";
import katex from "katex";
import { enableKatexSoftWrap, repairInstructionLatex } from "@/lib/latex";

export function InlineLatex({ content, repair = false }: { content: string; repair?: boolean }) {
  const ref = useRef<HTMLSpanElement>(null);

  useEffect(() => {
    if (!ref.current) return;
    katex.render(repair ? repairInstructionLatex(content) : content, ref.current, {
      throwOnError: false,
      displayMode: false,
    });
    enableKatexSoftWrap(ref.current);
  }, [content, repair]);

  return <span ref={ref} />;
}

type QuestionPromptProps = {
  content: string;
};

/** Renders prompt LaTeX with no continuation/wrap dashes. */
export function QuestionPrompt({ content }: QuestionPromptProps) {
  return (
    <span className="question-prompt">
      <InlineLatex content={content} />
    </span>
  );
}

export function InstructionLatex({ content }: { content: string }) {
  return <InlineLatex content={content} repair />;
}
