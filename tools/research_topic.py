#!/usr/bin/env python3
"""
Research tool using WebSearch to gather information on a topic.
Output: JSON with key points, stats, and sources.
"""
import json
import sys


def research_topic(topic: str) -> dict:
    """
    Placeholder that demonstrates the research structure.
    In production, this would be orchestrated by an Agent using WebSearch/WebFetch.
    """
    return {
        "topic": topic,
        "title": f"Research on {topic}",
        "key_points": [
            "Point 1: Key finding about the topic",
            "Point 2: Important context or trend",
            "Point 3: Emerging insight or statistic"
        ],
        "stats": [
            {"label": "Metric A", "value": "42%", "context": "year-over-year growth"},
            {"label": "Metric B", "value": "$2.5B", "context": "market size"},
            {"label": "Metric C", "value": "127M", "context": "active users"}
        ],
        "sources": [
            {"title": "Source 1", "url": "https://example.com/1"},
            {"title": "Source 2", "url": "https://example.com/2"}
        ]
    }


if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "AI trends"
    result = research_topic(topic)
    print(json.dumps(result, indent=2))
