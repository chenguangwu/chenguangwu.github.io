#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P4 行业元数据对齐：把 industry 元数据错配（≠ 真实目录）的工具，
其 meta 的 industry 改为真实目录名。INDUSTRY_DEFS 中仅 `text` 缺中文名，先补。
低风险：不改 URL、不删文件、不动 cat；仅修正分类归属，使分类名显示具体子行业。
"""
import os, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, "_build.py")
TOOLS_JSON = os.path.join(ROOT, "json", "tools.json")


def add_text_to_industry_defs():
    src = open(BUILD, encoding="utf-8").read()
    if "'text':" in src:
        return False
    # 在 INDUSTRY_DEFS 的闭合 } 前插入 text 条目
    m = re.search(r"(INDUSTRY_DEFS\s*=\s*\{.*?\n)(\})", src, re.S)
    new_entry = "    'text':          ('📝', '文本处理'),\n"
    new_src = src[: m.start(2)] + new_entry + src[m.start(2):]
    open(BUILD, "w", encoding="utf-8").write(new_src)
    return True


def fix_meta(content, dirname):
    def repl(mm):
        pre, body, post = mm.group(1), mm.group(2), mm.group(3)
        if re.search(r"industry=", body):
            body = re.sub(r"industry=[^,]+", "industry=" + dirname, body)
        elif "cat=" in body:
            body = re.sub(r"(cat=[^,]+)", r"\1, industry=" + dirname, body, count=1)
        else:
            body = "industry=" + dirname + ", " + body
        return pre + body + post

    return re.sub(r'(<meta name="toolbox" content=")([^"]*)(")', repl, content, count=1)


def main():
    added = add_text_to_industry_defs()
    print("INDUSTRY_DEFS 补 text 条目:", "已添加" if added else "已存在，跳过")

    t = json.load(open(TOOLS_JSON, encoding="utf-8"))
    mism = []
    for x in t:
        p = x.get("path") or (x["industry"] + "/" + x["file"])
        d = p.split("/", 1)[0]
        if x["industry"] != d:
            mism.append((p, d, x["industry"]))

    done, skipped = [], []
    for p, d, wrong in mism:
        fpath = os.path.join(ROOT, "tools", p)
        if not os.path.exists(fpath):
            skipped.append(p + " (磁盘缺失)")
            continue
        c = open(fpath, encoding="utf-8").read()
        if 'name="toolbox"' not in c:
            skipped.append(p + " (无 toolbox meta)")
            continue
        new_c = fix_meta(c, d)
        if new_c == c:
            skipped.append(p + " (未改动)")
            continue
        open(fpath, "w", encoding="utf-8").write(new_c)
        done.append(f"{p}: {wrong} -> {d}")
        # print("FIX:", p, wrong, "->", d)

    print(f"\n完成：{len(done)} 个工具 industry 元数据已对齐到目录；跳过 {len(skipped)} 个。")
    for s in skipped[:20]:
        print("SKIP:", s)


if __name__ == "__main__":
    main()
