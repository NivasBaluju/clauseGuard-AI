import urllib.request
import urllib.parse
import re
import json
import time
from pathlib import Path

def search_ddg(query):
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote_plus(query)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    )
    try:
        resp = urllib.request.urlopen(req, timeout=12)
        html = resp.read().decode("utf-8", errors="ignore")
        raw_links = re.findall(r'href="([^"]+uddg=[^"]+)"', html)
        decoded = []
        for l in raw_links:
            m = re.search(r"uddg=([^&]+)", l)
            if m:
                actual_url = urllib.parse.unquote(m.group(1))
                if actual_url.startswith("http") and not any(skip in actual_url for skip in ["duckduckgo", "yandex", "bing"]):
                    decoded.append(actual_url)
        return decoded
    except Exception as e:
        print(f"Error searching '{query}': {e}")
        return []

if __name__ == "__main__":
    queries = [
        ("rental", "sample residential lease agreement site:gov filetype:pdf"),
        ("rental", "residential tenancy agreement template site:edu filetype:pdf"),
        ("rental", "model residential lease housing authority site:gov filetype:pdf"),
        ("offer", "sample job offer letter site:edu filetype:pdf"),
        ("offer", "employment offer letter template site:gov filetype:pdf"),
        ("offer", "faculty staff offer letter template site:edu filetype:pdf"),
        ("insurance", "specimen policy form homeowners site:gov filetype:pdf"),
        ("insurance", "renters policy specimen HO-4 site:gov filetype:pdf"),
        ("insurance", "homeowners broad form policy specimen site:gov filetype:pdf"),
    ]

    results = {}
    for cat, q in queries:
        print(f"Searching: {q}...")
        links = search_ddg(q)
        print(f"  Found {len(links)} links")
        if cat not in results:
            results[cat] = []
        for l in links:
            if l not in results[cat]:
                results[cat].append(l)
        time.sleep(2)

    with open("ml/discovered_urls.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\nTotal Discovered:")
    for cat, urls in results.items():
        print(f"  {cat}: {len(urls)} unique URLs")
