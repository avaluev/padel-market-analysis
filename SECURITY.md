# Security policy

## Reporting a vulnerability

Open a GitHub issue with the label `security`, or contact the maintainer privately if the issue is sensitive. We will respond within 5 business days.

## Scope

This repository ships a static HTML bundle and a research pipeline. The relevant attack surfaces:

- **The pipeline** consumes web content via curl and Playwright. URL validation, response caching, and HTTP-only enforcement (no `file://`) live in `scripts/verify_links.sh`.
- **The OpenRouter API key** is loaded from `OPENROUTER_API_KEY` env only. There are no committed credentials.
- **The deployed bundle** is fully static. Security headers (HSTS, CSP, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy) are configured in `vercel.json`.

## Out of scope

- Vulnerabilities in third-party dependencies (Playwright, Node) — please report upstream.
- Issues requiring social-engineering of the maintainer.
