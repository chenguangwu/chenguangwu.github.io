#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Q1 一期（gen_q1e）英文同步：向 slug-en.json 与 _en_override.json 顶部插入 13 个新工具的高质量语义化英文。
保持其余格式不变（仅在开头 { 后插入），避免重刷整个 i18n 文件。
"""
import json

NEW = {
    "it/roman-numeral-converter": {"en": "Roman Numeral Converter",
        "ed": "Roman Numeral Converter - Convert between Arabic numbers (1-3999) and Roman numerals with a live lookup table. Free, browser-only."},
    "it/mime-type-lookup": {"en": "MIME Type Lookup",
        "ed": "MIME Type Lookup - Map a file extension to its MIME type (e.g. json to application/json) or reverse. Free, browser-only."},
    "it/http-methods-reference": {"en": "HTTP Methods Reference",
        "ed": "HTTP Methods Reference - See GET/POST/PUT/PATCH/DELETE semantics, safe and idempotent flags, and typical uses. Free, browser-only."},
    "it/json-repair": {"en": "JSON Repairer",
        "ed": "JSON Repairer - Fix broken JSON (trailing commas, single quotes, comments) and validate it locally. Free, browser-only."},
    "text/text-to-braille": {"en": "Text to Braille",
        "ed": "Text to Braille - Convert letters, digits and punctuation to Unicode Braille (U+2800). Free, browser-only."},
    "text/text-to-1337": {"en": "Text to Leet Speak",
        "ed": "Text to Leet Speak - Turn text into 1337 with low, medium and high substitution levels. Free, browser-only."},
    "encode/binary-to-ascii": {"en": "Binary / Hex to ASCII",
        "ed": "Binary / Hex to ASCII - Decode 8-bit binary or 2-digit hex groups back to readable text. Free, browser-only."},
    "text/text-to-ascii-art": {"en": "Text to ASCII Art",
        "ed": "Text to ASCII Art - Render A-Z and 0-9 as 5x5 pixel banner text for terminals and READMEs. Free, browser-only."},
    "it/triangle-calculator": {"en": "Triangle Calculator",
        "ed": "Triangle Calculator - Compute perimeter, area (Heron) and angles from three sides, with type detection. Free, browser-only."},
    "it/prime-checker": {"en": "Prime Number Checker",
        "ed": "Prime Number Checker - Test if a number is prime and factor composites locally. Free, browser-only."},
    "design/color-shade-generator": {"en": "Color Shade Generator",
        "ed": "Color Shade Generator - Produce tint and shade ramps from a base HEX color for UI palettes. Free, browser-only."},
    "it/ipv4-range-expander": {"en": "IPv4 Range Expander",
        "ed": "IPv4 Range Expander - Expand a CIDR into network, broadcast, usable host count and range. Free, browser-only."},
    "it/ipv6-converter": {"en": "IPv6 Address Converter",
        "ed": "IPv6 Address Converter - Switch between compressed (::) and full 8-group IPv6 forms. Free, browser-only."},
}

def insert_after_brace(path, with_ind=False):
    with open(path, encoding="utf-8") as f:
        s = f.read()
    parts = []
    for k, v in NEW.items():
        v2 = dict(v)
        if with_ind:
            v2["ind"] = k.split("/")[0]
        parts.append('"%s":%s' % (k, json.dumps(v2, ensure_ascii=False, separators=(",", ":"))))
    block = ",\n".join(parts)
    idx = s.index("{") + 1
    new_s = s[:idx] + "\n" + block + ",\n" + s[idx:]
    json.loads(new_s)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_s)
    print("updated", path)

insert_after_brace("i18n/tools/slug-en.json", with_ind=False)
insert_after_brace("i18n/tools/_en_override.json", with_ind=True)
print("OK")
