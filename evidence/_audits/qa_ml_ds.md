# Padel Research OS — Tri-Role Audit

Run under audit: `20260501T135005Z`. Final:
`reports/final/padel-ai-coach-research.html` (~50 KB, 2,035 lines).

---

## QA — pass-with-caveats

Real gates exist; the cracks are at the boundaries.

**Findings**

1. Gate stack is layered. `scripts/run_pipeline.sh:32–48` runs 17 phase
   checkers; `scripts/check_dod.py:7–27` aggregates 20 + `verify_links.sh`.
   Universal checks (first-person, quote dedup, numeric trace, link verify)
   run on every phase (`run_pipeline.sh:79–84`).
2. Link verifier is robust: 3× retry on 000/5xx, slash canonicalisation,
   per-URL HTML cache. Latest run: 78/78 OK in
   `evidence/20260501T135005Z/_logs/verify_links.log` (zero FAIL).
3. Stabilization-cycle is operational.
   `evidence/_failures/2026-05-01_quote_lengths_overreach.md` logs the bug;
   the fix is encoded inline in `scripts/check_quote_lengths.py:11–28`
   (suffix scoping) and `scripts/check_first_person.py:30–34` (URL strip).
4. Reproducibility is asserted but not exercised. `scripts/build_all.sh:6–9`
   claims byte-identical re-runs, but no `tests/` harness diffs against a
   golden, and `.github/workflows/deploy-pages.yml` only uploads to Pages.
   The `_build_*.py` files are static dicts so a re-run passes trivially —
   pipeline drift would not be caught.
5. Gap discipline is uneven.
   `evidence/20260501T135005Z/19_uae_uzbekistan_check.json:24` carries
   `data_gap`. But `15_market_size.json` has no `data_gaps` field at all
   despite the unsourced €22/year ARPU anchor.

**Recommendations**

- Add `tests/test_reproducibility.sh` that hashes every `evidence/<run>/*.json`
  after a clean rebuild and fails on diff.
- Make `data_gaps` a required key on `15_market_size.json` via a new
  `check_market_size.py`.
- Codify €22/year and €7.99/month anchors in `config/sources.yaml` with
  tier_1 URLs.

---

## ML — pass-with-caveats

Reasoning sandwich is implemented and auditable. Hallucination prevention is
layered. Two architectural rules are stated but not enforced: arithmetic
sandboxing and confidence-driven downstream filtering.

**Findings**

1. Model assignments match the stated architecture. Opus on
   `red-team-critic.md`, `canonical-synthesizer.md`, `archetype-synthesizer.md`,
   `deep-research-orchestrator.md`; Haiku on `peer-extractor.md`,
   `report-renderer.md`. Prompt files cross-reference identically.
2. Multi-arm fan-out is sound. `.claude/agents/deep-research-orchestrator.md:15–25`
   defines four independent arms (Sonar Deep, Sonar Pro, Tongyi,
   o4-mini-deep-research) with a no-cross-contamination rule and a 50-call
   loop killer. Twelve arm artifacts in `evidence/.../​_research_arms/`.
3. Yes-man check is enforced as code. `scripts/check_red_team.py:21–22`
   fails the run if every verdict is `pass`; the run has 3 of 6 segments
   at `pass_with_caveats` (`06_red_team.json:5–11`).
4. Confidence scoring is captured but unused.
   `evidence/.../01_job_stories/JS-001.yaml:24` through `JS-004.yaml`
   declare `confidence: 0.30–0.35`, `source: 'assumption'`. No downstream
   filter, weight, or report annotation surfaces this — `canonical_brief.json`
   and the HTML treat these jobs as if validated.
5. The "LLMs do not perform arithmetic" rule (`CLAUDE.md:48`) has no
   enforcement. `scripts/_build_15_market_size.py:9–60` is a `PAYLOAD = {...}`
   literal — numbers are author-typed, not computed. No `python_subprocess_executed`
   flag, no calc.py + output.txt pair, no DoD check distinguishing computed
   vs. asserted numbers.

**Recommendations**

- Surface `confidence` in the HTML next to the `Inference, with caveat` tag
  and fail DoD if any `confidence < 0.5` claim has no open `gaps_to_probe_next`.
- Replace `_build_15_market_size.py`'s static dict with a real
  `market_size_calc.py` that imports inputs from `config/sources.yaml`,
  writes `_calc_output.txt`, and stamps `calculation_method`. Add a
  checker enforcing the stamp.

---

## DS — pass-with-caveats

Sources are tier-tagged; SOM arithmetic is reproducible. The blocking
defect is a silent SAM redefinition between two evidence files; the HTML
uses the larger figure without flagging the swap.

**Findings**

1. SOM math reproduces. 5,000 × €7.99 × 12 = €479,400 (file: €0.48M);
   20,000 × €7.99 × 12 = €1,917,600 (file: €1.92M); annual ARPU €95.88
   matches the €96 anchor.
   `evidence/20260501T135005Z/15_market_size.json:60–67`.
2. SAM is ambiguous and the report quietly picks the larger one.
   `15_market_size.json:46–55` says €380M / 17M players / 8 geos.
   `20_sam_global_market_check.json:51–57` redefines SAM at 21 countries /
   65,965 courts / 29.9M players. The HTML
   (`reports/final/padel-ai-coach-research.html:483, 510, 555`) headlines
   29.9M / €657M without annotating the override.
3. Tier discipline holds for analyst sources. `15_market_size.json:74–135`:
   3× tier_1 (Deloitte/Playtomic, Playtomic 2025, FIP 2025), 5× tier_2
   (InsightAce, Business Research Insights, Market Growth Reports, Grand
   View, Intel Market). No tier_3 leakage.
4. UAE/Uzbekistan check is exemplary methodology.
   `19_uae_uzbekistan_check.json:8–28` documents inclusion (UAE 950 courts
   → INCLUDE; UZ 8 → EXCLUDE) with `verified_quotes`, a `data_gap` note
   for the FIP 2025 PDF, and a `note_on_existing_evidence` reconciling
   the prior padel.fyi figure against FIP.
5. The €22/year ARPU anchor — the multiplier the entire SAM rests on — has
   no source URL at `15_market_size.json:52` ("low end of Strava +
   booking-app combined ARPU"). It is the single largest unsourced
   numerical input in the deliverable.

**Recommendations**

- Add an explicit `sam_versions` array to `15_market_size.json` (v1 =
  priority-geo, v2 = global-court-share) and have the HTML tag which one
  it uses.
- Append `arpu_basis: { eur_per_year: 22, source_urls: [...] }` and fail
  DoD if any €/player number lacks source URLs.
- Add a SAM sensitivity row at €15 / €22 / €30 ARPU so the brittleness is
  visible.
