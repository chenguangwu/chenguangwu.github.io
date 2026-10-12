#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具页「交互形态基线测绘」（只读，不改任何文件）。

用途：为 DEV-PLAN 的「工具页功能优化 / 个性化」专项提供客观基线 ——
按分类统计每页具备的「功能模块指纹」，算出交互深度分，找出薄弱页与统一化重灾区。

判定口径（只看 <body> 之后的正文，规避 head 内联 CSS 干扰）：
  chart     : 存在 <canvas> / <svg> / class 含 chart|pie|plot|graph|gauge|bar-|spark
  table     : 存在 <table
  export    : 正文含 导出|复制|下载|保存为|export|copy|clipboard|下载图片
  persist   : 脚本含 localStorage（历史记录 / 收藏 / 记住输入）
  preset    : 正文含 示例|预设|一键填充|常见场景|preset|示例数据
  tabs      : 存在 class 含 tab|step|wizard|accordion
  compare   : 正文含 对比|方案对比|compare|对比表
  faq       : 正文含 常见问题|FAQ|答疑
  crosslink : 正文指向其他工具页（../xxx.html 或 /tools/）的链接数

输出：scripts/_ux_baseline.json + 控制台按分类聚合表（按薄弱页占比降序）
"""
import json
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")

CHART_RE = re.compile(r"<canvas|<svg|class=\"[^\"]*(chart|pie|plot|graph|gauge|spark|bar-)[^\"]*\"", re.I)
TABLE_RE = re.compile(r"<table", re.I)
EXPORT_RE = re.compile(r"导出|复制|下载|保存为|export|clipboard|download", re.I)
PERSIST_RE = re.compile(r"localStorage", re.I)
PRESET_RE = re.compile(r"示例|预设|一键填充|常见场景|preset", re.I)
TABS_RE = re.compile(r"class=\"[^\"]*(tab|step|wizard|accordion)[^\"]*\"", re.I)
COMPARE_RE = re.compile(r"对比|比较|compare", re.I)
FAQ_RE = re.compile(r"常见问题|FAQ|答疑|问与答", re.I)
INPUT_RE = re.compile(r"<(input|select|textarea)\b", re.I)
CROSS_RE = re.compile(
    r'href="(?:(?:\.\./){1,3}(?:tools/)?[a-z0-9\-]+/[a-z0-9\-]+\.html|(?!index\.html)[a-z0-9\-]+\.html)"',
    re.I)
# 指南页不是「工具 → 工具」导流，不计入 crosslink
GUIDE_RE = re.compile(r'guides/', re.I)
SCRIPT_RE = re.compile(r"<script\b[^>]*>(.*?)</script>", re.I | re.S)


def scan_one(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        s = f.read()
    i = s.find("<body")
    body = s[i:] if i >= 0 else s
    # 去掉 script 块后的正文（避免 JS 字符串里的中文误判 FAQ/对比）
    scripts = "".join(SCRIPT_RE.findall(body))
    text = SCRIPT_RE.sub(" ", body)

    feats = {
        "chart": bool(CHART_RE.search(body)),
        "table": bool(TABLE_RE.search(body)),
        "export": bool(EXPORT_RE.search(text)),
        "persist": bool(PERSIST_RE.search(scripts)),
        "preset": bool(PRESET_RE.search(text)),
        "tabs": bool(TABS_RE.search(body)),
        "compare": bool(COMPARE_RE.search(text)),
        "faq": bool(FAQ_RE.search(text)),
    }
    cross = len(set(h for h in CROSS_RE.findall(body) if not GUIDE_RE.search(h)))
    inputs = len(INPUT_RE.findall(body))
    feats["crosslink"] = cross >= 2
    score = sum(1 for v in feats.values() if v)
    return {
        "score": score,
        "feats": feats,
        "inputs": inputs,
        "cross": cross,
        "bytes": len(s),
    }


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    only = args[0] if args else None
    slug_mode = '--slug' in sys.argv
    gate = '--gate' in sys.argv
    rows = []
    for ind in sorted(os.listdir(TOOLS)):
        d = os.path.join(TOOLS, ind)
        if not os.path.isdir(d):
            continue
        if only and ind != only:
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".html"):
                continue
            p = os.path.join(d, fn)
            r = scan_one(p)
            r["ind"] = ind
            r["slug"] = fn[:-5]
            rows.append(r)

    by_ind = defaultdict(list)
    for r in rows:
        by_ind[r["ind"]].append(r)

    feat_names = ["chart", "table", "export", "persist", "preset", "tabs", "compare", "faq", "crosslink"]
    agg = {}
    for ind, rs in by_ind.items():
        n = len(rs)
        weak = sum(1 for r in rs if r["score"] <= 2)
        agg[ind] = {
            "n": n,
            "avg": round(sum(r["score"] for r in rs) / n, 2),
            "weak": weak,
            "weak_pct": round(weak * 100.0 / n, 1),
            "feat": {k: round(sum(1 for r in rs if r["feats"][k]) * 100.0 / n, 1) for k in feat_names},
            "avg_inputs": round(sum(r["inputs"] for r in rs) / n, 2),
        }

    total = len(rows)
    allfeat = {k: round(sum(1 for r in rows if r["feats"][k]) * 100.0 / total, 1) for k in feat_names}
    out = {
        "total": total,
        "avg_score": round(sum(r["score"] for r in rows) / total, 2),
        "weak_total": sum(1 for r in rows if r["score"] <= 2),
        "all_feat_pct": allfeat,
        "by_ind": dict(sorted(agg.items(), key=lambda kv: (-kv[1]["weak"], -kv[1]["n"]))),
    }
    out_path = os.path.join(ROOT, "scripts", "_ux_baseline.json")

    # --gate：与基线快照比对，任何页分数下降即失败（门禁用法）
    if gate:
        base_path = os.path.join(ROOT, "scripts", "_ux_baseline_snapshot.json")
        if not os.path.isfile(base_path):
            print("❌ 缺少基线快照 scripts/_ux_baseline_snapshot.json（先跑一次不带 --gate 生成）")
            sys.exit(2)
        with open(base_path, encoding="utf-8") as f:
            base = json.load(f)
        base_map = {}
        for ind, a in base.get("by_ind", {}).items():
            base_map[ind] = a
        regressed = []
        for ind, a in agg.items():
            b = base_map.get(ind)
            if not b:
                continue
            if a["avg"] + 1e-9 < b["avg"]:
                regressed.append(f"{ind}: 均分 {b['avg']} → {a['avg']}")
            elif a["weak"] > b["weak"]:
                regressed.append(f"{ind}: 薄弱页 {b['weak']} → {a['weak']}")
        if out["avg_score"] + 1e-9 < base["avg_score"]:
            regressed.append(f"全站均分 {base['avg_score']} → {out['avg_score']}")
        if regressed:
            print("❌ UX 门禁失败（分数回退）：")
            for r in regressed[:30]:
                print("   -", r)
            sys.exit(1)
        print(f"✅ UX 门禁通过：全站均分 {base['avg_score']} → {out['avg_score']}（无回退）")
        return

    # 写入策略：单分类扫描不得污染全站基线（否则 --gate 会拿错基线比对）
    if only:
        # 单分类诊断输出写到 .workbuddy/（已 gitignore），避免污染仓库
        ux_dir = os.path.join(ROOT, ".workbuddy", "ux")
        os.makedirs(ux_dir, exist_ok=True)
        ind_path = os.path.join(ux_dir, f"baseline_{only}.json")
        with open(ind_path, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
    else:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)

    # --slug：输出该分类逐页薄弱清单（供批次选页）
    if slug_mode and only:
        rs = sorted(by_ind.get(only, []), key=lambda r: (r["score"], r["slug"]))
        print(f"{only}：{len(rs)} 页，逐页清单（按分数升序 = 最该先改的在前）")
        for r in rs[:200]:
            miss = [k for k, v in r["feats"].items() if not v]
            print(f"  {r['score']}/9  {r['slug']:<44} 缺：{','.join(miss)}")
        return

    print(f"总计 {total} 页，平均交互深度 {out['avg_score']}/9，薄弱页(score<=2) {out['weak_total']} 页")
    print("全站功能覆盖率：", " ".join(f"{k}={v}%" for k, v in allfeat.items()))
    print()
    print(f"{'分类':<18}{'页数':>5}{'均分':>6}{'薄弱':>6}{'薄弱%':>7}{'输入数':>7}")
    for ind, a in list(out["by_ind"].items())[:40]:
        print(f"{ind:<18}{a['n']:>5}{a['avg']:>6}{a['weak']:>6}{a['weak_pct']:>7}{a['avg_inputs']:>7}")


if __name__ == "__main__":
    main()
