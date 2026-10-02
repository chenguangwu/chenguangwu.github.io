#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'tcm-chemistry')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'tcm-chemistry')
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
    out = {'slug': slug, 'industry': 'tcm-chemistry', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
DISCL_M = " A professional medical tool based on authoritative medical standards, for reference only."

def main():
    write('calc-44', build('calc-44', [
        "\U0001F9EE Extraction Count Calculator (Partition Coefficient Method)",
        "Computes the required number of extractions and the overall recovery from the partition coefficient K, original solution volume V0, solvent volume V per extraction and the target recovery, and plots recovery against the number of extractions.",
        "Core formulas (from the input variables): Math.ceil(Math.log(1-0.999999)/Math.log(q)); Math.ceil(Math.log(1-tFrac)/Math.log(q)); min(max(target,0),99.999)/100",
        "Extraction count calculation (partition coefficient)",
        "/ extraction count calculation (partition coefficient)",
        "Partition coefficient K",
        "Original solution volume V0 (mL)",
        "Solvent volume V per extraction (mL)",
        "\U0001F4A1 Fraction remaining in the original phase after one extraction = V0 / (V0 + K*V); after n extractions the total remainder = [V0/(V0+K*V)]^n; total recovery = 1 - remainder; required count n = lg(1-target) / lg[V0/(V0+K*V)].",
        "\U0001F4C8 Recovery against number of extractions",
        "Partition coefficient K = concentration in the extract phase / concentration in the original phase (at equilibrium)",
        "Several small-volume extractions are better than one large-volume extraction (for the same total solvent volume)",
        "\U0001F4DA In-depth analysis: extraction count calculation (volumetric method)",
        "Fraction remaining in the aqueous phase",
        "Back-calculated N from the target recovery",
        "Single-volume comparison",
        "Back-calculated count",
        "V0 = 100 mL, V = 25 mL, K = 4; the single-extraction remainder q = 100/(100+4x25) = 0.5; reaching 99% needs 1-0.5^n >= 0.99, so about 7 extractions.",
        "Merged volume",
        "Adding all at once needs 7x25 = 175 mL: single-extraction recovery = 4x1.75/(1+4x1.75) = 87.5%, still below the 99% reached by 7 separate extractions.",
        "How does it differ from the partition coefficient method?",
        "The same physical process expressed two ways: q = V0/(V0+K*V) corresponds to the remaining fraction.",
        "How many extractions are practical?",
        "Weighing solvent against energy, extraction is usually stopped at 2-3 times when 85-95% is reached.",
        "About Extraction Count Calculation (Partition Coefficient)",
        "Used for liquid-liquid extraction process calculation. Based on the partition coefficient K, the original solution volume, the solvent volume per extraction and the target recovery, it computes the required number of extractions and the overall recovery by the partition law and compares it with a single extraction using the same total solvent, showing the advantage of many small extractions.",
        "Exact partition law solution",
        "Recovery against number of extractions curve",
        "Single extraction vs multiple extractions",
        "Extraction process design for TCM active components",
        "Extraction scheme optimization for chemical analysis",
        "Laboratory separation and purification teaching",
        "Economics of solvent usage",
        "Partition coefficient K",
        "Original solution volume",
        "Solvent volume",
        "Target recovery",
    ]))
    write('chromatography-gradient', build('chromatography-gradient', [
        "\U0001F4D0 Silica Gel Column Chromatography Elution Gradient Designer",
        "Designs a gradient elution scheme from the target component type to optimize separation",
        "Designs a gradient elution scheme from the target component type to optimize separation.",
        "Chromatography (silica gel column) elution gradient designer",
        "/ Elution gradient design",
        "Sample component type",
        "Alkaloids",
        "Volatile oil",
        "Mixture (unknown)",
        "Silica gel ratio (sample:silica gel)",
        "1:30 (easy separation)",
        "1:50 (routine separation)",
        "1:100 (difficult separation)",
        "1:200 (fine separation)",
        "Column diameter (cm)",
        "Sample load (g)",
        "Add acid modifier (alkaloids)",
        "Add base modifier (organic acids)",
        "\U0001F4D0 Design the gradient scheme",
        "\U0001F4DA In-depth analysis: silica gel column chromatography elution gradient design",
        "Sample mass x silica gel ratio",
        "Column volume and column height",
        "BV elution volume",
        "Silica gel amount",
        "Sample 1 g with a 30:1 silica gel ratio gives 30 g of silica gel; silica gel bulk density is about 0.5 g/mL so the volume is 60 mL (about 60 BV).",
        "Column height",
        "Column diameter 3 cm gives a radius of 1.5 cm; column height = 60/(pi x 1.5^2) = 60/7.07 is about 8.5 cm, a reasonable packing range.",
        "How is the silica gel ratio chosen?",
        "The routine range is 30-100:1 (sample:silica gel); take the larger value for difficult separations.",
        "What is BV?",
        "Bed volume; elution volume is often expressed in BV, and 1 BV is about the bulk volume of the silica gel.",
        "About the Chromatography (Silica Gel Column) Elution Gradient Designer",
        "Silica Gel Column Chromatography Elution Gradient Designer - automatically designs an elution gradient scheme from the component type, including silica gel column chromatography parameters." + DISCL_M,
    ]))
    write('detector-4', build('detector-4', [
        "\U0001F48A Incompatibility (Physicochemical) Detection",
        "Enter two Chinese medicine names to check whether there are eighteen antagonisms, nineteen fears and other compatibility taboos or physicochemical interactions",
        "Compatibility taboos: compares the two entered Chinese medicines against the eighteen antagonisms and nineteen fears mnemonics, for example licorice antagonizes kansui, daiji, zexie and yuanhua; aconite antagonizes banxia, Gualou, beimu, bailian and baiji; lilu antagonizes the shen group, xixin and shaoyao. A hit warns the two should not be used together; the result is for reference only and actual use must follow medical advice.",
        "Medicine A",
        "Medicine B",
        "Check compatibility",
        "\U0001F4DA In-depth analysis: compatibility taboo detection (database)",
        "Antagonistic pair lookup",
        "Same-formula warning",
        "Component conflict",
        "Antagonistic pair",
        "Entering \"licorice + kansui\" hits an eighteen-antagonism entry and flags a compatibility taboo; \"aconite + banxia\" also falls under aconite antagonizing banxia, Gualou and beimu.",
        "Avoid in the same formula",
        "\"lilu + ginseng\" falls under lilu antagonizing the shen group, so a database hit is flagged red and the two should not share a formula.",
        "How does it differ from physicochemical taboos?",
        "This tool leans on database lookup of antagonistic pairs, while physicochemical taboos lean on pH and precipitation reactions.",
        "Does a hit mean the combination is banned?",
        "Traditional taboos warn against it; modern practice has a few exception formulas, but the combination is avoided as routine.",
        "Eighteen antagonisms: licorice antagonizes kansui, yuanhua, daiji and zexie; lilu antagonizes ginseng, glehnia, danshen, xuanshen, kushen, xixin and shaoyao; aconite antagonizes banxia, beimu, Gualou and baiji",
        "Nineteen fears: sulfur fears mirabilite, mercury fears arsenic, wolf poison fears litharge, croton antagonizes morning glory, clove antagonizes turmeric and so on",
        "Compatibility taboos were summarized from the experience of physicians through the ages, and modern research has confirmed some of them as increased toxicity or reduced efficacy",
        "A few classic formulas such as Haizao Yuhu Tang (zexie + licorice) use an antagonistic pair together and must be used under expert guidance",
        "This tool only checks the eighteen antagonisms and nineteen fears and does not cover all drug interactions; follow medical advice when using medicines",
        "About Incompatibility (Physicochemical) Detection",
        "Chinese medicine compatibility taboo detection tool; enter two Chinese medicine names to automatically check whether eighteen antagonisms, nineteen fears and other compatibility taboos exist and give a detailed explanation.",
        "Full coverage of the eighteen antagonisms and nineteen fears",
        "Bidirectional matching (A + B = B + A)",
        "With sources and detailed notes",
        "Supports common Chinese medicine names",
        "Safety review of TCM prescriptions",
        "Chinese medicine compatibility teaching",
        "Pharmacist prescription review reference",
        "Chinese medicine knowledge learning",
    ]))


if __name__ == '__main__':
    main()