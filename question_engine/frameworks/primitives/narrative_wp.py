"""Narrative word-problem samplers (coin / age) on continuous D + upgrades.

Required structure is enforced in the sampler; optional complexity is purchased
via ``DifficultyFactor`` upgrades (knobs in ``difficulty_knobs.json`` →
``narrative_wp``). Presentation is composed from small phrase fragments — not
N full Mad-Libs sentence scripts.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from question_engine.frameworks.difficulty_budget import DifficultyFactor, select_upgrades
from question_engine.frameworks.primitives.difficulty_knobs import fget, section
from question_engine.frameworks.primitives.registry import PRIM_EQUATIONS, PrimitiveContext
from question_engine.frameworks.primitives.word_problems import WordProblemItem

# ---------------------------------------------------------------------------
# Shared phrase fragments (data-driven pools — keep short)
# ---------------------------------------------------------------------------

_NAMES = ("Alex", "Jordan", "Sam", "Riley", "Casey", "Taylor", "Morgan", "Quinn")

_COIN_FRAMES: tuple[tuple[str, str, str], ...] = (
    # (id, with_total_pattern, without_total_pattern) — {n} total, {d} denoms, {who} name
    ("jar", "A jar contains {n} coins, all {d}", "A jar contains only {d}"),
    ("piggy", "{who}'s piggy bank has {n} coins, all {d}", "{who}'s piggy bank holds only {d}"),
    ("register", "A cash register has {n} coins, all {d}", "A cash register holds only {d}"),
    ("pocket", "{who} has {n} coins in a pocket, all {d}", "{who} has only {d} in a pocket"),
    ("vending", "A vending change box has {n} coins, all {d}", "A vending change box holds only {d}"),
)

_DENOM: dict[str, tuple[str, str, int]] = {
    "quarter": ("quarter", "quarters", 25),
    "dime": ("dime", "dimes", 10),
    "nickel": ("nickel", "nickels", 5),
    "penny": ("penny", "pennies", 1),
}

_PAIR_DEFAULT = ("quarter", "nickel")
_PAIR_ALT = (("quarter", "dime"), ("dime", "nickel"), ("quarter", "penny"))


def _knob(key: str, default: float) -> float:
    return fget("narrative_wp", key, default)


def _money(cents: int) -> tuple[str, str]:
    s = f"{cents / 100.0:.2f}"
    return f"\\${s}", f"${s}"


def _join_clauses(parts: list[str]) -> str:
    """Compose 'A. B. C?' style from clause fragments."""
    cleaned = [p.strip().rstrip(".") for p in parts if p and p.strip()]
    if not cleaned:
        return ""
    capped: list[str] = []
    for p in cleaned:
        if p:
            capped.append(p[:1].upper() + p[1:] if p[0].islower() else p)
    body = ". ".join(capped[:-1])
    last = capped[-1]
    if body:
        return f"{body}. {last}"
    return last


# ---------------------------------------------------------------------------
# Coin — structure sample, then compose render
# ---------------------------------------------------------------------------


def _coin_upgrades() -> tuple[DifficultyFactor, ...]:
    # Costlier structure first so high D can buy three_denoms / trade before
    # cheap ask/polish modifiers consume the budget (select_upgrades is greedy).
    return (
        DifficultyFactor("three_denoms", _knob("coin_three_denoms_cost", 8.0), ("structure",)),
        DifficultyFactor("trade_step", _knob("coin_trade_step_cost", 10.0), ("structure",)),
        DifficultyFactor("rel_ratio", _knob("coin_rel_ratio_cost", 5.0), ("structure",)),
        DifficultyFactor("rel_diff", _knob("coin_rel_diff_cost", 5.0), ("structure",)),
        DifficultyFactor("ask_value", _knob("coin_ask_value_cost", 4.0), ("ask",)),
        DifficultyFactor("alt_pair", _knob("coin_alt_pair_cost", 3.0), ("structure",)),
        DifficultyFactor("larger_scale", _knob("coin_larger_scale_cost", 2.5), ("magnitude",)),
        DifficultyFactor("ask_other", _knob("coin_ask_other_cost", 2.0), ("ask",)),
    )


_COIN_MAJORS = ("trade_step", "three_denoms", "rel_ratio", "rel_diff")


def _weighted_pick(rng, factors: list[DifficultyFactor]) -> DifficultyFactor:
    weights = [max(0.1, f.cost) ** 1.4 for f in factors]
    total = sum(weights)
    r = rng.random() * total
    acc = 0.0
    for f, w in zip(factors, weights):
        acc += w
        if r <= acc:
            return f
    return factors[-1]


def _coin_ids_from_budget(ctx: PrimitiveContext) -> set[str]:
    """Buy at most one major structure upgrade, then polish modifiers."""
    eff = ctx.effective_d(PRIM_EQUATIONS)
    catalog = list(_coin_upgrades())
    majors = [f for f in catalog if f.id in _COIN_MAJORS]
    mods = [f for f in catalog if f.id not in _COIN_MAJORS]

    ids: set[str] = set()
    rem = float(eff)
    affordable = [f for f in majors if f.cost <= rem + 1e-9]
    if affordable:
        # Soft chance to stay on base shape even when upgrades are affordable.
        stay_base = 0.35 if eff < 6 else (0.12 if eff < 14 else 0.05)
        if ctx.rng.random() >= stay_base:
            pick = _weighted_pick(ctx.rng, affordable)
            ids.add(pick.id)
            rem -= pick.cost

    purchased_mods, _, _ = select_upgrades(mods, rem, rng=ctx.rng)
    ids |= {f.id for f in purchased_mods}
    if "trade_step" in ids:
        ids.discard("ask_value")
    if "ask_value" in ids and "ask_other" in ids:
        ids.discard("ask_other")
    return ids


def sample_coin_wp(ctx: PrimitiveContext) -> WordProblemItem:
    """Sample a coin word problem via upgrade spend + composed presentation."""
    ids = _coin_ids_from_budget(ctx)

    for _ in range(12):
        try:
            spec = _build_coin_spec(ctx, ids)
            return _render_coin(spec)
        except ValueError:
            if not ids:
                break
            costs = {f.id: f.cost for f in _coin_upgrades()}
            drop = max(ids, key=lambda i: costs.get(i, 0))
            ids.discard(drop)
            ctx.note_degraded(drop)

    return _render_coin(_build_coin_spec(ctx, set()))


@dataclass(frozen=True)
class _CoinSpec:
    """Abstract coin problem — required: ≥2 denoms + value/count constraints."""

    denom_keys: tuple[str, ...]
    counts: tuple[int, ...]
    # Which facts are presented (required structure always includes enough to solve).
    give_total_count: bool
    give_total_value: bool
    give_one_count: bool
    known_idx: int  # when give_one_count
    ratio_mult: int | None  # n0 = mult * n1
    diff_k: int | None  # n0 = n1 + k
    ask: Literal["count", "value"]
    ask_idx: int
    # Optional trade: after swapping nickels→dimes, give final value; ask start quarters.
    trade_n: int | None
    frame_id: str
    name: str
    upgrades: tuple[str, ...]
    shape_id: str
    n_constraints: int


def _build_coin_spec(ctx: PrimitiveContext, ids: set[str]) -> _CoinSpec:
    rng = ctx.rng
    name = rng.choice(_NAMES)
    frame_id = rng.choice(_COIN_FRAMES)[0]
    scale = 1.35 if "larger_scale" in ids else 1.0
    lo = max(2, int(3 * scale))
    hi = max(lo + 2, int((8 if "larger_scale" not in ids else 14) * scale))

    if "trade_step" in ids:
        # Required: start with quarters + nickels; trade t nickels for t dimes;
        # given start nickels + final value → find start quarters.
        n0 = rng.randint(max(6, lo + 2), hi + 4)
        t = rng.randint(2, min(5, n0 - 2))
        q = rng.randint(lo, hi)
        keys = ("quarter", "nickel", "dime")
        # counts after trade for value: q quarters, n0-t nickels, t dimes
        counts = (q, n0, t)  # store start q, start n, trade t
        shape = "trade"
        n_con = 3
        return _CoinSpec(
            denom_keys=keys,
            counts=counts,
            give_total_count=False,
            give_total_value=True,
            give_one_count=True,
            known_idx=1,
            ratio_mult=None,
            diff_k=None,
            ask="count",
            ask_idx=0,
            trade_n=t,
            frame_id=frame_id,
            name=name,
            upgrades=tuple(sorted(ids)),
            shape_id=f"coin:{shape}",
            n_constraints=n_con,
        )

    if "three_denoms" in ids:
        keys = ("quarter", "dime", "nickel")
        q = rng.randint(lo, hi)
        di = rng.randint(lo, hi)
        # Required third constraint: nickels related to dimes.
        if rng.random() < 0.55:
            ni, ratio_mult, diff_k = di, None, None  # equal — encoded as diff 0 via flag
            # Use ratio_mult=1 to mean equal counts of last two.
            ratio_mult = 1
        else:
            k = rng.randint(1, 4)
            ni, ratio_mult, diff_k = di + k, None, k
        counts = (q, di, ni)
        ask_idx = 0 if "ask_other" not in ids else rng.randint(0, 2)
        shape_bits = ["three"]
        if diff_k is not None:
            shape_bits.append("diff")
        else:
            shape_bits.append("eq")
        return _CoinSpec(
            denom_keys=keys,
            counts=counts,
            give_total_count=True,
            give_total_value=True,
            give_one_count=False,
            known_idx=0,
            ratio_mult=ratio_mult,
            diff_k=diff_k,
            ask="count",
            ask_idx=ask_idx,
            trade_n=None,
            frame_id=frame_id,
            name=name,
            upgrades=tuple(sorted(ids)),
            shape_id="coin:" + "+".join(shape_bits),
            n_constraints=3,
        )

    # Two-denom base (required structure).
    if "alt_pair" in ids:
        a, b = rng.choice(_PAIR_ALT)
    else:
        a, b = _PAIR_DEFAULT
    keys = (a, b)

    ratio_mult = None
    diff_k = None
    give_total = True
    give_one = False
    known_idx = 0

    if "rel_ratio" in ids:
        ratio_mult = 3 if rng.random() < 0.35 else 2
        n1 = rng.randint(lo, hi)
        n0 = ratio_mult * n1
        give_total = False  # ratio replaces total-count as the count constraint
        counts = (n0, n1)
        shape_bits = ["ratio"]
    elif "rel_diff" in ids:
        diff_k = rng.randint(2, 6)
        n1 = rng.randint(lo, hi)
        n0 = n1 + diff_k
        give_total = False
        counts = (n0, n1)
        shape_bits = ["diff"]
    else:
        # Classic: total count + value (or one known count + value).
        if rng.random() < 0.35:
            # one known count + value
            n0 = rng.randint(lo, hi)
            n1 = rng.randint(lo, hi)
            give_total = False
            give_one = True
            known_idx = 0 if rng.random() < 0.5 else 1
            counts = (n0, n1)
            shape_bits = ["one_known"]
        else:
            total = rng.randint(lo + hi // 2, hi * 2)
            n0 = rng.randint(2, max(3, total - 2))
            n1 = total - n0
            counts = (n0, n1)
            shape_bits = ["count_value"]

    ask: Literal["count", "value"] = "value" if "ask_value" in ids else "count"
    if ask == "value":
        # Absolute counts must be pinned without giving the dollar total.
        shape_bits.append("ask_value")
        ask_idx = 0
        give_total_value = False
        if ratio_mult is not None or diff_k is not None:
            give_total = True
            give_one = False
            # Rebuild counts consistent with relation + a free total.
            if ratio_mult is not None and ratio_mult > 1:
                n1 = max(lo, counts[1] if len(counts) > 1 else lo)
                counts = (ratio_mult * n1, n1)
            elif diff_k is not None:
                n1 = max(lo, counts[1] if len(counts) > 1 else lo)
                counts = (n1 + diff_k, n1)
        elif give_one:
            # one known count alone cannot pin the other — force ratio + total.
            give_one = False
            give_total = True
            ratio_mult = 2
            n1 = max(lo, counts[1] if len(counts) > 1 else lo)
            counts = (2 * n1, n1)
            shape_bits = ["ratio", "ask_value"]
        else:
            # Classic count_value → add ratio so value is determined from counts.
            give_total = True
            ratio_mult = 2
            n1 = max(lo, 2)
            counts = (2 * n1, n1)
            shape_bits = ["ratio", "ask_value"]
    else:
        ask_idx = 1 if "ask_other" in ids else 0
        if "ask_other" in ids:
            shape_bits.append("ask_other")
        give_total_value = True

    n_con = 2
    if "three_denoms" in ids:
        n_con = 3

    return _CoinSpec(
        denom_keys=keys,
        counts=counts,
        give_total_count=give_total,
        give_total_value=give_total_value,
        give_one_count=give_one,
        known_idx=known_idx,
        ratio_mult=ratio_mult,
        diff_k=diff_k,
        ask=ask,
        ask_idx=ask_idx,
        trade_n=None,
        frame_id=frame_id,
        name=name,
        upgrades=tuple(sorted(ids)),
        shape_id="coin:" + "+".join(shape_bits),
        n_constraints=n_con,
    )


def _denom_phrase(keys: tuple[str, ...]) -> str:
    plurals = [_DENOM[k][1] for k in keys]
    if len(plurals) == 2:
        return f"{plurals[0]} and {plurals[1]}"
    return f"{plurals[0]}, {plurals[1]}, and {plurals[2]}"


def _frame_intro(frame_id: str, *, name: str, total: int | None, denoms: str) -> str:
    for fid, with_t, without_t in _COIN_FRAMES:
        if fid == frame_id:
            if total is not None:
                return with_t.format(n=total, d=denoms, who=name)
            return without_t.format(d=denoms, who=name)
    if total is not None:
        return f"A jar contains {total} coins, all {denoms}"
    return f"A jar contains only {denoms}"


def _render_coin(spec: _CoinSpec) -> WordProblemItem:
    denoms = _denom_phrase(spec.denom_keys)
    cents_vals = [_DENOM[k][2] for k in spec.denom_keys]
    plurals = [_DENOM[k][1] for k in spec.denom_keys]

    # Trade path — special compose.
    if spec.trade_n is not None:
        q, n0, t = spec.counts
        final_cents = q * 25 + (n0 - t) * 5 + t * 10
        ml, mt = _money(final_cents)
        clauses = [
            f"{spec.name} had some quarters and {n0} nickels",
            f"{spec.name} traded {t} nickels for {t} dimes",
            f"The coins were then worth {mt}",
            f"How many quarters did {spec.name} have?",
        ]
        text = _join_clauses(clauses)
        latex_clauses = [
            f"{spec.name} had some quarters and {n0} nickels",
            f"{spec.name} traded {t} nickels for {t} dimes",
            f"The coins were then worth {ml}",
            f"How many quarters did {spec.name} have?",
        ]
        latex = r"\text{" + _join_clauses(latex_clauses) + "}"
        return WordProblemItem(
            latex=latex,
            text=text,
            answer_latex=str(q),
            kind="coin",
            equation_latex=f"25q + 5({n0}-{t}) + 10({t}) = {final_cents}",
            upgrades=spec.upgrades,
            effective_d=float(spec.n_constraints * 4),
            shape_id=spec.shape_id,
            n_constraints=spec.n_constraints,
            frame=spec.frame_id,
        )

    total = sum(spec.counts)
    value_cents = sum(c * v for c, v in zip(spec.counts, cents_vals))

    total_for_intro = total if spec.give_total_count else None
    intro = _frame_intro(
        spec.frame_id, name=spec.name, total=total_for_intro, denoms=denoms
    )

    clauses_t: list[str] = [intro]
    clauses_l: list[str] = [intro]

    if spec.give_one_count:
        i = spec.known_idx
        clauses_t.append(f"There are {spec.counts[i]} {plurals[i]}")
        clauses_l.append(f"There are {spec.counts[i]} {plurals[i]}")

    if spec.ratio_mult == 1 and len(spec.denom_keys) == 3:
        clauses_t.append(f"there are as many {plurals[2]} as {plurals[1]}")
        clauses_l.append(f"there are as many {plurals[2]} as {plurals[1]}")
    elif spec.ratio_mult is not None and spec.ratio_mult > 1:
        if spec.ratio_mult == 2:
            rel = f"there are twice as many {plurals[0]} as {plurals[1]}"
        else:
            rel = (
                f"there are {spec.ratio_mult} times as many {plurals[0]} "
                f"as {plurals[1]}"
            )
        clauses_t.append(rel)
        clauses_l.append(rel)

    if spec.diff_k is not None:
        # Two-denom: more of first; three-denom with diff: more nickels than dimes.
        if len(spec.denom_keys) == 3:
            more_pl = plurals[2]
            less_pl = plurals[1]
            more_sg = _DENOM[spec.denom_keys[2]][0]
        else:
            more_pl = plurals[0]
            less_pl = plurals[1]
            more_sg = _DENOM[spec.denom_keys[0]][0]
        more_word = more_sg if spec.diff_k == 1 else more_pl
        verb = "is" if spec.diff_k == 1 else "are"
        rel = f"there {verb} {spec.diff_k} more {more_word} than {less_pl}"
        clauses_t.append(rel)
        clauses_l.append(rel)

    if spec.give_total_value:
        ml, mt = _money(value_cents)
        clauses_t.append(f"the coins are worth {mt} in total")
        clauses_l.append(f"the coins are worth {ml} in total")

    if spec.ask == "value":
        clauses_t.append("What is the total value of the coins?")
        clauses_l.append("What is the total value of the coins?")
        ml, _ = _money(value_cents)
        answer = ml
    else:
        ask_pl = plurals[spec.ask_idx]
        clauses_t.append(f"How many {ask_pl} are there?")
        clauses_l.append(f"How many {ask_pl} are there?")
        answer = str(spec.counts[spec.ask_idx])

    text = _join_clauses(clauses_t)
    latex = r"\text{" + _join_clauses(clauses_l) + "}"

    return WordProblemItem(
        latex=latex,
        text=text,
        answer_latex=answer,
        kind="coin",
        equation_latex="; ".join(
            f"{plurals[i]}={spec.counts[i]}" for i in range(len(spec.counts))
        ),
        upgrades=spec.upgrades,
        effective_d=float(4 + 3 * max(0, spec.n_constraints - 2) + len(spec.upgrades)),
        shape_id=spec.shape_id,
        n_constraints=spec.n_constraints,
        frame=spec.frame_id,
    )


# ---------------------------------------------------------------------------
# Age — structure sample + compose
# ---------------------------------------------------------------------------


def _age_upgrades() -> tuple[DifficultyFactor, ...]:
    return (
        DifficultyFactor("three_people", _knob("age_three_people_cost", 9.0), ("structure",)),
        DifficultyFactor("times_as_old", _knob("age_times_as_old_cost", 7.0), ("structure",)),
        DifficultyFactor("future_shift", _knob("age_future_shift_cost", 5.0), ("structure",)),
        DifficultyFactor("past_shift", _knob("age_past_shift_cost", 5.0), ("structure",)),
        DifficultyFactor("larger_ages", _knob("age_larger_ages_cost", 2.0), ("magnitude",)),
        DifficultyFactor("ask_older", _knob("age_ask_older_cost", 1.5), ("ask",)),
    )


_AGE_MAJORS = ("three_people", "times_as_old", "future_shift", "past_shift")


@dataclass(frozen=True)
class _AgeSpec:
    names: tuple[str, ...]
    ages: tuple[int, ...]
    diff: int
    sum_now: int
    shift_years: int | None  # future (+) or past (−) applied to sum clue
    times: int | None
    ask_idx: int
    upgrades: tuple[str, ...]
    shape_id: str
    n_constraints: int


def sample_age_wp(ctx: PrimitiveContext) -> WordProblemItem:
    eff = ctx.effective_d(PRIM_EQUATIONS)
    catalog = list(_age_upgrades())
    majors = [f for f in catalog if f.id in _AGE_MAJORS]
    mods = [f for f in catalog if f.id not in _AGE_MAJORS]
    ids: set[str] = set()
    rem = float(eff)
    affordable = [f for f in majors if f.cost <= rem + 1e-9]
    if affordable:
        stay_base = 0.35 if eff < 6 else (0.12 if eff < 14 else 0.05)
        if ctx.rng.random() >= stay_base:
            pick = _weighted_pick(ctx.rng, affordable)
            ids.add(pick.id)
            rem -= pick.cost
    purchased_mods, _, _ = select_upgrades(mods, rem, rng=ctx.rng)
    ids |= {f.id for f in purchased_mods}
    if "three_people" in ids:
        ids.discard("ask_older")

    for _ in range(10):
        try:
            return _render_age(_build_age_spec(ctx, ids))
        except ValueError:
            if not ids:
                break
            costs = {f.id: f.cost for f in _age_upgrades()}
            drop = max(ids, key=lambda i: costs.get(i, 0))
            ids.discard(drop)
            ctx.note_degraded(drop)
    return _render_age(_build_age_spec(ctx, set()))


def _build_age_spec(ctx: PrimitiveContext, ids: set[str]) -> _AgeSpec:
    rng = ctx.rng
    hi = 28 if "larger_ages" in ids else 18
    lo = 8 if "larger_ages" not in ids else 12

    if "three_people" in ids:
        names = tuple(rng.sample(list(_NAMES), 3))
        b = rng.randint(lo, hi)
        d1 = rng.randint(2, 8)
        d2 = rng.randint(2, 8)
        a, c = b + d1, b + d2
        ages = (a, b, c)
        # Constraints: A older than B by d1, C older than B by d2, sum = S → find B
        return _AgeSpec(
            names=names,
            ages=ages,
            diff=d1,
            sum_now=sum(ages),
            shift_years=None,
            times=None,
            ask_idx=1,
            upgrades=tuple(sorted(ids)),
            shape_id="age:three",
            n_constraints=3,
        )

    names = tuple(rng.sample(list(_NAMES), 2))
    younger = rng.randint(lo, hi)
    if "times_as_old" in ids:
        times = 3 if rng.random() < 0.3 else 2
        older = times * younger
        diff = older - younger
        shape = "times"
    else:
        times = None
        diff = rng.randint(2, 10 if "larger_ages" in ids else 8)
        older = younger + diff
        shape = "sum_diff"

    ages = (older, younger)
    shift = None
    if "future_shift" in ids:
        shift = rng.randint(3, 8)
        shape = "future"
    elif "past_shift" in ids:
        # Keep past ages positive.
        shift = -rng.randint(2, min(6, younger - 1))
        shape = "past"

    ask_idx = 0 if "ask_older" in ids else 1
    if "ask_older" in ids:
        shape = shape + "+ask_older"

    n_con = 2 + (1 if shift is not None else 0)
    return _AgeSpec(
        names=names,
        ages=ages,
        diff=diff,
        sum_now=sum(ages),
        shift_years=shift,
        times=times,
        ask_idx=ask_idx,
        upgrades=tuple(sorted(ids)),
        shape_id=f"age:{shape}",
        n_constraints=n_con,
    )


def _render_age(spec: _AgeSpec) -> WordProblemItem:
    years = "years"
    clauses: list[str] = []

    if len(spec.names) == 3:
        a_n, b_n, c_n = spec.names
        a, b, c = spec.ages
        clauses.append(f"{a_n} is {a - b} {years} older than {b_n}")
        clauses.append(f"{c_n} is {c - b} {years} older than {b_n}")
        clauses.append(f"The sum of their ages is {spec.sum_now} {years}")
        clauses.append(f"How old is {b_n}?")
        answer = str(b)
    else:
        older_n, younger_n = spec.names
        older_a, younger_a = spec.ages
        if spec.times is not None:
            if spec.times == 2:
                clauses.append(f"{older_n} is twice as old as {younger_n}")
            else:
                clauses.append(
                    f"{older_n} is {spec.times} times as old as {younger_n}"
                )
        else:
            clauses.append(
                f"{older_n} is {spec.diff} {years} older than {younger_n}"
            )

        if spec.shift_years is not None and spec.shift_years > 0:
            y = spec.shift_years
            future_sum = spec.sum_now + 2 * y
            clauses.append(
                f"In {y} {years}, the sum of their ages will be {future_sum} {years}"
            )
        elif spec.shift_years is not None and spec.shift_years < 0:
            y = -spec.shift_years
            past_sum = spec.sum_now - 2 * y
            clauses.append(
                f"{y} {years} ago, the sum of their ages was {past_sum} {years}"
            )
        else:
            clauses.append(
                f"The sum of their ages is {spec.sum_now} {years}"
            )

        ask_name = spec.names[spec.ask_idx]
        clauses.append(f"How old is {ask_name}?")
        answer = str(spec.ages[spec.ask_idx])

    text = _join_clauses(clauses)
    latex = r"\text{" + text + "}"
    return WordProblemItem(
        latex=latex,
        text=text,
        answer_latex=answer,
        kind="age",
        equation_latex=f"ages={spec.ages}",
        upgrades=spec.upgrades,
        effective_d=float(4 + 3 * max(0, spec.n_constraints - 2) + len(spec.upgrades)),
        shape_id=spec.shape_id,
        n_constraints=spec.n_constraints,
        frame="",
    )


# ---------------------------------------------------------------------------
# Consecutive — D-gated upgrades over required consecutive structure
# ---------------------------------------------------------------------------


def _consecutive_upgrades() -> tuple[DifficultyFactor, ...]:
    return (
        DifficultyFactor("more_count", _knob("consec_more_count_cost", 3.0), ("structure",)),
        DifficultyFactor("parity_even", _knob("consec_parity_cost", 4.0), ("structure",)),
        DifficultyFactor("parity_odd", _knob("consec_parity_cost", 4.0), ("structure",)),
        DifficultyFactor("sum_first_last", _knob("consec_sum_first_last_cost", 3.5), ("ask",)),
        DifficultyFactor("product_goal", _knob("consec_product_cost", 7.0), ("ask",)),
        DifficultyFactor("larger_start", _knob("consec_larger_start_cost", 2.0), ("magnitude",)),
    )


_COUNT_WORDS = {2: "two", 3: "three", 4: "four", 5: "five"}


def sample_consecutive_wp(
    ctx: PrimitiveContext, settings: dict[str, Any] | None = None
) -> WordProblemItem:
    settings = settings or {}
    eff = ctx.effective_d(PRIM_EQUATIONS)
    purchased, _, _ = select_upgrades(_consecutive_upgrades(), eff, rng=ctx.rng)
    ids = {f.id for f in purchased}
    # Preset / UI toggles can force structure beyond upgrade spend.
    if bool(settings.get("allow_consecutive_even")):
        ids.add("parity_even")
    if bool(settings.get("allow_consecutive_odd")):
        ids.add("parity_odd")
    if bool(settings.get("allow_sum_first_last_goal")):
        ids.add("sum_first_last")
    if bool(settings.get("allow_product_goal")):
        ids.add("product_goal")
    if "parity_even" in ids and "parity_odd" in ids:
        drop = "parity_odd" if ctx.rng.random() < 0.5 else "parity_even"
        ids.discard(drop)
    if "product_goal" in ids and "sum_first_last" in ids:
        ids.discard("sum_first_last")

    lo_c = int(settings.get("min_consecutive_count") or section("narrative_wp").get("consec_min_count", 2))
    hi_c = int(settings.get("max_consecutive_count") or section("narrative_wp").get("consec_max_count", 5))
    lo_c, hi_c = max(2, min(5, lo_c)), max(2, min(5, hi_c))
    if lo_c > hi_c:
        lo_c, hi_c = hi_c, lo_c

    count = lo_c
    if "more_count" in ids:
        count = ctx.rng.randint(lo_c, hi_c)
    else:
        count = min(hi_c, max(lo_c, 2 if eff < 5 else 3))

    parity = "any"
    if "parity_even" in ids:
        parity = "even"
    elif "parity_odd" in ids:
        parity = "odd"

    if "product_goal" in ids:
        goal = "product"
    elif "sum_first_last" in ids:
        goal = "sum_first_last"
    else:
        goal = "sum"

    step = 1 if parity == "any" else 2
    span = 12 if "larger_start" in ids else 20
    start = ctx.rng.randint(2 if parity != "any" else 1, span + count * step)
    if parity == "even" and start % 2:
        start += 1
    elif parity == "odd" and start % 2 == 0:
        start += 1
    values = [start + i * step for i in range(count)]
    phrase = _COUNT_WORDS.get(count, str(count))
    if parity == "even":
        phrase = f"{phrase} consecutive even integers"
    elif parity == "odd":
        phrase = f"{phrase} consecutive odd integers"
    else:
        phrase = f"{phrase} consecutive integers"

    if goal == "product":
        clue = values[0] * values[-1]
        text = (
            f"The product of the first and last of {phrase} is {clue}. "
            f"Find the smallest integer."
        )
    elif goal == "sum_first_last":
        clue = values[0] + values[-1]
        text = (
            f"The sum of the first and last of {phrase} is {clue}. "
            f"Find the smallest integer."
        )
    else:
        clue = sum(values)
        # Slight wording variety from a 2-fragment pool (not N Mad-Libs).
        if count >= 4 and ctx.rng.random() < 0.5:
            text = f"Find the smallest of {phrase} whose sum is {clue}."
        else:
            text = f"The sum of {phrase} is {clue}. Find the smallest integer."

    shape = f"consec:{parity}:{goal}:n{count}"
    n_con = 1 + (1 if parity != "any" else 0) + (1 if goal != "sum" else 0)
    return WordProblemItem(
        latex=r"\text{" + text + "}",
        text=text,
        answer_latex=str(start),
        kind="consecutive",
        equation_latex=f"start={start}",
        upgrades=tuple(sorted(ids)),
        effective_d=eff,
        shape_id=shape,
        n_constraints=n_con,
        frame="",
    )


def narrative_item_metadata(item: WordProblemItem, ctx: PrimitiveContext) -> dict[str, Any]:
    """Standard metadata for galleries / ML (shape_id, spend, upgrades, …)."""
    return {
        **ctx.metadata(),
        "shape_id": item.shape_id,
        "template_id": item.shape_id,  # alias for gallery tooling
        "shape": item.shape_id,
        "n_constraints": item.n_constraints,
        "frame": item.frame,
        "upgrades": list(item.upgrades),
        "wp_kind": item.kind,
        "primitive_engine": "narrative_wp",
    }
