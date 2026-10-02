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
    write('kaidian-yunyingyuguizeduibijisuanqi', build('kaidian-yunyingyuguizeduibijisuanqi', [
        "\U0001F6CD\uFE0F Store Setup, Operations and Rules Comparison Calculator",
        "Compare how well the operating rules fit and the margin of leadership, from the combined scores of two platforms.",
        "Platform (Store Setup / Operations / Rules) Familiarity",
        "/ Platform (Store Setup / Operations / Rules) Familiarity",
        "\U0001F4D6 View the \"Store Setup, Operations and Rules Comparison Calculator Guide\"",
        "This tool compares the store setup and operating costs of several platforms using the deposit, commission rate, annual fee and traffic rules, and outputs a comparison verdict.",
        "Platform A combined score",
        "Platform B combined score",
        "\U0001F4A1 Average score = (A + B) \u00f7 2; margin of leadership = (A \u2212 B) \u00f7 B \u00d7 100%; the higher-scoring platform is the better choice as the main operating platform.",
        "\U0001F4DA In-depth Analysis: Store Setup, Operations and Rules Comparison Calculator",
        "Store setup comparison: enter each platform's deposit, commission and annual fee to compute the first-year entry cost.",
        "Rules comparison: compare traffic allocation and campaign thresholds to see which platform suits the category better.",
        "Classroom demo: show how sensitive the",
        "profit margin",
        "is to the commission rate.",
        "Example: platform A charges 5% commission with a 10000 deposit, platform B 8% with a 5000 deposit; for high-ticket products A saves on commission.",
        "How much does commission matter?",
        "Commission cuts straight into profit; the difference is significant for high-ticket or high-volume sales, making it a key factor when choosing a platform. " + DISCL_E,
        "Is the deposit refundable?",
        "Most are refundable but conditional, paid back only after the store is closed and settled, so the capital tied up must be counted. " + DISCL_E,
        "Is the annual fee worth it?",
        "Annual fees usually buy traffic or tool benefits; for low-frequency, low-volume stores they may not pay off, so judge by expected sales. " + DISCL_E,
        "About \"Platform (Store Setup / Operations / Rules) Familiarity\"",
        "Platform (Store Setup / Operations / Rules) Familiarity.",
        "Compare store setup and operating costs across platforms",
        "Comparing first-year entry costs across platforms",
        "Estimating the impact of commission rates on profit",
        "Comparing the capital tied up in deposits and annual fees",
        "Choosing a platform that fits the category",
        "Store setup",
        "Operations",
    ]))

    write('kedan-jiandanjia-liandailv', build('kedan-jiandanjia-liandailv', [
        "\U0001F6CD\uFE0F Order Value (Item Price / Attachment Rate)",
        "Compute the average item price, average order value and sales scale from the sales amount and units sold.",
        "\U0001F4D6 View the \"Order Value (Item Price / Attachment Rate) Guide\"",
        "Average order value = sales / orders",
        "This tool computes average order value, average item price and the attachment rate from sales, order count and item count, supporting attachment-sales analysis for stores.",
        "Sales amount (\u00a5)",
        "Units sold",
        "\U0001F4A1 Average item price = sales \u00f7 units sold; average order value = average item price \u00d7 attachment rate (a reference of 1.5 items per order).",
        "\U0001F4DA In-depth Analysis: Order Value (Item Price / Attachment Rate)",
        "Order value analysis: enter sales and order count to compute the average order value.",
        "Attachment analysis: enter the item count and order count to compute the attachment rate (items per order).",
        "Classroom demo: average order value = average item price \u00d7 attachment rate.",
        "Example: sales 10000, orders 200, items 320 gives an average order value of 50, an average item price of 31.25 and an attachment rate of 1.6 items per order.",
        "What is the attachment rate?",
        "The average number of items per order, reflecting cross-selling ability; raising it lifts order value without extra traffic. " + DISCL_E,
        "What is the average order value formula?",
        "= sales / orders = average item price \u00d7 attachment rate; the three move together, so improving any one of them raises order value. " + DISCL_E,
        "Is a higher attachment rate always better?",
        "A moderate increase helps, but forced bundling hurts the experience; rely on sensible combinations and recommendations. " + DISCL_E,
        "About \"Order Value (Item Price / Attachment Rate)\"",
        "Order Value (Item Price / Attachment Rate).",
        "Compute order value and attachment from sales and item count",
        "Average order value and average item price accounting",
        "Attachment rate analysis and improvement",
        "Diagnosing in-store attachment sales",
        "Evaluating the effect of bundle recommendations",
        "Item price",
        "Attachment rate",
    ]))

    write('pingjia-chaping-tuihuo-lv', build('pingjia-chaping-tuihuo-lv', [
        "\U0001F4CB Review (Negative / Return) Rate",
        "Compute the return rate, retained order rate and returns per thousand orders from orders and returns.",
        "\U0001F4D6 View the \"Review (Negative / Return) Rate Guide\"",
        "Return rate = returns / orders",
        "This tool computes the positive review rate, negative review rate and return rate from the review, negative review and return counts, supporting service and quality monitoring.",
        "Orders",
        "Returns",
        "\U0001F4A1 Return rate = returns \u00f7 orders \u00d7 100%; retention rate = (orders \u2212 returns) \u00f7 orders \u00d7 100%; a return rate above 5% means the product and its description need checking.",
        "\U0001F4DA In-depth Analysis: Review (Negative / Return) Rate",
        "Experience monitoring: enter reviews and negative reviews to compute the negative review rate and set a threshold alert.",
        "Quality analysis: enter returns and orders to compute the return rate and locate the high-return categories.",
        "Classroom demo: negative review rate = negative reviews / total reviews.",
        "Example: 1000 reviews with 30 negative gives a 3% negative rate; 50 returns out of 1000 orders gives a 5% return rate.",
        "How is the negative review rate calculated?",
        "= negative reviews / total reviews; looking only at positive reviews overlooks the neutral ones, so the negative rate gives a more direct picture. " + DISCL_E,
        "Is a high return rate a problem?",
        "A high return rate hurts profit and experience; separate out the main causes (sizing, quality, description mismatch) and fix each one. " + DISCL_E,
        "Can reviews be faked?",
        "Fake reviews break platform rules and distort the picture; improve the experience from genuine reviews instead of falsifying them. " + DISCL_E,
        "About \"Review (Negative / Return) Rate\"",
        "Review (Negative / Return) Rate.",
        "Compute positive, negative and return rates with alerts",
        "Negative review rate threshold monitoring",
        "Locating high-return categories",
        "Attributing causes in experience and quality control",
        "Review structure health dashboard",
        "Negative",
        "Returns",
    ]))

    write('report', build('report', [
        "\U0001F4C8 BI (Report / Visualisation) Dashboard",
        "Period-over-period dashboard for business metrics",
        "\U0001F4D6 View the \"BI (Report / Visualisation) Dashboard Guide\"",
        "Enter one line per metric as \"metric, current, previous\". The period-over-period change = (current \u2212 previous) \u00f7 previous \u00d7 100%. The tool totals the number of metrics that rose and fell plus the average change, and names the metric with the largest increase; inverse metrics such as the return rate need to be read against the business definition.",
        "Metric data (one \"metric, current, previous\" per line)",
        "GMV,320000,300000\nOrders,5200,5000",
        "Generate dashboard",
        "\U0001F4DA In-depth Analysis: How to Build a Period-over-Period Dashboard for Business Metrics",
        "E-commerce operators organise GMV, order count, average order value,",
        "conversion rate",
        "and return rate into a dashboard weekly or monthly to see the overall trend at a glance.",
        "Before a review meeting, compare the current and previous periods to find the metrics with the largest rise and the sharpest fall, and set the next optimisation priorities.",
        "When comparing several stores side by side, use the average period-over-period change to judge whether the overall trend is up, flat or down.",
        "Trial calculation for five metrics",
        "Enter \"GMV,860000,720000; Orders,12400,10800; Average order value,69.35,66.67; Conversion rate,3.20,2.85; Return rate,4.80,5.60\" and the period-over-period changes are +19.44%, +14.81%, +4.02%, +12.28% and \u221214.29%, with 4 metrics up and 1 down, an average change of +7.25%, and GMV showing the largest increase.",
        "How is the overall verdict judged?",
        "An average change of \u22655% counts as an overall uptrend, \u2264\u22125% as an overall downtrend, and anything in between as basically flat; inverse metrics are best read separately.",
        "What if the previous period is 0?",
        "The change divides by the previous period value, so rows with a previous value of 0 are skipped; fill in real previous-period data or switch to another definition.",
        "Can metrics of different magnitudes be compared?",
        "This tool only compares the current and previous periods of the same metric and never compares magnitudes across metrics, so metrics of different scales can be placed together to see trends.",
        "About \"BI (Report / Visualisation) Dashboard\"",
        "BI (Report / Visualisation) Dashboard.",
        "Visualising multi-dimensional business metric cards",
        "Building daily or weekly business dashboards",
        "Highlighting abnormal key metrics in red",
        "Showing period-over-period, year-over-year and share figures",
        "Snapshot summary of core metrics",
    ]))

    write('response-2', build('response-2', [
        "\U0001F3A7 Customer Service (Enquiry / Complaint) Response",
        "Compute the on-time response rate and the number of overdue tickets from enquiry volume and on-time responses.",
        "\U0001F4D6 View the \"Customer Service (Enquiry / Complaint) Response Guide\"",
        "Customer service response = timeliness statistics",
        "This tool computes average response time, first response time and resolution rate metrics from enquiry volume, first response duration and resolution rate.",
        "Total enquiries",
        "Responses within 5 minutes",
        "\U0001F4A1 On-time rate = responses within 5 minutes \u00f7 total enquiries \u00d7 100%; overdue count = total enquiries \u2212 on-time responses; an on-time rate below 90% means more agents are needed.",
        "\U0001F4DA In-depth Analysis: Customer Service (Enquiry / Complaint) Response",
        "Response assessment: enter session volume and response durations to compute the average and first response times.",
        "Resolution rate: enter the number resolved and the total to compute the resolution rate and gauge service quality.",
        "Classroom demo: the response time distribution (P50/P90) is more telling than the average.",
        "Example: 500 sessions with 25000 seconds of total response time gives an average of 50 seconds; 460 resolved gives a 92% resolution rate.",
        "Average or percentile?",
        "The average is easily skewed by long sessions, so P50 and P90 better reflect what most users experience. " + DISCL_E,
        "How is the resolution rate defined?",
        "= resolved / total; the definition covers both on-the-spot resolution and follow-up, and must be closed within the SLA. " + DISCL_E,
        "What if responses are slow?",
        "Peak-hour scheduling plus script templates or a bot in front can cut the first response time, but complex issues still need a human. " + DISCL_E,
        "About \"Customer Service (Enquiry / Complaint) Response\"",
        "Customer Service (Enquiry / Complaint) Response.",
        "Compute average and first response times plus the resolution rate",
        "Assessing customer service response times",
        "P50/P90 distribution of first response",
        "Resolution rate and service quality monitoring",
        "Reference for peak-hour scheduling",
        "Enquiry",
        "Complaint",
    ]))


if __name__ == '__main__':
    main()
