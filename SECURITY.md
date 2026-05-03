# Security policy

## Reporting a vulnerability

If you find a security vulnerability in this repository (leaked secret, dependency vulnerability, content-injection vector, deploy-pipeline issue), please **do not file a public issue**. Instead, contact the author directly:

- LinkedIn: <https://www.linkedin.com/in/valuev/>
- Telegram: <https://t.me/ASNKT>

Include:

- The affected file or URL.
- Steps to reproduce.
- The impact you assessed.

Acknowledgement target: within seven days. Mitigation timeline depends on severity.

## Scope

In scope:

- Secrets accidentally committed to the repository.
- Vulnerabilities in the GitHub Actions workflows under `.github/workflows/`.
- Vulnerabilities in build / publish scripts under `scripts/`.
- Cross-site scripting or content-injection vectors in published HTML pages.
- Misconfigured `robots.txt` or `security.txt` rules.

Out of scope:

- Vulnerabilities in third-party crawler behaviour (GPTBot, ClaudeBot, etc.) — report those to the operator.
- Content disagreements (factual disputes, source-quality concerns) — file a public issue instead.

## Supported versions

The repository follows a rolling-release model on `main`. Security fixes land on `main` and ship through the next deploy.

## Response

Confirmed vulnerabilities are added to `evidence/_security/<date>.md` after mitigation. The note includes the vulnerability class, the fix, and the regression check added to prevent recurrence (in line with the project's stabilisation cycle).
