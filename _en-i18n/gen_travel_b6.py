#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'travel')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'travel')
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
    out = {'slug': slug, 'industry': 'travel', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('jet-lag-recovery', build('jet-lag-recovery', [
        "\U0001F634 Jet Lag Recovery Calculator",
        "Generate a personalized jet-lag plan from your time difference to reset your body clock scientifically",
        "\U0001F4C5 Recovery Plan",
        "\u23F0 Daily Schedule",
        "\U0001F4D6 Jet Lag Knowledge",
        "Origin Time Zone",
        "\U0001F1E8\U0001F1F3 Beijing (UTC+8)",
        "\U0001F1EF\U0001F1F5 Tokyo (UTC+9)",
        "\U0001F1EC\U0001F1E7 London (UTC+0)",
        "\U0001F1EB\U0001F1F7 Paris (UTC+1)",
        "\U0001F1FA\U0001F1F8 New York (UTC-5)",
        "\U0001F1FA\U0001F1F8 Los Angeles (UTC-8)",
        "\U0001F1E6\U0001F1FA Sydney (UTC+10)",
        "\U0001F1E6\U0001F1EA Dubai (UTC+4)",
        "\U0001F1E7\U0001F1F7 Sao Paulo (UTC-3)",
        "\U0001F1EE\U0001F1F3 New Delhi (UTC+5:30)",
        "\U0001F1F9\U0001F1ED Bangkok (UTC+7)",
        "Destination Time Zone",
        "Flight Duration (hours)",
        "Morning Departure",
        "Afternoon Departure",
        "Evening Departure",
        "Night Departure",
        "Personal Adaptation Rate",
        "Fast Adapter",
        "Slow Adapter",
        "+0 hours",
        "Estimated recovery: 0 days",
        "\U0001F4C5 Daily Schedule Adjustment Suggestions",
        "\U0001F9E0 Jet Lag Principles",
        "Jet lag is a physiological condition caused by crossing multiple time zones quickly, which puts the body's biological clock (circadian rhythm) out of sync with the new day-night cycle. Main symptoms include:",
        "Daytime drowsiness and nighttime insomnia",
        "Poor concentration and slower reactions",
        "Appetite changes and indigestion",
        "Mood swings and irritability",
        "Headache and muscle soreness",
        "\U0001F305 Why is flying east harder to adjust to?",
        "The body's natural circadian period is about 24.2 hours, slightly longer than a day. Therefore:",
        "Flying west:",
        "extends the day, which matches the natural tendency of the body clock, and usually allows an adjustment of 1.5 to 2 hours per day",
        "Flying east:",
        "shortens the day and requires the body clock to advance, usually allowing only 1 to 1.5 hours of adjustment per day",
        "Recovery time when flying east is about 1.5 times that of flying west",
        "\U0001F48A Comparison of Common Remedies",
        "Light Therapy",
        "The most natural and effective method, regulating melatonin secretion through light exposure",
        "Melatonin",
        "Taking it before bed may help adjustment; follow medical advice",
        "It keeps you alert during the day but should be avoided after 3pm",
        "Sleeping Pills",
        "May affect deep sleep quality, so regular use is not recommended",
        "Exercise",
        "Moderate daytime exercise helps shift the rhythm",
        "\u2708\ufe0f Tips During the Flight",
        "Hydration:",
        "The cabin air is dry, so drink about 200ml of water per hour of flying",
        "Avoid alcohol and caffeine:",
        "Both worsen dehydration and hurt sleep quality",
        "Move around on a schedule:",
        "Get up and walk every 2 to 3 hours to promote circulation",
        "Wear loose clothing:",
        "Choose comfortable clothes that help you relax and sleep",
        "Adjust your watch:",
        "Set it to destination time right after boarding to get into the right state early",
        "Tip:",
        "If the trip lasts only 2 to 3 days and heads west, consider not fully adjusting and instead keeping a schedule close to your home time zones, which makes recovery easier on return.",
        "\U0001F4DA In-Depth Analysis: Estimating Jet Lag Recovery Days",
        "Business Trips Across Time Zones",
        "Eastward / Westward Adaptation",
        "Progressive Schedule Adjustment",
        "New York to Beijing (13h East)",
        "From \u22125 to +8, diff = 13 > 0 heading east, days = ceil(13 \u00f7 1.5 \u00d7 1) = 9 days at normal rate; the fast tier \u00d7 0.7 \u2248 7 days. Move bedtime about 1.4 hours earlier each day.",
        "Beijing to New York (13h West)",
        "diff = \u221213 < 0 heading west, days = ceil(13 \u00f7 2 \u00d7 1) = 7 days; westward is generally about a third faster than eastward.",
        "Why is eastward harder?",
        "The human circadian period is slightly longer than 24 hours, so compressing the day is harder. The estimate uses 1.5 hours per day eastward and 2 hours per day westward.",
        "How do I use the timeline?",
        "It generates the wake and sleep offset for each day from recoveryDays, converging on destination time day by day.",
        "About \"Jet Lag Recovery Calculator\"",
        "Jet Lag Recovery Calculator. A travel tool that is essential for trips and works offline.",
    ]))


if __name__ == '__main__':
    main()