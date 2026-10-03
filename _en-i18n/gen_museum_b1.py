#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'museum')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'museum')
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
    out = {'slug': slug, 'industry': 'museum', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('audio-guide-timer', build('audio-guide-timer', [
        '⏱️ Audio Guide Duration Matcher',
        'Compute total audio-guide narration duration, matching exhibit count with visitor available time',
        'The Audio Guide Duration Matcher performs professional calculation and outputs results based on input parameters.',
        '/ Audio Guide Duration Matcher',
        '📖 View the User Guide for Audio Guide Duration Matcher',
        'Quick estimate',
        'Per-exhibit detail',
        '📚 Deep Dive: Audio Guide Duration Planning',
        'When scheduling group tours, estimate total duration from exhibit count, per-exhibit narration time, movement and opening/closing time; judge whether it fits the available time and give trade-off suggestions.',
        'In personalized tours (per-exhibit duration), list each exhibit time share and cumulative time, comparing with available time to identify over-time segments.',
        'For overtime emergencies, give three adjustment paths: shorten per-exhibit narration, reduce exhibit count, or compress movement time, keeping the overall group pace.',
        'Group tour duration accounting example',
        'A team with 5 exhibits, 120 sec per exhibit narration, 30 sec movement per segment, 60 sec opening/closing, 20 min available. Total duration = 5×120 + 4×30 + 60 = 780 sec (13 min); available 20×60 = 1200 sec; time margin +420 sec (7 min surplus); per-exhibit available floor(1200÷5) = 240 sec. Per-exhibit scenario: bronze ding 120 / bianzhong 150 / jade bi disc 90 / pottery figurine 100 / gold-silver ware 110, total 570 sec; with 10 min (600 sec) available only 30 sec remain, so per-exhibit must be compressed or exhibits reduced.',
        'What to do if overtime?',
        'The tool gives three options: 1) shorten per-exhibit narration to floor((per-exhibit × available − movement − opening) ÷ count) sec; 2) reduce explained exhibits to floor((available − opening) ÷ (per-exhibit + movement)) pieces; 3) compress movement time. Prioritize cutting redundant exhibits and movement gaps, keeping key halls.',
        'How to use the average per-exhibit duration?',
        'Per-exhibit available = floor(available sec ÷ exhibit count), used to quickly judge whether the current per-exhibit setting exceeds the limit; if one far exceeds the average, prioritize compressing it. The per-exhibit view also shows each item share and cumulative time, easing precise trimming.',
        'About the Audio Guide Duration Matcher',
    ]))
    write('era-comparator', build('era-comparator', [
        '📜 Dynasty Comparison',
        'Compare the basic information of two dynasties/periods to understand historical development',
        'Dynasty Comparison',
        '/ Dynasty Comparison',
        '📖 View the User Guide for Dynasty Comparison',
        'Dynasty comparison basis: duration = end year − start year; synchronous comparison uses the Gregorian calendar year as axis, marking each dynasty start order and overlap interval; the span can be converted to the ratio of China recorded history length (about 2070 BCE to present, about 4100 years) for horizontal quantitative comparison.',
        '📚 Deep Dive: Dynasty Comparison',
        'Quickly verify the start/end eras and durations of two dynasties when preparing lessons or homework, e.g. Tang 618–907 (289 years), Ming 1368–1644 (276 years).',
        'Compare coexisting regimes in divided periods: select "Three Kingdoms (220–280)" and "Jin (266–420)", the tool computes a 14-year overlap (266–280) of the two regimes.',
        'When making a timeline or comparison table, take fields like founding monarch, capital, territory and population directly, avoiding flipping through chronologies one by one.',
        'Duration = end year − start year; coexistence period = later dynasty start year − earlier dynasty end year (positive means overlap exists). BCE years are represented as negatives, e.g. Xia dynasty starts at −2070 (i.e. 2070 BCE).',
        'Tang (618–907, 289 years) vs Ming (1368–1644, 276 years): no time overlap, duration difference 13 years. If Zhou (−1046–−256, 790 years) vs Qin (−221–−206, 15 years): Zhou ends at −256 earlier than Qin starts at −221, no overlap, Zhou is 775 years longer than Qin. If Three Kingdoms (220–280) vs Jin (266–420): overlap 266–280 totals 14 years.',
        'Why are dynasty start/end years often marked "approximate"?',
        'Early dynasties (Xia, Shang, Zhou) dates are mostly inferred from documents and the Xia-Shang-Zhou Chronology Project, with academic ranges; after Qin the chronology is more certain, but divided periods (Three Kingdoms, Northern and Southern Dynasties) take regime founding or unification as the boundary, and different general histories may differ.',
        'How to understand "coexistence period"?',
        'When the two selected dynasties timelines intersect, the overlap years are shown, mainly for divided periods, e.g. Wei-Shu-Wu and early Western Jin, Northern and Southern Dynasties and surrounding regimes. Unified dynasties generally do not overlap.',
        'Why do the tool and history books years differ?',
        'This tool follows a single authoritative chronology (including Chronology Project values); different textbooks or general histories may round or adopt alternative accounts, which is a normal difference; when citing, follow the convention of the textbook you use.',
        'History Timeline - Free quick-reference tool, online history timeline | ToolBox Free Online Tools',
        'Historical Calendar - Free online tool, online historical calendar | ToolBox Free Online Tools',
        'About Dynasty Comparison',
        'Dynasty Comparison. A history and humanities tool, helping query and learn historical and cultural knowledge.',
    ]))
    write('exhibit-spacing', build('exhibit-spacing', [
        '📏 Exhibit Spacing Designer',
        'Compute recommended viewing distance and exhibit spacing from exhibit size and optimal viewing angle',
        'Core calculation formula (by input variables): (|(dEye)| + h÷2) ÷ Math.tan(va × π ÷ 180); (w÷2) ÷ Math.tan(ha × π ÷ 180); min(360 ÷ (recSpacing×2 + 40), 1)',
        '/ Exhibit Spacing Designer',
        '📖 View the User Guide for Exhibit Spacing Designer',
        '📚 Deep Dive: Exhibit Spacing and Viewing Distance',
        'When designing exhibition lines/layout, estimate optimal and minimum viewing distance from exhibit size and set viewing angle (30° horizontal half-angle / 15° vertical half-angle), avoiding too close to see incompletely or too far to see clearly.',
        'When arranging a single-sided display wall, estimate exhibits per meter by recommended spacing, planning exhibition-line length and display density.',
        'For two people side by side or large exhibits, increase spacing and retreat distance to prevent adjacent exhibits from interfering with each other viewing or blocking sightlines.',
        'Viewing distance and spacing calculation example',
        'A painting width 50 cm, height 70 cm, center height 160 cm, horizontal half-angle 30°, vertical half-angle 15°, eye height 150 cm, 1 viewer. Horizontal distance = 25÷tan30° ≈ 43.3 cm; vertical distance = (|160−150|+35)÷tan15° ≈ 167.9 cm; optimal viewing distance = max = 167.9 cm; minimum distance = √(50²+70²)×0.6 ≈ 51.6 cm; recommended spacing = max(50+60×0.8, 50×1.5) = 98 cm; about 1 piece per meter.',
        'How to set horizontal/vertical half-angles?',
        'Empirical optimal horizontal viewing angle about 30° (half-angle), vertical about 15°; large-format or detail-reading exhibits can increase the half-angle (shorten distance); sculptures/3D exhibits should increase retreat distance and spacing. The optimal distance takes the larger of horizontal and vertical, ensuring the whole piece is within a comfortable viewing angle.',
        'Why does recommended spacing take the larger value?',
        'Spacing must accommodate both exhibit width and viewer standing position (shoulder width × side-by-side count × 0.8 passage margin), and be no less than 1.5× the painting width, preventing adjacent exhibits from overlapping viewing and interfering. Larger spacing fits fewer per wall, a trade-off between display density and viewing comfort.',
        'About the Exhibit Spacing Designer',
    ]))

if __name__ == '__main__':
    main()
