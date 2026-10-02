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
    write('recommender-10', build('recommender-10', [
        "\U0001F37D\ufe0f Food Guide (Specialties, Distribution, Recommendations)",
        "Specialties / Distribution / Recommendations",
        "The food guide is generated from destination elements: signature cuisine (3 to 5 representative local dishes), distribution areas (sightseeing zones, old towns, night markets), per-person budget tiers (economy CNY 30 to 60, mid-range CNY 60 to 150, upscale above CNY 150) and recommended meal hours (breakfast 6 to 9, lunch 11 to 13, dinner 17 to 20). Total spend = per-person cost \u00d7 people \u00d7 meals \u00d7 days.",
        "\U0001F4DA In-Depth Analysis: Food Specialty Recommendations",
        "Destination Cuisine",
        "Where the Specialties Are",
        "Random Inspiration",
        "Generate 5 Beijing Food Picks",
        "With a count of 5, random picks from the city library include \"Beijing Roast Duck\", \"Noodles with Soybean Paste\", \"Braised Offal\", \"Dou Zhi with Crisp Ring\" and \"Mutton Hotpot\", with distribution notes to help you find the shop.",
        "Adjustable Count",
        "The count box clamps between 1 and 50; entering 20 yields 20 candidates, which makes it easy to build a food map.",
        "What are the recommendations based on?",
        "They are random samples from a built-in city-to-specialty mapping rather than live ratings, so they suit inspiration rather than decision making.",
        "Can it locate specific restaurants?",
        "Only down to the cuisine or famous-venue level; use a map tool together for specific stores.",
        "About \"Food Guide (Specialties, Distribution, Recommendations)\"",
        "Food Guide (Specialties, Distribution, Recommendations). A travel tool that is essential for trips and works offline.",
    ]))
    write('recommender-9', build('recommender-9', [
        "\U0001F4CB Accommodation Recommendation (Type, Booking, Reviews)",
        "Type / Booking / Reviews",
        "Accommodation recommendations are grouped by need: hostel (CNY 50 to 150 per person per night), budget hotel (CNY 150 to 350), mid to upscale (CNY 350 to 800) and resort (above CNY 800). Booking considerations cover location (within 1 km of a subway station), cancellation policy, rating (prefer 4.5 or above) and review count (more than 100 reviews is more meaningful). Accommodation budget = nightly rate \u00d7 nights \u00d7 rooms.",
        "\U0001F4DA In-Depth Analysis: Accommodation Recommendation Guide",
        "Accommodation Types",
        "Booking Considerations",
        "Review Dimensions",
        "Generate 5 Accommodation Suggestions",
        "With a count of 5, picks from the destination library include \"Old Town Guesthouse\", \"Hotel Near the Subway\" and \"Lakeside Resort\", each with its type and booking notes.",
        "Count Limit",
        "Supports 1 to 50; entering 12 yields 12 items, and anything above the limit is clamped to 50.",
        "Does it include prices?",
        "It does not include live room rates, only types and filtering dimensions. Check prices on a booking platform.",
        "How should I read reviews?",
        "It highlights three dimensions: location, cleanliness and cancellation policy. The tool does not scrape platform ratings.",
        "About \"Accommodation Recommendation (Type, Booking, Reviews)\"",
        "Accommodation Recommendation (Type, Booking, Reviews). A travel tool that is essential for trips and works offline.",
    ]))
    write('timezone-converter-advanced', build('timezone-converter-advanced', [
        "\U0001F310 Advanced Time Zone Converter",
        "Choose a source and target time zone, then enter a time to convert",
        "Source Time",
        "Select a time zone to convert",
        "\U0001F4D0 Notes on Time Zones and Daylight Saving Time",
        "UTC: Coordinated Universal Time, the global time reference",
        "Beijing Time: UTC+8 (China does not observe daylight saving time)",
        "New York: UTC-5 (EST) / UTC-4 (EDT daylight saving time, second Sunday in March to first Sunday in November)",
        "London: UTC+0 (GMT) / UTC+1 (BST daylight saving time, last Sunday in March to last Sunday in October)",
        "Moscow: UTC+3 (Russia does not observe daylight saving time)",
        "Dubai: UTC+4 (no daylight saving time)",
        "Tokyo: UTC+9 (no daylight saving time)",
        "Sydney: UTC+10 (AEST) / UTC+11 (AEDT daylight saving time, first Sunday in October to first Sunday in April)",
        "Note: this tool uses the browser Intl API to handle daylight saving time automatically",
        "\U0001F4DA In-Depth Analysis: Advanced Time Zone Converter",
        "Cross-Time-Zone Meetings",
        "Flight Schedule Conversion",
        "Daylight Saving Time Handling",
        "09:00 Shanghai to New York",
        "From Asia/Shanghai (+8) to America/New_York (\u22125, or \u22124 under daylight saving time), New York shows 21:00 on the previous day (20:00 in winter time). The tool picks the daylight saving offset automatically by date.",
        "Reverse Calculation",
        "Enter the target time in toTime to work back to fromTime, which helps when scheduling two-way calls.",
        "Is daylight saving time accurate?",
        "Offsets are computed for the specific date with the Intl API, including daylight saving time; extremely early historical years may deviate.",
        "Which time zones are supported?",
        "A list of major IANA time zones is built in, covering the commonly used cities.",
        "About \"Advanced Time Zone Converter\"",
        "Advanced Time Zone Converter. A travel tool that is essential for trips and works offline.",
        "How to Use the Advanced Time Zone Converter",
        "Estimating travel planning, itineraries and expenses.",
        "What does the Advanced Time Zone Converter do?",
        "Choose a source and target time zone and enter a local time to convert it precisely into the corresponding time in another zone, with daylight saving time handled, for scheduling cross-border meetings, calls and flight connections.",
        "How do I use the Advanced Time Zone Converter?",
        "What scenarios suit the Advanced Time Zone Converter?",
        "Shown after conversion",
    ]))
    write('travel-adapter-guide', build('travel-adapter-guide', [
        "\U0001F4DA Global Plug and Socket Guide",
        "Learn the plug types and voltages of each country so you can prepare an adapter in advance",
        "Travel Plug Guide",
        "/ Travel Plug Guide",
        "Socket types are coded from A to O (A: two flat pins, B: two flat pins plus ground, C: two round pins, G: three rectangular pins, and so on). Nominal voltage ranges from 100 to 240 V at 50 or 60 Hz. Compatibility is judged by whether the plug shape matches and whether the voltage falls within the device input range (100 to 240 V). A voltage mismatch requires a transformer, where power = voltage \u00d7 current; exceeding the transformer's rated power causes overload.",
        "\U0001F529 Plug Type Diagrams",
        "US / Japan / Canada",
        "Two flat pins",
        "US / Canada",
        "Three flat pins (grounded)",
        "Europe / Asia",
        "Two round pins",
        "India / UK",
        "Three large round pins",
        "Europe / Germany / France",
        "Two round pins (grounded)",
        "UK / Hong Kong / Singapore",
        "Three rectangular pins",
        "Three angled flat pins",
        "China / Australia / New Zealand",
        "Figure-eight flat pins",
        "Three small round pins",
        "\U0001F4DA In-Depth Analysis: Global Plug and Socket Guide",
        "Plug Type Lookup",
        "Voltage Cross-check",
        "Destination Preparation",
        "Japan Plugs",
        "Japan uses type A and B two-pin flat plugs at 100 V. A two-pin Chinese plug fits directly, but a transformer is required (do not connect 100 V devices to 220 V).",
        "UK Three-Pin",
        "The UK, Hong Kong and Singapore use type G three-pin flat plugs at 230 to 240 V, so a converter is needed; the tool looks up plug type and voltage by country name.",
        "What if the voltage does not match?",
        "A matching plug shape does not mean a matching voltage. Taking 100/120 V devices to a 220 V country requires a transformer, otherwise they burn out.",
        "Can I search a region?",
        "Fuzzy search by country or region name returns the plug type and voltage range.",
        "About \"Travel Plug Guide\"",
        "Travel Plug Guide. A travel tool that is essential for trips and works offline.",
        "\U0001F50D Search country or region...",
    ]))


if __name__ == '__main__':
    main()