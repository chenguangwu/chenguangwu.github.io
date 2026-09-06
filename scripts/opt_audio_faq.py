#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audio 分类 FAQPage 结构化数据注入（三处清理之一：JSON-LD）。"""
import os, re, json, sys

ROOT = "tools/audio"
DATA = "i18n/tools/content_deepdive.json"
data = json.load(open(DATA, encoding="utf-8"))


def _has_faq(obj):
    if isinstance(obj, dict):
        t = obj.get("@type")
        if t == "FAQPage" or (isinstance(t, list) and "FAQPage" in t):
            return True
        return any(_has_faq(v) for v in obj.values())
    if isinstance(obj, list):
        return any(_has_faq(x) for x in obj)
    return False


def strip_old_faq(s):
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
        key = "audio/" + base
        s2, removed = strip_old_faq(s)
        ld = build_faq_ld(key)
        if ld is None:
            print("SKIP (no faqs):", f)
            continue
        ld_s = json.dumps(ld, ensure_ascii=False, indent=2)
        script = '<script type="application/ld+json">\n%s\n</script>' % ld_s
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
