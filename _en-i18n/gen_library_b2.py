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
    write('generator-label', build('generator-label', [
        '✨ Archive Box Spine Label Print Format Generator',
        'Online tool for generating archive box spine label print formats',
        'Archive Box Spine Label Print Format Generator',
        '/ Archive Box Spine Label Print Format Generator',
        '📖 View the User Guide for Archive Box Spine Label Print Format Generator',
        'Based on archive box specs and spine character count, generate batch-printable spine label layouts from fields like fonds number, year, organization, start-end item numbers and box number; font size auto-adjusts with box thickness (30/40/50 mm). Results can be copied directly for use, and data never leaves the browser.',
        '📚 Deep Dive: Archive Box Spine Label Print Format Generator',
        'Per the DA/T archive arrangement rules, mark fonds number, year, organization (or issue), start-end item numbers and box number on the spine, generating a batch-printable spine label format.',
        'When archiving, set font size and characters per line by spine thickness (common 30 mm/40 mm/50 mm) to keep labels centered on the spine without misalignment.',
        'Before transfer and lending, verify spine info: consecutive box numbers and start-end item numbers matching the in-box file list, to avoid wrong or missing boxes.',
        'A standard spine label',
        'Fonds number A032, year 2024, organization Office, start-end item numbers 0001-0150, box number 012. The generated format is laid out for 30 mm spine thickness: row 1 fonds number, row 2 year, row 3 organization, row 4 start-end item numbers, row 5 box number; font size auto-shrinks with row count to stay readable.',
        'Which fields are usually printed on the spine?',
        'Per archive industry standards, the spine is usually marked top-to-bottom: fonds number, year, organization (or issue), start-end item numbers, box number. The exact fields and order follow your unit’s Archive Scope and Arrangement Rules.',
        'How does different spine thickness affect the result?',
        'Spine thickness (30/40/50 mm etc.) determines printable row height and font size. Greater thickness allows more fields and larger font; too dense makes printing hard to read. It is recommended to choose a template by actual box type before batch printing.',
        'Reference Format Converter (GB/T 7714)',
        'About the Archive Box Spine Label Print Format Generator',
        'Archive Box Spine Label Print Format Generator. A free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.',
    ]))
    write('index', build('index', [
        '📚 Library & Archive Tools',
        'Library & Archive',
        'Library & Archive Tools',
        'Generate reference citation formats per GB/T 7714-2015, supporting multiple document types',
        'Enter the due date, actual return date and daily rate to compute overdue days and fine; supports fixed or tiered rates (higher the longer) and a per-book fine cap, suitable for librarians or readers to check.',
        'Generate archive box spine labels per the Archival Number Compilation Rules, supporting vertical layout of fields like archival number, title and year; print directly on A4 paper and cut for use, easing neat shelving and retrieval in archive cabinets.',
        'Archive Box Spine Label Print Format Generator',
        'Based on archive box specs and spine character count, generate batch-printable spine label layouts from fields like fonds number, year, organization, start-end item numbers and box number; font size auto-adjusts with box thickness (30/40/50 mm). Results can be copied directly for use, data never leaves the browser.',
        'CLC Classification Number Generator',
        'Enter a book or subject keyword to match the corresponding class number and class name in the China Library Classification (CLC), and list related superordinate and subordinate categories, assisting book cataloging and classified shelving.',
        'Bookshelf Capacity Designer',
        'Enter shelf layers, layer length, average book thickness and fill rate to compute books per shelf, and estimate shelves needed, total shelving length and occupied area, assisting library space planning and procurement estimates.',
        'The Statistics (Quantity/Type/Usage) Report is a free online library & archive tool, the Statistics (Quantity/Type/Usage) Report. A free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected. Runs purely front-end, no data upload, no registration, ready to use by opening the browser.',
        'About Library & Archive Tools',
        'The Library & Archive Tools collection includes 7 free online tools covering common calculation, conversion and lookup needs in library and archive scenarios. Whether you are a practitioner, student or ordinary user in the field, you can find ready-to-use small tools here. All tools run purely front-end, no data uploaded to the server, protecting your privacy and security.',
        'The library & archive tools on this page include (representative selection):',
        'These tools help you quickly complete common library and archive tasks without memorizing complex formulas or manual conversion; just enter to get results.',
        'Do the library & archive tools need to be downloaded or registered?',
        'No. All library & archive tools on this page are pure front-end online tools; open the page to use directly, no software install, no account registration, no data upload.',
        'Are the library & archive tool results accurate? Is the data safe?',
        'The tools compute locally in your browser based on public math formulas and general industry standards, with results instantly available. All computation is done locally on your device; data is never uploaded to the server, and your privacy and security are protected.',
    ]))
    write('overdue-fine', build('overdue-fine', [
        '🧮 Overdue Borrowing Fine Calculator',
        'Compute overdue days and fines for book borrowing, supporting tiered rates and fine caps',
        'Core calculation formula (by input variables): d1 × dailyFine + d2 × dailyFine × 1.5 + d3 × dailyFine × 2; min(max(overdueDays - 7, 0), 23); max(overdueDays - 30, 0)',
        '/ Overdue Borrowing Fine Calculator',
        '📖 View the User Guide for Overdue Borrowing Fine Calculator',
        'Enable tiered rate',
        'Enable fine cap',
        '📚 Deep Dive: Overdue Borrowing Fine Calculator',
        'Library reader overdue fines: readers who fail to return books on time are fined per day; enabling a tiered rate (first 7 days base, days 8-30 at 1.5×, over 30 days at 2×) deters long-term hoarding; librarians enter borrow/return dates to auto-issue a fine.',
        'Internal borrowing accounting in a resource room: a corporate resource room sets a cap (e.g. max 5 CNY per book) on cross-department borrowed drawings and bids to avoid high fines from long loans, using the "cap" switch to bound the per-book maximum.',
        'Multiple books overdue at once: a reader borrows several books and they are all overdue on the same day; sum by count; this tool multiplies "overdue count" by the per-book fine to get the total payable, easing a combined fine notice.',
        'Example: 40 days overdue · 0.5 CNY/day · 2 books · tiered (uncapped)',
        'Breakdown: first 7 days 7×0.5 = 3.5 CNY; days 8-30, 23 days ×0.5×1.5 = 17.25 CNY; from day 31, 10 days ×0.5×2 = 10 CNY. Per book total 3.5+17.25+10 = 30.75 CNY; 2 books total 61.50 CNY. | Comparison: if a 50 CNY/book cap is used, the per-book cap is 50 CNY, total 100 CNY (this example does not hit the cap). Without tiering, per book = 40×0.5 = 20 CNY, total 40 CNY.',
        'How is the tiered rate segmented?',
        'First 7 days at base daily rate; days 8-30 at 1.5×; from day 31 at 2×. The three segments do not overlap and accumulate continuously; overdue days fall into their respective intervals and sum, with no double charging.',
        'How to use the cap (upper limit)?',
        'Check "Enable cap" and fill the limit; when a per-book fine exceeds the limit, charge the limit instead and stop accumulating; suitable for internal resource-room borrowing where high fines are undesired.',
        'About the Overdue Borrowing Fine Calculator',
    ]))
    write('convert-ref-cite', build('convert-ref-cite', [
    ]))

if __name__ == '__main__':
    main()
