#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Q1 三期（gen_q1g）英文同步：向 i18n/tools/slug-en.json（卡片名）与 i18n/tools/_en_override.json
（嵌套 {en,ed,ind}）插入 13 个工具的高质量语义化英文。采用「在 { 后插入」范式。
注意：_en_override.json 的值必须是 dict {en,ed,ind}，否则 _build.py 的 apply_en_override 会报 AttributeError。
"""
import json

NEW = {
    "it/xml-validator": {"en": "XML Validator",
        "ed": "XML Validator - Check XML for well-formedness: tag pairing, quoted attributes and illegal characters, with error location. Free, browser-only."},
    "it/csv-validator": {"en": "CSV Validator",
        "ed": "CSV Validator - Verify column counts are consistent, quotes are balanced and fields are non-empty, flagging bad rows. Free, browser-only."},
    "it/css-minify": {"en": "CSS Minifier",
        "ed": "CSS Minifier - Strip comments and redundant whitespace to shrink CSS for faster loads, preserving semantics. Free, browser-only."},
    "it/js-minify": {"en": "JS Minifier",
        "ed": "JS Minifier - Remove comments and extra whitespace from JavaScript for a quick size reduction, without renaming variables. Free, browser-only."},
    "it/markdown-lint": {"en": "Markdown Linter",
        "ed": "Markdown Linter - Check heading levels, list formatting, link syntax and duplicate headings, with fix suggestions. Free, browser-only."},
    "it/hash-identifier": {"en": "Hash Identifier",
        "ed": "Hash Identifier - Guess the algorithm (MD5/SHA1/SHA256/SHA512/BCrypt) from a hash length, charset and known prefix. Free, browser-only."},
    "it/gitignore-generator": {"en": ".gitignore Generator",
        "ed": ".gitignore Generator - Pick stacks (Python/Node/Go/Rust/Java/.NET/IDE) and merge a ready .gitignore file. Free, browser-only."},
    "it/dockerfile-generator": {"en": "Dockerfile Generator",
        "ed": "Dockerfile Generator - Choose base image, exposed port and start command to produce a usable Dockerfile. Free, browser-only."},
    "it/sitemap-generator": {"en": "Sitemap Generator",
        "ed": "Sitemap Generator - Paste one URL per line to build a standard sitemap.xml with lastmod for search engines. Free, browser-only."},
    "design/color-blindness-sim": {"en": "Color Blindness Simulator",
        "ed": "Color Blindness Simulator - Approximate how a color looks under protanopia, deuteranopia or tritanopia to check accessibility. Free, browser-only."},
    "it/nginx-config-generator": {"en": "Nginx Config Generator",
        "ed": "Nginx Config Generator - Pick static site or reverse proxy and fill params to emit a server block config. Free, browser-only."},
    "it/kubernetes-yaml-generator": {"en": "Kubernetes YAML Generator",
        "ed": "Kubernetes YAML Generator - Enter name, image, port and replicas to produce a Deployment plus Service manifest. Free, browser-only."},
    "it/meta-tags-generator": {"en": "Meta Tags Generator",
        "ed": "Meta Tags Generator - Generate SEO and social share (Open Graph / Twitter Card) meta tags from title, description, URL and image. Free, browser-only."},
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


if __name__ == "__main__":
    insert_after_brace("i18n/tools/slug-en.json", with_ind=False)
    insert_after_brace("i18n/tools/_en_override.json", with_ind=True)
    print("OK")
