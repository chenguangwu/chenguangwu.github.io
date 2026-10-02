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
    write('index', build('index', [
        "\u2708\ufe0f Travel Tools",
        "Travel",
        "Travel Tools",
        "See the current time in major cities worldwide and convert between them at a glance, making it easy to schedule cross-time-zone calls, collaboration and livestreams with quick reference for common cities.",
        "Travel Budget Calculator: itemizes trip spending across transport, accommodation, food, tickets and so on and totals it up, flagging overspending; used for travel finance planning.",
        "International Tip Calculator: pick a destination country and get a tip percentage and amount suggestion based on local custom; a reference for spending on outbound trips.",
        "Enter mileage, fuel consumption, fuel price and tolls to compute the total fuel and toll cost of a road trip, with support for comparing multiple vehicles and splitting the cost per person; used for long-distance drive and carpool budgeting.",
        "Enter the origin and destination time zones and the number of time-zone days crossed to generate a personalized jet-lag schedule (light exposure, sleep and meal timing), helping cross-time-zone travelers adjust their body clock sensibly.",
        "Travel Photo Storage Calculator: estimates the memory card space needed from the number of shots, per-file size and format; used for travel gear preparation.",
        "Trip Days Calculator",
        "Trip Days and Countdown Calculator: computes the total trip length or the countdown to departure, for itinerary planning and reminders.",
        "Advanced Time Zone Converter",
        "Choose a source and target time zone and enter a local time to convert it precisely into the corresponding time in another zone, with daylight saving time handled, for scheduling cross-border meetings, calls and flight connections.",
        "Enter an industry keyword or preferred style to quickly generate a batch of registrable shop and company name candidates, for startup naming, brand brainstorming and travel market stall naming.",
        "Passport Number Format Validator: checks the length and format validity of passport numbers from various countries, for pre-checks on forms and identity verification.",
        "Pick a business, family or outdoor trip template to auto-generate a categorized packing list, with checkable progress saved locally so that key items such as documents and chargers are not left behind.",
        "Food Recommendation Guide Generator: generates specialty food, distribution and recommendation guides for a destination to assist travel dining planning; results are for reference.",
        "Accommodation Recommendation Generator: generates accommodation types, booking points and review references for a destination to assist the choice of lodging; results are for reference.",
        "Time Zone Lookup",
        "Time Zone Lookup (IANA Time Zone)",
        "Enter the number of travel days, destination and party size to compare the coverage and price of different insurance types such as medical, baggage and delay, helping you pick a cost-effective travel insurance plan.",
        "Luggage Size Checker",
        "Enter the length, width, height and weight of your luggage and compare it against each airline's cabin allowance (dimensions and weight) to see whether it meets check-in or carry-on requirements, for a pre-trip compliance self-check.",
        "Currency Cheat Sheet",
        "Enter a target currency code and a reference rate to generate a quick reference table for common round amounts (such as 10, 50, 100), making mental conversion while shopping abroad easy; rates are for reference only.",
        "Visa Requirement Checker",
        "Look up visa requirements for holders of ordinary Chinese passports travelling to various countries and regions (for reference only; official sources prevail)",
        "Travel Plug Guide",
        "Look up the socket type, nominal voltage and frequency for countries and regions worldwide, with a note on the adapter and voltage adaptation needed, for planning safe charging and power use before a trip.",
        "Includes common emergency phrases for travel abroad (getting help, medical care, police) with tap-to-read pronunciation across several languages, for quick reference when language is a barrier.",
        "Targets appear randomly on the board and must be clicked quickly; hit rate and reaction time are tracked to train aim and hand-eye coordination, with best scores recorded. Runs entirely in the browser with no network needed.",
        "About \"Travel Tools\"",
        "This Travel Tools collection gathers 21 free online tools covering the common calculation, conversion and lookup needs of travel scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you will find ready-to-use practical utilities here. All tools run entirely in the browser, never upload data to a server, and protect your privacy.",
        "The travel tools included on this page include (a few representative ones):",
        "These tools help you finish common travel tasks quickly without memorizing complex formulas or converting by hand; enter the values and get the answer.",
        "Do the travel tools require a download or registration?",
        "No. All travel tools on this page are pure front-end online tools: open the page and use them directly. No software to install, no account to register, and no data is uploaded.",
        "Are the calculation results accurate, and is my data safe?",
        "Tools compute locally in your browser based on public mathematical formulas and general industry standards, so results are immediate. All computation happens on your own device, data is never uploaded to a server, and your privacy is protected.",
    ]))
    write('international-tip-calculator', build('international-tip-calculator', [
        "\U0001F9EE International Tip Calculator",
        "Automatically suggest an appropriate tip based on the destination country",
        "Core formula (over the input variables): (tipMin + tipMax) \u00f7 2; bill \u00d7 min \u00f7 100; bill \u00d7 max \u00f7 100",
        "Select Country / Region",
        "\U0001F1FA\U0001F1F8 United States",
        "\U0001F1E8\U0001F1E6 Canada",
        "\U0001F1EA\U0001F1FA Continental Europe",
        "\U0001F1F0\U0001F1F7 South Korea",
        "\U0001F1F8\U0001F1EC Singapore",
        "\U0001F1E6\U0001F1FA Australia",
        "\U0001F1F2\U0001F1FD Mexico",
        "\U0001F1EE\U0001F1F3 India",
        "\U0001F1E7\U0001F1F7 Brazil",
        "\U0001F1E6\U0001F1EA United Arab Emirates",
        "\U0001F1EA\U0001F1EC Egypt",
        "Service Type",
        "\U0001F37D\ufe0f Restaurant",
        "\U0001F3E8 Hotel Service",
        "\U0001F695 Taxi",
        "\U0001F5FA\ufe0f Tour Guide",
        "\U0001F9E3 Porter",
        "\U0001F378 Bar",
        "Currency",
        "Suggested Tip",
        "\U0001F4DA In-Depth Analysis: International Tip Calculator",
        "Splitting a Restaurant Bill",
        "Tip Differences Across Countries",
        "Comparing Service Tiers",
        "$200 US Bill",
        "Choosing the US standard of 15 to 20% gives a tip of $30 to $40, an average of $35, and a total of $235; split four ways that is about $58.75 per person.",
        "Zero Tip in Japan",
        "With Japan min and max both at 0, an $8000 bill gets a tip of 0 and the total is unchanged, roughly 15 to 20% higher than the US for the same amount.",
        "How are the rates set?",
        "Preset ranges follow each country's custom (such as US 15 to 20%, Europe 5 to 10%, Japan 0) and can be switched in the country drop-down.",
        "Does it include currency conversion?",
        "It computes the tip percentage only. The currency is for display; use a separate currency tool for exchange rates.",
        "About \"International Tip Calculator\"",
        "International Tip Calculator. A travel tool that is essential for trips and works offline.",
    ]))
    write('travel-photo-storage', build('travel-photo-storage', [
        "\U0001F5BC\ufe0f Travel Photo Storage Calculator",
        "Estimate the memory card space needed for shooting while travelling",
        "Required storage = photo usage + video usage. Photo usage = days \u00d7 shots per day \u00d7 average size per file (phone about 4 MB, APS-C about 12 MB, full frame about 25 MB, RAW about 40 to 60 MB). Video usage = days \u00d7 minutes shot per day \u00d7 size per minute (1080p about 130 MB/min, 4K about 350 MB/min). Recommended capacity = required \u00d7 1.3 to leave headroom, converted at 1000 MB = 1 GB.",
        "Photos per Day",
        "Camera Type",
        "\U0001F4F1 Phone (3-5MB per photo)",
        "\U0001F4F7 Compact Camera (5-8MB per photo)",
        "\U0001F4F8 APS-C Mirrorless / DSLR (8-15MB per photo)",
        "\U0001F4F7 Full Frame (20-35MB per photo)",
        "\U0001F4F7 Medium Format (50-100MB per photo)",
        "\U0001F4BE RAW+JPEG (about 2x the size)",
        "Video Recording",
        "No Video",
        "1080p 30fps (~45MB/min)",
        "4K 30fps (~400MB/min)",
        "4K 60fps (~600MB/min)",
        "Video Minutes per Day",
        "Estimated Storage Needed",
        "\U0001F4DA In-Depth Analysis: Travel Photo Storage Estimation",
        "Memory Card Capacity",
        "Video Share",
        "Camera Model Differences",
        "Phone, 7 Days at 200 Photos per Day",
        "phone[3,5]MB average 4 gives photos 1400\u00d74 = 5600MB; adding 4k30 video at 30min \u00d7 400MB \u00d7 7 = 84000MB; total \u2248 89600MB \u2248 87.5GB, so a 128GB card is recommended.",
        "Full Frame Uses More Space",
        "fullframe[20,35]MB average 27.5 gives about 38500MB for the same 1400 shots; RAW is counted on top, so the card needs to be larger.",
        "Video Bitrate",
        "1080p30 \u2248 45MB/min, 4k30 \u2248 400MB/min, 4k60 \u2248 600MB/min; choose according to your camera.",
        "Does it include backups?",
        "It computes single-card capacity only. Use two cards or a cloud backup; the tool does not back up your data for you.",
        "About \"Travel Photo Storage Calculator\"",
        "Travel Photo Storage Calculator. A travel tool that is essential for trips and works offline.",
    ]))
    write('packing-list', build('packing-list', [
        "\U0001F4CB Travel Packing List",
        "Categorized packing lists, multiple templates, progress tracking, saved locally",
        "Trip Name",
        "0 / 0 items packed",
        "Total Items",
        "Packed",
        "Not Packed",
        "\U0001F4DD Packing List",
        "\U0001F4CB Select Template",
        "Clear All",
        "Reset List",
        "Choose a trip type template to generate a list quickly",
        "Leisure Vacation",
        "Outdoor Camping",
        "Family Trip",
        "Honeymoon",
        "Backpacking",
        "Winter Skiing",
        "Island Beach",
        "\U0001F4A1 Packing Tips",
        "Luggage rule:",
        "Lay out the list \u2192 spread everything out \u2192 remove half \u2192 pack and go",
        "Folding technique:",
        "Rolling clothes saves more space than folding and reduces creases",
        "Sorting:",
        "Use packing cubes to group clothing by category so it is easy to find",
        "Valuables:",
        "Keep passports, wallets and electronics in your carry-on rather than checked luggage",
        "Liquid limits:",
        "Carry-on liquids are limited to 100ml per container and 1L in total",
        "Emergency preparation:",
        "Carry a change of clothes with you in case checked luggage is delayed",
        "Electronics:",
        "Power banks must be carried in the cabin, not checked, with rated energy no more than 100Wh",
        "First aid kit:",
        "Cold medicine, stomach medicine, adhesive bandages, motion sickness pills and allergy medicine",
        "\U0001F4DC History",
        "\U0001F4DA In-Depth Analysis: Travel Packing List",
        "Generate from a Template",
        "Check Off Progress",
        "Multi-category Stats",
        "3 Categories, 24 Items in Total",
        "Clothing 10, toiletries 8, electronics 6 for 24 items in total; 16 checked off gives progress of 16\u00f724\u00d7100 \u2248 66.7%, with 8 items left.",
        "Custom Add and Remove",
        "You can add items to any category (press Enter to submit); the total and completion rate recalculate live,",
        "progress bar",
        "widens as you check items off.",
        "Where is the data stored?",
        "The list is stored locally in the browser (localStorage) and survives a refresh; history can be cleared to reset.",
        "Are there templates?",
        "Business, family and outdoor templates are built in; load one in a click and then add or remove items.",
        "About \"Travel Packing List\"",
        "Travel Packing List. A travel tool that is essential for trips and works offline.",
    ]))


if __name__ == '__main__':
    main()