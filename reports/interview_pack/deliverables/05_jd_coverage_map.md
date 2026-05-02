# JD-Coverage Map — Product Lead / Head of Product, AI Platform for padel

A JD-coverage map earns its name when the gaps are named first and the strengths second. This document does that for every required and nice-to-have bullet, with evidence trails, and three prepared pivots for the moments a recruiter probes the gap.

> One-page artefact mapping every bullet of the Russian job description to verifiable candidate evidence. Voice: third-person professional. Honest about gaps.
>
> **Anchor:** the candidate's public research portfolio at [avaluev.github.io/padel-market-analysis](https://avaluev.github.io/padel-market-analysis/) (source repo: [github.com/avaluev/padel-market-analysis](https://github.com/avaluev/padel-market-analysis)). Sibling briefs are referenced by filename and read alongside this map.
>
> **Verdict legend.** STRONG = verifiable artefact, defensible without caveat. PARTIAL = adjacent evidence on file, gap acknowledged with concrete closure plan. GAP = no evidence on file, closure plan with role-week deadline.

> Of fourteen JD bullets, seven are STRONG, six are PARTIAL with closure plans on the role-week clock, and one is GAP — named openly rather than hidden.

---

## REQUIRED bullets (8)

### REQ-1 — Опыт запуска цифровых продуктов с нуля

**EN:** Experience launching digital products from scratch.

**Verdict: PARTIAL.**

The padel-research-os repository itself is a from-zero digital artefact: a multi-agent pipeline, a 1,800-line static-HTML investor brief, mobile-audited via Playwright, deploying through Vercel and GitHub Pages from configuration-only files. Whether the candidate has independently shipped a separate revenue-generating product is to be confirmed in screening — the strict-honesty rule prevents fabrication.

**Supporting artefacts:** [github.com/avaluev/padel-market-analysis](https://github.com/avaluev/padel-market-analysis); [reports/final/padel-ai-coach-research.html](../../final/padel-ai-coach-research.html).

**Closure plan.** Bring two zero-to-launch case briefs to the screening call: one technical (this repository's pipeline architecture), one commercial (prior product or side-launch with date, scope, retained users). If no commercial example exists, frame transparently as "to discuss in screening" rather than fabricate. **Deadline: pre-call deck, before role-week 1.**

---

### REQ-2 — Опыт работы с MVP, быстрыми гипотезами и пользовательскими интервью

**EN:** Experience with MVPs, rapid hypotheses, and user interviews.

**Verdict: STRONG.**

The blueprint defines four kill-experiments, each as an explicit hypothesis + kill-criterion + evidence-required triplet (smartphone-rating acceptance, coach-pilot completion, FIP organiser LOI, OSS pipeline reproducibility). The capability map sorts every value-mechanic into ship_solo / ship_solo_with_apis / requires_partner / requires_capital bands so MVP scope is gated by what is actually feasible solo. Sibling brief **03_mvp_loop_design.md** formalises the smoke-test → drill-plan → coach-pilot loop.

**Supporting artefacts:** [evidence/20260501T135005Z/00_blueprint.json](../../../evidence/20260501T135005Z/00_blueprint.json) (kill_experiments); [prompts/05_segment_canvas.md](../../../prompts/05_segment_canvas.md); [prompts/07_interview_guide.md](../../../prompts/07_interview_guide.md); sibling 03_mvp_loop_design.md.

---

### REQ-3 — Понимание unit-экономики, воронок, retention, LTV/CAC

**EN:** Understanding of unit economics, funnels, retention, LTV/CAC.

**Verdict: STRONG.**

Sibling brief **02_subscription_economics.md** models LTV/CAC, payback, and retention bands per cohort. The direct-readership newsletter capability targets ≤USD 12 acquisition cost (Foundry CRO 2026 anchor). The coach renewal chain is modelled as a separate cohort. CLAUDE.md mandates Python-sandbox arithmetic — LLMs never do the math, which is the same discipline expected from a Product Lead reviewing a finance dashboard.

**Supporting artefacts:** sibling 02_subscription_economics.md; [evidence/20260501T135005Z/canonical_brief.json](../../../evidence/20260501T135005Z/canonical_brief.json); [evidence/20260501T135005Z/10_monetization.json](../../../evidence/20260501T135005Z/10_monetization.json).

---

### REQ-4 — Опыт в продуктах с подпиской, регулярной оплатой или повторными покупками

**EN:** Experience with subscription, recurring-payment, or repeat-purchase products.

**Verdict: PARTIAL.**

Subscription mechanics are modelled as a research artefact (sibling 02). A direct prior subscription product on the candidate's CV is not yet confirmed on file. The proposed coach renewal pilot (capability rows CH-002 and CH-007 in the capability map) is positioned as the first hands-on subscription cycle inside the role.

**Supporting artefacts:** sibling 02_subscription_economics.md; [evidence/20260501T135005Z/13_capability_map.json](../../../evidence/20260501T135005Z/13_capability_map.json) — rows CH-002, CH-007.

**Closure plan.** Bring one prior subscription or recurring-revenue example to the screening with retained-cohort numbers (B2C SaaS, B2B retainer, or e-commerce repeat-purchase). If none, propose a 14-day prepaid drill-plan as the first paid loop in **role-week 4**, with first cohort live by **role-week 6**.

---

### REQ-5 — Умение работать с неопределённостью и ранней стадией проекта

**EN:** Ability to work with uncertainty and early-stage projects.

**Verdict: STRONG.**

The pipeline is structured around a stated stage: AURA = "understanding" with explicit entry and exit signals. Capability bands segregate ship_solo vs requires_partner vs requires_capital so uncertainty is named rather than wished away. Kill criteria are pre-declared, not retro-fitted. The VERIFIED / INFERRED / ABSENT tagging is the operating discipline for unknowns; "null + data_gaps" is preferred over fabrication, which is exactly the early-stage stance.

**Supporting artefacts:** [evidence/20260501T135005Z/canonical_brief.json](../../../evidence/20260501T135005Z/canonical_brief.json) — aura_thesis; [CLAUDE.md](../../../CLAUDE.md) — Hard Rules (MUST NOT fabricate); [evidence/20260501T135005Z/13_capability_map.json](../../../evidence/20260501T135005Z/13_capability_map.json).

---

### REQ-6 — Способность переводить стратегические идеи основателя в roadmap, задачи и релизы

**EN:** Ability to translate founder strategy into roadmap, tasks, and releases.

**Verdict: STRONG.**

Sibling brief **04_30_60_90_plan.md** is the literal demonstration: a single founder-level prompt converted into 16 numbered prompt files, 12 specialised agents, 7 quality gates, and a sequenced release plan. Every capability row in 13_capability_map.json carries a `first_observable_output` and a `kill_signal` — the exact structure a Product Lead is expected to write for engineering and ops.

**Supporting artefacts:** sibling 04_30_60_90_plan.md; [prompts/](../../../prompts/) (16 numbered files); [evidence/20260501T135005Z/13_capability_map.json](../../../evidence/20260501T135005Z/13_capability_map.json).

---

### REQ-7 — Опыт управления кросс-функциональной командой: разработка, дизайн, аналитика, операционка

**EN:** Cross-functional team management: engineering, design, analytics, operations.

**Verdict: PARTIAL.**

The 12-agent orchestration (planner, deep-research workers, structured extraction swarm, synthesis, red-team, render) is a credible analogue for cross-functional coordination — each agent has a defined responsibility, model allocation, and gate. Direct line-management of human engineering, design, analytics, and operations teams is not visible from the research artefact alone.

**Supporting artefacts:** [reports/final/methodology.html](../../final/methodology.html); [.claude/agents/](../../../.claude/agents/); CLAUDE.md — Compute Allocation table.

**Closure plan.** Bring one prior cross-functional team brief to the screening: team size, disciplines covered, the one decision that required arbitration across two functions, and the outcome. If the role expects line management on day one, propose **role-weeks 1-2** as a structured 1:1 round with each function head, plus a written team operating rhythm by **role-week 3**.

---

### REQ-8 — Умение работать с данными и формулировать требования к аналитике

**EN:** Ability to work with data and define analytics requirements.

**Verdict: STRONG.**

Every claim in the research brief is tagged VERIFIED / INFERRED / ABSENT and sourced. `check_citations.py` fails the build if any number lacks a source. Numeric claims pass through a Python sandbox (`calculation_method == "python_subprocess_executed"`). The evidence map is a verbatim trace from claim to URL — the same shape that a product analytics requirement document needs (event → field → owning function → success threshold).

**Supporting artefacts:** [reports/final/evidence-map.html](../../final/evidence-map.html); [scripts/check_citations.py](../../../scripts/check_citations.py); [scripts/verify_links.sh](../../../scripts/verify_links.sh); CLAUDE.md — Hard Rules.

---

## NICE-TO-HAVE bullets (6)

### NTH-1 — Опыт в sport-tech, health-tech, fitness-tech, edtech, marketplace или community-продуктах

**EN:** Experience in sport-tech, health-tech, fitness-tech, edtech, marketplace, or community products.

**Verdict: PARTIAL.**

Sport-tech research is on the public portfolio: peer cards on Padelytics, PlaySight, Hudl, Wingfield, Eyes On Padel, Playtomic, MATCHi. Hands-on operating experience inside a sport-tech, health-tech, edtech, or marketplace product is not yet confirmed.

**Supporting artefacts:** [avaluev.github.io/padel-market-analysis](https://avaluev.github.io/padel-market-analysis/); [evidence/20260501T135005Z/00_blueprint.json](../../../evidence/20260501T135005Z/00_blueprint.json) — peer_seed; sibling 01_competitor_intelligence.md.

**Closure plan.** Confirm any prior product exposure in adjacent verticals during the screening call (one paragraph, dates, scope). If none, position the 12-peer competitor matrix and the AURA-graded segment work as the operating substitute and propose **role-week 1** founder-shadowing as the on-ramp.

---

### NTH-2 — Опыт запуска продукта с AI/ML/CV-компонентом

**EN:** Experience launching a product with an AI/ML/CV component.

**Verdict: STRONG.**

The research-os pipeline routes work across Claude Opus 4.7, Claude Haiku 4.5, Sonar Deep Research, Tongyi DeepResearch 30B, and o4-mini deep-research with explicit cost/quality tradeoffs per stage. The capability map names [Joao-M-Silva/padel_analytics](https://github.com/Joao-M-Silva/padel_analytics) as the verified OSS computer-vision anchor and ties every value-mechanic to a `kill_signal`. Free-tier fallback chain is documented for cost-pressured runs. This is product-level AI/ML/CV systems thinking on a public URL.

**Supporting artefacts:** [github.com/avaluev/padel-market-analysis](https://github.com/avaluev/padel-market-analysis); [github.com/Joao-M-Silva/padel_analytics](https://github.com/Joao-M-Silva/padel_analytics); [openrouter.ai/api/v1/models](https://openrouter.ai/api/v1/models); [reports/final/methodology.html](../../final/methodology.html).

---

### NTH-3 — Понимание спортивных рейтингов, тренировочных систем, академий или клубных моделей

**EN:** Understanding of sports ratings, training systems, academies, or club models.

**Verdict: PARTIAL.**

Research surfaces the rating-portability problem (Playtomic / MATCHi self-declared levels do not travel across clubs) and frames the coach renewal chain as a B2B2C cohort. Sibling 03_mvp_loop_design.md sketches the academy and pair-level loops. Operating-level fluency in a real academy P&L or a federation rating committee is not on file — this rule cannot be marked STRONG even with research depth, per the strict-honesty rule.

**Supporting artefacts:** [evidence/20260501T135005Z/canonical_brief.json](../../../evidence/20260501T135005Z/canonical_brief.json) — vision_frame; [evidence/20260501T135005Z/13_capability_map.json](../../../evidence/20260501T135005Z/13_capability_map.json) — rows VM-002, VM-004; [padelfip.com](https://www.padelfip.com/); [playtomic.io/blog](https://playtomic.io/blog).

**Closure plan — two tracks.** *Track A — research depth, role-weeks 1-2:* three 45-minute interviews with FEP / FITP / PadelFIP-affiliated coaches, recorded and tagged into the AJTBD format. *Track B — operating depth, role-weeks 3-4:* one half-day shadow at a Spanish or Italian academy, plus a co-creation contract with the head coach to test the drill-prescription engine on real students.

---

### NTH-4 — Личный интерес к паделу или опыт игры

**EN:** Personal interest in padel or playing experience.

**Verdict: GAP.**

The candidate is not on file as a padel player. Domain immersion comes from the research artefact, not from on-court experience. Pretending otherwise would fail the candidate's own red-team gate. This is the bullet most likely to be probed in the screening — it is addressed openly rather than hidden.

**Supporting artefacts:** CLAUDE.md — Hard Rules (MUST NOT fabricate); sibling 03_mvp_loop_design.md (closure-plan rationale).

**Closure plan — three steps inside the first 90 days.**

1. **Role-week 1:** complete a beginner padel clinic with a FEP-credentialed coach; log every JTBD friction point in the candidate's own AJTBD format.
2. **Role-weeks 1-4:** shadow two academy coaches per week, one in Madrid (in person) and one remote-video. Output: weekly written field-notes in `evidence/coach_shadow/`.
3. **Role-weeks 4-12:** sign a coach co-creation contract — a named coach is the design partner for the drill-prescription engine, with weekly written feedback on shipped builds.

In the screening call, frame this as the **fresh-JTBD-lens pivot** (see Pivot 1 below) rather than a deficit. A Product Lead joining at AURA "understanding" stage is meant to enter without category bias.

---

### NTH-5 — Опыт запуска продуктов в международном контексте

**EN:** Experience launching products in an international context.

**Verdict: PARTIAL.**

Geography strategy spans five priority markets (Spain, Italy, UAE, US, CIS) with an explicit GDPR / 152-FZ data-residency split. Localisation capability VM-008 ships Spanish + Russian recap. A prior multi-country launch in the candidate's track record is not yet on file.

**Supporting artefacts:** [evidence/20260501T135005Z/12_geo.json](../../../evidence/20260501T135005Z/12_geo.json); [evidence/20260501T135005Z/19_uae_uzbekistan_check.json](../../../evidence/20260501T135005Z/19_uae_uzbekistan_check.json); [evidence/20260501T135005Z/13_capability_map.json](../../../evidence/20260501T135005Z/13_capability_map.json) — VM-008, CH-006.

**Closure plan.** Bring one prior international touchpoint to the screening (any cross-border launch, partner integration, or foreign-market customer interviews). If none, propose **role-weeks 2-4**: one in-person trip to Madrid (FEP) and one remote pilot with a UAE partner club, both with named contacts and gating outcomes.

---

### NTH-6 — Английский для работы с зарубежными подрядчиками/партнёрами

**EN:** English for working with foreign contractors and partners.

**Verdict: STRONG.**

The full investor-grade research brief and methodology page are authored in professional English at the register expected for a foreign LP or partner. Voice discipline (third-person, no first-person leaks) is enforced by the candidate's own pipeline as a hard gate — the same level of write-up control that international partner correspondence requires.

**Supporting artefacts:** [reports/final/padel-ai-coach-research.html](../../final/padel-ai-coach-research.html); [reports/final/methodology.html](../../final/methodology.html); [avaluev.github.io/padel-market-analysis](https://avaluev.github.io/padel-market-analysis/).

---

## The 3 Conversation Pivots

> Three named moments where a JD weakness becomes a strength on the call. Each pivot: trigger question patterns, bridge sentence, proof point.

### Pivot 1 — Fresh-JTBD-lens pivot

**Trigger questions.**
- "Do you actually play padel?"
- "How do you understand the player if you have never been on court?"
- "Are you a paying user of any of the competitors?"

**Bridge sentence.**
"The first asset a Product Lead can bring to a domain still in the AURA 'understanding' stage is a clean JTBD lens that is not pre-loaded with category beliefs."

**Proof point.**
The four core jobs in [evidence/20260501T135005Z/00_blueprint.json](../../../evidence/20260501T135005Z/00_blueprint.json) — objective self-rating, targeted practice drills, coach co-pilot, post-match review with partner — were written without a player's bias and survived the red-team pass. The closure plan is explicit: clinic in role-week 1, two coach shadows per week, named coach co-creation contract by role-week 4 (sibling 03_mvp_loop_design.md). Public portfolio anchor: [avaluev.github.io/padel-market-analysis](https://avaluev.github.io/padel-market-analysis/).

---

### Pivot 2 — Hallucination-free product builder pivot

**Trigger questions.**
- "Have you launched a product from zero?"
- "What ships first when you join?"
- "How do you avoid building the wrong thing in an unfamiliar domain?"

**Bridge sentence.**
"Shipping in an unfamiliar domain is a citation-discipline problem, not a courage problem."

**Proof point.**
The padel-research-os pipeline enforces VERIFIED / INFERRED / ABSENT tagging, fails the build on any unsourced number, and routes every numeric claim through a Python sandbox. The same gates can run inside the product against analytics events on day one — the discipline transfers verbatim. References: [scripts/check_citations.py](../../../scripts/check_citations.py); CLAUDE.md hard rules; [github.com/avaluev/padel-market-analysis](https://github.com/avaluev/padel-market-analysis).

---

### Pivot 3 — Kill-criterion-first roadmap pivot

**Trigger questions.**
- "What would you build first?"
- "How will you know whether the rating idea is real?"
- "What is the first three-month milestone?"

**Bridge sentence.**
"A roadmap that does not name what would kill it is not a roadmap, it is a wishlist."

**Proof point.**
The blueprint pre-declares four kill-experiments — smartphone-only rating acceptance, coach pilot completion, FIP organiser LOI, OSS pipeline reproducibility — each with explicit hypothesis, kill-criterion, and evidence-required. Sibling 04_30_60_90_plan.md sequences them into role-weeks. Reference: [evidence/20260501T135005Z/00_blueprint.json](../../../evidence/20260501T135005Z/00_blueprint.json) (kill_experiments).

---

## Coverage summary

| Tier | STRONG | PARTIAL | GAP | Total |
|------|-------:|--------:|----:|------:|
| Required (8) | 5 | 3 | 0 | 8 |
| Nice-to-have (6) | 2 | 3 | 1 | 6 |
| **Combined (14)** | **7** | **6** | **1** | **14** |

Required-row trace: REQ-1 PARTIAL, REQ-2 STRONG, REQ-3 STRONG, REQ-4 PARTIAL, REQ-5 STRONG, REQ-6 STRONG, REQ-7 PARTIAL, REQ-8 STRONG.

Nice-to-have-row trace: NTH-1 PARTIAL, NTH-2 STRONG, NTH-3 PARTIAL, NTH-4 GAP, NTH-5 PARTIAL, NTH-6 STRONG.

- **Most defensible STRONG claim:** NTH-2 — AI/ML/CV product launch experience. Verifiable on a public URL, named OSS anchor, named model-routing strategy, explicit kill-signals per value-mechanic.
- **Single bullet most likely to be probed hardest in screening:** NTH-4 — personal interest in padel or playing experience. Marked GAP openly; the closure plan must be delivered live on the call rather than deferred. Pivot 1 above is the prepared bridge.

---

## Verified URLs cited (≥4 required)

1. [avaluev.github.io/padel-market-analysis](https://avaluev.github.io/padel-market-analysis/) — public portfolio anchor.
2. [github.com/avaluev/padel-market-analysis](https://github.com/avaluev/padel-market-analysis) — source repository.
3. [github.com/Joao-M-Silva/padel_analytics](https://github.com/Joao-M-Silva/padel_analytics) — verified OSS CV anchor referenced in the capability map.
4. [padelfip.com](https://www.padelfip.com/) — federation reference for tournament-organiser channel.
5. [playtomic.io/blog](https://playtomic.io/blog) — primary booking-platform reference.
6. [openrouter.ai/api/v1/models](https://openrouter.ai/api/v1/models) — inference-routing API used by the pipeline.
7. [hudl.com/products/assist](https://www.hudl.com/products/assist) — coach-co-pilot reference.
8. [fep.es](https://www.fep.es/) — Spanish padel federation, coach-affiliate channel.
