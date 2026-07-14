from dataclasses import dataclass
from typing import Literal

from ..utils.instruction_latex import resolve_instruction_latex, resolve_instruction_text

CatalogIntent = Literal["ready", "shared_family", "scaffold"]


def derive_catalog_intent(type_id: str, generator: str) -> CatalogIntent:
    """Classify how a catalog entry relates to its producer family."""
    if generator == "scaffold":
        return "scaffold"
    if generator != type_id:
        return "shared_family"
    return "ready"


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

    @property
    def intent(self) -> CatalogIntent:
        return derive_catalog_intent(self.id, self.generator)


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
