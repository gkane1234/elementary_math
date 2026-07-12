"use client";

import { useEffect, useId, useRef } from "react";
import katex from "katex";
import { enableKatexSoftWrap } from "@/lib/latex";
import {
  choiceLetter,
  type MultipleChoiceOption,
} from "@/lib/multiple-choice";

type MultipleChoiceOptionsProps = {
  choices: MultipleChoiceOption[];
  questionId: string;
  /** Interactive radios vs print-only lettered list. */
  interactive?: boolean;
};

function ChoiceLatex({ content }: { content: string }) {
  const ref = useRef<HTMLSpanElement>(null);

  useEffect(() => {
    if (!ref.current) return;
    katex.render(content, ref.current, {
      throwOnError: false,
      displayMode: false,
    });
    enableKatexSoftWrap(ref.current);
  }, [content]);

  return <span ref={ref} />;
}

export function MultipleChoiceOptions({
  choices,
  questionId,
  interactive = false,
}: MultipleChoiceOptionsProps) {
  const groupId = useId();

  if (choices.length === 0) return null;

  if (interactive) {
    return (
      <fieldset
        className="mc-choices mc-choices-interactive"
        name={`${groupId}-${questionId}`}
        onClick={(event) => event.stopPropagation()}
        onMouseDown={(event) => event.stopPropagation()}
      >
        <legend className="sr-only">Answer choices</legend>
        {choices.map((choice, index) => {
          const letter = choiceLetter(choice, index);
          const inputId = `${groupId}-${questionId}-${choice.id}`;
          return (
            <label className="mc-choice" key={choice.id} htmlFor={inputId}>
              <input
                id={inputId}
                type="radio"
                name={`${groupId}-${questionId}`}
                value={choice.id}
              />
              <span className="mc-choice-letter">{letter}.</span>
              <span className="mc-choice-latex">
                <ChoiceLatex content={choice.latex} />
              </span>
            </label>
          );
        })}
      </fieldset>
    );
  }

  return (
    <ul className="mc-choices mc-choices-print">
      {choices.map((choice, index) => {
        const letter = choiceLetter(choice, index);
        return (
          <li className="mc-choice" key={choice.id}>
            <span className="mc-choice-letter">{letter}.</span>
            <span className="mc-choice-latex">
              <ChoiceLatex content={choice.latex} />
            </span>
          </li>
        );
      })}
    </ul>
  );
}
