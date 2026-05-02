# Contributing

This is primarily a portfolio / case-study repository, but improvements to the pipeline and the audit harness are welcome.

## Ground rules

- Open an issue before a large PR.
- Every change to `reports/final/` must pass `scripts/verify_links.sh` (HTTP 200 on every URL).
- Every change touching the pipeline must keep the seven quality gates passing (see [methodology](reports/final/methodology.html)).
- No fabricated facts in the example artefacts — if a number is added or revised, it must carry a verifiable source.
- Prefer small, focused PRs over large ones.

## Running locally

```bash
npm install
npx playwright install chromium

# Verify all cited URLs
bash scripts/verify_links.sh

# Mobile audit
npm run audit:baseline
npm run audit:post
npm run audit:diff
```

## Style

- Vanilla HTML+CSS in `reports/final/`. No frameworks.
- Node scripts use ES modules and the standard library; only Playwright is allowed as a dev dependency.
- Python scripts run with the system interpreter; no virtual envs unless absolutely required.
