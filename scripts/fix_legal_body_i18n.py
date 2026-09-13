#!/usr/bin/env python3
"""legal (54) 英文态八维根治 — A 批次：
1. 为 54 个真实工具写真实英文名 + 英文 intro（覆盖 body.title/h1/intro + en 嵌套、legal.json en-US、_en_override en/ed）
2. 清 7 个 legal-body.json 孤儿键（全站无页面）：generator-18 / estimate-accident / lookup-classify-1 / lookup-19 / lookup-social / lookup-register / simulator-37
保持原缩进：legal.json / legal-body.json indent=2；_en_override.json indent=1。
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I18N = os.path.join(ROOT, 'i18n', 'tools')
SUF = " Free online tool on ToolBox — 100% client-side, no data uploaded, no install. Part of the Law & Compliance tools."

# slug -> (英文名, 英文intro/描述)
EN_MAP = {
 "arbitration-fee": ("Arbitration Fee Calculator",
   "Estimate arbitration filing and handling fees for commercial disputes using the progressive amount tiers under the arbitration commission fee rules."),
 "calc-16": ("Limitation Period Expiration Calculator",
   "Compute when the general three-year civil limitation period expires under Civil Code Article 188 from the date the right was known to be harmed."),
 "calc-17": ("IP Protection Term Calculator",
   "Compute the protection term and remaining years for invention patents (20y), utility models (10y), designs (15y) and trademarks (10y, renewable) from filing or registration date."),
 "calc-8": ("Year-End Bonus Income Tax Calculator",
   "Compare the separate-taxation method (monthly-converted rate) versus folding the bonus into annual comprehensive income to find the lower individual income tax."),
 "calc-96": ("Contract Breach / Penalty Calculator",
   "Estimate contract breach liability and liquidated damages using the agreed daily rate, capped at 30% of actual loss under the Civil Code."),
 "calc-interest": ("Private Lending Interest Calculator",
   "Calculate accrued interest on a private loan using the agreed rate capped at 4x LPR, with separate handling for pre- and post-2020 judicial rules."),
 "calculator-calc-6": ("Liquidated Damages Calculator",
   "Compute liquidated damages from principal, contractual daily interest rate and overdue days, with the statutory 30% loss cap."),
 "calendar-qr": ("Calendar QR Code",
   "Turn any selected date or date range into a scannable QR code to share the calendar entry without uploading data."),
 "calendar": ("Perpetual Calendar",
   "Browse any year's Gregorian calendar with weekday, lunar date, solar terms and public holidays for quick date reference."),
 "child-support": ("Child Support Calculator",
   "Estimate monthly child support using the income-ratio, fixed-amount or percentage method under local enforcement guidance."),
 "consumer-protection": ("Consumer Refund & Treble Damages Calculator",
   "Compute the refund plus triple compensation a merchant must pay for deceptive goods under Consumer Rights Protection Law Article 55 (minimum 500 yuan)."),
 "contract-templates": ("Contract Template Library",
   "Browse and copy editable contract and agreement templates across common categories; reference only, not legal advice."),
 "court-fee": ("Litigation Fee Calculator",
   "Estimate the court acceptance fee for civil cases using the progressive property/non-property fee schedule under the litigation fee rules."),
 "debt-statute-limitations": ("Debt Limitation Period Calculator",
   "Compute when the limitation period on a debt claim expires, counted from the last repayment or acknowledgment that interrupts the period."),
 "divorce-property": ("Divorce Property Division Calculator",
   "Split total marital property by an agreed percentage, separating premarital down payments from post-marital joint repayments."),
 "double-wage-no-contract": ("Double Wage (No Contract) Calculator",
   "Estimate the extra month's wage for each uncovered month (up to 11 months) when no written labor contract was signed under Labor Contract Law Article 82."),
 "estimate-12": ("Severance (N+1) Estimator",
   "Estimate statutory economic compensation as N (or N+1 with notice) months of average wage by years of service under the Labor Contract Law."),
 "estimate-40": ("Labor Claim Estimator",
   "Get a rough estimate of a labor dispute, work-injury or compensation claim from a few key inputs to gauge case value before filing."),
 "estimate-salary": ("Labor Dispute Compensation Estimator",
   "Estimate compensation across common labor dispute scenarios (overtime, severance, injury) from your inputs."),
 "falv-yijian-han-beiwanglu-bianxie": ("Legal Opinion / Letter / Memo Writer",
   "Draft structured legal opinions, demand letters or memoranda from guided prompts; template output, not legal advice."),
 "falvwenshuguanjiancizidongtiqu": ("Legal Document Keyword Extractor",
   "Paste any legal document to auto-extract key terms and clause keywords for faster review, all client-side."),
 "feisu-ipo-simu-binggou-yewu": ("Non-Litigation Practice Helper (IPO / PE / M&A)",
   "Track milestones and checklists for non-litigation corporate work such as IPO, private placement and M&A; planning aid only."),
 "food-safety": ("Food Safety Refund & Tenfold Damages Calculator",
   "Compute the refund plus tenfold price compensation (minimum 1000 yuan) for non-compliant food under Food Safety Law Article 148."),
 "generator-17": ("Legal Document Template Generator",
   "Generate editable contract or agreement templates by selecting a type and filling guided fields; reference only."),
 "housing-fund-loan": ("Housing Provident Fund Loan Calculator",
   "Estimate your housing provident fund loan ceiling from account balance, monthly contribution and the local loan-to-deposit ratio."),
 "inheritance-share": ("Statutory Inheritance Share Calculator",
   "Allocate the estate among statutory heirs (spouse, children, parents) by equal-share rules, accounting for the surviving spouse's separate half."),
 "ipr-damages": ("IP Infringement Damages Calculator",
   "Estimate intellectual property infringement damages using actual loss, infringer's profit or the statutory cap under the IP law methods."),
 "jicheng-yizhu-gongzheng-yichan-fenpei": ("Will / Notarization / Estate Distribution Planner",
   "Compare estate distribution under a valid will, statutory succession order or notarized will to understand each heir's share."),
 "labor-compensation-n1": ("N+1 Severance Calculator",
   "Compute the N+1 severance package (N months plus one month notice) by years of service and average wage under Labor Contract Law Articles 47/40."),
 "labor-compensation": ("Economic Compensation Calculator",
   "Compute statutory economic compensation by years of service and average monthly wage for lawful termination scenarios."),
 "late-payment-interest": ("Late Payment Interest Calculator",
   "Estimate overdue payment interest using an LPR multiple (capped at 4x) or the double penalty-interest rule for delayed commercial payments."),
 "lawyer-fee-reference": ("Lawyer Fee Reference",
   "Reference typical lawyer fee ranges by case type and claimed amount using local bar guidance; estimate only."),
 "legal-age": ("Legal Age Calculator",
   "Compute a person's age at key legal milestones (majority, marriage, criminal responsibility) from birth date."),
 "legal-aid-eligibility": ("Legal Aid Eligibility Checker",
   "Check whether you may qualify for legal aid based on income threshold and case type under local legal aid rules."),
 "legal-calculator": ("Legal Calculator (General)",
   "A general-purpose calculator for everyday legal and financial computations without uploading data."),
 "legal-reference": ("Legal Query Tool",
   "Quickly look up common legal thresholds, statutory rates and reference values in one place."),
 "loan-statute-limitations": ("Loan Limitation Period Calculator",
   "Compute when the limitation period on a loan expires from the last repayment or a demand that interrupts the period."),
 "marriage-property-agreement": ("Marriage Property Agreement Calculator",
   "Allocate property between spouses under a prenuptial or postnuptial agreement, separating separate and joint assets."),
 "notarization-fee": ("Notarization Fee Reference",
   "Reference notary public fee ranges by document type and notarized value using the local notarization tariff."),
 "overtime-pay": ("Overtime Pay Calculator",
   "Compute overtime pay at 150% (weekday), 200% (rest day) and 300% (statutory holiday) rates under Labor Law Article 44."),
 "patent-fee-calculator": ("Patent Fee Calculator",
   "Estimate patent office fees including filing, examination and annual fees by patent type and applicant status (individual or entity)."),
 "patent-term-calculator": ("Patent Term Calculator",
   "Compute a patent's remaining protection term and expiration date from its filing or grant date by patent type."),
 "personal-injury": ("Personal Injury Compensation Calculator",
   "Estimate personal injury compensation from medical expenses, lost income and disability grade under tort liability rules."),
 "rent-deposit": ("Rent Deposit Dispute Helper",
   "Estimate how much of a rental deposit should be returned and the lawful deduction limits in a tenancy dispute."),
 "severance-pay": ("Unlawful Termination Damages Calculator",
   "Compute the 2N statutory damages for unlawful termination (double economic compensation) by years of service and average wage."),
 "social-security-base": ("Social Security Contribution Base Query",
   "Look up the local social security contribution base upper and lower limits and determine the applicable band for a given salary."),
 "stamp-duty-legal": ("Legal Document Stamp Duty Calculator",
   "Estimate the stamp duty payable on contracts and legal documents by document type and taxable amount under the Stamp Duty Law."),
 "statute-limitations": ("Statute of Limitations Calculator",
   "Compute when the limitation period expires for general or special civil claims from the date the right was known to be harmed."),
 "trademark-class-search": ("Trademark Class Search",
   "Search the 45 international trademark classes by product or service keyword to find the right filing class."),
 "trademark-fee": ("Trademark Registration Fee Calculator",
   "Estimate trademark registration official fees by number of classes and applicant status (individual or entity) under the fee schedule."),
 "traffic-accident-compensation": ("Traffic Accident Compensation Calculator",
   "Estimate traffic accident compensation from medical expenses, lost income, disability grade and the fault liability ratio."),
 "will-template-generator": ("Will Template Generator",
   "Generate an editable will template by selecting the form and filling guided fields; reference only, not legal advice."),
 "will-witness-requirements": ("Will Witness Requirements Guide",
   "Explain the qualifications and exclusions for will witnesses and the witnessing formalities under the Civil Code."),
 "work-injury-compensation": ("Work Injury Compensation Calculator",
   "Estimate work-injury insurance benefits including the lump-sum disability grant and allowance by disability grade and average wage."),
}

ORPHANS = ["generator-18", "estimate-accident", "lookup-classify-1", "lookup-19",
           "lookup-social", "lookup-register", "simulator-37"]


def load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def dump(p, obj, ind):
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=ind)
        f.write('\n')


body = load(os.path.join(I18N, 'legal-body.json'))
sj = load(os.path.join(I18N, 'legal.json'))
enov = load(os.path.join(I18N, '_en_override.json'))

n_ok = 0
for slug, (name, intro) in EN_MAP.items():
    body[slug] = {"title": name, "intro": intro, "h1": name,
                  "en": {"title": name, "h1": name, "intro": intro}}
    e = sj.setdefault(slug, {})
    e['en-US'] = {"title": name, "h1": name, "intro": intro}
    sj[slug] = e
    enov['legal/' + slug] = {"en": name, "ed": name + ". " + intro + SUF, "ind": "legal"}
    n_ok += 1

# 清孤儿键
removed = []
for k in ORPHANS:
    for store, key in ((body, k), (sj, k), (enov, 'legal/' + k)):
        if key in store:
            del store[key]
            removed.append(key)

dump(os.path.join(I18N, 'legal-body.json'), body, 2)
dump(os.path.join(I18N, 'legal.json'), sj, 2)
dump(os.path.join(I18N, '_en_override.json'), enov, 1)

print(f"已写真实英文 {n_ok} 条")
print(f"已清理孤儿键 {len(removed)}: {removed}")
