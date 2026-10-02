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
    write('assessor-risk-12', build('assessor-risk-12', [
        "\u2696\uFE0F Safety (certification / compliance / risk) assessment",
        "A cosmetic safety compliance risk assessment checklist that checks each requirement against regulation",
        "Product information",
        "Product category",
        "Special cosmetics (whitening, sunscreen, hair dye, etc.)",
        "Children's cosmetics",
        "Compliance checklist",
        "Set the compliance status of each item and the system automatically computes the compliance score and risk level",
        "Assess compliance risk",
        "Based on the Cosmetics Supervision and Administration Regulation and the Cosmetic Safety Technical Standard",
        "Compliant = 2 points, partially compliant = 1 point, non-compliant = 0 points, not applicable = 2 points",
        "Results are for reference only; formal compliance assessment must be carried out by a qualified institution",
        "\U0001F4DA In-depth analysis: cosmetic compliance risk assessment",
        "Before filing a new product, check item by item whether each ingredient appears on the prohibited or restricted lists of the Cosmetic Safety Technical Standard.",
        "For imported cosmetics, verify the labelling and whether efficacy claims are substantiated, to avoid non-compliant advertising.",
        "Contract manufacturers run a compliance self-check for brands and deliver a risk level together with a remediation list.",
        "Weighted risk scoring example",
        "Set ingredient safety at 40, labelling compliance at 30, efficacy substantiation at 20 and production qualification at 10 (100 points each). The weighted risk score = 40\u00D70.4 + 30\u00D70.3 + 20\u00D70.2 + 10\u00D70.1 = 30 points. Under the bands 0-30 low risk, 31-60 medium risk and 61-100 high risk, this case is low risk but the efficacy substantiation documents are still missing.",
        "Can this replace the official filing review?",
        "No. This tool is a pre-filing self-check that screens against the Cosmetics Supervision and Administration Regulation and the safety technical standard. The regulator's review conclusion is what finally counts.",
        "Which items are most likely to be judged high risk?",
        "Detected prohibited ingredients, efficacy claims without scientific support, and special cosmetics without a registration certificate are the three that are normally judged high risk and require immediate remediation.",
        "About the Safety (certification/compliance/risk) assessment",
        "A cosmetic safety compliance risk assessment tool that checks product filing, ingredient compliance, test reports and labelling against the Cosmetics Supervision and Administration Regulation, the Cosmetic Safety Technical Standard and related requirements item by item, then outputs a compliance score and risk level.",
        "16-item core compliance checklist",
        "Weighted scoring that highlights high-risk items",
        "Automatically lists the issues that need remediation",
        "Pre-launch compliance self-check for cosmetics",
        "Quality and safety risk assessment",
        "Document check before product filing",
        "Supply chain compliance audit",
        "e.g. XX moisturizing cream",
    ]))

    write('bmi-beauty', build('bmi-beauty', [
        "\U0001F484 Beauty BMI",
        "Not just BMI, but also body shape analysis, ideal weight range and beauty recommendations",
        "Core formulas (by input variable): max(0, min(100, ((bmi - 15) \u00F7 20) \u00D7 100)); idealWeight(h, gender) \u00D7 0.95; idealWeight(h, gender) \u00D7 1.05",
        "Beauty BMI",
        " / Beauty BMI",
        "Waist (cm, optional)",
        "Hip (cm, optional)",
        "\U0001F4DA In-depth analysis: Beauty BMI",
        "Want to know whether you fall in",
        "a healthy range, and the corresponding",
        "range.",
        "Work out the gap in kilograms between your current BMI and your target BMI before body management.",
        "A quick baseline for beauty advisors combining BMI and body shape to give clients diet and exercise advice.",
        "BMI and ideal weight example",
        "For a height of 1.65 m and a weight of 58 kg, BMI = 58 \u00F7 1.65\u00B2 = 21.3, which is in the healthy range (18.5-23.9). The ideal weight lower bound = 18.5 \u00D7 1.65\u00B2 \u2248 50.3 kg and the upper bound = 23.9 \u00D7 1.65\u00B2 \u2248 65.1 kg, so the current 58 kg sits in the middle of the range.",
        "Does a normal BMI guarantee a good figure?",
        "Not necessarily. BMI does not distinguish muscle from fat, so a fit person may have a high BMI but a low body fat percentage. Read it together with",
        "body fat percentage",
        "and waist circumference; a healthy waist for women is usually under 80 cm.",
        "How does the beauty version differ from ordinary BMI?",
        "The calculation is the same, but the beauty version adds the ideal weight range and shape-typing advice, plus reminders about the influence of muscle mass and body fat, which makes it easier to align with a body management plan.",
        "About the Beauty BMI",
        "Beauty BMI. A beauty and skincare tool that helps calculate product dosage and mixing ratios.",
        "e.g. 70",
        "e.g. 90",
    ]))

    write('calc-1', build('calc-1', [
        "\U0001F9F4 Skin type test",
        "Use a short questionnaire to determine your skin type and get basic skincare recommendations.",
        "The questionnaire scores dimensions such as oiliness, tightness and sensitivity, and the combined score falling into a band determines dry, oily, combination, normal or sensitive skin. A large gap between the T-zone and cheek scores suggests combination skin. Results follow the sensations you report, so retest when the season changes.",
        "One hour after cleansing, how does your face feel?",
        "Oily overall, clearly so in the T-zone",
        "Tight and dry, even flaking",
        "Oily T-zone, dry cheeks",
        "Comfortable, neither oily nor dry",
        "What are your pores like?",
        "Large pores, prone to oiliness",
        "Fine but dry",
        "Noticeably large in the T-zone, fine on the cheeks",
        "Even and fine",
        "Do you get sensitive, red or stinging easily?",
        "How are acne and blackheads?",
        "Often oily with acne and blackheads",
        "Occasional bumps from dryness",
        "Many blackheads in the T-zone, few on the cheeks",
        "How does your skin look after makeup?",
        "Makeup slides off, skin gets oily",
        "Makeup cakes and flakes",
        "T-zone makeup slides off, cheeks cake",
        "Smooth and natural",
        "How glossy is your skin?",
        "Oily shine overall",
        "Dull and lacking glow",
        "Oily shine in the T-zone, matte cheeks",
        "Natural glow",
        "Test your skin type",
        "Click test after answering all questions.",
        "\U0001F4DA In-depth analysis: skin type test",
        "Not sure whether your skin is dry, oily or combination before you start skincare? Use this questionnaire to self-test.",
        "Skin condition changes with the seasons, so re-evaluate your current skin type and adjust your products.",
        "Beauty counters recommend cleanser and cream types to clients based on their skin type.",
        "Questionnaire scoring example",
        "Set oiliness at 12 points (20 max), tightness at 15 points (20 max) and sensitivity at 8 points (20 max). High oiliness with low tightness points to oily skin; high tightness with low oiliness points to dry skin; an oily T-zone with dry cheeks points to combination skin. The combined score falling into a band yields the skin type.",
        "What should I do if I test as combination skin?",
        "Care for the zones separately: control oil in the T-zone and moisturize the cheeks. Choose a gentle amino-acid cleanser that does not strip, layer a cream on the cheeks, and avoid strong-cleansing products all over the face.",
        "Do the results change with the season?",
        "Yes. Being drier in winter and oilier in summer is common, so test once per season. Sensitive skin is also affected by ambient temperature and humidity, so judge by your current state.",
    ]))


if __name__ == '__main__':
    main()
