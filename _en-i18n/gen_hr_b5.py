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
    write('social-insurance', build('social-insurance', [
        "💰 Social Insurance and Housing Fund Breakdown",
        "Individual and employer contribution breakdown with customisable rates (reference values, subject to local policy)",
        "📖 Read the \"Social Insurance and Housing Fund Breakdown\" guide",
        "Social insurance = base × contribution rate",
        "Beijing",
        "Shanghai",
        "Guangzhou",
        "Shenzhen",
        "Contribution rate settings (%)",
        "Individual",
        "💰 Calculate breakdown",
        "Employer + individual total",
        "Rates are reference values. Policies differ by region and are adjusted annually, so follow the local social security bureau's published figures. Work injury and maternity insurance are paid by the employer only; individuals do not contribute.",
        "📚 Deep dive: splitting individual and employer amounts by contribution base and statutory rates",
        "When HR runs the monthly payroll, split pension, medical, unemployment, work injury, maternity and",
        "housing fund",
        "into individual and employer amounts by base.",
        "Employees check their payslips and understand where the difference between take-home and pre-tax comes from.",
        "Re-estimate the monthly individual and employer totals when the base is adjusted or staff transfer across pooling regions.",
        "Base 10000 with common rates",
        "Individual: pension 8% = 800, medical 2% = 200, unemployment 0.5% = 50, housing fund 12% = 1200 → total 2250; employer pension 16% = 1600, medical 9% = 900, etc. Rates can be customised.",
        "Cap check at base 20000",
        "If the local ceiling is 3 times the average wage, amounts above the base are counted at the ceiling; the tool flags the cap automatically.",
        "Are the rates uniform nationwide?",
        "Pension, unemployment and work injury have national baseline ranges, while medical insurance and the housing fund are set by the pooling region; rates in the tool can be edited manually to match local policy.",
        "Why are the results reference values?",
        "Because rates and ceilings are adjusted annually by region, the tool uses your inputs",
        ", while actual contributions are determined by the social security agency.",
        "About \"Social Insurance and Housing Fund Breakdown\"",
        "Social Insurance and Housing Fund Breakdown - individual and employer contribution breakdown with customisable contribution base and rates. Free online HR tool. Business and office tool to improve work efficiency, data processed locally to protect privacy.",
    ]))

    write('stats-funnel-recruit', build('stats-funnel-recruit', [
        "💰 Recruitment (Channel / Budget / Funnel) Statistics",
        "Channel / budget / funnel",
        "📖 Read the \"Recruitment (Channel / Budget / Funnel) Statistics\" guide",
        "📐 Calculation principle",
        "Enter headcounts at each recruitment funnel stage (resumes → interviews → offers → onboarding) to automatically compute stage conversion rates and the overall conversion rate, locating the stage with the heaviest loss. All computation runs locally in the browser.",
        "Resumes / applications received",
        "Number entering interviews",
        "Number receiving offers",
        "Number actually onboarded",
        "📚 Deep dive: joint statistics on recruitment channels, budget and funnel",
        "Aggregate spend and output by channel to compute cost per offer (CPO) and cost per hire.",
        "When budget is tight, shift resources from low-efficiency channels to high-conversion ones.",
        "Quarterly recruitment effectiveness review supporting next year's budget planning.",
        "CPO comparison across three channels",
        "A headhunter spends 60000 CNY for 6 offers → CPO 10000; referrals spend 10000 for 8 offers → CPO 1250; job boards spend 30000 for 4 offers → CPO 7500, so referrals deliver the best value.",
        "Budget reallocation",
        "Cutting 30% of job board budget and moving it to referrals is expected to yield 3 more offers for the same spend.",
        "Is a low CPO always better?",
        "You also need onboarding retention and job seniority; CPO is naturally high for senior roles but those hires carry more value, and looking at cost alone risks cutting a key channel.",
        "How are brand channels measured?",
        "Passive applications are hard to attribute; use channel tagging plus a post-onboarding source questionnaire, so you do not count only paid channels.",
        "About \"Recruitment (Channel / Budget / Funnel) Statistics\"",
        "Recruitment (Channel / Budget / Funnel) Statistics. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
    ]))

    write('tracking-hours', build('tracking-hours', [
        "📊 Training Hours Statistics",
        "Annual hour accumulation and gaps with completion rate and a list of employees below target",
        "📖 Read the \"Training Hours Statistics\" guide",
        "Training hours = accumulated − gap",
        "Annual required hours",
        "Statistics cutoff date",
        "Department",
        "Employee training hour details",
        "Completion rate = completed hours ÷ required hours × 100%; gap = required hours − completed hours. Use it to plan remedial training.",
        "📚 Deep dive: training hour accumulation and compliance gaps",
        "Track completed hours and gaps against annual requirements by role (e.g. 40 hours).",
        "Remind employees in compliance-critical roles (safety, licensure) to complete remedial training before the deadline.",
        "Aggregate by department to see overall compliance rates and support the training budget.",
        "40 completed / 40 required",
        "Gap = 40 − 40 = 0, compliant; the tool shows a green light.",
        "60 required but only 35 completed",
        "Gap is 25 hours with 90 days to the deadline → at least 2 hours per week is advised; the tool produces a catch-up plan.",
        "Do internal training sessions count toward hours?",
        "Recognised internal training and online courses usually count, but sign-in sheets and duration records must be kept as evidence.",
        "Can surplus hours be carried over?",
        "Most companies do not carry them over, so they are valid within the year; a few allow part of the quota to roll into the next year, which depends on policy.",
        "About \"Training Hours Statistics\"",
        "Training Hours Statistics - annual hour accumulation and gaps with employee training completion rate and a list of those below target. Free online HR tool. Business and office tool to improve work efficiency, data processed locally to protect privacy.",
    ]))


if __name__ == '__main__':
    main()