#!/usr/bin/env python3
# meteorology batch6 (7 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'meteorology')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'meteorology')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'heat-index': [
"🌡️ Apparent Temperature Calculation",
"Compute the heat index at high temperature and humidity, and the wind chill index at low temperature with wind",
'📖 View the "Apparent Temperature Calculation User Guide"',
"HI = apparent index (combined temperature and humidity)",
"Use the NWS Rothfusz heat index when the air temperature is ≥27°C and humidity ≥40%; the wind chill index when the air temperature is ≤10°C with wind; in the remaining range the apparent temperature is close to the actual air temperature.",
"📚 In-depth: Heat Index",
"At high temperature and humidity, from air temperature and",
"compute the apparent heat index.",
"Heat-stroke risk grading and outdoor work restrictions.",
"Compare health risk under dry heat and humid heat.",
"High temperature and humidity",
'32°C, relative humidity 70%: the Rothfusz formula gives a heat index ≈41°C, far above the actual temperature, at the "danger" level; avoid prolonged outdoor activity.',
"Dry-heat comparison",
"Also 32°C but 30% humidity → heat index ≈32°C, close to the actual temperature; dry heat risk is much lower, showing humidity is the main cause of mugginess.",
"Why is the heat index often higher than the air temperature?",
"High humidity suppresses sweating and evaporative cooling, so it feels hotter than dry heat; the formula already includes the cross term of T and RH.",
"What is the applicable range of the heat index?",
"Usually significant only when T≥27°C and RH≥40%; the heat index is not reported at low temperature with high humidity.",
'About the "Apparent Temperature Calculation"',
"Apparent Temperature Calculation is an online tool in the scientific research field. A scientific research tool using standard scientific formulas for accurate calculation.",
"Is this tool free?",
"Completely free, no registration, use it directly in the browser.",
"Uses standard scientific calculation formulas for accurate and reliable results.",
"Does it support mobile use?",
"Yes. The page is responsively adapted and works normally on mobile and desktop.",
],
'cloud-identify': [
"🔍 Cloud Identification",
"WMO ten-genera cloud classification, mapping cloud families to cloud base height, appearance features and weather indications",
'📖 View the "Cloud Identification User Guide"',
"Classified by the WMO ten genera: low clouds (cumulus, cumulonimbus, stratocumulus, stratus, nimbostratus, with bases mostly below 2000 m), middle clouds (altostratus, altocumulus, with bases 2000 to 6000 m), high clouds (cirrus, cirrostratus, cirrocumulus, with bases above 6000 m); cumulonimbus indicates thunderstorms and heavy precipitation, cirrostratus often signals an approaching front and worsening weather, and stratocumulus usually means stable weather.",
"All cloud families",
"High clouds",
"Middle clouds",
"Low clouds",
"Vertically developed clouds",
"Clouds are divided into four families by cloud base height: high clouds (>5 km), middle clouds (2.5-5 km), low clouds (<2.5 km) and vertically developed clouds (strong vertical growth).",
"📚 In-depth: Cloud Form Identification",
"Identify cumulus/stratus/cirrus etc. by height and form.",
"Predict short-term weather from clouds (e.g. cumulonimbus thunderstorms).",
"Label cloud types for photography and outreach.",
"Cirrus (Ci) is white and wispy, above 6 km, made of ice crystals, and often signals an approaching weather system; after cirrus appears the weather may change within 24-48 h.",
"Cumulonimbus (Cb) has a dark flat base and an anvil top, accompanied by lightning, rainstorm and strong wind; seeing it signals a severe convection warning.",
"How many cloud families are there?",
"By height they are divided into high/middle/low clouds plus vertically developed clouds, 10 genera in total (e.g. Ci/Cs/Cc, Ac/As, Cu/Sc/St/Ns, Cb).",
"Can clouds forecast the weather?",
"Only a rough nowcast (hour-scale) judgment is possible; accurate forecasts still rely on soundings and numerical models.",
'About the "Cloud Identification"',
"Cloud Identification is an online tool in the scientific research field. A scientific research tool using standard scientific formulas for accurate calculation.",
"Search cloud genus / features / weather indication...",
],
'saturation-vapor-pressure': [
"Saturation Vapor Pressure e_s",
"Compute the saturation vapor pressure from the air temperature via the Magnus formula e_s = 6.1094·exp(17.625T/(T+243.04)).",
"Saturation Vapor Pressure (Magnus) Calculator",
"/ Saturation Vapor Pressure Calculator",
"Saturation Vapor Pressure Calculator",
'📖 View the "Saturation Vapor Pressure e_s User Guide"',
"The saturation vapor pressure grows exponentially with temperature.",
"📚 In-depth: Saturation Vapor Pressure Calculation",
"Compute the saturation vapor pressure at that temperature from the air temperature (Tetens formula).",
"As a",
"/ dew point /",
"absolute humidity",
"base quantity.",
"Used in evapotranspiration and phase-change calculations.",
"Room temperature",
"25°C: e_s=6.1078×exp(17.27×25/(25+237.3)) ≈31.7 hPa; 30°C → ≈42.4 hPa, so a 5°C rise in temperature increases the saturation vapor pressure by about one third.",
"Steep rise with temperature",
'At 0°C e_s≈6.1 hPa and at 20°C ≈23.4 hPa; warming makes the air\'s water-holding capacity rise nearly exponentially, the root cause of "hotter feels muggier".',
"Why use the Tetens formula?",
"The empirical formula is accurate enough from 0-50°C and easy to compute, commonly used in meteorology and hydrology; for wider temperature ranges use Goff-Gratch.",
"Saturation vapor pressure and its unit?",
"Commonly hPa (millibar), a factor of 10 different from kPa; convert when mixing.",
],
'precipitation-rate': [
"Rainfall Grade",
"Determine the grade of light/moderate/heavy/rainstorm/heavy rainstorm from the hourly rainfall (mm/h).",
"Rainfall Intensity Grading Calculator",
"/ Rainfall Intensity Grading Calculator",
'📖 View the "Rainfall Grade User Guide"',
"Rainfall grades are divided by hourly precipitation (mm/h): light rain less than 2.5, moderate 2.5 to 8, heavy 8 to 16, rainstorm 16 to 50, heavy rainstorm 50 to 100, extraordinary rainstorm not less than 100; the magnitude is estimated by the corresponding basis of hourly rain intensity and 24-hour rainfall.",
"Hourly rainfall (mm/h)",
"Uses the common grading of the China Meteorological Administration: light rain <2.5, moderate <8, heavy <16, rainstorm <50, heavy rainstorm <100.",
"📚 In-depth: Precipitation Intensity Calculation",
"From unit-time",
"precipitation",
"compute the rain intensity (mm/h).",
"Graded rain intensity sets the nowcast warning.",
"Compare the intensity of showers and steady precipitation.",
"Rain intensity conversion",
"10-minute rainfall 2 mm → equivalent to 12 mm/h, moderate rain; if 10 minutes gives 8 mm → 48 mm/h heavy rain.",
"Warning thresholds",
"A rain intensity ≥20 mm/h or ≥50 mm/h (1 h) triggers a rainstorm warning; urban flooding depends on the peak rain intensity rather than the total.",
"Which causes disasters, rain intensity or total?",
"Short-duration heavy rainfall (rain intensity) more easily causes waterlogging; a large but gentle total is easier to drain, so cities look at the peak rain intensity.",
"The boundary between light and moderate rain?",
"1 h rain intensity <2.5 light, 2.5-8 moderate, 8-16 heavy, >16 rainstorm (approximate).",
],
'precipitation-calc': [
"🧮 Precipitation Calculation",
"Compute the precipitation intensity from the amount and duration, determine the precipitation grade, and estimate the water volume by area",
'📖 View the "Precipitation Calculation User Guide"',
"Precipitation intensity = precipitation (mm) ÷ duration; 1-hour rainfall is graded as below 2.5 mm light rain, 2.5 to 8 mm moderate, 8 to 16 mm heavy, above 16 mm rainstorm (above 50 mm in 24 hours is also called a rainstorm); total water volume = precipitation (mm) × catchment area (m²) ÷ 1000, in cubic meters or tons, used for drainage and waterlogging assessment.",
"Precipitation (mm)",
"Duration (minutes)",
"Area (m², optional)",
"Precipitation grade (China Meteorological, by 1-hour intensity): light rain <2.5, moderate 2.6-8.0, heavy 8.1-15.9, rainstorm ≥16 mm/h; 1 mm of precipitation equals 1 liter of water per square meter.",
"📚 In-depth: Precipitation Calculation",
"Compute the total precipitation from rain intensity and duration.",
"Convert mm into water volume per unit area (1 mm=1 L/m²).",
"Rainstorm magnitude grading (moderate/heavy/rainstorm/heavy rainstorm).",
"Intensity × time",
"Rain intensity 10 mm/h for 3 h → precipitation 30 mm; 1 mm of precipitation = 1 L of water per m², so a 100 m² roof collects 3000 L.",
"Rainstorm grading",
"24 h rainfall 50-99.9 mm rainstorm, 100-249.9 heavy rainstorm, ≥250 extraordinary rainstorm; in this example 30 mm is heavy rain.",
"How to convert mm and cm?",
'1 mm=0.1 cm; precipitation is inherently a "water depth" unit, and multiplying by area gives volume.',
"Is 1 mm of water a lot?",
"1 mm=1 L/m²; it looks thin, but over 1 km² a city receives 1000 tons of water, so waterlogging depends on the drainage rate.",
'About the "Precipitation Calculation"',
"Precipitation Calculation is an online tool in the scientific research field. A scientific research tool using standard scientific formulas for accurate calculation.",
],
'wind-direction': [
"Wind Direction Bearing",
"Map the wind direction angle (°) to a 16-point compass name (e.g. N, NE, SSW).",
"Wind Direction (16-point) Calculator",
"/ Wind Direction Bearing Calculator",
"Wind Direction Bearing Calculator",
'📖 View the "Wind Direction Bearing User Guide"',
"Wind direction bearing = angle → 16-point",
"Wind direction angle (°) (°)",
"Meteorological wind direction means the direction the wind comes from: 225° means a southwest wind (blowing from the southwest).",
"📚 In-depth: Wind Direction Conversion",
"Convert the bearing (degrees) to a 16-point direction (N/NNE/NE...).",
"Convert between wind vane readings and reports.",
"Determine the receptor for pollution dispersion by wind direction.",
"Angle to bearing",
"90°→east (E), 225°→southwest (SW), 0°/360°→north (N), 315°→northwest (NW); one step every 22.5°, 16 points in total.",
"Meaning of the source direction",
'A "north wind" blows from the north (toward the south); when the pollution source is to the north, the downwind (south) receptors have high concentrations, so siting looks at the direction of travel.',
"Is wind direction the source or the destination?",
"Meteorological wind direction is the source direction (a north wind comes from the north); but wind barbs often draw the direction of travel, so distinguish carefully when reading charts.",
"Are 16 points enough?",
"Enough for daily use; fine dispersion uses a continuous 0-360° angle, and bearings are just a broadcast simplification.",
],
'dew-point': [
"Dew Point (Magnus Formula)",
"Back-calculate the dew point Td from the air temperature and relative humidity via the Magnus formula.",
"Dew Point Calculator",
"/ Dew Point Calculator",
'📖 View the "Dew Point (Magnus Formula) User Guide"',
"Dew point Td = inverse Magnus formula",
"The Magnus empirical formula has good accuracy from 0-50°C.",
"The higher the dew point, the more humid the air.",
"📚 In-depth: Dew Point Calculation",
"From air temperature and",
"compute the dew point (the temperature at which air cools to condensation).",
"A high dew point = muggy; a dew point close to the air temperature = nearly saturated and about to rain.",
"Warehousing/pharmaceuticals control the dew point to prevent condensation.",
"Room-temperature example",
"25°C, relative humidity 60%: with the Magnus formula α=(17.27×25)/(237.7+25)+ln0.6 ≈1.133, dew point Td=237.7×1.133/(17.27−1.133) ≈16.7°C.",
"Near saturation",
"Air temperature 20°C, RH 95% → dew point ≈19.1°C, less than 1°C from the air temperature, very prone to condensation/fog.",
"Can the dew point be higher than the air temperature?",
"No. The dew point is ≤ the air temperature; the smaller the difference the more humid, and a negative difference indicates abnormal data.",
"What is the dew point used for?",
"To judge condensation, fog and mold risk, and to set the target for air-conditioning dehumidification (water only condenses below the dew point).",
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
    print('gen_meteorology_b6 done')
