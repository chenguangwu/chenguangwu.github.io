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
    write('showcase-monitor', build('showcase-monitor', [
        '⛅ Showcase Temperature & Humidity Monitor',
        'Look up temperature and humidity preservation standards for different artifact materials, and judge whether the showcase measured values meet them',
        'The Showcase Temperature & Humidity Monitor performs professional calculation and outputs results based on input parameters.',
        '/ Showcase Temperature & Humidity Monitor',
        '📖 View the User Guide for Showcase Temperature & Humidity Monitor',
        '📚 Deep Dive: Showcase Environment Monitoring',
        'Before artifacts enter storage / exhibition, look up the recommended temperature and humidity range by material (metal/ceramic/painting-calligraphy/silk/lacquer-wood, etc.), and verify whether the showcase measured temperature and humidity meet the standard.',
        'During daily monitoring, record daily temperature and humidity fluctuations and compare with material tolerance to judge whether dehumidification/humidification or temperature control equipment is needed, preventing metal corrosion, paper embrittlement and wood cracking.',
        'When an environment exceeds the limit and alarms, give targeted control advice (heat/cool, humidify/dehumidify) until it returns to the compliant range.',
        'Material environment compliance check example',
        'A painting-calligraphy exhibit recommends temperature 18~20℃, humidity 50~55%. Measured 19℃, 52% → both temperature and humidity fall in range, judged "compliant"; if measured 22℃, 45%, then temperature exceeds the 20℃ upper limit (judged non-compliant, advise cooling below 20℃), and humidity, though near the 50~55% lower bound, is low. Metal requires humidity <40% to prevent rust, painting-calligraphy requires 50~55% to prevent drying cracks; the two standards must not be mixed.',
        'Why do temperature and humidity differ so much by material?',
        'Materials differ in moisture absorption / thermal expansion: metal/leather fear damp (metal <40%, leather 50~60%), painting-calligraphy/silk fear dryness and light (50~55% and low illuminance), lacquer-wood-bamboo needs moisture (55~65%) to prevent cracking. Mixed storage neglects one for another; control must be by material in separate cases.',
        'Why control daily fluctuation too?',
        'Short-term drastic temperature and humidity fluctuations cause repeated material expansion/contraction, condensation and mold, harming artifacts more than mean deviation. The industry requires daily temperature fluctuation ≤±2~3℃, humidity ≤±5%, needing continuous monitoring rather than only instantaneous values.',
        'About the Showcase Temperature & Humidity Monitor',
    ]))
    write('timeline-viewer', build('timeline-viewer', [
        '📜 History Timeline',
        'View Chinese and foreign historical events along a timeline',
        'History Timeline',
        '/ History Timeline',
        '📖 View the User Guide for History Timeline',
        'Timeline conversion: sort events by year using the Gregorian calendar year as axis; years-ago = current year − event year; dynasty interval = start year to end year, overlap interval takes the intersection of the two intervals; BCE years participate in sorting as negatives, ensuring correct chronological order.',
        '📚 Deep Dive: History Timeline',
        'When reviewing for middle/high school history exams, sort Chinese and foreign major events by timeline, e.g. 221 BCE Qin unification, 476 fall of Western Rome, 1453 fall of Constantinople.',
        'For East-West comparison: place events of the same century in China and the world side by side, e.g. 18th-century Industrial Revolution vs Qing Kang-Qian golden age.',
        'When creating content or scheduling reports, sort events by year to generate a visualized timeline context.',
        'Events are stored structured as "year (negative for BCE) + title + brief", rendered sorted ascending by year; supports East-West comparison filtering. Internally sorted by integer years uniformly, BCE auto-precedes (221 BCE earlier than 202 BCE).',
        'Filtering "3rd century BCE" yields 221 BCE Qin unifying the six states, 202 BCE end of Chu-Han contention (Han founded); filtering "15th century" yields 1405 Zheng He first maritime voyage, 1453 Ottomans destroy Byzantium; filtering "19th century" yields 1840 Opium War, 1861 Self-Strengthening Movement, 1894 First Sino-Japanese War.',
        'What is the timeline data source?',
        'A publicly compiled list of common-sense major events, for building a study context, not an academic full set; for in-depth research, rely on authoritative general histories or historical sources.',
        'How to sort BCE years?',
        'Internally BCE is represented by negatives, the smaller the earlier (221 BCE earlier than 202 BCE), auto-preceded at render, no manual conversion needed.',
        'Can events be exported or customized?',
        'Currently read-only browsing; to customize the event list, export events to a spreadsheet for your own editing and visualization.',
        'Historical Calendar - Free online tool, online historical calendar | ToolBox Free Online Tools',
        'Dynasty Comparison - Free online tool, online dynasty comparison | ToolBox Free Online Tools',
        'About History Timeline',
        'History Timeline is an online tool in the history and humanities field. A history and humanities tool, helping query and learn historical and cultural knowledge.',
    ]))
    write('visitor-route', build('visitor-route', [
        '📐 Visitor Route Planner',
        'Based on Dijkstra shortest path algorithm, plan the visiting route among exhibition halls (shortest distance)',
        '/ Visitor Route Planner',
        '📖 View the User Guide for Visitor Route Planner',
        '📚 Deep Dive: Visitor Route Planning',
        'When designing in-museum circulation, treat halls as nodes and passages as weighted edges (distance/duration), use Dijkstra shortest path algorithm to plan the optimal visiting order from entrance to exit, reducing backtracking.',
        'Under flow-control / one-way visiting, adjust the path by passage weight, balancing visitor flow among halls and avoiding congested segments.',
        'For multi-target visiting (only key halls), set start/end and must-see nodes to quickly get the shortest connecting path and total distance.',
        'Shortest circulation planning example',
        'Hall A (entrance) →B passage 20 m, B→C 30 m, A→C direct 80 m. From A to C, Dijkstra compares A→C direct 80 m with A→B→C cumulative 20+30=50 m, yielding shortest path A→B→C, total distance 50 m (better than direct 80 m). Similarly, arrange the whole shortest route "entrance → bronze hall → ceramic hall → painting hall → jade hall → exit".',
        'Why is a detour sometimes shorter?',
        'Dijkstra finds the global shortest by edge weights (passage distance), not simply straight-line nearness; via a transit node the cumulative weight may be smaller (e.g. A→B→C=50m < direct 80m). Planning follows the algorithm result; intuition easily misjudges.',
        'Besides distance, what else can edge weights use?',
        'Edge weights can be set to travel time, congestion or energy use; the algorithm applies equally; to consider "must-visit key halls", set them as intermediate nodes and solve in segments then concatenate paths, getting a constrained shortest route.',
        'About the Visitor Route Planner',
    ]))

if __name__ == '__main__':
    main()
