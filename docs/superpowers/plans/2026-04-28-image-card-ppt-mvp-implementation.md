# Image Card PPT MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a complete local MVP pipeline for `image-card-ppt`: load schema, render per-card HTML with template data, capture PNG images using Playwright, and emit a generation report.

**Architecture:** Implement a small Python package under `skills/image-card-ppt/scripts/src/image_card_ppt` with clear boundaries: schema validation, template loading + data shaping, screenshot rendering, and report writing. Expose one CLI command (`build`) that coordinates the flow and exits non-zero on render failures.

**Tech Stack:** Python 3 standard library, `playwright`, `pytest`

---

### Task 1: Project scaffold and import wiring

**Files:**
- Create: `skills/image-card-ppt/scripts/src/image_card_ppt/__init__.py`
- Create: `skills/image-card-ppt/scripts/src/image_card_ppt/paths.py`
- Create: `skills/image-card-ppt/scripts/tests/conftest.py`
- Create: `skills/image-card-ppt/scripts/requirements.txt`

- [ ] **Step 1: Write the failing test**

```python
from image_card_ppt.paths import templates_dir

def test_templates_dir_exists():
    assert templates_dir().exists()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd skills/image-card-ppt/scripts && pytest tests -k templates_dir_exists -v`
Expected: FAIL with `ModuleNotFoundError` or missing function

- [ ] **Step 3: Write minimal implementation**

```python
from pathlib import Path

def templates_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "templates"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd skills/image-card-ppt/scripts && pytest tests -k templates_dir_exists -v`
Expected: PASS

### Task 2: Schema validation and load

**Files:**
- Create: `skills/image-card-ppt/scripts/src/image_card_ppt/schema.py`
- Create: `skills/image-card-ppt/scripts/tests/test_schema.py`

- [ ] **Step 1: Write the failing test**

```python
def test_load_schema_requires_title_cards_metadata(tmp_path):
    # write invalid schema missing title
    ...
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd skills/image-card-ppt/scripts && pytest tests/test_schema.py -v`
Expected: FAIL because loader does not exist

- [ ] **Step 3: Write minimal implementation**

```python
def load_schema(path: Path) -> dict:
    # parse json and raise ValueError when required fields missing
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd skills/image-card-ppt/scripts && pytest tests/test_schema.py -v`
Expected: PASS

### Task 3: Template loading and card HTML rendering

**Files:**
- Create: `skills/image-card-ppt/scripts/src/image_card_ppt/template.py`
- Create: `skills/image-card-ppt/scripts/tests/test_template.py`

- [ ] **Step 1: Write the failing test**

```python
def test_render_card_html_injects_config_and_card_data():
    ...
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd skills/image-card-ppt/scripts && pytest tests/test_template.py -v`
Expected: FAIL because template module does not exist

- [ ] **Step 3: Write minimal implementation**

```python
def render_card_html(template_html: str, config: dict, card_payload: dict) -> str:
    # prepend script with window.TEMPLATE_CONFIG and window.CARD_DATA
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd skills/image-card-ppt/scripts && pytest tests/test_template.py -v`
Expected: PASS

### Task 4: Playwright rendering module

**Files:**
- Create: `skills/image-card-ppt/scripts/src/image_card_ppt/render.py`
- Create: `skills/image-card-ppt/scripts/tests/test_render.py`

- [ ] **Step 1: Write the failing test**

```python
def test_render_card_png_calls_playwright_page_api(monkeypatch, tmp_path):
    ...
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd skills/image-card-ppt/scripts && pytest tests/test_render.py -v`
Expected: FAIL because render function does not exist

- [ ] **Step 3: Write minimal implementation**

```python
def render_html_to_png(html_path: Path, output_png: Path, width: int, height: int) -> None:
    # open chromium, set viewport, goto file://, screenshot
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd skills/image-card-ppt/scripts && pytest tests/test_render.py -v`
Expected: PASS

### Task 5: Report generation and CLI pipeline

**Files:**
- Create: `skills/image-card-ppt/scripts/src/image_card_ppt/report.py`
- Create: `skills/image-card-ppt/scripts/src/image_card_ppt/cli.py`
- Create: `skills/image-card-ppt/scripts/tests/test_cli.py`

- [ ] **Step 1: Write the failing test**

```python
def test_build_pipeline_writes_html_png_and_report(tmp_path, monkeypatch):
    ...
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd skills/image-card-ppt/scripts && pytest tests/test_cli.py -v`
Expected: FAIL because build pipeline not implemented

- [ ] **Step 3: Write minimal implementation**

```python
def main(argv=None) -> int:
    # parse args, run build, return 0 on success else non-zero
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd skills/image-card-ppt/scripts && pytest tests/test_cli.py -v`
Expected: PASS

### Task 6: End-to-end smoke verification

**Files:**
- Modify: `skills/image-card-ppt/scripts/tests/test_cli.py`

- [ ] **Step 1: Add a smoke scenario against `outputs/ai-video-tech/schema.json`**

```python
def test_build_smoke_from_repo_schema(...):
    ...
```

- [ ] **Step 2: Run targeted tests**

Run: `cd skills/image-card-ppt/scripts && pytest tests -v`
Expected: all tests pass

