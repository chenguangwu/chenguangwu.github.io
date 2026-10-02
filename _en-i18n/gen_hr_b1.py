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
#!/usr/bin/env python3

def main():
    write('analysis-29', build('analysis-29', [
        "\U0001F9D1\u200D\U0001F4BC Turnover Cost and Retention Priority",
        "Estimate the total cost of turnover and the benefit of retention from headcount leaving, replacement cost and time to competence",
        "The real cost of turnover far exceeds the hiring expense: a new hire needs a period of time to become competent before producing, and that period counts as a capacity ramp loss at half of average output per person, which often exceeds the replacement cost itself. The tool adds the two parts to get the total turnover cost and divides it per person to judge a sensible ceiling on retention spending; it also gives the amount saved by cutting turnover by 30% so you can weigh the return on retention measures. Turnover rate uses the period basis (people leaving divided by headcount). All calculations run locally in the browser and no data is uploaded.",
        "\U0001F4D6 See the \"Turnover (Analysis/Forecast/Retention) Strategy User Guide\"",
        "Turnover rate = people leaving \u00F7 headcount \u00D7 100%; replacement cost = people leaving \u00D7 cost per replacement; capacity ramp loss = people leaving \u00D7 time to competence \u00D7 average monthly output \u00D7 50%; total turnover cost = replacement cost + capacity ramp loss",
        "Headcount in post (people)",
        "People leaving in the period (people)",
        "Replacement cost per person (CNY)",
        "Time to competence for a new hire (months)",
        "Average monthly output per person (CNY)",
        "\U0001F4DA In-depth analysis: Turnover Cost and Retention Priority",
        "Annual turnover cost review",
        "Return on investment assessment of retention spending",
        "Attrition risk assessment for core roles",
        "Turnover rate = people leaving \u00F7 headcount \u00D7 100%; replacement cost = people leaving \u00D7 cost per replacement; capacity ramp loss = people leaving \u00D7 time to competence \u00D7 average monthly output \u00D7 50%; total turnover cost = replacement cost + capacity ramp loss.",
        "With 200 in post, 18 leaving, a replacement cost of 24000 CNY each, a 2-month time to competence and average monthly output of 30000 CNY: turnover rate = 18/200 = 9.00%; replacement cost 432000 CNY; capacity ramp loss = 18\u00D72\u00D730000\u00D70.5 = 540000 CNY; total turnover cost 972000 CNY, or 54000 CNY per person; cutting turnover by 30% would save 291600 CNY.",
        "Why is capacity loss counted at 50%?",
        "A new hire's output ramps up during the time to competence, so it is roughly estimated at half of full output; if the role has a long learning curve, raise the time to competence yourself.",
        "At what turnover rate should you worry?",
        "It varies a lot by industry: under 8% is generally low, 8%-15% moderate and above 15% high. Core technical and managerial roles should be tracked separately.",
        "About \"Turnover (Analysis/Forecast/Retention) Strategy\"",
        "Turnover (analysis/forecast/retention) strategy. A free online tool processed entirely in the browser, uploads no data and protects your privacy.",
    ]))

    write('annual-leave-calc', build('annual-leave-calc', [
        "\U0001F9EE Annual Leave Calculator",
        "Calculate the annual leave entitlement from length of service and the full-year working period (reference standard).",
        " / Annual Leave Calculator",
        "\U0001F4D6 See the \"annual-leave-calc User Guide\"",
        "Statutory annual leave is banded by cumulative years of service: 1 to under 10 years gives 5 days, 10 to under 20 years gives 10 days, and 20 years or more gives 15 days. Days for the current year = full-year entitlement \u00D7 remaining months in the year \u00F7 12. Service under 1 year earns no statutory annual leave, and the prorated result is kept to one decimal place.",
        "Continuous service in the current year (years)",
        "Months worked in the current year (default 12)",
        "Calculate annual leave",
        "\U0001F4DA In-depth analysis: Statutory Annual Leave by Cumulative Service",
        "HR works out cumulative service from social insurance records and the labour contract when a new employee joins, to set the annual leave band for that year.",
        "Employees self-estimate how many days they can take in the year, using cumulative service and the months in post.",
        "Each branch applies the same banding in the Regulations on Paid Annual Leave for Employees, avoiding manual errors.",
        "Employee with 5 years of service",
        "Cumulative service of at least 1 but under 10 years \u2192 statutory 5 days; entering tenure=5, months=12 \u2192 5 days entitled.",
        "Employee with 12 years of service",
        "At least 10 but under 20 years \u2192 10 days; tenure=12, months=12 \u2192 10 days. If only 6 months were in post that year, prorate by the remaining calendar days (see the",
        "Annual Leave Proration",
        "tool).",
        "How do company tenure and total service differ?",
        "Statutory annual leave is banded by cumulative service including previous employers, while company tenure usually only affects extra company benefits, so the two are accounted for separately.",
        "How is someone who joined mid-year handled?",
        "The full band is only given if you worked the whole year; if you were in post for only part of the year, prorate by the remaining calendar days, which the annual leave proration tool handles.",
    ]))

    write('annual-leave-prorate', build('annual-leave-prorate', [
        " / Annual Leave Proration Calculator",
        "\U0001F4D6 See the \"annual-leave-prorate User Guide\"",
        "\U0001F9EE Annual Leave Proration Calculator",
        "If someone joins or leaves mid-year, annual leave is prorated by the remaining calendar days. Enter the start date, cumulative service and the proration cut-off date to get the year's entitlement automatically.",
        "Cumulative service (years)",
        "Proration cut-off date (31/12 of that year, or the leaving date)",
        "\U0001F4DA In-depth analysis: Prorating Annual Leave in the Year of Joining or Leaving",
        "For a new employee who joined in March, the year's entitlement is prorated by the share of calendar days from the start date to year end.",
        "For someone leaving during the year, prorate by the last day in post, and HR uses this to settle pay for untaken annual leave.",
        "Cumulative service sets the band, and multiplying by the share of days in post gives the usable days.",
        "Joined 15 March with 5 years of service, cut-off 31 December",
        "Band 5 days; days in post = 365\u221274 = 291; prorated = 291/365\u00D75 \u2248 3.99 \u2192 fractions under 0.5 days are not counted, so 3.5 days are actually available.",
        "Left on 1 November with 12 years of service",
        "Band 10 days; days in post = 305; prorated = 305/365\u00D710 \u2248 8.36 \u2192 rounded to 8 days.",
        "How is a fraction under 1 day handled?",
        "Under the regulations, fractions of a full day are usually not prorated; many companies use 0.5 day as the smallest unit, so follow your own company policy.",
        "Does a leap year change the calculation?",
        "The denominator uses the actual days in that year (366 in a leap year) and the numerator the real days in post, so the ratio method adapts automatically.",
        "1-9 years of service gives 5 days, 10-19 years gives 10 days, 20 or more gives 15 days",
        "Mid-year joiners and leavers are prorated by the share of remaining calendar days, with fractions under 0.5 day not counted",
        "Prorated = base \u00D7 days in post that year \u00F7 365",
        "The result is for reference only; the Regulations on Paid Annual Leave for Employees and your organisation's policy govern.",
    ]))


if __name__ == '__main__':
    main()
