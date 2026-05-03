# Padel Research OS — Quality Bar

> Single source of truth for every research, synthesis, red-team, and rendering agent invoked under this operating contract. Every agent prompt MUST reference this file (`Obey QUALITY_BAR.md`) instead of repeating requirements inline. Updates here propagate to all downstream agents on the next run.

**Canonical location:** `padel-research-os/QUALITY_BAR.md`
**Version:** 1.0 — 2026-05-03
**Override priority:** This file overrides agent-defaults; `padel-research-os/CLAUDE.md` overrides this file when in direct conflict; user-issued instructions override both.

---

## 1. Hard rules — MUST NOT

| # | Rule | Failure mode it prevents |
|---|---|---|
| H-1 | MUST NOT fabricate quotes, statistics, dollar figures, market sizes, or company facts. If a number is not on a verified URL, it is `null` and goes in `data_gaps`. | Citation laundering; reviewer clicks the link, finds nothing. |
| H-2 | MUST NOT cite a URL without storing the fetched response in `evidence/`. Citation without evidence is pipeline failure. | Quote-without-source. |
| H-3 | MUST NOT use demographic-only segments. Segments must include job + constraint + trigger + alternatives_hired. | "Demographic in disguise" red-team failure. |
| H-4 | MUST NOT claim "better UX" or "AI-powered" as a moat. Use the moat taxonomy (network, data, brand, distribution, switching cost, integration, regulatory, learning curve). | Vanity moat. |
| H-5 | MUST NOT use first-person pronouns (I, we, my, our, us, me, mine, ours) anywhere in `reports/` or `deliverables/`. | Voice leak. |
| H-6 | MUST NOT promise budgets, timelines, or headcount. Phrasing is capability-conditional ("the role would coordinate …", "solo execution can …"). | Wish-based commitments. |
| H-7 | MUST NOT skip the red-team pass before a section enters `reports/final/` or `deliverables/`. | Unreviewed claims shipped. |
| H-8 | MUST NOT tag a claim VERIFIED if the verbatim quote is internal product language, not vendor-page text. | Fabricated attribution (red-team finding HIGH-2/HIGH-4 from 2026-05-03 review). |
| H-9 | MUST NOT cross-reference a metric across deliverables without making the cross-reference explicit. If 04 instruments an event, 03 must build it; if 02 prices a market, 04 must respect that price. | Cross-doc contradiction (red-team finding HIGH-1/HIGH-3/HIGH-5). |

---

## 2. Hard rules — MUST

| # | Rule | Verification command |
|---|---|---|
| M-1 | Every URL renders HTTP 200 (or documented 3xx) in `verify_links.sh`. | `bash scripts/verify_links.sh` |
| M-2 | Every numeric claim carries a `source_url` and a verbatim quote ≤15 words from that URL. | `python3 scripts/check_citations.py` |
| M-3 | Every factual claim is tagged: `VERIFIED` (URL fetched, quoted ≤15 words), `INFERRED` (logical step from a verified claim, marked as such), or `ABSENT` (gap acknowledged). | grep for tag presence per claim |
| M-4 | Original-language phrasing preserved for verbatim quotes; translations live in a `translation:` field with original retained. | manual sample audit |
| M-5 | Every numeric calculation runs through the Python sandbox. LLMs do not perform arithmetic. The output of arithmetic must be reproducible from the JSON inputs. | `python3 -c "..."` re-run on cited math |
| M-6 | Every section that ships to `reports/final/` has a red-team verdict of `pass` or `pass_with_caveats` recorded in `_redteam/<section>.md`. | red-team report present per section |
| M-7 | Every deliverable references this file at the top: `Quality bar: see padel-research-os/QUALITY_BAR.md`. | grep for the line |
| M-8 | Mobile-first layout: no element renders below 12px on viewports ≥320px wide; no horizontal scroll outside `.table-wrap` and `<pre>`; all images have alt text. | `node scripts/audit_sources.mjs` |

---

## 3. Citation tag taxonomy

| Tag | Meaning | Example |
|---|---|---|
| `VERIFIED` | URL was fetched at runtime, response stored in `evidence/`, quote is verbatim ≤15 words from that response. | "Strava Premium plan billed monthly anchored at $11.99" — strava.com/premium |
| `INFERRED` | The claim is a logical step from one or more `VERIFIED` claims; the inference itself is not on any source page. | "Padel-specific Q4 churn likely 2–3× baseline (Iberia outdoor pattern, no first-party measurement yet)" |
| `INTERNAL` | The claim is a kill-threshold, internal product policy, or analytical decision authored by the candidate, NOT a vendor or source quote. Must not be wrapped in `VERIFIED` quote marks. | "At EUR 7.99/month, ≥8% paid conversion within three matches is keep; <4% triggers hedge model." |
| `INFERRED_INHERITED` | The claim extrapolates from a numeric range published by a verified source. Must show the derivation arithmetic. | "F5 retention ~50–60% derived from Foundry 12-month 35–45% via monthly survival math" |
| `ABSENT` | No verified source could be located. The gap is documented in `data_gaps`. The claim itself is `null`. | LTV at RUB 499 with no Telegram CAC published — null + data_gap entry |

**Common failure pattern (banned):** A vendor-page claim presented with a `verified_quote` field whose value is a descriptive phrase like "Clutch club tier published in vendor capture" rather than vendor-page text. This is `INFERRED` (Sonar paraphrase), not `VERIFIED`.

---

## 4. Voice rules

- **Voice:** Third-person professional. Capability-conditional where a future commitment would otherwise sound first-person.
- **Sample fix:**
  - PASSIVE/wishful: "We will validate the rating accuracy."
  - ACTIVE/capability-conditional: "The role would validate rating accuracy in week 1 of the pilot."
  - First-person leak (BANNED): "I would validate rating accuracy."

- **Hook openings:** Each deliverable opens with a 1–2 sentence framing claim before the first H2 — capability-conditional, not first-person.
- **Pull quotes:** One markdown blockquote (`> …`) per major H2 carries the load-bearing claim.
- **Active voice preferred** when it reads natural and stays third-person.

---

## 5. Quality gates per artifact type

### Research arm (deep search agent)
- ≥1 distinct verified URL per numeric claim.
- `VERIFIED` quotes ≤15 words, original-language preserved.
- `data_gaps` array populated for every absent claim.
- Tongyi-tier (free model) outputs are CROSS-VALIDATED by at least one paid Perplexity arm before merge.

### Synthesis brief (deliverable in `deliverables/*.md`)
- ≥8 distinct verified URLs.
- Hook opening present.
- Every claim carries a tag (`VERIFIED | INFERRED | INTERNAL | ABSENT`).
- Cross-document consistency: any metric used in multiple briefs must use the same value or call out the version difference.
- `data_gaps` summary appears at the end.
- HTML render passes mobile audit (M-8).

### Red-team report
- ≥3 HIGH issues identified (else verdict is "diplomatic — retry").
- ≥5 MEDIUM issues identified.
- ≥2 fabrication risks (claim that LOOKS sourced but isn't; or number whose URL says something different).
- Survivorship-bias check (graveyard non-empty or limitation declared).
- Cross-document consistency table.
- 8 "founder will ask" questions with strongest-current-answer + honest gap.

### Rendering (HTML for GitHub Pages)
- Mobile-first audit: 0 issues across iPhone SE, iPhone 13, Pixel 7, iPad Mini, desktop-1280.
- All external links return HTTP 200/3xx (LinkedIn 999 is a documented false-positive of bot-detection on HEAD).
- All images: alt text present, lazy-loaded with proper aspect-ratio reservation, served from same origin (no hot-linking).
- Author footer + JSON-LD + `link rel="me"` chain present on every page.
- Model fingerprint in footer enumerates paid + free models actually invoked (per `evidence/00_model_provenance.json`).

---

## 6. Cross-document consistency contract

Any metric or claim used in more than one deliverable MUST be sourced from a single canonical artefact.

| Canonical source | Authoritative for |
|---|---|
| `evidence/<run-id>/10_monetization.json` | Pricing, churn, LTV/CAC assumptions, geo localization, kill thresholds |
| `evidence/<run-id>/03_peers_dedup.json` | Verified peer set, peer URLs, peer categories |
| `evidence/<run-id>/06_red_team.json` | Segment validity (PASS / FAIL / KILL / MERGE) |
| `evidence/<run-id>/05_jobs_graph.json` | Job stories, alternatives_hired, switch triggers |
| `evidence/<run-id>/15_market_size.json` | TAM / SAM / SOM by geography |
| `reports/sources/evidence/00_model_provenance.json` | Models invoked, billing class, downstream evidence |

**If a deliverable needs a number, it reads from the canonical source first.** If the canonical source has the number with a different value than the deliverable, the deliverable is wrong.

---

## 7. Anti-hallucination enforcement (the four laws)

1. **Citation requirement** — every numeric claim has `source_url` + `verified_quote` ≤15 words.
2. **Python math requirement** — every number that is the output of arithmetic is tagged `calculation_method: python_explicit` and the formula appears in plain text.
3. **Null > fabrication** — when no source is found, write `null` and add a `data_gap` entry. A null with documentation is valid; a fabricated number is pipeline failure.
4. **Canonical immutability** — once a synthesis JSON is written, downstream deliverables read from it, not from underlying research files. If two artefacts disagree, the canonical wins.

---

## 8. Stabilization cycle

Every red-team finding becomes a new rule. The append-only ledger:

- 2026-05-03 — Red-team flagged fabricated Foundry CRO threshold quote → added H-8 (no internal text wrapped as VERIFIED).
- 2026-05-03 — Red-team flagged 30-60-90 plan instrumenting events the MVP loop never builds → added H-9 (cross-doc instrumentation contract).
- 2026-05-03 — Red-team flagged Hudl scale figures sourced from CoachLogic → added M-mandatory canonical-source-first behavior under §6.

When a rule is added here, also:
- Update `padel-research-os/CLAUDE.md` Hard Rules table to mirror the addition (see §1 there).
- Add a regression check to `scripts/check_citations.py` if the rule is grep-able.
- Update the offending agent prompt template in `.claude/agents/`.

No retries without a new rule.

---

## 9. The reasoning sandwich (model allocation)

| Phase | Model class | Effort |
|---|---|---|
| Plan / reconnaissance | `anthropic/claude-opus-4.x` | extended thinking, max budget |
| Deep search & extraction | `perplexity/sonar-deep-research`, `perplexity/sonar-pro`, `alibaba/tongyi-deepresearch-30b-a3b` (free, redundancy only), `openai/o4-mini-deep-research` | parallel fan-out |
| Structured extraction | `anthropic/claude-haiku-4.5` (sub-agent swarm) | standard |
| Synthesis & framing | `anthropic/claude-opus-4.x` | extended thinking |
| Red-team & verification | `anthropic/claude-opus-4.x` | extended thinking, max budget |
| Render & format | `anthropic/claude-haiku-4.5` | standard |

**Free fallback chain (declared, used only when paid credits are tight):** `nvidia/nemotron-3-super-120b-a12b:free`, `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free`, `inclusionai/ling-2.6-1t:free`. Outputs from free models are tagged `free_model_paraphrase` and cross-validated by at least one paid arm before merge.

---

## 10. The single sentence

> Every claim earns its place by pointing to a URL the reviewer can click, a number the reviewer can re-run in Python, or a `null` plus a `data_gap` the reviewer can challenge — nothing in between.

Agents that violate any rule above produce pipeline failures. The pipeline does not retry without first updating this file with a new rule that prevents the failure mode.
