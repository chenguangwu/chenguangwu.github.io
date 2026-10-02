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
    write('luggage-size-checker', build('luggage-size-checker', [
        "\u2705 Airline Luggage Size Checker",
        "Check whether your luggage meets the size and weight requirements of major airlines (for reference only)",
        "\"Check whether your luggage meets the size and weight requirements of major airlines (for reference only)\" is computed from the input parameters with professional calculations and outputs a result.",
        "Luggage Size Checker",
        "/ Luggage Size Checker",
        "\u2713 Size Check",
        "\U0001F4CB Airline Table",
        "\U0001F4A1 Packing Tips",
        "\U0001F392 Carry-on Luggage",
        "\U0001F9F3 Checked Luggage",
        "Filter:",
        "Domestic Airlines",
        "International Airlines",
        "Low-cost Airlines",
        "\u2705 Summary of Luggage Rules from Major Airlines",
        "Search airlines",
        "\U0001F392 Carry-on Packing Tips",
        "Rolling clothes:",
        "Roll garments into cylinders, which saves more space than folding and reduces creases",
        "Packing cubes:",
        "Use compression bags to group clothing, making it easier to find things and saving space",
        "Heavy items at the bottom:",
        "Put shoes and toiletry bags and other heavy items at the bottom to keep the center of gravity stable",
        "Use the gaps:",
        "Stuff socks, underwear and other small items into shoes or empty corners",
        "Carry-on essentials:",
        "Valuables, documents and power banks must be carried on, not checked",
        "Liquid limits:",
        "Carry-on liquids are limited to 100ml per container and 1L in total, and must go in a transparent bag",
        "\U0001F4CF Common Luggage Size Reference",
        "20-inch Carry-on Case",
        "about 55\u00d735\u00d722cm",
        "24-inch Checked Case",
        "about 65\u00d742\u00d726cm",
        "28-inch Checked Case",
        "about 75\u00d750\u00d730cm",
        "Backpack",
        "about 45\u00d730\u00d720cm",
        "How to measure:",
        "Use the maximum outer dimensions including wheels, telescoping handle and grab handles",
        "Weight limits:",
        "Low-cost airlines check weight strictly and overweight fees are high",
        "Membership benefits:",
        "Gold and Platinum members of an airline usually get extra baggage allowance",
        "Cabin differences:",
        "Business and first class baggage allowance is usually twice that of economy",
        "Alliance reciprocity:",
        "Members of alliances such as Star Alliance or Oneworld may enjoy extra allowance",
        "\u26a0\ufe0f The data above is for reference only, and airlines may change the rules at any time. Always check the airline's official website for the latest baggage policy before travelling.",
        "\U0001F4DA In-Depth Analysis: Luggage Size Compliance Check",
        "Choosing a Carry-on Case",
        "Comparing Airline Limits",
        "Three-Side Sum and Over-Limit Warnings",
        "20-Inch Carry-on Case",
        "Dimensions 34\u00d750\u00d720cm give a three-side sum of 104cm; Air China's carry-on limit is 115cm, so the size passes and with weight \u22645kg it passes overall. A three-side sum of 118 would be flagged as \"close to the limit\".",
        "Low-cost Airlines Are Stricter",
        "Airlines such as AirAsia and Ryanair often limit carry-on to 90 to 100cm and 7kg, so the same case may fail; switch to the lcc filter to see the difference.",
        "How is the three-side sum computed?",
        "Length + width + height. Some airlines also cap each side separately, so the tool compares both dimensions and weight.",
        "How about checked luggage?",
        "Switch to the checked type and the result is judged by each airline's check-in size and weight limits.",
        "About \"Luggage Size Checker\"",
        "Luggage Size Checker. A travel tool that is essential for trips and works offline.",
        "Enter an airline name...",
    ]))
    write('road-trip-gas-cost', build('road-trip-gas-cost', [
        "\U0001F9EE Road Trip Fuel Cost Calculator",
        "Compute road trip costs across multiple dimensions, with multi-vehicle comparison, tolls and per-person splitting",
        "Core formula (over the input variables): d \u00d7 c \u00f7 100",
        "\U0001F699 Multi-Vehicle Comparison",
        "\U0001F4D6 Reference Data",
        "Total Distance (km)",
        "Highway Tolls (CNY)",
        "Number of Passengers",
        "Compact Sedan (6-7L)",
        "Mid-size Sedan (7-8L)",
        "City SUV (8-10L)",
        "Off-road SUV (12-15L)",
        "Electric Vehicle (energy use)",
        "\u2795 Add to Comparison",
        "Total Trip Cost",
        "Fuel Needed",
        "Tolls",
        "Cost per Person",
        "Cost per Kilometer",
        "Cost per Person per Kilometer",
        "Money-saving tips:",
        "Keeping an economical speed of 80 to 100 km/h saves about 15% fuel; planning the route ahead to avoid congestion; carpooling with several people greatly reduces the per-person cost.",
        "Added",
        "vehicles",
        "No vehicles in the comparison yet; click \"Add to Comparison\" to begin",
        "\u26fd Recent Fuel Price Reference (CNY/L)",
        "\U0001F697 Common Vehicle Fuel Consumption Reference",
        "Fuel Vehicle Consumption Reference (L/100km)",
        "Micro car (Fit, POLO):",
        "Compact Sedan (Lavida, Corolla):",
        "Mid-size Sedan (Camry, Magotan):",
        "Compact SUV (CR-V, RAV4):",
        "Mid-size SUV (Highlander, Tiguan L):",
        "Off-road SUV (Wrangler, Tank 300):",
        "MPV (GL8, Odyssey):",
        "\U0001F6E3\ufe0f Highway Toll Reference",
        "Small passenger car:",
        "about CNY 0.4 to 0.6 per kilometer",
        "Free highways on holidays:",
        "Spring Festival, Qingming, Labour Day and National Day",
        "ETC discount:",
        "Usually 5% off",
        "\u26a0\ufe0f The data above is for reference only. Actual fuel consumption is affected by driving habits, road conditions, temperature and load, so go by actual consumption.",
        "\U0001F4DA In-Depth Analysis: Road Trip Fuel Cost Calculator",
        "Long-distance Fuel Estimates",
        "Splitting Costs Among People",
        "Comparing Vehicle Types",
        "1000km by Sedan",
        "Distance 1000, consumption 7L/100km, fuel price CNY 8/L, tolls 300: fuel = 1000 \u00d7 7 \u00f7 100 \u00d7 8 = 560, total 860; for 2 people that is 430 each and CNY 0.86 per kilometer.",
        "Comparing Multiple Vehicles",
        "An SUV at 10L over the same distance gives 800 in fuel plus 300 in tolls = 1100; switch to the comparison tab to add several plans and take the smallest minTotal.",
        "How is it calculated for EVs?",
        "Choose the EV preset to convert from energy consumption, or enter the battery consumption as fuel consumption and the electricity price as the fuel price.",
        "Is the toll field required?",
        "No, it can be left blank (default 0); only fuel and tolls are included in the total.",
        "About \"Road Trip Fuel Cost Calculator\"",
        "Road Trip Fuel Cost Calculator. A travel tool that is essential for trips and works offline.",
    ]))


if __name__ == '__main__':
    main()