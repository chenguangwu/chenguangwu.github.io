#!/usr/bin/env python3
"""幂等下架 energy 分类 4 个真重复工具及其配套指南。

待下架工具（保留权威页）：
  cop-heatpump           -> 保留 heat-pump-cop
  calculator-calc-5      -> 保留 heat-pump-cop
  solar-output-physics   -> 保留 solar-panel-power
  specific-energy        -> 保留 energy-density

每个待下架工具都有配套指南 <slug>-guide.html，一并下架。

清理范围（避免线上残留入口/断链/门禁失败）：
  - 源 HTML：tools/energy/<slug>.html, guides/<slug>-guide.html
  - 其它指南里的 chip 硬链接（<a class="tool-chip" href=.../<slug>.html>）
  - json/guides.json 注册项（tool == <slug>.html）
  - i18n/tools/energy.json（裸 slug）
  - i18n/tools/_en_override.json / slug-en.json / _en_desc.json（energy/<slug>）
  - i18n/tools/content_deepdive.json（energy/<slug>，indent=1+\\n）
  - i18n/tools/energy-body.json（裸 slug）
  - scripts/enmap/energy.json（裸 slug）
  - i18n/locale-zh-TW.json（energy.<slug>.*）
  - scripts/verify_energy_calc.js 的 4 个用例块

所有 JSON 重排均按原文 detect 的 indent + trailing newline 保格式。
"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUGS = ["cop-heatpump", "calculator-calc-5", "solar-output-physics", "specific-energy"]
APPLY = "--apply" in sys.argv
log = []

def p(*a):
    log.append(" ".join(str(x) for x in a))

def detect_indent(raw):
    for line in raw.splitlines():
        m = re.match(r'^(\s+)\S', line)
        if m:
            return len(m.group(1))
    return 2

def load_json(path):
    raw = open(path, encoding="utf-8").read()
    obj = json.loads(raw)
    indent = detect_indent(raw)
    trailing = raw.endswith("\n")
    return obj, indent, trailing

def dump_json(obj, indent, trailing):
    s = json.dumps(obj, ensure_ascii=False, indent=indent)
    if trailing:
        s += "\n"
    return s

def remove_keys_prefix(d, prefixes):
    """d 为 dict，移除 key 以任一 prefix 开头的项。返回移除数。"""
    rm = [k for k in list(d.keys()) if any(k.startswith(p) for p in prefixes)]
    for k in rm:
        del d[k]
    return len(rm)

def remove_keys_exact(d, keys):
    rm = [k for k in keys if k in d]
    for k in rm:
        del d[k]
    return len(rm)

# ── 1) 删除源 HTML ──────────────────────────────────────────────
for s in SLUGS:
    for f in [f"tools/energy/{s}.html", f"guides/{s}-guide.html"]:
        fp = os.path.join(ROOT, f)
        if os.path.exists(fp):
            if APPLY:
                os.remove(fp)
            p(f"[{'DELETE' if APPLY else 'DRY'}] {f}")

# ── 2) 清理其它指南里的 chip 硬链接 ──────────────────────────────
chip_pat = re.compile(
    r'<a class="tool-chip"[^>]*href="[^"]*tools/energy/(?:%s)\.html"[^>]*>.*?</a>'
    % "|".join(re.escape(s) for s in SLUGS)
)
guides_dir = os.path.join(ROOT, "guides")
for fn in sorted(os.listdir(guides_dir)):
    if not fn.endswith(".html"):
        continue
    fp = os.path.join(guides_dir, fn)
    raw = open(fp, encoding="utf-8").read()
    new, n = chip_pat.subn("", raw)
    if n:
        if APPLY:
            open(fp, "w", encoding="utf-8").write(new)
        p(f"[{'FIX' if APPLY else 'DRY'}] {fn}: 移除 {n} 个 chip 硬链接")

# ── 3) json/guides.json（list，按 tool 字段）─────────────────────
gj = os.path.join(ROOT, "json/guides.json")
obj, indent, trailing = load_json(gj)
before = len(obj)
obj = [e for e in obj if not (isinstance(e, dict) and e.get("tool") in [f"{s}.html" for s in SLUGS])]
if len(obj) != before:
    if APPLY:
        open(gj, "w", encoding="utf-8").write(dump_json(obj, indent, trailing))
    p(f"[{'FIX' if APPLY else 'DRY'}] guides.json: 移除 {before-len(obj)} 条注册")

# ── 4) i18n 字典 ────────────────────────────────────────────────
# 4a energy.json（裸 slug）
ej = os.path.join(ROOT, "i18n/tools/energy.json")
obj, indent, trailing = load_json(ej)
n = remove_keys_exact(obj, SLUGS)
if n:
    if APPLY:
        open(ej, "w", encoding="utf-8").write(dump_json(obj, indent, trailing))
    p(f"[{'FIX' if APPLY else 'DRY'}] energy.json: 移除 {n} 个裸 slug 键")

# 4b _en_override / slug-en / _en_desc（energy/<slug>）
for fn, keyfmt in [("_en_override.json", "energy/{}"), ("slug-en.json", "energy/{}"),
                   ("_en_desc.json", "energy/{}")]:
    fp = os.path.join(ROOT, "i18n/tools", fn)
    obj, indent, trailing = load_json(fp)
    keys = [keyfmt.format(s) for s in SLUGS]
    n = remove_keys_exact(obj, keys)
    if n:
        if APPLY:
            open(fp, "w", encoding="utf-8").write(dump_json(obj, indent, trailing))
        p(f"[{'FIX' if APPLY else 'DRY'}] {fn}: 移除 {n} 个 energy/<slug> 键")

# 4c content_deepdive.json（energy/<slug>，固定 indent=1 + \n）
cd = os.path.join(ROOT, "i18n/tools/content_deepdive.json")
obj, indent, trailing = load_json(cd)
keys = [f"energy/{s}" for s in SLUGS]
n = remove_keys_exact(obj, keys)
if n:
    if APPLY:
        open(cd, "w", encoding="utf-8").write(dump_json(obj, 1, True))
    p(f"[{'FIX' if APPLY else 'DRY'}] content_deepdive.json: 移除 {n} 个 energy/<slug> 键")

# 4d energy-body.json（裸 slug）
eb = os.path.join(ROOT, "i18n/tools/energy-body.json")
obj, indent, trailing = load_json(eb)
n = remove_keys_exact(obj, SLUGS)
if n:
    if APPLY:
        open(eb, "w", encoding="utf-8").write(dump_json(obj, indent, trailing))
    p(f"[{'FIX' if APPLY else 'DRY'}] energy-body.json: 移除 {n} 个裸 slug 键")

# 4e enmap/energy.json（裸 slug）
em = os.path.join(ROOT, "scripts/enmap/energy.json")
obj, indent, trailing = load_json(em)
n = remove_keys_exact(obj, SLUGS)
if n:
    if APPLY:
        open(em, "w", encoding="utf-8").write(dump_json(obj, indent, trailing))
    p(f"[{'FIX' if APPLY else 'DRY'}] enmap/energy.json: 移除 {n} 个裸 slug 键")

# 4f locale-zh-TW.json（energy.<slug>.* 前缀）
lt = os.path.join(ROOT, "i18n/locale-zh-TW.json")
obj, indent, trailing = load_json(lt)
prefixes = [f"energy.{s}." for s in SLUGS]
n = remove_keys_prefix(obj, prefixes)
if n:
    if APPLY:
        open(lt, "w", encoding="utf-8").write(dump_json(obj, indent, trailing))
    p(f"[{'FIX' if APPLY else 'DRY'}] locale-zh-TW.json: 移除 {n} 个 energy.<slug>.* 键")

# ── 5) verify_energy_calc.js 用例块（基于行的括号计数，稳健处理嵌套 inputs:{}）──
vp = os.path.join(ROOT, "scripts/verify_energy_calc.js")
vraw = open(vp, encoding="utf-8").read()
vlines = vraw.split("\n")
removed = 0
for s in SLUGS:
    needle = f'slug: "energy/{s}"'
    # 定位 slug 所在行
    slug_ln = None
    for li, line in enumerate(vlines):
        if needle in line:
            slug_ln = li
            break
    if slug_ln is None:
        continue
    # 向上找对象开括号行（形如 "  {" 的单独行）
    obj_start_ln = None
    for li in range(slug_ln, -1, -1):
        if re.match(r'^\s*\{\s*$', vlines[li]):
            obj_start_ln = li
            break
    if obj_start_ln is None:
        continue
    # 向下括号计数找闭括号行
    depth = 0; end_ln = None
    for li in range(obj_start_ln, len(vlines)):
        for ch in vlines[li]:
            if ch == "{": depth += 1
            elif ch == "}": depth -= 1
        if depth == 0 and li > obj_start_ln:
            end_ln = li
            break
    if end_ln is None:
        continue
    # 闭括号后的逗号行（单独 ","）
    post_start = end_ln + 1
    if post_start < len(vlines) and vlines[post_start].strip() == ",":
        post_start += 1
    # 开括号前的连续注释行（// ...）
    pre_start = obj_start_ln
    while pre_start - 1 >= 0 and vlines[pre_start - 1].lstrip().startswith("//"):
        pre_start -= 1
    # 删除 [pre_start, post_start) 行
    vlines = vlines[:pre_start] + vlines[post_start:]
    removed += 1
if removed:
    vnew = "\n".join(vlines)
    if APPLY:
        open(vp, "w", encoding="utf-8").write(vnew)
    p(f"[{'FIX' if APPLY else 'DRY'}] verify_energy_calc.js: 移除 {removed} 个用例块")

print("\n".join(log))
print(f"\n模式: {'APPLY (已落盘)' if APPLY else 'DRY-RUN (未改动)'}")
