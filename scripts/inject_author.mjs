#!/usr/bin/env node
// Idempotent injector for author / contact footer + digital fingerprint
// across every portfolio HTML page. Adds:
//  - <meta name="author"> in <head>
//  - JSON-LD <script type="application/ld+json"> Person/CreativeWork block
//    (this is the search-engine-readable digital fingerprint)
//  - <footer class="author"> at the end of <main> with LinkedIn / Telegram /
//    GitHub repo links
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const FINAL = path.join(ROOT, "reports/final");

const PERSON = {
  name: "Alexandr Valuev",
  linkedin: "https://www.linkedin.com/in/valuev/",
  telegram: "https://t.me/ASNKT",
  github: "https://github.com/avaluev",
  repo: "https://github.com/avaluev/padel-market-analysis",
};

const PAGES = [
  {
    file: "index.html",
    title: "Deep Research OS — Padel AI Coach case study",
    desc: "Multi-agent, multi-model research pipeline. Investor-grade strategic brief produced from a single prompt.",
  },
  {
    file: "padel-ai-coach-research.html",
    title: "Padel AI Coach — Strategic Brief",
    desc: "Investor-grade strategic brief on the Padel AI coaching opportunity.",
  },
  {
    file: "evidence-map.html",
    title: "Padel AI Coach — Evidence Map",
    desc: "Source-trace document for the Padel AI Coach Strategic Brief.",
  },
  {
    file: "methodology.html",
    title: "Deep Research OS — Methodology",
    desc: "The multi-agent pipeline architecture behind the Padel AI Coach research.",
  },
];

function buildJsonLd(page) {
  const ld = {
    "@context": "https://schema.org",
    "@type": "CreativeWork",
    name: page.title,
    description: page.desc,
    inLanguage: "en",
    license: "https://www.apache.org/licenses/LICENSE-2.0",
    isAccessibleForFree: true,
    isPartOf: {
      "@type": "Collection",
      name: "Deep Research OS — Padel AI Coach case study",
      url: PERSON.repo,
    },
    codeRepository: PERSON.repo,
    author: {
      "@type": "Person",
      name: PERSON.name,
      url: PERSON.linkedin,
      sameAs: [PERSON.linkedin, PERSON.telegram, PERSON.github, PERSON.repo],
    },
    creator: {
      "@type": "Person",
      name: PERSON.name,
      url: PERSON.linkedin,
    },
    datePublished: "2026-05-03",
  };
  return `<script type="application/ld+json">\n${JSON.stringify(ld, null, 2)}\n</script>`;
}

function buildAuthorMeta() {
  return [
    `<meta name="author" content="${PERSON.name}">`,
    `<link rel="me" href="${PERSON.linkedin}">`,
    `<link rel="me" href="${PERSON.telegram}">`,
    `<link rel="me" href="${PERSON.github}">`,
  ].join("\n");
}

function buildFooter() {
  return `<footer class="author-foot" role="contentinfo">
  <div class="author-shell">
    <div class="author-line">
      <span class="who">By <strong>${PERSON.name}</strong></span>
      <span class="dot-sep" aria-hidden="true">·</span>
      <a href="${PERSON.linkedin}" rel="me noopener" target="_blank">LinkedIn</a>
      <span class="dot-sep" aria-hidden="true">·</span>
      <a href="${PERSON.telegram}" rel="me noopener" target="_blank">Telegram</a>
      <span class="dot-sep" aria-hidden="true">·</span>
      <a href="${PERSON.repo}" rel="me noopener" target="_blank">GitHub repository</a>
    </div>
    <div class="author-fingerprint">
      <span>Run <code>20260501T135005Z</code></span>
      <span class="dot-sep" aria-hidden="true">·</span>
      <span>Apache 2.0</span>
      <span class="dot-sep" aria-hidden="true">·</span>
      <span>Models: Claude Opus 4.7 + Sonnet 4.6 + Haiku 4.5 · Perplexity Sonar (pro / deep / reasoning) · Alibaba Tongyi 30B (free arm)</span>
    </div>
  </div>
</footer>`;
}

const FOOTER_CSS = `
/* Author footer + digital fingerprint */
.author-foot{
  margin-top:48px;
  padding:24px 0 calc(32px + env(safe-area-inset-bottom,0));
  border-top:1px solid var(--line, #e6e6e6);
  font-size:.825rem;
  color:var(--ink-mute, #71717a);
}
.author-foot .author-shell{
  display:flex;flex-direction:column;gap:8px;
  flex-wrap:wrap;
}
.author-foot .author-line,
.author-foot .author-fingerprint{
  display:flex;flex-wrap:wrap;align-items:center;gap:6px 10px;
}
.author-foot .author-line .who{color:var(--ink-soft, #3f3f46)}
.author-foot .author-line strong{color:var(--ink, #0a0a0a);font-weight:600}
.author-foot a{color:var(--accent, #0a6cf3)}
.author-foot .dot-sep{color:var(--ink-mute, #71717a);user-select:none}
.author-foot code{font-size:.75rem}
@media (min-width:640px){
  .author-foot .author-shell{flex-direction:row;align-items:center;justify-content:space-between}
}
@media print{
  .author-foot{break-before:auto;break-inside:avoid}
  .author-foot a{color:#000}
}
`;

const FOOTER_BEGIN_TAG = '<footer class="author-foot"';
const META_BEGIN = '<meta name="author"';
const LD_BEGIN = '<script type="application/ld+json">';

function stripBetween(html, start, end) {
  // Remove first occurrence of substring spanning [start..end].
  const i = html.indexOf(start);
  if (i === -1) return html;
  const j = html.indexOf(end, i);
  if (j === -1) return html;
  return html.slice(0, i) + html.slice(j + end.length);
}

function ensureHeadInjections(html, page) {
  // Strip any prior author meta + JSON-LD that we previously injected.
  let out = html;
  // Strip prior author meta block (single rel=me lines + author meta)
  out = out.replace(/<meta name="author"[^>]*>\n?/g, "");
  out = out.replace(/<link rel="me"[^>]*>\n?/g, "");
  // Strip prior JSON-LD
  out = out.replace(
    /<script type="application\/ld\+json">[\s\S]*?<\/script>\n?/g,
    "",
  );
  // Inject before </head>
  const block = `${buildAuthorMeta()}\n${buildJsonLd(page)}\n`;
  out = out.replace(/<\/head>/i, `${block}</head>`);
  return out;
}

function ensureFooterStyle(html) {
  if (html.includes("/* Author footer + digital fingerprint */")) return html;
  // Insert just before </style>
  return html.replace(/<\/style>/i, `${FOOTER_CSS}</style>`);
}

function ensureFooter(html) {
  // Strip prior author footer.
  let out = html;
  const begin = out.indexOf(FOOTER_BEGIN_TAG);
  if (begin !== -1) {
    const end = out.indexOf("</footer>", begin);
    if (end !== -1) {
      let cut = end + "</footer>".length;
      if (out[cut] === "\n") cut += 1;
      out = out.slice(0, begin) + out.slice(cut);
    }
  }
  // Insert before </main>
  const footerHtml = buildFooter();
  if (out.includes("</main>")) {
    out = out.replace(/<\/main>/i, `${footerHtml}\n</main>`);
  } else {
    // Fallback: before </body>
    out = out.replace(/<\/body>/i, `${footerHtml}\n</body>`);
  }
  return out;
}

let touched = 0;
for (const page of PAGES) {
  const abs = path.join(FINAL, page.file);
  if (!fs.existsSync(abs)) {
    console.warn(`skip ${page.file}: not found`);
    continue;
  }
  const before = fs.readFileSync(abs, "utf8");
  let after = before;
  after = ensureHeadInjections(after, page);
  after = ensureFooterStyle(after);
  after = ensureFooter(after);
  if (after !== before) {
    fs.writeFileSync(abs, after);
    touched += 1;
    console.log(`injected author + fingerprint into ${page.file}`);
  }
}
console.log(`\n${touched} file(s) touched.`);
