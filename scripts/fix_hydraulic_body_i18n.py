#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hydraulic (56) 分类英文态数据源根治：同步三端 + 补中文态缺口。

三处数据源（与 science/sports/fun/ai/biz/life/agriculture 同坑，§6「英文态数据源三处」）：
  ① i18n/tools/hydraulic-body.json   -> build `_prerender_tool_body` 预渲染 h1 + 首个 <p>
  ② i18n/tools/hydraulic.json en-US  -> industry JSON 的 ed 最高优先级源
  ③ i18n/tools/_en_override.json     -> 运行时 en（h2/h1）与 ed

本轮缺口：
  - 56 页 en-US / body / ov 三端英文为占位或代号（如 "Calc Power 2" / "Flow 1"）
  - 6 页（assessor-22 / calc-flow-1 / calc-pressure / calc-speed / cycle-19 / tester-blast）
    在三端**全缺**，由 ZH_TITLE / ZH_INTRO 补中文名与简介
  - 孤立键清理：body 11 个（含跨行业残留 buoyancy-force / hydrostatic-pressure /
    kinematic-viscosity / orifice-discharge / reynolds-number，已迁 fluid/aerospace）、
    lj 5 个、ov 6 个

用法：
  python3 scripts/fix_hydraulic_body_i18n.py --dry-run
  python3 scripts/fix_hydraulic_body_i18n.py --apply
"""
import argparse
import glob
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools', 'hydraulic')
OV = os.path.join(ROOT, 'i18n', 'tools', '_en_override.json')
BODY = os.path.join(ROOT, 'i18n', 'tools', 'hydraulic-body.json')
GIS = os.path.join(ROOT, 'i18n', 'tools', 'hydraulic.json')

# 6 个三端全缺的工具：补中文名与简介（依据页面 <h1> 与实际功能）
ZH_TITLE = {
    'assessor-22': '节水（器具/水效）评估',
    'calc-flow-1': '真空发生器流量计算',
    'calc-pressure': '管径计算（重力流/压力流）',
    'calc-speed': '气缸推力/速度计算',
    'cycle-19': '气动维护（排水/加油/检修）周期',
    'tester-blast': '耐压（试验/安全/爆破）测试',
}

ZH_INTRO = {
    'assessor-22': '按国家标准水效等级，依据器具实测流量评定一级（高效节水）至不合格，并对比新旧器具的日/年用水量与人均节水量，辅助节水改造决策。',
    'calc-flow-1': '由吸盘直径、吸盘数量、真空度、供气压力、安全系数与目标响应时间，计算单/总吸附力、所需抽吸流量与推荐真空发生器规格，辅助真空搬运系统选型。',
    'calc-pressure': '按压力流（Hazen-Williams）或重力流（Manning）两类工况，由设计流量、水温、管长与管材反算所需管径，并推荐相邻标准 DN 规格。',
    'calc-speed': '由缸径、行程、供气压力、负载、排气口口径与活塞杆直径，计算气缸推进/拉回推力、活塞速度、循环时间并校核缓冲能力。',
    'cycle-19': '按气动元件类型与维护周期排定排水、加油与检修计划，生成维护日历与到期提醒，辅助气动系统日常保养组织。',
    'tester-blast': '按压力容器规范，由设计压力、工作压力、材料抗拉/屈服强度、容器内径与壁厚，计算试验压力、保压时间、爆破压力与安全裕度，辅助耐压试验与安全评定。',
}

# NAME = 英文名（h1 / 导航 / 英文态标题），INTRO = 真实英文描述（intro / ed）。
NAME = {
    'analysis-frequency': 'Flood Frequency Analysis (Design Flood)',
    'area-capacity': 'Reservoir Capacity Curve Fitting',
    'assessor-22': 'Water-Saving Fixture / Water Efficiency Assessor',
    'assessor-33': 'Hydraulic Energy Efficiency & Recovery Assessor',
    'bernoulli-velocity': 'Bernoulli Equation Calculator (Downstream Velocity)',
    'calc-1': 'Pipe Hydraulics Calculator (Velocity / Pressure Drop)',
    'calc-2': 'Pump Head Calculator',
    'calc-26': "Open Channel Uniform Flow Calculator (Manning's Equation)",
    'calc-3': 'Pipe Friction Head Loss Calculator',
    'calc-4': 'Orifice Flow Calculator',
    'calc-5': 'Siphon Height Calculator',
    'calc-54': 'Sluice Gate Open/Close Force Calculator',
    'calc-flow-1': 'Vacuum Generator Flow Calculator',
    'calc-power-2': 'Cooling Heat Exchange Power Calculator',
    'calc-pressure': 'Pipe Diameter Calculator (Gravity / Pressure Flow)',
    'calc-pressure-capacity': 'Accumulator Capacity Calculator',
    'calc-protection': 'Water Hammer Protection Calculator',
    'calc-speed': 'Pneumatic Cylinder Force & Speed Calculator',
    'calc-speed-itinerary': 'Hydraulic Cylinder Force, Speed & Stroke Calculator',
    'continuity-pipe': 'Continuity Equation Calculator (Pipe Reducer)',
    'cycle-19': 'Pneumatic Maintenance Cycle Planner (Drain / Oil / Service)',
    'dam-stability': 'Dam Stability Calculator',
    'daohongxi-shuitousunshi-maishen': 'Inverted Siphon Head Loss & Burial Depth',
    'darcy-head-loss': 'Darcy-Weisbach Head Loss Calculator',
    'density-4': 'Earth-Rock Dam Fill Density Control',
    'detector-22': 'Oil Cleanliness Classifier (ISO 4406 / NAS 1638)',
    'flow': 'Spillway Discharge Calculator',
    'flow-1': 'Ecological Minimum Release Flow Calculator',
    'flow-pipeline': 'Diversion Pipeline Sizing Calculator',
    'flow-power': 'Hydropower Output Calculator',
    'flow-rate': 'Flow Rate Calculator',
    'flow-velocity': 'Flow Velocity Calculator',
    'gear-1': 'Hydraulic Pump Selection',
    'hazen-williams-headloss': 'Hazen-Williams Head Loss Calculator',
    'lifespan': 'Hydraulic Seal Selection & Lifespan',
    'manning-flow': 'Manning Open Channel Flow Calculator',
    'mianbanduishibachenjiangyuce': 'CFRD Settlement Predictor',
    'minor-head-loss': 'Minor Head Loss Calculator',
    'power-3': 'Pump Station Efficiency Calculator',
    'power-torque': 'Hydraulic Motor Selection',
    'pressure-diagnosis': 'Hydraulic Fault Diagnosis',
    'pressure-drop': 'Pipeline Design (Wall Thickness / Velocity / Pressure Drop)',
    'pressure-flow-1': 'Hydraulic Valve Selection',
    'pump-power': 'Pump Power Calculator',
    'qudao-buchong-buyu-liusu': 'Canal Non-Scouring / Non-Silting Velocity',
    'ratio-24': 'Hydraulic Servo System Calculator',
    'rectangular-weir': 'Rectangular Sharp-Crested Weir Calculator',
    'shenliu-jinrunxian-weizhi': 'Seepage Line (Phreatic Line) Position',
    'speed-pressure': 'Hydraulic Circuit Design',
    'spillway-calc': 'Spillway Calculator',
    'temp-7': 'Concrete Thermal Cracking Prevention',
    'tester-blast': 'Pressure Vessel Pressure Test & Safety Assessment',
    'velocity-from-flow': 'Velocity from Flow Rate Calculator',
    'water-level': 'Water Level Calculator',
    'yeyayouxiangsheji': 'Hydraulic Tank Designer',
    'yuji-nisha-kurongsunshi': 'Reservoir Sedimentation Loss Estimator',
}

INTRO = {
    'analysis-frequency': 'Fit a flood series to a frequency curve and read off design peak flow and volume for return periods such as 20, 50 and 100 years, for flood-control planning and spillway design.',
    'area-capacity': 'Enter water-level/area pairs to fit a level-capacity curve by trapezoidal integration, and query the storage volume at any water level for reservoir operation and water-supply planning.',
    'assessor-22': 'Grade a water fixture against national water-efficiency levels from its measured flow, and compare daily and annual water use against the old fixture, with per-person savings, to support retrofit decisions.',
    'assessor-33': 'Calculate hydraulic pump volumetric, mechanical and overall efficiency, and assess potential-energy recovery rate and VFD energy savings from load, height and duty cycle.',
    'bernoulli-velocity': 'Solve downstream velocity v2 from upstream/downstream pressure, known velocity and elevation by Bernoulli energy conservation, and read the total head difference between two points.',
    'calc-1': 'Compute circular-pipe velocity, Reynolds number, friction loss and pressure drop by the Darcy-Weisbach equation, including local-loss terms, for room-temperature clean water.',
    'calc-2': 'From suction and discharge static heads plus friction and minor losses, calculate the total pump head required, for pump selection in water-supply and drainage systems.',
    'calc-26': "For a trapezoidal channel, apply Manning's equation to compute uniform-flow discharge and velocity (set side slope m = 0 for a rectangular section).",
    'calc-3': 'Compute circular-pipe friction head loss, pressure drop and flow velocity by the Hazen-Williams formula, supporting common flow and diameter unit choices.',
    'calc-4': 'Enter head, orifice diameter and discharge coefficient to compute orifice discharge flow, for water supply, drainage and hydraulic design.',
    'calc-5': 'Estimate the maximum allowable siphon height that avoids cavitation at the pump inlet, from local atmospheric pressure, water temperature and pipe losses.',
    'calc-54': 'From gate self-weight, upstream/downstream head difference, seal friction coefficient and water-column downforce, calculate opening and closing forces to check hoist capacity.',
    'calc-flow-1': 'Size a vacuum generator and suction cups from cup diameter, cup count, vacuum level, air-supply pressure, safety factor and target response time, with gripping force and required flow.',
    'calc-power-2': 'From coolant flow and inlet/outlet temperature difference, compute heat-exchange power (kW) by specific heat, and back-calculate the cooling-water flow needed to hold that load.',
    'calc-pressure': 'Determine the required pipe diameter for pressure flow (Hazen-Williams) or gravity flow (Manning) from design flow, water temperature, pipe length and material, and recommend the next standard DN.',
    'calc-pressure-capacity': 'From working pressure range, gas pre-charge pressure and oil volume change, size a bladder accumulator under isothermal or adiabatic assumptions for shock absorption, leakage make-up or auxiliary power.',
    'calc-protection': 'Judge direct or indirect water hammer from valve-closure time versus wave travel time, compute the pressure rise, check pipeline safety and advise on slow-closing valves, surge tanks or air valves.',
    'calc-speed': 'From bore, stroke, air pressure, load, exhaust port size and rod diameter, calculate pneumatic cylinder push/pull force, piston speed, cycle time and cushioning adequacy.',
    'calc-speed-itinerary': 'From bore, rod diameter, supply pressure and flow of a double-acting single-rod cylinder, compute thrust and pull force, piston speed and stroke time for machine design and cycle-time checks.',
    'continuity-pipe': 'Apply A1v1 = A2v2 to find the velocity after a pipe diameter change from the inlet area/velocity and the outlet area.',
    'cycle-19': 'Plan drain, lubrication and service cycles for pneumatic components by element type and cycle length, generated as a maintenance calendar with due-date reminders.',
    'dam-stability': 'From unit-length gravity-dam geometry, concrete unit weight, upstream water level and foundation parameters, compute anti-sliding and anti-overturning safety factors under static water pressure.',
    'daohongxi-shuitousunshi-maishen': 'Estimate the head loss and required burial depth of an inverted siphon from pipe diameter, flow and terrain, for farmland water conservancy and water-supply crossings.',
    'darcy-head-loss': 'Compute pipe friction pressure drop by dP = f(L/D)(rho v^2/2) from friction factor, pipe length and diameter, fluid density and velocity.',
    'density-4': 'From wet density, water content and maximum dry density, compute compacted dry density and degree of compaction and check it against specification for earth-rock dam and embankment fill.',
    'detector-22': 'Enter particle counts by size range per 100 mL of oil to automatically classify ISO 4406 and NAS 1638 cleanliness codes and suggest suitable applications for each level.',
    'flow': 'Compute spillway discharge capacity by the weir-flow formula Q = m*b*sqrt(2g)*H^(3/2) for ogee or broad-crested weirs, for flood routing and outlet-works checks.',
    'flow-1': 'Compute the ecological minimum release flow from long-term mean flow and a base-flow coefficient, and assess ecological status with the Tennant method, for instream-flow management.',
    'flow-pipeline': 'From design diversion flow and economic velocity, calculate the recommended pipe diameter and estimate friction head loss by Manning, balancing investment and pumping energy.',
    'flow-power': 'From net head, diversion flow and turbine/generator efficiencies, compute electrical output and, with annual utilisation hours, estimate annual generation for small hydropower appraisal.',
    'flow-rate': 'Calculate pipe flow (Q = A x v from area and mean velocity) or open-channel flow (Manning from bed slope, roughness and hydraulic radius) to estimate a section conveyance capacity.',
    'flow-velocity': "Compute mean velocity in an open channel by Manning's equation and classify the flow regime by Reynolds number (laminar/transitional/turbulent) and Froude number (subcritical/supercritical).",
    'gear-1': 'From required system flow, working pressure and pump speed, calculate displacement and recommend a suitable pump type (gear / vane / piston) for hydraulic system matching.',
    'hazen-williams-headloss': 'Compute head loss h_f = 10.67*L*Q^1.852/(C^1.852*D^4.87) from flow, pipe length, roughness coefficient C and diameter (SI units).',
    'lifespan': 'From working pressure, temperature, medium and speed, recommend seal material (NBR / FKM / PU) and type (O-ring / Yx-ring / Glyd ring) and estimate seal service life for maintenance planning.',
    'manning-flow': 'Compute open-channel uniform-flow discharge Q = (1/n)*A*R^(2/3)*sqrt(S) from roughness n, cross-sectional area A, hydraulic radius R and bed slope S.',
    'mianbanduishibachenjiangyuce': 'Predict construction-period and post-completion settlement of a concrete-face rockfill dam by layer-wise summation and an exponential consolidation model, from dam height, modulus, unit weight and consolidation parameters.',
    'minor-head-loss': 'Compute local head loss h_L = K*v^2/(2g) for valves, elbows and fittings from the loss coefficient K and velocity.',
    'power-3': 'From flow, head and shaft power, compute pump effective power, operating efficiency and energy use and cost (water density 1000 kg/m3, g = 9.81 m/s2).',
    'power-torque': 'From required torque, speed and system pressure difference, calculate motor displacement, required flow and power and recommend a motor type.',
    'pressure-diagnosis': 'Diagnose likely hydraulic faults from rated and measured pressure, internal leakage, dominant vibration frequency and oil temperature, with rule-based causes and repair advice.',
    'pressure-drop': 'Estimate pipeline friction pressure drop and check wall thickness from diameter, velocity and length, for industrial piping and hydraulic system design.',
    'pressure-flow-1': 'From maximum flow, working pressure, control mode and valve function, calculate the valve bore and recommend a suitable valve type and size.',
    'pump-power': 'Compute pump shaft (input) power by P = rho*g*Q*H/eta from fluid density, gravity, flow, head and efficiency.',
    'qudao-buchong-buyu-liusu': 'Estimate the reasonable non-scouring and non-silting velocity range for a canal from section geometry and roughness, for open-channel design and scour/silt checks.',
    'ratio-24': 'From load mass, stroke, response frequency and supply pressure, calculate servo-cylinder area, required flow, hydraulic natural frequency and servo-valve flow gain to assess system bandwidth.',
    'rectangular-weir': 'Compute weir discharge Q = (2/3)*Cd*b*sqrt(2g)*H^1.5 from discharge coefficient, weir width and head over the crest.',
    'shenliu-jinrunxian-weizhi': 'Estimate the phreatic line position and seepage exit point of an earth dam from dam parameters and permeability coefficient, for stability and seepage-control design.',
    'speed-pressure': 'From cylinder bore and rod diameter, load and required speed, calculate push/pull chamber areas, required pressure and flow to design circuit pressure and flow parameters.',
    'spillway-calc': 'Compute spillway discharge Q by the weir-flow formula from weir type, head over crest, width and composite discharge coefficient, for quick flood-release checks.',
    'temp-7': 'From placing temperature, ambient temperature, hydration heat rise and structure thickness, compute internal-external and base temperature differences and the anti-cracking safety factor.',
    'tester-blast': 'From design and working pressure, material tensile and yield strength, vessel bore and wall thickness, compute test pressure, hold time, burst pressure and safety factor per pressure-vessel rules.',
    'velocity-from-flow': 'Compute mean velocity v = Q/A from volumetric flow and cross-sectional area, for pipes and channels, to check velocity against specification limits.',
    'water-level': 'From piezometric head, velocity and elevation, split position, pressure and velocity head and sum total head by Bernoulli, for pressure-tap analysis and pump-suction teaching.',
    'yeyayouxiangsheji': 'From pump flow, working pressure, system efficiency and allowable temperature rise, size the hydraulic reservoir volume and heat-dissipation area and judge whether a cooler is needed.',
    'yuji-nisha-kurongsunshi': 'Estimate reservoir storage loss from sediment inflow, capacity and desilting parameters, for reservoir operation and service-life assessment.',
}

DEFAULT_NOTE = [
    '本工具纯前端运行，数据不会上传到服务器',
    '建议在主流浏览器（Chrome/Safari/Firefox/Edge）中使用',
    '计算结果仅供参考，请以实际应用场景为准',
]


def load(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


_CANDIDATES = (
    dict(indent=0, separators=(',', ':')),
    dict(indent=1, separators=(',', ':')),
    dict(indent=1),
    dict(indent=2, separators=(',', ':')),
    dict(indent=2),
    dict(indent=None, separators=(',', ':')),
    dict(indent=None),
)


def dump_like(path, data, orig_raw):
    """按文件原有 JSON 格式回写：逐一尝试候选格式，取能无损还原原串的那个。"""
    body_raw = orig_raw.rstrip('\n')
    trailing = '\n' if orig_raw.endswith('\n') else ''
    try:
        orig = json.loads(orig_raw)
    except Exception:
        orig = None
    if orig is not None:
        for c in _CANDIDATES:
            try:
                if json.dumps(orig, ensure_ascii=False, **c) == body_raw:
                    return json.dumps(data, ensure_ascii=False, **c) + trailing
            except Exception:
                continue
    return json.dumps(data, ensure_ascii=False, indent=2) + trailing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--apply', action='store_true')
    a = ap.parse_args()
    if not a.dry_run and not a.apply:
        ap.error('需指定 --dry-run 或 --apply')

    slugs = sorted(
        os.path.basename(f)[:-5]
        for f in glob.glob(os.path.join(TOOLS, '*.html'))
        if os.path.basename(f) != 'index.html'
    )
    missing_name = [s for s in slugs if s not in NAME]
    missing_intro = [s for s in slugs if s not in INTRO]
    if missing_name or missing_intro:
        print('!! NAME/INTRO 缺条目:', missing_name, missing_intro)
        return 1

    ov_raw = open(OV, encoding='utf-8').read()
    body_raw = open(BODY, encoding='utf-8').read()
    gis_raw = open(GIS, encoding='utf-8').read()
    ov = json.loads(ov_raw)
    body = json.loads(body_raw)
    gis = json.loads(gis_raw)

    chg_en = chg_ed = chg_body = added_body = added_gis = chg_zh = 0

    for slug in slugs:
        name = NAME[slug]
        intro = INTRO[slug]
        k = 'hydraulic/' + slug

        e = ov.get(k)
        if not isinstance(e, dict):
            e = {'ind': 'hydraulic'}
        if e.get('en') != name:
            chg_en += 1
        if e.get('ed') != intro:
            chg_ed += 1
        e['en'] = name
        e['ed'] = intro
        e.setdefault('ind', 'hydraulic')
        ov[k] = e

        b = body.get(slug)
        if not isinstance(b, dict):
            b = {}
            added_body += 1
            print('  + hydraulic-body.json 新增条目:', slug)
        if b.get('title') != name or b.get('h1') != name or b.get('intro') != intro:
            chg_body += 1
        b['title'] = name
        b['h1'] = name
        b['intro'] = intro
        en = b.get('en')
        if not isinstance(en, dict):
            en = {}
        en['title'] = name
        en['h1'] = name
        en['intro'] = intro
        b['en'] = en
        body[slug] = b

        g = gis.get(slug)
        if not isinstance(g, dict):
            g = {}
            added_gis += 1
            print('  + hydraulic.json 新增条目:', slug)
        z = g.get('zh-CN')
        if not isinstance(z, dict):
            z = {}
        if not (z.get('title') or '').strip():
            zt = ZH_TITLE.get(slug)
            if zt:
                z['title'] = zt
                z['h1'] = zt
                chg_zh += 1
        if not (z.get('intro') or '').strip():
            zi = ZH_INTRO.get(slug)
            if zi:
                z['intro'] = zi
                chg_zh += 1
        g['zh-CN'] = z
        eu = g.get('en-US')
        if not isinstance(eu, dict):
            eu = {}
        eu['title'] = name
        eu['h1'] = name
        eu['intro'] = intro
        g['en-US'] = eu
        if 'note' not in g:
            g['note'] = list(DEFAULT_NOTE)
        gis[slug] = g

    # 孤儿/跨行业残留键清理：本行业数据源中不属于 hydraulic 工具页的键一律删除。
    hy_slugs = set(slugs)
    orph_body = [k for k in list(body.keys()) if k not in hy_slugs]
    for k in orph_body:
        del body[k]
    orph_ov = [k for k in list(ov.keys())
               if k.startswith('hydraulic/') and k.split('/', 1)[1] not in hy_slugs]
    for k in orph_ov:
        del ov[k]
    orph_gis = [k for k in list(gis.keys()) if k not in hy_slugs]
    for k in orph_gis:
        del gis[k]

    print('\n--- 汇总 ---')
    print('hydraulic 工具页:', len(slugs))
    print('_en_override  en 更新:', chg_en, ' ed 更新:', chg_ed)
    print('hydraulic-body 更新:', chg_body, ' 新增:', added_body)
    print('hydraulic.json 更新 en-US:', len(slugs), ' 新增条目:', added_gis, ' 中文 title/intro 补齐:', chg_zh)
    print('孤儿键删除  body:', len(orph_body), ' _en_override:', len(orph_ov), ' hydraulic.json:', len(orph_gis))
    if orph_body:
        print('   body:', orph_body)
    if orph_ov:
        print('   ov  :', orph_ov)
    if orph_gis:
        print('   gis :', orph_gis)

    if a.dry_run:
        print('\n[dry-run] 未写盘')
        return 0

    open(OV, 'w', encoding='utf-8').write(dump_like(OV, ov, ov_raw))
    open(BODY, 'w', encoding='utf-8').write(dump_like(BODY, body, body_raw))
    open(GIS, 'w', encoding='utf-8').write(dump_like(GIS, gis, gis_raw))
    print('\n已写盘:', OV, BODY, GIS)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
