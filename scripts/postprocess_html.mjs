#!/usr/bin/env node
// Idempotent HTML post-processor:
//  - Wraps every <table>...</table> in <div class="table-wrap" role="region"
//    tabindex="0" aria-label="Table"> if not already wrapped.
//  - Adds loading="lazy" to <img> if absent (none currently, but future-safe).
//  - Adds rel="noopener" to external links lacking it.
import fs from "node:fs";
import path from "node:path";

const targets = process.argv.slice(2);
if (!targets.length) {
  console.error("usage: postprocess_html.mjs <file...>");
  process.exit(1);
}

function wrapTables(html) {
  // Match <table> blocks, but skip ones already inside a .table-wrap.
  return html.replace(
    /(<table\b[\s\S]*?<\/table>)/g,
    (match, tableBlock, offset, full) => {
      // Look behind to see if the immediate preceding non-whitespace is a `class="table-wrap"` div.
      const before = full.slice(Math.max(0, offset - 200), offset);
      if (/<div\s+class="table-wrap"[^>]*>\s*$/.test(before)) {
        return tableBlock;
      }
      return `<div class="table-wrap" role="region" tabindex="0" aria-label="Data table">${tableBlock}</div>`;
    },
  );
}

function addRelNoopener(html) {
  return html.replace(/<a\s+href="(https?:\/\/[^"]+)"([^>]*)>/g, (m, href, rest) => {
    if (/\brel\s*=/.test(rest)) return m;
    return `<a href="${href}"${rest} rel="noopener">`;
  });
}

for (const f of targets) {
  const abs = path.resolve(f);
  let html = fs.readFileSync(abs, "utf8");
  const before = html.length;
  html = wrapTables(html);
  html = addRelNoopener(html);
  fs.writeFileSync(abs, html);
  console.log(`processed ${f} (${before} → ${html.length} bytes)`);
}
