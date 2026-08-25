#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为 Q1 batch 02 的 5 个工具追加高质量语义化英文（最小侵入：仅插入行）。"""
import io, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (slug, en_title, en_desc)
BATCH = [
    ("it/csv-to-yaml", "CSV to YAML Converter",
     "CSV to YAML Converter - Paste CSV text and convert to YAML lists (first row as header) or plain arrays. Supports quoted fields. Free, browser-only."),
    ("it/mac-generator", "MAC Address Generator",
     "MAC Address Generator - Generate random MAC addresses in bulk, with optional vendor OUI prefix. Copy results instantly. Free, browser-only."),
    ("it/ipv6-ula", "IPv6 ULA Generator",
     "IPv6 ULA Generator - Generate IPv6 Unique Local Address (fd00::/8) prefixes and sample addresses with random global IDs. Free, browser-only."),
    ("it/phone-parser", "Phone Number Parser & Formatter",
     "Phone Number Parser & Formatter - Enter any phone number and get E.164 and grouped national/international formats by country. Free, browser-only."),
    ("it/git-cheatsheet", "Git Command Cheat Sheet",
     "Git Command Cheat Sheet - Search common Git commands by category with keyword filter, copy ready-to-use snippets. Free, browser-only."),
]

def insert_lines(path, make_line):
    with io.open(path, "r", encoding="utf-8") as f:
        text = f.read()
    # 已存在则跳过
    new = []
    for slug, en, ed in BATCH:
        if ('"%s"' % slug) in text:
            print("  skip (exists):", slug)
            continue
        new.append(make_line(slug, en, ed))
    if not new:
        print("  nothing to add in", os.path.basename(path))
        return
    # 在首行 '{' 之后插入
    nl = text.index("\n", text.index("{")) + 1
    inserted = "".join(line + "\n" for line in new)
    text = text[:nl] + inserted + text[nl:]
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("  added %d entries ->" % len(new), os.path.basename(path))

ov = os.path.join(ROOT, "i18n", "tools", "_en_override.json")
sl = os.path.join(ROOT, "i18n", "tools", "slug-en.json")

insert_lines(ov, lambda s, en, ed: '"%s":{"en":"%s","ed":"%s","ind":"%s"}' % (s, en, ed, s.split("/")[0]))
insert_lines(sl, lambda s, en, ed: '"%s":{"en":"%s","ed":"%s"}' % (s, en, ed))

# 校验
import json
for p in (ov, sl):
    json.load(io.open(p, encoding="utf-8"))
    print("  JSON valid:", os.path.basename(p))
