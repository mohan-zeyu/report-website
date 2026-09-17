# Report Wiki

A ready-to-edit documentation site built with Material for MkDocs. Its layout is modeled on the [mihomo docs](https://wiki.metacubex.one/en/) and its project reference points to the [shared ChatGPT brief](https://chatgpt.com/share/6aab766a-b104-83ec-b3d3-c22c2887cf3c).

## Preview locally

```bash
uv sync
uv run mkdocs serve
```

Open <http://127.0.0.1:8000>.

## Add content

1. Create or edit a `.md` file in `docs/`.
2. Add new pages to the `nav:` section of `mkdocs.yml`.
3. Put images in `docs/assets/`.
4. Validate with `uv run mkdocs build --strict`.

The rendered writing guide is available under **Writing guide → Add and edit content** in the site navigation.

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
