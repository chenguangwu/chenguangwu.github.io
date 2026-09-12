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
        hits = list(PAT.finditer(src))
        if not hits:
            skipped.append((slug, 'no-match'))
            continue
        if len(hits) > 1:
            skipped.append((slug, 'multi-match:%d' % len(hits)))
            continue
        new_src = PAT.sub(lambda m: m.group(1) + en + m.group(3), src, count=1)
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
