# -*- coding: utf-8 -*-
"""为 beauty 分类 21 个工具注入真实 FAQPage 结构化数据（负向后顾注入文档级 </body>）。"""
import json, os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CD = os.path.join(ROOT, "i18n", "tools", "content_deepdive.json")

def main():
    data = json.load(open(CD, encoding="utf-8"))
    files = sorted(f for f in glob.glob(os.path.join(ROOT, "tools", "beauty", "*.html"))
                   if not f.endswith("index.html"))
    ok = 0
    for f in files:
        base = os.path.basename(f)[:-5]
        key = "beauty/" + base
        if key not in data:
            print("SKIP no content key:", base)
            continue
        faqs = data[key].get("faqs", [])
        if not faqs:
            print("SKIP no faqs:", base)
            continue
        faqpage = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q["q"],
                 "acceptedAnswer": {"@type": "Answer", "text": q["a"]}}
                for q in faqs
            ],
        }
        s = open(f, encoding="utf-8").read()
        # 删除旧 FAQPage LD（若有）
        s = re.sub(r'<script type="application/ld\+json"[^>]*>\s*\{\s*"@context"\s*:\s*"https://schema\.org".*?"@type"\s*:\s*"FAQPage".*?</script>\s*', "", s, flags=re.S)
        block = '\n<script type="application/ld+json">\n' + json.dumps(faqpage, ensure_ascii=False, indent=2) + "\n</script>"
        if "</body>" in s:
            s = s.replace("</body>", block + "\n</body>", 1)
        else:
            s = s + block + "\n"
        open(f, "w", encoding="utf-8").write(s)
        ok += 1
        print("OK", base)
    print("beauty FAQPage injected:", ok)

if __name__ == "__main__":
    main()
