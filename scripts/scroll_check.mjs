#!/usr/bin/env node
// Capture sticky-nav visibility during scroll on tablet/desktop and FAB
// behaviour on mobile (does the nav stay reachable while reading?).
import { chromium, devices } from "playwright";
import path from "node:path";
import fs from "node:fs/promises";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const OUT = path.join(ROOT, "evidence", "_mobile_audit", "scroll");

const PAGES = [
  "reports/final/padel-ai-coach-research.html",
  "reports/final/evidence-map.html",
];
const PROFILES = [
  { key: "iphone-13", spec: devices["iPhone 13"] },
  { key: "ipad-mini", spec: devices["iPad Mini"] },
  { key: "desktop-1280", spec: { viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1, isMobile: false, hasTouch: false } },
];

await fs.mkdir(OUT, { recursive: true });
const browser = await chromium.launch();
for (const pageRel of PAGES) {
  const pageKey = path.basename(pageRel, ".html");
  for (const p of PROFILES) {
    const ctx = await browser.newContext(p.spec);
    const page = await ctx.newPage();
    await page.goto("file://" + path.resolve(ROOT, pageRel), { waitUntil: "load" });
    const dir = path.join(OUT, pageKey, p.key);
    await fs.mkdir(dir, { recursive: true });
    // Top of page
    await page.screenshot({ path: path.join(dir, "01-top.png"), fullPage: false });
    // Scroll halfway and re-capture
    await page.evaluate(() => window.scrollTo({ top: 1500, behavior: "instant" }));
    await page.waitForTimeout(300);
    await page.screenshot({ path: path.join(dir, "02-scrolled-1500.png"), fullPage: false });
    // Scroll deeper
    await page.evaluate(() => window.scrollTo({ top: 4000, behavior: "instant" }));
    await page.waitForTimeout(300);
    await page.screenshot({ path: path.join(dir, "03-scrolled-4000.png"), fullPage: false });
    // On mobile (<720px viewport), tap the FAB to open the sheet, capture
    const vw = (p.spec.viewport && p.spec.viewport.width) || 0;
    if (p.spec.isMobile && vw && vw < 720) {
      // Scroll to the top so the FAB hit-target is uncontested.
      await page.evaluate(() => window.scrollTo({ top: 0, behavior: "instant" }));
      await page.waitForTimeout(150);
      const fabVisible = await page.$eval(".nav-summary", (el) => {
        const r = el.getBoundingClientRect();
        const cs = getComputedStyle(el);
        return r.width > 0 && r.height > 0 && cs.display !== "none" && cs.visibility !== "hidden";
      }).catch(() => false);
      if (fabVisible) {
        await page.click(".nav-summary", { timeout: 3000 });
        await page.waitForTimeout(300);
        await page.screenshot({ path: path.join(dir, "04-sheet-open.png"), fullPage: false });
      }
    }
    await ctx.close();
    console.log(`captured ${pageKey} / ${p.key}`);
  }
}
await browser.close();
console.log(`screenshots in ${OUT}`);
