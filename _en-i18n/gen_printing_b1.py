#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'printing')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'printing')
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
    out = {'slug': slug, 'industry': 'printing', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
# -*- coding: utf-8 -*-
def main():
    write('analysis-7', build('analysis-7', [
        '📊 Light Box Brightness (cd/m²) Uniformity Analysis',
        'Enter brightness readings (cd/m²) from each measurement point on a light box or viewing table to compute average brightness, dispersion and uniformity U₁ (min ÷ average), so you can judge whether the whole surface has dark spots or brightness gradients. Uniformity of at least 0.7 is generally considered good. Data is processed only in the local browser and never uploaded.',
        '📖 Read the "Light Box Brightness (cd/m²) Uniformity Analysis User Guide"',
        'Average brightness L̄ = Σ Li ÷ n',
        'Uniformity U₁ = min brightness ÷ average brightness',
        'Enter brightness readings (cd/m²) from each measurement point on a light box or viewing table to compute average brightness, dispersion and uniformity U₁ (min ÷ average), so you can judge whether the whole surface has dark spots or brightness gradients. Uniformity of at least 0.7 is generally considered good. All data is processed only in the local browser and never uploaded.',
        'Brightness readings at measurement points (cd/m², separated by commas or newlines)',
        'Analyze uniformity',
        '📚 Deep dive: light box brightness (cd/m²) uniformity analysis',
        'Measure brightness at multiple points on light boxes, illuminated letters and billboards before shipping to check whether the whole surface lights evenly, avoiding dark spots that hurt the display effect.',
        'Check illuminance uniformity on a printing viewing table: lay out a grid of points on the surface, measure cd/m² and confirm there is no brightness gradient that skews color judgment.',
        'Sampling check of panel and screen brightness consistency: measure multiple points across devices from the same batch and use statistics to judge whether the dispersion exceeds the allowed range.',
        'Take "8 measurement points on the front of a light box, brightness (cd/m²) values 320, 348, 365, 355, 372, 338, 351, 360" as an example',
        'Data count n=8, sum 2809, mean 351.13,',
        '353, min 320, max 372, range 52, variance 234.11,',
        '15.30. Uniformity has two common conventions: min/max = 320/372≈0.86 (closer to 1 means more uniform), or dispersion 1-(max-min)/mean = 1-52/351.13≈0.852; the standard deviation of 15.30 cd/m² reflects how much each point fluctuates around the mean. If the contract requires uniformity ≥0.9, this light box at 0.86 fails and the light source layout needs adjusting.',
        'How is uniformity computed?',
        'Commonly "min brightness / max brightness" or "1-(max-min)/average". The former is intuitive but sensitive to outliers; the latter is more responsive to overall dispersion. This tool also reports the standard deviation so you can tell a smooth gradient from a single sudden drop - an isolated drop often signals a single LED bead or a local light guide defect.',
        'What is the unit cd/m²?',
        'Candela per square meter, the international SI unit of luminance (also called nit). It is the nominal brightness unit for light boxes and displays. Measurement needs a photometer probe calibrated in a dark environment, otherwise ambient light raises the readings and underestimates true uniformity.',
        'About "Light Box Brightness (cd/m²) Uniformity Analysis"',
        'Light Box Brightness (cd/m²) Uniformity Analysis. A free online tool processed entirely in the browser, no data uploaded, your privacy and security protected.',
    ]))

    write('convert-gsm', build('convert-gsm', [
        '📏 Paper Weight (gsm) and Thickness Conversion',
        '📖 Read the "Paper Weight (gsm) and Thickness Conversion User Guide"',
        'Paper weight',
        'Milli paper weight',
        'Kilo paper weight',
        'Thickness conversion',
        'Milli thickness conversion',
        'Kilo thickness conversion',
        '📚 Deep dive: paper weight (gsm) and thickness conversion',
        'When purchasing, unify different nominal labels (weight gsm or thickness μm/μm equivalent) to a comparable basis so cost per unit area can be computed.',
        'When selecting materials, convert between weight and thickness to balance stiffness, hand feel and printability (thick paper is stiff but costly, thin paper is cheap but soft).',
        'When quotes from multiple suppliers use different bases (some quote gsm, some thickness), convert to a common basis before comparing prices.',
        'Take "weight 150, conversion coefficient 0.8, source unit 1, target unit 2, find the converted value" as an example',
        'Compute with r = v×rate×f/t: 150×0.8×1/2 = 60. This formula is a general',
        'backbone - v is the source value, rate is the dimension coefficient (such as a density ratio), and f/t is the ratio of source to target unit. For example converting gsm to "thickness relative to a reference basis" or vice versa, just plug in the right f and t; there is no need to memorize the density of every paper type.',
        'What is gsm?',
        'Grams per square meter, the standard nominal for paper weight (e.g. 80gsm copy paper, 250gsm card stock). It indirectly reflects thickness and stiffness, but the same gsm with different pulp or calendering still yields different thicknesses.',
        'Can weight and thickness be converted exactly?',
        'Strict conversion requires paper density (ρ): thickness t = weight/(ρ×1000), where ρ is about 0.6~0.9 g/cm³. This tool folds density into rate via r = v×rate×f/t, which suits quick conversion within the same category; across categories (coated vs uncoated) densities differ, so measured values still govern.',
        'About "Paper Weight (gsm) and Thickness Conversion"',
        'Paper Weight (gsm) and Thickness Conversion. A free online tool processed entirely in the browser, no data uploaded, your privacy and security protected.',
    ]))

    write('index', build('index', [
        '🖨️ Printing Technology Tools',
        'Printing Technology',
        'Printing Technology Tools',
        'Enter the total page count of a book or periodical and the fold (e.g. 16 open), and the tool computes the required sheet count with sheet = total pages / fold (single-sided); for duplex printing divide by 2 again, which helps estimate paper usage, printing cost and binding scheduling.',
        'Paper Weight (gsm) and Thickness Conversion',
        'The Paper Weight (gsm) and Thickness Conversion tool converts between weight and thickness via the density relation, suited to cost estimation for printing, packaging material selection and unified paper specifications.',
        'Packaging Box Unfolding',
        'Enter the length, width and height of a rectangular packaging box; the tool computes the total unfolded paper area with 2×(L×W+L×H+W×H) and can convert it to reams, for printing quotes and carton material accounting.',
        'Enter printed area, solid coverage and ink laydown (g/m²) to estimate total ink consumption for a single sheet or a whole print run, helping printers cost consumables, schedule ink refills and control spot color mixing ratios.',
        'Estimate ink consumption from printed area, ink coverage, ink film thickness, ink density and print run, supporting single color and CMYK four-color separation',
        'Online light box brightness uniformity analysis: enter multi-point brightness data to compute min/max and uniformity metrics, for print proofing and quality inspection. Runs purely in the browser.',
        'Carton Structure Design',
        'Enter the inner dimensions (length/width/height) of a carton or a target volume; the tool computes crease positions, the nesting layout size and tuck-flap parameters for folding cartons, assisting packaging structure design and die-line drawing to reduce trial die waste.',
        'About "Printing Technology Tools"',
        'This Printing Technology Tools collection gathers 7 free online tools covering the common calculation, conversion and lookup needs of printing technology. Whether you are a practitioner, a student or an ordinary user, you will find ready-to-use utilities here. Every tool runs purely in the browser; no data is uploaded to the server, so your privacy and security are protected.',
        'Printing technology tools included on this page (representative tools only):',
        'These tools help you finish common printing technology tasks fast, with no need to memorize complex formulas or convert by hand - input and you get the result.',
        'Do the Printing Technology Tools require downloads or registration?',
        'No. All Printing Technology Tools on this page are pure front-end online tools: open the page and use them right away, with no software to install, no account to register, and no data uploaded.',
        'Are the Printing Technology Tools results accurate, and is the data safe?',
        'The tools compute in your browser using public math formulas and common industry standards, so results are available instantly. All computation happens locally on your device; no data is uploaded to the server, so privacy and security are guaranteed.',
    ]))


if __name__ == '__main__':
    main()
