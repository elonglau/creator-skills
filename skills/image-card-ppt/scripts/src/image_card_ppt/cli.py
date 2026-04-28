import argparse
from pathlib import Path

from .paths import templates_dir
from .render import render_html_to_png
from .report import write_report
from .schema import load_schema, resolve_style
from .template import build_card_payload, load_template_config, load_template_html, render_card_html


def build_pipeline(
    input_path: Path,
    output_dir: Path,
    style_override: str | None = None,
    brand_name: str | None = None,
    brand_subtitle: str | None = None,
) -> int:
    schema = load_schema(input_path)
    style = resolve_style(schema, style_override)
    t_dir = templates_dir()
    config = load_template_config(t_dir, style)
    template_html = load_template_html(t_dir, style)

    if brand_name or brand_subtitle:
        config = dict(config)
        config["brand"] = dict(config.get("brand", {}))
        if brand_name:
            config["brand"]["name"] = brand_name
        if brand_subtitle:
            config["brand"]["subtitle"] = brand_subtitle

    canvas = schema.get("canvas") or config.get("canvas") or {"width": 1080, "height": 1440}
    width = int(canvas.get("width", 1080))
    height = int(canvas.get("height", 1440))

    html_dir = output_dir / "html"
    img_dir = output_dir / "images"
    html_dir.mkdir(parents=True, exist_ok=True)
    img_dir.mkdir(parents=True, exist_ok=True)

    failures: list[dict[str, str]] = []
    artifacts: list[dict[str, str]] = []

    for index, card in enumerate(schema["cards"]):
        seq = f"{index:02d}"
        ctype = card.get("type", "page")
        base_name = f"card-{seq}-{ctype}"
        html_path = html_dir / f"{base_name}.html"
        png_path = img_dir / f"{base_name}.png"

        payload = build_card_payload(schema, card, index, config)
        html_path.write_text(render_card_html(template_html, config, payload), encoding="utf-8")

        try:
            render_html_to_png(html_path, png_path, width=width, height=height)
            artifacts.append({"html": str(html_path), "image": str(png_path), "type": ctype})
        except Exception as exc:  # noqa: BLE001
            failures.append({"card": base_name, "error": str(exc)})

    report_path = output_dir / "report.json"
    write_report(
        report_path,
        {
            "input": str(input_path),
            "style": style,
            "card_count": len(schema["cards"]),
            "success_count": len(artifacts),
            "failure_count": len(failures),
            "artifacts": artifacts,
            "failures": failures,
        },
    )
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build image-card-ppt HTML and PNG artifacts.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build", help="Render cards from schema JSON.")
    build.add_argument("--input", required=True, type=Path, help="Path to schema JSON.")
    build.add_argument("--output-dir", required=True, type=Path, help="Output directory.")
    build.add_argument("--style", default=None, help="Override style name.")
    build.add_argument("--brand-name", default=None, help="Override brand name.")
    build.add_argument("--brand-subtitle", default=None, help="Override brand subtitle.")

    args = parser.parse_args(argv)
    if args.command == "build":
        return build_pipeline(
            input_path=args.input,
            output_dir=args.output_dir,
            style_override=args.style,
            brand_name=args.brand_name,
            brand_subtitle=args.brand_subtitle,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

