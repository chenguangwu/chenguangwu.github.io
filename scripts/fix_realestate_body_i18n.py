#!/usr/bin/env python3
"""realestate (54) 英文态八维根治 — A+B 批次（一次成型）：
A：为 54 个真实工具写真实英文名 + 英文 intro，同步四端数据源：
   realestate-body.json(title/h1/intro + en 嵌套) / realestate.json(en-US) /
   _en_override.json(en/ed) / industry-realestate.json(en/ed)
B：直接同步页面静态英文（title-en meta / desc-en meta / h2 内文 / p 内文），
   保留 data-zh 中文原文，避免触发 _build.py 非 CJK 占位页英文未注入缺陷（不动共享构建脚本）。
孤儿键清理：tool-013-33 / tool-014-72。
保持原缩进：realestate.json / realestate-body.json indent=2；_en_override.json indent=1；
industry-realestate.json 维持读入缩进（json.dump indent=1）。
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I18N = os.path.join(ROOT, 'i18n', 'tools')
JSONDIR = os.path.join(ROOT, 'json')
TOOLS = os.path.join(ROOT, 'tools', 'realestate')
SUF = (" Free online tool on ToolBox — 100% client-side, no data uploaded, no install. "
       "Part of the Real Estate tools.")

# slug -> (英文名, 英文intro/描述)
EN_MAP = {
 "analysis-24": ("Property Value Trend Analyzer",
   "Estimate expected appreciation or depreciation of a property from location, price and surrounding factors, generating a comparison checklist to support decisions."),
 "analysis-41": ("Real Estate Market Analysis Report",
   "Produce a market analysis, forecast and strategy report by measuring supply-demand and price trends from key indicators."),
 "analysis-42": ("Competitor Monitoring & Analysis",
   "Track competing projects' price, product and absorption performance and output response suggestions for marketing and positioning."),
 "analysis-45": ("Commercial Space & Footfall Analysis",
   "Analyze a commercial project's scale mix, business-format combination and footfall capacity from input parameters."),
 "analysis-conversion": ("Customer Profiling & Conversion Study",
   "Profile customer segments and evaluate the conversion funnel from input data for property marketing."),
 "analysis-risk-1": ("Investment Feasibility & Risk Analysis",
   "Measure a project's NPV, return and risk indicators by general financial rules for real estate investment."),
 "assessor-23": ("Building Condition & Residual Value Appraisal",
   "Assess a building's condition rate and residual value using the age-life and scoring methods."),
 "assessor-38": ("Mortgage Loan Calculator",
   "Compute a property mortgage loan: loanable amount, rate and term from assessed value, loan-to-value, rate and years."),
 "assessor-39": ("Property Tax Calculator",
   "Compute property-related taxes (deed tax, property tax, VAT) from assessed value and applicable tax rates."),
 "assessor-40": ("Insurance Replacement Value Assessment",
   "Compute replacement cost, actual cash value, insured value and loss indemnity with proportional settlement."),
 "assessor-41": ("Judicial Appraisal Compliance Check",
   "Check compliance of judicial real estate appraisal across qualifications, procedure, standards and report."),
 "assessor-42": ("Collective Land Acquisition Compensation",
   "Compute collective land expropriation compensation from land, resettlement, attachments and young-crop fees."),
 "assessor-43": ("Business Valuation (Asset-Based)",
   "Value a business by the asset-based approach: net asset value from total assets minus total liabilities."),
 "assessor-44": ("Intangible Asset Valuation (Income Approach)",
   "Value intangible assets by the income approach using excess earnings and a capitalization rate."),
 "assessor-45": ("Tax Assessment & Dispute Workflow",
   "Guide the tax-assessment, objection and administrative reconsideration workflow; compute from assessed value."),
 "assessor-46": ("Appraiser Ethics Self-Check",
   "Self-check a real estate appraiser's ethics across independence, impartiality, competence, confidentiality and continuing education."),
 "assessor-47": ("Location Condition Assessment",
   "Assess location conditions: transport, schooling, medical, retail, environment and planning."),
 "assessor-return": ("Income Capitalization Valuation",
   "Value property by the income capitalization method V = NOI / r from annual rent, vacancy and operating cost."),
 "assessor-risk-10": ("Cultural-Tourism Project Risk Assessment",
   "Assess cultural-tourism project risk across market, operation, policy, finance and environment."),
 "assessor-second-hand": ("Second-Hand Home Quick Valuation (Comparison)",
   "Quickly value a resale home by the sales comparison approach from comparable transactions with location, area and floor adjustments."),
 "calc-1": ("Mortgage Equal-Installment vs Equal-Principal",
   "Compare equal-installment and equal-principal repayment: monthly payment, total interest and schedule from amount, term and rate."),
 "calc-2": ("Rental Yield Calculator",
   "Compute the rental yield (annual rent / investment) from price (or down payment) and monthly rent, comparable against the mortgage payment."),
 "calc-70": ("Land Base Price & Floor Area Price",
   "Compute unit land price and floor area price from area, transaction price, FAR and building density versus the base land price."),
 "calc-93": ("Sales Comparison Approach Calculator",
   "Estimate value by the comparison approach, adjusting comparable sale prices by location, floor, orientation and other factors."),
 "calc-assessor": ("Demolition & Relocation Compensation",
   "Compute demolition compensation: housing compensation, moving and temporary relocation allowance from area, unit price and standard."),
 "calc-cost": ("Capital Opportunity Cost Calculator",
   "Measure the implicit cost (foregone next-best return) of committing capital to a real estate project."),
 "calc-return": ("REITs Return Calculator",
   "Compute dividend yield, NAV premium/discount and leveraged return from NAV, market price, annual dividend, shares and leverage."),
 "chiyou-qijianyunying-feiyong": ("Holding Period Operating Cost",
   "Estimate recurring holding costs (tax, property management, maintenance) for a property over the holding period."),
 "convert-area-shared": ("Floor / Inner / Shared Area Converter",
   "Convert among gross floor area, inner area and shared (common) area by factor; check the usable-rate."),
 "cost-depreciation": ("Cost Approach with Depreciation",
   "Value property by the cost approach: replacement cost minus depreciation; for insurance and asset accounting."),
 "cost-depreciation-1": ("Composite Cost Approach Valuation",
   "Synthesize replacement cost, depreciation and land value into a property value when no active comparable market exists."),
 "cost-return": ("Valuation Method Suitability Analyzer",
   "Quantify which of the comparison, income and cost approaches fits a property given its traits, data and market."),
 "depreciation-2": ("Building Depreciation Calculator",
   "Estimate building depreciation and present value by the age-life method or condition rate."),
 "down-payment": ("Down Payment & Loan Estimator",
   "From total price and down-payment ratio compute the down payment, commercial/provident-fund loan amounts, and repayment by rate and term."),
 "estimate-37": ("Vacancy Loss Estimator",
   "From potential gross rent, vacancy rate, collection loss and concession compute effective gross income (EGI) and vacancy loss."),
 "estimate-analysis-2": ("Investment Analysis & Decision Model",
   "Model project feasibility by cash flow and return metrics for development and investment decisions."),
 "fangdichan-xintuo-jijinguzhi": ("Real Estate Trust Fund Valuation",
   "Value REITs-type assets by NAV and return from input parameters."),
 "fund-loan": ("Housing Provident Fund Loan Quota",
   "Estimate the provident-fund loan quota by both the balance-multiple and monthly-contribution methods, taking the higher."),
 "fund-loan-1": ("Provident Fund Loan Eligibility",
   "Compute the maximum provident-fund loan from account balance and contribution base before applying."),
 "generator-assessor": ("Appraisal Report Template Generator",
   "Generate an editable appraisal report template with summary, method and conclusion placeholders; drafting aid only."),
 "layout-score": ("Floor Plan Scoring",
   "Score a floor plan (out of 100) from usable rate, regularity, width-depth ratio and lighting."),
 "market-valuation": ("Resale Home Valuation (Comparison)",
   "Quickly estimate value from the neighborhood reference average with floor, orientation, renovation and age adjustments."),
 "paimai-baoliujia-qipaijia-sheding": ("Auction Reserve & Starting Price Setter",
   "Set the reserve and starting-price range from appraised value and strategy for judicial auctions and asset disposal."),
 "price-discount-1": ("Pricing & Discount Strategy",
   "From cost and positioning set discount depth and concession space for promotions and channel pricing."),
 "pv": ("Discounted Cash Flow (NPV) Calculator",
   "Discount future cash flows to present value by a discount rate (NPV basis) for real estate investment."),
 "rater-usable-layout": ("Usable-Rate & Regularity Scorer",
   "From gross and usable area and width-depth compute usable rate and regularity (depth/width ratio) with a rating."),
 "rent-1": ("Market Rent & Potential Gross Income",
   "Estimate market rent level and potential gross income from input parameters for landlord pricing and investment."),
 "return-1": ("Income Capitalization (Net Income / Cap Rate)",
   "Value income property by net operating income divided by capitalization rate."),
 "return-2": ("Income Approach Valuation (NOI / Cap Rate)",
   "Value by direct capitalization and DCF from annual NOI, cap rate and growth rate."),
 "shichang-bijiaofa-anlixiuzheng": ("Sales Comparison Case Adjustment",
   "Input several comparable sale prices and adjustment coefficients; compute each adjusted price and a weighted estimate."),
 "summary-second-hand": ("Resale Home Tax Summary (Deed/PIT/VAT)",
   "Sum resale transaction taxes (deed tax, personal income tax, VAT) by general rules from contract price and holding years."),
 "tudi-jizhundijia-luxianjia-xishuxiuzheng": ("Land Base/Route Price Coefficient Adjustment",
   "From base or route land price with term, date, FAR, zone and specific-factor coefficients compute the adjusted land price."),
 "xianjinliuyuce": ("Cash Flow Forecast",
   "Forecast multi-year NOI from rent income, vacancy, operating expense ratio, debt service and rent growth."),
 "yanglao-dichan-touzi-tuichu-jihui": ("Senior Housing Investment & Exit",
   "Evaluate senior/healthcare real estate return and exit paths from input parameters."),
}

ORPHANS = ["tool-013-33", "tool-014-72"]

_CJK = re.compile(r'[\u4e00-\u9fff]')


def esc_html(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def esc_attr(s):
    return esc_html(s).replace('"', '&quot;')


def load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def dump(p, obj, ind):
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=ind)
        f.write('\n')


body = load(os.path.join(I18N, 'realestate-body.json'))
sj = load(os.path.join(I18N, 'realestate.json'))
enov = load(os.path.join(I18N, '_en_override.json'))
ind = load(os.path.join(JSONDIR, 'industry-realestate.json'))

# ---- A：四端数据源 ----
n_ok = 0
for slug, (name, intro) in EN_MAP.items():
    body[slug] = {"title": name, "intro": intro, "h1": name,
                  "en": {"title": name, "h1": name, "intro": intro}}
    e = sj.setdefault(slug, {})
    e['en-US'] = {"title": name, "h1": name, "intro": intro}
    sj[slug] = e
    enov['realestate/' + slug] = {"en": name, "ed": name + ". " + intro + SUF, "ind": "realestate"}
    # industry-realestate.json en/ed
    for it in ind:
        if it.get('file') == slug + '.html':
            it['en'] = name
            it['ed'] = name + ". " + intro + SUF
            break
    n_ok += 1

# 清孤儿键
removed = []
for k in ORPHANS:
    for store, key in ((body, k), (sj, k), (enov, 'realestate/' + k)):
        if key in store:
            del store[key]
            removed.append(key)

dump(os.path.join(I18N, 'realestate-body.json'), body, 2)
dump(os.path.join(I18N, 'realestate.json'), sj, 2)
dump(os.path.join(I18N, '_en_override.json'), enov, 1)
dump(os.path.join(JSONDIR, 'industry-realestate.json'), ind, 1)

# ---- B：页面静态英文同步 ----
n_title = n_desc = n_h2 = n_p = 0
for slug, (name, intro) in EN_MAP.items():
    fp = os.path.join(TOOLS, slug + '.html')
    if not os.path.exists(fp):
        continue
    s = open(fp, encoding='utf-8').read()

    # title-en meta（任意属性顺序）
    s2 = re.sub(r'(<meta\b[^>]*\bname="title-en"[^>]*\bcontent=")[^"]*(")',
                lambda m: m.group(1) + esc_attr(name) + m.group(2), s, count=1)
    if s2 != s:
        n_title += 1
    s = s2

    # desc-en meta（任意属性顺序）
    ed = name + ". " + intro + SUF
    s2 = re.sub(r'(<meta\b[^>]*\bname="desc-en"[^>]*\bcontent=")[^"]*(")',
                lambda m: m.group(1) + esc_attr(ed) + m.group(2), s, count=1)
    if s2 != s:
        n_desc += 1
    s = s2

    # h2 内文（保留 icon 前缀 + data-zh）；整段开标签捕获，避免 group 错位
    def _h2(m):
        open_tag, inner, close = m.group(1), m.group(2), m.group(3)
        mm = re.match(r'^([^\u4e00-\u9fffA-Za-z0-9]*)([\s\S]*)$', inner)
        icon = mm.group(1) if mm else ''
        return '%s%s%s' % (open_tag, esc_html(icon + name), close)
    s2 = re.sub(r'(<h2\b[^>]*data-zh="[^"]*">)([\s\S]*?)(</h2>)', _h2, s, count=1)
    if s2 != s:
        n_h2 += 1
    s = s2

    # p 静音内文（保留 data-zh）
    s2 = re.sub(
        r'(<p\s+style="font-size:13px;color:var\(--text-muted\)[^"]*"[^>]*>)([\s\S]*?)(</p>)',
        lambda m: m.group(1) + esc_html(intro) + m.group(3), s, count=1)
    if s2 != s:
        n_p += 1
    s = s2

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(s)

print(f"A 已写真实英文 {n_ok} 条；清孤儿键 {len(removed)}: {removed}")
print(f"B 页面同步：title-en={n_title} desc-en={n_desc} h2={n_h2} p={n_p}")
