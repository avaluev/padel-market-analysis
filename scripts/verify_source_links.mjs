#!/usr/bin/env node
// Verify all external links from source markdown pages return HTTP 200 (or 3xx).

import { readFileSync, readdirSync, writeFileSync } from 'fs';
import { join } from 'path';

const ROOT = '/Users/sxope/Documents/2026/Research/28.Padel/Claude/padel-research-os';
const PAGES_DIR = join(ROOT, 'reports/final/sources');
const AUDIT_DIR = join(ROOT, 'reports/sources/_audit');

const linkRe = /href="(https?:\/\/[^"]+)"/g;
const allLinks = new Set();
const linkSources = new Map(); // link -> Set of pages

for (const f of readdirSync(PAGES_DIR).filter(x => x.endsWith('.html'))) {
  const html = readFileSync(join(PAGES_DIR, f), 'utf8');
  let m;
  while ((m = linkRe.exec(html))) {
    allLinks.add(m[1]);
    if (!linkSources.has(m[1])) linkSources.set(m[1], new Set());
    linkSources.get(m[1]).add(f);
  }
}

const links = [...allLinks].sort();
console.log(`Verifying ${links.length} unique external links...`);

const results = [];
const concurrency = 8;
let idx = 0;

async function worker() {
  while (idx < links.length) {
    const i = idx++;
    const url = links[i];
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), 12000);
    try {
      const res = await fetch(url, {
        method: 'HEAD',
        redirect: 'follow',
        signal: ctrl.signal,
        headers: { 'User-Agent': 'Mozilla/5.0 (sources-verifier)' },
      });
      clearTimeout(t);
      // some servers reject HEAD; retry GET on 4xx/5xx
      if (res.status >= 400) {
        const ctrl2 = new AbortController();
        const t2 = setTimeout(() => ctrl2.abort(), 12000);
        try {
          const res2 = await fetch(url, { method: 'GET', redirect: 'follow', signal: ctrl2.signal,
            headers: { 'User-Agent': 'Mozilla/5.0 (sources-verifier)' } });
          clearTimeout(t2);
          results.push({ url, status: res2.status, method: 'GET-fallback', sources: [...linkSources.get(url)] });
        } catch (e2) {
          clearTimeout(t2);
          results.push({ url, status: 0, error: e2.message, method: 'GET-fallback', sources: [...linkSources.get(url)] });
        }
      } else {
        results.push({ url, status: res.status, method: 'HEAD', sources: [...linkSources.get(url)] });
      }
    } catch (e) {
      clearTimeout(t);
      // Try GET on HEAD failure
      try {
        const ctrl3 = new AbortController();
        const t3 = setTimeout(() => ctrl3.abort(), 12000);
        const res3 = await fetch(url, { method: 'GET', redirect: 'follow', signal: ctrl3.signal,
          headers: { 'User-Agent': 'Mozilla/5.0 (sources-verifier)' } });
        clearTimeout(t3);
        results.push({ url, status: res3.status, method: 'GET-after-HEAD-err', sources: [...linkSources.get(url)] });
      } catch (e2) {
        results.push({ url, status: 0, error: e2.message, method: 'all-failed', sources: [...linkSources.get(url)] });
      }
    }
  }
}

await Promise.all(Array.from({ length: concurrency }, () => worker()));

results.sort((a, b) => a.url.localeCompare(b.url));
const ok = results.filter(r => r.status >= 200 && r.status < 400).length;
const fail = results.filter(r => r.status === 0 || r.status >= 400);

writeFileSync(join(AUDIT_DIR, 'link_verify_report.json'), JSON.stringify({
  run_at: new Date().toISOString(),
  total: results.length, ok, failed: fail.length,
  results,
}, null, 2));

console.log(`\n=== LINK VERIFY ===`);
console.log(`Total: ${results.length}  OK: ${ok}  FAIL: ${fail.length}`);
if (fail.length) {
  console.log('\nFailures:');
  for (const f of fail) {
    console.log(`  ${f.status || 'ERR'}  ${f.url}  (in ${f.sources.join(', ')})  ${f.error || ''}`);
  }
}
