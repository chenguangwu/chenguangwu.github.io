#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 endocrinology 分类 hardcoded 套话与错误元数据：
1) B类套话 "工作与生活中的相关计算与查询。" 在 6 个页面的 FAQ JSON-LD + opt-guide + opt-faq 三处替换为真实场景；
2) calc-1.html 删除指向错误「增值税」指南的 tool-guide-link（指南文件实为增值税，与 HOMA-IR 工具错配）；
3) 修正 toolbox meta 的 cat 错标：finance/validator/math -> health（endocrinology 属健康类）。
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OLD = "工作与生活中的相关计算与查询。"

# 6 个含 B类套话的页面 -> 真实内分泌场景描述（用于三处位置）
REAL_B = {
 "tools/endocrinology/mage-index.html": "解读连续血糖监测(CGM)数据量化日内血糖波动，用于 1 型糖尿病血糖变异性管理与低血糖恐惧患者的波动优化。",
 "tools/endocrinology/short-stature-prediction.html": "评估儿童身高偏离的遗传靶身高与生长潜力，结合骨龄辅助矮小症筛查与生长激发试验指征判断。",
 "tools/endocrinology/graves-trab.html": "鉴别甲亢病因（Graves 病 vs 其他）、预测抗甲状腺药物停药后复发，以及监测妊娠期胎儿/新生儿甲亢风险。",
 "tools/endocrinology/calcium-pth-axis.html": "鉴别高钙血症病因（原发性甲旁亢 vs 恶性/肉芽肿病）与慢性肾病继发性甲旁亢等钙磷代谢紊乱。",
 "tools/endocrinology/detector-metabolism.html": "筛查阵发性高血压（嗜铬细胞瘤）与儿童腹痛高血压（神经母细胞瘤）等儿茶酚胺分泌性肿瘤。",
}

# toolbox meta cat 错标修正：原串 -> 新串
CAT_FIX = {
 "tools/endocrinology/frax-score.html": ("cat=finance,industry=endocrinology", "cat=health,industry=endocrinology"),
 "tools/endocrinology/detector-metabolism.html": ("cat=validator,industry=endocrinology", "cat=health,industry=endocrinology"),
 "tools/endocrinology/cycle-hormone.html": ("cat=math,industry=endocrinology", "cat=health,industry=endocrinology"),
}

GUIDE_RE = re.compile(r'\s*<div class="tool-guide-link" data-guide-link="1">\s*<a href="\.\./\.\./guides/calc-1-guide\.html">📖 查看「增值税计算使用指南」</a>\s*</div>')

def main():
    # 1) B类清理
    for rel, real in REAL_B.items():
        fp = os.path.join(ROOT, rel)
        s = open(fp, encoding="utf-8").read()
        n = s.count(OLD)
        if n == 0:
            print(f"  [skip B] {rel}: 无套话")
            continue
        s = s.replace(OLD, real)
        assert s.count(OLD) == 0
        open(fp, "w", encoding="utf-8").write(s)
        print(f"  [ok B] {rel}: 替换 {n} 处")
    # 2) calc-1 指南链接删除
    fp = os.path.join(ROOT, "tools/endocrinology/calc-1.html")
    s = open(fp, encoding="utf-8").read()
    if GUIDE_RE.search(s):
        s = GUIDE_RE.sub("", s)
        open(fp, "w", encoding="utf-8").write(s)
        print("  [ok] calc-1.html: 删除错误的增值税指南链接")
    else:
        print("  [skip] calc-1.html: 未匹配指南链接块")
    # 3) cat 修正
    for rel, (a, b) in CAT_FIX.items():
        fp = os.path.join(ROOT, rel)
        s = open(fp, encoding="utf-8").read()
        if a in s:
            s = s.replace(a, b)
            open(fp, "w", encoding="utf-8").write(s)
            print(f"  [ok cat] {rel}: {a} -> {b}")
        else:
            print(f"  [skip cat] {rel}: 未找到 {a}")
    print("hardcode 清理完成")

if __name__ == "__main__":
    main()
