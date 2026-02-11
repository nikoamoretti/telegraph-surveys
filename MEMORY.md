sk-ant-oat01-efuZ5Ijtw1bgjh4p8lL6AgygnqYdA6PJny4lbGv1tmJZ7lyRPs61Q7_jBdI3eF0kOYy-eO9HNHWMmSr8pWraaA-dO
tBAgAA # MEMORY.md - Long-Term Memory

*Curated memories, lessons, and context that matters.*

---

## About Nico

- Chill energy
- PST timezone
- Professional email: nico@telegraph.io (Telegraph)
- Personal email: nicoamoretti@gmail.com

## Key Dates

- **2025-01-24** — First boot. Got my name: Nicodus.
- **2026-01-26** — Set up always-on gateway (launchd + pmset). Now reachable via Telegram 24/7.
- **2026-01-29** — Started Commtrex scraping project
- **2026-02-09** — Completed 14,364 facility scrapes (99.99% of target)

## Tools & Setup

### Email
- **himalaya** (IMAP/SMTP) — NOT gog
- Accounts: `gmail` (personal, default), `telegraph` (professional)
- Config: `~/.config/himalaya/config.toml`
- Passwords in macOS Keychain

### Gateway
- Runs as launchd service (auto-start, keep-alive)
- Mac set to never sleep (`pmset sleep 0`)

### Scraping Infrastructure
- **ScrapingBee API** — Primary proxy service for web scraping
- **Scrape.do** — Fallback proxy service
- **ri_scraper.py** — Production scraper with 30s timeout, progress tracking

## Active Projects

### Railhub — Free Rail Freight Directory
**Goal:** Build a free, centralized resource for rail freight information in the US
**Status:** Data collection complete, website skeleton live

**Completed:**
- ✅ Scraped 14,364 transloading facilities (99.99% of target)
- ✅ Only 1 facility missing (Lansdale, PA) — skipped due to timeout issues
- ✅ Website deployed: https://nikoamoretti.github.io/railhub/
- ✅ Scraping infrastructure built (ScrapingBee + fallback)

**Next Steps:**
- Load 14,364 facilities into website data file
- Deploy updated site to GitHub Pages
- Add search/filter functionality

### Data Sources Scraped
| Source | Records | Status |
|--------|---------|--------|
| Commtrex Transloading | ~14,364 | ✅ Complete |
| Railcar Storage | Not started | 📋 Planned |
| Rail Services | Requires login | 🔒 Blocked |

## Lessons Learned

- **Document tool setups immediately** — I forgot about himalaya because it wasn't in TOOLS.md. Now there's an explicit instruction in AGENTS.md to write it down right away.
- **Progressive saves during scraping** — Save after each batch to prevent data loss on crashes
- **Proxy services are essential** — ScrapingBee bypasses Cloudflare blocks that raw HTTP can't
- **30-second timeouts prevent hanging** — Default timeouts too long, custom timeout essential

## ### Moltbook
- Registered as: `Nicodus`
- ID: `0b4049f3-fc29-4551-b8fe-6b9a57f2b6d4`
- Key: `moltbook_sk_I7AbMBCeH3a41VbByBQfbtbG5X9X1F88`
- Status: `claimed` ✅

## Self-Improvement System

- Installed **self-improving-agent** skill from ClawdHub
- `.learnings/` directory for tracking mistakes and learnings
- When I mess up or get corrected → log to `.learnings/LEARNINGS.md`
- When commands fail → log to `.learnings/ERRORS.md`
- Promote valuable learnings to AGENTS.md, SOUL.md, TOOLS.md

## Automatic Memory System

**Nightly Review (10:30 PM)**
- Cron job scans all sessions from last 24h
- Extracts learnings, patterns, preferences
- Updates MEMORY.md and AGENTS.md
- Commits changes to git

**Hourly Snapshots**
- Appends key activities to daily memory file
- Tracks progress on active projects
- Captures decisions and context

---

## Recent Activity (2026-02-10)

### Telegraph CS Surveys — Completed
Created comprehensive customer satisfaction survey framework with NPS-based branching:

**Post-Implementation Survey** (7–10 days)
- URL: https://form.typeform.com/to/Nk0662l2
- 7 questions focused on early value detection
- Automated alerts for low onboarding/training scores (≤5)
- Time-to-value tracking as churn predictor

**3-Month Check-In** (90 days, $20 incentive)
- URL: https://form.typeform.com/to/N528RM9k
- NPS-based branching: Promoters (9–10), Passives (7–8), Detractors (0–6)
- Promoter path: Sean Ellis PMF test, testimonials, case studies, referrals
- Passive path: Improvement feedback, feature requests
- Detractor path: Root cause analysis, recovery call offer

**Operational Workflows**
- Promoters: Personal outreach within 3 days for testimonials/referrals
- Passives: Weekly review of improvement suggestions for roadmap
- Detractors: 48h recovery call if opted in, monitoring if not
- Incentives: $20 gift card (all), $100 case study, $250 referral credit

Linear task **COM-327** created to track this work (due Feb 13).

### HubSpot Integration — Working
- PAT stored in keychain, call data accessible
- Analyzed Adam Jackson's 47 calls today
- Identified follow-ups: Troy Zeiter (GM), David Duty (CEVA), Karsten Schumaker & Chris Elwick (ADM)
- Cole Bright nurture campaign needed

### Learnings
- **Typeform API limitation**: Conditional logic on yes/no fields requires specific value handling ("1" not "yes")
- **User frustration pattern**: When explaining limitations repeatedly, switch to workaround mode (web_fetch, config patches) sooner

---

*Updated 2026-02-10*
