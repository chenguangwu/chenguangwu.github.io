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
    write('rater-performance', build('rater-performance', [
        "👥 Property Performance Assessment Scoring System",
        "Weighted scoring across six dimensions (customer satisfaction 20% + facility maintenance 20% + response timeliness 15% + collection rate 15% + safety compliance 15% + environmental quality 15%), automatically producing an assessment grade",
        "Performance (assessment / scoring) system",
        "/ Performance (Assessment / Scoring) System",
        "📖 Read the \"Property Performance Assessment Scoring System\" guide",
        "Performance assessment = weighted indicator scoring",
        "Customer satisfaction score (0-100)",
        "Facility maintenance quality (0-100)",
        "Response timeliness score (0-100)",
        "Collection rate score (0-100)",
        "Safety compliance score (0-100)",
        "Environmental quality score (0-100)",
        "📊 Calculate assessment score",
        "💡 Weighted score = Σ(dimension score × weight) / Σweight. Grades: A (≥90) excellent / B (80-89) good / C (70-79) pass / D (60-69) needs improvement / E (<60) fail. Reference dimension scores: survey average satisfaction, facility intact rate, ticket response on-time rate, actual collection rate, safety inspection pass rate, environmental patrol pass rate.",
        "Enter 0-100 for each dimension based on actual assessment data",
        "Weights are customisable and default to industry experience; a total of 100% is recommended",
        "Customer satisfaction is best based on the quarterly survey mean (sample ≥30%)",
        "Response timeliness: responding within 15 minutes scores 100, deducting 5 points for every additional 10 minutes",
        "Safety compliance covers fire protection, lifts, power distribution and gas special equipment inspection pass rates",
        "Results are for reference only; actual assessment should follow the contract terms and local property management rules",
        "📚 Deep dive: property performance assessment scoring system",
        "Property project managers score each role monthly",
        "Multi-dimensional weighting computes composite performance for bonuses",
        "Low-scoring staff get an improvement plan and re-assessment",
        "Weighted scoring",
        "Repair response (weight 20, score 90) + environmental hygiene (25, 85) + safety order (20, 88) + owner satisfaction (25, 82) + cost control (10, 78) → composite = 20%×90 + 25%×85 + 20%×88 + 25%×82 + 10%×78 = 85.15.",
        "Grade application",
        "≥90 excellent, 80-89 good, 70-79 pass, <70 needs improvement; 85.15 is good with a bonus coefficient of 1.0; two consecutive months below 70 triggers training.",
        "How should weights be set?",
        "By the core duties of each role: customer service emphasises satisfaction, engineering emphasises response, security emphasises order, with differentiated weights.",
        "Where does the satisfaction data come from?",
        "From follow-up ratings and complaint rates, to avoid looking only at internal man-hours and ending up busy but non-compliant.",
        "About \"Property Performance Assessment Scoring System\"",
        "Property Performance Assessment Scoring System supports weighted scoring across six dimensions: customer satisfaction, facility maintenance quality, response timeliness, collection rate, safety compliance and environmental quality. Weights are customisable, A-E grade results are generated automatically, and weak links are identified with improvement advice.",
        "Six assessment dimensions covering the full scope of property service quality",
        "Customisable weights to fit different project assessment needs",
        "Bar chart visualisation of each dimension's score",
        "Automatic identification of the lowest dimension with improvement advice",
        "Quarterly / annual performance assessment for property companies",
        "Service quality evaluation by homeowners committees",
        "Horizontal comparison across multiple projects",
        "Property service contract performance evaluation",
        "Customer satisfaction",
        "Customer satisfaction weight",
        "Facility maintenance",
        "Facility maintenance weight",
        "Response timeliness",
        "Response timeliness weight",
        "Collection rate",
        "Collection rate weight",
        "Safety compliance",
        "Safety compliance weight",
        "Environmental quality",
        "Environmental quality weight",
    ]))

    write('assessor-manager-1', build('assessor-manager-1', [
        "⚖️ Outsourcing (Assessment / Contract / Supervision) Management",
        "Property service outsourcing supplier assessment management, covering qualification assessment, contract compliance and process supervision",
        "Core calculation formula (from input variables): total÷max×100",
        "📖 Read the \"Outsourcing (Assessment / Contract / Supervision) Management\" guide",
        "Supplier information",
        "Supplier name",
        "Outsourcing type",
        "Cleaning service",
        "Greening maintenance",
        "Facility maintenance",
        "Parking management",
        "Contract amount (10k CNY/year)",
        "Contract term (months)",
        "I. Qualification assessment (weight 30%)",
        "II. Contract compliance (weight 30%)",
        "III. Process supervision (weight 40%)",
        "Evaluate outsourcing management",
        "Three-dimension weighted scoring: qualification assessment 30% + contract compliance 30% + process supervision 40%",
        "Scoring standard: 5=excellent, 4=good, 3=fair, 2=poor, 1=fail",
        "Assessment results serve as reference for renewal, replacement or assessment decisions",
        "📚 Deep dive: outsourcing (assessment / contract / supervision) management",
        "Assess supplier qualifications when tendering cleaning or maintenance outsourcing",
        "Supervise the contractor's service against KPIs during contract execution",
        "Decide on renewal or exit based on performance scores before the term ends",
        "Qualification assessment",
        "Supplier A: complete contract terms (5) + full insurance (5) + no incidents in the last 3 years (5) = 15 points; Supplier B lacks insurance (-3) → A is shortlisted.",
        "Performance supervision",
        "Monthly KPI: cleaning compliance 92% (target 95%), 4 complaints → deduction, issue a rectification letter; two consecutive months of non-compliance triggers the contractual penalty.",
        "What does outsourcing assessment look at?",
        "Qualifications (licences, insurance, track record), price reasonableness, emergency plans and historical reputation, all of which matter.",
        "Is the property company exempt when outsourcing causes problems?",
        "No. The property company bears overall responsibility to owners for outsourced services, and the contract must specify recourse and penalties.",
        "About \"Outsourcing (Assessment / Contract / Supervision) Management\"",
        "Property service outsourcing supplier assessment management tool that weighted-scores suppliers across three dimensions (qualification assessment 30%, contract compliance 30%, process supervision 40%), outputting a composite rating, weak links and supplier management recommendations.",
        "Three-dimension weighted scoring system",
        "16 professional assessment indicators",
        "Automatic identification of failed items with rectification advice",
        "Reference for supplier renewal/replacement decisions",
        "Annual assessment of outsourcing suppliers",
        "Qualification review before contract renewal",
        "Supplier selection and tender evaluation",
        "Continuous supervision of outsourcing service quality",
        "e.g. XX Property Services Co., Ltd.",
    ]))

    write('cycle-elevator', build('cycle-elevator', [
        "⏱️ Lift (Maintenance / Annual Inspection) Cycle",
        "Lift maintenance and annual inspection cycle management, auto-deriving the next due date from fortnightly/quarterly/half-yearly/annual maintenance and the statutory annual inspection, with overdue compliance warnings.",
        "📖 Read the \"Lift (Maintenance / Annual Inspection) Cycle\" guide",
        "➕ Add lift",
        "Building / location",
        "Lift number",
        "Installation date",
        "Add lift",
        "📊 Maintenance record summary",
        "💡 After adding a lift, enter the most recent maintenance record of each type and the system derives the next due date. Without records it counts from the installation date.",
        "Maintenance cycles follow general norms; local regulations and the lift user manual take precedence",
        "The annual inspection is a statutory test; operating while overdue is a violation, so submit for inspection on time",
        "📚 Deep dive: lift (maintenance / annual inspection) cycle",
        "The property engineering department logs each lift's maintenance date and annual inspection due date monthly, flagging upcoming and overdue items",
        "When handing over to a new maintenance contractor, verify the maintenance history and the next due date",
        "Maintenance planning",
        "Continuity",
        "Export the lift maintenance ledger during homeowners committee patrols to confirm no overdue unit is still running",
        "Single-lift upcoming reminder",
        "Lift 3 in an 18-storey residential building was last serviced on 2026-03-10 with a 15-day cycle → next due 2026-03-25; if today is 2026-03-28 it shows \"3 days overdue\" and the fortnightly service must be arranged immediately.",
        "Annual inspection",
        "Countdown",
        "Lift installed 2019-06-01 with a 1-year statutory special equipment inspection cycle → next annual inspection 2026-06-01; when less than 30 days remain it prompts preparation of the self-inspection report and submission materials.",
        "What is the difference between maintenance and annual inspection cycles?",
        "Maintenance is routine fortnightly or monthly servicing (every 15 or 30 days), while the annual inspection is the statutory periodic test for special equipment (usually once a year). Both need reminders before due and neither substitutes for the other.",
        "What are the consequences of an overdue inspection?",
        "Operating a lift past its inspection due date is a regulatory violation; authorities may order it out of service and impose fines. The overdue flag in the ledger pressures timely scheduling to avoid running a defective unit.",
        "About \"Lift (Maintenance / Annual Inspection) Cycle\"",
        "Property management lift maintenance and annual inspection cycle tracking tool with five built-in cycle types (fortnightly, quarterly, half-yearly, annual maintenance and the statutory annual inspection), automatically computing the next due date from the latest maintenance record, warning by urgency level and outputting compliance status.",
        "Auto-derivation of five maintenance cycle types",
        "Overdue and upcoming expiry warnings",
        "Maintenance personnel and parts records",
        "Compliance status at a glance",
        "Exportable records for backup",
        "e.g. Building 1 Unit 1",
        "e.g. DT-01",
        "e.g. Mitsubishi NEXIEZ",
    ]))


if __name__ == '__main__':
    main()