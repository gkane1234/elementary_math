import assert from "node:assert/strict";
import { describe, it } from "node:test";
import {
  listGalleryEntries,
  splitWorksheetChoices,
  worksheetsIncludingTopic,
} from "./worksheet-gallery";

describe("worksheetsIncludingTopic", () => {
  it("matches a catalog sheet by its seed", () => {
    const matches = worksheetsIncludingTopic("g6_introduction_to_ratios");
    assert.ok(matches.some((entry) => entry.id === "g6-ratios-level-1"));
  });

  it("includes a sheet whose plan places the topic on the page", () => {
    const matches = worksheetsIncludingTopic("g6_equivalent_ratios", {
      "g6-ratios-level-1": ["g6_introduction_to_ratios", "g6_equivalent_ratios"],
    });
    assert.deepEqual(
      matches.map((entry) => entry.id),
      ["g6-ratios-level-1"],
    );
  });

  it("returns nothing when no sheet uses the topic", () => {
    assert.deepEqual(worksheetsIncludingTopic("not_a_real_topic"), []);
  });
});

describe("splitWorksheetChoices", () => {
  it("keeps topic matches out of the general list", () => {
    const split = splitWorksheetChoices("calc_limits_by_direct_evaluation");
    assert.ok(split.includesTopic.some((entry) => entry.id === "calc-limits-level-2"));
    assert.ok(split.others.every((entry) => entry.id !== "calc-limits-level-2"));
    assert.equal(
      split.includesTopic.length + split.others.length,
      listGalleryEntries().length,
    );
  });

  it("lists every catalog sheet once", () => {
    const split = splitWorksheetChoices("");
    const ids = [...split.includesTopic, ...split.others].map((entry) => entry.id);
    assert.equal(new Set(ids).size, ids.length);
    assert.ok(ids.length >= 10);
    assert.deepEqual(split.includesTopic, []);
  });
});
