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
    # ===== ceremony-timeline (46) =====
    en = [
        "📜 Memorial Service Timeline Planner",
        "Plan the farewell ceremony flow timeline, customize segments and durations (data saved locally)",
        "📖 View the usage guide for Memorial Service Flow Timeline",
        "Ceremony start time",
        "Farewell hall size",
        "Small (under 30 people)",
        "Medium (30-100 people)",
        "Large (over 100 people)",
        "Add segment",
        "Load standard flow",
        "Copy timeline",
        "📖 Memorial Service Flow Description",
        "Check-in and welcome",
        ": guests sign in, wear white flowers and black armbands, about 15-30 minutes",
        "Farewell ceremony",
        ": host announces start, moment of silence, eulogy, about 15-20 minutes",
        "Body farewell",
        ": guests circle the casket once to pay respects, depends on number of attendees",
        "Family thanks",
        ": family gives thank-you speech, about 5-10 minutes",
        "Procession and cremation",
        ": hearse sees off, proceed to crematorium",
        "• Large memorials need extra segments like attendee representative speeches and memorial video playback",
        "• Customs vary by region; adjust the flow to actual conditions",
        "📚 Deep Dive: Memorial Service Flow Timeline",
        "Farewell ceremony flow arrangement",
        "Check-in and farewell order arrangement",
        "Multi-segment duration coordination",
        "Add each segment name and duration from the start time; the tool lays out the timeline by accumulation, helping control overall pace and transitions.",
        "09:00 check-in (30min) → 09:30 remembrance (40min) → 10:10 body farewell (20min) → 10:30 ceremony end and photo (10min), total about 100 minutes; if remembrance is compressed to 25 minutes it ends at 10:15. Timeline saved locally.",
        "Can I change the segment name?",
        "You can customize each segment's name and duration; the timeline rearranges in real time.",
        "Will the data be lost?",
        "Stored in the browser locally; clearing cache will erase it, so screenshot or print for safekeeping is recommended.",
        "About 'Memorial Service Timeline Planner'",
        "Memorial service timeline planner, arranges each farewell ceremony segment in time order, auto-computes duration, supports customization and standard flow templates.",
        "Visual timeline display",
        "Auto-arrange by duration",
        "Built-in small/large flow templates",
        "Memorial farewell ceremony planning",
        "Reasonable duration per segment",
        "Confirm flow with family",
        "Funeral service flow reference",
        "Segment name",
        "Duration (minutes)",
        "Description (optional)",
    ]
    mp = build('ceremony-timeline', en); write('ceremony-timeline', mp)

    # ===== funeral-budget-planner (37) =====
    en = [
        "💰 Funeral Expense Budget Planner",
        "Plan funeral expenses by category, auto-sum the budget (data saved locally)",
        "📖 View the usage guide for Funeral Expense Budget Summary",
        "💰 Funeral Expense Budget Planner",
        "Basic funeral",
        "Ritual and mourning hall",
        "Cemetery burial",
        "Service fees",
        "Load reference budget",
        "Budget item details",
        "📖 Expense Reference Notes",
        ": body pickup, storage, cremation, ashes storage etc. (some items have government relief exemptions)",
        ": burial clothes, mourning hall setup, farewell ceremony, wreaths and baskets, band",
        ": cemetery/grave, tombstone engraving, burial ceremony, burial goods",
        ": funeral service, host, video, catering reception",
        "• Prices and customs vary greatly by region; budget is for planning reference only",
        "• Reserve 10% of total budget as contingency",
        "📚 Deep Dive: Funeral Expense Budget Summary",
        "Clarify each expense before funeral",
        "Compare and plan multiple options",
        "Family jointly verify accounts",
        "Fill expenses row by row by category: body pickup, cremation, ashes storage, ritual setup, etc.; the tool summarizes by category and saves locally for checking the total anytime.",
        "Pickup 800 + cremation 1200 + ashes storage 300 + farewell ritual 2000 + catering misc 1000 = total 5300 CNY; checking 'simple handling' to remove ritual and catering gives about 2300 CNY, the difference is clear at a glance. Data is saved locally only.",
        "Will the expenses be uploaded?",
        "No upload; all stored in the browser locally; keep the page open and do not clear cache to retain.",
        "Can I export the list?",
        "You can copy or print the page; pure front-end has no cloud export, keep it yourself as needed.",
        "About 'Funeral Expense Budget Planner'",
        "Funeral expense budget planner, plans expenses by basic funeral, ritual hall, cemetery burial etc., auto-sums and gives contingency suggestions.",
        "Five major expense category statistics",
        "Built-in reference budget template",
        "Funeral expense advance planning",
        "Expense category statistics and verification",
        "Budget reasonableness assessment",
        "Multi-plan expense comparison",
        "Item name (e.g.: urn)",
        "Amount (CNY)",
    ]
    mp = build('funeral-budget-planner', en); write('funeral-budget-planner', mp)

    # ===== grave-design (54) =====
    en = [
        "📐 Cemetery Tombstone Inscription Designer",
        "Design inscription layout and estimate cemetery area, with preview of inscription effect",
        "📖 View the usage guide for Tombstone Design and Inscription Layout",
        "The tombstone layout follows field types: heading title (Gu Xiankao, Gu Xianbi, Xiankao, Xianbi) + deceased name + birth and death dates + erector + erection time; slab face area = slab width × slab height, text area height = slab height × 0.6 to 0.7, with 15% margin top and bottom; cemetery area = site length × width, common single grave about 0.5 to 1 m², double grave 1 to 1.5 m²; character spacing = (text area width - total text width) ÷ (character count + 1).",
        "Inscription content",
        "Inscription heading (e.g.: Gu Xiankao)",
        "Inscription template",
        "Father inscription",
        "Mother inscription",
        "Joint burial inscription",
        "Minimal inscription",
        "Birth year (lunar)",
        "Death year (lunar)",
        "Inscription body / epitaph",
        "A diligent father who managed the household thriftily, with virtue flowing to descendants. Passed away suddenly on a certain day of a certain month in 2023, aged 78. This stele is erected in eternal memory, to show remembrance.",
        "Cemetery specs",
        "Tombstone width (m)",
        "Tombstone height (m)",
        "Cemetery site length (m)",
        "Cemetery site width (m)",
        "Generate preview",
        "Copy inscription",
        "📖 Inscription Layout Notes",
        "Heading",
        ": centered, largest font, indicates the deceased's status (Gu Xiankao/Gu Xianbi/Xiankao/Xianbi)",
        "Center column (name)",
        ": in the middle, largest font, the 'hui' (taboo-name) character slightly smaller to show respect",
        "Birth and death years",
        ": on both sides or below the name, traditionally in lunar uppercase",
        "Epitaph",
        ": briefly describes life virtues; keep concise, not verbose",
        "Signature",
        ": erector name and erection time, bottom right",
        "• Character count follows the 'He-Sheng-Lao' auspicious rule: the last digit of the total count falling on 'Sheng' or 'Lao' (of the Sheng-Lao-Bing-Si-Ku cycle) is auspicious",
        "• Cemetery area = site length × width, reserve space for ritual activities",
        "📚 Deep Dive: Tombstone Design and Inscription Layout",
        "Layout reference before engraving",
        "Title format check (Xiankao/Xianbi etc.)",
        "Cemetery site area estimation",
        "Fill heading title, name, birth/death years and signature by inscription format; the tool generates layout preview; cemetery area = site length × width for footprint estimation.",
        "Site length 2.5 m × width 1.5 m = area 3.75 m²; slab face 0.8 m (W) × 1.0 m (H) lays out 'Late Father Mr. Li [personal name omitted] / 1945—2023 / erected by filial son'. Titles by gender and seniority: Xiankao (father)/Xianbi (mother).",
        "How to choose the title?",
        "Father uses Xiankao/Gu Xiankao, mother uses Xianbi/Gu Xianbi; with official rank or honorific use 'Xian', peers self-style 'Ai zi/Ai nv'. Follow clan custom.",
        "Is the footprint over limit?",
        "The cemetery area is only estimated by your entered length × width; compliance depends on local funeral management regulations.",
        "About 'Cemetery Tombstone Inscription Designer'",
        "Cemetery tombstone inscription designer, provides inscription templates and layout preview, and estimates tombstone and cemetery area, assisting inscription planning.",
        "Multiple built-in inscription templates",
        "Real-time inscription layout preview",
        "Character-count auspicious check (He-Sheng-Lao)",
        "Tombstone inscription plan planning",
        "Inscription character-count auspicious check",
        "Cemetery area estimation",
        "Inscription content drafting reference",
    ]
    mp = build('grave-design', en); write('grave-design', mp)

if __name__ == '__main__':
    main()
