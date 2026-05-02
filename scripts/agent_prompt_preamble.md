# Reusable Agent Prompt Preamble

> Copy-paste the block below at the top of every Agent invocation prompt.
> It replaces the boilerplate that was previously inlined in every agent brief.
> Updates to quality requirements happen in `QUALITY_BAR.md`, not here.

---

## ➤ Standard preamble (paste at top of every agent prompt)

```
PROJECT CONTEXT
- Working dir: /Users/sxope/Documents/2026/Research/28.Padel/Claude/padel-research-os
- Operating contract: padel-research-os/CLAUDE.md
- Quality bar (authoritative): padel-research-os/QUALITY_BAR.md — read it before doing anything

QUALITY BAR
You MUST obey QUALITY_BAR.md without exception. The hard rules (MUST / MUST NOT),
citation tag taxonomy (VERIFIED / INFERRED / INTERNAL / INFERRED_INHERITED / ABSENT),
voice rules (third-person, capability-conditional, no first-person pronouns),
cross-document consistency contract, and per-artifact quality gates all live there.
Do not paraphrase those rules into your output — apply them.

VERIFICATION
Before returning a result, run the relevant verification commands listed in
QUALITY_BAR.md §2 for your artifact type, and confirm clean exit.
```

---

## ➤ Per-task addendum (one line, inline)

After the preamble, the agent prompt only needs:
- the *task* (what to produce)
- the *inputs* (which evidence files to read)
- the *outputs* (where to write)
- the *return summary* shape

Everything else (citation rules, voice, gates, fallback chain) is delegated to `QUALITY_BAR.md`.

---

## ➤ Anti-pattern to avoid

❌ DO NOT do this in agent prompts (this is what red-team review caught on 2026-05-03):

```
Quality gates:
- Every numeric claim has source_url + verified_quote ≤15 words.
- No first-person pronouns.
- Capability-conditional phrasing only.
- Cite at least N distinct verified URLs.
- Free fallback chain when paid is tight: nemotron-3-super, nemotron-3-nano, ling-2.6.
- ... (10 more lines)
```

This was repeated in every research-arm prompt with subtle variations. Rules drifted across runs. Some prompts forgot the citation tag taxonomy. Quality bar was inconsistent.

✅ DO this:

```
Obey QUALITY_BAR.md. Apply the quality gates for the "Synthesis brief" artifact type (§5).
```

The quality bar updates once, all downstream agents inherit consistently.
