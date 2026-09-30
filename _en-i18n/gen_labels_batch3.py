#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_labels_batch3.py — 前缀字典第三批（report8 残留的前导标签形态）。

筛选铁律（防中英混杂垃圾，比留中文更糟）：
1. 只收「术语 + 数值/英文/标点」前导形态，且术语 >= 3 字（极不可能是更长中文词的词素前缀）。
2. 跳过：整句 OUTPUT（风荷载较大…/信用良好…/甲醛…/噪点…/配合响应式…/对比度优秀…/夏普比率低于…）、
   大段代码块（配置参数 #N 多行）、数字→中文转换器真实输出（壹仟…/一千零一…）、打字单字碎片（文分/分词…）。
3. 少数 2 字键必须配更长键兜住（配色 + 配色方案），避免 配色方案→Palette 方案 半译。
4. 译文零中文才入库。
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PF = os.path.join(ROOT, "i18n", "tools", "en", "_prefix.json")

# 硬译字典：键=前导中文术语，值=英文（可带尾空格以分隔变量）
B = {
    # —— 通用量纲/物理量（>=3 字，安全）——
    "完整数字": "Full number",
    "生成的": "Generated ",
    "示例文字": "Sample text ",
    "市场风险溢价": "Market risk premium ",
    "风险补偿": "Risk premium ",
    "端温差": "End temp diff ",
    "对比度": "Contrast ",
    "分辨率": "Resolution ",
    "比转速": "Specific speed ",
    "等效硬度": "Equivalent hardness ",
    "碳减排": "Carbon reduction ",
    "实时预览": "Live preview ",
    "相邻最小明度差": "Adjacent min lightness diff ",
    "按视口宽度": "By viewport width ",
    "内部收益率": "Internal rate of return ",
    "净现值": "Net present value ",
    "盈利指数": "Profitability index ",
    "项目可行": "Project feasible ",
    "回收估价": "Recycle estimate ",
    "有效年利率": "Effective annual rate ",
    "名义费率年化": "Nominal annualized rate ",
    "还款明细": "Repayment details ",
    "获利指数": "Profitability index ",
    "所需退休资金": "Required retirement fund ",
    "适用税率": "Applicable tax rate ",
    "五险一金": "Social insurance ",
    "到手工资": "Take-home pay ",
    "组合平均收益率": "Portfolio avg return ",
    "无风险利率": "Risk-free rate ",
    "超额收益": "Excess return ",
    "夏普比率": "Sharpe ratio ",
    "年化夏普": "Annualized Sharpe ",
    "长词数": "Long word count ",
    "单方指标": "Per-cubic-meter cost ",
    "平米指标": "Per-sqm cost ",
    "延米指标": "Per-linear-meter cost ",
    "风压高度变化系数": "Wind pressure height coeff ",
    "风振系数": "Gust factor ",
    "风荷载标准值": "Wind load standard value ",
    "载荷比": "Load ratio ",
    "寿命指数": "Life index ",
    "保温层厚度": "Insulation thickness ",
    "对数平均温差": "Log mean temp diff ",
    "所需换热面积": "Required heat-exchange area ",
    "孔偏差": "Hole deviation ",
    "轴偏差": "Shaft deviation ",
    "计算应力": "Calculated stress ",
    "综合调差系数": "Composite adjustment coeff ",
    "总流量": "Total flow ",
    "亩用药液量": "Liquid per mu ",
    "作业效率": "Work efficiency ",
    "每分钟作业面积": "Area per minute ",
    "药液量": "Liquid amount ",
    "均匀度": "Uniformity ",
    "电池能量": "Battery energy ",
    "理论最大航程": "Theoretical max range ",
    "安全航程": "Safe range ",
    "平均功率": "Average power ",
    "水灰比": "Water-cement ratio ",
    "配制强度": "Mix strength ",
    "至少需要": "At least ",
    "检查井间距": "Manhole spacing ",
    "所需总光通量": "Required total luminous flux ",
    "理论光通量": "Theoretical luminous flux ",
    "单灯实际光通": "Actual luminous flux per lamp ",
    "媒体查询": "Media query ",
    "桌面优先": "Desktop-first ",
    "合外力": "Net force ",
    "未知数": "Unknown ",
    "点击我": "Click me",
    # —— 2 字键：必须配更长键兜住，避免半译 ——
    "配色": "Palette ",
    "配色方案": "Palette scheme",
    "密度": "Density ",
    "密度板": "MDF",
    "体积": "Volume ",
    "体积模量": "Bulk modulus",
    "体积流量": "Volumetric flow ",
    "体积磨损率": "Volumetric wear rate ",
    "时间": "Time ",
    "时间常数": "Time constant ",
    "时间序列": "Time series",
    "时间复杂度": "Time complexity",
    "组成": "Composition: ",
    "组成分析": "Composition analysis",
    "矩阵": "Matrix ",
    "矩阵乘法": "Matrix multiplication",
    "周期": "Period ",
    "周期性": "Periodic",
    "距离": "Distance ",
    "距离传感器": "Distance sensor",
    "密钥": "Key: ",
    "密钥管理": "Key management",
    "当前": "Current ",
    "当前值": "Current value",
    "标题": "Title ",
    "标题栏": "Title bar",
    "时间": "Time ",
    "时间序列": "Time series",
    "时间复杂度": "Time complexity",
    "浓度": "Concentration ",
    "浓度计": "Concentration meter",
    "水泥": "Cement ",
    "水泥砂浆": "Cement mortar",
    "石子": "Aggregate ",
    "合格": "Qualified ",
    "合格率": "Qualification rate",
    "路宽": "Road width ",
    "能耗": "Energy consumption ",
    "能耗比": "Energy efficiency ratio",
    "手机": "Mobile ",
    "手机端": "Mobile",
    "平板": "Tablet ",
    "平板端": "Tablet",
    "桌面": "Desktop ",
    "桌面端": "Desktop",
    "向量": "Vector ",
    "向量积": "Cross product",
    "视角": "Angle: ",
    "视角范围": "Angle range",
    "粒子": "Particles ",
    "粒子数": "Particle count",
    "画布": "Canvas ",
    "画布尺寸": "Canvas size",
    "宽屏": "Widescreen ",
    "宽屏模式": "Widescreen mode",
    "绿色盲": "Deuteranopia ",
    "通过": "Pass ",
    "通过率": "Pass rate",
}

def has_cjk(s):
    return any('\u4e00' <= c <= '\u9fff' for c in s)

def main():
    cur = json.load(open(PF, encoding="utf-8"))
    added = 0
    for k, v in B.items():
        if has_cjk(v):
            print("REJECT (translation has CJK):", repr(k), "->", repr(v)); sys.exit(1)
        if k in cur:
            if cur[k] != v:
                print("SKIP exists diff:", repr(k), cur[k], "vs", v)
            continue
        cur[k] = v
        added += 1
    # 零中文校验（全量）
    bad = [(k, v) for k, v in cur.items() if has_cjk(v)]
    if bad:
        print("FATAL zero-chinese violation:", bad[:5]); sys.exit(1)
    json.dump(cur, open(PF, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(PF, "a", encoding="utf-8").write("\n")
    print("merged. added:", added, "total keys:", len(cur), "zero-chinese: OK")

if __name__ == "__main__":
    main()
