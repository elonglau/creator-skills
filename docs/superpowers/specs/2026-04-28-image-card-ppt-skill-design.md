# image-card-ppt Skill Design

Date: 2026-04-28

## Goal

Create the first version of `skills/image-card-ppt/SKILL.md` for an AI-agent-facing skill that turns raw Xiaohongshu content drafts into structured information card outputs.

The MVP documentation should make the intended workflow clear before implementation exists. It should define what the agent should do, what inputs it should expect, what outputs the future scripts will produce, and what boundaries the MVP will keep.

## Audience

The primary reader is an AI coding/content agent. The document should not be written as a generic human README. It should tell the agent when to use the skill and how to reason through the task.

Human-facing usage can be added later after scripts and examples exist.

## Proposed SKILL.md Structure

The initial `SKILL.md` should include:

1. Frontmatter with `name: image-card-ppt` and a concise description.
2. Purpose and activation criteria.
3. Expected inputs.
4. MVP workflow.
5. Draft fixed schema for card content.
6. Template style configuration concept.
7. Expected output artifacts.
8. Quality checks.
9. MVP non-goals.
10. Future extension points.

## MVP Workflow

The agent workflow should be described as:

1. Accept raw manuscript text from the user.
2. Extract or rewrite the manuscript into a fixed intermediate schema.
3. Split the schema into a sequence of information cards.
4. Choose a template style configuration, such as design style or technology style.
5. Render each card through an HTML template.
6. Use a local Python script with Playwright to convert HTML cards into images.
7. Return generated image paths and summarize the card sequence.

The first `SKILL.md` only documents this flow. It does not need to include working scripts yet.

## Draft Schema

The document should define a practical draft schema so future implementation has a target:

- `title`: main topic or cover title.
- `subtitle`: optional supporting line.
- `audience`: intended reader.
- `tone`: writing and visual tone.
- `cards`: ordered list of card objects.
- `cards[].type`: card role, such as `cover`, `point`, `steps`, `quote`, or `summary`.
- `cards[].headline`: card title.
- `cards[].body`: short content blocks for the card.
- `cards[].visual_hint`: optional guidance for layout, image choice, or emphasis.
- `metadata`: source text summary, template name, and generation notes.

This schema can change during implementation, but the MVP skill should establish it as the default contract.

## Template Configuration

The MVP should describe templates as named configurations rather than hardcoded one-off HTML files.

Each template style should eventually control:

- Canvas size.
- Typography.
- Colors.
- Spacing.
- Decorative elements.
- Card type layout rules.

The initial documented examples should include `design` and `tech` styles because those are already part of the user goal.

## Outputs

The future implementation should produce:

- A normalized schema JSON file.
- One HTML file per card, or an equivalent renderable HTML artifact.
- One image per card rendered through Playwright.
- A short generation report listing card count, template style, and output paths.

## Error Handling

The skill should instruct the agent to stop and ask for clarification when the raw draft is too short, lacks a coherent topic, or conflicts with the requested card style.

The skill should avoid silent fallback behavior. If rendering fails in future scripts, the agent should identify the root cause from the script or browser error before changing templates or schema.

## Testing Expectations

The MVP skill document should state that future implementation needs minimal tests for:

- Schema generation from a sample manuscript.
- Template configuration loading.
- HTML rendering output existence.
- Playwright screenshot generation.

## Non-Goals

The MVP should not promise:

- Multi-platform publishing.
- Automated Xiaohongshu upload.
- AI image generation.
- Complex design systems.
- A GUI editor.
- Production-grade template marketplace behavior.

These can be future work after the local generation loop is stable.

## Acceptance Criteria

The initial `SKILL.md` is acceptable when:

- It clearly targets AI-agent execution.
- It documents the raw-text to schema to HTML to image flow.
- It names the expected Python and Playwright rendering direction without requiring implementation.
- It includes the draft schema and template configuration concept.
- It keeps the MVP scope narrow and avoids promising future features as current behavior.
