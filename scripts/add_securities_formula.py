#!/usr/bin/env python3
"""securities 分类公式框补充（收口批次 C）：为缺框的计算类工具注入真实公式框。
用法：python3 scripts/add_securities_formula.py [--apply]
与 scripts/add_fishery_formula.py 同构：在首个锚点（tip-box/tabs/scale-row/set-row/tool-result/input-row/subject-row）前插入 formula-box。
"""
import argparse
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools", "securities")

ANCHORS = [
    "tip-box", "tabs", "scale-row", "set-row", "tool-result", "input-row", "subject-row",
]

FORMULAS = {
    "beta-calc": (
        "β = Cov(Rs, Rm) / Var(Rm)",
        "用个股与市场收益率序列求协方差，除以市场收益率方差；等价于 β = ρ(s,m)·σs / σm，衡量个股相对市场的系统性风险。",
    ),
    "bond-convexity": (
        "P = Σ CFt / (1+y/f)^t；Macaulay D = (Σ t·PVt / P) / f；修正久期 D* = Macaulay / (1+y/f)；"
        "凸性 = Σ PVt·t(t+1) / (P·(1+y/f)²·f²)",
        "先按每期票息与到期还本折现得债券价格；Macaulay 久期为现金流时间的加权平均（按期折为年）；"
        "凸性刻画久期对利率的二阶敏感度，用于修正价格—收益率曲线的弯曲。",
    ),
    "bond-duration": (
        "Macaulay D = Σ t·PVt / P（期）→ 年 = D / f；修正久期 D* = Macaulay / (1+y/f)",
        "Macaulay 久期 = 各期现金流现值乘以其时间 t 之和除以债券价格；修正久期 = Macaulay 除以 (1+每期收益率)，"
        "表示收益率变动 1% 时价格变动的百分比。",
    ),
    "calc-1": (
        "净盈亏 = 卖出额 − 买入额 − 买入佣金 − 卖出佣金 − 印花税 − 过户费；"
        "佣金 = max(成交额 × 佣金率, 最低佣金)；印花税 = 卖出额 × 税率（仅卖出单边）",
        "买入额 = 买入价×股数、卖出额 = 卖出价×股数；佣金按成交额比例收取且不低于最低佣金；"
        "印花税仅卖出单边征收，过户费按成交额比例双向收取。",
    ),
    "calc-29": (
        "中轨 = MA(N)；上/下轨 = 中轨 ± K × σN；σN = √( Σ(price_i − MA)² / N )",
        "布林带以 N 周期移动平均为中轨、以 K 倍标准差为带宽；价格触及上/下轨分别视为超买/超卖信号，带宽收窄常意味波动率下降。",
    ),
    "position-sizing": (
        "固定风险：股数 = 资金 × 风险% / |入场价 − 止损价|；"
        "凯利：f* = 胜率 − 败率 / 盈亏比（半凯利 = f* / 2）",
        "固定分数法先确定单笔可承受亏损（资金×风险%），再除以每股风险得到仓位；"
        "凯利公式按胜率与盈亏比给出最优下注比例，实务常用半凯利降低回撤。",
    ),
    "technical-indicator": (
        "MA(N) = Σ最近N个收盘价 / N；MACD：DIF = EMA(快) − EMA(慢)、DEA = EMA(DIF, 9)、柱 = (DIF − DEA) × 2；"
        "RSI = 100 − 100 / (1 + 平均涨幅 / 平均跌幅)；KDJ：RSV = (C − L9)/(H9 − L9)×100、K/D 递推平滑、J = 3K − 2D",
        "MA 为 N 日收盘均价；MACD 取快慢 EMA 之差（DIF）与其 9 日 EMA（DEA），柱状为二者差的两倍；"
        "RSI 用平均涨跌幅衡量超买超卖；KDJ 先算 RSV 再做 K/D 平滑，J 线放大信号。",
    ),
}


def build_box(eq, desc):
    return (
        '<div class="card formula-box">\n'
        '  <h3>📐 计算公式</h3>\n'
        '  <div class="formula-eq">%s</div>\n'
        '  <p class="formula-desc">%s</p>\n'
        '</div>\n'
    ) % (eq, desc)


def find_anchor(s):
    for a in ANCHORS:
        m = re.search(
            r'<(?:\w+)\b[^>]*\bclass="[^"]*\b%s\b[^"]*"[^>]*>' % re.escape(a), s)
        if m:
            return m.start()
    return -1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    total = len(FORMULAS)
    done = skipped = 0
    for slug, (eq, desc) in FORMULAS.items():
        fp = os.path.join(TOOLS_DIR, slug + ".html")
        if not os.path.isfile(fp):
            print("  缺失: %s" % slug)
            continue
        s = open(fp, encoding="utf-8").read()
        if 'class="formula-box"' in s:
            skipped += 1
            continue
        pos = find_anchor(s)
        if pos < 0:
            print("  无锚点(跳过): %s" % slug)
            continue
        box = build_box(eq, desc)
        s2 = s[:pos] + box + s[pos:]
        if a.apply:
            open(fp, "w", encoding="utf-8").write(s2)
        done += 1
        print("  补框: %s" % slug)
    print("公式框：已补 %d / 缺框 0 / 跳过(已有) %d（共 %d）" % (done, skipped, total))


if __name__ == "__main__":
    main()
