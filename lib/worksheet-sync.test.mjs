/**
 * Lightweight Node tests for worksheet sync planning (mirrors lib/worksheet-sync.ts).
 * Run: node --test lib/worksheet-sync.test.mjs
 */
import { describe, it } from "node:test";
import assert from "node:assert/strict";

function settingsEqual(left, right) {
  return JSON.stringify(left) === JSON.stringify(right);
}

function sectionRequiresRegenerate(section, previous) {
  if (!previous) return false;
  return (
    previous.type_id !== section.type_id ||
    !settingsEqual(previous.settings, section.settings)
  );
}

function planSectionSync(section, existing, forceRegenerate = false) {
  const kept = existing.filter((question) => question.topic === section.type_id);

  if (forceRegenerate || kept.length === 0) {
    return { kind: "regenerate", generateCount: section.count };
  }

  if (kept.length === section.count) {
    return { kind: "keep", questions: kept };
  }

  if (kept.length < section.count) {
    return {
      kind: "append",
      questions: kept,
      generateCount: section.count - kept.length,
    };
  }

  return { kind: "trim", questions: kept.slice(0, section.count) };
}

function q(id, topic = "algebra") {
  return { id, topic, prompt_latex: id };
}

describe("sectionRequiresRegenerate", () => {
  it("does not regenerate when only count changes", () => {
    const prev = { id: "s1", type_id: "algebra", count: 5, settings: { difficulty: 0.4 } };
    const next = { ...prev, count: 8 };
    assert.equal(sectionRequiresRegenerate(next, prev), false);
  });

  it("regenerates when settings change", () => {
    const prev = { id: "s1", type_id: "algebra", count: 5, settings: { difficulty: 0.4 } };
    const next = { ...prev, settings: { difficulty: 0.8 } };
    assert.equal(sectionRequiresRegenerate(next, prev), true);
  });
});

describe("planSectionSync", () => {
  const section = { id: "s1", type_id: "algebra", count: 5, settings: {} };

  it("keeps existing questions when count is unchanged", () => {
    const existing = [q("a"), q("b"), q("c"), q("d"), q("e")];
    const plan = planSectionSync(section, existing);
    assert.equal(plan.kind, "keep");
    assert.deepEqual(
      plan.questions.map((item) => item.id),
      ["a", "b", "c", "d", "e"],
    );
  });

  it("appends only the delta when count increases", () => {
    const existing = [q("a"), q("b"), q("c"), q("d"), q("e")];
    const plan = planSectionSync({ ...section, count: 8 }, existing);
    assert.equal(plan.kind, "append");
    assert.equal(plan.generateCount, 3);
    assert.deepEqual(
      plan.questions.map((item) => item.id),
      ["a", "b", "c", "d", "e"],
    );
  });

  it("trims from the end when count decreases", () => {
    const existing = [q("a"), q("b"), q("c"), q("d"), q("e")];
    const plan = planSectionSync({ ...section, count: 3 }, existing);
    assert.equal(plan.kind, "trim");
    assert.deepEqual(
      plan.questions.map((item) => item.id),
      ["a", "b", "c"],
    );
  });

  it("regenerates when forceRegenerate is true", () => {
    const existing = [q("a"), q("b"), q("c"), q("d"), q("e")];
    const plan = planSectionSync(section, existing, true);
    assert.equal(plan.kind, "regenerate");
    assert.equal(plan.generateCount, 5);
  });
});
