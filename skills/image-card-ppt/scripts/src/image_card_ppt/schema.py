import json
from pathlib import Path
from typing import Any

REQUIRED_TOP_LEVEL_FIELDS = ("title", "cards", "metadata")
ALLOWED_VARIANTS = {"cover", "image_page", "text_page", "summary"}


def load_schema(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    validate_schema(data)
    return data


def validate_schema(data: dict[str, Any]) -> None:
    for field in REQUIRED_TOP_LEVEL_FIELDS:
        if field not in data:
            raise ValueError(f"schema missing required field: {field}")

    if not isinstance(data["cards"], list) or not data["cards"]:
        raise ValueError("schema cards must be a non-empty list")

    for index, card in enumerate(data["cards"]):
        if not isinstance(card, dict):
            raise ValueError(f"card[{index}] must be object")
        variant = card.get("variant")
        if variant and variant not in ALLOWED_VARIANTS:
            raise ValueError(f"card[{index}] has unsupported variant: {variant}")


def resolve_style(schema: dict[str, Any], override_style: str | None) -> str:
    if override_style:
        return override_style
    metadata = schema.get("metadata", {})
    return metadata.get("template") or "design"


def media_index(schema: dict[str, Any]) -> dict[str, dict[str, Any]]:
    assets = schema.get("media_assets") or []
    return {asset["id"]: asset for asset in assets if isinstance(asset, dict) and "id" in asset}

