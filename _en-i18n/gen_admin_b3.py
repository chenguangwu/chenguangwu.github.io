#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'admin')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'admin')
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
    out = {'slug': slug, 'industry': 'admin', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('supplies-forecast', build('supplies-forecast', [
        "\U0001F52E Office-Supplies Consumption Forecast",
        "Enter historical monthly consumption and use the moving-average method to forecast next month's demand, aiding procurement planning",
        "Core calculation formula (by input variables): i-maWin+1",
        "Office-Supplies Forecast",
        "/ Office-Supplies Forecast",
        "\U0001F4D6 View the User Guide for Office-Supplies Consumption Forecast",
        "Item Name",
        "Moving-Average Window (months)",
        "Safety-Stock Coefficient",
        "Historical Consumption Data (monthly usage)",
        "\u2795 Add Month",
        "\U0001F4CB Forecast Detail",
        "Actual Consumption",
        "Moving-Average Method",
        ": take the arithmetic mean of the most recent N months' actual consumption as next month's forecast. A larger window is smoother but lags; a smaller window is more sensitive but more volatile.",
        "\U0001F4DA In-depth: Office-Supplies Consumption Forecast",
        "Enter monthly issuance of A4 paper, toner cartridges, etc., forecast next month's demand with moving average, and combine with the safety-stock coefficient to set the reorder point, avoiding stockouts or overstock.",
        "When preparing the quarterly procurement budget, trend-forecast high-frequency consumables as a basis for price negotiation and volume locking with suppliers.",
        "During volatile periods such as outbreaks or promotions, enlarge the moving-average window to smooth anomalous months and prevent a single-month spike from misleading procurement volume.",
        "A4 Paper Next-Month Consumption and Safety Stock",
        "A4 paper consumption over the last 6 months: 12,14,11,13,15,12 (boxes). With a moving-average window of 3, the recent three-month mean = (13+15+12)/3 ≈ 13.33 boxes; with a safety-stock coefficient of 1.2, safety stock ≈ 16 boxes. Next month, recommend stocking about 'forecast 13.33 + safety 16' ≈ 29 boxes, after deducting current inventory.",
        "How to choose the moving-average window?",
        "A smaller window is more sensitive (tracks recent fluctuation); a larger window is smoother (resists single-month anomalies). For stable consumables a 3-6 month window suffices; for pronounced seasonality or promotion spikes, enlarge the window or forecast by segment. The window only affects smoothing, not the historical data.",
        "What does the safety-stock coefficient represent?",
        "The coefficient scales 'forecast demand' up into a 'stocking target', covering uncertain consumption during the lead time. A coefficient of 1.2 means stocking 20% more on top of the forecast. A larger coefficient reduces stockout risk but ties up more capital; set it by weighing supply lead time against stockout cost.",
        "About Office-Supplies Forecast",
        "Office-Supplies Forecast is an online tool in the business-office domain. Business-office tools boost work efficiency, with data processed locally to protect privacy.",
    ]))
    write('travel-subsidy', build('travel-subsidy', [
        "\U0001F9EE Domestic Travel Subsidy Calculator",
        "Calculate travel subsidy by destination city category and number of days, including meal allowance, transport allowance and accommodation cap",
        "\"Calculate travel subsidy by destination city category and number of days, including meal allowance, transport allowance and accommodation cap\" - professional calculation and result output based on input parameters.",
        "Travel Subsidy Calculator",
        "/ Travel Subsidy Calculator",
        "\U0001F4D6 View the User Guide for Domestic Travel Subsidy Calculator",
        "Meal Allowance Standard (CNY/day)",
        "Local Transport Allowance (CNY/day)",
        "Travel City Details",
        "\u2795 Add City",
        "\U0001F4CB Subsidy Detail Table",
        "Meal Allowance",
        "Transport Allowance",
        "Accommodation Cap/day",
        "Total Accommodation Cap",
        "\U0001F4CA City-Category Accommodation Cap Reference",
        "City Category",
        "Representative Cities",
        "Accommodation Cap (CNY/day)",
        "Tier-1 Cities",
        "Beijing, Shanghai",
        "Tier-2 Cities",
        "Guangzhou, Shenzhen, Hangzhou, Nanjing",
        "Tier-3 Cities",
        "Provincial Capitals and Sub-Provincial Cities",
        "Tier-4 Cities",
        "Other Cities",
        "Subsidy standards are reference values, subject to your unit's travel policy. Meal and transport allowances are calculated by actual travel days; accommodation is reimbursed within the cap on a real-cost basis.",
        "\U0001F4DA In-depth: Domestic Travel Subsidy Calculator",
        "When sales or implementation staff claim travel reimbursement, apply meal and local-transport allowance standards by destination city category and travel days; the tool auto-sums the total subsidy, reducing manual table lookups.",
        "For on-site or long-term business trips, enter different cities and days by segment and total the subsidy, easing reconciliation with finance.",
        "For training, conference and other travel accounting, distinguish the different allowance tiers of 'with meals/lodging' versus 'transport only' to avoid omission or exceeding standards.",
        "Tier-1 City 5-Day Travel Subsidy",
        "Destination: tier-1 city, 5 days, meal allowance 100 CNY/day, local transport allowance 80 CNY/day. Total subsidy = (100+80) x 5 = 900 CNY. If the host provides meals for 2 of those days, the meal allowance counts 3 days = 300 CNY, total 540 CNY, reflecting the principle of 'reimbursement on actual cost, no duplicate collection'.",
        "What are the subsidy standards based on?",
        "Travel allowance standards vary by region and unit, usually tiered by city category (e.g. tier-1 / tier-2 / other) and job grade, subject to your unit's travel policy and finance-department standards. The tool only does arithmetic aggregation; enter the actually enforced values for the specific standards.",
        "Can I still receive the allowance if the host arranges meals and lodging?",
        "General rule: when the host unit covers meals, no meal allowance is paid; the same applies to transport. The tool supports per-day separate payment; when filing, deduct actual covered days to avoid claiming above standard.",
        "About Travel Subsidy Calculator",
        "Travel Subsidy Calculator is an online tool in the business-office domain. Business-office tools boost work efficiency, with data processed locally to protect privacy.",
    ]))
    write('version-control', build('version-control', [
        "\U0001F5C2\uFE0F File Version Management",
        "Record file version numbers, revision notes and author, support semantic versioning (SemVer), and store data locally in the browser",
        "\U0001F4D6 View the User Guide for File Version Management",
        "File Name",
        "Version Type",
        "Patch (0.0.X)",
        "Minor (0.X.0)",
        "Major (X.0.0)",
        "Suggested Version",
        "Revisor",
        "Revision Notes",
        "\u2795 Publish New Version",
        "\U0001F504 Auto-Suggest Version",
        "\U0001F4C2 Version History",
        "\U0001F4E4 Export JSON",
        "Semantic Versioning",
        "MAJOR: incompatible API changes; MINOR: backward-compatible feature additions; PATCH: backward-compatible bug fixes",
        "Data is stored in the browser's localStorage; clearing browser data will lose it, so please export a backup promptly.",
        "\U0001F4DA In-depth: File Version Management",
        "After each revision of a requirements doc or design, bump the version among 'patch / minor / major' and auto-suggest the version number, keeping the team's nomenclature consistent.",
        "When a design undergoes an incompatible major revision, use a Major bump and prompt to notify downstream synchronously, avoiding misuse of the old version.",
        "Small fixes like weekly reports or meeting minutes use a Patch bump - leaving a trace without raising version expectations.",
        "Three Bump Types from 1.2.3",
        "Current version 1.2.3: choose 'Patch' -> 1.2.4 (typo fix / minor tweak); choose 'Minor' -> 1.3.0 (add a requirements section, lower digits reset to zero); choose 'Major' -> 2.0.0 (overall restructure, minor/patch digits reset to zero). The tool also records the revisor and revision notes, forming a traceable version chain.",
        "How to read semantic versioning (SemVer)?",
        "Format is major.minor.patch (X.Y.Z). A major change means incompatible changes, a minor change means backward-compatible new features, a patch change means backward-compatible bug fixes. When a lower digit bumps, higher digits reset to zero (e.g. 1.3.1 follows 1.3.0).",
        "How to avoid version chaos when multiple people edit one document?",
        "Agree that 'whoever edits bumps the version and fills revision notes', and a major change must notify all collaborators; pair with a shared drive or Git-style concurrency lock, pulling latest before editing. The tool generates standard version numbers and traces, not replacing the collaboration workflow.",
        "About File Version Management",
        "File Version Management is an online tool in the business-office domain. Business-office tools boost work efficiency, with data processed locally to protect privacy.",
        "e.g. 1.2.3",
        "Describe this revision...",
    ]))

if __name__ == '__main__':
    main()
