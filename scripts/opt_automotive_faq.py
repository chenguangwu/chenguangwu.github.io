# -*- coding: utf-8 -*-
"""为 automotive 53 个工具页注入真实 FAQPage 结构化数据（负向后顾注入文档级 </body>），并先清除旧 LD。"""
import json, re, os, glob

DATA = json.load(open("i18n/tools/content_deepdive.json", encoding="utf-8"))


def make_ld(key):
    e = DATA.get(key)
    if not e:
        return None
    qas = [
        {"@type": "Question", "name": q["q"],
         "acceptedAnswer": {"@type": "Answer", "text": q["a"]}}
        for q in e.get("faqs", [])
    ]
    if not qas:
        return None
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": qas}


def inject(s, key):
    ld = make_ld(key)
    if not ld:
        return s, False
    # 先删除已有的 FAQPage JSON-LD（早期残留套话）
    s = re.sub(
        r'<script type="application/ld\+json">.*?"@type"\s*:\s*"FAQPage".*?</script>',
        "", s, flags=re.S)
    block = ('<script type="application/ld+json">\n'
             + json.dumps(ld, ensure_ascii=False, indent=2)
             + '\n</script>')
    # 负向后顾：注入到文档级 </body> 之前
    if re.search(r'</body>', s):
        s = re.sub(r'(?s)(.*)</body>', lambda m: m.group(1) + "\n" + block + "\n</body>", s, count=1)
    else:
        s = s + "\n" + block + "\n"
    return s, True


def main():
    n = 0
    for f in sorted(glob.glob("tools/automotive/*.html")):
        if f.endswith("index.html"):
            continue
        key = "automotive/" + os.path.basename(f)[:-5]
        s = open(f, encoding="utf-8").read()
        s2, ok = inject(s, key)
        if ok:
            open(f, "w", encoding="utf-8").write(s2)
            n += 1
            print("OK", key)
        else:
            print("SKIP", key)
    print("injected", n)


if __name__ == "__main__":
    main()
