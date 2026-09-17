# Add and edit content

## Edit an existing page

Open any `.md` file under `docs/`. A typical page starts with one top-level heading, followed by short sections:

```markdown
# Analysis summary

One or two sentences that explain the purpose of this page.

## Key finding

Write the supporting evidence here.

## Recommendation

Explain the action and who owns it.
```

Save the file. If the preview server is running, the browser reloads it automatically.

## Add a new page

1. Create a Markdown file, for example `docs/findings/customer-trends.md`.
2. Add the page to `nav:` in `mkdocs.yml`.
3. Link to it from related pages with a relative link.
4. Run `uv run mkdocs build --strict` to catch mistakes.

Add this navigation entry:

```yaml
nav:
  - Home: index.md
  - Findings:
      - Customer trends: findings/customer-trends.md
```

Link to it from another page:

```markdown
Read the [customer trends](../findings/customer-trends.md).
```

## Add an image

Copy the image to `docs/assets/`, then use:

```markdown
![Short description of the image](../assets/chart.png)
```

The description helps screen-reader users and appears if the image cannot load. Use lowercase file names with hyphens, such as `quarterly-revenue.png`.

## Keep pages useful

A strong documentation page tells the reader:

1. what this page is about;
2. what they need to know or do;
3. the evidence or example they need; and
4. where to go next.

For project claims and decisions, trace the detail back to the [shared source brief](../reference/project-brief.md) or another named source.

