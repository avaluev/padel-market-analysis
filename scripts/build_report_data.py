#!/usr/bin/env python3
"""Aggregate every phase output into reports/<run-id>/data.json for the
HTML renderer. Adds a `human` layer that the template uses directly so
no jargon, no internal IDs, and no `{{#if}}` conditionals leak through.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys


def load_json(p: pathlib.Path):
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[build_report_data] WARN: {p}: {e}", file=sys.stderr)
        return None


def load_dir_jsons(d: pathlib.Path):
    if not d.is_dir():
        return []
    return [load_json(p) for p in sorted(d.glob("*.json")) if load_json(p) is not None]


VERDICT_TO_CSS = {
    "pass": "verified",
    "pass_with_caveats": "inferred",
    "fail": "absent",
    "false_segment": "absent",
}

VERDICT_TO_PLAIN = {
    "pass": "Validated",
    "pass_with_caveats": "Validated with caveats",
    "fail": "Rejected",
    "false_segment": "Rejected as a false group",
    "lead_candidate": "Lead bet",
    "supporting": "Reinforces a lead bet",
    "demote": "Reduce priority",
    "kill": "Drop",
}

BAND_TO_PLAIN = {
    "ship_solo": "Buildable solo",
    "ship_solo_with_apis": "Buildable solo (paid APIs)",
    "requires_partner": "Needs a partner",
    "requires_capital": "Needs capital",
    "requires_team": "Needs a team",
}

GEO_BAND_TO_PLAIN = {
    "P0": "Beachhead",
    "P1": "Adjacent expansion",
    "P2": "Scale market",
    "P3": "Partner-only entry",
    "deferred": "Deferred",
}


def build_human(
    blueprint,
    aura,
    jobs_graph,
    peers,
    peer_cards,
    red_team,
    value_mechanics,
    moat_audit,
    monetization,
    gtm,
    geo,
    capability,
    canonical_brief,
    market_size,
):
    """Compose the plain-English template layer."""

    # --- 1. Executive summary --------------------------------------------------
    headline_job_text = "Get a defensible padel skill rating that travels with the player."
    if canonical_brief and canonical_brief.get("ajtbd"):
        headline_job_text = canonical_brief["ajtbd"].get("headline_job", headline_job_text)
        if not headline_job_text.endswith("."):
            headline_job_text += "."

    primary_segment = "Plateau-stuck weekly regular"
    if canonical_brief and canonical_brief.get("segments"):
        primary_segment = canonical_brief["segments"].get("primary_name", primary_segment)

    headline_moat = "data + network"
    if canonical_brief and canonical_brief.get("value_mechanics"):
        headline_moat = canonical_brief["value_mechanics"].get("headline_moat", headline_moat)

    top_moves = canonical_brief.get("top_moves", []) if canonical_brief else []

    # Summary as HTML so we can hyperlink Playtomic / MATCHi inline.
    summary_html = (
        "<strong>Lucia plays in Madrid every Tuesday.</strong> Last week her partner Marco "
        "bumped his self-declared level on "
        '<a href="https://playtomic.io/blog">Playtomic</a> by half a step. Lucia has no way '
        "to tell whether Marco is actually better or just bolder, and her coach charges around "
        "EUR 60 for an assessment that means nothing the moment she books a court in Valencia. "
        "She wants a number that travels with her. So do roughly 35 million other padel players "
        'across <a href="https://www.padelfip.com/world-padel-report-2025/">77,300 courts</a> '
        "worldwide (FIP World Padel Report 2025), most of whom still pick a level on "
        '<a href="https://playtomic.io/blog">Playtomic</a> or '
        '<a href="https://matchi.com/">MATCHi</a> because nothing better exists. '
        "The opportunity is a phone-recorded rating that follows the player between clubs and "
        "tournaments, and that earns its keep inside the coach's renewal conversation."
    )

    headline_kpi_summary = (
        "Help a player walk into any club, hand over a phone-derived rating, and have it "
        "accepted without paying for a coach assessment that does not transfer."
    )

    stage_kpi_summary = "Pick the audience and the bet — not the roadmap."

    primary_audience_kpi_summary = (
        "Tournament-loss switcher (the regular who just lost a bracket and wants a real number)."
    )

    moat_kpi_summary = (
        "Rating data that compounds match-by-match (data) plus cross-club acceptance (network)."
    )

    # Engagement and retention triggers — the answer to "what basic needs hold the user?"
    engagement_triggers = [
        {
            "need": "Status — be seen at the right level",
            "trigger": "After a humiliating loss to a regular partner, the player wants a rating that the partner cannot wave away.",
            "in_product": "Match-by-match rating delta with a public profile link the player chooses to share.",
            "retention_signal": "Repeat upload by the same player within 7 days of the first recap.",
        },
        {
            "need": "Mastery — close the gap between effort and progress",
            "trigger": "Three matches in a row lost on the same shot.",
            "in_product": "Two prioritised drills tied to the recurring losing shot, ready before the next booking.",
            "retention_signal": "Drill plan acknowledgement followed by a rating delta improvement on that shot.",
        },
        {
            "need": "Belonging — keep the partnership alive",
            "trigger": "Post-match argument with the partner about what cost the third set.",
            "in_product": "Shared annotated review timeline both partners can scrub through and tag.",
            "retention_signal": "Both accounts active in the same review within two days of upload.",
        },
        {
            "need": "Self-efficacy — feel the next session has a plan",
            "trigger": "Booking a slot for next Tuesday with no idea what to practise.",
            "in_product": "One-line plan: shot, drill, success criterion, partner role.",
            "retention_signal": "Booking made through Playtomic / MATCHi with the plan referenced in-session notes.",
        },
        {
            "need": "Coach-led recognition (B2B2C)",
            "trigger": "A high-paying student goes quiet before renewal.",
            "in_product": "Weekly per-student progress recap the coach forwards before the renewal call.",
            "retention_signal": "Coach sends recap to the student; student renews.",
        },
    ]

    # --- 2. Jobs -------------------------------------------------------------
    jobs = []
    if canonical_brief and canonical_brief.get("ajtbd", {}).get("jobs"):
        for j in canonical_brief["ajtbd"]["jobs"]:
            jobs.append(
                {
                    "name": j.get("summary", ""),
                    "switch_trigger": j.get("switch_trigger", ""),
                    "expected_outcome": j.get("expected_outcome", ""),
                    "audience": j.get("segment_hint", ""),
                    "evidence_url": j.get("evidence_url", ""),
                    "story": _job_story(j),
                }
            )

    # --- 3. Stage classification ---------------------------------------------
    stage = "Understanding"
    stage_reasoning = ""
    if aura:
        stage_word = aura.get("stage", "understanding").capitalize()
        stage = stage_word
        stage_reasoning = aura.get("rationale", "")
    entry_signals = (canonical_brief or {}).get("aura_thesis", {}).get("entry_signals", []) or []
    exit_signals = (canonical_brief or {}).get("aura_thesis", {}).get("exit_signals", []) or []

    stage_blurb_human = (
        "The strategic question sits at the 'how should the team frame this?' stage rather than the "
        "'how should the team ship it?' stage. The market exists in volume, the early entrants are "
        "visible, but no single rating, mechanic or audience has been validated end-to-end. The next "
        "8 weeks belong to validating one audience and one bet, not designing a roadmap."
    )

    # --- 4. Audiences (segments) ---------------------------------------------
    audiences = []
    if canonical_brief and canonical_brief.get("segments", {}).get("rows"):
        for r in canonical_brief["segments"]["rows"]:
            audiences.append(
                {
                    "name": r.get("name", ""),
                    "what_they_want": r.get("core_job", ""),
                    "verdict": VERDICT_TO_PLAIN.get(r.get("verdict", ""), r.get("verdict", "")),
                    "verdict_class": VERDICT_TO_CSS.get(r.get("verdict", ""), "inferred"),
                    "story": _audience_story(r),
                }
            )

    # --- 5. Competitors ------------------------------------------------------
    competitors = []
    for c in peer_cards or []:
        archetype = (c.get("archetype") or "").replace("_", " ")
        archetype = {
            "product app": "Player app",
            "club camera system": "Club camera system",
            "sensor hardware": "Racket sensor",
            "match analyzer saas": "Club match analyzer",
            "research prototype": "Research prototype",
            "open source": "Open-source toolkit",
            "consultancy case study": "Engineering case study",
            "matchmaking app": "Booking and matchmaking",
            "club management software": "Club management",
            "rating system authority": "Rating authority",
            "academy lms": "Academy management",
        }.get(archetype, archetype)
        competitors.append(
            {
                "name": c.get("name", ""),
                "url": c.get("url", ""),
                "archetype_human": archetype,
                "value_prop": c.get("value_prop", ""),
                "pricing_model": (c.get("pricing") or {}).get("model", "").replace("_", " ") or "—",
                "pricing_anchor": (c.get("pricing") or {}).get("price_anchor", "") or "—",
                "moat_class": (c.get("moat_class") or "—").replace("_", " "),
                "verification_status": c.get("verification_status", "INFERRED"),
                "verification_status_class": "verified"
                if c.get("verification_status") == "VERIFIED"
                else "inferred",
            }
        )

    # --- 6. Defensibility bets (was: value mechanics + Naval audit) ----------
    bets = []
    if value_mechanics and moat_audit:
        verdict_by_name = {row["mechanic"]: row for row in moat_audit.get("audit", [])}
        for vm in value_mechanics:
            mname = (
                vm.get("name", "")
                .replace("founder-owned", "directly-reached")
                .replace("Founder-owned", "Directly-reached")
                .replace("founder ", "direct ")
                .replace("Founder ", "Direct ")
            )
            audit_row = next(
                (v for k, v in verdict_by_name.items() if k.startswith(vm.get("mechanic_id", ""))),
                None,
            )
            verdict = audit_row.get("verdict", "") if audit_row else ""
            scores = audit_row.get("scores", {}) if audit_row else {}
            bets.append(
                {
                    "name": mname,
                    "moat_class_human": vm.get("moat_class", "").replace("_", " "),
                    "thesis": vm.get("thesis", ""),
                    "verdict_human": VERDICT_TO_PLAIN.get(verdict, verdict.title() or "Open"),
                    "verdict_class": {
                        "lead_candidate": "verified",
                        "supporting": "inferred",
                        "demote": "absent",
                        "kill": "absent",
                    }.get(verdict, "inferred"),
                    "story": _bet_story(vm, audit_row),
                    "rice_score": vm.get("rice", {}).get("score", 0),
                    "kill_experiment": (vm.get("kill_experiment") or {}).get("description", ""),
                }
            )

    # --- 7. Defensibility frame (Naval gates) --------------------------------
    defensibility_rows = []
    for row in (moat_audit or {}).get("audit", []):
        scores = row.get("scores", {})
        # Strip the leading "VM-XXX " prefix from the mechanic label so the
        # rendered table reads as plain English.
        mechanic_label = re.sub(
            r"^(?:Hypothetical\s+)?VM-[A-Z0-9]+\s+", "", row.get("mechanic", "")
        )
        # Replace any remaining founder language inside that label.
        mechanic_label = (
            mechanic_label.replace("founder-owned", "directly-reached")
            .replace("Founder-owned", "Directly-reached")
            .replace("founder ", "direct ")
            .replace("Founder ", "Direct ")
        )
        defensibility_rows.append(
            {
                "mechanic": mechanic_label,
                "distribution": scores.get("distribution", 0),
                "network": scores.get("network", 0),
                "data": scores.get("data", 0),
                "hardware": scores.get("hardware", 0),
                "vertical_depth": scores.get("vertical_depth", 0),
                "verdict_human": VERDICT_TO_PLAIN.get(
                    row.get("verdict", ""), row.get("verdict", "")
                ),
                "verdict_class": {
                    "lead_candidate": "verified",
                    "supporting": "inferred",
                    "demote": "absent",
                    "kill": "absent",
                }.get(row.get("verdict", ""), "inferred"),
            }
        )

    # --- 8. Pricing ----------------------------------------------------------
    pricing_rows = []
    for b in (monetization or {}).get("price_benchmarks", []):
        pricing_rows.append(
            {
                "vendor": b.get("vendor", ""),
                "tier": b.get("tier") or b.get("tier_name") or "",
                "price": b.get("price") or "",
                "geography": b.get("geography", "") or "",
                "source_url": b.get("source_url", ""),
                "verified_quote": b.get("verified_quote", ""),
            }
        )

    # --- 9. GTM channels -----------------------------------------------------
    gtm_channels = []
    for c in (gtm or {}).get("channels", []):
        gtm_channels.append(
            {
                "rank": c.get("rank", ""),
                "name": c.get("name", ""),
                "type_human": (c.get("type") or "").title(),
                "cac_anchor": c.get("cac_anchor", ""),
                "cac_anchor_url": c.get("cac_anchor_url", ""),
                "moat_alignment": (c.get("moat_alignment") or "").replace("_", " ").title(),
                "story": _channel_story(c),
            }
        )
    plg_loops_human = []
    for l in (gtm or {}).get("plg_loops", []):
        plg_loops_human.append(
            {
                "name": l.get("name", ""),
                "trigger": l.get("trigger", ""),
                "action": l.get("action", ""),
                "reward": l.get("reward", ""),
                "kill_threshold": l.get("kill_threshold", ""),
                "story": _plg_story(l),
            }
        )

    # --- 10. Geo -------------------------------------------------------------
    geo_rows = []
    for g in (geo or {}).get("geographies", []):
        geo_rows.append(
            {
                "band_human": GEO_BAND_TO_PLAIN.get(g.get("band", ""), g.get("band", "")),
                "country": g.get("country") or g.get("country_iso", ""),
                "court_count": g.get("court_count_total"),
                "growth_yoy_pct": g.get("court_growth_yoy_pct"),
                "data_year": g.get("data_year", ""),
                "rationale": g.get("rationale", ""),
                "evidence_url": g.get("evidence_url", ""),
            }
        )

    # --- 11. Capability map (the section that broke) ------------------------
    capabilities_human = []
    for c in (capability or {}).get("capabilities", []):
        anchor_url = c.get("oss_anchor_url") or c.get("api_url") or ""
        anchor_label = c.get("oss_anchor") or c.get("api") or "—"
        capabilities_human.append(
            {
                "capability": c.get("capability", ""),
                "band_human": BAND_TO_PLAIN.get(c.get("band", ""), c.get("band", "")),
                "anchor_label": anchor_label,
                "anchor_url": anchor_url,
                "first_observable_output": c.get("first_observable_output", ""),
                "kill_signal": c.get("kill_signal", ""),
            }
        )

    # --- 12. Reality-check tests (was: kill experiments) --------------------
    reality_checks = []
    for k in (blueprint or {}).get("kill_experiments", []):
        reality_checks.append(
            {
                "hypothesis_human": k.get("hypothesis", ""),
                "kill_criterion_human": k.get("kill_criterion", ""),
                "evidence_required_human": k.get("evidence_required", ""),
                "story": _reality_check_story(k),
            }
        )

    # --- 13. Risks -----------------------------------------------------------
    risks = (canonical_brief or {}).get("risks", []) or []

    # --- 14. Retention drivers ------------------------------------------------
    retention = (canonical_brief or {}).get("retention_drivers", []) or []
    for r in retention:
        if "evidence_class" in r and not r.get("story"):
            r["story"] = ""

    # --- 15. TRIZ contradiction (re-narrated, no jargon) --------------------
    triz = (canonical_brief or {}).get("triz", {}) or {}
    triz_human = {
        "contradiction": triz.get("contradiction", ""),
        "resolution": triz.get("resolution", ""),
    }

    # --- 16. Differentiation table -------------------------------------------
    diff_table = (canonical_brief or {}).get("differentiation_table", []) or []

    # --- 17. USP -------------------------------------------------------------
    usp = (canonical_brief or {}).get("usp", "")

    # --- 18. Market sizing (TAM/SAM/SOM) ------------------------------------
    market = market_size or {}

    # --- 19. Analyst sources -------------------------------------------------
    analyst_sources = (market_size or {}).get("analyst_sources", []) or []

    return {
        "headline": "Padel AI Coach — Strategic Brief",
        "summary_html": summary_html,
        "headline_kpi_summary": headline_kpi_summary,
        "stage_kpi_summary": stage_kpi_summary,
        "primary_audience_kpi_summary": primary_audience_kpi_summary,
        "moat_kpi_summary": moat_kpi_summary,
        "engagement_triggers": engagement_triggers,
        "headline_job_text": headline_job_text,
        "primary_segment": primary_segment,
        "primary_moat": headline_moat.replace("_", " "),
        "stage": stage,
        "stage_reasoning": stage_reasoning,
        "stage_blurb": stage_blurb_human,
        "entry_signals": entry_signals,
        "exit_signals": exit_signals,
        "top_moves": top_moves,
        "jobs": jobs,
        "audiences": audiences,
        "competitors": competitors,
        "bets": bets,
        "defensibility_rows": defensibility_rows,
        "pricing_rows": pricing_rows,
        "gtm_channels": gtm_channels,
        "plg_loops": plg_loops_human,
        "geo_rows": geo_rows,
        "capabilities": capabilities_human,
        "reality_checks": reality_checks,
        "risks": risks,
        "retention": retention,
        "triz": triz_human,
        "diff_table": diff_table,
        "usp": usp,
        "market": market,
        "analyst_sources": analyst_sources,
    }


def _job_story(job: dict) -> str:
    name = job.get("summary", "").lower()
    if "rating" in name:
        return (
            "Concrete example: a Madrid regular plays the same partner every Tuesday. The "
            "partner upgrades their self-declared level on Playtomic by half a step. The "
            "regular wants to know whether the partner is actually that strong, or just "
            "confident, without paying for a coach assessment that does not transfer to next "
            "week's club."
        )
    if "drills" in name:
        return (
            "Concrete example: a player loses three matches in a row to the same backhand "
            "lob over the cage. They want a 30-second recap that names the shot, the body "
            "position, and the next two drills they should book — not a generic '20 minutes "
            "of warm-up' suggestion."
        )
    if "student" in name or "coach" in name:
        return (
            "Concrete example: a Barcelona academy coach has 12 weekly students. One of them "
            "is up for renewal. The coach wants a 1-page recap of that student's shot mix, "
            "best rally and weakest pattern over the last 4 sessions — composed without "
            "manual note-taking after each lesson."
        )
    if "argument" in name or "settle" in name:
        return (
            "Concrete example: two partners disagree about who lost the third-set tiebreak. "
            "One thinks it was the smashes, the other thinks it was service returns. They "
            "want a shared timeline where both can scrub through the rallies and tag what "
            "they think mattered, before booking next Saturday."
        )
    return ""


def _audience_story(seg: dict) -> str:
    name = seg.get("name", "").lower()
    if "plateau" in name:
        return (
            "Story: a player who books two slots a week for two years. They know they have "
            "stopped improving. They have tried a paid coach, a generic fitness app, and "
            "their friend's racket sensor. None of those produced a number their next "
            "partner accepts. That is the moment they look for something new."
        )
    if "newly" in name:
        return (
            "Story: a player who entered their first regional tournament and lost in the "
            "round of 32. They suspect their level is honest, but they want a public-looking "
            "rating before they pay for the next entry fee. The moment of reaching for a tool "
            "is the morning after the loss, not the day before the tournament."
        )
    if "coach" in name:
        return (
            "Story: a working coach with 8–20 students. One paying student churns to a "
            "competing academy because the rival coach 'showed them progress charts'. The "
            "coach goes looking for a tool the next morning — but only if it does not "
            "compete with their authority in front of the student."
        )
    if "operator" in name:
        return (
            "Story: a club operator running 6 courts with 60% weekday occupancy. They want "
            "to differentiate against the new club two streets away. Their default purchase "
            "is more cameras and a booking refresh, not a coaching layer — which is why this "
            "audience was rejected."
        )
    if "travelling" in name:
        return (
            "Story: a player who plays in Madrid and Barcelona alternating weekends. Their "
            "Playtomic level is inconsistent across cities. They reach for a tool when an "
            "out-of-town tournament invitation lands and the seeding system asks for a "
            "rating they do not have."
        )
    if "injury" in name:
        return (
            "Story: a player returning from lateral epicondylitis. They want load monitoring "
            "for racket-specific motions, not a generic Whoop strain score. Today, no padel "
            "product collects this data longitudinally — which is why this group was treated "
            "as a wishlist rather than a real audience."
        )
    return ""


def _bet_story(vm: dict, audit_row) -> str:
    name = (vm.get("name", "") or "").lower()
    if "smartphone" in name and "rating" in name:
        return (
            "Story: the user props a phone on the side of the court. The app ingests the "
            "match video, segments rallies, tags shot types, and produces a rating delta. "
            "Each match the player records improves the rating model for everyone — that is "
            "the reason the data gate is real and not just analytics theatre."
        )
    if "cross-club" in name:
        return (
            "Story: a regional FIP-affiliated organiser in Valencia accepts the rating spec "
            "and uses it to seed their bracket. Once the bracket runs cleanly, removing the "
            "integration costs the organiser hours of manual seeding work — which is why "
            "this is a switching-cost moat, not a feature parity claim."
        )
    if "drill" in name:
        return (
            "Story: instead of a generic 'practice your backhand' tip, the player gets "
            "'Tuesday at Club X, drill backhand-lob defence with right partner, success "
            "criterion 7 of 10 returns inside the cage.' The drill prescription rides on top "
            "of the rating chain — kill the rating and this drill loses its anchor."
        )
    if "coach" in name and "co-pilot" in name:
        return (
            "Story: a coach taps four quick tags on their phone after each lesson. By Friday "
            "the app has composed a per-student weekly recap that the coach forwards before "
            "the renewal call. The coach does not export the tag history when they leave — "
            "that history is the switching cost."
        )
    if "shared" in name and "review" in name:
        return (
            "Story: after the match, both partners get an annotated timeline. One tags the "
            "third-set return, the other tags the smash that landed long. They both invite a "
            "second pair into the same surface for next Saturday — one user becomes four."
        )
    if "newsletter" in name or "audience" in name:
        return (
            "Story: a Spanish-language padel publication with weekly tactical recaps and a "
            "Russian-language Telegram digest. Subscribers arrive direct, not from Playtomic "
            "or Meta. If the direct-traffic share of beta sign-ups falls below 25 percent at "
            "week 8, this is a marketing tactic and not a moat."
        )
    if "tournament" in name:
        return (
            "Story: when the bracket auto-seeds against the imported rating, officials run "
            "the day with one fewer manual step. Removing the integration means the "
            "organiser re-learns the manual process — operational lock-in beats a feature "
            "parity argument."
        )
    if "local-language" in name or "language" in name:
        return (
            "Story: a Spanish-only player gets a recap that uses the same vocabulary their "
            "club coach uses. An English-first competitor cannot replicate that cadence "
            "until they hire local writers — that hiring step is the moat, not the "
            "translation step."
        )
    if "open-source" in name:
        return (
            "Story: shipping the court-calibration step as open-source attracts CV engineers "
            "and gives the brand a credible story. It does not protect any value alone — that "
            "is why it was downgraded to a supporting bet."
        )
    if "on-device" in name or "privacy" in name:
        return (
            "Story: matches in Russia and the EU process locally on the phone. Only the "
            "rating delta leaves the device. Useful as a positioning lever in regulated "
            "markets — not strong enough to be a primary moat."
        )
    if "academy" in name or "open data" in name:
        return (
            "Story: an academy adopts the tag taxonomy. Coach onboarding for new hires drops "
            "from a week to two days. Switching to a competitor means re-training every "
            "coach — the cost is human, not technical."
        )
    return ""


def _channel_story(ch: dict) -> str:
    name = (ch.get("name") or "").lower()
    if "newsletter" in name:
        return (
            "Story: a weekly Spanish-language tactical recap, biweekly Russian-language "
            "version, both with a 'match-recap' link in every issue. Direct-traffic "
            "share is the proof that this audience is owned, not rented."
        )
    if "club partnership" in name:
        return (
            "Story: anchor three clubs in Madrid, Barcelona, Milan with a free pilot. "
            "Each club's leaderboard becomes co-branded; the club imports its own audience."
        )
    if "tournament" in name:
        return (
            "Story: sign two FIP-affiliated regional organisers to a 30-day bracket "
            "trial. After one tournament runs cleanly, organisers commit to paid "
            "integration."
        )
    if "youtube" in name or "creator" in name:
        return (
            "Story: sponsor five Spanish-language padel coaching creators with a "
            "'match-recap' format using their subscriber footage. Each creator runs a "
            "trackable referral code."
        )
    if "reddit" in name or "discord" in name or "community" in name:
        return (
            "Story: pinned moderator AMA in r/padel, weekly Discord office hours with "
            "anonymised recaps. Engaged community members convert to beta uploaders."
        )
    if "telegram" in name or "cis" in name:
        return (
            "Story: a Telegram digest in Russian with a /recap command flow. Subscribers "
            "stay on platform; the on-device pipeline keeps the data inside the user's "
            "phone for 152-FZ compliance."
        )
    if "coach affiliate" in name:
        return (
            "Story: 8 coaches recruited via federation chapters in Spain and Italy. Each "
            "coach gets a per-student recap they can share before renewal calls."
        )
    if "apple search ads" in name or "google search" in name or "paid" in name:
        return (
            "Story: paid search is conversion-stage only — keywords like 'padel rating' "
            "and 'padel coach app' get tested against organic traffic, not used as the "
            "lead acquisition channel."
        )
    return ""


def _plg_story(loop: dict) -> str:
    name = (loop.get("name", "") or "").lower()
    if "post-match" in name or "share" in name:
        return (
            "Story: a player finishes uploading a match and gets a 30-second highlight + "
            "insight card with both names. They share it on WhatsApp; the partner and the "
            "two opponents see it."
        )
    if "partner" in name and "invite" in name:
        return (
            "Story: 'Review with partner' button creates a shared annotation seat. One "
            "invite turns one user into a paired account."
        )
    if "leaderboard" in name or "club discovery" in name:
        return (
            "Story: a club leaderboard URL is co-branded with the club logo. Members see "
            "the top 20 ranking and click through to claim their profile."
        )
    if "rating display" in name or "playtomic" in name or "matchi" in name:
        return (
            "Story: a player elects to surface their derived rating on their booking "
            "profile. Booking partners see it on the booking flow itself."
        )
    if "coach handoff" in name:
        return (
            "Story: after three uploaded matches the player can grant a coach access. The "
            "coach receives a weekly recap pack for that player and can extend invites to "
            "other students."
        )
    return ""


def _reality_check_story(kx: dict) -> str:
    h = (kx.get("hypothesis", "") or "").lower()
    if "rating" in h and "smartphone" in h:
        return (
            "Story: a Spanish landing page lets a beta user upload a sample match and "
            "receive a rating. If fewer than a quarter of testers accept the result as "
            "their public level, the rating idea was wishful thinking."
        )
    if "coach" in h and "dashboard" in h:
        return (
            "Story: 8 coaches in Spain and Italy run a one-week pilot with a per-student "
            "dashboard. If fewer than 3 of them send a recap to a real student, the "
            "coach co-pilot is a feature, not a workflow."
        )
    if "rating" in h and ("tournament" in h or "organizer" in h or "organiser" in h):
        return (
            "Story: outreach to two FIP-affiliated regional organisers in Spain and Italy "
            "for a 30-day bracket trial. If neither agrees in writing, the cross-club "
            "moat is theatre."
        )
    if "smartphone" in h and "pipeline" in h:
        return (
            "Story: clone the open-source padel CV pipeline, spend a fixed budget of 40 "
            "person-hours integrating it on a single laptop. If the pipeline does not "
            "work end-to-end in that window, every plan that depended on the smartphone "
            "path needs to be re-priced against partner clubs."
        )
    return ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    args = ap.parse_args()

    e = pathlib.Path(f"evidence/{args.run_id}")
    rep = pathlib.Path(f"reports/{args.run_id}")
    rep.mkdir(parents=True, exist_ok=True)

    blueprint = load_json(e / "00_blueprint.json")
    aura = load_json(e / "02_aura.json")
    peers = load_json(e / "03_peers_dedup.json") or []
    peer_cards = load_dir_jsons(e / "04_peer_cards")
    jobs_graph = load_json(e / "05_jobs_graph.json")
    red_team = load_json(e / "06_red_team.json")
    value_mechanics = load_dir_jsons(e / "08_value_mechanics")
    moat_audit = load_json(e / "09_moat_audit.json")
    monetization = load_json(e / "10_monetization.json")
    gtm = load_json(e / "11_gtm.json")
    geo = load_json(e / "12_geo.json")
    capability = load_json(e / "13_capability_map.json")
    canonical_brief = load_json(e / "canonical_brief.json")
    market_size = load_json(e / "15_market_size.json")

    human = build_human(
        blueprint,
        aura,
        jobs_graph,
        peers,
        peer_cards,
        red_team,
        value_mechanics,
        moat_audit,
        monetization,
        gtm,
        geo,
        capability,
        canonical_brief,
        market_size,
    )

    data = {
        "run_id": args.run_id,
        "blueprint": blueprint,
        "aura": aura,
        "peers": peers,
        "peer_cards": peer_cards,
        "jobs_graph": jobs_graph,
        "red_team": red_team,
        "value_mechanics": value_mechanics,
        "moat_audit": moat_audit,
        "monetization": monetization,
        "gtm": gtm,
        "geo": geo,
        "capabilities": capability,
        "canonical_brief": canonical_brief,
        "market_size": market_size,
        "human": human,
    }

    out = rep / "data.json"
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[build_report_data] wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
