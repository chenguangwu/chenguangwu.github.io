#!/usr/bin/env python3
"""幂等下架 19 个「模板短名 vs 专名」系统双命名冗余工具（保留更全的专名版）。

取证（语义层，非仅 h1 同名）：
  全站 h1 归一化模糊聚类（>=0.82）得 387 相似对；其中 108 对同目录且差异仅在于
  「器/计/算」后缀 + 全半角括号 —— 典型的机器模板命名（calc-N/rater-N/analysis-N/
  convert-N/assessor-N/拼音长串/date-diff 等）与描述性专名（bishop-score/ovarian-reserve…）
  双命名重复。逐对比对 calc 真实输入集：
    - 0 对字节/结构完全相同（75 对不同输入、33 查表型）
    - 但专名版的「真实用户输入集」是模板版超集（删模板不丢任何功能）的 19 对 → 本批删除
    - 其余 49+38 对涉及全局复用编号页(calc-N 30+行业)或描述性短名(date-diff vs
      date-difference-calculator)等，需更细的 canonical 规则，单列后续处理。

保留方（权威页）均在 tools.json 重建后保留；本批仅删冗余模板方，URL 移除但该工具仍有
专名页服务同一查询，属低影响、不涉 SEO 风险。

清理范围（避免线上残留入口/断链/门禁失败）：
  - 源 HTML：tools/<ind>/<slug>.html；中文指南 guides/<slug>-guide.html（.en.html 留专项）
  - 其它页 chip 硬链接（含 .en.html 内部指向已删工具者）
  - json/guides.json 注册项（tool == <slug>.html）
  - i18n/tools/<ind>.json（裸 slug）+ <ind>-body.json
  - i18n/tools/_en_override.json / slug-en.json / _en_desc.json / content_deepdive.json（<ind>/<slug>）
  - scripts/enmap/<ind>.json（裸 slug）
  - i18n/locale-zh-TW.json（<ind>.<slug>.* 前缀）
  - scripts/verify_*.js 用例块（slug 或 <ind>/<slug>，基于行括号计数）
  - zh-tw 残留繁体产物（find zh-tw -name '*slug*' -delete）
所有 JSON 重排均按原文 detect 的 indent + trailing newline 保格式。
"""
import os, re, json, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = "--apply" in sys.argv
log = []

# (industry, slug) —— 专名版为模板版真实输入超集，且 basename 未跨行业全局复用
ITEMS = [
    ("cardiology", "rater-11"),            # -> has-bled
    ("cosmetic-derm", "aging-1"),          # -> glogau-photoaging
    ("dermatology", "rater-29"),           # -> insect-bite-reaction
    ("gastroenterology", "rater-14"),       # -> mayo-score
    ("neurology", "assessor-11"),           # -> midas
    ("neurology", "rater-20"),              # -> qmg
    ("obstetrics", "assessor-12"),          # -> ovarian-reserve
    ("obstetrics", "due-date-1"),           # -> due-date
    ("obstetrics", "gestational"),          # -> gestational-age
    ("obstetrics", "rater-25"),             # -> bishop-score
    ("pediatrics", "tester-6"),             # -> pediatric-asthma
    ("pulmonology", "assessor-8"),          # -> gina-asthma
    ("rehabilitation", "assessor-2"),       # -> boston-aphasia
    ("rehabilitation", "rater-2"),          # -> flacc-scale
    ("reproductive-medicine", "rater-30"),  # -> testicular-biopsy
    ("reproductive-medicine", "rater-31"),  # -> embryo-grading
    ("tcm-chemistry", "convert-41"),        # -> toxicity-dose
    ("tcm-pharmacy", "assessor-3"),         # -> tcm-adr-assessment
    ("urology", "rater-3"),                 # -> ipss-score
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

# ── 2) 清理其它页的 chip 硬链接 ─────────────────────────────────
slug_re = "|".join(re.escape(s) for _, s in ITEMS)
chip_pat = re.compile(
    r'<a class="tool-chip"[^>]*href="[^"]*(?:tools/(?:%s)/(?:%s)\.html|guides/(?:%s)-guide(?:\.html|\.en\.html))"[^>]*>.*?</a>'
    % (slug_re, slug_re, slug_re)
)
deleted_guides = {f"{s}-guide.html" for _, s in ITEMS}
for sub in ["guides", "tools"]:
    d = os.path.join(ROOT, sub)
    if not os.path.isdir(d):
        continue
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".html"):
            continue
        fp = os.path.join(d, fn)
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
# 用例 slug 书写格式不统一（可能 "slug": "x" / slug:"x" / slug: "x"，且 { 可能
# 与 slug 同行内联），统一按带引号的值 "ind/slug" 定位，再向上找最近的 {（含
# slug 所在行），从字符级括号计数定匹配 }，支持嵌套 {}。
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
        # 向上找最近的 {（含 slug 所在行，兼容内联 { slug:）
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
