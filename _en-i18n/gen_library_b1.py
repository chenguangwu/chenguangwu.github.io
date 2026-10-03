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
    write('archive-label', build('archive-label', [
        '✨ Archive Box Label Generator',
        'Generate archive box spine labels with vertical layout, supporting print (A4 paper recommended)',
        '/ Archive Box Label Generator',
        '📖 View the User Guide for Archive Box Label Generator',
        'The archival number follows the Archival Number Compilation Rules, composed of fonds number + catalog number + file number (e.g. A01-2024-WS-001); label area height = spine height × (1 − 8% top and bottom margins); vertical font size = label area width ÷ (longest field length + 2), with even letter spacing; rows per A4 page = floor(usable height ÷ single label height), labels per row = floor(usable width ÷ single label width); crop marks expand 1 to 2 mm beyond the label size for easy cutting and shelving.',
        '📚 Deep Dive: Archive Box Label Generator',
        'Document archives filing: an agency organizes its annual document archives; fonds number X043, catalog number 001, box number 012, year 2023, retention period "permanent", organization "Office", title "Annual Work Summary and Meeting Minutes", start-end item numbers 001-085, archiving unit "XX City Archives"; one-click generate standard archival number and box-face label.',
        'Project archive box spine printing: in engineering projects, file by project; print the archival number, title, year, retention period and start-end item numbers on the spine for easy shelving and retrieval; this tool assembles scattered fields into standard label text, avoiding manual copy errors.',
        'Batch transfer and inventory: when transferring archives, count by box with consecutive box numbers (e.g. 012-020); use this tool to generate labels box by box, ensuring consecutive archival numbers and complete elements for handover and later retrieval.',
        'Example: generate a standard archive box label',
        'Input: fonds number=X043, catalog number=001, box number=012, year=2023, retention period=permanent, organization/issue=Office, title=Annual Work Summary and Meeting Minutes, start-end item numbers=001-085, archiving unit=XX City Archives. | Archival number = fonds number-catalog number-box number = X043-001-012; box face shows "Archival number X043-001-012 | Title Annual Work Summary and Meeting Minutes | 2023 · Permanent | Office · Item numbers 001-085". The copied text includes seven elements: archival number, title, year, retention period, organization/issue, start-end item numbers and archiving unit, ready to paste into a label printing template.',
        'How are the parts of the archival number arranged?',
        'Archival number = fonds number-catalog number-box number, joined by hyphens. The fonds number is the unique code of the archiving unit; the catalog number distinguishes record categories (e.g. documents, accounting, projects); the box number is the sequential loading number within the box; together they uniquely identify one box of archives within a fonds.',
        'What retention periods are available?',
        'Per the Document Archive Retention Period Table, there are three tiers: "permanent", "fixed 30 years" and "fixed 10 years". Fixed-term archives must be appraised before expiry, then destroyed or extended; both the box face and the retrieval field should be marked truthfully for due disposal.',
        'About the Archive Box Label Generator',
    ]))
    write('citation-format', build('citation-format', [
        '🏋️ Reference Format Converter',
        'Generate reference citation formats per GB/T 7714-2015, supporting multiple document types',
        '/ Reference Format Converter',
        '📖 View the User Guide for Reference Format Converter',
        '📚 Deep Dive: Reference Format Converter',
        'Academic paper reference citation: journals require GB/T 7714 format; one-click convert mixed bibliographies of books, journal articles and theses into standard citations, avoiding manual layout errors and inconsistent punctuation.',
        'Graduation thesis reference list: graduate students number each reference by the "sequential coding system"; the tool auto-adds type identifiers ([M]/[J]/[D]/[C]…) by document type, generating a paste-ready list.',
        'Cross-type document unification: a single paper may cite standards [S], patents [P], web [EB/OL] and newspapers [N]; the tool applies templates by type, keeping identifiers and punctuation consistent.',
        'Example: output for book and journal types',
        'Select "Book": authors Zhang San, Li Si | title Introduction to Data Mining | edition 2 | place Beijing | publisher China Machine Press | year 2021 | pages 100-150 → [1] Zhang San, Li Si. Introduction to Data Mining[M]. 2nd ed. Beijing: China Machine Press, 2021:100-150. | Select "Journal": author Wang Wu | title Survey of Recommender Systems | journal Journal of Library Science in China | year,vol(issue) 2023,49(3) | pages 12-18 → [1] Wang Wu. Survey of Recommender Systems[J]. Journal of Library Science in China, 2023,49(3):12-18.',
        'What are the document type identifiers?',
        'Common ones: monograph [M], journal [J], thesis [D], conference [C], report [R], standard [S], patent [P], newspaper [N], electronic bulletin [EB/OL]; they must match the actual carrier type, as wrong identifiers make the citation non-standard.',
        'How to handle multiple authors?',
        'GB/T 7714 states: list all authors if 3 or fewer; if more than 3, list the first 3 then add "et al."; this tool collects authors line by line and formats per this rule, with foreign authors surname-first.',
        'About the Reference Format Converter',
    ]))
    write('clc-classifier', build('clc-classifier', [
        '📚 CLC Classification Number Generator',
        'China Library Classification (CLC) lookup: enter a subject keyword to match a classification number',
        '/ CLC Classification Number Generator',
        '📖 View the User Guide for CLC Classification Number Generator',
        '📚 Deep Dive: CLC Classification Number Generator',
        'Cataloger class lookup: for new arrivals, locate the top class among 22 basic categories (A Marxism → Z General works) by subject, then drill down to secondary categories to get a class number like "TP3 Computing technology".',
        'Call number completion: after getting the class number, you still need to add the author number/copy number to shelve; this tool suggests additional rules (e.g. TP3/123 or TP3/W285) to write the call number directly.',
        'Subject search aid: readers search with keywords (e.g. "Psychology"); the tool fuzzy-matches within category names and class numbers, returning candidate categories to quickly locate the shelf area.',
        'Example: locate class numbers by searching "Computer" and "Psychology"',
        'Search "Computer": hits T Industrial technology → TP Automation, computer technology → TP3 Computing technology, computer technology; after selecting TP3, the call number is suggested as TP3/123 (copy number) or TP3/W285 (author number, W from the pinyin initial of "Wang"). | Search "Psychology": hits B Philosophy, religion → B84 Psychology. Call number = class number + author number/copy number, the actual basis for shelving and finding books.',
        'How many basic categories does CLC have?',
        'The China Library Classification has 22 basic categories, denoted by letters (A-Z, excluding I, O, U, V, W, X, Y): A Marxism-Leninism, B Philosophy-religion, C Social sciences general, D Politics-law, T Industrial technology (TP Computers) … Z General works. Each major class further divides into secondary and tertiary categories.',
        'What is the difference between a class number and a call number?',
        'A class number (e.g. TP3) only indicates subject membership; a call number = class number + author number/copy number (e.g. TP3/123), used to uniquely identify one book among the same class, and is the actual basis for shelving and finding books.',
        'About the CLC Classification Number Generator',
        'Enter a subject term to search classification',
    ]))

if __name__ == '__main__':
    main()
