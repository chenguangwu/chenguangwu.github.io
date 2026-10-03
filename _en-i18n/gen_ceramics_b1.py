#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'ceramics')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'ceramics')
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
    out = {'slug': slug, 'industry': 'ceramics', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # ---------------- clay-shrinkage (25) ----------------
    write('clay-shrinkage', build('clay-shrinkage', [
        "🧮 Clay Shrinkage Calculator",
        "Compute the drying shrinkage, firing shrinkage and total shrinkage of clay, and supports back-calculation: deriving the wet clay dimensions from the target finished size.",
        "🔁 Back-calculate making dimensions from the finished size",
        "📋 Shrinkage notes",
        "📚 Deep dive: Clay Shrinkage Calculation",
        "Total shrinkage conversion: after measuring the drying shrinkage and the firing shrinkage separately, derive the total linear shrinkage by (1 - drying shrinkage rate) × (1 - firing shrinkage rate), used for scaling up the greenware.",
        "Greenware scaling calculation: given the target finished size and the total shrinkage, back-derive the enlarged wet / dry dimensions so the diameter and height meet the target after firing.",
        "Abnormal shrinkage troubleshooting: batch-to-batch shrinkage variation of the same recipe often reflects differences in moisture content, wedging uniformity or aging time, and can warn of cracking risk in advance.",
        "Greenware scaling worked example",
        "Entering a dry greenware height of 90mm and a fired height of 81mm, the tool computes a firing shrinkage of 10%; if the total shrinkage is about 12%, the wet clay should be scaled by about 1.136, giving a wet height of about 102mm.",
        "What is the difference between drying and firing shrinkage?",
        "Drying shrinkage is the linear shrinkage caused by water loss (usually 5%-8%); firing shrinkage is the further shrinkage from glass phase formation and mineral rearrangement at high temperature (up to 10%-14% for porcelain clay). The two occur at different stages and must be measured separately.",
        "What shrinkage rate is normal?",
        "It depends on the clay: earthenware totals about 8%-12%, stoneware about 10%-14%, and porcelain clay can reach 12%-16%; too much variation within the same recipe means the clay state is unstable, so recheck the moisture content and wedging process.",
        "How do you use the scaling?",
        "Finished size ÷ (1 − total shrinkage) = wet clay size. For example a finished diameter of 100mm with 12% total shrinkage calls for a wet dimension of about 114mm. Beginners should leave a margin and fire a test sample to calibrate.",
        "The Clay Shrinkage Calculator is an online tool for potters and studios, computing shrinkage from drying and firing dimensions and assisting greenware scaling, processed entirely in the browser with data calculated locally to protect privacy.",
        "One-click conversion of ceramic parameters: shrinkage, ratio, temperature and wheel speed computed in real time",
        "Local calculation: data never leaves the browser, protecting recipe and process secrets",
        "Results can be copied and exported: convenient for records and refiring comparison",
        "Fits many clay bodies and glaze formulas: earthenware, stoneware and porcelain all work",
        "Greenware scaling design: back-derive wet dimensions from the total shrinkage",
        "Abnormal shrinkage troubleshooting: batch variation warns of cracking risk",
        "Wedging and aging process assessment: stable output rate",
        "Teaching and test firing calibration: quick conversion reference",
    ]))

    # ---------------- glaze-ratio (39) ----------------
    write('glaze-ratio', build('glaze-ratio', [
        "🏺 Glaze Recipe Ratio Calculator",
        "Compute the weighing amount of each raw material from the glaze recipe percentages, and estimate the water needed to mix the glaze slip (dipping / pouring / spraying).",
        "Core formulas (by input variable): (total+water)÷1.55; total×m.pct÷100",
        "📋 Recipe notes",
        "Recipe percentages: ",
        "A glaze recipe is expressed as the percentage of each raw material in the total dry materials, and the sum should be 100%.",
        "Weighing: ",
        "Weight of a raw material = total weight × percentage / 100.",
        "Water added: ",
        "Water-to-glaze ratio = water / dry glaze. Dipping glaze is thicker (water content about 35%-45%, specific gravity 1.5-1.7), while sprayed glaze is thinner (water content about 50%-60%).",
        "Specific gravity reference: ",
        "Dipping glaze slip has a specific gravity of about 1.55-1.70 g/mL; sprayed glaze about 1.30-1.45 g/mL. In practice it must be adjusted to the body's water absorption and the glaze layer thickness.",
        "📚 Deep dive: Glaze Recipe Ratio Calculator",
        "Base glaze weighing: multiply the recipe by",
        "the total glaze weight to get the precise gram weight of each raw material such as feldspar, quartz, kaolin and frit, reducing manual conversion errors.",
        "Water-to-glaze ratio estimation: dipping, pouring and spraying have different slip specific gravity requirements, so the water is estimated from the total glaze powder weight to control the glaze layer thickness and the risk of running.",
        "Test tile scaling: back-derive a 50-200g test firing tile from a production recipe, keeping the proportion of each raw material consistent for quick verification of color and gloss.",
        "Base transparent glaze weighing worked example",
        "Recipe feldspar 40 / quartz 30 / kaolin 20 / calcite 10, total weight 500g. The tool outputs 200/150/100/50g of each raw material and suggests adding water for dipping glaze at about 1:1-1:1.2 of the glaze powder weight.",
        "What is the difference between raw-material glazes and frit glazes?",
        "In a raw-material glaze the raw materials are ground directly into the glaze; in a frit glaze some water-soluble or toxic materials are first melted into glass and then crushed, giving better safety and stability. When weighing, frit is counted as the finished frit weight and is not broken back down into the original oxides.",
        "How is the water-to-glaze ratio determined?",
        "A common glaze slip specific gravity is 1.4-1.5 (thicker for dipping, thinner for spraying). Start adding water at about 1:1 of the glaze powder weight, then correct with a hydrometer or flow meter; too much water causes running, too little causes uneven thickness.",
        "Does weighing error affect the fired color?",
        "Yes. A 1%-2% deviation in colorant or frit ratio already produces a visible color difference, so use a 0.1g precision balance for colored glazes and keep the grind fineness fixed.",
        "The Glaze Recipe Ratio Calculator is an online tool for potters and studios, computing the weighing amount of each raw material from the glaze formula percentages and estimating the mixing water, processed entirely in the browser with data calculated locally to protect privacy.",
        "One-click conversion of ceramic parameters: shrinkage, ratio, temperature and wheel speed computed in real time",
        "Local calculation: data never leaves the browser, protecting recipe and process secrets",
        "Results can be copied and exported: convenient for records and refiring comparison",
        "Fits many clay bodies and glaze formulas: earthenware, stoneware and porcelain all work",
        "Base glaze weighing: compute the gram weight of each raw material from the recipe percentages",
        "Water-to-glaze ratio estimate: water amount for dipping / pouring / spraying",
        "Test tile scaling: back-derive a test tile from a large recipe",
        "Color glaze re-mixing: verify the fired color by keeping the ratio",
        "How to use the Glaze Recipe Ratio Calculator",
        "Base glaze weighing: multiply the recipe percentages by the total glaze weight to get the precise gram weight of each raw material such as feldspar, quartz, kaolin and frit, reducing manual conversion errors; water-to-glaze ratio estimate: dipping, pouring and spraying have different slip specific gravity requirements, so water is estimated from the total glaze powder weight to control the glaze layer thickness and the risk of running.",
        "What does the Glaze Recipe Ratio Calculator do?",
        "How do you use the Glaze Recipe Ratio Calculator?",
        "Which scenarios suit the Glaze Recipe Ratio Calculator?",
    ]))


if __name__ == '__main__':
    main()
