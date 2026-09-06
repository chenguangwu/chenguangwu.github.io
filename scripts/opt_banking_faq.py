# -*- coding: utf-8 -*-
"""为 banking 分类 27 个工具注入真实 FAQPage 结构化数据（负向后顾文档级 </body>）。"""
import os, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools", "banking")
CONTENT = os.path.join(ROOT, "i18n", "tools", "content_deepdive.json")


def build_faq_ld(key):
    data = json.load(open(CONTENT, encoding="utf-8"))
    e = data.get(key)
    if not e or "faqs" not in e:
        return None
    main = []
    for f in e["faqs"]:
        q = f.get("q", "").strip()
        a = f.get("a", "").strip()
        if not q or not a:
            continue
        main.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
    if not main:
        return None
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": main,
    }


def inject_ld(s, ld):
    block = "\n<script type=\"application/ld+json\">%s</script>" % json.dumps(ld, ensure_ascii=False)
    # 删除已有 FAQPage LD（先固化旧版）
    s = re.sub(r'<script type="application/ld\+json">\s*\{[^{}]*"@type"\s*:\s*"FAQPage"[^{}]*\}\s*</script>', "", s, flags=re.S)
    s = re.sub(r'<script type="application/ld\+json">\s*\{.*?"@type"\s*:\s*"FAQPage".*?\}\s*</script>', "", s, flags=re.S)
    # 文档级 </body> 前注入（负向后顾，避免落入 tool-runtime 模板区）
    s = re.sub(r'(</body>)', lambda m: block + "\n" + m.group(1), s, count=1)
    return s


def main():
    files = sorted(f for f in os.listdir(TOOLS_DIR) if f.endswith(".html") and f != "index.html")
    ok = 0
    for fn in files:
        key = "banking/" + fn[:-5]
        ld = build_faq_ld(key)
        if not ld:
            print("SKIP no faqs:", key)
            continue
        p = os.path.join(TOOLS_DIR, fn)
        s = open(p, encoding="utf-8").read()
        s2 = inject_ld(s, ld)
        if s2 != s:
            open(p, "w", encoding="utf-8").write(s2)
        ok += 1
        print("OK", key)
    print("banking FAQPage LD injected:", ok)


if __name__ == "__main__":
    main()
