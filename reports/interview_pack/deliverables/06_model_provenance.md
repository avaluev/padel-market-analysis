# Model Provenance & Radical Transparency

Every number in the pack is only as honest as the model that produced it. This page names every model, its billing class, and the artefact it touched.

> Every claim downstream of this page is only as honest as the model that produced it. This page enumerates every model invoked across the research pipeline, its billing class, and the artefacts it produced. Verification method: `grep -oE '"model":\s*"[^"]+"'` across `evidence/20260501T135005Z/_research_arms/*.json`, cross-referenced with the orchestration contract in `padel-research-os/CLAUDE.md`.

## Why this page exists

The public portfolio at [avaluev.github.io/padel-market-analysis](https://avaluev.github.io/padel-market-analysis/) has, until this audit, named only the Anthropic Claude family in its author footer ("Built with Claude Opus 4.7 + Claude Haiku 4.5 + Claude Sonnet 4.6"). That phrasing was incomplete. The deep-search workhorse of the pipeline was the paid Perplexity Sonar tier; one research arm ran on a free Alibaba Tongyi model. Both facts deserve the same visibility as the Claude lineup.

Radical transparency here is not a virtue signal — it is a hiring signal. Any reviewer who asks "which numbers came from a free model?" deserves an answer that points to a file, not a paragraph.

## Models actually invoked

### Paid frontier — primary

| Model ID | Vendor | Role | Produced research arms |
|---|---|---|---|
| `perplexity/sonar-pro` | Perplexity (via OpenRouter) | Primary deep search and peer discovery | `B_sonar_pro.json`, `E2_pricing_pro.json`, `G_gtm_sonar.json`, `H_naval_sonar.json`, `H2_naval_pro.json` |
| `perplexity/sonar-deep-research` | Perplexity (via OpenRouter) | Long-form research with multi-step web traversal | `A_sonar_deep.json`, `E_pricing_sonar.json`, `F_geo_sonar.json`, `J_market_size_big4.json` |
| `perplexity/sonar-reasoning-pro` | Perplexity (via OpenRouter) | Reasoning over peer set and adversarial red-team | `I_peers_reasoning.json`, `Z_redteam_final.json` |
| `anthropic/claude-opus-4.x` | Anthropic (via Claude Code) | Plan, synthesis, red-team direction, final write-up | Orchestration of `00_blueprint.json` through `15_market_size.json` |
| `anthropic/claude-haiku-4.5` | Anthropic (via Claude Code) | Structured-extraction sub-agents and render templates | Normalization steps of `evidence/<phase>.json` |
| `anthropic/claude-sonnet-4.6` | Anthropic (via Claude Code) | Mid-tier coding where Opus would be over-spec | `scripts/_build_*.py` generation |

### Free model — single arm

| Model ID | Vendor | Role | Produced research arms |
|---|---|---|---|
| `alibaba/tongyi-deepresearch-30b-a3b` | Alibaba (via OpenRouter free tier) | **Redundancy arm only** — output cross-validated by paid Perplexity arms before any claim entered final reports | `C_tongyi.json` |

The Tongyi arm fed into `03_peers_dedup.json` as one of three sources for peer discovery; every Tongyi-discovered peer was independently corroborated by `B_sonar_pro.json` (paid) before being added to the verified set.

### Free fallback chain — declared but NOT invoked

Three free models appear in the operating contract (`padel-research-os/CLAUDE.md`) as a fallback chain when paid Anthropic credits are tight. Verification of `evidence/20260501T135005Z/_research_arms/` returns zero invocations of any of them in this run.

| Model ID | Status |
|---|---|
| `nvidia/nemotron-3-super-120b-a12b:free` | Declared in fallback chain · NOT invoked |
| `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` | Declared in fallback chain · NOT invoked |
| `inclusionai/ling-2.6-1t:free` | Declared in fallback chain · NOT invoked |

This is documented to prevent confusion between *declared model availability* and *measured model usage* — two different claims, often conflated in vendor-led marketing.

## Paid versus free split

- **By research-arm count:** 11 of 12 research arms (~92%) ran on paid Perplexity Sonar tiers.
- **By synthesis share:** 100% of synthesis, red-team, and final report assembly ran on paid Anthropic models.
- **By token cost:** Not preserved in this evidence run. The operating contract calls for a `cost_report.sh` script that future runs are expected to emit. Until then, token-cost splits are a documented gap, not a measurement.

## How model identity is verified per claim

Every numeric claim in a downstream report cites a `source_url` and a verbatim quote ≤15 words. Those quotes are the gold standard. The model identity behind any given claim is recoverable in two steps:

1. The claim cites an evidence file (e.g., `10_monetization.json`).
2. The evidence file lists which research arm it derives from; the arm header carries the `"model"` field.

This page exists so a reviewer can do the trace without reading the source code.

## Data gaps

- **Token-cost split per model is not preserved** in this evidence run; only model identity and arm membership are recoverable. Closure: future runs are expected to emit `cost_report.sh` per the operating contract's tooling section.
- **The precise Anthropic model used per Claude Code session step** (Opus vs Sonnet vs Haiku) is not stamped into evidence files; the declared mapping in `padel-research-os/CLAUDE.md` is the source of truth, not a measurement.
- **The single Tongyi arm (`C_tongyi.json`) was not penalised in any final score** even though it ran on a free model; its claims were corroborated by paid arms before merge, and the cross-validation logic itself is not yet automated.

## Transparency statement for public pages

> Research pipeline ran primarily on paid Perplexity Sonar tiers (`sonar-pro`, `sonar-deep-research`, `sonar-reasoning-pro`) for web traversal, with one free Alibaba Tongyi arm used for redundancy. Synthesis, planning, and adversarial review ran on paid Anthropic Claude (Opus 4.x, Sonnet 4.6, Haiku 4.5) via the Claude Code orchestrator. The fallback free-model chain declared in the operating contract (Nvidia Nemotron, InclusionAI Ling) was not invoked in this run. Token-cost splits per model are a documented gap for future runs.

## Source files

- Ground-truth JSON: [`reports/interview_pack/evidence/00_model_provenance.json`](../evidence/00_model_provenance.json)
- Operating contract: `padel-research-os/CLAUDE.md` — kept private (see [`.gitignore`](https://github.com/avaluev/padel-market-analysis/blob/main/.gitignore)) to protect orchestration internals; the rules summarised on this page are the public-safe extract.
- Research arms: `evidence/20260501T135005Z/_research_arms/*.json` (12 files)
- Cross-validation rule: every Tongyi-derived claim must appear in at least one paid Perplexity arm before merge.
