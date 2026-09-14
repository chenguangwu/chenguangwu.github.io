#!/usr/bin/env python3
"""Run the ToolBox build and release quality gates in a fixed order.

The runner deliberately performs no Git or index-submission actions. It is
safe to use locally and from CI, and it stops at the first failed gate while
preserving the original command output and exit code.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


GATES = (
    ("build", ("python3", "_build.py")),
    ("static tests", ("python3", "_test_static.py")),
    ("dead-link audit", ("python3", "_audit_links.py", "--check")),
    ("asset audit", ("python3", "_audit_assets.py", "--check")),
    ("calculation regression", ("node", "scripts/verify_calc.js")),
    # 与上一项区别：verify_calc 是「冒烟」（不报错即可），本项是「正确性」
    # ——注入已知输入后按权威测试向量断言输出（§4.1.1）。用例写在脚本内，逐分类扩充。
    ("it calc correctness", ("node", "scripts/verify_it_calc.js")),
    # general 分类的正确性验证（工程标准公式 / 独立复算），与 it 分开维护用例集。
    ("general calc correctness", ("node", "scripts/verify_general_calc.js")),
    # finance 分类的正确性验证（校验位算法 / 金融公式），用例集独立维护。
    ("finance calc correctness", ("node", "scripts/verify_finance_calc.js")),
    # design 分类的正确性验证（单位换算 / 色度学 / 摄影光学），用例集独立维护。
    ("design calc correctness", ("node", "scripts/verify_design_calc.js")),
    # science 分类的正确性验证（经典力学 / 电学 / 化学 / 统计），用例集独立维护。
    ("science calc correctness", ("node", "scripts/verify_science_calc.js")),
    # sports 分类的正确性验证（力量 1RM / VO2max / 心率 / 氧脉搏 / 齿比 / 坡度 / SWOLF / 出汗率）。
    ("sports calc correctness", ("node", "scripts/verify_sports_calc.js")),
    # fun 分类的正确性验证（烧烤/火锅分量、冥想分段、婚宴桌数、步幅速度换算）。
    ("fun calc correctness", ("node", "scripts/verify_fun_calc.js")),
    # ai 分类的正确性验证（混淆矩阵四指标 / 欧氏曼哈顿余弦 / 交叉熵 / Sigmoid / Softmax /
    # Cohen's Kappa / AUC 秩次 / 学习率衰减 / Transformer 参数量）。
    ("ai calc correctness", ("node", "scripts/verify_ai_calc.js")),
    # biz 分类的正确性验证（服务质量加权评分 / 会议人·小时成本 / 岗位权重胜任力 /
    # 单价单位归一化 / 风险矩阵分级 / 演示计时均分 / 定长折行 / 字符画视觉宽度）。
    ("biz calc correctness", ("node", "scripts/verify_biz_calc.js")),
    # life 分类的正确性验证（停车计费封顶 / 百分比 / 温度换算 / Mifflin 热量 / 饮水计划 /
    # 罩杯换算 / 日期差含端日 / 生日悖论 / 闰年规则 / 单位因子换算 / 选址加权模型）。
    ("life calc correctness", ("node", "scripts/verify_life_calc.js")),
    # agriculture 分类的正确性验证（作物需水 ETc / 肥料表观利用率 / 农机油耗 / 存栏密度 /
    # 土壤有机质 / 水肥 EC 注肥比例 / 干物质换算 / 光照积分 DLI / 收获损失率 / 配比十字交叉 /
    # 肥料当季利用率差减法 / 连作障碍指数）。
    ("agriculture calc correctness", ("node", "scripts/verify_agriculture_calc.js")),
    # hydraulic 分类的正确性验证（伯努利求流速 / 连续性变径 / 达西-魏斯巴赫 / Hazen-Williams /
    # 曼宁明渠 / 局部水头损失 / 水泵功率 / 矩形堰 / 由流量求流速 / 明渠均匀流 / 能量分解 /
    # 水力发电 / 泵站效率 / 蓄能器容量 / 水锤防护 / 液压伺服 / 水泵扬程）。
    ("hydraulic calc correctness", ("node", "scripts/verify_hydraulic_calc.js")),
    # statistics 分类的正确性验证（Z 分数 / 单样本 t / 变异系数 / 加权平均 / 标准误 /
    # 对立事件 / 四分位距与异常值 / 正态区间概率 / 二项 PMF·CDF / 正态 CDF / 泊松 PMF /
    # 百分等级 / 比例置信区间 / 均值·比例样本量 / 相对风险 / 比值比 / 相关系数 /
    # 均值中位数极差 / 标准差方差 / 偏度峰度 / 单样本 t 检验 / F 方差齐性 / 卡方检验 /
    # 最小二乘回归 / 几何·调和平均 / 极差 / MAD / 样本方差·标准差 / 总体方差）。
    # 注：statistics-4 置信区间、statistics-5 样本量的逆正态 z 反解实现有误，未纳入（见 DEV-PLAN §9.3）。
    ("statistics calc correctness", ("node", "scripts/verify_statistics_calc.js")),
    # legal 分类的正确性验证（加班费 / 违法解除2N / 经济补偿N / N+1 / 逾期付款利息 / 抚养费 /
    # 离婚财产分割 / 诉讼费 / 知识产权保护期 / 年终奖个税 / 民间借贷利息 / 法律援助资格 / 工伤赔偿）。
    # 注：traffic-accident-compensation 伤残赔偿系数倒置缺陷未纳入（见 DEV-PLAN §9.3）。
    ("legal calc correctness", ("node", "scripts/verify_legal_calc.js")),
    # realestate 分类的正确性验证（房贷等额本息/等额本金总利息、租金毛·净回报率、首付与月供、
    # 公积金额度双轨取小 + 当地上限封顶、按揭可贷额度与月供·总利息、二手房契税与增值税及附加、
    # 单位地价·楼面地价与溢价率、REITs 股息率与资本化率、市场比较法估价、建筑面积换算）。
    # 注：calc-93/pv/depreciation-2 为跨行业通用 A/B 模板、summary-second-hand 名实不符，均未纳入。
    ("realestate calc correctness", ("node", "scripts/verify_realestate_calc.js")),
    ("energy calc correctness", ("node", "scripts/verify_energy_calc.js")),
    ("health calc correctness", ("node", "scripts/verify_health_calc.js")),
    ("healthcare calc correctness", ("node", "scripts/verify_healthcare_calc.js")),
    ("edu calc correctness", ("node", "scripts/verify_edu_calc.js")),
    ("marketing calc correctness", ("node", "scripts/verify_marketing_calc.js")),
    ("meteorology calc correctness", ("node", "scripts/verify_meteorology_calc.js")),
    ("optical calc correctness", ("node", "scripts/verify_optical_calc.js")),
    ("surveying calc correctness", ("node", "scripts/verify_surveying_calc.js")),
    ("fishery calc correctness", ("node", "scripts/verify_fishery_calc.js")),
    ("securities calc correctness", ("node", "scripts/verify_securities_calc.js")),
    ("aerospace calc correctness", ("node", "scripts/verify_aerospace_calc.js")),
    ("geology calc correctness", ("node", "scripts/verify_geology_calc.js")),
    ("machinery calc correctness", ("node", "scripts/verify_machinery_calc.js")),
    ("math calc correctness", ("node", "scripts/verify_math_calc.js")),
    ("accounting calc correctness", ("node", "scripts/verify_accounting_calc.js")),
    ("fitness calc correctness", ("node", "scripts/verify_fitness_calc.js")),
    ("eco calc correctness", ("node", "scripts/verify_eco_calc.js")),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run ToolBox build and quality gates in the required order."
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip _build.py for local re-checks only; do not use for release or CI.",
    )
    return parser.parse_args()


def run_gate(number: int, total: int, name: str, command: tuple[str, ...]) -> int:
    print(f"\n[{number}/{total}] {name}: {' '.join(command)}", flush=True)
    started = time.monotonic()
    try:
        completed = subprocess.run(command, cwd=ROOT, check=False)
    except FileNotFoundError as exc:
        executable = command[0]
        print(f"FAIL: required executable is not available: {executable}", file=sys.stderr)
        print(f"detail: {exc}", file=sys.stderr)
        return 127

    elapsed = time.monotonic() - started
    if completed.returncode == 0:
        print(f"PASS: {name} ({elapsed:.1f}s)", flush=True)
    else:
        print(
            f"FAIL: {name} exit={completed.returncode} ({elapsed:.1f}s)",
            file=sys.stderr,
            flush=True,
        )
    return completed.returncode


def main() -> int:
    args = parse_args()
    gates = list(GATES)
    if args.skip_build:
        gates = gates[1:]
        print("WARNING: build gate skipped; use this mode for local re-checks only.")

    for number, (name, command) in enumerate(gates, start=1):
        exit_code = run_gate(number, len(gates), name, command)
        if exit_code:
            print(f"\nQuality gates stopped after: {name}", file=sys.stderr)
            return exit_code

    print(f"\nAll {len(gates)} quality gates passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
