"""Gallery notes flag tokens written from the live rater."""

from __future__ import annotations

from question_engine.ml.gallery_notes_flags import (
    apply_notes_action,
    gold_is_graph_live_is_text,
    has_token,
)


def test_low_variety_round_trip(tmp_path, monkeypatch):
    from question_engine.ml import gallery_notes_flags as gnf

    monkeypatch.setattr(gnf, "NOTES_DIR", tmp_path)
    type_id = "zz_live_rating_flag_smoke"
    first = apply_notes_action(type_id, "too_unvaried")
    md = (tmp_path / f"{type_id}.md").read_text(encoding="utf-8")
    assert "LOW_VARIETY" in first["tokens"]
    assert has_token(md, "LOW_VARIETY")
    assert re_word(md, "LOW_VARIETY")

    second = apply_notes_action(type_id, "varied_enough")
    md2 = (tmp_path / f"{type_id}.md").read_text(encoding="utf-8")
    assert "LOW_VARIETY" not in second["tokens"]
    assert not has_token(md2, "LOW_VARIETY")
    assert "VARIED" not in md2


def test_varied_enough_keeps_limitations(tmp_path, monkeypatch):
    from question_engine.ml import gallery_notes_flags as gnf

    monkeypatch.setattr(gnf, "NOTES_DIR", tmp_path)
    type_id = "zz_keep_limitations"
    (tmp_path / f"{type_id}.md").write_text(
        "# Notes\n\n## Variety notes\n\n`LOW_VARIETY`\n\n## Limitations\n\n`LIMITATIONS` remains.\n",
        encoding="utf-8",
    )
    out = apply_notes_action(type_id, "varied_enough")
    md = (tmp_path / f"{type_id}.md").read_text(encoding="utf-8")
    assert "LOW_VARIETY" not in out["tokens"]
    assert has_token(md, "LIMITATIONS")


def test_wrong_skill_adds_unclear_and_optional_not_implemented(tmp_path, monkeypatch):
    from question_engine.ml import gallery_notes_flags as gnf

    monkeypatch.setattr(gnf, "NOTES_DIR", tmp_path)
    type_id = "zz_wrong_skill"
    with_core = apply_notes_action(type_id, "wrong_skill", has_core=True)
    assert "UNCLEAR" in with_core["tokens"]
    assert "NOT_IMPLEMENTED" not in with_core["tokens"]

    no_core = apply_notes_action(type_id, "wrong_skill", has_core=False)
    assert "NOT_IMPLEMENTED" in no_core["tokens"]
    md = (tmp_path / f"{type_id}.md").read_text(encoding="utf-8")
    assert has_token(md, "UNCLEAR")
    assert has_token(md, "NOT_IMPLEMENTED")


def test_needs_figures_unclear_when_graph_gold(tmp_path, monkeypatch):
    from question_engine.ml import gallery_notes_flags as gnf

    monkeypatch.setattr(gnf, "NOTES_DIR", tmp_path)
    type_id = "zz_needs_figures"
    (tmp_path / f"{type_id}.md").write_text(
        "# Notes\n\nGold is graph-match of f / f' figures.\n\n## Limitations\n\nNo figure bank.\n",
        encoding="utf-8",
    )
    out = apply_notes_action(type_id, "needs_figures", has_svg=False)
    assert "LIMITATIONS" in out["tokens"]
    assert "UNCLEAR" in out["tokens"]
    assert gold_is_graph_live_is_text(
        (tmp_path / f"{type_id}.md").read_text(encoding="utf-8"),
        type_id,
        has_svg=False,
    )


def re_word(md: str, token: str) -> bool:
    import re

    return bool(re.search(rf"\b{token}\b", md))
