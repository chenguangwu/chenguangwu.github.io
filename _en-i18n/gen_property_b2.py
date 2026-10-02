#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'property')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'property')
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
    out = {'slug': slug, 'industry': 'property', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('cost-profit', build('cost-profit', [
        "💰 Budget (Cost / Income / Profit) Preparation",
        "Compute profit, profit margin and cost ratio for a property project from cost and income, for annual budgeting and break-even analysis.",
        "📖 Read the \"Budget (Cost / Income / Profit) Preparation\" guide",
        "Profit = income − cost; profit margin = profit ÷ income × 100%; cost ratio = cost ÷ income",
        "A property budget centres on cost and income: profit = income − cost, profit margin = profit ÷ income, cost ratio = cost ÷ income. This shows whether the project breaks even and how much pricing headroom exists, supporting annual budgeting and break-even calculation.",
        "Income (CNY)",
        "💡 Profit = income − cost; profit margin = profit ÷ income × 100%; cost ratio = cost ÷ income.",
        "📚 Deep dive: budget (cost / income / profit) preparation",
        "Property companies draw up the annual project budget at the start of the year (labour, energy, repairs, profit)",
        "Revise it on a rolling basis through the year based on actual completion",
        "Calculate the",
        "break-even point",
        "Annual budget",
        "Income: property fees 2.4 million + parking 0.54 million + value-added services 0.3 million = 3.24 million; cost: labour 1.8 million + energy 0.36 million + repairs 0.3 million + management 0.24 million = 2.7 million → profit 0.54 million,",
        "profit margin",
        "Break-even",
        "With fixed cost 2 million and a target margin of 15%, required income is 2 / (1 - 15%) ≈ 2.35 million; the current 3.24 million already covers it with room to spare.",
        "What profit margin counts as reasonable?",
        "For residential property it is",
        "mostly 8%-15%. Too low means costs or fees must be adjusted; too high invites questions.",
        "Is a big gap between budget and final accounts normal?",
        "A variance under 10% is normal. Overruns usually come from repairs or energy exceeding expectations and should be explained and revised on a rolling basis.",
        "About \"Budget (Cost / Income / Profit) Preparation\"",
        "Budget (Cost / Income / Profit) Preparation. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
        "Cost",
        "Income",
    ]))

    write('shared-area', build('shared-area', [
        "📐 Common Area (Gross-Up) Area Calculation",
        "Aggregate the area of each common area component to compute the gross-up coefficient, per-unit allocation and usable area ratio",
        "\"Aggregate the area of each common area component to compute the gross-up coefficient, per-unit allocation and usable area ratio\" performs a professional calculation from the input parameters and outputs the result.",
        "📖 Read the \"Common Area (Gross-Up) Area Calculation\" guide",
        "Total in-unit area per household (㎡)",
        "Number of units to calculate",
        "Common area details (component name + area in ㎡)",
        "+ Add component",
        "📚 Deep dive: common area (gross-up) area calculation",
        "The developer or property company allocates the building's common area across units in proportion to in-unit area, based on the survey report",
        "Before a transaction, verify whether the gross-up coefficient is reasonable (typically 10%-20% for residential)",
        "When a homeowners committee questions an excessive gross-up, check components such as lift shafts, stairwells and lobbies one by one",
        "Standard residential allocation",
        "Building in-unit area 8000 ㎡ and common area 1200 ㎡ → gross-up coefficient = 1200 / 8000 = 15%; a unit with 100 ㎡ in-unit area → its allocated common area = 100 × 15% = 15 ㎡, giving a title area of 115 ㎡.",
        "With component detail",
        "Lift shaft 400 + stairwell 300 + lobby 200 + plant room 300 = 1200 ㎡, allocated by in-unit proportion; the largest component is the lift shaft, taking 33.3% of the common area.",
        "What gross-up coefficient counts as normal?",
        "Low-rise residential is about 10%-15% and high-rise 15%-25%. Above 25%, check whether components that should not be included have been counted in.",
        "Can I measure the common area myself?",
        "No, the report from a qualified surveying institution governs. This tool verifies whether the allocation calculation is correct and does not constitute a new survey.",
        "About \"Common Area (Gross-Up) Area Calculation\"",
        "Enter the area of common area components such as lift shafts, stairwells and corridors to automatically compute total common area, the gross-up coefficient, per-unit allocation and the usable area ratio.",
        "Custom common area components",
        "Automatic gross-up coefficient",
        "Usable area ratio assessment",
        "Per-unit allocation detail",
        "Common Area Calculation Tool - detailed accounting of common area by component, computing the gross-up coefficient and per-unit allocation. Free online property management tool. Business and office tool to improve work efficiency, data processed locally to protect privacy.",
    ]))

    write('fee-allocation', build('fee-allocation', [
        "🧾 Property Fee Allocation Calculator",
        "Allocate total property fees by area or by household count, with customisable per-household detail",
        "📖 Read the \"Property Fee Allocation Calculator\" guide",
        "Property fee allocation = area proportion",
        "Total property fees (CNY)",
        "Allocation method",
        "Allocate by floor area",
        "Split equally by household count",
        "Per-household details (name + area in ㎡)",
        "+ Add household",
        "📚 Deep dive: property fee allocation",
        "Property management allocates",
        "common energy and repair costs across households",
        "Mixed residential and commercial buildings allocate residential and commercial rates separately",
        "When a household questions its allocation, explain the per-unit figures item by item using the area detail",
        "Allocation by area",
        "Total shared cost 30000 CNY over a billable area of 10000 ㎡ → unit rate 3 CNY/㎡; unit A at 100 ㎡ pays 300 CNY and unit B at 150 ㎡ pays 450 CNY.",
        "Blended rates",
        "Residential 2.5 CNY/㎡ and commercial 5 CNY/㎡; residential 8000 ㎡ and commercial 2000 ㎡ → residential 20000 CNY + commercial 10000 CNY = 30000 CNY, matching the total budget.",
        "Is allocation by area fair?",
        "The area method is the industry norm and embodies intergenerational fairness; splitting equally per household is also possible but must be approved by a homeowners' vote.",
        "Can commercial and residential units use the same rate?",
        "Commercial rates are usually higher (lifts,",
        "air conditioning load",
        "are heavy), so the contract or covenant must be explicit and the two must not be mixed.",
        "About \"Property Fee Allocation Calculator\"",
        "The Property Fee Allocation Calculator allocates total property fees by floor area proportion or equally per household, and automatically generates a per-household allocation table.",
        "Two allocation methods: area / household count",
        "Customisable per-household details",
        "Automatic share and amount calculation",
        "Results can be copied",
        "Property Fee Allocation Calculator - allocate property fees by area or household count. Free online property management tool running entirely in the front end with no data uploaded. Business and office tool to improve work efficiency, data processed locally to protect privacy.",
    ]))

    write('cleaning-allocation', build('cleaning-allocation', [
        "🏢 Cleaning Task Allocation",
        "Compute workload from area and difficulty, then balance the assignment across cleaning staff",
        "📖 Read the \"Cleaning Task Allocation\" guide",
        "Cleaning allocation = area × frequency coverage",
        "Number of cleaning staff",
        "Task details (area + area in ㎡ + difficulty)",
        "Assign tasks",
        "📚 Deep dive: cleaning task allocation",
        "The property cleaning supervisor assigns tasks to cleaners based on the area and soiling difficulty of each zone",
        "Temporarily raise the frequency of key zones before holidays or events",
        "New staff start on low-difficulty zones and build up the load gradually",
        "Allocation for a 5-person team",
        "Two lift cars (20 ㎡ each, hard), lobby (300 ㎡, medium), corridors (600 ㎡, medium), underground car park (1500 ㎡, hard) → weighted by difficulty (hard counts as 2× the man-hours per ㎡), giving the car park 2 people and the rest 3.",
        "Temporary frequency increase",
        "On an event day the lobby cleaning frequency goes from 1 to 3 times a day, multiplying man-hours by 3; 0.5 FTE must be seconded from another zone and this is posted on the roster.",
        "How are difficulty levels set?",
        "By soiling frequency and cleaning time: lifts and car parks are hard, lobbies and corridors medium, offices easy.",
        "What if there are not enough staff?",
        "Prioritise meeting the hard zones, allowing medium zones to be combined or reduced in frequency, and post the roster to avoid complaints from missed items.",
        "About \"Cleaning Task Allocation\"",
        "Computes workload from zone area and difficulty coefficients, then assigns tasks across multiple cleaning staff with a greedy balancing algorithm to keep workloads even.",
        "Difficulty coefficient weighting",
        "Greedy balanced allocation",
        "Balance assessment",
        "Visualised workload",
        "Cleaning Task Allocation Tool - optimises the assignment of tasks to cleaning staff by balancing workload. Free online property management tool. Business and office tool to improve work efficiency, data processed locally to protect privacy.",
        "How to use Cleaning Task Allocation",
        "What does Cleaning Task Allocation do?",
        "Enter the area and cleaning difficulty coefficient of each zone; the tool converts them into standard workload and balances the assignment across multiple cleaning staff, outputting each person's zones and man-hours so property management can schedule fairly by area and difficulty and avoid overload.",
        "How do I use Cleaning Task Allocation?",
        "Which scenarios suit Cleaning Task Allocation?",
    ]))


if __name__ == '__main__':
    main()