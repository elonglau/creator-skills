from image_card_ppt.template import build_card_payload, render_card_html


def test_render_card_html_injects_config_and_card_data():
    html = "<html><body><div>demo</div><script>console.log(1)</script></body></html>"
    config = {"style": "design", "brand": {"name": "N", "subtitle": "S"}}
    payload = {"type": "cover", "headline": "h"}
    rendered = render_card_html(html, config, payload)
    assert "window.TEMPLATE_CONFIG" in rendered
    assert "window.CARD_DATA" in rendered
    assert rendered.count("window.TEMPLATE_CONFIG") == 1


def test_build_card_payload_maps_media_refs():
    schema = {
        "cards": [{"type": "point", "variant": "image_page", "media_refs": ["asset_001"]}],
        "media_assets": [{"id": "asset_001", "src": "/tmp/a.png", "alt": "sample", "notes": "caption"}],
    }
    card = schema["cards"][0]
    config = {"brand": {"name": "Brand", "subtitle": "Sub"}, "defaultVariant": "image_page"}
    payload = build_card_payload(schema, card, 1, config)
    assert payload["media"]["id"] == "asset_001"
    assert payload["media"]["src"] == "/tmp/a.png"

