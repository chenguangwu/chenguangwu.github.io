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
    write('meeting-conflict', build('meeting-conflict', [
        "\U0001F50D Meeting Conflict Detection",
        "Add multiple schedule time ranges, automatically detect time conflicts and visualise a timeline",
        "\U0001F4D6 View the User Guide for Meeting Conflict Detection",
        "Schedule List",
        "\u2795 Add Schedule",
        "\U0001F4CA Timeline Visualization",
        "\U0001F50D Conflict Detection Result",
        "\U0001F4DA In-depth: Meeting Conflict Detection",
        "Aggregate several colleagues' schedules (name, time) and detect clashes, issuing a conflict alert in advance to ease rescheduling or delegation.",
        "When one meeting room is requested by multiple meetings, use the tool to check the timeline, mark resource-contention periods and assign priority.",
        "When mixing on-site + remote scheduling, check whether the same host's offline and online meetings overlap, avoiding double-booking the host.",
        "Two schedules of the same host clash",
        "Enter schedules: Requirements Review Wed 14:00-15:00, Iteration Planning Wed 14:30-15:30, Stand-up Thu 09:30-09:45. The tool finds Requirements Review and Iteration Planning overlap at 14:30-15:00, warns the same host cannot attend both, and suggests delaying Iteration Planning by 30 minutes or offsetting it from Requirements Review.",
        "Compared with ",
        " - what is the difference?",
        "Both judge time-interval overlaps but with different emphasis: this tool leans toward schedule/person clash alerts and rescheduling advice, while the other leans toward date-based meeting-room and time-slot detection. Pick either by preference; the conclusions are consistent.",
        "What to do after a conflict is detected?",
        "Prioritise adjusting the lower-priority meeting's time, or change the host/venue; if parallel sessions are unavoidable, split venues or switch to an asynchronous review. The tool only provides a conflict list and suggestions; the final schedule is confirmed by the meeting organiser.",
        "About Meeting Conflict Detection",
        "Meeting Conflict Detection is an online tool in the business-office domain. Business-office tools boost work efficiency, with data processed locally to protect privacy.",
    ]))
    write('register-depreciation', build('register-depreciation', [
        "\U0001F4C9 Fixed Assets (Registration / Depreciation / Inventory)",
        "Register asset information and automatically calculate depreciation (straight-line / double-declining-balance / sum-of-years'-digits), generating a depreciation schedule and book value.",
        "\"Register asset information and automatically calculate depreciation (straight-line / double-declining-balance / sum-of-years'-digits), generating a depreciation schedule and book value.\" Professional calculation and result output based on the input parameters.",
        "\U0001F4D6 View the User Guide for Fixed Assets (Registration / Depreciation / Inventory)",
        "Register Asset",
        "Asset Name",
        "Electronic Equipment",
        "Office Furniture",
        "Buildings",
        "Purchase Date",
        "Original Value (CNY)",
        "Sum-of-Years'-Digits",
        "Asset Inventory",
        "Filter Category:",
        "Close",
        "\U0001F4DA In-depth: Fixed Assets (Registration / Depreciation / Inventory)",
        "When booking new laptops, printers, etc., fill in original value, salvage value, useful life and",
        ", and the tool auto-computes annual/monthly depreciation, generating an archivable depreciation ledger.",
        "At year-end depreciation accrual, batch-calculate the current period's depreciation for all fixed assets and export a list for bookkeeping and tax filing.",
        "During vehicle or equipment inventory, verify book original value against accumulated depreciation and judge impairment or retirement by current second-hand salvage value.",
        "Laptop Straight-Line Depreciation Estimate",
        "Asset: Lenovo laptop, category electronic equipment, original value 6000 CNY, salvage value 600 CNY, useful life 5 years, straight-line. Annual depreciation = (6000-600) / 5 = 1080 CNY, monthly depreciation = 90 CNY; after 5 years the book salvage value is exactly 600 CNY. If instead using",
        "double-declining-balance",
        ", depreciation is higher in the first two years and declines later.",
        "What are the differences among the three depreciation methods?",
        "Straight-line is equal each year; double-declining-balance front-loads and back-loads less (accelerated depreciation);",
        "is also accelerated but gentler. Once an accounting depreciation method is chosen it must not be changed arbitrarily; tax depreciation has separate rules, detailed in the ",
        "Enterprise Income Tax",
        "Law and your unit's financial policy; the tool only demonstrates the calculation.",
        "Can salvage value be zero?",
        "Yes. If no salvage value is expected at retirement, enter 0 for salvage value, then annual depreciation = original value / useful life. Too low or too high a salvage rate affects each period's expense; estimate reasonably by referencing similar assets' historical disposal prices.",
        "In the last two years, double-declining-balance automatically switches to straight-line (per Chinese accounting-standard convention)",
        "Depreciation is calculated in units of \"year\"; the purchase year is counted as a full year",
        "Results are for reference only; actual depreciation should follow the enterprise's accounting policy",
        "About Fixed Assets (Registration / Depreciation / Inventory)",
        "A fixed-asset registration, depreciation and inventory management tool. Supports three depreciation methods - straight-line, double-declining-balance and sum-of-years'-digits - and auto-generates a year-by-year depreciation schedule with real-time book value.",
        "Automatic calculation of three depreciation methods",
        "Year-by-year depreciation schedule and accumulated depreciation",
        "Real-time book value and depreciation progress",
        "Filter by category and keyword search",
        "Asset list CSV export",
        "Enterprise fixed-asset ledger management",
        "Monthly/annual financial depreciation accrual",
        "Asset inventory and book-vs-physical reconciliation",
        "Book-value confirmation before asset disposal",
        "e.g. Lenovo laptop",
        "Search asset name...",
    ]))

if __name__ == '__main__':
    main()
