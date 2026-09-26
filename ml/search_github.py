import urllib.request
import urllib.parse
import json

headers = {
    "User-Agent": "ClauseGuard-Dataset-Builder/1.0",
    "Accept": "application/vnd.github.v3+json",
}

queries = [
    ("rental", "residential lease agreement in:path extension:txt"),
    ("rental", "residential tenancy agreement in:path extension:md"),
    ("offer", "offer letter in:path extension:txt"),
    ("offer", "employment agreement in:path extension:txt"),
    ("insurance", "policy specimen in:path extension:txt"),
]

for cat, q in queries:
    url = f"https://api.github.com/search/code?q={urllib.parse.quote_plus(q)}&per_page=10"
    print(f"Searching GitHub Code for: {q}...")
    try:
        req = urllib.request.Request(url, headers=headers)
        res = urllib.request.urlopen(req, timeout=12)
        data = json.loads(res.read().decode())
        items = data.get("items", [])
        print(f"  Found {len(items)} items (total: {data.get('total_count', 0)})")
        for item in items[:5]:
            raw_url = item.get("html_url", "").replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
            print("   ->", item.get("name"), "|", raw_url)
    except Exception as e:
        print(f"  Error: {e}")
