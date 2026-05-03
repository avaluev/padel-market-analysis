# Changelog

All notable changes to this repository.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project follows rolling releases on `main`.

## [Unreleased]

### Added

- New unified content + SEO quality gate at `scripts/check_quality.py` with 14 distinct checks (H1 uniqueness, run-ID leak, candidate framing, jargon, marketing claims, link syntax, internal IDs, meta tags, JSON-LD, image attributes, internal links, nav consistency, SEO assets).
- New SEO asset generator at `scripts/build_seo_assets.py` producing `robots.txt`, `llms.txt`, `llms-full.txt`, `sitemap.xml`, `feed.xml`, `humans.txt`, `manifest.webmanifest`, `favicon.svg`, `.well-known/security.txt`.
- New idempotent content sanitiser at `scripts/sanitise_pages.py` for top-level static pages.
- New unified page builder at `scripts/build_pages.mjs` — flat output, AI-search optimised template with JSON-LD, OG, Twitter Card, mobile-first hamburger nav.
- Skills under `~/.claude/skills/` for `geo-optimization`, `aio-optimization`, `aeo-optimization`, `llmo-optimization`, `seo-structured-data`.
- Universal rules under `~/.claude/rules/common/` for `ai-search-optimization` and `content-quality-gates`.
- Test suite under `tests/` (51 tests, ~72% coverage on the new modules).
- CI workflow at `.github/workflows/quality-gates.yml` blocking merge to `main` on lint / typecheck / test / quality / link-verify / secret-scan failures.
- `pyproject.toml`, `Makefile`, `.pre-commit-config.yaml` for developer experience.
- `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`.
- Research summary at `evidence/research/ai-search-optimization/SUMMARY.md` documenting 67 unique sources across the four AI-search paradigms.

### Changed

- Public site directory restructured from `reports/final/interview-pack/*.html` to flat `reports/final/*.html`. Old pages renamed to research-portfolio framing:
  - `interview-pack/competitor-intelligence.html` → `competitor-landscape.html`
  - `interview-pack/subscription-economics.html` → `subscription-economics.html` (flattened)
  - `interview-pack/mvp-loop-design.html` → `mvp-design.html` (full rewrite)
  - `interview-pack/30-60-90-plan.html` → `90-day-plan.html`
  - `interview-pack/model-provenance.html` → `model-provenance.html` (flattened)
- `mvp-design.html` rewritten as a visual-first page with two inline SVG diagrams (product loop, decision tree), three pilot-track comparison, and a five-row risk register. Removed all internal IDs, JSON file references, "kill experiment" jargon, and budget figures.
- `index.html` rewritten with a citable summary lead, JSON-LD `@graph`, all eight report tiles, and no marketing badges or unverified stat grid.
- Navigation across all ten pages unified to a mobile-first hamburger drawer that expands to a horizontal row at ≥ 880px.
- The hyperbolic "live or die on one channel" claim in `subscription-economics.html` softened to "the only acquisition channel that clears a healthy LTV-to-CAC ratio in every pricing scenario", which matches what the source actually supports.
- Subscription Economics URL register fixed: literal `<https://...>` markdown auto-link text now properly converts to `<a href>` anchor tags.

### Removed

- Page `interview-pack/jd-coverage-map.html` deleted from the working tree and scrubbed from git history (force-push of cleaned history; collaborators must re-clone).
- AI-marketing badges removed from every page: "100% link-verified", "Zero LLM arithmetic", "12 specialist agents", "4+ frontier models", "7 quality gates", "Mobile-first audited".
- The "By the numbers" stat grid on `index.html` and `methodology.html` removed (unverified internal counts including "Bundle size < 50 KB" which was never measured by a script).
- All "Run 20260501T135005Z" timestamp leaks removed from page headers, hero metas, and author footers.
- All instances of "candidate" framing removed from public-facing prose (~50 occurrences across `padel-ai-coach-research.html`, `evidence-map.html`, and the report pages).
- Internal IDs (`VM-001`, `CH-006`, `RL-003`, `FM-101`, `DG-04`, `SEG-002`, etc.) removed from user-facing prose.
- Jargon ("kill experiment", "kill threshold", "north star metric", "red team", "Wizard of Oz", "anti-pattern") replaced with plain English.

### Security

- New `gitleaks` pre-commit hook and CI job for secret scanning.
- New `.well-known/security.txt` per RFC 9116.

## How to migrate

If you have a clone of this repository from before the history scrub:

```bash
# Save any local work to a branch first.
git checkout -b my-local-work
git push origin my-local-work

# Then re-clone.
cd ..
rm -rf padel-market-analysis
git clone https://github.com/avaluev/padel-market-analysis.git
```

The previously-published URL `…/interview-pack/jd-coverage-map.html` returns 404. There is no replacement page; the page was a job-application artefact that did not belong in a public research portfolio.
