"use client";

type QuestionContextMenuProps = {
  x: number;
  y: number;
  onEditSettings: () => void;
  onRegenerate: () => void;
  onIncreaseSpace: () => void;
  onDecreaseSpace: () => void;
  onRemove: () => void;
  onClose: () => void;
};

export function QuestionContextMenu({
  x,
  y,
  onEditSettings,
  onRegenerate,
  onIncreaseSpace,
  onDecreaseSpace,
  onRemove,
  onClose,
}: QuestionContextMenuProps) {
  return (
    <>
      <button className="context-backdrop" type="button" aria-label="Close menu" onClick={onClose} />
      <menu className="context-menu" style={{ top: y, left: x }}>
        <button type="button" onClick={onEditSettings}>
          Edit settings...
        </button>
        <button type="button" onClick={onRegenerate}>
          Regenerate question
        </button>
        <button type="button" onClick={onIncreaseSpace}>
          Add more space
        </button>
        <button type="button" onClick={onDecreaseSpace}>
          Reduce space
        </button>
        <button type="button" className="danger" onClick={onRemove}>
          Remove question
        </button>
      </menu>
    </>
  );
}
