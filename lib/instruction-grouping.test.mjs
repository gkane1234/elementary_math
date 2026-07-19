/**
 * Mirrors lib/worksheet.ts groupQuestionsByInstruction for a lightweight Node test.
 * Run: node --test lib/instruction-grouping.test.mjs
 */
import { describe, it } from "node:test";
import assert from "node:assert/strict";

function groupQuestionsByInstruction(questions) {
  if (questions.length === 0) return [];
  const groups = [];
  let current = null;
  questions.forEach((question, index) => {
    const instruction = question.instruction_latex ?? null;
    if (!current || current.instruction !== instruction) {
      current = { instruction, questions: [question], startIndex: index };
      groups.push(current);
      return;
    }
    current.questions.push(question);
  });
  return groups;
}

describe("groupQuestionsByInstruction", () => {
  it("factors A A B A into three consecutive groups", () => {
    const questions = [
      { id: "1", instruction_latex: "A" },
      { id: "2", instruction_latex: "A" },
      { id: "3", instruction_latex: "B" },
      { id: "4", instruction_latex: "A" },
    ];
    const groups = groupQuestionsByInstruction(questions);
    assert.equal(groups.length, 3);
    assert.equal(groups[0].instruction, "A");
    assert.deepEqual(
      groups[0].questions.map((q) => q.id),
      ["1", "2"],
    );
    assert.equal(groups[1].instruction, "B");
    assert.deepEqual(
      groups[1].questions.map((q) => q.id),
      ["3"],
    );
    assert.equal(groups[2].instruction, "A");
    assert.deepEqual(
      groups[2].questions.map((q) => q.id),
      ["4"],
    );
  });
});
