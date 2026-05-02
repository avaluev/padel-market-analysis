# Red-Team Report — Padel AI Platform Interview Pack

**Reviewer voice.** Hostile red-team. Third-person. No diplomacy.
**Pack under review.** `reports/interview_pack/deliverables/01..06_*.md` plus `reports/interview_pack/evidence/*.json`.
**Method.** Each deliverable read line-by-line. Evidence JSON cross-checked against the markdown. Every numeric claim re-computed. Every "verified quote" sampled for provenance integrity. First-person leak audit run via `grep -nE '\b(I|we|my|our|us|me|mine|ours)\b'` on the full deliverables tree.
**Verdict format.** `HIGH | MEDIUM | LOW`. HIGH = a recruiter or founder will catch this on first read and credibility takes material damage.

---

## 1. Severity findings

### HIGH-1. The 30-60-90 plan tests a viral pair-share surface that the MVP design does not build

- **Where.** `reports/interview_pack/deliverables/04_30_60_90_plan.md:101` lists `share_clicked, partner_invited, partner_activated` as instrumented events. `04:160` (productisation table) sets a kill metric of `Pair-level surface drives ≥ 1.5x sharing rate vs single-user baseline`. Hypothesis `H-07` at `04:212` promises to measure this in days 45–60. By contrast `reports/interview_pack/deliverables/03_mvp_loop_design.md:10–48` (the entire core loop) defines a single-player → coach → outcome loop. `03` mentions "partner role" once at line 32 in the context of a drill description (one player among the four on court), never as a viral share surface. There is no recap-share, no partner-invite link, no pair-activation step in the manual MVP.
- **Why this damages credibility.** The competitor brief (`01:111-114` WS-003) names "smartphone-only consumer pair-share" as one of three white-space pillars and a kill metric. The 30-60-90 plan inherits that thesis as a measured hypothesis. The MVP design then quietly drops the pair-share mechanic. A founder reading 03 next to 04 will ask "what surface generates `partner_invited`?" and there is no answer. The interview pack contradicts itself on the wedge thesis it pitched in 01.
- **Fix.** Either (a) add a Stage 2.5 "share to partner" step to `03` with success metric, owner, and detection signal, or (b) cut `share_clicked / partner_invited / partner_activated / H-07` from `04` and admit the pair-viral surface is post-pilot. Pretending the manual loop will produce events the loop does not generate is the most fixable but most embarrassing inconsistency in the pack.

### HIGH-2. A "verified quote" attributed to Foundry CRO is internal product language

- **Where.** `04:121–123` presents this block as a Foundry CRO quote:

  > "At EUR 7.99/month, ≥ 8 percent of activated free users convert to paid within three matches; below 4 percent paid conversion → trigger hedge model (B2B coach SaaS)." Source: foundrycro.com/blog/cac-benchmarks-2026.

  Cross-checked at `reports/interview_pack/evidence/04_30_60_90_plan.json:177` — the same string appears as `verified_quote`. Foundry CRO publishes generic CAC and conversion benchmarks. They do not publish anchor-specific kill thresholds that mention "EUR 7.99/month" or "trigger hedge model (B2B coach SaaS)". The text is internal product language laundered through a Foundry citation.
- **Why this damages credibility.** `CLAUDE.md` Hard Rule states `MUST NOT fabricate quotes` and `MUST tag every factual claim … VERIFIED (URL fetched, content quoted within ±15 words)`. The quote is 32 words. It cannot be on Foundry CRO's published page. It is fabrication of attribution. A founder who clicks the Foundry link will find no such sentence, and the candidate's "anti-hallucination" pitch collapses on the same artefact that pitches it.
- **Fix.** Rewrite the block as: "Internal threshold (synthesised from Foundry CRO 2026 5–9% free-to-paid range): at EUR 7.99/month, ≥8% paid conversion within three matches is keep; <4% triggers hedge model." Remove the quotation marks. Cite Foundry CRO only for the 5–9% range, with the actual verbatim quote that already exists in `evidence/02_subscription_economics.json:180`.

### HIGH-3. Subscription economics (02) and 30-60-90 (04) test a market 02 has not modeled

- **Where.** `02:64-103` enumerates LTV/CAC scenarios for Portugal (EUR 6.49), Spain/Italy (EUR 7.99), and UAE (AED 49). Russia is absent. `04:111-119` then introduces an `RU | Direct-channel | RUB 499/month` smoke-test tier inside Phase B and Hypothesis `H-04` at `04:209` says "Smoke-test paid conversion (ES + RU)". `04:281-287` (R-04 risk) elevates 152-FZ on-device compliance to medium-high risk on the Russian path. The unit-economics document never computes LTV, CAC, or LTV:CAC for the Russian price tier. There is no churn assumption, no FX, no payback window for RUB 499.
- **Why this damages credibility.** A founder running channel decisions will ask "what's the LTV at RUB 499 and what blended CAC clears 3:1?". The pack has no answer. Worse: 04 presents the Russian smoke test as a primary kill/keep gate; running a kill/keep gate against a price the unit economics has not validated is a sequencing error any product lead should catch. The "Russian-speaking direct channel" is referenced consistently across `01:50, 01:108, 01:113, 04:111, 04:281, 05:183` but the financial model in `02` is silent on it. Cross-doc consistency fails on the candidate's own primary geography sub-thesis.
- **Fix.** Add a fourth scenario to 02 Section C: ARPU EUR equivalent of RUB 499 at the published 0.55 PPP index in `evidence/20260501T135005Z/10_monetization.json:140-142`, with explicit churn assumption (the Russian path has no Strava-class flywheel data, so 8-9% upper band is the honest setting), CAC stack including the Telegram-only constraint (no Apple Search Ads, no Meta), and the resulting LTV:CAC. If LTV:CAC organic does not clear 3:1 at honest churn, demote H-04 to a fact-finding test only and remove it as a kill gate.

### HIGH-4. Two competitor pricing claims are anchored to fabricated "verified quotes"

- **Where.** `01:63` (Clutch): the deliverable cites `"Clutch club tier published in vendor capture" — clutchapp.io` as the verbatim quote anchoring the EUR 53/month price. `evidence/01_competitor_intelligence.json:132-138` confirms this: the `verified_quote.text` field is literally the descriptive phrase "Clutch club tier published in vendor capture" with `source_url: clutchapp.io` and the next field admits the source is `evidence/20260501T135005Z/10_monetization.json price_benchmarks; price_anchor labelled 'around EUR 53/month per club tier per Sonar pricing capture'`. The Sonar capture is paraphrased numbers from a Perplexity search, not a verbatim screenshot of a clutchapp.io price card. Same pattern at `02:23` for Clutch (status: VERIFIED — internal capture), `02:25` for MATCHi (EUR 107/month "internal capture").
- **Why this damages credibility.** A founder running diligence on Clutch's pricing will look at clutchapp.io, find no public EUR 53/month tier, then look at the candidate's "verified quote" field and see a placeholder phrase. The pack admits the quote is not on the vendor page (DG-2, DG-3 in 01; DG-03, DG-04 in 02), but still tags it `VERIFIED`. The disclosure is buried in a data-gap table while the headline tag stays VERIFIED. This is exactly the citation-without-evidence pattern `CLAUDE.md` Hard Rules forbid (`MUST NOT cite a URL without storing the fetched response in evidence/`).
- **Fix.** Change tag from `VERIFIED` to `INFERRED` (Sonar paraphrase) on every internal-capture price. Remove "verified_quote" placeholders that are not vendor-page text. Add the Sonar-derived nature to the cell, not just to a footnote at the bottom.

### HIGH-5. Padelytics vs Playtomic pricing-disclosure stories contradict each other across deliverables

- **Where.** `01:84` (Playtomic): "Tier numeric pricing is gated behind a sales conversation; logged as DG-3." `02:26` (Playtomic): pricing is `USD 37 / 109.08 / 274 per month per club` with a `"Standard $37 / Professional $109.08 / Champion $274 monthly"` quote tagged `VERIFIED`. The two evidence files agree on this conflict: `evidence/01_competitor_intelligence.json:208` says `"data_gap": "Tier numeric pricing is gated behind sales conversation"` while `evidence/02_subscription_economics.json:118-129` lists the actual numbers with `verification_method: WebSearch 2026-05-03 cross-checked products.playtomic.io/playtomic-manager`.
- **Why this damages credibility.** The two deliverables run on the same 2026-05-03 verification day and reach opposite conclusions on whether Playtomic prices are public. A reviewer who reads the pack in order (01 → 02) will ask "did the candidate not check 02 before writing 01?" The pack is internally fact-checking itself wrong.
- **Fix.** Update `01` Playtomic pricing block to match `02`. Move DG-3 to "individual tier breakdown not displayed on pricing landing without account creation, but per-tier monthly figures are surfaced on `products.playtomic.io/playtomic-manager`". Cite the secondary URL.

### HIGH-6. The MVP loop's "Hudl scale" claim is sourced to CoachLogic's data

- **Where.** `03:88` reads: "Hudl, with `40K Registered Users` across `30 Countries Worldwide` (per coach-logic.com for the adjacent CoachLogic comparison; Hudl scale verified independently at hudl.com/products/assist), still uses analyst tagging in most sports." The 40K / 30 countries figures come from `coach-logic.com` per `03:220` and `evidence/03_mvp_loop_design.json:485-486`. CoachLogic is a separate, much smaller competitor (covered at `01:150` as an academy/LMS adjacency). Hudl's Assist FAQ does not surface 40K users / 30 countries; that is CoachLogic's claim, not Hudl's. The parenthetical "Hudl scale verified independently at hudl.com/products/assist" provides no Hudl-specific number.
- **Why this damages credibility.** Hudl's actual scale is ~170K teams (cited correctly elsewhere in `01:144` as `170,000+ teams`). A founder familiar with the sport-tech category will know CoachLogic and Hudl are not the same vendor and that Hudl is two orders of magnitude larger than 40K users. Attributing CoachLogic's scale to Hudl reads as either careless cross-reference or padding the manual-first argument with a number that doesn't fit. Either way the moment falsifies the candidate's "data discipline" pitch live in front of the reviewer.
- **Fix.** Replace the Hudl scale parenthetical with the verified figure that already exists in the pack: `Hudl ~170,000 teams worldwide` per `01:144`. Move the CoachLogic 40K / 30-countries figure to its proper home (CoachLogic LMS comparison), or delete it.

---

### MEDIUM-1. UAE CAC arithmetic violates the Python-sandbox rule

- **Where.** `02:99`: `EUR 121.66 | 94 × 1.4 / 1.085 = 121.66`. Re-run in Python: `94 * 1.4 / 1.085 = 121.290…`. The deliverable's stated formula does not produce the stated result. The downstream LTV:CAC paid for UAE (1.67) was computed against the wrong CAC; the right number gives 1.68.
- **Why this matters.** `CLAUDE.md` Hard Rule: `MUST run every numeric calculation through the Python sandbox. LLMs do not perform arithmetic.` A 0.4-EUR error is small, but the existence of the error proves the sandbox rule was not followed. A founder running the 30-second arithmetic check on the most-quoted scenario row catches it.
- **Fix.** Replace EUR 121.66 with EUR 121.29 throughout `02` and `evidence/02_subscription_economics.json:312`. Re-state the LTV:CAC paid UAE as 1.68. Add a comment in the JSON `paid_meta_uae_uplift_calc` that the figure was Python-recomputed.

### MEDIUM-2. F5 retention benchmark inflates the Foundry CRO range with no shown derivation

- **Where.** `02:44` claims F5 (paid month 1 → paid month 3) is **"~50–60% inferred from sport-tech 12-month range 35–45%"**. Tag: `VERIFIED_INHERITED`. The Foundry CRO source (`evidence/02_subscription_economics.json:200-201`) shows 35-45% for **12-month** retention. The inference 35-45% (12mo) → 50-60% (90-day) is asserted with no math. Standard cohort decay would put 90-day retention substantially higher than 12-month, but the candidate did not show the derivation.
- **Why this matters.** The 50-60% figure feeds the LTV math indirectly via the retention story, and the deliverable presents it as a benchmark when it is in fact an internal extrapolation. A reviewer will ask: "what survival curve assumption gets you from 35-45% at 12mo to 50-60% at 90 days?". The pack has no answer in `02`. The pack has the right disclosure ("inferred"), wrong tag (VERIFIED_INHERITED).
- **Fix.** Either (a) show the derivation explicitly (e.g., "assumes monthly churn ≤7%, then 90-day survival = (1-0.07)^3 ≈ 80%; 50-60% is the conservative lower band"), or (b) demote the tag to `INFERRED` and remove it from the LTV scenarios as a load-bearing input.

### MEDIUM-3. The Whoop drill-prescription "verified quote" was lifted from a third-party marketing page

- **Where.** `02:125` cites *"Whoop personalises strain and recovery guidance per member"* with anchor URL `whoop.com/us/en/membership/`. `evidence/02_subscription_economics.json:395-398` reveals the actual `primary_analogue_source` is `https://wellness.alibaba.com/fitlife/whoop-membership-pricing-guide` — an Alibaba-hosted third-party affiliate page, not Whoop. The whoop.com URL is in the deliverable; the actual quote source is not.
- **Why this matters.** This is citation laundering: the deliverable cites the vendor URL while the actual source is a third-party SEO page. A reviewer who clicks `whoop.com/us/en/membership/` and Ctrl-F's "personalises strain and recovery guidance per member" will not find it. The pack also tags the lever as `INFERRED` (correctly) but the verbatim phrasing format suggests verbatim sourcing.
- **Fix.** Cite the Alibaba wellness page as the analogue URL and openly mark it as "third-party paraphrase of Whoop coaching surface". Or pull the actual Whoop verbiage from `whoop.com/us/en/membership/` and replace the quote.

### MEDIUM-4. CoachLogic URL is inconsistent across deliverables

- **Where.** `02:128` and `04:130` cite `coachlogic.com`. `03:88` and `03:220` cite `coach-logic.com`. `01:150` cites `coachlogic.com`. Two different domains for the same company across the same pack.
- **Why this matters.** A founder reviewing the URL register at the back of each deliverable will assume the candidate did not run `verify_links.sh` consistently across files. If only one of the two is the real domain, the other returns 404 and the pack fails its own MUST-rule (`MUST run verify_links.sh and exit clean`).
- **Fix.** Pick one domain (real CoachLogic homepage is `coach-logic.com` as of late-2025 documented public state, but verify with `curl -sI` once on the live URL), update everywhere, and add it to the URL whitelist for `verify_links.sh`.

### MEDIUM-5. The Whoop pricing claim contradicts the JD-coverage anti-fabrication self-pitch

- **Where.** `02:20` cites Whoop One/Peak/Life at `USD 199 / 239 / 359 per year (annual-only billing)` with quote *"WHOOP One $199 / Peak $239 / Life $359 per year"* tagged VERIFIED. The Whoop public pricing surface (https://www.whoop.com/us/en/membership/) prices vary over time and the WHOOP 5.0 launch (Q2 2025) introduced a different tier set than One/Peak/Life. If the page now reads "Performance" or "WHOOP 5.0 Members", the verbatim claim no longer matches and the candidate's own anti-hallucination guarantee fails on a 30-second click.
- **Why this matters.** This is a re-verification risk inherent to vendor pricing. The pack has not surfaced a captured-at-2026-05-03 screenshot in the deliverable text (the screenshot is in `screenshots/whoop.png`, but the deliverable does not state the Whoop tier set was unchanged from a captured baseline). A recruiter who clicks the link a week later may find different pricing.
- **Fix.** Add a "captured-on" timestamp inline next to every vendor-priced verbatim quote in `02` table, with a 7-day re-verification SLA. For Whoop specifically, screenshot the support page (which `evidence/02_subscription_economics.json:44` already cites as secondary) and link to the screenshot artefact.

### MEDIUM-6. The PlaySight USD 82M acquisition figure is presented as transaction value when the source qualifies it

- **Where.** `01:167` reads: `acquired by Slinger Bag (now Connexa Sports) in October 2021 in a transaction estimated at USD 82 million before earnout based on Slinger's previous market close share price`. The 82M is stated, then the deliverable adds the qualifier. But the section header "Pivot signal" treats the deal as a meaningful failure data point. The Slinger press release at the cited URL describes the deal as a stock-for-stock structure where the headline figure is a fluctuating implied value based on Slinger's share price at signing — Slinger's share price subsequently collapsed (the company eventually delisted and rebranded to Connexa). The "82M transaction value" is therefore technically a peak-implied number, not a realised consideration.
- **Why this matters.** A reviewer with M&A literacy will ask "what was the actual cash value?". The pack does not disclose Slinger's stock-price collapse and the corresponding mark-down on PlaySight's effective sale price. Selectively quoting the peak-implied value to bolster the "graveyard signal" framing is rhetorically convenient but factually thin.
- **Fix.** Add one sentence noting Slinger's stock-price subsequent collapse, the Connexa rebrand, and that the realised consideration was below the headline 82M peak-implied. Cite a follow-up news source.

### MEDIUM-7. First-person voice leak inside the WTP survey question

- **Where.** `02:167` quotes the survey question: *"If your booking app published a derived rating, would you still pay EUR 7.99 for ours?"* The word `ours` is a first-person possessive. Run: `grep -nE '\b(I|we|my|our|us|me|mine|ours)\b' reports/interview_pack/deliverables/02_subscription_economics.md` confirms the leak at line 167 (other matches at lines 20, 125, 195 are URL false-positives `whoop.com/us/en/`; matches in `03` lines 181, 183 are `P × I` math notation false-positives; match in `06:19` is `I_peers_reasoning.json` filename).
- **Why this matters.** `CLAUDE.md` Hard Rule: `MUST NOT use first-person pronouns (I, we, my, our) anywhere in reports/`. The leak is one word, but the candidate's interview pitch (`05`) advertises "Voice discipline (third-person, no first-person leaks) is enforced by the candidate's own pipeline as a hard gate". A reviewer running `grep -nE` lives the contradiction. The pack fails the candidate's own gate.
- **Fix.** Rewrite the survey question to: *"If your booking app published a derived rating, would users still pay EUR 7.99 for the candidate platform?"* Or: *"would you still pay EUR 7.99 for the alternative product?"* Then re-run the grep and verify zero leaks.

---

## 2. Fabrication risk register

A fabrication risk is a claim that *looks sourced* but isn't, OR a number whose source URL says something different.

### F-1. Foundry CRO "kill threshold" quote is a fabricated attribution

- **Where.** `04:121-123`. Verbatim cited as a Foundry CRO statement; the language is internal product policy, not generic CAC benchmarks.
- **Verification command.**
  ```bash
  curl -s 'https://foundrycro.com/blog/cac-benchmarks-2026/' | grep -i "EUR 7.99\|trigger hedge model\|three matches"
  ```
  Empty output expected.
- **Status if confirmed.** HIGH severity (already counted in HIGH-2). Caught by any reader who clicks the source URL.

### F-2. Clutch / MATCHi "verified quotes" are placeholders, not vendor-page text

- **Where.** `evidence/01_competitor_intelligence.json:132-138` (Clutch) and `evidence/02_subscription_economics.json` (MATCHi).
- **Verification command.**
  ```bash
  curl -s 'https://www.clutchapp.io/' | grep -i "club tier\|EUR 53\|€53"
  curl -s 'https://matchi.com/' | grep -i "Business\|EUR 107\|€107\|per court"
  ```
  Empty output expected.
- **Status if confirmed.** HIGH severity (already counted in HIGH-4). The "verified quote" placeholders are an admission that the price was Sonar-paraphrased, not vendor-page-captured.

### F-3 (additional). Foundry CRO "USD 12 newsletter CAC" has no quote in the evidence

- **Where.** `02:114` references `published Foundry CRO USD 12 newsletter CAC`. `evidence/02_subscription_economics.json:240-242` lists `"organic_newsletter_calc": "USD 12 / 1.085 = 11.06"` and `"organic_newsletter_source": "https://foundrycro.com/blog/cac-benchmarks-2026/ — newsletter benchmark USD 12"` — but no `verified_quote` field for the USD 12 figure itself. The funnel section of the same JSON file has verified quotes for the 6.6%, 30-50%, 5-9%, 1.7% benchmarks; the USD 12 figure is asserted with no quote.
- **Verification command.**
  ```bash
  curl -s 'https://foundrycro.com/blog/cac-benchmarks-2026/' | grep -i "newsletter\|USD 12\|\$12"
  ```
  If empty, the USD 12 was paraphrased without a verbatim source — same fabrication pattern as F-1.
- **Status.** Re-classify as MEDIUM unless `curl` returns substantive matches.

---

## 3. Survivorship bias check

The competitor brief at `01:163-179` presents only two graveyard entries: PlaySight (acquired into Slinger Bag, 2021) and Wingfield (multisport sprawl, *not actually dead*).

**Findings.**

- The PlaySight entry is the only genuinely-dead-or-absorbed comp in the pack. Wingfield is alive and selling. There is no failed *padel-AI* startup in the graveyard — every padel-native vendor named in 01 (Padelytics, Clutch, SPASH, Eyes On Padel, PadelPlay, Aiball, Court Sense, Padelboard, Padelstats, Padel Radar, Joao-M-Silva academic) is presented as alive. That is statistically implausible for a 2024–2026 vintage of CV/AI sport startups; some of them must have stalled, pivoted, or wound down.
- `01:21–29` ("Why these three, and why not others") deselects six peers but classifies all of them as alive. None are deselected for being dead.
- The pack does cite `06_red_team.json` SEG-001 SEG-003 segment kills internally, but those are *segment* kills, not *competitor* deaths.

**Why this is a survivorship-bias signal.** A founder who spent any time in padel-tech in 2024–2025 saw at least one or two consumer-app launches lose runway. Their absence from the graveyard suggests the candidate's source pool (`03_peers_dedup.json`) is winners-only.

**Fix.** Surface at least one additional graveyard entry: a winding-down padel app, a pivoted match-recording startup, or a Kickstarter-funded racket-sensor that did not ship. If the source pool genuinely contains no dead padel-AI competitors, state that explicitly as a research limitation in `01` rather than letting the absence read as cherry-picking.

---

## 4. Cross-document consistency

| Question | Answer | Evidence |
|---|---|---|
| Does 02's churn assumption match 04's? | **Mostly yes.** 02:69-96 uses 6-9% monthly churn (8% Lean, 7% Anchor, 6% Premium). 04:239 references the same 6-9% range from 10_monetization. | OK |
| Does the WTP threshold in 04 match 02's pricing anchor? | **Partial mismatch.** 04:121 quotes a Foundry CRO "kill threshold" of <4% paid; 02:42 lists 5-9% Foundry CRO range with the 4% kill threshold appended in narrative. The numerical thresholds line up, but 04 dresses the threshold as a Foundry quote while 02 marks it correctly as inherited from `10_monetization`. | Inconsistent presentation; same number. |
| Does the MVP loop in 03 deliver the metrics 04 promises to track? | **NO.** See HIGH-1. 04 instruments `share_clicked / partner_invited / partner_activated / drill_acknowledged / recap_opened`. 03 builds only `recap_opened / drill_acknowledged / coach_outcome_tag`. Pair-share surface is absent in 03. | Major gap. |
| Is the Russian-speaking direct channel referenced consistently? | **Referenced consistently in the rhetoric, modeled inconsistently.** Mentioned in 01:50/108/113, 04:111-119/281-287, 05:183. Modeled financially in `evidence/20260501T135005Z/10_monetization.json` (RUB 499) but not in `02` LTV/CAC scenarios. | Cross-doc gap, see HIGH-3. |
| Do 01 and 02 agree on Playtomic pricing disclosure? | **NO.** See HIGH-5. 01 says gated. 02 says VERIFIED. | Material contradiction. |
| Do CoachLogic URLs match across 01/02/03/04? | **NO.** See MEDIUM-4. Two different domains (`coachlogic.com` vs `coach-logic.com`) used. | Verify-links risk. |
| Do drill-acknowledgement thresholds match across 03 and 04? | **No, but defensibly.** 03:33 says 40% (single-club pilot target). 04:159 says 10% (productisation gate, lower bar from VM-003 cold-traffic). The two are stage-different (pilot vs productisation), but the deliverables do not call out the staged thresholds. A reviewer reading both will ask "which 40% / 10% applies when?". | Documentation gap, not arithmetic gap. |

---

## 5. First-person leak audit

Command run: `grep -nE '\b(I|we|my|our|us|me|mine|ours)\b' reports/interview_pack/deliverables/*.md`.

| Line | Match | Verdict |
|---|---|---|
| `02:20` | `whoop.com/us/en/` | URL false-positive. |
| `02:125` | `whoop.com/us/en/` | URL false-positive. |
| `02:167` | `for ours?` (inside survey question) | **REAL LEAK.** See MEDIUM-7. |
| `02:195` | `whoop.com/us/en/` | URL false-positive. |
| `03:181` | `P × I` (math notation) | False-positive. |
| `03:183` | `P × I` (table header) | False-positive. |
| `06:19` | `I_peers_reasoning.json` (filename) | False-positive. |

**Net result.** One real first-person leak (`02:167`). Six false-positives. The candidate's own self-claim ("zero first-person leaks enforced as hard gate") is contradicted by the artefact. Fixable in one line.

---

## 6. The "founder will ask this" list — eight questions

For each: the question, the strongest current answer in the pack, the gap if answered honestly.

### Q1. "If you've never played padel, why is your shot taxonomy correct?"

- **Strongest current answer.** `03:151-176` — coach co-creation contract with veto rights on every taxonomy label, plus a shadowing schedule of ≥2 sessions per week × 6 weeks. `05:166-174` (NTH-4 Pivot 1) frames the gap as a fresh-JTBD-lens advantage.
- **Gap if honest.** The taxonomy ships *without* coach veto in the first iteration of the MVP because the coach is recruited at week 0–1 of the pilot, not before the pack ships. If the interviewer asks "show me the taxonomy as it stands today, before the coach signs the contract", the answer is "it's a draft against the open-source pipeline labels and Decorte CVPR 2024 paper". That is honest but thin.

### Q2. "Padelytics is shipping. What stops them from adding a cross-club rating in 6 months?"

- **Strongest current answer.** `01:49` (Blind spot 1) — no cross-club rating spine because the network mechanic is unstaked; landing a tournament-organiser LOI before Padelytics moves owns the spine. `04:181-189` (C.5 rating-platform decision memo) gives a 12-week LOI window.
- **Gap if honest.** Padelytics already has Iberian/LATAM club distribution; if a competitor landed an LOI first, Padelytics could counter-bundle "free derived rating with your existing Padelytics Pro subscription" and the candidate's distribution moat (a Spanish + Russian newsletter) is slower to compound than Padelytics' pre-existing club roster. The pack does not model the speed of Padelytics' counter-move.

### Q3. "Your LTV:CAC at paid Meta is 1.32x at the anchor and 0.94x in worst case. Why isn't paid Meta dead in the water?"

- **Strongest current answer.** `02:112` — paid Meta is treated as a hedge above EUR 7.99 anchor at churn ≤7%. The interpretation paragraph correctly says paid Meta is net-positive only above the anchor.
- **Gap if honest.** A 1.32x LTV:CAC paid does not pay back inside any reasonable subscription window when payback period is the 6-12 months a B2C subscription typically targets. The candidate has not computed payback period anywhere in `02`. The implication is that paid Meta is an experimental channel, not a scaling channel — but the wording in `02:112` is ambiguous on which.

### Q4. "Walk me through the math: how does a 90-day cohort move to a 12-month cohort at 6-9% monthly churn?"

- **Strongest current answer.** `02:59` — `average_lifetime_months = 1 / monthly_churn_rate`. The formula assumes a flat exponential churn process. At 8% monthly churn, lifetime = 12.5 months and 12-month survival = (1-0.08)^12 ≈ 36.7%, which lands inside Foundry CRO 35-45% — internally consistent.
- **Gap if honest.** The flat-churn assumption is wildly inappropriate for a sport-tech subscription with seasonal churn (FM-103, the 2-3x Q4 multiplier the candidate explicitly flags as the most-critical data gap). A founder will ask "what's your churn curve, not your average?" — the pack has only the average. The honest answer is that the math is a point-estimate; the real curve is data the candidate would instrument first and scale later.

### Q5. "Show me the OSS pipeline running on club footage. What's the actual accuracy?"

- **Strongest current answer.** `03:24` flags Joao-M-Silva pipeline as research-grade with 8 GB VRAM floor. `04:257-263` (R-01) acknowledges the OSS pipeline cannot reach acceptable accuracy is the rank-1 risk. `04:270` says accuracy validation runs in week 1 of phase A.
- **Gap if honest.** Accuracy validation has not been run yet. The pack is research, not a working prototype. If the founder asks for a video demo, the candidate has nothing to show. The honest answer is "the validation is week 1 of the role, not pre-call". This may or may not be acceptable depending on the founder's expectations.

### Q6. "Why FIP/national federation LOIs and not something faster?"

- **Strongest current answer.** `04:181-189` — Option A is FIP-affiliated organiser integration, two LOIs in 6 weeks. Option B is derived-only rating on smartphone footage. Branch logic at `04:188-189`.
- **Gap if honest.** Federation LOIs are not the fastest path; they are a *legibility* path. A faster path would be partnering directly with one club coach and one league captain (a "league of friends" play — tournament-by-tournament). The pack does not consider this option. The reviewer may push: "have you mapped the smaller social paths between organisers?" — answer is no, and the federation path is over-indexed because it sounds important on paper.

### Q7. "What's your competitive response if Playtomic ships a derived rating tomorrow?"

- **Strongest current answer.** `02:163-167` (FM-102) — kill experiment that surveys 200 Playtomic/MATCHi power users on whether they would still pay if their booking app published a derived rating; threshold ≥30% retain WTP. `01:90` — Playtomic's self-declared rating is a structural credibility gap.
- **Gap if honest.** The 30% retention threshold is not anchored to anything but the candidate's intuition; there is no benchmark, no peer survey, no Strava-vs-Garmin parallel. A founder will ask: "at what retention does the wedge survive — 50%? 30%? 10%?". The pack has 30% but no defense of why 30%.

### Q8. "You promote 'kill criteria' as a discipline. Show me the kill criterion that fired and pivoted you in this very pack."

- **Strongest current answer.** `06_red_team.json` (referenced from `04:51-60`) lists segments killed (SEG-004 club operator, SEG-006 injury-aware returner) and merged (SEG-005 → SEG-001). The pack does demonstrate it has used kill criteria.
- **Gap if honest.** The pack pre-dates execution. Every kill criterion fired in *segment selection*, not in *experimentation*. A founder will ask: "what experiment have you run that killed an idea?". The honest answer is none — this is research, not execution. The candidate has used kill criteria as a *frame*, not as a *practice*. Pivot 3 in `05:243-249` advertises pre-declared kill criteria, which is honest but distinct from a track record of bets killed in flight.

---

## 7. The "kill the pack" verdict

**Question.** If one of the six deliverables had to be deleted to make the pack stronger, which?

**Verdict.** **Delete `06_model_provenance.md`.**

**Why.** `06` is the only deliverable that does not earn its slot. The other five are job-relevant evidence: 01 = competitor intelligence, 02 = unit economics, 03 = MVP design, 04 = 30-60-90 plan, 05 = JD coverage map. A founder hiring a Product Lead reads each one and gets value. `06` is meta — it explains the model split inside the candidate's research pipeline. That is interesting to a Claude / ML reviewer; it is *signal noise* to a hiring panel for a Product Lead. The radical-transparency framing reads as defensive posture ("here is what was not hidden"), and it draws attention to a non-issue: nobody asked which model produced the research, but `06` insists the answer matters. The pack is materially stronger if `06` is folded into the methodology footer of the public portfolio (one paragraph) and the deliverables tree shrinks to five.

**Counter-argument considered.** `06` exists to demonstrate citation discipline. The discipline is better demonstrated *inside* the live evidence trail of `01-04` (every claim cites a source URL and an evidence file), not as a separate provenance doc. Deleting `06` reduces noise without reducing signal.

**Why each of the other five earns its slot.**

- **01** is the strongest single-deliverable answer to "do you understand the competitive landscape?". It is the only document in the pack that names PlaySight's pivot, Wingfield's tennis-first posture, and the seven moat classes. Cuttable issues are real (HIGH-4, HIGH-5, HIGH-6, MEDIUM-6, survivorship-bias gap), but the artefact category is essential.
- **02** is the only document with explicit LTV/CAC math. The JD requires unit economics literacy. Cut 02 and the candidate has no quantitative answer to "show me the model".
- **03** is the only document showing how the candidate would actually *operate* in the first 6 weeks. Without 03, the pack reads as analysis with no execution surface. Major issue is HIGH-1 (pair-share gap), but the document type is essential.
- **04** is the only document tying everything to a calendar. Required by the role.
- **05** is the only document explicitly addressing the JD bullet-by-bullet. Without 05 the candidate is asking the recruiter to do the JD-mapping work.

---

## Appendix A — Verification commands run during this review

```bash
# First-person leak audit (RAW)
grep -nE '\b(I|we|my|our|us|me|mine|ours)\b' \
  /Users/sxope/Documents/2026/Research/28.Padel/Claude/padel-research-os/reports/interview_pack/deliverables/*.md

# Cross-doc Russian / 152-FZ presence check
grep -n "Russian\|152-FZ\|Telegram\|RUB" \
  /Users/sxope/Documents/2026/Research/28.Padel/Claude/padel-research-os/reports/interview_pack/deliverables/*.md

# Arithmetic re-run on LTV/CAC (Python sandbox)
python3 -c "print(94*1.4/1.085)"        # UAE CAC: 121.29 vs claimed 121.66
python3 -c "print(round(7.99*14.29,2))" # LTV Anchor
python3 -c "print(round(64.90/86.64,2))"# LTV:CAC paid Worst

# Cost-envelope arithmetic
python3 -c "
items = [0, 360, 15, 7.5, 240, 200, 150, 50]
sub = sum(items); con = 0.10*sub
print(sub, con, sub+con)
"  # Subtotal 1022.5 / contingency 102.25 / total 1124.75

# Playtomic / Padelytics pricing disclosure cross-check
grep -nE 'pricing|verified_quote|tier_disclosed' \
  /Users/sxope/Documents/2026/Research/28.Padel/Claude/padel-research-os/reports/interview_pack/evidence/01_competitor_intelligence.json

# Provenance arms model split check
for f in /Users/sxope/Documents/2026/Research/28.Padel/Claude/padel-research-os/evidence/20260501T135005Z/_research_arms/*.json; do
  echo "$(basename $f): $(grep -oE '"model":"[^"]*"' $f | head -1)"
done
# Confirms 11 of 12 arms on Perplexity Sonar variants; 1 on Tongyi.

# To run before the next ship of the pack — verify external citations
curl -s 'https://foundrycro.com/blog/cac-benchmarks-2026/' \
  | grep -i "EUR 7.99\|trigger hedge model\|three matches"   # F-1 verification
curl -s 'https://www.clutchapp.io/' \
  | grep -i "club tier\|EUR 53\|€53"                          # F-2 Clutch verification
curl -s 'https://matchi.com/' \
  | grep -i "Business\|EUR 107\|€107\|per court"              # F-2 MATCHi verification
curl -s 'https://foundrycro.com/blog/cac-benchmarks-2026/' \
  | grep -i "newsletter\|USD 12\|\$12"                        # F-3 verification
```

---

## Appendix B — Issue summary table

| ID | Severity | One-line issue | File:Line |
|---|---|---|---|
| HIGH-1 | HIGH | MVP loop omits pair-share surface that 04 instruments and tests | `04:101,160,212` vs `03:10-48` |
| HIGH-2 | HIGH | Foundry CRO "verified quote" is internal product language | `04:121-123` |
| HIGH-3 | HIGH | 02 does not model the Russian price tier that 04 smoke-tests | `04:111-119,209` vs `02:64-103` |
| HIGH-4 | HIGH | Clutch/MATCHi prices tagged VERIFIED with placeholder quotes | `01:63`, `02:23,25` |
| HIGH-5 | HIGH | 01 says Playtomic prices gated; 02 lists them as VERIFIED | `01:84` vs `02:26` |
| HIGH-6 | HIGH | CoachLogic's 40K/30-countries figure attributed to Hudl | `03:88` |
| MED-1 | MEDIUM | UAE CAC arithmetic 94×1.4/1.085 ≠ 121.66 (real: 121.29) | `02:99` |
| MED-2 | MEDIUM | F5 retention 50–60% inferred from 35–45% with no shown derivation | `02:44` |
| MED-3 | MEDIUM | Whoop drill-prescription quote sourced from third-party Alibaba page | `02:125` vs `evidence/02:395-398` |
| MED-4 | MEDIUM | CoachLogic URL inconsistency (`coachlogic.com` vs `coach-logic.com`) | `01:150,02:128,03:88,04:130` |
| MED-5 | MEDIUM | Whoop One/Peak/Life pricing risk (5.0 launch may have changed tiers) | `02:20` |
| MED-6 | MEDIUM | PlaySight USD 82M = peak-implied stock value, not realised cash | `01:167` |
| MED-7 | MEDIUM | First-person leak `ours` inside survey question | `02:167` |
| F-1 | (HIGH) | Foundry CRO "kill threshold" attribution (verification command provided) | `04:121-123` |
| F-2 | (HIGH) | Vendor-page "verified quotes" that aren't on the vendor page | `01:63`, `02:23,25` |
| F-3 | (MED) | Foundry CRO USD 12 newsletter CAC has no verbatim quote in evidence | `02:114` |

---

## Appendix C — Caption-image mismatch noted during read

`01:254-256` — the screenshot file is `screenshots/padelfip.png` but the caption reads "Eyes On Padel parent · Wingfield-style installations and PadelFIP rating authority context". The caption conflates Eyes On Padel (a vendor at `eyeson.sport`) with PadelFIP (the federation). No `eyeson.png` is present in `screenshots/`. Fix: either add an Eyes On Padel screenshot, or rewrite the caption to be PadelFIP-only.
