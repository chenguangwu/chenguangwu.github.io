#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'exhibition')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'exhibition')
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
    out = {'slug': slug, 'industry': 'exhibition', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # ---------- assessor-61 (40) ----------
    slug = 'assessor-61'
    en = [
        '🎪 Exhibition Assessment, Metrics & Optimization System',
        'Assessment / Metrics / Optimization',
        '📖 View "Exhibition Assessment, Metrics & Optimization System User Guide"',
        'Overall exhibition assessment = scale + audience quality + brand exposure + lead efficiency + organization service + ROI (6 items, each scored 1 to 5); average score = total ÷ 6; average ≥ 4.5 is excellent, 3.5–4.4 good, 2.5–3.4 fair, below 2.5 poor; recommend long-term investment in exhibitions with average ≥ 4.5 and build an optimization checklist by the lowest-scored dimension.',
        'Exhibition Comprehensive Assessment Indicator System (6 dimensions, 1–5 points each)',
        '1. Participation Scale (exhibitors / area)',
        'Large (5 pts)',
        'Fairly large (4 pts)',
        'Medium (3 pts)',
        'Relatively small (2 pts)',
        'Very small (1 pt)',
        '2. Audience Quality (professionalism)',
        'Very high (5 pts)',
        'High (4 pts)',
        'Very poor (1 pt)',
        '3. Brand Exposure Effect',
        'Highly effective (5 pts)',
        'Poor (2 pts)',
        'Extremely poor (1 pt)',
        '4. Lead Acquisition Efficiency',
        'Very low (1 pt)',
        '5. Organization Service (process / support)',
        '6. Return on Investment (ROI)',
        'Far exceeds expectations (5 pts)',
        'Exceeds expectations (4 pts)',
        'In line (3 pts)',
        'Below expectations (2 pts)',
        'Assessment Indicators',
        '📚 In-Depth Analysis: Exhibition Assessment, Metrics & Optimization System',
        'Score each of the 6 dimensions—participation scale, audience quality, brand exposure, lead efficiency, organization service, ROI—from 1 to 5 to quantify a single exhibition’s overall performance.',
        'After scoring multiple exhibitions side by side, rank them by total score to identify consistently high scorers (key annual shows) and persistently low scorers (suspend or replace).',
        'Highlight weak dimensions scored ≤ 2 to form the next show’s improvement checklist and drive continuous optimization.',
        'Composite Score Example',
        'The 6 dimensions are scored "fairly large (4)", "high (4)", "good (4)", "very high (5)", "good (4)", "exceeds expectations (4)"; composite score 25/30 (mean 4.17), rated "good assessment", no weak items, recommend continued participation with detail optimization.',
        'How are the scoring criteria defined?',
        'You assign each dimension 1–5 by your actual experience; the tool only aggregates and averages. Companies may build their own scorecard to anchor each level’s definition for cross-show consistency.',
        'Can scoring replace professional assessment?',
        'No. This tool is a lightweight self-assessment scoring, suitable for quick review and side-by-side comparison; major decisions still require business data and on-site inspection.',
        'About the "Exhibition Assessment, Metrics & Optimization System"',
        'Exhibition Assessment, Metrics & Optimization System. A free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.',
    ]
    write(slug, build(slug, en))

    # ---------- assessor-evacuation (33) ----------
    slug = 'assessor-evacuation'
    en = [
        'Safety (Evacuation / Fire / Load-Bearing) Assessment',
        'Evacuation / Fire / Load-Bearing',
        '📖 View "Safety (Evacuation, Fire & Load-Bearing) Assessment User Guide"',
        'Venue safe evacuation is assessed by 6 checks (evacuation routes, safe exits, fire facilities, approved capacity, aisle width, evacuation distance): required safe exits = designed headcount ÷ single-exit capacity (≈250 people per exit); minimum aisle width = 0.6 m per 100 people; evacuation distance usually ≤ 30 m (dead-end corridor ≤ 22 m); if measured occupancy exceeds approved capacity, it is overcrowded and flow control must start immediately.',
        'Venue Safe Evacuation and Fire/Load-Bearing Assessment (6 checks)',
        'Exhibition Hall Area (m²)',
        'Expected Occupancy',
        'Number of Evacuation Exits',
        'Evacuation Aisle Width (m)',
        'Maximum Evacuation Distance (m)',
        'Floor Load (kN/m²)',
        'Automatic Fire Alarm System',
        'Automatic Sprinkler System',
        'Mechanical Smoke Extraction System',
        'Emergency Lighting',
        'Emergency Broadcast',
        'Assess Safety',
        '📚 In-Depth Analysis: Safety (Evacuation, Fire & Load-Bearing) Assessment',
        'Enter hall area, occupancy, exit count and aisle width to estimate crowd density and total required evacuation width, catching overcrowding or insufficient passages early.',
        'Check against the maximum evacuation distance and floor-load thresholds to identify risk points with evacuation distance over 40 m or insufficient load-bearing capacity, and require remediation.',
        'Tick the presence of 5 fire facilities—alarm, sprinkler, smoke extraction, emergency lighting, emergency broadcast; unticked items are automatically counted as hazards and a remediation list is output.',
        'Venue Safety Example',
        'Area 5000 m², occupancy 2000, 4 exits each 3 m wide, max evacuation distance 35 m, floor load 5 kN/m², all 5 fire systems present: crowd density 0.4 person/m², estimated',
        'Evacuation Time',
        'about 5.5 minutes, hazards 0, conclusion "safe and compliant".',
        'How is evacuation time estimated?',
        'By headcount ÷ (total exit width × per-width',
        'Passage Capacity',
        '55 people/min) × 60 as approximation; this is a rough engineering estimate—formal evacuation design should follow fire codes.',
        'Where do the thresholds (0.5 person/m², 40 m, 4 kN/m²) come from?',
        'They are common exhibition-safety reference values for quick screening; specific limits vary with venue type and local fire regulations, and formal review should follow the code documents.',
        'About the "Safety (Evacuation, Fire & Load-Bearing) Assessment"',
        'Safety (Evacuation, Fire & Load-Bearing) Assessment. A free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.',
    ]
    write(slug, build(slug, en))

    # ---------- index (17) ----------
    slug = 'index'
    en = [
        '🎫 Exhibition Service Tools',
        'Exhibition Services',
        'Exhibition Service Tools',
        'Exhibition composite assessment indicator tool. Quantifies exhibition effectiveness across 6 dimensions (1–5 points each), aggregates scores and gives optimization suggestions for standardized exhibition management and continuous improvement.',
        'Venue safe evacuation / fire / load-bearing assessment tool. Evaluates evacuation routes, fire facilities and structural load safety against a 6-item checklist, outputs risk items and remediation suggestions to protect exhibition personnel.',
        'Post-show assessment / report / follow-up summary tool. Generates post-exhibition effectiveness evaluation and follow-up reports along the dimensions of ROI analysis and customer follow-up, helping sales teams capture leads and review outcomes.',
        'Exhibition budget (cost / control / optimization) analysis tool. Inputs each exhibition expense and revenue, computes cost structure by general financial rules and gives control/optimization advice for participation cost management and ROI evaluation.',
        'Exhibition budget (revenue / expense / profit-loss) analysis tool. Inputs participation revenue and expenses, calculates break-even and net profit to support financial decisions and budgeting for exhibition projects.',
        'Audience statistics / behavior / feedback research tool. Inputs audience traffic, dwell time and survey feedback, computes means, proportions and correlations by standard statistical methods for exhibition operation optimization and audience profiling.',
        'About "Exhibition Service Tools"',
        'The Exhibition Service Tools collection includes 6 free online tools covering common calculation, conversion and lookup needs in exhibition services. Whether you are a professional, student or general user, you can find ready-to-use mini tools here. All tools run purely in the browser; no data is uploaded to servers, protecting your privacy.',
        'The exhibition service tools featured on this page include (representative samples):',
        'These tools help you quickly complete common exhibition-service tasks without memorizing complex formulas or manual conversions—just enter to get results.',
        'Do the exhibition service tools need download or registration?',
        'No. All exhibition service tools on this page are pure front-end online tools—open the page and use them directly, no software install, no account registration, and no data upload.',
        'Are the exhibition service tools’ results accurate? Is the data safe?',
        'The tools compute locally in your browser based on public mathematical formulas and general industry standards, with results available instantly. All calculations are done on your device; data is never uploaded to servers, ensuring privacy and security.',
    ]
    write(slug, build(slug, en))

    # ---------- stats-12 (23) ----------
    slug = 'stats-12'
    en = [
        '🎪 Audience (Statistics / Behavior / Feedback) Research',
        'Enter traffic per time slot, dwell time and survey scores separately to quantify audience behavior',
        '📖 View "Audience (Statistics, Behavior & Feedback) Research User Guide"',
        'Traffic: sum headcounts per time slot for total traffic, take the max as peak slot, compute average pace. Dwell time: use mean, median and range to characterize the distribution. Survey scores (1–5): use mean and standard deviation to measure experience stability; smaller SD means more stable.',
        '① Audience traffic per time slot (each line "slot,count")',
        '② Dwell-time samples (minutes, comma- or newline-separated)',
        '③ Survey scores (1–5, comma- or newline-separated)',
        '📚 In-Depth Analysis: Audience (Statistics, Behavior & Feedback) Research',
        'Enter the audience traffic per time slot (e.g., hourly visits) and use',
        'Descriptive Statistics',
        'the mean, peak and fluctuation to judge crowded periods and traffic-pacing rhythm.',
        'Aggregate survey feedback scores (satisfaction 1–5) and compute the mean and',
        ', quantify audience experience stability and locate areas needing improvement.',
        'Compare the dwell time across different exhibition zones’',
        'and range to identify high-attraction and low-stickiness zones, optimizing circulation and content layout.',
        'Audience Data Example',
        'Input a set of dwell times (e.g., 3, 5, 8, 12, 6, 4, 9 minutes); the tool outputs count 7, sum 47, mean ≈ 6.71, median 6, range 9, variance and standard deviation, helping characterize the audience behavior distribution.',
        'Can the tool compute correlation?',
        'This tool provides single-group descriptive statistics (mean, variance, etc.) and does not compute correlation directly; for multivariate correlation, export the data to professional statistical software.',
        'Are small-sample results reliable?',
        'The statistics themselves are accurate, but small samples (e.g., fewer than 10 entries) have limited representativeness; conclusions are for reference only—accumulate enough samples before judging.',
        'About "Audience (Statistics, Behavior & Feedback) Research"',
        'Audience (Statistics, Behavior & Feedback) Research. A free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.',
    ]
    write(slug, build(slug, en))


if __name__ == '__main__':
    main()
