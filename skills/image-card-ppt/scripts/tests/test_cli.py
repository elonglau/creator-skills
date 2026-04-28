import json

from image_card_ppt.cli import build_pipeline


def test_build_pipeline_writes_html_png_and_report(tmp_path, monkeypatch):
    schema_path = tmp_path / "schema.json"
    schema_path.write_text(
        json.dumps(
            {
                "title": "T",
                "cards": [
                    {"type": "cover", "variant": "cover", "headline": "H1", "body": ["b1"]},
                    {"type": "summary", "variant": "summary", "headline": "H2", "body": ["b2"]},
                ],
                "metadata": {"template": "design"},
            }
        ),
        encoding="utf-8",
    )

    def fake_render(html_path, output_png, width, height):
        output_png.write_bytes(b"png")

    monkeypatch.setattr("image_card_ppt.cli.render_html_to_png", fake_render)

    out_dir = tmp_path / "out"
    exit_code = build_pipeline(schema_path, out_dir)
    assert exit_code == 0

    report = json.loads((out_dir / "report.json").read_text(encoding="utf-8"))
    assert report["card_count"] == 2
    assert report["success_count"] == 2
    assert (out_dir / "html" / "card-00-cover.html").exists()
    assert (out_dir / "images" / "card-00-cover.png").exists()


def test_build_pipeline_supports_all_mvp_variants(tmp_path, monkeypatch):
    schema_path = tmp_path / "schema.json"
    schema_path.write_text(
        json.dumps(
            {
                "title": "T",
                "cards": [
                    {"type": "cover", "variant": "cover", "headline": "cover", "body": ["x"]},
                    {"type": "point", "variant": "image_page", "headline": "image", "body": ["x"]},
                    {"type": "point", "variant": "text_page", "headline": "text", "body": ["x"]},
                    {"type": "summary", "variant": "summary", "headline": "summary", "body": ["x"]},
                ],
                "metadata": {"template": "design"},
            }
        ),
        encoding="utf-8",
    )

    def fake_render(html_path, output_png, width, height):
        output_png.write_bytes(b"png")

    monkeypatch.setattr("image_card_ppt.cli.render_html_to_png", fake_render)
    out_dir = tmp_path / "out"
    exit_code = build_pipeline(schema_path, out_dir)
    assert exit_code == 0
    report = json.loads((out_dir / "report.json").read_text(encoding="utf-8"))
    assert report["success_count"] == 4

