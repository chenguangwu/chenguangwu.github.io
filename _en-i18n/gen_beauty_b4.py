#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'beauty')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'beauty')
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
    out = {'slug': slug, 'industry': 'beauty', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
#!/usr/bin/env python3


def main():
    write('checker-assessor-2', build('checker-assessor-2', [
        "\u2696\uFE0F Quality (inspection / durability / appearance) assessment",
        "Three-dimensional cosmetic quality assessment: a combined score for quality inspection, durability and visual appeal",
        "Composite score = compliance safety \u00D7 40% + durability stability \u00D7 30% + visual appeal \u00D7 30%. For each dimension the score rate = dimension score \u00F7 (5 \u00D7 the sum of its item weights) \u00D7 100%; after conversion to a 100-point scale the dimensions are combined by weight. A composite of 90 or more is excellent, 80 to 89 good, 70 to 79 fair and below 70 poor. Items scoring 1 to 2 are put on the improvement list.",
        "Score each metric (5=excellent / 4=good / 3=fair / 2=poor / 1=fail)",
        "Durability dimension",
        "Visual appearance dimension",
        "Three dimensions: quality inspection (compliance and safety), durability (stability and lasting performance), visual appearance (sensory and design)",
        "Composite score = weighted average of the three dimensions (quality 40% + durability 30% + appearance 30%)",
        "Results are for reference only; actual testing should follow laboratory data",
        "\U0001F4DA In-depth analysis: cosmetic quality inspection assessment",
        "Score the finished product across compliance safety, durability stability and visual appearance.",
        "Marketing uses it to measure the quality gap between competitors and own products and set the upgrade direction.",
        "The quality control post outputs a composite rating with fixed weights for factory release decisions.",
        "Three-dimension weighted example",
        "Set compliance safety 90, durability stability 82 and visual appearance 78 (100 each) with weights 40%/30%/30%. The composite = 90\u00D70.4 + 82\u00D70.3 + 78\u00D70.3 = 84.0 points, which is good, though the appearance dimension could raise the packaging quality.",
        "Why does compliance safety carry the highest weight?",
        "Compliance and safety are a precondition for going to market and act as a pass-fail gate. Durability and appearance affect experience but do not touch the safety floor, so their weights step down.",
        "Do all three scores have to be high for a good product?",
        "Ideally yes, but with limited resources prioritize compliance and stability; appearance can be improved through small adjustments to packaging and texture without investing evenly in all three.",
        "About the Quality (inspection/durability/appearance) assessment",
        "A three-dimensional cosmetic quality assessment tool that scores quality inspection (compliance and safety 40%), durability (stability and lasting performance 30%) and visual appearance (sensory and design 30%) by weight, then outputs a composite quality rating with improvement suggestions.",
        "Three-dimension weighted assessment (inspection / durability / appearance)",
        "15 detailed quality metrics",
        "Visualizes the three-dimension quality comparison",
        "Outputs targeted improvement suggestions",
        "Comprehensive cosmetic quality assessment",
        "Quality acceptance for product development",
        "Competitor quality comparison",
        "Quality improvement target setting",
    ]))

    write('face-hair-match', build('face-hair-match', [
        "\U0001F484 Face shape and hairstyle matching",
        "Match hairstyles to 7 face shapes and find the style that suits you best",
        "Face shape and hairstyle matching",
        " / Face shape and hairstyle matching",
        "Match hair outlines and cutting notes to seven face shapes (round, square, long, heart, diamond, oval, triangle) on the principle of playing up strengths and softening flaws: add width for long faces, add length for round faces and soften the jaw for square faces. Match scores are weighted across the shaping dimensions of each face shape.",
        "Choose your face shape",
        "\U0001F487 Recommended hairstyles",
        "\U0001F4DA In-depth analysis: face shape and hairstyle matching",
        "Unsure of your face shape and want a cut that makes your face look smaller and more balanced.",
        "Give your stylist a reference before the cut so you avoid a regret.",
        "A stylist matches cutting notes to each of the seven face shapes for clients.",
        "Round face shaping example",
        "A round face (length-to-width ratio about 1, zygomatic width about equal to jaw width) suits a side part with volume on top to elongate the vertical line, and should avoid blunt bangs and short styles that cling to the face. In the match score the \"vertical elongation\" dimension carries the highest weight, which recommends a layered collarbone cut.",
        "How do I tell whether I have a round or a square face?",
        "A round face has soft angles with length and width close to equal; a square face has clear jaw corners and hard lines. Measure zygomatic width against jaw width \u2014 a small difference combined with a square jaw usually means a square face.",
        "Do all seven face shapes follow the same rules?",
        "No. An oval face suits almost anything, while the rest rely on playing up strengths and softening flaws: add width for long faces, add length for round faces, soften the jaw for square faces and narrow a wide forehead for heart faces. The rules differ.",
        "About Face Shape and Hairstyle matching",
        "Face shape and hairstyle matching is an online tool for everyday life. An everyday-life utility, close to daily needs, practical and convenient.",
    ]))

    write('hair-dye-ratio', build('hair-dye-ratio', [
        "\U0001F484 Hair dye mixing ratio calculator",
        "Developer strength and colour cream mixing ratios, for precise hair dye formulation",
        "Hair dye mixing ratio",
        " / Hair dye mixing ratio",
        "Target lift level",
        "No lift (same level or darker)",
        "Lift 1 level",
        "Lift 2 levels",
        "Lift 3 levels",
        "Lift 4 levels",
        "Lift 5 levels",
        "Lift 6 levels",
        "Hair condition",
        "Normal hair",
        "Resistant hair (coarse and thick)",
        "Porous hair (damaged)",
        "Previously bleached hair",
        "Amount settings",
        "Colour cream amount (g)",
        "Mixing ratio",
        "\U0001F4CA Mixing result",
        "\U0001F4DA In-depth analysis: hair dye mixing ratio calculator",
        "Mix colour cream and developer at home or in a salon, setting the ratio from the target level difference.",
        "Use a lower developer strength for root touch-ups to reduce irritation.",
        "Train beginners to master the standard 1:1 or 1:1.5 ratios and avoid colour mismatch.",
        "Developer strength selection example",
        "For same-level dyeing (no bleach) use 6% (20 vol) developer with colour:developer = 1:1; to lift 2-3 levels use 9% (30 vol), still 1:1 but with a longer processing time; for root touch-ups use 3% (10 vol) to reduce irritation. The smaller the target level difference, the lower the developer strength.",
        "Does a higher developer strength always give a lighter result?",
        "Yes, but with limits. 3%/6%/9%/12% correspond to 10/20/30/40 vol, and the higher the strength the stronger the lifting power; going beyond what you need over-damages the hair and risks uneven, over-processed roots.",
        "What happens if the ratio is wrong?",
        "Too thin gives uneven colour and too thick is hard to spread. Too little developer means weak colour payoff, too much means fast oxidation and blotchy results. Follow the brand's stated colour-to-developer volume ratio exactly.",
        "About Hair dye mixing ratio",
        "Hair dye mixing ratio is an online tool for everyday life. An everyday-life utility, close to daily needs, practical and convenient.",
    ]))


if __name__ == '__main__':
    main()
