# -*- coding: utf-8 -*-
"""P4 增强：自动从页面可见文本提取标准公式并注入 formula-box（升 A 级）。

复用 scripts/inject_formula_box.py 的 inject()（幂等，已含 formula-box 则 skip）。
本脚本只负责"自动提取公式 eq"，再调用 inject()。

提取规则（针对质量优化）：
- 仅对 quality=B 且有 function calc、无 formula-box、非重定向桩的页面。
- 从可见正文（去 script/style/tag）找含 = 号且含数字/符号的句子。
- 截断到噪音词（⚠️/本工具/使用说明/注意/例：等）之前。
- 排除无信息量泛模板（基准值/指标加权/预测值=基准/仅供/遵医嘱 等）。
- 长度 6~60 字符。

用法：
  python3 scripts/inject_formula_auto.py --industry statistics --dry-run
  python3 scripts/inject_formula_auto.py --industry statistics
  python3 scripts/inject_formula_auto.py --all --dry-run
"""
import os, re, sys, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inject_formula_box import inject

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools")
import json as _json
TOOLS = _json.load(open(os.path.join(ROOT, "json", "tools.json"), encoding="utf-8"))

CUT = re.compile(r'(⚠️|本工具|使用说明|注意事项|按 Enter|Ctrl|提示：|参考：|注：|常见|例如|例：|建议)')
VAGUE = re.compile(r'(基准值|基准 ?值|指标加权|预测值 = 基准|学习参考|仅供|实际用药|遵医嘱|仅供参考|同时展示差值|稳定性指数综合考虑|留头甩头|复制结果|清空|📋|查询记录|计算历史|计算报告|输入数据|计算评分|输入时请注意|输入时|评分|分级|量表|计算 |总分|平均分)')
EQ = re.compile(
    r'([A-Za-z0-9_.\u4e00-\u9fff\u03b1-\u03c9\u00b2\u00b3\u207f\u221a\u03c0\u03c3\u0394\u2211\u222b\u2202\u03bb\u03bc\u03c1\u03b8\u03b1\u03b2\u03b3\u03c9\u03c6\u03b7\u03c4\u00d7\u00f7\u00b1\u2264\u2265\u2248%]+\s*[=\uff1d\u2248\u2261]\s*.{2,60})')


def vis_text(c):
    c = re.sub(r'<script.*?</script>', '', c, flags=re.S)
    c = re.sub(r'<style.*?</style>', '', c, flags=re.S)
    c = re.sub(r'<[^>]+>', '', c)
    return re.sub(r'\s+', ' ', c).strip()


def extract_eq(c):
    v = vis_text(c)
    best = None
    for m in EQ.finditer(v):
        s = m.group(1).strip()
        cm = CUT.search(s)
        if cm:
            s = s[:cm.start()].strip()
        if len(s) < 6 or len(s) > 60:
            continue
        if VAGUE.search(s):
            continue
        if not re.search(r'[=\uff1d]|[0-9\u00b2\u00b3\u221a\u03c0\u00d7\u00f7%]', s):
            continue
        if best is None or len(s) > len(best):
            best = s
    return best


# 公式域白名单：仅这些非临床专业域自动提取（排除通用/生活/业务域泛模板 + 医学临床域量表噪音）
FORMULA_DOMAINS = set("""
signal quantum metrology aerospace kinematics nuclear optics optical structural geometry
economics securities banking tax insurance accounting surveying energy meteorology realestate
sports math robotics geology investment science hydraulic fire machinery metalwork fishery
procurement language legal statistics fluid thermodynamics dynamics
electromagnetism materials acoustics chemistry civil automotive electrical ballistics
metallurgy textile process quality packaging paper glass paint cable pipe dailychem chemical
seismology astronomy geophysics hydrology railway maritime
""".split())


def candidates(industry=None):
    out = []
    inds = None
    if industry:
        inds = set(industry.split(","))
    for t in TOOLS:
        if t.get("quality") != "B":
            continue
        if inds and t.get("industry") not in inds:
            continue
        if (not inds) and t.get("industry") not in FORMULA_DOMAINS:
            continue
        fp = os.path.join(TOOLS_DIR, t["path"])
        if not os.path.exists(fp):
            continue
        c = open(fp, encoding="utf-8").read()
        if "function calc" not in c:
            continue
        if "formula-box" in c or "TOOLBOX-REDIRECT" in c:
            continue
        eq = extract_eq(c)
        if eq:
            out.append((t["industry"], t["path"].split("/")[-1].replace(".html", ""), eq))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--industry", default=None)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    cands = candidates(args.industry)
    print("可自动提取公式的 B 级候选: %d" % len(cands))
    if args.dry_run:
        for ind, slug, eq in cands:
            print("  [%s] %s  ::  %s" % (ind, slug, eq))
        return
    stats = {}
    for ind, slug, eq in cands:
        r = inject(ind, slug, eq)
        stats[r] = stats.get(r, 0) + 1
    print("注入结果:", stats)


if __name__ == "__main__":
    main()
