#!/usr/bin/env python3
"""幂等下架 5 个跨分类真重复工具（保留权威页），沿用 retire_energy_dupes 清理清单。

待下架（保留更全/命名规范版）：
  sports/diving-no-decompression        -> 保留 sports/calc-time（潜水 NDL，9 输入全集）
  sports/time-30                        -> 保留 sports/youyonghuashuixiaolv-swolf（SWOLF，10 输入）
  tcm-pharmacy/generator-28             -> 保留 tcm-pharmacy/formula-song（方歌生成器，更全）
  it/mime-type-lookup                  -> 保留 it/mime-type（MIME 速查，更全）
  it/http-methods-reference            -> 保留 it/http-methods（HTTP 方法，更全）

取证（语义层，非仅 h1 同名）：
  - 查表/生成器型（it mime/http、tcm 生成器）：desc/数据完全一致，被下架者为早期英文占位低质副本
  - 子集型（sports diving/time-30）：calc 公式证实为保留版的简化子集
  - 已排除 finance/salary-after-tax vs payroll-calculator（累计预扣法 vs 含年终奖城市比例，同名异功能）
  - 已排除 ophthalmology 两 OSDI 页（算法不同，一个疑似错误版）
  - 已排除 agriculture/calc-2（calc-N 编号页全局 30+ 分类复用，guides.json 按文件名注册，牵连系统性命名问题，单独专项）

清理范围（避免线上残留入口/断链/门禁失败）：
  - 源 HTML：tools/<ind>/<slug>.html；指南 guides/<slug>-guide.html(+.en.html 若存在)
  - 其它页的 chip 硬链接（<a class="tool-chip" href=.../<slug>.html 或 /<slug>-guide.html>）
  - json/guides.json 注册项（tool == <slug>.html）
  - i18n/tools/<ind>.json（裸 slug）
  - i18n/tools/_en_override.json / slug-en.json / _en_desc.json（<ind>/<slug>）
  - i18n/tools/content_deepdive.json（<ind>/<slug>，indent=1+\n）
  - i18n/tools/<ind>-body.json（裸 slug）
  - scripts/enmap/<ind>.json（裸 slug）
  - i18n/locale-zh-TW.json（<ind>.<slug>.* 前缀）
  - scripts/verify_<ind>_calc.js 用例块（needle: slug 或 <ind>/<slug>，基于行括号计数）

所有 JSON 重排均按原文 detect 的 indent + trailing newline 保格式。
"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = "--apply" in sys.argv
log = []

# (industry, slug, has_guide)
ITEMS = [
    ("sports", "diving-no-decompression", False),
    ("sports", "time-30", False),
    ("tcm-pharmacy", "generator-28", False),
    ("it", "mime-type-lookup", True),
    ("it", "http-methods-reference", True),
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

# ── 1) 删除源 HTML + 指南 ──────────────────────────────────────
for ind, slug, has_guide in ITEMS:
    for f in [f"tools/{ind}/{slug}.html"]:
        fp = os.path.join(ROOT, f)
        if os.path.exists(fp):
            if APPLY:
                os.remove(fp)
            p(f"[{'DELETE' if APPLY else 'DRY'}] {f}")
    if has_guide:
        # 仅删中文指南 .html；.en.html 英文副本留待「指南英文副本清理」专项处理
        # （zh-tw 构建产物指南页含指向 .en.html 的英文版链接，提前删会造成死链）
        for gf in [f"guides/{slug}-guide.html"]:
            fp = os.path.join(ROOT, gf)
            if os.path.exists(fp):
                if APPLY:
                    os.remove(fp)
                p(f"[{'DELETE' if APPLY else 'DRY'}] {gf}")

# ── 2) 清理其它页的 chip 硬链接 ────────────────────────────────
slug_re = "|".join(re.escape(s) for _, s, _ in ITEMS)
# 匹配 tools/<ind>/<slug>.html 或 guides/<slug>-guide.html（含 .en 变体）
chip_pat = re.compile(
    r'<a class="tool-chip"[^>]*href="[^"]*(?:tools/(?:%s)/(?:%s)\.html|guides/(?:%s)-guide(?:\.html|\.en\.html))"[^>]*>.*?</a>'
    % (slug_re, slug_re, slug_re)
)
# 本批将删除的指南文件名（步骤 1），步骤 2 跳过避免重建空页
deleted_guides = set()
for _, slug, has_guide in ITEMS:
    if has_guide:
        deleted_guides.add(f"{slug}-guide.html")
for sub in ["guides", "tools"]:
    d = os.path.join(ROOT, sub)
    if not os.path.isdir(d):
        continue
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".html"):
            continue
        fp = os.path.join(d, fn)
        # 跳过已被步骤 1 删除的源文件（避免 open('w') 重建空页）
        if not os.path.exists(fp) or fn in deleted_guides:
            continue
        raw = open(fp, encoding="utf-8").read()
        new, n = chip_pat.subn("", raw)
        if n:
            if APPLY:
                open(fp, "w", encoding="utf-8").write(new)
            p(f"[{'FIX' if APPLY else 'DRY'}] {sub}/{fn}: 移除 {n} 个 chip 硬链接")

# ── 3) json/guides.json（list，按 tool 字段）────────────────────
gj = os.path.join(ROOT, "json/guides.json")
if os.path.exists(gj):
    obj, indent, trailing = load_json(gj)
    before = len(obj)
    wanted = {f"{s}.html" for _, s, _ in ITEMS}
    obj = [e for e in obj if not (isinstance(e, dict) and e.get("tool") in wanted)]
    if len(obj) != before:
        if APPLY:
            open(gj, "w", encoding="utf-8").write(dump_json(obj, indent, trailing))
        p(f"[{'FIX' if APPLY else 'DRY'}] guides.json: 移除 {before-len(obj)} 条注册")

# ── 4) i18n 字典 ────────────────────────────────────────────────
for ind, slug, _ in ITEMS:
    # 4a <ind>.json（裸 slug）
    ej = os.path.join(ROOT, f"i18n/tools/{ind}.json")
    if os.path.exists(ej):
        obj, indent, trailing = load_json(ej)
        n = remove_keys_exact(obj, [slug])
        if n:
            if APPLY:
                open(ej, "w", encoding="utf-8").write(dump_json(obj, indent, trailing))
            p(f"[{'FIX' if APPLY else 'DRY'}] {ind}.json: 移除 {n} 个裸 slug 键")
    # 4b _en_override / slug-en / _en_desc（<ind>/<slug>）
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
    # 4c content_deepdive.json（<ind>/<slug>，固定 indent=1+\n）
    cd = os.path.join(ROOT, "i18n/tools/content_deepdive.json")
    obj, _, _ = load_json(cd)
    key = f"{ind}/{slug}"
    n = remove_keys_exact(obj, [key])
    if n:
        if APPLY:
            open(cd, "w", encoding="utf-8").write(dump_json(obj, 1, True))
        p(f"[{'FIX' if APPLY else 'DRY'}] content_deepdive.json: 移除 {n} 个 {key} 键")
    # 4d <ind>-body.json（裸 slug）
    eb = os.path.join(ROOT, f"i18n/tools/{ind}-body.json")
    if os.path.exists(eb):
        obj, indent, trailing = load_json(eb)
        n = remove_keys_exact(obj, [slug])
        if n:
            if APPLY:
                open(eb, "w", encoding="utf-8").write(dump_json(obj, indent, trailing))
            p(f"[{'FIX' if APPLY else 'DRY'}] {ind}-body.json: 移除 {n} 个裸 slug 键")
    # 4e enmap/<ind>.json（裸 slug）
    em = os.path.join(ROOT, f"scripts/enmap/{ind}.json")
    if os.path.exists(em):
        obj, indent, trailing = load_json(em)
        n = remove_keys_exact(obj, [slug])
        if n:
            if APPLY:
                open(em, "w", encoding="utf-8").write(dump_json(obj, indent, trailing))
            p(f"[{'FIX' if APPLY else 'DRY'}] enmap/{ind}.json: 移除 {n} 个裸 slug 键")
    # 4f locale-zh-TW.json（<ind>.<slug>.* 前缀）
    lt = os.path.join(ROOT, "i18n/locale-zh-TW.json")
    if os.path.exists(lt):
        obj, indent, trailing = load_json(lt)
        n = remove_keys_prefix(obj, [f"{ind}.{slug}."])
        if n:
            if APPLY:
                open(lt, "w", encoding="utf-8").write(dump_json(obj, indent, trailing))
            p(f"[{'FIX' if APPLY else 'DRY'}] locale-zh-TW.json: 移除 {n} 个 {ind}.{slug}.* 键")

# ── 5) verify_<ind>_calc.js 用例块（基于行的括号计数）──────────
for ind, slug, _ in ITEMS:
    vp = os.path.join(ROOT, f"scripts/verify_{ind}_calc.js")
    if not os.path.exists(vp):
        continue
    vraw = open(vp, encoding="utf-8").read()
    vlines = vraw.split("\n")
    removed = 0
    # 可能需要多轮（同一文件多个 slug 已循环，这里每 slug 处理一次）
    needle = f'slug: "{ind}/{slug}"'
    if needle not in vraw:
        needle = f'"{ind}/{slug}"'
    if needle not in vraw:
        needle = slug
    slug_ln = None
    for li, line in enumerate(vlines):
        if needle in line:
            slug_ln = li
            break
    if slug_ln is None:
        continue
    obj_start_ln = None
    for li in range(slug_ln, -1, -1):
        if re.match(r'^\s*\{\s*$', vlines[li]):
            obj_start_ln = li
            break
    if obj_start_ln is None:
        continue
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
    post_start = end_ln + 1
    if post_start < len(vlines) and vlines[post_start].strip() == ",":
        post_start += 1
    pre_start = obj_start_ln
    while pre_start - 1 >= 0 and vlines[pre_start - 1].lstrip().startswith("//"):
        pre_start -= 1
    vlines = vlines[:pre_start] + vlines[post_start:]
    removed += 1
    if removed:
        vnew = "\n".join(vlines)
        if APPLY:
            open(vp, "w", encoding="utf-8").write(vnew)
        p(f"[{'FIX' if APPLY else 'DRY'}] verify_{ind}_calc.js: 移除 {removed} 个用例块")

print("\n".join(log))
print(f"\n模式: {'APPLY (已落盘)' if APPLY else 'DRY-RUN (未改动)'}")
