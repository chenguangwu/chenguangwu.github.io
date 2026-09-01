#!/usr/bin/env python3
# 批量将工具页的优质中文描述写回 i18n 字典的 zh-CN.intro 字段。
# 用法: python3 scripts/apply_intro.py <mapping.json>
# mapping.json: {"tools/<ind>/<slug>.html": "新的中文描述", ...}
# 写回时探测原文件缩进，保持最小 diff；仅修改 intro，不触碰 title/h1 等其他字段。
import json, re, os, sys

SRC = sys.argv[1] if len(sys.argv) > 1 else "/tmp/batch1_intro.json"
I18N_DIR = "i18n/tools"
TOOLS_DIR = "tools"


def detect_indent(raw):
    m = re.search(r"\n([ \t]+)\"", raw)
    return len(m.group(1)) if m else 2


def main():
    mapping = json.load(open(SRC, encoding="utf-8"))
    cnt = 0
    for path, new in mapping.items():
        parts = path.split("/")
        if len(parts) < 3 or parts[0] != "tools":
            print("SKIP bad path", path)
            continue
        ind = parts[1]
        slug = os.path.splitext(parts[2])[0]
        fp = os.path.join(I18N_DIR, ind + ".json")
        if not os.path.isfile(fp):
            print("SKIP no json", path)
            continue
        raw = open(fp, encoding="utf-8").read()
        indn = detect_indent(raw)
        data = json.loads(raw)
        e = data.get(slug)
        if not isinstance(e, dict):
            e = {}
            data[slug] = e
        e.setdefault("zh-CN", {})
        e["zh-CN"]["intro"] = new
        with open(fp, "w", encoding="utf-8") as o:
            o.write(json.dumps(data, ensure_ascii=False, indent=indn))
            o.write("\n")
        cnt += 1
    print("UPDATED", cnt, "entries from", SRC)


if __name__ == "__main__":
    main()
