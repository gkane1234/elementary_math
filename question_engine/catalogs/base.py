from dataclasses import dataclass

from ..utils.instruction_latex import resolve_instruction_latex, resolve_instruction_text


@dataclass(frozen=True)
class TypeCatalogEntry:
    id: str
    name: str
    category: str
    subcategory: str | None = None
    description: str = ""
    instruction_latex: str = ""
    instruction_text: str = ""
    generator: str = "scaffold"
    count_default: int = 10


def entry(
    id: str,
    name: str,
    category: str,
    *,
    subcategory: str | None = None,
    generator: str = "scaffold",
    description: str = "",
    instruction_latex: str = "",
    instruction_text: str = "",
    count_default: int = 10,
) -> TypeCatalogEntry:
    return TypeCatalogEntry(
        id=id,
        name=name,
        category=category,
        subcategory=subcategory,
        generator=generator,
        description=description or f"Practice {name.lower()}.",
        instruction_latex=resolve_instruction_latex(instruction_latex, instruction_text),
        instruction_text=resolve_instruction_text(instruction_text),
        count_default=count_default,
    )
