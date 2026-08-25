#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内容指纹去重扫描：对全站工具页做"正文归一化指纹"，找真正冗余（正文+标题都雷同）的工具。
排除：TOOLBOX-REDIRECT 桩、<script>/<style>、nav/footer/breadcrumb/品牌 boilerplate。
输出：按指纹聚类的重复组（>1 成员），供人工/自动清理决策。
"""
import os, re, hashlib, json
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")

BOILER = re.compile(
    r"(ToolBox|工具箱|首页|分类|关于|反馈|复制到剪贴板|计算结果|请输入|"
    r"免责声明|本工具|仅供参考|GitHub|备案|版权|All rights reserved|"
    r"breadcrumb|BreadcrumbList|nav-|footer|navbar|sidebar|语言|中文|English)",
    re.I,
)

SCRIPT = re.compile(r"<script[\s\S]*?</script>", re.I)
STYLE = re.compile(r"<style[\s\S]*?</style>", re.I)
TAG = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")
REDIRECT = re.compile(r"TOOLBOX-REDIRECT")

def normalize(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        html = f.read()
    if REDIRECT.search(html):
        return None
    html = SCRIPT.sub(" ", html)
    html = STYLE.sub(" ", html)
    # 去掉 nav / footer / breadcrumb 区域
    html = re.sub(r'<nav[\s\S]*?</nav>', " ", html, flags=re.I)
    html = re.sub(r'<footer[\s\S]*?</footer>', " ", html, flags=re.I)
    html = re.sub(r'class="[^"]*(breadcrumb|navbar|sidebar|nav-|footer)[^"]*"[\s\S]*?</[a-z]+>', " ", html, flags=re.I)
    text = TAG.sub(" ", html)
    text = WS.sub(" ", text).strip()
    # 去掉 boilerplate 词
    toks = [t for t in BOILER.split(text)]
    text = " ".join(toks)
    # 去掉纯数字/标点碎片
    words = [w for w in re.findall(r"[\u4e00-\u9fffA-Za-z0-9]+", text) if len(w) > 1]
    return " ".join(words)

def main():
    fp_map = defaultdict(list)
    files = 0
    for dirpath, _, fnames in os.walk(TOOLS):
        for fn in fnames:
            if not fn.endswith(".html"):
                continue
            p = os.path.join(dirpath, fn)
            body = normalize(p)
            if body is None or len(body) < 40:
                continue
            files += 1
            h = hashlib.md5(body.encode("utf-8")).hexdigest()
            rel = os.path.relpath(p, ROOT)
            fp_map[h].append((rel, len(body)))

    # 聚类：同指纹>1 且 不同文件路径
    dups = {h: v for h, v in fp_map.items() if len(v) > 1}
    print(f"扫描工具页: {files}")
    print(f"唯一正文指纹: {len(fp_map)}")
    print(f"重复组(>1 成员): {len(dups)}")
    total_dup_tools = sum(len(v) for v in dups.values())
    print(f"涉及工具总数: {total_dup_tools}")
    print("=" * 70)
    rows = []
    for h, v in sorted(dups.items(), key=lambda kv: -len(kv[1])):
        rows.append((h, v))
        members = ", ".join(f"{r}({n})" for r, n in v)
        print(f"[{len(v)}] {members}")
    # 导出 JSON 便于后续处理
    out = [{"hash": h, "members": [{"path": r, "len": n} for r, n in v]} for h, v in rows]
    with open(os.path.join(ROOT, "scripts", "_dup_scan.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("=" * 70)
    print("已导出 scripts/_dup_scan.json")

if __name__ == "__main__":
    main()
