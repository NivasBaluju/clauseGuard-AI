import urllib.request
import re
import urllib.parse

url = "https://html.duckduckgo.com/html/?q=residential+lease+agreement+site:gov+filetype:pdf"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
resp = urllib.request.urlopen(req, timeout=10)
data = resp.read().decode("utf-8", errors="ignore")

with open("ml/ddg_page.html", "w", encoding="utf-8") as f:
    f.write(data)

print(f"Saved {len(data)} bytes to ml/ddg_page.html")
# Print all hrefs in the page
hrefs = re.findall(r'href="([^"]+)"', data)
print(f"Total hrefs: {len(hrefs)}")
for h in hrefs[:15]:
    print("  href:", h)
