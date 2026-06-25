"""Inspect what's actually in the pages — look at content sections and ipai xlsx link."""
import re
from pathlib import Path

RAW = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_html")

# ipai: find xlsx links
ipai = (RAW / "ipai.html").read_text(encoding="utf-8")
xlsx_links = re.findall(r'href=["\']([^"\']*(?:\.xlsx?|\.csv)[^"\']*)["\']', ipai, flags=re.I)
print("=== ipai xlsx links ===")
for l in xlsx_links:
    print(" -", l)

# participatives: find JS / AJAX endpoints
part = (RAW / "participatives.html").read_text(encoding="utf-8")
# Find all script srcs
scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', part, flags=re.I)
print("\n=== participatives script srcs ===")
for s in scripts[:30]:
    print(" -", s)

# Find data-* attributes / inline JSON
inline_json = re.findall(r'(?:var|data|json|results|content)\s*[:=]\s*(\{[\s\S]{50,500}?\})', part)
print(f"\n=== inline JSON candidates: {len(inline_json)} ===")
for j in inline_json[:5]:
    print(" -", j[:200])

# eZ publish / ezjscore AJAX pattern (BAM uses ezjscore)
ajax_calls = re.findall(r'(?:ezjscore|ezajax|loadContent|fetchContent)\s*\(\s*["\']([^"\']+)["\']', part, flags=re.I)
print(f"\n=== ezjscore/ajax: {len(ajax_calls)} ===")
for a in ajax_calls[:10]:
    print(" -", a)

# Look for hash-based fetch URL pattern
hash_urls = re.findall(r'href=["\']([^"\']+/content/view/[^"\']*/full/[^"\']+)["\']', part, flags=re.I)
print(f"\n=== content/view/ hash urls: {len(hash_urls)} ===")
for u in hash_urls[:10]:
    print(" -", u)

# Find input forms with action URLs (might be data submit)
forms = re.findall(r'<form[^>]*action=["\']([^"\']+)["\']', part, flags=re.I)
print(f"\n=== form actions: {len(forms)} ===")
for f in forms[:5]:
    print(" -", f)

# Print the title and any 'shortcut' content
title = re.search(r"<title>([^<]+)</title>", part)
print(f"\ntitle: {title.group(1) if title else 'none'}")

# Look for any URL fragment containing 'json', 'export', 'download'
export_urls = re.findall(r'["\']([^"\']*(?:export|download|json|api)[^"\']*)["\']', part, flags=re.I)
print(f"\n=== export/download/api mentions: {len(export_urls)} ===")
unique_export = sorted(set(export_urls))
for u in unique_export[:20]:
    print(" -", u)