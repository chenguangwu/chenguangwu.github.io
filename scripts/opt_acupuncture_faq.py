# -*- coding: utf-8 -*-
"""acupuncture 23 工具：删旧套话 FAQPage LD + 注入真实 FAQPage LD。

纪律：
- 旧套话 FAQPage LD 必须先行删除，否则注入幂等判断 if 'FAQPage' in s 会跳过。
- 真实 FAQPage LD 从 content_deepdive.json 的 faqs 生成（与 deep-dive 真实 FAQ 一致）。
- 注入位置必须用负向后顾只匹配【文档级】</body>（排除 JS 字符串字面量内的同名标签），
  避免把 JSON 塞进函数 <script> 块导致计算回归门禁挂。
- 标题保持纯工具名（不加"免费"、不加"- ToolBox"），本脚本不改动任何 title。
"""
import json, os, re, sys

ROOT = "tools/acupuncture"
CD = json.load(open("i18n/tools/content_deepdive.json", encoding="utf-8"))

# 匹配所有 application/ld+json 块（JSON 内不含 </script>，块独立）
LD_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.DOTALL)
FAQ_MARK = re.compile(r'"@type"\s*:\s*"FAQPage"')
# 文档级 </body> 负向后顾
BODY_RE = re.compile(r"(?<!['\"\w])</body>")


def build_faq_ld(faqs):
    obj = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": qa["q"],
             "acceptedAnswer": {"@type": "Answer", "text": qa["a"]}}
            for qa in faqs
        ],
    }
    return obj


def process(path, slug, dry):
    s = open(path, encoding="utf-8").read()
    base = "acupuncture/" + slug
    faqs = (CD.get(base) or {}).get("faqs") or []
    if not faqs:
        print("  [WARN] no faqs for", base)
        return

    report = []

    # 1) 删除含 FAQPage 的旧 ld+json 块
    old_blocks = [m.group(0) for m in LD_RE.finditer(s) if FAQ_MARK.search(m.group(1))]
    if old_blocks:
        for blk in old_blocks:
            s = s.replace(blk, "")
        report.append("del-old-faq-ld x%d" % len(old_blocks))

    # 2) 注入真实 FAQPage LD 到文档级 </body> 前
    if 'FAQPage' not in s:
        ld_obj = build_faq_ld(faqs)
        ld_json = json.dumps(ld_obj, ensure_ascii=False)
        json.loads(ld_json)  # 自测合法
        ld_block = '<script type="application/ld+json">\n' + ld_json + '\n</script>'
        new_s, n = BODY_RE.subn(ld_block + '\n</body>', s, count=1)
        if n != 1:
            raise RuntimeError("body inject count=%d in %s" % (n, path))
        s = new_s
        report.append("inject-faq-ld(%d qa)" % len(faqs))
    else:
        report.append("FAQPage already present (skip)")

    if dry:
        print("DRY", slug, "->", ", ".join(report))
        return
    open(path, "w", encoding="utf-8").write(s)
    print("OK ", slug, "->", ", ".join(report))


def main():
    dry = "--dry" in sys.argv
    files = [f for f in os.listdir(ROOT) if f.endswith(".html") and f != "index.html"]
    files.sort()
    print("processing %d acupuncture tools (dry=%s)" % (len(files), dry))
    for f in files:
        slug = f[:-5]
        process(os.path.join(ROOT, f), slug, dry)


if __name__ == "__main__":
    main()
