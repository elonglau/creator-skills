import json

import pytest

from image_card_ppt.schema import load_schema, resolve_style


def test_load_schema_requires_title_cards_metadata(tmp_path):
    schema_path = tmp_path / "schema.json"
    schema_path.write_text(json.dumps({"cards": [], "metadata": {}}), encoding="utf-8")
    with pytest.raises(ValueError, match="title"):
        load_schema(schema_path)


def test_load_schema_accepts_valid_minimum_schema(tmp_path):
    schema_path = tmp_path / "schema.json"
    schema_path.write_text(
        json.dumps(
            {
                "title": "t",
                "cards": [{"type": "cover", "variant": "cover"}],
                "metadata": {"template": "tech"},
            }
        ),
        encoding="utf-8",
    )
    loaded = load_schema(schema_path)
    assert loaded["title"] == "t"
    assert resolve_style(loaded, None) == "tech"

