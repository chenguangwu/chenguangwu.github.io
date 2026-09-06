# -*- coding: utf-8 -*-
"""beneficiation 分类 FAQPage 结构化数据注入（先删旧 LD，负向后顾注入文档级 </body>）。"""
import os, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools", "beneficiation")
CAT = "beneficiation"

LD_RE = re.compile(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', re.S)


def main():
    data = json.load(open(os.path.join(ROOT, "i18n", "tools", "content_deepdive.json"), encoding="utf-8"))
    files = sorted(f for f in os.listdir(TOOLS_DIR) if f.endswith(".html") and f != "index.html")
    n_ok = 0
    for fn in files:
        base = fn[:-5]
        key = "%s/%s" % (CAT, base)
        if key not in data:
            print("SKIP no content key:", key); continue
        e = data[key]
        faqs = e.get("faqs", [])
        if not faqs:
            print("SKIP no faqs:", key); continue
        ld = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}}
                for q in faqs
            ],
        }
        ld_str = json.dumps(ld, ensure_ascii=False)
        block = '<script type="application/ld+json">%s</script>' % ld_str
        path = os.path.join(TOOLS_DIR, fn)
        s = open(path, encoding="utf-8").read()
        # 删掉该文件所有旧 FAQPage LD
        s2 = LD_RE.sub(lambda m: "", s)
        # 负向后顾：注入到文档级 </body> 之前
        if "</body>" in s2:
            s2 = s2.replace("</body>", block + "\n</body>", 1)
        else:
            s2 = s2 + block
        open(path, "w", encoding="utf-8").write(s2)
        n_ok += 1
        print("OK", key)
    print("beneficiation FAQPage LD injected:", n_ok)


if __name__ == "__main__":
    main()
