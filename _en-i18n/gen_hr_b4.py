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
    write('comp-time-calculator', build('comp-time-calculator', [
        "Comp-Time (Time Off in Lieu) Calculator",
        "/ Comp-Time (Time Off in Lieu) Calculator",
        "📖 Read the \"comp-time-calculator\" guide",
        "🧮 Comp-Time (Time Off in Lieu) Calculator",
        "How much comp-time have you accrued? Using the Labour Law multipliers: weekday overtime 1.5x, rest-day 2x (eligible for time off in lieu), statutory holidays 3x. Enter overtime hours to convert them automatically into days of comp-time.",
        "Overtime hours are converted into comp-time using the Labour Law multipliers: weekday overtime is 1.5x, rest-day overtime is 2x (time off in lieu can be arranged), statutory holiday overtime is 3x (no time off in lieu, overtime pay must be paid); comp-time days = overtime hours × multiplier ÷ 8; rest-day overtime already covered by equal hours of time off in lieu is no longer paid.",
        "Overtime hours",
        "Weekday extension",
        "Rest day",
        "Statutory holiday",
        "Standard daily working hours (h)",
        "📚 Deep dive: converting overtime hours into comp-time entitlement",
        "Rest-day overtime should be covered by time off in lieu first, exchanged at 1:1 for comp-time days.",
        "HR keeps a ledger of each employee's overtime pool and reminds them to use it before it expires.",
        "Take comp-time in a block after a project sprint to balance team workload.",
        "12 days of overtime accumulated, 8 hours per day",
        "At standard working hours, one rest day of overtime exchanges for one day of comp-time → 12 days available; if extended hours are included, it is converted by duration.",
        "5 days used",
        "Remaining comp-time = 12 − 5 = 7 days; the tool tracks the balance and validity period.",
        "Does comp-time expire?",
        "Most companies require last year's overtime to be used before the end of the first quarter of the following year, after which it converts to",
        "overtime pay",
        "— check your own policy for the exact rule.",
        "Can extended weekday overtime be taken as comp-time?",
        "Extended weekday overtime normally pays 150% wages rather than time off in lieu; only rest-day overtime is prioritised for time off in lieu, and the two are handled separately.",
        "Multipliers: weekday 1.5, rest day 2, statutory holiday 3",
        "Comp-time days = overtime hours × multiplier ÷ standard daily working hours",
        "Statutory holiday overtime is in principle paid at 300% wages and is not replaced by comp-time",
        "Results are for reference only; the Labour Law and local implementation rules prevail",
    ]))

    write('performance-ranking', build('performance-ranking', [
        "🎯 Performance Score Normalisation and Ranking",
        "Normalise a person's score against the team maximum (on a 100-point scale) to give the relative gap and ranking percentile for horizontal performance comparison.",
        "📖 Read the \"Performance Score Normalisation and Ranking\" guide",
        "Normalised score = own score ÷ team maximum × 100; relative gap = (maximum − own) ÷ maximum × 100%",
        "Performance normalisation maps scores of different scales and different teams onto the same 0-100 range: normalised score = own ÷ maximum × 100, relative gap = (maximum − own) ÷ maximum, which makes cross-group horizontal ranking straightforward.",
        "Own score",
        "Team maximum score",
        "💡 Normalised score = own ÷ team maximum × 100; relative gap = (maximum − own) ÷ maximum.",
        "📚 Deep dive: performance score normalisation and ranking",
        "Teams use different score scales, so normalise with (score ÷ maximum) × 100 onto a common ruler.",
        "Before applying forced distribution, check whether the normalised distribution is bimodal and then decide the ratios.",
        "Take the top of the normalised ranking in descending order for the promotion shortlist.",
        "Normalised comparison",
        "Group A maximum 85 and Group B maximum 92; a score of 80 in Group A normalises to 80/85×100≈94.1, while 85 in Group B normalises to 85/92×100≈92.4, so that employee in Group A is relatively stronger.",
        "Ranking cutoff",
        "Take the top 20% after normalisation into the promotion pool; the tool marks the cutoff line.",
        "Should I normalise by the maximum or the mean?",
        "Maximum-based normalisation is more sensitive to gaps, while mean-based normalisation is more stable; with small teams the mean is preferable to reduce outlier influence.",
        "Can normalisation replace calibration?",
        "No. Normalisation only resolves scale differences; how strict or lenient the scoring is still has to be settled in a calibration meeting.",
        "About \"Performance Score Normalisation and Ranking\"",
        "Performance Score Normalisation and Ranking. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
        "How to use Performance Score Normalisation and Ranking",
        "What does Performance Score Normalisation and Ranking do?",
        "The Performance Score Normalisation and Ranking tool takes raw performance scores for multiple employees, normalises and ranks them with grades, supporting fair ordering and result application in performance reviews.",
        "How do I use Performance Score Normalisation and Ranking?",
        "Which scenarios suit Performance Score Normalisation and Ranking?",
        "Score A",
        "Score B",
    ]))

    write('performance-score', build('performance-score', [
        "👥 Performance Review",
        "Multi-dimensional weighted calculation of total performance score, normalisation and ranking",
        "📖 Read the \"Performance Review\" guide",
        "Performance = weighted indicators",
        "Normalisation method",
        "Raw weighted score",
        "Min-Max normalisation",
        "Z-Score standardisation",
        "Top performer ratio (%)",
        "Unacceptable ratio (%)",
        "Review dimensions and weights (%)",
        "+ Add dimension",
        "Employee scores",
        "👥 Calculate performance",
        "Weighted score = Σ(dimension score × weight). Min-Max normalises to 0~100; Z-Score reflects relative standing. Forced distribution applies the top and unacceptable ratios.",
        "📚 Deep dive: weighted aggregation of performance indicators",
        "Multi-indicator reviews (results 40%, capability 30%, values 30%) are summed by weight.",
        "When mixing OKR and KPI, assign weights to the different dimensions and combine them into a total score.",
        "Align scales in the calibration meeting to avoid inconsistent strictness across departments.",
        "Three weighted indicators",
        "Results 90×0.4 + capability 80×0.3 + values 95×0.3 = 36+24+28.5 = 88.5 points.",
        "Effect of changing weights",
        "Lowering values from 0.3 to 0.2 and raising results to 0.5 changes the total to 91 for the same inputs; the tool shows weight sensitivity.",
        "How should weights be set to be fair?",
        "Set a baseline top-down based on role value and strategic priorities, then align horizontally in a calibration meeting so managers cannot set them arbitrarily.",
        "Should scores be normalised?",
        "For cross-team comparison, normalise first with performance-ranking and then sort, which is more comparable.",
        "About \"Performance Review\"",
        "Performance Review - score normalisation and ranking, multi-dimensional weighted calculation of total performance score and grade. Free online HR tool. Business and office tool to improve work efficiency, data processed locally to protect privacy.",
    ]))

    write('recruitment-funnel', build('recruitment-funnel', [
        "👥 Recruitment Conversion Analysis",
        "Stage-by-stage conversion rate analysis with a visualised recruitment funnel and per-stage pass rates",
        "📖 Read the \"Recruitment Conversion Analysis\" guide",
        "Recruitment conversion = stage ÷ previous stage",
        "Recruitment scenario",
        "Technical role hiring",
        "Campus recruitment",
        "Sales role hiring",
        "Job title",
        "Recruitment stage",
        "📚 Deep dive: breaking down conversion rates across the recruitment funnel",
        "An HR review of a Java engineer role: 100 resumes → 20 interviews → 5 offers, pinpointing the stage with the biggest loss.",
        "Compare funnels across different jobs to find the root cause of low interview pass rates (question difficulty / pay / location).",
        "Show the business owner the end-to-end conversion efficiency from headcount request to onboarding.",
        "100 resumes / 20 interviews / 5 offers",
        "Resume→interview rate = 20%, interview→offer rate = 25%, overall",
        "conversion rate",
        "= 5%; the tool lists every segment and locates the bottleneck at the interview stage.",
        "Multi-channel comparison",
        "Referrals send 30 and convert 8 while headhunters send 20 and convert 6; computing conversion rates separately shows referrals are more efficient.",
        "When conversion rates drop sharply, which segment do you check first?",
        "Compare adjacent segments first to find the node with the largest period-on-period drop (such as interview→offer), then examine pay competitiveness and interviewer consistency.",
        "Are conversion rates reliable with small samples?",
        "Single-role samples of single digits fluctuate heavily, so aggregate by job family or by quarter before drawing conclusions.",
        "About \"Recruitment Conversion Analysis\"",
        "Recruitment Conversion Analysis - stage-by-stage conversion rate analysis with a visualised recruitment funnel and per-stage pass rates. Free online HR tool. Business and office tool to improve work efficiency, data processed locally to protect privacy.",
    ]))


if __name__ == '__main__':
    main()