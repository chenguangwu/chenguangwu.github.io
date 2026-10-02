#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'tcm-pharmacy')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'tcm-pharmacy')
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
    out = {'slug': slug, 'industry': 'tcm-pharmacy', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
DISCL_M = " A professional medical tool based on authoritative medical standards, for reference only."

def main():
    write('medicinal-wine', build('medicinal-wine', [
        "\U0001F9EE Medicinal Wine Steeping (Concentration / Time) Calculator",
        "Computes the optimal alcohol strength, steeping time and daily dose for medicinal wine from the herb type and amount",
        "Core formulas (from the input variables): min(d.maxDailyDose, Math.round(weight * 0.4)); Math.round(wineVolume / recommendedDose); Math.round((d.minDays + d.maxDays) / 2)",
        "/ Medicinal wine steeping calculator",
        "Warning: medicinal wine contains alcohol and is contraindicated in liver disease, pregnancy, alcohol allergy and while taking medication. This tool is for reference only; use it under the guidance of a TCM practitioner.",
        "Select the medicinal wine type",
        "Total herb weight (g)",
        "White liquor amount (ml)",
        "White liquor alcohol strength (%)",
        "Adult (60 kg)",
        "Adult (70 kg)",
        "Adult (80 kg)",
        "\U0001F4D6 Common medicinal wine recipe reference",
        "\U0001F4D0 Steeping knowledge",
        "Medicinal wine ratio",
        "The usual medicinal wine ratio is herb : white liquor = 1:5 to 1:10 (weight to volume). Tonic medicinal wines suit 1:5 to 1:8 and wind-dampness dispelling types suit 1:8 to 1:10.",
        "Alcohol strength selection",
        "50-60 degrees:",
        "Suitable for root, rhizome and animal materials, with good extraction (most commonly used)",
        "40-50 degrees:",
        "Suitable for flower, leaf and aromatic materials, reducing volatile oil loss",
        "60-70 degrees:",
        "Suitable for resin and gum materials that need high-strength alcohol to dissolve",
        "Steeping time",
        "Flowers and leaves: 7-15 days; roots and rhizomes: 15-30 days; animal or mineral materials: 30-60 days. Shake once every 3-5 days during steeping and inspect regularly. Active constituents dissolve fastest in the first 7 days.",
        "Dosing",
        "Generally 10-30 ml each time, 1-2 times per day. Take after meals or at bedtime. Though beneficial, medicinal wine should not be overdosed, and daily alcohol intake should not exceed 25 g.",
        "\U0001F4DA In-depth analysis: medicinal wine steeping (concentration / time / dose) preparation",
        "Tonic medicinal wine",
        "Blood-activating medicinal wine",
        "Daily wellness",
        "100 g crude herb + 1 L at 50% vol",
        "The herb to wine ratio is 1:10, crude drug concentration = 100/(1000x0.05)x100 = 10%, pure ethanol about 500 g; for a 60 kg adult using 0.4 g/kg/day the limit is 60 ml/day, take 24 ml/day split into 2 doses of 12 ml; total drinking days ceil(1000/24) = 42 days.",
        "Medicinal wine for a 60 kg elderly person",
        "The adult recommended dose is weight x 0.4 = 24 ml/day, 2 doses a day of 12 ml each; daily pure alcohol 12 g (above half of the dietary guideline limit of 25 g/day), so elderly people should reduce to 10-15 ml/day.",
        "How long should it steep before drinking?",
        "Roots and rhizomes need 30-60 days (take the mean of minDays and maxDays), flowers and leaves 14-21 days; too short gives insufficient extraction and too long risks souring and deterioration; refrigerated storage is recommended.",
        "What alcohol strength should I choose?",
        "White liquor of about 50-60 degrees generally extracts well: too low (below 40 degrees) leaves fat-soluble and some alkaloid components insufficiently extracted and risks mold, while too high (above 70 degrees) coagulates proteins on the herb surface and actually blocks extraction. Tonic types commonly use about 50 degrees and wind-dampness blood-activating types can use 60 degrees. The steeping container must be sealed and protected from light; ceramic or glass is best, and metal and plastic should be avoided.",
        "About the Medicinal Wine Steeping (Concentration / Time) Calculator",
        "Medicinal Wine Steeping (Concentration / Time) Calculator." + DISCL_M,
        "How to use the Medicinal Wine Steeping (Concentration / Time) Calculator",
        "What does the Medicinal Wine Steeping (Concentration / Time) Calculator do?",
        "Based on the herb type and amount, computes the optimal alcohol strength, steeping time and daily dose for medicinal wine, suitable for wellness wine preparation.",
        "How do I use the Medicinal Wine Steeping (Concentration / Time) Calculator?",
        "Which scenarios suit the Medicinal Wine Steeping (Concentration / Time) Calculator?",
    ]))
    write('patent-medicine', build('patent-medicine', [
        "\U0001F33F Chinese Patent Medicine (Functions and Indications) Quick Lookup",
        "Looks up the functions, indications, composition, usage, dosage and precautions of common Chinese patent medicines",
        "/ Chinese patent medicine quick lookup",
        "Search (drug name / function / symptom)",
        "Exterior-releasing",
        "Heat-clearing",
        "Tonic",
        "Qi-regulating",
        "Dampness-dispelling",
        "Tranquilizing",
        "Blood-activating",
        "Phlegm-resolving and cough-relieving",
        "Total",
        "Chinese patent medicines",
        "Warning: medication notes",
        "Syndrome-based prescribing",
        "Chinese patent medicines must be selected on the basis of syndrome differentiation and treatment. The same disease may have different syndromes and the same syndrome may occur in different diseases. For example colds divide into wind-cold and wind-heat, which call for completely different medicines.",
        "Combined use",
        "When combining Chinese patent medicines with each other or with Western medicines, compatibility taboos must be observed. Patent medicines containing the same ingredient should not be taken together to avoid overdose.",
        "Warning: this tool is for study reference only; follow medical advice for specific use. Pregnant women, children, the elderly and those with impaired liver or kidney function must be especially careful.",
        "\U0001F4DA In-depth analysis: Chinese patent medicine (functions and indications) quick lookup",
        "Clinical prescribing",
        "Pharmacy consultation",
        "Patient self-check",
        "Suxiao Jiuxin Wan",
        "Functions: moves qi and blood, dispels stasis and relieves pain; indications: qi stagnation and blood stasis type coronary heart disease angina; contains chuanxiong and borneol; take 4-6 pills three times daily dissolved in the mouth, and 10-15 pills for an acute attack.",
        "Ganshi Qingre Keli",
        "Functions: disperses wind and cold, releases the exterior and clears heat; indications: wind-cold common cold (headache, fever, chills and body aches); dissolve 12 g in boiled water twice daily; one course is 3 days; contraindicated in wind-heat colds and exterior deficiency spontaneous sweating.",
        "What are the key points when reading the package insert?",
        "Check whether [functions and indications] match the syndrome, whether [usage and dosage] exceeds the age limit, whether [contraindications] include allergy, pregnancy or liver damage, and whether [precautions] mention Western medicine interactions (for example avoid combining ephedrine-containing products with antihypertensives).",
        "Can the same name from different manufacturers be substituted?",
        "If the prescription, dosage form, specification and functions of a same-named patent medicine are consistent it can generally be substituted; but note three points: (1) some products have \"same name different formula\" (local standards differing from national",
        "ones); (2) dose specifications and dosing frequency differ, so the daily dose after conversion may vary; (3) compound preparations containing Western ingredients (such as some cold medicines containing paracetamol) must be checked when switching manufacturers to avoid duplicating a Western medicine already being taken.",
        "About the Chinese Patent Medicine (Functions and Indications) Quick Lookup",
        "Chinese Patent Medicine (Functions and Indications) Quick Lookup." + DISCL_M,
        "e.g. cold, Liuwei Dihuang Wan, heat-clearing...",
    ]))
    write('pregnancy-contraindication', build('pregnancy-contraindication', [
        "\U0001F4DA Pregnancy Contraindication (Use With Caution / Prohibited) List Lookup",
        "Looks up the graded pregnancy contraindications of Chinese medicine, covering the prohibited, to avoid and use with caution levels",
        "/ Pregnancy contraindication lookup",
        "Warning: medication safety in pregnancy is critical! This tool is for professional reference only, and pregnant women must take herbs under physician guidance.",
        "Prohibited",
        "To avoid",
        "Use with caution",
        "Total",
        "records",
        "\U0001F4D6 Classification of pregnancy contraindications",
        "Prohibited herbs",
        "Absolutely forbidden, mostly potent poisons or violently abortifacient drugs. Include croton, blistering beetle, musk, sanleng, ezhu, leech, gadfly, shanglu, kansui, daiji, genkwa, morning glory seed, realgar and qingfen.",
        "Herbs to avoid",
        "In principle not to be used, as they may cause substantial harm to the fetus. Include aconite, aconite root, centipede, scorpion, mercury, arsenolite, akebia stem, strychnine, chuanwu and caowu.",
        "Herbs to use with caution",
        "Should be used cautiously depending on the condition and avoided where possible. Include blood-activating and stasis-dispelling herbs (safflower, peach kernel, achyranthes, chuanxiong), qi-moving and stagnation-breaking herbs (immature bitter orange, areca), pungent and hot herbs (dried ginger, cinnamon) and slippery diuretic herbs (coix, plantago seed).",
        "Principles of medication in pregnancy",
        "1. The first 3 months of pregnancy are especially critical; avoid all unnecessary medication",
        "2. When the condition requires it, choose drugs with no or minimal effect on the fetus",
        "3. Strictly control dose and course, and stop as soon as the condition is cured",
        "4. Never use prohibited or to-avoid herbs; use use-with-caution herbs only as appropriate under an experienced physician",
        "\U0001F4DA In-depth analysis: pregnancy contraindication (use with caution / prohibited) list",
        "Obstetric prescribing",
        "Compounding and dispensing",
        "Patient self-check",
        "Mercury, arsenic, realgar, qingfen, blistering beetle, strychnine, toad venom, chuanwu, caowu, lilu, gourd tip, chalcanthite, kansui, daiji, genkwa, morning glory seed, shanglu, musk, leech, gadfly, sanleng, ezhu and croton are all potent poisons or strong purgatives that break blood, absolutely prohibited in pregnancy.",
        "Achyranthes, chuanxiong, safflower, peach kernel, turmeric, moutan, immature bitter orange, mature bitter orange, rhubarb, senna, aloe, mirabilite, aconite and cinnamon act to promote menstruation and move blood or are pungent and hot, so they are used with caution in pregnancy and, if necessary, only short term in small amounts.",
        "How do I judge quickly?",
        "Enter the herb name and the system returns the level (prohibited or use with caution), the reason and substitution suggestions; TCM pregnancy contraindications follow the dual standard of the Pregnancy Contraindication Song plus the Chinese Pharmacopoeia appendix.",
        "What is the difference between use with caution and prohibited?",
        "Prohibited means never used (mostly potent poisons or strongly blood-breaking and stasis-expelling or opening orifices, such as leech, gadfly, musk, croton and morning glory seed); use with caution means that when truly necessary it may be used short term after a physician weighs the risks and controls the dose and course (such as peach kernel, safflower, rhubarb, aconite and dried ginger). The stage of pregnancy also matters: the early period (first 3 months) when embryonic organs form is the most sensitive and contraindications are enforced most strictly, while the middle and late periods can be relatively relaxed but still need caution. Lactation also requires considering transfer into breast milk.",
        "About the Pregnancy Contraindication (Use With Caution / Prohibited) List Lookup",
        "Pregnancy Contraindication (Use With Caution / Prohibited) List Lookup." + DISCL_M,
        "Enter the herb name, such as aconite or safflower...",
    ]))


if __name__ == '__main__':
    main()