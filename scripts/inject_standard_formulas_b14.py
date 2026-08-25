#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B-OPT14 · 人工核实后的"真正标准公式"注入。
仅对经人工确认含教科书级标准公式的 B 级工具注入 formula-box，升 A。
幂等：已含 formula-box 则跳过。挂在第一个 <h2> 之后。
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")

BOXES = {
 "accounting/assessor-risk-11.html": """
    <div class="formula-box">
      <div class="formula-title">📐 计算公式（Altman Z-Score 破产风险模型）</div>
      <div class="formula-eq">Z = 1.2·X₁ + 1.4·X₂ + 3.3·X₃ + 0.6·X₄ + 1.0·X₅</div>
      <div class="formula-desc">X₁=营运资本/总资产，X₂=留存收益/总资产，X₃=息税前利润/总资产，X₄=权益市值/总负债，X₅=销售收入/总资产。Z≥2.99 安全区，1.81–2.99 灰色区，&lt;1.81 危险区。</div>
    </div>
""",
 "finance/investment-calculator.html": """
    <div class="formula-box">
      <div class="formula-title">📐 计算公式</div>
      <div class="formula-eq">累计回报率 = (期末价值 − 总投入) / 总投入</div>
      <div class="formula-eq">年化收益率 CAGR = (期末价值 / 总投入)^(1 / 年数) − 1</div>
      <div class="formula-desc">总投入 = 初始投入 + 追加投入。CAGR 已考虑复利；简单年化 = 累计回报率 / 年数（不计复利）。</div>
    </div>
""",
 "finance/calc-2.html": """
    <div class="formula-box">
      <div class="formula-title">📐 计算公式（IRR / NPV）</div>
      <div class="formula-eq">NPV = Σ [ CFₜ / (1 + r)^t ]</div>
      <div class="formula-eq">IRR = 使 NPV = 0 的折现率 r</div>
      <div class="formula-desc">CFₜ 为第 t 期现金流（期初投入为负），r 为折现率。IRR 反映项目实际收益率。</div>
    </div>
""",
 "edu/calc-4.html": """
    <div class="formula-box">
      <div class="formula-title">📐 计算公式</div>
      <div class="formula-eq">剩余权重 = 100 − 当前权重</div>
      <div class="formula-eq">剩余考核平均分 = (目标成绩 − 当前成绩) / 剩余权重 × 100</div>
      <div class="formula-desc">当前成绩按当前权重加权；剩余考核需达到的平均分决定能否达成目标。</div>
    </div>
""",
 "edu/grade-weight-calculator.html": """
    <div class="formula-box">
      <div class="formula-title">📐 计算公式</div>
      <div class="formula-eq">加权总分 = Σ(成绩ᵢ × 权重ᵢ / 100)</div>
      <div class="formula-eq">最终加权平均分 = 加权总分 / (总权重 / 100)</div>
      <div class="formula-desc">权重以百分比计；剩余权重下所需成绩 = (目标 − 已得加权分) / (剩余权重 / 100)。</div>
    </div>
""",
 "endocrinology/calc-1.html": """
    <div class="formula-box">
      <div class="formula-title">📐 计算公式（HOMA 模型）</div>
      <div class="formula-eq">HOMA-IR = (空腹血糖 × 空腹胰岛素) / 22.5</div>
      <div class="formula-eq">HOMA-β = (20 × 空腹胰岛素) / (空腹血糖 − 3.5)</div>
      <div class="formula-desc">空腹血糖单位 mmol/L，空腹胰岛素单位 mU/L。适用于稳定代谢状态成人，不用于胰岛素治疗或 β 细胞衰竭者。</div>
    </div>
""",
 "securities/capm-return.html": """
    <div class="formula-box">
      <div class="formula-title">📐 计算公式（CAPM 资本资产定价模型）</div>
      <div class="formula-eq">E(r) = r_f + β·(r_m − r_f)</div>
      <div class="formula-desc">r_f 无风险利率，β 个股相对市场波动，r_m 市场预期收益率，(r_m − r_f) 市场风险溢价。</div>
    </div>
""",
}

def inject(path, box):
    p = os.path.join(TOOLS, path)
    if not os.path.exists(p):
        print(f"  ✗ 文件不存在: {path}"); return False
    h = open(p, encoding="utf-8").read()
    if "formula-box" in h:
        print(f"  ⊝ 已有 formula-box，跳过: {path}"); return False
    m = re.search(r"<h2[^>]*>.*?</h2>", h, re.S)
    if not m:
        print(f"  ✗ 无 <h2>，无法挂载: {path}"); return False
    idx = m.end()
    # 在 </h2> 后插入（保持缩进风格：前面一个换行+4空格）
    new_box = "\n" + "".join("    " + ln if ln.strip() else ln for ln in box.splitlines(keepends=True))
    h2 = h[:idx]
    rest = h[idx:]
    nh = h2 + new_box + rest
    open(p, "w", encoding="utf-8").write(nh)
    print(f"  ✓ 已注入: {path}")
    return True

def main():
    print(f"注入标准公式框（共 {len(BOXES)} 个候选）")
    done = 0
    for path, box in BOXES.items():
        if inject(path, box):
            done += 1
    print(f"本次实际注入: {done} 个")

if __name__ == "__main__":
    main()
