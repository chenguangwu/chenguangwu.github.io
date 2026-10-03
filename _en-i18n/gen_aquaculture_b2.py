#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'aquaculture')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'aquaculture')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    return mp


def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'aquaculture', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # ---------------- fuhua-shuiliu-rongyang-tiaojian (20) ----------------
    write('fuhua-shuiliu-rongyang-tiaojian', build('fuhua-shuiliu-rongyang-tiaojian', [
        "🐟 Hatching (Water Flow / Dissolved Oxygen) Conditions",
        "Compute the water exchange rate from hatchery bucket volume, inflow rate, target dissolved oxygen, inflow dissolved oxygen and egg count, and judge whether the dissolved oxygen is sufficient.",
        "Core formulas (by input variable): iv.flow×(iv.target-iv.inflow)×60÷1000; iv.flow×60÷iv.vol; iv.eggs×0.001",
        "📖 Read the \"Hatching (Water Flow / Dissolved Oxygen) Conditions User Guide\"",
        "💡 Formula: exchange rate (times/h) = inflow rate × 60 ÷ volume; dissolved oxygen supply (g/h) = inflow rate × (target dissolved oxygen − inflow dissolved oxygen) × 60 ÷ 1000; oxygen demand (g/h) = egg count × 0.001.",
        "📚 Deep dive: Hatching (Water Flow / Dissolved Oxygen) Conditions",
        "A hatchery designs the inflow rate of the hatching bucket to ensure sufficient dissolved oxygen during embryo development and timely removal of metabolic waste.",
        "Troubleshoot low hatching rates (insufficient water flow, inadequate dissolved oxygen, excessive egg density).",
        "Compare the differences in hatching water flow and dissolved oxygen requirements between the four major Chinese carps and cold-water fish.",
        "Verifying dissolved oxygen with a 0.5 m³ bucket and 30 L/min inflow",
        "Exchange rate = 30 L/min × 60 / 500 L = 3.6 times per hour. With inflow dissolved oxygen of 8 mg/L and embryo consumption bringing the outflow down to about 6.5 mg/L, this is still above the 5~6 mg/L safety line, so it is judged sufficient; if the egg count doubles and raises consumption so the outflow approaches 4 mg/L, the flow rate must be raised above 50 L/min or extra aeration added.",
        "What is the minimum dissolved oxygen for hatching water?",
        "Fish embryos consume a lot of oxygen during development, so the hatching water generally requires dissolved oxygen ≥ 5~6 mg/L, and the outflow end of a raceway or hatching bucket should not fall below 4 mg/L. Below this, embryo development slows and deformity and mortality increase, so the inflow rate should be increased or aeration added to maintain it.",
        "What water exchange rate is appropriate?",
        "Hatching buckets and raceways commonly exchange 2~5 times the water volume per hour; take the upper limit when egg density is high or the water is warm. An insufficient exchange rate causes ammonia and CO₂ to accumulate and lowers dissolved oxygen, which is a common cause of falling hatching rates.",
        "Hatching bucket volume",
        "Inflow rate",
        "Target dissolved oxygen",
        "Inflow dissolved oxygen",
        "Egg count",
    ]))

    # ---------------- hardness-water-quality (20) ----------------
    write('hardness-water-quality', build('hardness-water-quality', [
        "🐟 Water Quality (Total Alkalinity / Hardness) Adjustment",
        "Enter the current total alkalinity, target total alkalinity and water volume to compute the amount of sodium bicarbonate or lime to add.",
        "Core formulas (by input variable): diff×iv.vol÷1000; adjust×0.84; adjust×0.56",
        "📖 Read the \"Water Quality (Total Alkalinity / Hardness) Adjustment User Guide\"",
        "💡 Formula: adjustment amount (kg, expressed as CaCO₃) = (target value − current value) × volume ÷ 1000; sodium bicarbonate amount = adjustment amount × 0.84; lime (CaO) amount = adjustment amount × 0.56.",
        "📚 Deep dive: Water Quality (Total Alkalinity / Hardness) Adjustment",
        "When the total alkalinity of a pond or nursery water body is low, compute the sodium bicarbonate or lime dose to stabilize pH and strengthen buffering.",
        "Shrimp and crab culture (sensitive to hardness) adjusts calcium and magnesium hardness to promote molting and shell formation.",
        "Restorative calcium and alkalinity supplementation after heavy rain turns the water acidic and drops the alkalinity sharply.",
        "Computing baking soda for 1000 m³ of water with alkalinity 40→100 mg/L",
        "A 60 mg/L increase is needed (expressed as CaCO₃). Baking soda NaHCO₃",
        "molecular weight",
        "is 84 and the CaCO₃ equivalent is 50, giving a conversion factor of 84/50 = 1.68, so each m³ needs 60 × 1.68 = 100.8 g, about 100.8 kg in total for 1000 m³. If hardness also needs raising, switch to lime (such as quicklime CaO) and account for calcium and magnesium separately.",
        "What is the difference between total alkalinity and total hardness, and do both need adjusting?",
        "Total alkalinity reflects the water's ability to buffer acid-base fluctuation (expressed as CaCO₃), while total hardness reflects the total of calcium and magnesium ions. For most water bodies, prioritize keeping alkalinity at 80~150 mg/L to stabilize pH; crustaceans such as shrimp and crab are sensitive to hardness (especially calcium and magnesium) and need hardness adjusted synchronously during molting. Baking soda raises alkalinity only, while lime and calcium chloride raise or lower hardness as well.",
        "How much baking soda counts as too much?",
        "Compute it from the alkalinity gap to the target and avoid a large single-dose increase (it is recommended to split doses, keep each increment within 20~30 mg/L, and monitor pH). Long-term alkalinity >300 mg/L (as CaCO₃) together with excessive hardness may upset the ion balance, so rely on measured values and supplement as needed rather than adding heavily on a fixed schedule.",
        "Current total alkalinity",
        "Target total alkalinity",
        "Water volume",
    ]))

    # ---------------- index (19) ----------------
    write('index', build('index', [
        "🐟 Aquaculture Tools",
        "Aquaculture",
        "Aquaculture Tools",
        "Hatching (Water Flow / Dissolved Oxygen) Conditions",
        "Compute the water exchange rate from hatchery bucket volume, inflow rate, target dissolved oxygen, inflow dissolved oxygen and egg count, and judge whether the dissolved oxygen is sufficient.",
        "Enter the current total alkalinity, target total alkalinity and water volume to compute the amount of sodium bicarbonate or lime to add.",
        "Aerator (Power / Area) Sizing",
        "Enter pond area, water depth, cultured species and target dissolved oxygen increase to estimate the total aerator power and unit count, assisting aquaculture aeration equipment selection.",
        "Feeding (Frequency / Particle Size) Optimization",
        "Compute the daily feeding rate, daily feed amount, recommended feeding frequency and feed particle size from average fish weight, water temperature, species and stock biomass.",
        "Estimate live fish transport survival rate, risk level and recommended density from transport time, water temperature, loading density and average fish weight.",
        "About \"Aquaculture Tools\"",
        "The Aquaculture Tools collection gathers 5 free online tools covering the common calculation, conversion and lookup needs of aquaculture scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you will find ready-to-use utilities here. Every tool runs entirely in the browser and never uploads data to the server, so your privacy is protected.",
        "The aquaculture tools listed on this page include (a few representative tools):",
        "These tools help you finish common aquaculture tasks quickly, with no need to memorize complex formulas or do manual conversions - just enter the inputs and get the result.",
        "Do the aquaculture tools require a download or an account?",
        "No. Every tool on this page is a pure front-end online tool: open the page and use it right away, with no software to install, no account to register, and no data uploaded.",
        "Are the aquaculture tool results accurate? Is the data safe?",
        "The tools compute locally in your browser based on public mathematical formulas and general industry standards, so results are available instantly. All computation happens locally on your device and no data is uploaded to the server, so your privacy is fully protected.",
    ]))


if __name__ == '__main__':
    main()
