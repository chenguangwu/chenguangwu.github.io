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
    # ---------------- area-power (20) ----------------
    write('area-power', build('area-power', [
        "📐 Aerator (Power / Area) Sizing",
        "Estimate the required aerator power and unit count from pond area, water depth, species and the target dissolved oxygen increase.",
        "Core formulas (by input variable): iv.area×iv.depth×666.67×iv.delta×0.001×iv.coef; Math.ceil(power÷iv.unitpw)",
        "📖 Read the \"Aerator (Power / Area) Sizing User Guide\"",
        "💡 Formula: oxygen demand (kg) = area × depth × 666.67 × dissolved oxygen increase × 0.001 × species coefficient; required power (kW) = oxygen demand × oxygen transfer efficiency (1.5 kgO₂/kW·h); unit count = power ÷ power per unit (rounded up).",
        "📚 Deep dive: Aerator (Power / Area) Sizing",
        "When building or renovating a grow-out pond, size the total aerator power and unit count from the water surface area, depth and cultured species.",
        "High-density culture (such as shrimp or yellow catfish) has a high night-time dissolved oxygen risk in summer, so the aeration capacity must be verified as sufficient.",
        "Growers compare the water surface area covered per unit power of different models such as paddlewheel, water wheel and micro-bubble aeration.",
        "Sizing paddlewheel aerators for a 10-mu intensive carp pond",
        "For an intensive carp and crucian carp pond estimated at 0.5 kW per mu, 10 mu needs about 5 kW total. Choosing a 1.5 kW paddlewheel aerator gives unit count = 5 / 1.5 ≈ 3.3, rounded up to 4 units (allowing for standby and zoned placement). High-density or shrimp ponds can be raised to 0.6~0.75 kW per mu.",
        "How many kilowatts of aeration per mu are appropriate?",
        "The empirical value for ordinary intensive fish ponds is 0.3~0.5 kW per mu; high-oxygen-consumption species such as Pacific white shrimp or yellow catfish, and high-density culture, can be raised to 0.6~0.75 kW per mu. In practice it should also be judged together with water depth, water exchange conditions and night-time aeration duration.",
        "How to choose between paddlewheel, water wheel and micro-bubble aeration?",
        "Paddlewheel units have strong lift and upper/lower water exchange, suiting deep-water main-culture fish ponds; water wheel units drive circulation and aerate evenly, suiting shallow shrimp and crab ponds; micro-bubble aeration produces fine bubbles with high oxygen utilization but needs a matching blower, suiting high-level ponds and indoor recirculating water systems.",
        "Pond area (mu)",
        "Average water depth (meters)",
        "Cultured species",
        "Target dissolved oxygen increase",
        "Power per aerator unit",
    ]))

    # ---------------- density-7 (19) ----------------
    write('density-7', build('density-7', [
        "🚚 Transport (Density / Aeration) Survival Rate",
        "Estimate live fish transport survival rate, risk level and recommended density from transport time, water temperature, loading density and average fish weight.",
        "Core formulas (by input variable): min(max(iv.weight÷100,0.5),2.0); max(iv.density÷100,0.3)",
        "📖 Read the \"Transport (Density / Aeration) Survival Rate User Guide\"",
        "💡 Formula: risk index = transport time × temperature coefficient × density coefficient × body size coefficient; survival rate = 100 − risk index × correction value (0.5); recommended density = 1000 ÷ (time × temperature coefficient × body size coefficient) (corresponding to 95% survival).",
        "📚 Deep dive: Transport (Density / Aeration) Survival Rate",
        "Before long-distance transport of fry or adult fish, estimate the loading density and whether continuous aeration or cooling is needed, to avoid oxygen depletion deaths en route.",
        "Live fish delivery companies set loading and aeration standards for different seasons according to transport distance and water temperature.",
        "Compare the allowable density difference between oxygen-filled sealed bags and open fish baskets.",
        "Estimating loading density for 4 hours at 18°C with grass carp fry",
        "Grass carp fry at 50 g average weight, water temperature 18°C, transport 4 hours: metabolism is lower at low temperature, and open fish baskets allow about 200~250 kg/m³; with sealed oxygen-filled bags and ice cooling to 12°C, density can be raised to 300~400 kg/m³. Beyond 6 hours or water temperature >25°C, the density must be lowered and aeration increased.",
        "Is a lower transport density always better?",
        "Not necessarily. Too low a density means a small water volume, and water quality fluctuations and fish collision stress become larger instead; the economic density should be chosen while ensuring dissolved oxygen and ammonia stay controllable. Generally short hauls use 200~300 kg/m³, and longer hauls with temperature control and oxygen can go higher; adjust for species and water temperature.",
        "How to judge oxygen depletion risk during transport?",
        "Watch for fish surfacing, frantic swimming, darkened body color and gathering at the surface with rapid breathing - these are signs of oxygen depletion. Prevention relies on controlling density, continuous aeration (pure oxygen is better), cooling to lower metabolism, and periodic water exchange or topping up with fresh water on long hauls.",
        "Transport time (hours)",
        "Water temperature (Celsius)",
        "Loading density",
        "Average fish weight",
    ]))

    # ---------------- frequency-9 (21) ----------------
    write('frequency-9', build('frequency-9', [
        "📡 Feeding (Frequency / Particle Size) Optimization",
        "Compute the daily feeding rate, daily feed amount, recommended feeding frequency and feed particle size from average fish weight, water temperature, species and stock biomass.",
        "Core formulas (by input variable): rate÷100×iv.biomass; rate÷100×1000",
        "📖 Read the \"Feeding (Frequency / Particle Size) Optimization User Guide\"",
        "💡 Formula: daily feeding rate = base feeding rate × temperature correction coefficient × species coefficient; daily feed amount = daily feeding rate × stock biomass; feeding frequency and feed particle size are looked up in a table by fish size.",
        "📚 Deep dive: Feeding (Frequency / Particle Size) Optimization",
        "Farmers set the daily feed amount from stock biomass and water temperature, avoiding overfeeding that ruins water quality or underfeeding that slows growth.",
        "Switch feed particle size and feeding frequency across growth stages (fry / adult fish).",
        "Manage the difference in",
        "feeding rate",
        "between summer high temperatures and spring low temperatures, reducing waste and water quality pressure.",
        "Estimating daily feeding for 1000 kg of grass carp at 25°C and 200 g average weight",
        "A water temperature of 25°C is in the optimal range, where the grass carp feeding rate is about 2.5%~3%; daily feed amount = 1000 kg × 3% = 30 kg. Feed 3~4 times a day (morning, noon and evening), choosing a 3~4 mm particle size to match the mouth size; if the temperature drops below 15°C, the feeding rate should fall to within 1% and the frequency should be reduced.",
        "How do you adjust the feeding rate when the temperature changes?",
        "Most warm-water fish feed actively at 20~30°C, where the feeding rate is 2%~4%; below 15°C digestive capacity drops, so it should fall to about 1% or be fed every other day; below 10°C most species stop feeding. During rainy or overcast days and around oxygen depletion, the amount should also be reduced or feeding stopped.",
        "How do you choose the feed particle size?",
        "The particle size should be one the fish can swallow comfortably, generally about 1/4~1/3 of body length or per the species size table (e.g. grass carp at 50 g uses 1.5~2 mm, at 200 g uses 3~4 mm, at 500 g uses 4~5 mm). Too large is hard to swallow and too small creates wasteful dust, so the size should be stepped up as the fish grow.",
        "Average fish weight",
        "Water temperature (Celsius)",
        "Cultured species",
        "Total stock biomass",
    ]))


if __name__ == '__main__':
    main()
