"""Word-problem template framework — narrative prompts with numeric slots."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Any, Callable

from .base import QuestionFramework
from ..generators.utils import random_int_range

SlotSampler = Callable[[dict], tuple[str, str | None]]

_NAMES = ("Alex", "Jordan", "Sam", "Taylor", "Morgan", "Casey", "Riley", "Jamie")
_LETTERS = ("A", "B", "C", "D")


@dataclass
class WordProblemTemplate:
    """Declarative word-problem shell with injectable numeric slots."""

    template_latex: str
    template_text: str
    variable_slots: dict[str, SlotSampler] = field(default_factory=dict)
    answer_slot: str | None = None

    def render(self, settings: dict) -> tuple[str, str, str | None]:
        values: dict[str, str] = {}
        answer: str | None = None
        for name, sampler in self.variable_slots.items():
            display, slot_answer = sampler(settings)
            values[name] = display
            if self.answer_slot == name and slot_answer is not None:
                answer = slot_answer
        latex = self.template_latex.format(**values)
        text = self.template_text.format(**values)
        return latex, text, answer


def _difficulty_range(settings: dict) -> tuple[int, int]:
    difficulty = str(settings.get("difficulty", "medium"))
    if difficulty == "easy":
        return 2, 12
    if difficulty == "hard":
        return 10, 50
    return 5, 25


def _pick_name(settings: dict, *, index: int = 0) -> str:
    style = str(settings.get("name_style", "names"))
    if style == "letters":
        return _LETTERS[index % len(_LETTERS)]
    if style == "person_a_b":
        return "Person A" if index == 0 else "Person B"
    return random.choice(_NAMES)


def _format_answer(value: float | int, settings: dict) -> str:
    if bool(settings.get("integer_only_answers", True)):
        value = int(round(value))
        return str(value)
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.1f}".rstrip("0").rstrip(".")


def _append_units(answer: str, settings: dict) -> str:
    units = str(settings.get("answer_units", ""))
    if not units:
        return answer
    if units == "dollars":
        return f"\\${answer}" if answer.startswith("\\") else f"${answer}"
    return f"{answer} {units}"


def _unit_label(settings: dict, default: str) -> str:
    if not bool(settings.get("show_unit_labels", True)):
        return ""
    units = str(settings.get("answer_units", ""))
    return units or default


def _random_value(settings: dict, *, lo: int | None = None, hi: int | None = None) -> int:
    default_lo, default_hi = _difficulty_range(settings)
    minimum = lo if lo is not None else default_lo
    maximum = hi if hi is not None else default_hi
    return random_int_range(minimum, maximum)


class WordProblemFramework(QuestionFramework):
    """Batch generation wrapper around a word-problem template or subclass."""

    problem_kind: str = "generic"

    def __init__(self, template: WordProblemTemplate | None = None):
        self.template = template

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {
            "difficulty": settings.get("difficulty", "medium"),
            "answer_units": settings.get("answer_units", ""),
            "problem_kind": self.problem_kind,
            "max_steps": int(settings.get("max_steps", 2)),
        }

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        if self.template is None:
            raise NotImplementedError(
                f"{self.__class__.__name__} requires build_prompt or a WordProblemTemplate."
            )
        latex, text, answer = self.template.render(settings)
        if answer is not None:
            answer = _append_units(answer, settings)
        return latex, text, answer


class DistanceRateTimeFramework(WordProblemFramework):
    problem_kind = "distance_rate_time"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        name = _pick_name(settings)
        unit = _unit_label(settings, "mi")
        time_unit = "hr" if unit in ("mi", "km", "") else "min"
        variant = random.choice(["find_time", "find_distance", "find_rate"])

        if variant == "find_time":
            rate = _random_value(settings, lo=4, hi=20)
            time = _random_value(settings, lo=2, hi=8)
            distance = rate * time
            answer = _format_answer(time, settings)
            latex = (
                rf"\text{{{name} travels {distance} {unit} at {rate} {unit}/{time_unit}. "
                rf"How many {time_unit} does the trip take?}}"
            )
            text = (
                f"{name} travels {distance} {unit} at {rate} {unit}/{time_unit}. "
                f"How many {time_unit} does the trip take?"
            )
        elif variant == "find_distance":
            rate = _random_value(settings, lo=5, hi=25)
            time = _random_value(settings, lo=2, hi=6)
            distance = rate * time
            answer = _format_answer(distance, settings)
            latex = (
                rf"\text{{{name} drives at {rate} {unit}/{time_unit} for {time} {time_unit}. "
                rf"How many {unit} does {name} travel?}}"
            )
            text = (
                f"{name} drives at {rate} {unit}/{time_unit} for {time} {time_unit}. "
                f"How many {unit} does {name} travel?"
            )
        else:
            distance = _random_value(settings, lo=20, hi=120)
            divisors = [d for d in range(2, 13) if distance % d == 0]
            time = random.choice(divisors) if divisors else max(2, distance // 10)
            rate = distance // time
            answer = _format_answer(rate, settings)
            latex = (
                rf"\text{{{name} travels {distance} {unit} in {time} {time_unit}. "
                rf"What is the average speed in {unit}/{time_unit}?}}"
            )
            text = (
                f"{name} travels {distance} {unit} in {time} {time_unit}. "
                f"What is the average speed in {unit}/{time_unit}?"
            )

        return latex, text, _append_units(answer, settings)


class WorkProblemFramework(WordProblemFramework):
    problem_kind = "work"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        a_name = _pick_name(settings, index=0)
        b_name = _pick_name(settings, index=1)
        integer_only = bool(settings.get("integer_only_answers", True))

        for _ in range(40):
            a_time = _random_value(settings, lo=2, hi=12)
            b_time = _random_value(settings, lo=2, hi=12)
            if a_time == b_time:
                continue
            together = (a_time * b_time) / (a_time + b_time)
            if integer_only and abs(together - round(together)) > 1e-9:
                continue
            answer = _format_answer(together, settings)
            time_unit = _unit_label(settings, "hr") or "hr"
            latex = (
                rf"\text{{{a_name} can finish a job in {a_time} {time_unit} and {b_name} "
                rf"can finish the same job in {b_time} {time_unit}. Working together, "
                rf"how many {time_unit} will it take them to finish the job?}}"
            )
            text = (
                f"{a_name} can finish a job in {a_time} {time_unit} and {b_name} "
                f"can finish the same job in {b_time} {time_unit}. Working together, "
                f"how many {time_unit} will it take them to finish the job?"
            )
            return latex, text, _append_units(answer, settings)

        a_time, b_time = 3, 6
        answer = _format_answer(2, settings)
        time_unit = _unit_label(settings, "hr") or "hr"
        latex = (
            rf"\text{{{a_name} can finish a job in {a_time} {time_unit} and {b_name} "
            rf"can finish the same job in {b_time} {time_unit}. Working together, "
            rf"how many {time_unit} will it take them to finish the job?}}"
        )
        text = (
            f"{a_name} can finish a job in {a_time} {time_unit} and {b_name} "
            f"can finish the same job in {b_time} {time_unit}. Working together, "
            f"how many {time_unit} will it take them to finish the job?"
        )
        return latex, text, _append_units(answer, settings)


class AgeProblemFramework(WordProblemFramework):
    problem_kind = "age"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        older = _pick_name(settings, index=0)
        younger = _pick_name(settings, index=1)
        diff = _random_value(settings, lo=2, hi=8)
        younger_age = _random_value(settings, lo=8, hi=20)
        older_age = younger_age + diff
        total = younger_age + older_age
        answer = _format_answer(younger_age, settings)
        year_unit = _unit_label(settings, "years") or "years"
        latex = (
            rf"\text{{{older} is {diff} {year_unit} older than {younger}. "
            rf"The sum of their ages is {total} {year_unit}. How old is {younger}?}}"
        )
        text = (
            f"{older} is {diff} {year_unit} older than {younger}. "
            f"The sum of their ages is {total} {year_unit}. How old is {younger}?"
        )
        return latex, text, _append_units(answer, settings)


class ConsecutiveIntegersFramework(WordProblemFramework):
    problem_kind = "consecutive_integers"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        count = min(int(settings.get("max_steps", 2)) + 1, 4)
        middle = _random_value(settings, lo=5, hi=25)
        start = middle - (count // 2)
        values = list(range(start, start + count))
        total = sum(values)
        answer = _format_answer(start, settings)
        if count == 2:
            phrase = "two consecutive integers"
        elif count == 3:
            phrase = "three consecutive integers"
        else:
            phrase = f"{count} consecutive integers"
        latex = rf"\text{{The sum of {phrase} is {total}. Find the smallest integer.}}"
        text = f"The sum of {phrase} is {total}. Find the smallest integer."
        return latex, text, answer


class CoinProblemFramework(WordProblemFramework):
    problem_kind = "coin"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        total_coins = _random_value(settings, lo=12, hi=30)
        quarters = _random_value(settings, lo=4, hi=total_coins - 4)
        nickels = total_coins - quarters
        total_cents = quarters * 25 + nickels * 5
        answer = _format_answer(quarters, settings)
        dollars = total_cents / 100
        dollar_text = f"\\${dollars:.2f}" if dollars == int(dollars) else f"\\${dollars:.2f}"
        latex = (
            rf"\text{{A jar contains {total_coins} coins, all quarters and nickels, "
            rf"worth {dollar_text} in total. How many quarters are in the jar?}}"
        )
        text = (
            f"A jar contains {total_coins} coins, all quarters and nickels, "
            f"worth ${dollars:.2f} in total. How many quarters are in the jar?"
        )
        return latex, text, _append_units(answer, settings)


class MixtureProblemFramework(WordProblemFramework):
    problem_kind = "mixture"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        total = _random_value(settings, lo=8, hi=20)
        low_pct = random.choice([10, 15, 20, 25])
        high_pct = low_pct + random.choice([20, 25, 30])
        target_pct = low_pct + random.choice([5, 10, 15])
        while target_pct >= high_pct:
            target_pct = low_pct + 5
        high_amount = total * (target_pct - low_pct) // (high_pct - low_pct)
        answer = _format_answer(high_amount, settings)
        unit = _unit_label(settings, "L") or "L"
        latex = (
            rf"\text{{How many {unit} of a {high_pct}\% solution must be added to "
            rf"{total - high_amount} {unit} of a {low_pct}\% solution to obtain "
            rf"{total} {unit} of a {target_pct}\% solution?}}"
        )
        text = (
            f"How many {unit} of a {high_pct}% solution must be added to "
            f"{total - high_amount} {unit} of a {low_pct}% solution to obtain "
            f"{total} {unit} of a {target_pct}% solution?"
        )
        return latex, text, _append_units(answer, settings)


class PerimeterAreaFramework(WordProblemFramework):
    problem_kind = "perimeter_area"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        unit = _unit_label(settings, "ft") or "ft"
        variant = random.choice(["perimeter", "area"])

        if variant == "perimeter":
            width = _random_value(settings, lo=4, hi=15)
            diff = _random_value(settings, lo=2, hi=6)
            length = width + diff
            perimeter = 2 * (length + width)
            answer = _format_answer(width, settings)
            latex = (
                rf"\text{{A rectangle has length {diff} {unit} more than its width. "
                rf"If the perimeter is {perimeter} {unit}, what is the width in {unit}?}}"
            )
            text = (
                f"A rectangle has length {diff} {unit} more than its width. "
                f"If the perimeter is {perimeter} {unit}, what is the width in {unit}?"
            )
        else:
            width = _random_value(settings, lo=3, hi=10)
            diff = _random_value(settings, lo=2, hi=5)
            length = width + diff
            area = length * width
            answer = _format_answer(length, settings)
            latex = (
                rf"\text{{A rectangle has width {width} {unit} and area {area} {unit}^2. "
                rf"What is the length in {unit}?}}"
            )
            text = (
                f"A rectangle has width {width} {unit} and area {area} {unit}^2. "
                f"What is the length in {unit}?"
            )

        return latex, text, _append_units(answer, settings)


class PercentWordProblemFramework(WordProblemFramework):
    problem_kind = "percent"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        name = _pick_name(settings)
        variant = random.choice(["discount", "tax", "markup", "interest"])
        price = _random_value(settings, lo=20, hi=200)
        rate = random.choice([5, 8, 10, 12, 15, 20, 25])

        if variant == "discount":
            sale = price * (100 - rate) // 100
            answer = _format_answer(sale, settings)
            latex = (
                rf"\text{{{name} buys an item priced at \${price}. "
                rf"It is on sale for {rate}\% off. What is the sale price?}}"
            )
            text = (
                f"{name} buys an item priced at ${price}. "
                f"It is on sale for {rate}% off. What is the sale price?"
            )
        elif variant == "tax":
            total = price * (100 + rate) // 100
            answer = _format_answer(total, settings)
            latex = (
                rf"\text{{A \${price} purchase has {rate}\% sales tax added. "
                rf"What is the total cost?}}"
            )
            text = f"A ${price} purchase has {rate}% sales tax added. What is the total cost?"
        elif variant == "markup":
            new_price = price * (100 + rate) // 100
            answer = _format_answer(new_price, settings)
            latex = (
                rf"\text{{A store marks up a \${price} item by {rate}\%. "
                rf"What is the selling price?}}"
            )
            text = f"A store marks up a ${price} item by {rate}%. What is the selling price?"
        else:
            interest = price * rate // 100
            answer = _format_answer(interest, settings)
            latex = (
                rf"\text{{{name} invests \${price} at {rate}\% simple interest for one year. "
                rf"How much interest is earned?}}"
            )
            text = (
                f"{name} invests ${price} at {rate}% simple interest for one year. "
                f"How much interest is earned?"
            )

        return latex, text, f"\\${answer}" if not str(settings.get("answer_units", "")) else _append_units(answer, settings)


class ProportionWordProblemFramework(WordProblemFramework):
    problem_kind = "proportion"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        unit_count = _random_value(settings, lo=2, hi=6)
        unit_price_cents = random.choice([50, 75, 100, 125, 150, 200])
        target_count = unit_count + _random_value(settings, lo=2, hi=6)
        cost_cents = unit_price_cents * target_count // unit_count
        answer = _format_answer(cost_cents / 100, settings)
        items = random.choice(["apples", "notebooks", "markers", "bottles of water"])
        latex = (
            rf"\text{{If {unit_count} {items} cost \${unit_price_cents / 100:.2f}, "
            rf"how much do {target_count} {items} cost at the same rate?}}"
        )
        text = (
            f"If {unit_count} {items} cost ${unit_price_cents / 100:.2f}, "
            f"how much do {target_count} {items} cost at the same rate?"
        )
        return latex, text, f"\\${answer}"


class OneStepEquationWordFramework(WordProblemFramework):
    problem_kind = "one_step_equation"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        name = _pick_name(settings)
        op = random.choice(["subtract", "add", "multiply", "divide"])
        result = _random_value(settings, lo=10, hi=60)

        if op == "subtract":
            spent = _random_value(settings, lo=5, hi=20)
            start = result + spent
            answer = _format_answer(start, settings)
            latex = (
                rf"\text{{{name} had some money, spent \${spent}, and has \${result} left. "
                rf"How much did {name} start with?}}"
            )
            text = (
                f"{name} had some money, spent ${spent}, and has ${result} left. "
                f"How much did {name} start with?"
            )
        elif op == "add":
            received = _random_value(settings, lo=5, hi=20)
            start = result - received
            answer = _format_answer(start, settings)
            latex = (
                rf"\text{{{name} had some money, received \${received}, and now has \${result}. "
                rf"How much did {name} start with?}}"
            )
            text = (
                f"{name} had some money, received ${received}, and now has ${result}. "
                f"How much did {name} start with?"
            )
        elif op == "multiply":
            factor = random.choice([2, 3, 4, 5])
            start = result // factor
            answer = _format_answer(start, settings)
            latex = (
                rf"\text{{{name} collected {factor} equal donations totaling \${result}. "
                rf"How much was each donation?}}"
            )
            text = (
                f"{name} collected {factor} equal donations totaling ${result}. "
                f"How much was each donation?"
            )
        else:
            factor = random.choice([2, 3, 4, 5])
            start = result * factor
            answer = _format_answer(start, settings)
            latex = (
                rf"\text{{{name} shared \${start} equally among {factor} friends. "
                rf"How much did each friend receive?}}"
            )
            text = (
                f"{name} shared ${start} equally among {factor} friends. "
                f"How much did each friend receive?"
            )

        return latex, text, f"\\${answer}"


class TwoStepEquationWordFramework(WordProblemFramework):
    problem_kind = "two_step_equation"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        for _ in range(40):
            coeff = random.choice([2, 3, 4, 5])
            constant = _random_value(settings, lo=3, hi=15)
            number = _random_value(settings, lo=4, hi=20)
            result = coeff * number - constant
            if result <= 0:
                continue
            answer = _format_answer(number, settings)
            latex = (
                rf"\text{{{constant} less than {coeff} times a number is {result}. "
                rf"Find the number.}}"
            )
            text = f"{constant} less than {coeff} times a number is {result}. Find the number."
            return latex, text, answer

        number = 5
        answer = _format_answer(number, settings)
        latex = r"\text{7 less than 3 times a number is 8. Find the number.}"
        text = "7 less than 3 times a number is 8. Find the number."
        return latex, text, answer


class SystemsWordProblemFramework(WordProblemFramework):
    problem_kind = "systems"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        adult_price = random.choice([10, 12, 15])
        child_price = adult_price - random.choice([2, 4])
        child_count = _random_value(settings, lo=20, hi=60)
        adult_count = _random_value(settings, lo=20, hi=60)
        total_tickets = adult_count + child_count
        total_revenue = adult_count * adult_price + child_count * child_price
        answer = _format_answer(adult_count, settings)
        latex = (
            rf"\text{{Adult tickets cost \${adult_price} and child tickets cost \${child_price}. "
            rf"{total_tickets} tickets were sold for a total of \${total_revenue}. "
            rf"How many adult tickets were sold?}}"
        )
        text = (
            f"Adult tickets cost ${adult_price} and child tickets cost ${child_price}. "
            f"{total_tickets} tickets were sold for a total of ${total_revenue}. "
            f"How many adult tickets were sold?"
        )
        return latex, text, answer


class InequalityWordProblemFramework(WordProblemFramework):
    problem_kind = "inequality"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        name = _pick_name(settings)
        tests_taken = random.choice([3, 4, 5])
        current_total = _random_value(settings, lo=60, hi=90) * tests_taken // 3
        goal = current_total + _random_value(settings, lo=15, hi=40)
        needed = math.ceil((goal - current_total))
        answer = _format_answer(needed, settings)
        latex = (
            rf"\text{{{name} has scored a total of {current_total} points on {tests_taken} tests "
            rf"and wants at least {goal} points after one more test. "
            rf"What is the minimum score needed on the next test?}}"
        )
        text = (
            f"{name} has scored a total of {current_total} points on {tests_taken} tests "
            f"and wants at least {goal} points after one more test. "
            f"What is the minimum score needed on the next test?"
        )
        return latex, text, answer


class GcfLcmWordFramework(WordProblemFramework):
    problem_kind = "gcf_lcm"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        variant = random.choice(["lcm", "gcf"])
        require_gt_one = bool(settings.get("require_gcf_greater_than_one", True))
        if variant == "lcm":
            a = random.choice([6, 8, 9, 10, 12])
            b = random.choice([8, 10, 12, 15, 18])
            value = math.lcm(a, b)
            answer = _format_answer(value, settings)
            latex = (
                rf"\text{{Hot dogs come in packs of {a} and buns come in packs of {b}. "
                rf"What is the least number of each needed so there are no leftovers?}}"
            )
            text = (
                f"Hot dogs come in packs of {a} and buns come in packs of {b}. "
                f"What is the least number of each needed so there are no leftovers?"
            )
        else:
            g_lo = 2 if require_gt_one else 1
            g = random.randint(g_lo, 6)
            multipliers = [2, 3, 4, 5, 6, 7, 8, 9]
            m1 = random.choice(multipliers)
            m2 = random.choice([m for m in multipliers if m != m1 and math.gcd(m1, m) == 1])
            roses, tulips = m1 * g, m2 * g
            answer = _format_answer(g, settings)
            latex = (
                rf"\text{{A florist has {roses} roses and {tulips} tulips to make identical "
                rf"arrangements. What is the greatest number of arrangements that can be made?}}"
            )
            text = (
                f"A florist has {roses} roses and {tulips} tulips to make identical "
                f"arrangements. What is the greatest number of arrangements that can be made?"
            )
        return latex, text, answer


class NumberLineWordFramework(WordProblemFramework):
    problem_kind = "number_line"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        start = _random_value(settings, lo=-15, hi=10)
        change = _random_value(settings, lo=3, hi=20)
        if random.choice([True, False]):
            end = start + change
            latex = (
                rf"\text{{The temperature was {start}\textdegree{{}}F and rose {change}\textdegree{{}}F. "
                rf"What is the new temperature?}}"
            )
            text = f"The temperature was {start}°F and rose {change}°F. What is the new temperature?"
        else:
            end = start - change
            latex = (
                rf"\text{{The temperature was {start}\textdegree{{}}F and dropped {change}\textdegree{{}}F. "
                rf"What is the new temperature?}}"
            )
            text = f"The temperature was {start}°F and dropped {change}°F. What is the new temperature?"
        answer = _format_answer(end, settings)
        return latex, text, answer


class CoordinateDistanceWordFramework(WordProblemFramework):
    problem_kind = "coordinate_distance"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        x1 = _random_value(settings, lo=-5, hi=5)
        y1 = _random_value(settings, lo=-5, hi=5)
        dx = _random_value(settings, lo=3, hi=8)
        dy = _random_value(settings, lo=3, hi=8)
        x2, y2 = x1 + dx, y1 + dy
        distance = math.sqrt(dx * dx + dy * dy)
        answer = _format_answer(distance, settings)
        unit = _unit_label(settings, "units") or "units"
        latex = (
            rf"\text{{Point A is at ({x1}, {y1}) and point B is at ({x2}, {y2}) on a coordinate plane. "
            rf"How far apart are the points in {unit}?}}"
        )
        text = (
            f"Point A is at ({x1}, {y1}) and point B is at ({x2}, {y2}) on a coordinate plane. "
            f"How far apart are the points in {unit}?"
        )
        return latex, text, _append_units(answer, settings)


class SimilarFiguresWordFramework(WordProblemFramework):
    problem_kind = "similar_figures"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        ratio = random.choice([2, 3, 4])
        small_side = _random_value(settings, lo=3, hi=10)
        large_side = small_side * ratio
        answer = _format_answer(large_side, settings)
        unit = _unit_label(settings, "cm") or "cm"
        latex = (
            rf"\text{{Two similar triangles have a scale factor of {ratio}:1. "
            rf"The smaller triangle has a side of {small_side} {unit}. "
            rf"What is the corresponding side in the larger triangle?}}"
        )
        text = (
            f"Two similar triangles have a scale factor of {ratio}:1. "
            f"The smaller triangle has a side of {small_side} {unit}. "
            f"What is the corresponding side in the larger triangle?"
        )
        return latex, text, _append_units(answer, settings)
