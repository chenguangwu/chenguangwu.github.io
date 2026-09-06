# -*- coding: utf-8 -*-
"""为 baking 分类 9 个工具页注入真实 FAQPage 结构化数据（负向后顾注入文档级 </body>）。"""
import os, re, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CD = json.load(open(os.path.join(ROOT, "i18n", "tools", "content_deepdive.json"), encoding="utf-8"))

TOOLS_DIR = os.path.join(ROOT, "tools", "baking")

LD_RE = re.compile(r'<script type="application/ld\+json"[^>]*class="faq-[^"]*"[^>]*>.*?</script>', re.S)
HEAD = '<script type="application/ld+json" class="faq-page-ld">'
TAIL = '</script>'

def build_ld(faqs):
    obj = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in [(x["q"], x["a"]) for x in faqs]
        ],
    }
    return HEAD + json.dumps(obj, ensure_ascii=False) + TAIL

def main():
    files = sorted(f for f in glob.glob(os.path.join(TOOLS_DIR, "*.html")) if not f.endswith("index.html"))
    ok = 0
    for f in files:
        base = os.path.basename(f)[:-5]
        key = "baking/" + base
        if key not in CD:
            print("SKIP no key:", base)
            continue
        faqs = CD[key].get("faqs", [])
        if len(faqs) < 1:
            print("SKIP no faqs:", base)
            continue
        s = open(f, encoding="utf-8").read()
        s = LD_RE.sub("", s)  # 删旧
        block = "\n" + build_ld(faqs) + "\n</body>"
        s = re.sub(r"</body>", block, s, count=1)
        open(f, "w", encoding="utf-8").write(s)
        ok += 1
        print("OK", base, "faqs=%d" % len(faqs))
    print("baking FAQPage LD injected:", ok)

if __name__ == "__main__":
    main()
