"""Precalculus skeleton generators — trig identity / equation species."""

from __future__ import annotations

from typing import Any, Callable

from question_engine.core.models import Question
from question_engine.frameworks.primitives import build_context
from question_engine.frameworks.primitives.algebraic_ml import enrich_algebraic_meta
from question_engine.frameworks.primitives.trig_skeleton import (
    sample_trig_double_angle_item,
    sample_trig_factor_eq_item,
    sample_trig_product_to_sum_item,
    sample_trig_rewrite_item,
    sample_trig_sum_diff_item,
    use_trig_double_angle_skeleton,
    use_trig_factor_eq_skeleton,
    use_trig_identity_skeleton,
    use_trig_product_to_sum_skeleton,
    use_trig_sum_diff_skeleton,
)
from question_engine.generators.utils import make_questions


def _meta_builder(last: dict[str, Any], topic: str, *, generator: str, pack: str):
    def metadata_builder(_p: str, _t: str, answer: str | None) -> dict[str, Any]:
        meta = dict(last.get("meta") or {})
        return enrich_algebraic_meta(
            meta,
            pack=pack,
            generator=generator,
            methods_used=list(meta.get("methods_used") or ["trig_identity"]),
            answer=answer,
            course_tag="pc" if str(topic).startswith("pc_") else "a2",
        )

    return metadata_builder


def _skeleton_or_old(
    topic: str,
    settings: dict,
    *,
    use_skel: Callable[[dict], bool],
    old_key: str,
    sample,
    generator: str,
    pack: str,
    default_leaf: str,
) -> list[Question]:
    # Skeleton species are PC-catalog-driven; A2 shared keys stay on old path.
    if not str(topic or "").startswith("pc_") or not use_skel(settings):
        from question_engine.generators import precalc as _precalc_mod

        return _precalc_mod.GENERATORS[old_key](topic, settings)

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}
    local = dict(settings)

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            local,
            [],
            leaf_id=str(topic or default_leaf),
        )
        item = sample(ctx, leaf_id=str(topic or ""))
        answer = item.answer_latex if include_answer_key else None
        last["meta"] = item.metadata
        return item.prompt_latex, item.prompt_text, answer

    return make_questions(
        topic,
        count,
        include_answer_key,
        build,
        metadata_builder=_meta_builder(last, topic, generator=generator, pack=pack),
        settings=settings,
    )


def trig_basic_identities(topic: str, settings: dict) -> list[Question]:
    """Fundamental trig identities — TrigRewrite skeleton (default) or old path."""
    return _skeleton_or_old(
        topic,
        settings,
        use_skel=use_trig_identity_skeleton,
        old_key="trig_basic_identities",
        sample=sample_trig_rewrite_item,
        generator="trig_basic_identities",
        pack="structured_trig_identity",
        default_leaf="pc_fundamental_identities",
    )


def trig_sum_difference(topic: str, settings: dict) -> list[Question]:
    """Sum/difference identities — TrigSumDiff skeleton (default) or old path."""
    return _skeleton_or_old(
        topic,
        settings,
        use_skel=use_trig_sum_diff_skeleton,
        old_key="trig_sum_difference",
        sample=sample_trig_sum_diff_item,
        generator="trig_sum_difference",
        pack="structured_trig_identity",
        default_leaf="pc_sum_and_difference_identities",
    )


def trig_multiple_angle(topic: str, settings: dict) -> list[Question]:
    """Double-angle identities — TrigDoubleAngle skeleton (default) or old path."""
    return _skeleton_or_old(
        topic,
        settings,
        use_skel=use_trig_double_angle_skeleton,
        old_key="trig_multiple_angle",
        sample=sample_trig_double_angle_item,
        generator="trig_multiple_angle",
        pack="structured_trig_identity",
        default_leaf="pc_multiple_angle_identities",
    )


def trig_product_to_sum(topic: str, settings: dict) -> list[Question]:
    """Product-to-sum identities — TrigProductToSum skeleton (default) or old path."""
    return _skeleton_or_old(
        topic,
        settings,
        use_skel=use_trig_product_to_sum_skeleton,
        old_key="trig_product_to_sum",
        sample=sample_trig_product_to_sum_item,
        generator="trig_product_to_sum",
        pack="structured_trig_identity",
        default_leaf="pc_product_to_sum_identities",
    )


def trig_factoring_equations(topic: str, settings: dict) -> list[Question]:
    """Factoring trig equations — TrigFactorEq on gold-locked leaf; else old path.

    ``pc_equations_and_multiple_angle_identities`` is LOW_VARIETY / gold unlocked —
    keep old path (gallery red-header only).
    """
    leaf = str(topic or "")
    if leaf == "pc_equations_and_multiple_angle_identities":
        from question_engine.generators import precalc as _precalc_mod

        return _precalc_mod.GENERATORS["trig_factoring_equations"](topic, settings)
    return _skeleton_or_old(
        topic,
        settings,
        use_skel=use_trig_factor_eq_skeleton,
        old_key="trig_factoring_equations",
        sample=sample_trig_factor_eq_item,
        generator="trig_factoring_equations",
        pack="structured_trig_equation",
        default_leaf="pc_equations_with_factoring_and_fundamental_identities",
    )


GENERATORS: dict[str, Any] = {
    "trig_basic_identities": trig_basic_identities,
    "trig_sum_difference": trig_sum_difference,
    "trig_multiple_angle": trig_multiple_angle,
    "trig_product_to_sum": trig_product_to_sum,
    "trig_factoring_equations": trig_factoring_equations,
}
