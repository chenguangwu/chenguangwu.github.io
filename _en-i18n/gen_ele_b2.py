#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'electrical')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'electrical')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
DISCL = "Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected."
EXTRA = {}
def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items)); sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en)); sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en)); sys.exit(1)
        mp[z] = en
    return mp
def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'electrical', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('voltage-drop', build('voltage-drop', [
        "🎚️ Voltage Drop Calculation",
        "Low-voltage line voltage drop calculation and conductor cross-section selection, supporting single-phase and three-phase systems.",
        "Core formula (by input variable): dropV÷baseU×100; P×1000÷(baseU×cos)",
        "System type",
        "Transmitted power P (kW)",
        "Line length L (m)",
        "Copper (ρ=0.0184)",
        "Aluminium (ρ=0.0294)",
        "Conductor cross-section S (mm²)",
        "Allowed voltage drop (%)",
        "Back-calculate the required cross-section",
        "📋 Calculation notes",
        "Voltage drop formula (resistive approximation):",
        "• Three-phase: ΔU = √3 × I × R × cosφ × L / 1000 (V), where R = ρ / S",
        "• Single-phase: ΔU = 2 × I × R × cosφ × L / 1000 (V)",
        "• Current I = P / (U × cosφ × phase factor)",
        "Resistivity ρ (Ω·mm²/m):",
        "Copper 0.0184, aluminium 0.0294 (at a working temperature of about 60°C)",
        "Allowed voltage drop:",
        "Generally ≤5% for power circuits and 2.5%-3% for lighting.",
        "📚 Deep dive: Voltage Drop Calculation",
        "Long-distance distribution: 50m of 4mm² copper single-phase at 20A gives U% = 5.5%, so it must be increased to 6mm².",
        "Photovoltaic DC side: 30m of 4mm² DC cable with a 6A load, verifying the voltage drop is ≤3%.",
        "Motor terminal voltage: for a 50m supply distance, verify the terminal voltage at starting stays ≥90% of Un.",
        "LED fixture supply: low-voltage 24V long-distance feeders where voltage drop directly affects illuminance.",
        "100m of 2.5mm² copper at 220V, 10A, single-phase",
        "R = 0.0175×100/2.5 = 0.7Ω; U% = 2×10×0.7/220×100% ≈ 6.4%, above 5%, so a thicker conductor is required.",
        "Why multiply the resistance by 2?",
        "In a single-phase two-wire system (live plus neutral) the current travels through both the outgoing and the return conductor, so you multiply by 2; a balanced three-phase system only needs the √3 factor. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "What harm does too much voltage drop cause?",
        "Motor starting torque becomes insufficient and it overheats, lighting illuminance drops, electronics reset, and capacitor compensation fails. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "How do I reduce the voltage drop?",
        "Increase the cross-section, shorten the supply distance, raise the supply voltage level, or install voltage regulation and compensation equipment nearby. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "About \"Voltage Drop Calculation\"",
        "The Voltage Drop Calculation is an online tool for electrical engineering that verifies the voltage drop percentage from conductor length, cross-section and load current, running entirely in the front end with no data uploaded.",
    ]))

    write('transformer-sizing', build('transformer-sizing', [
        "🧊 Transformer Capacity Sizing",
        "Distribution transformer kVA capacity sizing, recommending a model from the calculated load and the standard capacity series.",
        "Core formula (by input variable): Math.ceil(St÷100)×100; pick÷(√(3)×uKv)",
        "Total active calculated load P (kW)",
        "Demand factor Kd",
        "Transformer load factor β (economic load factor)",
        "Reserve factor (1.0-1.2)",
        "System voltage U (kV)",
        "Calculate the model",
        "📋 Sizing notes",
        "Apparent calculated load Sjs = P × Kd / cosφ",
        "Transformer capacity St ≥ Sjs × reserve factor / load factor",
        "Common oil-immersed transformer standard capacity series (kVA):",
        "Recommended load factor:",
        "An economic running load factor is 0.65-0.8; 0.75 is commonly used.",
        "📚 Deep dive: Transformer Capacity Sizing",
        "Factory distribution transformer: a 800kVA load with a 0.7 simultaneity factor plus 1.25 reserve leads to choosing 1000kVA.",
        "Photovoltaic grid-tie step-up: 1000V DC to 400V AC, choose a boxed step-up transformer.",
        "Rectifier transformer: a 12-pulse rectifier paired with a phase-shifting transformer.",
        "Data centre UPS input transformer: Class K or Class H insulation for high temperature resistance.",
        "Load S = 600kVA, cosφ = 0.85, simultaneity 0.8, reserve 1.2",
        "P = 600×0.85 = 510kW; S_selected = 510/(0.8×1.2) ≈ 531kVA, so 630kVA is chosen from the standard series.",
        "Why size the capacity by apparent power?",
        "The transformer nameplate is marked in kVA rather than kW, and the winding insulation and temperature rise are determined by the current, independent of",
        ". This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "How do I choose the short-circuit impedance Uk%?",
        "Generally 4%-6% for distribution transformers; a higher impedance lowers the short-circuit current and makes protection easier to set, but brings more voltage drop and slightly higher losses. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "How does the efficiency grade affect the choice?",
        "SC10/SC11/SC12 dry-type and SH15 oil-immersed units are Class 1 energy efficiency, which saves noticeably on electricity over long-term running. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "About \"Transformer Capacity Sizing\"",
        "The Transformer Capacity Sizing tool is an online tool for electrical engineering that picks kVA from apparent power, simultaneity factor and reserve factor, running entirely in the front end with no data uploaded.",
    ]))

    write('power-factor-compensation', build('power-factor-compensation', [
        "🔌 Power Factor Compensation",
        "Compensation capacitor capacity calculation: the capacitor capacity needed to raise the power factor from its current value to the target value.",
        "🔌 Power Factor Compensation",
        "Current power factor cosφ1",
        "Target power factor cosφ2",
        "Compute the compensation capacity",
        "📋 Compensation principle",
        "Compensation capacity formula:",
        "where φ = arccos(cosφ), tanφ = sinφ / cosφ",
        "Compensation effect:",
        "• Apparent power drops from S1 to S2",
        "• Reactive power drops from Q1 to Q2",
        "• Line current drops accordingly, reducing losses",
        "Rule of thumb:",
        "The target power factor is usually taken as 0.9-0.95; going too high (such as 0.98+) tends to over-compensate and is not economical.",
        "📚 Deep dive: Power Factor Compensation",
        "Factory",
        "analysis: identify the low cosφ equipment (motors, welding machines, rectifiers).",
        "Utility assessment: high-voltage customers are penalized when cosφ falls short of the requirement.",
        "Reading your electricity bill: understand the power factor adjustment charge.",
        "Capacitor compensation setup: stage the automatic switching to prevent over-compensation.",
        "Load P = 100kW, cosφ = 0.8",
        "S = P/cosφ = 125kVA; Q = P×tanφ = 75kvar; raising it to 0.95 requires 42kvar of compensation.",
        "Is the closer cosφ is to 1 the better?",
        "0.95-1 is excellent and below 0.85 gets penalized, but forcing it above 1 over-compensates and feeds reactive power back, raising the voltage and overloading equipment. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "What are displacement factor and distortion factor?",
        "Displacement factor = the fundamental cosφ; distortion factor = the phase shift caused by harmonics; total power factor = displacement × distortion. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "How do I improve the power factor?",
        "Prefer equipment with a high cosφ, compensate capacitors locally, and size motors properly so they do not run unloaded. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "About \"Power Factor Compensation\"",
        "The Power Factor Compensation tool is an online tool for electrical engineering focused on cosφ correction and compensation capacity verification, running entirely in the front end with no data uploaded.",
    ]))

    write('calc-2', build('calc-2', [
        "🧮 Three-Phase Power Calculation",
        "Computes active power, reactive power, apparent power and the current deviation from the three-phase voltage, current and power factor.",
        "Line voltage U (V)",
        "Line current I (A)",
        "U, I and cosφ known",
        "U, P and cosφ known",
        "U, Q and cosφ known",
        "Active power P (kW)",
        "Reactive power Q (kvar)",
        "Three-phase active power P = √3 × U × I × cosφ",
        "Three-phase reactive power Q = √3 × U × I × sinφ",
        "Three-phase apparent power S = √3 × U × I",
        "Power factor angle φ = arccos(cosφ), sinφ = √(1 - cos²φ)",
        "📚 Deep dive: Three-Phase Power Calculation",
        "380V three-phase motor: I=50A, cosφ=0.82 → P=26.9kW, Q=19.7kvar, S=32.8kVA.",
        "Post-compensation decision: raise cosφ from 0.78 to 0.95 and solve for the compensation capacitor capacity.",
        "Line current deviation: back-calculate the current cosφ from P and the measured U/I to spot under- or over-compensation.",
        "Single-phase load conversion: when three phases are unbalanced, compute total power and line losses phase by phase.",
        "10kW three-phase heater with cosφ=0.95",
        "Why is the line current √3 times the phase current?",
        "In a balanced three-phase system the line current equals the phase current,",
        "while in a delta connection it needs a further ×√3 (U_line/U_phase); in a star connection the two are equal. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "Why does cosφ have to be corrected above 0.9?",
        "Utilities generally require high-voltage customers to keep cosφ ≥ 0.9, otherwise they are",
        "penalized through the power factor adjustment charge; line losses and equipment capacity utilization also improve. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "What is the vector relationship between S, P and Q?",
        "S² = P² + Q²; cosφ = P/S, sinφ = Q/S; for a purely resistive load Q=0 and for a purely inductive load P=0. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "Available options",
    ]))

if __name__ == '__main__':
    main()
