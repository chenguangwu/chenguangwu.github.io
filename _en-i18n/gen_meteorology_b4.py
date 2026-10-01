#!/usr/bin/env python3
# meteorology batch4 (6 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'meteorology')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'meteorology')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'dafengyingxiangpinggu': [
"📋 Gale Impact Assessment",
"Enter the mean wind speed and gust wind speed to determine the wind force on the Beaufort scale, compute the gust factor and assess the degree of gale impact.",
'📖 View the "Gale Impact Assessment User Guide"',
"📐 Calculation Method",
"Gale impact assessment feeds the mean wind speed and gust wind speed into the Beaufort scale (a nonlinear lookup between wind speed and force); the gust level gives the warning level; the gust factor = gust ÷ mean wind, and the larger it is the more pronounced the structural wind vibration and the higher the risk to billboards, tower cranes, street trees and work at height, so reinforcement and shutdown measures must be implemented according to the level.",
"Mean wind speed V̄ (m/s)",
"Gust wind speed Vg (m/s)",
"💡 The Beaufort scale divides wind force into levels 0-12 by wind speed range; the gust factor G = Vg / V̄ reflects turbulence intensity; the gale warning follows the level corresponding to the gust wind speed.",
"The Beaufort scale is the internationally used wind force standard, from level 0 calm to level 12 hurricane",
"The gust factor is usually between 1.2 and 2.0; the larger it is the stronger the turbulence",
"Gale blue warning: gust ≥17.2 m/s (force 8); yellow: ≥24.5 m/s (force 10); orange: ≥28.5 m/s (force 11); red: ≥32.7 m/s (force 12)",
"📚 In-depth: Gale Impact Assessment",
"Determined by mean wind and gust",
"and impact.",
"Assess gale damage to protected agriculture, billboards and street trees.",
"Set school and work suspension thresholds for emergency response.",
"Mean and gust",
"Mean wind speed 15 m/s → force 7 (near gale, whole trees in motion); gust 25 m/s → force 10 (storm), which can tear off billboards; reinforce them.",
"Response thresholds",
"A gust reaching force 8 (≥17.2 m/s) triggers a warning and force 10 (≥24.5 m/s) a school-suspension recommendation; in this example a gust of 25 m/s triggers the suspension recommendation.",
"Look at mean or gust wind?",
"Disaster assessment looks at the gust (instantaneous maximum) and building wind design uses the gust; the mean wind is used for overall rating.",
"At what wind force do schools close?",
"It varies by region; commonly force 8-9 gusts are yellow and force 10-11 are orange with school suspension, subject to local warnings.",
'About the "Gale Impact Assessment"',
"Based on the Beaufort scale, the gale impact assessment tool takes the mean wind speed and gust wind speed, automatically determines the wind force, computes the gust factor, and maps the gust intensity to the gale warning level, giving descriptions of land impact and sea state.",
"Automatic Beaufort force 0-12 determination",
"Gust factor and turbulence intensity assessment",
"Blue/yellow/orange/red four-level gale warning",
"Land impact and sea state description",
"Gale warning level determination",
"Construction safety assessment",
"Wind-force reference for outdoor activities",
"Safety assurance for maritime navigation",
],
'strength-3': [
"📋 Radar Echo Intensity Assessment",
"Enter the echo intensity, echo top height and echo area to comprehensively assess the convective intensity grade, hail probability and precipitation contribution.",
'📖 View the "Radar Echo Intensity Assessment User Guide"',
"📐 Calculation Method",
"Radar echo intensity: reflectivity factor Z=10^(dBZ/10), rain rate R=(Z/200)^(1/1.6) mm/h; hail probability is estimated jointly from dBZ and echo top height h; liquid water content VIL=3.44×10⁻⁶·Z^(4/7)·h (kg/m²); the convective grade is determined by dBZ thresholds (<30 weak convection, <50 strong convection, ≥55 hail possible, ≥60 strong hail), and the precipitation contribution is estimated from area and intensity.",
"Echo intensity (dBZ)",
"Echo top height (km)",
"Echo area (km²)",
"💡 Hail probability PH = clamp(0.6·(dBZ-40)/30 + 0.4·(H-5)/10); convective intensity is determined from dBZ combined with echo top height; VIL approximation = 3.44e-6·Z^(4/7)·H.",
"The hail probability is an empirical estimate based on dBZ and echo top height; in practice it must be combined with sounding and environmental fields",
"VIL (vertically integrated liquid water) uses a single-layer approximation and is only an order-of-magnitude reference",
"The echo top height generally refers to the height of the 18 dBZ echo",
"📚 In-depth: Wind Force Intensity Assessment",
"Estimate structural loads from wind speed and wind pressure.",
"Wind resistance check for billboards/greenhouses.",
"Gale disaster loss grading.",
"Wind speed 20 m/s, air density 1.225 → dynamic pressure = 0.5×1.225×20² ≈ 245 Pa; a 10 m² windward face receives about 2450 N ≈ 250 kgf of thrust.",
"Wind resistance check",
"Design wind resistance 0.5 kPa, actual 0.245 kPa leaves ample margin; a gust of 30 m/s → 0.55 kPa exceeds the design, requiring reinforcement.",
"Is wind pressure related to wind speed squared?",
"Dynamic pressure ∝ wind speed squared; doubling the wind speed quadruples the thrust, so gale damage increases sharply.",
"How large is the wind pressure unit Pa?",
"1 Pa=1 N/m²; 250 Pa seems small but multiplied by the area of a large billboard the total force is very large.",
'About the "Radar Echo Intensity Assessment"',
"Enter the radar echo intensity, echo top height and echo area to comprehensively assess the convective intensity grade, estimate the hail probability, the vertically integrated liquid water (VIL) and the regional precipitation magnitude, providing a quantitative reference for severe convection warnings.",
"Convective intensity grade assessment",
"Empirical hail probability estimation",
"VIL approximation calculation",
"Regional water flux estimation",
"Severe convection and hail warning",
"Radar meteorology analysis",
"Nowcasting support",
"Reference for artificial hail suppression operations",
],
'jiaotongqixianganquantishi': [
"🫁 Traffic Meteorological Safety Advisory",
"Enter the visibility, road surface temperature and wind speed to comprehensively assess the impact of adverse weather such as low visibility, icing and crosswind on traffic safety and output a warning level.",
'📖 View the "Traffic Meteorological Safety Advisory User Guide"',
"📐 Calculation Method",
"Road meteorological safety is judged by grading three items: visibility (vis) (<50 m special grade, <200 m red, <500 m orange, <1000 m yellow, otherwise good), road surface temperature (rt) (<−3°C red, <0°C orange, <2°C yellow), and crosswind (v) (≥24 m/s red, stepping down). If any item reaches red/orange, the corresponding control advice (speed limit, anti-skid, closure) is given to ensure driving safety.",
"Visibility (m)",
"Road surface temperature (°C)",
"💡 Visibility <50 m dense fog (special grade), 50-200 dense fog (red), 200-500 fog (orange), 500-1000 mist (yellow); road surface temperature <0°C icing risk; wind speed ≥17 m/s strong crosswind.",
"The warning level takes the highest of the three risks: visibility, icing and crosswind",
"When the road surface temperature is below 0°C, humidity must be considered to judge actual icing; this tool warns by temperature",
"The crosswind effect is particularly significant on highway bridges and elevated sections",
"📚 In-depth: Traffic Meteorological Safety Advisory",
"Give road safety advisories by visibility / road surface temperature / wind.",
"Graded warning for fog, freezing rain and crosswind sections.",
"Navigation overlays weather to give speed-limit / detour advice.",
"Low visibility",
"Visibility 200 m → dense fog (<500 m); advise turning on fog lights, limiting speed to 60, keeping distance, and the highway may be closed.",
"Road icing",
"Road surface temperature −2°C with precipitation → icing risk; advise fitting snow chains / no driving; bridge decks freeze earlier than ordinary roads.",
"How is visibility graded?",
"≥1000 m normal, 500-1000 significant impact, <500 dense fog (highways easily closed), <200 extremely dense fog.",
"Where is crosswind most dangerous?",
"On bridges, wind gaps and highway overpasses; the crosswind pushes vehicles off course, especially large vehicles; advise slowing down and gripping the wheel.",
'About the "Traffic Meteorological Safety Advisory"',
"Enter the visibility, road surface temperature and wind speed to individually assess the three meteorological risks of low visibility (fog), road icing and strong crosswind, take the highest as the comprehensive traffic meteorological warning level, and give graded control advice.",
"Graded low-visibility warning",
"Road icing risk assessment",
"Strong crosswind impact judgment",
"Comprehensive warning and control advice",
"Highway weather warning",
"Keeping roads open and smooth in winter",
"Traffic command and dispatch",
"Travel safety reference",
],
'lvyouqixiangzhishu': [
"⛅ Tourism Meteorological Index",
"Enter the temperature, humidity, wind speed and UV index to compute a weighted tourism suitability index and get travel advice.",
'📖 View the "Tourism Meteorological Index User Guide"',
"📐 Calculation Method",
"The tourism meteorological index weights four comfort items, temperature (T), humidity (RH), wind speed (V) and UV: temperature score = 100−|T−22|×3.5, humidity score = 100−|RH−55|×0.9, wind score = 100−|V−3|×6, UV score = 100−UV×9 (all clamped to 0-100); the composite idx = 0.35×temperature + 0.20×humidity + 0.20×wind + 0.25×UV, and the higher it is the better suited for travel (≥80 excellent, ≥65 suitable, ≥50 fair, ≥35 not very suitable, <35 unsuitable).",
"UV index UV (0-11+)",
"💡 Tourism suitability = 0.35·temperature score + 0.20·humidity score + 0.20·wind score + 0.25·UV score; each sub-score is 100 at the comfort value and decreases with deviation, and the higher the composite score the better suited for travel.",
"The temperature comfort zone is 18-26°C, humidity 40-65%, wind speed 1-5 m/s and UV 0-5",
"UV index 0-2 low, 3-5 moderate, 6-7 high, 8-10 very high, 11+ extreme",
"This index is an empirical model; actual experience varies from person to person",
"📚 In-depth: Tourism Meteorological Index",
"Compute the travel suitability index from temperature, humidity, wind and sunshine.",
'Give a "is today good for visiting" recommendation for a destination.',
"Stagger visitor peaks at scenic spots by the index.",
"Suitable example",
"Air temperature 22°C, RH 55%, wind speed 2 m/s, clear → tourism index ≈85 (suitable), comfortable and good for the outdoors.",
"Unsuitable example",
"Air temperature 35°C, RH 80% or force-8 gale → index <40 (unsuitable); advise staying indoors or rescheduling.",
"How is the index computed?",
"Temperature, humidity, wind and sunshine are weighted by comfort into 0-100; the higher the more suitable for travel, with thresholds fine-tuned by region (e.g. highlands).",
"Does a high index mean sun exposure is fine?",
"Suitable does not mean low UV; in summer you still need to check the UV index and take separate sun protection.",
'About the "Tourism Meteorological Index"',
"Combining the four meteorological elements of temperature, humidity, wind speed and UV, it computes sub-scores from each element's deviation relative to the comfort zone and sums them with weights to get a 0-100 tourism meteorological suitability index, outputting travel advice and a UV protection notice.",
"Four-factor weighted suitability assessment",
"Quantification of sub-scores",
"Five-level suitability determination",
"UV protection notice",
"Travel itinerary planning",
"Scenic-spot meteorological services",
"Outdoor activity planning",
"Travel weather reference",
],
'taifengdingqiang': [
"🌤️ Typhoon Intensity Estimation",
"Enter the typhoon's minimum central sea-level pressure to estimate the maximum wind speed near the center using the Atkinson-Holliday empirical formula and determine the typhoon intensity grade.",
'📖 View the "Typhoon Intensity Estimation User Guide"',
"Knot = 0.5144 m/s. The lower the pressure, the stronger the maximum wind speed.",
"Minimum central pressure Pc (hPa)",
"💡 Atkinson-Holliday (1977): Vmax (knots) = 10.35×(1010-Pc)^0.615; 1 knot = 0.5144 m/s. The lower the pressure, the stronger the maximum wind speed.",
"The Atkinson-Holliday formula is a statistical empirical relationship for tropical cyclones in the Northwest Pacific",
"The environmental pressure is taken as 1010 hPa; estimates are high for weaker systems and are for intensity reference only",
'Typhoon grades follow China\'s "Grades of Tropical Cyclones" GB/T 19201 standard (2-minute mean wind)',
"📚 In-depth: Typhoon Intensity Grading",
"Determine the typhoon grade from the maximum wind speed near the center (from force 12 in China).",
"Distinguish typhoon / severe typhoon / super typhoon.",
"Match warning signals with defense measures.",
"Wind-speed grading",
"Maximum wind near the center Vms=40 m/s → falls in 32.7-41.4 → force 13 (typhoon); Vms=55 m/s → ≥51.0 → force 16 (super typhoon).",
"Warning correspondence",
"Force 12 (≥32.7) yellow, force 14 (≥41.5) orange, force 16 (≥51.0) red; the super typhoon red is the highest level and requires comprehensive defense.",
"From what force is a typhoon called a typhoon in China?",
"A surface maximum wind near the center ≥ force 12 (≥32.7 m/s) is called a typhoon; tropical storm is force 8-9 and severe tropical storm force 10-11.",
"How is wind speed measured?",
"By aircraft penetration or buoy/radar retrieval; ground stations are often destroyed by the eyewall, so intensity estimation uses the maximum wind speed.",
'About the "Typhoon Intensity Estimation"',
"Enter the tropical cyclone's minimum central sea-level pressure to estimate the maximum sustained wind speed near the center via the Atkinson-Holliday (1977) empirical formula and determine the intensity grade (TD/TS/STS/TY/STY/SuperTY) per China's \"Grades of Tropical Cyclones\" GB/T 19201.",
"Atkinson-Holliday wind speed estimation",
"Multi-unit wind speed conversion",
"Beaufort force and typhoon grade",
"Typhoon emergency response advice",
"Tropical cyclone intensity estimation",
"Typhoon prevention and disaster reduction decision-making",
"Reference for marine and aviation typhoon avoidance",
"Meteorological teaching and outreach",
],
'speed-11': [
"🌤️ Radar Reflectivity Interpretation",
"Enter the radar reflectivity factor (dBZ) to estimate the rain intensity via the Z-R relationship and identify the echo type and convective intensity.",
'📖 View the "Radar Reflectivity Interpretation User Guide"',
"Z = 200·R^1.6, so R = (Z/200)^(1/1.6)",
"Radar reflectivity factor (dBZ)",
"💡 Z-R relationship (Marshall-Palmer): Z = 200·R^1.6, so R = (Z/200)^(1/1.6); Z = 10^(dBZ/10), in mm⁶/m³, and R is the hourly rain intensity in mm/h.",
"Uses the classic Marshall-Palmer Z=200R^1.6 relationship, applicable to the average conditions of stratiform and convective clouds",
"Z-R coefficients differ by region, season and precipitation type; results are for reference only",
"dBZ≥45 indicates convective precipitation, ≥55 possible hail, ≥65 high risk of strong hail",
"📚 In-depth: Wind Speed Processing and Statistics",
"Compute the mean and maximum wind from instantaneous wind speed.",
"Determine the design wind speed using wind roses/percentiles.",
"Wind turbine control uses 2min/10min mean wind.",
"Statistical window",
"10min mean 8 m/s, maximum 15 m/s → max/mean ratio 1.875, the gust factor used for building wind loads.",
"Design wind speed",
"The annual maximum wind speed sample takes the 50-year return-period percentile ≈ 28 m/s as the wind-resistant design basis for structures.",
"Over what period is the mean wind taken?",
"Meteorological convention uses a 10 min mean and a 3 s gust; wind turbines use the 10 min mean for power and the 3 s maximum for loads.",
"How much larger is the maximum wind than the mean wind?",
"The gust factor is usually 1.5-2.5, varying with the underlying surface and stability, and larger in cities than over the sea.",
'About the "Radar Reflectivity Interpretation"',
"Enter the weather radar reflectivity factor (dBZ) to retrieve the rain intensity via the Marshall-Palmer Z-R relationship and, by dBZ magnitude, identify echo types such as stratiform cloud, convective cloud, rainstorm and hail, providing a reference for severe convection identification.",
"Rain intensity retrieval via the Z-R relationship",
"Reflectivity factor Z conversion",
"Echo type and convective identification",
"Precipitation grade and daily amount estimation",
"Weather radar echo analysis",
"Severe convection nowcasting",
"Quantitative precipitation estimation QPE",
"Meteorological teaching and training",
],
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
        if it.get('src_diff') and it.get('zh_src'):
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
    return mp

def write(slug, mp):
    os.makedirs(OUT, exist_ok=True)
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('name', slug)
    out = {'slug': slug, 'industry': 'meteorology', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

if __name__ == '__main__':
    for slug, en_list in EN.items():
        mp = build(slug, en_list)
        write(slug, mp)
    print('gen_meteorology_b4 done')
