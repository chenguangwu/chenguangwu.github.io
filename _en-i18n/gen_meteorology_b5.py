#!/usr/bin/env python3
# meteorology batch5 (6 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'meteorology')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'meteorology')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'jiangshuigailvguji': [
"🎲 Precipitation Probability Estimation",
"Enter the column-integrated water vapor flux and the lifted index (LI) to estimate the probability and magnitude of precipitation, combining moisture conditions and atmospheric stability.",
'📖 View the "Precipitation Probability Estimation User Guide"',
"Water vapor flux Q (g/(cm·hPa·s))",
"Lifted index LI (°C, negative means unstable)",
"💡 Precipitation probability P = clamp(40 + 1.5·Q - 8·LI, 5, 99); precipitation intensity R = max(0, 0.8·(Q-5) - 1.2·LI) mm/h. The larger Q is, the more abundant the moisture, and the more negative LI is, the more unstable, the higher the precipitation probability.",
"The lifted index LI is the difference between the 500 hPa environmental temperature and the parcel temperature; a negative value indicates instability",
"The water vapor flux reflects the column moisture transport intensity, with typical summer values of 10-30 g/(cm·hPa·s)",
"This formula is an empirical statistical model; actual precipitation is also affected by triggering mechanisms, terrain and more",
"📚 In-depth: Precipitation Probability Estimation",
"Estimate today's precipitation probability from the rain frequency of historically similar weather.",
"Use the fraction of ensemble members with precipitation as the probability.",
'Give a plain-language interpretation of "30% precipitation".',
"Historical frequency method",
'Of the past 100 days of "similar circulation + humidity", 70 had rain → precipitation probability ≈70%; advise bringing an umbrella.',
"Ensemble members",
'Of the 20 ensemble members, 6 forecast rain → probability 30%, meaning "possibly but unlikely", decide by the importance of the activity.',
"What does a 30% precipitation probability mean?",
'It means a 30% chance of rain at any point in the forecast area, not "raining for 30% of the time/area".',
"Can probabilities be added up?",
"They cannot be simply added; probabilities from different sources must use the same basis (location/time window).",
'About the "Precipitation Probability Estimation"',
"Enter the column-integrated water vapor flux and the lifted index (LI) to estimate the probability of precipitation and its intensity magnitude, combining moisture transport conditions and atmospheric stratification stability, providing a reference for precipitation nowcasting.",
"Moisture-stability two-factor model",
"Quantitative precipitation probability estimation",
"Precipitation intensity and grade determination",
"Atmospheric stability grading",
"Nowcasting support for precipitation",
"Heavy precipitation potential analysis",
"Reference for flood-control warnings",
"Meteorological teaching and diagnosis",
],
'wet-bulb-temperature': [
"Wet-Bulb Temperature T_w",
"Estimate the wet-bulb temperature from air temperature and relative humidity via the Stull (2011) empirical polynomial, applicable to 5-95% RH and -20-50°C.",
"Wet-Bulb Temperature (Stull Empirical Formula) Calculator",
"/ Wet-Bulb Temperature Calculator",
"Wet-Bulb Temperature Calculator",
'📖 View the "Wet-Bulb Temperature T_w User Guide"',
"Wet-Bulb Temperature T_w (iterative approximation)",
"Stull 2011 single-equation approximation, iteration-free, commonly used in engineering and meteorological outreach.",
"📚 In-depth: Wet-Bulb Temperature Calculation",
"From air temperature and",
"compute the wet-bulb temperature (the evaporative cooling limit).",
"Heat stress (WBGT) and health risk.",
"Cooling tower",
"/ evaporative cooling efficiency assessment.",
"Room-temperature example",
"30°C, relative humidity 70%: Stull approximation wet-bulb ≈25.6°C; the lower the humidity, the lower the wet-bulb (stronger evaporation), and at saturation the wet-bulb = air temperature.",
"Health significance",
"A wet-bulb of 35°C is the human heat-dissipation limit (cooling by sweating fails); though rare, it is fatal under extreme heat and humidity, and a wet-bulb above 28°C already means high-risk work.",
"Is the wet-bulb the same as the apparent temperature?",
'No. The wet-bulb is "the temperature when evaporation reaches its limit", a physical quantity; the apparent temperature is a composite sensation, and only WBGT includes the wet-bulb as a heat-stress index.',
"Can the wet-bulb reach 35°C?",
"Rarely, and it requires extremely hot and humid conditions; if it occurs, outdoor activity is extremely dangerous, and it is a research direction for climate tipping points.",
"How to use Wet-Bulb Temperature T_w",
"What does Wet-Bulb Temperature T_w do?",
"How do I use Wet-Bulb Temperature T_w?",
"What scenarios is Wet-Bulb Temperature T_w suitable for?",
"The wet-bulb temperature T_w is the temperature when water evaporation reaches adiabatic saturation, reflecting the upper limit of cooling and the evaporative cooling potential; the larger the wet-bulb depression, the drier and the stronger the evaporation.",
"Assess heat stress and the human heat-dissipation limit (a wet-bulb ≈35°C is the physiological tolerance ceiling), irrigation and HVAC design.",
"Boundary",
"Estimated from dry-bulb, humidity and pressure; different formulas (Stull etc.) have an error of about ±0.3°C, and precise meteorology relies on measured wet-bulb values.",
],
'risk-14': [
"⛅ Meteorological Health Risk Warning",
"Enter the temperature, humidity, wind speed and pressure to compute how far each meteorological element deviates from the comfort zone and weight them into a composite health risk index and warning level.",
'📖 View the "Meteorological Health Risk Warning User Guide"',
"📐 Calculation Method",
"The meteorological health risk weights the hazard functions of four elements, temperature, humidity, wind speed and pressure, deviating from the comfort zone: fT=|T−22|/28, fRH=|RH−55|/60, fV=V/18, fP=|P−1013|/40 (all clamped to 0-1), and the composite R=100×(0.35fT+0.20fRH+0.20fV+0.25fP); the higher R is, the greater the risk of triggering cardiovascular and respiratory diseases, so sensitive groups need enhanced protection.",
"💡 Formula: R = 100×(0.35·f(T)+0.20·f(RH)+0.20·f(V)+0.25·f(P)), where f is the normalized hazard function of each element's deviation from the comfort zone; the larger R, the higher the risk.",
"This index is an empirical composite meteorological sensitivity model, with the comfort zone taken as temperature 22°C, humidity 55% and pressure 1013 hPa",
"The weights reference the incidence patterns of meteorologically sensitive diseases such as cardiovascular and respiratory conditions",
"The result is for health protection reference only and cannot replace a medical diagnosis",
"📚 In-depth: Meteorological Risk Grading (Composite)",
"Conduct risk grading for a single hazard or multiple superimposed hazards.",
"Support emergency plans and resource pre-positioning.",
"Compare risk across regions to set priorities.",
"Risk is divided into 4 levels: blue (<40)/yellow (40-60)/orange (60-80)/red (>80); a region at a composite 72 falls into orange and must launch the corresponding response.",
"Superposition",
"Rainstorm (yellow) + gale (orange) superimposed → take the higher and elevate one level to red due to coupling, since flooding carries amplified backflow risk.",
"Do the risk level and warning color match?",
'They usually correspond one-to-one (blue, yellow, orange, red), but risk is "likelihood × consequence" while warnings also include real-time urgency, so there are slight differences.',
"How are multiple hazards superimposed assessed?",
"Generally take the highest level and adjust upward for coupling effects, to avoid underestimating compound disasters by looking at a single hazard.",
'About the "Meteorological Health Risk Warning"',
"Combining the four meteorological elements of temperature, humidity, wind speed and pressure, it computes each element's deviation relative to the human comfort zone and sums them with weights to get a 0-100 meteorological health risk index, outputting a four-level warning and protection advice.",
"Four-element weighted composite assessment",
"Quantification of each risk contribution",
"Four-level warning determination",
"Targeted health protection advice",
"Health protection for chronic disease patients",
"Warning reference for nursing homes/schools",
"Outdoor work safety notice",
"Meteorological health outreach",
],
'humidity-1': [
"🌡️ Dew Point Comfort Calculation",
"Enter the temperature and relative humidity to compute the dew point, vapor pressure, apparent temperature and comfort grade.",
'📖 View the "Dew Point Comfort Calculation User Guide"',
"Dew point comfort = f(temperature, dew point)",
"💡 Magnus dew point formula: γ=ln(RH/100)+17.27T/(237.3+T), Td=237.3γ/(17.27-γ); THI=T-0.55(1-RH/100)(T-14.5).",
"The dew point uses the Magnus-Tetens empirical formula, with an accuracy of about ±0.4°C",
"The apparent temperature uses the Australian apparent temperature formula (no wind or radiation correction)",
"At high temperature and humidity the heat index is automatically enabled; the result is for apparent-temperature reference only",
"📚 In-depth: Relative Humidity and Apparent Temperature",
"Compute from dry/wet bulb or dew point and temperature",
'Explain "the same temperature feels different at different humidity".',
"Recommended indoor comfort humidity is 40%-60%.",
"Back-calculate from dew point",
"Air temperature 25°C, dew point 16.7°C: RH=100×exp((17.27×16.7/(237.7+16.7))−(17.27×25/(237.7+25))) ≈60%.",
"Comfort range",
"RH<30% dry (dry throat, static), >70% humid (mold, stuffiness), 40%-60% most comfortable; target humidification/dehumidification at this.",
"How does relative humidity change over a day?",
"When the moisture content is relatively stable, rising temperature lowers RH and falling temperature raises RH, so RH peaks in the early morning and is lowest in the afternoon.",
"Is the hygrometer inaccurate?",
"Mostly due to temperature drift and lag; calibrate regularly with saturated salt solutions to avoid long-term bias.",
'About the "Dew Point Comfort Calculation"',
"Enter the air temperature and relative humidity to compute the dew point and vapor pressure via the Magnus-Tetens formula, determine the human comfort grade using the temperature-humidity index (THI), and compute the heat index at high temperature and humidity to assess heat-stroke risk.",
"Magnus formula dew point calculation",
"Vapor pressure and apparent temperature",
"THI six-level comfort determination",
"High-temperature heat index warning",
"Indoor environment comfort assessment",
"Heat-stroke prevention reference",
"HVAC dehumidification control",
"Meteorological outreach and teaching",
],
'isa-temperature': [
"ISA Temperature",
"Find the air temperature from altitude using the ISA model: in the troposphere (≤11 km) it drops 6.5°C per kilometer, and the base of the stratosphere is isothermal.",
"International Standard Atmosphere (ISA) Temperature Calculator",
"/ International Standard Atmosphere Temperature Calculator",
"International Standard Atmosphere Temperature Calculator",
'📖 View the "Temperature User Guide"',
"Altitude h (km)",
"Sea-level standard temperature 15°C; at 11 km it is about −56.5°C, the tropopause.",
"📚 In-depth: International Standard Atmosphere Temperature",
"Compute the ISA standard temperature by altitude (troposphere lapse rate 6.5°C/km).",
"Convert aviation performance to the standard atmosphere reference.",
"Altimeter/density altitude assessment.",
"By altitude",
"Altitude 5.5 km: standard temperature = 15−6.5×5.5 = 15−35.75 = −20.75°C; if the actual is warmer, the density altitude is higher and engine thrust drops.",
"By feet",
"10000 ft: T=15−1.98×10=−4.8°C (1.98°C/1000 ft, i.e. 6.5°C/km); the base of the stratosphere at 11 km is constantly −56.5°C.",
"Is the ISA the real atmosphere?",
"No, it is a sea-level standard model with a sea-level pressure of 1013.25 hPa and 15°C; the real atmosphere deviates and requires corrections.",
"Why use density altitude?",
"Aircraft performance depends on air density rather than geometric altitude; a warm deviation makes the density altitude higher than the indicated altitude, affecting takeoff roll.",
"How to use Temperature",
"What does Temperature do?",
"How do I use Temperature?",
"What scenarios is Temperature suitable for?",
"International Standard Atmosphere (ISA) troposphere temperature T=288.15−6.5·h (h is altitude in km, in K), i.e. about 6.5°C per 1 km rise.",
"Units and range",
"The result can be shown in K or °C; the formula applies only to the troposphere (altitude ≤ 11 km). The stratosphere (11-20 km) is essentially isothermal at about 216.65 K.",
"The ISA is an average standard model; the real atmosphere deviates noticeably with latitude/season/weather, so for aviation/meteorology rely on measurements.",
],
'temp-pressure': [
"⛅ Temperature-Pressure-Humidity Conversion",
"Compute the saturation vapor pressure, actual vapor pressure, dew point and air density from air temperature, relative humidity and pressure",
'📖 View the "Temperature-Pressure-Humidity Conversion User Guide"',
"Td=243.04·ln(e/6.1094)/(17.625−ln(e/6.1094)); air density accounts for the moisture effect.",
"Formula: the saturation vapor pressure uses the Magnus-Tetens formula eₛ=6.1094·exp(17.625T/(T+243.04)) hPa; dew point Td=243.04·ln(e/6.1094)/(17.625−ln(e/6.1094)); air density accounts for the moisture effect.",
"📚 In-depth: Combined Temperature-Humidity-Pressure Calculation",
"Input temperature, humidity and pressure together to compute dew point/density/apparent temperature.",
"Atmospheric density for flight/ventilation calculations.",
"One-stop conversion of multiple parameters.",
"Combined",
"25°C, RH 60%, pressure 1000 hPa → dew point ≈16.7°C, air density ≈1.17 kg/m³ (slightly less than the standard 1.225 due to warm moisture).",
"Density applications",
"Density 1.17 is used for ventilation conversion: air volume (m³/h)×1.17 = mass flow (kg/h),",
"Fan selection",
"looks at the mass flow.",
"What do temperature, humidity and pressure compute together?",
"Air density, dew point, apparent temperature and other derived quantities; density is a core parameter for fluid/flight/ventilation.",
"What does low density affect?",
"Low density (warm-humid/high altitude) lowers engine thrust, fan air flow and lift, requiring correction to actual conditions.",
'About the "Temperature-Pressure-Humidity Conversion"',
"Temperature-Pressure-Humidity Conversion is an online tool in the scientific research field. A scientific research tool using standard scientific formulas for accurate calculation.",
"How to use Temperature-Pressure-Humidity Conversion",
"What does Temperature-Pressure-Humidity Conversion do?",
"Enter the air temperature, relative humidity and pressure to compute the saturation vapor pressure, actual vapor pressure, dew point and air density, commonly used for atmospheric sounding, ventilation heat exchange and meteorological parameter conversion.",
"How do I use Temperature-Pressure-Humidity Conversion?",
"What scenarios is Temperature-Pressure-Humidity Conversion suitable for?",
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
    print('gen_meteorology_b5 done')
