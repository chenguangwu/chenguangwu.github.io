#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
只读检查：定位所有 TOOLBOX-REDIRECT 桩，并检测是否有源文件（HTML/JS/非构建JSON）
硬编码链接指向这些桩（删除桩会产生站内死链）。
使用完整路径匹配（归一化为 /tools/xxx/yyy.html），避免 basename 同名误报。
"""
import os, re
from urllib.parse import urlparse, urljoin

ROOT = "/Users/cgw/project/cgw/chenguangwu.github.io"
SITE_HOST = "chenguangwu.github.io"
MARKER = "TOOLBOX-REDIRECT"

# 1. 收集桩：tools/ 下含 TOOLBOX-REDIRECT 标记的 .html（排除 zh-tw 产物）
stub_set = set()          # 归一化路径 /tools/.../x.html
stub_list = []            # 相对ROOT路径 tools/.../x.html
stub_target = {}          # 桩路径 -> canonical 目标路径
for dirpath, dirnames, filenames in os.walk(os.path.join(ROOT, "tools")):
    rel_dir = os.path.relpath(dirpath, ROOT).replace(os.sep, "/")
    if rel_dir.startswith("zh-tw/"):
        continue
    for fn in filenames:
        if not fn.endswith(".html"):
            continue
        fp = os.path.join(dirpath, fn)
        with open(fp, encoding="utf-8", errors="ignore") as f:
            head = f.read(3000)
        if MARKER in head:
            rel = os.path.relpath(fp, ROOT).replace(os.sep, "/")
            norm = "/" + rel
            stub_set.add(norm)
            stub_list.append(rel)
            m = re.search(r'<link rel="canonical" href="([^"]+)"', head)
            tgt = ""
            if m:
                u = urlparse(m.group(1))
                tgt = u.path if u.netloc == SITE_HOST else m.group(1)
            stub_target[norm] = tgt

stub_list.sort()
print(f"[1] 找到桩数量: {len(stub_list)}")
for rel in stub_list:
    print(f"    STUB /{rel}  ->  {stub_target.get('/'+rel,'')}")

# 指向另一个桩的跳转链检测
chain = [s for s in stub_list if stub_target.get("/"+s, "") in stub_set]
if chain:
    print(f"[!] 警告：以下桩的 canonical 指向另一个桩（跳转链）：{chain}")

# 2. 扫描源文件
EXCLUDE_DIRS = {"zh-tw", "node_modules", ".git", ".workbuddy"}
# 构建产物 json（删除桩+重建会自动清除），排除以免噪音
BUILD_JSON = {"json/tools.json"}
BUILD_JSON_PREFIX = ("json/industry-", "json/guides.json")

link_re = re.compile(r'''(?:href|src)\s*=\s*["']([^"']+)["']''', re.I)
js_url_re = re.compile(r'''["']((?:https?://[^\s"']+?|/[^\s"']*?\.[a-z]{2,5}(?:[?#][^\s"']*)?))["']''', re.I)

def should_skip(path):
    parts = path.split(os.sep)
    return any(ex in parts for ex in EXCLUDE_DIRS)

def normalize(base_file, link):
    link = link.strip().split("#")[0]
    if not link or link.startswith("mailto:") or link.startswith("tel:") \
       or link.startswith("data:") or link.startswith("javascript:"):
        return None
    if link.startswith("//"):
        link = "https:" + link
    if link.startswith("http://") or link.startswith("https://"):
        p = urlparse(link)
        return p.path if p.netloc == SITE_HOST else None
    joined = urljoin("file://" + base_file, link)
    if joined.startswith("file://"):
        path = joined[len("file://"):]
        if path.startswith(ROOT):
            path = path[len(ROOT):]
        return path
    return None

refs = {s: [] for s in stub_set}

def scan_file(fp):
    rel = os.path.relpath(fp, ROOT).replace(os.sep, "/")
    if ("/" + rel) in stub_set:
        return  # 跳过桩自身
    # 排除构建产物 json
    if rel in BUILD_JSON or rel.startswith(BUILD_JSON_PREFIX):
        return
    try:
        with open(fp, encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception:
        return
    for m in link_re.finditer(content):
        n = normalize(fp, m.group(1))
        if n in stub_set:
            refs[n].append(rel)
    for m in js_url_re.finditer(content):
        n = normalize(fp, m.group(1))
        if n in stub_set:
            refs[n].append(rel)

# HTML + JS + 其它源文件
exts = (".html", ".js", ".json", ".xml", ".php", ".asp", ".aspx")
for dirpath, dirnames, filenames in os.walk(ROOT):
    if should_skip(dirpath):
        continue
    for fn in filenames:
        if fn.lower().endswith(exts):
            scan_file(os.path.join(dirpath, fn))

print("\n[2] 死链引用汇总（删除桩后会被指向的源文件）")
total = 0
for s in sorted(stub_set):
    r = sorted(set(refs[s]))
    if r:
        total += len(r)
        print(f"  {s}\n     被引用 {len(r)} 处: {r}")
print(f"\n  有外部引用的桩: {sum(1 for s in stub_set if refs[s])}")
print(f"  无外部引用的桩: {sum(1 for s in stub_set if not refs[s])}")
print(f"  外部引用总数: {total}")
