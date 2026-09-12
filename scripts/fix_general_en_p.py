#!/usr/bin/env python3
"""general 分类：英文 intro <p> 占位串真实化（分批）。

背景：general 工具页的可见 intro 形如
    <p style="..." data-zh="中文描述">XXX is available directly in your browser, with no data uploaded.</p>
占位串写在源文件里（非 build 注入），data-zh 已带真实中文，只需把占位英文换成真实英文。

用法：
    python3 scripts/fix_general_en_p.py --dry-run    # 只报告，不落盘
    python3 scripts/fix_general_en_p.py --apply      # 落盘
安全约束：
  - 只匹配「带 data-zh 且内部是占位串」的单个 <p>，正则保留 <p attrs> 与 </p> 原样，
    仅替换标签内部文本，杜绝双 </p> 与跨段破坏（it ③ 教训）。
  - 单个文件若匹配到多处，跳过并报告，人工复核后再处理。
后续批次继续往 EN_MAP 追加即可。
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLACE = 'is available directly in your browser'
PAT = re.compile(
    r'(<p\b[^>]*data-zh="[^"]*"[^>]*>)([^<]*' + re.escape(PLACE) + r'[^<]*)(</p>)'
)
# 更新模式：页面 <p> 已是真实英文（无占位串）时，按 data-zh 定位唯一英文 <p>，
# 让 EN_MAP 始终是页面 intro 的单一数据源（改 EN_MAP → 重跑 --apply 即同步）。
PAT_ANY = re.compile(r'(<p\b[^>]*data-zh="[^"]*"[^>]*>)([^<]*)(</p>)')
CJK = re.compile(r'[\u4e00-\u9fff]')

# ---- 首批：中文描述清晰、可直接写成有信息量英文的 50 个 ----
EN_MAP = {
    'air-1': "Enter concentrations of the six criteria pollutants to compute the AQI and identify the primary pollutant under China's HJ 633-2012 standard, with health guidance for each AQI band. Enter CO in mg per cubic metre.",
    'assessor-19': "Computes the wind-resistance grade of a building structure per GB 50009 from basic wind pressure, terrain category, shape factor and structural height.",
    'bearing-1': "Computes rolling bearing fatigue life from basic dynamic load rating C and equivalent dynamic load P using the ISO 281 rating equation L10=(C/P)^p, reported in million revolutions, hours or years.",
    'bearing-load': "Computes the equivalent dynamic load P = X·Fr + Y·Fa from radial load Fr, axial load Fa and the radial and axial factors X and Y, the load input needed for bearing life ratings.",
    'calc-flow': "From nozzle flow rate, nozzle count, spray width and travel speed, computes spray volume per mu and field efficiency to plan agricultural drone or boom sprayer applications.",
    'calc-ratio-2': "From stock concentration, target concentration and total volume needed, computes how much concentrate and water to mix along with the dilution factor.",
    'calc-speed-capacity': "From battery capacity, average current draw and cruise speed, estimates drone flight endurance, maximum range and usable pack energy.",
    'calc-strength-ratio': "From target strength grade, cement grade and aggregate type, computes the water-cement ratio and material quantities per cubic metre of concrete using the Bolomey formula.",
    'calculator-calc-10': "Accepts x,y data pairs, one per line with comma or space separators, and fits a least-squares regression line y=ax+b together with the coefficient of determination R squared.",
    'calculator-calc-11': "Enter the real and imaginary parts of two complex numbers to obtain their sum, difference, product and quotient, each also expressed in polar form as modulus and argument.",
    'color-temp-2': "Recommends a colour temperature and illuminance level for the chosen application, then sizes total luminous flux and luminaire count from room area.",
    'concentration-20': "From system capacity and current versus target concentration, computes how much concentrate or water to add, covering both direct top-up and drain-and-refill exchange.",
    'concentration-22': "From coated area, dry film thickness, solids content and loss rate, computes theoretical and actual coating consumption in litres or kilograms.",
    'convert-21': "Converts plain decimal numbers to scientific notation and back, handling both standard power-of-ten form and E-notation such as 1.5e6.",
    'convert-22': "Converts SI unit prefixes across powers of ten, covering kilo, mega, giga, milli, micro, nano and the rest.",
    'convert-content': "Converts cigarette nicotine and tar figures between labelled content and delivered amount per cigarette so products can be compared on equal terms.",
    'detector-139': "Determines calibration intervals for measuring instruments and lists the calibration items applicable to each instrument type.",
    'detector-16': "Sizing worksheet for human-presence sensors: computes detection coverage and required sensitivity from mounting height, lens pattern and expected target motion.",
    'detector-173': "Installation and commissioning checklist covering mechanical alignment, wiring verification, no-load and loaded trial runs, and acceptance criteria.",
    'detector-175': "Equipment selection worksheet: matches required capacity against the duty point and lists the technical specifications to compare between candidate models.",
    'detector-194': "Turns a reported fault into a repair plan with symptom-to-cause mapping, the parts and tools required, and the inspection checklist that confirms the fix.",
    'detector-lifespan': "Estimates remaining tool life and the regrind interval from measured flank wear, accumulated cutting time and material removal.",
    'detector-manager-protection': "Scores occupational health risk by hazard type and exposure level, then lists the matching engineering controls and personal protective equipment.",
    'distance-power-frequency': "Estimates maximum line-of-sight transmission distance via the Friis free-space path loss equation from transmit power, frequency, transmit and receive antenna gains and receiver sensitivity.",
    'estimate-14': "Estimates used-car residual value by both the age-based and mileage-based methods from original price, age and annual mileage, then reports a blended valuation.",
    'estimate-15': "From purchase amount, tax refund rate and handling fee rate, estimates refund due, fees and net cash received, with optional currency conversion.",
    'estimate-36': "From exposure wavelength and numerical aperture, estimates lithographic resolution and depth of focus by the Rayleigh criterion for semiconductor process-node assessment.",
    'estimate-39': "From floor area and unit rates for each work item, produces a preliminary construction cost estimate together with cost per square metre.",
    'fabric-1': "From yarn linear density, warp and weft density and fabric width, computes grammage per square metre and total roll weight.",
    'fabric-3': "From yarn count, weave density and shrinkage rate, grades overall fabric quality on an A/B/C scale.",
    'flow-14': "From flow rate, head, fluid density and pump efficiency, computes hydraulic power, shaft power and motor power, then recommends a standard motor rating.",
    'flow-itinerary': "From bore diameter, stroke, system pressure and rod diameter, computes cylinder thrust and pull, swept volume per stroke and required flow.",
    'frequency-15': "From ultrasonic frequency, amplitude and tool diameter, computes vibration velocity, acceleration, power density and the resulting material removal rate.",
    'frequency-3': "From a chosen reference pitch for A4, computes the frequency of all 88 piano keys under twelve-tone equal temperament.",
    'gravity': "From each accessory weight and its arm about the gimbal axis, positive ahead of the lens and negative behind it, computes the combined centre of gravity and checks moment balance.",
    'hardness-14': "From workpiece hardness and the operation, rough grinding, finish grinding or polishing, recommends abrasive type, grit size and wheel surface speed.",
    'lifespan-10': "From material type and service conditions, scores recyclability, predicted service life and environmental suitability in one composite assessment.",
    'lifespan-12': "From equipment power, operating hours, energy saving rate and electricity tariff, computes lifetime energy savings and the payback period.",
    'lifespan-18': "From noise grade, bearing speed and duty conditions, estimates retention life for low-noise bearing designs.",
    'lifespan-20': "From precision class, applied load and rotational speed, computes precision bearing L10 rating life and precision-retention life.",
    'lifespan-23': "From oil type, operating temperature and speed, estimates lubrication life under a low-oil-mist design.",
    'lifespan-24': "From concentration, temperature and contamination level, estimates the service life of water-based cutting fluids and coolants.",
    'lifespan-25': "From cooling rate, temperature swing amplitude and material constants, computes thermal fatigue life using the Coffin-Manson relation.",
    'lifespan-26': "From operating temperature, applied stress and material constants, estimates high-temperature creep rupture life via the Larson-Miller parameter.",
    'lifespan-4': "From stress amplitude, mean stress and tensile strength, estimates fatigue life using the Goodman mean-stress correction and the Basquin equation.",
    'lifespan-5': "From temperature, humidity and pH, assesses material bio-stability life using biodegradation kinetics.",
    'lifespan-6': "From coating thickness, corrosion rate and environment class, computes remaining coating life and the recommended maintenance window.",
    'lifespan-7': "From seal material, operating temperature, pressure and shaft speed, estimates seal service life.",
    'lifespan-8': "From material type, recycling rate and process energy, computes a recyclability index together with carbon reduction and overall environmental benefit.",
    'lifespan-9': "Estimates service life of high-performance engineering materials under real duty conditions via the Arrhenius thermal degradation model combined with stress factors.",
    # ---- 第二批：中文描述清晰的功率/压力/扭矩/电气/材料/切割类（40 个）----
    'lifespan-corrosion': "From corrosion rate, initial wall thickness and corrosion allowance, estimates remaining service life and the recommended inspection interval.",
    'lifespan-wear-2': "From wear rate, allowable wear and operating time, estimates wear-out life and the recommended inspection interval.",
    'power-16': "From transmitted power, driving pulley speed and gear ratio, recommends a V-belt type, minimum pulley diameter, belt speed, centre distance and datum length.",
    'power-7': "From total kitchen-appliance power and simultaneous-use factor, computes the required demand power and current, then recommends a circuit-breaker rating and conductor cross-section.",
    'power-focal': "From laser power, focal length, cutting speed and material type, estimates maximum cutting depth, spot diameter and power density using the line-energy method.",
    'power-voltage-1': "From total load power, power factor and voltage level, computes apparent power and load current, then recommends a standard transformer capacity and loading rate.",
    'power-voltage': "From load torque, speed and voltage, computes the required motor power and recommends a standard motor power rating, pole count and motor series.",
    'pressure-18': "From room area, ceiling height, orientation and occupancy, estimates the cooling load and recommends an air-conditioner model and capacity.",
    'pressure-5': "From water pressure, abrasive flow, material type and thickness, assesses waterjet cutting capability and estimates cutting speed and time per metre.",
    'pressure-flow-4': "Based on the adiabatic compression process, computes theoretical and shaft power and recommends a compressor model and size.",
    'pressure-flow-5': "From flow rate, differential pressure and fluid density, computes the Cv/Kv flow coefficient and recommends a valve nominal diameter.",
    'pressure-flow-6': "From target purity and feed-gas purity, computes the required high-purity and dilution-gas blend flow rates for gas mixing.",
    'pressure-weld': "From spindle speed, downforce and welding speed, estimates friction-welding heat input power and specific line energy using the shoulder-friction model.",
    'rater-1': "Assists grading collectibles by the NGC/Sheldon 70-point deduction model for coins and the PSE 100-point model for stamps, scoring condition from listed flaws.",
    'ratio-50': "Computes each component amount, safety margin and reaction heat estimate for a chemical formulation ratio to support safe batching.",
    'ratio-fuel-oil': "Blends two fuels by volume ratio and computes the blended oil density, calorific value and energy density.",
    'speed-26': "From transmitted power, speed and gear ratio, recommends a chain type, sprocket tooth count and computes chain speed.",
    'speed-7': "From flight parameters and camera field of view, estimates single-pass ground coverage area, effective scan swath and survey mission time for drone operations.",
    'speed-8': "From molybdenum-wire diameter, cutting speed and workpiece thickness, estimates the actual feed rate, surface roughness Ra and corresponding machining-precision grade for WEDM.",
    'speed-9': "From cutting current, cutting speed, arc temperature and nozzle bore, estimates the maximum plasma-arc cut depth and kerf width.",
    'strength-34': "From bolt specification, strength grade and loading state, checks whether tensile and shear strength meet the requirement.",
    'strength-color-diff': "From the CIE Lab values of a standard and a sample, computes the delta-E colour difference, grey-scale fastness grade and pass/fail verdict.",
    'tax': "From the excluding-VAT construction cost, computes each tax amount and the including-VAT cost at the 9% construction VAT plus local surcharges.",
    'temp-26': "Select a gas group and temperature class to view the explosion-proof marking, typical gases and equipment-selection guidance.",
    'temp-pressure-3': "Computes internal-pressure cylindrical-shell wall thickness per GB 150, including corrosion allowance and material negative tolerance.",
    'temp-time-concentration': "From etchant concentration and temperature, estimates the etch rate and computes the time needed to reach a target depth.",
    'thread-4': "From thread specification and material type, computes cutting speed, spindle speed and feed rate.",
    'time-33': "From layer height, infill ratio, model volume and print speed, estimates total FDM print time, filament mass and length.",
    'torque-1': "From motor power, speed, reduction ratio and safety factor, computes output torque and recommends a model.",
    'torque-2': "From rated torque, service factor and safety factor, computes the selection torque and recommends a coupling type.",
    'torque-3': "From system torque and the temperature or wear compensation rate, computes the actual compensation torque required.",
    'torque-motion': "From load force, stroke, actuation time and safety factor, selects an electric actuator thrust and power.",
    'torque-response': "From speed, moment of inertia and braking time, computes the required braking torque and braking power.",
    'torque': "From bolt specification, strength grade and friction coefficient, computes fastening torque, preload and stress.",
    'turnover-2': "From stock quantity, average daily consumption and procurement lead time, computes the turnover rate, days of supply and recommended stock level.",
    'voltage-8': "From current rating, conductor count and voltage level, selects a copper-cable cross-section.",
    'voltage-9': "From current, ambient temperature, laying method and line length, selects a conductor cross-section and verifies the voltage drop.",
    'voltage-current-1': "Based on Faraday's laws of electrolysis, from current, electrolysis time and electrochemical equivalent, computes deposit mass, coating thickness and current efficiency.",
    'voltage': "From accelerating voltage, beam current and welding speed, computes electron-beam power, line energy, power density and an estimated penetration depth.",
    'wear-4': "Based on the Archard wear equation, from material hardness, contact pressure, sliding velocity and friction coefficient, computes the volumetric wear rate and estimated wear depth.",
    # ---- 第三批：detector/tester 多指标合规评估 + 专项工具（49 个，清零 p 占位）----
    'analysis-43': "Statistical analysis of engineering quantity metrics (per-unit, per-square-metre, per-linear-metre): computes mean, total and distribution of the entered dataset.",
    'analysis-44': "Investment variance analysis: computes deviation, trend and corrective benchmarks from the entered series to support rebalancing decisions.",
    'assessor-20': "Micro-machining quality assessment: scores machining accuracy, heat-affected-zone width, cutting speed and laser power against precision targets.",
    'calc-stats-1': "Statistical distribution calculator: computes probability, mean and variance for normal, Poisson and binomial models from the entered dataset.",
    'detector-118': "Composite quality-assurance scoring for products: rates standards conformance, inspection pass rate, environmental compliance and certified management system into an overall qualification verdict.",
    'detector-121': "Composite compliance check for thermal-insulation materials: scores thermal conductivity, flame-retardant class and environmental pass rate against regulatory thresholds.",
    'detector-123': "Composite compliance check for bonding and waterproofing materials: scores bond strength, impermeability grade and environmental pass rate.",
    'detector-126': "Composite compliance check for adhesive joints: scores bond strength, post-aging strength retention and environmental pass rate.",
    'detector-128': "Composite quality check for industrial oils and lubricants: scores kinematic viscosity at 40C, water content and flash point against grade specifications.",
    'detector-131': "Composite compliance check for concrete and masonry: scores compressive strength, impermeability grade and environmental pass rate.",
    'detector-134': "Composite quality check for rubber and elastomer products: scores breaking tenacity, elongation at break and abrasion loss.",
    'detector-155': "Composite condition assessment for rotating machinery: scores vibration velocity, radial clearance and rotational accuracy against running-tolerance limits.",
    'detector-159': "Composite rating for spring and support components: scores stiffness, rated load and fatigue life against design limits.",
    'detector-200': "Composite quality check for petroleum and lubricating oils: scores kinematic viscosity, water content and acid value (TAN) against specification limits.",
    'detector-205': "Composite corrosion and adsorption rating for surface-treated parts: scores salt-spray hours, damp-heat test duration and adsorption capacity.",
    'detector-207': "Composite rating for mould-release agents: scores demoulding force, residue level and environmental compliance.",
    'detector-211': "Composite purity check for chemical raw materials: scores purity, moisture content and impurity level against grade limits.",
    'detector-213': "Composite purity check for oils and esters: scores purity, moisture content and acid value (TAN) against specification limits.",
    'detector-aging-1': "Composite safety rating for heat-resistant materials: scores heat-resistance temperature, post-aging strength retention and safety class.",
    'detector-aging-2': "Composite durability rating for elastic and foam materials: scores compressive strength, resilience and post-aging mass-change rate.",
    'detector-aging': "Composite reliability rating for electrical enclosures: scores withstand voltage, temperature rating and aging endurance time.",
    'detector-composition-1': "Composite quality scoring for formulated products: rates main-component content, performance pass rate and overall quality score.",
    'detector-composition-aging': "Composite rating for cooling and thermal materials: scores cooling efficiency, post-aging performance retention and composition conformance.",
    'detector-composition': "Composite compliance check for chemical products: scores composition conformance, purity and environmental pass rate.",
    'detector-concentration-1': "Composite rating for aqueous process fluids: scores concentration, pH value and rust-prevention grade against control limits.",
    'detector-concentration-2': "Composite rating for suspensions and slurries: scores mean particle size, concentration and pH value against specification.",
    'detector-concentration': "Composite hygiene rating for water and cleaning solutions: scores concentration, pH value and total bacterial count (CFU/mL).",
    'detector-corrosion-1': "Composite rating for greases and lubricants: scores dropping point, cone penetration and corrosion-test grade.",
    'detector-corrosion': "Composite rating for cleaning and pickling processes: scores cleaning efficiency, corrosion rate and residual contaminant level.",
    'detector-hardness-lifespan-1': "Composite rating for wear-resistant parts: scores hardness, abrasion loss and service life against endurance targets.",
    'detector-hardness-lifespan': "Composite rating for abrasive and granular materials: scores mean particle size, hardness and service life.",
    'detector-hardness-torque': "Composite rating for fastened and machined parts: scores tightening torque, hardness and dimensional deviation against tolerance.",
    'detector-length-lifespan': "Composite rating for belts and tensile members: scores tension strength, length deviation and fatigue life.",
    'detector-pressure-torque': "Composite rating for sealed connectors and fittings: scores seal leakage rate, pressure rating and tightening torque.",
    'detector-protection-2': "Composite rating for hazardous-area equipment: scores explosion-proof class, sealing class and ingress-protection (IP) grade.",
    'detector-resistance-1': "Composite safety rating for earthing and lightning-protection systems: scores earthing resistance, lightning-protection class and equipotential-bonding resistance.",
    'detector-resistance-aging': "Composite rating for insulating materials: scores insulation resistance, volume resistivity and post-aging insulation retention.",
    'detector-resistance': "Composite rating for electrical insulation: scores insulation resistance, volume resistivity and withstand voltage.",
    'detector-strength-lifespan': "Composite rating for porous and structural parts: scores aperture deviation, tensile strength and service life.",
    'detector-stretch': "Composite rating for tensile and rubber products: scores abrasion loss, tensile strength and fatigue-cycle count.",
    'detector-water-pressure-1': "Composite non-destructive rating for pressure vessels: scores UT sensitivity, MT indication grade and hydrostatic test pressure multiple.",
    'detector-water-pressure': "Composite integrity rating for pressurized equipment: scores NDT pass rate, hydrostatic hold time and pneumatic leakage rate.",
    'generator-23': "Logic truth-table generator: builds the complete truth table for a Boolean expression and outputs the requested number of rows.",
    'generator-24': "24-point puzzle generator: produces the requested number of arithmetic puzzles solvable to 24 using addition, subtraction, multiplication and division.",
    'generator-25': "Magic-square generator: builds odd-order magic squares where every row, column and diagonal sums to the same constant.",
    'recommender-24': "Substitution recommender: suggests alternative products or solutions from the entered criteria and lists the recommended options.",
    'stats-energy': "Energy-consumption dashboard: computes statistics (mean, peak, trend) and a short forecast from the entered consumption series.",
    'tester-40': "Maintenance decision support: selects repair, replace or test actions for equipment by fault type and tallies the required test items.",
    'tester-maintenance': "Maintenance planning support: recommends replacement, servicing or testing based on equipment type, service level, age and accumulated run-hours.",
    # ---- 第四批：英文描述层收尾（p 已真实、ed 仍有套话尾巴 / analysis-21 纯套话） ----
    'analysis-21': "Analyze multispectral (NDVI) imagery; conversion factors follow SI and relevant standards, with results keeping input precision.",
    'bearing': "Estimate motor bearing maintenance interval from bore and speed (dn factor).",
    'calc-13': "Compute calendar and workday differences between two dates.",
    'calc-14': "Compute exact age in years, months and days.",
    'calc-196': "Compute insulation thickness to control surface temperature.",
    'calc-197': "Compute the LMTD and required heat-transfer area from heat duty, fluid temperatures and the overall heat-transfer coefficient.",
    'calc-200': "Compute required motor power from load and efficiency.",
    'calc-203': "Per ISO 286 (GB/T 1800), compute hole and shaft deviations and the resulting clearance or interference from the basic size and a fit code such as H7/g6.",
    'calc-204': "Compute formwork support spacing by bearing-area method.",
    'calc-205': "Compute steel quantity for double-row coupler scaffolds.",
    'calc-206': "Verify single-standard coupler scaffold safety under load.",
    'calc-21': "Compute windfall tax and net lottery prize.",
    'calc-94': "Adjust project cost by material, labor and equipment indices.",
    'dianhuaxuedunhuakongzhi': "Control electrochemical passivation of iron by the Pourbaix (E-pH) diagram.",
    'fengjixuanxingjisuan': "Size fan shaft and motor power from airflow and pressure.",
    'gongchengzaojiazhishujisuan': "Compute construction cost indices from materials and labor.",
    'gongyebengxuanxing': "Select an industrial pump from flow rate, head and medium type.",
    'gongyeshebeigonglvpipei': "Match motor power to load, speed and drive efficiency.",
    'hanjiegongyicanshu': "Set welding parameters by material thickness and process (SMAW/TIG/MIG).",
    'huanbaonaimopinggu': "Evaluate eco-friendly wear resistance by material and environment (temp, humidity).",
    'jienengfanganjisuan': "Estimate annual energy savings from power, runtime and saving rate.",
    'jiguanghanjieguangbanjisuan': "Compute laser weld spot size from Gaussian focus, M^2 and defocus.",
    'jiguangrongfuhoudujisuan': "Estimate single-pass laser cladding height from powder mass and parabolic cross-section.",
    'jingmishebeixuanxing': "Select precision equipment by accuracy, load, stroke and speed.",
    'kongtiaolengfuhejisuan': "Compute HVAC cooling load from envelope, solar, occupancy and equipment gains.",
    'liangshuzhihe-chengjizuida-zuixiao-shuxueti': "Solve math problems for the maximum/minimum sum or product of two numbers.",
    'lizishujianshejisuan': "Compute ion beam sputtering yield from energy, angle, target Z and current density.",
    'naimoxingpinggujisuan': "Evaluate wear resistance with the Archard wear equation.",
    'nianjieqiangdujisuan': "Compute adhesive bond strength from area and shear strength.",
    'pidaizhangjinjisuan': "Calculate V-belt tension from pitch, center distance, speed and power.",
    'rechengxiangwenchapandu': "Read infrared thermal delta-T from ambient temp and emissivity.",
    'runhuayougenghuanzhouqi': "Estimate lubricant change interval by Arrhenius law from oil capacity.",
    'runhuayouzhanduxuanxing': "Select lubricant viscosity by temperature, load and speed.",
    'shachepiangenghuanzhouqi': "Estimate brake pad replacement interval from current, new and wear-rate thickness.",
    'shebeiweihuzhouqi': "Plan equipment maintenance interval by type and daily runtime.",
    'shebeizulinfeilvjisuan': "Compute equipment lease rate by straight-line depreciation, maintenance and target margin.",
    'shusongdaixuanxingjisuan': "Size conveyor belt width and drive power from capacity, distance and incline.",
    'taocizhouchengshoumingjisuan': "Compute ceramic bearing L10 rated life by ISO 281.",
    'wurenjixuantingwuchajisuan': "Estimate UAV hover error from GPS, barometer and wind effects.",
    'zhilengshebeixuanxing': "Size refrigeration equipment and estimate ideal Carnot COP from cooling load and temperatures.",
    'zhiliangyanshouchouyang': "Plan acceptance sampling by lot size N and standard attribute plans.",
}


def main():
    do_apply = '--apply' in sys.argv
    if not do_apply and '--dry-run' not in sys.argv:
        print('用法: python3 scripts/fix_general_en_p.py --dry-run | --apply')
        return 1

    changed, skipped = 0, []
    for slug, en in EN_MAP.items():
        path = os.path.join(ROOT, 'tools', 'general', slug + '.html')
        if not os.path.exists(path):
            skipped.append((slug, 'file-missing'))
            continue
        src = open(path, encoding='utf-8').read()
        src_pat = PAT
        hits = list(PAT.finditer(src))
        if not hits:
            # 回退：页面 <p> 已是真实英文，按 data-zh 定位唯一英文 <p> 以同步 EN_MAP 变更
            cand = [m for m in PAT_ANY.finditer(src)
                    if m.group(2).strip() and not CJK.search(m.group(2))]
            if len(cand) == 1:
                hits = cand
                src_pat = PAT_ANY
        if not hits:
            skipped.append((slug, 'no-match'))
            continue
        if len(hits) > 1:
            skipped.append((slug, 'multi-match:%d' % len(hits)))
            continue
        new_src = src_pat.sub(lambda m: m.group(1) + en + m.group(3), src, count=1)
        if new_src == src:
            skipped.append((slug, 'no-change'))
            continue
        if do_apply:
            open(path, 'w', encoding='utf-8').write(new_src)
        changed += 1

    tag = 'APPLY' if do_apply else 'DRY-RUN'
    print('%s: 本次处理 %d 个, 跳过 %d 个' % (tag, changed, len(skipped)))
    for slug, reason in skipped[:30]:
        print('  skip  %-32s %s' % (slug, reason))
    return 0


if __name__ == '__main__':
    sys.exit(main())
