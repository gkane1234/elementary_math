export function distributeToColumns<T>(items: T[], columnCount: number): T[][] {
  const effectiveColumns = Math.max(1, Math.min(columnCount, items.length || 1));
  if (effectiveColumns <= 1 || items.length === 0) {
    return [items];
  }

  const columns: T[][] = Array.from({ length: effectiveColumns }, () => []);

  items.forEach((item, index) => {
    const columnIndex = index % effectiveColumns;
    columns[columnIndex].push(item);
  });

  return columns;
}

export function columnStartNumber(
  _columns: unknown[][],
  columnIndex: number,
): number {
  return columnIndex + 1;
}

export function resolveColumnCount(questionCount: number, setting: string | number): number {
  if (questionCount <= 1) return 1;

  if (typeof setting === "string" && setting.toLowerCase() === "auto") {
    if (questionCount <= 4) return 1;
    if (questionCount <= 10) return Math.min(2, questionCount);
    return Math.min(3, questionCount);
  }

  const requested = Math.max(1, Math.min(3, Number(setting)));
  return Math.min(requested, questionCount);
}

export function flattenColumnOrder<T>(columns: T[][]): T[] {
  if (columns.length <= 1) {
    return columns[0] ?? [];
  }

  const maxLength = Math.max(...columns.map((column) => column.length));
  const items: T[] = [];

  for (let row = 0; row < maxLength; row += 1) {
    for (let columnIndex = 0; columnIndex < columns.length; columnIndex += 1) {
      const item = columns[columnIndex][row];
      if (item !== undefined) {
        items.push(item);
      }
    }
  }

  return items;
}

export function insertAtIndex<T>(items: T[], fromIndex: number, toIndex: number): T[] {
  if (fromIndex === toIndex || fromIndex < 0 || toIndex < 0) return items;
  const next = [...items];
  const [moved] = next.splice(fromIndex, 1);
  const adjustedIndex = fromIndex < toIndex ? toIndex - 1 : toIndex;
  next.splice(adjustedIndex, 0, moved);
  return next;
}
