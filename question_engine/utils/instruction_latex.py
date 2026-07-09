"""Helpers for worksheet instruction LaTeX headers."""

from __future__ import annotations

DEFAULT_INSTRUCTION_TEXT = "Solve."
DEFAULT_INSTRUCTION_LATEX = r"\text{Solve.}"


def wrap_instruction_text(text: str) -> str:
    return f"\\text{{{text}}}"


def repair_instruction_latex(latex: str | None) -> str | None:
    """Repair \\text{...} corrupted when \\t was read as a tab escape."""
    if latex is None:
        return None
    if not latex:
        return latex
    if latex.startswith("\t") and latex[1:4] == "ext":
        return r"\text" + latex[4:]
    if latex.startswith("ext{"):
        return "\\text{" + latex[4:]
    return latex


def resolve_instruction_latex(
    instruction_latex: str = "",
    instruction_text: str = "",
) -> str:
    if instruction_latex:
        return repair_instruction_latex(instruction_latex) or DEFAULT_INSTRUCTION_LATEX
    text = instruction_text or DEFAULT_INSTRUCTION_TEXT
    return wrap_instruction_text(text)


def resolve_instruction_text(instruction_text: str = "") -> str:
    return instruction_text or DEFAULT_INSTRUCTION_TEXT
