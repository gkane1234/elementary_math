import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { worksheetsIncludingTopic } from "./worksheet-gallery";

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
