# Mobile audit diff — baseline vs. post-redesign

Captured at: 2026-05-02T17:34:47.845Z

| Page / Device | FCP (ms) | LCP (ms) | CLS | h-Overflow | Small standalone taps | Inline-prose small links |
|---|---:|---:|---:|---:|---:|---:|
| evidence-map / desktop-1280 | 28 → 28 | — → — | 0.0000 → 0.0000 | no → no | 34 → 34 (≈) | 67 → 67 (≈) |
| evidence-map / ipad-mini | 28 → 36 | — → — | 0.0000 → 0.0000 | no → no | 34 → 34 (≈) | 59 → 36 (-23) |
| evidence-map / iphone-13 | 28 → 28 | — → — | 0.0000 → 0.0000 | no → no | 25 → 25 (≈) | 56 → 33 (-23) |
| evidence-map / iphone-se | 28 → 24 | — → — | 0.0000 → 0.0000 | no → no | 25 → 25 (≈) | 49 → 26 (-23) |
| evidence-map / pixel-7 | 28 → 36 | — → — | 0.0000 → 0.0000 | no → no | 25 → 25 (≈) | 58 → 35 (-23) |
| padel-ai-coach-research / desktop-1280 | 44 → 44 | — → — | 0.0000 → 0.0000 | no → no | 78 → 78 (≈) | 113 → 113 (≈) |
| padel-ai-coach-research / ipad-mini | 40 → 44 | — → — | 0.0000 → 0.0000 | no → no | 60 → 60 (≈) | 95 → 35 (-60) |
| padel-ai-coach-research / iphone-13 | 68 → 40 | — → — | 0.0000 → 0.0000 | no → no | 50 → 50 (≈) | 88 → 28 (-60) |
| padel-ai-coach-research / iphone-se | 40 → 36 | — → — | 0.0000 → 0.0000 | no → no | 50 → 50 (≈) | 89 → 29 (-60) |
| padel-ai-coach-research / pixel-7 | 40 → 40 | — → — | 0.0000 → 0.0000 | no → no | 50 → 50 (≈) | 90 → 30 (-60) |

## Notes

- **Small standalone taps** are interactive controls (buttons, isolated links) under 44×44 px — the iOS HIG and WCAG 2.5.5 minimum. This count must trend toward 0.
- **Inline-prose small links** are links inside paragraphs/lists that share a line with surrounding text. WCAG 2.5.5 explicitly excludes these from the 44×44 rule; the count is informational.
- **CLS** = cumulative layout shift; <0.1 is good; the report has no images so it stays at 0.
- **LCP** is null/undefined here because the static page has no large image as LCP candidate; FCP is the relevant proxy.
- **h-Overflow** flags whether the document scrollWidth exceeds the viewport — must remain "no" on every device.
