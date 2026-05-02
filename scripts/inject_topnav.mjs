#!/usr/bin/env node
// Idempotent injector for the cross-page top navigation.
// Inserts <link rel="stylesheet" href="topnav.css"> into <head> and a
// <header class="topnav"> block as the first child of <body> on every
// configured page. Also bumps scroll-padding-top and sidenav top offsets
// to account for the sticky bar.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const FINAL = path.join(ROOT, "reports/final");

const PAGES = [
  { file: "index.html", id: "home" },
  { file: "padel-ai-coach-research.html", id: "brief" },
  { file: "evidence-map.html", id: "evidence" },
  { file: "methodology.html", id: "methodology" },
  { file: "404.html", id: null }, // no aria-current
];

const NAV_ITEMS = [
  { id: "home", href: "index.html", label: "Home" },
  { id: "brief", href: "padel-ai-coach-research.html", label: "Strategic Brief" },
  { id: "evidence", href: "evidence-map.html", label: "Evidence Map" },
  { id: "methodology", href: "methodology.html", label: "Methodology" },
];

function buildNav(currentId) {
  const links = NAV_ITEMS.map((item) => {
    const cur = item.id === currentId ? ' aria-current="page"' : "";
    return `    <a class="np" href="${item.href}"${cur}>${item.label}</a>`;
  }).join("\n");
  return [
    `<header class="topnav" role="navigation" aria-label="Cross-page navigation">`,
    `  <a class="brand" href="index.html"><span class="dot" aria-hidden="true"></span>Deep Research OS</a>`,
    links,
    `  <span class="spacer"></span>`,
    `  <span class="ext">Run 20260501T135005Z</span>`,
    `</header>`,
  ].join("\n");
}

const STYLE_LINK = `<link rel="stylesheet" href="topnav.css">`;
const TOPNAV_BEGIN = "<header class=\"topnav\"";
const TOPNAV_END_TAG = "</header>";

function ensureStylesheet(html) {
  if (html.includes(STYLE_LINK)) return html;
  // Insert just before </head>
  return html.replace(/<\/head>/i, `${STYLE_LINK}\n</head>`);
}

function stripExistingTopnav(html) {
  // Remove any previously-injected topnav block (idempotency).
  const start = html.indexOf(TOPNAV_BEGIN);
  if (start === -1) return html;
  const end = html.indexOf(TOPNAV_END_TAG, start);
  if (end === -1) return html;
  // include the closing tag and trailing newline (if any)
  let endIdx = end + TOPNAV_END_TAG.length;
  if (html[endIdx] === "\n") endIdx += 1;
  return html.slice(0, start) + html.slice(endIdx);
}

function insertTopnav(html, navHtml) {
  // Insert just after <body> (skipping any attributes).
  return html.replace(/(<body[^>]*>\s*)/i, (m) => `${m}${navHtml}\n`);
}

function adjustOffsets(html) {
  // Scroll-padding-top: bump to leave room for sticky topnav.
  let out = html.replace(
    /scroll-padding-top:\s*72px/g,
    "scroll-padding-top:120px",
  );
  // Sidenav top offset: bump from 24px to 64px so it sits below the topnav.
  out = out.replace(/(\s)top:\s*24px;/g, "$1top:64px;");
  out = out.replace(/(\s)top:\s*24px;\s*align-self:\s*start/g, " top:64px;align-self:start");
  // The mobile bottom-sheet calculation `calc(100vh - 48px)` (max-height of
  // the desktop rail) should subtract the topnav height too.
  out = out.replace(
    /max-height:\s*calc\(100vh\s*-\s*48px\)/g,
    "max-height:calc(100vh - 88px)",
  );
  return out;
}

let touched = 0;
for (const { file, id } of PAGES) {
  const abs = path.join(FINAL, file);
  if (!fs.existsSync(abs)) {
    console.warn(`skip ${file}: not found`);
    continue;
  }
  const before = fs.readFileSync(abs, "utf8");
  let after = before;
  after = ensureStylesheet(after);
  after = stripExistingTopnav(after);
  after = insertTopnav(after, buildNav(id));
  after = adjustOffsets(after);
  if (after !== before) {
    fs.writeFileSync(abs, after);
    touched += 1;
    console.log(`injected topnav into ${file}`);
  } else {
    console.log(`no changes for ${file}`);
  }
}
console.log(`\n${touched} file(s) touched.`);
