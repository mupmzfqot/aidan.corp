# Agent Guide — aidan.my

Context and conventions for AI coding agents working on this repository. For company-facing information see [README.md](README.md).

## What this repo is

The static marketing site for [aidan.my](https://aidan.my), served via GitHub Pages (custom domain in [CNAME](CNAME)).

- **No build step.** Plain HTML, CSS, and vanilla JavaScript.
- **No package manager, no framework, no bundler.** Do not introduce one without explicit instruction.
- **Multi-page** site with a shared nav and footer injected at runtime by JS.

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full structural breakdown and [DEVELOPMENT.md](DEVELOPMENT.md) for workflows.

## Quick reference

| Task | File / Command |
| --- | --- |
| Serve locally | `python3 -m http.server 8000` |
| Edit shared nav / footer | [assets/js/partials.js](assets/js/partials.js) |
| Edit global styles | [assets/css/styles.css](assets/css/styles.css) |
| Edit scroll-reveal styles | [assets/css/reveal.css](assets/css/reveal.css) |
| Edit interactive JS | [assets/js/main.js](assets/js/main.js) |
| Regenerate OG images | `python3 scripts/build-og-images.py` |
| Update site index | [sitemap.xml](sitemap.xml) |

## Conventions

- **Clean URLs — never link to `index.html`.** Internal links and canonical URLs use the trailing-slash directory form: `ventures/`, `../contact/`, `https://aidan.my/group/`. Never `ventures/index.html` or `https://aidan.my/group/index.html`. The `index.html` filename is an implementation detail of static hosting and must not appear in any user-visible URL.
- **Paths via `data-base`.** Every page sets `<html data-base="..." data-page="...">`. `partials.js` reads `data-base` to resolve nav/footer asset URLs. Root pages use `data-base=""`; pages one level deep use `data-base="../"`; two levels deep use `data-base="../../"`. Get this right or the nav/footer will 404.
- **Per-page metadata is inline.** Each `index.html` has its own `<title>`, `description`, Open Graph, Twitter Card, and JSON-LD blocks. Update them when page content changes — do not centralize them.
- **Theme color:** `#E75B2A` (Aidan orange). Brand gradient is `var(--grad-sunset)`.
- **Fonts:** Plus Jakarta Sans (body) and JetBrains Mono (eyebrow / monospace accents) via Google Fonts.
- **Icons** are inline SVGs with class `ti`. Do not add an icon font or external icon library.
- **Reveal-on-scroll** uses the `.reveal` class with optional `.d-1`, `.d-2`, `.d-3` delays. Handled by [main.js](assets/js/main.js).

## When making changes

- **Adding a new page:** see the "Adding a page" section in [DEVELOPMENT.md](DEVELOPMENT.md). Always update [sitemap.xml](sitemap.xml) and add the page to nav links in [partials.js](assets/js/partials.js) if it belongs in primary navigation.
- **Adding a venture:** edit the relevant section in [ventures/index.html](ventures/index.html). Image goes in `assets/images/ventures/` (use `.contain` on the tile if the logo needs letterboxing rather than cropping).
- **Editing nav or footer:** edit [partials.js](assets/js/partials.js) only. Do not paste nav/footer markup into individual pages.
- **Touching SEO metadata:** keep the JSON-LD `@id` URLs, canonical URLs, and `og:url` consistent with the page's deployed URL on `aidan.my`.

## What not to do

- Do not add a build step, framework, or dependency manager.
- Do not duplicate nav/footer markup into pages — it must stay in [partials.js](assets/js/partials.js).
- Do not commit generated OG images without re-running the script for any page whose title/description changed.
- Do not hardcode absolute paths starting with `/assets/...` in pages — use relative paths so subpaths work both locally and on GitHub Pages.
- Do not link to `index.html` in any `href` or canonical URL — always use the trailing-slash directory form (e.g. `ventures/`, not `ventures/index.html`).
- Do not add tracking, analytics, or third-party scripts without explicit instruction.
