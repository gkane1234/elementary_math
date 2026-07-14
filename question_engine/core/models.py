from dataclasses import asdict, dataclass, field
from typing import Any, Literal

from packages.polynomial_core import normalize_expression_signs


@dataclass
class Question:
    id: str
    topic: str
    prompt_latex: str
    prompt_text: str
    answer_latex: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        # Global cleanup: never emit `5+-2` or `2/-1` in prompts/answers.
        self.prompt_latex = normalize_expression_signs(self.prompt_latex)
        self.prompt_text = normalize_expression_signs(self.prompt_text)
        if self.answer_latex is not None:
            self.answer_latex = normalize_expression_signs(self.answer_latex)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class QuestionSet:
    title: str
    questions: list[Question]
    settings_snapshot: dict[str, Any] = field(default_factory=dict)
    instruction_latex: str | None = None
    instruction_text: str | None = None
    columns: int = 1

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "questions": [q.to_dict() for q in self.questions],
            "settings_snapshot": self.settings_snapshot,
            "instruction_latex": self.instruction_latex,
            "instruction_text": self.instruction_text,
            "columns": self.columns,
        }


@dataclass
class SettingField:
    key: str
    label: str
    type: Literal["int", "range", "select", "bool"]
    default: Any
    min: int | None = None
    max: int | None = None
    options: list[str] | None = None
    group: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        return {k: v for k, v in data.items() if v is not None}
