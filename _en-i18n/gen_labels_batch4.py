#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_labels_batch4.py — 前缀字典第四批（report9 残留的净量纲/字段标签）

策略（防 garble 铁律，与 batch2/3 一致）：
- 只收 >=3 字中文键（工程/物理/化学量纲名 + 结果区字段标签），几乎不可能是
  更长中文词的词素前缀 -> 零中英混杂垃圾风险。
- 排除：整句 OUTPUT（评估句/维护指令/演示样本）、打字样本、产品型号名、
  含句子标点的串、已在 _prefix.json 的键。
- 译文必须零中文（any CJK in value -> 拒绝入库）。
运行：python3 _en-i18n/gen_labels_batch4.py
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREFIX = os.path.join(ROOT, "i18n/tools/en/_prefix.json")

# —— 硬译字典：键=中文标签，值=英文（零中文） ——
B = {
    # 涂覆/材料
    "涂布率": "Coverage rate",
    "湿膜厚度": "Wet film thickness",
    # 流体/黏度
    "运动黏度": "Kinematic viscosity",
    "运动粘度": "Kinematic viscosity",
    # 电化学
    "析氢线": "Hydrogen evolution line",
    "析氧线": "Oxygen evolution line",
    "电位低于钝化临界": "Potential below passivation threshold",
    # 通信/射频
    "最大视距距离": "Max line-of-sight distance",
    "最大距离": "Max distance",
    "可容许路径损耗": "Allowable path loss",
    "收发总增益": "Total Tx/Rx gain",
    # 光学
    "总焦深": "Total depth of field",
    "焦点光斑直径": "Focal spot diameter",
    "离焦光斑直径": "Defocused spot diameter",
    "光斑直径": "Spot diameter",
    # 建筑/造价
    "单方造价": "Unit construction cost",
    # 纺织
    "面料克重": "Fabric weight",
    "经向克重": "Warp weight",
    "纬向克重": "Weft weight",
    "每匹面积": "Area per bolt",
    "估算克重": "Estimated weight",
    # 风机/气动
    "中等功率风机": "Medium-power fan",
    # 液压/气动
    "无杆腔面积": "Rodless chamber area",
    "有杆腔面积": "Rod-side chamber area",
    # 机加工
    "材料去除率": "Material removal rate",
    "工具面积": "Tool area",
    "小时去除量": "Hourly removal volume",
    "估算粗糙度": "Estimated roughness",
    "表面粗糙度": "Surface roughness",
    "额定扭矩": "Rated torque",
    "扭矩系数": "Torque coefficient",
    "角减速度": "Angular deceleration",
    "最大切割深度": "Max cutting depth",
    "切割速度": "Cutting speed",
    "切割效率": "Cutting efficiency",
    "线能量": "Line energy",
    "丝杠直径": "Lead screw diameter",
    "单道截面积": "Single-pass cross-section area",
    "焊缝截面积": "Weld cross-section area",
    "熔化速率": "Melting rate",
    "材料系数": "Material coefficient",
    "镀层厚度": "Coating thickness",
    "厚度增速": "Thickness growth rate",
    "沉积体积": "Deposited volume",
    "总磨损体积": "Total wear volume",
    "蚀刻速率": "Etch rate",
    "有效体积": "Effective volume",
    # 重量/重心
    "总重量": "Total weight",
    "合成重心": "Combined center of gravity",
    # 磨料
    "铬刚玉": "Chrome corundum",
    # 环保
    "年碳减排": "Annual carbon reduction",
    # 疲劳/蠕变
    "热疲劳寿命": "Thermal fatigue life",
    "热应变幅值": "Thermal strain amplitude",
    "稳态蠕变速率": "Steady-state creep rate",
    "疲劳极限": "Fatigue limit",
    "安全裕度": "Safety margin",
    "线膨胀系数": "Linear expansion coefficient",
    # 厚度/腐蚀/磨损
    "剩余厚度": "Remaining thickness",
    "有效厚度": "Effective thickness",
    "已消耗厚度": "Consumed thickness",
    "降解速率": "Degradation rate",
    "温度比": "Temperature ratio",
    "应力比": "Stress ratio",
    "修正腐蚀速率": "Corrected corrosion rate",
    "修正磨损率": "Corrected wear rate",
    "离子通量": "Ion flux",
    "比磨损率": "Specific wear rate",
    # 硬度/强度
    "维氏硬度": "Vickers hardness",
    "剪切强度": "Shear strength",
    # 电气
    "推荐铜线截面": "Recommended copper wire section",
    "功率密度": "Power density",
    "建议速度": "Recommended speed",
    "单位负荷": "Unit load",
    "相对密度": "Relative density",
    "混合密度": "Mixed density",
    "能量密度": "Energy density",
    "比功率": "Specific power",
    "抽样比": "Sampling ratio",
    "低功耗": "Low power",
    "数据量": "Data volume",
    "变异系数": "Coefficient of variation",
    # 统计
    "标准误": "Standard error",
    "边际误差": "Margin of error",
    "置信区间": "Confidence interval",
    "计算判别式": "Compute discriminant",
    # 物理力学
    "向心力": "Centripetal force",
    "向心加速度": "Centripetal acceleration",
    "静电力": "Electrostatic force",
    "观测频率": "Observed frequency",
    "频率偏移": "Frequency offset",
    "电场强度": "Electric field strength",
    "重力势能": "Gravitational potential energy",
    "弹簧力": "Spring force",
    "速度平方": "Velocity squared",
    "摩尔质量": "Molar mass",
    "原子序数": "Atomic number",
    "水平射程": "Horizontal range",
    "最大高度": "Max height",
    # 暖通
    "房间体积": "Room volume",
    "围护结构负荷": "Envelope load",
    # 气体
    "高纯气量": "High-purity gas volume",
    "稀释气量": "Dilution gas volume",
    "日需高纯气": "Daily high-purity gas demand",
    "日需稀释气": "Daily dilution gas demand",
    # 评级/其他
    "品相得分": "Grade score",
    "覆盖面积": "Coverage area",
    "巡查效率": "Inspection efficiency",
    # 色彩差异
    "明度差": "Lightness difference",
    "红绿差": "Red-green difference",
    "黄蓝差": "Yellow-blue difference",
    "色相差": "Hue difference",
}

def main():
    pf = json.load(open(PREFIX, encoding="utf-8"))
    orig = len(pf)
    added = 0
    bad = []
    for k, v in B.items():
        if k in pf:
            continue
        if any("\u4e00" <= c <= "\u9fff" for c in v):
            bad.append((k, v))
            continue
        pf[k] = v
        added += 1
    if bad:
        print("REJECTED (contains CJK):", bad)
        sys.exit(1)
    json.dump(pf, open(PREFIX, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    open(PREFIX, "a").write("\n")
    print(f"added {added} (total {orig} -> {len(pf)}); zero-CJK check passed")

if __name__ == "__main__":
    main()
