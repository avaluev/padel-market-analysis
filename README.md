# Deep Research Operating System — Padel AI Coach case study

> A reproducible, multi-agent, multi-model research pipeline that produces an investor-grade strategic brief from a single prompt. Evidence-graded, link-verified, mobile-first, deployable as a static bundle.

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Static HTML](https://img.shields.io/badge/output-static_HTML-success)](reports/final/)
[![Mobile-first](https://img.shields.io/badge/mobile--first-Playwright_audited-success)](evidence/_mobile_audit/DIFF.md)
[![Zero hallucination](https://img.shields.io/badge/citations-100%25_verified-success)](scripts/verify_links.sh)

---

## What this repository proves

This is the public-facing artefact of a research operating system that:

1. **Ingests a single fuzzy prompt** ("research the AI padel coach opportunity") and produces a 1,800-line investor-grade HTML brief with every numeric claim sourced.
2. **Routes work across 4+ frontier models** (Claude Opus 4.7 for strategy, Sonar Deep Research / Tongyi DeepResearch / o4-mini for parallel web fan-out, Claude Haiku 4.5 for structured extraction) with explicit cost/quality tradeoffs per stage.
3. **Enforces zero hallucination** through hard gates: every URL fetched, every quote ≤15 words from the verified source, every number computed in a Python sandbox, every section red-teamed before merge.
4. **Ships as static HTML** with a Playwright-audited mobile-first design, sticky navigation, dark mode, safe-area insets, and 0.0 CLS across 5 device profiles.
5. **Self-deploys** to Vercel or GitHub Pages through configuration-only files (no build step).

The case study is real: a strategic brief on the [Padel AI Coach opportunity](reports/final/padel-ai-coach-research.html). The pipeline is the actual product.

---

## Outputs (open these first)

| Artefact | What it is | Size |
|---|---|---:|
| **[Strategic Brief](reports/final/padel-ai-coach-research.html)** | 18-section investor-grade research report | ~126 KB |
| **[Evidence Map](reports/final/evidence-map.html)** | Source-trace; verbatim quotes for every claim | ~42 KB |
| **[Methodology](reports/final/methodology.html)** | The pipeline itself — architecture, models, gates | ~30 KB |
| **[Index / Landing](reports/final/index.html)** | Public entry point | ~3 KB |

Total bundle: 4 HTML files, zero JS dependencies, zero external resources. Loads under 50 KB gzip.

---

## The architecture (one paragraph)

A reasoning-sandwich pipeline. **Top slice:** strategic models (Claude Opus 4.7) plan the research arms, frame the audience, and run the red-team. **Middle slice:** parallel deep-research workers (Perplexity Sonar Deep Research, Alibaba Tongyi DeepResearch 30B, OpenAI o4-mini deep-research) fan out across the same questions, returning citations, not opinions. **Bottom slice:** Claude Haiku 4.5 swarms structure the returned data into JSON/YAML using strict schemas with `null` allowed for unknowns and `data_gaps` for the missing pieces. **Glue:** Python orchestration runs the calculations (no LLM arithmetic), shell scripts verify every URL with HTTP 200, a citation checker fails the build if any number lacks a source, and a final synthesis step writes the immutable canonical brief that downstream agents (deck assembler, translator, renderer) consume verbatim. **Gates:** seven quality gates in sequence — research brief validity → citation coverage → mathematical integrity → red-team minimum issues → regulatory coverage → deck completeness → output file completeness.

Full architecture in [`reports/final/methodology.html`](reports/final/methodology.html).

---

## Why this pattern works

| Anti-pattern | What we do instead |
|---|---|
| Single model writing analysis from training data | Multi-model fan-out; every claim cites a URL fetched at runtime |
| LLM arithmetic | All numbers come from executed Python; `calculation_method == "python_subprocess_executed"` is a hard gate |
| "We talked to users" without quotes | Verbatim quote ≤15 words from the source URL, archived to `evidence/<run-id>/` |
| Demographic segments ("SMB founders") | Job + trigger + alternatives + outcome signature — demographic-only segments are rejected by the segmentation gate |
| "Better UX" as moat | Named moat class from a 7-class taxonomy: network / data / brand / distribution / switching cost / integration / regulatory / learning curve |
| Polished slop output | Red-team agent must surface ≥3 HIGH-severity issues before any section enters `reports/final/` |

---

## Tech stack

**Models (via [OpenRouter](https://openrouter.ai))**
- `anthropic/claude-opus-4-7` (Claude Opus 4.7) — strategic synthesis, red-team, USP construction
- `anthropic/claude-haiku-4-5` (Claude Haiku 4.5) — structured extraction sub-agent swarm
- `perplexity/sonar-deep-research` — primary deep search arm
- `alibaba/tongyi-deepresearch-30b-a3b` — secondary search arm (cross-check)
- `openai/o4-mini-deep-research` — tertiary arm with different RAG strategy
- Free fallback chain (`nvidia/nemotron-3-super-120b-a12b:free` → `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free`) for first-pass scans only; final synthesis stays on paid frontier models.

**Orchestration**
- Bash + Python for the pipeline driver
- Claude Code agent definitions in `.claude/agents/` (12 specialised agents)
- Single-file YAML/JSON schemas per artefact type

**Verification**
- `scripts/verify_links.sh` — HTTP 200 check on every URL, response body archived to `evidence/<run-id>/_cache/`
- `scripts/check_citations.py` — fails the build if any numeric claim has no source
- Python sandbox for every calculation; LLMs never do arithmetic

**Output rendering**
- Vanilla HTML + CSS, no framework, no build step
- Mobile-first via fluid typography (`clamp()`), bottom-sheet navigation drawer, sticky side rail on tablet+
- [Playwright audit harness](scripts/audit_mobile.mjs) across iPhone 13 / Pixel 7 / iPhone SE / iPad Mini / desktop 1280

**Deployment**
- [`vercel.json`](vercel.json) for Vercel (security headers, pretty rewrites)
- [`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml) for GitHub Pages
- Same bundle works on Netlify or Cloudflare Pages with a static-site preset

---

## Reproducing the run

```bash
# 1. Set the OpenRouter key.
export OPENROUTER_API_KEY=sk-or-...

# 2. Install Node deps for the audit harness.
npm install
npx playwright install chromium

# 3. Run the pipeline (skips the parts that wrote the case study; replace
#    with a new prompt for a fresh run).
bash scripts/run_pipeline.sh

# 4. Verify every URL still returns 200.
bash scripts/verify_links.sh

# 5. Audit mobile responsiveness.
npm run audit:baseline
npm run audit:post
npm run audit:diff        # writes evidence/_mobile_audit/DIFF.md

# 6. Deploy.
vercel --prod
# or push to main; GitHub Pages workflow publishes reports/final/
```

---

## What a reviewer should look at

For a CTO:
- [`scripts/verify_links.sh`](scripts/verify_links.sh) — the link verifier. Note URL canonicalisation, the response cache, retry-with-backoff on 5xx, and 200/203/3xx/4xx classification.
- [`scripts/audit_mobile.mjs`](scripts/audit_mobile.mjs) — Playwright harness. Note the inline-prose vs standalone-tap-target distinction (WCAG 2.5.5 nuance most audit scripts get wrong).
- [`reports/final/padel-ai-coach-research.html`](reports/final/padel-ai-coach-research.html) — vanilla HTML+CSS, ~12-line JS. No bundler. Loads under 50 KB gzip. Sticky nav, bottom-sheet drawer, dark mode, safe-area insets, print stylesheet.

For a CPO / Head of Product:
- [Section 2 of the brief](reports/final/padel-ai-coach-research.html#market-size) — TAM/SAM/SOM aligned in same currency and unit, every country sourced.
- [Section 3](reports/final/padel-ai-coach-research.html#ajtbd) — Jobs to be done in canonical form (when … wants … so that), forces of progress, alternatives currently hired, opportunity scoring.
- [Evidence Map](reports/final/evidence-map.html) — the source-trace document. Every quote verbatim from the named file or URL.

For a Head of Research / Data Science:
- [`evidence/20260501T135005Z/01_job_stories/JS-001.yaml`](evidence/20260501T135005Z/01_job_stories/JS-001.yaml) — structured AJTBD job story with confidence scoring and `gaps_to_probe_next`.
- [`evidence/20260501T135005Z/06_red_team.json`](evidence/20260501T135005Z/06_red_team.json) — segment stress-test verdicts. Note that 3 of 6 candidate segments are flagged `non-pass` — this is the discipline; an audit that says "everything passes" is itself a failure.
- [`evidence/20260501T135005Z/20_sam_global_market_check.json`](evidence/20260501T135005Z/20_sam_global_market_check.json) — comprehensive 21-country SAM rebuild after the original list was flagged as incomplete. Documents the inclusion threshold, exclusions (Uzbekistan: 8 courts, below threshold), and the audit trail.

---

## Repository map

```
.
├── reports/final/                    Customer-facing publishable bundle
│   ├── index.html                    Landing page
│   ├── padel-ai-coach-research.html  Strategic brief (18 sections)
│   ├── evidence-map.html             Source-trace companion
│   ├── methodology.html              The pipeline itself
│   ├── 404.html
│   ├── robots.txt
│   └── README.md                     Bundle README (deploy notes)
│
├── evidence/20260501T135005Z/        Run artefacts (frozen, immutable)
│   ├── 00_blueprint.json             Run plan
│   ├── 01_job_stories/               JS-001 to JS-004 (AJTBD)
│   ├── 03_peers_dedup.json           Verified competitor list
│   ├── 04_peer_cards/                17 peer cards
│   ├── 06_red_team.json              Segment stress test
│   ├── 08_value_mechanics/           VM-001 to VM-011 with RICE
│   ├── 09_moat_audit.json            Five-gate moat filter
│   ├── 12_geo.json                   Country bands
│   ├── 13_capability_map.json        ship_solo / needs_partner / needs_capital
│   ├── 15_market_size.json           TAM / SAM / SOM
│   ├── 19_uae_uzbekistan_check.json  UAE/Uzbekistan SAM verification
│   ├── 20_sam_global_market_check.json  Comprehensive 21-country SAM
│   └── canonical_brief.json          Immutable downstream label set
│
├── evidence/_mobile_audit/           Playwright audit artefacts
│   ├── DIFF.md                       Before/after metrics
│   ├── baseline/, post/              Per-device screenshots + metrics
│   └── scroll/                       Scroll-position screenshots
│
├── evidence/_audits/                 Multi-perspective code/pipeline audits
│
├── scripts/
│   ├── audit_mobile.mjs              Playwright mobile audit
│   ├── audit_diff.mjs                Baseline vs post diff report
│   ├── postprocess_html.mjs          Table-wrap + rel=noopener
│   ├── scroll_check.mjs              Sticky-nav verification
│   ├── verify_links.sh               HTTP 200 gate
│   ├── check_citations.py            Source-required gate
│   └── run_pipeline.sh               End-to-end orchestrator
│
├── .claude/agents/                   12 specialist agent definitions
├── .github/workflows/deploy-pages.yml
├── vercel.json
├── package.json
├── LICENSE                           Apache 2.0
└── README.md                         (this file)
```

---

## Author

**Alexandr Valuev** · Product strategy · AI-driven research pipelines · Multi-agent orchestration.

- LinkedIn — [linkedin.com/in/valuev](https://www.linkedin.com/in/valuev/)
- Telegram — [t.me/ASNKT](https://t.me/ASNKT)
- GitHub — [github.com/avaluev](https://github.com/avaluev)
- This repo — [github.com/avaluev/padel-market-analysis](https://github.com/avaluev/padel-market-analysis)

The artefacts in this repository were produced in collaboration with Claude (Anthropic) acting as the orchestrator across 12 specialised agents (Claude Opus 4.7 for strategy and red-team; Claude Sonnet 4.6 and Claude Haiku 4.5 for execution; Perplexity Sonar Deep Research, Alibaba Tongyi DeepResearch 30B, and OpenAI o4-mini deep-research for parallel web fan-out). The methodology, prompt design, evidence schemas, gate definitions, and editorial decisions are mine; the models executed the pipeline.

---

## License

[Apache License 2.0](LICENSE) — use, fork, redistribute, including commercial. Attribution required for derivatives. The Padel AI Coach analysis is shared as a worked example; the pipeline is the contribution.
