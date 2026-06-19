#!/usr/bin/env python3
"""
Format newsletter content into polished HTML email.
Incorporates brand colors: blue (#0055CC) and green (#4CAF50).
"""
import json
import sys
import os
from pathlib import Path


def format_newsletter_html(
    subject: str,
    headline: str,
    content: str,
    infographic_html: str,
    cta_text: str = "Learn More",
    cta_url: str = "#"
) -> str:
    """
    Wrap newsletter content in branded HTML email template.
    """

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{subject}</title>
</head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background: #f5f5f5;">
    <div style="max-width: 600px; margin: 0 auto; background: white;">
        <!-- Header with brand color -->
        <div style="
            background: linear-gradient(135deg, #0055CC 0%, #004499 100%);
            padding: 30px;
            text-align: center;
            color: white;
        ">
            <div style="font-size: 12px; letter-spacing: 2px; text-transform: uppercase; opacity: 0.9; margin-bottom: 10px;">
                Newsletter
            </div>
            <h1 style="margin: 0; font-size: 32px; font-weight: bold;">
                {headline}
            </h1>
        </div>

        <!-- Body content -->
        <div style="padding: 40px 30px;">
            {content}
        </div>

        <!-- Infographic section -->
        <div style="padding: 0 30px;">
            {infographic_html}
        </div>

        <!-- CTA button -->
        <div style="padding: 30px; text-align: center;">
            <a href="{cta_url}" style="
                background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
                color: white;
                padding: 12px 32px;
                text-decoration: none;
                border-radius: 6px;
                font-weight: 600;
                font-size: 14px;
                display: inline-block;
            ">
                {cta_text}
            </a>
        </div>

        <!-- Footer -->
        <div style="
            background: #f9f9f9;
            border-top: 1px solid #e0e0e0;
            padding: 20px 30px;
            text-align: center;
            font-size: 12px;
            color: #666;
        ">
            <p style="margin: 5px 0;">
                <strong style="color: #0055CC;">Virtual Assistant Resources</strong>
            </p>
            <p style="margin: 5px 0;">
                Newsletter © 2026. All rights reserved.
            </p>
            <p style="margin: 5px 0; color: #999;">
                You're receiving this because you subscribed to our updates.
            </p>
        </div>
    </div>
</body>
</html>
"""
    return html


if __name__ == "__main__":
    # Example usage
    example_content = """
    <p style="font-size: 16px; line-height: 1.6; color: #333;">
        Discover the latest insights and trends shaping the industry today.
        Our research reveals key opportunities for growth and innovation.
    </p>
    """

    example_infographic = """
    <div style="background: #f0f8ff; padding: 20px; border-radius: 8px; text-align: center; color: #0055CC;">
        <strong>Key Metrics from This Month</strong>
    </div>
    """

    html = format_newsletter_html(
        subject="Newsletter",
        headline="Latest Industry Insights",
        content=example_content,
        infographic_html=example_infographic,
        cta_text="Read Full Article"
    )

    print(html)
