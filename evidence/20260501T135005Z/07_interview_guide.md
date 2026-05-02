# JTBD Interview Guide — Padel AI Coach

This guide instruments the validation phase that follows the run. The
candidate, once hired, executes the recruitment, runs eight to twelve
60-min interviews per surviving segment, and feeds the parsed
respondent records into the canonical brief at the next research wave.
The guide is built so a non-specialist can run interviews without
coaching loss. No padel-specific software is required. Pen, notebook,
phone-recording app.

## How to use

Run with one segment at a time. Recruit six to eight recent switchers
per segment. Recent switcher means a player who, in the last six
months, started or abandoned a coaching, rating, or training tool
relevant to padel. Schedule a 60-min slot. Record audio with explicit
consent. After each session, log methodology issues against the
self-audit checklist at the bottom.

## Recruitment

### Channels per segment

- SEG-001 the plateau-stuck regular: padel club newsletter mailing
 lists in Madrid, Barcelona, Milan; subreddit r/padel posts pinned by
 moderators; Padel Business Magazine newsletter
 ([newsletter.padelbusinessmagazine.com](https://newsletter.padelbusinessmagazine.com/p/spain-s-growth-continues-padel-courts-up-5-to-17-000-in-2024)).
- SEG-002 the newly-ranked competitor: regional FIP-affiliated
 tournament organisers in Spain
 ([padelfip.com](https://www.padelfip.com/calendar-fip-championships/));
 the federation chapters at FEP ([fep.es](https://www.fep.es/)) and
 FITP ([fitp.it](https://www.fitp.it/)).
- SEG-003 the club coach: coach forums adjacent to CoachLogic
 ([coachlogic.com](https://coachlogic.com/)); padel academy operator
 groups; Spanish and Italian padel federation chapters.

### Pre-screen filters

- Played padel for at least six months at a club address.
- Hired or fired a coaching, rating, or training tool in the last six
 months. The hire or fire is a discrete event, not an opinion.
- Available for a single 60-min slot in the next two weeks.
- Comfortable being audio-recorded.

### Sample recruitment messages (three versions)

Sample A — Spanish padel community channel:

- Hook line: "Padel club regulars."
- Frame: a researcher is running short conversations about how players choose coaching or rating tools.
- Logistics: 60 minutes, recorded, no product pitch.
- Call to action: reply with "padel" plus the city to start.

Sample B — federation chapter newsletter:

- Hook line: "Tournament-experienced players."
- Frame: the conversation is about the last coaching or rating tool a player tried.
- Logistics: 60 minutes, audio recorded, no pitch.
- Call to action: reply if interested.

Sample C — coach community channel:

- Hook line: "Coaches with four to twenty students per week."
- Frame: the topic is how progress is tracked and shown at renewal.
- Logistics: 60 minutes, audio recorded, no pitch.
- Call to action: reply with the city.

## Interview structure (60-min)

| Block | Time | Purpose |
|-------|------|---------|
| Rapport + emotional contact | 0–8 min | Trust, set frame, no padel content |
| Story discovery | 8–25 min | The switch story, in past tense |
| Force mapping | 25–40 min | Push, Pull, Anxiety, Habit |
| Alternatives mapping | 40–50 min | What was hired and what was fired |
| Outcome scoring | 50–58 min | Importance × satisfaction |
| Close + referrals | 58–60 min | Clean exit |

## Past tense story discovery

Each question is past tense. No future-tense, no hypothetical.

- "Take the conversation back to the day the decision started. What
 was happening that week?"
- "Who else was in the room or on the call?"
- "Walk through the last match before the decision. What happened on
 the court?"
- "Describe the first attempt to fix the problem. What was tried?"
- "Describe the moment the previous tool stopped being trusted."
- "Who else was consulted between the trigger and the switch?"
- "Walk through the first time the new tool was used. What worked and
 what was awkward?"
- "Describe the conversation with a partner about the new tool."

Every question carries one laddering-up probe ("why did that matter?")
and one laddering-down probe ("what did that look like?").

## Forces of progress (Push, Pull, Anxiety, Habit)

### Push — struggle on the status quo

- "What about the previous tool stopped being trusted?"
- "What was the moment the previous tool felt insufficient?"
- "Describe a specific failure of the previous tool."
- "What was being avoided when the previous tool stayed?"

### Pull — attraction of the new solution

- "When the new tool first came up, what specifically caught
 attention?"
- "What was the first piece of evidence that suggested the new tool
 could solve the problem?"
- "Who was the first person to mention the new tool?"

### Anxiety — fear of switching

- "What was a worry about trying the new tool?"
- "What had to be true for the switch to feel safe?"
- "Describe a moment where the switch nearly stalled."

### Habit — inertia of the old way

- "What about the old way was hard to walk away from?"
- "Where did the old way still show up after the switch?"
- "What was the cost of staying on the old way?"

## Alternatives mapping

- "What other options were considered before settling on the chosen
 tool?"
- "Walk through the rejection of each option in order."
- "Where was each rejected option insufficient?"
- "What had to be true for an option to be reconsidered?"

## Outcome scoring

For each named outcome:

- "On a 1 to 10 scale, how important is the outcome?"
- "On a 1 to 10 scale, how well did the current solution deliver the
 outcome?"

Compute opportunity_score = importance + max(0, importance −
satisfaction). The score is a candidate-side artifact, not a
respondent-side rating.

## Close + referrals

- "Who else should the conversation continue with?"
- "What was missing from the questions today?"

## Methodology issues log (self-audit, fill after each interview)

- [ ] Did the interviewer talk more than 20 percent of the session?
- [ ] Did the interviewer ask any leading or hypothetical question?
- [ ] Did the interviewer pitch a feature?
- [ ] Was emotional contact established before story discovery?
- [ ] Was every Push, Pull, Anxiety, Habit branch covered?
- [ ] Was the recording consented to and saved?
- [ ] Were any quotes paraphrased on the spot rather than transcribed?

## Coding instructions for transcript parsing

After interviews, transcripts go to evidence/_external/interviews/R-XXX.txt.
The interview-transcript-parser prompt at
vendored/-product-os/prompts/interview-transcript-parser.md
extracts structured records to evidence/<run-id>/_interviews/R-XXX.json.
This pipeline does not run interviews — it produces the instrument
and the validation rules.

## Stop conditions

- Recruitment yields fewer than four respondents per segment after
 two weeks. Escalate to a partner club or tournament organiser via
 Premier Padel ([premierpadel.com](https://premierpadel.com/)).
- Average interviewer talk time exceeds 25 percent across the first
 three sessions. Pause; recalibrate the rapport block before
 continuing.
