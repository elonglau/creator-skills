from pathlib import Path

import image_card_ppt.render as render_mod


def test_render_html_to_png_calls_playwright_page_api(monkeypatch, tmp_path):
    calls = {}

    class FakePage:
        def goto(self, url, wait_until, timeout):
            calls["goto"] = (url, wait_until, timeout)

        def wait_for_timeout(self, ms):
            calls["wait"] = ms

        def screenshot(self, path):
            calls["screenshot"] = path
            Path(path).write_bytes(b"png")

    class FakeBrowser:
        def new_page(self, viewport):
            calls["viewport"] = viewport
            return FakePage()

        def close(self):
            calls["closed"] = True

    class FakeChromium:
        def launch(self):
            calls["launch"] = True
            return FakeBrowser()

    class FakePlaywright:
        chromium = FakeChromium()

    class FakeContext:
        def __enter__(self):
            return FakePlaywright()

        def __exit__(self, exc_type, exc, tb):
            return False

    monkeypatch.setattr(render_mod, "sync_playwright", lambda: FakeContext())

    html = tmp_path / "card.html"
    png = tmp_path / "card.png"
    html.write_text("<html></html>", encoding="utf-8")
    render_mod.render_html_to_png(html, png, width=1080, height=1440)

    assert calls["launch"] is True
    assert calls["viewport"] == {"width": 1080, "height": 1440}
    assert calls["goto"][1] == "domcontentloaded"
    assert calls["goto"][2] == 15_000
    assert calls["screenshot"] == str(png)
    assert png.exists()


def test_render_html_to_png_falls_back_to_x64_headless_shell(monkeypatch, tmp_path):
    calls = {"launches": []}

    class PlaywrightLikeError(Exception):
        pass

    class FakePage:
        def goto(self, url, wait_until, timeout):
            return None

        def wait_for_timeout(self, ms):
            return None

        def screenshot(self, path):
            Path(path).write_bytes(b"png")

    class FakeBrowser:
        def new_page(self, viewport):
            return FakePage()

        def close(self):
            return None

    class FakeChromium:
        def launch(self, executable_path=None):
            calls["launches"].append(executable_path)
            if executable_path is None:
                raise PlaywrightLikeError("Executable doesn't exist")
            return FakeBrowser()

    class FakePlaywright:
        chromium = FakeChromium()

    class FakeContext:
        def __enter__(self):
            return FakePlaywright()

        def __exit__(self, exc_type, exc, tb):
            return False

    monkeypatch.setattr(render_mod, "sync_playwright", lambda: FakeContext())
    monkeypatch.setattr(render_mod, "_detect_x64_headless_shell", lambda: "/tmp/chrome-headless-shell")

    html = tmp_path / "card.html"
    png = tmp_path / "card.png"
    html.write_text("<html></html>", encoding="utf-8")

    render_mod.render_html_to_png(html, png, width=1080, height=1440)

    assert calls["launches"] == [None, "/tmp/chrome-headless-shell"]
    assert png.exists()

