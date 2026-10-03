#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'admin')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'admin')
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
    out = {'slug': slug, 'industry': 'admin', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('analysis-30', build('analysis-30', [
        "\U0001F4B0 Administrative (Expense / Budget / Savings) Analysis",
        "Expense / Budget / Savings",
        "View the User Guide for Administrative (Expense / Budget / Savings) Analysis",
        "Variance = actual - budget; budget execution rate = total actual / total budget x 100%.",
        "Overspend items are those with actual greater than budget; savings items are those with actual less than budget. The overspend amount and savings amount are totalled separately.",
        "The anomaly alert prioritises the number of overspend items and the largest overspend item, helping administrative expense reconciliation and cost-reduction analysis.",
        "Expense data (each row: 'expense item, budget, actual')",
        "Office supplies,15000,15000\nTravel expenses,30000,27000\nUtilities,20000,21000",
        "Budget Analysis",
        "In-depth: Administrative Expense Budget Execution and Savings Analysis",
        "Administrative budget control",
        "Cost-reduction analysis and department expense reconciliation",
        "Overspend anomaly alert",
        "Variance = actual - budget; execution rate = actual / budget x 100%; overspend = sum of positive (actual-budget) items, savings = sum of positive (budget-actual) items.",
        "Office supplies 20000/23500, travel 50000/42000, utilities 30000/34500, communication 12000/10800, maintenance 15000/15000 -> total budget 127000, actual 125800, total variance -1200, execution rate 99.06%; 2 overspend items, largest overspend is utilities +4500 (115.00%).",
        "Is it fine to take no action just because the total is within budget?",
        "You still need to look at the structure. Total savings may hide a single-item overspend (e.g. a utilities overspend offset by travel savings), so each item should be reviewed individually.",
        "Can the savings amount be taken directly as a cost-reduction result?",
        "Distinguish active cost reduction from passive reduction caused by lower business volume, and judge accurately using volume metrics (e.g. per-capita expense).",
        "About Administrative (Expense / Budget / Savings) Analysis",
        "Administrative (expense / budget / savings) analysis. A free online tool that runs entirely in the browser, with no data uploaded, protecting your privacy and security.",
        "Office supplies,20000,23500",
    ]))
    write('checker-manager-training-hr', build('checker-manager-training-hr', [
        "\u2705 Confidentiality Management Compliance Self-Check",
        'Self-check implementation item by item across three modules - agreement management / training management / inspection management - automatically calculate each module\'s achievement rate and overall compliance, and output remediation suggestions.',
        "Confidentiality (Agreement / Training / Inspection) Management",
        "/ Confidentiality (Agreement / Training / Inspection) Management",
        "View the User Guide for Confidentiality Management Compliance Self-Check",
        "Overall compliance = sum of actual scores / sum of full marks x 100% (2 points per item); compliance not below 90% is excellent, 75%-89% is good, 60%-74% is basically compliant, below 60% is non-compliant; module score rate = module actual score / module full mark, the lowest-scoring module is listed as the priority for remediation; items not implemented (0) and partially implemented (1) must each form a remediation list with responsible person and deadline.",
        "Overall compliance = sum of actual scores / (item count x 2) x 100%",
        "This tool is for reference in confidentiality self-check and inspection preparation; it does not replace the determination of the competent confidentiality authority.",
        "In-depth: Confidentiality Management Compliance Self-Check",
        "During the annual confidentiality self-check, self-assess each clause such as 'classified media registration, classified personnel review, confidentiality education and training, unauthorized outbound control' (not implemented 0 / partially implemented 1 / implemented 2), then total the scores to determine the compliance level.",
        "Before a new project is initiated, perform a pre-assessment of confidentiality management, identify weak links (items scored 0) and promptly add controls to avoid leakage risk after launch.",
        "Before outsourced or on-site personnel enter, perform a confidentiality check to confirm whether their clauses reach 'implemented'; those who fail must not access sensitive materials.",
        "Self-assessment scores for 8 confidentiality clauses",
        "Self-score 8 clauses: 2,1,2,2,0,1,2,1 (full mark 16). Total 11, score rate 68.75%. Clause 5 'unauthorized outbound control' scored 0, a key gap that should be remediated first; overall falls in the 'basically compliant, needs improvement' range.",
        "How are the scoring criteria determined?",
        "Each item has three levels: not implemented = 0, partially implemented = 1, implemented = 2. The total is the sum of items, score rate = total / (2 x item count). Specific compliance requirements follow your unit's confidentiality policy and the Law on Guarding State Secrets; this tool only summarises the self-assessment.",
        "How to remediate when scores are low?",
        "First list the key clauses scored 0, and add policy, training and technical controls item by item; if the score rate is below 60%, suspend sensitive business and start a dedicated remediation, then re-assess until compliant.",
        "About Confidentiality Management Compliance Self-Check",
        "A confidentiality self-check tool for classified units, covering 12 points across three modules - confidentiality agreement, confidentiality training and confidentiality inspection - quantitatively assessing compliance and locating weak links, supporting confidentiality qualification and daily management.",
        "Three-module checklist: agreement / training / inspection",
        "Inspection preparation for confidentiality qualification",
        "Annual confidentiality management self-check",
        "Confidentiality education and training assessment",
        "Remediation task list generation",
        "How to Use the Confidentiality Management Compliance Self-Check",
    ]))
    write('detector-time', build('detector-time', [
        "\U0001F50D Meeting Time Conflict Detection",
        "Add multiple meeting schedules and automatically detect conflicts where time ranges overlap on the same date / weekday, marking conflicting pairs to assist scheduling and calendar coordination.",
        "Meeting Time Conflict Detection (Multiple Schedules)",
        "/ Meeting Time Conflict Detection (Multiple Schedules)",
        "View the User Guide for Meeting Time Conflict Detection",
        "➕ Add Schedule",
        'Supports scheduling by "date" or "weekday"; on the same date / weekday, if two meetings\' time ranges intersect, it is judged a conflict',
        "Time format is HH:MM; the end time must be later than the start time.",
        "Only detects time-dimension conflicts, ignoring location / people; runs entirely in the browser with no data uploaded.",
        "In-depth: Meeting Time Conflict Detection",
        "Enter a week's meetings (name, date, start/end time); the tool automatically finds same-day overlapping meetings, avoiding double-booking the same room or person.",
        "When coordinating cross-department weekly meetings, list each side's candidate slots first, then use the tool to pick non-conflicting combinations, reducing back-and-forth confirmation cost.",
        "When scheduling training or review meetings, check whether they overlap with an existing all-hands, preventing attendees from being stretched thin.",
        "Time-overlap detection for three meetings",
        "Enter: A Mon 09:00-10:30 (weekly meeting), B Mon 10:00-11:00 (requirements review), C Tue 14:00-15:00 (client meeting). The tool finds A and B overlap at 10:00-10:30 (conflict); C conflicts with none, and suggests moving B to after 10:30 to separate them.",
        "How is a conflict determined?",
        "On the same date, if two meetings' [start, end) intervals intersect, it is a conflict (touching endpoints such as ending at 10:30 and starting at 10:30 are not a conflict). Meetings on different dates do not affect each other. The rule follows the actual scheduling policy; the tool only does interval math.",
        "Does it support multi-day or recurring meetings?",
        "Currently it compares each record's date and start/end time pairwise, suitable for one-off or specified-date meetings. Recurring schedules (e.g. every Wednesday) can be entered week by week and checked separately; the tool does not auto-expand a weekly calendar.",
        "About Meeting Time Conflict Detection",
        "Enter multiple meeting schedules (by date or weekday); the tool automatically compares whether each meeting's time range overlaps on the same time dimension, quickly finding scheduling conflicts, suitable for administration, project management and team coordination.",
        "Add or remove schedules dynamically with real-time detection",
        "Supports scheduling by date or by weekday",
        "Precise location of conflicting pairs",
        "Administrative scheduling and meeting-room allocation",
        "Project management weekly plan check",
        "Personal schedule conflict self-check",
        "Team coordination and meeting consolidation",
        "How to Use Meeting Time Conflict Detection",
        "Meeting name",
        "Date or weekday",
        "End",
    ]))
    write('index', build('index', [
        "\U0001F5C2\uFE0F Administrative Management Tools",
        "Administrative Management",
        "Administrative Management Tools",
        "Travel Subsidy Calculator",
        "Calculates domestic travel subsidy by destination city category and number of days, including meal allowance, transport allowance and accommodation cap, auto-summing the total for reimbursement accounting.",
        "Office Supplies Forecast",
        "An office-supplies consumption forecaster: enter historical monthly usage and predict next month's demand with the moving-average method, aiding procurement planning and inventory stocking.",
        "Meeting Time Conflict Detection (Multiple Schedules)",
        "Add multiple meeting schedules and automatically detect conflicts where time ranges overlap on the same date / weekday, marking conflicting pairs to assist scheduling and calendar coordination.",
        "Confidentiality (Agreement / Training / Inspection) Management",
        "Around confidentiality-agreement signing, training records and periodic inspection, it provides a compliance self-check list and scoring, suitable for corporate confidentiality management, classified-post review and internal-audit remediation.",
        "Aggregates administrative office expense and budget-execution data, outputting cost structure, savings headroom and anomaly alerts, suitable for administrative budget control, cost-reduction analysis and department expense reconciliation.",
        "Registers asset information and automatically calculates depreciation (straight-line / double-declining-balance / sum-of-years'-digits), generating a depreciation schedule and book value.",
        "Records file version numbers, revision notes and author, supports semantic versioning (SemVer), and stores data locally in the browser.",
        "A meeting conflict detector: add multiple schedule time ranges, automatically detect overlaps and visualise a timeline, helping administrators coordinate scheduling and avoid clashes.",
        "About Administrative Management Tools",
        "The Administrative Management Tools collection contains 8 free online tools, covering common calculation, conversion and lookup needs in administrative scenarios. Whether you are a practitioner, student or ordinary user in the field, you can find ready-to-use small tools here. All tools run entirely in the browser, upload no data to the server, and protect your privacy and security.",
        "The administrative management tools on this page include (representative selection):",
        "These tools help you quickly complete common administrative tasks without memorising complex formulas or doing manual conversions; just enter to get results.",
        "Do the administrative management tools need to be downloaded or registered?",
        "No. All administrative management tools on this page are pure front-end online tools; open the web page to use them directly, with no software installation, no account registration, and no data upload.",
        "Are the calculation results of the administrative management tools accurate? Is the data safe?",
        "The tools calculate locally in your browser based on public mathematical formulas and general industry standards, with results available instantly. All computation is done locally on your device, data is never uploaded to the server, and your privacy and security are protected.",
    ]))

if __name__ == '__main__':
    main()
