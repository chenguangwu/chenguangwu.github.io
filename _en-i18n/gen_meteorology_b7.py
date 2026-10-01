#!/usr/bin/env python3
# meteorology batch7 (5 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'meteorology')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'meteorology')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'wind-chill': [
"Wind Chill Index",
"Estimate the apparent cold from air temperature and wind speed (km/h) via the Environment Canada WCT formula.",
"Wind Chill Index (WCT) Calculator",
"/ Wind Chill Index Calculator",
"Wind Chill Index Calculator",
'📖 View the "Wind Chill Index User Guide"',
"Wind speed v (km/h)",
"Applies only to cold conditions with air temperature ≤10°C and wind speed >4.8 km/h.",
"📚 In-depth: Wind Chill Index",
"Compute the apparent wind chill from air temperature and wind speed at low temperature with wind.",
"Frostbite risk and outdoor work restrictions.",
"Compare the apparent difference between calm and high wind.",
"Low temperature, high wind",
"−10°C, wind speed 20 km/h: V^0.16=20^0.16 ≈1.614, WC=13.12+0.6215×(−10)−11.37×1.614+0.3965×(−10)×1.614 ≈−17.8°C, much colder than −10°C.",
"Wind speed effect",
"At the same −10°C, wind speed from 5 to 20 km/h lowers the apparent temperature from about −14°C to −17.8°C; the stronger the wind the faster the heat loss.",
"Which temperature does it apply to?",
"Usually for air temperature ≤10°C and wind speed >4.8 km/h; at high temperature there is no wind chill effect, and the heat index is used instead.",
"Does an apparent temperature below the air temperature cause frostbite?",
"The lower the apparent temperature the faster the skin cools; exposure below −18°C for 30 min can cause frostbite, so limit outdoor duration by the wind chill grade.",
],
'relative-humidity': [
"Relative Humidity RH",
"Back-calculate the relative humidity from air temperature and dew point via the Magnus relationship.",
"Find the relative humidity from air temperature and dew point",
"/ Relative Humidity Back-Calculation Calculator",
"Relative Humidity Back-Calculation Calculator",
'📖 View the "Relative Humidity RH User Guide"',
"RH=100·exp[ aTd/(b+Td) − aT/(b+T) ], derived from Magnus.",
"📚 In-depth: Relative Humidity Calculation",
"Compute from dry-bulb and wet-bulb temperature (or dew point)",
"Compute RH as the ratio of actual to saturation vapor pressure.",
"Calibrate humidity sensors with the dry/wet bulb method.",
"Dew point method",
"Air temperature 25°C, dew point 16.7°C: RH=100×exp((17.27×16.7/(237.7+16.7))−(17.27×25/(237.7+25))) ≈60%.",
"Wet-bulb method",
"Dry-bulb 25°C, wet-bulb 19°C, pressure 1013 hPa → table/formula gives RH ≈60%, consistent with the dew point method.",
"Which is more accurate, wet-bulb or dew point?",
"The wet-bulb method is stable with good ventilation; the dew point method is more accurate at low temperature and high humidity; the two can cross-check each other.",
"Can RH exceed 100%?",
"Supersaturation can exceed 100% (in fog/clouds); at the surface it is usually ≤100%; brief supersaturation is called insufficient condensation nuclei.",
],
'pressure-altitude': [
"Pressure Altitude h",
"Back-calculate the altitude from pressure using the International Standard Atmosphere: h = 44330·(1 − (P/P₀)^0.1903).",
"Pressure Altitude Calculator",
"/ Pressure Altitude Calculator",
'📖 View the "Pressure Altitude h User Guide"',
"Sea-level pressure P₀ (hPa)",
"Applies to the troposphere; actual terrain is also affected by temperature stratification.",
"📚 In-depth: Pressure Altitude Calculation",
"Retrieve the pressure altitude from the station pressure (standard atmosphere).",
"Aviation density altitude and performance assessment.",
"Estimate altitude from pressure at mountain stations.",
"Estimate altitude from pressure",
"Station pressure 900 hPa: pressure altitude ≈(1−(900/1013.25)^0.1903)×44331 ≈990 m, close to the geometric altitude (under the standard atmosphere).",
"Altimeter correction",
"When the measured pressure is below the standard 1013.25 → the altimeter reading is too high; QNH correction is needed, otherwise takeoff altitude judgment is wrong.",
"Does pressure altitude equal the true altitude?",
"They are approximately equal only under the standard atmosphere; warm/cold deviations in the real atmosphere make the density altitude deviate from the geometric altitude, affecting flight.",
"Why does pressure decrease with height?",
"The weight of the air column decreases with height, so pressure decays exponentially, halving about every 5500 m.",
],
'humidex': [
"From air temperature and relative humidity, first find the vapor pressure e, then compute the humid-heat apparent index via Humidex = T + 0.5555·(e − 10).",
"Humidex Calculator",
"/ Humidex Calculator",
"Humidex Calculator",
'📖 View the "Humidex User Guide"',
"30-39 take note, 40+ dangerous, 45+ extremely dangerous (Canadian standard).",
"📚 In-depth: Humidex Muggy Apparent Index",
"The Canadian system uses temperature + vapor pressure to compute the muggy index.",
"Compare with the heat index for mid-to-high latitude humidity.",
"High-temperature warning reference",
"grading.",
"Muggy example",
'30°C, vapor pressure e≈29.6 hPa → Humidex=30+0.5555×(29.6−10)=30+10.9≈40.9, at the "very high discomfort" level.',
"Humidex 30-39 uncomfortable, 40-44 distressing, 45-49 dangerous, ≥50 extremely dangerous; in this example 40.9 falls into the distressing level.",
"What is the difference between Humidex and Heat Index?",
'Both use temperature and humidity, but Humidex directly adds a "vapor pressure correction term (0.5555(e−10))", while the heat index uses a full polynomial; the values are close but the basis differs slightly.',
"How is e obtained?",
"Vapor pressure e=RH/100×saturation vapor pressure (Tetens formula), then substitute into Humidex.",
],
'generator-30': [
"⛅ Fog (Visibility) Formation Conditions",
"Visibility",
'📖 View the "Fog (Visibility) Formation Conditions User Guide"',
"Fog is graded by visibility: visibility below 1 km is fog and 1 to 10 km is mist; the formation condition is that near-surface air is nearly saturated (relative humidity close to 100%) and the air temperature drops near the dew point, i.e. the difference between air temperature and dew point does not exceed 2°C; radiation fog mostly occurs on clear nights with light wind (wind speed 1 to 3 m/s) and on autumn/winter mornings, while advection fog forms when warm moist air flows over a cold surface; the smaller the temperature-dew point difference, the denser the fog.",
"📚 In-depth: Meteorological Power Generation Suitability Assessment",
"Wind-solar hybrid plants estimate generation by the local meteorological resources.",
"Determine the installed capacity and storage configuration from the resource grade.",
"Compare output across months for dispatch.",
"Wind-solar combination",
"A site with an annual mean wind speed of 6 m/s (wind power ≈133 W/m²) + annual irradiation 1500 kWh/m²; with wind-solar complementarity, wind in winter and solar in summer make the annualized utilization hours flatter than a single source.",
"Storage ratio",
"With a daily mean output fluctuation coefficient of 0.4, storage = daily average energy ×0.4 can peak-shave and valley-fill, improving the self-consumption rate.",
"Why is wind-solar complementarity stable?",
"Wind is strong in winter and weak in summer, and solar the opposite; they naturally complement each other, smoothing the output curve and reducing storage cost.",
"How is the resource grade determined?",
"Wind energy is graded by wind power density and solar by the annual total (e.g. Class III resource area); the two are assessed independently and then combined.",
'About the "Fog (Visibility) Formation Conditions"',
"Fog (Visibility) Formation Conditions. A free online tool with pure front-end processing; data is not uploaded, protecting privacy and security.",
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
    print('gen_meteorology_b7 done')
