# -*- coding: utf-8 -*-
"""为 archaeology 6 个工具注入真实 FAQPage JSON-LD 结构化数据（文档级 </body> 负向后顾注入）。"""
import json, re, glob, os

CD = json.load(open("i18n/tools/content_deepdive.json", encoding="utf-8"))

def ld_for(key):
    e = CD.get(key)
    if not e:
        return None
    main = []
    for f in e.get("faqs", []):
        q = f.get("q", "").strip()
        a = f.get("a", "").strip()
        if q and a:
            main.append({
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            })
    if not main:
        return None
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": main,
    }

# 文档级 </body> 负向后顾，确保只注入一次
BODY_RE = re.compile(r"</body>", re.S)

ok = 0
for f in sorted(glob.glob("tools/archaeology/*.html")):
    if f.endswith("index.html"):
        continue
    base = os.path.basename(f)[:-5]
    key = "archaeology/" + base
    obj = ld_for(key)
    if not obj:
        print("SKIP (no faq):", base)
        continue
    s = open(f, encoding="utf-8").read()
    if '"@type":"FAQPage"' in s or '"@type": "FAQPage"' in s:
        print("EXISTS:", base)
        continue
    ld = '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + "\n</script>\n"
    if not BODY_RE.search(s):
        print("NO BODY:", base)
        continue
    s2 = BODY_RE.sub(lambda m: ld + "</body>", s, count=1)
    open(f, "w", encoding="utf-8").write(s2)
    ok += 1
    print("OK:", base)

print("injected", ok)
