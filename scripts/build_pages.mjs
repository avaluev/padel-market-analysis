#!/usr/bin/env node
// Build the public site pages for the Padel Coaching Research portfolio.
//
// Reads markdown deliverables from reports/sources/deliverables/*.md,
// skips files marked DROP, applies content sanitisation (no internal IDs,
// no run timestamps, no first-person, no marketing badges), wraps each page
// in an AI-search-optimised HTML shell (JSON-LD, Open Graph, Twitter Card,
// canonical URL, semantic HTML5), and writes the result FLAT under
// reports/final/.
//
// Output URL set:
//   /                            (index.html, untouched here)
//   /padel-ai-coach-research.html  (main strategic brief, untouched here)
//   /evidence-map.html             (evidence trace, untouched here)
//   /methodology.html              (pipeline doc, untouched here)
//   /competitor-landscape.html     (was sources/competitor-intelligence)
//   /subscription-economics.html   (flattened)
//   /mvp-design.html               (was mvp-loop-design, REWRITTEN)
//   /90-day-plan.html              (was 30-60-90-plan)
//   /model-provenance.html         (flattened)
//
// Removed entirely:
//   /sources/jd-coverage-map.html  — deleted, history scrubbed
//
// Screenshots land in /screenshots/ (flat).

import { readFileSync, writeFileSync, readdirSync, mkdirSync, existsSync, unlinkSync, rmSync } from 'fs';
import { join, basename, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const ROOT = dirname(dirname(__filename));
const SRC_DIR = join(ROOT, 'reports/sources/deliverables');
const OUT_DIR = join(ROOT, 'reports/final');
const SHOTS_SRC = join(ROOT, 'reports/sources/screenshots');
const SHOTS_OUT = join(OUT_DIR, 'screenshots');

const SITE_ORIGIN = 'https://avaluev.github.io/padel-market-analysis';
const PUBLISHED = '2026-05-03';
const MODIFIED = new Date().toISOString().slice(0, 10);

mkdirSync(OUT_DIR, { recursive: true });
mkdirSync(SHOTS_OUT, { recursive: true });

// Page registry. SOURCE → output slug + metadata. Anything not listed is skipped.
const PAGES = {
  '01_competitor_intelligence.md': {
    slug: 'competitor-landscape',
    title: 'Padel Coaching Tech: Competitor Landscape',
    h1: 'Padel coaching tech — competitor landscape',
    description: 'Independent analysis of padel coaching apps, club software, and racket-sport AI: who has data moats, where the gaps sit, what failed and why. May 2026.',
    summary: 'A market scan of padel coaching tech in May 2026 finds the rating-clarity layer unowned: court-software vendors hold booking data without coaching insight, racket-sport AI vendors hold insight without booking distribution, and no single product compounds both. The full peer table covers seventeen vendors across padel, fitness, and racket-sport AI.',
    keywords: ['padel coaching apps', 'padel AI', 'racket sport analytics', 'padel competitor analysis 2026'],
    pageType: 'Article',
  },
  '02_subscription_economics.md': {
    slug: 'subscription-economics',
    title: 'Padel App Subscription Economics: Pricing, Churn, LTV/CAC',
    h1: 'Padel app subscription economics — pricing, churn, LTV/CAC',
    description: 'How a padel coaching subscription would price against eight verified anchors, with monthly churn, LTV/CAC by channel, and four geographic scenarios. Sourced data, no fabricated numbers.',
    summary: 'Eight verified subscription anchors across fitness and racket-sport markets in May 2026 frame a USD 12 to USD 15 monthly ceiling for consumer padel apps. Modelling four pricing scenarios (Portugal, Spain and Italy, the United Arab Emirates, and Russia) shows organic newsletter is the only acquisition channel that clears a healthy LTV-to-CAC ratio in every scenario; paid Meta only works above the EUR 7.99 anchor and at lower churn.',
    keywords: ['padel app pricing', 'subscription LTV CAC', 'sport tech churn benchmarks', 'organic newsletter SaaS'],
    pageType: 'Article',
  },
  '03_mvp_loop_design.md': {
    slug: 'mvp-design',
    title: 'Padel AI MVP Design: Capture, Insight, Practice Loop',
    h1: 'Padel AI MVP — capture, insight, practice loop',
    description: 'A visual-first MVP design for a padel coaching AI: a three-stage product loop, three pilot tracks compared, a decision tree, and a five-row risk register. Plain language, no jargon.',
    summary: 'A working padel coaching AI needs three things to compound into a product, not a tool: smartphone capture that succeeds without club hardware, an insight that a player can act on in their next session, and a coach who can sign off on the result. The three pilot tracks below trade speed against learning depth; the diagram shows what to build first under three different conditions.',
    keywords: ['padel MVP', 'product loop design', 'AI coaching pilot', 'padel app prototype'],
    pageType: 'Article',
  },
  '04_30_60_90_plan.md': {
    slug: '90-day-plan',
    title: 'Padel AI Platform: First 90 Days Operating Plan',
    h1: 'Padel AI platform — first 90 days operating plan',
    description: 'A first-quarter operating plan for a padel coaching AI: twelve testable hypotheses, a metric tree from north star to leading indicators, and a five-row risk register with named exit criteria.',
    summary: 'A first-quarter operating plan for a padel coaching AI is structured around twelve testable hypotheses, a metric tree from the headline number down to weekly leading indicators, and a risk register with named exit criteria. Days 1 to 30 focus on capture-quality validation in a single club; days 31 to 60 add a coach panel and the first paid cohort; days 61 to 90 measure ninety-day paid retention before any second-club expansion.',
    keywords: ['90 day plan', 'product lead operating plan', 'startup hypothesis testing', 'metric tree'],
    pageType: 'Article',
  },
  '06_model_provenance.md': {
    slug: 'model-provenance',
    title: 'Model Provenance: Every Model Used in This Research',
    h1: 'Model provenance — every model used in this research',
    description: 'Full disclosure of every AI model invoked across the research pipeline, the role each model played, and which billing class it fell under. Paid Anthropic, paid Perplexity, plus the single free Alibaba arm.',
    summary: 'Every AI model used in this research is named, with the artefact it produced and its billing class. Strategic synthesis used paid Anthropic Claude Opus and Sonnet. Deep web research used paid Perplexity Sonar (pro, deep research, and reasoning tiers) plus a single free Alibaba Tongyi DeepResearch arm as a cross-check. Structured extraction used Claude Haiku. No model output was accepted without a verifiable source URL.',
    keywords: ['AI research transparency', 'model provenance', 'multi model orchestration', 'AI accountability'],
    pageType: 'Article',
  },
  // SKIP: '05_jd_coverage_map.md' — deleted entirely. The source file should be removed.
};

const SKIPPED_SLUGS = new Set(['jd-coverage-map']);

// Topnav structure. Order matters. Items with `external: true` get target=_blank.
const NAV = [
  { href: 'index.html', label: 'Home' },
  { href: 'padel-ai-coach-research.html', label: 'Strategic brief' },
  { href: 'evidence-map.html', label: 'Evidence map' },
  { href: 'competitor-landscape.html', label: 'Competitors' },
  { href: 'subscription-economics.html', label: 'Economics' },
  { href: 'mvp-design.html', label: 'MVP design' },
  { href: '90-day-plan.html', label: '90-day plan' },
  { href: 'methodology.html', label: 'Methodology' },
  { href: 'model-provenance.html', label: 'Model provenance' },
];

// ------------------------------------------------------------------ md → html

const RUN_ID_REGEX = /\b\d{8}T\d{6}Z\b/g;

// Sanitiser. Applied to every markdown source before conversion.
// Removes run-id leaks, internal IDs, jargon, "candidate" framing, and the
// boilerplate metadata block that duplicates information now in the page shell.
function sanitiseMarkdown(md, page) {
  let out = md;

  // Drop the markdown H1 — we render H1 from page metadata.
  out = out.replace(/^# .+\n/, '');

  // Drop the boilerplate metadata block immediately after the H1:
  //   **Deliverable:** ...
  //   **Audience:** ...
  //   **Voice:** ...
  //   **Posture:** ...
  //   **Backing data:** ...
  //   **Anchor evidence:** ...
  //   **Run anchor:** ...
  out = out.replace(
    /(?:^\*\*(?:Deliverable|Audience|Voice|Posture|Backing data|Anchor evidence|Run anchor):\*\*[^\n]*\n)+/gm,
    ''
  );

  // Strip a leading lede paragraph that duplicates the page summary verbatim.
  // Heuristic: if the first 250 characters of the (now H1-stripped) source
  // contain hyperbolic framing patterns we want gone, drop the para.
  const hyperbolePatterns = [
    /live or die on/i,
    /every other acquisition path operates below the SaaS 3:1 floor at honest churn/i,
    /the riskiest assumption in a Padel AI Platform is value, not scalability/i,
  ];
  for (const re of hyperbolePatterns) {
    out = out.replace(re, '');
  }

  // Run-ID timestamps anywhere → strip the surrounding code/path/word fragment.
  // CRITICAL: handle markdown links `[text](url)` where url contains run-id
  // FIRST, otherwise the URL gets replaced with prose creating broken hrefs.
  // Pattern: `[backtick-wrapped name](path with run-id)` → just the name
  out = out.replace(/\[(`[^`]+`)\]\([^)]*evidence\/\d{8}T\d{6}Z\/[^)]*\)/g, '$1');
  // Pattern: `[plain text name](path with run-id)` → just plain text name
  out = out.replace(/\[([^\]]+)\]\([^)]*evidence\/\d{8}T\d{6}Z\/[^)]*\)/g, '$1');
  // Also strip evidence/.../file.json links that have NO run-id but reference
  // internal JSON files (these aren't part of the public site).
  out = out.replace(/\[(`[^`]+`)\]\([^)]*\.\.\/evidence\/[^)]+\)/g, '$1');
  out = out.replace(/\[([^\]]+)\]\([^)]*\.\.\/evidence\/[^)]+\)/g, '$1');
  out = out.replace(/\[(`[^`]+`)\]\([^)]*\.\.\/\.\.\/\.\.\/evidence\/[^)]+\)/g, '$1');
  out = out.replace(/\[([^\]]+)\]\([^)]*\.\.\/\.\.\/\.\.\/evidence\/[^)]+\)/g, '$1');

  // Now strip remaining bare references in prose / code spans.
  out = out.replace(/`evidence\/\d{8}T\d{6}Z\/[^`]*`/g, '`the published evidence`');
  out = out.replace(/evidence\/\d{8}T\d{6}Z\/[^\s`)\]]+/g, 'the published evidence');
  out = out.replace(/`evidence\/\d{8}T\d{6}Z\/`/g, '`the evidence directory`');
  out = out.replace(/Run\s+\d{8}T\d{6}Z/gi, '');
  out = out.replace(RUN_ID_REGEX, '');

  // "Candidate" framing → drop the qualifier (per locked plan decision).
  // First strip whole dependent clauses we want gone entirely.
  out = out.replace(/[Tt]he candidate is not a padel player\.\s*/g, '');
  out = out.replace(/[Tt]he candidate has no domain expertise[^.]*\.\s*/g, '');
  // "the/a/an candidate's X" → "the/a/an X"
  out = out.replace(/\b([Tt]he|[Aa]|[Aa]n)\s+candidate's\s+/g, '$1 ');
  // "the/a/an/this/that/every candidate X" → "the/a/an/... X"
  out = out.replace(
    /\b([Tt]he|[Aa]|[Aa]n|[Tt]hat|[Tt]his|[Tt]hose|[Tt]hese|[Ee]very|[Ss]ix|[Tt]wo|[Tt]hree|[Ff]our|[Ff]ive|[Ee]ight|[Tt]en|[Ee]leven)\s+candidate\s+(?=\w)/g,
    '$1 '
  );
  // Generic "X candidate Y" → "X Y"
  out = out.replace(/\bcandidate\s+(?=[a-z])/g, '');
  // Plural fallback
  out = out.replace(/\bcandidates\b/g, 'options');
  // Bare singular fallback (rare; prose like "the candidate." standalone)
  out = out.replace(/\b[Cc]andidate\b/g, '');

  // Internal IDs → name the thing instead of the ID.
  // Strip `(VM-001 in evidence...)` style parentheticals.
  out = out.replace(/\s*\([A-Z]{2,4}-\d{2,3}[^)]*\)/g, '');
  // Strip bare `VM-001`, `CH-006`, `RL-001`, `PB-005`, `PLG-005`, `FM-101`,
  // `DG-04`, `JS-001`, `SEG-001`, `CC-1`, `FM-3` style identifiers.
  out = out.replace(/\b(?:VM|CH|RL|PB|PLG|FM|DG|JS|SEG|CC|MM|SC|UC|FE|SC)-\d{1,3}\b/g, '');

  // JSON file paths inline → describe in prose.
  out = out.replace(/`\d{2}_[a-z_]+\.json(?:#[^`]+)?`/g, 'the published evidence');
  out = out.replace(/\b\d{2}_[a-z_]+\.json\b/g, 'the published evidence');
  out = out.replace(/`evidence\/[^`]+`/g, 'the published evidence');
  out = out.replace(/\bevidence\/[a-z0-9_/.-]+\b/g, 'the published evidence');

  // Jargon replacements (case-preserving where reasonable).
  const JARGON = [
    [/\bkill experiment(s)?\b/gi, 'stop test$1'],
    [/\bkill criteri(?:on|a)\b/gi, 'exit criteria'],
    [/\bkill threshold(s)?\b/gi, 'exit threshold$1'],
    [/\bkill signal(s)?\b/gi, 'stop signal$1'],
    [/\bkill metric(s)?\b/gi, 'stop metric$1'],
    [/\bkill_signals?\b/gi, 'stop signals'],
    [/\bkill_experiment(s)?\b/gi, 'stop test$1'],
    [/\bkill\b/gi, 'stop'],
    [/\bnorth star metric\b/gi, 'the one number that matters'],
    [/\bnorth star\b/gi, 'headline metric'],
    [/\bred[- ]team(?:ed|ing)?\b/gi, 'adversarial review'],
    [/\bRED-team\b/g, 'adversarial review'],
    [/\bWizard of Oz\b/g, 'manual prototype'],
    [/\banti[- ]pattern(s)?\b/gi, 'wrong move$1'],
    [/\bdata gap(s)?\b/gi, 'data gap$1'],
    [/\bdata_gaps?\b/gi, 'data gaps'],
    [/\bB2B2C\b/g, 'business-to-business-to-consumer'],
    [/\bB2B\b/g, 'business-to-business'],
    [/\bB2C\b/g, 'business-to-consumer'],
    [/\bGTM\b/g, 'go-to-market'],
    [/\bJTBD\b/g, 'jobs-to-be-done'],
    [/\bPLG\b/g, 'product-led growth'],
    // Citation-status tags should not appear in user-facing prose.
    [/\bVERIFIED_INHERITED\b/g, ''],
    [/\bINFERRED_INHERITED\b/g, ''],
    [/\bVERIFIED\b/g, ''],
    [/\bINFERRED\b/g, ''],
    [/\bABSENT\b/g, ''],
    [/\bASSUMPTION\b/g, ''],
  ];
  for (const [re, replacement] of JARGON) {
    out = out.replace(re, replacement);
  }

  // Dangling `— *` separators that the citation-tag stripping leaves behind.
  out = out.replace(/\s*—\s*\*\s*\*\s*/g, ' ');
  out = out.replace(/\s*\(\s*\*\s*\)\s*/g, ' ');
  // Empty parentheses created by ID stripping.
  out = out.replace(/\(\s*\)/g, '');
  // Double spaces left over.
  out = out.replace(/  +/g, ' ');
  // Trailing spaces on lines.
  out = out.replace(/[ \t]+$/gm, '');
  // Triple-blank-line collapse.
  out = out.replace(/\n{3,}/g, '\n\n');

  // Soften specific hyperbolic claims that were already flagged.
  out = out.replace(
    /Subscription economics for the Padel AI Platform live or die on one channel: organic newsletter\. Every other acquisition path operates below the SaaS 3:1 floor at honest churn, so the channel-mix decision is the pricing decision\./,
    'At the published USD 12 newsletter cost-per-acquisition, organic newsletter is the only acquisition channel that clears a healthy LTV-to-CAC ratio in every pricing scenario modelled below. Other channels work above specific price points; the channel mix decision and the pricing decision are linked.'
  );

  return out;
}

// Markdown to HTML.
// Handles: headings, paragraphs, lists (ul/ol), tables (with caption),
// blockquotes, code blocks, images, links (both [text](url) and <url> auto-link),
// inline code, bold, italic, horizontal rules.
// Block-level HTML tags that should pass through as-is, not wrapped in <p>.
const HTML_BLOCK_OPEN = /^<(figure|svg|div|aside|section|details|nav|table|ul|ol|pre|video|iframe|article)\b/i;
const HTML_BLOCK_CLOSE = /^<\/(figure|svg|div|aside|section|details|nav|table|ul|ol|pre|video|iframe|article)>\s*$/i;

function md2html(md) {
  const lines = md.split('\n');
  const out = [];
  let inCode = false;
  let inList = false;
  let inOL = false;
  let inTable = false;
  let tableHeader = false;
  let inHtmlBlock = false;
  let htmlBlockTag = '';
  let htmlDepth = 0;
  let para = [];

  function inline(s) {
    // Images first, before link conversion eats `![]()`.
    s = s.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, (_m, alt, url) => {
      const safeAlt = alt.replace(/"/g, '&quot;');
      // Local screenshot reference becomes <figure> with width/height for CLS.
      if (/^screenshots\//.test(url) || /^\.\.?\//.test(url)) {
        const cleanUrl = url.replace(/^\.\.\//, '');
        return `<figure class="shot"><img src="${cleanUrl}" alt="${safeAlt}" loading="lazy" decoding="async" width="1280" height="800"><figcaption>${safeAlt}</figcaption></figure>`;
      }
      return `<figure class="shot"><img src="${url}" alt="${safeAlt}" loading="lazy" decoding="async"><figcaption>${safeAlt}</figcaption></figure>`;
    });
    // Markdown links [text](url)
    s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_m, text, url) => {
      const isExternal = /^https?:\/\//.test(url);
      return isExternal
        ? `<a href="${url}" rel="noopener" target="_blank">${text}</a>`
        : `<a href="${url}">${text}</a>`;
    });
    // Markdown angle-bracket auto-links <https://...>
    // (this is the bug that broke the URL register)
    s = s.replace(/<(https?:\/\/[^>\s]+)>/g, (_m, url) =>
      `<a href="${url}" rel="noopener" target="_blank">${url}</a>`
    );
    // Bold
    s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    // Italic
    s = s.replace(/(^|[^*])\*([^*\s][^*]*[^*\s]|[^*\s])\*/g, '$1<em>$2</em>');
    // Inline code
    s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
    return s;
  }

  const flushPara = () => {
    if (para.length) {
      out.push('<p>' + inline(para.join(' ').trim()) + '</p>');
      para = [];
    }
  };
  const flushList = () => {
    if (inList) { out.push('</ul>'); inList = false; }
    if (inOL) { out.push('</ol>'); inOL = false; }
  };
  const flushTable = () => {
    if (inTable) { out.push('</tbody></table></div>'); inTable = false; }
  };

  for (let raw of lines) {
    const line = raw.replace(/\r$/, '');

    // Code fences
    if (line.startsWith('```')) {
      flushPara(); flushList(); flushTable();
      inCode = !inCode;
      out.push(inCode ? '<pre><code>' : '</code></pre>');
      continue;
    }
    if (inCode) {
      out.push(line.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'));
      continue;
    }

    // Raw HTML block: pass through unchanged. Track depth of the outer tag.
    if (!inHtmlBlock) {
      const m = line.match(HTML_BLOCK_OPEN);
      if (m) {
        flushPara(); flushList(); flushTable();
        inHtmlBlock = true;
        htmlBlockTag = m[1].toLowerCase();
        htmlDepth = 1;
        // Count any other opens / closes on this single line.
        const openRe = new RegExp(`<${htmlBlockTag}\\b`, 'gi');
        const closeRe = new RegExp(`</${htmlBlockTag}>`, 'gi');
        const opens = (line.match(openRe) || []).length;
        const closes = (line.match(closeRe) || []).length;
        htmlDepth += (opens - 1) - closes;
        out.push(line);
        if (htmlDepth <= 0) { inHtmlBlock = false; htmlBlockTag = ''; }
        continue;
      }
    } else {
      const openRe = new RegExp(`<${htmlBlockTag}\\b`, 'gi');
      const closeRe = new RegExp(`</${htmlBlockTag}>`, 'gi');
      htmlDepth += (line.match(openRe) || []).length;
      htmlDepth -= (line.match(closeRe) || []).length;
      out.push(line);
      if (htmlDepth <= 0) { inHtmlBlock = false; htmlBlockTag = ''; }
      continue;
    }

    // Horizontal rule
    if (/^---+\s*$/.test(line)) {
      flushPara(); flushList(); flushTable();
      out.push('<hr>');
      continue;
    }

    // Headings
    const headingMatch = line.match(/^(#{1,6})\s+(.+)$/);
    if (headingMatch) {
      flushPara(); flushList(); flushTable();
      const level = headingMatch[1].length;
      const text = headingMatch[2];
      // Slugify for anchor IDs (used by AEO jump-link patterns).
      const id = text.toLowerCase()
        .replace(/<[^>]+>/g, '')
        .replace(/[^a-z0-9\s-]/g, '')
        .trim()
        .replace(/\s+/g, '-')
        .slice(0, 60);
      out.push(`<h${level} id="${id}">${inline(text)}</h${level}>`);
      continue;
    }

    // Tables
    if (/^\s*\|.+\|\s*$/.test(line)) {
      flushPara(); flushList();
      const isSeparator = /^\s*\|[\s:|-]+\|\s*$/.test(line);
      if (!inTable && !isSeparator) {
        out.push('<div class="table-wrap"><table>');
        inTable = true;
        tableHeader = true;
      }
      if (isSeparator) {
        if (tableHeader) {
          // Already emitted thead opening in the previous header row branch.
        }
        tableHeader = false;
        continue;
      }
      const cells = line.trim().slice(1, -1).split('|').map((c) => c.trim());
      if (tableHeader) {
        out.push('<thead><tr>' + cells.map((c) => `<th>${inline(c)}</th>`).join('') + '</tr></thead><tbody>');
      } else {
        out.push('<tr>' + cells.map((c) => `<td>${inline(c)}</td>`).join('') + '</tr>');
      }
      continue;
    } else if (inTable) {
      flushTable();
    }

    // Lists
    if (/^\s*[-*]\s+/.test(line)) {
      flushPara();
      if (inOL) { out.push('</ol>'); inOL = false; }
      if (!inList) { out.push('<ul class="crisp">'); inList = true; }
      out.push('<li>' + inline(line.replace(/^\s*[-*]\s+/, '')) + '</li>');
      continue;
    }
    if (/^\s*\d+\.\s+/.test(line)) {
      flushPara();
      if (inList) { out.push('</ul>'); inList = false; }
      if (!inOL) { out.push('<ol class="crisp">'); inOL = true; }
      out.push('<li>' + inline(line.replace(/^\s*\d+\.\s+/, '')) + '</li>');
      continue;
    }

    // Blank line
    if (line.trim() === '') {
      flushPara(); flushList();
      continue;
    }

    // Blockquote
    if (line.startsWith('> ')) {
      flushPara(); flushList();
      out.push('<blockquote>' + inline(line.slice(2)) + '</blockquote>');
      continue;
    }

    // Default: paragraph accumulation
    para.push(line);
  }

  flushPara(); flushList(); flushTable();
  return out.join('\n');
}

// ------------------------------------------------------------------ shell

function jsonLdArticle(page) {
  const url = `${SITE_ORIGIN}/${page.slug}.html`;
  return JSON.stringify({
    '@context': 'https://schema.org',
    '@type': page.pageType,
    'headline': page.h1,
    'description': page.description,
    'inLanguage': 'en',
    'url': url,
    'mainEntityOfPage': { '@type': 'WebPage', '@id': url },
    'datePublished': PUBLISHED,
    'dateModified': MODIFIED,
    'author': {
      '@type': 'Person',
      'name': 'Alexandr Valuev',
      'url': 'https://www.linkedin.com/in/valuev/',
      'sameAs': [
        'https://www.linkedin.com/in/valuev/',
        'https://github.com/avaluev',
        'https://t.me/ASNKT',
      ],
    },
    'publisher': {
      '@type': 'Organization',
      'name': 'Deep Research OS',
      'url': SITE_ORIGIN,
    },
    'keywords': page.keywords.join(', '),
    'isAccessibleForFree': true,
    'license': 'https://www.apache.org/licenses/LICENSE-2.0',
  }, null, 2);
}

function jsonLdBreadcrumb(page) {
  const url = `${SITE_ORIGIN}/${page.slug}.html`;
  return JSON.stringify({
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    'itemListElement': [
      { '@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': `${SITE_ORIGIN}/` },
      { '@type': 'ListItem', 'position': 2, 'name': page.h1, 'item': url },
    ],
  }, null, 2);
}

function navHtml(currentSlug) {
  const items = NAV.map((n) => {
    const isActive = n.href === `${currentSlug}.html`;
    return `<a class="np" href="${n.href}"${isActive ? ' aria-current="page"' : ''}>${n.label}</a>`;
  }).join('\n  ');
  return `<header class="topnav" role="navigation" aria-label="Site navigation">
  <a class="brand" href="index.html"><span class="dot" aria-hidden="true"></span>Padel Research</a>
  <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-nav" aria-label="Open navigation menu">
    <span class="nav-toggle-bar" aria-hidden="true"></span>
    <span class="nav-toggle-bar" aria-hidden="true"></span>
    <span class="nav-toggle-bar" aria-hidden="true"></span>
  </button>
  <nav id="primary-nav" class="nav-links" aria-label="Primary">
  ${items}
  </nav>
</header>`;
}

function shell(page, bodyHtml) {
  const url = `${SITE_ORIGIN}/${page.slug}.html`;
  const ogImage = `${SITE_ORIGIN}/og-default.png`;
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0a0a0a" media="(prefers-color-scheme: dark)">
<meta name="color-scheme" content="light dark">
<meta name="description" content="${page.description}">
<meta name="keywords" content="${page.keywords.join(', ')}">
<meta name="author" content="Alexandr Valuev">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta property="og:type" content="article">
<meta property="og:title" content="${page.title}">
<meta property="og:description" content="${page.description}">
<meta property="og:url" content="${url}">
<meta property="og:image" content="${ogImage}">
<meta property="og:site_name" content="Padel Coaching Tech Research">
<meta property="og:locale" content="en_US">
<meta property="article:published_time" content="${PUBLISHED}T00:00:00Z">
<meta property="article:modified_time" content="${MODIFIED}T00:00:00Z">
<meta property="article:author" content="https://www.linkedin.com/in/valuev/">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="${page.title}">
<meta name="twitter:description" content="${page.description}">
<meta name="twitter:image" content="${ogImage}">
<title>${page.title}</title>
<link rel="canonical" href="${url}">
<link rel="alternate" type="application/rss+xml" title="Padel Research" href="${SITE_ORIGIN}/feed.xml">
<link rel="me" href="https://www.linkedin.com/in/valuev/">
<link rel="me" href="https://t.me/ASNKT">
<link rel="me" href="https://github.com/avaluev">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<script type="application/ld+json">
${jsonLdArticle(page)}
</script>
<script type="application/ld+json">
${jsonLdBreadcrumb(page)}
</script>
<style>
  :root{
    --bg:#fff; --bg-soft:#fafafa; --bg-card:#fff; --bg-elev:#f5f7fa;
    --ink:#0a0a0a; --ink-soft:#3f3f46; --ink-mute:#71717a;
    --line:#e6e6e6;
    --accent:#0a6cf3; --accent-soft:#e6efff; --accent-ink:#fff;
    --good:#0a8a52; --warn:#b54708; --bad:#b42318;
    --shadow:0 1px 2px rgba(0,0,0,.04),0 1px 1px rgba(0,0,0,.04);
    --shadow-elev:0 6px 24px rgba(0,0,0,.08);
    --radius:10px;
    --safe-l:env(safe-area-inset-left,0); --safe-r:env(safe-area-inset-right,0); --safe-b:env(safe-area-inset-bottom,0);
  }
  @media (prefers-color-scheme: dark){
    :root{
      --bg:#0a0a0a; --bg-soft:#101012; --bg-card:#141416; --bg-elev:#181a1d;
      --ink:#fafafa; --ink-soft:#d4d4d8; --ink-mute:#a1a1aa;
      --line:#27272a;
      --accent:#3b9bff; --accent-soft:#0e2440; --accent-ink:#0a0a0a;
      --good:#2f9961; --warn:#d97706; --bad:#ef4444;
      --shadow-elev:0 6px 24px rgba(0,0,0,.5);
    }
  }
  *,*::before,*::after{box-sizing:border-box}
  html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
  @media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{animation-duration:.001ms !important;transition-duration:.001ms !important}}
  body{margin:0;background:var(--bg);color:var(--ink);
    font:400 17px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI Variable","Segoe UI","SF Pro Text",system-ui,Roboto,"Helvetica Neue",Arial,sans-serif;
    -webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;
    padding-left:var(--safe-l);padding-right:var(--safe-r);
    overflow-x:clip;
    text-rendering:optimizeLegibility;
    font-feature-settings:"kern","liga","calt","ss01";
  }
  a{color:var(--accent);text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:2px;text-decoration-color:color-mix(in srgb,var(--accent) 35%,transparent)}
  a:hover{text-decoration-color:var(--accent)}
  :focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:4px}
  ::selection{background:color-mix(in srgb,var(--accent) 30%,transparent);color:var(--ink)}

  .skip-link{position:absolute;left:-9999px;top:auto;width:1px;height:1px;overflow:hidden}
  .skip-link:focus{position:fixed;left:8px;top:8px;z-index:200;width:auto;height:auto;padding:8px 12px;background:var(--accent);color:#fff;border-radius:6px}

  /* Top nav: mobile-first hamburger drawer, expands to row on tablet+ */
  .topnav{position:sticky;top:0;z-index:60;background:color-mix(in srgb,var(--bg) 92%,transparent);-webkit-backdrop-filter:saturate(140%) blur(8px);backdrop-filter:saturate(140%) blur(8px);border-bottom:1px solid var(--line);padding:8px 16px;display:flex;align-items:center;gap:8px;min-height:52px}
  .topnav .brand{display:inline-flex;align-items:center;gap:8px;font-weight:700;color:var(--ink);text-decoration:none;font-size:.95rem;letter-spacing:-.01em;flex-shrink:0}
  .topnav .brand .dot{width:8px;height:8px;border-radius:50%;background:var(--accent);display:inline-block}
  .nav-toggle{margin-left:auto;display:inline-flex;flex-direction:column;justify-content:center;gap:4px;width:44px;height:44px;padding:10px;border:1px solid var(--line);border-radius:8px;background:var(--bg-soft);cursor:pointer}
  .nav-toggle:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
  .nav-toggle-bar{display:block;width:100%;height:2px;background:var(--ink);border-radius:2px;transition:transform 200ms ease,opacity 200ms ease}
  .nav-toggle[aria-expanded="true"] .nav-toggle-bar:nth-child(1){transform:translateY(6px) rotate(45deg)}
  .nav-toggle[aria-expanded="true"] .nav-toggle-bar:nth-child(2){opacity:0}
  .nav-toggle[aria-expanded="true"] .nav-toggle-bar:nth-child(3){transform:translateY(-6px) rotate(-45deg)}
  .nav-links{display:none;position:absolute;left:0;right:0;top:52px;flex-direction:column;gap:2px;padding:12px;background:var(--bg);border-bottom:1px solid var(--line);box-shadow:var(--shadow-elev);max-height:calc(100vh - 52px);overflow-y:auto}
  .nav-links a.np{display:block;padding:12px 14px;border-radius:8px;color:var(--ink-soft);text-decoration:none;font-size:.95rem;font-weight:500;min-height:44px}
  .nav-links a.np:hover{background:var(--bg-soft);color:var(--ink)}
  .nav-links a.np[aria-current="page"]{background:var(--accent-soft);color:var(--accent);font-weight:600}
  .nav-toggle[aria-expanded="true"] + .nav-links{display:flex}
  @media (min-width:880px){
    .nav-toggle{display:none}
    .nav-links{display:flex !important;position:static;flex-direction:row;flex-wrap:wrap;gap:4px;padding:0;background:transparent;border:none;box-shadow:none;max-height:none;overflow:visible;flex:1}
    .nav-links a.np{padding:8px 12px;font-size:.875rem;min-height:36px;display:inline-flex;align-items:center}
  }
  @media print{.topnav{display:none}}

  .wrap{max-width:760px;margin:0 auto;padding:clamp(24px,6vw,64px) clamp(16px,5vw,28px) calc(64px + var(--safe-b))}
  @media (min-width:1024px){ .wrap{max-width:780px} }

  h1{font-size:clamp(1.875rem,1.5rem + 2.2vw,2.6rem);line-height:1.12;letter-spacing:-0.025em;margin:0 0 .5em;text-wrap:balance;color:var(--ink);font-weight:700}
  h2{font-size:clamp(1.25rem,1.05rem + .65vw,1.5rem);margin:52px 0 14px;letter-spacing:-.015em;line-height:1.25;text-wrap:balance;font-weight:650}
  h2::before{content:"";display:block;width:32px;height:2px;background:var(--accent);margin-bottom:14px;border-radius:2px;opacity:.7}
  h3{font-size:1.1rem;margin:32px 0 10px;letter-spacing:-.01em;line-height:1.3;font-weight:600}
  h4{font-size:.85rem;margin:22px 0 8px;color:var(--ink-soft);text-transform:uppercase;letter-spacing:.06em;font-weight:600}
  p{margin:.7em 0 1em;color:var(--ink-soft);text-wrap:pretty;hyphens:auto;-webkit-hyphens:auto;overflow-wrap:break-word}
  p strong{color:var(--ink);font-weight:600}
  em{font-style:italic;color:var(--ink)}
  .summary{font-size:1.0625rem;line-height:1.6;color:var(--ink);background:var(--bg-soft);border-left:3px solid var(--accent);padding:18px 22px;border-radius:0 var(--radius) var(--radius) 0;margin:0 0 32px}
  blockquote{margin:1.2em 0;padding:.7em 1.1em;border-left:3px solid var(--accent);background:var(--bg-soft);color:var(--ink);border-radius:0 var(--radius) var(--radius) 0;font-size:1.0625rem;line-height:1.55}
  blockquote p{color:var(--ink);margin:.3em 0}
  ul.crisp,ol.crisp{margin:14px 0 18px;padding-left:1.2em}
  ul.crisp li,ol.crisp li{margin:.55em 0;color:var(--ink-soft);padding-left:.2em}
  ul.crisp li::marker{color:var(--accent)}
  ol.crisp li::marker{color:var(--accent);font-weight:600}
  ul.crisp li strong, ol.crisp li strong{color:var(--ink)}
  hr{border:none;border-top:1px solid var(--line);margin:36px 0}

  code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.86em;background:var(--bg-elev);padding:1px 5px;border-radius:4px;border:1px solid var(--line);overflow-wrap:anywhere;word-break:break-word}
  pre{margin:14px 0;background:var(--bg-elev);border:1px solid var(--line);border-radius:var(--radius);padding:14px 16px;overflow-x:auto;font-size:.8125rem;line-height:1.5;-webkit-overflow-scrolling:touch}
  pre code{background:none;border:none;padding:0;font-size:1em}

  .table-wrap{overflow-x:auto;margin:18px -4px;border:1px solid var(--line);border-radius:var(--radius);background:var(--bg-soft);-webkit-overflow-scrolling:touch}
  table{width:100%;border-collapse:collapse;font-size:.875rem;min-width:max-content}
  th,td{padding:10px 14px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}
  th{background:var(--bg-elev);font-weight:600;color:var(--ink);font-size:.78rem;text-transform:uppercase;letter-spacing:.06em;white-space:nowrap}
  tbody tr:last-child td{border-bottom:none}
  tbody tr:hover{background:var(--bg-elev)}

  figure.shot{margin:24px 0;border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;background:var(--bg-soft);box-shadow:var(--shadow)}
  figure.shot img{display:block;width:100%;height:auto;aspect-ratio:1280/800;object-fit:cover}
  figure.shot figcaption{padding:10px 14px;font-size:.825rem;color:var(--ink-mute);border-top:1px solid var(--line);background:var(--bg-elev);line-height:1.45}

  .author-foot{margin-top:48px;padding:24px 16px calc(32px + env(safe-area-inset-bottom,0));border-top:1px solid var(--line);font-size:.825rem;color:var(--ink-mute);max-width:1100px;margin-left:auto;margin-right:auto}
  .author-foot .author-shell{display:flex;flex-direction:column;gap:10px;flex-wrap:wrap}
  .author-foot .author-line{display:flex;flex-wrap:wrap;align-items:center;gap:6px 10px;line-height:1.5}
  .author-foot .author-line strong{color:var(--ink);font-weight:600}
  .author-foot a{color:var(--accent)}
  .author-foot .dot-sep{color:var(--ink-mute);user-select:none}
  @media (min-width:768px){.author-foot .author-shell{flex-direction:row;align-items:center;justify-content:space-between}}
</style>
</head>
<body>

<a class="skip-link" href="#main">Skip to main content</a>

${navHtml(page.slug)}

<main id="main" class="wrap" role="main">
<article>
<h1>${page.h1}</h1>
<p class="summary">${page.summary}</p>

${bodyHtml}

</article>
</main>

<footer class="author-foot" role="contentinfo">
  <div class="author-shell">
    <div class="author-line">
      <span>By <strong>Alexandr Valuev</strong></span>
      <span class="dot-sep" aria-hidden="true">·</span>
      <a href="https://www.linkedin.com/in/valuev/" rel="me noopener" target="_blank">LinkedIn</a>
      <span class="dot-sep" aria-hidden="true">·</span>
      <a href="https://github.com/avaluev/padel-market-analysis" rel="me noopener" target="_blank">Repository</a>
      <span class="dot-sep" aria-hidden="true">·</span>
      <span>Apache 2.0</span>
    </div>
  </div>
</footer>

<script>
// Mobile nav toggle. Trap focus, support Escape to close.
(function(){
  var btn = document.querySelector('.nav-toggle');
  var menu = document.getElementById('primary-nav');
  if (!btn || !menu) return;
  function close(){ btn.setAttribute('aria-expanded','false'); }
  function open(){ btn.setAttribute('aria-expanded','true'); var first = menu.querySelector('a'); if (first) first.focus(); }
  function toggle(){ btn.getAttribute('aria-expanded') === 'true' ? close() : open(); }
  btn.addEventListener('click', toggle);
  document.addEventListener('keydown', function(e){ if (e.key === 'Escape') { close(); btn.focus(); } });
  menu.addEventListener('click', function(e){ if (e.target.tagName === 'A' && window.matchMedia('(max-width: 879px)').matches) close(); });
})();
</script>

</body>
</html>`;
}

// ------------------------------------------------------------------ build

function copyScreenshots() {
  if (!existsSync(SHOTS_SRC)) return;
  for (const f of readdirSync(SHOTS_SRC)) {
    if (/\.(png|jpg|jpeg|webp|svg)$/i.test(f)) {
      const buf = readFileSync(join(SHOTS_SRC, f));
      writeFileSync(join(SHOTS_OUT, f), buf);
    }
  }
}

function buildOnePage(srcFile) {
  const meta = PAGES[srcFile];
  if (!meta) {
    console.log(`[skip] ${srcFile} (not in PAGES registry)`);
    return null;
  }
  const md = readFileSync(join(SRC_DIR, srcFile), 'utf8');
  const cleaned = sanitiseMarkdown(md, meta);
  const body = md2html(cleaned);
  const html = shell(meta, body);
  writeFileSync(join(OUT_DIR, `${meta.slug}.html`), html);
  console.log(`[built] ${meta.slug}.html (${html.length.toLocaleString()} bytes)`);
  return meta;
}

function deleteLegacyOutput() {
  // Remove the old sources/ subdirectory entirely.
  const legacy = join(OUT_DIR, 'sources');
  if (existsSync(legacy)) {
    rmSync(legacy, { recursive: true, force: true });
    console.log(`[clean] removed legacy ${legacy}`);
  }
}

function main() {
  copyScreenshots();
  deleteLegacyOutput();
  const built = [];
  for (const f of Object.keys(PAGES)) {
    const m = buildOnePage(f);
    if (m) built.push(m);
  }
  console.log(`\nTotal pages built: ${built.length}`);
  console.log(`Output: ${OUT_DIR}`);
  return built;
}

main();
