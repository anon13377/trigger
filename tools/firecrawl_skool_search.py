#!/usr/bin/env python3
"""
Search Skool.com for Spanish-speaking sales communities using Firecrawl.
Output: JSON + CSV in .tmp/
"""
import json
import csv
import os
import sys
import time
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FIRECRAWL_API_KEY")
SEARCH_URL = "https://api.firecrawl.dev/v1/search"

QUERIES = [
    "site:skool.com ventas online español comunidad",
    "site:skool.com ventas remotas curso",
    "site:skool.com sales spanish speaking community",
    "site:skool.com remote sales español",
    "site:skool.com curso de ventas online",
    "site:skool.com vender por internet comunidad",
    "site:skool.com high ticket sales español",
    "site:skool.com closer de ventas",
]

def search(query, limit=20):
    resp = requests.post(
        SEARCH_URL,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json={"query": query, "limit": limit},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json().get("data", [])

def main():
    if not API_KEY:
        print("ERROR: FIRECRAWL_API_KEY not found in .env")
        sys.exit(1)

    os.makedirs(".tmp", exist_ok=True)
    seen_urls = set()
    results = []

    for q in QUERIES:
        print(f"Searching: {q}")
        try:
            hits = search(q)
            for h in hits:
                url = h.get("url", "")
                if url and url not in seen_urls and "skool.com" in url:
                    seen_urls.add(url)
                    results.append({
                        "name": h.get("title", "").strip(),
                        "url": url,
                        "description": h.get("description", "").strip(),
                        "markdown_preview": (h.get("markdown", "") or "")[:500],
                    })
            print(f"  -> {len(hits)} hits, {len(results)} unique so far")
        except Exception as e:
            print(f"  -> Error: {e}")
        time.sleep(1)

    results.sort(key=lambda r: r["name"].lower())

    with open(".tmp/skool_spanish_sales_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    with open(".tmp/skool_spanish_sales_results.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["name", "url", "description"])
        w.writeheader()
        for r in results:
            w.writerow({k: r[k] for k in ["name", "url", "description"]})

    print(f"\nDone! {len(results)} unique Skool groups found.")
    print(f"  JSON: .tmp/skool_spanish_sales_results.json")
    print(f"  CSV:  .tmp/skool_spanish_sales_results.csv")

if __name__ == "__main__":
    main()
