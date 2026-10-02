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
    write('extraction-counts', build('extraction-counts', [
        "\U0001F9EE Extraction Count Calculator",
        "Computes the number of extractions and the recovery of each step from the partition coefficient (K) and the phase ratio",
        "Core formulas (from the input variables): Math.ceil(Math.log(1 - target/100) / Math.log(remainFraction)); (K x singleRatio / (1 + K x singleRatio)) x 100; (1 - remainNow) x 100",
        "Extraction count (partition coefficient) calculator",
        "/ Extraction count calculation",
        "Partition coefficient K (organic phase / aqueous phase)",
        "Phase ratio per extraction (V organic / V aqueous)",
        "Initial total amount (mg, optional)",
        "\U0001F9EE Compute the extraction scheme",
        "\U0001F4DA In-depth analysis: extraction count calculation (partition coefficient method)",
        "Single-extraction rate",
        "Cumulative recovery",
        "Merged solvent comparison",
        "3 extractions",
        "K = 4 with solvent/water ratio per extraction = 0.25: the single-extraction remainder = 1/(1+4x0.25) = 0.5, cumulative after n times = 1-0.5^n, and 3 times gives 87.5%.",
        "One merged extraction vs several",
        "With the same total solvent ratio of 0.75, one extraction gives 4x0.75/(1+4x0.75) = 75%; three extractions of 0.25 each reach 87.5%, so separate extractions are more efficient.",
        "Why is separate extraction better?",
        "The remainder fraction is fixed each time, so multiplying it several times lowers the residue exponentially and raises the total recovery.",
        "What is K?",
        "The partition coefficient is the target concentration ratio between the organic and aqueous phases; the larger it is, the easier the target moves into the organic phase.",
        "About Extraction Count (Partition Coefficient) Calculator",
        "Extraction count calculator - computes the number of liquid-liquid extraction rounds and the recovery from the partition coefficient, an aid for separation and purification in Chinese medicine chemistry." + DISCL_M,
    ]))
    write('extraction-solvent', build('extraction-solvent', [
        "\U0001F4DA Extraction Solvent Selection Guide",
        "Recommends the best extraction solvent system from the target component type and polarity",
        "/ Extraction solvent selection",
        "Target component type",
        "Alkaloids (free base)",
        "Alkaloid salts",
        "Anthraquinone aglycones",
        "Anthraquinone glycosides",
        "Terpenes / volatile oils",
        "Organic acids",
        "Polysaccharides",
        "Extraction purpose",
        "Routine extraction",
        "Enrichment and purification",
        "Content assay",
        "Industrial production",
        "Target polarity range (optional)",
        "High polarity (water soluble)",
        "Moderate polarity",
        "Low polarity (fat soluble)",
        "Heating condition",
        "Room-temperature maceration",
        "Heated reflux",
        "Heat-sensitive components (avoid high temperature)",
        "\U0001F4DA Generate the recommendation",
        "\U0001F4CC View all solvents",
        "\U0001F4DA In-depth analysis: extraction solvent selection guide",
        "Polarity matching",
        "Industrial substitutes",
        "Heat-sensitive conditions",
        "Flavonoid extraction",
        "Flavonoids are of moderate polarity, so ethanol or methanol comes first; for industrial scale ethanol replaces methanol to cut toxicity, and heat-sensitive components use low-temperature ultrasound or percolation.",
        "Volatile oils",
        "Volatile oils are lipophilic, so use petroleum ether / diethyl ether or steam distillation; avoid prolonged high-temperature decoction that loses volatiles.",
        "How is polarity chosen?",
        "Like dissolves like: alkaloid salts are hydrophilic and free bases lipophilic; glycosides are hydrophilic and terpenes lipophilic.",
        "Why does industry use ethanol?",
        "Low toxicity, easy to recover and adjustable in polarity by concentration, making it more suitable for scale-up than methanol.",
        "About the Extraction Solvent Selection Guide",
        "Extraction solvent selection guide - picks the best extraction solvent from the polarity of the Chinese medicine component, with solvent polarity parameter data." + DISCL_M,
    ]))
    write('fingerprint-similarity', build('fingerprint-similarity', [
        "\U0001F4CC Fingerprint Similarity Evaluator",
        "Computes the similarity between a Chinese medicine fingerprint and a reference fingerprint (correlation coefficient / cosine of the angle)",
        "/ Fingerprint similarity",
        "Reference fingerprint (reference / common pattern)",
        "Sample 1 fingerprint",
        "Sample 2 fingerprint",
        "Sample 3 fingerprint",
        "Sample 4 fingerprint",
        "\U0001F4CC Compute the similarity",
        "\U0001F4DA In-depth analysis: fingerprint similarity evaluation",
        "Correlation coefficient",
        "Multi-batch consistency",
        "Similarity worked example",
        "Reference peak intensities [120,130,110,90] and sample [125,128,115,88]: pearson about 0.998 and cosine about 0.999, taking the larger score about 0.999 above 0.95 to judge them consistent.",
        "Abnormal batch",
        "Reference [120,130,110,90] and abnormal sample [80,60,55,40]: pearson about 0.21, clearly deviant, indicating a charging or process deviation.",
        "Which similarity should I use?",
        "Generally take the larger of pearson and cosine as the combined score, to avoid a single index being unstable.",
        "What is the pass threshold?",
        "TCM injections and extracts usually require similarity of 0.90 to 0.95 or above, depending on the pharmacopoeial standard.",
        "About the Fingerprint Similarity Evaluator",
        "Fingerprint similarity evaluator - computes Chinese medicine fingerprint similarity, supporting the correlation coefficient method and the cosine method." + DISCL_M,
        "Enter peak area data separated by commas or newlines\ne.g. 120,150,200,180,90,45,30",
        "Comma separated",
    ]))


if __name__ == '__main__':
    main()