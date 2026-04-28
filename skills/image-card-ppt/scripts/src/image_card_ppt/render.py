from pathlib import Path

from playwright.sync_api import sync_playwright


def render_html_to_png(
    html_path: Path, output_png: Path, width: int, height: int, page_wait_ms: int = 120
) -> None:
    output_png.parent.mkdir(parents=True, exist_ok=True)
    html_url = html_path.resolve().as_uri()
    with sync_playwright() as playwright:
        browser = _launch_chromium_with_fallback(playwright)
        page = browser.new_page(viewport={"width": width, "height": height})
        page.goto(html_url, wait_until="domcontentloaded", timeout=15_000)
        page.wait_for_timeout(page_wait_ms)
        page.screenshot(path=str(output_png))
        browser.close()


def _launch_chromium_with_fallback(playwright):
    try:
        return playwright.chromium.launch()
    except Exception as exc:  # noqa: BLE001
        if "Executable doesn't exist" not in str(exc):
            raise
        x64_path = _detect_x64_headless_shell()
        if not x64_path:
            raise
        return playwright.chromium.launch(executable_path=x64_path)


def _detect_x64_headless_shell() -> str | None:
    base = Path("/var/folders")
    if not base.exists():
        return None
    candidates = list(base.glob("**/playwright/chromium_headless_shell-*/chrome-headless-shell-mac-x64/chrome-headless-shell"))
    if not candidates:
        return None
    return str(candidates[0])

