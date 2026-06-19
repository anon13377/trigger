# Workflow: Monitor Anthropic Website for Updates

## Objective
Detect and report new updates, releases, and announcements on anthropic.com twice daily (6am CT and 6pm CT).

## Required Inputs
- None (tool is self-contained with embedded URLs)

## Tools Used
- `tools/monitor_anthropic_website.py` - Fetches Anthropic website pages using WebFetch and compares against baseline

## Procedure

1. **Scheduled Execution**
   - Tool is triggered at 6:00 AM CT and 6:00 PM CT via cloud scheduler
   - No manual intervention required

2. **Fetching & Baseline Comparison**
   - Tool fetches key Anthropic pages using Claude Code's built-in WebFetch:
     - https://www.anthropic.com/ (main landing)
     - https://www.anthropic.com/news (news & announcements)
     - https://www.anthropic.com/research (research publications)
   - Tool extracts plain text content (first 5000 chars)
   - Compares current state against baseline stored in `.tmp/anthropic_baseline.json`

3. **Change Detection**
   - Identifies new pages not previously seen
   - Compares content using content hash for quick detection
   - Extracts lines mentioning: release, announcement, update, new, launch, available, introducing, published, claude, model
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

- **WebFetch fails**: Network issue or page unavailable. Tool logs error and continues. Check Anthropic site is accessible.
- **Fetch timeout**: Tool has 30-second timeout per page. If timeouts occur, note in logs and retry next run.
- **Missing baseline**: Tool creates baseline on first run automatically. Subsequent runs compare against it.
- **No content fetched**: If all pages fail to fetch, tool exits with error code 1. Check network connectivity.

## Scheduling

Run via cloud scheduler (e.g., `/schedule` or cron):
- **6:00 AM CT** (11:00 AM UTC): `python tools/monitor_anthropic_website.py`
- **6:00 PM CT** (11:00 PM UTC): `python tools/monitor_anthropic_website.py`

## Notes & Learnings

- **First run**: Will detect nothing (baseline just created). Subsequent runs show real changes.
- **No API limits**: WebFetch is free and has no rate limits beyond normal web request courtesy.
- **Content extraction**: Only first 5000 chars of text stored to reduce storage. Increase if more detail needed.
- **Keyword detection**: Hardcoded keywords include: release, announcement, update, new, launch, available, introducing, published, claude, model. Expand as needed.
- **Content hashing**: Uses Python hash for quick comparison. First run creates baseline, subsequent runs only flag content that has changed.
