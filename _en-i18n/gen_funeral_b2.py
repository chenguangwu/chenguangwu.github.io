#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'funeral')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'funeral')
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
    out = {'slug': slug, 'industry': 'funeral', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # ===== index (20) =====
    en = [
        "⚱️ Funeral Service Tools",
        "Funeral Service",
        "Funeral Service Tools",
        "Estimate ashes amount from the deceased weight (adult about 2-3 kg), compute the required urn internal size and placement space, assisting in choosing a suitable urn and niche.",
        "Sacrifice Date Reminder (by lunar/solar term)",
        "Add sacrifice anniversaries by Gregorian or lunar calendar; auto-convert and show the countdown to the next sacrifice, including 24 solar terms query.",
        "Memorial Service Timeline Planner",
        "Plan the farewell ceremony flow timeline, customize each segment and duration, data saved locally, convenient for arranging check-in and farewell order.",
        "Generate tombstone design by inscription format, including heading title (Gu Xiankao/Gu Xianbi/Xiankao/Xianbi), body and signature layout, for engraving reference.",
        "Compute suitable sacrifice dates like Qingming and Zhongyuan by lunar date and 24 solar terms, and generate death anniversary and memorial reminder lists, helping families arrange mourning and tomb-sweeping time.",
        "Funeral Expense Budget Planner",
        "The funeral expense budget planner is a free online funeral service tool. Basic funeral: body pickup, storage, cremation, ashes storage etc. (some items have government relief exemptions). Runs purely front-end, no data upload, no registration; open the browser and use directly.",
        "About 'Funeral Service Tools'",
        "The Funeral Service Tools collection includes 6 free online tools covering common calculation, conversion and query needs in funeral service scenarios. Whether you are a practitioner, student or ordinary user in the field, you can find ready-to-use mini tools here. All tools run purely front-end, data is not uploaded to servers, protecting privacy and security.",
        "The funeral service tools included on this page are (some representative tools):",
        "These tools help you quickly complete common funeral-service tasks without memorizing complex formulas or manual conversion; enter to get results.",
        "Do the funeral service tools need download or registration?",
        "No. All funeral service tools on this page are pure front-end online tools; open the webpage and use directly, no software install, no account registration, and no data upload.",
        "Are the funeral service tool results accurate? Is data safe?",
        "Tools compute locally in your browser based on public math formulas and general industry standards, results are instant. All computation happens locally on your device, data is not uploaded to servers, privacy and security are guaranteed.",
    ]
    mp = build('index', en); write('index', mp)

    # ===== memorial-date (57) =====
    en = [
        "📅 Sacrifice Date Reminder",
        "Compute sacrifice dates by lunar calendar and solar terms, add death anniversary and memorial reminders",
        "📖 View the usage guide for Suitable Sacrifice Dates and Death Anniversary Reminders",
        "Death anniversary (Gregorian)",
        "Deceased title",
        "Save death anniversary reminder",
        "Clear reminders",
        "📅 Upcoming Sacrifice Dates",
        "📚 Traditional Sacrifice Festivals",
        "Festival",
        "Qingming Festival",
        "Gregorian 4/4 or 4/5",
        "Solar term, the most important sacrifice day",
        "Zhongyuan Festival",
        "Lunar July 15",
        "Commonly called Ghost Festival, honoring ancestors",
        "Hanyi Festival",
        "Lunar October 1",
        "Sending winter clothes to ancestors",
        "New Year's Eve",
        "Last day of lunar December",
        "Year-end ancestor worship",
        "Shangyuan Festival",
        "Lunar January 15",
        "Lantern Festival, ancestor worship in some regions",
        "Death anniversary / yearly",
        "The month and day of passing each year",
        "First 7 days, 100 days, anniversary",
        "First 7 days (Touqi)",
        ": 7 days after passing",
        "Third/Fifth 7 days (Sanqi/Wuqi)",
        ": 21 / 35 days after passing",
        "100 days (Baibai)",
        ": 100 days after passing",
        "Anniversary (Zhounian)",
        ": 1 year and 3 years after passing (varies by custom)",
        "• Lunar-to-Gregorian conversion uses standard calendar algorithm, results are accurate",
        "📚 Deep Dive: Suitable Sacrifice Dates and Death Anniversary Reminders",
        "Qingming/Zhongyuan and other festival arrangements",
        "Death anniversary and memorial reminder list",
        "Lunar and Gregorian conversion",
        "Compute sacrifice days like Qingming (Gregorian about April 4-6) and Zhongyuan (lunar July 15) by lunar calendar or 24 solar terms, and generate death anniversary/memorial reminder lists.",
        "Set death anniversary as Gregorian 2023-03-12, then the 1st anniversary reminder in 2024 is 2024-03-12, 2nd anniversary 2025-03-12; Qingming by that year's solar term about April 4, Zhongyuan is lunar July 15 (corresponding Gregorian August 18, 2024). Reminders are local only.",
        "Is the Qingming date the same every year?",
        "No; Qingming is a solar term, Gregorian about April 4-6 floating, based on that year's solar term moment.",
        "How to convert lunar birthday to Gregorian?",
        "The tool has built-in lunar conversion; enter lunar to get the corresponding Gregorian sacrifice day; results follow the standard lunar calendar.",
        "About 'Sacrifice Date Reminder'",
        "Sacrifice date reminder, computes Qingming, Zhongyuan, Hanyi, New Year's Eve and other sacrifice dates by lunar calendar and solar terms, and supports death anniversary reminders.",
        "Built-in lunar-to-Gregorian algorithm",
        "Touqi, Baibai, anniversary auto-computed",
        "Death anniversary reminder saved locally",
        "Traditional sacrifice festival query",
        "Death anniversary Touqi/Baibai/anniversary reminders",
        "Lunar death anniversary and Gregorian conversion",
        "Sacrifice schedule advance planning",
        "Optional",
    ]
    mp = build('memorial-date', en); write('memorial-date', mp)

    # ===== reminder-3 (49) =====
    en = [
        "📅 Sacrifice Date Reminder (by lunar/solar term)",
        "Add sacrifice anniversaries by Gregorian or lunar calendar; auto-convert and show the countdown to the next sacrifice, including 24 solar terms query.",
        "📖 View the usage guide for Sacrifice Anniversary Countdown",
        "Add by Gregorian",
        "Add by lunar",
        "Repeat yearly",
        "Add reminder",
        "Month 1",
        "Month 2",
        "Month 3",
        "Month 4",
        "Month 5",
        "Month 6",
        "Month 7",
        "Month 8",
        "Month 9",
        "Month 10",
        "Month 11",
        "Month 12",
        "Leap month",
        "Repeat yearly (by lunar)",
        "Countdown to next sacrifice",
        "No reminders yet; please add above.",
        "All sacrifice reminders",
        "Current year's 24 solar terms",
        "Solar terms are often used to determine sacrifice seasons (e.g. Qingming, Dongzhi). The table below is",
        "year solar term dates.",
        "You can add sacrifice anniversaries by Gregorian or lunar calendar; after checking 'repeat yearly' the system auto-computes the next sacrifice date. Each lunar year maps to a different Gregorian date, which the tool auto-converts. Common sacrifice solar terms: Qingming (tomb-sweeping), Zhongyuan (July 15), Dongzhi, New Year's Eve, etc.",
        "📚 Deep Dive: Sacrifice Anniversary Countdown",
        "Daily mourning reminder",
        "Solar term sacrifice arrangement",
        "Multi-anniversary management",
        "Add Gregorian or lunar sacrifice day; the tool converts and shows the",
        "countdown",
        "to the next sacrifice, with built-in 24 solar terms query to assist arrangement.",
        "Set death anniversary on March 12 yearly, current October 12 → about 153 days to next; adding lunar October 1 (Hanyi Festival) adds another parallel countdown. Countdown computed locally, no network.",
        "Will it push notifications?",
        "Pure front-end only shows countdown, no push; you can manually set phone reminders.",
        "Is the lunar date accurate?",
        "Converted by standard lunar calendar; solar terms follow astronomical algorithm; extreme years corrected by authoritative almanac.",
        "About 'Sacrifice Date Reminder (by lunar/solar term)'",
        "Sacrifice date management reminder tool, supports adding anniversaries by Gregorian or lunar calendar, auto-converts lunar and Gregorian, repeats yearly, with built-in current-year 24 solar terms query, helping you sacrifice on time and remember the departed.",
        "Supports Gregorian and lunar input",
        "Lunar auto-converts to Gregorian (covers 1900-2099)",
        "Repeat yearly, auto-compute next sacrifice date",
        "Built-in current-year 24 solar term date query",
        "Next sacrifice countdown reminder",
        "e.g.: late father's death anniversary",
        "e.g.: Qingming sacrifice",
    ]
    mp = build('reminder-3', en); write('reminder-3', mp)

    # ===== urn-size (48) =====
    en = [
        "🧮 Urn Size Calculator",
        "Estimate ashes amount from weight, compute required urn size and placement space",
        "📖 View the usage guide for Urn Size Estimation",
        "Adult ashes amount is about 2% to 3% of body weight (a 60 kg person about 1.5 to 2 kg, volume 2 to 3 L); required urn volume = ashes volume × (1 + 30% margin); the inner size must hold the ashes bag, common inner dimensions length 20 to 30 cm, width 15 to 20 cm, height 15 to 20 cm; each 10 kg increase in body weight adds about 0.4 L volume; before placement verify the niche inner diameter matches the urn outer diameter, and reserve space for opening and decorative parts.",
        "Deceased weight (kg)",
        "Cremation method",
        "Standard cremation",
        "High-temperature cremation (finer ashes)",
        "Placement method",
        "Placement type",
        "Urn rack (niche)",
        "Grave burial",
        "Home temporary storage",
        "Urn material",
        "Wooden",
        "📖 Ashes Amount and Size Notes",
        "Ashes amount estimate",
        ": adult ashes about 2-3 kg, positively correlated with body weight",
        "Ashes density",
        ": about 1.0-1.2 g/cm³, high-temperature cremation finer with slightly higher density",
        "Urn volume",
        ": recommended 1.5-2 times the ashes volume for easy storage",
        "Common urn sizes",
        ": length about 25-35 cm, width about 18-25 cm, height about 18-25 cm",
        "Urn rack niche",
        ": common single niche about 35 cm × 30 cm × 30 cm",
        "Joint burial",
        ": double-grave joint burial needs a double urn or two separate urns",
        "• Actual ashes amount is affected by cremation furnace temperature and duration; choose a slightly larger size",
        "📚 Deep Dive: Urn Size Estimation",
        "Urn purchase reference",
        "Niche space matching",
        "Estimate ashes by body weight",
        "Adult ashes about 2-3 kg (about 3-4% of body weight); estimate ashes amount by body weight, then give urn inner volume and side-length suggestions.",
        "Deceased weight 65 kg → ashes about 65×0.04 ≈ 2.6 kg (within 2-3 kg range); choose an urn with inner volume ≥ 3 L (about 15×15×14 cm inner cavity) to place, and match the niche space accordingly. For purchase reference only.",
        "Is the ashes amount fixed?",
        "Varies by person, about 3-4% of body weight, also affected by cremation temperature and duration; 2-3 kg is the common adult range, not a precise value.",
        "How much larger should the urn be than the ashes?",
        "Leave 10-20% margin for placement and padding; base on actual ashes amount and urn inner cavity size.",
        "About 'Urn Size Calculator'",
        "Urn size calculator, estimates ashes amount from deceased weight and height, deriving urn inner/outer diameter and placement space needs.",
        "Weight and height dual-parameter ashes estimate",
        "Supports different cremation methods and materials",
        "Auto-compute urn rack niche space",
        "Urn purchase size reference",
        "Urn rack niche reservation",
        "Grave space planning",
        "Joint burial space assessment",
    ]
    mp = build('urn-size', en); write('urn-size', mp)

if __name__ == '__main__':
    main()
