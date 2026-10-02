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
    write('compatibility-taboo', build('compatibility-taboo', [
        "\U0001F48A Incompatibility (Physicochemical) Detector",
        "Detects classic TCM compatibility taboos (eighteen antagonisms and nineteen fears) as well as physicochemical incompatibilities",
        "/ Compatibility taboo detection",
        "Classic compatibility taboos",
        "Physicochemical compatibility taboos",
        "Quick reference",
        "Medicine A",
        "Medicine B",
        "\U0001F48A Detect taboos",
        "Acidity/basicity of constituent A",
        "Acidic (such as organic acids)",
        "Alkaline (such as alkaloids)",
        "Contains tannins",
        "Contains protein / amino acids",
        "Contains glycosides",
        "Contains flavonoids",
        "Contains metal ions",
        "Acidity/basicity of constituent B",
        "Solubility of constituent A",
        "Lipophilic",
        "Amphiphilic",
        "pH of the compatibility environment",
        "\U0001F9EA Physicochemical analysis",
        "Eighteen antagonisms",
        "Licorice antagonizes:",
        "Kansui, Beijing daiji, zexie and yuanhua",
        "Aconite antagonizes (chuanwu, caowu, fuzi):",
        "Banxia, Gualou, beimu (chuanbei, zhebei), bailian and baiji",
        "Lilu antagonizes:",
        "Ginseng, dangshen, glehnia (beishashen, nanshashen), danshen, xuanshen, kushen, xixin and shaoyao (baishao, chishao)",
        "Nineteen fears",
        "Sulfur fears mirabilite, mercury fears arsenic, wolf poison fears litharge",
        "Croton fears morning glory, clove fears turmeric, chuanwu/caowu fears rhino horn",
        "Yaoxiao fears sanleng, official cinnamon fears fluorite, ginseng fears wulingzhi",
        "Pregnancy contraindications",
        "Prohibited:",
        "Croton, morning glory seed, daiji, shanglu, musk, sanleng, ezhu, leech, gadfly, blistering beetle, realgar and qingfen",
        "Use with caution:",
        "Safflower, peach kernel, niuxi, chuanxiong, fuzi, dried ginger, cinnamon, banxia, arisaema and mirabilite",
        "Common physicochemical compatibility taboos",
        "Type of constituent A",
        "Type of constituent B",
        "Taboo result",
        "Example",
        "Precipitation",
        "Coptis + gallnut",
        "Acidic constituent",
        "Salt formation / precipitation",
        "Coptis + hawthorn",
        "Coagulating precipitation",
        "Trichosanthes root + sanguisorba",
        "Metal ions (Fe3+/Al3+)",
        "Complexation and color change",
        "Scutellaria + pyrite",
        "Glycoside",
        "Strong acid / strong alkali",
        "Hydrolysis and loss of activity",
        "Ginseng + smoked plum",
        "Organic acid",
        "Metal ion (Ca2+)",
        "Hawthorn + gypsum",
        "\U0001F4DA In-depth analysis: compatibility (physicochemical) taboo detection",
        "Acid-base / glycoside reactions",
        "Licorice + kansui, zexie, daiji and yuanhua falls under \"zexie, daiji, sui, yuanhua all fight gancao\"; chuanwu or fuzi + banxia, Gualou or beimu falls under aconite antagonizing banxia, Gualou and beimu; lilu antagonizes ginseng, danshen, kushen and similar.",
        "Physicochemical reactions",
        "Alkaloids (alkaline) form water-soluble salts below pH 4 and precipitate as free bases above pH 9; tannins (such as gallnut) readily complex and precipitate with alkaline constituents, so co-decocting them should be avoided.",
        "Can the eighteen antagonisms share a formula?",
        "They are traditional taboos, and modern research has evidence of increased toxicity in some cases, so clinical formulas usually avoid co-decocting them.",
        "How does pH affect it?",
        "Alkaloids are alkaline, while glycosides hydrolyze or precipitate at extreme acid or alkaline values, so the environmental pH must be considered in compatibility.",
        "About the Incompatibility (Physicochemical) Detector",
        "Incompatibility physicochemical detector - detects the eighteen antagonisms and nineteen fears of TCM and analyzes physicochemical compatibility taboos." + DISCL_M,
    ]))


if __name__ == '__main__':
    main()