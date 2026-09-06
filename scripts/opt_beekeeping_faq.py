# -*- coding: utf-8 -*-
"""为 beekeeping 分类每个工具页注入真实 FAQPage 结构化数据（负向后顾注入文档级 </body>）。"""
import json, os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAT = "beekeeping"

def build_ldqa(e):
    main = []
    for it in e.get("faqs", []):
        main.append({
            "@type": "Question",
            "name": it.get("q", ""),
            "acceptedAnswer": {"@type": "Answer", "text": it.get("a", "")}
        })
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": main
    }

def main():
    with open(os.path.join(ROOT, "i18n", "tools", "content_deepdive.json"), encoding="utf-8") as f:
        data = json.load(f)
    files = sorted(glob.glob(os.path.join(ROOT, "tools", CAT, "*.html")))
    ok = 0
    for f in files:
        if f.endswith("index.html"):
            continue
        base = os.path.basename(f)[:-5]
        key = "%s/%s" % (CAT, base)
        if key not in data:
            continue
        entry = data[key]
        if not entry.get("faqs"):
            continue
        ld = build_ldqa(entry)
        ld_str = json.dumps(ld, ensure_ascii=False)
        s = open(f, encoding="utf-8").read()
        # 删除已有 FAQPage LD（避免重复）
        s = re.sub(r'<script type="application/ld\+json"[^>]*>\{?[^\n]*"@type"\s*:\s*"FAQPage".*?</script>', "", s, flags=re.S)
        # 负向后顾：在文档级 </body> 前注入
        if "</body>" in s:
            block = '<script type="application/ld+json">%s</script>\n</body>' % ld_str
            s = s.replace("</body>", block, 1)
            open(f, "w", encoding="utf-8").write(s)
            ok += 1
            print("OK", base)
        else:
            print("SKIP no </body>:", base)
    print("beekeeping FAQPage LD injected:", ok)

if __name__ == "__main__":
    main()
