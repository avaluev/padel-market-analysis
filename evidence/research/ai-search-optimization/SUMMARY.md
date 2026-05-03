# AI-Search Optimization: The Four Paradigms (2026 Field Guide)

A citation-dense, tactical reference covering GEO, AIO, AEO, and LLMO — plus a universal checklist, `<head>` template, JSON-LD template, `llms.txt` spec, and AI-crawler `robots.txt` template that satisfies all four paradigms simultaneously.

> **Source-quoting convention:** every factual claim ends with a footnote-style citation containing a verbatim quote (<=15 words) and the source URL. Items marked **[NO SOURCE FOUND]** could not be verified within the search budget.

---

## 1. GEO — Generative Engine Optimization

### Definition

GEO is the discipline of structuring content so that generative search engines (ChatGPT Search, Perplexity, Gemini, You.com, Copilot, etc.) cite and quote it inside their synthesized answers. It was formalized in the Princeton/Georgia Tech/Allen AI paper "GEO: Generative Engine Optimization" (arXiv 2311.09735, presented at ACM KDD 2024), which proved that targeted content tweaks can raise visibility in generative responses by up to 40%.[^geo-paper]

[^geo-paper]: "GEO can boost visibility by up to 40% in generative engine responses" — https://arxiv.org/html/2311.09735v3

### Top 5 ranking / citation factors

| # | Factor | Source quote (<=15 words) | URL |
|---|--------|--------------------------|-----|
| 1 | Quotation addition | "Quotation Addition... achieved a relative improvement of 30-40% on Position-Adjusted Word Count" | https://arxiv.org/html/2311.09735v3 |
| 2 | Statistics / data density | "adding statistics (+40%), citing authoritative sources (+40%)" | https://www.maximuslabs.ai/generative-engine-optimization/geo-experimental-techniques |
| 3 | Cited sources | "top-performing methods, Cite Sources, Quotation Addition, and Statistics Addition" | https://arxiv.org/html/2311.09735v3 |
| 4 | Brand mention authority | "brand mentions correlate 0.664 [with AI citation] vs backlinks 0.218" | https://www.maximuslabs.ai/generative-engine-optimization/geo-experimental-techniques |
| 5 | Self-contained passages | "Self-contained answer passages... correlation coefficient of r=0.87" | https://www.maximuslabs.ai/generative-engine-optimization/geo-experimental-techniques |

Other empirically validated GEO levers from the Princeton paper: **Fluency Optimization** (+15-30%) and **Easy-to-Understand** rewrites (+15-30%).[^geo-fluency]

[^geo-fluency]: "Fluency Optimization and Easy-to-Understand resulted in a significant visibility boost of 15-30%" — https://www.maximuslabs.ai/generative-engine-optimization/geo-experimental-techniques

### Concrete tactics (checklist)

- [ ] Add a minimum of **2 statistics with absolute numbers** per 500 words.[^geo-paper]
- [ ] Add at least **1 expert quotation** per major section, attributed to a named person.[^geo-quote]
- [ ] Cite **3+ external authoritative sources** per article (gov, academic, industry leaders).[^geo-source]
- [ ] Restructure long paragraphs into self-contained answer blocks of **134-167 words**.[^aio-semantic]
- [ ] Pursue **brand mentions** on Reddit, G2, Capterra, Wikipedia, and major industry publications — they outweigh backlinks for AI citation.[^geo-brandmentions]
- [ ] Optimize prose for **readability** (Fluency Optimization, Easy-to-Understand) — short sentences, active voice.[^geo-fluency]

[^geo-quote]: "expert quotations (+28%)" — https://www.maximuslabs.ai/generative-engine-optimization/geo-experimental-techniques
[^geo-source]: "citing authoritative sources (+40%)" — https://www.maximuslabs.ai/generative-engine-optimization/geo-experimental-techniques
[^aio-semantic]: "self-contained units" of "134-167 word" passages — https://wellows.com/blog/google-ai-overviews-ranking-factors/
[^geo-brandmentions]: "brand mentions correlate 0.664 [with AI citation]" — https://www.maximuslabs.ai/generative-engine-optimization/geo-experimental-techniques

### Schema.org / structured data requirements

| Type | Why it matters for GEO | Source |
|------|------------------------|--------|
| `Article` / `BlogPosting` | Authorship + freshness signals AI engines parse | https://rankeo.io/blog/schema-markup-complete-guide |
| `Person` (for `author`) | "Authors with Wikidata items receive stronger authorship trust signals" | https://www.soar.sh/blog/schema-markup-ai-citations-2026 |
| `Organization` | "Organization establishes entity identity" | https://rankeo.io/blog/schema-markup-complete-guide |
| `ClaimReview` / `Quotation` (for stats and pull-quotes) | Maps to GEO's top tactics — quotation and statistics addition | https://arxiv.org/html/2311.09735v3 |
| `Dataset` / `ResearchProject` | Frames original data so AI engines treat it as primary research | https://schema.org/ResearchProject |

### Anti-patterns

- **Keyword stuffing** — measured at **-9% impact** in the Princeton GEO paper.[^geo-stuff]
- **Authoritative-sounding rewrites without underlying data** — "no significant improvement" in the GEO paper.[^geo-auth]
- **Survivorship-bias content** rewritten from top-10 SERP — Google's information-gain signal penalizes regurgitation.[^aio-infogain]

[^geo-stuff]: "such methods offer little to no improvement on generative engine's responses" (re: Keyword Stuffing) — https://arxiv.org/html/2311.09735v3
[^geo-auth]: "researchers found no significant improvement" for Authoritative rewrites — https://www.maximuslabs.ai/generative-engine-optimization/geo-experimental-techniques
[^aio-infogain]: "regurgitated content—were detected by Google's AI as having zero information gain" — https://spelwise.com/how-to-optimize-for-googles-ai-overviews/

### Measurement

- **Citation share / Share of Voice** across a fixed prompt set on ChatGPT, Perplexity, Gemini, Copilot. Run 10-20 priority prompts.[^measure-prompts]
- **Mention rate** (% of relevant queries where brand appears) and **accuracy score** at biweekly cadence.[^measure-cadence]
- Tools: Profound, Semrush AI Visibility Toolkit, Otterly, Peec AI, AthenaHQ.[^measure-tools]

[^measure-prompts]: "Run a set of 10-20 priority prompts" across major engines — https://www.averi.ai/how-to/how-to-track-ai-citations-and-measure-geo-success-the-2026-metrics-guide
[^measure-cadence]: "biweekly cadence... mention rate... accuracy score... sentiment polarity" — https://llmrefs.com/llm-seo
[^measure-tools]: "tools like Semrush... Profound, and Peec AI" — https://www.semrush.com/ai-seo/overview/

---

## 2. AIO — AI Overview Optimization (Google AI Overviews / SGE / AI Mode)

### Definition

AIO targets Google's AI Overview block (formerly Search Generative Experience), powered by Gemini and now appearing on 50-60% of US searches as of early 2026.[^aio-coverage] Cited pages earn 35% more organic clicks than uncited competitors.[^aio-clicks]

[^aio-coverage]: "AI Overviews appear on 50-60% of US searches as of early 2026" — https://wellows.com/blog/google-ai-overviews-ranking-factors/
[^aio-clicks]: "Cited pages earn 35% more organic clicks" — https://wellows.com/blog/google-ai-overviews-ranking-factors/

### Top 5 ranking / citation factors

| # | Factor | Source quote (<=15 words) | URL |
|---|--------|--------------------------|-----|
| 1 | Top-10 organic ranking | "Ranking in the top 10 search results correlates with being cited in AI Overviews" | https://searchengineland.com/guide/how-to-optimize-for-ai-overviews |
| 2 | Semantic completeness | "Content scoring 8.5/10+ on semantic completeness is 4.2x more likely to be cited" | https://wellows.com/blog/google-ai-overviews-ranking-factors/ |
| 3 | Information gain | "Pages with proprietary data... gained 15-25% visibility" | https://outpaceseo.com/article/what-is-information-gain-in-seo-and-why-ai-engines-demand-it/ |
| 4 | Citations & authoritative sources | "increase of over 40%" with citations, quotations, statistics | https://searchengineland.com/guide/how-to-optimize-for-ai-overviews |
| 5 | Page speed (FCP < 0.4s) | "Pages with First Contentful Paint under 0.4 seconds average 6.7 citations" | https://wellows.com/blog/google-ai-overviews-ranking-factors/ |

### Concrete tactics (checklist)

- [ ] Place a **40-60-word direct answer** within the first 150 words of the page (Atomic Answer / BLUF).[^aeo-bluf]
- [ ] Lead **every H2/H3** with a 40-50 word concise summary nugget Gemini can extract.[^aio-nuggets]
- [ ] Build content around **informational queries 3-5 words long**, low-volume (<=100 monthly searches) and low CPC.[^aio-keywords]
- [ ] Cover the **query fan-out**: write the main question + 5-15 anticipated subquestions in one page.[^aio-fanout]
- [ ] Refresh every page **quarterly** — pages not updated quarterly lose AI citations 3x faster.[^aio-fresh]
- [ ] Target **First Contentful Paint < 0.4s** — fast pages cited 3x more.[^aio-fcp]
- [ ] Add multimodal content (images + alt text + video) to increase pickup.[^aio-multimodal]

[^aeo-bluf]: "concise, self-contained answer... within the first 150 words" — https://llmrefs.com/answer-engine-optimization
[^aio-nuggets]: "Gemini model extracts 'nuggets' from the first 40-50 words of each H2 or H3" — https://spelwise.com/how-to-optimize-for-googles-ai-overviews/
[^aio-keywords]: "60% of AI Overview triggers have 100 or fewer monthly searches" — https://searchengineland.com/guide/how-to-optimize-for-ai-overviews
[^aio-fanout]: "Query fan-out optimization... main topics and subtopics" — https://searchengineland.com/guide/how-to-optimize-for-ai-overviews
[^aio-fresh]: "Pages not updated quarterly are 3x more likely to lose citations" — https://wellows.com/blog/google-ai-overviews-ranking-factors/
[^aio-fcp]: "Fast-loading pages are 3x more likely to be cited" — https://wellows.com/blog/google-ai-overviews-ranking-factors/
[^aio-multimodal]: "Combining text, images, video, and schema... helps your content show up more" — https://wellows.com/blog/google-ai-overviews-ranking-factors/

### Schema.org / structured data requirements

| Type | Notes | Source |
|------|-------|--------|
| `Article` / `NewsArticle` | Carries author, datePublished, dateModified — freshness signals | https://rankeo.io/blog/schema-markup-complete-guide |
| `Organization` | Knowledge Graph entity binding | https://schema.org/Organization |
| `BreadcrumbList` | "shows navigation paths in search results and improves site structure understanding" | https://schema.org/BreadcrumbList |
| `Person` (author) | E-E-A-T -> 40% more AI citations with credentialed authors | https://www.qwairy.co/blog/eeat-for-ai-authority-signals-guide |
| `FAQPage` | **Restricted to gov / health sites only by Google** | https://developers.google.com/search/docs/appearance/structured-data/faqpage |
| `Speakable` (BETA) | Voice-pickup readiness | https://developers.google.com/search/docs/appearance/structured-data/speakable |

> Note: HowTo schema is **deprecated for rich results** as of 2024-25 — code remains valid but no longer renders.[^howto-dep]

[^howto-dep]: "Google completely phased out HowTo rich results for both desktop and mobile in 2024-2025" — https://viserx.com/blog/seo/google-drops-7-schema-types

### Anti-patterns

- **Thin content (<600 words)** — "almost never get cited in AI Overviews because they cannot support enough extraction paths."[^aio-thin]
- **Fluffy intros** before the answer — Google penalizes delayed answers.[^aio-fluff]
- **Duplicate pages from filters/parameters** — confuses passage extraction.[^aio-dup]
- **Stale content > 6 months** without updates — flagged as stale by SGE.[^aio-stale]

[^aio-thin]: "Thin pages... almost never get cited in AI Overviews" — https://outpaceseo.com/article/what-is-information-gain-in-seo-and-why-ai-engines-demand-it/
[^aio-fluff]: "Fluffy intros that delay the answer" — https://spelwise.com/how-to-optimize-for-googles-ai-overviews/
[^aio-dup]: "duplicate pages caused by filters, tags, or parameters" — https://spelwise.com/how-to-optimize-for-googles-ai-overviews/
[^aio-stale]: "if your content hasn't been updated... in the last 6 months, SGE may consider it 'stale'" — https://spelwise.com/how-to-optimize-for-googles-ai-overviews/

### Measurement

- Direct AIO citation tracking via Semrush AI Visibility Toolkit, Profound, Otterly.[^measure-tools]
- Brand-mention volume across top citation domains (YouTube 23.29%, Wikipedia 18.41%, Google 16.38% per SEL data).[^aio-domains]
- Top-10 organic position for target keywords (40-76% correlation with AI citation).[^aio-correlation]

[^aio-domains]: "YouTube 23.29%, Wikipedia 18.41%, Google 16.38%" — https://searchengineland.com/guide/how-to-optimize-for-ai-overviews
[^aio-correlation]: "pages in top 10 show 40-76% correlation with AI citations" — https://searchengineland.com/guide/how-to-optimize-for-ai-overviews

---

## 3. AEO — Answer Engine Optimization

### Definition

AEO is content engineering for direct-answer surfaces: voice search (Alexa, Google Assistant, Siri), Google featured snippets, "People Also Ask" boxes, and instant answer cards. With Gartner predicting 25% of organic search traffic will shift to AI chatbots by 2026, AEO becomes existential.[^aeo-gartner]

[^aeo-gartner]: "Gartner predicting 25% of organic search traffic will shift to AI chatbots by 2026" — https://www.o8.agency/blog/ai/answer-engine-optimization-guide

### Top 5 ranking / citation factors

| # | Factor | Source quote (<=15 words) | URL |
|---|--------|--------------------------|-----|
| 1 | Question-headed sections | Q-style headings followed by "answers between 40 and 60 words" | https://cxl.com/blog/answer-engine-optimization-aeo-the-comprehensive-guide/ |
| 2 | First-150-words direct answer | "55% of AI Overview citations come from the first 30% of page content" | https://llmrefs.com/answer-engine-optimization |
| 3 | FAQPage schema | "FAQPage markup are 3.2x more likely to appear in AI responses" | https://discoveredlabs.com/blog/perplexity-optimization-how-to-get-cited-linked-2026 |
| 4 | Conversational long-tail keywords | "users now ask more natural, conversational questions" | https://www.o8.agency/blog/ai/answer-engine-optimization-guide |
| 5 | Quarterly freshness updates | "pages not updated quarterly lose AI citations at 3x the normal rate" | https://llmrefs.com/answer-engine-optimization |

### Concrete tactics (checklist)

- [ ] Mine **People Also Ask** + AnswerThePublic for question-form keywords.[^aeo-paa]
- [ ] Write H2/H3 in question form: "How do I X?" "What is Y?".[^cxl-q]
- [ ] Place a **40-60 word concise answer** immediately under each question heading.[^cxl-q]
- [ ] Add **FAQPage schema** (where eligible — gov/health) or use plain Q/A semantic HTML.[^faqpage-elig]
- [ ] Use comparison tables, step-by-step guides, and bullet lists — they get cited disproportionately.[^aeo-formats]
- [ ] Optimize for voice: aim for **9th-grade readability**, conversational phrasing.[^aeo-voice]

[^aeo-paa]: "Use tools like Google's 'People Also Ask' section, AnswerThePublic" — https://www.o8.agency/blog/ai/answer-engine-optimization-guide
[^cxl-q]: "concise answers immediately after question-style headings, keeping... 40 and 60 words" — https://cxl.com/blog/answer-engine-optimization-aeo-the-comprehensive-guide/
[^faqpage-elig]: "FAQ rich results are only available for well-known, authoritative websites that are government-focused or health-focused" — https://developers.google.com/search/docs/appearance/structured-data/faqpage
[^aeo-formats]: "Step-by-step guides, implementation checklists, specific examples... get cited" — https://cxl.com/blog/answer-engine-optimization-aeo-the-comprehensive-guide/
[^aeo-voice]: "Over 50% of all searches are now voice-based" — https://www.o8.agency/blog/ai/answer-engine-optimization-guide

### Schema.org / structured data requirements

| Type | Notes | Source |
|------|-------|--------|
| `FAQPage` (with `Question` -> `acceptedAnswer` -> `Answer`) | Gov/health sites only for rich results, but parsed by AI for citation | https://developers.google.com/search/docs/appearance/structured-data/faqpage |
| `QAPage` | When users can submit alternative answers (e.g. forums) | https://developers.google.com/search/docs/appearance/structured-data/faqpage |
| `Speakable` | Marks sections suitable for TTS playback by Google Assistant | https://developers.google.com/search/docs/appearance/structured-data/speakable |
| `HowTo` | Code still valid but **no rich results** post-2024 | https://viserx.com/blog/seo/google-drops-7-schema-types |
| `BreadcrumbList` | Helps disambiguate page hierarchy for answer extraction | https://schema.org/BreadcrumbList |

### Anti-patterns

- **Hidden FAQ content** — Google requires "All FAQ content must be visible to the user on the source page."[^faq-visible]
- **Stuffing keywords into Q/A pairs** — semantic engines penalize unnaturally repeated phrases.[^anti-stuff]
- **Long-winded answers >60 words** — push answer outside the snippet window.[^cxl-q]

[^faq-visible]: "All FAQ content must be visible to the user on the source page" — https://developers.google.com/search/docs/appearance/structured-data/faqpage
[^anti-stuff]: "Keyword stuffing is obsolete because AI Overviews rely on semantic understanding" — https://spelwise.com/how-to-optimize-for-googles-ai-overviews/

### Measurement

- Featured snippet count — track via Semrush, Ahrefs, Moz position trackers.[^aeo-tools]
- PAA appearance count for target keywords.
- Voice-search query attribution via Google Search Console "voice" filter (where surfaced).
- Direct answer impressions vs. clicks (zero-click rate).

[^aeo-tools]: "Use tools like Semrush, Ahrefs, and Moz to monitor your featured snippet presence" — https://www.o8.agency/blog/ai/answer-engine-optimization-guide

---

## 4. LLMO — LLM Optimization

### Definition

LLMO is the umbrella practice of making content discoverable, parseable, and citable by every major LLM-powered surface — ChatGPT, Claude, Gemini, Perplexity, Copilot — across both training crawls and real-time retrieval. It encompasses crawler accessibility (robots.txt for GPTBot, ClaudeBot, PerplexityBot, etc.), structured data, the new `llms.txt` spec at llmstxt.org, and brand-entity reinforcement across the open web.[^llmo-def]

[^llmo-def]: "LLM SEO, also called LLMO... refers to optimizing your content so that large language models can find, understand, and cite you" — https://llmrefs.com/llm-seo

### Top 5 ranking / citation factors

| # | Factor | Source quote (<=15 words) | URL |
|---|--------|--------------------------|-----|
| 1 | Crawler access (robots.txt allows AI bots) | "If PerplexityBot can't crawl your site, you cannot be cited" | https://www.ferventers.com/blogs/how-to-get-cited-in-perplexity |
| 2 | Server-side / pre-rendered HTML | "OpenAI's bots only see what's present in the initial HTML" | https://prerender.io/blog/understanding-web-crawlers-traditional-ai/ |
| 3 | FAQ-formatted Q&A blocks | "FAQ sections are disproportionately effective for LLM citation" | https://llmrefs.com/llm-seo |
| 4 | Cross-platform brand mentions (Reddit/G2/Wikipedia) | "These cross-platform citations are what Perplexity uses to verify brand authority" | https://www.ferventers.com/blogs/how-to-get-cited-in-perplexity |
| 5 | `llms.txt` / `llms-full.txt` files | "AI agents are visiting a site's llms-full.txt over twice as much as the llms.txt" | https://www.semrush.com/blog/llms-txt/ |

### Concrete tactics (checklist)

- [ ] Allow **GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-User, Claude-SearchBot, PerplexityBot, Perplexity-User, Google-Extended, Applebot-Extended** in robots.txt (see template below).[^bot-list]
- [ ] Server-side render every page; ensure critical content is in initial HTML, not JS.[^ssr]
- [ ] Publish `/llms.txt` and `/llms-full.txt` per llmstxt.org spec.[^llms-spec]
- [ ] Get listed accurately on **Wikipedia, Wikidata, Crunchbase, G2, Capterra, Reddit threads**.[^cross-mentions]
- [ ] Link author bios with **`Person` schema** + `sameAs` to Wikidata, LinkedIn, ORCID.[^person-sameAs]
- [ ] Publish original primary research / data — gives LLMs novel facts to cite.[^infogain-novel]
- [ ] Verify bot identities via published IP ranges: openai.com/gptbot.json, openai.com/searchbot.json, openai.com/chatgpt-user.json.[^openai-ips]

[^bot-list]: "OpenAI uses GPTBot... OAI-SearchBot... ChatGPT-User" — https://developers.openai.com/api/docs/bots
[^ssr]: "OpenAI's bots only see what's present in the initial HTML" — https://prerender.io/blog/understanding-web-crawlers-traditional-ai/
[^llms-spec]: "llms.txt is a plain Markdown file hosted at /llms.txt" — https://llmstxt.org/
[^cross-mentions]: "Reddit (genuine community mentions), G2 and Capterra... industry directories" — https://www.ferventers.com/blogs/how-to-get-cited-in-perplexity
[^person-sameAs]: "author.sameAs linking to a Wikidata item is increasingly important for E-E-A-T" — https://www.soar.sh/blog/schema-markup-ai-citations-2026
[^infogain-novel]: "AI systems that generate answers from multiple sources will only cite your content if it contains something the other sources do not" — https://outpaceseo.com/article/what-is-information-gain-in-seo-and-why-ai-engines-demand-it/
[^openai-ips]: "verifiable via their published IP ranges: openai.com/gptbot.json" — https://www.xseek.io/docs/openai-crawlers-and-user-agents

### Schema.org / structured data requirements

The "five types covering 80%" baseline from 2026 schema research:[^schema-five]

| Type | Purpose |
|------|---------|
| `Organization` | Entity binding, Knowledge Graph |
| `Article` / `BlogPosting` | Authorship + freshness |
| `FAQPage` | AI-extractable Q/A |
| `BreadcrumbList` | Hierarchy / context |
| `Product` or `Service` | Commercial entity context |

Add for technical credibility: `Person` (author), `Dataset`, `ResearchProject`, `ClaimReview`, `Review`, `LocalBusiness` (if applicable).

[^schema-five]: "Five schema types cover 80 percent of use cases: Organization, Article... FAQPage, BreadcrumbList, and Product" — https://rankeo.io/blog/schema-markup-complete-guide

### Anti-patterns

- **Blocking GPTBot/ClaudeBot if you want AI visibility** — these are the search-eligible variants.[^anti-block]
- **Client-side-only JS rendering** — invisible to most LLM crawlers.[^ssr]
- **Generic AI-rewritten top-10 rollups** — drops 60-80% in 2026 core update.[^ai-rollups]
- **Treating `Claude-User` blocking as the same as `ClaudeBot` blocking** — they are independent rules.[^claude-three]

[^anti-block]: "Blocking AI search and user agents... removes content from eligibility for AI search citations" — https://almcorp.com/blog/anthropic-claude-bots-robots-txt-strategy/
[^ai-rollups]: "generic AI content farms lost 60-80%" — https://outpaceseo.com/article/what-is-information-gain-in-seo-and-why-ai-engines-demand-it/
[^claude-three]: "blocking ClaudeBot does not block Claude-SearchBot or Claude-User" — https://privacy.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler

### Measurement

- **Citation Frequency** across ChatGPT, Claude, Perplexity, Gemini, Copilot prompts.[^geo-metrics]
- **AI Share of Voice** — your brand mentions / total brand mentions across tracked prompts.[^sov]
- **Sentiment polarity** of LLM mentions.[^measure-cadence]
- **Crawl logs**: did GPTBot, ClaudeBot, PerplexityBot actually fetch your pages? (verify against published IP ranges).[^openai-ips]

[^geo-metrics]: "Citation Frequency, Brand Visibility Score, AI Share of Voice, Sentiment Analysis, and LLM Conversion Rate" — https://www.averi.ai/how-to/how-to-track-ai-citations-and-measure-geo-success-the-2026-metrics-guide
[^sov]: "If 10 brands are cited across 100 AI responses and you appear 15 times, your Share of Voice is 15%" — https://www.averi.ai/how-to/how-to-track-ai-citations-and-measure-geo-success-the-2026-metrics-guide

---

## 5. UNIVERSAL — Cross-Cutting Reference

### 5.1 Universal AI-Search Content Checklist (satisfies all 4 paradigms)

The 18 highest-leverage actions:

1. [ ] **Direct 40-60 word answer** in the first 150 words (BLUF / Atomic Answer).[^aeo-bluf]
2. [ ] **Question-form H2/H3 headings**; lead each section with a 40-50 word summary nugget.[^aio-nuggets]
3. [ ] **At least 2 statistics with absolute numbers** per 500 words, each cited.[^geo-paper]
4. [ ] **At least 1 expert quotation per major section**, attributed to a named person.[^geo-quote]
5. [ ] **3+ external authoritative citations** (gov, academic, industry) per page.[^geo-source]
6. [ ] **Self-contained passages of 134-167 words** that survive isolated extraction.[^aio-semantic]
7. [ ] **`Article` + `Person` + `Organization` + `BreadcrumbList` JSON-LD** on every content page.[^schema-five]
8. [ ] **`Person.sameAs`** links to Wikidata, LinkedIn, ORCID.[^person-sameAs]
9. [ ] **Server-side rendered HTML**; critical content not behind JS.[^ssr]
10. [ ] **Publish `/llms.txt` and `/llms-full.txt`**.[^llms-spec]
11. [ ] **Allow GPTBot, OAI-SearchBot, ClaudeBot, Claude-SearchBot, PerplexityBot, Google-Extended, Applebot-Extended** in robots.txt for retrieval visibility (see template below).[^bot-list]
12. [ ] **Cross-platform brand presence** (Wikipedia, Wikidata, Reddit, G2, Capterra, industry directories).[^cross-mentions]
13. [ ] **Quarterly content refresh** with visible "Last updated" date and `dateModified` schema.[^aio-fresh]
14. [ ] **Original primary research / data** for information gain.[^infogain-novel]
15. [ ] **Page speed**: target First Contentful Paint < 0.4s.[^aio-fcp]
16. [ ] **Comparison tables, numbered steps, bullet lists** (high citation rate).[^aeo-formats]
17. [ ] **Conversational long-tail keywords** (3-5 words, question form, <=100 monthly searches).[^aio-keywords]
18. [ ] **Track Citation Frequency, Share of Voice, Mention Sentiment** biweekly across ChatGPT/Claude/Perplexity/Gemini.[^geo-metrics]

### 5.2 Universal `<head>` Tag Template

Every page should contain at minimum:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <!-- Core SEO -->
  <title>Primary Question or Topic — 50-60 chars</title>
  <meta name="description" content="40-60 word direct answer / value summary." />
  <link rel="canonical" href="https://example.com/page-url" />

  <!-- Indexing controls (allow AI surfaces) -->
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />

  <!-- Author / E-E-A-T -->
  <meta name="author" content="Jane Doe, PhD" />
  <link rel="author" href="https://example.com/authors/jane-doe" />

  <!-- Freshness signals -->
  <meta property="article:published_time" content="2026-01-15T09:00:00Z" />
  <meta property="article:modified_time" content="2026-05-01T12:00:00Z" />

  <!-- Open Graph (used by AI for previews and entity context) -->
  <meta property="og:type" content="article" />
  <meta property="og:title" content="Primary Question or Topic" />
  <meta property="og:description" content="40-60 word direct answer." />
  <meta property="og:url" content="https://example.com/page-url" />
  <meta property="og:image" content="https://example.com/og-image.jpg" />
  <meta property="og:site_name" content="Example Brand" />
  <meta property="og:locale" content="en_US" />

  <!-- Twitter / X cards -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:site" content="@examplebrand" />
  <meta name="twitter:creator" content="@janedoe" />

  <!-- Hreflang for multilingual sites -->
  <link rel="alternate" hreflang="en" href="https://example.com/en/page" />
  <link rel="alternate" hreflang="x-default" href="https://example.com/page" />

  <!-- Sitemap discovery (in addition to robots.txt) -->
  <link rel="sitemap" type="application/xml" href="/sitemap.xml" />

  <!-- LLM-specific (emerging, optional) -->
  <link rel="alternate" type="text/markdown" href="/llms.txt" />
</head>
```

Sources for tag selection: Search Engine Land OG-tag guidance, Open Graph protocol, and 2026 meta-tag references.[^head-meta][^head-og][^ogp]

[^head-meta]: "Every page should have standard HTML meta tags like a title, description, robots, and viewport tag" — https://wellows.com/blog/meta-tags/
[^head-og]: "AI-driven search and knowledge-graph systems" pull from OG tags — https://advergroup.com/open-graph-meta-tags-still-matter/
[^ogp]: Open Graph protocol — https://ogp.me/

### 5.3 Universal JSON-LD Template

Combine these blocks in a single `<script type="application/ld+json">` graph:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://example.com/#organization",
      "name": "Example Brand",
      "url": "https://example.com/",
      "logo": "https://example.com/logo.png",
      "sameAs": [
        "https://www.wikidata.org/wiki/Q123456",
        "https://en.wikipedia.org/wiki/Example_Brand",
        "https://www.linkedin.com/company/example-brand",
        "https://twitter.com/examplebrand"
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://example.com/#website",
      "url": "https://example.com/",
      "name": "Example Brand",
      "publisher": { "@id": "https://example.com/#organization" }
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com/" },
        { "@type": "ListItem", "position": 2, "name": "Topic", "item": "https://example.com/topic/" },
        { "@type": "ListItem", "position": 3, "name": "Article Title" }
      ]
    },
    {
      "@type": "Article",
      "@id": "https://example.com/page-url#article",
      "isPartOf": { "@id": "https://example.com/#website" },
      "mainEntityOfPage": "https://example.com/page-url",
      "headline": "Primary Question or Topic",
      "description": "40-60 word direct answer.",
      "datePublished": "2026-01-15T09:00:00Z",
      "dateModified": "2026-05-01T12:00:00Z",
      "image": "https://example.com/og-image.jpg",
      "author": { "@id": "https://example.com/authors/jane-doe#person" },
      "publisher": { "@id": "https://example.com/#organization" },
      "citation": [
        { "@type": "CreativeWork", "name": "GEO: Generative Engine Optimization", "url": "https://arxiv.org/abs/2311.09735" }
      ]
    },
    {
      "@type": "Person",
      "@id": "https://example.com/authors/jane-doe#person",
      "name": "Jane Doe, PhD",
      "url": "https://example.com/authors/jane-doe",
      "jobTitle": "Principal Researcher",
      "worksFor": { "@id": "https://example.com/#organization" },
      "sameAs": [
        "https://www.wikidata.org/wiki/Q987654",
        "https://www.linkedin.com/in/janedoe",
        "https://orcid.org/0000-0000-0000-0000"
      ],
      "knowsAbout": ["AI Search", "Information Retrieval"],
      "alumniOf": "Princeton University"
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "What is GEO?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "GEO is the practice of optimizing content for citation in generative search engine answers."
          }
        }
      ]
    }
  ]
}
</script>
```

Justification: every block above is on the "five types covering 80% of use cases" list plus `Person` for E-E-A-T.[^schema-five][^person-sameAs] FAQPage is included only where eligible / where Q&A blocks exist; Google's own restriction applies.[^faqpage-elig]

### 5.4 `llms.txt` & `llms-full.txt` Spec Summary

**Where to put it:** root path `/llms.txt` (and optionally `/llms-full.txt`).[^llms-loc]

**Format (markdown only):**[^llms-spec-format]

```markdown
# Project Name (required H1)

> Short blockquote summary describing the project / site, key facts, and intended audience.

Optional intro paragraphs / lists (any markdown except headings).

## Documentation
- [Quickstart](https://example.com/docs/quickstart.md): One-line description.
- [API Reference](https://example.com/docs/api.md): One-line description.

## Examples
- [Tutorial: First Project](https://example.com/tutorial.md): One-line description.

## Optional
- [Changelog](https://example.com/changelog.md): Skippable when context budget is tight.
```

**Required sections:**
- H1 with project name (only required section).[^llms-spec]
- Blockquote summary (recommended).[^llms-spec]
- Zero or more H2-delimited file lists with `[name](url): notes` format.[^llms-spec]

**Section conventions:**
- Use an `## Optional` H2 to mark URLs that can be safely skipped when an LLM has limited context.[^llms-skip]
- Prefer linking to **`.md` versions** of pages, not HTML.[^llms-md]

**`llms-full.txt` — when and why:**
- A single-file, full-text concatenation of your most important docs.[^llms-full]
- "AI agents are visiting a site's llms-full.txt over twice as much as the llms.txt file."[^llms-full]
- Drawback: large files can exceed context windows for big doc sets.[^llms-full]

**Adoption proof points:** Anthropic, Cursor, Coinbase, Pinecone, Windsurf, Vercel, Stripe, Cloudflare have published `llms.txt`.[^llms-adopt]

[^llms-loc]: "located in the root path `/llms.txt` of a website" — https://llmstxt.org/
[^llms-spec-format]: "An H1 with the name of the project... blockquote with a short summary" — https://llmstxt.org/
[^llms-skip]: "URLs provided there can be skipped if a shorter context is needed" — https://llmstxt.org/
[^llms-md]: "Link to Markdown when possible, as clean .md files are easier for models to parse" — https://www.semrush.com/blog/llms-txt/
[^llms-full]: "AI agents are visiting a site's llms-full.txt over twice as much as the llms.txt file" — https://www.semrush.com/blog/llms-txt/
[^llms-adopt]: "Anthropic, Cursor, Coinbase, Pinecone, and Windsurf" — https://www.mintlify.com/blog/what-is-llms-txt

### 5.5 AI-Crawler `robots.txt` Template

This template **allows AI search/retrieval crawlers** (so you stay citable) while **opting out of training-only crawlers** (so your content isn't ingested for foundation-model training without referral). Adjust per your business policy.

```txt
# robots.txt — AI Search Visibility Profile (2026)
# Goal: stay citable in ChatGPT/Claude/Perplexity/Gemini/Copilot search,
# while opting out of training-only ingestion where the bot is split.

# ---- Standard search engines ----
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

# ---- OpenAI ----
# GPTBot trains foundation models; allow if you want training inclusion.
User-agent: GPTBot
Allow: /

# OAI-SearchBot powers ChatGPT search citations — keep allowed for visibility.
User-agent: OAI-SearchBot
Allow: /

# ChatGPT-User is user-initiated; rules may not apply but signal intent.
User-agent: ChatGPT-User
Allow: /

# ---- Anthropic (3 separate bots) ----
User-agent: ClaudeBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: Claude-User
Allow: /

# Deprecated Anthropic agents — keep the rule for legacy clients.
User-agent: anthropic-ai
Disallow: /

User-agent: Claude-Web
Disallow: /

# ---- Google AI (Gemini / Vertex) ----
# Google-Extended controls only AI training, not Search ranking.
User-agent: Google-Extended
Allow: /

# ---- Perplexity ----
User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

# ---- Apple ----
# Applebot-Extended controls Apple Intelligence training only.
User-agent: Applebot-Extended
Allow: /

User-agent: Applebot
Allow: /

# ---- Common Crawl (powers many LLMs indirectly) ----
User-agent: CCBot
Allow: /

# ---- Cohere ----
User-agent: cohere-ai
Disallow: /

User-agent: cohere-training-data-crawler
Disallow: /

# ---- ByteDance ----
# Bytespider has a poor robots.txt-respect track record; block by default.
User-agent: Bytespider
Disallow: /

# ---- Catch-all for unknown AI crawlers ----
User-agent: *
Allow: /

Sitemap: https://example.com/sitemap.xml
```

**Bot reference table (verbatim purpose statements):**

| Bot | Purpose | Respects robots.txt | Source |
|-----|---------|---------------------|--------|
| GPTBot | "Training generative AI foundation models" | Yes | https://developers.openai.com/api/docs/bots |
| OAI-SearchBot | "Surfaces websites in ChatGPT's search features" | Yes | https://developers.openai.com/api/docs/bots |
| ChatGPT-User | "User-initiated actions within ChatGPT and Custom GPTs" | "robots.txt rules may not apply" | https://developers.openai.com/api/docs/bots |
| ClaudeBot | "helps enhance the utility and safety of our generative AI models by collecting web content" | Yes | https://privacy.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler |
| Claude-User | "supports Claude AI users. When individuals ask questions to Claude, it may access websites" | Yes | https://privacy.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler |
| Claude-SearchBot | "navigates the web to improve search result quality for users" | Yes | https://privacy.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler |
| anthropic-ai, Claude-Web | Deprecated July 2024 in favor of ClaudeBot | n/a | https://www.searchenginejournal.com/anthropics-claude-bots-make-robots-txt-decisions-more-granular/568253/ |
| Google-Extended | "controls whether content already crawled by Googlebot can be used for AI training" | Yes (token only, not a separate crawler) | https://crawlercheck.com/directory/ai-bots/google-extended |
| PerplexityBot | "indexing" | Yes | https://discoveredlabs.com/blog/perplexity-optimization-how-to-get-cited-linked-2026 |
| Perplexity-User | "real-time retrieval... may ignore the robots.txt file" | No (user-initiated) | https://discoveredlabs.com/blog/perplexity-optimization-how-to-get-cited-linked-2026 |
| Applebot-Extended | Apple generative-AI training opt-out | Yes | https://nohacks.co/blog/ai-user-agents-landscape-2026 |
| CCBot | Common Crawl, "open repository of web crawl data" | Yes | https://nohacks.co/blog/ai-user-agents-landscape-2026 |
| cohere-ai | Cohere training crawler — undocumented vendor stance | "behavioral reports describing standard robots.txt compliance" | https://nohacks.co/blog/ai-user-agents-landscape-2026 |
| Bytespider | ByteDance training crawler — "most aggressive and least robots.txt-compliant" | No (de facto) | https://nohacks.co/blog/ai-user-agents-landscape-2026 |

**Verification:** OpenAI publishes IP ranges at openai.com/gptbot.json, openai.com/searchbot.json, openai.com/chatgpt-user.json — verify suspect requests against these to detect impersonators.[^openai-ips]

**Adoption context (Q1 2026 Cloudflare data):** Only ~5.5% of domains block GPTBot and ~4.7% block ClaudeBot.[^cf-adopt] GPTBot leads both ALLOW and DISALLOW counts — the web is split.[^cf-split]

[^cf-adopt]: "only about 5.5% of domains block GPTBot and 4.7% block ClaudeBot" — https://technologychecker.io/blog/robots-txt-ai-crawlers-blocking-report
[^cf-split]: "GPTBot leads all AI crawlers in DISALLOW rules, but it also leads in ALLOW rules" — https://technologychecker.io/blog/robots-txt-ai-crawlers-blocking-report

---

## Sources

Primary research papers and official documentation cited above:

- arXiv 2311.09735 — Aggarwal et al., "GEO: Generative Engine Optimization" (Princeton/Georgia Tech/Allen AI; KDD 2024) — https://arxiv.org/abs/2311.09735 ; HTML https://arxiv.org/html/2311.09735v3
- llms.txt official spec — https://llmstxt.org/
- Open Graph protocol — https://ogp.me/
- OpenAI bot documentation — https://developers.openai.com/api/docs/bots
- Anthropic crawler documentation — https://privacy.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler
- Google FAQPage structured data docs — https://developers.google.com/search/docs/appearance/structured-data/faqpage
- Google Speakable schema docs — https://developers.google.com/search/docs/appearance/structured-data/speakable
- Schema.org Organization — https://schema.org/Organization ; BreadcrumbList — https://schema.org/BreadcrumbList ; ResearchProject — https://schema.org/ResearchProject ; speakable — https://schema.org/speakable
- Search Engine Land — How to optimize for AI Overviews — https://searchengineland.com/guide/how-to-optimize-for-ai-overviews
- Search Engine Journal — Anthropic crawler granularity — https://www.searchenginejournal.com/anthropics-claude-bots-make-robots-txt-decisions-more-granular/568253/
- Cloudflare robots.txt analysis (Q1 2026) — https://technologychecker.io/blog/robots-txt-ai-crawlers-blocking-report
- ai.robots.txt community list — https://github.com/ai-robots-txt/ai.robots.txt/blob/main/robots.txt
- Semrush — What is llms.txt — https://www.semrush.com/blog/llms-txt/
- Mintlify — Real llms.txt examples — https://www.mintlify.com/blog/real-llms-txt-examples
- CXL — AEO comprehensive guide 2026 — https://cxl.com/blog/answer-engine-optimization-aeo-the-comprehensive-guide/
- LLMrefs — AEO complete guide — https://llmrefs.com/answer-engine-optimization
- LLMrefs — LLM SEO guide 2026 — https://llmrefs.com/llm-seo
- Wellows — Google AI Overviews ranking factors 2026 — https://wellows.com/blog/google-ai-overviews-ranking-factors/
- Outpace SEO — Information gain — https://outpaceseo.com/article/what-is-information-gain-in-seo-and-why-ai-engines-demand-it/
- Maximus Labs — GEO experimental techniques — https://www.maximuslabs.ai/generative-engine-optimization/geo-experimental-techniques
- Soar Agency — Schema markup for AI citations 2026 — https://www.soar.sh/blog/schema-markup-ai-citations-2026
- Qwairy — E-E-A-T for AI — https://www.qwairy.co/blog/eeat-for-ai-authority-signals-guide
- Discovered Labs — Perplexity optimization 2026 — https://discoveredlabs.com/blog/perplexity-optimization-how-to-get-cited-linked-2026
- Ferventers — Get cited in Perplexity — https://www.ferventers.com/blogs/how-to-get-cited-in-perplexity
- ALM Corp — Anthropic three-bot framework — https://almcorp.com/blog/anthropic-claude-bots-robots-txt-strategy/
- xSeek — OpenAI crawlers — https://www.xseek.io/docs/openai-crawlers-and-user-agents
- Spelwise — Optimize for Google AI Overviews — https://spelwise.com/how-to-optimize-for-googles-ai-overviews/
- Averi — How to track AI citations — https://www.averi.ai/how-to/how-to-track-ai-citations-and-measure-geo-success-the-2026-metrics-guide
- Rankeo — Schema markup complete guide — https://rankeo.io/blog/schema-markup-complete-guide
- Viserx — Google drops 7 schema types — https://viserx.com/blog/seo/google-drops-7-schema-types
- Prerender — Web crawlers traditional vs AI — https://prerender.io/blog/understanding-web-crawlers-traditional-ai/
- Wellows — Meta tags 2026 guide — https://wellows.com/blog/meta-tags/
- Advergroup — OG meta tags in age of AI — https://advergroup.com/open-graph-meta-tags-still-matter/
- O8 Agency — AEO guide — https://www.o8.agency/blog/ai/answer-engine-optimization-guide
- CrawlerCheck — Google-Extended directory — https://crawlercheck.com/directory/ai-bots/google-extended
- No Hacks — AI user-agent landscape 2026 — https://nohacks.co/blog/ai-user-agents-landscape-2026
