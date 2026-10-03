#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'packaging')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'packaging')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    return mp


def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'packaging', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # ---------------- calc-66 (39) ----------------
    write('calc-66', build('calc-66', [
        "📦 Carton Compression / Stacking Calculator",
        "Enter the carton dimensions, board type, stacking height, safety factor and gross weight per box to compute BCT and the maximum stacking height with the McKee formula",
        "Core formulas (by input variable): max(1,Math.floor(stackH/boxH)); Math.floor(1+maxAbove); 5.87 x ECT x SQRT(Z x t)",
        "Carton length L (mm)",
        "Carton width W (mm)",
        "Carton height H (mm)",
        "Board type",
        "BC double wall (ECT 6.5 kN/m)",
        "AC double wall (ECT 8.0 kN/m)",
        "3A triple wall (ECT 11.0 kN/m)",
        "Desired stacking height (m)",
        "Gross weight per box (kg)",
        "Tip: McKee formula: BCT = 5.87 x ECT x SQRT(Z x t), where Z = perimeter 2(L+W) and t = board caliper. The safety factor K covers time and temperature/humidity degradation (usually 3-5).",
        "Compute by",
        "for a quick result, which can be copied with one click",
        "Required compression strength = (stacking layers - 1) x unit weight x g x K",
        "Maximum stacking layers = 1 + BCT / (unit weight x g x K)",
        "Safety factor recommendation: 3 for dry warehousing, 4-5 for humid or long-haul",
        "This tool runs entirely in the browser; results are estimates, and the measured BCT is authoritative",
        "📚 Deep dive: Carton Compression / Stacking Calculator",
        "Warehouse stacking planning: given the carton dimensions, board type and desired stacking height, use the McKee formula to compute the box compression strength BCT and compare it with the required strength to judge whether the stacking plan is safe.",
        "Board selection: BC/AC double wall and 3A triple wall differ in ECT and caliper, so stacking to the same height needs different strength; use the tool to compare and pick the most cost-effective board.",
        "Trade-off in the safety factor: take K = 3 for dry warehousing and 4-5 for humid long-haul routes, discounted for time and temperature/humidity degradation, so the cartons are not already crushed on arrival.",
        "Worked example (box 400 x 300 x 250 mm, BC double wall ECT 6.5 kN/m thickness 5.5 mm, stacking 2.5 m, K=3, gross weight 12 kg)",
        "Perimeter Z = 2 x (400 + 300) / 1000 = 1.4 m. BCT = 5.87 x ECT x SQRT(Z x t) = 5.87 x 6500 x SQRT(1.4 x 0.0055) = 3348 N (about 341 kgf). Total layers = floor(2.5 / 0.25) = 10 layers; required compression strength = (layers - 1) x unit weight x g x K = (10 - 1) x 12 x 9.81 x 3 = 3178 N. BCT 3348 N >= 3178 N, so the plan works but the margin is small; maximum stackable layers = floor(1 + 3348 / (12 x 9.81 x 3)) = 10 layers (height 2.5 m). The tool computes with the McKee formula BCT = 5.87 x ECT x SQRT(Z x t) and compares it with the stacking requirement.",
        "What are ECT and t in the McKee formula?",
        "ECT is edge crush strength (Edge Crush Test, N/m or kN/m), reflecting how well the board resists compression standing on edge; t is the total board caliper (m). BCT = 5.87 x ECT x SQRT(Z x t) is an empirical formula where Z is the box perimeter. This tool has built-in ECT and caliper presets for BC/AC/3A, and you can substitute measured values.",
        "Why is the safety factor K set to 3-5?",
        "K covers strength loss from storage time, board softening from high temperature and humidity, and uneven stacking. Take 3 for dry, temperature-controlled short hauls and 4-5 for humid, long-haul or long-term storage. A larger K is safer but consumes more material, so weigh it against the actual logistics conditions.",
        "About \"Carton Compression / Stacking Calculator\"",
        "Applies the McKee formula to compute the box compression strength (BCT) from the carton perimeter, board edge crush strength (ECT) and caliper, then evaluates the maximum stacking height and stacking safety against the gross weight per box and the safety factor. Runs entirely in the browser, no data uploaded.",
        "McKee formula BCT calculation",
        "BC/AC/3A three board presets",
        "Required strength vs actual BCT comparison",
        "Maximum stacking layers and height",
        "Corrugated carton selection and stacking design",
        "Warehouse stacking height review",
        "Shipping packaging safety assessment",
        "Packaging cost and strength balance",
    ]))

    # ---------------- index (17) ----------------
    write('index', build('index', [
        "📦 Packaging Engineering Tools",
        "Packaging Engineering",
        "Packaging Engineering Tools",
        "Enter the carton dimensions, board type, stacking height, safety factor and gross weight per box to compute BCT and the maximum stacking height with the McKee formula",
        "The carton master case size calculator derives the outer length, height and width from the inner item layout and clearance, supporting packaging design and cartonization optimization for e-commerce and logistics.",
        "The cushioning material thickness calculator derives the required cushioning layer thickness from the product fragility value and drop height, suited to shipping packaging protection design, vibration damping plans and cost trade-offs.",
        "The shrink film shrink rate and heat seal parameter tool estimates the shrink ratio, heat seal temperature and speed from the inputs, suited to wrap packaging process planning and equipment tuning.",
        "The carton sealing tape and hot melt adhesive strength tool evaluates the sealing bond strength from adhesion parameters, suited to choosing a sealing scheme and judging seal reliability under transport vibration.",
        "The corrugated flute and strength design tool estimates compression and edge crush strength from the flute type and board parameters, suited to carton selection, stacking design and shipping packaging verification.",
        "About \"Packaging Engineering Tools\"",
        "The Packaging Engineering Tools collection gathers 6 free online tools covering the common calculation, conversion and lookup needs of packaging engineering scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you will find ready-to-use utilities here. Every tool runs entirely in the browser and never uploads data to the server, so your privacy is protected.",
        "The packaging engineering tools listed on this page include (a few representative tools):",
        "These tools help you finish common packaging engineering tasks quickly, with no need to memorize complex formulas or do manual conversions - just enter the inputs and get the result.",
        "Do the packaging engineering tools require a download or an account?",
        "No. Every tool on this page is a pure front-end online tool: open the page and use it right away, with no software to install, no account to register, and no data uploaded.",
        "Are the packaging engineering tool results accurate? Is the data safe?",
        "The tools compute locally in your browser based on public mathematical formulas and general industry standards, so results are available instantly. All computation happens locally on your device and no data is uploaded to the server, so your privacy is fully protected.",
    ]))


if __name__ == '__main__':
    main()
