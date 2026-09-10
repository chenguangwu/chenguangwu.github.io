#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""通用：把工具页源 html 的旧 FAQPage JSON-LD 同步为 content_deepdive 的真实 FAQ。

背景：早期 opt_content.py 在工具页手写了一段 FAQPage ld+json，内容是通用套话
（"X 是做什么的？""如何使用 X？在对应的输入框或选项中填写…""计算结果准确吗？"）。
这段 LD _build.py 不会重建（构建只重建 deep-dive 可见区块），因此是遗留套话；
同时它会与 deep-dive 注入的真实 FAQ 发出不一致的结构化信号。

本脚本用 content_deepdive 的 faqs 覆盖它，使结构化数据与页面真实 FAQ 一致。

用法:
    python3 scripts/opt_faq_ld_sync.py --cat mechanical          # 整个分类
    python3 scripts/opt_faq_ld_sync.py --cat mechanical --dry    # 只报数
    python3 scripts/opt_faq_ld_sync.py --files a.html b.html
"""
import re, glob, os, sys, json

DATA = "i18n/tools/content_deepdive.json"
LD_RE = re.compile(
    r'(<script type="application/ld\+json">\s*)(\{.*?"@type"\s*:\s*"FAQPage".*?\})(\s*</script>)',
    re.S,
)
CLICHE = ("在对应的输入框或选项中填写", "工作与生活中的相关计算", "点击「计算」或「生成」按钮")


def build_ld(faqs):
    entity = []
    for f in faqs:
        q = (f.get("q") or "").strip()
        a = (f.get("a") or "").strip()
        if not q or not a:
            continue
        entity.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        })
    if not entity:
        return None
    return json.dumps(
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entity},
        ensure_ascii=False,
    )


def main():
    args = sys.argv[1:]
    dry = "--dry" in args
    if "--cat" in args:
        cat = args[args.index("--cat") + 1]
        files = [f for f in glob.glob("tools/%s/*.html" % cat) if not f.endswith("index.html")]
    elif "--files" in args:
        i = args.index("--files") + 1
        files = [a for a in args[i:] if not a.startswith("--")]
    else:
        print("需要 --cat <分类> 或 --files <文件...>")
        return 1

    data = json.load(open(DATA, encoding="utf-8"))
    done = skipped = 0
    for f in sorted(files):
        t = open(f, encoding="utf-8").read()
        m = LD_RE.search(t)
        if not m:
            continue
        old = m.group(2)
        if not any(c in old for c in CLICHE):
            skipped += 1          # 已是真实内容，跳过
            continue
        slug = "%s/%s" % (f.split("/")[-2], os.path.basename(f)[:-5])
        e = data.get(slug)
        faqs = (e or {}).get("faqs") or []
        new = build_ld(faqs)
        if new is None:
            print("NO FAQ for", slug)
            continue
        t = t[:m.start(2)] + new + t[m.end(2):]
        if not dry:
            open(f, "w", encoding="utf-8").write(t)
        done += 1
        print("  %-46s FAQ %d 条已同步" % (f, len(faqs)))
    print("同步 %d 个文件，跳过(已真实) %d 个%s" % (done, skipped, "（dry-run 未落盘）" if dry else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
