# Newsletter Automation System

A WAT framework workflow for automating newsletter creation: research → write → design → send.

## Quick Start

### Step 1: Generate Newsletter HTML
```bash
python tools/orchestrate_newsletter.py "Your Topic Here"
```

This generates `.tmp/newsletter_final.html` with:
- Researched facts and stats
- Branded design (blue #0055CC + green #4CAF50 colors)
- Responsive HTML infographic
- Ready-to-send email template

**Example:**
```bash
python tools/orchestrate_newsletter.py "AI trends in 2026"
```

### Step 2: Create Gmail Draft
Use the Gmail MCP tool to create a draft:

```
mcp__claude_ai_Gmail__create_draft
  to: "pvegasrentals@gmail.com"
  subject: "Your Topic Here"
  body: <paste full HTML from .tmp/newsletter_final.html>
```

**Or in code:**
```python
from mcp_tools import gmail_create_draft

html = open('.tmp/newsletter_final.html').read()
gmail_create_draft(
    to="pvegasrentals@gmail.com",
    subject="AI Trends in 2026",
    body=html
)
```

### Step 3: Review & Send
1. Open Gmail
2. Find the draft in your drafts folder
3. Take a screenshot (or review in browser)
4. Click Send when ready

---

## System Architecture

### Tools
- **`research_topic.py`** — Gathers data from web sources
- **`generate_infographic.py`** — Creates styled HTML stat cards
- **`format_newsletter_html.py`** — Wraps content in email template
- **`orchestrate_newsletter.py`** — Master orchestrator (calls all tools)

### Workflow
See `workflows/send_newsletter.md` for detailed SOP with edge cases.

### Branding
- **Colors**: Blue (#0055CC), dark blue (#004499), green (#4CAF50)
- **Logo/Assets**: Available in `brand_assests/` folder
- **Template**: Responsive, email-client safe (inline CSS only)

---

## Customization

### Change Recipient Email
Edit `orchestrate_newsletter.py` or pass email to Gmail MCP:

```python
gmail_create_draft(
    to="your.email@example.com",  # Change this
    subject="...",
    body=html
)
```

### Change CTA Text & URL
Edit `orchestrate_newsletter.py` line ~100:

```python
final_html = run_format(
    headline=research["title"],
    content=content,
    infographic_html=infographic,
    cta_text="Your Button Text",  # Change this
    cta_url="https://your-url.com"  # And this
)
```

### Change Brand Colors
Edit color values in:
- `tools/generate_infographic.py` (look for #0055CC, #4CAF50)
- `tools/format_newsletter_html.py` (same colors)

---

## How It Works (Detail)

### Step 1: Research
The agent uses **WebSearch** and **WebFetch** tools to:
1. Search for the topic
2. Fetch top 3-5 sources
3. Extract key points and statistics
4. Return structured JSON:
   ```json
   {
     "title": "Topic Name",
     "key_points": ["...", "...", "..."],
     "stats": [
       {"label": "Growth", "value": "42%", "context": "YoY"},
       ...
     ],
     "sources": [{"title": "...", "url": "..."}]
   }
   ```

### Step 2: Write Content
The agent formats research into newsletter body:
- Headline
- Introduction
- 3 body sections with key points
- Call-to-action

### Step 3: Generate Infographic
Python tool converts stats into HTML/CSS:
- Blue gradient stat cards
- Green accent numbers
- Responsive flexbox layout
- Email-safe inline styles

### Step 4: Format Email
Combines content + infographic into full HTML email:
- Blue gradient header
- Responsive layout (max 600px for email clients)
- Inline CSS (no external stylesheets)
- Green CTA button
- Branded footer

### Step 5: Send via Gmail
Gmail MCP creates a draft for review before sending.

---

## Files Structure

```
tools/
  ├── research_topic.py          # Research orchestrator
  ├── generate_infographic.py    # HTML infographic generator
  ├── format_newsletter_html.py  # Email template
  └── orchestrate_newsletter.py  # Master workflow runner

workflows/
  └── send_newsletter.md         # Detailed SOP

.tmp/
  └── newsletter_final.html      # Generated output (gitignored)

brand_assests/                    # Brand colors & logo
  └── ChatGPT Image Jun 17, 2026, 04_26_36 PM.png
```

---

## Troubleshooting

### "Email formatting looks broken in Gmail"
→ Check that inline CSS is present. Gmail doesn't support external stylesheets.

### "Research returned no results"
→ Try broader search terms in `orchestrate_newsletter.py`, or use known stats for the topic.

### "Stats display wrong"
→ Verify JSON format matches expected structure (label, value, context).

---

## Future Enhancements

- **Real research integration**: Replace placeholder with actual WebSearch orchestration
- **Image generation**: Integrate Key.ai API when available for custom graphics
- **Template variations**: Add dark mode, accent color options
- **Subscriber list**: Support CSV/Google Sheet for multiple recipients
- **Scheduling**: Automate newsletter creation on a schedule (cron)
