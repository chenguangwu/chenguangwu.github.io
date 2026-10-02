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
    write('report-manager', build('report-manager', [
        "🔍 Finance (Income and Expenditure / Reports / Audit) Management",
        "Property income and expenditure statements with balance analysis",
        "📖 Read the \"Finance (Income and Expenditure / Reports / Audit) Management\" guide",
        "Enter one line per item as \"item,income,expenditure\". Balance = income − expenditure; balance rate = balance ÷ income × 100%. The summary gives total income, total expenditure and the overall balance, and pinpoints the largest expenditure item and the number of deficit items, for property operating statements and audit self-checks.",
        "Income and expenditure item data (one line per item, \"item,income,expenditure\")",
        "Property fees,260000,150000\nParking fees,60000,18000\nCommon area energy,0,45000",
        "Generate report",
        "📚 Deep dive: property income and expenditure statements and balance calculation",
        "Property companies aggregate property fees,",
        "parking fees",
        ", advertising space rental and other income against the corresponding expenditure each month, producing a statement for management review.",
        "When a homeowners committee or auditor checks common income against common energy expenditure, this tool computes the balance and deficit items quickly.",
        "When taking over a new project, trial-calculate the balance rate from expected income and expenditure to assess whether the project is viable.",
        "Trial calculation across four items",
        "Entering \"property fees,320000,180000; parking fees,85000,22000; advertising,40000,5000; common energy,0,96000\" gives total income 445000.00, total expenditure 303000.00, balance +142000.00, balance rate 31.91%, with property fees as the largest expenditure item and 1 deficit item.",
        "How do I fill in an item with no income?",
        "Enter 0 for income. Pure expenditure items such as common area energy are counted as deficit items and reflected in the balance.",
        "How should the balance rate be interpreted?",
        "Balance rate = balance ÷ income × 100%, showing how much surplus each 1 CNY of income leaves behind. It is a core indicator of operating quality for a property project.",
        "Can I compare multiple projects at once?",
        "Currently one input is one statement with multiple income and expenditure items. To compare projects, calculate them separately and record the results, or prefix each item with the project name and merge the input.",
        "About \"Finance (Income and Expenditure / Reports / Audit) Management\"",
        "Finance (Income and Expenditure / Reports / Audit) Management. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
    ]))

    write('response-1', build('response-1', [
        "🏢 Maintenance (Repair Request / Response) Timeliness",
        "Compute the maintenance response duration from the repair request and response timestamps, and judge the compliance tier against the SLA threshold for property repair service assessment.",
        "📖 Read the \"Maintenance (Repair Request / Response) Timeliness\" guide",
        "Response duration = response time − request time (minutes); SLA example: ≤30 minutes excellent, ≤60 minutes good",
        "Property maintenance response timeliness is measured by the interval from request to response: convert the request and response times into minutes of the day, then response duration = response − request. Judge the compliance tier against SLA thresholds such as 30 or 60 minutes, for service assessment and improvement.",
        "Request time (minutes, 0-1439)",
        "Response time (minutes)",
        "💡 Response duration = response time − request time (minutes); ≤30 minutes is excellent, ≤60 minutes is good.",
        "📚 Deep dive: maintenance (repair request / response) timeliness",
        "The property front desk records each repair request and the first response time",
        "Flags overdue unresponded tickets in red for follow-up",
        "A monthly average response duration is used for assessment",
        "Repair requests",
        "12 requests logged in the morning with an average response of 1.8 h; 2 of them exceeded 2 h (3.5 h and 4 h respectively) → flagged in red, with the responsible teams held accountable.",
        "Comparison against the promise",
        "The contract promises a response within 2 h; this month's measured mean is 1.8 h with a 92% compliance rate → basically compliant, but the weekend mean of 2.6 h needs extra staffing.",
        "From what point to what point is response duration measured?",
        "From the time the owner's request is logged to the first contact or arrival by the repair technician; the subsequent repair time is excluded.",
        "How are overdue tickets handled?",
        "The system flags them in red and escalates to the supervisor, to check whether the cause is insufficient staffing or misdispatch and avoid a backlog.",
        "About \"Maintenance (Repair Request / Response) Timeliness\"",
        "Maintenance (Repair Request / Response) Timeliness. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
        "Request",
    ]))

    write('response-4', build('response-4', [
        "🏢 Maintenance (Response / Completion / Follow-up) Timeliness",
        "Compute the total maintenance completion duration from the request and completion timestamps and judge against the SLA whether the job was finished on time, for ticket closure assessment.",
        "📖 Read the \"Maintenance (Response / Completion / Follow-up) Timeliness\" guide",
        "Completion duration = completion time − request time (minutes); SLA example: ≤8 hours (480 minutes) on time",
        "Maintenance completion timeliness is the interval from repair request to finished repair. Convert the timestamps into minutes, then completion duration = completion − request, and judge on time versus overdue against the SLA (such as 8 hours), for ticket assessment and service level management.",
        "Request time (minutes, 0-1439)",
        "Completion time (minutes)",
        "💡 Completion duration = completion time − request time (minutes); ≤480 minutes (8h) is on time.",
        "📚 Deep dive: maintenance (response / completion / follow-up) timeliness",
        "The property service centre tracks the duration from request to completion and the follow-up rate for each ticket",
        "Assess the on-time rate of outsourced maintenance contractors",
        "Pull up the ticket timeline as evidence when owners complain about slow response",
        "Timeliness of a single ticket",
        "Requested at 09:00, responded at 10:30 (1.5 h), completed at 14:00 (5 h), followed up at 11:00 the next day → response compliant (≤2 h), completion compliant (≤8 h), follow-up done.",
        "Monthly assessment",
        "300 tickets this month, 285 response-compliant (95%), 270 completion-compliant (90%), follow-up rate 88% → the misses concentrate in overnight requests, so a night shift is needed.",
        "How are response and completion durations defined?",
        "Response runs from ticket acceptance to arrival on site, completion from arrival to finished repair; the thresholds differ (e.g. response 2 h, completion 8 h).",
        "What does a low follow-up rate affect?",
        "Follow-up is the handle on closure and satisfaction. Below 85% it usually means the ticket system does not enforce closure.",
        "About \"Maintenance (Response / Completion / Follow-up) Timeliness\"",
        "Maintenance (Response / Completion / Follow-up) Timeliness. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
        "Completion",
    ]))

    write('energy', build('energy', [
        "⚡ Energy (Utilities / Gas) Cost Allocation",
        "Estimate procurement freight from the goods weight and freight rate, giving the freight cost per tonne and an annual estimate for larger volumes, for procurement logistics cost calculation.",
        "📖 Read the \"Energy (Utilities / Gas) Cost Allocation\" guide",
        "Freight = weight × freight rate (CNY/kg); freight per tonne = freight rate × 1000",
        "Procurement freight = weight × freight rate; freight per tonne = freight rate × 1000, which makes quoting across logistics providers easy. Then estimate the annual freight cost from the number of annual purchase batches to support logistics cost control.",
        "Goods weight (kg)",
        "Freight rate (CNY/kg)",
        "💡 Freight = weight × freight rate; freight per tonne = freight rate × 1000.",
        "📚 Deep dive: energy (utilities / gas) cost allocation",
        "The property allocates the building's common energy cost across units by consumption or by floor area",
        "Common area utilities are accounted separately from each unit's own consumption",
        "Compare the reduction in allocated cost after energy-saving retrofits",
        "Allocating by consumption",
        "A unit uses 320 kWh in the month while residents in total use 4800 kWh and the common energy cost is 9600 CNY → the unit's share is 6.67%, so it is allocated 640 CNY.",
        "Area-based fallback",
        "For old buildings without sub-metering, allocation uses",
        "floor area: a 100 ㎡ unit out of a total 10000 ㎡ × 9600 CNY common energy cost = 96 CNY. When the results diverge widely from the consumption method, prioritise installing sub-meters.",
        "What does common energy include?",
        "Lifts, corridor lighting, water pumps and fire protection systems in common areas, excluding in-unit consumption.",
        "Which method is better, consumption or floor area?",
        "With sub-metering, the consumption method is fairest; without it only floor area is available, which invites disputes, so retrofitting with meters is advisable.",
        "About \"Energy (Utilities / Gas) Cost Allocation\"",
        "Energy (Utilities / Gas) Cost Allocation. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
        "Utilities",
        "Gas",
    ]))


if __name__ == '__main__':
    main()