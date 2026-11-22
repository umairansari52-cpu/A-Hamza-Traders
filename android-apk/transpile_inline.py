#!/usr/bin/env python3
"""Transpile inline JavaScript in the packaged copy for older Android WebView."""
import re
import subprocess
from pathlib import Path

source = Path("index.html").read_text(encoding="utf-8")
pattern = re.compile(r"(<script\b([^>]*)>)([\s\S]*?)(</script\s*>)", re.IGNORECASE)

def convert(match):
    opening, attrs, body, closing = match.groups()
    if re.search(r"\bsrc\s*=", attrs, re.IGNORECASE):
        return match.group(0)
    script_type = re.search(r"""\btype\s*=\s*["']?([^"'\s>]+)""", attrs, re.IGNORECASE)
    if script_type and script_type.group(1).lower() not in ("text/javascript", "application/javascript", "module"):
        return match.group(0)
    result = subprocess.run(
        ["npx", "--no-install", "babel", "--no-comments"],
        input=body, text=True, capture_output=True, check=True
    )
    return opening + result.stdout + closing

converted, count = pattern.subn(convert, source)
if count < 1:
    raise SystemExit("No inline JavaScript blocks found")
out = Path("android-apk/generated-assets")
out.mkdir(parents=True, exist_ok=True)
(out / "index.html").write_text(converted, encoding="utf-8")
print(f"Transpiled {count} inline JavaScript blocks for older Android WebView.")
