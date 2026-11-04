#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""通用：把工具页源 html 的旧 FAQPage JSON-LD 同步为 content_deepdive 的真实 FAQ。

背景：早期 opt_content.py 在工具页手写了一段 FAQPage ld+json，内容是通用套话
（"X 是做什么的？""如何使用 X？在对应的输入框或选项中填写…""计算结果准确吗？"）。
这段 LD _build.py 不会重建（构建只重建 deep-dive 可见区块），因此是遗留套话；
同时它会与 deep-dive 注入的真实 FAQ 发出不一致的结构化信号。

本脚本用 content_deepdive 的 faqs 覆盖它，使结构化数据与页面真实 FAQ 一致。

⚠ 2026-11-04 修复：旧实现用整页正则
`(<script …ld+json>\s*)(\{.*?"@type":"FAQPage".*?\})(</script>)`，
`.*?`（含换行）会从**本页第一个** ld+json 块的 `{` 一路跨到 FAQPage 块的 `}`，
把中间的 WebApplication LD、TOOLBOX-SECURITY meta、privacy/metrics/i18n/nav
脚本、hreflang 整段吞掉（实测 heat-stress-index.html 少 47 行）。
现改为**逐块**匹配 `<script type="application/ld+json">…</script>`，
每块单独 json.loads，只替换 `@type=="FAQPage"` 那一块，其余块字节原样保留。

用法:
    python3 scripts/opt_faq_ld_sync.py --cat mechanical             # 默认 dry-run
    python3 scripts/opt_faq_ld_sync.py --cat mechanical --apply     # 真正写盘
    python3 scripts/opt_faq_ld_sync.py --files a.html b.html --apply
"""
import re, glob, os, sys, json

DATA = "i18n/tools/content_deepdive.json"

# 逐块匹配，禁止跨块（`.*?` 只在单块内部展开）
LD_BLOCK_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)

# 落盘前后的结构自检项：任一数量变化即中止（说明改动了 LD 之外的结构）
GUARDS = (
    '<script type="application/ld+json">',
    '<meta name="toolbox"',
    'TOOLBOX-SECURITY',
    'js/privacy.js',
    'js/i18n.js',
    'hreflang',
)

CLICHE = ("在对应的输入框或选项中填写", "工作与生活中的相关计算", "点击「计算」或「生成」按钮")


def build_ld(faqs, pretty=False):
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
        indent=1 if pretty else None,
    )


def guard_counts(text):
    return {k: text.count(k) for k in GUARDS}


def rewrite_file(text, faqs):
    """只替换 FAQPage 那一个块的内容，其余字节原样保留。
    返回 (新文本, 是否有改动, 被替换块是否为多行排版)。"""
    hit = [False]
    pretty = [False]

    def repl(m):
        inner = m.group(1)
        try:
            j = json.loads(inner)
        except Exception:
            return m.group(0)          # 解析不了的块一律不碰
        if not isinstance(j, dict) or j.get("@type") != "FAQPage":
            return m.group(0)          # 非 FAQPage 块字节原样保留
        if not any(c in inner for c in CLICHE):
            return m.group(0)          # 已是真实内容
        hit[0] = True
        is_pretty = "\n" in inner.strip()
        pretty[0] = is_pretty
        new_ld = build_ld(faqs, pretty=is_pretty)
        if new_ld is None:
            return m.group(0)
        # 保留原块首尾空白（单行块不动换行数；多行块按原风格缩进重排）
        lead = re.match(r"\s*", inner).group(0)
        trail = re.search(r"\s*$", inner).group(0)
        return '<script type="application/ld+json">' + lead + new_ld + trail + "</script>"

    return LD_BLOCK_RE.sub(repl, text), hit[0], pretty[0]


def main():
    args = sys.argv[1:]
    apply = "--apply" in args
    if "--cat" in args:
        cat = args[args.index("--cat") + 1]
        files = [f for f in glob.glob("tools/%s/*.html" % cat) if not f.endswith("index.html")]
    elif "--files" in args:
        i = args.index("--files") + 1
        files = [a for a in args[i:] if not a.startswith("--")]
    else:
        print("需要 --cat <分类> 或 --files <文件...>；默认 dry-run，写盘加 --apply")
        return 1

    data = json.load(open(DATA, encoding="utf-8"))
    writes = []
    done = skipped = 0
    for f in sorted(files):
        t = open(f, encoding="utf-8").read()
        slug = "%s/%s" % (f.replace(os.sep, "/").split("/")[-2], os.path.basename(f)[:-5])
        faqs = (data.get(slug) or {}).get("faqs") or []
        if build_ld(faqs) is None:
            if slug in data:
                print("NO FAQ for", slug)
            skipped += 1
            continue
        nt, changed, pretty = rewrite_file(t, faqs)
        if not changed:
            skipped += 1
            continue
        before, after = guard_counts(t), guard_counts(nt)
        diff = {k: (before[k], after[k]) for k in before if before[k] != after[k]}
        if diff:
            print("ABORT %s 结构计数变化: %s" % (f, diff))
            return 2
        if not pretty and nt.count("\n") != t.count("\n"):
            print("ABORT %s 单行 LD 块导致行数变化 %d → %d"
                  % (f, t.count("\n"), nt.count("\n")))
            return 2
        writes.append((f, t, nt, len(faqs)))
        done += 1
        print("  %-46s FAQ %d 条待同步" % (f, len(faqs)))

    if apply:
        for f, old, new, _ in writes:
            open(f, "w", encoding="utf-8").write(new)
    print("同步 %d 个文件，跳过(已真实/无 FAQ) %d 个%s"
          % (done, skipped, "" if apply else "（dry-run 未落盘，写盘加 --apply）"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
