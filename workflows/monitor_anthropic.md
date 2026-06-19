# Workflow: Monitor Anthropic Website for Updates

## Objective
Detect and report new updates, releases, and announcements on anthropic.com twice daily (6am CT and 6pm CT).

## Required Inputs
- None (tool is self-contained with embedded URLs)

## Tools Used
- `tools/monitor_anthropic_website.py` - Scrapes Anthropic website and compares against baseline

## Procedure

1. **Scheduled Execution**
   - Tool is triggered at 6:00 AM CT and 6:00 PM CT via cloud scheduler
   - No manual intervention required

2. **Scraping & Baseline Comparison**
   - Tool scrapes key Anthropic pages:
     - https://www.anthropic.com/ (main landing)
     - https://www.anthropic.com/news (news & announcements)
     - https://www.anthropic.com/research (research publications)
   - Tool extracts title, description, and markdown content (first 5000 chars)
   - Compares current state against baseline stored in `.tmp/anthropic_baseline.json`

3. **Change Detection**
   - Identifies new pages not previously seen
   - Flags title and description changes
   - Extracts lines mentioning: release, announcement, update, new, launch, available, introducing, published
   - Stores changes in timestamped JSON report in `.tmp/`

4. **Report Generation**
   - Creates report: `.tmp/anthropic_monitor_report_YYYYMMDD_HHMMSS.json`
   - Report includes:
     - `new_sections`: New pages detected
     - `updated_content`: Changes found in existing content
     - `timestamp`: When the check ran
   - Baseline is automatically updated for next comparison

5. **Notification**
   - If changes detected: Report output is printed to console/logs
   - If no changes: Quiet execution, "No changes detected" logged
   - (Optional future: Email/Slack notification can be added)

## Expected Output
- Timestamped JSON report in `.tmp/anthropic_monitor_report_*.json`
- Updated baseline snapshot in `.tmp/anthropic_baseline.json`
- Exit code 0 in all cases (success/no changes)

## Error Handling

- **Firecrawl API fails**: Check FIRECRAWL_API_KEY in .env. Verify API quota not exceeded. Wait and retry next scheduled run.
- **Scraping timeout**: Tool has 30-second timeout per page. If timeouts occur, note in logs and retry next run.
- **Missing baseline**: Tool creates baseline on first run automatically. Subsequent runs compare against it.
- **No FIRECRAWL_API_KEY**: Tool exits with error code 1. Check .env configuration.

## Scheduling

Run via cloud scheduler (e.g., `/schedule` or cron):
- **6:00 AM CT** (11:00 AM UTC): `python tools/monitor_anthropic_website.py`
- **6:00 PM CT** (11:00 PM UTC): `python tools/monitor_anthropic_website.py`

## Notes & Learnings

- **First run**: Will detect nothing (baseline just created). Subsequent runs show real changes.
- **Rate limiting**: Firecrawl API has usage limits. Monitor call count if running more frequently.
- **Content extraction**: Only first 5000 chars of markdown stored to reduce storage. Increase if more detail needed.
- **Keyword detection**: Currently hardcoded keyword list. Can be expanded as needed (research, claude, model, etc.).
