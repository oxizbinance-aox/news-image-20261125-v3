#!/usr/bin/env python3
"""Layout validator for news-image-20261125-v3.

Fails the build (exit 1) when the rendered page breaks any rule:
entry.png must be 1024x1024, pin_debug.txt must show 13/13 pins on
land, region counts must add to 38 with no region above 7, and the
last ALSO number must be 38. Run after draw_news25_v3.py.
"""
import re
import sys
from PIL import Image

fails = []

try:
    img = Image.open("entry.png")
    if img.size != (1024, 1024):
        fails.append(f"entry.png is {img.size}, expected (1024, 1024)")
    if img.mode != "RGB":
        fails.append(f"entry.png mode is {img.mode}, expected RGB")
except FileNotFoundError:
    fails.append("entry.png missing — run draw_news25_v3.py first")

land_ok = 0
pins_seen = set()
regions = {}
try:
    text = open("pin_debug.txt").read()
    for line in text.splitlines():
        m = re.match(r"\s*(\d+)\s*\|\s*(\S+(?:\s\S+)?)\s*\|", line)
        if m and "|" in line and "True" in line:
            pins_seen.add(int(m.group(1)))
            land_ok += 1
    m = re.search(r"regions: \{([^}]*)\}", text)
    if m:
        for part in m.group(1).split(","):
            k, v = part.split(":")
            regions[k.strip().strip("'")] = int(v)
    if len(pins_seen) != 13 or land_ok != 13:
        fails.append(f"pins on land: {land_ok}/13, seen {sorted(pins_seen)}")
    if sum(regions.values()) != 38:
        fails.append(f"region counts add to {sum(regions.values())}, not 38")
    if regions and max(regions.values()) > 7:
        fails.append(f"a region tops 7: {regions}")
    if "last also: 38" not in text:
        fails.append("last ALSO number is not 38")
except FileNotFoundError:
    fails.append("pin_debug.txt missing — run draw_news25_v3.py first")

try:
    readme = open("README.md").read()
    for needle in ["38 stories", "7 regions", "DATE CHECK", "HOW CHECKED",
                   "PIN COLOUR = REGION"]:
        if needle not in readme:
            fails.append(f"README missing: {needle}")
except FileNotFoundError:
    fails.append("README.md missing")

if fails:
    print("VALIDATOR FAIL")
    for f in fails:
        print(" -", f)
    sys.exit(1)
print(f"VALIDATOR PASS: entry.png 1024x1024, pins 13/13 on land, "
      f"regions {regions} = 38, last ALSO 38")
