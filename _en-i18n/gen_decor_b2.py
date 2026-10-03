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
    write('index', build('index', [
        '🛋️ Interior Decoration Tools',
        'Interior Decoration',
        'Interior Decoration Tools',
        'Latex Paint Color-Mix Calculator',
        'Enter the target color and base paint mass, and by pigment ratio (light 0.3–1%, medium 1–3%, dark 3–8%) compute the required pigment amount, assisting precise latex paint tinting.',
        'Ceiling Panel Quantity Calculator',
        'The Ceiling Panel Quantity Calculator is a free online interior-decoration tool; estimate before ceiling work: enter room length/width, panel spec and waste rate to get panel count, main/secondary keel usage and purchase advice, avoiding over-buy waste or short-buy reorder. Runs purely front-end, no data upload, no registration...',
        'Estimate curtain fabric meters by window size, fullness ratio and fabric width, accounting for pattern-match and edge waste, helping verify usage before buying to avoid waste or shortage.',
        'Wallpaper Quantity Calculator: by wall size and wallpaper width, length and waste rate, compute required rolls and panels, assisting material prep and budget for wallpapering.',
        'Room Illumination Calculator: by room type and area, compute required illuminance, luminous flux and lamp power, assisting home lighting design.',
        'Enter each wall length and door opening width, compute net skirting length by perimeter minus door openings (window sills not deducted), easing material purchase and usage estimate.',
        'Enter indoor formaldehyde, TVOC, benzene and other pollutant concentrations and judge by GB/T 18883 whether indoor air quality passes',
        'Construction (Process/Duration) Scheduling',
        'Automatically compute duration, total float and critical path by the Critical Path Method (CPM), and draw a Gantt chart.',
        'About Interior Decoration Tools',
        'The Interior Decoration Tools collection contains 8 free online tools covering common calculation, conversion and lookup needs in interior decoration scenarios. Whether you are a practitioner, student or ordinary user, you can find ready-to-use small tools here. All tools run purely front-end, upload no data to the server, and protect your privacy and security.',
        'The interior decoration tools on this page include (representative selection):',
        'These tools help you quickly complete common interior-decoration tasks without memorizing complex formulas or manual conversions; just enter to get results.',
        'Do the interior decoration tools need to be downloaded or registered?',
        'No. All interior decoration tools on this page are pure front-end online tools; open the page to use directly, no software install, no account registration, no data upload.',
        'Are the interior decoration tools results accurate? Is the data safe?',
        'The tools compute locally in your browser based on public math formulas and general industry standards, with results instantly available. All computation is done locally on your device; data is never uploaded to the server, and your privacy and security are protected.',
    ]))
    write('paint-color-mix', build('paint-color-mix', [
        '🧮 Latex Paint Color-Mix Calculator',
        'Select a target color and compute the pigment addition ratio and amount',
        '📖 View the User Guide for Latex Paint Color-Mix Calculator',
        'Pigment ratio = pigment mass ÷ latex paint mass × 100%',
        'Latex paint amount (kg)',
        'Tint depth',
        'Light (pigment 0.5%)',
        'Medium-light (pigment 1%)',
        'Medium (pigment 2%)',
        'Dark (pigment 4%)',
        'Select target color',
        '📖 Tinting notes',
        'Pigment ratio',
        '= pigment mass ÷ latex paint mass × 100%',
        '• Light pigment ratio about 0.3–1%, medium 1–3%, dark 3–8%',
        '• Follow the "light to dark" principle, add small amounts multiple times, mix thoroughly',
        '• For the same space, tint enough at once to avoid color difference from a second batch',
        '• For dark latex paint, use a matching dark base paint for better coverage',
        '• The formula is a reference ratio; actual effect depends on base paint and pigment brand, so test a sample first',
        '📚 Deep Dive: Latex Paint Color-Mix Calculator',
        'Wall light-color touch-up: with 5 kg base paint and light ratio 0.5%, pigment ≈ 5 × 0.005 = 0.025 kg; confirm with a sample before bulk.',
        'Medium-dark accent wall: dark ratio rises to 3%–8%; for large amounts, add pigment in batches and compare with the color card after stirring.',
        'Multi-bucket same-color mixing: convert pigment uniformly by total base paint mass to avoid ratio drift and color difference across batches.',
        'Medium tint amount',
        'Example: base paint 10 kg, target medium, pigment ratio 2%.',
        'How to set the ratio?',
        'Light 0.3%–1%, medium 1%–3%, dark 3%–8%, depending on pigment concentration and base paint whiteness.',
        'Tinted color looks off?',
        'Different base batches, water content and uneven stirring all cause color shift; always compare a sample with the color card before bulk.',
        'Why does dark use more pigment?',
        'Dark colors have poor coverage and need more pigment to saturate, so the ratio is significantly higher; add pigment in stages to avoid going too dark at once.',
        'About Latex Paint Color-Mix Calculator',
        'The Latex Paint Color-Mix Calculator provides common color formulas and computes each pigment addition amount by latex paint amount and tint depth.',
        '12 common color formulas',
        'Pigment ratio auto-allocated',
        'Supports light/medium/dark depths',
        'Home wall color matching',
        'Pre-select decoration color schemes',
        'Pigment purchase estimate',
        'Sample test-color ratio reference',
    ]))
    write('room-illumination', build('room-illumination', [
        '🛠️ Room Illumination Calculator',
        'Compute required illuminance, luminous flux and lamp power by room type and area',
        'Core calculation formula (by input variables): Math.ceil(totalWatt / wattPer)',
        '📖 View the User Guide for Room Illumination Calculator',
        'Classroom',
        'Entry hall / corridor',
        'Room area (m²)',
        'Target illuminance (lux)',
        'LED lamp (90 lm/W)',
        'LED lamp (80 lm/W)',
        'CFL (70 lm/W)',
        'CFL (60 lm/W)',
        'Incandescent (15 lm/W)',
        'Single lamp power (W)',
        'Utilization factor (0.4–0.8)',
        'Maintenance factor (0.6–0.9)',
        '📖 Illuminance reference standard (GB 50034)',
        'Space',
        'Recommended illuminance (lux)',
        'General activity; add local lighting at reading areas',
        'Soft preferred; bedside reading 150 lux',
        'Countertop needs 300 lux local lighting',
        '200 lux local lighting in front of mirror',
        'Desk reading and writing',
        'Dining table accent lighting',
        'General office; drafting 500 lux',
        'Desk illuminance',
        'Total luminous flux',
        '= area × illuminance ÷ (utilization factor × maintenance factor)',
        'Total power',
        '= total luminous flux ÷ luminous efficacy (lm/W)',
        'Lamp count',
        '= total power ÷ single lamp power (rounded up)',
        '• Utilization factor relates to room reflectance and luminaire light distribution; light-colored walls take a high value',
        '• Maintenance factor accounts for light decay and dust; regular cleaning keeps it high',
        '📚 Deep Dive: Room Illumination Calculator',
        'Living room base lighting: choose living-room recommended illuminance 100–300 lux, area × illuminance gives total flux, then convert to lamp count by single-lamp lumens.',
        'Study/kitchen accent lighting: raise local illuminance (study 300–500, kitchen counter 500+), zone-based configuration.',
        'Energy-saving replacement: given target flux, reverse-compute power by LED efficacy (about 80–120 lm/W), compare with original lamps for savings.',
        'Living room illuminance need',
        'Example: living room 20 m², take 200 lux.\n• Total flux ≈ 20 × 200 = 4000 lm\n• Choose 800 lm/lamp LED, about 5 lamps needed; or one main lamp of 4000 lm',
        'Where do the illuminance reference values come from?',
        'Taken from the residential-building recommended values in the Standard for Lighting Design of Buildings GB 50034, varying by function.',
        'How to convert power?',
        'Power = luminous flux ÷ efficacy (LED about 100 lm/W); old fluorescent/incandescent have much lower efficacy.',
        'Is computing only the main lamp enough?',
        'Not enough; zone-based (base + accent + ambient) is recommended. This tool gives a total reference; split by layout in practice.',
        'About Room Illumination Calculator',
        'The Room Illumination Calculator, per national illuminance standards, computes required luminous flux, lamp power and count by room area.',
        '9 built-in space illuminance standards',
        'Multiple lamp efficacy options supported',
        'Adjustable utilization and maintenance factors',
        'Home decoration lamp selection',
        'Office lighting design',
        'Classroom illuminance acceptance',
        'Energy-saving retrofit evaluation',
    ]))

if __name__ == '__main__':
    main()
