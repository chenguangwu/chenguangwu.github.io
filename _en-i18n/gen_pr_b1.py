#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'pr')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'pr')
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
    out = {'slug': slug, 'industry': 'pr', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('assessor-56', build('assessor-56', [
        "📢 Event (Planning/Execution/Evaluation) Full Plan",
        "A structured score of the whole PR event process from planning through execution to evaluation, covering six dimensions: goal setting, budget management, audience analysis, channel strategy, execution quality and effect evaluation.",
        "📖 View the usage guide for 'Event (Planning/Execution/Evaluation) Full Plan'",
        "PR event full-plan score = goal setting + budget management + audience analysis + channel strategy + execution quality + effect evaluation (0 to 5 points each, 30 in total); 25 or above is excellent, 20 to 24 is good, 15 to 19 is qualified, and below 15 is unqualified, requiring the planning scheme to be re-evaluated.",
        "1. Goal clarity (SMART principle)",
        "5-Goals are explicit and quantifiable",
        "4-Fairly clear",
        "3-Basic clarity",
        "2-Not explicit enough",
        "1-Goals are vague",
        "2. Budget reasonableness",
        "5-Budget is sufficient and reasonable",
        "4-Basicly reasonable",
        "3-Slight deviation",
        "2-Clearly insufficient",
        "3. Audience targeting precision",
        "5-Precise targeting",
        "4-Fairly precise",
        "3-Basicly in place",
        "2-Vague targeting",
        "1-Lacking targeting",
        "4. Channel strategy diversity",
        "5-Multi-channel synergy",
        "4-Fairly rich channels",
        "3-Average channels",
        "2-Single channel",
        "1-No strategy",
        "5. Execution quality",
        "5-Excellent execution",
        "4-Good execution",
        "3-Average execution",
        "2-Poor execution",
        "1-Chaotic execution",
        "6. Effect evaluation completeness",
        "5-Evaluation system is complete",
        "1-No evaluation",
        "The assessment covers 6 core dimensions across the three stages of planning, execution and evaluation",
        "Complete the evaluation within 1-2 weeks after the event ends to ensure the data is accurate",
        "A total score above 25 is excellent, and 20 or above is good",
        "Dimensions scoring below 3 need focused attention and improvement",
        "📚 Deep Dive: Event (Planning/Execution/Evaluation) Full Plan",
        "After an offline event wraps up, score 0-5 on each of the six dimensions of goal setting, budget, audience, channel, execution and effect to quantify the quality of the whole plan.",
        "Compare the scores of the same event at the planning stage (before) and the review (after) to see whether execution fell short.",
        "Rank the scores of multiple events horizontally to identify which event types (launch/pop-up/salon) consistently score high and are reproducible.",
        "Scoring criteria",
        "6 dimensions, 0-5 points each: ① goal setting ② budget management ③ audience analysis ④ channel strategy ⑤ execution quality ⑥ effect evaluation; total = the sum of the six, 30 in total. Grades: ≥25 excellent, ≥20 good, ≥15 qualified, <15 unqualified.",
        "A product launch scores goal 5 + budget 5 + audience 4 + channel 5 + execution 5 + effect 4 = 28 points, judged excellent (≥25), and the tool suggests 'reuse it as a benchmark case'. By contrast, a hastily organised market scores goal 2 + budget 2 + audience 1 + channel 2 + execution 1 + effect 1 = 9 points, judged unqualified (<15), and the tool suggests 're-evaluate the planning scheme'. The gap between 28 and 9 comes mainly from audience analysis and execution quality, which are the review focus.",
        "Are the scoring dimensions all weighted equally?",
        "This tool uses equal weights (0-5 each, 30 in total). In real management effect evaluation is often more critical; if you want to apply weights (e.g. effect at 30%), adjust the weights yourself when interpreting the total, or reflect the weight difference in the sub-scores. Equal weights suit quick horizontal comparison.",
        "Can data on unqualified events be reported externally as is?",
        "It is not recommended. An unqualified score usually means 'meets the basic standard but needs improvement' or even 'has substantial problems'; internally it is review input, while externally you should present the improved version or a desensitised summary of results. The scores from this tool serve only as an internal quality benchmark.",
        "About 'Event (Planning/Execution/Evaluation) Full Plan'",
        "The PR event full-plan assessment tool quantifies an event across six dimensions - goal setting, budget management, audience analysis, channel strategy, execution quality and effect evaluation - helping PR teams review event results systematically.",
        "Full-process assessment across 6 dimensions",
        "SMART principle benchmarking",
        "PR event review and assessment",
        "Event scheme review",
        "Team performance assessment",
        "Event effect benchmark analysis",
    ]))

    write('assessor-manager-2', build('assessor-manager-2', [
        "🚀 Reputation (Management/Assessment/Improvement) Strategy",
        "A systematic assessment of corporate brand reputation covering five dimensions - brand awareness, public trust, crisis resilience, stakeholder relations and online reputation - to help formulate reputation improvement strategies.",
        "📖 View the usage guide for 'Reputation (Management/Assessment/Improvement) Strategy'",
        "Brand reputation composite score = brand awareness + public trust + crisis resilience + stakeholder relations + online reputation (0 to 5 points each, 25 in total); 21 or above is outstanding reputation, 17 to 20 is good, 12 to 16 is average, and below 12 is reputation risk requiring an immediate repair plan.",
        "1. Brand awareness",
        "5-High awareness",
        "4-Fairly high awareness",
        "3-Medium awareness",
        "2-Low awareness",
        "1-Almost unknown",
        "2. Public trust",
        "5-High trust",
        "4-Fairly trusting",
        "3-Average trust",
        "2-Insufficient trust",
        "1-Trust crisis",
        "3. Crisis response resilience",
        "5-Very strong resilience",
        "4-Fairly strong resilience",
        "3-Average resilience",
        "2-Insufficient resilience",
        "1-No response capability",
        "4. Stakeholder relations",
        "5-Good relations",
        "4-Fairly good relations",
        "3-Average relations",
        "2-Tense relations",
        "1-Deteriorating relations",
        "5. Online reputation (search/social)",
        "5-Positive and dominant",
        "4-Mainly positive",
        "3-Positive and negative about equal",
        "2-Mainly negative",
        "3-Negative and dominant",
        "Reputation assessment should be carried out regularly (quarterly is recommended)",
        "Online reputation can be monitored through search keywords and social media public opinion",
        "Dimensions scoring below 3 need focused improvement",
        "Crisis resilience is the core defence line of reputation management",
        "📚 Deep Dive: Reputation (Management/Assessment/Improvement) Strategy",
        "In the quarterly brand health review, score 0-5 on each of the five items - brand awareness, public trust, crisis resilience, stakeholders and online reputation - to quantify the reputation level.",
        "Assess once before and once after a crisis to see whether the crisis resilience score drops sharply and to evaluate the progress of reputation repair.",
        "Weak dimensions scoring ≤2 are automatically flagged in red as the priority investment direction for the next quarter's reputation improvement.",
        "Scoring criteria",
        "5 dimensions, 0-5 points each: ① brand awareness ② public trust ③ crisis resilience ④ stakeholders (employees/regulators/community) ⑤ online reputation; total = the sum of the five, 25 in total. Grades: ≥21 outstanding reputation, ≥17 good, ≥12 average, <12 reputation risk. Any dimension scoring ≤2 is listed as a 'dimension needing improvement'.",
        "A mature brand scores awareness 5 + trust 5 + resilience 4 + stakeholders 5 + online 4 = 23 points, judged outstanding reputation with no weak dimensions. By contrast, a brand that just went through a quality complaint scores awareness 2 + trust 1 + resilience 2 + stakeholders 1 + online 1 = 7 points, judged reputation risk, with all five dimensions - brand awareness, public trust, crisis resilience, stakeholders and online reputation - flagged as needing improvement. This shows it is not a single-point problem but a systemic trust collapse, requiring an overall reputation repair rather than a local patch.",
        "Can a low reputation score always be recovered?",
        "It depends on the root cause. If the low score comes from verifiable factual problems (quality, compliance), the precondition for repair is to close the loop on the facts first; a reputation tool is only a 'water level gauge', not a 'repair agent'. If the low score comes from misunderstanding or information gaps, it can recover fairly quickly through transparent communication. The weak dimensions flagged by this tool help you locate the priority.",
        "What is the difference between online reputation and brand awareness?",
        "Brand awareness measures 'how many people know you and what they know', while online reputation measures 'the sentiment and word of mouth in the online voice'. A brand may have high awareness (everyone knows it) but poor online reputation (search results are all negative). When both are low it is most dangerous, because negative sentiment spreads quickly under high awareness.",
        "About 'Reputation (Management/Assessment/Improvement) Strategy'",
        "The brand reputation assessment tool evaluates a company's reputation across five dimensions - brand awareness, public trust, crisis resilience, stakeholder relations and online reputation - helping identify reputation risk and formulate improvement strategies.",
        "Reputation assessment across 5 dimensions",
        "Automatic identification of weak dimensions",
        "Reputation risk warning",
        "Regular brand reputation assessment",
        "Post-crisis reputation repair",
        "Annual reputation report",
    ]))

    write('assessor-57', build('assessor-57', [
        "📋 CSR (Project/Communication/Evaluation) Planning",
        "A full-chain score of a corporate social responsibility (CSR) project from project design and communication strategy through to effect evaluation, covering five dimensions: social value, stakeholders, communication strategy, sustainability and the evaluation system.",
        "📖 View the usage guide for 'CSR (Project/Communication/Evaluation) Planning'",
        "CSR project score = social value + stakeholders + communication strategy + sustainability + evaluation system (0 to 5 points each, 25 in total); 21 or above is excellent, 17 to 20 is good, 12 to 16 is qualified, and below 12 is unqualified, requiring the project framework to be redesigned.",
        "1. Project social value and match with social needs",
        "5-Highly matches social needs",
        "4-Matches fairly well",
        "3-Matches basically",
        "2-Low match",
        "1-Detached from real needs",
        "2. Stakeholder participation",
        "5-Deep participation by multiple parties",
        "4-Fairly good participation",
        "3-Basic participation",
        "2-Insufficient participation",
        "1-Lacking participation",
        "3. Communication strategy effectiveness",
        "5-Precise and effective communication strategy",
        "4-Fairly good strategy",
        "3-Average strategy",
        "2-Weak strategy",
        "1-No communication strategy",
        "4. Project sustainability",
        "5-Long-term sustainable",
        "4-Fairly sustainable",
        "3-Feasible in the short term",
        "2-Weak sustainability",
        "1-One-off project",
        "5. Effect evaluation and SDG alignment",
        "5-Complete evaluation and aligned with the SDGs",
        "1-No evaluation system",
        "CSR projects should address real social needs and avoid vanity projects",
        "Assessment against the UN Sustainable Development Goals (SDGs) is recommended",
        "Stakeholders include communities, government, NGOs, employees, customers and others",
        "Sustainability is an important evaluation dimension for CSR projects",
        "📚 Deep Dive: CSR (Project/Communication/Evaluation) Planning",
        "Before a CSR project is approved, score 0-5 on each of the five dimensions of social value, stakeholders, communication strategy, sustainability and the evaluation system to predict the quality of the project.",
        "Re-assess at the mid-project review to see whether communication and sustainability have kept up, avoiding 'doing it but not saying it' or 'a passing flurry'.",
        "Score and rank several CSR topics together, prioritising projects that score high and fit the corporate strategy.",
        "Scoring criteria",
        "5 dimensions, 0-5 points each: ① social value ② stakeholders (coverage and participation) ③ communication strategy ④ sustainability ⑤ evaluation system; total = the sum of the five, 25 in total. Grades: ≥21 excellent, ≥17 good, ≥12 qualified, <12 unqualified.",
        "A rural revitalisation project scores social value 5 + stakeholders 4 + communication 5 + sustainability 4 + evaluation 4 = 22 points, judged excellent (≥21), and the tool suggests 'roll it out'. By contrast, a tokenistic charitable donation scores social value 3 + stakeholders 3 + communication 2 + sustainability 2 + evaluation 3 = 13 points, judged qualified (≥12), but the low communication and sustainability scores flag the pattern that 'donations are easy, long-term mechanisms are weak', so communication and closed-loop evaluation need to be added.",
        "Does a high CSR score mean a large social contribution?",
        "A high score means 'balanced, communicable and sustainable design', but it does not mean an absolutely large contribution. This tool is a quality prediction benchmark before approval; real contribution depends on the measurable outputs after delivery (beneficiaries, emission reductions, employment created, etc.). An excellent score should be a signal that the project is 'worth investing in', not proof of results.",
        "Why is the 'evaluation system' listed as a separate dimension?",
        "Many CSR projects fail at 'did it but no _measure' - there are events but no data, so nothing can be reported to regulators, ESG raters or the public. Listing the evaluation system separately forces the metrics, data definitions and third-party verification to be thought through at approval time, avoiding having nothing to report at year end.",
        "About 'CSR (Project/Communication/Evaluation) Planning'",
        "The CSR project assessment tool quantifies corporate social responsibility projects across five dimensions - social value, stakeholder participation, communication strategy, sustainability and effect evaluation - helping CSR teams evaluate project quality and impact.",
        "5-dimension CSR assessment framework",
        "Assessment aligned with the SDGs",
        "CSR project approval review",
        "Mid-project execution review",
        "CSR report preparation",
        "ESG rating reference",
    ]))


if __name__ == '__main__':
    main()
