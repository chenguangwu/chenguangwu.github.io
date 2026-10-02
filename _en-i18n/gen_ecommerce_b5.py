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
    write('stats-flow-conversion', build('stats-flow-conversion', [
        "\U0001F4A7 Traffic (UV / PV / Conversion) Statistics",
        "UV / PV / Conversion",
        "\U0001F4D6 View the \"Traffic (UV / PV / Conversion) Statistics Guide\"",
        "Conversion rate = conversions \u00f7 UV; visitor depth = PV \u00f7 UV; sales = conversions \u00d7 average order value",
        "Enter a site's UV, PV, conversions and average order value to quickly estimate the traffic conversion rate, visitor browsing depth and expected sales, supporting operational assessment.",
        "UV (unique visitors)",
        "PV (page views)",
        "Conversions",
        "Average order value (\u00a5, optional)",
        "\U0001F4DA In-depth Analysis: Traffic (UV / PV / Conversion) Statistics",
        "Traffic quality: enter UV and PV to compute pages per visitor (PV/UV) and the bounce rate.",
        "Conversion assessment: enter orders and UV to compute the UV",
        "conversion rate",
        "Classroom demo: PV/UV reflects how deeply the content engages visitors.",
        "Example: UV 5000, PV 20000, orders 150 gives 4 pages per visitor and a UV conversion rate of 3%.",
        "What is the difference between UV and PV?",
        "UV counts unique visitors and PV counts page views; a higher PV/UV means visitors stay longer and browse deeper. " + DISCL_E,
        "What about a high bounce rate?",
        "Leaving after a single page means the landing page is unappealing or slow to load, so optimise the first screen and its relevance. " + DISCL_E,
        "Should conversion be measured on UV or PV?",
        "Measuring conversion on UV is more stable, since a visitor with several pages counts once, and it avoids inflation from PV. " + DISCL_E,
        "About \"Traffic (UV / PV / Conversion) Statistics\"",
        "Traffic (UV / PV / Conversion) Statistics.",
        "Compute depth and conversion rate from UV and PV",
        "Traffic quality and bounce rate analysis",
        "UV conversion rate assessment",
        "Diagnosing how deeply content engages",
        "Optimising landing page hand-off",
    ]))

    write('stats-profit', build('stats-profit', [
        "\U0001F4B0 Profit Margin (Product / Store) Statistics",
        "Product / Store",
        "\U0001F4D6 View the \"Profit Margin (Product / Store) Statistics Guide\"",
        "Gross profit = revenue \u2212 cost; net profit = revenue \u2212 cost \u2212 expenses \u2212 taxes; gross margin = gross profit / revenue; net margin = net profit / revenue",
        "Enter the sales, purchase cost, operating expenses and taxes of a product or a store to quickly estimate gross profit, net profit and the corresponding margins, with an optional units-sold figure for per-product profit.",
        "Sales / revenue (\u00a5)",
        "Cost of sales (\u00a5)",
        "Operating expenses (\u00a5)",
        "Taxes (\u00a5)",
        "Units sold (optional)",
        "Compute profit",
        "\U0001F4DA In-depth Analysis: Profit Margin (Product / Store) Statistics",
        "Profit accounting: enter sales and each expense item to compute",
        "Product comparison: enter several SKUs and rank them to find the high- and low-margin products.",
        "Classroom demo: net margin = (gross profit \u2212 expenses \u2212 refunds) / revenue.",
        "Example: sales 100000, purchases 50000, promotion 15000, commission 5000, logistics 8000 gives net profit 22000 and a net margin of 22%.",
        "Gross or net profit?",
        "Gross profit deducts direct costs, while net profit also deducts promotion, commission, logistics, refunds and taxes; at store level net profit is the truer figure. " + DISCL_E,
        "Are refunds an expense?",
        "Refunds reduce revenue and usually carry a shipping loss, so they must be included or profit looks inflated. " + DISCL_E,
        "What if a product is loss-making?",
        "Traffic-driver products are often loss-making, acquiring customers at a loss, and are offset by profit products; the mix as a whole only needs to be profitable, so judge each product by its role. " + DISCL_E,
        "About \"Profit Margin (Product / Store) Statistics\"",
        "Profit Margin (Product / Store) Statistics.",
        "Compute gross and net profit across all costs",
        "Profit accounting per product and per store",
        "Ranking profit across multiple SKUs",
        "Combining traffic drivers with profit products",
        "Estimating the impact of refunds on profit",
    ]))

    write('wuliu-fahuo-cangchu-gongyinglian-zhenghe', build('wuliu-fahuo-cangchu-gongyinglian-zhenghe', [
        "\U0001F69A Logistics (Shipping / Warehousing / Supply Chain) Consolidation",
        "Compute the warehousing cost per order and per ten thousand orders from the shipment count and warehousing cost.",
        "\U0001F4D6 View the \"Logistics (Shipping / Warehousing / Supply Chain) Consolidation Guide\"",
        "Logistics consolidation = route optimisation",
        "This tool computes logistics consolidation cost and timeliness from shipment volume, warehouse turnover and fulfilment lead time, supporting supply chain coordination and warehouse network optimisation.",
        "Shipments",
        "Monthly warehousing cost (\u00a5)",
        "\U0001F4A1 Warehousing cost per order = warehousing cost \u00f7 shipments; cost per ten thousand orders = per-order cost \u00d7 10000; used to assess the value of integrated warehousing and delivery.",
        "\U0001F4DA In-depth Analysis: Logistics (Shipping / Warehousing / Supply Chain) Consolidation",
        "Warehouse network optimisation: enter each warehouse's coverage and cost to compare the total fulfilment cost of a single warehouse against distributed warehouses.",
        "Timeliness assessment: enter the time from dispatch to delivery to compute the average and the on-target rate.",
        "Classroom demo: shipping from the nearest warehouse cuts both lead time and freight.",
        "Example: a single warehouse shipping nationwide averages 3.5 days with freight at 8%; with forward warehouses it averages 2 days and freight 6%, cutting both time and cost.",
        "Is distributed warehousing worth it?",
        "Distributed warehouses cut lead time but add rent and inventory, so it pays off only in high-velocity regions and raises costs where sales are slow. " + DISCL_E,
        "How is turnover calculated?",
        "Inventory turnover = cost of goods sold / average inventory; a higher figure means better capital efficiency, though too low a stock level risks stockouts. " + DISCL_E,
        "What makes consolidation hard?",
        "Connecting and aligning data across OMS, WMS and TMS systems is the key, since inconsistent definitions make optimisation difficult. " + DISCL_E,
        "About \"Logistics (Shipping / Warehousing / Supply Chain) Consolidation\"",
        "Logistics (Shipping / Warehousing / Supply Chain) Consolidation.",
        "Compute logistics consolidation cost and fulfilment lead time",
        "Comparing fulfilment cost for single and distributed warehouses",
        "Warehouse network coverage optimisation",
        "Assessing inventory turnover efficiency",
        "Monitoring supply chain coordination timeliness",
        "Shipping",
        "Warehousing",
    ]))

    write('wuliu-lanshou-qianshou-shixiao', build('wuliu-lanshou-qianshou-shixiao', [
        "\U0001F69A Logistics (Pickup / Delivery) Timeliness",
        "Compute the delivery rate, in-transit parcels and the undelivered share from pickup and delivery counts.",
        "\U0001F4D6 View the \"Logistics (Pickup / Delivery) Timeliness Guide\"",
        "Logistics timeliness = pickup-to-delivery duration",
        "This tool computes logistics timeliness and the overdue rate from pickup, transit and delivery times, supporting carrier assessment and timeliness monitoring.",
        "Parcels picked up",
        "Parcels delivered",
        "\U0001F4A1 Delivery rate = parcels delivered \u00f7 parcels picked up \u00d7 100%; in-transit parcels = picked up \u2212 delivered; a delivery rate below 95% means the last leg needs checking.",
        "\U0001F4DA In-depth Analysis: Logistics (Pickup / Delivery) Timeliness",
        "Timeliness assessment: enter pickup and delivery times to compute the fulfilment duration and the overdue rate.",
        "Carrier comparison: enter the on-time rate for several carriers and pick the more reliable one.",
        "Classroom demo: break the journey into legs (pickup \u2192 line haul \u2192 last mile) to locate the slow point.",
        "Example: picked up at T0 and delivered at T+2.5 days gives a fulfilment time of 2.5 days; against a promised 3 days it is on target, and the overdue rate is the share of parcels exceeding 3 days.",
        "How is timeliness calculated?",
        "= delivery time \u2212 pickup or order time; judge overdue against the promised duration and inspect leg by leg for the bottleneck. " + DISCL_E,
        "Does the overdue rate matter?",
        "Overdue deliveries hurt the experience and drive refunds; they are central to carrier assessment and need continuous monitoring rather than a one-off check. " + DISCL_E,
        "Who is responsible when pickup is slow?",
        "Slow pickup usually lies with the merchant's dispatch or the local depot, while slow line haul lies with the carrier; assign responsibility before fixing it. " + DISCL_E,
        "About \"Logistics (Pickup / Delivery) Timeliness\"",
        "Logistics (Pickup / Delivery) Timeliness.",
        "Compute logistics timeliness and the overdue rate",
        "Assessing fulfilment duration and overdue rate",
        "Comparing on-time rates across carriers",
        "Locating slow points leg by leg",
        "Evaluating carrier service quality",
        "Pickup",
        "Delivery",
    ]))


if __name__ == '__main__':
    main()
