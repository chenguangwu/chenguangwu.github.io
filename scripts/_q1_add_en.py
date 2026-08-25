#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Q1 批次01 英文同步：向 slug-en.json 与 _en_override.json 顶部插入 6 个新工具的高质量语义化英文。
保持其余格式不变（仅在开头 { 后插入），避免重刷整个 i18n 文件。
"""
import json, io

NEW = {
    "design/px-to-rem": {"en": "Px to Rem Converter",
        "ed": "Px to Rem Converter - Convert pixel values to rem with a customizable root font size. Free, instant, browser-only."},
    "design/rem-to-px": {"en": "Rem to Px Converter",
        "ed": "Rem to Px Converter - Convert rem units back to pixels using the root font size. Free, instant, browser-only."},
    "design/flexbox-generator": {"en": "Flexbox Layout Generator",
        "ed": "Flexbox Layout Generator - Visually build display:flex CSS with live preview and copy-ready code. Free, instant, browser-only."},
    "design/vh-vw": {"en": "Viewport Unit Converter (vw/vh)",
        "ed": "Viewport Unit Converter - Convert between vw/vh and px by viewport width or height. Free, instant, browser-only."},
    "it/text-to-ascii": {"en": "Text to ASCII Converter",
        "ed": "Text to ASCII Converter - Show decimal, hex and 8-bit binary for each character. Free, instant, browser-only."},
    "it/text-to-unicode": {"en": "Text to Unicode Codepoint",
        "ed": "Text to Unicode Codepoint - Show the U+ codepoint and UTF-16 escape for every character including CJK and emoji. Free, instant, browser-only."},
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
    # validate
    json.loads(new_s)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_s)
    print("updated", path)

insert_after_brace("i18n/tools/slug-en.json", with_ind=False)
insert_after_brace("i18n/tools/_en_override.json", with_ind=True)
print("OK")
