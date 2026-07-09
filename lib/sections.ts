import type { TopicSection } from "@/lib/types";
import { insertAtIndex } from "./columns";

export function moveSection(
  sections: TopicSection[],
  fromIndex: number,
  toIndex: number,
): TopicSection[] {
  return insertAtIndex(sections, fromIndex, toIndex);
}
