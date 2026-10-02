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
    write('aging-calculator', build('aging-calculator', [
        "\U0001F9F4 Multi-Dimensional Skin Age Test",
        "Answer 15 professional questions to find out your skin's true age",
        "Skin Age Test",
        " / Skin Age Test",
        "Actual age",
        "Start the test \u2192",
        "\u2190 Previous question",
        "\U0001F504 Retake the test",
        "\U0001F4BE Save result",
        "\U0001F486 Age-based skincare routines",
        "\U0001F9EA Anti-aging ingredient guide",
        "\U0001F338 Ages 20-25: prevention first",
        "Core: sunscreen + hydration + cleansing",
        "Focus: prevent photoaging and keep up basic hydration",
        "Optional: antioxidant serum (vitamin C)",
        "Avoid: over-cleansing and frequent exfoliation",
        "\U0001F33A Ages 25-30: early anti-aging",
        "Core: antioxidants + first anti-wrinkle steps",
        "Focus: add an eye cream and a serum to your routine",
        "Recommended: vitamin C, niacinamide, Pro-Xylane",
        "Note: keep a regular schedule and cut back on late nights",
        "\U0001F339 Ages 30-40: full anti-aging",
        "Core: anti-wrinkle + firming + fading dark spots",
        "Focus: retinoids, peptides and Pro-Xylane",
        "Recommended: retinol, hexapeptide-8, vitamin C",
        "Advice: consider regular professional treatments (e.g. IPL photorejuvenation)",
        "\U0001F490 Ages 40+: intensive repair",
        "Core: firming and lifting + plumping repair",
        "Focus: high-concentration anti-aging actives",
        "Recommended: high-strength retinol, Pro-Xylane, growth factors",
        "Note: gentle nourishment, avoid irritation",
        "\u2728 Celebrity anti-aging ingredient table",
        "Benefit",
        "Suitable skin type",
        "Retinol (vitamin A)",
        "Anti-wrinkle, soften lines, boost collagen",
        "Resilient skin types",
        "Use at night, build tolerance gradually, not for use during pregnancy",
        "Antioxidant, brighten, fade dark spots",
        "All skin types",
        "Use in the morning, always follow with sunscreen; prototype vitamin C can sting",
        "Niacinamide",
        "Control oil, brighten, reinforce the barrier",
        "Oily and combination skin",
        "Start at a low concentration; some people are sensitive to it",
        "Pro-Xylane",
        "Firming, repair, boost collagen",
        "Gentle and non-irritating, suitable for sensitive skin",
        "Peptides",
        "Anti-wrinkle, firming, botox-like effect",
        "Gentle, requires consistent long-term use",
        "Ceramides",
        "Repair the barrier, hydrate",
        "Dry and sensitive skin",
        "Gentle, can be combined with other actives",
        "Hydrate, moisturize, plump",
        "Layering different molecular weights works better",
        "Astaxanthin",
        "Antioxidant, anti-photoaging",
        "Gentle, works even better alongside vitamin C",
        "\u26A0\uFE0F Skincare ingredients should be matched to your own skin type; patch-test behind the ear first. Start efficacy products at a low concentration to build tolerance.",
        "\U0001F4DA In-depth analysis: multi-dimensional skin age test",
        "If you are past 25 and want an objective reading of your skin's true age, compare it with your chronological age to spot early aging.",
        "Establish a baseline before medical aesthetics or anti-aging skincare so later improvements are easy to compare.",
        "Skincare brands collect multi-dimensional questionnaires from users and turn them into personalized suggestions for anti-aging categories such as lipstick and serum.",
        "Weighted five-dimension example",
        "Set wrinkles at 38, dark spots at 42, elasticity at 40, pores at 45 and sensitivity at 30 (60 points each), with weights of 0.25/0.20/0.20/0.15/0.20. The weighted score = 38\u00D70.25 + 42\u00D70.20 + 40\u00D70.20 + 45\u00D70.15 + 30\u00D70.20 = 39.0 points. The 35-45 band corresponds to a skin age roughly 2-5 years above chronological age, indicating mild premature aging.",
        "Can questionnaire results replace a dermatologist's diagnosis?",
        "No. The skin age test is a rough estimate based on a self-report questionnaire, meant for daily reference and trend tracking. Dark spots, elasticity and the like need professional instruments such as VISIA imaging or a dermatoscope; if anything looks abnormal, please see a doctor.",
        "How are the dimension weights determined?",
        "The weights reflect how much each aging sign influences perceived visual age, so wrinkles and dark spots carry more weight. Different scales use different band thresholds; this tool uses a 100-point mapping and reports a range rather than a precise age in years.",
        "About the Skin Age Test",
        "Skin age test. A beauty and skincare tool that helps calculate product dosage and mixing ratios. A professional beauty tool based on authoritative cosmetic science, for reference only.",
    ]))

    write('analysis-cost-profit', build('analysis-cost-profit', [
        "\U0001F4B0 Salon revenue, cost and profit analysis",
        "Estimate gross profit, net profit and the break-even customer count from customer volume, average ticket and per-client consumables",
        "A salon's costs fall into two groups: consumables (products, single-use items) grow linearly with customer volume and are variable costs; labor, rent and equipment depreciation occur at a fixed monthly amount and are fixed costs. Revenue comes from customer volume times average ticket; subtract variable consumables to get gross profit. Then use \"contribution margin per client = average ticket \u2212 per-client consumables\" to spread fixed costs across every client, which gives the break-even customer count. The business only turns a profit above that number, and the excess is the safety margin. All calculations run locally in your browser and no data is uploaded.",
        "Operating revenue = customer volume \u00D7 average ticket; gross profit = operating revenue \u2212 customer volume \u00D7 per-client consumables; operating profit = gross profit \u2212 (labor + rent and other fixed costs); break-even customer count = (labor + fixed costs) \u00F7 (average ticket \u2212 per-client consumables)",
        "Customer volume (clients/month)",
        "Per-client consumables cost (CNY)",
        "Labor cost (CNY/month)",
        "Rent and fixed costs (CNY/month)",
        "\U0001F4DA In-depth analysis: salon revenue, cost and profit analysis",
        "Monthly profit-and-loss review for a store",
        "Break-even customer estimate for a new shop",
        "Pricing and consumables cost assessment",
        "Operating revenue = customer volume \u00D7 average ticket; gross profit = operating revenue \u2212 customer volume \u00D7 per-client consumables; operating profit = gross profit \u2212 (labor + rent and other fixed costs);",
        "break-even",
        "customer volume = (labor + fixed costs) \u00F7 (average ticket \u2212 per-client consumables).",
        "With 420 clients, an average ticket of 320, per-client consumables of 60, labor of 30,000 and fixed costs of 35,000, revenue is 134,400, variable consumables 25,200 and gross profit 109,200 (",
        "81.25%); fixed cost is 65,000 and operating profit 44,200 (",
        "32.89%); the per-client",
        "contribution margin is",
        "260, so the break-even customer count = 65,000/260 = 250.00 clients, leaving a safety margin of 170 clients.",
        "What is the contribution margin per client used for?",
        "It is the amount each additional customer contributes toward covering fixed costs. Dividing the fixed costs by it gives the break-even customer count, which anchors both customer-acquisition targets and pricing.",
        "What net profit margin counts as healthy?",
        "Salons typically run a 10%-25% net margin; asset-heavy medical aesthetics and asset-light quick-cut salons differ widely, so read it together with the rent and labor shares of revenue.",
        "About the Financial (revenue/cost/profit) analysis",
        "Financial (revenue/cost/profit) analysis. A beauty and skincare tool that helps calculate product dosage and mixing ratios.",
    ]))

    write('analysis-detector-diagnosis', build('analysis-detector-diagnosis', [
        "\U0001F9F4 Skin testing, analysis and diagnosis technology",
        "Testing / analysis / diagnosis",
        "The tools report relative reference values across dimensions such as moisture, oil, pigment, pores and sensitivity, and place your skin into a quadrant using empirical ranges (for example moisture 40-60, oil 30-55). Readings are affected by ambient temperature and humidity and by recent skincare, so treat them as daily reference only; if something looks abnormal or discomfort persists, see a dermatologist.",
        "Skin test metrics (each 0-100, reference: moisture 40-60 / oil 30-55)",
        "Moisture",
        "Oil",
        "Pigment",
        "Pores",
        "Analyze skin type",
        "\U0001F4DA In-depth analysis: skin testing and analysis technology",
        "Once a skin analyzer gives you moisture, oil, pigment and pore readings, you want to know which skin type they correspond to.",
        "Sensitive-skin users assess barrier status to decide whether to simplify their routine.",
        "Skincare advisors use the test report to recommend a product set and explain what each metric means.",
        "Moisture-oil quadrant example",
        "Set moisture at 38 (reference range 40-60) and oil at 62 (reference range 30-55). Moisture is low while oil is high, which places the reading in the \"oily outside, dry inside\" zone: a water-deprived barrier with compensatory oil production. Hydrate and control oil rather than cleansing more aggressively.",
        "Can an analyzer reading serve as a diagnosis?",
        "No. Home and counter-top analyzers give relative reference values that shift with ambient temperature and humidity, the measurement site, and recent skincare. If readings are abnormal or discomfort persists, get a professional assessment at a dermatology clinic.",
        "How do I get accurate moisture and oil readings?",
        "Measure 2-3 times under constant temperature at the same site, 30 minutes after cleansing, and take the average. A single reading fluctuates a lot, so the trend matters more than the absolute value.",
        "About Skin (testing/analysis/diagnosis) technology",
        "Skin (testing/analysis/diagnosis) technology. A beauty and skincare tool that helps calculate product dosage and mixing ratios.",
    ]))


if __name__ == '__main__':
    main()
