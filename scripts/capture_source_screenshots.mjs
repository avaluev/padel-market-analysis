import { chromium } from 'playwright';
import { mkdirSync } from 'fs';
import { join } from 'path';

const OUT = '/Users/sxope/Documents/2026/Research/28.Padel/Claude/padel-research-os/reports/sources/screenshots';
mkdirSync(OUT, { recursive: true });

const targets = [
  { id: 'padelytics',   url: 'https://www.padelytics.ai/' },
  { id: 'wingfield',    url: 'https://www.wingfield.io/' },
  { id: 'playtomic',    url: 'https://playtomic.com/' },
  { id: 'strava',       url: 'https://www.strava.com/premium' },
  { id: 'whoop',        url: 'https://www.whoop.com/membership/' },
  { id: 'swingvision',  url: 'https://swing.tennis/' },
  { id: 'hudl',         url: 'https://www.hudl.com/pricing' },
  { id: 'clutch',       url: 'https://www.clutchapp.io/' },
  { id: 'padelfip',     url: 'https://www.padelfip.com/' },
  { id: 'matchi',       url: 'https://matchi.com/' },
  { id: 'spash',        url: 'https://spash.com/en/match-analyzer-ia-clubs-padel/' },
  { id: 'coachlogic',   url: 'https://coachlogic.com/' },
];

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1280, height: 800 } });

for (const t of targets) {
  try {
    const page = await context.newPage();
    await page.goto(t.url, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(2500);
    await page.screenshot({ path: join(OUT, `${t.id}.png`), fullPage: false });
    console.log(`OK  ${t.id}`);
    await page.close();
  } catch (e) {
    console.log(`ERR ${t.id}: ${e.message}`);
  }
}

await browser.close();
