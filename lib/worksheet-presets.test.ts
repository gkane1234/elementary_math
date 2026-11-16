import assert from "node:assert/strict";
import { describe, it } from "node:test";
import {
  presetsIncludingTopic,
  removePreset,
  topicsOnWorksheet,
  upsertPreset,
  type SavedWorksheetPreset,
} from "./worksheet-presets";
import type { WorksheetDraft } from "./types";

function draft(topics: string[]): WorksheetDraft {
  return {
    title: "Practice",
    columns: 1,
    questions: topics.map((topic, index) => ({
      id: `q${index}`,
      topic,
      prompt_latex: "x",
      prompt_text: "x",
      spacing: 1,
      generation_settings: {},
    })),
  };
}

function preset(id: string, topics: string[]): SavedWorksheetPreset {
  return {
    id,
    title: id,
    savedAt: "2026-11-16T00:00:00.000Z",
    worksheet: draft(topics),
    sections: [],
    topics,
  };
}

describe("topicsOnWorksheet", () => {
  it("collects section topics and question topics once", () => {
    assert.deepEqual(
      topicsOnWorksheet(draft(["ratios", "ratios"]), [
        { id: "s1", type_id: "intro", count: 1, settings: {} },
        { id: "s2", type_id: "ratios", count: 1, settings: {} },
      ]),
      ["intro", "ratios"],
    );
  });
});

describe("presetsIncludingTopic", () => {
  const presets = [preset("a", ["ratios"]), preset("b", ["limits"])];

  it("returns saved sheets that include the topic", () => {
    assert.deepEqual(
      presetsIncludingTopic(presets, "ratios").map((entry) => entry.id),
      ["a"],
    );
  });

  it("returns nothing for a blank topic", () => {
    assert.deepEqual(presetsIncludingTopic(presets, " "), []);
  });
});

describe("upsertPreset", () => {
  it("inserts a new preset at the front and replaces an existing id", () => {
    const first = preset("a", ["ratios"]);
    const inserted = upsertPreset([], first);
    assert.equal(inserted[0]?.id, "a");
    const updated = preset("a", ["limits"]);
    assert.deepEqual(upsertPreset(inserted, updated)[0]?.topics, ["limits"]);
    assert.equal(upsertPreset(inserted, updated).length, 1);
  });

  it("removes a preset by id", () => {
    assert.deepEqual(removePreset([preset("a", ["ratios"]), preset("b", ["limits"])], "a").map((entry) => entry.id), [
      "b",
    ]);
  });
});
