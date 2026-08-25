#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P3a：给 C 级公式工具注入 formula-box 公式面板，提升质量分级（C→A）。

策略：
- 仅处理「公式域行业 + 质量 C」的工具。
- 从 <h2> 中提取括号里的公式（如 Δf = f_s / N）；提取不到则跳过（不生成破窗面板）。
- 在 intro 段落之后插入 .formula-box（含 计算公式 + 说明）。
- 不改任何计算逻辑，纯增量增强。
"""
import os, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORMULA_INDUSTRIES = {
    "signal", "acoustics", "aerospace", "astronomy", "tax", "materials",
    "structural", "surveying", "electromagnetism", "metrology", "quantum",
    "securities", "energy", "economics", "optics", "geometry", "robotics",
    "kinematics", "dynamics", "nuclear", "math", "optical", "realestate",
    "science", "banking", "insurance", "accounting", "statistics", "chemistry",
    "thermodynamics", "fluid", "process",
}

INTRO_RE = re.compile(
    r'(<p style="font-size:13px;color:var\(--text-muted\);margin-bottom:16px;">.*?</p>)',
    re.S,
)
FORMULA_RE = re.compile(r'[（(]([^（）()]*[=≈∝][^（）()]*)[)）]')
# 回退：h2 中直接出现的「带 = ≈ ∝ 的数学表达式」（无括号包裹）
FORMULA_FALLBACK = re.compile(
    r'[\wΔΩα-ω.+\-*/^()\s≈∝=]{2,}[=≈∝][\wΔΩα-ω.+\-*/^()\s≈∝=]{2,}'
)


def _looks_like_formula(eq):
    return bool(re.search(r'[=≈∝·×÷*/\^αβγδελμπρστφωΔΩ√]', eq))


def extract_formula(h2):
    m = FORMULA_RE.search(h2)
    if m and _looks_like_formula(m.group(1)):
        return m.group(1).strip()
    # 去掉 emoji / 中文描述，仅保留含运算符的数学片段
    fb = FORMULA_FALLBACK.search(h2)
    if fb:
        eq = fb.group(0).strip()
        # 去掉可能前缀的中文/emoji 杂项
        eq = re.sub(r'^[^=≈∝A-Za-zΔΩα-ω\d(]+', '', eq)
        if _looks_like_formula(eq):
            return eq
    return None


def main():
    t = json.load(open(os.path.join(ROOT, "json", "tools.json")))
    targets = [
        (x["industry"], x["file"])
        for x in t
        if x.get("quality") == "C" and x["industry"] in FORMULA_INDUSTRIES
    ]
    print("候选 C 级公式工具：", len(targets))

    added = 0
    skipped = 0
    for ind, f in targets:
        path = os.path.join(ROOT, "tools", ind, f)
        if not os.path.exists(path):
            skipped += 1
            continue
        s = open(path, encoding="utf-8").read()
        if "formula-box" in s:
            skipped += 1
            continue
        h2m = re.search(r"<h2>(.*?)</h2>", s, re.S)
        if not h2m:
            skipped += 1
            continue
        eq = extract_formula(h2m.group(1))
        if not eq:
            skipped += 1
            continue
        intro_m = INTRO_RE.search(s)
        if not intro_m:
            skipped += 1
            continue
        desc = re.sub(r"<[^>]+>", "", intro_m.group(1)).strip()
        box = (
            '\n\n    <div class="formula-box">\n'
            '      <div class="formula-title">📐 计算公式</div>\n'
            f'      <div class="formula-eq">{eq}</div>\n'
            f'      <p class="formula-desc">{desc}</p>\n'
            "    </div>\n"
        )
        s2 = s[: intro_m.end()] + box + s[intro_m.end():]
        open(path, "w", encoding="utf-8").write(s2)
        added += 1
    print(f"已注入 formula-box：{added}；跳过：{skipped}")


if __name__ == "__main__":
    main()
