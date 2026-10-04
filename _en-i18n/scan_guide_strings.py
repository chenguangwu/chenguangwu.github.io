#!/usr/bin/env python3
"""扫描全部指南页，统计正文中文文本节点串频次，为 i18n/guides/_common.json 提供高频固定文案。"""
import os, re, json
from html.parser import HTMLParser
from collections import Counter

GUIDES = 'guides'
OUT = '_en-i18n/guide_strings_freq.json'

CJK = re.compile(r'[㐀-鿿-〿-￯]')

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_skip = 0
        self.texts = []
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'noscript'):
            self.in_skip += 1
    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript') and self.in_skip > 0:
            self.in_skip -= 1
    def handle_data(self, data):
        if self.in_skip: return
        for chunk in re.split(r'\n|\r', data):
            t = chunk.strip()
            if t and CJK.search(t):
                self.texts.append(t)

def main():
    files = sorted(f for f in os.listdir(GUIDES)
                   if f.endswith('.html') and f != 'index.html' and not f.endswith('.en.html'))
    counter = Counter()
    per_guide = {}
    for f in files:
        with open(os.path.join(GUIDES, f), encoding='utf-8', errors='ignore') as fh:
            data = fh.read()
        p = TextExtractor()
        try:
            p.feed(data)
        except Exception:
            pass
        uniq = set(p.texts)
        per_guide[f] = sorted(uniq)
        counter.update(uniq)
    with open(OUT, 'w', encoding='utf-8') as out:
        json.dump({'total_guides': len(files), 'frequency': dict(counter.most_common()),
                   'per_guide': per_guide}, out, ensure_ascii=False, indent=1)
    top = counter.most_common(60)
    print('total guides:', len(files))
    print('unique strings:', len(counter))
    print('--- TOP 60 by frequency ---')
    for s, c in top:
        print(f'{c:5d}  {s}')

if __name__ == '__main__':
    main()
