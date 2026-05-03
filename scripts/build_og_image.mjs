#!/usr/bin/env node
// Build the default Open Graph card (1200x630 PNG) used by every page's
// `<meta property="og:image">` tag. The image is rendered from an inline
// SVG via Playwright at exact 1200x630 pixels (the OG spec). Idempotent.

import { chromium } from "playwright";
import { writeFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const ROOT = dirname(dirname(__filename));
const OUT = join(ROOT, "reports/final/og-default.png");

const html = `<!doctype html>
<html><head><meta charset="utf-8"><style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{
    width:1200px;height:630px;
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI Variable","SF Pro Display",system-ui,sans-serif;
    background:linear-gradient(135deg,#0a0a0a 0%,#0e1a2e 60%,#0a6cf3 140%);
    color:#fafafa;display:flex;flex-direction:column;justify-content:space-between;
    padding:64px 72px;
  }
  .top{display:flex;align-items:center;gap:14px}
  .dot{width:18px;height:18px;border-radius:50%;background:#3b9bff;box-shadow:0 0 24px rgba(59,155,255,.5)}
  .brand{font-size:22px;font-weight:600;letter-spacing:-.005em;color:#a1c4f0}
  .title{font-size:84px;line-height:1.05;letter-spacing:-.025em;font-weight:700;max-width:1056px}
  .title em{color:#3b9bff;font-style:normal}
  .summary{font-size:24px;line-height:1.45;color:#d4d4d8;max-width:1056px;margin-top:24px}
  .bottom{display:flex;align-items:center;justify-content:space-between;font-size:18px;color:#a1a1aa}
  .author{display:flex;align-items:center;gap:12px}
  .author strong{color:#fafafa;font-weight:600}
  .url{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:18px;color:#3b9bff}
</style></head><body>
  <div>
    <div class="top">
      <div class="dot"></div>
      <div class="brand">Padel Coaching Tech Research</div>
    </div>
    <div class="title" style="margin-top:32px">An <em>evidence-graded</em> research portfolio<br>on padel coaching technology.</div>
    <div class="summary">Eight pages: competitor landscape, subscription economics, MVP design,
      ninety-day plan, methodology, model provenance. Every claim cites a verifiable source URL.</div>
  </div>
  <div class="bottom">
    <div class="author">By <strong>Alexandr Valuev</strong></div>
    <div class="url">avaluev.github.io/padel-market-analysis</div>
  </div>
</body></html>`;

const browser = await chromium.launch();
const context = await browser.newContext({
  viewport: { width: 1200, height: 630 },
  deviceScaleFactor: 1,
});
const page = await context.newPage();
await page.setContent(html, { waitUntil: "networkidle" });
const buf = await page.screenshot({ type: "png", omitBackground: false });
writeFileSync(OUT, buf);
const sizeKB = Math.round(buf.length / 1024);
console.log(`wrote ${OUT} (${sizeKB} KB at 1200x630)`);
await browser.close();
