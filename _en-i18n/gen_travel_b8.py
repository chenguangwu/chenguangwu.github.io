#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'travel')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'travel')
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
    out = {'slug': slug, 'industry': 'travel', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('travel-insurance-comparison', build('travel-insurance-comparison', [
        "\U0001F6E1\ufe0f Travel Insurance Comparison Assistant",
        "Compare the coverage and price of different types of travel insurance against your travel needs",
        "\U0001F3AF Smart Recommendations",
        "\U0001F4CA Detailed Comparison",
        "\U0001F4D6 Buying Guide",
        "Destination Type",
        "\U0001F30F Asia Nearby",
        "\U0001F30D Europe / Schengen",
        "\U0001F30E Americas / Long Haul",
        "\U0001F3D4\ufe0f Outdoor / High Risk",
        "Coverage Focus",
        "Economical Basic",
        "Medical Priority",
        "Comprehensive Coverage",
        "Age Bracket",
        "18-50 (standard)",
        "51-65 (+20%)",
        "66-75 (+50%)",
        "Over 75 (+100%)",
        "Includes High-risk Sports",
        "Mild (diving / hiking)",
        "Extreme (skiing / mountaineering)",
        "Flight Delay Coverage",
        "Basic (CNY 500)",
        "High (CNY 1500)",
        "\U0001F4CA Detailed Comparison of Coverage Liability",
        "\U0001F4DC Past Plans",
        "\U0001F4CB Main Coverage Items of Travel Insurance",
        "Accidental death or disability:",
        "A lump-sum payout for death or disability caused by an accident",
        "Medical expenses:",
        "Medical costs from illness or accident during the trip (including outpatient and inpatient care)",
        "Emergency medical evacuation:",
        "The cost of urgent evacuation back home or to a better hospital",
        "Flight delay:",
        "Compensation when a flight is delayed beyond the agreed time (usually 4 to 6 hours)",
        "Lost or delayed baggage:",
        "Compensation when checked baggage is lost or delayed beyond the agreed time",
        "Trip cancellation or shortening:",
        "Compensation for costs when a trip is cancelled or shortened due to force majeure",
        "Personal liability:",
        "Compensation for third-party injury or property damage caused by an accident",
        "Bank card fraud:",
        "Compensation for losses from bank card fraud during the trip",
        "\U0001F4A1 Key Buying Points",
        "Make the medical coverage sufficient:",
        "For developed countries in Europe and North America, at least CNY 500000 is advised; the Schengen visa requires no less than EUR 30000 (about CNY 250000)",
        "Read the exclusions:",
        "High-risk sports (diving, skiing, mountaineering and so on) usually need extra cover",
        "Emergency rescue service:",
        "Choose an insurer with a global rescue network, which can save your life when it matters",
        "When to buy:",
        "Buying 1 to 2 weeks before departure is advised; trip cancellation insurance needs an even earlier start",
        "Disclose truthfully:",
        "Pre-existing conditions must be disclosed, otherwise the claim may be refused",
        "Keep the receipts:",
        "Keep invoices and supporting documents for medical treatment and shopping to make claims easier",
        "\U0001F30D Destination Recommendations",
        "Suggested Medical Coverage",
        "Special Attention",
        "CNY 100,000 to 300,000",
        "Watch for coverage of tropical diseases such as dengue",
        "Japan, Korea / Hong Kong, Macao, Taiwan",
        "CNY 200,000 to 500,000",
        "Medical costs are high, so buy full coverage",
        "Europe Schengen",
        "at least CNY 300,000 (mandatory)",
        "Must satisfy the Schengen visa requirement",
        "US, Canada, Australia, New Zealand",
        "CNY 500,000 to 1,000,000",
        "Medical costs are extremely high, so high coverage is advised",
        "Africa / South America",
        "CNY 300,000 to 500,000",
        "Pay attention to disease coverage and emergency rescue",
        "Outdoor / Adventure",
        "above CNY 500,000",
        "Must include high-risk sports coverage",
        "\u26a0\ufe0f The prices and coverage above are for reference only. Actual coverage, exclusions and prices follow the insurer's official terms. Please read the insurance contract carefully before buying.",
        "\U0001F4DA In-Depth Analysis: Travel Insurance Comparison",
        "Destination Selection",
        "Age and Sports Factors",
        "Medical Coverage Thresholds",
        "Europe, 7 Days, Age 30",
        "factor = max(0.5, 7 \u00f7 7) = 1, so the base plan basePrice[200, 400] \u00d7 1 \u00d7 ageMult \u00d7 sportMult = CNY 200 to 400. Schengen requires medical coverage of at least EUR 30000 (about CNY 250000), so pick a compliant plan.",
        "High-risk Sports Surcharge",
        "Choosing skiing raises sportMult, and with the high delay tier the delay payout is \u00d7 1.5; use the comparison tab to find the smallest minTotal.",
        "How do prices change?",
        "basePrice \u00d7 duration factor \u00d7 age factor \u00d7 sport factor. The longer the trip (days \u00f7 7), the more expensive it gets.",
        "Any Schengen caveats?",
        "European plans need medical coverage of at least EUR 30000, otherwise the visa may be refused.",
        "About \"Travel Insurance Comparison Assistant\"",
        "Travel Insurance Comparison Assistant. A travel tool that is essential for trips and works offline.",
    ]))
    write('visa-requirement-checker', build('visa-requirement-checker', [
        "\u2705 Visa Requirement Checker (Chinese Passport)",
        "Look up visa requirements for holders of ordinary Chinese passports travelling to various countries and regions (for reference only; official sources prevail)",
        "Visa Requirement Checker",
        "/ Visa Requirement Checker",
        "\U0001F30D Browse",
        "\U0001F5FA\ufe0f By Region",
        "\U0001F4CA Statistics Overview",
        "\U0001F4A1 Visa Tips",
        "\u2705 Visa Free",
        "\U0001F6EC Visa on Arrival",
        "\U0001F4F1 e-Visa",
        "\U0001F4CB Visa Required",
        "\U0001F5FA\ufe0f Browse by Region",
        "\U0001F4CA Visa Type Statistics",
        "\U0001F30D Total Countries / Regions",
        "\U0001F4C8 Visa Convenience Ranking (by visa-free plus visa-on-arrival count)",
        "\U0001F4CB Visa Type Descriptions",
        "Visa Free:",
        "No visa application needed in advance; entry with a valid passport, usually subject to a stay limit",
        "Visa on Arrival:",
        "The visa is issued at the airport or port of entry after arrival; photos, cash and similar are usually required",
        "e-Visa / ETA:",
        "Applied for online in advance, usually issued in 1 to 3 working days with no need to mail your passport",
        "Visa Required:",
        "A sticker visa must be applied for at the embassy or consulate in advance, possibly requiring an invitation letter or proof of assets",
        "\U0001F4A1 Visa Application Tips",
        "Plan ahead:",
        "Peak season visas for popular countries may take 1 to 2 months, so apply early",
        "Prepare documents:",
        "Check the required documents carefully, make sure photos meet the spec and that your bank balance is sufficient",
        "Itinerary:",
        "Prepare round-trip flight bookings, hotel bookings and a detailed itinerary",
        "Insurance:",
        "The Schengen visa requires medical coverage of at least EUR 30000, so buy travel insurance that meets the requirement",
        "Multiple-entry visas:",
        "Frequent travelers can apply for multi-year multiple-entry visas to save time and cost",
        "Passport validity:",
        "Most countries require at least 6 months of passport validity",
        "Blank pages:",
        "Make sure your passport has at least 2 to 3 blank visa pages",
        "Transit visas:",
        "Some countries require a transit visa even when you do not leave the airport",
        "Visa-free conditions:",
        "Some visa-free countries require a valid US, Canadian or Schengen visa",
        "Entry inspection:",
        "Even with a visa you may be refused entry, so have proof of itinerary ready",
        "\u26a0\ufe0f The information above is for reference only, and visa policies may change at any time. Before travelling, check the latest information on the destination country's embassy or consulate official website, or consult a professional visa agency.",
        "\U0001F4DA In-Depth Analysis: Visa Lookup for Chinese Passports",
        "Visa Free / On Arrival",
        "ETA / Visa Required",
        "Regional Statistics",
        "Thailand / Japan / United States",
        "Chinese passport: Thailand free (visa free), Japan eta or on-arrival, United States required with an interview; the list badges each type with its stay limit.",
        "Statistics View",
        "Convenience = (free + arrival count) \u00f7 total",
        ". A region with at least 70% easy is marked green, making destination choices easier.",
        "Is the data authoritative?",
        "This is a built-in reference table. Visa policies change frequently, so check embassy or consulate announcements before travelling.",
        "Are the stay limits accurate?",
        "Common visa-free and on-arrival stay limits are listed; for special groups or document requirements, official sources prevail.",
        "About \"Visa Requirement Checker\"",
        "Visa Requirement Checker. A travel tool that is essential for trips and works offline.",
        "\U0001F50D Search for a country or region...",
    ]))


if __name__ == '__main__':
    main()