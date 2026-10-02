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
    write('aim-trainer', build('aim-trainer', [
        "\U0001F3AF Aim Trainer",
        "This tool is a pure front-end online utility. Data is processed locally in the browser and never uploaded to a server, and the calculation follows the standards and rules of the relevant field; results are for reference only. Tool name: Aim Trainer - an online tool in the travel domain.",
        "Hit rate = hits \u00f7 targets shown \u00d7 100%; average reaction time = \u03a3 reaction times \u00f7 hits; the effective click area is the circle within target radius r (area = \u03c0r\u00b2), so smaller targets produce longer reaction times. Scores are judged on two metrics, hit rate and average reaction time: under 250 ms is excellent and 250 to 400 ms is good.",
        "Hits:",
        "Misses:",
        "Time left:",
        "Click \"Start\" to begin training",
        "Tap the targets that appear within 30 seconds",
        "\U0001F4DA In-Depth Analysis: Scoring Aim Training Sessions",
        "Hand Stability for Shooting and Esports",
        "Reaction Speed Training",
        "30-Second Time-Limited Challenge",
        "45 Hits in 30 Seconds",
        "45 hits and 5 misses within 30 seconds means 50 attempts, giving an accuracy of 45/50\u00d7100 = 90%. The average interval between hits is about 0.67 seconds, which is an above-average result.",
        "Comparing Two Sessions",
        "A first session with 38 hits (76% accuracy) and a second with 45 hits (90%), repeated a week apart, reveals the trend in hand stability and attention.",
        "How is accuracy calculated?",
        "Accuracy = hits \u00f7 total attempts (hits + misses) \u00d7 100. Training is fixed at 30 seconds, and more hits means shorter intervals.",
        "What scenarios suit it?",
        "Warming up for FPS games, rehabilitation of fine hand movements, and self-assessment of reaction speed; record several rounds and read the curve.",
        "About \"Aim Trainer\"",
        "Aim Trainer is an online tool in the travel domain. A travel tool that is essential for trips and works offline.",
    ]))
    write('business-name-generator', build('business-name-generator', [
        "\U0001F3E2 Business Name Generator",
        "This generator produces content on the front end by rule, either randomly or deterministically, following the specified format specification. Results can be copied and used directly, and no data leaves the browser. Tool name: Business Name Generator - a free generator tool, an online business name generator, free to use.",
        "Coffee / Food and Beverage",
        "Tech / Software",
        "Fashion / Apparel",
        "Consulting / Services",
        "Retail / E-commerce",
        "\U0001F4DA In-Depth Analysis: Business Name Generator",
        "Naming a New Store",
        "Brand Naming",
        "Event and IP Naming",
        "Eight Names for the Food and Beverage Industry",
        "Choosing \"Food and Beverage\" with a count of 8 yields combinations such as \"Food Light Bistro\", \"A Bowl of Rivers and Lakes\" and \"Cooking Smoke Collection\", which you can copy and then rerun for other industries in bulk.",
        "Controlling the Count Limit",
        "The count box supports 1 to 50; entering 50 generates 50 candidates and anything above the limit is clamped to 50 to keep the page from getting too long.",
        "Do the names carry trademark risk?",
        "It only makes creative combinations. Before real use, check the trademark database and the business registry for duplicates to avoid infringement.",
        "Can I specify a style?",
        "Names are randomly assembled from industry word lists. You can pick synonyms from the results and rewrite them, but the tool does not guarantee unique semantics.",
        "About \"Business Name Generator\"",
        "Business Name Generator. A travel tool that is essential for trips and works offline.",
    ]))
    write('travel-budget-calculator', build('travel-budget-calculator', [
        "\U0001F4B0 Travel Budget Calculator",
        "Plan your travel spending so the trip feels more secure",
        "Total trip budget = transport + accommodation (nightly rate \u00d7 nights) + food (per person per day \u00d7 people \u00d7 days) + tickets + shopping + contingency; per person = total \u00f7 people. Contingency is usually reserved at 10% to 15% of the total, and an overspending risk is flagged when actual spending exceeds the total or a single item exceeds 120% of its budget.",
        "Number of Travelers",
        "\U0001F4CA Estimated Costs by Category",
        "\u2708\ufe0f Airfare / Transport",
        "\U0001F3E8 Accommodation / Night",
        "\U0001F37D\ufe0f Food / Day",
        "\U0001F3AB Attraction Tickets",
        "\U0001F6CD\ufe0f Shopping / Souvenirs",
        "\U0001F198 Emergency Fund",
        "\u00a5 0 per person per day",
        "\U0001F4DA In-Depth Analysis: Travel Budget Calculator",
        "Total Budget Estimate",
        "Per Person / Per Day",
        "Share Visualization",
        "5 Days, 2 People",
        "Transport 3000 + accommodation 400\u00d75 = 2000 + food 150\u00d75 = 750 + tickets 800 + shopping 1000 + contingency 500 = CNY 8050; that is CNY 4025 per person and CNY 805 per day. Food accounts for 750 \u00f7 8050 \u2248 9.3%.",
        "Raising Shopping",
        "Changing shopping to 3000 brings the total to 10050 and the pie chart updates live, so you can see which category is over budget and trim it.",
        "Does the food cost already account for the number of people?",
        "Food is computed as cost per person per day \u00d7 days and is not multiplied by the head count again; transport and accommodation are usually a single lump sum.",
        "Is there a share chart?",
        "Each of the six categories is computed as value \u00f7 total \u00d7 100",
        " and rendered as a bar or pie chart.",
        "About \"Travel Budget Calculator\"",
        "Travel Budget Calculator. A travel tool that is essential for trips and works offline.",
    ]))
    write('travel-days-counter', build('travel-days-counter', [
        "\U0001F9EE Trip Days and Countdown Calculator",
        "Calculate the total number of trip days, or how long until departure",
        "Trip Days Calculator",
        "/ Trip Days Calculator",
        "Trip days = (return date \u2212 departure date) \u00f7 86400000 + 1 (counting both endpoints); nights = days \u2212 1; countdown to departure = ceil(departure date \u2212 current date). Months and years are accumulated automatically by timestamp, and a leap-year February adds one day; days elapsed = current date \u2212 departure date.",
        "Return Date",
        "Depart Today",
        "Return +7 days",
        "\U0001F4DA In-Depth Analysis: Trip Days and Countdown",
        "Trip Span",
        "Departure",
        "Countdown",
        "Days Elapsed",
        "days = ceil((9/7 \u2212 9/1)/86400000) + 1 = 7 days, nights = 6, hours = 168, weeks = 1; counting both endpoints gives 7 days.",
        "Countdown to a Future Departure",
        "With start set to 9/10 and now at 9/1, untilStart = ceil((start \u2212 now)/86400000) = 9 days, which is useful for pre-trip planning.",
        "Does the day count include both endpoints?",
        "Yes. One day is added to the milliseconds difference between end and start, and nights = days \u2212 1 gives the number of overnight stays.",
        "What if the countdown goes negative?",
        "Once start has passed, sinceEnd becomes positive, indicating how many days ago the trip ended.",
        "About \"Trip Days Calculator\"",
        "Trip Days Calculator. A travel tool that is essential for trips and works offline.",
    ]))


if __name__ == '__main__':
    main()