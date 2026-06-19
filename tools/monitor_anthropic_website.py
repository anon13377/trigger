#!/usr/bin/env python3
"""
Monitor anthropic.com for new updates and releases using WebFetch.
Compares current state against last known state and reports changes.
Output: JSON report to .tmp/
"""
import json
import os
import sys
from datetime import datetime
import subprocess
from html.parser import HTMLParser

# Baseline snapshot location
BASELINE_FILE = ".tmp/anthropic_baseline.json"


def webfetch(url):
    """Fetch URL content using Claude Code's built-in WebFetch tool"""
    try:
        result = subprocess.run(
            ["claude", "web", "fetch", url],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            return result.stdout
        else:
            print(f"WebFetch error for {url}: {result.stderr}", file=sys.stderr)
            return ""
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return ""


def extract_text(html):
    """Extract plain text from HTML"""
    class HTMLTextExtractor(HTMLParser):
        def __init__(self):
            super().__init__()
            self.text = []
            self.in_script = False
            self.in_style = False

        def handle_starttag(self, tag, attrs):
            if tag in ("script", "style"):
                if tag == "script":
                    self.in_script = True
                else:
                    self.in_style = True

        def handle_endtag(self, tag):
            if tag == "script":
                self.in_script = False
            elif tag == "style":
                self.in_style = False

        def handle_data(self, data):
            if not self.in_script and not self.in_style:
                text = data.strip()
                if text:
                    self.text.append(text)

    parser = HTMLTextExtractor()
    try:
        parser.feed(html)
        return " ".join(parser.text)
    except:
        return html[:5000]


def scrape_anthropic():
    """Scrape key pages from anthropic.com"""
    pages = [
        "https://www.anthropic.com/",
        "https://www.anthropic.com/news",
        "https://www.anthropic.com/research",
    ]

    content = {}
    for url in pages:
        print(f"Fetching {url}...", file=sys.stderr)
        html = webfetch(url)

        if html:
            text = extract_text(html)
            # Extract title from HTML meta tags or use URL
            title = url.split("/")[-1] or "homepage"
            content[url] = {
                "title": title,
                "text": text[:5000],  # First 5000 chars
                "hash": hash(text) & 0x7FFFFFFF,  # Content hash for quick comparison
            }
        else:
            print(f"Failed to fetch {url}", file=sys.stderr)

    return content


def extract_key_sections(text):
    """Extract potential update/release mentions from text"""
    lines = text.lower().split("\n")
    keywords = ["release", "announcement", "update", "new", "launch", "available", "introducing", "published", "claude", "model"]

    relevant_lines = []
    for line in lines:
        if any(kw in line for kw in keywords) and len(line.strip()) > 15:
            relevant_lines.append(line.strip()[:100])

    return relevant_lines[:15]


def detect_changes(current, baseline):
    """Compare current scrape with baseline, return what's new"""
    changes = {
        "new_sections": [],
        "updated_content": [],
        "timestamp": datetime.utcnow().isoformat(),
    }

    for url, current_data in current.items():
        if url not in baseline:
            changes["new_sections"].append({
                "url": url,
                "title": current_data.get("title", ""),
                "change_type": "new_page"
            })
            continue

        baseline_data = baseline.get(url, {})

        # Quick check: compare content hash
        if current_data.get("hash") != baseline_data.get("hash"):
            # Content changed, extract what's new
            current_key = set(extract_key_sections(current_data.get("text", "")))
            baseline_key = set(extract_key_sections(baseline_data.get("text", "")))

            new_mentions = current_key - baseline_key
            if new_mentions:
                changes["updated_content"].append({
                    "url": url,
                    "change_type": "content_updated",
                    "new_mentions": list(new_mentions)[:10],
                })

    return changes


def main():
    os.makedirs(".tmp", exist_ok=True)

    # Fetch current state
    current = scrape_anthropic()

    if not current:
        print("ERROR: Failed to fetch any pages from anthropic.com", file=sys.stderr)
        sys.exit(1)

    # Load baseline (or create if doesn't exist)
    baseline = {}
    if os.path.exists(BASELINE_FILE):
        with open(BASELINE_FILE, "r") as f:
            baseline = json.load(f)

    # Detect changes
    report = detect_changes(current, baseline)

    # Save current as new baseline
    with open(BASELINE_FILE, "w") as f:
        json.dump(current, f, indent=2)

    # Generate report
    report_file = f".tmp/anthropic_monitor_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)

    num_changes = len(report['new_sections']) + len(report['updated_content'])
    print(f"Report: {report_file}")
    print(f"Changes detected: {num_changes} update(s)")

    if num_changes > 0:
        print("\n=== ANTHROPIC WEBSITE UPDATES ===")
        print(json.dumps(report, indent=2))
    else:
        print("No changes detected.")

    sys.exit(0)


if __name__ == "__main__":
    main()
