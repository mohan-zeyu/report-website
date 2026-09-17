# Run the site

The project uses [uv](https://docs.astral.sh/uv/) to keep its Python tools isolated from the rest of your computer.

## Start a live preview

From this folder, run:

```bash
uv sync
uv run mkdocs serve
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000). Leave the command running while you edit. Most saved changes appear automatically.

Press ++ctrl+c++ in the terminal to stop the server.

## Check the production build

Before publishing, run:

```bash
uv run mkdocs build --strict
```

This validates links, navigation, and configuration. The generated website is written to `site/`.

!!! note
    You normally do not edit anything inside `site/`. MkDocs recreates that folder every time it builds.

