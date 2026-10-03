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
    write('appliance-cycle', build('appliance-cycle', [
        "\u23F1\uFE0F Home Appliance Cleaning Cycle Schedule",
        "Record each appliance's last cleaning time and auto-remind the next deep-cleaning date (data saved locally)",
        "\U0001F4D6 View the User Guide for Home Appliance Cleaning Cycle Schedule",
        "Next clean date = last clean date + suggested cycle (days); reference cycles: AC filter 1 month, range hood 3 months, fridge 3-6 months, washing machine 3 months, water heater 6-12 months, water dispenser 1-2 months; overdue days = current date - next clean date, positive means a reminder is due; on-time completion rate = completed cleans / due items x 100%.",
        "View Reminder Date",
        "Reset All Records",
        "Copy Cleaning Plan",
        "\U0001F4D6 Deep-Cleaning Instructions",
        ": wash the filter monthly, deep-clean the evaporator 1-2 times a year",
        "Washing Machine",
        ": clean the inner drum with detergent each quarter, wipe the door seal dry weekly",
        "Range Hood",
        ": soak and wash the filter monthly, deep disassembly wash once a year",
        "Refrigerator",
        ": power off and defrost-wash each quarter, wipe the gasket monthly",
        "Water Heater",
        ": wash the inner tank every six months, replace the magnesium rod",
        "Water Dispenser",
        ": clean the interior monthly, disinfect quarterly",
        "\u2022 Use a dedicated cleaner to avoid damaging appliance parts",
        "\U0001F4DA In-depth: Home Appliance Cleaning Cycle Schedule",
        "When a homemaker or cleaning staff plans a monthly cleaning schedule, tick items off this table one by one to avoid missing high-grease appliances (e.g. range hood, stove).",
        "When moving out of a rental, or",
        "before move-in deep-clean acceptance, cross-check the cycle table to confirm which appliances need disassembly wash and deodorising first.",
        "For a newly bought appliance's first maintenance, set a reminder referencing the suggested cycle to prevent early wear such as mouldy gaskets or clogged filters.",
        "Example Cleaning Cycles for Range Hood and Refrigerator",
        "Range hood: wipe the surface weekly, disassemble and degrease the interior each quarter; refrigerator: tidy expired food weekly, defrost quarterly and deodorise with baking-soda water. The output is an actionable monthly cleaning checklist.",
        "How often should the AC be cleaned?",
        "Vacuum and wash the filter every 2 weeks, professionally clean the evaporator and fan wheel each season, and do a full deep maintenance about once a year; frequent-use or pet-owning households can increase the frequency.",
        "Can this cycle table be used directly as an acceptance standard?",
        "It can serve as a reference baseline, but adjust for local water quality, grease volume and usage intensity; acceptance should be based on actual cleanliness and odour, not mechanically applying the cycle.",
        "How often should the washing machine be cleaned?",
        "Run the inner drum on the tub-clean cycle empty about once a month, wipe the door gasket dry weekly to prevent mould, clean the inlet-valve filter each season, and air-dry the drum before long idle periods.",
        "About Home Appliance Cleaning Cycle Schedule",
        "Home Appliance Cleaning Cycle Schedule covers 14 common appliances, records cleaning times and auto-reminds due and upcoming items, with cleaning-method notes.",
        "Cleaning-cycle management for 14 appliance types",
        "One-click record today's cleaning",
        "Home appliance cleaning management",
        "Cleaning-company service scheduling",
        "Property appliance maintenance plan",
        "Deep-cleaning cycle reminders",
    ]))
    write('area-hours', build('area-hours', [
        "\U0001F52E Cleaning Man-Hour Estimator",
        "Estimate required man-hours and staffing based on cleaning area and type",
        "\U0001F4D6 View the User Guide for Cleaning Man-Hour Estimator",
        "Required man-hours (h) = cleaning area (m2) / per-person efficiency (m2/h) x dirt coefficient; per-person efficiency by type (daily cleaning 200-300 m2/h, deep cleaning 40-80 m2/h, post-construction cleaning 20-40 m2/h); dirt coefficient: light 1.0, medium 1.3, heavy 1.8; required staff = total hours / planned duration, per-person hours = total hours / staff.",
        "Number of Cleaners",
        "Dirt Level",
        "Fairly dirty",
        "Very dirty",
        "Severe soiling",
        "Cleaning Type",
        "\U0001F4D6 Man-Hour Estimation Notes",
        "Daily Cleaning",
        ": about 8-12 min/m2, including floor, desk and basic restroom cleaning",
        "Post-Construction Cleaning",
        ": about 15-25 min/m2, first full cleaning after renovation",
        "Deep Cleaning",
        ": about 12-20 min/m2, including deep kitchen/restroom and glass",
        "Exterior Wall Washing",
        ": about 3-8 min/m2, requires professional equipment and high-altitude work",
        "Carpet Cleaning",
        ": about 5-10 min/m2, including pre-spray, extraction and drying",
        "\u2022 Actual man-hours are affected by layout, belongings and equipment efficiency",
        "\u2022 Suggest 2-3 people per team to improve efficiency and safety",
        "\U0001F4DA In-depth: Cleaning Man-Hour Estimator",
        "When bidding or quoting a monthly contract, first estimate person-hours by area and zone type, then multiply by unit price for the quote, avoiding missed items from guesswork.",
        "For a newly delivered building's post-construction cleaning, compute the schedule by area and heavy-soil coefficient to decide how many people and days are needed.",
        "For temporary extra cleaning before/after large events, quickly estimate the relief cleaners needed from foot traffic and soiling.",
        "Example: 1000 m2 Office Daily Cleaning Man-Hours",
        "Choose office zone type and light soiling; at a baseline of about 0.02 person-hours/m2, estimate about 20 person-hours; with two shifts, about 2-3 people work one day.",
        "What dirt coefficient is generally used?",
        "Daily light soiling about 1.0, medium soiling 1.3-1.5, post-construction or heavy grease 1.8-2.0; final value by on-site survey.",
        "Does the estimate include time to replace consumables?",
        "By default it includes only cleaning labour hours, not auxiliary time like fetching, replenishing trash bags and cleaner, or charging equipment; add those separately.",
        "Are exterior or high-altitude jobs included?",
        "No. This tool targets indoor flat-surface cleaning; exterior walls and high-altitude glass are specialised jobs, calculated separately by facade area and safety level.",
        "About Cleaning Man-Hour Estimator",
        "Cleaning Man-Hour Estimator estimates total and per-person man-hours from area, type and dirt level, aiding staffing and schedule planning.",
        "8 selectable cleaning types",
        "Adjustable dirt-level coefficient",
        "Auto-calculates per-person hours and schedule",
        "Cleaning-company quoting and scheduling",
        "Housekeeping staffing planning",
        "Post-construction cleaning schedule assessment",
        "Personal post-renovation cleaning budget",
    ]))
    write('checker-10', build('checker-10', [
        "\u2696\uFE0F Cleaning Quality Inspection and Assessment Scoring",
        "Inspect cleaning quality item by item by zone, 0-5 points each, auto-compute zone scores and overall assessment score, and give reward/penalty suggestions per the reward-penalty system.",
        "Quality (Inspection / Assessment / Reward-Penalty) System",
        "/ Quality (Inspection / Assessment / Reward-Penalty) System",
        "\U0001F4D6 View the User Guide for Cleaning Quality Inspection and Assessment Scoring",
        "Overall assessment score = sum of zone averages / number of zones x 20",
        "Generate Assessment Result",
        "Score each item by cleaning quality: 0=not done / 1=very poor / 2=poor / 3=fair / 4=good / 5=excellent",
        "Overall assessment score = sum of zone averages / number of zones x 20 (converted to a 100-point scale)",
        ">=90 excellent (reward), 80-89 good, 70-79 pass, <70 fail (penalty)",
        "Items scored 0 are listed as serious deductions and must be corrected immediately",
        "\U0001F4DA In-depth: Cleaning Quality Inspection and Assessment Scoring",
        "During monthly assessment of an outsourced cleaning company, the client inspects and scores 10 items one by one as the basis for payment and contract renewal.",
        "The cleaning team self-checks and rectifies, treating low-score items as priorities, forming a closed-loop record.",
        "Before a new project moves in, use a unified standard to confirm the delivered cleanliness meets the bar.",
        "Example: 10-Item Score Summary",
        "Each item 0-10: floor 9, glass 8, restroom 7, trash 10, odour 8, furniture 9, skirting 7, fixtures 8, signage 10, safety 9, total 85, grade B (above pass).",
        "Are the 10 items equally weighted?",
        "By default each item is equally weighted at 10 points; you can also set higher weights for high-risk items like restrooms and floors in the table, per contract.",
        "What score counts as passing?",
        "Usually total >=80 is pass, >=90 is excellent; below 80 requires time-bound rectification and re-inspection; the exact threshold is set by the client.",
        "How to record deductions effectively?",
        "Suggest photo location + text description +",
        ", serving as both the assessment basis and facilitating traceable rectification, avoiding verbal disputes.",
        "About Cleaning Quality Inspection and Assessment Scoring",
        "A quality-inspection and assessment tool for property and cleaning-service companies, scoring item by item across four zones - floor, restroom, glass/doors and public facilities - and auto-generating assessment scores and reward/penalty suggestions.",
        "15-item checklist across four zones",
        "Quantified 0-5 scoring",
        "Auto-identifies serious deductions (score 0)",
        "Reward/penalty suggestions by score",
        "Monthly property cleaning quality assessment",
        "Cleaning-company project acceptance check",
        "Cleaner performance assessment",
        "Cleaning-service quality improvement",
    ]))

if __name__ == '__main__':
    main()
