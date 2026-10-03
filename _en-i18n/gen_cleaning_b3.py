#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'cleaning')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'cleaning')
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
    out = {'slug': slug, 'industry': 'cleaning', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('index', build('index', [
        "\U0001F9F9 Cleaning Tools",
        "Cleaning",
        "Cleaning Tools",
        "Cleaner Dilution-Ratio Calculator computes dilution ratio, concentrate and water volumes for various cleaners, standardising ratios and avoiding waste.",
        "Cleaning-Supplies Consumption Calculator estimates usage and reorder cycle by area and frequency, aiding property consumables procurement and inventory.",
        "Cleaning Staff Weekly Schedule Manager supports morning/mid shifts and rest switching, auto-totalling each person's workload and balance.",
        "Cleaning Man-Hour Estimator estimates required man-hours and staffing by area and type, aiding cleaning scheduling and quoting.",
        "Quality (Inspection / Assessment / Reward-Penalty) System",
        "Score cleaning quality item by item by zone and item, output overall assessment score (100-point) and grade, linked to reward/penalty suggestions, for cleaning-service assessment management.",
        "Process (Standardization / Operation / Inspection) Formulation",
        "Assess cleaning-process standardization across three modules - SOP formulation, operation spec, inspection standard - with 15 key points, outputting a percentage and grade to improve the system.",
        "Manage carpet vacuum, deep wash and dry cycles. Recommend care frequency by type and intensity, track maintenance due dates, with a common-stain guide.",
        "Record each appliance's last cleaning time and auto-remind the next deep-cleaning date, covering many common appliances, with data saved locally.",
        "About Cleaning Tools",
        "The Cleaning Tools collection contains 8 free online tools covering common calculation, conversion and lookup needs in cleaning scenarios. Whether you are a practitioner, student or ordinary user in the field, you can find ready-to-use small tools here. All tools run entirely in the browser, upload no data to the server, and protect your privacy and security.",
        "The cleaning tools on this page include (representative selection):",
        "These tools help you quickly complete common cleaning tasks without memorising complex formulas or doing manual conversions; just enter to get results.",
        "Do the cleaning tools need to be downloaded or registered?",
        "No. All cleaning tools on this page are pure front-end online tools; open the web page to use them directly, with no software installation, no account registration, and no data upload.",
        "Are the cleaning tools' results accurate? Is the data safe?",
        "The tools calculate locally in your browser based on public mathematical formulas and general industry standards, with results available instantly. All computation is done locally on your device, data is never uploaded to the server, and your privacy and security are protected.",
    ]))
    write('staff-schedule', build('staff-schedule', [
        "\U0001F9F9 Cleaning Shift Schedule",
        "Manage cleaning staff weekly shifts, auto-totalling each person's workload and balance (data saved locally)",
        "\U0001F4D6 View the User Guide for Cleaning Shift Schedule",
        "Weekly schedule by shift: per-person weekly hours = sum of shift durations (morning and mid shifts 8 h each, rest 0); per-person hours = total hours / staff; workload balance = 1 - (per-person hours std dev / per-person hours mean), closer to 1 is more balanced; each person rests at least 1 day per week, no more than 6 consecutive workdays; when short-staffed, add relief by absence rate = absent person-times / scheduled person-times x 100%.",
        "Add Staff",
        "Auto-Schedule",
        "Staff and Workload",
        "\U0001F4D6 Scheduling Notes",
        "Shift A",
        ": morning shift 07:00-15:00, responsible for daily cleaning",
        "Shift B",
        ": mid shift 15:00-23:00, responsible for maintenance cleaning",
        "Rest",
        ": rest day, suggest at least 1 rest day per person per week",
        "\u2022 Auto-schedule assigns each person 6 workdays and 1 rotating rest day per week",
        "\u2022 Task volume is computed from responsible area and scheduled days",
        "\u2022 Click a table cell to manually adjust the shift",
        "\U0001F4DA In-depth: Cleaning Shift Schedule",
        "Mall cleaning schedule: add reinforced shifts around peak hours (before open, after close), keep midday patrol.",
        "Office night shift for trash collection and common-area upkeep, off-peak from daytime inspection, reducing tenant disturbance.",
        "Before holidays or large events, add temporary shifts by estimated foot traffic and assign relief staff.",
        "Example: 5 People, Three Shifts, 8 Zones",
        "Morning 2 people prep zones 1-3 before open, mid 2 patrol zones 4-6, evening 1 closes zones 7-8 and collects trash; each person no more than 8 h/day, rest interval >=11 h.",
        "How to avoid consecutive-shift overwork?",
        "Set a minimum rest interval (e.g. >=11 h between shifts) and a daily hours cap; the schedule auto-flags conflicts in red for manual review and adjustment.",
        "How to schedule a multi-skilled person?",
        "Tag multi-skills in staff attributes (e.g. high-altitude, equipment), and prioritise assigning them to zones needing that skill, improving coverage efficiency.",
        "Who covers a temporary absence?",
        "Maintain an available relief pool, backfill by zone familiarity nearby, and sync the responsibility-zone tags to avoid missed zones.",
        "About Cleaning Shift Schedule",
        "Cleaning Shift Schedule manages weekly shifts for cleaning staff, supports morning/mid/rest switching, and auto-totals workload and balance.",
        "Click a cell to switch shift",
        "One-click auto-schedule generation",
        "Workload and area statistics",
        "Property cleaning weekly schedule management",
        "Cleaning-company staff dispatch",
        "Workload balance analysis",
        "Housekeeping team task assignment",
        "Staff name",
        "Responsible area (m2)",
    ]))
    write('supply-usage', build('supply-usage', [
        "\U0001F9EE Cleaning-Supplies Consumption Calculator",
        "Estimate consumption and reorder cycle of various cleaning supplies by area and frequency",
        "Core formula (by input variables): Math.ceil(totalNeed / s.packSize)",
        "\U0001F4D6 View the User Guide for Cleaning-Supplies Consumption Calculator",
        "Cleaning Frequency",
        "Once daily",
        "Twice daily",
        "Every 2 days",
        "Twice weekly",
        "Weekly",
        "\U0001F4D6 Consumption Reference",
        "All-Purpose Cleaner",
        ": about 2-3 ml/m2, used diluted",
        "Glass Cleaner",
        ": about 1-2 ml/m2, spray and wipe",
        "Disinfectant",
        ": about 1-2 ml/m2, focus on restroom and kitchen",
        "Hand Soap",
        ": about 0.5-1 ml per use per person",
        "Trash Bags",
        ": 1-2 per bin per day",
        "Cleaning Cloths / Mops",
        ": replace or wash about once weekly",
        "\u2022 Actual consumption is affected by soiling level and operating habits",
        "\U0001F4DA In-depth: Cleaning-Supplies Consumption Calculator",
        "A property team prepares the monthly cleaning-consumables procurement budget, estimating each category's usage by managed area and foot traffic.",
        "Set warehouse stock and reorder points to avoid stockouts that halt work or overstock that expires (e.g. disinfectant shelf life).",
        "Cost-control review: compare actual issuance with the estimate to find waste or uncounted steps.",
        "Example: 5000 m2 Monthly Trash-Bag Use",
        "Public area about 1 bag per 100 m2 per day, over 30 days 5000 m2 is about 1500/month; times a foot-traffic factor (e.g. 1.3) gives about 1950; stock accordingly with a 10% safety buffer.",
        "How to adjust for high foot traffic?",
        "Multiply the baseline by a foot-traffic factor; high-frequency zones like subway entrances and mall atria take 1.3-1.5, low-frequency offices take 1.0-1.1.",
        "Does the estimate include equipment wear?",
        "By default only consumables (trash bags, cleaners, mops, gloves, etc.) are counted, not dust pushers or scrubbers' depreciation; equipment goes in a separate asset ledger.",
        "How to reduce consumable waste?",
        "Adopt measured issuance and trade-in, mix concentration on demand (avoid excess cleaner), and replace disposable mops with reusable ones to significantly cut consumption.",
        "About Cleaning-Supplies Consumption Calculator",
        "Cleaning-Supplies Consumption Calculator estimates consumption of 10 common cleaning supplies by area, frequency and cycle, with safety-stock and procurement suggestions.",
        "Consumption statistics for 10 cleaning supplies",
        "Supports custom frequency and cycle",
        "Auto safety-stock calculation",
        "Cleaning-company consumables procurement",
        "Property cleaning budget planning",
        "Cleaning-supplies inventory management",
        "Home cleaning-supplies stocking",
    ]))

if __name__ == '__main__':
    main()
