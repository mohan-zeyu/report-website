# Organize navigation

The `nav:` block in `mkdocs.yml` controls the menu. Indentation defines the hierarchy.

```yaml
nav:
  - Home: index.md
  - Findings:
      - Overview: findings/index.md
      - Customer trends: findings/customer-trends.md
  - Recommendations:
      - Overview: recommendations/index.md
```

## Rules to remember

- Use spaces for indentation; YAML does not accept tabs.
- Every file path is relative to `docs/`.
- Keep labels short because they appear in the sidebar.
- Put an `index.md` page at the start of a large section to orient readers.
- A Markdown file can exist without appearing in `nav:`, but readers must have a link to find it.

## Rename or move a page

When you rename a Markdown file, update both `mkdocs.yml` and any links pointing to it. Then run the strict build:

```bash
uv run mkdocs build --strict
```

MkDocs reports missing pages and invalid navigation entries in the terminal.

