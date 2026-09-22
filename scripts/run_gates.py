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
    # 防复发（缺陷 N）：构建期英文预渲染曾把页面 intro 注入 <script> 内 JS 字符串的
    # <p> 提示位（未转义撇号/换行）→ 脚本整块 SyntaxError、计算器静默失效。既有门禁
    # （静态结构/链接/资源/calc 冒烟/用例断言）都不校验 inline JS 语法，故单列一道。
    ("inline js syntax", ("node", "scripts/check_inline_js_syntax.js")),
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
    # 注：statistics-4 置信区间、statistics-5 样本量的逆正态 z 反解实现有误，未纳入（见 DEV-PLAN §7.1）。
    ("statistics calc correctness", ("node", "scripts/verify_statistics_calc.js")),
    # legal 分类的正确性验证（加班费 / 违法解除2N / 经济补偿N / N+1 / 逾期付款利息 / 抚养费 /
    # 离婚财产分割 / 诉讼费 / 知识产权保护期 / 年终奖个税 / 民间借贷利息 / 法律援助资格 / 工伤赔偿）。
    # 注：traffic-accident-compensation 伤残赔偿系数倒置缺陷未纳入（见 DEV-PLAN §7.1）。
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
    ("thermodynamics calc correctness", ("node", "scripts/verify_thermodynamics_calc.js")),
    ("banking calc correctness", ("node", "scripts/verify_banking_calc.js")),
    ("hematology calc correctness", ("node", "scripts/verify_hematology_calc.js")),
    ("math calc correctness", ("node", "scripts/verify_math_calc.js")),
    ("accounting calc correctness", ("node", "scripts/verify_accounting_calc.js")),
    ("fitness calc correctness", ("node", "scripts/verify_fitness_calc.js")),
    ("eco calc correctness", ("node", "scripts/verify_eco_calc.js")),
    ("insurance calc correctness", ("node", "scripts/verify_insurance_calc.js")),
    ("obstetrics calc correctness", ("node", "scripts/verify_obstetrics_calc.js")),
    ("ophthalmology calc correctness", ("node", "scripts/verify_ophthalmology_calc.js")),
    ("encode calc correctness", ("node", "scripts/verify_encode_calc.js")),
    ("metalwork calc correctness", ("node", "scripts/verify_metalwork_calc.js")),
    ("photo calc correctness", ("node", "scripts/verify_photo_calc.js")),
    ("tax calc correctness", ("node", "scripts/verify_tax_calc.js")),
    ("acoustics calc correctness", ("node", "scripts/verify_acoustics_calc.js")),
    ("chemistry calc correctness", ("node", "scripts/verify_chemistry_calc.js")),
    ("dynamics calc correctness", ("node", "scripts/verify_dynamics_calc.js")),
    ("economics calc correctness", ("node", "scripts/verify_economics_calc.js")),
    ("electromagnetism calc correctness", ("node", "scripts/verify_electromagnetism_calc.js")),
    ("fluid calc correctness", ("node", "scripts/verify_fluid_calc.js")),
    ("geometry calc correctness", ("node", "scripts/verify_geometry_calc.js")),
    ("investment calc correctness", ("node", "scripts/verify_investment_calc.js")),
    ("kinematics calc correctness", ("node", "scripts/verify_kinematics_calc.js")),
    ("materials calc correctness", ("node", "scripts/verify_materials_calc.js")),
    ("metrology calc correctness", ("node", "scripts/verify_metrology_calc.js")),
    ("nuclear calc correctness", ("node", "scripts/verify_nuclear_calc.js")),
    ("optics calc correctness", ("node", "scripts/verify_optics_calc.js")),
    ("quantum calc correctness", ("node", "scripts/verify_quantum_calc.js")),
    ("robotics calc correctness", ("node", "scripts/verify_robotics_calc.js")),
    ("signal calc correctness", ("node", "scripts/verify_signal_calc.js")),
    ("structural calc correctness", ("node", "scripts/verify_structural_calc.js")),
    ("reproductive-medicine calc correctness", ("node", "scripts/verify_reproductive-medicine_calc.js")),
    ("livestock calc correctness", ("node", "scripts/verify_livestock_calc.js")),
    ("neurology calc correctness", ("node", "scripts/verify_neurology_calc.js")),
    ("construction calc correctness", ("node", "scripts/verify_construction_calc.js")),
    ("pulmonology calc correctness", ("node", "scripts/verify_pulmonology_calc.js")),
    ("astronomy calc correctness", ("node", "scripts/verify_astronomy_calc.js")),
    ("clinical-nursing calc correctness", ("node", "scripts/verify_clinical-nursing_calc.js")),
    ("dentistry calc correctness", ("node", "scripts/verify_dentistry_calc.js")),
    ("cardiology calc correctness", ("node", "scripts/verify_cardiology_calc.js")),
    ("clinical-lab calc correctness", ("node", "scripts/verify_clinical-lab_calc.js")),
    ("pediatrics calc correctness", ("node", "scripts/verify_pediatrics_calc.js")),
    ("psychiatry calc correctness", ("node", "scripts/verify_psychiatry_calc.js")),
    # 心理/临床量表页增强（psych-kit.js）行为验证：进度条、高危热线、未答确认、分级徽章、
    # 娱乐标识、纯前端自检。覆盖 18 个 span 答题页（PHQ-9/GAD-7/CAGE 等）的真实计分与增强行为，
    # 弥补 harness 无法注入 span 选项的缺口（DEV-PLAN §九 缺陷 G 闭环）。
    ("psych-kit behavior (jsdom)", ("node", "scripts/verify_psych_kit.cjs")),
    ("rheumatology calc correctness", ("node", "scripts/verify_rheumatology_calc.js")),
    ("urology calc correctness", ("node", "scripts/verify_urology_calc.js")),
    ("electronics calc correctness", ("node", "scripts/verify_electronics_calc.js")),
    ("food-testing calc correctness", ("node", "scripts/verify_food-testing_calc.js")),
    ("food calc correctness", ("node", "scripts/verify_food_calc.js")),
    ("dermatology calc correctness", ("node", "scripts/verify_dermatology_calc.js")),
    ("rehabilitation calc correctness", ("node", "scripts/verify_rehabilitation_calc.js")),
    ("tcm-pharmacy calc correctness", ("node", "scripts/verify_tcm-pharmacy_calc.js")),
    ("acupuncture calc correctness", ("node", "scripts/verify_acupuncture_calc.js")),
    ("ent calc correctness", ("node", "scripts/verify_ent_calc.js")),
    ("tcm-chemistry calc correctness", ("node", "scripts/verify_tcm-chemistry_calc.js")),
    ("endocrinology calc correctness", ("node", "scripts/verify_endocrinology_calc.js")),
    ("tcm-diagnosis calc correctness", ("node", "scripts/verify_tcm-diagnosis_calc.js")),
    ("nephrology calc correctness", ("node", "scripts/verify_nephrology_calc.js")),
    ("gastroenterology calc correctness", ("node", "scripts/verify_gastroenterology_calc.js")),
    ("accessibility calc correctness", ("node", "scripts/verify_accessibility_calc.js")),
    ("admin calc correctness", ("node", "scripts/verify_admin_calc.js")),
    ("advertising calc correctness", ("node", "scripts/verify_advertising_calc.js")),
    ("antiques calc correctness", ("node", "scripts/verify_antiques_calc.js")),
    ("aquaculture calc correctness", ("node", "scripts/verify_aquaculture_calc.js")),
    ("archaeology calc correctness", ("node", "scripts/verify_archaeology_calc.js")),
    ("audio calc correctness", ("node", "scripts/verify_audio_calc.js")),
    ("audit calc correctness", ("node", "scripts/verify_audit_calc.js")),
    ("automotive calc correctness", ("node", "scripts/verify_automotive_calc.js")),
    ("baking calc correctness", ("node", "scripts/verify_baking_calc.js")),
    ("beauty calc correctness", ("node", "scripts/verify_beauty_calc.js")),
    ("bonding calc correctness", ("node", "scripts/verify_bonding_calc.js")),
    ("bridge calc correctness", ("node", "scripts/verify_bridge_calc.js")),
    ("ceramics calc correctness", ("node", "scripts/verify_ceramics_calc.js")),
    ("chemical calc correctness", ("node", "scripts/verify_chemical_calc.js")),
    ("civil calc correctness", ("node", "scripts/verify_civil_calc.js")),
    ("cleaning calc correctness", ("node", "scripts/verify_cleaning_calc.js")),
    ("cognition calc correctness", ("node", "scripts/verify_cognition_calc.js")),
    ("data calc correctness", ("node", "scripts/verify_data_calc.js")),
    ("decor calc correctness", ("node", "scripts/verify_decor_calc.js")),
    ("chinese-cook calc correctness", ("node", "scripts/verify_chinese-cook_calc.js")),
    ("dance calc correctness", ("node", "scripts/verify_dance_calc.js")),
    ("chess calc correctness", ("node", "scripts/verify_chess_calc.js")),
    ("chinese calc correctness", ("node", "scripts/verify_chinese_calc.js")),
    ("dyeing calc correctness", ("node", "scripts/verify_dyeing_calc.js")),
    ("ecommerce calc correctness", ("node", "scripts/verify_ecommerce_calc.js")),
    ("edu2 calc correctness", ("node", "scripts/verify_edu2_calc.js")),
    ("elderly calc correctness", ("node", "scripts/verify_elderly_calc.js")),
    ("electrical calc correctness", ("node", "scripts/verify_electrical_calc.js")),
    ("engineering calc correctness", ("node", "scripts/verify_engineering_calc.js")),
    ("exhibition calc correctness", ("node", "scripts/verify_exhibition_calc.js")),
    ("fengshui calc correctness", ("node", "scripts/verify_fengshui_calc.js")),
    ("fire calc correctness", ("node", "scripts/verify_fire_calc.js")),
    ("floral calc correctness", ("node", "scripts/verify_floral_calc.js")),
    ("forex calc correctness", ("node", "scripts/verify_forex_calc.js")),
    ("funeral calc correctness", ("node", "scripts/verify_funeral_calc.js")),
    ("futures calc correctness", ("node", "scripts/verify_futures_calc.js")),
    ("gardening calc correctness", ("node", "scripts/verify_gardening_calc.js")),
    ("gas calc correctness", ("node", "scripts/verify_gas_calc.js")),
    ("glass calc correctness", ("node", "scripts/verify_glass_calc.js")),
    ("home calc correctness", ("node", "scripts/verify_home_calc.js")),
    ("hotel calc correctness", ("node", "scripts/verify_hotel_calc.js")),
    ("hr calc correctness", ("node", "scripts/verify_hr_calc.js")),
    ("hvac calc correctness", ("node", "scripts/verify_hvac_calc.js")),
    ("jewelry calc correctness", ("node", "scripts/verify_jewelry_calc.js")),
    ("legal2 calc correctness", ("node", "scripts/verify_legal2_calc.js")),
    ("logistics calc correctness", ("node", "scripts/verify_logistics_calc.js")),
    ("cosmetic-derm calc correctness", ("node", "scripts/verify_cosmetic-derm_calc.js")),
    ("film calc correctness", ("node", "scripts/verify_film_calc.js")),
    ("fire-rescue calc correctness", ("node", "scripts/verify_fire-rescue_calc.js")),
    ("food-processing calc correctness", ("node", "scripts/verify_food-processing_calc.js")),
    ("forensic-medicine calc correctness", ("node", "scripts/verify_forensic-medicine_calc.js")),
    ("forestry calc correctness", ("node", "scripts/verify_forestry_calc.js")),
    ("gardening2 calc correctness", ("node", "scripts/verify_gardening2_calc.js")),
    ("kids calc correctness", ("node", "scripts/verify_kids_calc.js")),
    ("language calc correctness", ("node", "scripts/verify_language_calc.js")),
    ("library calc correctness", ("node", "scripts/verify_library_calc.js")),
    ("logistics2 calc correctness", ("node", "scripts/verify_logistics2_calc.js")),
    ("manufacturing calc correctness", ("node", "scripts/verify_manufacturing_calc.js")),
    ("maritime calc correctness", ("node", "scripts/verify_maritime_calc.js")),
    ("martial calc correctness", ("node", "scripts/verify_martial_calc.js")),
    ("mechanical calc correctness", ("node", "scripts/verify_mechanical_calc.js")),
    ("media calc correctness", ("node", "scripts/verify_media_calc.js")),
    ("medical calc correctness", ("node", "scripts/verify_medical_calc.js")),
    ("medical2 calc correctness", ("node", "scripts/verify_medical2_calc.js")),
    ("metallurgy calc correctness", ("node", "scripts/verify_metallurgy_calc.js")),
    ("mining calc correctness", ("node", "scripts/verify_mining_calc.js")),
    ("misc2 calc correctness", ("node", "scripts/verify_misc2_calc.js")),
    ("leather calc correctness", ("node", "scripts/verify_leather_calc.js")),
    ("misc calc correctness", ("node", "scripts/verify_misc_calc.js")),
    ("restaurant calc correctness", ("node", "scripts/verify_restaurant_calc.js")),
    ("welding calc correctness", ("node", "scripts/verify_welding_calc.js")),
    ("pr calc correctness", ("node", "scripts/verify_pr_calc.js")),
    ("rubber calc correctness", ("node", "scripts/verify_rubber_calc.js")),
    ("procurement calc correctness", ("node", "scripts/verify_procurement_calc.js")),
    ("property calc correctness", ("node", "scripts/verify_property_calc.js")),
    ("photo2 calc correctness", ("node", "scripts/verify_photo2_calc.js")),
    ("pet calc correctness", ("node", "scripts/verify_pet_calc.js")),
    ("petrochem calc correctness", ("node", "scripts/verify_petrochem_calc.js")),
    ("process calc correctness", ("node", "scripts/verify_process_calc.js")),
    ("pet-training calc correctness", ("node", "scripts/verify_pet-training_calc.js")),
    ("office calc correctness", ("node", "scripts/verify_office_calc.js")),
    ("parenting calc correctness", ("node", "scripts/verify_parenting_calc.js")),
    ("quality calc correctness", ("node", "scripts/verify_quality_calc.js")),
    ("video calc correctness", ("node", "scripts/verify_video_calc.js")),
    ("paper calc correctness", ("node", "scripts/verify_paper_calc.js")),
    ("packaging calc correctness", ("node", "scripts/verify_packaging_calc.js")),
    ("road calc correctness", ("node", "scripts/verify_road_calc.js")),
    ("music calc correctness", ("node", "scripts/verify_music_calc.js")),
    ("railway calc correctness", ("node", "scripts/verify_railway_calc.js")),
    ("project calc correctness", ("node", "scripts/verify_project_calc.js")),
    ("rental calc correctness", ("node", "scripts/verify_rental_calc.js")),
    ("safety calc correctness", ("node", "scripts/verify_safety_calc.js")),
    ("nutrition calc correctness", ("node", "scripts/verify_nutrition_calc.js")),
    ("printing calc correctness", ("node", "scripts/verify_printing_calc.js")),
    ("psychology calc correctness", ("node", "scripts/verify_psychology_calc.js")),
    ("museum calc correctness", ("node", "scripts/verify_museum_calc.js")),
    ("telecom calc correctness", ("node", "scripts/verify_telecom_calc.js")),
    ("plastic calc correctness", ("node", "scripts/verify_plastic_calc.js")),
    ("transport calc correctness", ("node", "scripts/verify_transport_calc.js")),
    ("niche calc correctness", ("node", "scripts/verify_niche_calc.js")),
    ("pets calc correctness", ("node", "scripts/verify_pets_calc.js")),
    ("image calc correctness", ("node", "scripts/verify_image_calc.js")),
    ("research calc correctness", ("node", "scripts/verify_research_calc.js")),
    ("sales calc correctness", ("node", "scripts/verify_sales_calc.js")),
    ("security calc correctness", ("node", "scripts/verify_security_calc.js")),
    ("seismology calc correctness", ("node", "scripts/verify_seismology_calc.js")),
    ("service calc correctness", ("node", "scripts/verify_service_calc.js")),
    ("shipping calc correctness", ("node", "scripts/verify_shipping_calc.js")),
    ("stage calc correctness", ("node", "scripts/verify_stage_calc.js")),
    ("startup calc correctness", ("node", "scripts/verify_startup_calc.js")),
    ("stats calc correctness", ("node", "scripts/verify_stats_calc.js")),
    ("text calc correctness", ("node", "scripts/verify_text_calc.js")),
    ("textile calc correctness", ("node", "scripts/verify_textile_calc.js")),
    ("travel calc correctness", ("node", "scripts/verify_travel_calc.js")),
    ("tunnel calc correctness", ("node", "scripts/verify_tunnel_calc.js")),
    ("urban calc correctness", ("node", "scripts/verify_urban_calc.js")),
    ("usedcar calc correctness", ("node", "scripts/verify_usedcar_calc.js")),
    ("wedding calc correctness", ("node", "scripts/verify_wedding_calc.js")),
    ("woodwork calc correctness", ("node", "scripts/verify_woodwork_calc.js")),
    ("woodworking calc correctness", ("node", "scripts/verify_woodworking_calc.js")),
    ("yi calc correctness", ("node", "scripts/verify_yi_calc.js")),
    # 反回归（P0-2 / DEV-PLAN §7.1）：禁止任何 verify 脚本残留 _selfcheck 假门禁标记
    # 或「空输入」假用例。真用例都带真实 inputs，本门禁零误伤；一旦存在假门禁即判红，
    # 强制还原为真实 inputs+expect。置于最后，不阻塞其余门禁先跑完。
    ("anti-regression: no fake gates", ("node", "scripts/selfcheck_false_pass.js", "scripts")),
    # 判别力门禁（DEV-PLAN §8.2）：模拟「输入注入失败」——把用例 inputs 换回页面默认值，
    # 用例必须 FAIL。仍 PASS 的即含「不依赖被测点的逃生项」（任一命中即通过机制的第二次
    # 隐蔽假通过）。存量入基线 scripts/discriminate_baseline.json，只准降不准增。
    ("anti-regression: case discrimination", ("node", "scripts/discriminate_check.js")),
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
