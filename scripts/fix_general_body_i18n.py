#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""根治 general 英文态正文数据源（§4.1.5）：i18n/tools/general-body.json + _en_override.json。

背景（审计盲区）：前几批只修了页面 HTML 的可见英文（p/desc-en/ed），未同步 build 预渲染
与运行时 i18n 所用的数据源，导致：
  - general-body.json 的 intro 140/180 仍是占位串「Xxx is available directly in your browser…」
    （英文态 ?lang=en-US 的正文 intro 即取自此）；
  - title 81+ 条为工具代号（Assessor 19 / Detector 175 / Frequency 3 …），英文态 h2 显示代号；
  - 连带 4 个页面因 formula-box 插在首个 <p> 前，被 _prerender_tool_body 把占位串注入 formula-desc。

本脚本按中文 deep-dive 标题为 180 个工具补真实英文名（NAME），intro 复用 fix_general_en_p 的
EN_MAP（页面可见英文同源）。写入 _en_override.json 的 en 与 general-body.json 的
title/h1/en.{title,h1}，保证 h2、h1、导航、英文态一致。

用法：
  python3 scripts/fix_general_body_i18n.py --dry-run
  python3 scripts/fix_general_body_i18n.py --apply
"""
import argparse, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from fix_general_en_p import EN_MAP  # noqa: E402

OV = os.path.join(ROOT, "i18n", "tools", "_en_override.json")
BODY = os.path.join(ROOT, "i18n", "tools", "general-body.json")
GIS = os.path.join(ROOT, "i18n", "tools", "general.json")

# 真实英文名（h2/h1/导航），取代工具代号
NAME = {
    "air-1": "Air Quality Index (AQI) Calculator",
    "analysis-21": "Descriptive Statistics Calculator",
    "analysis-43": "Unit-Metric Descriptive Statistics",
    "analysis-44": "Dataset Statistical Analysis",
    "assessor-19": "Wind-Resistance Grade Assessor",
    "assessor-20": "Micro-Machining Quality Assessor",
    "bearing": "Motor Bearing Maintenance Interval",
    "bearing-1": "Bearing Rating Life Calculator (ISO 281)",
    "bearing-load": "Bearing Equivalent Dynamic Load",
    "calc-13": "Date Difference Calculator",
    "calc-14": "Age Calculator (Exact to Day)",
    "calc-196": "Pipe Insulation Thickness Calculator",
    "calc-197": "Heat Exchanger Sizing (LMTD)",
    "calc-200": "Motor Selection Calculator",
    "calc-203": "Fits & Tolerance Calculator (ISO 286)",
    "calc-204": "Formwork Prop Spacing Calculator",
    "calc-205": "Scaffold Steel Consumption Estimate",
    "calc-206": "Scaffold Standard Stability Check",
    "calc-94": "Construction Cost Index Adjustment",
    "calc-flow": "Crop-Spraying Flow & Dosage",
    "calc-ratio-2": "Solution Dilution Ratio Calculator",
    "calc-speed-capacity": "Drone Endurance & Range Estimate",
    "calc-stats-1": "Descriptive Statistics (Sequence)",
    "calc-strength-ratio": "Concrete Mix Ratio (Bolomey)",
    "calculator-calc-10": "Linear Regression Calculator",
    "calculator-calc-11": "Complex Number Calculator",
    "color-temp-2": "Lighting Color Temperature Config",
    "concentration-20": "Coolant Concentration Top-Up",
    "concentration-22": "Paint Consumption Calculator",
    "convert-21": "Scientific Notation Converter",
    "convert-22": "SI Prefix Converter",
    "convert-content": "Hazardous Substance Content Converter",
    "detector-118": "Quality Composite Scoring",
    "detector-121": "Insulation Material Incoming Inspection",
    "detector-123": "Waterproofing Material Inspection",
    "detector-126": "Structural Adhesive Inspection",
    "detector-128": "Lubricating Oil Quality Check",
    "detector-131": "Concrete Incoming Inspection",
    "detector-134": "Rubber Product Inspection",
    "detector-139": "Measuring Equipment Calibration Interval",
    "detector-155": "Bearing Performance Inspection",
    "detector-159": "Mechanical Part Properties Check",
    "detector-16": "Occupancy Sensor Coverage Estimator",
    "detector-173": "Equipment Cable Sizing & Current",
    "detector-175": "Pump/Fan Shaft Power & Motor",
    "detector-194": "Equipment Repair/Replace Decision",
    "detector-200": "Lubricating Oil Quality Judgement",
    "detector-205": "Coating Weathering Inspection",
    "detector-207": "Release Agent Inspection",
    "detector-211": "Chemical Raw Material Inspection",
    "detector-213": "Chemical Product Inspection",
    "detector-aging": "Insulation Material Aging Inspection",
    "detector-aging-1": "Material Heat Resistance Inspection",
    "detector-aging-2": "Foam Material Inspection",
    "detector-composition": "Chemical Composition Inspection",
    "detector-composition-1": "Material Composition Inspection",
    "detector-composition-aging": "Cooling System Inspection",
    "detector-concentration": "Disinfectant Inspection",
    "detector-concentration-1": "Cutting Fluid Inspection",
    "detector-concentration-2": "Powder Material Inspection",
    "detector-corrosion": "Industrial Cleaner Inspection",
    "detector-corrosion-1": "Grease Quality Judgement",
    "detector-hardness-lifespan": "Abrasive Inspection",
    "detector-hardness-lifespan-1": "Steel Abrasive Inspection",
    "detector-hardness-torque": "Fastener Inspection",
    "detector-length-lifespan": "Belt & Rope Inspection",
    "detector-lifespan": "Tool Regrinding & Life Assessment",
    "detector-manager-protection": "Occupational Health Risk Scoring",
    "detector-pressure-torque": "Valve Inspection",
    "detector-protection-2": "Electrical Equipment Inspection",
    "detector-resistance": "HV Insulation Material Inspection",
    "detector-resistance-1": "Electrical System Inspection",
    "detector-resistance-aging": "Insulation Resistance & Aging Check",
    "detector-strength-lifespan": "Mechanical Part Inspection",
    "detector-stretch": "Material Mechanics Inspection",
    "detector-water-pressure": "Pressure Vessel Inspection",
    "detector-water-pressure-1": "Weld Inspection",
    "dianhuaxuedunhuakongzhi": "Electrochemical Passivation & Pourbaix",
    "distance-power-frequency": "Wireless Video Link Distance (Friis)",
    "estimate-14": "Used-Car Residual Value Estimate",
    "estimate-15": "Overseas Tax Refund Estimate",
    "estimate-36": "Lithography Resolution & DOF (Rayleigh)",
    "estimate-39": "Engineering Investment Estimate",
    "fabric-1": "Fabric Weight & Yarn Consumption",
    "fabric-3": "Fabric Quality Assessment",
    "fengjixuanxingjisuan": "Fan Sizing Calculator",
    "flow-14": "Pump Sizing Calculator",
    "flow-itinerary": "Hydraulic Cylinder Sizing",
    "frequency-15": "Ultrasonic Machining Parameters",
    "frequency-3": "Musical Tuning Frequency (Equal Temperament)",
    "generator-23": "Logic Truth Table Generator",
    "generator-24": "24-Point Game Generator",
    "generator-25": "Magic Square Generator (Odd Order)",
    "gongchengzaojiazhishujisuan": "Construction Cost Index Calculator",
    "gongyebengxuanxing": "Industrial Pump Sizing",
    "gongyeshebeigonglvpipei": "Industrial Equipment Power Matching",
    "gravity": "Gimbal Center of Gravity Balancing",
    "hanjiegongyicanshu": "Welding Process Parameters",
    "hardness-14": "Abrasive Hardness Selection",
    "huanbaonaimopinggu": "Eco Wear-Resistance Assessment",
    "jienengfanganjisuan": "Energy-Saving Plan Calculator",
    "jiguanghanjieguangbanjisuan": "Laser Welding Spot Calculator",
    "jiguangrongfuhoudujisuan": "Laser Cladding Thickness",
    "jingmishebeixuanxing": "Precision Equipment Selection",
    "kongtiaolengfuhejisuan": "Air-Conditioning Cooling Load",
    "liangshuzhihe-chengjizuida-zuixiao-shuxueti": "Two-Number Sum/Product Min-Max",
    "lifespan-10": "Recyclable Material Assessment",
    "lifespan-12": "Energy-Saving Life Calculation",
    "lifespan-18": "Low-Noise Life Assessment",
    "lifespan-20": "Precision Bearing Life",
    "lifespan-23": "Low-Oil-Mist Life (Arrhenius)",
    "lifespan-24": "Water-Based Fluid Life",
    "lifespan-25": "Thermal Fatigue Life (Coffin-Manson)",
    "lifespan-26": "Creep Life Calculator (Larson-Miller)",
    "lifespan-4": "Fatigue Life (Goodman + Basquin)",
    "lifespan-5": "Polymer Biostability Life Estimate",
    "lifespan-6": "Anti-Corrosion Coating Life (ISO 12944)",
    "lifespan-7": "Seal Life Calculator",
    "lifespan-8": "Recyclability Assessment",
    "lifespan-9": "Polymer Life Prediction (Arrhenius)",
    "lifespan-corrosion": "Corrosion-Resistance Life",
    "lifespan-wear-2": "Low-Wear Life Calculator",
    "lizishujianshejisuan": "Ion Beam Sputtering Calculator",
    "naimoxingpinggujisuan": "Wear-Resistance Assessment (Archard)",
    "nianjieqiangdujisuan": "Bond Strength & Allowable Load",
    "pidaizhangjinjisuan": "Belt Tension Calculator",
    "power-16": "V-Belt Drive Selection",
    "power-7": "Kitchen Appliance Power Matching",
    "power-focal": "Laser Cutting Energy & Depth",
    "power-voltage": "Motor Selection (Power/Poles)",
    "power-voltage-1": "Transformer Selection",
    "pressure-18": "Cooling Capacity Selection",
    "pressure-5": "Waterjet Cutting Capability",
    "pressure-flow-4": "Compressor Sizing",
    "pressure-flow-5": "Valve Sizing (Cv/Kv)",
    "pressure-flow-6": "Gas Purity Flow Calculator",
    "pressure-weld": "Friction Stir Welding Parameters",
    "rater-1": "Coin/Stamp Grade Rating Aid",
    "ratio-50": "Chemical Ratio Safety Calculator",
    "ratio-fuel-oil": "Blended Fuel Density & Calorific Value",
    "rechengxiangwenchapandu": "Thermal Imaging Temperature Reading (MRTD)",
    "recommender-24": "Alternative Recommendation Support",
    "runhuayougenghuanzhouqi": "Oil Change Interval (Arrhenius)",
    "runhuayouzhanduxuanxing": "Oil Viscosity Selection (ISO VG)",
    "shachepiangenghuanzhouqi": "Brake Pad Replacement Interval",
    "shebeiweihuzhouqi": "Equipment Maintenance Interval",
    "shebeizulinfeilvjisuan": "Equipment Rental Rate Calculator",
    "shusongdaixuanxingjisuan": "Conveyor Belt Sizing",
    "speed-26": "Chain Drive Selection",
    "speed-7": "Drone Patrol Efficiency",
    "speed-8": "Wire-Cut Precision Calculator",
    "speed-9": "Plasma Cutting Thickness",
    "stats-energy": "Energy Consumption Dashboard",
    "strength-34": "Fastener Strength Check",
    "strength-color-diff": "Color Difference Quality (ΔE)",
    "taocizhouchengshoumingjisuan": "Ceramic Bearing Life Calculator",
    "tax": "Construction VAT & Surcharges",
    "temp-26": "Explosion-Proof Mark Lookup",
    "temp-pressure-3": "Pressure Vessel Wall Thickness (GB 150)",
    "temp-time-concentration": "Etching Time Calculator",
    "tester-40": "Repair Service Plan Generator",
    "tester-maintenance": "Maintenance Plan Generator",
    "thread-4": "Thread Machining Parameters",
    "time-33": "3D Print Time Estimate (FDM)",
    "torque": "Bolt Tightening Torque",
    "torque-1": "Gearbox Selection",
    "torque-2": "Coupling Selection",
    "torque-3": "Torque Compensation Calculator",
    "torque-motion": "Actuator Selection",
    "torque-response": "Braking Torque Calculator",
    "turnover-2": "Material Turnover Calculator",
    "voltage": "Electron Beam Welding Parameters",
    "voltage-8": "Cable Cross-Section Selection",
    "voltage-9": "Conductor Ampacity Selection",
    "voltage-current-1": "Electrolysis Rate (Faraday's Law)",
    "wear-4": "Wear Rate Calculator (Archard)",
    "wurenjixuantingwuchajisuan": "Drone Hover Error Calculator",
    "zhilengshebeixuanxing": "Refrigeration Equipment Sizing",
    "zhiliangyanshouchouyang": "Quality Acceptance Sampling",
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    if not (a.dry_run or a.apply):
        print("请指定 --dry-run 或 --apply")
        return 2

    ov = json.load(open(OV, encoding="utf-8"))
    body = json.load(open(BODY, encoding="utf-8"))
    gis = json.load(open(GIS, encoding="utf-8"))
    miss_name = [s for s in EN_MAP if s not in NAME]
    miss_body = [s for s in NAME if s not in body]
    print(f"NAME {len(NAME)} 条；EN_MAP {len(EN_MAP)} 条；缺英文名 {miss_name}；body 缺条目 {miss_body}")

    changed_title = changed_intro = changed_gis = 0
    for slug, name in NAME.items():
        intro = EN_MAP[slug]
        k = "general/" + slug
        if k in ov:
            if ov[k].get("en") != name:
                changed_title += 1
            ov[k]["en"] = name
        if slug in body:
            e = body[slug]
            if e.get("intro") != intro:
                changed_intro += 1
            e["title"] = name
            e["h1"] = name
            e["intro"] = intro
            en = e.get("en")
            if isinstance(en, dict):
                en["title"] = name
                en["h1"] = name
                en["intro"] = intro
        if slug in gis:
            gi = gis[slug]
            en_us = gi.get("en-US")
            if not isinstance(en_us, dict):
                en_us = {}
                gi["en-US"] = en_us
            if en_us.get("intro") != intro:
                changed_gis += 1
            en_us["title"] = name
            en_us["h1"] = name
            en_us["intro"] = intro
    print(f"英文名更新 {changed_title} 条；intro 更新 {changed_intro} 条；general.json en-US 更新 {changed_gis} 条")

    if a.dry_run:
        for slug in list(NAME)[:3]:
            print(f"  预览 {slug}: name={NAME[slug]!r}\n        intro={EN_MAP[slug][:90]!r}")
        return 0

    json.dump(ov, open(OV, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(body, open(BODY, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    json.dump(gis, open(GIS, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("已写入 _en_override.json(1) / general-body.json(2) / general.json(2)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
