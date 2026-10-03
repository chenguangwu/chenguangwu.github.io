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
    write('historical-calendar', build('historical-calendar', [
        '📅 Historical Calendar',
        'Convert Gregorian dates to lunar calendar, sexagenary (ganzhi) year, zodiac and solar terms, and view historical events',
        'Historical Calendar',
        '/ Historical Calendar',
        '📖 View the User Guide for Historical Calendar',
        '📅 Calendar view',
        'Previous month',
        'Next month',
        '🌙 Details',
        '📌 Historical events',
        '📚 Deep Dive: Historical Calendar',
        'Look up the lunar date, zodiac and ganzhi of a Gregorian birthday, e.g. 2000-01-01 → lunar Ji-Mao year, 25th day of 11th month, zodiac Rabbit, ganzhi Ji-Mao.',
        'When studying traditional culture or creating content, look up representative "On This Day" events and the solar term the day belongs to.',
        'Quickly convert solar term dates, e.g. 2024-06-21 is Summer Solstice, 2024-02-04 is Beginning of Spring.',
        'Ganzhi = heavenly stem (take "year−4" mod 10) + earthly branch (take "year−4" mod 12); zodiac = (year−4) mod 12 (0=Rat…11=Pig); the lunar calendar is derived from the built-in LUNAR_INFO new-moon table for large/small months and leap months, covering about 1900–2100.',
        '2024-02-10 → lunar Jia-Chen year, 1st day of 1st month (Spring Festival), zodiac Dragon, ganzhi Jia-Chen; this day is after Beginning of Spring (2024-02-04), so by the traditional zodiac convention it is Dragon. 2000-01-01: year−4=1996, 1996 mod 10=6 → heavenly stem "Ji", 1996 mod 12=4 → earthly branch "Mao", hence Ji-Mao year, zodiac Rabbit.',
        'Lunar conversion',
        'Why is there a year limit?',
        'The built-in LUNAR_INFO only contains new-moon data for about 1900–2100; dates outside the range cannot be converted; for earlier or later, please use a professional tool.',
        'By which "year" are ganzhi and zodiac calculated?',
        'Traditional metaphysics takes "Beginning of Spring" as the boundary: those born before it count as the previous year ganzhi. This tool uses the Gregorian year rounded (simplified convention); for a strict metaphysical convention, adjust by the Beginning of Spring boundary yourself.',
        'Are the "On This Day" events complete?',
        'Only some publicly compiled representative events are included, not exhaustive; for rigorous research, rely on authoritative historical sources or professional history databases.',
        'History Timeline - Free online tool, online history timeline | ToolBox Free Online Tools',
        'Dynasty Comparison - Free online tool, online dynasty comparison | ToolBox Free Online Tools',
        'About Historical Calendar',
        'Historical Calendar is an online tool in the history and humanities field. A history and humanities tool, helping query and learn historical and cultural knowledge.',
    ]))
    write('index', build('index', [
        '🏛️ Museum Exhibition Tools',
        'Museum Exhibition',
        'Museum Exhibition Tools',
        'Compute illuminance (lux) from light source luminous flux, distance and showcase area, and check against artifact illuminance limits for compliance, giving adjustment advice if exceeded.',
        'Dynasty Comparison',
        'Dynasty Comparison is a free online museum exhibition tool, Dynasty Comparison. A history and humanities tool, helping query and learn historical and cultural knowledge. Runs purely front-end, no data upload, no registration, ready to use by opening the browser.',
        'Enter exhibit count and each exhibit narration duration (or quick-estimate by average duration) to compute total audio-guide duration and match visitor available time; if exceeded, give trimming or speed-up adjustment plans. For museum curation and tour scheduling.',
        'Historical Calendar',
        'Historical Calendar is a free online museum exhibition tool, Historical Calendar is an online tool in the history and humanities field. A history and humanities tool, helping query and learn historical and cultural knowledge. Runs purely front-end, no data upload, no registration, ready to use by opening the browser.',
        'Enter exhibit size and recommended optimal viewing angle (or viewing-distance coefficient) to compute the optimal viewing distance between viewers and exhibits and reasonable spacing between adjacent exhibits. For gallery floor planning, avoiding crowds and ensuring viewing experience.',
        'Based on Dijkstra shortest path algorithm, plan the shortest visiting route among multiple halls, suitable for museum guides and route optimization.',
        'History Timeline',
        'History Timeline is a free online museum exhibition tool, History Timeline is an online tool in the history and humanities field. A history and humanities tool, helping query and learn historical and cultural knowledge. Runs purely front-end, no data upload, no registration, ready to use by opening the browser.',
        'Select artifact material (metal, ceramic, painting-calligraphy, silk, lacquer-wood, etc.), enter the showcase measured temperature and humidity, check against preservation standards for compliance and give control advice. For museum collection environment monitoring and preventive conservation.',
        'About Museum Exhibition Tools',
        'The Museum Exhibition Tools collection includes 8 free online tools covering common calculation, conversion and lookup needs in museum exhibition scenarios. Whether you are a practitioner, student or ordinary user in the field, you can find ready-to-use small tools here. All tools run purely front-end, no data uploaded to the server, protecting your privacy and security.',
        'The museum exhibition tools on this page include (representative selection):',
        'These tools help you quickly complete common museum exhibition tasks without memorizing complex formulas or manual conversion; just enter to get results.',
        'Do the museum exhibition tools need to be downloaded or registered?',
        'No. All museum exhibition tools on this page are pure front-end online tools; open the page to use directly, no software install, no account registration, no data upload.',
        'Are the museum exhibition tool results accurate? Is the data safe?',
        'The tools compute locally in your browser based on public math formulas and general industry standards, with results instantly available. All computation is done locally on your device; data is never uploaded to the server, and your privacy and security are protected.',
    ]))
    write('lighting-lux', build('lighting-lux', [
        '🧮 Showcase Illuminance Calculator',
        'Compute illuminance (lux) from light source luminous flux, distance and showcase area, and check artifact illuminance limits',
        'Core calculation formula (by input variables): 2 × π × (1 - Math.cos(halfBeam)); 2 × dist × Math.tan(halfBeam); beam ÷ 2 × π ÷ 180',
        '/ Showcase Illuminance Calculator',
        '📖 View the User Guide for Showcase Illuminance Calculator',
        '📚 Deep Dive: Showcase Illuminance Calculator',
        'When laying out showcase lighting, estimate total effective luminous flux from fixture count, luminous flux, utilization factor and glass transmittance; use the average illuminance method E=Φ/A to assess whether the exhibit illuminance limit is exceeded.',
        'For accent lighting design (spotlights), use point-source center illuminance E=I/d² and spot diameter to evaluate the lighting effect, avoiding local overexposure or too-small spots.',
        'For graded-sensitive exhibits (paintings/silk highly sensitive), check against GB/T 23863-2009 limits (highly sensitive 50 lx, low/medium sensitive 150 lx, insensitive 300 lx); dim or add filters if necessary.',
        'Showcase illuminance compliance check example',
        'A showcase with 4 LED lamps (500 lm each,',
        'Beam angle',
        '36°, utilization factor 0.7), glass transmittance 100%, area 10 m², distance to exhibit 2 m, highly sensitive (limit 50 lx). Total effective luminous flux = 4×500×0.7×1.0 = 1400 lm; average illuminance = 1400÷10 = 140 lx; solid angle = 2π(1−cos18°) ≈ 0.307 sr, single-lamp intensity ≈ 350÷0.307 ≈ 1138 cd, center illuminance ≈ 1138÷4×4 ≈ 1138 lx; spot diameter = 2×2×tan18° ≈ 1.30 m. Conclusion: average 140 lx far exceeds the highly sensitive 50 lx, must dim (replace with lower-lumen source / dimming / add filter).',
        'What standard are the illuminance limits based on?',
        'Per GB/T 23863-2009 Museum Lighting Design Code: highly sensitive exhibits (paintings, silk, etc.) ≤50 lx and annual light exposure ≤150,000 lx·h; low/medium sensitive ≤150 lx; insensitive ≤300 lx. Lighting must match the exhibit sensitivity.',
        'Why do average and center illuminance differ so much?',
        'Average illuminance E = total luminous flux ÷ area reflects overall brightness; center illuminance E = I/d² reflects the spotlight center peak (a point source attenuates with the square of distance). The spot center is often far above the average, so accent lighting must control both to avoid local overexposure damaging artifacts.',
        'About the Showcase Illuminance Calculator',
    ]))

if __name__ == '__main__':
    main()
