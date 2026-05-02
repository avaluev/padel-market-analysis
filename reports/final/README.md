# Padel AI Coach — Reports bundle

Two static HTML pages plus an index, designed mobile-first and ready to deploy on GitHub Pages, Vercel, Netlify, or any static host.

## Files

| File | Purpose |
|---|---|
| `index.html` | Landing page that links to the brief and evidence map. |
| `padel-ai-coach-research.html` | Customer-facing strategic brief (18 sections, ~110 KB). |
| `evidence-map.html` | Companion document tracing every claim back to source files. |
| `404.html` | 404 fallback. |
| `robots.txt` | Allows all crawlers. |

## Mobile-first design

- Fluid typography via `clamp()` — no breakpoints needed for type.
- **Mobile (<720px)**: floating action button bottom-right opens a bottom-sheet drawer (driven by `<details>` so it works without JavaScript).
- **Tablet / desktop (≥720px)**: sticky always-visible side rail, never scrolls out of view.
- **Touch targets**: 44 px minimum on standalone controls per Apple HIG and WCAG 2.5.5; inline prose links exempt.
- **Tables**: horizontal scroll with sticky thead on overflow.
- **Reduced motion**, **dark mode**, **iPhone safe-area insets**, **print stylesheet**, **`@supports`-free CSS** for maximum compatibility.

## Deployment

### GitHub Pages (zero-config)
Push to `main`. The workflow at `.github/workflows/deploy-pages.yml` will publish `reports/final/` automatically.

### Vercel
The `vercel.json` at the repo root sets `outputDirectory: reports/final`, security headers, and pretty rewrites:
- `/brief` → strategic brief
- `/evidence` → evidence map

```bash
vercel --prod
```

### Netlify / Cloudflare Pages
Point the build to `reports/final` as the publish directory. No build command needed.

## Auditing

```bash
npm install
npx playwright install chromium

# Capture screenshots and metrics across iPhone 13 / Pixel 7 / iPhone SE / iPad Mini / Desktop 1280
npm run audit:baseline   # snapshot before changes
# … make changes …
npm run audit:post       # snapshot after changes
npm run audit:diff       # writes evidence/_mobile_audit/DIFF.md
```

The harness captures: TTFB, FCP, LCP, CLS, transfer bytes, document height, horizontal overflow, console errors, request failures, viewport screenshots, full-page screenshots, and an inline-vs-standalone tap-target audit.
