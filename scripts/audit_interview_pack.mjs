#!/usr/bin/env node
// Multi-viewport Playwright audit for the Padel AI Coach interview pack.
// Captures: screenshots per device, console errors, layout overflow, image-load errors.

import { chromium, devices } from 'playwright';
import { mkdirSync, writeFileSync, readdirSync } from 'fs';
import { join } from 'path';

const ROOT = '/Users/sxope/Documents/2026/Research/28.Padel/Claude/padel-research-os';
const PAGES_DIR = join(ROOT, 'reports/final/interview-pack');
const AUDIT_DIR = join(ROOT, 'reports/interview_pack/_audit');
mkdirSync(AUDIT_DIR, { recursive: true });

// Use local HTTP server to test as it would run on GitHub Pages
const BASE_URL = process.env.AUDIT_BASE_URL || 'http://127.0.0.1:8765/interview-pack';
const htmlFiles = readdirSync(PAGES_DIR).filter(f => f.endsWith('.html')).sort();
const urls = htmlFiles.map(f => ({
  name: f.replace(/\.html$/, ''),
  url: `${BASE_URL}/${f}`,
}));

const profiles = [
  { id: 'iphone-13',     ...devices['iPhone 13'] },
  { id: 'iphone-se',     ...devices['iPhone SE'] },
  { id: 'pixel-7',       ...devices['Pixel 7'] },
  { id: 'ipad-mini',     ...devices['iPad Mini'] },
  { id: 'desktop-1280',  viewport: { width: 1280, height: 800 }, userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0)' },
];

const report = { run_at: new Date().toISOString(), pages: {} };

const browser = await chromium.launch({ headless: true });

for (const profile of profiles) {
  const ctx = await browser.newContext({
    viewport: profile.viewport,
    userAgent: profile.userAgent,
    deviceScaleFactor: profile.deviceScaleFactor,
    isMobile: profile.isMobile,
    hasTouch: profile.hasTouch,
  });
  for (const { name, url } of urls) {
    const page = await ctx.newPage();
    const consoleErrs = [];
    const failedRequests = [];
    page.on('console', msg => {
      if (msg.type() === 'error') consoleErrs.push(msg.text());
    });
    page.on('requestfailed', req => failedRequests.push(`${req.method()} ${req.url()} :: ${req.failure()?.errorText}`));

    try {
      await page.goto(url, { waitUntil: 'networkidle', timeout: 20000 });
      // Trigger lazy-loaded images by scrolling
      await page.evaluate(async () => {
        await new Promise(resolve => {
          let total = 0;
          const dist = 200;
          const t = setInterval(() => {
            window.scrollBy(0, dist);
            total += dist;
            if (total >= document.body.scrollHeight) { clearInterval(t); resolve(); }
          }, 80);
        });
        await new Promise(r => setTimeout(r, 800));
        window.scrollTo(0, 0);
      });
      await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(()=>{});
    } catch (e) {
      report.pages[name] = report.pages[name] || {};
      report.pages[name][profile.id] = { error: e.message };
      await page.close();
      continue;
    }

    const layout = await page.evaluate(() => {
      const docW = document.documentElement.clientWidth;
      const overflow = [];
      const tooSmallFonts = [];
      const seen = new Set();

      function isInsideScrollable(el) {
        let p = el.parentElement;
        while (p) {
          const cs = window.getComputedStyle(p);
          if (cs.overflowX === 'auto' || cs.overflowX === 'scroll' || cs.overflow === 'auto' || cs.overflow === 'scroll') return true;
          p = p.parentElement;
        }
        return false;
      }

      document.querySelectorAll('*').forEach(el => {
        const r = el.getBoundingClientRect();
        // skip elements that are intentionally horizontally scrollable (tables in .table-wrap, pre code blocks)
        if ((r.right > docW + 1 || r.left < -1) && !isInsideScrollable(el) && !['HTML','BODY'].includes(el.tagName)) {
          const k = el.tagName + ':' + (el.className || '').toString().slice(0,30);
          if (!seen.has(k)) {
            seen.add(k);
            overflow.push({ tag: el.tagName, cls: el.className.toString().slice(0,40), right: Math.round(r.right), docW });
          }
        }
        const cs = window.getComputedStyle(el);
        const fs = parseFloat(cs.fontSize);
        if (fs && fs < 12 && el.textContent && el.textContent.trim().length > 5) {
          const k = 'fs:' + el.tagName + ':' + Math.round(fs);
          if (!seen.has(k)) {
            seen.add(k);
            tooSmallFonts.push({ tag: el.tagName, fontSize: fs, sample: el.textContent.trim().slice(0,40) });
          }
        }
      });
      // Wait briefly to confirm lazy-loaded images settle
      const imgsBroken = Array.from(document.images).filter(i => i.loading !== 'lazy' && (!i.complete || i.naturalWidth === 0)).map(i => i.src);
      const titleEl = document.querySelector('h1');
      const linksTotal = document.querySelectorAll('a[href]').length;
      const linksExternal = Array.from(document.querySelectorAll('a[href]')).filter(a => /^https?:/.test(a.href)).length;
      return {
        viewportW: docW,
        title: titleEl ? titleEl.textContent.trim() : null,
        overflowCount: overflow.length,
        overflowSample: overflow.slice(0, 5),
        tooSmallFontsCount: tooSmallFonts.length,
        tooSmallFontsSample: tooSmallFonts.slice(0, 5),
        imgsBroken,
        linksTotal,
        linksExternal,
      };
    });

    const shotPath = join(AUDIT_DIR, `${profile.id}_${name}.png`);
    await page.screenshot({ path: shotPath, fullPage: false });

    report.pages[name] = report.pages[name] || {};
    report.pages[name][profile.id] = {
      ...layout,
      consoleErrors: consoleErrs,
      failedRequests,
      screenshot: shotPath,
    };
    await page.close();
  }
  await ctx.close();
}

await browser.close();

writeFileSync(join(AUDIT_DIR, 'audit_report.json'), JSON.stringify(report, null, 2));

// Summary
console.log('=== AUDIT SUMMARY ===');
let totalIssues = 0;
for (const [name, profiles] of Object.entries(report.pages)) {
  for (const [pid, data] of Object.entries(profiles)) {
    if (data.error) {
      console.log(`FAIL  ${name} @ ${pid}: ${data.error}`);
      totalIssues++;
      continue;
    }
    const flags = [];
    if (data.overflowCount > 0) flags.push(`overflow=${data.overflowCount}`);
    if (data.tooSmallFontsCount > 0) flags.push(`smallFonts=${data.tooSmallFontsCount}`);
    if (data.imgsBroken.length > 0) flags.push(`brokenImgs=${data.imgsBroken.length}`);
    if (data.consoleErrors.length > 0) flags.push(`consoleErr=${data.consoleErrors.length}`);
    if (data.failedRequests.length > 0) flags.push(`failedReq=${data.failedRequests.length}`);
    if (flags.length) {
      console.log(`WARN  ${pid.padEnd(13)} ${name.padEnd(30)} ${flags.join(' ')}`);
      totalIssues += flags.length;
    } else {
      console.log(`OK    ${pid.padEnd(13)} ${name.padEnd(30)} links=${data.linksExternal}/${data.linksTotal} fontFloor>=12`);
    }
  }
}
console.log(`\nTotal flag count: ${totalIssues}`);
console.log(`Report: ${join(AUDIT_DIR, 'audit_report.json')}`);
