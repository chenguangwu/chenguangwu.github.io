#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'printing')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'printing')
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
    out = {'slug': slug, 'industry': 'printing', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
# -*- coding: utf-8 -*-
def main():
    write('sheet-calc', build('sheet-calc', [
        '🧮 Print Sheet Count Calculator',
        'Compute print sheet count, paper usage and fold correspondence from total pages and format',
        '📖 Read the "Print Sheet Count Calculator User Guide"',
        'Full-sheet paper usage = sheets × copies × (1 + spoilage rate)',
        'Total pages',
        'Format (full sheet = ? pages)',
        '16 open (16 pages per full sheet)',
        '32 open (32 pages per full sheet)',
        '8 open (8 pages per full sheet)',
        '4 open (4 pages per full sheet)',
        'Folio (2 pages per full sheet)',
        '64 open (64 pages per full sheet)',
        'Print run (copies)',
        'Spoilage rate (%)',
        'Duplex printing',
        'Print sheets',
        '= total pages / open (single-sided); ÷ 2 for duplex',
        'Full-sheet paper usage',
        '= sheets × copies × (1 + spoilage rate)',
        'Open',
        ': how many parts a full sheet is cut into, e.g. 16 open means one full sheet yields 16 parts',
        'Note: real printing also involves nesting, bleed and binding method, so this tool gives basic estimates.',
        '📚 Deep dive: print sheet count calculation',
        'Before printing a book or periodical, estimate sheets per copy from total pages and open size, then compute full-sheet paper usage and reams, for pricing and paper preparation.',
        'Compare paper usage between single-sided and duplex: with duplex, sheets per copy halve, saving substantial paper.',
        'Include the spoilage rate (printing/binding loss) in quotes to avoid preparing paper to the net count and running short on reprint.',
        'Take "total pages 320, 16 open, 2,000 copies, 8% spoilage, duplex printing" as an example',
        'Sheets per copy = pages/(open × duplex factor) = 320/(16×2) = 10 sheets. Full-sheet paper usage = 10×2000×(1+8%) = 21,600 full sheets; reams = 21,600/500 = 43.2 reams (1 ream = 500 full sheets). Switching to single-sided gives 20 sheets per copy and 43,200 full sheets = 86.4 reams, doubling paper use. Here 320 pages divides evenly by 16×2=32 for a whole sheet count; when real page counts do not divide evenly, round up or keep the remainder.',
        'Why divide sheets by open size and the duplex factor?',
        'One full sheet yields "open" pages after folding and cutting; duplex printing prints both sides, so sheets per copy = total pages/(open×2). For example 16 open duplex gives 32 pages per full sheet, so 320 pages needs 10 full sheets. Single-sided gives only 16 pages per full sheet.',
        'What is the ream unit?',
        'A paper measurement unit where 1 ream = 500 full sheets (some specialty paper uses 1000 sheets per ream, so confirm the supplier convention). On a quote, ream price × reams gives paper cost, and the spoilage rate covers loss.',
        'About "Print Sheet Count Calculator"',
        'The Print Sheet Count Calculator computes sheets per copy, full-sheet paper usage and reams from total pages, format, print run and spoilage rate, with single-sided and duplex switching.',
        'Quick format presets',
        'Automatic single/duplex conversion',
        'Spoilage rate counted automatically',
        'Book and periodical paper estimation',
        'Prepress cost accounting',
        'Paper purchasing plan',
        'Printing process planning',
    ]))


if __name__ == '__main__':
    main()
