#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'ecommerce')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'ecommerce')
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
    out = {'slug': slug, 'industry': 'ecommerce', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

DISCL_E = "Results are for e-commerce operations estimates, product selection and decision reference only; they are not financial or tax advice and do not replace the latest platform rules or formal reconciliation \u2014 the platform's official rules and actual accounts prevail."


def main():
    write('analysis-25', build('analysis-25', [
        "\U0001F4CA Competitor (Price Comparison / Monitoring) Analysis",
        "Competitor Price Comparison and Gap Monitoring",
        "\U0001F4D6 View the \"Competitor (Price Comparison / Monitoring) Analysis Guide\"",
        "Enter one line per item as \"item, your price, competitor price\". The gap = your price \u2212 competitor price; the gap rate = gap \u00f7 competitor price \u00d7 100%. A negative value means your store is cheaper. The summary gives the number of items where you are cheaper or dearer plus the average gap rate, and pinpoints the item with the smallest gap, for product pricing and competitor price monitoring.",
        "Price comparison data (one \"item, your price, competitor price\" per line)",
        "Item A,99,109\nItem B,199,189",
        "Price comparison analysis",
        "\U0001F4DA In-depth Analysis: Competitor Price Comparison and Gap Monitoring",
        "E-commerce operators regularly capture competitors' prices for the same products, compare them item by item with their own prices, find the items at a price disadvantage and decide whether to reprice or replace them.",
        "Before a big promotion, take stock of the price band and use the average gap rate to judge whether your overall pricing is high or competitive.",
        "During product selection, compare the gap between candidate products and competitors to assess how much of a price war you could absorb later.",
        "Trial calculation for four products",
        "Enter \"Item A,89,99; Item B,159,149; Item C,45,45; Item D,299,329\" and the gaps are \u221210, +10, 0 and \u221230, with gap rates of \u221210.10%, +6.71%, 0.00% and \u22129.12%; 2 items are cheaper, 1 is dearer, the average gap rate is \u22123.13%, and the item with the lowest gap is Item D.",
        "What does a negative gap rate mean?",
        "It means your price is below the competitor's; the larger the negative value, the stronger your price advantage. A positive value means your store is dearer, putting you at a price disadvantage.",
        "How is the overall verdict judged?",
        "An average gap rate below \u22122% counts as an overall price advantage, above 2% as overall on the high side, and anything in between as roughly on par.",
        "What if the competitor price is 0?",
        "The gap rate divides by the competitor price, so rows with a competitor price of 0 are skipped; please enter real, valid competitor prices.",
        "About \"Competitor (Price Comparison / Monitoring) Analysis\"",
        "Competitor (Price Comparison / Monitoring) Analysis.",
        "Enter the final prices of the same product across platforms to compute gaps and monitoring alerts automatically",
        "Multi-platform product selection, price comparison and lowest-price judgement",
        "Historical price tracking and fake-discount monitoring for key SKUs",
        "Gap review before and after campaign price changes",
        "Quick view of the competitor price band distribution",
        "Item A,89,99",
    ]))

    write('analysis-70', build('analysis-70', [
        "\U0001F680 Review (Data / Analysis / Improvement) Mechanism",
        "Data / Analysis / Improvement",
        "Review (Data / Analysis / Improvement) Mechanism",
        "/ Review (Data / Analysis / Improvement) Mechanism",
        "\U0001F4D6 View the \"analysis-70 Guide\"",
        "Enter GMV, order count, refund rate and customer acquisition cost period by period; compute the period-over-period GMV growth rate in chronological order, compare the period-by-period changes in refund rate and acquisition cost, automatically flag the periods that worsened (refund rate or acquisition cost up more than 0.3pt period over period), and finally give an overall review verdict of \"improving / needs attention\".",
        "Enter the operating metrics for each period (one per line: period, GMV, orders, refund rate %, acquisition cost)",
        "Period 1,120000,3400,3.5,28\nPeriod 2,138000,3900,3.1,26\nPeriod 3,152000,4200,2.8,25",
        "Review analysis",
        "\U0001F4DA In-depth Analysis: Descriptive Statistics of Review Data",
        "Paste in a set of daily or weekly metrics needed for the review and first check the",
        "count and total to be sure nothing is missing, then look at the mean and",
        "to judge the central tendency.",
        "Use the range and",
        "to judge how dispersed the daily or weekly metrics for the review are; a large standard deviation means inconsistent definitions or outliers.",
        "Run two batches separately and compare their means and standard deviations for a first take on the difference.",
        "Example of the daily or weekly metrics needed for the review",
        "Enter the daily or weekly metrics for the review: 128,142,135,160,151,129,147. Sample size 7, total 992, mean 141.71, median 142, range 32, standard deviation 11.71. The mean 141.7 and the median 142 are almost identical, which shows this batch of",
        "data is distributed",
        "evenly; day 4 at 160 is the peak, so go back and check what action was taken that day.",
        "Can it generate review conclusions or improvement items automatically?",
        "No. The tool only performs descriptive statistics on the numbers; it includes no attribution analysis, funnel breakdown or improvement suggestion generation. The output can serve as input for a review meeting.",
        "What input formats are supported?",
        "Values separated by commas, spaces or line breaks all work, and non-numeric content is ignored automatically. One value per line in chronological order is recommended so you can match them against dates later.",
        "Competitor (Monitoring / Analysis / Response) Research",
        "About \"Review (Data / Analysis / Improvement) Mechanism\"",
        "Review (Data / Analysis / Improvement) Mechanism. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
        "Period 1,120000,3400,3.5,28\nPeriod 2,138000,3900,3.1,26\nPeriod 3,152000,4200,2.8,25",
    ]))

    write('analysis-71', build('analysis-71', [
        "\U0001F4CA Competitor (Monitoring / Analysis / Response) Research",
        "Monitoring / Analysis / Response",
        "Competitor (Monitoring / Analysis / Response) Research",
        "/ Competitor (Monitoring / Analysis / Response) Research",
        "\U0001F4D6 View the \"analysis-71 Guide\"",
        "Aggregate each competitor's price, monthly sales, rating and delivery lead time; compute the price range and average price; sort by rating and mark the highest-rated and fastest-shipping ones; then suggest a differentiated competitive strategy based on your relative position.",
        "Enter the metrics for each competitor (one per line: competitor, price, monthly sales, rating, delivery days)",
        "Competitor A,199,5200,4.8,2\nCompetitor B,229,3100,4.6,3\nCompetitor C,179,8800,4.9,1",
        "Competitor analysis",
        "\U0001F4DA In-depth Analysis: Descriptive Statistics of Competitor Monitoring Data",
        "Paste in a set of monitored competitor metrics and first check the",
        "count and total to be sure nothing is missing, then look at the mean and",
        "to judge the central tendency.",
        "Use the range and",
        "to judge how dispersed the monitored competitor metrics are; a large standard deviation means inconsistent definitions or outliers.",
        "Run two batches separately and compare their means and standard deviations for a first take on the difference.",
        "Example of monitored competitor metrics",
        "Enter the monitored competitor metrics: 99,105,102,118,112,97,108. Sample size 7, total 741, mean 105.86, median 105, range 21, standard deviation 6.79. The mean 105.9 is slightly above the median 105, showing one or two high observations (118, 112) pulled the average up, so the median describes the typical level better.",
        "Can it fetch competitor data automatically?",
        "No. The tool has no data collection or scraping capability; you need to paste in the values you have already monitored for the statistics.",
        "Why do my figures come out so different?",
        "First make sure the definitions match: data from different channels or different time granularities (daily vs weekly) must not be mixed in one batch. Fix one definition before entering data.",
        "Review (Data / Analysis / Improvement) Mechanism",
        "About \"Competitor (Monitoring / Analysis / Response) Research\"",
        "Competitor (Monitoring / Analysis / Response) Research. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
        "Competitor A,199,5200,4.8,2\nCompetitor B,229,3100,4.6,3\nCompetitor C,179,8800,4.9,1",
    ]))

    write('analysis-conversion-funnel', build('analysis-conversion-funnel', [
        "\U0001F3AF Conversion (Funnel / Drop-off) Analysis",
        "Funnel / Drop-off",
        "\U0001F4D6 View the \"Conversion (Funnel / Drop-off) Analysis Guide\"",
        "Adjacent conversion rate = this stage's count \u00f7 the previous stage's count \u00d7 100%",
        "Overall conversion rate = \u03a0 of the adjacent conversion rates = last stage \u00f7 first stage \u00d7 100%",
        "Funnel stages (one per line: stage name, count, in top-to-bottom order)",
        "Impressions,12000\nClicks,900\nAdd to cart,270\nOrders,108\nPayments,90",
        "Analyze funnel",
        "\U0001F4DA In-depth Analysis: Conversion (Funnel / Drop-off) Analysis",
        "Bottleneck identification: enter the headcount at each funnel stage and compute the",
        "conversion rate",
        "between adjacent stages to find where the biggest drop-off occurs.",
        "Campaign review: enter the funnel data for a campaign and compare it with industry benchmarks to see which stage is weak.",
        "Classroom demo: the drop-off rate = 1 \u2212 conversion rate, and multiplying the stages gives the overall conversion.",
        "Example: impressions 10000 \u2192 clicks 500 (5%) \u2192 add to cart 100 (20%) \u2192 orders 30 (30%) \u2192 payments 24 (80%), overall conversion 0.24%.",
        "How should the funnel stages be defined?",
        "Split them along the business path (impressions \u2192 clicks \u2192 add to cart \u2192 orders \u2192 payment); the definitions must be consistent across stages before conversion can be computed. " + DISCL_E,
        "What about the sum of drop-off rates?",
        "Drop-off rates cannot simply be added up; the overall conversion rate is the product of the stage conversion rates. " + DISCL_E,
        "Where do industry benchmarks come from?",
        "They vary a lot by category (higher for standard goods, lower for non-standard ones); use your own history and published benchmarks for the same category as reference. " + DISCL_E,
        "About \"Conversion (Funnel / Drop-off) Analysis\"",
        "Conversion (Funnel / Drop-off) Analysis.",
        "Enter the headcount at each funnel stage to compute conversion and drop-off automatically",
        "Locate bottlenecks from impressions \u2192 clicks \u2192 add to cart \u2192 payment",
        "Funnel review for major promotions",
        "Compare with industry benchmarks to find weak stages",
        "Compare conversion before and after a landing page redesign",
        "For example: Impressions,10000",
    ]))

    write('analysis-cost-8', build('analysis-cost-8', [
        "\U0001F4B0 Cost (Control / Optimization / Benefit) Analysis",
        "Control / Optimization / Benefit",
        "\U0001F4D6 View the \"Cost (Control / Optimization / Benefit) Analysis Guide\"",
        "Break-even volume = fixed costs \u00f7 (unit price \u2212 unit variable cost); unit contribution margin = unit price \u2212 unit variable cost",
        "Cost-volume-profit (CVP) analysis: enter fixed costs, unit variable cost and unit price to compute the unit contribution margin, break-even volume and break-even revenue, supporting pricing and cost control.",
        "Fixed costs (\u00a5)",
        "Unit variable cost (\u00a5)",
        "Unit price (\u00a5)",
        "Compute break-even",
        "\U0001F4DA In-depth Analysis: Cost (Control / Optimization / Benefit) Analysis",
        "Gross margin accounting: enter the selling price and each cost item to compute gross profit and",
        ", then spot the low-margin products.",
        "Cost structure: enter the shares of promotion, commission and logistics to see whether expenses eat the profit.",
        "Classroom demo: gross margin = (price \u2212 cost) / price.",
        "Example: price 100, purchase 50, promotion 15, commission 5, logistics 8, total cost 78, gross profit 22, gross margin 22%.",
        "What is the difference between gross and net profit?",
        "Gross profit deducts direct costs, while net profit also deducts taxes and amortisation; this tool stops at gross profit, so net profit should come from your financial accounts. " + DISCL_E,
        "Is commission a cost?",
        "Platform commission is a variable cost and should be included in the unit cost, otherwise gross profit looks inflated. " + DISCL_E,
        "Does a high cost ratio mean a loss?",
        "A high cost ratio with high turnover can still be profitable; look at cost-effectiveness and repeat purchases, since the ratio alone can mislead. " + DISCL_E,
        "About \"Cost (Control / Optimization / Benefit) Analysis\"",
        "Cost (Control / Optimization / Benefit) Analysis.",
        "Compute gross profit itemised by purchase, commission, logistics and promotion",
        "Gross margin accounting per product and per store",
        "Identify and optimise low-margin products",
        "Analysis of the cost structure shares",
        "Profit estimation before and after promotions",
    ]))


if __name__ == '__main__':
    main()
