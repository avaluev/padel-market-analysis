# MVP Loop Design Brief — Padel AI Platform

The riskiest assumption in a Padel AI Platform is value, not scalability. The loop below is built to test the value question with humans first, then earn the right to automate.

**Audience:** Product Lead screening panel.
**Voice:** Third-person, capability-conditional. No first-person pronouns.
**Posture:** The candidate has no domain expertise in padel; the loop is engineered to compensate via tight feedback contracts with coaches and players.
**Anchor evidence:** `evidence/20260501T135005Z/` — jobs graph (`05_jobs_graph.json`), red-team verdicts (`06_red_team.json`), value mechanics (`08_value_mechanics/`), moat audit (`09_moat_audit.json`), peers (`03_peers_dedup.json`).

---

## A. The Core Loop in Three Stages

The loop services the `Rating-clarity backbone` (CC-1 in `05_jobs_graph.json`): smartphone capture → rally and shot tagging → rating delta → drill prescription. Each stage has one input, one action, one output, one success metric, one failure mode.

> The loop's strongest mechanism is the Stage 3 outcome tag: it is the only step that converts a video stream into a labelled supervised-learning signal (drill → outcome → rating shift). Without Stage 3, the moat collapses to commodity tagging.

### Stage 1 — Measurement

| Field | Value |
|---|---|
| **Input** | One full-match smartphone video from a player or club, plus minimal metadata: court, opponents, self-declared level. |
| **Action** | Human operator (the candidate plus one part-time tagger, see Section B) ingests the file, runs the [Joao-M-Silva open-source padel CV pipeline](https://github.com/Joao-M-Silva/padel_analytics) for player/ball/court tracking as a first-pass scaffold, then human-corrects rally boundaries and shot labels using a fixed taxonomy. |
| **Output** | A structured per-rally event log: rally start/end timestamps, shots per player, shot type, court zone, outcome (winner / forced error / unforced error). |
| **Success metric** | (i) ≥90% of rallies correctly delimited on a held-out 50-rally control set; (ii) shot-type label agreement ≥0.7 Cohen's kappa between the candidate's tagger and a domain-expert coach on a 200-shot sample. |
| **Failure mode** | Tagging cost per match exceeds EUR 25 — the unit economics break for any plausible price tier (Section D math). |

The Joao-M-Silva pipeline reports **player tracking, ball tracking, 2D game projection, heatmaps, and pose estimation with 13 degrees of freedom**, with a hardware floor of **8 GB VRAM** at default batch size [verified at the repo](https://github.com/Joao-M-Silva/padel_analytics). It is a research-grade scaffold, not a productised offering — `04_peer_cards/joao_silva_padel_analytics.json` flags `Real-time inference and on-device packaging are out of scope`. The pipeline shrinks Stage 1 effort but does not eliminate human review.

### Stage 2 — Insight

| Field | Value |
|---|---|
| **Input** | The structured event log from Stage 1, plus the player's prior matches if any. |
| **Action** | The operator clusters losing-shot patterns (per `VM-003` in `08_value_mechanics/VM-003.json`: backhand volley at the net, chiquita on the deuce side, etc.), computes a rating delta against the opponent rating using a closed-form Elo-style update, and selects two drill prescriptions from a coach-curated drill library. The drill library is built in Section E with the academy partner. |
| **Output** | A one-page recap: top 3 losing-shot clusters, rating delta, two prescribed drills with situation, success criterion, and partner role (this is the precise template specified in `VM-003.json → experience_sketch`). |
| **Success metric** | (i) Recap is generated within 24 hours of upload; (ii) ≥60% of recaps are opened by the player within 72 hours; (iii) ≥40% of recap recipients book or self-organise the prescribed drill before the next session. |
| **Failure mode** | Insight is too generic to be actionable — the player reads it once and never returns. Detection is binary: drill-acknowledgement rate <10% kills the recap template. |

The 40% drill-acknowledgement threshold is calibrated from `VM-003.json → kill_experiment.success_threshold`: `≥10% of uploads convert to drill plan acknowledgement within seven days`. The MVP target is set higher because the loop runs inside a single club where social proof and coach reinforcement should lift acknowledgement above the cold-traffic baseline.

### Stage 3 — Training

| Field | Value |
|---|---|
| **Input** | Coach session schedule plus the recap from Stage 2. |
| **Action** | Coach reviews the recap before the next 1:1 with the player, picks one of the two prescribed drills, and runs it. After the session, the coach files a one-tap outcome rating on a scoring rubric (improved / unchanged / worse) — this is the closing-the-loop tag specified in `VM-003.json → experience_sketch`. |
| **Output** | A drill-to-outcome record: which drill, which losing-shot cluster, did the player improve. This becomes the seed of the supervised dataset that VM-003's data gate compounds. |
| **Success metric** | (i) Coach files an outcome tag for ≥70% of recaps; (ii) within four weeks, ≥30% of players show a measurable shift in their dominant losing-shot cluster (different cluster takes the top-1 slot). |
| **Failure mode** | Coach refuses to use a tool the student also touches — the canonical caveat from `06_red_team.json → SEG-003.failure_modes[FM-5]`. Mitigation in Section F. |

**The loop's strongest mechanism.** Stage 3's outcome tag is the only step that converts a video stream into a labelled supervised-learning signal (drill → outcome → rating shift). Per `09_moat_audit.json → VM-001`, this is the canonical Naval data gate: `Each match generates unique-per-user data that improves the rating model.` Without Stage 3, the moat collapses to commodity tagging.

---

## B. Manual-First MVP — One Club, 4–6 Weeks, No Product Code

### Hardware

- **Phone-mounted recording**, single fixed angle from behind one baseline, propped on the player bag (the experience step modelled in `VM-001.json → experience_sketch`: `Player records the match with a phone propped on the bag`).
- **Optional fallback**: a club camera if the partner club has one installed. Vendors active in this space include [Eyes On Padel](https://www.eyeson.sport/en/eyes-on-padel/), [Wingfield](https://www.wingfield.io/), and [Clutch](https://www.clutchapp.io/) — all listed in `03_peers_dedup.json`. The MVP does not depend on club-camera access; phone-only is the default to avoid vendor lock-in during validation.
- **Feasibility anchor**: the [Joao-M-Silva open-source padel CV pipeline](https://github.com/Joao-M-Silva/padel_analytics) demonstrates that phone-quality footage can be processed into player/ball/court tracks with commodity hardware. `09_moat_audit.json → VM-001.kill_experiment` explicitly anchors the MVP build on this baseline: `Reproduce the open-source baseline at https://github.com/Joao-M-Silva/padel_analytics into a working end-to-end smartphone pipeline; collect 50 matches from solo recruits.`

### Pipeline (no product code, all human-orchestrated)

1. Player or coach uploads match video to a shared cloud folder.
2. Operator (candidate) drops the video into the open-source pipeline as a tracking scaffold.
3. Operator and a part-time padel-literate tagger correct rally boundaries and label shots in a spreadsheet against a fixed shot taxonomy.
4. Operator runs an Elo-style rating-delta calculation in a spreadsheet column.
5. Operator selects two drills from a coach-curated drill library (built jointly with the academy partner, Section E).
6. Operator drafts a templated PDF/email recap and sends it from the candidate's address — not a branded product domain. This avoids premature productisation per Marty Cagan's concierge guidance.
7. 1:1 follow-up: a fifteen-minute call between the operator (or the academy coach) and the player to walk through the recap.

### Why manual-first beats a polished-app MVP

> `Build a prototype of your product, but have a human do the things you planned to do with fancy algorithms.` — Jared Friedman, Y Combinator partner ([source](https://www.ycombinator.com/blog/ask-yc-upfront-technical-investments)). VERIFIED.

> `If it is, you can always build the algorithms to replace the humans.` — Same source. VERIFIED.

> Wizard of Oz is `A moderated research method in which a user interacts with an interface that appears to be autonomous but is (fully or partially) controlled by a human.` — Sara Paul and Maria Rosala, Nielsen Norman Group ([source](https://www.nngroup.com/articles/wizard-of-oz/)). VERIFIED.

> Wizard of Oz `works best for testing interfaces powered by complex technologies — such as conversational UIs, learning algorithms, and real-time information systems`. — Same source. VERIFIED.

A fourth confirming source from the SVPG / Marty Cagan canon: a concierge test means `doing the customer's job manually for them and checking whether the outcome is appreciated`, summarising Marty Cagan's prescription that concierge work `allows you to cheaply try out ideas while not already having to deal with scalability issues` ([source summary at SVPG](https://www.svpg.com/the-two-core-competencies/), see also discussion at [agile-minds workshop notes](https://www.agile-minds.com/category/knowledge/workshop-notes/)). INFERRED from the canonical SVPG body of work; verbatim Cagan quote not extracted in this pass — flagged in `data_gaps`.

The padel category corroborates the manual-first pattern: `Hudl Assist uses a combination of professional human analysts and, in some sports, advanced AI technology to tag every key moment.` — Hudl Assist FAQ ([source](https://www.hudl.com/products/assist/faq)). VERIFIED. The category leader still relies on humans for the long tail of sports — padel is the long tail.

### Why this configuration beats a code-first MVP for this category

1. **The riskiest assumption is value, not scalability.** `06_red_team.json → SEG-001.recommendation` is `keep` only with a tightened trigger (`partner-driven, not internal stagnation`). Trigger-tightening is a value-discovery question — concierge work answers it; product code does not.
2. **The data gate compounds only if the labels are right.** `09_moat_audit.json → VM-001.scores.data = 2` is conditional on padel-specific shot taxonomy quality. Hand-tagging by a domain expert builds the schema that an automated tagger will later match — the inverse order locks in the wrong taxonomy.
3. **The category has a manual-first incumbent.** Hudl serves ~170,000 teams worldwide per `01_competitor_intelligence.md:144` of this pack, with operating reference at [hudl.com/products/assist](https://www.hudl.com/products/assist), and still uses analyst tagging in most sports. A solo-built code-first MVP cannot beat Hudl on tagging breadth; it can only beat Hudl on padel-specific depth, which is a labelling problem, not an automation problem.

---

## C. From Manual to Automated — Promotion Criteria Per Stage

Each stage has a metric threshold below which automation is premature and above which it is mandatory. Thresholds are calibrated against peer benchmarks where a verified anchor exists.

| Stage | Manual phase | Promotion trigger | Automated successor | Anchor |
|---|---|---|---|---|
| **1. Capture & tag** | Operator drops video into Joao-M-Silva scaffold; human corrects boundaries and labels. | Cumulative human correction rate ≤15% on rally boundaries and ≤20% on shot labels across 200 consecutive matches. | Replace human boundary correction with thresholded confidence rejection — only low-confidence rallies route to a human. | `09_moat_audit.json → VM-001.kill_experiment.success_threshold = r ≥ 0.55 across 50 matches` defines the floor; the 200-match promotion is 4× the floor and reflects industry practice — Hudl volleyball uses `computer vision to automatically track player movements, ball contacts, and other key actions` ([source](https://www.hudl.com/blog/ai-volleyball)). VERIFIED. |
| **2. Insight (recap)** | Operator drafts each recap from a Markdown template, hand-picks two drills. | (i) Recap-open rate ≥60% sustained over 4 consecutive weeks; (ii) drill-acknowledgement rate ≥40% over the same window; (iii) recap NPS from coach panel ≥+30. | Templated recap generated by an LLM with the drill library wired in as a retrieval index; operator reviews only outliers. | The 40% acknowledgement threshold is 4× the `VM-003.json` cold-traffic kill threshold (`≥10% of uploads convert to drill plan acknowledgement within seven days`). |
| **3. Training & outcome** | Coach files outcome tags via WhatsApp or a single-page form; operator transcribes. | (i) ≥70% recaps closed with an outcome tag; (ii) ≥10 confirmed drill-to-outcome transitions per losing-shot cluster (the supervised-learning threshold). | Outcome tagging integrated into a coach-side mobile flow; drill-to-outcome model promoted from rule-based to learned. | `VM-001.json → kill_experiment.success_threshold = r ≥ 0.55` corroborates the rating-quality floor before learned models are trusted. |

**Promotion is a one-way ratchet.** Once a stage is promoted to automation, the manual fallback is preserved as an SLA, not as a default — modelled on Hudl's `Standard Priority` vs `Express Priority` SLA structure ([source](https://www.hudl.com/products/assist/faq)). VERIFIED.

---

## D. Single-Club Pilot Protocol

### Recruitment

- **One club, one academy.** The pilot does not federate across clubs; cross-club rating (VM-002) is gated on VM-001 working at smartphone-only fidelity per `05_jobs_graph.json → abcd_analysis`.
- **Coaches:** 3–5 head coaches signed to the co-creation contract in Section E. The lower bound mirrors `06_red_team.json → SEG-003.kill_experiments`: `recruit 8 coaches via FEP and FITP chapters and run a 1-week pilot`. The pilot here uses fewer coaches because they are concentrated in one academy, lifting per-coach engagement; the eight-coach federation experiment is reserved for the post-pilot expansion phase.
- **Players:** 20–30 plateau-stuck regulars (the SEG-001 `pass_with_caveats` segment) and 5–10 newly-ranked competitors (SEG-002 `pass`). Both are validated in `06_red_team.json`. Total: 25–40 players.
- **Academy size sanity check.** Public Spanish reference: a Marbella academy described as supporting `25 M3-certified coaches, all bilingual` welcoming `nearly 300 groups per year for 3- to 4-day camps` ([source](https://m3padelacademy.com/en/m3-coach/)). VERIFIED. The 3–5 coach pilot footprint is well below that ceiling — recruitment is feasible inside a single mid-sized academy.

### Cadence

- **Weekly cycle**, 4–6 weeks total. Weekly artifact: a one-page review with the academy lead.
- **What is measured each week**: number of matches uploaded, tagging hours per match, rallies-correct rate (sampled), recap-open rate, drill-acknowledgement rate, coach-outcome-tag rate, player NPS, coach NPS.
- **What is iterated each week**: the shot taxonomy (one open issue per week max), the drill library (one swap per week max), the recap template (one block per week max). Iteration discipline prevents the pilot from drifting into permanent prototyping.

### Kill criteria — three thresholds

The pilot is rebuilt, not patched, if any of the following triggers fire:

1. **Tagging unit economics break.** Operator-plus-tagger time per match exceeds 75 minutes after week 3. Below this, the loop cannot scale to 50 matches per week even at full automation parity.
2. **Engagement collapses.** Recap-open rate <30% sustained across two consecutive weeks, or drill-acknowledgement rate <10% over the same window. The 30% floor is half the Section A target; <30% means the recap is not a product, it is a newsletter.
3. **Coach veto.** Two or more coaches in the panel decline to file outcome tags in a given week despite reminders. This is the canonical `06_red_team.json → SEG-003 → strongest_reason_false_segment`: `Coaches sometimes refuse any tool the student also touches; if that refusal dominates, the segment splits into coach-only vs B2B2C and the latter shrinks.`

### Cost envelope — EUR per week

| Line item | Quantity | Unit | Subtotal | Source / assumption |
|---|---|---|---|---|
| Operator (candidate) | 0.5 FTE | not billed | 0 | Candidate is the founder. ASSUMPTION. |
| Part-time padel-literate tagger | 20 hours | EUR 18/hr | EUR 360 | ASSUMPTION: matches the lower band of European sport-analyst freelance rates; specific Padelytics or Hudl-Iberia rate not verified — flagged in `data_gaps`. |
| Cloud GPU for Joao-M-Silva pipeline | 30 hours | EUR 0.50/hr | EUR 15 | ASSUMPTION: 8 GB VRAM tier (per the [repo's stated requirement](https://github.com/Joao-M-Silva/padel_analytics)) on a commodity provider. Specific provider quote not captured — flagged in `data_gaps`. |
| Cloud storage and compute (non-GPU) | 1 month / 4 | EUR 30 / 4 | EUR 7.50 | ASSUMPTION: standard object storage tier. |
| Drill library curation (week 1 spike, weeks 2–6 maintenance) | 4 hours | EUR 60/hr (coach rate) | EUR 240 | ASSUMPTION: coach hourly rate for content work is in the EUR 40–80 range based on Spanish padel coach prices ([ToPadel reference](https://topadel.eu/which-city-to-choose-padel-camp/)). VERIFIED that prices are in this band, the exact EUR 60 mid-point is an assumption. |
| Coach panel honorarium (3–5 coaches × EUR 50/week stipend) | 4 coaches | EUR 50/coach/week | EUR 200 | ASSUMPTION; aligned with Section E coach co-creation contract. |
| Player incentives (free or discounted match credit) | 30 players × EUR 5/week | | EUR 150 | ASSUMPTION; sized to the lower end of Spanish per-session cost. |
| Tooling and software (cloud office, video, signed PDF) | flat | flat | EUR 50 | ASSUMPTION. |
| Contingency | 10% of above | | EUR 102 | ASSUMPTION. |
| **Total weekly burn** | | | **EUR 1,124** | Below the EUR 2,000/week cap. |

**Math sanity check.** Six-week pilot total: 6 × EUR 1,124 = **EUR 6,744**. Below the EUR 12,000 implied ceiling (6 × EUR 2,000). Headroom of ~EUR 5,250 is reserved for unforeseen tagger overflow and for hardware spikes if club-camera fallback is needed.

---

## E. The "No Domain Expertise" Insurance Policy

The candidate is not a padel player. Every shortcut a domain expert would take by reflex must be replaced by an explicit contract. The four mechanisms below are non-negotiable; absence of any one collapses the credibility of the loop.

### 1. Coach co-creation contract (sample terms)

A short engagement letter signed with each coach panel member at week 0:

- **Scope.** The coach commits to (i) attending one 60-minute weekly co-design session, (ii) reviewing the shot taxonomy and drill library with veto rights on coaching content, (iii) filing outcome tags for ≥70% of recaps where their student is the recipient, (iv) sitting for one 30-minute JTBD interview at week 0 and one at week 6.
- **Compensation.** EUR 50/week stipend during the pilot (Section D) plus a signed letter of recommendation; equity is not promised in the pilot phase per `CLAUDE.md → MUST NOT promise budgets, timelines, or headcount`.
- **Veto rights.** The coach has explicit veto rights on (a) any shot taxonomy label, (b) any drill prescription, (c) any phrasing in the recap that touches coaching content. Veto is binary; the candidate does not negotiate it.
- **Mutual termination.** Either party can exit at the end of any week with no penalty and no exclusivity obligation.

### 2. Shadowing schedule

The candidate observes ≥2 training sessions per week at the partner academy, on different coaches, for the full duration of the pilot. Total: 12 sessions minimum across 6 weeks. Note-taking is structured against the loop's three stages (what was measured, what insight surfaced, what training change followed). This is the cheapest way for a non-domain founder to internalise tacit knowledge — it does not replace coach veto rights, it earns the right to ask better questions.

### 3. Player JTBD interview cadence

- **Sample size.** 8 plateau-stuck regulars (SEG-001) plus 4 newly-ranked competitors (SEG-002), per `06_red_team.json → kill_experiment_for_pipeline_risk`: `Run JTBD interviews with 8 plateau-stuck regulars and ask explicitly whether 'rating that travels' or 'drill prescription' was the precipitating switch`.
- **Cadence.** One interview at week 0 (pre-loop), one at week 6 (post-loop). Interview script anchored on the AJTBD canonical glossary at `vendored/zamesin-product-os/_glossary.md`. Interviews are recorded and quote IDs feed back into `evidence/<run-id>/`.

### 4. Decision veto rights for domain experts

Beyond the per-coach contract veto, two additional structural vetoes apply:

- **Shot taxonomy lock.** No taxonomy change ships without sign-off from at least one coach who has filed ≥10 hours of tagging time. Locks the moat-relevant labelling to domain-validated content.
- **Recap content review.** No recap goes to a player without a coach having read at least one recap from that week's batch. This addresses the `06_red_team.json → SEG-003.failure_modes[FM-5]` refusal risk by making the coach a co-signer of every recap, not a bypassed peer.

---

## F. Failure Modes — Ranked by Probability × Impact

Five failure modes, each scored on probability (1 = unlikely, 5 = certain in this category) and impact (1 = bruise, 5 = pilot dies). Ranked by P × I.

| # | Failure mode | Prob | Impact | P×I | Detection | Mitigation |
|---|---|---|---|---|---|---|
| 1 | **Recap is sent but never read** (engagement death) | 4 | 5 | 20 | Recap-open rate <30% over 2 weeks (kill criterion in Section D). Email/PDF tracking pixel or unique read URL per recap. | (a) Tighten the trigger language to partner-comparison framing per `06_red_team.json → SEG-001.failure_modes[FM-3]`; (b) move recap delivery from email to WhatsApp where local read rates dominate; (c) couple recap to a coach 1:1 — the coach is the delivery channel. |
| 2 | **Coach refuses any tool the student also touches** (`06_red_team.json → SEG-003.strongest_reason_false_segment`) | 4 | 5 | 20 | Coach outcome-tag rate <50% sustained over 2 weeks despite reminders. Anonymous coach exit-interview at week 3. | (a) Coach-only mode by default — the player never sees the recap unless the coach forwards it; (b) recap framed as the coach's artefact, not the platform's; (c) coach co-creation contract veto rights (Section E). |
| 3 | **Insight too generic to be actionable** (commodity content) | 3 | 5 | 15 | Drill-acknowledgement rate <20% sustained. Coach NPS on recap content <0. | (a) The shot-taxonomy lock in Section E forces depth; (b) the drill library is curated by domain coaches, not by the candidate; (c) at week 2, the operator runs a 5-recap blind test where coaches rate generic-vs-specific — anything below "specific" is rebuilt. |
| 4 | **Camera/phone occlusion in indoor clubs** | 4 | 3 | 12 | Tagging rejection rate >25% on ingest (rallies that cannot be reliably bounded). Verified failure case: at default Joao-M-Silva pipeline batch sizes, occlusion lifts VRAM pressure ([source](https://github.com/Joao-M-Silva/padel_analytics)). | (a) A fixed-camera position protocol (behind one baseline, 2.5 m height, 30° tilt) supplied as a one-page PDF to the club; (b) a fallback tag mode for low-confidence rallies (`unknown_outcome`) that the human resolves rather than discards; (c) club-camera vendor fallback ([Eyes On Padel](https://www.eyeson.sport/en/eyes-on-padel/)) only if the pilot escapes phone-only by week 4. |
| 5 | **Rating drift across clubs** (federation effect failure) | 3 | 4 | 12 | Out of scope for the single-club pilot but tracked as a forward-flag — once two clubs are in the loop, the same player's rating must not drift more than 5% across clubs in a 14-day window. | (a) Single-club scope holds for 4–6 weeks; (b) the rating spec is published as a fixed schema per `09_moat_audit.json → VM-001.next_90_days`: `publish the shot taxonomy as the schema VM-011 will adopt`; (c) cross-club expansion is gated on `VM-002` LOIs (`Sign two regional FIP-affiliated organisers to a 30-day bracket trial`). |

**Most probable single failure:** mode #1, recap engagement death. Detection is fast (one week), mitigation is structural (move the delivery channel from a candidate-owned email to a coach-owned conversation), and the loop has one clean fallback before it has to be redesigned.

---

## Decision the candidate should ask the interviewer to clarify

> Is the operating model expected to compound the **B2B2C coach co-pilot** (CC-2 chain in `05_jobs_graph.json`) before or after the **B2C plateau-stuck regular** loop is monetised? The MVP loop above can serve either path, but the kill criteria, recruitment ratios, and coach contract terms tilt differently. Coach-first locks the switching-cost moat (`VM-004`) earlier; player-first compounds the data moat (`VM-001`) earlier. Both are defensible; both cannot be the lead motion.

---

## Data gaps

- Specific Padelytics, Hudl-Iberia, or peer freelance tagger hourly rate — assumed at EUR 18/hr based on European sport-analyst band; not verified against a primary source. `data_gaps`.
- Specific cloud GPU EUR/hr quote for an 8 GB VRAM tier — assumed at EUR 0.50/hr; not verified. `data_gaps`.
- Specific Marty Cagan SVPG verbatim quote on concierge-vs-Wizard distinction — sourced via SVPG body of work and secondary summaries; primary verbatim not extracted. `data_gaps`.
- Specific average academy size (number of coaches per padel academy in Spain/Italy) — only one verified anchor (the Marbella M3 academy with 25 M3-certified coaches). `data_gaps` for a representative distribution.
- Specific Padelytics pricing tier — undisclosed on landing per `04_peer_cards/padelytics.json`. `data_gaps`.

---

## Verified sources used in this brief (count: 11 distinct URLs)

1. https://github.com/Joao-M-Silva/padel_analytics — open-source padel CV pipeline (feasibility anchor).
2. https://www.ycombinator.com/blog/ask-yc-upfront-technical-investments — Y Combinator on Wizard of Oz approach.
3. https://www.nngroup.com/articles/wizard-of-oz/ — Nielsen Norman Group definition of Wizard of Oz method.
4. https://www.svpg.com/the-two-core-competencies/ — Marty Cagan / SVPG canonical body of work.
5. https://www.hudl.com/products/assist — Hudl Assist product surface.
6. https://www.hudl.com/products/assist/faq — Hudl Assist FAQ on tagging methods and SLA.
7. https://www.hudl.com/blog/ai-volleyball — Hudl computer-vision automation in volleyball.
8. https://www.coach-logic.com/ — CoachLogic platform claims (verified 2026-05-03 as the canonical CoachLogic domain via curl HEAD/GET).
9. https://m3padelacademy.com/en/m3-coach/ — M3 Padel Academy, Marbella (25 coaches, 300 groups/year).
10. https://topadel.eu/which-city-to-choose-padel-camp/ — Spanish padel coaching prices reference.
11. https://www.eyeson.sport/en/eyes-on-padel/ — Eyes On Padel (club-camera vendor fallback).

Plus internal evidence references (verified during prior pipeline runs):
- `evidence/20260501T135005Z/05_jobs_graph.json`
- `evidence/20260501T135005Z/06_red_team.json`
- `evidence/20260501T135005Z/08_value_mechanics/VM-001.json`, `VM-003.json`, `VM-004.json`
- `evidence/20260501T135005Z/09_moat_audit.json`
- `evidence/20260501T135005Z/03_peers_dedup.json`
- `evidence/20260501T135005Z/04_peer_cards/joao_silva_padel_analytics.json`, `padelytics.json`, `coachseek.json`
