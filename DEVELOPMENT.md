# Development

How to work on the [aidan.my](https://aidan.my) site locally.

## Prerequisites

- Python 3 (only needed for the local server and the OG image script)
- A modern browser

No `npm install`, no toolchain to set up.

## Run the site locally

From the repo root:

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

Any static server works (`npx serve`, `caddy file-server`, etc.) — pick whichever is convenient. The site has no API and no environment variables.

## Deploy

The site is hosted on GitHub Pages and serves from the `main` branch at the root. Pushing to `main` deploys.

## Common tasks

### Add a new page

1. Create the directory and file, e.g. `news/index.html`.
2. Set the root element correctly — `data-base` must match the page's depth from the repo root:
   ```html
   <html lang="en" data-base="../" data-page="news">
   ```
3. Copy the head block from an existing page at the same depth. Update:
   - `<title>` and `<meta name="description">`
   - All Open Graph and Twitter Card tags (title, description, `og:url`, image paths)
   - The `canonical` link
   - The JSON-LD `BreadcrumbList`
4. Body must include the mount points and script tags:
   ```html
   <body>
     <div id="nav-mount"></div>
     <!-- page content -->
     <div id="footer-mount"></div>
     <script src="../assets/js/partials.js"></script>
     <script src="../assets/js/main.js"></script>
   </body>
   ```
5. If the page belongs in primary navigation, add a link in [assets/js/partials.js](assets/js/partials.js) inside the `navHTML` template.
6. Add the page URL to [sitemap.xml](sitemap.xml).
7. Generate or add an OG image (see below).

### Add a venture

Edit [ventures/index.html](ventures/index.html) and append a tile in the right section (Technology, Education, or Other ventures):

```html
<article class="venture-tile reveal">
  <div class="tile-image contain"><img src="../assets/images/ventures/your-logo.png" alt="Venture Name" /></div>
  <h4>Venture Name</h4>
  <p>One-line description.</p>
</article>
```

Drop the image into [assets/images/ventures/](assets/images/ventures/). Use `class="tile-image contain"` for logos that should be letterboxed; use `class="tile-image"` for full-bleed photographs.

### Update nav or footer

Both are in [assets/js/partials.js](assets/js/partials.js) — `navHTML` and `footerHTML` template literals. Edits propagate to every page on next load. Do not paste nav/footer markup into individual pages.

### Update contact information

Phone, email, and address appear in three places — keep them in sync:

1. [assets/js/partials.js](assets/js/partials.js) — footer block.
2. [contact/index.html](contact/index.html) — visible page content.
3. [index.html](index.html) — JSON-LD `Organization` schema.

### Regenerate Open Graph images

```bash
python3 scripts/build-og-images.py
```

Outputs land in [assets/images/og/](assets/images/og/) at 1200×630. Re-run whenever a page's title or hero changes, and commit the regenerated PNGs.

### Update the sitemap

[sitemap.xml](sitemap.xml) is hand-maintained. When adding or removing a page, add or remove the corresponding `<url>` block. Use absolute `https://aidan.my/` URLs.

## Style and conventions

- **Two-space indent** in HTML and JS, matching what's already in the repo.
- **Inline SVG icons** with `class="ti"` (target icon). Do not import an icon font.
- **Brand color:** `#E75B2A`. Brand gradient: `var(--grad-sunset)`.
- **Reveal animations:** add `class="reveal"` (optionally `d-1`, `d-2`, `d-3` for staggered delays) to any element you want to fade up on scroll.
- **Relative asset paths only.** Never start with `/assets/...`.
- **Clean URLs.** Internal links and canonical URLs use the trailing-slash directory form — `ventures/`, `../contact/`, `https://aidan.my/group/`. Never link to `index.html` directly.

## Troubleshooting

- **Nav or footer doesn't show up / images broken in nav.** Check `data-base` on `<html>` — it must match the page's depth.
- **Active nav link not highlighted.** Check `data-page` on `<html>` matches the `data-key` used in [partials.js](assets/js/partials.js).
- **Page missing from Google.** Confirm it's in [sitemap.xml](sitemap.xml) and that [robots.txt](robots.txt) isn't blocking it.
- **OG preview is stale.** Re-run `scripts/build-og-images.py` and clear the social platform's cache (Facebook Sharing Debugger, Twitter Card Validator).
