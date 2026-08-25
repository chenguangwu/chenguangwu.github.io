#!/usr/bin/env python3
"""从 B 级工具的 HTML/JS 中提炼可读性公式，注入 formula-box 升 A。

策略（零语义风险）：
  针对 JS/HTML 中 *已经写好* 的「公式展示串」（如结果区 .step-line /
  .stat-card 里写的 "IQR = Q3 - Q1"、"τ = R×C"），直接提取为 formula-box，
  而非从计算逻辑反推（反推易错）。

用法：
  python3 scripts/find_b_formulas.py --dry-run     # 仅打印候选，不写入
  python3 scripts/find_b_formulas.py               # 执行注入
"""
import os, re, json, html, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools")
TOOLS_JSON = os.path.join(ROOT, "json", "tools.json")

# 数学符号（公式必备）：含 ASCII、全角/特殊运算符、希腊字母、上下标、函数
MATH = re.compile(r'[+\-*/^×÷√≈·−]|Math\.|[\u00b2\u00b3]|[\u03b1-\u03c9\u0391-\u03a9]'
                  r'|\b(sin|cos|tan|log|ln|sqrt|pow|exp)\b', re.I)
# 说明性噪声词（含这些的不是核心公式）
NOISE = re.compile(r'(步骤|说明|方案|只有|其中|表示|反映|评估|判定|建议|注意|例如|如：|即|换算|查表)')
# 非公式过滤（属性/URL/选择器/CSS/代码关键字）
BAD = re.compile(r'(http|href|src|type=|class=|id=|name=|style=|\[type|@media|'
                 r'content=|charset|viewport|Expires=|Set-Cookie|path=|border|'
                 r'function|return|var |let |const )', re.I)
# 候选： 变量/中文词/希腊字母 = 表达式(3~80字符, 单行, 不含 <>"' ; 换行)
CAND = re.compile(r'([A-Za-z\u4e00-\u9fff\u03b1-\u03c9\u0391-\u03a9][\w\u4e00-\u9fff\u03b1-\u03c9\u0391-\u03a9]*)'
                  r'\s*[=\uff1d]\s*([^<>"\'\n;]{3,80})')


def collect_text(c):
    """只在 HTML 可见文本（去掉 <script>/<style> 后）找公式。
    JS 代码赋值（line=line.slice、camera=() 权限串等）都在 <script> 内，
    会被剔除；真公式展示在 .step-line/.stat-card/.info-box 等文本节点。"""
    c2 = re.sub(r'<script[^>]*>.*?</script>', ' ', c, flags=re.S)
    c2 = re.sub(r'<style[^>]*>.*?</style>', ' ', c2, flags=re.S)
    c2 = re.sub(r'<[^>]+>', ' ', c2)  # 去掉所有标签及属性，只留可见文本
    out = []
    for m in CAND.finditer(c2):
        lhs, rhs = m.group(1), m.group(2).strip()
        if BAD.search(lhs) or BAD.search(rhs):
            continue
        if not MATH.search(rhs):
            continue
        # 取到第一个「说明符」前的「核心公式」；保留数学括号 ( ) [ ] { }
        cut = len(rhs)
        for sep in ['。', '；', '：', '（', '）', '、', '，']:
            j = rhs.find(sep)
            if 3 <= j < cut:
                cut = j
        core = rhs[:cut].strip()
        # 排除非公式（CSS 像素值、日期示例、层级公式被拆坏、残缺 tan(°)）
        if re.search(r'\d{4}-\d{1,2}-\d{1,2}', core):
            continue
        if re.search(r'^\d{1,2}/\d{1,2}$', core):
            continue
        if re.search(r'px', core) and len(lhs) <= 2:
            continue
        if 'tan(°)' in core:
            continue
        # 仅排除 poisson 式被拆坏的层级公式（X = k) = ...），不误杀 Z=(X-μ)/σ 等合法公式
        if lhs in ('X', 'Y', 'Z') and (core.startswith(')') or ') =' in core or core.startswith('k)')):
            continue
        # 排除示例数值/多句说明/题干/条件/残缺括号
        if '→' in core or '；' in core:
            continue
        if re.search(r'香蕉|火车|手表|水果|交通工具|测量工具', core):
            continue
        if '当' in core or '当' in lhs:
            continue
        # 排除括号不配平的残缺公式（如 MD = -6.5)）
        if core.count('(') != core.count(')') or core.count('[') != core.count(']'):
            continue
        # 排除以运算符结尾的残缺公式
        if core.endswith(('÷', '×', '+', '-', '/', '*', '^', '(', '[')):
            continue
        if len(core) < 3:
            continue
        full = "%s = %s" % (lhs, core)
        if len(full) > 120:
            continue
        out.append(full)
    # 去重保序
    seen, uniq = set(), []
    for x in out:
        if x not in seen:
            seen.add(x)
            uniq.append(x)
    return uniq


def score(s):
    """评分：数学符号越多越高；含说明词扣分；长度适中。"""
    sc = len(MATH.findall(s))
    if NOISE.search(s):
        sc -= 3
    L = len(s)
    if 12 <= L <= 55:
        sc += 2
    elif L < 12 or L > 70:
        sc -= 1
    return sc


def best_formula(c):
    cands = collect_text(c)
    if not cands:
        return None
    cands.sort(key=score, reverse=True)
    return cands[0]


def inject(ind, slug, eq):
    fp = os.path.join(TOOLS_DIR, ind, slug + ".html")
    if not os.path.exists(fp):
        return "missing"
    c = open(fp, encoding="utf-8").read()
    if "formula-box" in c or "TOOLBOX-REDIRECT" in c:
        return "skip"
    # 插入到第一个 <h2> 之后（与 upgrade_b_formula 一致的稳定锚点）
    h2 = re.search(r'(<h2[^>]*>.*?</h2>)', c, re.S)
    if not h2:
        return "no-h2"
    anchor = h2.end()
    fb = ('\n    <div class="formula-box">\n'
          '      <div class="formula-title">\U0001F4D0 计算公式</div>\n'
          '      <div class="formula-eq">%s</div>\n'
          '    </div>' % html.escape(eq))
    c2 = c[:anchor] + fb + c[anchor:]
    open(fp, "w", encoding="utf-8").write(c2)
    return "ok"


def main():
    dry = "--dry-run" in sys.argv
    data = json.load(open(TOOLS_JSON, encoding="utf-8"))
    # 只处理 B 级、非重定向
    targets = []
    for t in data:
        if t.get("quality") != "B":
            continue
        if t.get("redirect") or t.get("quality") == "REDIRECT":
            continue
        p = "tools/%s" % t["path"]
        if not os.path.exists(p):
            continue
        c = open(p, encoding="utf-8").read()
        if "TOOLBOX-REDIRECT" in c or "formula-box" in c:
            continue
        eq = best_formula(c)
        if eq:
            targets.append((t["industry"], t["path"].split("/")[-1].replace(".html", ""), eq))
    print("候选 B 级工具(含可读公式):", len(targets))
    ok = skip = miss = noh2 = 0
    for ind, slug, eq in targets:
        if dry:
            print("  %-22s %-34s | %s" % (ind, slug, eq[:70]))
            continue
        r = inject(ind, slug, eq)
        if r == "ok":
            ok += 1
        elif r == "skip":
            skip += 1
        elif r == "missing":
            miss += 1
        else:
            noh2 += 1
            print("  [no-h2] %s/%s  eq=%s" % (ind, slug, eq[:50]))
    if not dry:
        print("注入结果: ok=%d skip=%d missing=%d no-h2=%d" % (ok, skip, miss, noh2))


if __name__ == "__main__":
    main()
