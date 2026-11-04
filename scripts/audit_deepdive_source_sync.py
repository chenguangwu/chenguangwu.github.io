#!/usr/bin/env python3
"""deep-dive 源头同步门禁：页面 deep-dive 段 vs i18n/tools/content_deepdive.json

背景（2026-11-05 事故）：
  `_build.py` 会用 content_deepdive.json 重建工具页的 deep-dive 段（见 _build.py
  「内容深度块」注入逻辑）。如果只改页面、不改 JSON，下一次 `_build.py`（提交前必跑）
  就会把页面级修复整段回退——没有报错、没有告警。svg-to-png 的 FAQ、hematology 四页
  的分值纠正都踩过这个坑。

本脚本把「页面与源头不一致」变成红灯：任何 deep-dive 文案改动必须页面与 JSON 同一批提交，
且 JSON 保持仓库规范 indent=1。

用法：
  python3 scripts/audit_deepdive_source_sync.py --check    # 判红（门禁用）
  python3 scripts/audit_deepdive_source_sync.py --report   # 只列不判红（人工排查）

比对口径（与 4726 条普查一致）：
  1. HTML 实体连续解码（最多 3 次），使 `&lt;` / `&gt;` / `&lt;p&gt;` 与 JSON 原文同形；
  2. 块级标签替换为空格、其余真标签剥除（保留标签内文本）；
  3. 折叠连续空白、去首尾空白后逐字比对。
  真标签判定必须要求标签名后紧跟空白 / `/` / `>`，否则 `P(Z<z)` 里的 `<z)`
  会被误当成标签整块吞掉（statistics/z 曾因此误报）。
"""
import argparse
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DD_PATH = os.path.join(ROOT, "i18n", "tools", "content_deepdive.json")
TOOLS_DIR = os.path.join(ROOT, "tools")
SNIPPET = 200

# 真标签：标签名后必须是空白 / `/` / `>`（避免把 `P(Z<z)` 的 `<z)` 当标签）
TAG_RE = re.compile(r"</?([A-Za-z][A-Za-z0-9]*)(?:\s[^>]*)?/?>")
BLOCK_RE = re.compile(
    r"</?(?:p|div|br|li|ul|ol|dl|dt|dd|h[1-6]|section|table|thead|tbody|tr|td|th)"
    r"(?:\s[^>]*)?/?>",
    re.I,
)
SECTION_START_RE = re.compile(r'<section class="deep-dive"')
SECTION_TAG_RE = re.compile(r"<section\b|</section>")
TITLE_RE = re.compile(r"<h2>📚 深度解析：(.*?)</h2>", re.S)
LIST_RE = re.compile(r'<ul class="dd-list">(.*?)</ul>', re.S)
LI_RE = re.compile(r"<li>(.*?)</li>", re.S)
EXAMPLE_RE = re.compile(
    r'<div class="dd-example"><div class="dd-ex-title">(.*?)</div>'
    r'<div class="dd-ex-body">(.*?)</div></div>',
    re.S,
)
FAQ_RE = re.compile(r'<dl class="dd-faq">(.*?)</dl>', re.S)
FAQ_ITEM_RE = re.compile(r"<dt>(.*?)</dt><dd>(.*?)</dd>", re.S)


def norm(value):
    """归一化：解码实体 → 剥标签（保留文本）→ 折叠空白。"""
    text = "" if value is None else str(value)
    for _ in range(3):
        decoded = html.unescape(text)
        if decoded == text:
            break
        text = decoded
    text = BLOCK_RE.sub(" ", text)
    text = TAG_RE.sub("", text)
    text = re.sub(r"[\s\u00a0]+", " ", text)
    return text.strip()


def clip(text):
    text = text or ""
    return text if len(text) <= SNIPPET else text[:SNIPPET] + "…"


def find_section(raw):
    """按 <section> 配平取出 deep-dive 段，取不到返回 None。"""
    match = SECTION_START_RE.search(raw)
    if not match:
        return None
    start = match.start()
    depth = 0
    for tag in SECTION_TAG_RE.finditer(raw, start):
        if tag.group(0).startswith("</"):
            depth -= 1
            if depth == 0:
                return raw[start:tag.end()]
        else:
            depth += 1
    return raw[start:]


def extract_page(raw):
    """提取页面 deep-dive 四类字段（归一化后）。无该段返回 None。"""
    section = find_section(raw)
    if section is None:
        return None
    title_match = TITLE_RE.search(section)
    title = norm(title_match.group(1)) if title_match else ""
    scenarios = []
    list_match = LIST_RE.search(section)
    if list_match:
        scenarios = [norm(x) for x in LI_RE.findall(list_match.group(1))]
    examples = []
    for item in EXAMPLE_RE.finditer(section):
        examples.append({"title": norm(item.group(1)), "body": norm(item.group(2))})
    faqs = []
    faq_match = FAQ_RE.search(section)
    if faq_match:
        faqs = [{"q": norm(q), "a": norm(a)} for q, a in FAQ_ITEM_RE.findall(faq_match.group(1))]
    return {"title": title, "scenarios": scenarios, "examples": examples, "faqs": faqs}


def extract_json(entry):
    return {
        "title": norm(entry.get("title")),
        "scenarios": [norm(x) for x in (entry.get("scenarios") or [])],
        "examples": [
            {"title": norm(e.get("title")), "body": norm(e.get("body"))}
            for e in (entry.get("examples") or [])
        ],
        "faqs": [
            {"q": norm(f.get("q")), "a": norm(f.get("a"))}
            for f in (entry.get("faqs") or [])
        ],
    }


def item_text(item):
    """把 scenarios 字符串 / examples(title,body) / faqs(q,a) 统一成一行展示文本。"""
    if isinstance(item, dict):
        return "｜".join(str(item.get(k, "")) for k in ("title", "body", "q", "a") if item.get(k))
    return str(item)


def diff_items(field, page_val, json_val):
    """返回 (页面侧片段, JSON 侧片段) 列表，最多 3 组；按下标配对，便于看出改前/改后。"""
    if field == "title":
        # 调用方按 (页面侧, JSON 侧) 二元组格式化；字段名已在 issues 头部打印。
        return [(clip(page_val), clip(json_val))]
    page_list = page_val if isinstance(page_val, list) else []
    json_list = json_val if isinstance(json_val, list) else []
    rows = []
    for idx in range(max(len(page_list), len(json_list))):
        page_item = page_list[idx] if idx < len(page_list) else None
        json_item = json_list[idx] if idx < len(json_list) else None
        if page_item == json_item:
            continue
        rows.append((
            "" if page_item is None else item_text(page_item),
            "" if json_item is None else item_text(json_item),
        ))
        if len(rows) >= 3:
            break
    return [(clip(a), clip(b)) for a, b in rows]


def audit(report_only=False):
    with open(DD_PATH, encoding="utf-8") as fh:
        entries = json.load(fh)

    scanned = skipped = 0
    issues = []
    for key in sorted(entries):
        page_path = os.path.join(TOOLS_DIR, key + ".html")
        if not os.path.exists(page_path):
            skipped += 1
            continue
        scanned += 1
        with open(page_path, encoding="utf-8", errors="ignore") as fh:
            raw = fh.read()
        page = extract_page(raw)
        if page is None:
            issues.append((key, "deep-dive", ["页面缺整段 deep-dive（构建会按 JSON 注入）"]))
            continue
        expected = extract_json(entries[key])
        for field in ("title", "scenarios", "examples", "faqs"):
            if page[field] != expected[field]:
                rows = diff_items(field, page[field], expected[field])
                issues.append((key, field, [f"页面: {a}\n      JSON: {b}" for a, b in rows]))

    for key, field, rows in issues:
        print(f"❌ {key} | 差异字段: {field}")
        for row in rows:
            print(f"      {row}")
    print(f"\n[deepdive] 扫描 {scanned} 页，跳过无页面 {skipped} 条，不一致 {len(issues)} 页")

    if issues:
        print("提示：改页面 deep-dive/FAQ 必须同批改 i18n/tools/content_deepdive.json（indent=1），"
              "否则下次 _build.py 会整段回退。")
    if report_only:
        return 0
    return 1 if issues else 0


def main():
    parser = argparse.ArgumentParser(description="deep-dive 页面与 content_deepdive.json 同步检查")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="不一致时 exit 1（默认，门禁用）")
    mode.add_argument("--report", action="store_true", help="只列出差异，不判红")
    args = parser.parse_args()
    return audit(report_only=args.report)


if __name__ == "__main__":
    sys.exit(main())
