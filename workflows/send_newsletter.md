# Newsletter Automation Workflow

## Objective
Given a topic, research it, write newsletter content, generate an infographic, format as HTML email, and send via Gmail.

## Inputs
- **Topic**: Research subject (e.g., "AI trends in 2026", "Virtual assistant tools")
- **Recipient Email**: Gmail address to send the draft to (default: `pvegasrentals@gmail.com`)
- **CTA URL**: Call-to-action link (optional, default: "#")

## Outputs
- Gmail draft with full HTML email containing research-backed content and infographic
- Screenshottable HTML email ready for review

---

## Execution Steps

### Step 1: Research (Agent-Orchestrated)
**Tool**: `tools/research_topic.py`

1. Use **WebSearch** and **WebFetch** tools to research the topic
2. Collect 3-5 reliable sources
3. Extract key points, statistics, and quotes
4. Compile into structured JSON with:
   - `title`: formatted topic name
   - `key_points`: 3-4 main findings
   - `stats`: list of {label, value, context} for infographic
   - `sources`: list of {title, url}

**Output**: JSON file or variable with research data

---

### Step 2: Write Content (Agent Task)
**Tool**: N/A (Agent writes directly)

Given the research from Step 1, compose newsletter body:
- **Headline**: Compelling, concise (6-10 words)
- **Introduction**: 2-3 sentences setting context
- **Sections**: 3-4 body sections (each 2-3 sentences) covering key points
- **Call-to-Action**: 1-2 sentence closing call-to-action
- **Format**: Plain text or simple HTML with `<p>` tags

**Output**: HTML string with newsletter copy

---

### Step 3: Generate Infographic
**Tool**: `tools/generate_infographic.py`

Input the stats from Step 1 (list of {label, value, context} objects).
Tool generates styled HTML/CSS stat cards with:
- Blue (#0055CC) and green (#4CAF50) brand colors
- Gradient backgrounds
- Responsive layout
- Email-client safe (inline CSS only)

**Output**: HTML string with infographic

---

### Step 4: Format HTML Email
**Tool**: `tools/format_newsletter_html.py`

Combine:
- Headline (from Step 2)
- Content (from Step 2)
- Infographic (from Step 3)
- CTA text & URL (from inputs)

Tool wraps in full HTML email template with:
- Branded header (blue gradient)
- Responsive layout
- Footer with branding
- Inline CSS for email compatibility

**Output**: Complete HTML email string

---

### Step 5: Send via Gmail
**Tool**: Gmail MCP `create_draft`

1. Call Gmail MCP tool: `mcp__claude_ai_Gmail__create_draft`
2. Parameters:
   - `to`: recipient email address
   - `subject`: topic headline
   - `body`: full HTML from Step 4
3. Gmail will create a draft in the recipient's inbox
4. You review the draft in Gmail, take a screenshot, then send manually

**Output**: Gmail draft (ready to review & send)

---

## Edge Cases & Notes

- **Research fails**: If WebSearch returns minimal results, use broader search terms or fallback sources
- **Missing stats**: If fewer than 3 stats are found, use general market metrics or growth rates related to the topic
- **Email rendering**: All CSS is inline; no external styles. Test in Gmail draft before sending.
- **Single recipient**: Currently hardcoded as `pvegasrentals@gmail.com`. To change, update the recipient email in the Gmail MCP call.

## Verification Checklist
- [ ] Gmail draft created successfully
- [ ] Opened draft in Gmail (web or app)
- [ ] All images/formatting visible and correct
- [ ] Brand colors (blue & green) applied
- [ ] Infographic stats readable
- [ ] CTA button visible
- [ ] Ready to screenshot or send
