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
    # 2026-10-02 补漏：<option>自然（Medium）</option> 在英文态被 _prefix「自然→Natural」吃掉汉字后
    # 只剩全角括号，旧版 --extract（仅 CJK 口径）漏收 ⇒ 字典缺键、--check 仍报残留。
    # 探针已改为 RESIDUAL_RE 口径对齐 --check；此处按源文形态补键。
    EXTRA['calc-2'] = {'自然（Medium）': 'Natural (Medium)'}
    write('calc-2', build('calc-2', [
        "\U0001F3A8 Foundation shade matching",
        "Recommend a foundation shade and selection tips based on your skin depth and undertone.",
        "Skin depth",
        "Very fair (Fair)",
        "Light (Light)",
        "Tan (Tan)",
        "Deep (Deep)",
        "Vein colour (determines cool or warm)",
        "Purple/blue leaning \u2192 cool",
        "Both purple and green \u2192 neutral",
        "Green/olive leaning \u2192 warm",
        "Gold and silver jewellery test",
        "Silver looks better \u2192 cool",
        "Both work \u2192 neutral",
        "Gold looks better \u2192 warm",
        "Reaction to sun exposure",
        "Burns easily",
        "Red first, then tans",
        "Tans easily",
        "Match my shade",
        "Pick your skin depth and undertone, then click match.",
        "Shade selection tips",
        "Swatch on the jawline where it meets the neck, not the back of the hand.",
        "Wait 30 seconds to see how the foundation settles into your skin tone.",
        "Natural daylight gives the most accurate read.",
        "The shade should be invisible, blending naturally into your skin.",
        "\U0001F4DA In-depth analysis: foundation shade matching",
        "Counter swatching is hard, so you want to pick a foundation shade close to your skin depth and undertone.",
        "Afraid of a colour mismatch when buying foundation online? Self-assess the undertone first, then compare with the brand's shade chart.",
        "A makeup artist quickly narrows candidates down to 2-3 shades before a bride's trial session.",
        "Lightness and undertone selection example",
        "Set skin lightness L = 62 (medium) and the vein test leaning green (warm yellow). That maps to a warm (yellow-based) foundation; take a warm shade with L close to 62 from the brand chart (for example natural 03) and swatch at the jawline-neck junction for the most accurate read. Cool pink undertones tend to look grey on the face.",
        "How do I tell whether I am cool or warm?",
        "Look at the veins on your wrist: blue-purple means cool, green means warm. Alternatively try gold and silver jewellery \u2014 if gold flatters you more you are usually warm, if silver flatters you more you are cool. Neutral undertones suit both.",
        "Why should I swatch on the jawline at a counter?",
        "The jaw connects the face and the neck, so that area is closest to your overall skin colour and less affected by local redness, which avoids a face-neck colour difference.",
    ]))

    write('checker-14', build('checker-14', [
        "\u2696\uFE0F Quality (standards / inspection / improvement) system",
        "A cosmetic quality standards inspection system covering sensory, physicochemical, microbiological and packaging dimensions",
        "Weighted composite score = \u03A3 (metric score \u00D7 metric weight) \u00F7 \u03A3 (4 \u00D7 metric weight) \u00D7 100%. Metrics are scored excellent 4, good 3, fair 2, poor 1. Dimension ratings follow the score rate (\u2265 90% excellent, 75% to 89% good, 60% to 74% fair, below 60% poor). Any metric scoring 2 or below is put on the improvement list and prioritised in descending weight order.",
        "Score each inspection item (excellent=4/good=3/fair=2/poor=1) and the system automatically computes the composite quality score with improvement suggestions",
        "Assess quality level",
        "Composite score = weighted average of all items",
        "Inspect regularly and keep improving quality management",
        "\U0001F4DA In-depth analysis: cosmetic quality system inspection",
        "Brands score a new product across four dimensions: sensory, physicochemical, microbiological and packaging labelling.",
        "QC staff score each item against the standards and produce a composite score with improvement suggestions.",
        "Contract manufacturers self-assess maturity before accepting an order to judge whether they can meet the client's quality requirements.",
        "Four-dimension weighted example",
        "Set sensory 85, physicochemical 90, microbiological 95 and packaging labelling 80 (100 each), with weights 0.3/0.3/0.25/0.15. The composite = 85\u00D70.3 + 90\u00D70.3 + 95\u00D70.25 + 80\u00D70.15 = 88.25 points, reaching grade A (\u2265 85) though packaging labelling could be optimized.",
        "Why does microbiology carry such a high weight?",
        "Microbial contamination directly affects usage safety (pathogens, failed preservatives) and is a compliance red line, so it is weighted above appearance-oriented metrics.",
        "If the composite score is low, which item should I fix first?",
        "Prioritise low-scoring items that are both high-weight and easy to improve, such as non-compliant packaging labelling and sensory stability. Physicochemical and microbiological issues have to be solved at the formula and process level.",
        "About the Quality (standards/inspection/improvement) system",
        "A cosmetic quality standards inspection and assessment system that checks product quality across four dimensions \u2014 sensory indicators, physicochemical indicators, microbiological indicators and packaging labelling \u2014 and outputs a weighted composite score, per-dimension ratings and targeted improvement suggestions.",
        "Four-dimension quality assessment (sensory / physicochemical / microbiological / packaging)",
        "Weighted scoring that highlights key metrics",
        "Visualizes the quality level of each dimension",
        "Automatically generates quality improvement suggestions",
        "Factory release quality inspection for cosmetics",
        "Periodic quality management self-check",
        "Quality improvement plan drafting",
        "Supplier quality audit",
    ]))

    write('checker-assessor-1', build('checker-assessor-1', [
        "\u2696\uFE0F Quality (inspection / assessment / improvement) mechanism",
        "A PDCA-based cosmetic quality check-assess-improve mechanism that outputs the maturity and improvement path of each stage",
        "Score each of the four PDCA stages (plan, do, check, act) and take the equal-weight average as system maturity. C (check) supplies the data and A (act) forms the closed loop; a weak stage drags the composite score down, which locates the bottleneck.",
        "PDCA stage assessment",
        "Score each stage capability (1-5), where 1 = not established, 2 = initially established, 3 = partially implemented, 4 = running effectively, 5 = continuously optimized",
        "P - Plan",
        "D - Do",
        "C - Check",
        "A - Act",
        "Assess the improvement mechanism",
        "PDCA cycle: Plan \u2192 Do \u2192 Check \u2192 Act",
        "Maturity 1-5 points; the composite score reflects how closed-loop the quality management is",
        "Evaluate once a quarter and keep driving quality improvement",
        "\U0001F4DA In-depth analysis: cosmetic quality PDCA assessment",
        "A quality lead uses the PDCA cycle (plan, do, check, act) to assess system maturity.",
        "Score each stage during a system audit to locate weak links.",
        "Consulting advisors diagnose the quality system and deliver an improvement path.",
        "PDCA maturity example",
        "Set P (plan) at 70, D (do) at 80, C (check) at 65 and A (act) at 60 (100 each). The equal-weight composite = (70+80+65+60) \u00F7 4 = 68.75 points. Low C and A show that the check-and-improve loop is weak, so data collection and corrective-action tracking come first.",
        "Which of the four PDCA stages matters most?",
        "A (act) is often overlooked yet most critical \u2014 without effective corrective and preventive action problems recur. C (check) supplies the data, and the two together form the closed loop.",
        "How are the maturity scores used?",
        "To compare product lines against each other and to read trends year over year. Stages below the threshold go into next quarter's improvement plan instead of being treated as a one-off pass.",
        "About the Quality (inspection/assessment/improvement) mechanism",
        "A cosmetic quality improvement mechanism assessment tool based on the PDCA (plan, do, check, act) cycle. It scores 16 capability metrics across the four stages and outputs per-stage maturity, weak links and the priority improvement path.",
        "16 quality management capability metrics",
        "Automatic identification and ranking of weak links",
        "Quality management system maturity assessment",
        "Quality improvement plan drafting",
    ]))


if __name__ == '__main__':
    main()
