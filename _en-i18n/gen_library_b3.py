#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'library')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'library')
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
    out = {'slug': slug, 'industry': 'library', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('shelf-capacity', build('shelf-capacity', [
        '🧊 Bookshelf Capacity Designer',
        'Compute single-shelf capacity, shelving length and required shelf count, assisting collection space planning',
        'Core calculation formula (by input variables): totalRowLen × (rowGap + 0.5); Math.ceil(shelfNeeded ÷ perRow); layerLen × 100',
        '/ Bookshelf Capacity Designer',
        '📖 View the User Guide for Bookshelf Capacity Designer',
        '📚 Deep Dive: Bookshelf Capacity Designer',
        'Library opening/expansion planning: for a new reading room, back-calculate required shelf count and layout from collection size; enter layers, layer length, book thickness and fill rate to compute per-shelf capacity and rows, estimating occupied area.',
        'Dense stack renovation: converting single-face shelves to double-face (faces=2) multiplies capacity; when layers and layer length are limited, use this tool to compare single/double-face plans and choose the most cost-effective layout.',
        'Estimating uneven book thickness: thickness varies greatly by category (reference books thick, journals thin); use average thickness and a fill rate (e.g. 90%) to leave margin, avoiding inability to fit after full shelving.',
        'Example: 6 layers · layer length 2 m · double-face · book thickness 3 cm · fill 90% · target 5000 books',
        'Books per layer = layer length (cm) × fill rate ÷ book thickness = 200×0.9÷3 = 60 books; per shelf = 60×6×2 (double-face) = 720 books; shelves needed = ceil(5000÷720) = 7; rows = ceil(7÷5) = 2 rows; total shelving length = shelves per row 5 × layer length 2 m × rows 2 = 20 m; aisle total length = 2×1.2 m = 2.4 m; estimated area = total shelving length 20 m × (aisle 1.2 m + estimated shelf depth 0.5 m) = 34.0 m².',
        'What fill rate is appropriate?',
        'Commonly 85%-95%; lower is safer but wastes space. Reference books and albums take lower values; ordinary books can take about 90%, leaving margin for spine thickness and shelving, avoiding inability to insert after full shelving.',
        'How to compute double-face shelves?',
        'Per-shelf capacity = books per layer × layers × faces; double-face has faces=2, about 2× a single-face shelf. Total shelving length = single-face layer length × shelves per row × rows; area is a rough estimate, and walls and end shelves must still be counted in practice.',
        'About the Bookshelf Capacity Designer',
    ]))
    write('stats-report', build('stats-report', [
        '📊 Statistics (Quantity/Type/Usage) Report',
        'Quantity/Type/Usage',
        'Enter total collection, annual loans, registered readers and visits; summarize utilization rate, turnover rate, per-capita loans and per-capita visits and other collection-usage report metrics for annual business statistics and collection development decisions. Utilization rate = loan copies ÷ collection copies × 100%; turnover rate = loan copies ÷ collection copies. Computation is done locally in the browser, no data uploaded to the server.',
        '/ Statistics (Quantity/Type/Usage) Report',
        '📖 View the User Guide for Statistics (Quantity/Type/Usage) Report',
        'Circulation rate = annual loan copies ÷ total collection copies × 100%; per-capita reader loans = annual loan copies ÷ registered readers; visit rate = annual visits ÷ registered readers; new-acquisition ratio = annual new collection ÷ total collection copies × 100%; book turnover days = 365 ÷ circulation rate; year-over-year change rate of each metric = (this-year value − last-year value) ÷ last-year value × 100%, used for horizontal and vertical comparison of collection use efficiency.',
        'Total collection copies',
        'Annual loan copies',
        'Registered readers',
        'Annual visits',
        'Annual new collection',
        'Generate statistics report',
        '📚 Deep Dive: Statistics (Quantity/Type/Usage) Report',
        'When taking inventory of archives or assets, enter ledger details to auto-summarize total items, quantities and ratios by type, generating a classification statistics report for verification.',
        'Compute utilization: utilization rate = used item-times ÷ total items × 100%, output by month or year, reflecting collection activity and usage structure.',
        'Cross-summarize by dimensions (year, type, custodian organization) to locate long-idle or high-frequency categories, assisting shelving and digitization priority decisions.',
        'Annual utilization rate calculation',
        'A fonds with total 1200 items, 360 used-times registered in a year, utilization rate = 360÷1200×100% = 30%. Split by type: document category 800 items used 300 times (37.5%), business category 400 items used 60 times (15%), showing the document category is used more frequently.',
        'How to compute utilization reasonably?',
        "Common approach: utilization rate = used item-times within the period ÷ total items × 100%. Note the numerator is 'item-times' (the same item counted repeatedly when used multiple times) and the denominator is 'item count'; they have different units and must be listed separately in the report to avoid misreading.",
        'Are type ratio and utilization the same thing?',
        "No. Type ratio = items of a type ÷ total items, reflecting collection structure; utilization reflects how frequently items are retrieved. Only combined can you judge 'which categories are many, which are used much'; looking at one alone leads to misjudgment.",
        'Archive Box Spine Label Print Format Generator',
        'Reference Format Converter (GB/T 7714)',
        'About the Statistics (Quantity/Type/Usage) Report',
        'Statistics (Quantity/Type/Usage) Report. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.',
    ]))

if __name__ == '__main__':
    main()
