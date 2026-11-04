#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量表总账自动核对（只报不改）

对 tools/ 下带评分标尺（refBar）或「满分」自述的量表页做三项静态核对：
  1) 满分不符：各条目最大分值之和 ≠ 页面自述满分；
  2) 切点未覆盖：refBar 相邻档位 hi 与下一档 lo 不衔接（断档/重叠）；
  3) 档位不可达：最高档下界 > 满分（该档永远进不去），或首档 lo != 0。

用法：
  python3 scripts/audit_scale_ledger.py                 # 扫全部行业
  python3 scripts/audit_scale_ledger.py neurology psychiatry
  python3 scripts/audit_scale_ledger.py --json /tmp/x.json

判定口径（保守，输出供人工筛，不自动改页）：
  - 条目最大分来源优先级：静态 <select> 的 option value 最大值 → JS 循环
    `for(var s=0;s<=N;s++)` → 标签「（0–N分）」→ `o:[…]` 数组；
  - 自述满分优先取「满分 N」，其次「N 分制」「总分 0–N」；
  - 同一页出现多个自述满分（如分表/子量表）时，取与条目和最接近的那个并标注。
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")
INDUSTRIES = [
    "neurology", "psychiatry", "rheumatology", "pulmonology", "dentistry",
    "cardiology", "clinical-nursing", "rehabilitation", "urology", "dermatology",
    "obstetrics", "healthcare", "pediatrics",
]

SELECT_RE = re.compile(r"<select[^>]*>(.*?)</select>", re.S | re.I)
OPTION_RE = re.compile(r'<option[^>]*value="(?:-|−)?(\d+(?:\.\d+)?)"', re.I)
LOOP_RE = re.compile(r"for\s*\(\s*var\s+\w+\s*=\s*0\s*;\s*\w+\s*<=\s*(\d+)\s*;\s*\w+\+\+\s*\)")
RANGE_LABEL_RE = re.compile(r"（\s*0\s*[–\-~—]\s*(\d+)\s*分\s*）")
RADIO_RE = re.compile(r'<input[^>]*type="radio"[^>]*>', re.I)
ATTR_RE = re.compile(r'(\w+)\s*=\s*"([^"]*)"')
CLAIM_RES = [
    re.compile(r"满分[^=]{0,24}=\s*(\d+(?:\.\d+)?)"),
    re.compile(r"满分[^0-9×]{0,6}(\d+(?:\.\d+)?)"),
    re.compile(r"(\d+(?:\.\d+)?)\s*分制"),
    re.compile(r"总分\s*0\s*[–\-~—]\s*(\d+(?:\.\d+)?)"),
]
BANDS_RE = re.compile(r"bands\s*:\s*\[(.*?)\]\s*\}", re.S)
BAND_ITEM_RE = re.compile(r"\{[^{}]*?lo\s*:\s*([^,]*)[^{}]*?hi\s*:\s*([^,}]*)[^{}]*\}")
IF_RE = re.compile(r"total\s*(>=|<=|>|<)\s*(\d+(?:\.\d+)?)")


def read(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def num(x):
    x = str(x).strip().strip('"\'')
    if x in ("null", "None", "undefined", ""):
        return None
    try:
        v = float(x)
        return int(v) if v == int(v) else v
    except ValueError:
        return None


def parse_item_maxes(html):
    """返回 (条目最大分之和, 依据说明) 或 (None, ...)"""
    # 0a) JS 数组型条目（o:[…] / opts|options:[{v}]）优先于动态模板判定
    arr0 = []
    for m in re.finditer(r"o\s*:\s*\[([^\]]*)\]([^}]{0,200})", html):
        n = len(re.findall(r"['\"]", m.group(1))) // 2
        vm = re.search(r"v\s*:\s*\[([^\]]*)\]", m.group(2))
        if vm:
            vs = [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", vm.group(1))]
            if vs:
                arr0.append(max(vs))
        elif n >= 2:
            arr0.append(n - 1)
    opt0 = []
    for a in re.findall(r"(?:options|opts)\s*:\s*\[(.*?)\]\s*[,}]", html, re.S):
        vs = [float(x) for x in re.findall(r"v\s*:\s*(\d+(?:\.\d+)?)", a)]
        if vs:
            opt0.append(max(vs))
    if len(arr0) >= 2:
        return sum(arr0), f"{len(arr0)} 个 o:[…] 选项数组（有 v 用真实分，否则按下标）"
    if len(opt0) >= 2:
        return sum(opt0), f"{len(opt0)} 个 opts/options:[{{v}}] 选项组"

    # 0b) JS 循环生成 select：for(var s=0;s<=5;s++) + questions 数组
    loops = [int(x) for x in LOOP_RE.findall(html)]
    qmatch = re.search(r"var\s+questions\s*=\s*\[(.*?)\];", html, re.S)
    if loops and qmatch:
        nq = len(re.findall(r"['\"]", qmatch.group(1))) // 2
        if nq:
            return loops[0] * nq, f"{nq} 题 × 循环上限 {loops[0]}"

    # 1) 静态 select（≥3 才算真实条目；动态页残留模板通常只有 1–2 个）
    sel_max = []
    for m in SELECT_RE.finditer(html):
        vals = [float(v) for v in OPTION_RE.findall(m.group(1).replace("−", "-"))]
        if vals:
            sel_max.append(max(vals))
    if len(sel_max) >= 3:
        # 计分 checkbox：仅统计标签里明写分值的（如「糖尿病 (1分)」）
        cb_hits = re.findall(r'<input[^>]*type="checkbox"[^>]*>(.{0,60}?)'
                             r'(?:</label>|</div>|</p>)', html, re.S | re.I)
        cb_max = sum(float(x) for s in cb_hits for x in re.findall(r"[（(]\s*(\d+(?:\.\d+)?)\s*分", s))
        # 同标签内 `<span class="score-pts">+N</span>` 形态（TIMI 等）；有则以其为准，避免与标签「N分」重复计
        pts = [float(x) for x in re.findall(
            r'class="score-pts"[^>]*>\s*[+＋]?\s*(\d+(?:\.\d+)?)', html)]
        if pts:
            cb_max = sum(pts)
        # number input 的 max（如疼痛 0–10 直接填分数）
        num_max = sum(float(m) for m in re.findall(
            r'<input[^>]*type="number"[^>]*max="(\d+(?:\.\d+)?)"', html, re.I))
        # 显式加权项：label 含「×2」的紧随 select，其最大分再计一次（如 TWSTRS 持续时间）
        extra = 0
        for m in re.finditer(r'<label>(.*?)</label>(.*?)</select>', html, re.S | re.I):
            if '×2' in m.group(1) or '× 2' in m.group(1):
                vals = [float(v) for v in OPTION_RE.findall(m.group(2).replace("−", "-"))]
                if vals:
                    extra += max(vals)
        parts = [f"{len(sel_max)} 个静态 select"]
        if cb_max: parts.append(f"checkbox +{cb_max:g}")
        if num_max: parts.append(f"number max +{num_max:g}")
        if extra: parts.append(f"加权项 ×2 +{extra:g}")
        return sum(sel_max) + cb_max + num_max + extra, " + ".join(parts)

    # 2) 模板串 + questions 数组：`<select id="q${i}">` × 9 题（PHQ-9/IPSS 等）
    qarr = re.search(r"questions\s*=\s*\[(.*?)\];", html, re.S)
    tpl_sel = re.search(r"<select[^>]*\$\{[^>]*>((?:(?!</select>).)*)</select>",
                        html, re.S | re.I)
    if qarr and tpl_sel:
        n = len(re.findall(r"'[^']{3,}'|\"[^\"]{3,}\"", qarr.group(1)))
        # 优先取 opts 数组的真实分值（模板 select 只是渲染壳）
        op = re.search(r"opts\s*=\s*\[(.*?)\];", html, re.S)
        vals = [float(x) for x in re.findall(r"v\s*:\s*(\d+(?:\.\d+)?)", op.group(1))] if op else []
        if not vals:
            vals = [float(v) for v in OPTION_RE.findall(tpl_sel.group(1).replace("−", "-"))]
        if n >= 2 and vals:
            return n * max(vals), f"{n} 题 × 单题上限 {max(vals):g}"

    # 3) 构造式声明：N 项/题 × 每项 0–M；括号内逐项上限；权重合计 × 程度
    decl = parse_declared_composition(html)
    if decl[0] is not None:
        return decl

    # 4) 动态生成 select（JS 拼接/模板串/createElement）：静态 select 只是残留模板，不能当条目
    if re.search(r"<select[^>]*id=\"[^\"]*'\s*\+\s*\w+", html) or \
       re.search(r"<select[^>]*id=\"[^\"]*\$\{\w+\}" , html) or \
       "createElement('select')" in html or 'createElement("select")' in html:
        return None, "动态生成条目（静态 select 为模板，不计入）"

    # 4) radio 单选组：按 name 分组取组内最大 value，再求和（PHQ-9、HAS-BLED 等）
    groups = {}
    for tag in RADIO_RE.findall(html):
        at = dict(ATTR_RE.findall(tag))
        name, val = at.get("name"), num(at.get("value", ""))
        if name and val is not None:
            groups[name] = max(groups.get(name, 0), float(val))
    if len(groups) >= 2:
        # 同页 checkbox 按 1 分计（代码形如 `renal?1:0`）
        cb_plain = 0
        if re.search(r"\.checked\s*\?\s*1\s*:\s*0", html):
            cb_plain = html.count('<input type="checkbox"')
        return sum(groups.values()) + cb_plain, \
            f"{len(groups)} 个 radio 组（组内取最大）" + (f" + {cb_plain} 个 checkbox(1分)" if cb_plain else "")

    # 5) 标签「（0–N分）」，N 上限 30，避免把「0-100分」进度条文案计入
    labels = [int(x) for x in RANGE_LABEL_RE.findall(html) if int(x) <= 30]
    if len(labels) >= 2:
        return sum(labels), f"{len(labels)} 个「0–N分」条目标签"
    return None, "无法静态解析条目最大分"


def parse_declared_composition(html):
    """从页面自述公式推断总分上限（构造式量表）。

    支持四类口径：
      A 均匀条目：`15 个神经功能项目…满分 42` / `8 个问题（每项 0 至 5）`
      B 逐项上限：`（步态 0–8 / 站立 0–6 / 坐位 0–4 …）`
      C 加权合计：`权重合计 21` + `程度 0–3` → 21×3
      D 题数×单题上限：`满分 = 题数×4` + `共 25 题`
    """
    # B0 「A 项 + B 项 + C 项之和（每项 0–M 分）」→ 项数合计 × 单题上限（WOMAC 等）
    m = re.search(r"([^。；\n]{0,90}?)之和\s*（\s*每项\s*0\s*[–\-~—]\s*(\d+)", html)
    if m:
        ns = [int(x) for x in re.findall(r"(\d+)\s*项", m.group(1)) if 0 < int(x) < 60]
        if len(ns) >= 2:
            return sum(ns) * int(m.group(2)), f"{'+'.join(map(str, ns))} 项 × 每项上限 {m.group(2)}"

    # B0' 「N 项 × 1–M」/「N 项×1-7」（FIM 等：每项最低 1 分）
    m = re.search(r"(\d+)\s*项\s*[×x*]\s*1\s*[–\-~—]\s*(\d+)", html)
    if m:
        return int(m.group(1)) * int(m.group(2)), f"{m.group(1)} 项 × 1–{m.group(2)}（按上限计）"

    # B 逐项上限（括号内至少 3 段「X 0–N」）
    for par in re.findall(r"（([^（）]{10,200})）", html):
        rs = [int(x) for x in re.findall(r"[^\s，、/／]+\s*0\s*[–\-~—]\s*(\d+)", par)]
        if len(rs) >= 3:
            return sum(rs), f"括号内 {len(rs)} 项逐项上限求和"

    # A 均匀条目：N 项/题/个问题 + 每项 0–M
    m = re.search(r"(\d+)\s*(?:个)?(?:项|题|条|个问题|个条目)[^。；\n]{0,40}?"
                  r"每(?:\s*项|\s*题|\s*条)?\s*(?:0\s*(?:至|[–\-~—])\s*(\d+))", html)
    if m:
        n, hi = int(m.group(1)), int(m.group(2))
        if n >= 2 and hi >= 1:
            return n * hi, f"{n} 项 × 每项上限 {hi}"

    # A' `N 个问题（每项 0 至 5）`
    m = re.search(r"(\d+)\s*个(?:问题|条目)\s*（\s*每项\s*0\s*至\s*(\d+)", html)
    if m:
        return int(m.group(1)) * int(m.group(2)), f"{m.group(1)} 项 × 每项上限 {m.group(2)}"

    # C 加权合计 × 程度上限
    w = re.search(r"权重合计\s*(\d+(?:\.\d+)?)", html)
    g = re.search(r"程度\s*0\s*[–\-~—]\s*(\d+)", html)
    if w and g:
        return float(w.group(1)) * int(g.group(1)), f"权重合计 {w.group(1)} × 程度上限 {g.group(1)}"

    # D 满分 = 题数 × M
    m = re.search(r"满分\s*=\s*题数\s*×\s*(\d+)", html)
    if m:
        n = re.search(r"共?\s*(\d+)\s*题", html)
        if n:
            return int(n.group(1)) * int(m.group(1)), f"{n.group(1)} 题 × {m.group(1)}"
    return None, ""


def parse_claims(html):
    claims = []
    for rx in CLAIM_RES:
        for m in rx.finditer(html):
            v = num(m.group(1))
            if v is not None and v > 0:
                claims.append(float(v))
    # 去重保序
    out = []
    for c in claims:
        if c not in out:
            out.append(c)
    return out


def parse_bands(html):
    m = BANDS_RE.search(html)
    if not m:
        return []
    bands = []
    for b in BAND_ITEM_RE.finditer(m.group(1)):
        lo, hi = num(b.group(1)), num(b.group(2))
        bands.append((lo, hi))
    return bands


def parse_if_thresholds(html):
    th = []
    for op, v in IF_RE.findall(html):
        th.append((op, float(v)))
    return th


def classify_mode(html, path=""):
    """区分「逐项求和」与「序数/成分/加权/动态」量表，后者不适用简单满分求和。"""
    base = os.path.basename(path).lower()
    if base == "edss.html":
        return '序数量表（非求和）'
    if re.search(r"C[1-7]\b", html) and '成分' in html:
        return '成分计分（非逐项求和）'
    if ('权重' in html or '加权' in html) and ('Σ' in html or '×' in html):
        return '加权量表'
    if html.count('<input type="radio"') >= 4:
        return 'radio 单选计分'
    if 'ACT' in html and 'GINA' in html:
        return '同页多量表'
    if 'createElement(\'select\')' in html or 'createElement("select")' in html:
        return '动态生成条目'
    # JS 字符串拼接 / 模板串生成 select（id 内出现 `'+i+'` 或 `${i}`）
    if re.search(r"<select[^>]*id=\"[^\"]*'\s*\+\s*\w+", html) or \
       re.search(r"<select[^>]*id=\"[^\"]*\$\{\w+\}", html):
        return '动态生成条目'
    return '逐项求和'


def audit_page(path, html):
    issues = []
    mode = classify_mode(html, path)
    item_max, basis = parse_item_maxes(html)
    # radio / 动态生成的页面只要总账能静态还原条目上限，就纳入求和核对
    if item_max is not None and mode in ('radio 单选计分', '动态生成条目'):
        mode = '逐项求和（已补解析）'
    claims = parse_claims(html)
    band = parse_bands(html)

    # ---- 满分核对 ----
    if item_max is not None and claims:
        claim = min(claims, key=lambda c: abs(c - item_max))
        if abs(claim - item_max) > 1e-6:
            issues.append({
                "type": "满分不符",
                "detail": f"自述满分 {claim:g}，条目最大分之和 {item_max:g}（{basis}）",
            })

    # ---- 档位衔接 ----
    if band:
        bs = sorted(band, key=lambda x: (x[0] is None, x[0] if x[0] is not None else 0))
        for i in range(len(bs) - 1):
            lo_i, hi_i = bs[i]
            lo_n, hi_n = bs[i + 1]
            if hi_i is None:
                issues.append({"type": "切点未覆盖", "detail": f"第 {i+1} 档 hi=null 却仍有后续档"})
            elif lo_n is None:
                continue
            elif abs(float(hi_i) - float(lo_n)) > 1e-6:
                issues.append({
                    "type": "切点未覆盖",
                    "detail": f"第 {i+1} 档 [{lo_i:g},{hi_i:g}) 与第 {i+2} 档起点 {lo_n:g} "
                              f"{'断档' if float(hi_i) < float(lo_n) else '重叠'}",
                })
        if bs[-1][1] is not None:
            issues.append({"type": "切点未覆盖", "detail": f"最高档 hi={bs[-1][1]:g} 非开放区间"})
        # 不可达 / 起点异常
        top_lo = bs[-1][0]
        ref_max = item_max if item_max is not None else (claims[0] if claims else None)
        if ref_max is not None and top_lo is not None and float(top_lo) > float(ref_max):
            issues.append({
                "type": "档位不可达",
                "detail": f"最高档下界 {top_lo:g} > 满分 {ref_max:g}，该档永远进不去",
            })
        if bs[0][0] is not None and float(bs[0][0]) != 0:
            issues.append({"type": "切点未覆盖", "detail": f"首档下界 {bs[0][0]:g} ≠ 0"})

    # ---- if 阈值链 ----
    if not band and item_max is not None:
        ops = parse_if_thresholds(html)
        ups = [v for op, v in ops if op in (">=", ">")]
        if ups:
            top = max(ups)
            if top > item_max:
                issues.append({
                    "type": "档位不可达",
                    "detail": f"最高档判定 total>{top:g}，但满分仅 {item_max:g}",
                })
    if mode not in ('逐项求和', '逐项求和（已补解析）'):
        issues = [{"type": "跳过", "detail": f"{mode}：不适用简单满分求和核对"}]
    return {
        "page": os.path.relpath(path, ROOT),
        "mode": mode,
        "item_max": item_max,
        "basis": basis,
        "claims": claims,
        "bands": band,
        "issues": issues,
    }


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    out_json = "/tmp/scale_ledger.json"
    if "--json" in sys.argv:
        out_json = sys.argv[sys.argv.index("--json") + 1]
    inds = args or INDUSTRIES
    results = []
    for ind in inds:
        d = os.path.join(TOOLS, ind)
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if not name.endswith(".html") or name == "index.html":
                continue
            path = os.path.join(d, name)
            html = read(path)
            if "refBar" not in html and "满分" not in html:
                continue
            results.append(audit_page(path, html))

    real = [r for r in results if r["issues"] and r["issues"][0]["type"] != "跳过"]
    skipped = [r for r in results if r["issues"] and r["issues"][0]["type"] == "跳过"]
    print(f"扫描量表候选页 {len(results)} 个：逐项求和 {len(results)-len(skipped)} 个，"
          f"非求和/动态 {len(skipped)} 个（已跳过）")
    print(f"检出偏差 {len(real)} 页 / {sum(len(r['issues']) for r in real)} 条\n")
    dev = real
    for r in skipped[:5]:
        print(f"· 跳过 {r['page']}：{r['issues'][0]['detail']}")
    for r in dev[:10]:
        print(f"■ {r['page']}  （条目最大分={r['item_max']}，自述={r['claims']}，{r['basis']}）")
        for it in r["issues"]:
            print(f"    [{it['type']}] {it['detail']}")
    if len(dev) > 10:
        print(f"\n…… 其余 {len(dev)-10} 页见 {out_json}")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(dev, f, ensure_ascii=False, indent=2)
    print(f"\n完整结果：{out_json}")


if __name__ == "__main__":
    main()
