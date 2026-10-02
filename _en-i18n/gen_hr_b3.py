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
    write('attendance-stats', build('attendance-stats', [
        "📊 Attendance Statistics Report",
        "Tardiness and early-departure statistics with batch calculation of attendance rate and salary deductions",
        "📖 Read the \"Attendance Statistics Report\" guide",
        "Attendance stats = present / absent / overtime",
        "Required working days in the period",
        "Deduction per late arrival (CNY)",
        "Deduction per early departure (CNY)",
        "Deduction per day of absenteeism (CNY)",
        "Employee attendance details",
        "Attendance rate = actual present days ÷ required days × 100%; deduction = late × late rate + early departure × early rate + absenteeism × absenteeism rate. Data is computed locally only and never uploaded.",
        "📚 Deep dive: attendance, absence and overtime statistics",
        "Roll monthly present days, absences, tardiness and overtime hours into one report with a single click.",
        "Reconcile the perfect-attendance bonus and the comp-time leave balance.",
        "Flag abnormal attendance (consecutive tardiness) for follow-up by the supervisor.",
        "22 required, 20 actual",
        "2 days absent and 8 hours of overtime; the perfect-attendance bonus is cancelled due to the absence, and the 8 overtime hours enter the comp-time pool.",
        "Tardiness trend",
        "An employee is late 5 days in a row; the tool highlights it in red and prompts a conversation.",
        "Do statutory holidays count as attendance?",
        "They do not count toward required days. Statistics are based on the roster and actual clock-in/out records, and the system usually excludes them automatically.",
        "How does overtime link to payroll?",
        "Extended weekday overtime goes through",
        "overtime pay",
        "while rest-day overtime can be converted to comp-time leave, consistent with the comp-time and overtime tools.",
        "About \"Attendance Statistics Report\"",
        "Attendance Statistics Report - tardiness and early-departure statistics with batch calculation of employee attendance rate, tardiness and early-departure counts and salary deductions. Free online HR tool. Business and office tool to improve work efficiency, data processed locally to protect privacy.",
    ]))

    write('calc-81', build('calc-81', [
        "👥 Employee Referral (Incentive / Process / Effectiveness) Calculator",
        "Compute the incentive amount for a single referral from the bonus base and achievement coefficient, plus an annual estimate and how many referrals each 10000 CNY of cost can fund.",
        "📖 Read the \"Employee Referral (Incentive / Process / Effectiveness) Calculator\" guide",
        "Referral incentive = base × coefficient; annual estimate = per-case amount × successful referrals per year",
        "Referral incentive = bonus base × achievement coefficient (such as tiered coefficients for joining and passing probation); then the annual incentive total is estimated from the number of successful referrals per year, which can be compared with the per-hire cost of external channels to measure referral ROI.",
        "Referral base (CNY)",
        "Achievement coefficient",
        "💡 Referral incentive = base × coefficient; annual estimate = per-case amount × successful referrals per year.",
        "📚 Deep dive: referral incentives and effectiveness calculation",
        "Reconcile the total incentive from successful referrals × per-case bonus × coefficient.",
        "Compare referral cost against headhunter cost to justify the strength of the referral policy.",
        "Set tiered coefficients (double pay for critical roles) to stimulate high-quality recommendations.",
        "10 successful hires, base 500, coefficient 1.2",
        "Incentive = 10×500×1.2 = 6000 CNY; the tool breaks it down by job family.",
        "Tiered coefficients",
        "General roles use a 1.0 coefficient and scarce roles 1.5; mixing 10 hires across both tiers gives a higher weighted total, and the tool buckets them automatically.",
        "How soon after joining should the bonus be paid?",
        "It is common to tie it to passing probation or completing a 3-6 month retention period, preventing rewards for people who leave immediately; the tool can roll statistics by the number who pass the retention window.",
        "Referral",
        "calculated how?",
        "Total referral bonus ÷ referrals hired, compared with headhunter fee ÷ headhunter hires, is usually more than 60% lower for referrals.",
        "About \"Employee Referral (Incentive / Process / Effectiveness) Calculator\"",
        "Employee Referral (Incentive / Process / Effectiveness) Calculator. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
        "Incentive",
        "Process",
    ]))

    write('eap-xinli-zixun-weiji-ziyuan', build('eap-xinli-zixun-weiji-ziyuan', [
        "💭 EAP (Psychology / Counselling / Crisis) Resources",
        "Based on workforce size and the intensity of psychological support needs, recommend an EAP employee care programme tier.",
        "📖 Read the \"EAP (Psychology / Counselling / Crisis) Resources\" guide",
        "Tier: headcount >=500 and intensity >=60 → Comprehensive; headcount >=200 or intensity >=40 → Standard; otherwise Basic",
        "EAP (Employee Assistance Programme) solutions are tiered by company size and demand intensity: large organisations with strong demand get comprehensive service (counselling + crisis + training); small and mid-sized organisations get standard or basic service, balancing cost against coverage of employee care.",
        "Workforce size (people)",
        "Psychological demand intensity (0-100)",
        "💡 Headcount >=500 and intensity >=60 → Comprehensive; >=200 or intensity >=40 → Standard; otherwise Basic.",
        "📚 Deep dive: matching EAP psychology and crisis resources",
        "Match employees to counselling resources and hotlines by topic (emotion / relationships / addiction / crisis).",
        "Pull up the tiered response path quickly during an HR crisis review.",
        "Promote self-service resources to lower the barrier to seeking help.",
        "General emotional distress",
        "Matched with short-term EAP counselling (6-8 sessions) plus self-guided meditation; the tool provides the booking entry point and a privacy note.",
        "Crisis signals",
        "When self-harm language appears, the tool highlights it in red and lists 24h hotlines and the accompanying escalation process, prioritising safety.",
        "Is EAP confidential?",
        "Counselling content is confidential to the employer; reporting is triggered only in statutory circumstances such as imminent crisis, and boundaries should be stated clearly during promotion to build trust.",
        "How can usage rates be improved?",
        "Anonymous promotion plus referral training for managers works better than mandates; the tool can track reach rather than forcing participation.",
        "About \"EAP (Psychology / Counselling / Crisis) Resources\"",
        "EAP (Psychology / Counselling / Crisis) Resources. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
        "Psychology",
        "Counselling",
    ]))

    write('hris-zizhuyuaiduibijisuanqi', build('hris-zizhuyuaiduibijisuanqi', [
        "👥 HRIS, Self-Service and AI Comparison Calculator",
        "Compare HRIS and AI maturity to recommend a focus for the digital HR roadmap.",
        "Digital (HRIS / Self-Service / AI) Planning",
        "/ Digital (HRIS / Self-Service / AI) Planning",
        "📖 Read the \"HRIS, Self-Service and AI Comparison Calculator\" guide",
        "Overall gap = |HRIS − AI|; HRIS weight ratio = HRIS ÷ (HRIS + AI) × 100%",
        "Digital HR weighs HRIS against self-service and AI: HRIS maturity reflects system coverage while AI maturity reflects intelligent decision-making. Comparing the two gives a roadmap focus; the weight ratio quantifies their relative share to help allocate transformation resources.",
        "HRIS maturity (0-100)",
        "AI maturity (0-100)",
        "💡 Overall gap = |HRIS − AI|; HRIS weight ratio = HRIS ÷ (HRIS + AI).",
        "📚 Deep dive: scoring HRIS, employee self-service and AI capability",
        "Score weighted across five dimensions during selection: functionality, implementation, cost, scalability and AI.",
        "Compare the total cost of ownership of in-house development against buying SaaS.",
        "Present radar-style comparison conclusions to the decision makers.",
        "Three weighted options",
        "A scores 9 on functionality and 6 on cost, B scores 7 on functionality and 8 on cost, C scores 8 on functionality and 7 on cost; weighting them together puts B highest, so the tool recommends buying mid-tier SaaS.",
        "TCO comparison",
        "In-house costs 1.2 million CNY over three years versus 300000 CNY per year for SaaS; the tool discounts the cash flows and finds the break-even point.",
        "How should the weights be set?",
        "By company stage: growth stage emphasises cost and speed, scale-up stage emphasises compliance and extensibility, so the weights shift accordingly.",
        "Does AI capability matter now?",
        "If there is a large volume of repetitive data entry and Q&A, AI self-service can cut transaction volume by over 30%, so it deserves a substantial weight.",
        "About \"Digital (HRIS / Self-Service / AI) Planning\"",
        "Digital (HRIS / Self-Service / AI) Planning. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
        "Self-service",
    ]))


if __name__ == '__main__':
    main()