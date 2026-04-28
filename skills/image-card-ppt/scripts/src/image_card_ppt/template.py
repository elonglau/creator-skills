import json
from pathlib import Path
from typing import Any

from .schema import media_index


def load_template_html(templates_dir: Path, style: str) -> str:
    return (templates_dir / f"{style}.html").read_text(encoding="utf-8")


def load_template_config(templates_dir: Path, style: str) -> dict[str, Any]:
    return json.loads((templates_dir / f"{style}.config.json").read_text(encoding="utf-8"))


def build_card_payload(
    schema: dict[str, Any], card: dict[str, Any], card_index: int, config: dict[str, Any]
) -> dict[str, Any]:
    total = len(schema["cards"])
    variant = card.get("variant")
    if not variant:
        variant = "cover" if card.get("type") == "cover" else config.get("defaultVariant", "image_page")

    media = _resolve_card_media(schema, card)
    brand = config.get("brand") or {}
    footer = card.get("footer") or {
        "left": f'{brand.get("name", "飞柳OnMyWay")} · AI Lab',
        "right": f"{card_index:02d} / {total:02d} · {card.get('type', 'page')}",
    }

    return {
        "type": card.get("type", "point"),
        "variant": variant,
        "layout": card.get("layout_hint", "no_media"),
        "brand": {"name": brand.get("name", "飞柳OnMyWay"), "subtitle": brand.get("subtitle", "")},
        "page": {"current": f"{card_index:02d}", "total": f"{total:02d}"},
        "chips": card.get("chips") or [],
        "eyebrow": card.get("eyebrow", ""),
        "headline": card.get("headline", ""),
        "body": card.get("body") or [],
        "media": media,
        "footer": footer,
        "stats": card.get("stats") or [],
    }


def render_card_html(template_html: str, config: dict[str, Any], card_payload: dict[str, Any]) -> str:
    bootstrap_script = (
        "<script>\n"
        f"window.TEMPLATE_CONFIG = {json.dumps(config, ensure_ascii=False)};\n"
        f"window.CARD_DATA = {json.dumps(card_payload, ensure_ascii=False)};\n"
        "</script>\n"
    )
    return template_html.replace("<script>", bootstrap_script + "<script>", 1)


def _resolve_card_media(schema: dict[str, Any], card: dict[str, Any]) -> dict[str, Any] | None:
    refs = card.get("media_refs") or []
    if not refs:
        return None

    assets = media_index(schema)
    asset = assets.get(refs[0])
    if not asset:
        return None

    return {
        "id": asset.get("id"),
        "src": asset.get("src"),
        "alt": asset.get("alt", ""),
        "caption": asset.get("notes", ""),
        "code": asset.get("id", "img"),
    }

