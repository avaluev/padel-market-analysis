# MVP Loop Design

## How a padel coaching app earns the right to exist

A padel coaching app has to compound three things into one product, not three: capture that succeeds without club hardware, an insight a player can act on in their next session, and a coach who signs off on the result. Skip any one and the loop stalls — capture without insight is a video archive, insight without coach buy-in is a newsletter, coach buy-in without capture is a workshop business. The diagram below is the smallest shape that closes the loop.

<figure class="diagram" role="img" aria-label="Three-stage product loop: capture, insight, practice. Player records a match on a phone. The recording becomes a one-page recap with two suggested drills. The coach reviews the recap and runs one drill in the next session. The session result feeds back into the next recap.">
<svg viewBox="0 0 760 320" xmlns="http://www.w3.org/2000/svg" role="img" aria-hidden="true" style="width:100%;height:auto;max-width:760px;display:block;margin:24px 0">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="#0a6cf3"/>
    </marker>
  </defs>
  <style>
    .stage { fill: #fafafa; stroke: #0a6cf3; stroke-width: 2; rx: 12; ry: 12; }
    .stage-num { fill: #0a6cf3; font: 700 14px system-ui; }
    .stage-title { fill: #0a0a0a; font: 700 16px system-ui; }
    .stage-body { fill: #3f3f46; font: 400 13px system-ui; }
    .arrow { stroke: #0a6cf3; stroke-width: 2; fill: none; marker-end: url(#arrow); }
    .loop { stroke: #0a6cf3; stroke-width: 2; stroke-dasharray: 4,4; fill: none; marker-end: url(#arrow); opacity: 0.6; }
    @media (prefers-color-scheme: dark) {
      .stage { fill: #181a1d; stroke: #3b9bff; }
      .stage-num { fill: #3b9bff; }
      .stage-title { fill: #fafafa; }
      .stage-body { fill: #d4d4d8; }
      .arrow { stroke: #3b9bff; }
      .loop { stroke: #3b9bff; }
    }
  </style>
  <rect class="stage" x="20"  y="60" width="220" height="180"/>
  <text class="stage-num"  x="40"  y="92">STAGE 1</text>
  <text class="stage-title" x="40" y="118">Capture</text>
  <text class="stage-body" x="40" y="148">Player props a phone</text>
  <text class="stage-body" x="40" y="166">behind the baseline,</text>
  <text class="stage-body" x="40" y="184">records one full match.</text>
  <text class="stage-body" x="40" y="212" style="font-style:italic">Output: a video file</text>
  <text class="stage-body" x="40" y="228" style="font-style:italic">and a few scoreline notes.</text>

  <rect class="stage" x="270" y="60" width="220" height="180"/>
  <text class="stage-num"  x="290" y="92">STAGE 2</text>
  <text class="stage-title" x="290" y="118">Insight</text>
  <text class="stage-body" x="290" y="148">A one-page recap names</text>
  <text class="stage-body" x="290" y="166">the three losing-shot</text>
  <text class="stage-body" x="290" y="184">patterns and suggests</text>
  <text class="stage-body" x="290" y="202">two practice drills.</text>
  <text class="stage-body" x="290" y="222" style="font-style:italic">Output: a single PDF</text>
  <text class="stage-body" x="290" y="238" style="font-style:italic">a coach can read in a minute.</text>

  <rect class="stage" x="520" y="60" width="220" height="180"/>
  <text class="stage-num"  x="540" y="92">STAGE 3</text>
  <text class="stage-title" x="540" y="118">Practice</text>
  <text class="stage-body" x="540" y="148">Coach reads the recap,</text>
  <text class="stage-body" x="540" y="166">runs one drill in the</text>
  <text class="stage-body" x="540" y="184">next session, marks</text>
  <text class="stage-body" x="540" y="202">whether it worked.</text>
  <text class="stage-body" x="540" y="222" style="font-style:italic">Output: a labelled</text>
  <text class="stage-body" x="540" y="238" style="font-style:italic">drill-to-outcome record.</text>

  <path class="arrow" d="M 240 150 L 270 150"/>
  <path class="arrow" d="M 490 150 L 520 150"/>
  <path class="loop"  d="M 630 240 Q 630 290 380 290 Q 130 290 130 240"/>
  <text class="stage-body" x="380" y="312" text-anchor="middle" style="font-style:italic">The next match starts the loop again, this time with a labelled outcome to learn from.</text>
</svg>
<figcaption>The loop in three steps. Each step has one input, one action, one output. The loop only compounds value if step three closes — without coach sign-off the recap is a guess.</figcaption>
</figure>

The strongest part of the loop is step three. It is the only place a video stream becomes a labelled training signal: which drill, which losing pattern, did the player improve. Without that closing tag, the model never gets better than commodity tagging.

---

## Three pilot tracks compared

Before any of the three pilots starts, decide which question matters more: how fast the loop can ship, or how deeply it can be measured. The table below trades the same loop against three different pilot shapes. None is wrong; the choice depends on what is unknown.

| Track | Who runs it | What it tests | What it learns | What it cannot tell you |
|---|---|---|---|---|
| **A · Single club, one academy** | One academy lead, three to five coaches, twenty to thirty regular players over four to six weeks | Whether players read the recap and act on it inside one social context | Whether the loop has any traction at all and where capture friction shows up | Whether the loop generalises across clubs or coaching styles |
| **B · Two clubs, paired** | Two academies in the same city, four to six coaches each, two cohorts of players running in parallel | Whether the loop survives a second context with different coach habits | Whether ratings drift across clubs and whether the recap template needs club-specific tuning | Whether the loop works in markets with different padel cultures (Iberia vs the Gulf vs the Russian-speaking world) |
| **C · Open beta, narrow geography** | A landing page in one city or country, anyone can sign up, no academy partnership | Whether the loop works for self-served players without a coach in the loop | What happens to retention when there is no human reinforcement at step three | Whether the loop works at all — open beta tests scale, it does not test value |

The honest order is A → B → C. Track A answers the value question with the smallest possible group of people. Track B tests whether what worked in one academy survives in another. Track C only makes sense after A and B return strong signals.

---

## What to build first

The diagram below shows the build order under three different early signals. Each branch picks the smallest next thing that earns the right to keep going.

<figure class="diagram" role="img" aria-label="Decision tree for what to build first. After running the single-club pilot, three outcomes are possible. If players engage but coaches resist, build coach-only delivery first. If coaches engage but players ignore the recap, change the delivery channel from email to messaging. If both engage, expand to a second club.">
<svg viewBox="0 0 760 460" xmlns="http://www.w3.org/2000/svg" role="img" aria-hidden="true" style="width:100%;height:auto;max-width:760px;display:block;margin:24px 0">
  <defs>
    <marker id="arrow2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="#0a6cf3"/>
    </marker>
  </defs>
  <style>
    .root { fill: #e6efff; stroke: #0a6cf3; stroke-width: 2; rx: 12; ry: 12; }
    .branch { fill: #fafafa; stroke: #0a6cf3; stroke-width: 1.5; rx: 12; ry: 12; }
    .leaf { fill: #f5f7fa; stroke: #71717a; stroke-width: 1; rx: 10; ry: 10; }
    .root-text, .branch-text { fill: #0a0a0a; font: 600 14px system-ui; }
    .leaf-text { fill: #3f3f46; font: 400 13px system-ui; }
    .edge { stroke: #0a6cf3; stroke-width: 1.5; fill: none; marker-end: url(#arrow2); }
    .edge-label { fill: #71717a; font: 400 12px system-ui; font-style: italic; }
    @media (prefers-color-scheme: dark) {
      .root { fill: #0e2440; stroke: #3b9bff; }
      .branch { fill: #181a1d; stroke: #3b9bff; }
      .leaf { fill: #181a1d; stroke: #71717a; }
      .root-text, .branch-text { fill: #fafafa; }
      .leaf-text { fill: #d4d4d8; }
      .edge { stroke: #3b9bff; }
      .edge-label { fill: #a1a1aa; }
    }
  </style>
  <rect class="root" x="280" y="20" width="200" height="56"/>
  <text class="root-text" x="380" y="42" text-anchor="middle">Run single-club pilot</text>
  <text class="root-text" x="380" y="62" text-anchor="middle">for four weeks</text>

  <path class="edge" d="M 360 76 L 130 130"/>
  <text class="edge-label" x="200" y="100">players read it,</text>
  <text class="edge-label" x="200" y="115">coaches resist</text>
  <path class="edge" d="M 380 76 L 380 130"/>
  <text class="edge-label" x="395" y="105">both engage</text>
  <path class="edge" d="M 400 76 L 630 130"/>
  <text class="edge-label" x="540" y="100">coaches engage,</text>
  <text class="edge-label" x="540" y="115">players ignore the recap</text>

  <rect class="branch" x="40" y="140" width="180" height="80"/>
  <text class="branch-text" x="130" y="167" text-anchor="middle">Coach-only delivery</text>
  <text class="leaf-text" x="130" y="187" text-anchor="middle">Coach receives the recap,</text>
  <text class="leaf-text" x="130" y="205" text-anchor="middle">decides whether to share.</text>

  <rect class="branch" x="280" y="140" width="200" height="80"/>
  <text class="branch-text" x="380" y="167" text-anchor="middle">Add a second club</text>
  <text class="leaf-text" x="380" y="187" text-anchor="middle">Test whether the loop</text>
  <text class="leaf-text" x="380" y="205" text-anchor="middle">survives a new context.</text>

  <rect class="branch" x="540" y="140" width="180" height="80"/>
  <text class="branch-text" x="630" y="167" text-anchor="middle">Change the channel</text>
  <text class="leaf-text" x="630" y="187" text-anchor="middle">Move recap from email</text>
  <text class="leaf-text" x="630" y="205" text-anchor="middle">to a chat the player reads.</text>

  <path class="edge" d="M 130 220 L 130 270"/>
  <path class="edge" d="M 380 220 L 380 270"/>
  <path class="edge" d="M 630 220 L 630 270"/>

  <rect class="leaf" x="40" y="280" width="180" height="64"/>
  <text class="leaf-text" x="130" y="305" text-anchor="middle">Coach owns the moment;</text>
  <text class="leaf-text" x="130" y="323" text-anchor="middle">the app stays out of sight.</text>

  <rect class="leaf" x="280" y="280" width="200" height="64"/>
  <text class="leaf-text" x="380" y="305" text-anchor="middle">Two-club rating drift</text>
  <text class="leaf-text" x="380" y="323" text-anchor="middle">becomes the new test.</text>

  <rect class="leaf" x="540" y="280" width="180" height="64"/>
  <text class="leaf-text" x="630" y="305" text-anchor="middle">Recap as a chat thread,</text>
  <text class="leaf-text" x="630" y="323" text-anchor="middle">not a downloadable file.</text>

  <path class="edge" d="M 130 344 L 130 380"/>
  <path class="edge" d="M 380 344 L 380 380"/>
  <path class="edge" d="M 630 344 L 630 380"/>

  <rect class="leaf" x="40"  y="390" width="180" height="56"/>
  <text class="leaf-text" x="130" y="425" text-anchor="middle">Player sees value via coach.</text>

  <rect class="leaf" x="280" y="390" width="200" height="56"/>
  <text class="leaf-text" x="380" y="425" text-anchor="middle">If drift is small, expand.</text>

  <rect class="leaf" x="540" y="390" width="180" height="56"/>
  <text class="leaf-text" x="630" y="425" text-anchor="middle">Open rate becomes read rate.</text>
</svg>
<figcaption>The next build is whichever the early signal asks for. Each branch picks the smallest change that turns a weak signal into a stronger one before any new feature gets added.</figcaption>
</figure>

---

## Risk register

The five things that can go wrong, ordered by how likely each is to break the pilot. Each row names the symptom early enough to react and the response that does not require rebuilding from scratch.

| Risk | What it looks like | Where to spot it | What to do |
|---|---|---|---|
| **Players never read the recap** | The PDF is opened by fewer than three in ten players within three days of receiving it | Email or chat read receipts during weeks two and three | Move the recap from a downloadable file to a short message inside the chat the player already uses with the coach |
| **Coaches refuse the tool** | Two or more coaches stop filing the outcome tag during a single week despite reminders | Weekly tagging report shared with the academy lead | Switch to coach-only delivery: the recap goes to the coach first; the player only sees what the coach decides to share |
| **The recap is too generic** | Players say "I already knew that" in week-three interviews | Two short interviews per coach panel, recorded for replay | Re-curate the drill list with the coaches and shorten the recap to one losing pattern instead of three |
| **Phone capture fails outdoors or indoors** | More than one in four matches cannot be processed because of light, occlusion, or angle | Ingestion log shows rejection rate by week | Publish a one-page setup card with where to mount the phone, what to point it at, and how high; offer a club-camera fallback if the partner club has one |
| **Ratings drift between clubs** | A player's rating changes by more than five percent across two clubs in two weeks | Cross-club rating comparison once a second club is added in track B | Lock the shot taxonomy to a published schema before any second-club expansion; treat the schema as a contract, not an evolving guess |

---

## What this loop is not

The loop is not a video editor. It is not a club-management tool. It is not a tournament organiser. It is not a marketplace for coaches. Each of those would compete with companies that have years of work in those categories. The loop earns its right to exist only on one job: turning the next match into a measurably better next session, with a coach in the room.

---

## How to read this against the rest of the research

This page describes the loop. The [strategic brief](padel-ai-coach-research.html) explains why it is the loop worth building. The [competitor landscape](competitor-landscape.html) shows which adjacent products already own pieces of it. The [subscription economics](subscription-economics.html) page works out what the loop has to be worth per month for the unit economics to land. The [ninety-day plan](90-day-plan.html) is what the first quarter looks like if track A starts on day one.
