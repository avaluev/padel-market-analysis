#!/usr/bin/env node
// Compare baseline and post audit summaries, write a markdown report.
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const BASE = path.join(ROOT, "evidence", "_mobile_audit");
const OUT = path.join(BASE, "DIFF.md");

async function load(label) {
  try {
    return JSON.parse(
      await fs.readFile(path.join(BASE, label, "summary.json"), "utf8"),
    );
  } catch {
    return null;
  }
}

function key(r) {
  return `${path.basename(r.page, ".html")} / ${r.device}`;
}

function fmt(n, d = 0) {
  if (n === null || n === undefined) return "—";
  return typeof n === "number" ? n.toFixed(d) : String(n);
}

function delta(post, base) {
  if (post === null || base === null || post === undefined || base === undefined) return "—";
  const d = post - base;
  if (Math.abs(d) < 0.5) return "≈";
  return d > 0 ? `+${fmt(d)}` : fmt(d);
}

const baseSummary = await load("baseline");
const postSummary = await load("post");
if (!baseSummary || !postSummary) {
  console.error("Missing baseline or post summary. Run npm run audit:baseline / audit:post first.");
  process.exit(1);
}

const baseMap = new Map(baseSummary.map((r) => [key(r), r]));
const postMap = new Map(postSummary.map((r) => [key(r), r]));

const allKeys = Array.from(new Set([...baseMap.keys(), ...postMap.keys()])).sort();

let md = `# Mobile audit diff — baseline vs. post-redesign\n\n`;
md += `Captured at: ${new Date().toISOString()}\n\n`;
md += `| Page / Device | FCP (ms) | LCP (ms) | CLS | h-Overflow | Small standalone taps | Inline-prose small links |\n`;
md += `|---|---:|---:|---:|---:|---:|---:|\n`;

for (const k of allKeys) {
  const b = baseMap.get(k) || {};
  const p = postMap.get(k) || {};
  const bm = b.metrics || {};
  const pm = p.metrics || {};
  const bSST = bm.tooSmallStandaloneTaps;
  const pSST = pm.tooSmallStandaloneTaps;
  const bIN = bm.tooSmallTaps;
  const pIN = pm.tooSmallTaps;
  md += `| ${k} | ${fmt(bm.fcp, 0)} → ${fmt(pm.fcp, 0)} | ${fmt(bm.lcp, 0)} → ${fmt(pm.lcp, 0)} | ${fmt(bm.cls, 4)} → ${fmt(pm.cls, 4)} | ${bm.horizontalOverflow ? "yes" : "no"} → ${pm.horizontalOverflow ? "yes" : "no"} | ${fmt(bSST)} → ${fmt(pSST)} (${delta(pSST, bSST)}) | ${fmt(bIN)} → ${fmt(pIN)} (${delta(pIN, bIN)}) |\n`;
}

md += `\n## Notes\n\n`;
md += `- **Small standalone taps** are interactive controls (buttons, isolated links) under 44×44 px — the iOS HIG and WCAG 2.5.5 minimum. This count must trend toward 0.\n`;
md += `- **Inline-prose small links** are links inside paragraphs/lists that share a line with surrounding text. WCAG 2.5.5 explicitly excludes these from the 44×44 rule; the count is informational.\n`;
md += `- **CLS** = cumulative layout shift; <0.1 is good; the report has no images so it stays at 0.\n`;
md += `- **LCP** is null/undefined here because the static page has no large image as LCP candidate; FCP is the relevant proxy.\n`;
md += `- **h-Overflow** flags whether the document scrollWidth exceeds the viewport — must remain "no" on every device.\n`;

await fs.writeFile(OUT, md);
console.log(`wrote ${OUT}`);
