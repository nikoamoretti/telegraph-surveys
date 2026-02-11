# TOOLS.md - Local Notes

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

---

## Email (himalaya)

Gmail is connected via **himalaya** (IMAP/SMTP), not `gog`.

| Account | Email | Default | Notes |
|---------|-------|---------|-------|
| gmail | nicoamoretti@gmail.com | yes | Personal |
| telegraph | nico@telegraph.io | no | Professional |

- Config: `~/.config/himalaya/config.toml`
- Passwords stored in macOS Keychain:
  - `himalaya-gmail` → nicoamoretti@gmail.com
  - `himalaya-telegraph` → nico@telegraph.io
- To switch accounts: `HIMALAYA_ACCOUNT=telegraph himalaya ...`
- To add accounts: edit config.toml + store app password in keychain

---

## Google / Gemini API Keys

| Key | Project | Used For |
|-----|---------|----------|
| AIzaSyAftL4I0WCAESY-HeXTE_qELyVOCmxvyqQ | Places API | goplaces, local-places skills |
| AIzaSyCkXwPOoQvZgJRNhH0dwz8JY0nNcDUqxI4 | Gemini | Memory search embeddings |

---

## Image Generation (nano-banana-pro)

- **Skill:** nano-banana-pro (Gemini 3 Pro Image)
- **API Key:** AIzaSyCkXwPOoQvZgJRNhH0dwz8JY0nNcDUqxI4 (same as memory search)
- **Usage:**
  ```bash
  export GEMINI_API_KEY="AIzaSyCkXwPOoQvZgJRNhH0dwz8JY0nNcDUqxI4"
  uv run ~/.npm-global/lib/node_modules/clawdbot/skills/nano-banana-pro/scripts/generate_image.py \
    --prompt "description" --filename output.png --resolution 1K
  ```
- **Resolutions:** 1K (default), 2K, 4K
- **Can also edit images** with `--input-image`

---

## Google Workspace (gog)

| Account | Services | Notes |
|---------|----------|-------|
| nico@telegraph.io | calendar, contacts, docs, drive, gmail, sheets | Professional |

- CLI: `gog` (installed via Homebrew)
- Credentials: `~/Library/Application Support/gogcli/`
- Use `GOG_ACCOUNT=nico@telegraph.io` or `--account` flag
- **Note**: For personal Gmail (nicoamoretti@gmail.com), use **himalaya** instead

---

## Scraping Infrastructure

### ScrapingBee (Primary)
- **Purpose:** Proxy service for web scraping (bypasses Cloudflare)
- **API Key:** Stored in environment or passed via `--api-key`
- **Usage:**
  ```bash
  export SCRAPINGBEE_API_KEY="your_key"
  python ri_scraper.py --state RI
  ```

### Scrape.do (Fallback)
- **Purpose:** Backup proxy service
- **Usage:** Built into ri_scraper.py as fallback

### ri_scraper.py
- **Location:** `~/clawd/ri_scraper.py`
- **Features:**
  - 30-second timeout (prevents hanging)
  - Progress tracking and logging
  - Configurable skip indices
  - Simulation mode for testing
- **Output:** CSV files with facility data

---

## Cameras
*(none configured yet)*

## SSH
*(none configured yet)*

## TTS
*(none configured yet)*

---

## Apollo.io (Company Enrichment)

- **API Key:** Stored in macOS Keychain as `apollo-api-key`
- **Skill:** `skills/apollo/`
- **Usage:**
  ```bash
  # Single company lookup (domain preferred)
  ./skills/apollo/scripts/enrich-company.sh --domain amazon.com
  ./skills/apollo/scripts/enrich-company.sh "Amazon"
  
  # Batch enrichment
  ./skills/apollo/scripts/batch-enrich.sh companies.txt output.json
  ```
- **Pro tip:** Domain lookups are way more accurate than name lookups
- **Returns:** industry, employees, revenue, location, LinkedIn, description

---

## Automatic Memory System

### Cron Jobs

| Job | Schedule | Purpose |
|-----|----------|---------|
| Daily Auto-Update | 4:00 AM | Update Clawdbot and skills |
| Nightly Memory Review | 10:30 PM | Extract learnings, update MEMORY.md |
| Daily Memory Snapshot | Every 6 hours | Log progress on active projects |

### Memory Files

| File | Purpose | Update Frequency |
|------|---------|------------------|
| `MEMORY.md` | Long-term curated memory | Nightly (auto) + manual |
| `memory/YYYY-MM-DD.md` | Daily raw logs | Every 6 hours (auto) + manual |
| `.learnings/LEARNINGS.md` | Corrections & insights | As needed |
| `.learnings/ERRORS.md` | Failed commands | As needed |

---

*Last updated: 2026-02-09*
