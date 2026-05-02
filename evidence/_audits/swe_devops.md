# SWE / DevOps audit — padel-research-os

Date: 2026-05-02
Scope: static HTML report bundle + Playwright audit harness + deployment scaffolding.

---

## SWE — code quality, correctness, semantics

**VERDICT: pass-with-caveats.** Code is idiomatic ES modules + vanilla DOM, semantics are mostly clean, one real DOM bug and one regex hazard.

### Findings

1. **Stale-closure bug in nav script — `reports/final/padel-ai-coach-research.html:2000` and `evidence-map.html:568`.** `document.querySelector('aside.sidenav, details.sidenav')` is called once at script start. The `<details>` element is the actual node; on viewports `<720px` the script does `nav.removeAttribute('open')` from inside the click handler, but the IntersectionObserver continues observing through the same `nav` reference even when the drawer is closed off-screen. Not a crash, but `current` stays mutated when the observer fires while the sheet is closed; hovering across nav links can leave two `aria-current="true"` because there is no full-list reset before re-tagging (line 2018 only clears `current`, not other accidentally-tagged links).

2. **Duplicate inline IIFE across the two reports.** `padel-ai-coach-research.html:1996-2033` and `evidence-map.html:566-593` are byte-for-byte the same logic. Two divergent copies will drift; the file is a static asset, but a shared `nav.js` referenced by both reports would remove the duplication while still being hostable on Pages/Vercel.

3. **`postprocess_html.mjs:18-29` table-wrap regex is fragile.** The non-greedy `<table\b[\s\S]*?<\/table>` matcher is fine for the current well-formed input, but a `<table>` whose attribute string contains the literal `</table>` inside a JS comment block or a CDATA-styled script will mis-anchor; the lookbehind that detects existing wraps only inspects 200 bytes before the match (`offset - 200`), so a `<div class="table-wrap" ...>` separated by a long whitespace block (e.g. an indented `<!-- comment -->`) will be missed and the table will be double-wrapped on a second run. The script labels itself "idempotent"; in practice it is conditionally idempotent.

4. **`audit_mobile.mjs:144-154` event-listener leak.** Listeners (`console`, `pageerror`, `requestfailed`) are attached to each `page` inside `runOnce` but never removed; `runOnce` is called once per `page` so this does not leak across iterations, but if the harness is ever refactored to reuse a page across pages/devices the closures will keep pushing into stale `consoleErrors` arrays. Add `page.off(...)` or use `page.once` for the navigation phase.

5. **HTML semantics are good.** Single `<h1>` per document, ordered `<h2>` flow, `<main id="main">`, skip-link, `aria-label` on sidenav, `role="region" tabindex="0" aria-label="Data table"` on every table wrap, `prefers-reduced-motion` honored. One nit: evidence-map has only 1 `<h3>` against 12 `<h2>`s — fine but slightly flat for a "map" doc.

### Recommendations

- Patch the IntersectionObserver handler to clear `aria-current` on every link before re-tagging (single-pass reset), then extract to `reports/final/nav.js` so both pages share one file.
- Tighten `postprocess_html.mjs`: parse with a forgiving HTML parser (e.g. `parse5`) instead of regex, or short-circuit when the file already contains the wrap marker. Add an `--idempotent-check` exit-non-zero mode for CI.
- Add an integration-style assertion in `audit_diff.mjs` that fails the build when any device shows `horizontalOverflow === true` or `tooSmallStandaloneTaps > 0` — currently the diff only renders Markdown.

---

## DevOps — deployment readiness, security, ops

**VERDICT: pass-with-caveats.** Headers, concurrency, and cache rules are sane; .gitignore and repo size are the real risks.

### Findings

1. **`.gitignore` is incomplete vs. actual artifacts on disk.** The `_mobile_audit` directory is **125 MB** (`baseline 59M + post 60M + scroll 5M`). The current rules at `.gitignore:5-12` only ignore `shot.png` per device. There are **20 `viewport.png` files** still tracked, plus `summary.json`, `metrics.json`, and DIFF.md. Running `git add -A` here will commit ~60 MB of binary screenshots. Add `evidence/_mobile_audit/**/viewport.png`, `evidence/_mobile_audit/**/metrics.json`, and consider ignoring the entire `evidence/_mobile_audit/{baseline,post}/` tree except `summary.json` and `DIFF.md`.

2. **Conflicting deploy targets, no single source of truth.** `vercel.json` (root) sets `outputDirectory: "reports/final"` with rewrites `/brief` and `/evidence`, while `.github/workflows/deploy-pages.yml` ships the same `reports/final` to GitHub Pages. The two hosts have different URL semantics — Pages does not honor Vercel rewrites, so `/brief` and `/evidence` will 404 on Pages. Either pick one host or document that the rewrites are Vercel-only and ship a Pages-side `index.html` that links to the `.html` files (already present, but the `cleanUrls: true` Vercel flag means `/padel-ai-coach-research` works on Vercel and not on Pages).

3. **Security headers are good but not bulletproof.** `vercel.json:11-17` sets HSTS, X-Content-Type-Options, Referrer-Policy, Permissions-Policy. Missing: `Content-Security-Policy` (the inline `<script>` and `<style>` blocks would need at minimum `script-src 'self' 'unsafe-inline'`; better, hash-based). `Strict-Transport-Security` lacks `preload` — fine if not submitting to the preload list, intentional choice. No `X-Frame-Options` / `frame-ancestors` — the report could be iframed by anyone. GitHub Pages cannot set custom headers at all, so on Pages none of these apply.

4. **`scripts/verify_links.sh:7` uses `set -uo pipefail` (no `-e`).** The `while` loop relies on `fail` counter to surface failures, which is intentional and correct for a multi-URL check (you want all results before exiting). However, the `curl … || echo "000 -"` fallback at line 77 silently masks DNS errors as transient retries; a permanently-dead host shows as `000` three times then `FAIL  000` — readable, but consumers reading the log have no `errno`. Fine, but worth a comment.

5. **No healthcheck / smoke story.** Workflow uploads artifact and calls `deploy-pages@v4` — no post-deploy curl of the deployed URL. If the artifact deploys but `index.html` is malformed, you find out from a human visiting the site. The repo also has a `404.html` (good), but Vercel won't serve it as a fallback unless you add `"errorPage": "404.html"` or a catch-all rewrite; current `vercel.json` has neither.

### Recommendations

- Tighten `.gitignore` to ignore the whole `evidence/_mobile_audit/{baseline,post}/` tree except the JSON summary, OR move screenshots to `evidence/_mobile_audit/.local/` and ignore that path entirely. Also confirm none of the 125 MB has already been committed (run `git log -- evidence/_mobile_audit/` after the repo is initialized).
- Add a `Content-Security-Policy` header to `vercel.json` (`default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'`) and a `X-Frame-Options: DENY` (or `frame-ancestors 'none'`). Add a Pages-side `_headers`/meta-equiv equivalent if Pages remains a target.
- Add a post-deploy smoke step to `deploy-pages.yml`: `curl -fsSL "${{ steps.deployment.outputs.page_url }}" | grep -q "Padel AI Coach"` — fails the workflow if the index does not render the expected `<h1>`.
