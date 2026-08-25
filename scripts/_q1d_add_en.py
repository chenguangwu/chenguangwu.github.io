#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Q1 批次 04 英文注入：写入 _en_override.json + slug-en.json（键 it/<slug>，尾部插入，幂等）。
用法：python3 scripts/_q1d_add_en.py
"""
import os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OV = os.path.join(ROOT, "i18n", "tools", "_en_override.json")
SL = os.path.join(ROOT, "i18n", "tools", "slug-en.json")

ENTRIES = [
    ("it/xml-to-yaml",
     {"en": "XML to YAML Converter",
      "ed": "XML to YAML Converter - Paste XML and convert it to YAML (attributes as @key, text as #text). Free, browser-only."}),
    ("it/yaml-to-xml",
     {"en": "YAML to XML Converter",
      "ed": "YAML to XML Converter - Paste YAML and convert it to XML (@key as attribute, #text as element text). Free, browser-only."}),
    ("it/xml-to-toml",
     {"en": "XML to TOML Converter",
      "ed": "XML to TOML Converter - Paste XML and convert it to TOML (attributes as @key). Free, browser-only."}),
    ("it/toml-to-xml",
     {"en": "TOML to XML Converter",
      "ed": "TOML to XML Converter - Paste TOML and convert it to XML (@key as attribute). Free, browser-only."}),
    ("it/random-string",
     {"en": "Random String Generator",
      "ed": "Random String Generator - Generate secure random strings with custom length and character sets (upper/lower/digit/symbol), batch output and one-click copy. Uses crypto.getRandomValues."}),
    ("it/whitespace",
     {"en": "Text Whitespace Cleaner",
      "ed": "Text Whitespace Cleaner - Trim line ends, remove blank lines, collapse spaces and normalize trailing newline. Pure client-side."}),
]


def insert_tail(path, entries):
    s = open(path, "r", encoding="utf-8").read()
    existing = json.loads(s)  # validate
    added = 0
    blocks = []
    for k, v in entries:
        if k in existing:
            continue
        obj = dict(v)
        if path.endswith("_en_override.json"):
            obj["ind"] = k.split("/")[0]
        blocks.append('"%s":%s' % (k, json.dumps(obj, ensure_ascii=False)))
        added += 1
    if not blocks:
        print("  (skip) %s 已含全部条目" % os.path.basename(path))
        return 0
    ins = ",\n".join(blocks)
    i = s.rfind("}")
    s = s[:i] + ",\n" + ins + "\n" + s[i:]
    json.loads(s)  # validate after insert
    open(path, "w", encoding="utf-8").write(s)
    print("  + %s 插入 %d 条" % (os.path.basename(path), added))
    return added


if __name__ == "__main__":
    print("写入 _en_override.json ...")
    insert_tail(OV, ENTRIES)
    print("写入 slug-en.json ...")
    insert_tail(SL, ENTRIES)
    print("完成")
