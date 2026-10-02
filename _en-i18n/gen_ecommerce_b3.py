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
    write('erp-dingdan-caigou-duijie', build('erp-dingdan-caigou-duijie', [
        "\U0001F6CD\uFE0F ERP (Order / Purchase) Integration",
        "Assess how well ERP order and purchase documents match, from the order count and purchase order count.",
        "\U0001F4D6 View the \"ERP (Order / Purchase) Integration Guide\"",
        "ERP integration = data mapping",
        "This tool computes the reorder point and replenishment advice from order volume, purchase lead time and safety stock, and generates an order-to-purchase field mapping to support ERP coordination.",
        "Orders",
        "Purchase orders",
        "\U0001F4A1 Document match rate = purchase orders \u00f7 orders \u00d7 100%; document difference = orders \u2212 purchase orders; purchase orders per order = purchase orders \u00f7 orders.",
        "\U0001F4DA In-depth Analysis: ERP (Order / Purchase) Integration",
        "Replenishment advice: enter average daily sales, lead time and safety stock to get the reorder point.",
        "Field mapping: enter the platform order fields and the ERP purchase fields to generate an integration mapping table.",
        "Classroom demo: reorder point = lead-time demand + safety stock.",
        "Example: daily 20, lead time 5 days, safety stock 100, reorder point = 20\u00d75+100=200, so replenish below that.",
        "How is the reorder point set?",
        "= average daily sales \u00d7 lead time + safety stock; falling below it triggers purchasing to prevent stockouts. " + DISCL_E,
        "Do the fields have to match for integration?",
        "Platform orders must be mapped to ERP item codes; mismatched codes lead to wrong or missed purchases. " + DISCL_E,
        "How much safety stock should be set?",
        "Balance stockout risk against capital tied up; set it higher when demand is volatile or lead times are long. " + DISCL_E,
        "About \"ERP (Order / Purchase) Integration\"",
        "ERP (Order / Purchase) Integration.",
        "Compute the reorder point and generate field mappings",
        "Reorder points and replenishment alerts",
        "Mapping platform orders to ERP items",
        "Setting safety stock against purchase lead time",
        "Stockout risk checks",
        "Orders",
        "Purchasing",
    ]))

    write('estimate-ranking', build('estimate-ranking', [
        "\U0001F3AF Ranking (Search / Weight) Estimation",
        "Estimate the combined ranking score and the gap to the first-page threshold from search volume and weight score.",
        "\U0001F4D6 View the \"Ranking (Search / Weight) Estimation Guide\"",
        "Ranking = weight \u00d7 factor",
        "This tool estimates the search ranking score and relative position from weighted factors such as sales, rating, clicks and conversion, supporting search optimisation.",
        "Keyword search volume",
        "Weight score",
        "\U0001F4A1 Combined ranking score = search volume \u00d7 weight score \u00f7 100; the first-page threshold is 90% of the search volume; the gap = threshold \u2212 ranking score.",
        "\U0001F4DA In-depth Analysis: Ranking (Search / Weight) Estimation",
        "Score estimation: enter each factor and its weight to compute the combined ranking score.",
        "Optimisation checks: raise the rating or conversion and watch the score change to locate the weak factor.",
        "Classroom demo: normalise first, then take the weighted sum.",
        "Example: sales weight 0.4 scoring 80, rating 0.3 scoring 70, conversion 0.3 scoring 60, combined = 0.4\u00d780+0.3\u00d770+0.3\u00d760=71.",
        "Where do the weights come from?",
        "Platform algorithms are not public; this tool estimates trends using empirical weights and serves only as a guide for the optimisation direction. " + DISCL_E,
        "Do the factors use different scales?",
        "Normalise them to the same scale before weighting, otherwise the factor with the largest scale dominates the result. " + DISCL_E,
        "Does a high score mean a higher rank?",
        "Ranking is also affected by real-time behaviour and personalisation, so the score only reflects a relative position under static weights. " + DISCL_E,
        "About \"Ranking (Search / Weight) Estimation\"",
        "Ranking (Search / Weight) Estimation.",
        "Estimate the search ranking score from weighted factors",
        "Search ranking score estimation",
        "Locating weak points in rating or conversion",
        "Comparing before and after title and main image optimisation",
        "Judging relative position within a category",
    ]))

    write('groupon-filler', build('groupon-filler', [
        "\"Groupon Filler\" performs a professional calculation from the input parameters and outputs the result.",
        "/ Threshold Order Filler Calculator",
        "\U0001F4D6 View the \"groupon-filler Guide\"",
        "\U0001F9EE Threshold Order Filler Calculator",
        "Short 12 yuan of the \"spend 300, get 50 off\" threshold? List the candidate product prices and the tool automatically finds the best filler combination (one or more products) and works out the smallest shortfall and the final amount paid.",
        "Discount amount (\u00a5)",
        "Current selected amount (\u00a5)",
        "Candidate filler product prices (comma separated)",
        "\U0001F4DA In-depth Analysis: Groupon Filler",
        "Filler shortfall: enter the cart amount and threshold to see how much more is needed to qualify.",
        "Scheme suggestions: enter candidate filler prices and pick the combination with the smallest overshoot.",
        "Classroom demo: \"just reaching the threshold\" beats \"far exceeding it\".",
        "Example: a cart of 268 against a \"spend 300, get 30 off\" threshold leaves a 32 yuan shortfall; adding a 35 yuan product gives the better deal and avoids wasteful overspending.",
        "Is filling the order worth it?",
        "Only if you actually need the filler item; buying something useless just to reach the threshold costs more, so look at the net benefit. " + DISCL_E,
        "Do thresholds stack?",
        "With multiple tiers (spend 300 get 30 off / spend 500 get 60 off) the highest tier reached applies; check whether tiers can be combined. " + DISCL_E,
        "How is the shortfall calculated?",
        "Shortfall = threshold \u2212 current amount; a negative value means the threshold is already met, and filling just past the threshold is the cheapest option. " + DISCL_E,
        "Best single item plus a two-item two-pointer combination for the smallest shortfall",
        "Candidate prices must be for products that can be added individually (some platform products are excluded from threshold offers)",
        "Amount paid = current amount + filler \u2212 discount; the lower the discount rate, the better the deal",
        "Results are for reference only; the e-commerce platform checkout page prevails",
    ]))

    write('index', build('index', [
        "\U0001F6CD\uFE0F E-commerce Tools",
        "E-commerce",
        "E-commerce Tools",
        "Threshold Order Filler Calculator",
        "The Threshold Order Filler Calculator is a free online e-commerce tool: short 12 yuan of the \"spend 300, get 50 off\" threshold? List the candidate product prices and it automatically finds the best filler combination (one or more products) and works out the smallest shortfall and the final amount paid. It runs purely in the browser, uploads no data, and needs no\u2026",
        "Enter the transaction amount and commission rate (or platform service fee ratio) to compute the commission or platform service fee deducted, helping merchants work out the amount actually received and the fee share.",
        "Enter the current and base period values (the same period last year or the previous period) to compute year-over-year and period-over-period growth rates, for trend analysis of e-commerce sales and operating metrics.",
        "Enter parameters such as order volume and purchase cycle to estimate how orders and purchasing line up in the ERP plus safety stock, supporting purchase planning for the e-commerce supply chain.",
        "Enter the number of reviews and negative reviews (or returns) to compute the negative review rate and return rate, for monitoring store service quality and product satisfaction and warning of anomalies in time.",
        "An e-commerce conversion funnel analysis tool: enter visit and order data for each stage to compute the drop-off and conversion rates from impression to purchase, locate where users drop out and optimise operations; it supports batch data and runs purely in the browser.",
        "Enter transaction amount, order count and item count to compute average order value, average item price and attachment rate, for assessing e-commerce sales efficiency and cross-selling, and guiding operational improvement.",
        "Review (Data / Analysis / Improvement) Mechanism",
        "Enter GMV, order count, refund rate and customer acquisition cost period by period, compute the period-over-period GMV growth rate in chronological order, compare the period-by-period changes in refund rate and acquisition cost, automatically flag the periods that worsened, and finally give an overall review verdict of \"improving /\u2026",
        "Platform (Store Setup / Operations / Rules) Familiarity",
        "Enter the store setup costs, commissions, traffic and rule parameters of different platforms to compute and compare the operating investment and returns of each, supporting the choice of platform.",
        "Enter weighted factors such as sales, reviews and clicks to estimate a product's relative ranking and weight score in search results, as a reference for e-commerce SEO and exposure optimisation.",
        "Enter safety stock, average daily sales and the replenishment cycle to compute the reorder point and alert stock automatically and show when to restock, for e-commerce stockout prevention.",
        "Enter livestream viewer counts and order counts to compute the view-to-order conversion rate and assess livestream selling against industry benchmarks, for operational reviews.",
        "Enter enquiry or complaint volumes and response times to compute the customer service response rate and average handling time, for assessing the efficiency of an e-commerce support team.",
        "Enter the original price, discount depth, spend threshold or coupon value to compute the final price, the margin given up and the impact on profit margin, supporting the design and estimation of promotional campaigns.",
        "Compute the profit margin of a single product or a whole store from cost and selling price, with batch entry and category roll-ups, helping sellers quickly identify high-margin and loss-making products; runs purely in the browser.",
        "Enter visitor counts (UV), page views (PV) and conversions to compute the conversion rate, views per visitor and other metrics, for e-commerce traffic and conversion funnel analysis.",
        "Enter shipment volume, warehousing fees and the cost of each supply chain link to estimate the total logistics cost and unit cost after consolidation, supporting cost optimisation of e-commerce fulfilment plans.",
        "Enter the costs of each e-commerce stage (purchasing, logistics, promotion, labour) to compute total cost and cost-effectiveness, compare optimisation options and help stores cut costs and raise efficiency.",
        "Drag in metrics to generate BI reports and charts for sales, traffic and more, with filtering and roll-ups, for an e-commerce business dashboard; pure front-end visualisation with no back-end database connection.",
        "Enter order, pickup and delivery times to compute the duration of each node and the overall fulfilment time, for monitoring e-commerce logistics timeliness and comparing carrier service levels.",
        "Competitor (Monitoring / Analysis / Response) Research",
        "Competitor (Monitoring / Analysis / Response) Research is a free online e-commerce tool: it aggregates each competitor's price, monthly sales, rating and delivery lead time, computes the price range and average price, sorts by rating and marks the highest-rated and fastest-shipping ones, then suggests a differentiated competitive strategy based on your relative position. Pure front-end\u2026",
        "Record a customer's purchase history, compute the average repurchase cycle and purchase frequency, forecast the next purchase date, and segment customers automatically (one-time / regular / VIP / churned).",
        "Organise competitor prices, selling points and reviews, compute price gaps and compare strengths and weaknesses, and generate a comparison view for product selection and pricing decisions; processed purely in the browser with no data leaving your device.",
        "About \"E-commerce Tools\"",
        "The E-commerce tools collection gathers 23 free online tools covering the common calculations, conversions and lookups needed in e-commerce scenarios. Whether you are a practitioner in the field, a student or a casual user, you will find handy tools here that work the moment you open them. All tools run purely in the browser and no data is uploaded to a server, so your privacy stays safe.",
        "The e-commerce tools listed on this page include (a selection of representative tools):",
        "These tools help you finish common e-commerce tasks quickly, with no need to memorize complex formulas or convert values by hand \u2014 just enter them and get results.",
        "Do the e-commerce tools need to be downloaded or registered?",
        "No. Every e-commerce tool on this page is a pure front-end online tool \u2014 open the page and use it right away, with no software to install, no account to register, and no data uploaded.",
        "Are the e-commerce tools' results accurate? Is my data safe?",
        "The tools compute locally in your browser using public formulas and common industry standards, so results appear instantly. All calculations run on your own device and no data is uploaded to a server, keeping your privacy secure.",
    ]))

    write('inventory-1', build('inventory-1', [
        "\U0001F3EC Inventory (Alert / Replenishment) Automation",
        "Compute the reorder point, safety stock and suggested replenishment point from average daily sales and lead time.",
        "\U0001F4D6 View the \"Inventory (Alert / Replenishment) Automation Guide\"",
        "Replenishment point = average daily sales \u00d7 lead time + safety stock",
        "This tool computes the reorder point and alerts from average daily sales, replenishment lead time and safety stock, and outputs a suggested replenishment quantity.",
        "Average daily sales (units)",
        "Replenishment lead time (days)",
        "\U0001F4A1 Reorder point = average daily sales \u00d7 lead time; safety stock is taken as 30% of demand variability; suggested replenishment point = reorder point \u00d7 1.3.",
        "\U0001F4DA In-depth Analysis: Inventory (Alert / Replenishment) Automation",
        "Alerts: enter current stock and the reorder point to judge whether a replenishment alert is triggered.",
        "Replenishment quantity: enter the target days of cover to get the suggested replenishment amount.",
        "Classroom demo: reorder point = lead-time demand + safety stock.",
        "Example: daily 15, lead time 7 days, safety 50, reorder point = 155; with 120 on hand an alert fires and restocking to 30 days of cover means 450.",
        "What is the reorder point formula?",
        "= average daily sales \u00d7 lead time + safety stock; replenish when stock falls below it to prevent stockouts while keeping capital in check. " + DISCL_E,
        "How much safety stock should be set?",
        "Set it by sales volatility and lead-time uncertainty; the less stable they are the higher it should be, balancing stockouts against capital tied up. " + DISCL_E,
        "How much should I replenish?",
        "Use the target cover (say 30 days): restock to average daily sales \u00d7 30, then subtract current stock to get the replenishment quantity. " + DISCL_E,
        "About \"Inventory (Alert / Replenishment) Automation\"",
        "Inventory (Alert / Replenishment) Automation.",
        "Compute the reorder point from average daily sales and lead time",
        "Inventory alerts and reorder points",
        "Estimating replenishment from target days of cover",
        "Setting safety stock",
        "Balancing stockouts against capital tied up",
        "Alert",
        "Replenishment",
    ]))


if __name__ == '__main__':
    main()
