#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为 Q1 batch 03 的 6 个工具追加高质量语义化英文（最小侵入：仅插入行，行尾带逗号）。"""
import io, os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (slug, en_title, en_desc)
BATCH = [
    ("it/yaml-to-toml", "YAML to TOML Converter",
     "YAML to TOML Converter - Paste YAML text and convert it to TOML with nested tables, arrays and common scalars. Free, browser-only."),
    ("it/toml-to-yaml", "TOML to YAML Converter",
     "TOML to YAML Converter - Paste TOML text and convert it to YAML, including [section] and [[array of tables]]. Free, browser-only."),
    ("it/yaml-to-json", "YAML to JSON Converter",
     "YAML to JSON Converter - Paste YAML text and convert it to formatted JSON with nested maps and lists. Free, browser-only."),
    ("it/toml-to-json", "TOML to JSON Converter",
     "TOML to JSON Converter - Paste TOML text and convert it to formatted JSON, including [section] and [[array of tables]]. Free, browser-only."),
    ("it/emoji-picker", "Emoji Picker",
     "Emoji Picker - Search emojis by keyword (Chinese or English), filter and click to copy. Built-in dataset, free, browser-only."),
    ("it/latex", "LaTeX Symbol & Command Cheat Sheet",
     "LaTeX Symbol & Command Cheat Sheet - Search common LaTeX math symbols and commands, see the notation and click to copy. Free, browser-only."),
]

def insert_lines(path, make_line):
    t = io.open(path, encoding="utf-8").read()
    new = []
    for slug, en, ed in BATCH:
        if ('"%s"' % slug) in t:
            print("  skip (exists):", slug); continue
        new.append(make_line(slug, en, ed))
    if not new:
        print("  nothing to add in", os.path.basename(path)); return
    nl = t.index("\n", t.index("{")) + 1
    inserted = "".join(line + "\n" for line in new)
    t = t[:nl] + inserted + t[nl:]
    io.open(path, "w", encoding="utf-8").write(t)
    print("  added %d entries ->" % len(new), os.path.basename(path))

ov = os.path.join(ROOT, "i18n", "tools", "_en_override.json")
sl = os.path.join(ROOT, "i18n", "tools", "slug-en.json")

insert_lines(ov, lambda s, en, ed: '"%s":{"en":"%s","ed":"%s","ind":"%s"},' % (s, en, ed, s.split("/")[0]))
insert_lines(sl, lambda s, en, ed: '"%s":{"en":"%s","ed":"%s"},' % (s, en, ed))

for p in (ov, sl):
    json.load(io.open(p, encoding="utf-8"))
    assert "},," not in io.open(p, encoding="utf-8").read(), p
    print("  JSON valid:", os.path.basename(p))
