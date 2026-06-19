# Skool Community Search via Firecrawl

## Objective
Find niche communities on Skool.com using Firecrawl's search API.

## Current Use Case
Spanish-speaking sales communities (remote sales, online sales, high ticket, closer de ventas).

## How to Run
```bash
python tools/firecrawl_skool_search.py
```

## What It Does
1. Runs 8 search queries combining `site:skool.com` with Spanish sales keywords
2. Deduplicates by URL, keeps only skool.com results
3. Outputs JSON + CSV to `.tmp/`

## Customizing for Other Niches
Edit the `QUERIES` list in `tools/firecrawl_skool_search.py`. Keep the `site:skool.com` prefix. Mix English and target-language terms for broader coverage.

## Output
- `.tmp/skool_spanish_sales_results.json` — full data including markdown preview
- `.tmp/skool_spanish_sales_results.csv` — clean spreadsheet (name, url, description)

## API Notes
- Firecrawl search endpoint: `POST https://api.firecrawl.dev/v1/search`
- 1-second delay between queries to avoid rate limits
- Key stored in `.env` as `FIRECRAWL_API_KEY`
