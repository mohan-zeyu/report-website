# Report Wiki

A ready-to-edit documentation site built with Material for MkDocs. Its layout is modeled on the [mihomo docs](https://wiki.metacubex.one/en/) and its project reference points to the [shared ChatGPT brief](https://chatgpt.com/share/6aab766a-b104-83ec-b3d3-c22c2887cf3c).

## Preview locally

```bash
uv sync
uv run mkdocs serve
```

Open <http://127.0.0.1:8000>.

## Add content

1. Create or edit a `.md` file in `docs/`. Put handwritten code articles in `docs/handwritten-code/` and start each one with its own `# Page title`.
2. Add new pages under the `Handwritten Code` section of `nav:` in `mkdocs.yml`. The section name labels the top tab; the Markdown heading labels the article.
3. Put images in `docs/assets/`.
4. Validate with `uv run mkdocs build --strict`.

Paths in `nav:` are relative to `docs/`. The root URL uses `docs/index.md` as the home page. If using `npm run sync:content -- /path/to/article.md`, keep a `#` heading in the source article.

You can also ask Codex to add a new handwritten code article, rename a navigation tab, reorder pages, or check a broken link. Point it to the relevant Markdown file when the content is outside this repository.

## Deploy to Cloudflare Workers

This repository is configured for Workers Static Assets. Install Wrangler and test the Workers runtime locally:

```bash
npm install
npm run preview:worker
```

For a manual release after authorizing Wrangler:

```bash
npx wrangler login
npm run deploy
```

For automatic releases, connect the repository under **Cloudflare → Workers & Pages → Create application → Import a repository** and use:

```text
Build command: pip install -r requirements.txt && mkdocs build --strict
Deploy command: npx wrangler deploy
Non-production deploy command: npx wrangler versions upload
```

The full setup and troubleshooting guide is under **Deployment → Cloudflare Workers** in the site navigation.
