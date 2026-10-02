#!/usr/bin/env python3
# gen_livestock_head.py — shared head for livestock batches b1..b6
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'livestock')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'livestock')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
DISCL = "Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected."
EXTRA = {
    'disinfectant-dilution': {"稀释倍数？": "Dilution factor?"},
}
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
    out = {'slug': slug, 'industry': 'livestock', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('calving-interval', build('calving-interval', [
        "Calving interval and reproductive-efficiency evaluator",
        "Evaluate dairy/beef calving interval, open days and reproductive efficiency to guide breeding management",
        "Core formula (by inputs): new Date(breedDate.getTime() + gestation \u00d7 86400000); new Date(lastDate.getTime() + 365 \u00d7 86400000); Math.round((nextDate - lastDate) \u00f7 86400000)",
        'View "Calving interval and reproductive-efficiency evaluator" guide',
        "Last calving date",
        "This breeding date",
        "Days to first breeding after calving (days)",
        "Number of breedings",
        "Gestation (days)",
        "Expected/actual calving date",
        "Reproductive-efficiency reference metrics",
        "Calving interval (days)",
        "Open days (days)",
        "First breeding after calving (days)",
        "Breeding count (times)",
        "Conception rate (%)",
        "Calving interval is the core efficiency metric. Ideal is 365 days (one calf per year); each extra day costs about 0.05\u20130.1 kg/day of milk, sharply hurting profit.",
        "Deep dive: Calving-interval analysis",
        "From calving dates, compute interval and open days.",
        "Assess reproductive efficiency and milk loss.",
        "Back-calculate conception rate from breeding count.",
        "Interval 390 days",
        "Gestation 283 days \u2192 open 107 days; 2 breedings \u2192 50% conception; 25 days over ideal, daily milk loss 25\u00d70.07 = 1.75 kg/day.",
        "Ideal interval",
        "Interval 365 days, 1 conception \u2192 open 82 days, 100% conception, no extra milk loss.",
        "What is the ideal interval?",
        "Dairy cows do best at 12\u201313 months (365\u2013395 days).",
        "How to estimate milk loss?",
        "Each extra day loses about 0.07 kg/day; long intervals significantly cut annual yield.",
        'About "Calving interval and reproductive-efficiency evaluator"',
        "Calving interval and reproductive-efficiency evaluator. " + DISCL,
    ]))
    write('castration-timing', build('castration-timing', [
        "Tail-docking and castration age selector",
        "Recommend optimal age and method for tail docking and castration by animal type",
        'View "Tail-docking and castration age selector" guide',
        "Chicken (beak trimming)",
        "Castration",
        "Tail docking",
        "Dehorning",
        "Beak trimming",
        "Key steps and precautions",
        "Castration",
        "\u2022 Earlier: less stress, faster recovery",
        "\u2022 Fast 6\u201312 h before to prevent intestinal prolapse",
        "\u2022 Strictly disinfect tools and site; prevent post-op infection",
        "\u2022 Welfare: perform under veterinary guidance, use analgesics when needed",
        "\u2022 Leave 1/3\u20131/2 of piglet tail to prevent tail biting",
        "\u2022 Lamb dock at 3\u20134 tail joints, keep coverage over the anus",
        "\u2022 Use rubber ring or hot-docker; control bleeding and disinfect",
        "\u2022 Best dehorn calves at 2\u20136 weeks before horn bud forms",
        "\u2022 Methods: hot iron, caustic soda, or surgical removal",
        "\u2022 After dehorning, control bleeding and prevent infection",
        "Welfare is increasingly regulated; some countries restrict or ban non-therapeutic docking/castration. Minimize stress and pain, use local anesthesia and analgesics when needed.",
        "Deep dive: Castration / docking / dehorning timing",
        "By species and birth date, estimate the suitable age window for each procedure.",
        "Piglet castration and docking, calf dehorning timing.",
        "Scheduling to avoid stress and infection.",
        "Piglet castration",
        "Born 2026-01-01, castration window 3\u20137 days \u2192 2026-01-04~01-08; docking same window.",
        "Calf dehorning",
        "Born 2026-01-01, dehorn 7\u201310 days \u2192 01-08~01-11 (hot dehorning earlier).",
        "Why early?",
        "Young animals have lighter nerve/pain response, less bleeding and stress.",
        "What age window?",
        "Pig castration/docking 1\u20137 days, calf dehorning within 1\u20133 weeks, per farm rules.",
        'About "Tail-docking and castration age selector"',
        "Tail-docking and castration age selector. " + DISCL,
    ]))
    write('detector-12', build('detector-12', [
        "Feed (aflatoxin / zearalenone) test",
        "Enter mycotoxin content in feed; judge against GB 13078 whether it exceeds limits and give a risk level",
        "Core formula (by inputs): (it.val\u00f7it.limit\u00d7100)",
        'View "Feed (aflatoxin / zearalenone) test" guide',
        "Feed type",
        "Pig compound feed",
        "Poultry compound feed",
        "Ruminant feed",
        "Piglet/chick feed",
        "Aflatoxin B1 (\u00b5g/kg)",
        "Zearalenone (\u00b5g/kg)",
        "Deoxynivalenol DON (\u00b5g/kg)",
        "Ochratoxin A (\u00b5g/kg)",
        "Deep dive: Feed mycotoxin test and judgment",
        "Compare measured AFB1/ZEA/DON/OTA values against limits.",
        "Limits by animal type (pig/poultry/ruminant/young).",
        "Exceedance alerts and risk scoring.",
        "Pig feed AFB1=80",
        "Pig compound feed limit 50 \u00b5g/kg: measured 80 \u2192 160% over, prohibit and return.",
        "Just meeting the limit",
        "AFB1=50 \u2192 equal to limit 100%, marginal; control the source.",
        "What is the limit basis?",
        "Per GB 13078 feed hygiene standard, tiered by animal and toxin.",
        "Stricter for young animals?",
        "Piglets/chicks and other young animals have stricter limits; judge separately.",
        "Testing is based on GB 13078-2017 Feed Hygiene Standard; toxin limits differ by animal feed",
        "Piglet/chick feed has the strictest limits, aflatoxin B1 \u226410 \u00b5g/kg",
        "Aflatoxin B1 is a strong carcinogen; over-limit feed is strictly forbidden and must be detoxified or destroyed",
        "Zearalenone strongly affects sow fertility; over-limit can cause abortion and infertility",
        "Test each batch before storage; keep dry to prevent mold",
        'About "Feed (aflatoxin / zearalenone) test"',
        "Feed mycotoxin test tool: enter aflatoxin B1, zearalenone, DON and ochratoxin A; judge against GB 13078 whether over limit and assess risk level.",
        "Simultaneous test of four major mycotoxins",
        "Based on GB 13078-2017",
        "Auto-match limits by animal feed",
        "Disposal advice for over-limit items",
        "Feed-material intake testing",
        "Compound-feed quality acceptance",
        "Farm safety management",
        "Feed-mill quality control",
    ]))
    write('disinfectant-dilution', build('disinfectant-dilution', [
        "Disinfectant dilution calculator",
        "Compute disinfectant dilution ratio, stock volume and available chlorine concentration",
        "Core formula (by inputs): stock \u00d7 total \u00f7 dilutionRatio \u00d7 10; target \u00d7 total \u00d7 10; stockVol \u00d7 1000",
        'View "Disinfectant dilution calculator" guide',
        "Disinfectant type",
        "84 disinfectant (sodium hypochlorite)",
        "Peracetic acid",
        "Formaldehyde solution",
        "Povidone iodine",
        "Quaternary ammonium",
        "Caustic soda (sodium hydroxide)",
        "Quicklime",
        "Stock concentration (%)",
        "Target use concentration (%)",
        "Total dilution volume needed (L)",
        "Common disinfectant reference concentrations",
        "Disinfectant",
        "Sodium hypochlorite (84)",
        "Shed and equipment disinfection",
        "Fumigation, spray disinfection",
        "Fumigation disinfection",
        "Skin, wound disinfection",
        "Quaternary ammonium",
        "Environment, equipment disinfection",
        "Caustic soda",
        "Solid",
        "Empty shed, floor disinfection",
        "10\u201320% emulsion",
        "Floor, wall disinfection",
        "Do not mix disinfectants arbitrarily. Clean off organic matter first, or efficacy drops sharply. For in-animal disinfection choose low-irritation products and ventilate.",
        "Deep dive: Disinfectant dilution preparation",
        "From stock and target concentration, get volume and dilution factor.",
        "Livestock-shed and instrument disinfection mixing.",
        "Estimate active ingredient (e.g., available chlorine).",
        "10% to 0.1% for 100 L",
        "Stock volume = target\u00d7total/stock = 0.1\u00d7100/10 = 1 L, add 99 L water, dilution 1:100.",
        "Different targets",
        "Target 0.5%: stock = 0.5\u00d7100/10 = 5 L, dilution 1:20.",
        "= stock concentration / target, e.g., 10%/0.1% = 100\u00d7.",
        "Use immediately after mixing?",
        "Most diluted disinfectants are unstable; mix fresh by need.",
        'About "Disinfectant dilution calculator"',
        "The Disinfectant dilution calculator is a general-purpose online tool. " + DISCL,
    ]))
    write('dongtishouroulv-beibiaohouceding', build('dongtishouroulv-beibiaohouceding', [
        "Carcass lean rate / backfat thickness measurement",
        "From backfat, live weight, sex and species, estimate carcass lean rate (%) and grade. Regression estimate; for reference only.",
        "Core formula (by inputs): carcass\u00d7lean\u00f7100",
        "Carcass lean rate / backfat thickness measurement",
        "/ Carcass lean rate / backfat thickness measurement",
        'View "Carcass lean rate / backfat thickness measurement" guide',
        "Backfat thickness (mm)",
        "Live weight (kg)",
        "Male",
        "Castrated male",
        "Estimate: lean rate = base \u2212 backfat coeff \u00d7 backfat \u2212 weight coeff \u00d7 (live \u2212 standard) + sex correction; carcass weight = live \u00d7 dressing percentage.",
        "Carcass lean-rate grading standard",
        "Measure backfat at the 6\u20137th rib (pig) or 12\u201313th rib (cattle)",
        "This is an empirical regression estimate; actual measurement should use carcass dissection",
        "Deep dive: Carcass lean rate and backfat measurement",
        "Estimate and grade lean rate from live weight and backfat.",
        "Aid for slaughter pricing and breeding value.",
        "Judge the suitable backfat range.",
        "Pig backfat 18 mm, live 100 kg",
        "Backfat 18 mm is suitable (\u226425 suitable); live 100 kg estimates lean rate ~55%\u201358%, carcass ~72 kg, lean ~40 kg.",
        "Backfat too fat",
        "Backfat 35 mm \u2192 too fat, lean rate drops ~3\u20135 points.",
        "What is backfat grading?",
        "Pigs: \u226415 lean, 15\u201325 suitable, 25\u201335 fat, >35 over-fat.",
        "Live-weight effect?",
        "Deviation from standard weight is corrected by coefficient; overweight often slightly lowers lean rate.",
        'About "Carcass lean rate / backfat thickness measurement"',
        "For quick live or carcass lean-rate estimation. Enter backfat, live weight, sex and species; estimate lean rate by empirical regression and grade by pig/cattle/sheep, also converting carcass and lean weight.",
        "Supports pig / cattle / sheep",
        "Auto rating and backfat evaluation",
        "Includes grading standard reference table",
        "Pre-slaughter lean-rate prediction for pigs",
        "Beef carcass quality grading",
        "Breeding selection by backfat screening",
        "Slaughter and processing pricing reference",
        "Backfat thickness",
        "Live weight",
    ]))

if __name__ == "__main__":
    main()
