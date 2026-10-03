#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'project')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'project')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    return mp


def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'project', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

#!/usr/bin/env python3


def main():
    write('analysis-28', build('analysis-28', [
        '📊 Stakeholder (Interest / Influence) Analysis',
        'Classify stakeholders by power and interest and output four-quadrant management strategies (manage closely / keep satisfied / keep informed / monitor)',
        '📖 View the Stakeholder (Interest / Influence) Analysis user guide',
        'Attention level = power × interest; the high or low power × high or low interest combination places the stakeholder in one of four quadrants',
        '+ Add stakeholder',
        'Analyse matrix',
        '📚 In-depth analysis: Stakeholder (Interest / Influence) Analysis',
        'Stakeholder identification and classification at project start-up: score the owner, designer, contractor, supervisor, government regulators and neighbouring residents from 1 to 5 on power (the ability to influence decisions) and interest (the degree of being affected by the project), and place them in four quadrants to determine differentiated management strategies.',
        'Communication during major changes or crises: when a change touches strongly interested parties, use the matrix to quickly lock onto the manage-closely group, prioritise one-to-one communication, and avoid missing key opponents whose objection could sink the change.',
        'Stakeholder engagement under limited resources: control the frequency and form of communication with the high-power, low-interest keep-satisfied group, use routine weekly reports for the low-power, high-interest keep-informed group, and spend limited effort on high-value communication.',
        'Worked example: positioning four typical stakeholders',
        'Enter 4 stakeholders (power 1-5, interest 1-5): owner (5,5) → attention 25 → manage closely (key player); government regulator (5,2) → attention 10 → keep satisfied; construction crew (2,5) → attention 10 → keep informed; neighbouring residents (1,2) → attention 2 → monitor. Rules: power ≥ 3 and interest ≥ 3 → manage closely; power ≥ 3 and interest < 3 → keep satisfied; power < 3 and interest ≥ 3 → keep informed; power < 3 and interest < 3 → monitor. The result shows the owner should be the top priority, the regulator satisfied through periodic reporting to senior management on its key demands, the crew kept transparent with weekly reports, and the residents only monitored at minimum cost.',
        'How are power and interest scored — is it too subjective?',
        'Use relative scoring (1-5) rather than absolute measurement: compare all parties horizontally first, then assign the band. You can refer to the usual positions in the Mendelow power-interest matrix — the owner or investor is usually high power and high interest, government regulators high power and low interest, front-line delivery teams low power and high interest, and the general public low power and low interest. The scores need not be exact; the point is to separate out who should be managed closely. Score jointly with the core team at project start-up and keep a record.',
        'What response strategy fits each of the four quadrants?',
        'Manage closely (high power, high interest): involve them deeply, decide jointly and communicate one-to-one at high frequency so they become project drivers. Keep satisfied (high power, low interest): report to senior management periodically and meet their key demands precisely, so they do not oppose the project because they feel ignored. Keep informed (low power, high interest): keep information transparent through weekly reports and review meetings so they feel respected. Monitor (low power, low interest): track developments at minimum cost and escalate communication only when needed. Strategies are adjusted dynamically as the project moves through stages.',
        'About Stakeholder (Interest / Influence) Analysis',
        'A stakeholder (interest / influence) analysis tool. A free online tool that runs entirely in the browser; data is never uploaded, keeping your privacy safe.',
    ]))

    write('assessor-risk-9', build('assessor-risk-9', [
        '📋 Risk (Identification / Assessment / Response) Cycle',
        'Project risk identification and assessment: 5 risks, probability × impact = risk value (1-25), automatically graded with response strategies',
        '📖 View the Risk (Identification / Assessment / Response) Cycle user guide',
        'Single risk value = probability of occurrence (1 to 5) × degree of impact (1 to 5), ranging from 1 to 25; risk levels are cut by score: up to 4 is low, 5 to 9 medium, 10 to 15 elevated, 16 to 25 high; the overall risk level takes the maximum across items; response strategies are matched to the level (accept for low, mitigate for medium, transfer for elevated, avoid for high), and high-risk items require a dedicated plan with a named owner.',
        'Risk 1: probability',
        '1-very low (<10%)',
        '2-low (10-30%)',
        '3-medium (30-50%)',
        '4-high (50-70%)',
        '5-very high (>70%)',
        'Risk 1: impact',
        '1-minimal',
        '2-minor',
        '4-major',
        '5-severe',
        'Risk 2: probability',
        'Risk 2: impact',
        'Risk 3: probability',
        'Risk 3: impact',
        'Risk 4: probability',
        'Risk 4: impact',
        'Risk 5: probability',
        'Risk 5: impact',
        '📚 In-depth analysis: Risk (Identification / Assessment / Response) Cycle',
        'Initial risk assessment at project initiation or feasibility study: list 5 key risks (such as cost overrun, schedule delay, quality defects, safety incidents and scope change), score each by probability × impact, and locate the very high risk items to respond to first.',
        'Risk pricing before bidding: turn high-probability, high-impact risks into a premium or contingency, supporting quotation and contract risk-allocation decisions.',
        'Periodic risk re-assessment in operations or production: re-score every quarter and track how the risk value moves (for example one risk rising from probability 3 to 4), adjusting response strategies and resource allocation dynamically.',
        'Worked example: scoring a 5-item risk matrix',
        '5 risks (probability 1-5 × impact 1-5): cost overrun (4,4) = 16 → very high risk; schedule delay (3,3) = 9 → medium risk; quality defects (2,5) = 10 → high risk; safety incident (1,2) = 2 → low risk; scope change (5,3) = 15 → high risk. The highest risk value is 16 (very high), and 3 items need priority response (risk value ≥ 10): cost overrun, quality defects and scope change. Grading thresholds follow the 5 × 5 = 25-cell matrix: ≤4 low, 5-9 medium, 10-15 high, 16-25 very high. Conclusion: cost overrun is the top risk and must be avoided or transferred; quality defects and scope change must be mitigated with a plan prepared; schedule delay should be mitigated; the safety incident is accepted and monitored routinely.',
        'Where do the 5×5 matrix thresholds (4/9/15) come from?',
        'From the probability-impact matrix, the common practice in PMBOK qualitative risk analysis: of the 25 cells, products 1-4 are low (the small-value region at the lower right), 5-9 medium, 10-15 high and 16-25 very high (the large-value region at the upper left), matching the four bands of organisational risk tolerance. The thresholds can be adjusted by industry — for low-tolerance sectors such as nuclear power or chemicals, the high line can drop to 8 to intercept risks more conservatively. The key is that the whole organisation aligns on the same basis and keeps it consistent across re-assessments.',
        'Must a high risk value always be avoided?',
        'Not necessarily; the strategy depends on cost-benefit and risk appetite: very high risks (such as the top cost-overrun item) are first avoided or transferred through insurance or subcontracting; high risks can be transferred plus mitigated by buying insurance and adding a plan; medium risks are mainly mitigated plus accepted; low risks are accepted and monitored routinely. High-impact, low-probability risks (such as quality defects at 2 × 5 = 10) are usually transferred or mitigated through contingency reserves and quality gates rather than simply abandoning the project. Strategies should be written into the risk register and re-assessed periodically.',
        'About Risk (Identification / Assessment / Response) Cycle',
        'A risk (identification / assessment / response) cycle tool. A free online tool that runs entirely in the browser; data is never uploaded, keeping your privacy safe.',
    ]))

    write('checker-12', build('checker-12', [
        '✅ Supervision (Duties / Inspection / Reporting) Work',
        'Engineering supervision work checklist (10 items, 2 points for compliant, 1 for partially compliant, 0 for non-compliant; full score 20)',
        '📖 View the Supervision (Duties / Inspection / Reporting) Work user guide',
        'The engineering supervision checklist has 10 items (quality control system, construction safety supervision, schedule plan management, cost and investment control, contract and change management, supervision log and monthly report, concealed work acceptance, side-by-side supervision records, coordination and communication mechanism, completion acceptance preparation), scored 2 for compliant, 1 for partially compliant and 0 for non-compliant, with a full score of 20; 18 or above is excellent, 14 to 17 good, 10 to 13 pass, and below 10 fail with rectification required within a deadline.',
        '1. Quality control system',
        'Compliant (2 points)',
        'Partially compliant (1 point)',
        'Non-compliant (0 points)',
        '2. Construction safety supervision',
        '3. Schedule plan management',
        '4. Cost / investment control',
        '5. Contract and change management',
        '6. Supervision log and monthly report',
        '7. Concealed work acceptance',
        '8. Side-by-side supervision records',
        '9. Coordination and communication mechanism',
        '10. Completion acceptance preparation',
        '📚 In-depth analysis: Supervision (Duties / Inspection / Reporting) Work',
        'Monthly assessment of supervision performance during construction: score the 10 items one by one (quality control system, construction safety supervision, schedule plan management, cost or investment control, contract and change management, supervision log and monthly report, concealed work acceptance, side-by-side supervision records, coordination and communication mechanism, completion acceptance preparation), output the score and grade, and use it as the basis for supervision fee payment and re-appointment.',
        'Self-check when setting up a supervision department for a new project: check for gaps against the list before start-up, making sure the system, archives, certificates and emergency plans are in place, so as to avoid being reported by the quality and safety supervision station or delaying the start.',
        'Third-party inspection or unannounced inspection rehearsal: score in advance with the same table to locate weak points (such as missing side-by-side records or delayed concealed work acceptance) and rectify them, reducing the risk of penalties.',
        'Worked example: 16 points from a mixed assessment of 10 items',
        'The 10 item scores are [compliant, compliant, partially compliant, compliant, partially compliant, compliant, partially compliant, partially compliant, compliant, compliant], i.e. 2/2/1/2/1/2/1/1/2/2, totalling 16 points. Full score 20, pass rate = 16 ÷ 20 × 100% = 80%. Grading thresholds: ≥18 excellent, ≥14 good, ≥10 fair, <10 fail. This example at 16 points is good, and the tool notes that requirements are basically met and continuous improvement on weak points is recommended; the weak points are items 3, 5, 7 and 8 (partially compliant), so priority should go to strengthening quality control, safety supervision, concealed work acceptance and side-by-side records.',
        'How were the 20-point grading thresholds (18/14/10) set?',
        'Thresholds are set by ',
        ' as follows: excellent ≥90% (18 points), good ≥70% (14 points), fair ≥50% (10 points), fail below 50%. These thresholds suit most supervision performance evaluations; if the project is highly complex or the contract is stricter, the good line can be raised to 16 points (80%) for stronger binding force. The thresholds should be stated in the evaluation scheme in advance to avoid later disputes.',
        'Can this checklist serve directly as legal evidence of supervision performance?',
        'No. This tool is a quick scoring table for self-check and rehearsal and does not constitute a legal performance record. Formal supervision performance is evidenced by signed and sealed supervision logs, side-by-side supervision records, concealed work acceptance forms, supervision notices and monthly reports, which carry legal weight in quality incidents or audits. Turn the results of this table into concrete rectification tasks and record them formally.',
        'About Supervision (Duties / Inspection / Reporting) Work',
        'A supervision (duties / inspection / reporting) work tool. A free online tool that runs entirely in the browser; data is never uploaded, keeping your privacy safe.',
    ]))

    write('checker-training-hr-1', build('checker-training-hr-1', [
        '✅ Safety (HSE / Training / Inspection) Implementation',
        'HSE safety implementation checklist (10 items, 2 points for meeting the standard, 1 for basically meeting it, 0 for failing it; full score 20)',
        '📖 View the Safety (HSE / Training / Inspection) Implementation user guide',
        'The HSE safety implementation checklist has 10 items (safety training records, special operation certificates, PPE provision and use, hazard source identification, emergency plan drills, safety inspection records, environmental protection measures, occupational health check-ups, incident reporting system, safety culture building), scored 2 for meeting the standard, 1 for basically meeting it and 0 for failing it, with a full score of 20; 18 or above is excellent, 14 to 17 good, 10 to 13 pass, and below 10 fail with operations suspended for rectification.',
        '1. Safety training records',
        'Basically meets the standard (1 point)',
        'Does not meet the standard (0 points)',
        '2. Special operation certificates',
        '3. PPE provision and use',
        '4. Hazard source identification',
        '5. Emergency plan drills',
        '6. Safety inspection records',
        '7. Environmental protection measures',
        '8. Occupational health check-ups',
        '9. Incident reporting system',
        '10. Safety culture building',
        '📚 In-depth analysis: Safety (HSE / Training / Inspection) Implementation',
        'Annual self-assessment of a company HSE management system: score the 10 items (safety training records, special operation certificates, PPE provision and use, hazard source identification, emergency plan drills, safety inspection records, environmental protection measures, occupational health check-ups, incident reporting system, safety culture building) to locate system gaps and draw up an improvement plan.',
        'Contractor and subcontractor safety qualification review on site entry: compare quickly with the table to find veto items such as special operations without certificates or missing safety training, and block unqualified teams from entering.',
        'Building work-safety standardisation: score against the list to find gaps such as missing occupational health check-ups or incomplete emergency drills, and support the standardisation rating application.',
        'Worked example: 12 points from 10 items triggers rectification',
        'The 10 item scores are [compliant, partially compliant, partially compliant, partially compliant, partially compliant, partially compliant, partially compliant, partially compliant, compliant, partially compliant], i.e. 2/1/1/1/1/1/1/1/2/1, totalling 12 points. Pass rate = 12 ÷ 20 × 100% = 60%. Grading: ≥18 excellent, ≥14 good, ≥10 fair, <10 fail. This example at 12 points is fair, and the tool notes that safety hazards exist, rectification is required within a deadline, and training and inspection frequency should be increased. The weak items are concentrated in items 2 to 8 (special operation certificates, PPE, hazard source identification, emergency drills, inspection records, environmental protection and occupational check-ups are all partially compliant) and should be the focus of the next rectification stage; among them, missing special operation certificates is a major hazard that must be dealt with immediately.',
        'Is there a difference between the HSE and EHS order?',
        'No substantive difference, only a habit of word order: Chinese companies mostly say HSE (Health, Safety, Environment), while some European systems say EHS (Environment, Health, Safety); both cover exactly the same health, safety and environment content. This tool uses HSE following domestic practice, which does not affect the check items or scoring logic.',
        'Does a fail score mean production must stop?',
        'It does not mean an immediate stop. This table is a self-assessment tool and triggers an internal rectification process; an actual order to suspend production is decided by the emergency management authority under the law. However, if the table shows situations such as special operations without certificates or major hazards left untreated, regulations require an immediate work stoppage for rectification, and work must not continue with known defects. Link the scoring results to the hazard register and escalate major items for immediate action.',
        'About Safety (HSE / Training / Inspection) Implementation',
        'A safety (HSE / training / inspection) implementation tool. A free online tool that runs entirely in the browser; data is never uploaded, keeping your privacy safe.',
    ]))

    write('manager-cost', build('manager-cost', [
        '💰 Cost Management (S-curve / Earned Value Management EVM)',
        'Enter the planned value (PV), earned value (EV) and actual cost (AC) for each period; the tool calculates earned value management indicators automatically and generates the S-curve.',
        '"Enter the planned value (PV), earned value (EV) and actual cost (AC) for each period; the tool calculates earned value management indicators automatically and generates the S-curve." — the tool runs a professional calculation from the input parameters and outputs the result.',
        'Cost (S-curve / Earned Value Management) EVM',
        '/ Cost Management (S-curve / EVM)',
        '📖 View the Cost Management (S-curve / Earned Value Management EVM) user guide',
        'Total project budget BAC (CNY)',
        'Total planned duration (days)',
        'Calculate earned value indicators',
        'Add period',
        'Save project',
        'Load project',
        'Period data input',
        'PV = planned value (budget for work scheduled), EV = earned value (budget for work completed), AC = actual cost (cost incurred), unit: CNY',
        'Earned value management indicators',
        'S-curve chart',
        'Planned value PV (cumulative)',
        'Earned value EV (cumulative)',
        'Actual cost AC (cumulative)',
        'Budget BAC',
        'PV (cumulative)',
        'EV (cumulative)',
        'AC (cumulative)',
        '📚 In-depth analysis: Cost Management (S-curve / Earned Value Management EVM)',
        'Routine joint cost and schedule monitoring: for engineering, IT or R&D projects, report the planned value PV, earned value EV and actual cost AC for each period monthly, use CV, SV, CPI and SPI to tell whether the project is over cost or behind schedule, and trigger correction in time for projects whose CPI or SPI falls below 0.9.',
        'Milestone reporting and S-curve review: plot the cumulative PV, EV and AC of each period into an S-curve and show the client or management the three-line deviation of plan versus actual versus earned value, supporting change approval and progress payment decisions.',
        'Completion forecasting (EAC / ETC / VAC): when CPI stays low mid-project, use the typical-variance method EAC = BAC / CPI to forecast total project cost, and estimate whether the budget will be exceeded, how much more is needed and the variance at completion, to support senior decisions.',
        'Worked example: BAC 1.5 million, 100 planned days, 3 cumulative periods',
        'Input: BAC = 1,500,000 CNY, total planned duration 100 days; 3 periods of data PV = 300,000 / 450,000 / 450,000, EV = 280,000 / 420,000 / 400,000, AC = 320,000 / 470,000 / 460,000 (unit: CNY). Cumulative PV = 1,200,000, EV = 1,100,000, AC = 1,250,000. CV = EV − AC = −150,000 CNY (cost overrun); SV = EV − PV = −100,000 CNY (schedule delay); CPI = EV / AC = 0.88 (low cost efficiency); SPI = EV / PV = 0.92 (low schedule efficiency); EAC = BAC / CPI = 1,704,545 CNY (budget 1,500,000, an overrun of 204,545); ETC = EAC − AC = 454,545 CNY; VAC = BAC − EAC = −204,545 CNY; earned value completion rate EV / BAC = 73.3%; the SPI-based forecast gives a total duration of about 109 days against 100 planned. Conclusion: both cost and schedule performance are low, so priority should go to crashing the schedule to recover SPI, and to analysing the root cause of the AC overrun.',
        'Both CPI and SPI are below 1 — can the project still be saved, and how should that be read?',
        'CPI below 1 means the value earned per unit of cost is below what was actually spent (an overrun), and SPI below 1 means actual progress lags the plan. Both below 1 means the project is both over cost and behind schedule. Generally CPI is the less reversible of the two, since money spent is hard to recover while schedule can be partly recovered through crashing or adding resources. As a rule of thumb, CPI or SPI below 0.9 triggers correction: first check whether the AC overrun comes from unit price increases or loss of control over quantities, then check whether the low EV is an efficiency problem or scope change not yet booked.',
        'How do I choose between the EAC methods (typical versus atypical variance)?',
        'The typical-variance method EAC = BAC / CPI assumes current cost performance continues to completion and is used when the trend will not improve by itself; this tool uses that method. The atypical-variance method EAC = AC + (BAC − EV) assumes the remaining work is executed at budget and is used when the root cause has been found and corrected and the project returns to plan afterwards. The choice depends on whether there is reliable evidence that the variance will not continue: use the atypical method only when corrective action has landed and can be verified, otherwise the typical method is the more conservative choice.',
        'CV = EV − AC (cost variance), SV = EV − PV (schedule variance)',
        'CPI = EV / AC (cost performance index), SPI = EV / PV (schedule performance index)',
        'EAC = BAC / CPI (estimate at completion), ETC = EAC − AC (estimate to complete), VAC = BAC − EAC (variance at completion)',
        'Green = performing well, yellow = needs attention, red = needs immediate correction',
        'About Cost Management (S-curve / EVM)',
        'An earned value management tool: by entering the planned value (PV), earned value (EV) and actual cost (AC) for each period, it automatically calculates cost and schedule variances, performance indices and completion forecasts, and generates an S-curve visualisation.',
        'Full calculation of CV / SV / CPI / SPI / EAC / ETC / VAC',
        'S-curve chart visualising PV / EV / AC trends',
        'Red, yellow and green performance status indicators',
        'Project completion cost and duration forecasting',
        'Multi-period comparative data analysis',
        'Project cost performance monitoring',
        'Earned value analysis report generation',
        'Project completion forecasting and early warning',
        'PMO portfolio health assessment',
        'e.g. website redesign project',
    ]))


if __name__ == '__main__':
    main()
