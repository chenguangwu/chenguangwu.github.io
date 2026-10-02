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
    write('assessor-training-hr', build('assessor-training-hr', [
        "📋 Training (Needs / Plan / Effectiveness) Assessment",
        "Enter pre- and post-training competency scores and participation details to evaluate training effectiveness with the four-level Kirkpatrick model.",
        "📖 Read the \"Training (Needs / Plan / Effectiveness) Assessment\" guide",
        "Training assessment = weighted needs and effectiveness",
        "Training topic",
        "Number of participants",
        "Training duration (hours)",
        "Average competency score before training (1-10)",
        "Average competency score after training (1-10)",
        "Knowledge test pass rate (%)",
        "Evaluate training effectiveness",
        "📚 Deep dive: training needs, planning and effectiveness assessment",
        "Set needs from a gap analysis, then assess plan feasibility and post-training effectiveness.",
        "Score the Kirkpatrick four levels (reaction / learning / behaviour / results) and combine them into training",
        "Rank annual training plans and invest first in high-leverage topics.",
        "Three-level weighting",
        "Urgency of need 5.5, plan feasibility 7.8, post-training effectiveness 8.5; weighting them together gives the tool a composite 7.4, which clears the threshold for approval.",
        "Effectiveness retrospective",
        "A course shows only a 20% behaviour change rate three months after training, below the 50% target, so increase the proportion of hands-on practice.",
        "How is effectiveness quantified?",
        "Combine post-training assessments, manager ratings and business metrics (such as a drop in error rate) across multiple sources; satisfaction scores alone tend to look inflated.",
        "Where do training needs come from?",
        "The intersection of performance gaps, competency model gaps and employee surveys should drive course prioritisation.",
        "Kirkpatrick four levels: L1 reaction (satisfaction), L2 learning (test), L3 behaviour (capability change), L4 results (business impact)",
        "Pre- and post-training competency comparison is the most intuitive effectiveness metric",
        "The satisfaction survey should be run immediately after the session ends",
        "Behaviour-level assessment is recommended as a follow-up 1-3 months after training",
        "Results-level assessment must be combined with KPI changes and takes a longer cycle",
        "About \"Training (Needs / Plan / Effectiveness) Assessment\"",
        "Training effectiveness assessment tool based on the Kirkpatrick four-level model, evaluating training effectiveness across satisfaction, knowledge testing and capability improvement.",
        "Kirkpatrick four-level model",
        "Pre- and post-training competency comparison",
        "L1/L2/L3 three-level scoring",
        "Automatic determination of effectiveness grade",
        "Corporate training effectiveness assessment",
        "Training programme acceptance",
        "Training system optimisation",
    ]))

    write('index', build('index', [
        "👥 Human Resources Tools",
        "Human Resources",
        "Human Resources Tools",
        "The Overtime Pay Calculator is a free online human resources tool; enter the parameters and get results in real time. Runs entirely in the browser, uploads no data and needs no registration.",
        "Annual Leave Proration Calculator",
        "The Annual Leave Proration Calculator is a free online human resources tool. If you joined or left the company mid-year, annual leave is prorated by the remaining calendar days. Enter the join date, cumulative service years and the proration cutoff date to compute the annual leave due for that year automatically. Runs entirely in the browser, uploads no data and needs no registration.",
        "Comp-Time Calculator",
        "The Comp-Time Calculator is a free online human resources tool. How much comp-time have you accrued? Using the Labour Law multipliers: weekday overtime 1.5x, rest-day 2x (eligible for time off in lieu), statutory holidays 3x. Enter overtime hours to convert them automatically into comp-time days. Runs entirely in the browser, uploads no data...",
        "Annual Leave Calculator",
        "Online annual leave calculator that estimates statutory annual leave days from working years of service and tenure, supporting both accumulated and prorated leave to help HR and employees schedule time off. Runs entirely in the browser.",
        "Employee referral (incentive / process / effectiveness) tool. Enter referral counts, rewards and conversion data to estimate referral incentive cost and recruitment effectiveness, for referral channel ROI assessment and programme optimisation.",
        "Policy (manual / process / form) generator. From the policy topic you enter, the front end generates policy manual, process and form framework text that can be copied and used directly, enabling fast drafting of HR policy documents.",
        "Gross-Up Calculator",
        "The Gross-Up Calculator is a free online human resources tool; enter the parameters and get results in real time. Runs entirely in the browser, uploads no data and needs no registration. Runs entirely in the browser, uploads no data, needs no registration, open the browser and use it...",
        "EAP (psychology / counselling / crisis) resource tool. Enter workforce size and psychological support demand to generate EAP psychology, counselling and crisis resource recommendations, for reference when building an employee care system.",
        "Enter headcounts at each recruitment stage (resume screening, interview, offer, onboarding) to compute per-stage conversion rates and the overall pass rate, visualised as a funnel chart that exposes loss points and helps HR assess channel quality and optimise the recruitment process.",
        "Digital (HRIS / self-service / AI) Planning",
        "HRIS / self-service / AI comparison calculator. Enter the parameters of HRIS, employee self-service and AI solutions to compare the cost and efficiency of digital HR management, for reference when selecting a digital HR roadmap.",
        "Attrition (analysis / forecasting / retention) strategy tool. Enter attrition rates, costs and retention measures, and the tool estimates attrition impact and retention priority with general methods, for HR attrition risk management (results are for reference only).",
        "Performance review tool. Computes total performance score, normalisation and ranking through multi-dimensional weighting, for quantitative scoring and grade assignment in employee reviews. Data is processed locally.",
        "Performance score normalisation and ranking tool. Enter raw performance scores for multiple employees, normalise and rank them with grades, supporting fair ordering and result application in performance reviews.",
        "Recruitment (channel / budget / funnel) statistics tool. Enter per-channel spend, resumes and hiring data to compute the recruitment funnel and cost per hire under financial rules, for recruitment budget and channel performance analysis (results are for reference only).",
        "Enter pre- and post-training competency scores and participation details to evaluate reaction, learning, behaviour and results levels with the Kirkpatrick four-level model, for HR training retrospectives.",
        "Attendance Statistics Report",
        "Batch import daily clock-in records to count late arrivals, early departures, absences and leave days, compute individual and team attendance rates, and apply the established deduction rules to salary deductions, producing an exportable attendance report that lightens the HR month-end workload.",
        "Enter annual training records and required hour targets, accumulate completed hours, identify gaps, compute completion rates and list employees below target, helping training administrators track annual continuing education and compliance training progress.",
        "Social Insurance and Housing Fund Breakdown",
        "Enter the contribution base and the rate for each statutory insurance and housing fund item to compute the monthly individual and employer amounts separately. Rates are customisable and results are reference values; actual contributions follow local social insurance policy.",
        "Salary band (range / percentile / equity) design tool. Enter the lower bound, upper bound and midpoint of a grade's salary to compute the salary band, percentile value and internal equity metrics, for pay structure design and benchmarking.",
        "About \"Human Resources Tools\"",
        "The Human Resources Tools collection contains 19 free online tools covering the common calculation, conversion and lookup needs of human resources scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you will find practical tools here that are ready to use the moment you open them. All tools run entirely in the front end and upload no data to the server, protecting privacy and security.",
        "The human resources tools collected on this page include (representative tools):",
        "These tools help you complete common human resources tasks quickly without memorising complex formulas or manual conversions - just enter the values and get the result.",
        "Do the human resources tools need downloading or registration?",
        "No. All human resources tools on this page are pure front-end online tools. Open the page and use them directly, with no software to install, no account to register and no data uploaded.",
        "Are the human resources tool results accurate, and is the data secure?",
        "The tools are based on public mathematical formulas and general industry standards, computing locally in your browser for instant results. All computation happens on your own device and data is never uploaded to the server, so privacy and security are assured.",
    ]))


if __name__ == '__main__':
    main()