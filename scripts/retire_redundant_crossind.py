#!/usr/bin/env python3
"""幂等下架 3 个「跨目录/同目录真重复」冗余工具（保留功能完全覆盖的权威页）。

取证（语义层，逐页比对 calc 输入集 + 公式系数）：
  - materials/density-basic  vs science/density-physics
      两页输入集完全相同（仅 V、m 两个变量），公式 ρ=m/V 固定 → 真重复。
      保留 science/density-physics（物理通用），下架 materials/density-basic。
  - science/z-score-calculator  vs statistics/z
      两页输入集相同（x、mu、sigma），均含 Z=(x-mu)/σ 与百分位 Φ → 真重复。
      保留 statistics/z（Z 分数本质属统计），下架 science/z-score-calculator。
  - fitness/calculator-calc-metabolism  vs fitness/calc-2
      两页均用 Mifflin+Harris 双公式 BMR，核心输入（年龄/性别/身高/体重）相同；
      calculator-calc-metabolism 仅多 historyBox（历史，非计算）→ 功能⊆calc-2。
      calc-2 是全局复用编号页（30+ 行业同名，不可删），下架 fitness 专名冗余版。
以上 3 处删除不丢失任何功能（保留方输入集 ⊇ 删除方），且影响范围小，不涉 SEO 风险。

清理范围（避免线上残留入口/断链/门禁失败）：
  - 源 HTML：tools/<ind>/<slug>.html；中文指南 guides/<slug>-guide.html
  - 其它页 chip 硬链接（含 .en.html 内部指向已删工具者）
  - json/guides.json 注册项（tool == <slug>.html）
  - i18n/tools/<ind>.json（裸 slug） + <ind>-body.json
  - i18n/tools/_en_override.json / slug-en.json / _en_desc.json / content_deepdive.json（<ind>/<slug>）
  - scripts/enmap/<ind>.json（裸 slug）
  - i18n/locale-zh-TW.json（<ind>.<slug>.* 前缀）
  - scripts/verify_*.js 用例块（字符级括号匹配，兼容内联 { slug: ）
  - zh-tw 残留繁体产物（精确路径，按 ind+slug，禁止子串匹配）
所有 JSON 重排均按原文 detect 的 indent + trailing newline 保格式。
"""
import os, re, json, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = "--apply" in sys.argv
log = []

# (industry, slug) —— 删除方（冗余），保留方功能完全覆盖
ITEMS = [
    ("materials", "density-basic"),            # -> science/density-physics
    ("science", "z-score-calculator"),         # -> statistics/z
    ("fitness", "calculator-calc-metabolism"), # -> fitness/calc-2（全局复用编号页，不可删）
]

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
    rm = [k for k in list(d.keys()) if any(k.startswith(p) for p in prefixes)]
    for k in rm:
        del d[k]
    return len(rm)

def remove_keys_exact(d, keys):
    rm = [k for k in keys if k in d]
    for k in rm:
        del d[k]
    return len(rm)

# ── 1) 删除源 HTML + 中文指南 ───────────────────────────────────
for ind, slug in ITEMS:
    fp = os.path.join(ROOT, f"tools/{ind}/{slug}.html")
    if os.path.exists(fp):
        if APPLY:
            os.remove(fp)
        p(f"[{'DELETE' if APPLY else 'DRY'}] tools/{ind}/{slug}.html")
    gf = os.path.join(ROOT, f"guides/{slug}-guide.html")
    if os.path.exists(gf):
        if APPLY:
            os.remove(gf)
        p(f"[{'DELETE' if APPLY else 'DRY'}] guides/{slug}-guide.html")

# ── 2) 清理其它页中指向已删工具的所有 <a> 链接（无论 class / 绝对或相对路径）──
# 覆盖：tool-chip（完整域名路径）+ related-tool-card（相对路径 slug.html）等任意形态。
targets = ([f"tools/{ind}/{slug}.html" for ind, slug in ITEMS]
           + [f"guides/{slug}-guide.html" for _, slug in ITEMS]
           + [f"guides/{slug}-guide.en.html" for _, slug in ITEMS]
           + [f"{slug}.html" for _, slug in ITEMS]          # 相对路径（同目录）
           + [f"{slug}-guide.html" for _, slug in ITEMS])
chip_pat = re.compile(
    r'<a\b[^>]*href="[^"]*(?:%s)[^"]*"[^>]*>[\s\S]*?</a>'
    % "|".join(re.escape(t) for t in targets)
)
deleted_guides = {f"{s}-guide.html" for _, s in ITEMS}
for pat in [os.path.join(ROOT, "tools", "**", "*.html"),
            os.path.join(ROOT, "guides", "**", "*.html")]:
    for fp in sorted(glob.glob(pat, recursive=True)):
        fn = os.path.basename(fp)
        if fn in deleted_guides:
            continue
        raw = open(fp, encoding="utf-8").read()
        new, n = chip_pat.subn("", raw)
        if n:
            if APPLY:
                open(fp, "w", encoding="utf-8").write(new)
            p(f"[{'FIX' if APPLY else 'DRY'}] {os.path.relpath(fp, ROOT)}: 移除 {n} 个 chip 硬链接")

# ── 3) json/guides.json（list，按 tool 字段）────────────────────
gj = os.path.join(ROOT, "json/guides.json")
if os.path.exists(gj):
    obj, indent, trailing = load_json(gj)
    before = len(obj)
    wanted = {f"{s}.html" for _, s in ITEMS}
    obj = [e for e in obj if not (isinstance(e, dict) and e.get("tool") in wanted)]
    if len(obj) != before:
        if APPLY:
            open(gj, "w", encoding="utf-8").write(dump_json(obj, indent, trailing))
        p(f"[{'FIX' if APPLY else 'DRY'}] guides.json: 移除 {before-len(obj)} 条注册")

# ── 4) i18n 字典 ────────────────────────────────────────────────
for ind, slug in ITEMS:
    ej = os.path.join(ROOT, f"i18n/tools/{ind}.json")
    if os.path.exists(ej):
        obj, indent, trailing = load_json(ej)
        n = remove_keys_exact(obj, [slug])
        if n:
            if APPLY:
                open(ej, "w", encoding="utf-8").write(dump_json(obj, indent, trailing))
            p(f"[{'FIX' if APPLY else 'DRY'}] {ind}.json: 移除 {n} 个裸 slug 键")
    for fn in ["_en_override.json", "slug-en.json", "_en_desc.json"]:
        fp = os.path.join(ROOT, "i18n/tools", fn)
        if not os.path.exists(fp):
            continue
        obj, indent, trailing = load_json(fp)
        key = f"{ind}/{slug}"
        n = remove_keys_exact(obj, [key])
        if n:
            if APPLY:
                open(fp, "w", encoding="utf-8").write(dump_json(obj, indent, trailing))
            p(f"[{'FIX' if APPLY else 'DRY'}] {fn}: 移除 {n} 个 {key} 键")
    cd = os.path.join(ROOT, "i18n/tools/content_deepdive.json")
    obj, _, _ = load_json(cd)
    key = f"{ind}/{slug}"
    n = remove_keys_exact(obj, [key])
    if n:
        if APPLY:
            open(cd, "w", encoding="utf-8").write(dump_json(obj, 1, True))
        p(f"[{'FIX' if APPLY else 'DRY'}] content_deepdive.json: 移除 {n} 个 {key} 键")
    eb = os.path.join(ROOT, f"i18n/tools/{ind}-body.json")
    if os.path.exists(eb):
        obj, indent, trailing = load_json(eb)
        n = remove_keys_exact(obj, [slug])
        if n:
            if APPLY:
                open(eb, "w", encoding="utf-8").write(dump_json(obj, indent, trailing))
            p(f"[{'FIX' if APPLY else 'DRY'}] {ind}-body.json: 移除 {n} 个裸 slug 键")
    em = os.path.join(ROOT, f"scripts/enmap/{ind}.json")
    if os.path.exists(em):
        obj, indent, trailing = load_json(em)
        n = remove_keys_exact(obj, [slug])
        if n:
            if APPLY:
                open(em, "w", encoding="utf-8").write(dump_json(obj, indent, trailing))
            p(f"[{'FIX' if APPLY else 'DRY'}] enmap/{ind}.json: 移除 {n} 个裸 slug 键")
    lt = os.path.join(ROOT, "i18n/locale-zh-TW.json")
    if os.path.exists(lt):
        obj, indent, trailing = load_json(lt)
        n = remove_keys_prefix(obj, [f"{ind}.{slug}."])
        if n:
            if APPLY:
                open(lt, "w", encoding="utf-8").write(dump_json(obj, indent, trailing))
            p(f"[{'FIX' if APPLY else 'DRY'}] locale-zh-TW.json: 移除 {n} 个 {ind}.{slug}.* 键")

# ── 5) 所有 verify_*.js 用例块（字符级括号匹配，兼容内联 { slug: ）──
for ind, slug in ITEMS:
    needle = f'"{ind}/{slug}"'
    for vp in sorted(glob.glob(os.path.join(ROOT, "scripts", "verify_*.js"))):
        vraw = open(vp, encoding="utf-8").read()
        if needle not in vraw:
            continue
        vlines = vraw.split("\n")
        slug_ln = next((li for li, line in enumerate(vlines) if needle in line), None)
        if slug_ln is None:
            continue
        obj_start_ln = None
        for li in range(slug_ln, -1, -1):
            if "{" in vlines[li]:
                obj_start_ln = li
                break
        if obj_start_ln is None:
            continue
        text = "\n".join(vlines[obj_start_ln:])
        depth = 0; end_pos = None
        for idx, ch in enumerate(text):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    end_pos = idx
                    break
        if end_pos is None:
            continue
        end_ln = obj_start_ln + text[:end_pos].count("\n")
        post_start = end_ln + 1
        if post_start < len(vlines) and vlines[post_start].strip() == ",":
            post_start += 1
        pre_start = obj_start_ln
        while pre_start - 1 >= 0 and vlines[pre_start - 1].lstrip().startswith("//"):
            pre_start -= 1
        vlines = vlines[:pre_start] + vlines[post_start:]
        if APPLY:
            open(vp, "w", encoding="utf-8").write("\n".join(vlines))
        p(f"[{'FIX' if APPLY else 'DRY'}] {os.path.basename(vp)}: 移除 {ind}/{slug} 用例块")

# ── 6) zh-tw 残留繁体产物（精确路径，按 ind+slug，禁止子串匹配）──
for ind, slug in ITEMS:
    for fp in [
        os.path.join(ROOT, f"zh-tw/tools/{ind}/{slug}.html"),
        os.path.join(ROOT, f"zh-tw/guides/{slug}-guide.html"),
        os.path.join(ROOT, f"zh-tw/guides/{slug}-guide.en.html"),
    ]:
        if os.path.isfile(fp):
            if APPLY:
                os.remove(fp)
            p(f"[{'DELETE' if APPLY else 'DRY'}] {os.path.relpath(fp, ROOT)} (zh-tw 残留)")

print("\n".join(log))
print(f"\n模式: {'APPLY (已落盘)' if APPLY else 'DRY-RUN (未改动)'}")
