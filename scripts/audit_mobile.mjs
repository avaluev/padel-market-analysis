#!/usr/bin/env node
// Mobile-first audit harness using Playwright.
// Captures: full-page screenshots per device, viewport screenshots, console errors,
// network failures, performance timing (TTFB, FCP, LCP via PerformanceObserver),
// CLS, layout overflow detection, font load timing, and basic accessibility heuristics.
// Output: <out>/<page>/<device>/{shot.png,viewport.png,metrics.json}
//
// Usage: node scripts/audit_mobile.mjs <label> [pages...]
//   label = baseline | post
//   pages default to reports/final/padel-ai-coach-research.html and evidence-map.html

import { chromium, devices } from "playwright";
import { fileURLToPath } from "node:url";
import path from "node:path";
import fs from "node:fs/promises";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");

const LABEL = process.argv[2] || "baseline";
const PAGES_INPUT = process.argv.slice(3);
const DEFAULT_PAGES = [
  "reports/final/padel-ai-coach-research.html",
  "reports/final/evidence-map.html",
];
const PAGES = PAGES_INPUT.length ? PAGES_INPUT : DEFAULT_PAGES;

const DEVICE_PROFILES = [
  { key: "iphone-13", spec: devices["iPhone 13"] },
  { key: "pixel-7", spec: devices["Pixel 7"] },
  { key: "iphone-se", spec: devices["iPhone SE"] },
  { key: "ipad-mini", spec: devices["iPad Mini"] },
  {
    key: "desktop-1280",
    spec: {
      viewport: { width: 1280, height: 900 },
      userAgent:
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
      deviceScaleFactor: 1,
      isMobile: false,
      hasTouch: false,
    },
  },
];

const OUT_BASE = path.join(ROOT, "evidence", "_mobile_audit", LABEL);

async function ensureDir(p) {
  await fs.mkdir(p, { recursive: true });
}

async function captureMetrics(page) {
  return await page.evaluate(() => {
    const nav = performance.getEntriesByType("navigation")[0];
    const paint = Object.fromEntries(
      performance.getEntriesByType("paint").map((p) => [p.name, p.startTime]),
    );
    const lcpEntries = performance.getEntriesByType("largest-contentful-paint");
    const lcp = lcpEntries.length
      ? lcpEntries[lcpEntries.length - 1].startTime
      : null;
    const layoutShifts = performance.getEntriesByType("layout-shift") || [];
    const cls = layoutShifts.reduce(
      (acc, s) => acc + (s.hadRecentInput ? 0 : s.value),
      0,
    );
    const totalBytes = (() => {
      let bytes = 0;
      performance.getEntriesByType("resource").forEach((r) => {
        bytes += r.transferSize || r.encodedBodySize || 0;
      });
      return bytes;
    })();
    const docHeight = Math.max(
      document.documentElement.scrollHeight,
      document.body.scrollHeight,
    );
    const viewportWidth = window.innerWidth;
    const horizontalOverflow = document.documentElement.scrollWidth > viewportWidth + 1;
    const fontsLoaded =
      document.fonts && document.fonts.status === "loaded" ? true : false;
    const heading = document.querySelector("h1")?.textContent || null;
    const linkCount = document.querySelectorAll("a[href]").length;
    const imageCount = document.querySelectorAll("img").length;
    const tableCount = document.querySelectorAll("table").length;
    // Tap-target audit. Per Apple HIG, the 44x44 minimum applies to *standalone*
    // controls — not inline links inside flowing prose, which the WCAG SC 2.5.5
    // exception explicitly allows. We split the count accordingly.
    function isInlineProseLink(el) {
      if (el.tagName !== "A") return false;
      const p = el.parentElement;
      if (!p) return false;
      const tag = p.tagName;
      if (!["P", "LI", "SPAN", "TD", "TH", "EM", "STRONG", "BLOCKQUOTE", "SMALL"].includes(tag)) return false;
      // Heuristic: parent has more text than just this link.
      const text = (p.textContent || "").trim();
      const linkText = (el.textContent || "").trim();
      return text.length > linkText.length + 5;
    }
    const allTaps = Array.from(
      document.querySelectorAll("a, button, [role='button']"),
    );
    const visibleTaps = allTaps.filter((el) => {
      const r = el.getBoundingClientRect();
      return r.width > 0 && r.height > 0;
    });
    const standaloneTaps = visibleTaps.filter((el) => !isInlineProseLink(el));
    const tooSmallStandaloneTaps = standaloneTaps.filter((el) => {
      const r = el.getBoundingClientRect();
      return r.width < 44 || r.height < 44;
    }).length;
    const tooSmallTaps = visibleTaps.filter((el) => {
      const r = el.getBoundingClientRect();
      return r.width < 32 || r.height < 24;
    }).length;
    return {
      ttfb: nav ? nav.responseStart : null,
      domContentLoaded: nav ? nav.domContentLoadedEventEnd : null,
      loadEvent: nav ? nav.loadEventEnd : null,
      fcp: paint["first-contentful-paint"] || null,
      lcp,
      cls,
      transferBytes: totalBytes,
      docHeight,
      viewportWidth,
      horizontalOverflow,
      fontsLoaded,
      heading,
      linkCount,
      imageCount,
      tableCount,
      tooSmallTaps,
      tooSmallStandaloneTaps,
      standaloneTapCount: standaloneTaps.length,
    };
  });
}

async function runOnce(page, deviceKey, pageRel, outDir) {
  await ensureDir(outDir);

  const consoleErrors = [];
  const requestFailures = [];
  page.on("console", (msg) => {
    if (msg.type() === "error" || msg.type() === "warning") {
      consoleErrors.push({ type: msg.type(), text: msg.text() });
    }
  });
  page.on("pageerror", (err) =>
    consoleErrors.push({ type: "pageerror", text: String(err) }),
  );
  page.on("requestfailed", (req) =>
    requestFailures.push({ url: req.url(), failure: req.failure() }),
  );

  const fileUrl = "file://" + path.resolve(ROOT, pageRel);
  const t0 = Date.now();
  await page.goto(fileUrl, { waitUntil: "load", timeout: 30000 });
  const navMs = Date.now() - t0;

  // Allow LCP / layout shifts to settle.
  await page.waitForTimeout(500);

  const metrics = await captureMetrics(page);

  await page.screenshot({
    path: path.join(outDir, "viewport.png"),
    fullPage: false,
  });
  await page.screenshot({
    path: path.join(outDir, "shot.png"),
    fullPage: true,
  });

  const result = {
    device: deviceKey,
    page: pageRel,
    label: LABEL,
    navMs,
    metrics,
    consoleErrors,
    requestFailures,
    capturedAt: new Date().toISOString(),
  };

  await fs.writeFile(
    path.join(outDir, "metrics.json"),
    JSON.stringify(result, null, 2),
  );

  return result;
}

async function main() {
  const browser = await chromium.launch();
  const summary = [];

  for (const pageRel of PAGES) {
    const pageKey = path.basename(pageRel, ".html");
    for (const profile of DEVICE_PROFILES) {
      const outDir = path.join(OUT_BASE, pageKey, profile.key);
      const ctx = await browser.newContext({
        ...profile.spec,
        reducedMotion: "reduce",
      });
      const page = await ctx.newPage();
      try {
        const r = await runOnce(page, profile.key, pageRel, outDir);
        summary.push(r);
        const m = r.metrics;
        console.log(
          `[${LABEL}] ${pageKey} / ${profile.key}: TTFB=${m.ttfb?.toFixed(0)}ms, FCP=${m.fcp?.toFixed(0)}ms, LCP=${m.lcp?.toFixed(0) ?? "?"}ms, CLS=${m.cls.toFixed(4)}, hOverflow=${m.horizontalOverflow}, smallStandaloneTaps=${m.tooSmallStandaloneTaps}/${m.standaloneTapCount} (incl. inline ${m.tooSmallTaps})`,
        );
      } catch (err) {
        console.error(
          `[${LABEL}] FAIL ${pageKey}/${profile.key}:`,
          err.message,
        );
        summary.push({
          device: profile.key,
          page: pageRel,
          error: String(err),
        });
      } finally {
        await ctx.close();
      }
    }
  }
  await browser.close();

  await fs.writeFile(
    path.join(OUT_BASE, "summary.json"),
    JSON.stringify(summary, null, 2),
  );
  console.log(`\nSummary written to ${path.join(OUT_BASE, "summary.json")}`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
