#!/usr/bin/env node
// Idempotent injector for the cross-page top navigation.
//
// On every configured page:
//   1. Inserts <link rel="stylesheet" href="topnav.css"> into <head> (once).
//   2. Inserts a <a class="skip-link"> right after <body>.
//   3. Inserts the <header class="topnav"> with mobile-first hamburger.
//   4. Inserts the small inline <script> that drives the hamburger toggle.
//   5. Adjusts scroll-padding-top and sidenav offsets to clear the sticky bar.
//
// The script is idempotent — running it twice produces the same output.
// It strips any previously-injected nav/script/skip-link before re-inserting.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const FINAL = path.join(ROOT, "reports/final");

// Pages that get the global topnav. Each page declares which nav link should
// be marked aria-current="page".
const PAGES = [
  { file: "index.html", currentHref: "index.html" },
  { file: "padel-ai-coach-research.html", currentHref: "padel-ai-coach-research.html" },
  { file: "evidence-map.html", currentHref: "evidence-map.html" },
  { file: "methodology.html", currentHref: "methodology.html" },
  { file: "competitor-landscape.html", currentHref: "competitor-landscape.html" },
  { file: "subscription-economics.html", currentHref: "subscription-economics.html" },
  { file: "mvp-design.html", currentHref: "mvp-design.html" },
  { file: "90-day-plan.html", currentHref: "90-day-plan.html" },
  { file: "model-provenance.html", currentHref: "model-provenance.html" },
  { file: "404.html", currentHref: null }, // no aria-current
];

// The flat nav. Order shapes the read order of the site.
const NAV_ITEMS = [
  { href: "index.html", label: "Home" },
  { href: "padel-ai-coach-research.html", label: "Strategic brief" },
  { href: "evidence-map.html", label: "Evidence map" },
  { href: "competitor-landscape.html", label: "Competitors" },
  { href: "subscription-economics.html", label: "Economics" },
  { href: "mvp-design.html", label: "MVP design" },
  { href: "90-day-plan.html", label: "90-day plan" },
  { href: "methodology.html", label: "Methodology" },
  { href: "model-provenance.html", label: "Model provenance" },
];

const NAV_SCRIPT = `<script>
// Mobile nav toggle — hamburger drawer with focus management and Esc-to-close.
(function () {
  var btn = document.querySelector('.topnav .nav-toggle');
  var menu = document.getElementById('primary-nav');
  if (!btn || !menu) return;
  function close() { btn.setAttribute('aria-expanded', 'false'); }
  function open() {
    btn.setAttribute('aria-expanded', 'true');
    var first = menu.querySelector('a');
    if (first) first.focus();
  }
  btn.addEventListener('click', function () {
    btn.getAttribute('aria-expanded') === 'true' ? close() : open();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && btn.getAttribute('aria-expanded') === 'true') {
      close();
      btn.focus();
    }
  });
  menu.addEventListener('click', function (e) {
    if (e.target.tagName === 'A' && window.matchMedia('(max-width: 879px)').matches) {
      close();
    }
  });
})();
</script>`;

const SKIP_LINK = '<a class="skip-link" href="#main">Skip to main content</a>';

function buildNav(currentHref) {
  const links = NAV_ITEMS.map((item) => {
    const cur = item.href === currentHref ? ' aria-current="page"' : "";
    return `    <a class="np" href="${item.href}"${cur}>${item.label}</a>`;
  }).join("\n");
  return [
    '<header class="topnav" role="navigation" aria-label="Site navigation">',
    '  <a class="brand" href="index.html"><span class="dot" aria-hidden="true"></span>Padel Research</a>',
    '  <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-nav" aria-label="Open navigation menu">',
    '    <span class="nav-toggle-bar" aria-hidden="true"></span>',
    '    <span class="nav-toggle-bar" aria-hidden="true"></span>',
    '    <span class="nav-toggle-bar" aria-hidden="true"></span>',
    '  </button>',
    '  <nav id="primary-nav" class="nav-links" aria-label="Primary">',
    links,
    '  </nav>',
    "</header>",
  ].join("\n");
}

const STYLE_LINK = '<link rel="stylesheet" href="topnav.css">';

function ensureStylesheet(html) {
  if (html.includes(STYLE_LINK)) return html;
  return html.replace(/<\/head>/i, `${STYLE_LINK}\n</head>`);
}

function stripBlock(html, startMarker, endMarker) {
  const start = html.indexOf(startMarker);
  if (start === -1) return html;
  const end = html.indexOf(endMarker, start);
  if (end === -1) return html;
  let endIdx = end + endMarker.length;
  while (endIdx < html.length && (html[endIdx] === "\n" || html[endIdx] === "\r")) {
    endIdx += 1;
  }
  return html.slice(0, start) + html.slice(endIdx);
}

function stripExistingTopnav(html) {
  // Strip any prior topnav block.
  let out = stripBlock(html, '<header class="topnav"', '</header>');
  // Strip any prior nav script (matches our inserted one or any older one).
  out = out.replace(
    /<script>[\s\S]*?Mobile nav toggle[\s\S]*?<\/script>\n?/g,
    "",
  );
  // Strip any prior skip-link.
  out = out.replace(/<a class="skip-link"[^>]*>[^<]*<\/a>\n?/g, "");
  return out;
}

function insertTopnav(html, navHtml) {
  // Insert skip-link + nav right after <body>, and the nav script before </body>.
  let out = html.replace(/(<body[^>]*>\s*)/i, (m) => `${m}${SKIP_LINK}\n${navHtml}\n`);
  out = out.replace(/<\/body>\s*<\/html>\s*$/i, `${NAV_SCRIPT}\n</body>\n</html>\n`);
  return out;
}

function adjustOffsets(html) {
  let out = html;
  // Bump scroll-padding-top to clear the sticky bar.
  out = out.replace(/scroll-padding-top:\s*\d+px/g, "scroll-padding-top:120px");
  out = out.replace(/(\s)top:\s*24px;/g, "$1top:64px;");
  out = out.replace(
    /max-height:\s*calc\(100vh\s*-\s*48px\)/g,
    "max-height:calc(100vh - 88px)",
  );
  return out;
}

function ensureMainId(html) {
  // The skip-link points to #main. Make sure the page has a target.
  if (html.includes('id="main"')) return html;
  // If there is a <main> tag without id, add it.
  if (/<main\b(?![^>]*id=)/.test(html)) {
    return html.replace(/<main\b/, '<main id="main"');
  }
  return html;
}

let touched = 0;
for (const { file, currentHref } of PAGES) {
  const abs = path.join(FINAL, file);
  if (!fs.existsSync(abs)) {
    console.warn(`skip ${file}: not found`);
    continue;
  }
  const before = fs.readFileSync(abs, "utf8");
  let after = before;
  after = ensureStylesheet(after);
  after = stripExistingTopnav(after);
  after = insertTopnav(after, buildNav(currentHref));
  after = ensureMainId(after);
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
