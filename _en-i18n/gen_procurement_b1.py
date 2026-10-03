#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'procurement')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'procurement')
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
    out = {'slug': slug, 'industry': 'procurement', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('analysis-cost', build('analysis-cost', [
        "💰 Procurement (Cost/Savings) Analysis",
        "Cost/Savings",
        "📖 View \"Procurement (Cost/Savings) Analysis Guide\"",
        "Single saving = (original unit price − new unit price) × purchase quantity; savings rate = (original unit price − new unit price) ÷ original unit price; annual saving = single saving × annual purchase frequency; net annual saving = annual saving − one-time investment; payback (orders) = one-time investment ÷ single saving.",
        "Purchase Quantity (units)",
        "Original Unit Price (CNY/unit)",
        "Negotiated Unit Price (CNY/unit)",
        "Annual Purchase Frequency",
        "One-time Investment (CNY)",
        "📚 In-Depth Analysis: Procurement Cost and Savings Analysis",
        "Compare prices before and after negotiation to calculate single-order savings and savings rate, quantifying bargaining outcomes.",
        "Combining annual purchase frequency with one-time investment (system/process transformation), estimate annual savings, net annual savings, and",
        "horizontally compare unit savings across multiple suppliers or purchases to locate the categories with the greatest cost-reduction potential.",
        "Example: annual framework price reduction",
        "Purchase quantity 1,000 units, original unit price 100 CNY, negotiated unit price 85 CNY, annual purchases 6, one-time investment 10,000 CNY: original amount 100,000 CNY, new amount 85,000 CNY, single saving 15,000 CNY, savings rate 15%, annual saving 90,000 CNY, net annual saving 80,000 CNY, payback about 0.67 orders (amortized by single saving).",
        "How is the savings rate calculated?",
        "Savings rate = (original unit price − new unit price) ÷ original unit price × 100%, reflecting the relative price drop; if only the total amount is given, convert it to a unit price first before substituting.",
        "What does the payback period refer to?",
        "The transformation/system cost invested to achieve price reduction, amortized by single saving into the required purchase orders (or converted to years); a shorter payback means faster return on cost-reduction investment; if the unit price does not drop, the saving is 0 and the payback is meaningless.",
        "About \"Procurement (Cost/Savings) Analysis\"",
        "Procurement (Cost/Savings) Analysis. Free online tool, pure front-end processing, no data uploaded, protecting privacy and security.",
    ]))
    write('assessor-26', build('assessor-26', [
        "📋 Supplier Admission Evaluation and Grading",
        "Enter the supplier's five-dimension information (qualification/finance/capacity/quality/delivery), and the system automatically calculates the admission score and grades them as strategic/preferred/qualified/eliminated suppliers.",
        "Supplier (Admission/Evaluation/Grading) System",
        "/ Supplier (Admission/Evaluation/Grading) System",
        "📖 View \"Supplier Admission Evaluation and Grading Guide\"",
        "Supplier admission score = weighted indicators",
        "I. Enterprise Qualification (weight 20%)",
        "Registered Capital (10k CNY)",
        "Business License Years (years)",
        "Industry Qualification Level",
        "Grade A / Class I",
        "Grade B / Class II",
        "Grade C / Class III",
        "Provisional Grade",
        "No Qualification",
        "ISO System Certification",
        "II. Financial Status (weight 20%)",
        "Annual Revenue (10k CNY)",
        "Debt-to-Asset Ratio (%)",
        "Credit Rating",
        "BB and below",
        "III. Production Capacity (weight 20%)",
        "Monthly Capacity Fulfillment Rate (%)",
        "Production Equipment Advancement",
        "Internationally Leading Automation",
        "Domestic Leading",
        "Industry Average",
        "Partially Outdated",
        "Equipment Backward",
        "IV. Quality System (weight 20%)",
        "Outgoing Pass Rate (%)",
        "Customer Complaint Rate (%)",
        "V. Delivery Record (weight 20%)",
        "On-time Delivery Rate (%)",
        "Cooperation Years (years)",
        "Admission Evaluation",
        "Five dimensions with equal weight (each 20%), each item full score 100",
        "Grading standard: ≥85 strategic supplier, 70-84 preferred, 60-69 qualified, <60 eliminated",
        "Debt-to-asset ratio >70% or no ISO certification automatically downgrades one level",
        "The evaluation result serves as an admission reference and should be combined with on-site inspection",
        "📚 In-Depth Analysis: Supplier Admission Evaluation and Grading",
        "Before introducing a new supplier, enter the five dimensions of qualification, finance, capacity, quality, and delivery, and automatically calculate the total admission score and determine strategic/preferred/qualified/eliminated.",
        "During the annual supplier re-evaluation, update the indicators, re-grade, and use as the basis for share allocation and replacement decisions.",
        "Perform sensitivity analysis on suppliers at critical scores: adjust the debt ratio or ISO certification status to observe whether deduction items are triggered, causing downgrade.",
        "Example: \"a quality manufacturer\"",
        "Input: registered capital 20,000,000 CNY, operating 12 years, qualification grade 4, ISO grade 4, revenue 80,000,000 CNY,",
        "Debt-to-Asset Ratio",
        "40%, credit grade 4, capacity fulfillment 160%, equipment grade 4, pass rate 99%, complaint rate 1%, on-time rate 97%, cooperation 6 years. Five-dimension scores: enterprise qualification 92, finance 87, capacity 88, quality 89.4, delivery 98.2; total = round((92+87+88+89.4+98.2)/5) = 91 → strategic supplier (≥85). No deductions (debt ratio ≤70, ISO ≠1). If changed to debt ratio 75% and no ISO certification, both items deduct 10 points, total drops to 71 → preferred supplier.",
        "How are the grading thresholds set?",
        "Total score ≥85 for strategic supplier (priority long-term agreement), ≥70 preferred, ≥60 qualified (limit share and track improvement), <60 unqualified (eliminated, not included in the list). Additional penalty items: debt-to-asset ratio >70% deducts 10 points, no ISO certification (iso=1) deducts 10 points; after deduction it may cross levels.",
        "How is each dimension scored?",
        "Qualification = registered capital/output coefficient + operating years + qualification grade + ISO grade; finance = revenue scale + debt-ratio grading (≤30→30 points, decreasing stepwise to >85→0) + credit rating; capacity = capacity fulfillment segmentation (≥150%→40 cap) + equipment grade; quality = pass-rate mapping + complaint deduction; delivery = on-time rate + cooperation years. Each item capped at 100, then take the five-dimension mean and round.",
        "About \"Supplier Admission Evaluation and Grading\"",
        "Supplier admission evaluation and grading management tool that quantitatively scores suppliers across five dimensions — enterprise qualification, financial status, production capacity, quality system, and delivery record — automatically grading them into four categories: strategic/preferred/qualified/eliminated, with support for automatic penalty deductions.",
        "Five-dimension equal-weight quantitative scoring",
        "Four-level automatic supplier grading",
        "High-debt/no-ISO automatic deduction mechanism",
        "Detailed per-dimension breakdown and status display",
        "Automatic admission suggestions",
        "New supplier admission evaluation",
        "Annual supplier grading management",
        "Procurement sourcing comparison",
        "Supplier performance improvement tracking",
    ]))
    write('index', build('index', [
        "🛒 Procurement and Supply Tools",
        "Procurement and Supply",
        "Procurement and Supply Tools",
        "The bidding method comparison tool compares the applicable scenarios and process essentials of procurement methods such as open bidding, invited bidding, and competitive negotiation, assisting compliant procurement decisions.",
        "Supplier (Admission/Evaluation/Grading) System",
        "Enter the supplier's five-dimension information (qualification/finance/capacity/quality/delivery); the system automatically calculates the admission score and grades them as strategic/preferred/qualified/eliminated suppliers.",
        "Supplier Composite Score (Quality/Price/Delivery)",
        "Enter quality/price/delivery data for multiple suppliers, customize weights, and the system automatically calculates composite scores and ranks them, assisting procurement decisions.",
        "The arrival on-time rate and pass-rate statistics tool aggregates on-time delivery and quality pass ratios of purchase orders, outputs metrics, and suits supplier performance evaluation and procurement optimization.",
        "Calculate on-time rate and defect rate by delivery date and arrival quality, aggregate by supplier or period, for supply chain performance evaluation; pure front-end statistics.",
        "The logistics transport mode and freight comparison tool compares freight and timeliness of express, LTL, FTL and other schemes by input parameters, assisting procurement and distribution logistics selection.",
        "Enter purchase price and benchmark price to calculate savings and savings rate, aggregate by category, for cost-reduction assessment and supplier price comparison; pure front-end statistics, no data leaving local.",
        "Economic Order Quantity",
        "Enter annual demand, cost per order, and unit annual holding cost; the tool solves, via the EOQ formula, the economic order quantity and order cycle that minimize total procurement and inventory cost, helping buyers balance replenishment frequency and storage expense.",
        "Supplier Scoring",
        "Weighted scoring across four dimensions — quality, price, delivery, service — with automatic ranking to select the best overall supplier, for procurement sourcing, performance appraisal, and supplier management.",
        "About \"Procurement and Supply Tools\"",
        "The Procurement and Supply Tools collection includes 9 free online tools covering common calculation, conversion, and lookup needs in procurement and supply scenarios. Whether you are a practitioner, student, or ordinary user in the field, you can find ready-to-use small tools here. All tools run purely front-end, data is not uploaded to servers, protecting privacy and security.",
        "The procurement and supply tools on this page include (representative tools):",
        "These tools help you quickly complete common procurement and supply tasks without memorizing complex formulas or manual conversion; just input to get results.",
        "Do the procurement and supply tools need to be downloaded or registered?",
        "No. All procurement and supply tools on this page are pure front-end online tools; open the page to use them directly, no software installation, no account registration, and no data upload.",
        "Are the calculation results of the procurement and supply tools accurate? Is the data safe?",
        "The tools compute locally in your browser based on public math formulas and general industry standards, with instant results. All calculations are completed locally on your device; data is not uploaded to servers, ensuring privacy and security.",
    ]))
if __name__ == '__main__':
    main()
