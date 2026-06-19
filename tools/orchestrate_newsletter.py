#!/usr/bin/env python3
"""
Master orchestration script for newsletter workflow.
This is the high-level coordinator that:
1. Takes a topic
2. Calls research_topic to gather data
3. Calls generate_infographic with stats
4. Calls format_newsletter_html with content + infographic
5. Outputs final HTML ready for Gmail

Usage:
  python orchestrate_newsletter.py "Your Topic Here"
"""
import json
import sys
import subprocess
from pathlib import Path

# Tool paths (relative to project root)
RESEARCH_TOOL = "tools/research_topic.py"
INFOGRAPHIC_TOOL = "tools/generate_infographic.py"
FORMAT_TOOL = "tools/format_newsletter_html.py"


def run_research(topic: str) -> dict:
    """Call research_topic.py and return JSON output."""
    result = subprocess.run(
        [sys.executable, RESEARCH_TOOL, topic],
        capture_output=True,
        text=True,
        check=True
    )
    return json.loads(result.stdout)


def run_infographic(stats: list) -> str:
    """Call generate_infographic.py with stats."""
    stats_json = json.dumps(stats)
    result = subprocess.run(
        [sys.executable, INFOGRAPHIC_TOOL, stats_json],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()


def run_format(
    headline: str,
    content: str,
    infographic_html: str,
    cta_text: str = "Learn More",
    cta_url: str = "#"
) -> str:
    """Call format_newsletter_html.py via Python subprocess (simpler than CLI args)."""
    # Import and call directly to avoid subprocess complexity
    import sys
    sys.path.insert(0, ".")
    from tools.format_newsletter_html import format_newsletter_html
    return format_newsletter_html(
        subject=headline,
        headline=headline,
        content=content,
        infographic_html=infographic_html,
        cta_text=cta_text,
        cta_url=cta_url
    )


def format_content(research: dict, headline: str = None) -> str:
    """Format research findings into newsletter body copy."""
    if not headline:
        headline = research.get("title", "Newsletter")

    content = f"""
    <p style="font-size: 16px; line-height: 1.6; color: #333; margin: 0 0 15px 0;">
        <strong>This Week's Highlights</strong>
    </p>
    """

    for i, point in enumerate(research.get("key_points", [])[:3], 1):
        content += f"""
        <p style="font-size: 14px; line-height: 1.6; color: #555; margin: 0 0 10px 0;">
            <strong>Point {i}:</strong> {point}
        </p>
        """

    content += """
    <p style="font-size: 12px; color: #999; margin: 15px 0 0 0;">
        Sources available in the resources section below.
    </p>
    """

    return content


def orchestrate(topic: str) -> str:
    """
    Master workflow: topic → research → content → infographic → formatted email.
    """
    print(f"[RESEARCH] {topic}")
    research = run_research(topic)

    print(f"[CONTENT] Formatting content...")
    content = format_content(research)

    print(f"[INFOGRAPHIC] Generating infographic...")
    infographic = run_infographic(research["stats"])

    print(f"[FORMAT] Formatting HTML email...")
    final_html = run_format(
        headline=research["title"],
        content=content,
        infographic_html=infographic,
        cta_text="Read Full Newsletter",
        cta_url="https://example.com"
    )

    return final_html


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python orchestrate_newsletter.py '<topic>'")
        print("Example: python orchestrate_newsletter.py 'AI trends 2026'")
        sys.exit(1)

    topic = sys.argv[1]
    html = orchestrate(topic)

    # Save output
    output_path = Path(".tmp") / "newsletter_final.html"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(html, encoding="utf-8")

    print(f"[SUCCESS] Newsletter generated: {output_path}")
    print(f"[NEXT] Ready to send via Gmail. Next step: create Gmail draft with this HTML.")
