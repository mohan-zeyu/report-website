# Getting started

This project uses [MkDocs](https://www.mkdocs.org/) with the [Material theme](https://squidfunk.github.io/mkdocs-material/). Content is plain Markdown, so you can write it in any text editor.

## Project layout

```text
report_website/
├── docs/                       # All pages and images
│   ├── assets/
│   ├── getting-started/
│   ├── guide/
│   ├── reference/
│   ├── stylesheets/
│   └── index.md                # Home page
├── mkdocs.yml                  # Site name, theme, menu, features
├── pyproject.toml              # Python dependencies
└── README.md                   # Quick commands for maintainers
```

## What to edit

- Edit page content in `docs/**/*.md`.
- Add or reorder menu items under `nav:` in `mkdocs.yml`.
- Put images and downloadable files in `docs/assets/`.
- Adjust colors and small visual details in `docs/stylesheets/extra.css`.

Continue with [Run the site](run-the-site.md) to start the live preview.

