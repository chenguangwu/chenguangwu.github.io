#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'fengshui')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'fengshui')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    return mp


def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'fengshui', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

#!/usr/bin/env python3

GDS = 'Good Day Selector - pick an activity and start date to see auspicious days from the Jian-Chu (Twelve Establish-Remove) almanac. Cultural reference only.'


def main():
    # ===== birthday-analysis (29) =====
    write('birthday-analysis', build('birthday-analysis', [
        'Birth-Time Folk Reference',
        'Estimate the Four Pillars (Ba Zi) from birth date and time to understand the innate pattern.',
        'Birth-Time Folk Reference',
        '/ Birth-Time Folk Reference (Ba Zi Culture)',
        'Birth-Time Folk Reference (Ba Zi Culture)',
        'Chart Reference',
        'Deep Dive: Birth-Time Folk Reference (Ba Zi Culture)',
        'Enter the Gregorian birth date and birth hour to lay out the year, month, day, and hour pillars with heavenly stems and earthly branches, and understand your Ba Zi structure.',
        'Tally the Five Elements (Metal, Wood, Water, Fire, Earth) distribution across the four pillars to see if any is overly strong or missing, as a folk-life reference from the traditional-culture perspective.',
        'Combining the day master’s heavenly stem with gender, it gives an overall life reading and fun suggestions for balancing the Five Elements.',
        'Example: 1990-01-01, Zi hour (male)',
        'The tool lays out the four pillars: year pillar Geng-Wu, month pillar Wu-Yin, day pillar Bing-Xu, hour pillar Wu-Zi (day master stem is Bing, of Fire). The Five Elements distribution is Metal 1 · Wood 1 · Water 1 · Fire 2 · Earth 3 — Earth is strong, nothing missing; overall reading: for a male, wealth and authority are the favorable elements, all Five Elements present, the chart fairly balanced. Results are for folk reference only; life depends on your own effort.',
        'Does Ba Zi charting use the lunar or Gregorian calendar?',
        'This tool takes the Gregorian date and birth hour directly and internally converts them via the stem-branch calendar into the year, month, day, and hour pillars;',
        'Lunar conversion',
        'is already included in the algorithm, so no manual conversion is needed.',
        'Must I compensate for whatever Five Element is missing?',
        'Ba Zi’s Five Elements are only a fun perspective of traditional destiny study; the so-called “missing” and “strong” have no scientific basis. For health and life planning follow modern medicine and reality; this tool’s results are for cultural reference only.',
        GDS,
        'About Birth-Time Folk Reference (Ba Zi Culture)',
        'The Birth-Time Folk Reference (Ba Zi Culture) tool: enter the Gregorian birthday and birth hour to lay out the year, month, day, and hour pillars with stems and branches and tally the Five Elements distribution.',
        'Lay out the Four Pillars (Ba Zi) from Gregorian birthday and birth hour',
        'Tally the Metal-Wood-Water-Fire-Earth distribution to see what is strong or missing',
        'Give an overall chart reading based on the day master’s stem and gender',
        'Offer fun Five-Element balancing suggestions (folk reference)',
        'Understand your Ba Zi structure and Five-Element strength',
        'A first look at the chart from the traditional-culture perspective',
        'Learn Ba Zi charting and stem-branch knowledge',
        'Explore folk-culture interests',
    ]))

    # ===== fengshui-calculator (36) =====
    write('fengshui-calculator', build('fengshui-calculator', [
        'Orientation Luo Pan Demo',
        'A simple orientation tool: enter a facing direction to see the corresponding Ba Gua orientation (for entertainment only, not feng shui advice).',
        'Orientation Luo Pan Demo',
        '/ Orientation Luo Pan Demo (Traditional Culture · Entertainment)',
        'Orientation Luo Pan Demo (Traditional Culture · Entertainment)',
        'View the Orientation Luo Pan Demo (Traditional Culture · Entertainment) (Fun Edition) User Guide',
        'Luo Pan',
        'Orientation Query',
        'Feng Shui Knowledge',
        'Prioritize a living environment that is comfortable, healthy, and convenient; do not over-rely on superstition.',
        'Deep Dive: Orientation Luo Pan Demo (Traditional Culture · Entertainment)',
        'Enter the house facing angle (0–360°); view the corresponding Ba Gua orientation, Twenty-Four Mountains, and Five-Element attribute.',
        'Directly pick the sitting-facing direction and house type to compare traditional claims with the modern scientific view on home orientation pros and cons.',
        'Learn the cultural basics of the Luo Pan orientation demo and the Twenty-Four Mountains, and save query history locally for review anytime.',
        'Example: due north at 0°',
        'Enter 0° (or pick the preset “Due North”); the tool shows the Ba Gua orientation as Kan trigram, element Water, Twenty-Four Mountains Ren-Zi-Gui, and lists the eight-direction trigrams. Switch to “House Orientation Analysis” and pick “Sitting North Facing South” to see traditional claims (Kan house, Li facing, water-fire already-settled) alongside the modern scientific view (good winter daylight, sheltered from north wind).',
        'What does the Orientation Luo Pan Demo (Traditional Culture · Entertainment) do?',
        'Enter the house facing angle, or directly pick the sitting-facing direction and house type, to view the corresponding Ba Gua orientation and trigram explanation. Results are an orientation reference from the traditional-culture angle, for entertainment only, not feng shui advice or a decision basis.',
        'How are the Twenty-Four Mountains divided?',
        'The Twenty-Four Mountains divide the 360° circle into 24 equal 15° segments, denoted by heavenly stems, earthly branches, and the Eight Trigrams, arranged clockwise from due north (Ren-Zi-Gui) to northwest (Xu-Qian-Hai); it is the traditional Luo Pan method for fixing orientation.',
        GDS,
        'About the Orientation Luo Pan Demo (Traditional Culture · Entertainment)',
        'The Orientation Luo Pan Demo (Traditional Culture · Entertainment) (Fun Edition) tool: enter the house facing angle or pick a sitting-facing direction to view the corresponding Ba Gua orientation, Twenty-Four Mountains, and Five-Element attribute.',
        'Convert a 0–360° angle into Ba Gua orientation and Twenty-Four Mountains',
        'Pick a sitting-facing direction to compare traditional claims with the modern scientific view',
        'Built-in Twenty-Four-Mountain orientation table and home-orientation key points',
        'Save query history locally for review anytime',
        'Understand the Ba Gua and Five Elements for a house orientation',
        'View home orientation from both traditional and modern perspectives',
        'Learn the Luo Pan orientation demo and Twenty-Four-Mountain culture',
        'A fun reference for home arrangement',
        'How to use the Orientation Luo Pan Demo',
        'Understand the Ba Gua orientation, Twenty-Four Mountains, and Five Elements for a house orientation; compare traditional claims with the modern scientific view on home layout; learn the Luo Pan orientation demo (Traditional Culture · Entertainment) and the Huang Li (almanac) culture. For entertainment reference only.',
        'What does the Orientation Luo Pan Demo (Traditional Culture · Entertainment) (Fun Edition) do?',
        'How do I use the Orientation Luo Pan Demo?',
        'Which scenarios suit the Orientation Luo Pan Demo (Traditional Culture · Entertainment) (Fun Edition)?',
    ]))

    # ===== fengshui-guide (28) =====
    write('fengshui-guide', build('fengshui-guide', [
        'Traditional Living-Culture Compendium',
        'Systematically learn traditional feng shui knowledge and improve your living and working environment.',
        'Traditional Living-Culture Compendium',
        '/ Traditional Living-Culture Compendium (Folk Research)',
        'Traditional Living-Culture Compendium (Folk Research)',
        'This handbook organizes traditional feng shui basics by scenario (main door, bedroom, wealth corner, sha energy, etc.); content comes from public folk sources, for cultural understanding and arrangement reference, not a decision basis.',
        'Deep Dive: Traditional Living-Culture Compendium (Folk Research)',
        'Browse traditional feng shui points by category “Basics / Residence / Wealth Corner / Sha Resolution / Office” to quickly understand the do’s and don’ts of each.',
        'Search by keyword (e.g. entryway, wealth corner, beam pressing overhead) to pinpoint the entry you need.',
        'Before arranging your home or office, check the layout principles for the relevant scenario as a fun reference.',
        'Example: “Bedroom Feng Shui”',
        'Under the “Residence” category you find: bedrooms should be quiet, the headboard should lean on a solid wall (not under a window), avoid facing a mirror, appliances, or a beam overhead; the couple’s bed should run north–south. These come from public folk sources and should be judged together with real factors like daylight and ventilation.',
        'Is feng shui scientifically based?',
        'Feng shui’s attention to daylight, ventilation, orientation, and circulation has some merit, but claims about fortune, wealth, or career lack scientific basis. Make comfort, health, and convenience the primary standards for your environment.',
        'What are the sources of this handbook’s content?',
        'Content is compiled from public traditional folk sources, categorized by scenario for quick lookup, for cultural understanding and arrangement reference, not any professional or decision advice.',
        GDS,
        'About the Traditional Living-Culture Compendium (Folk Research)',
        'The Traditional Living-Culture Compendium (Folk Research) organizes traditional feng shui points by Basics, Residence, Wealth Corner, Sha Resolution, and Office, and supports keyword search.',
        'Quick lookup of 20+ feng shui basics across five categories',
        'Keyword search to quickly locate entries',
        'Switch categories to browse Residence / Office / Wealth Corner points',
        'Fully offline, client-side lookup; data is not uploaded',
        'Check the do’s and don’ts of the main door, entryway, and bedroom when arranging your home',
        'Reference for office layout and seating taboos',
        'Understand the wealth corner and common sha-energy handling',
        'Systematic study of traditional feng shui culture',
        'e.g.: entryway, Ming Tang, wealth corner...',
    ]))

    # ===== good-day-selector (27) =====
    write('good-day-selector', build('good-day-selector', [
        'Traditional Date Suitability Reference (Folk Culture)',
        'Pick an activity type and query suitable dates within the next 30 days.',
        'Traditional Date Suitability Reference',
        '/ Traditional Date Suitability Reference (Folk Culture)',
        'Traditional Date Suitability Reference (Folk Culture)',
        'It derives the Twelve Establish-Remove Deities from the solar-term month branch and the daily stem-branch, then rates activity fit by the deities’ traditional do’s and don’ts; the algorithm is deterministic and reproducible, results for folk reference only.',
        'Query Suitability',
        'Deep Dive: Traditional Date Suitability Reference (Folk Culture)',
        'Choose an activity type (wedding / moving / opening / signing / burial / travel) and specify a start date.',
        'Derive each day’s do’s and don’ts for the next 30 days via the traditional “Twelve Establish-Remove Deities” and give a fit score for the activity.',
        'View the daily clash-zodiac hint to help avoid dates that clash with your own zodiac sign.',
        'Example: wedding day selection in September 2026',
        'The tool derives the daily Twelve Establish-Remove Deities from the solar-term month branch and day stem-branch, then rates wedding fit by the deities’ traditional do’s and don’ts. E.g. 2026-09-15 is a Ren-Zi day, a Ding (settled) day — traditionally good for marriage and blessing, high wedding score (5); 2026-09-10 is a Ding-Wei day, a Bi (closed) day — neither do nor don’t stands out, medium score (3). The algorithm is deterministic and reproducible; results are for folk reference only.',
        'How is an auspicious day calculated?',
        'This tool derives the “Twelve Establish-Remove Deities” (Jian, Chu, Man, Ping, Ding, Zhi, Po, Wei, Cheng, Shou, Kai, Bi) from the solar-term month branch and daily stem-branch, then rates the chosen activity’s fit by the deities’ traditional do’s-and-don’ts table and gives a score.',
        'Can the result be used as a day-selection basis?',
        'The Twelve Establish-Remove belongs to traditional Huang Li (almanac) folk custom; results are deterministic and reproducible but for cultural and folk reference only; for important schedules combine with real arrangements and personal judgment — this tool offers no decision advice.',
        'About the Traditional Date Suitability Reference (Folk Culture)',
        'The Traditional Date Suitability Reference (Folk Culture) tool: pick an activity type and start date, derive the next 30 days’ do’s/don’ts and scores via the traditional Twelve Establish-Remove Deities.',
        'Derive the daily Twelve Establish-Remove Deities from the solar-term month branch and day stem-branch',
        'Give an activity-fit score from the deities’ traditional do’s and don’ts',
        'Mark the daily clash-zodiac to help avoid taboos',
        'Deterministic and reproducible results, instant client-side calculation',
        'Select suitable dates for weddings, moving, and openings',
        'Folk reference for signing, travel, and burial',
        'Learn the Twelve Establish-Remove Deities and daily do’s/don’ts',
        'Study traditional culture and Huang Li (almanac) knowledge',
    ]))

    # ===== zodiac-lookup (26) =====
    write('zodiac-lookup', build('zodiac-lookup', [
        'Chinese Zodiac Folk Reference',
        'Query your zodiac sign, Five-Element attribute, and birth do’s/don’ts by birth year.',
        'Chinese Zodiac Folk Reference',
        '/ Chinese Zodiac Folk Reference',
        'Enter your birth year; by the stem-branch and zodiac mapping rules, find your zodiac sign, Na Yin Five Elements, and pairing do’s/don’ts; the sign-to-branch mapping is a fixed traditional rule, so results are stable and reproducible.',
        'Deep Dive: Chinese Zodiac Folk Reference',
        'Enter your birth year to quickly find your native zodiac sign, corresponding earthly branch, and Na Yin Five Elements, and learn the sign’s basic cultural meaning.',
        'For romance or socializing, refer to the Liu He / San He / Liu Chong sign-pairing do’s/don’ts to gauge how well signs match.',
        'Combine your native sign’s auspicious direction, lucky numbers, and colors as a fun reference for arrangement or choosing items.',
        'Example: 1990 (Year of the Horse)',
        'Born in 1990, the sign is Horse (Wu), earthly branch Wu, element Fire, Yin-Yang Yang; native hours 11:00–13:00, auspicious direction South, lucky numbers 2/7, colors red/purple; Liu He noble signs Tiger/Dog/Sheep, Liu Chong avoid Rat/Ox. From this you can learn the Horse sign’s traditional personality description and pairing do’s/don’ts.',
        'Is the zodiac counted by lunar or Gregorian year?',
        'The zodiac is bounded by the lunar New Year; people born in early January or February of the Gregorian calendar may still belong to the previous sign — confirm with that year’s Spring Festival date before checking.',
        'Are this tool’s results accurate?',
        'The zodiac, earthly branches, Five Elements, Na Yin, etc. are traditional-culture common knowledge; the tool computes by fixed rules with stable results; sign-pairing do’s/don’ts are for entertainment and social reference only, with no scientific claims.',
        GDS,
        'About the Chinese Zodiac Folk Reference',
        'The Chinese Zodiac Folk Reference tool: enter your birth year to find your zodiac sign, earthly branch, Na Yin Five Elements, and Liu He / San He / Liu Chong pairing do’s/don’ts.',
        'Covers the twelve zodiac signs’ earthly branches, Five Elements, Yin-Yang, and Na Yin attributes',
        'Auto-derive Liu He, San He noble signs, and Liu Chong avoid-pairings',
        'Give native hours, auspicious direction, lucky numbers, and colors',
        'Includes marriage do’s/don’ts reference, instant client-side query',
        'Understand your sign culture and native meaning',
        'Reference sign-pairing do’s/don’ts in romance and socializing',
        'Reference auspicious direction and lucky color when arranging or choosing items',
        'Study traditional culture and folk knowledge',
    ]))


if __name__ == '__main__':
    main()
