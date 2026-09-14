"""OpenStax story frames for A1 quantity-first narrative WP engines.

Quantity sampling stays in Mixture / DRT / Work frameworks. This module
rotates typed frames (vehicles, jobs, mix stories) so prompts are not one
Mad-Lib with name swaps, and never dump the hidden equation.
"""

from __future__ import annotations

from typing import Any

# OpenStax EA 3.4 / 2.6 vehicles (bike / drive / walk / bus / train).
DRT_VEHICLES: tuple[tuple[str, str, str], ...] = (
    ("bike", "rides a bike", "cyclist"),
    ("car", "drives", "driver"),
    ("walk", "walks", "walker"),
    ("bus", "rides a bus", "bus"),
    ("train", "rides a train", "train"),
)


def pick_drt_vehicle(rng: Any) -> tuple[str, str, str]:
    return rng.choice(DRT_VEHICLES)


# OpenStax EA 8.8 work applications (people jobs + printing press).
WORK_JOBS: tuple[tuple[str, str, str, str], ...] = (
    # frame_id, solo infinitive, same-task noun, together ask tail
    ("work_job", "finish a job", "the same job", "finish the job"),
    ("work_paint", "paint a house", "the same house", "finish painting"),
    ("work_lawn", "mow a lawn", "the same lawn", "finish mowing"),
    ("work_pool", "clean a pool", "the same pool", "finish cleaning"),
    ("work_press", "print an issue", "the same issue", "finish printing"),
)

# OpenStax EA 3.3 / IA 2.4 percent-mix stories (coins/tickets stay on coin leaf).
MIX_PERCENT_FRAMES: tuple[str, ...] = ("soil", "nuts", "alcohol")
MIX_COST_PRODUCTS: tuple[str, ...] = ("cinnamon", "coffee", "tea", "trail mix")


def vehicle_rate_bounds(vehicle: str, *, time_unit: str, band: str) -> tuple[int, int] | None:
    """Classroom speeds (mph / km/h). None means use the generic DRT band."""
    if time_unit not in {"hr", "h"}:
        return None
    table = {
        "walk": (2, 5),
        "bike": (8, 18),
        "bus": (18, 45),
        "car": (25, 70),
        "train": (35, 90),
    }
    bounds = table.get(vehicle)
    if bounds is None:
        return None
    lo, hi = bounds
    if band == "easy":
        return lo, min(hi, lo + 8)
    if band == "hard":
        return lo, hi
    return lo, max(lo + 4, hi - 4)


def catchup_rate_bounds(
    vehicle: str, *, time_unit: str, band: str
) -> tuple[tuple[int, int] | None, tuple[int, int] | None]:
    """Slow traveler uses `vehicle`; chaser uses a faster OpenStax partner."""
    chaser = {
        "walk": "bike",
        "bike": "car",
        "bus": "bus",
        "car": "car",
        "train": "train",
    }.get(vehicle, "car")
    return (
        vehicle_rate_bounds(vehicle, time_unit=time_unit, band=band),
        vehicle_rate_bounds(chaser, time_unit=time_unit, band=band),
    )


def _missing_go(name: str, vehicle: str, verb: str) -> str:
    if vehicle == "bike":
        return f"{name} bikes"
    if vehicle == "car":
        return f"{name} drives"
    if vehicle == "walk":
        return f"{name} walks"
    if vehicle == "bus":
        return f"{name} takes a bus"
    if vehicle == "train":
        return f"{name} takes a train"
    return f"{name} {verb}"


def missing_piece_stems(
    *,
    name: str,
    vehicle: str,
    verb: str,
    distance: int | str,
    rate: int | str,
    time: int | str,
    distance_u: str,
    time_u: str,
    speed_u: str,
    ask: str,
) -> tuple[str, str, str]:
    """Return (frame_id, latex_inner, text) for a one-motion missing piece."""
    fid = f"drt_missing_{vehicle}_{ask}"
    go = _missing_go(name, vehicle, verb)
    if ask == "find_time":
        inner = (
            f"{go} {distance} {distance_u} at {rate} {speed_u}. "
            f"How many {time_u} does the trip take?"
        )
    elif ask == "find_distance":
        inner = (
            f"{go} at {rate} {speed_u} for {time} {time_u}. "
            f"How many {distance_u} does {name} travel?"
        )
    else:
        inner = (
            f"{go} {distance} {distance_u} in {time} {time_u}. "
            f"What is the average speed in {speed_u}?"
        )
    return fid, inner, inner


def round_trip_stems(
    *,
    name: str,
    vehicle: str,
    t_there: int,
    t_back: int,
    r_there: int,
    r_back: int,
    distance: int,
    distance_u: str,
    time_u: str,
    speed_u: str,
    ask: str,
) -> tuple[str, str, str]:
    dest = {
        "bike": "a park",
        "car": "a destination",
        "walk": "the store",
        "bus": "town",
        "train": "the city",
    }.get(vehicle, "a destination")
    go = {
        "bike": f"{name} bikes to {dest}",
        "car": f"{name} drives to {dest}",
        "walk": f"{name} walks to {dest}",
        "bus": f"{name} rides a bus to {dest}",
        "train": f"{name} rides a train to {dest}",
    }.get(vehicle, f"{name} drives to {dest}")
    fid = f"drt_roundtrip_{vehicle}_{ask}"
    if ask == "find_speed_there":
        inner = (
            f"{go} in {t_there} {time_u} and returns in {t_back} {time_u} "
            f"at {r_back} {speed_u}. What was {name}'s speed on the way there?"
        )
    elif ask == "find_time_there":
        go_rate = {
            "bike": f"{name} bikes to {dest} at {r_there} {speed_u}",
            "car": f"{name} drives to {dest} at {r_there} {speed_u}",
            "walk": f"{name} walks to {dest} at {r_there} {speed_u}",
            "bus": f"{name} rides a bus to {dest} at {r_there} {speed_u}",
            "train": f"{name} rides a train to {dest} at {r_there} {speed_u}",
        }.get(vehicle, f"{name} drives to {dest} at {r_there} {speed_u}")
        inner = (
            f"{go_rate} and returns at {r_back} {speed_u}, taking "
            f"{t_back} {time_u} on the way back. How long did the trip there take?"
        )
    else:
        inner = (
            f"{go} {distance} {distance_u} at {r_there} {speed_u}, then returns "
            f"the same distance at {r_back} {speed_u}. "
            f"How many {time_u} does the round trip take?"
        )
    return fid, inner, inner


def opposite_stems(
    *,
    a_name: str,
    b_name: str,
    vehicle: str,
    rate_a: int,
    rate_b: int,
    meet_time: int,
    distance: int,
    distance_u: str,
    time_u: str,
    speed_u: str,
    ask: str,
    toward: bool,
) -> tuple[str, str, str]:
    if toward:
        fid = f"drt_opposite_toward_{vehicle}_{ask}"
        leave = (
            f"{a_name} and {b_name} leave two towns {distance} {distance_u} apart "
            f"at the same time and travel toward each other at {rate_a} {speed_u} "
            f"and {rate_b} {speed_u}"
        )
        if ask == "time":
            inner = f"{leave}. How many {time_u} until they meet?"
        else:
            inner = (
                f"{a_name} and {b_name} leave two towns at the same time and travel "
                f"toward each other at {rate_a} {speed_u} and {rate_b} {speed_u} "
                f"for {meet_time} {time_u}. How many {distance_u} apart were the towns?"
            )
        return fid, inner, inner
    fid = f"drt_opposite_leave_{vehicle}_{ask}"
    if ask == "time":
        inner = (
            f"{a_name} and {b_name} leave the same place at the same time "
            f"and travel in opposite directions at {rate_a} {speed_u} and "
            f"{rate_b} {speed_u}. They are {distance} {distance_u} apart when they "
            f"stop. How many {time_u} did they travel?"
        )
    else:
        inner = (
            f"{a_name} and {b_name} leave the same place at the same time "
            f"and travel in opposite directions at {rate_a} {speed_u} and "
            f"{rate_b} {speed_u} for {meet_time} {time_u}. "
            f"How many {distance_u} apart are they?"
        )
    return fid, inner, inner


def catchup_slow_stems(
    *,
    vehicle: str,
    head: int,
    fast: int,
    catch: int,
    time_u: str,
    speed_u: str,
) -> tuple[str, str, str]:
    """Several OpenStax same-direction catch-up frames (not one slow-bus script)."""
    if vehicle == "bike":
        fid = "drt_catchup_slow_bike"
        inner = (
            f"A cyclist leaves town at an unknown speed. {head} {time_u} later a car "
            f"leaves the same town at {fast} {speed_u} and catches up after "
            f"{catch} {time_u}. What is the cyclist's speed?"
        )
    elif vehicle == "walk":
        fid = "drt_catchup_slow_walk"
        inner = (
            f"A walker leaves a trailhead at an unknown speed. {head} {time_u} later "
            f"a cyclist leaves the same trailhead at {fast} {speed_u} and catches up "
            f"after {catch} {time_u}. What is the walker's speed?"
        )
    elif vehicle == "train":
        fid = "drt_catchup_slow_train"
        inner = (
            f"A slow train leaves a station traveling at an unknown speed. "
            f"{head} {time_u} later a faster train leaves the same station at "
            f"{fast} {speed_u} and catches up after {catch} {time_u}. "
            f"What is the slow train's speed?"
        )
    elif vehicle == "car":
        fid = "drt_catchup_slow_car"
        inner = (
            f"A slow car leaves a rest stop traveling at an unknown speed. "
            f"{head} {time_u} later a faster car leaves the same rest stop at "
            f"{fast} {speed_u} and catches up after {catch} {time_u}. "
            f"What is the slow car's speed?"
        )
    else:
        fid = "drt_catchup_slow_bus"
        inner = (
            f"A slow bus leaves a station traveling at an unknown speed. "
            f"{head} {time_u} later a faster bus leaves the same station at "
            f"{fast} {speed_u} and catches up after {catch} {time_u}. "
            f"What is the slow bus's speed?"
        )
    return fid, inner, inner


def catchup_named_stems(
    *,
    a_name: str,
    b_name: str,
    vehicle: str,
    verb: str,
    slow: int,
    fast: int,
    head: int,
    catch: int,
    time_u: str,
    speed_u: str,
    ask: str,
) -> tuple[str, str, str]:
    fid = f"drt_catchup_named_{vehicle}_{ask}"
    if ask == "find_leader_total_time":
        inner = (
            f"{a_name} {verb} at {slow} {speed_u}. {b_name} leaves later from the "
            f"same place at {fast} {speed_u} in the same direction and catches up "
            f"{catch} {time_u} after starting. How long had {a_name} been traveling "
            f"when caught?"
        )
    else:
        inner = (
            f"{a_name} {verb} at {slow} {speed_u}. {b_name} leaves from the same "
            f"place {head} {time_u} later at {fast} {speed_u} in the same direction. "
            f"How many {time_u} after {b_name} starts does {b_name} catch up to "
            f"{a_name}?"
        )
    return fid, inner, inner


def two_segment_stems(
    *,
    name: str,
    vehicle: str,
    verb: str,
    rate1: int,
    rate2: int,
    t1: int,
    t2: int,
    distance_u: str,
    time_u: str,
    speed_u: str,
) -> tuple[str, str, str]:
    fid = f"drt_twoseg_{vehicle}"
    go = _missing_go(name, vehicle, verb)
    inner = (
        f"{go} at {rate1} {speed_u} for {t1} {time_u}, then "
        f"at {rate2} {speed_u} for {t2} {time_u}. "
        f"How many {distance_u} does {name} travel in all?"
    )
    return fid, inner, inner


def pick_work_job(rng: Any) -> tuple[str, str, str, str]:
    return rng.choice(WORK_JOBS)


def work_two_people(
    *,
    frame: tuple[str, str, str, str],
    a_name: str,
    b_name: str,
    a_time: int,
    b_time: int,
    together: int,
    time_u: str,
    ask: str,
) -> tuple[str, str, str]:
    fid, solo, same, tail = frame
    if fid == "work_press":
        if ask == "together":
            inner = (
                f"Press #1 takes {a_time} {time_u} to print an issue and Press #2 "
                f"takes {b_time} {time_u}. Working together, how many {time_u} will "
                f"it take them to finish the job?"
            )
            return "work_press_together", inner, inner
        inner = (
            f"Press #1 takes {a_time} {time_u} to print an issue. Working with "
            f"Press #2, they finish in {together} {time_u}. How many {time_u} would "
            f"Press #2 need working alone?"
        )
        return "work_press_find_one", inner, inner
    if ask == "together":
        inner = (
            f"{a_name} can {solo} in {a_time} {time_u} and {b_name} can finish "
            f"{same} in {b_time} {time_u}. Working together, how many {time_u} will "
            f"it take them to {tail}?"
        )
        return f"{fid}_together", inner, inner
    inner = (
        f"{a_name} can {solo} in {a_time} {time_u}. Working with {b_name}, they "
        f"finish in {together} {time_u}. How many {time_u} would it take {b_name} "
        f"working alone?"
    )
    return f"{fid}_find_one", inner, inner


def work_three_people(
    *,
    frame: tuple[str, str, str, str],
    names: tuple[str, str, str],
    times: tuple[int, int, int],
    together: int,
    time_u: str,
    ask: str,
) -> tuple[str, str, str]:
    fid, solo, _same, tail = frame
    a_name, b_name, c_name = names
    a_time, b_time, c_time = times
    if ask == "together":
        inner = (
            f"{a_name}, {b_name}, and {c_name} can {solo} in {a_time}, {b_time}, and "
            f"{c_time} {time_u} respectively. Working together, how many {time_u} "
            f"will it take them to {tail}?"
        )
        return f"{fid}_three", inner, inner
    inner = (
        f"{a_name} and {b_name} can {solo} in {a_time} and {b_time} {time_u}. "
        f"With {c_name} helping, the three finish in {together} {time_u}. "
        f"How many {time_u} would {c_name} need alone?"
    )
    return f"{fid}_find_one_time", inner, inner


def work_starts_later(
    *,
    frame: tuple[str, str, str, str],
    a_name: str,
    b_name: str,
    a_time: int,
    b_time: int,
    delay: int,
    total: int,
    time_u: str,
) -> tuple[str, str, str]:
    fid, solo, same, _tail = frame
    inner = (
        f"{a_name} can {solo} in {a_time} {time_u} and {b_name} can finish {same} "
        f"in {b_time} {time_u}. {a_name} works alone for {delay} {time_u}, then "
        f"{b_name} joins. How many {time_u} from the start until the job is done?"
    )
    return f"{fid}_starts_later", inner, inner


def mix_percent_blend(
    *,
    frame: str,
    name: str,
    a1: int,
    a2: int,
    p1: int,
    p2: int,
) -> tuple[str, str, str]:
    if frame == "soil":
        fid = "mix_soil_blend"
        inner = (
            f"{name} mixes {a1} cubic yards of soil that is {p1}% sand with "
            f"{a2} cubic yards of soil that is {p2}% sand. "
            f"What percent of the mixture is sand?"
        )
        latex = (
            f"{name} mixes {a1} cubic yards of soil that is {p1}\\% sand with "
            f"{a2} cubic yards of soil that is {p2}\\% sand. "
            f"What percent of the mixture is sand?"
        )
        return fid, latex, inner
    if frame == "nuts":
        fid = "mix_nuts_blend"
        inner = (
            f"{name} mixes {a1} lb of nuts that are {p1}% peanuts with "
            f"{a2} lb of nuts that are {p2}% peanuts. "
            f"What percent of the new mixture is peanuts?"
        )
        latex = (
            f"{name} mixes {a1} lb of nuts that are {p1}\\% peanuts with "
            f"{a2} lb of nuts that are {p2}\\% peanuts. "
            f"What percent of the new mixture is peanuts?"
        )
        return fid, latex, inner
    fid = "mix_alcohol_blend"
    inner = (
        f"{name} mixes {a1} fl oz of a {p1}% alcohol solution with "
        f"{a2} fl oz of a {p2}% alcohol solution. "
        f"What is the concentration of the new mixture?"
    )
    latex = (
        f"{name} mixes {a1} fl oz of a {p1}\\% alcohol solution with "
        f"{a2} fl oz of a {p2}\\% alcohol solution. "
        f"What is the concentration of the new mixture?"
    )
    return fid, latex, inner


def mix_percent_find_amount(
    *,
    frame: str,
    name: str,
    known: int,
    unknown: int,
    p_known: int,
    p_unknown: int,
    p_mix: int,
) -> tuple[str, str, str]:
    """OpenStax EA 3.3 / IA 2.4: find an amount given a target blend percent."""
    if frame == "soil":
        fid = "mix_soil_find_amount"
        inner = (
            f"{name} mixes {known} cubic yards of soil that is {p_known}% sand with "
            f"some soil that is {p_unknown}% sand. The mixture is {p_mix}% sand. "
            f"How many cubic yards of the {p_unknown}% soil did {name} use?"
        )
        latex = (
            f"{name} mixes {known} cubic yards of soil that is {p_known}\\% sand with "
            f"some soil that is {p_unknown}\\% sand. The mixture is {p_mix}\\% sand. "
            f"How many cubic yards of the {p_unknown}\\% soil did {name} use?"
        )
        return fid, latex, inner
    if frame == "nuts":
        fid = "mix_nuts_find_amount"
        inner = (
            f"{name} mixes {known} lb of nuts that are {p_known}% peanuts with some "
            f"nuts that are {p_unknown}% peanuts. The blend is {p_mix}% peanuts. "
            f"How many pounds of the {p_unknown}% nuts did {name} add?"
        )
        latex = (
            f"{name} mixes {known} lb of nuts that are {p_known}\\% peanuts with some "
            f"nuts that are {p_unknown}\\% peanuts. The blend is {p_mix}\\% peanuts. "
            f"How many pounds of the {p_unknown}\\% nuts did {name} add?"
        )
        return fid, latex, inner
    fid = "mix_alcohol_find_amount"
    inner = (
        f"{name} mixes {known} fl oz of a {p_known}% alcohol solution with some "
        f"{p_unknown}% alcohol solution. The new mixture is {p_mix}% alcohol. "
        f"How many fl oz of the {p_unknown}% solution did {name} add?"
    )
    latex = (
        f"{name} mixes {known} fl oz of a {p_known}\\% alcohol solution with some "
        f"{p_unknown}\\% alcohol solution. The new mixture is {p_mix}\\% alcohol. "
        f"How many fl oz of the {p_unknown}\\% solution did {name} add?"
    )
    return fid, latex, inner


def mix_cost_blend(
    *,
    name: str,
    product: str,
    brand_a: str,
    brand_b: str,
    w1: int,
    w2: int,
    c1: int,
    c2: int,
) -> tuple[str, str, str]:
    fid = f"mix_cost_{product.replace(' ', '_')}"
    if product == "trail mix":
        inner = (
            f"{name} mixes {w1} lb of raisins costing ${c1} per lb with {w2} lb of "
            f"nuts costing ${c2} per lb to make trail mix. What is the cost per "
            f"pound of the trail mix?"
        )
        latex = (
            f"{name} mixes {w1} lb of raisins costing \\${c1} per lb with {w2} lb of "
            f"nuts costing \\${c2} per lb to make trail mix. What is the cost per "
            f"pound of the trail mix?"
        )
        return "mix_trail_blend", latex, inner
    inner = (
        f"{name} blends {w1} lb of {brand_a} {product} costing ${c1} per lb with "
        f"{w2} lb of {brand_b} {product} costing ${c2} per lb. What is the cost "
        f"per pound of the mixture?"
    )
    latex = (
        f"{name} blends {w1} lb of {brand_a} {product} costing \\${c1} per lb with "
        f"{w2} lb of {brand_b} {product} costing \\${c2} per lb. What is the cost "
        f"per pound of the mixture?"
    )
    return fid, latex, inner


def mix_cost_find_amount(
    *,
    name: str,
    total_w: int,
    c1: int,
    c2: int,
    target: str,
    unknown: int,
) -> tuple[str, str, str]:
    """IA 2.4 Ex 2.42 shape: trail mix of given total weight and target $/lb."""
    fid = "mix_trail_find_amount"
    inner = (
        f"{name} is mixing raisins and nuts to make {total_w} pounds of trail mix. "
        f"Raisins cost ${c1} a pound and nuts cost ${c2} a pound. If {name} wants "
        f"the trail mix to cost ${target} a pound, how many pounds of raisins "
        f"should {name} use?"
    )
    latex = (
        f"{name} is mixing raisins and nuts to make {total_w} pounds of trail mix. "
        f"Raisins cost \\${c1} a pound and nuts cost \\${c2} a pound. If {name} wants "
        f"the trail mix to cost \\${target} a pound, how many pounds of raisins "
        f"should {name} use?"
    )
    return fid, latex, inner
