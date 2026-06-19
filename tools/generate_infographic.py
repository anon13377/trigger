#!/usr/bin/env python3
"""
Generate HTML/CSS infographic from research stats.
Uses brand colors: blue (#0055CC) and green (#4CAF50).
"""
import json
import sys


def generate_infographic(stats: list) -> str:
    """
    Convert stats list into styled HTML infographic.
    Stats format: [{"label": "...", "value": "...", "context": "..."}, ...]
    """
    stat_cards = ""
    for stat in stats:
        stat_cards += f"""
        <div style="
            background: linear-gradient(135deg, #0055CC 0%, #004499 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            flex: 1;
            min-width: 150px;
        ">
            <div style="font-size: 32px; font-weight: bold; color: #4CAF50;">
                {stat['value']}
            </div>
            <div style="font-size: 14px; margin-top: 8px; font-weight: 600;">
                {stat['label']}
            </div>
            <div style="font-size: 12px; margin-top: 4px; opacity: 0.9;">
                {stat['context']}
            </div>
        </div>
        """

    html = f"""
    <div style="
        background: linear-gradient(135deg, rgba(0, 85, 204, 0.05) 0%, rgba(76, 175, 80, 0.05) 100%);
        padding: 30px;
        border-radius: 12px;
        margin: 20px 0;
    ">
        <div style="
            color: #0055CC;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
            text-align: center;
        ">
            Key Insights
        </div>
        <div style="
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            justify-content: center;
        ">
            {stat_cards}
        </div>
    </div>
    """
    return html


if __name__ == "__main__":
    # Example usage
    example_stats = [
        {"label": "Growth Rate", "value": "42%", "context": "YoY increase"},
        {"label": "Market Size", "value": "$2.5B", "context": "2026 valuation"},
        {"label": "Users", "value": "127M", "context": "Active worldwide"}
    ]

    if len(sys.argv) > 1:
        stats = json.loads(sys.argv[1])
    else:
        stats = example_stats

    html = generate_infographic(stats)
    print(html)
