# Natural Data Scraping: Master Source Catalogue & Time Estimates

This document is the definitive engineering plan for scraping real, human-authored industrial automation data from the internet. Every record collected here represents authentic engineering knowledge written by real PLC programmers, not AI-generated content.

---

## Category 1: Technical Forums & Q&A Platforms

| Source | Data Type | Access Method | Records Estimate | Hours to Scrape | Status |
|--------|-----------|---------------|-----------------|-----------------|--------|
| **StackOverflow** (tags: plc, scada, iec-61131) | Q&A Pairs | Official REST API (Free) | ~2,000 | 3 hrs | Done (92 collected) |
| **Engineering StackExchange** | Q&A Pairs | Official REST API (Free) | ~800 | 2 hrs | Running (blocked) |
| **PLCS.net Forums** | Thread discussions, code snippets | BeautifulSoup scraper | ~15,000 | 8-10 hrs | NOT STARTED |
| **Automation.net Forums** | Siemens TIA Portal specific Q&A | BeautifulSoup + Selenium | ~5,000 | 4-5 hrs | NOT STARTED |
| **Reddit r/PLC + r/Scada** | Troubleshooting threads | PRAW OAuth (needs token) | ~3,000 | 2 hrs | Blocked (403) |
| **MrPLC.com Forums** | Rockwell/Allen-Bradley code threads | BeautifulSoup scraper | ~8,000 | 6-7 hrs | NOT STARTED |
| **LinkedIn Technical Articles** | Engineering opinion articles | Selenium headless | ~500 | 3 hrs | NOT STARTED |

---

## Category 2: Open Source Code Repositories

| Source | Data Type | Access Method | Records Estimate | Hours to Scrape | Status |
|--------|-----------|---------------|-----------------|-----------------|--------|
| **GitHub (IEC 61131-3 repos)** | Raw .ST, .SCL files | git clone + regex | ~1,200 | 4 hrs | Done (400 raw, 91 verified) |
| **GitHub Gists (.scl, .st snippets)** | Isolated code snippets | Code Search API + PAT | ~600 | 3 hrs | Blocked (401) |
| **Google BigQuery (github_repos table)** | All GitHub .scl/.st files | SQL query (BigQuery) | ~50,000+ | 0.5 hr | NOT STARTED (BEST SOURCE) |
| **OSCAT Library** | Verified function blocks | TcOpen GitHub clone | ~363 | 0.5 hr | Done (363 verified) |
| **Siemens LGF Library** | Siemens SCL blocks | Git clone | ~8 | 0.25 hr | Done (8 collected) |
| **TcOpen Framework** | Beckhoff OOP ST code | Git clone | ~500 | 1 hr | Partially done |
| **Codesys Online Examples** | Standard function blocks | Web scraper | ~400 | 2 hrs | NOT STARTED |

---

## Category 3: Wikipedia & Knowledge Bases

| Source | Data Type | Access Method | Records Estimate | Hours to Scrape | Status |
|--------|-----------|---------------|-----------------|-----------------|--------|
| **Wikipedia (Automation domain)** | Domain knowledge text | MediaWiki API | ~10 | 0.5 hr | Done (10 records) |
| **Wikipedia (All IEC/ISA standards)** | Standards definitions | MediaWiki API full-text | ~200 | 1 hr | NOT STARTED |
| **IEC 61131-3 Online Docs** | Specification text | PDF scraper (PyMuPDF) | ~500 | 2 hrs | NOT STARTED |
| **ISA (automation standards)** | Technical glossary | BeautifulSoup | ~300 | 1.5 hrs | NOT STARTED |

---

## Category 4: Video Platforms (Transcript Extraction)

| Source | Data Type | Access Method | Records Estimate | Hours to Scrape | Status |
|--------|-----------|---------------|-----------------|-----------------|--------|
| **YouTube (RealPars channel)** | Tutorial transcripts | yt-dlp + residential proxy | ~500 | 4 hrs | Blocked (IP ban) |
| **YouTube (SiemensGlobal channel)** | TIA Portal tutorials | yt-dlp + residential proxy | ~200 | 2 hrs | Blocked (IP ban) |
| **YouTube Search (PLC tutorial)** | Mixed tutorial transcripts | yt-dlp + ytsearch | ~1,000 | 6 hrs | Partially blocked |

---

## Category 5: Academic & Industrial Papers

| Source | Data Type | Access Method | Records Estimate | Hours to Scrape | Status |
|--------|-----------|---------------|-----------------|-----------------|--------|
| **arXiv.org (cs.SY section)** | Systems engineering papers | arXiv REST API (Free) | ~2,000 | 3 hrs | NOT STARTED |
| **Google Scholar** | Paper abstracts | SerpAPI / Scholarly | ~5,000 | 5 hrs | NOT STARTED |
| **IEEE Xplore** | Automation control papers | Selenium + IEEE API | ~3,000 | 6 hrs | NOT STARTED |
| **ResearchGate** | Preprints + papers | BeautifulSoup + delay | ~1,000 | 4 hrs | NOT STARTED |

---

## Category 6: Vendor Documentation & Manuals

| Source | Data Type | Access Method | Records Estimate | Hours to Scrape | Status |
|--------|-----------|---------------|-----------------|-----------------|--------|
| **Siemens Industry Online Support** | TIA Portal code examples | Selenium authenticated | ~1,000 | 8 hrs | NOT STARTED |
| **Rockwell Automation Knowledgebase** | Allen-Bradley examples | Selenium authenticated | ~800 | 6 hrs | NOT STARTED |
| **Beckhoff InfoSys** | TwinCAT documentation | BeautifulSoup | ~1,200 | 4 hrs | NOT STARTED |
| **Omron Industrial Manuals (PDF)** | PLC programming manuals | PyMuPDF + PDF parser | ~600 | 3 hrs | NOT STARTED |
| **Schneider Electric eXchange** | Modicon PLC examples | BeautifulSoup + API | ~400 | 2 hrs | NOT STARTED |

---

## Summary Table: Prioritized by Impact vs Effort

| Priority | Source | Why Critical | Est. Records | Est. Hours |
|----------|--------|-------------|-------------|------------|
| ?? **CRITICAL** | Google BigQuery (GitHub Mirror) | Millions of lines of real code. One SQL query. | 50,000+ | 0.5 hr |
| ?? **CRITICAL** | PLCS.net + MrPLC Forums | Real engineers solving real problems. Best Q&A | 23,000 | 14-17 hrs |
| ?? **HIGH** | arXiv cs.SY Papers | Academic, structured, high-density engineering text | 2,000 | 3 hrs |
| ?? **HIGH** | Reddit PRAW (with OAuth) | Authentic troubleshooting language, very conversational | 3,000 | 2 hrs |
| ?? **MEDIUM** | YouTube Transcripts (with proxy) | Spoken natural language around code, unique training angle | 1,700 | 12 hrs |
| ?? **MEDIUM** | Beckhoff InfoSys + Siemens Docs | Authoritative vendor-verified data | 2,200 | 12 hrs |
| ?? **LOW** | IEEE Xplore / ResearchGate | High quality but very narrow domain coverage | 4,000 | 10 hrs |

**Total Estimated Records Available: ~90,000+**
**Total Estimated Scraping Time: ~65-80 hours (parallelized across threads)**
