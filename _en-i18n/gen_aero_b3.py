#!/usr/bin/env python3
# aerospace batch3 (5 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'aerospace')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'aerospace')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'delta-v-rocket': [
"Tsiolkovsky Rocket Equation",
"/ Rocket Delta-v",
"Rocket Delta-v",
'📖 View the "Tsiolkovsky Rocket Equation Guide"',
"Specific impulse Isp (s)",
"Initial mass (kg)",
"Final mass (kg)",
"The larger the mass ratio, the larger Δv.",
"Multi-stage rockets raise the effective mass ratio.",
"📚 In-Depth Analysis: Tsiolkovsky Rocket Equation",
"Single-stage ",
"Given a target Δv (such as about 9.4 km/s for orbit insertion), back-calculate the required mass ratio or specific impulse.",
"Assess whether an upper stage can place the payload into the target orbit.",
"Single-stage orbit-insertion velocity increment",
"specific impulse Isp",
"=300 s, initial mass m0=500 t and final mass mf=100 t. Δv = 300×9.81×ln(500/100) = 2943×ln(5) = 2943×1.609 ≈ 4733 m/s ≈ 4.73 km/s. A single stage is far from enough for orbit insertion, so multi-stage staging is needed.",
"Why is a single-stage rocket so hard to put into orbit?",
"Orbit insertion needs Δv≈9.4 km/s (more with gravity/drag losses). By the formula, Δv grows logarithmically with the mass ratio, so raising 4.7 to 9.4 would require the mass ratio to go from 5 to 25, which the structure can hardly bear, hence the use of multiple stages that drop shells one by one.",
"Which gravity is g0?",
"The standard gravitational acceleration 9.80665 m/s², used only as the ",
" constant for converting Isp (seconds) to exhaust velocity, and unrelated to the actual g at the launch site.",
],
'wing-loading': [
"Weight / Wing Area",
"Wing loading = W / S.",
"Wing loading W/S",
"/ Wing Loading",
"Wing loading",
'📖 View the "Weight / Wing Area Guide"',
"Wing loading = weight W ÷ wing area S, commonly in N/m² and kgf/m², with 1 kgf/m² = 9.80665 N/m²; estimate the stall speed V = sqrt(2×(W÷S) ÷ (ρ×CL_max)), taking air density ρ = 1.225 kg/m³ and maximum lift coefficient CL_max = 1.2.",
"High wing loading leads to high speed and low manoeuvrability.",
"Fighters have higher wing loading than gliders.",
"📚 In-Depth Analysis: Weight / Wing Area",
"Compute the wing loading W/S from weight W and wing area S, a compact characterisation of aircraft performance.",
"Compare the wing loading of different types to forecast takeoff/landing distance and manoeuvrability.",
"Assess how the wing-loading change after a weight increase (added equipment) affects performance.",
"Transport aircraft wing loading",
"Weight W=600000 N and wing area S=200 m², so wing loading W/S=3000 N/m² (≈306 kg/m²). This value is in the typical transport range, balancing takeoff/landing performance and cruise efficiency.",
"How does wing loading relate to the ",
"?",
"From the stall formula Vs=√(2W/(ρS·C_Lmax))=√(2·(W/S)/(ρ·C_Lmax)), the higher the wing loading the greater the stall speed and the longer the takeoff/landing distance. Carrier aircraft and trainers therefore deliberately use low wing loading.",
"Why use wing loading instead of looking at area directly?",
"Area alone cannot show how heavy a plane is for its size; dividing by weight (wing loading) reflects the load carried per unit wing area, is comparable across types and is one of the key non-dimensional aerodynamic and performance design indices.",
],
'wing-area-from-loading': [
"Required Wing Area from Weight and Wing Loading",
"Enter weight W and wing loading W/S to find the wing area.",
"Wing Area from Wing Loading Calculator",
"/ Wing Area from Wing Loading Calculator",
'📖 View the "Required Wing Area from Weight and Wing Loading Guide"',
"Wing loading W/S (N/m²)",
"Wing loading affects takeoff/landing and manoeuvrability.",
"📚 In-Depth Analysis: Required Wing Area from Weight and Wing Loading",
"In preliminary design, from the design weight W and the target ",
"wing loading W/S",
" back-calculate the required wing area S=W/(W/S).",
"Compare the area and the structure/performance trade-offs of different wing-loading options.",
"Given a limited wing area (such as wingspan/stand size), back-calculate the achievable wing loading.",
"Preliminary-design wing area",
"Design weight W=600000 N and target wing loading W/S=3000 N/m². Required area S=600000/3000=200 m². When the area is too large and limited by wingspan/stand size, wing loading must be raised (sacrificing low-speed performance) or weight reduced.",
"Is high or low wing loading better?",
"Low wing loading (large wing area) gives a low ",
", good manoeuvrability/takeoff-landing performance, but high induced drag and a heavy structure; high wing loading gives good cruise efficiency but a long takeoff/landing distance. Trade off by mission (low for fighters, high for bombers).",
"Should wing loading use weight or mass?",
"Aviation usually uses W/S (force/area, N/m²) because it directly relates to the lift = weight balance. If mass/area (kg/m²) is used, multiply by g to convert, and watch the unit consistency.",
],
'thrust-to-weight': [
"Thrust-to-Weight Ratio from Thrust and Weight",
"Enter thrust T and weight W to find the thrust-to-weight ratio.",
"T/W = Thrust / Weight",
"/ Thrust-to-Weight Calculator",
"Thrust-to-Weight Calculator",
'📖 View the "Thrust-to-Weight Ratio from Thrust and Weight Guide"',
"Thrust-to-weight ratio = T/W",
"Thrust T (N)",
"T/W>1 is needed to climb and take off vertically.",
"📚 In-Depth Analysis: Thrust-to-Weight Ratio from Thrust and Weight",
"Compute the thrust-to-weight ratio T/W from thrust T and weight W to measure acceleration/climb capability.",
"Compare the thrust-to-weight ratios of different aircraft (airliners/fighters) to assess manoeuvrability and takeoff performance.",
"Given a target thrust-to-weight ratio, back-calculate the required engine thrust or the weight-reduction target.",
"Transport aircraft thrust-to-weight ratio",
"Thrust T=120000 N (both engines combined) and weight W=600000 N. Thrust-to-weight ratio T/W=120000/600000=0.2. A transport is well served by 0.2-0.4; fighters are often >0.9 or even >1 for super-manoeuvrability.",
"What does a thrust-to-weight ratio greater than 1 mean?",
"Thrust exceeds weight, so in theory it can accelerate vertically (such as fighters/rockets), with super-manoeuvrability and short takeoff capability. Airliners have a thrust-to-weight ratio far below 1 and rely on ",
" rather than thrust to support their weight.",
"Is the static thrust-to-weight ratio the same as in flight?",
"No. The static thrust-to-weight ratio computed from the sea-level maximum static thrust of the engine is the highest; as thrust varies with speed/altitude, the actual ratio in flight changes. Performance assessment uses the value for the relevant operating condition.",
],
'climb-rate': [
"Excess power determines the rate of climb.",
"Rate of Climb (ROC)",
"/ Rate of Climb",
"Rate of climb",
'📖 View the "Rate of Climb (ROC) Guide"',
"ROC=0 (level-flight limit).",
"Available power (W)",
"Required power (W)",
"The greater the excess power, the faster the climb.",
"At rest ROC=0 (level-flight limit).",
"📚 In-Depth Analysis: Rate of Climb (ROC)",
"In performance accounting, compute the rate of climb ROC=(Pa−Ps)/W from the difference between available power Pa and required power Ps and the weight W.",
"Judge whether an aircraft can climb on a specified obstacle-clearance gradient, used for takeoff obstacle assessment.",
"Compare the rate of climb at different altitudes (power falls with altitude) to find the best climb speed.",
"Rate of climb from the available-power surplus",
"Available power Pa=2000 kW, required power Ps=1800 kW and weight W=600000 N. Power surplus=200000 W, ROC = 200000/600000 = 0.333 m/s = 1200 m/h. That is, it rises about 0.33 metres per second.",
"How do I convert the ft/min commonly seen for rate of climb?",
"1 m/s = 196.85 ft/min. In the example above 0.333 m/s ≈ 65.6 ft/min (an illustrative low value; a real transport is about 1000-2500 ft/min). Note that Pa and Ps use the same unit (watts) and W uses newtons, so the result is in m/s.",
"Why does the rate of climb fall at high altitude?",
"Engine power/thrust drops as air density falls while the required power rises with the true speed, so the available surplus is squeezed; the rate of climb therefore first rises then falls with altitude, giving a theoretical absolute ceiling.",
],
}

# term-link nodes missed by extract: zh -> en
EXTRA = {
'delta-v-rocket': {
    # 注：'火箭速度增量' 已由 item2（面包屑）映射为 "Rocket Delta-v"，term-link 同名节点共用该键，勿重复。
    '：Δv = Isp·g₀·ln(m₀/m_f)。': ': Δv = Isp·g0·ln(m0/mf).',
    '单位换算': 'unit conversion',
},
'wing-loading': {'失速速度': 'stall speed'},
'wing-area-from-loading': {'失速速度': 'stall speed'},
'thrust-to-weight': {'机翼升力': 'wing lift'},
}

def build(slug, en_list):
    path = os.path.join(WORK, slug + '.json')
    wj = json.load(open(path, encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('!! %s length mismatch %d vs %d' % (slug, len(en_list), len(items)))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if not en or not isinstance(en, str):
            print('!! %s empty translation' % slug)
            sys.exit(1)
        if CJK.search(en) or CNP.search(en):
            print('!! %s CJK/CNP violation: %s' % (slug, en[:60]))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('!! %s EXTRA CJK/CNP violation: %s' % (slug, en[:60]))
            sys.exit(1)
        mp[z] = en
    return mp

def write(slug, mp):
    os.makedirs(OUT, exist_ok=True)
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('name', slug)
    out = {'slug': slug, 'industry': 'aerospace', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

for slug, en_list in EN.items():
    write(slug, build(slug, en_list))
