"use client";

type ExportPdfButtonProps = {
  disabled: boolean;
};

export function ExportPdfButton({ disabled }: ExportPdfButtonProps) {
  const handlePrint = () => {
    window.print();
  };

  return (
    <button className="primary" onClick={handlePrint} disabled={disabled}>
      Export PDF
    </button>
  );
}
