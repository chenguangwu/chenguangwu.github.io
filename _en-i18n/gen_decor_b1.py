#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'decor')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'decor')
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
    out = {'slug': slug, 'industry': 'decor', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('ceiling-panel-quantity', build('ceiling-panel-quantity', [
        '/ Ceiling Panel Quantity Calculator',
        '📖 View the User Guide for Ceiling Panel Quantity Calculator',
        '📐 Ceiling Panel Quantity Calculator',
        'Estimate materials before ceiling work: enter room length/width, panel spec and waste rate to get the number of panels, main/secondary keel usage and purchase advice, avoiding over-buying waste or short-buy reorder.',
        'Ceiling area = room length × width; panel qty = ceiling area ÷ single panel area × (1 + waste rate 5% to 10%), rounded up to whole panels; main keel qty ≈ area ÷ main keel spacing (about 1.2 m) ÷ keel length; secondary keel qty ≈ area ÷ secondary keel spacing (about 0.6 m) ÷ keel length; edge trim length = room perimeter, converted to pieces by 2.4 m or 3 m each.',
        'Panel length (mm)',
        'Panel width (mm)',
        '📚 Deep Dive: Ceiling Panel Quantity Calculator',
        'Home living/dining ceiling: enter clear length × width and chosen spec, first get main-face panel count, then compute main keel (along long side) and secondary keel (perpendicular) by spacing, with 5%–10% waste reserved, then output a purchase list.',
        'Kitchen/bath aluminum gusset ceiling: for small spaces prefer 300×300 / 600×600 spec, divide area by single panel area for count, include edge cutting waste; keel spacing per national standard 600–1200 mm.',
        'Partial feature ceiling: for irregular areas use block decomposition + raised waste; add an extra 10%–15% waste at complex curves to avoid color difference from a second reorder.',
        'Living/dining aluminum gusset usage',
        'Example: length 5.2 m, width 3.6 m, choose 600×600 mm aluminum gusset (0.36 m² per panel), waste rate 8%.',
        'What waste rate is usually taken?',
        'Plain flat ceiling 5%–8%, irregular/mosaic 10%–15%, depending on cutting complexity and layout.',
        'Are there rules for keel spacing?',
        'Home light-gauge steel keel: main keel spacing usually 600–1200 mm, secondary keel 300–600 mm, must meet ceiling load and panel lap requirements.',
        'What if it differs from the contractor\'s measure?',
        'This tool estimates by input spec and waste rate; actual is subject to on-site re-measurement; counts vary by layout, so make a sample first then bulk purchase.',
        'Net qty = ceiling area ÷ single panel area, rounded up',
        'Purchase qty = net qty × (1 + waste rate), cutting and edge waste',
        'Main keel estimated at 1.2 m spacing; irregular ceilings vary greatly in usage',
        'This tool is an estimation reference; for precise quantity combine drawings with on-site measurement',
    ]))
    write('curtain-fabric', build('curtain-fabric', [
        '🧮 Curtain Fabric Calculator',
        'Compute required fabric by curtain rod width and height combined with fullness ratio',
        '📖 View the User Guide for Curtain Fabric Calculator',
        'Fabric length per panel = finished height + top/bottom hems + pattern-match waste',
        'Curtain rod / track width (m)',
        'Curtain finished height (m)',
        'Fullness ratio',
        '1.5x (simple, few folds)',
        '2x (standard, elegant)',
        '2.5x (luxury, many folds)',
        '3x (extreme stacking)',
        'Fabric and hems',
        'Fabric width (m)',
        '2.8 m (fixed-height buy-width)',
        '1.5 m (fixed-width buy-height)',
        'Left/right hems (m, each side)',
        'Top/bottom hems (m, total)',
        'Pattern-match waste (m, 0 if no pattern)',
        'Fixed-height buy-width',
        '(width 2.8 m, cut once along height): required fabric width = rod width × fullness ratio',
        '• Required panels = required fabric width ÷ fabric width (rounded up)',
        '• Fabric length per panel = finished height + top/bottom hems + pattern-match waste',
        'Total fabric',
        '= panels × fabric length per panel',
        '• Fullness ratio: living room/bedroom 2x, sheer curtains 2.5–3x, minimalist style 1.5x',
        '• Full-wall curtain height should be measured to the ceiling or below the cornice; floor-length leaves 2–3 cm margin',
        '📚 Deep Dive: Curtain Fabric Calculator',
        'Living-room French window: enter window width and finished height, choose fullness 2.0 and fabric width 1.4 m, compute total meters by window width × fullness ÷ fabric width rounded up × single-panel height + waste.',
        'Bedroom blackout curtain: when joined widths are insufficient, pattern matching is needed, add extra pattern-match waste; double-layer curtains (sheer + fabric) are counted separately.',
        'Roman/roller blinds: estimate by window width × window height × ratio + top/bottom roll hems; irregular windows counted in blocks.',
        'Full-window curtain fabric',
        'Example: window width 3.0 m, height 2.6 m, fullness 2.0, fabric width 1.4 m, top/bottom hems total 0.3 m.',
        'How to choose the fullness ratio?',
        'Sheer 1.5–1.8, cotton/linen 1.8–2.0, velvet/European 2.0–2.2; a larger ratio looks more draping but uses more fabric.',
        'How is pattern-match waste calculated?',
        'Fabric with a repeating pattern needs each panel aligned to the pattern repeat; usually add one repeat (about 0.1–0.3 m) per panel; solid color can be ignored.',
        'Can extra fabric be returned?',
        'Curtain fabric is usually sold cut by the meter and generally not returnable whole; use this tool to estimate precisely, leave a small margin, then buy more if needed.',
        'About Curtain Fabric Calculator',
        'The Curtain Fabric Calculator computes required fabric by curtain rod width and height, combined with fullness ratio, fabric width and hem allowance.',
        'Multiple fullness ratios supported',
        'Adjustable fabric width and hems',
        'Pattern-match waste auto-included',
        'Home curtain fabric purchase',
        'Soft-decoration design budget',
        'Double-layer curtain usage estimate',
        'Engineering soft-decoration material tally',
    ]))
    write('detector-18', build('detector-18', [
        '♻️ Environmental (Formaldehyde/Test) Indicators',
        'Enter indoor formaldehyde, TVOC, benzene and other pollutant concentrations and judge whether indoor air quality meets the GB/T 18883 standard',
        '📖 View the User Guide for Environmental (Formaldehyde/Test) Indicators',
        'Per GB/T 18883-2022: 1-hour mean formaldehyde <= 0.08 mg/m³, benzene <= 0.03, toluene <= 0.20, xylene <= 0.20, 8-hour mean TVOC <= 0.60 (all in mg/m³); if any measured value exceeds its limit, that pollutant is over-standard and the overall result fails; sampling should be done after sealing for 12 hours; if over-standard, increase ventilation or use air purification.',
        'Formaldehyde concentration (mg/m³)',
        'TVOC concentration (mg/m³)',
        'Benzene concentration (mg/m³)',
        'Ammonia concentration (mg/m³)',
        'Radon concentration (Bq/m³)',
        '📚 Deep Dive: Environmental (Formaldehyde/Test) Indicators',
        'Self-test before moving into a new home: enter measured formaldehyde and TVOC values, compare item by item with GB/T 18883 limits (formaldehyde 0.10, TVOC 0.60 mg/m³, etc.), output pass / over-standard and the exceedance multiple.',
        'Office ventilation assessment: judge after multiple samplings averaged, give improvement advice combined with ventilation duration (ventilation, activated carbon, plants, professional treatment).',
        'Re-test comparison: compare pre- and post-treatment data on the same screen to see whether the concentration drop enters the safe range.',
        'Formaldehyde / TVOC judgment',
        'Example: after sealing 12 h, measured formaldehyde 0.14 mg/m³, TVOC 0.45 mg/m³.',
        'Which standard are the limits based on?',
        'This tool defaults to GB/T 18883 (occupied indoor); it differs from GB 50325 (acceptance), which is stricter; distinguish as needed.',
        'What affects the values?',
        'Pre-sampling seal duration, temperature, humidity and ventilation history all significantly affect results; sample under standard conditions.',
        'What to do if over-standard?',
        'Increase ventilation, control pollution sources, and if necessary use professional treatment and re-test; this tool is only a judgment reference and does not represent a CMA test report.',
        'Testing is based on GB/T 18883-2022 Indoor Air Quality Standard; sampling requires closing doors and windows for 12 hours',
        'Formaldehyde limit <= 0.10 mg/m³, TVOC <= 0.60 mg/m³, benzene <= 0.11 mg/m³, ammonia <= 0.20 mg/m³, radon <= 300 Bq/m³',
        'Newly decorated rooms are advised to ventilate 3–6 months before testing; avoid air fresheners before testing',
        'Sampling points should avoid vents, be at least 0.5 m from walls, and 0.8–1.5 m in height',
        'This tool results are for reference only; formal testing should be done by a CMA-qualified testing institution',
        'About Environmental (Formaldehyde/Test) Indicators',
        'An indoor air quality testing tool: enter formaldehyde, TVOC, benzene, ammonia, radon and other pollutant concentrations, judge against GB/T 18883 whether it passes, and give remediation advice.',
        'Five pollutants tested in sync',
        'Based on GB/T 18883-2022 standard',
        'Auto remediation advice for over-standard items',
        'New-home air testing',
        'Indoor environment acceptance',
        'Office air quality assessment',
        'School / kindergarten environment testing',
    ]))

if __name__ == '__main__':
    main()
