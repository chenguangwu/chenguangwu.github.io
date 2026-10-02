#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'hr')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'hr')
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
    out = {'slug': slug, 'industry': 'hr', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('generator-36', build('generator-36', [
        "✨ Policy (Manual / Process / Form) Generator",
        "Manual / Process / Form",
        "📖 Read the \"Policy (Manual / Process / Form) Generator\" guide",
        "The HR policy manual is assembled by section: General Provisions (purpose, basis, scope) + Definitions + Responsibility Allocation + Process and Operating Standards + Assessment, Rewards and Penalties + Supplementary Provisions and Effective Date. Clauses are numbered sequentially as \"Article X\", process steps are numbered in order, and forms are listed as field inventories so they can be adopted directly.",
        "📚 Deep dive: policy manual and process form generation",
        "Produce first drafts of attendance, leave and reimbursement policies from templates in minutes.",
        "The matching approval flow and form fields are generated alongside, so you start from a draft instead of a blank page.",
        "When revising a policy, reuse the previous structure and only change the clauses that differ.",
        "Batch 5 policy types",
        "Select any 5 of attendance / leave / reimbursement / travel / confidentiality and the tool generates the drafts and forms in parallel, ready for human review.",
        "Form fields",
        "Reimbursement forms automatically carry amount, reason and approval-chain fields, and export in a ready-to-use format.",
        "Can I use the output directly?",
        "It is a draft framework. Have legal and business teams review the local clauses (such as maternity leave days) before publishing.",
        "What if it conflicts with our real templates?",
        "The company's current effective policy takes precedence; the output only speeds up drafting and does not replace compliance review.",
        "About \"Policy (Manual / Process / Form) Generator\"",
        "Policy (Manual / Process / Form) Generator. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
    ]))

    write('gross-up-calculator', build('gross-up-calculator', [
        "🧾 Gross-Up Calculator",
        "Enter your take-home pay to estimate the pre-tax salary and taxable deductions.",
        "/ Gross-Up Calculator",
        "📖 Read the \"gross-up-calculator\" guide",
        "Backing out pre-tax from after-tax uses trial-and-error iteration: let X be the pre-tax salary, then X − social insurance (X × insurance rate) − income tax = take-home pay; taxable income = X − social insurance − threshold (5000 CNY). Income tax is computed with the seven-bracket progressive rates (3% to 45%), and X is adjusted bracket by bracket until the equation holds.",
        "Take-home pay (CNY)",
        "Social insurance / housing fund rate (e.g. 0.225)",
        "Threshold (default 5000)",
        "Back out the pre-tax salary",
        "📚 Deep dive: backing out pre-tax salary and taxable income from take-home pay",
        "When you promise 8000 of take-home pay, work out how much pre-tax salary is needed to cover income tax and social insurance.",
        "Negotiating recruiter packages or designing expatriate allowances: back out the gross package from the target net income.",
        "Plan the separate taxation of annual bonuses and compare the take-home difference between merging it into salary or paying it separately.",
        "Take-home 8000, insurance rate 0.225, threshold 5000",
        "First solve pre-tax = (take-home − threshold × tax rate + quick deduction) / (1 − rate × (1 − insurance rate)) iteratively; the tool tries each bracket and converges near 9300 pre-tax.",
        "Higher bracket at 15000 take-home",
        "Once the 20% bracket applies the quick deduction becomes 16920, so the back-solved pre-tax figure grows markedly; the tool converges bracket by bracket using the progressive table.",
        "Why can't I just divide?",
        "Income tax is progressive and social insurance is based on the pre-tax salary, so take-home and pre-tax are nested; you have to iterate across tax brackets.",
        "How are special additional deductions handled?",
        "They stack on top of the threshold, such as children's education and mortgage interest; the tool reflects the threshold you enter.",
    ]))

    write('bandwidth-1', build('bandwidth-1', [
        "🌐 Salary Band (Range / Percentile / Equity) Design",
        "Compute the lower and upper bounds, absolute width and band ratio of a salary band from its midpoint and spread, for pay-grade salary structure design.",
        "📖 Read the \"Salary Band (Range / Percentile / Equity) Design\" guide",
        "Lower bound = midpoint × (1 − spread%); upper bound = midpoint × (1 + spread%); band width = upper bound − lower bound",
        "A salary band expands symmetrically around the midpoint by the spread percentage: lower bound = midpoint × (1 − spread%), upper bound = midpoint × (1 + spread%), the band width is the difference between them, and the band ratio = upper bound ÷ lower bound. A typical spread is 20%-50%, used to define the negotiable salary range of one pay grade.",
        "Salary midpoint (CNY)",
        "Band spread (±%)",
        "💡 Lower bound = midpoint × (1 − spread%); upper bound = midpoint × (1 + spread%); band width = upper bound − lower bound.",
        "📚 Deep dive: salary band and percentile design",
        "Set a band around the midpoint of each grade (e.g. ±50%) to frame the salary range.",
        "Check whether the offered salary for a new hire falls inside the band, avoiding bands that are too wide or too compressed.",
        "At annual review time, look at where an employee sits in the percentile range to decide the size of the increase.",
        "Midpoint 10000, band 50%",
        "Range = 10000×(1±0.5) = 5000~15000; an offer of 13000 sits at the 80th percentile, which is high and needs approval.",
        "Overlap",
        "A 30% overlap between adjacent grade bands makes lateral moves easier; the tool reports the overlap.",
        "Is a wider band always better?",
        "Too wide weakens the distinction between grades and too narrow limits hiring flexibility; 40%-60% is common, chosen by how mobile the talent market is.",
        "How do I read the percentile?",
        "Map salary ÷ (upper bound − lower bound) + lower bound to a percentile; a high position means the employee is near the top of the band, so promotion or a broader band is likely.",
        "About \"Salary Band (Range / Percentile / Equity) Design\"",
        "Salary Band (Range / Percentile / Equity) Design. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
        "Band",
        "Percentile",
    ]))

    write('overtime-pay-calc', build('overtime-pay-calc', [
        "💵 Overtime Pay Calculator",
        "Estimate overtime pay using the statutory multipliers, based on the hourly wage derived from daily working hours.",
        "/ Overtime Pay Calculator",
        "📖 Read the \"overtime-pay-calc\" guide",
        "Weekday overtime pay = hourly wage × 1.5 × overtime hours; rest-day overtime pay = hourly wage × 2 × hours; statutory holiday overtime pay = hourly wage × 3 × hours; total overtime pay = the sum of the three; hourly wage = monthly salary ÷ 21.75 ÷ 8, where 21.75 is the statutory number of payable days per month.",
        "Base hourly rate (CNY)",
        "Weekday overtime hours (1.5×)",
        "Rest-day overtime hours (2×)",
        "Statutory holiday overtime hours (3×)",
        "📚 Deep dive: computing overtime pay from monthly salary and overtime periods",
        "Weekday",
        "Extended weekday overtime is paid at 150%, rest-day overtime at 200% and statutory holiday overtime at 300%.",
        "For HR monthly",
        "overtime pay",
        "totals, cross-checked against attendance and shift records.",
        "Estimate overtime cost for contractors or project-based staff to support quoting and scheduling.",
        "Monthly salary 10000, 8 hours of weekday extended overtime",
        "Hourly wage = 10000÷21.75÷8 ≈ 57.47; at the 1.5× weekday rate → 57.47×1.5×8 ≈ 689.6 CNY.",
        "Monthly salary 8000, one rest day of overtime (8h)",
        "With a base of 8000 the hourly rate ≈ 45.98; at the rest-day 2× rate → 45.98×2×8 ≈ 736 CNY.",
        "Where does 21.75 come from?",
        "Monthly payable days = (365−104)÷12 = 21.75, the statutory basis for converting a monthly salary into a daily or hourly wage.",
        "Does the comprehensive working-hours system use the same basis?",
        "Under the comprehensive working-hours system overtime is judged by total hours over a cycle: the excess is paid at 150%, while statutory holidays remain at 300%, which differs from standard working hours.",
    ]))


if __name__ == '__main__':
    main()