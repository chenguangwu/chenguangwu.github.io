#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'electronics')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'electronics')
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
    out = {'slug': slug, 'industry': 'electronics', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
#!/usr/bin/env python3
DISCL_E = " This is a basic electronics calculation aid; results are for circuit design and teaching reference only and do not replace formal PCB design, EMC and product reliability requirements."

def main():
    write('pcb-power', build('pcb-power', [
        "\u26A1 PCB Power Temperature Rise Estimate",
        "Estimate board temperature rise from the cooling area and convection conditions (empirical model, for reference only)",
        "Core formulas (by input): min(density\u00F70.2\u00D7100,100); 0.4 + 0.6\u00D7(cov\u00F7100); a \u00F7 10000",
        "\U0001F4D6 See the \"PCB Power Temperature Rise User Guide\"",
        "Total power P (W)",
        "Cooling area A (cm\u00B2)",
        "Copper thickness",
        "Convection condition",
        "Natural convection (still air)",
        "Light airflow (1~2 m/s)",
        "Strong airflow (3~5 m/s)",
        "Forced air cooling (>5 m/s)",
        "Copper coverage (%)",
        "\u26A1 Estimate temperature rise",
        "Click to estimate",
        "Estimation notes",
        "Calculation model",
        "Temperature rise \u0394T = P / (h \u00D7 A_eff), where h is the convective heat transfer coefficient (W/m\u00B2\u00B7K) and A_eff the effective cooling area.",
        "The effective area is corrected for copper thickness and coverage ratio: thicker and wider copper spreads heat better.",
        "Power density reference",
        "Below 0.05 W/cm\u00B2: conventional design, temperature rise stays under control",
        "0.05 ~ 0.15 W/cm\u00B2: watch the thermal design and consider more copper",
        "Above 0.15 W/cm\u00B2: dense heating, forced air cooling or a heatsink is advised",
        "\U0001F4DA In-depth analysis: PCB Power Temperature Rise Estimate",
        "5W on board with natural cooling: about 30\u00B0C rise (no copper pour assist).",
        "Large copper pour: 5W over 50cm\u00B2 gives under 10\u00B0C rise.",
        "Forced air at 1m/s: the heat transfer coefficient improves 2~3 times.",
        "Thermal via array: nine 0.3mm vias under the IC cut 10\u00B0C.",
        "3W on board, 25cm\u00B2, with copper pour",
        "Natural cooling \u0394T\u224812\u00B0C; ambient 25\u00B0C gives a board at 37\u00B0C; a 0.5mm aluminium base plate removes 50%.",
        "Why does copper pour lower PCB temperature rise?",
        "Copper conducts heat at 400W/m\u00B7K, so a pour enlarges the cooling area and evens out temperature, while also lowering ground impedance and EMI." + DISCL_E,
        "How are thermal vias chosen?",
        "Use 0.2~0.3mm holes on a 1mm pitch, filled with solder or copper paste so the thermal resistance stays below 5\u00B0C/W." + DISCL_E,
        "Why do multilayer boards cool better?",
        "Inner copper planes sit in parallel with the outer layers thermally; power and ground planes double as heat spreaders with high thermal capacity." + DISCL_E,
        "About \"PCB Power Temperature Rise Estimate\"",
        "This tool estimates board temperature from onboard power, cooling area and convection conditions, helping with thermal checks on power and power-amplifier boards; it runs entirely in the browser and uploads no data.",
    ]))

    write('pcbzukangdieceng', build('pcbzukangdieceng', [
        "\u26A1 PCB Impedance Stackup",
        "Enter dielectric constant, trace width, dielectric thickness and copper thickness to compute microstrip characteristic impedance",
        "Core formulas (by input): 87\u00F7\u221A(er+1.41)\u00D7Math.log(5.98\u00D7h\u00F7(0.8\u00D7w+t))",
        "\U0001F4D6 See the \"PCB Impedance Stackup User Guide\"",
        "Dielectric constant Er",
        "Trace width (mm)",
        "Dielectric thickness (mm)",
        "Copper thickness (mm)",
        "\U0001F4A1 Microstrip impedance Z0 = 87/\u221A(Er+1.41) \u00D7 ln(5.98\u00D7H/(0.8\u00D7W+T)) (simplified IPC-2141 form)",
        "Applies to microstrip (surface traces)",
        "FR4 dielectric constant is about 4.2~4.6",
        "Stripline impedance needs a different formula",
        "\U0001F4DA In-depth analysis: PCB Impedance Stackup",
        "USB differential 90\u03A9: Dk=4.2, H=0.2mm, W=0.4mm, S=0.2mm.",
        "HDMI 100\u03A9 differential: Dk=4.5, H=0.15mm, W=0.25mm.",
        "RF 50\u03A9 single-ended: Dk=4.2, H=0.5mm, W\u22480.95mm.",
        "DDR 50\u03A9 single-ended: Dk=3.8, H=0.1mm, W\u22480.18mm.",
        "Microstrip Z\u2080\u224856\u03A9; stripline needs a different formula (two reference planes).",
        "Microstrip versus stripline?",
        "A microstrip has only one reference plane and a half-open field; a stripline has planes on both sides and a closed field, so the impedance formulas differ." + DISCL_E,
        "What is the real value of Dk?",
        "FR4 Dk=4.2~4.6 (frequency dependent); at high frequency Rogers RO4350 holds Dk=3.48 steadily, and high-speed links want low loss tangent." + DISCL_E,
        "How tight is the impedance tolerance?",
        "Single-ended is typically \u00B110% and differential \u00B18%; high-speed serial links (PCIe, for example) usually need \u00B15% with the fab tuning trace width." + DISCL_E,
        "About \"PCB Impedance Stackup\"",
        "This tool uses the simplified IPC-2141 formula to compute microstrip characteristic impedance from dielectric constant, trace width, dielectric thickness and copper thickness, making it a basic tool for impedance control on high-speed digital and RF PCBs.",
        "Microstrip impedance calculation",
        "IPC-2141 standard formula",
        "Parameters adjust in real time",
        "High-speed PCB impedance control",
        "Stackup structure design",
        "Trace width impedance tuning",
        "RF circuit routing",
        "Dielectric constant Er",
        "Trace width (mm)",
        "Dielectric thickness (mm)",
        "Copper thickness (mm)",
    ]))

    write('resistor-calculator', build('resistor-calculator', [
        "\U0001F9EE Resistance Calculator",
        "Series/parallel/colour code/divider",
        "Core formulas (by input): (b1.v \u00D7 10 + b2.v) \u00D7 b3.m; min(...rs); max(...rs)",
        "Resistance Calculation",
        " / Resistance Calculation",
        "\U0001F4D6 See the \"Resistance Calculator User Guide\"",
        "\U0001F4DA In-depth analysis: Resistance Calculator",
        "Current limiting: LED with Vcc=5V, Vf=2V, If=10mA \u2192 R=300\u03A9 at 1/4W.",
        "Divider sampling: Vin=12V, Vout=3V \u2192 R1:R2=3:1, for example 30k\u03A9 + 10k\u03A9.",
        "Pull-up resistor: on I\u00B2C the 4.7k\u03A9 value plus bus capacitance sets the rise time.",
        "\u03C0 attenuator: 6dB/10dB/20dB pads for 50\u03A9 systems.",
        "LED limiting 5V\u21922V 10mA",
        "R=300\u03A9, P=I\u00B2R=0.03W \u2192 choose 300\u03A9 1/4W (8 times headroom).",
        "How much power rating?",
        "Rate at least 4 times the actual dissipation (long-term derating to 25%); for pulse loads use I\u00B2t." + DISCL_E,
        "Why are there E24 and E96 series?",
        "E24 has 5% tolerance in 24 steps and E96 has 1% in 96 steps; pick E96 when precision matters." + DISCL_E,
        "How do I choose a pull-up value?",
        "I\u00B2C typically uses 4.7k\u03A9 (balancing speed and power); long lines need it reduced to 2.2k\u03A9 or lower." + DISCL_E,
        "About \"Resistance Calculation\"",
        "Resistance Calculation covers series/parallel equivalent resistance, voltage division and power budgeting, making it a basic tool for electronic circuit design and component selection; it runs entirely in the browser and uploads no data.",
    ]))

    write('smt-stencil', build('smt-stencil', [
        "\U0001F4D0 SMT Stencil Design",
        "Stencil aperture sizing with area ratio, aspect ratio and solder paste volume",
        "Core formulas (by input): min(160\u00F7apL, 160\u00F7apW, 120); padW\u00D7(1-reduce\u00F7100); padL\u00D7(1-reduce\u00F7100)",
        "\U0001F4D6 See the \"SMT Stencil Design User Guide\"",
        "Pad width W (mm)",
        "Pad length L (mm)",
        "Stencil thickness (mm)",
        "Aperture reduction ratio (%)",
        "Component pitch (mm)",
        "Aperture shape",
        "Paste transfer rate (%)",
        "\U0001F4D0 Design calculation",
        "Design rules",
        "Area ratio",
        "(Area Ratio) = aperture area / aperture wall area, 0.66 or above recommended",
        "Aspect ratio",
        "(Aspect Ratio) = aperture width / stencil thickness, 1.5 or above recommended",
        "For fine pitch (\u22640.5mm) reduce the aperture a little to prevent bridging",
        "When the area ratio is low, use a stepped or electroformed stencil",
        "\U0001F4DA In-depth analysis: SMT Stencil Design",
        "QFP pins: aperture width 90% of pad width, length 100% of pad length.",
        "0402 parts: aperture equal to pad width, length +0.1mm.",
        "BGA with 0.5mm balls: use a 0.45mm round aperture in the stencil.",
        "CSP/WLCSP: apertures at 80% to avoid bridging.",
        "0603 pad 1.6\u00D70.8mm",
        "Stencil aperture 1.6\u00D70.9mm; area ratio about 0.7 (compliant); paste volume 0.21mm\u00B3.",
        "Why are apertures smaller than pads?",
        "To stop paste overflowing and bridging; making apertures 10~20% smaller than leads or pads is the rule of thumb (IPC 7525)." + DISCL_E,
        "Area ratio versus aspect ratio?",
        "Area ratio = aperture area / side wall area, above 0.66 for easy release; aspect ratio = aperture width / stencil thickness, above 1.5 for clean release." + DISCL_E,
        "Laser versus etched stencils?",
        "Laser stencils have smoother walls and suit fine-pitch QFP/BGA; etching is cheaper but leaves rough walls that bridge easily." + DISCL_E,
        "About \"SMT Stencil Design\"",
        "SMT Stencil Design computes aperture area ratio, aspect ratio and paste volume from PCB pad dimensions and process requirements, making it a basic tool for SMT process design; it runs entirely in the browser and uploads no data.",
    ]))


if __name__ == '__main__':
    main()
