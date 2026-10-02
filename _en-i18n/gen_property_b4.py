#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'property')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'property')
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
    out = {'slug': slug, 'industry': 'property', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('checker-7', build('checker-7', [
        "✅ Quality (Inspection / Standard / Rectification) System",
        "Property service quality inspection system covering quality checks and rectification assessment across the cleaning, security, greening and facilities modules",
        "📖 Read the \"Quality (Inspection / Standard / Rectification) System\" guide",
        "Weighted quality score: each check item scores excellent 4, good 3, fair 2, poor 1; module score rate = Σ(item score × item weight) ÷ Σ(item weight × 4) × 100%; total score weights each module score rate by module weight; items scoring 2 or below go on the rectification list.",
        "Quality inspection checklist",
        "Score each metric (excellent=4/good=3/fair=2/poor=1); the system automatically computes the composite quality score and rectification advice",
        "Evaluate quality system",
        "Four modules weighted: cleaning 25% + security 25% + greening 20% + facilities 30%",
        "A composite score of 85 or above is excellent, 70-84 good, 55-69 pass, below 55 fail",
        "📚 Deep dive: quality (inspection / standard / rectification) system",
        "Property management scores common areas item by item with a checklist",
        "Problem items are prioritised for rectification by weight",
        "Self-check compliance before a street or industry inspection",
        "Scoring sheet",
        "Floor free of stains (3 points), glass free of water marks (2), corridors free of clutter (2), fire escape route clear (3), lawn free of yellowing (2), trees free of dead branches (2) → maximum 14; 3 points deducted in practice (glass + corridors) → 11 points.",
        "Rectification priority",
        "Fire escape route occupied (3 points) takes priority over yellowing lawn (2 points): clear the obstruction first, then re-green; higher-weighted items affect the total score more.",
        "How should checklist weights be set?",
        "Safety items (fire protection, escape routes) carry the highest weight, appearance items next, reflecting risk-first priority.",
        "Does a low score always mean a failure?",
        "Look at the threshold; usually 85% or above passes. Safety items are a single-vote veto, so occupying a fire escape route fails the check outright.",
        "About \"Quality (Inspection / Standard / Rectification) System\"",
        "Property service quality inspection assessment tool that weighted-scores 23 indicators across four modules (cleaning 25%, security 25%, greening 20%, facilities maintenance 30%), outputting a quality grade and rectification list.",
        "Weighted assessment across four service modules",
        "23 quality inspection indicators",
        "Automatic identification and ranking of rectification items",
        "Visualised quality level per module",
        "Monthly/quarterly property service quality inspection",
        "Quality rectification planning",
        "Project quality assessment scoring",
        "Owner satisfaction improvement analysis",
    ]))

    write('checker-11', build('checker-11', [
        "✅ Quality (Standard / Inspection / Improvement) Cycle",
        "PDCA-cycle-based assessment of property service quality management, evaluating maturity across standard setting, inspection execution and problem rectification",
        "📖 Read the \"Quality (Standard / Inspection / Improvement) Cycle\" guide",
        "PDCA assessment: the four stages P standard setting, D inspection execution, C inspection evaluation and A improvement are scored 1 to 5 per question; stage score = mean of that stage's questions; total score = mean of the four stages; grade follows the average: 4.5 and above continuous optimisation, 3.5 to 4.4 effective operation, 2.5 to 3.4 partially implemented, 1.5 to 2.4 initially established, below 1.5 not established.",
        "P - Standard Setting (Plan)",
        "1=not established, 2=initially established, 3=partially implemented, 4=effective operation, 5=continuous optimisation",
        "D - Inspection Execution (Do)",
        "C - Inspection Evaluation (Check)",
        "A - Improvement (Act)",
        "Evaluate quality cycle",
        "PDCA cycle: Plan (standard setting) → Do (inspection execution) → Check (inspection evaluation) → Act (improvement)",
        "Maturity scored 1-5; the composite score reflects the closure level of quality management",
        "Assess once a quarter to keep pushing quality improvement",
        "📚 Deep dive: quality (standard / inspection / improvement) cycle",
        "The property quality department runs daily, weekly and monthly inspections against cleaning, security, greening and maintenance standards",
        "Inspection issues are logged, rectified and re-checked to closure",
        "Monthly quality scores are used to assess the project manager",
        "Weekly inspection closure",
        "40 items checked this week, 34 compliant, 6 problems (cleaning 3, security 2, greening 1) → 6 items rectified within 3 days; 5 passed re-check and 1 was deferred, carried into the next period.",
        "Monthly scoring",
        "Weights per dimension: cleaning 30, security 25, greening 20, maintenance 25, with scores 88, 90, 82, 85 → weighted 86.4; greening below 85 goes on the improvement list.",
        "How often should quality inspection happen?",
        "Daily (on site) plus weekly (themed) plus monthly (comprehensive), with more frequent checks in key areas.",
        "Does finding a problem without rectifying it count as a pass?",
        "No. Closure requires rectification followed by a passing re-check; otherwise the item stays open on the books.",
        "About \"Quality (Standard / Inspection / Improvement) Cycle\"",
        "PDCA-cycle-based property service quality management assessment tool that scores 16 indicators across four stages (standard setting, inspection execution, inspection evaluation and improvement), outputting stage maturity and an improvement path.",
        "16 property management quality indicators",
        "Automatic identification of weak links",
        "Property quality management system maturity assessment",
        "Quality improvement planning",
    ]))

    write('checker-recorder-drill', build('checker-recorder-drill', [
        "🔥 Fire Safety (Drill / Inspection) Records",
        "Fire drill records and fire facility inspection checklists, supporting drill assessment and routine fire inspection logging",
        "\"Fire drill records and fire facility inspection checklists, supporting drill assessment and routine fire inspection logging\" performs a professional calculation from the input parameters and outputs the result.",
        "📖 Read the \"Fire Safety (Drill / Inspection) Records\" guide",
        "Fire drill records",
        "Fire facility inspection",
        "Drill basic information",
        "Drill date",
        "Drill type",
        "Evacuation drill",
        "Firefighting drill",
        "Combined drill",
        "Number of participants",
        "Evacuation time (seconds)",
        "Drill assessment items",
        "Assess drill",
        "Inspection basic information",
        "Inspection date",
        "Inspector",
        "Fire facility inspection checklist",
        "Assess inspection result",
        "Fire drills at least once every six months; fire facilities inspected at least once a month",
        "Drill assessment: 5=excellent, 4=good, 3=fair, 2=poor, 1=fail",
        "Facility inspection: pass / fail / not applicable; failed items need immediate rectification",
        "📚 Deep dive: fire safety (drill / inspection) records",
        "Property management organises a fire drill every six months and files the record",
        "Routine fire inspections log problem items and rectification",
        "Produce drill and inspection ledgers when facing inspections",
        "Drill record",
        "Drill on 2026-05-12 with 60 participants, evacuation time 3.5 min (target ≤5 min), extinguisher hands-on 100% pass → assessment passed and archived.",
        "Inspection problems",
        "Two blocked fire escape routes and one expired extinguisher found → cleared or replaced within 3 days, re-check passed, closure date recorded.",
        "How often are fire drills held?",
        "For high-rise residential and similar buildings at least once every six months, keeping sign-in sheets, photos and the assessment available for the street authority.",
        "How long should inspection records be kept?",
        "At least 2 years is recommended; drill and hazard rectification closure records are key evidence for accountability and due diligence after an incident.",
        "About \"Fire Safety (Drill / Inspection) Records\"",
        "Fire drill records and fire facility inspection tool supporting fire drill assessment (10 indicators) and routine fire facility inspection (10 check items), automatically generating assessment reports and rectification lists.",
        "Fire drill assessment (including evacuation time analysis)",
        "10-item fire facility inspection checklist",
        "Automatic rectification list for failed items",
        "Dual drill / inspection mode switching",
        "Semi-annual property fire drill records",
        "Monthly fire facility patrol",
        "Fire safety inspection and rectification",
        "Fire ledger management",
        "Inspector name",
    ]))


if __name__ == '__main__':
    main()