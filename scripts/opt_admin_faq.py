#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""admin 分类 FAQPage 结构化数据注入。
- 删除 admin 所有 html 中【旧套话】FAQPage LD（含"工作与生活中的相关计算"等模板答案）。
- 从 i18n/tools/content_deepdive.json 的 faqs 生成【真实】FAQPage LD。
- 注入位置用负向后顾（只匹配文档级 </body>）排除 JS 字符串字面量内的同名标签，避免把 JSON 塞进函数 script 块。
- 标题保持纯工具名，本脚本不改动 <title>。
"""
import os, re, json, sys

ROOT = "tools/admin"
DATA = "i18n/tools/content_deepdive.json"

data = json.load(open(DATA, encoding="utf-8"))

OLD_FAQ_MARKERS = ("工作与生活中的相关计算", "在对应的输入框或选项中填写", "本校验工具")


def _has_faq(obj):
    """递归判定 JSON-LD 对象是否含 FAQPage。"""
    if isinstance(obj, dict):
        t = obj.get("@type")
        if t == "FAQPage" or (isinstance(t, list) and "FAQPage" in t):
            return True
        return any(_has_faq(v) for v in obj.values())
    if isinstance(obj, list):
        return any(_has_faq(x) for x in obj)
    return False


def strip_old_faq(s):
    """删除页面中已有的 FAQPage LD 整块（无论新旧，注入前先清空，保证幂等）。
    稳健方式：遍历所有 ld+json 块，解析 JSON 后递归判定是否含 FAQPage，是则整块删除。
    """
    pat = re.compile(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', re.S)
    removed = 0
    dels = []
    for m in pat.finditer(s):
        blk = m.group(1).strip()
        is_faq = False
        try:
            obj = json.loads(blk)
            is_faq = _has_faq(obj)
        except Exception:
            is_faq = False
        if is_faq:
            dels.append((m.start(), m.end()))
    for st, en in sorted(dels, reverse=True):
        s = s[:st] + s[en:]
        removed += 1
    return s, removed


def build_faq_ld(key):
    e = data.get(key)
    if not e:
        return None
    faqs = e.get("faqs") or []
    if not faqs:
        return None
    items = []
    for f in faqs:
        q = (f.get("q") or "").strip()
        a = (f.get("a") or "").strip()
        if not q or not a:
            continue
        items.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a}
        })
    if not items:
        return None
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": items
    }


def main():
    dry = "--dry" in sys.argv
    files = sorted([f for f in os.listdir(ROOT) if f.endswith(".html") and f != "index.html"])
    for f in files:
        path = os.path.join(ROOT, f)
        s = open(path, encoding="utf-8").read()
        base = f[:-5]
        key = "admin/" + base

        s2, removed = strip_old_faq(s)
        ld = build_faq_ld(key)
        if ld is None:
            print("SKIP (no faqs):", f)
            continue
        ld_s = json.dumps(ld, ensure_ascii=False, indent=2)
        script = '<script type="application/ld+json">\n%s\n</script>' % ld_s

        # 负向后顾：只匹配文档级 </body>
        m = re.search(r'(?<![\'"\w])</body>', s2)
        if not m:
            print("NO </body>:", f)
            continue
        new_s = s2[:m.start()] + script + "\n" + s2[m.start():]
        if dry:
            print("DRY %s: removed_old=%d injected=%d" % (f, removed, 1))
        else:
            open(path, "w", encoding="utf-8").write(new_s)
            print("OK %s: removed_old=%d injected=%d" % (f, removed, 1))


if __name__ == "__main__":
    main()
