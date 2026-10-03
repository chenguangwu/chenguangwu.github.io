#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'chinese-cook')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'chinese-cook')
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
    out = {'slug': slug, 'industry': 'chinese-cook', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # ===== cutting-sizes (46) =====
    write('cutting-sizes', build('cutting-sizes', [
        '⚖️ Knife-cutting size reference',
        'Reference for Chinese-cuisine knife specifications; select a cut style to view standard sizes and suitable dishes',
        '📖 View "Knife-cutting size reference user guide"',
        'Knife-cutting size reference: summarizes standard millimeter sizes and suitable dishes for common Chinese knife cuts (minced, diced, shredded, sliced, strip, chunk), a pure front-end local lookup to standardize cutting and ensure even heating.',
        'Select cut style',
        'Minced',
        'Diced',
        'Shredded',
        'Sliced',
        'Strip',
        'Chunk',
        'Large dice',
        'Large chunk',
        '📋 Full knife-cut specification table',
        'Tip: sizes are common industry references; adjust flexibly by dish and ingredient in practice. Uniform thickness matters more than exact size.',
        '📚 In-depth: knife-cutting size reference',
        'Cut ingredients to "thin shreds" or "roll-cut chunks" per recipe, follow the standard sizes, avoid uneven size causing raw/overcooked mix.',
        'For meal prep plating or banquet arrangement, uniform cutting sizes improve consistency and appearance; braised and stir-fried dishes especially demand uniformity.',
        'When a beginner learns knife skills or trains apprentices, use the size table to quantify "about 0.3cm shreds, 1cm dice", reducing vague "a little" / "some" expressions.',
        'Pork-shred size for stir-fried pork shreds',
        'Pork tenderloin shreds: thick shreds about 0.4×0.4×4cm, thin shreds about 0.3×0.3×5cm; cut sides (pepper, bamboo shoot) to the same spec so they cook evenly in one pan and plate neatly.',
        'Are there standards for shred and slice lengths?',
        'Common shred length 4–6cm, width/thickness 0.2–0.4cm; slice thickness 0.2–0.5cm by ingredient — leafy thin, root/stem slightly thicker, for easy eating and even heating.',
        'Why emphasize uniform size?',
        'The closer the sizes, the more uniform the doneness at the same temperature and time, avoiding big chunks raw inside and small ones overcooked; also key to banquet beauty and consistent texture.',
        'How to cut roll-cut (guillotine) chunks?',
        'Roll the ingredient 45° and cut while turning, about 1/4 turn per cut, yielding irregular multi-sided chunks; common for potato and radish braises, increasing surface area to absorb flavor.',
        'About "knife-cutting size reference"',
        'The knife-cutting size reference table summarizes standard sizes and suitable dishes for common Chinese knife cuts (minced, diced, shredded, sliced, strip, chunk), helping cooking enthusiasts master standard cutting specs.',
        'Covers 8 common knife-cut styles',
        'Marks standard sizes and shapes',
        'Links example suitable dishes',
        'Chinese knife-cut size reference table - minced/diced/shredded/sliced/strip/minced knife specs, Chinese cooking cutting spec reference, shred/slice/dice/chunk size comparison. A daily-life tool, close to life, practical and convenient.',
        'Cut by recipe: follow standard sizes to shred and chop, avoid uneven size and raw/overcooked mix',
        'Meal prep plating: uniform cutting sizes improve banquet consistency and appearance',
        'Learning knife skills / training: quantify "thin shred / roll-cut chunk" in mm, reducing vague expressions',
        'How to use knife-cutting size reference',
        'For home meal prep, banquet plating and learning knife skills: cut by recipe standard sizes to ensure even heating and neat appearance; also suits cooking beginners to quantify knife specs, reducing vague "a little / some" operations.',
        'What does knife-cutting size reference do?',
        'Chinese knife-cut size reference; select a cut style to view standard sizes (minced/diced/shredded/sliced/strip) and suitable dishes, standardizing prep and output.',
        'How to use knife-cutting size reference?',
        'Which scenarios is knife-cutting size reference suitable for?',
        'Specification meaning',
        'Knife-cut sizes are distinguished by edge length / diameter: shred about 0.2–0.3 cm, dice about 1 cm³, slice about 0.2–0.3 cm thick, chunk about 2–3 cm. Smaller specs absorb flavor and cook faster.',
        'Choose knife cut by dish: quick-fry suits shred/slice, braise suits chunk, ensuring even heating and consistent texture.',
        'Sizes are general references; follow the recipe requirement; hand cutting has individual variation.',
    ]))

    # ===== estimate-16 (19) =====
    write('estimate-16', build('estimate-16', [
        '🔮 Percentage calculator (Chinese cooking)',
        'Compute percentage, proportion, growth rate, etc. of a value',
        'Braising reduction (remaining percentage) estimate',
        '/ Braising reduction (remaining percentage) estimate',
        '📖 View "Percentage calculator (Chinese cooking) user guide"',
        'Remaining percentage = post-reduction amount ÷ pre-reduction amount × 100%; concentration factor = pre-reduction amount ÷ post-reduction amount; change = new − old, change rate = (new − old) ÷ old × 100%; general proportion = total × percentage ÷ 100; braise until 60%–70% remaining for thick sauce coating the spoon, 40%–50% for sweet-and-sour reduction standard; when more than half reduced, switch to low heat to avoid scorching.',
        '📚 In-depth: percentage calculator (Chinese cooking)',
        'When kneading dough or curing, add water and seasoning by flour / meat weight',
        '(e.g. 50% flour water, 2% meat salt) to keep each recipe stable and reproducible.',
        'Check dish cost and yield rate: use net weight ÷ gross weight for yield rate, compare cost-effectiveness of different purchase specs.',
        'Low-sugar low-salt recipe tuning: lower sugar and salt proportionally by original-weight percentage, record before/after values, easy to recreate.',
        'Dumpling dough water ratio',
        'Flour 500g, water at 50% = 250g (about 250ml); salt 1% = 5g. After converting to percentage, any flour amount can be scaled by ratio, dough consistency stays the same.',
        'What is the percentage base?',
        'Chinese cooking mostly takes the main ingredient weight (flour, meat) or total weight as 100%, seasonings by their percentage; a unified base enables horizontal comparison of different recipes.',
        'How to compute yield rate?',
        'Yield rate = net weight ÷ gross weight × 100%; e.g. potato after peeling 800g / gross 1000g = 80%, for cost and usage estimate.',
        'Is 2% salt for cured meat a general value?',
        'Home-cured meat about 1–2% salt (of meat weight), more for soy-cured and bacon; adjust by taste and preservation need; this tool only does percentage conversion.',
    ]))

    # ===== index (18) =====
    write('index', build('index', [
        '🥘 Chinese cooking tools',
        'Chinese cooking',
        'Chinese cooking tools',
        'Sauce-ratio calculator: select sauce type and base spoon count to auto-compute each seasoning amount, recreating standard flavor profiles and stable output.',
        'Braising reduction (remaining percentage) estimate',
        'Enter the liquid volume or weight before and after cooking to estimate the braising reduction remaining percentage and concentration, also supports general proportion and increase/decrease rate, for controlling heat.',
        'Chinese knife-cut size reference; select a cut style to view standard sizes (minced/diced/shredded/sliced/strip) and suitable dishes, standardizing prep and output.',
        'Chinese cooking oil-temperature guide; by oil-temperature gear view the temperature range, traits and suitable cooking methods (30%–90% heat), aiding heat control.',
        'Chinese cooking heat-control guide; by heat gear view traits and suitable cooking methods (high/medium/low heat), aiding cooking process arrangement.',
        'Ingredient substitution finder; enter an ingredient to search substitution options or view replacement suggestions and ratios, solving cooking substitution when short of an item.',
        'About "Chinese cooking tools"',
        'The Chinese cooking tools collection gathers 6 free online tools, covering common calculation, conversion and lookup needs in Chinese-cooking scenarios. Whether you are a practitioner, student or ordinary user in the field, you can find ready-to-use small tools here. All tools run entirely in the browser, data is not uploaded to the server, protecting privacy and security.',
        'The Chinese cooking tools collected on this page include (some representative tools):',
        'These tools help you quickly complete common Chinese-cooking tasks without memorizing complex formulas or manual conversion; just input to get results.',
        'Do the Chinese cooking tools need download or registration?',
        'No. All Chinese cooking tools on this page are pure front-end online tools; open the page and use directly, no software install, no account registration, and no data upload.',
        'Are the Chinese cooking tools calculation results accurate? Is the data safe?',
        'Tools compute locally in your browser based on public math formulas and general industry standards, results are instant. All operations complete on your device, data is not uploaded to any server, privacy and security are guaranteed.',
    ]))

    print('body_chinese-cook_b1 done')

if __name__ == '__main__':
    main()
