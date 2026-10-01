#!/usr/bin/env python3
# meteorology batch1 (7 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'meteorology')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'meteorology')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'absolute-humidity': [
"Absolute Humidity AH",
"From air temperature and relative humidity, estimate the mass of water vapor per unit volume of air (g/m³) with an empirical formula.",
"Absolute Humidity Calculator",
"/ Absolute Humidity Calculator",
'📖 View the "Absolute Humidity AH User Guide"',
"Represents the mass of water vapor per cubic meter of air.",
"📚 In-depth: Absolute Humidity Calculation",
"Given the air temperature and",
", calculate how many grams of water vapor a unit volume of air contains.",
"Compare the absolute humidity difference at the same humidity in winter and summer to explain \"damp cold / damp heat\".",
"In greenhouse/warehouse humidity control, absolute humidity determines the",
"dehumidification load",
"Room-temperature example",
"25°C with 60% relative humidity: saturation vapor pressure ≈31.7 hPa, actual vapor pressure = 31.7×0.6 ≈19.0 hPa; absolute humidity = 216.7×19.0/(25+273.15) ≈13.8 g/m³.",
"Winter comparison",
"5°C with 60% relative humidity: saturation pressure ≈8.7 hPa, actual ≈5.2 hPa, absolute humidity ≈4.4 g/m³, far below the summer 13.8, so winter feels dry.",
"What is the difference between absolute and relative humidity?",
"Relative humidity is a measure of \"how close to saturation\"",
", while absolute humidity is \"how many grams of water vapor are actually present\"; when temperature changes, relative humidity changes greatly while absolute humidity stays relatively stable.",
"Why is it drier when the heating is on in winter?",
"Heating raises the temperature but the amount of water vapor is unchanged, so absolute humidity stays the same while relative humidity drops sharply, making it feel dry; you need humidification, not just heating.",
],
'air-aqi': [
"⚖️ Air Quality AQI Calculation",
"Enter the six pollutant concentrations; per the HJ 633-2012 standard, compute the IAQI for each and take the maximum to get the AQI. Units: μg/m³ (CO in mg/m³).",
'📖 View the "Air Quality AQI Calculation User Guide"',
"AQI = piecewise linear interpolation per pollutant",
"💡 Formula: IAQI = (IAQI_high − IAQI_low)/(C_high − C_low) × (C − C_low) + IAQI_low; AQI = max(IAQI of each pollutant), and the primary pollutant is the one with the largest IAQI.",
"Uses the concentration breakpoints of China's \"Technical Regulation on Ambient Air Quality Index (AQI) (on trial)\" HJ 633-2012",
"When the O₃ concentration exceeds 200 μg/m³, the 1-hour IAQI is extrapolated from the breakpoints for reference only",
"The calculated results are for reference only; actual air quality is subject to official monitoring releases",
"📚 In-depth: Air Quality Index (AQI) Calculation",
"Compute the IAQI sub-index from PM2.5/PM10/SO₂ etc. and take the maximum to get the AQI.",
"Identify the primary pollutant and the exceedance grade.",
"Give health and outdoor-activity advice based on the AQI.",
"PM2.5 dominant",
"PM2.5=75 μg/m³: falls in the segment (35,75]→(50,100), IAQI=50+(75−35)/(75−35)×(100−50)=100; PM10=50→IAQI=50. AQI=max=100 (Good), primary pollutant PM2.5.",
"Excellent-grade example",
"With PM2.5=35 and PM10=50, each IAQI=50, AQI=50 (Excellent), no primary pollutant, normal outdoor activity is fine.",
"Why does the AQI take the maximum?",
"The AQI takes the maximum IAQI across pollutants, representing the health risk of the \"worst\" one, which is the primary pollutant.",
"How many AQI levels are there?",
"0-50 Excellent, 51-100 Good, 101-150 Light, 151-200 Moderate, 201-300 Heavy, >300 Severe; sensitive groups should take care above 100.",
'About the "Air Quality AQI Calculation"',
"Based on China's HJ 633-2012 standard, the Air Quality Index (AQI) calculator takes the six pollutant concentrations PM2.5, PM10, SO₂, NO₂, CO and O₃, computes the individual air quality sub-index (IAQI) for each, takes the maximum as the AQI, and identifies the primary pollutant and its corresponding health impact grade.",
"Compute the IAQI for each of the six pollutants",
"Automatically identify the primary pollutant",
"Six-level health impact grading",
"Ambient air quality assessment",
"Meteorological and environmental data analysis",
],
'analysis-31': [
"🔮 Climate (Forecast/Anomaly/Extreme) Analysis",
"Forecast/Anomaly/Extreme",
"Compare the current observation with the climatological normal (usually a 30-year climate average) to compute the anomaly, anomaly percentage and standardized anomaly σ, and grade it as normal, slightly strong/weak or significantly extreme by the absolute value of σ. Data is processed only locally in the browser and is never uploaded.",
'📖 View the "Climate (Forecast/Anomaly/Extreme) Analysis User Guide"',
"Anomaly = observation − climatological normal",
"Standardized anomaly σ = anomaly ÷ historical standard deviation",
"Compare the current observation with the climatological normal (usually a 30-year climate average) to compute the anomaly, anomaly percentage and standardized anomaly σ, and grade it as normal, slightly strong/weak or significantly extreme by the absolute value of σ. All data is processed only locally in the browser and never uploaded.",
"Current observation",
"Climatological normal",
"Historical standard deviation",
"Element unit",
"📚 In-depth: Climate Anomaly and Standardized Extreme Analysis",
"Compare this month's or season's temperature and precipitation observations with the climatological normal to give the magnitude of the high or low deviation.",
"Use the standardized anomaly σ to judge whether the deviation reaches the magnitude of an extreme event, aiding climate assessment and briefing materials.",
"Compute separately for multiple stations or elements and compare horizontally which regions deviate most in the same period.",
"Magnitude of above-normal temperature",
"A station's July mean temperature is 26.8°C, the climatological normal 24.2°C, the historical",
"standard deviation 1.1°C. Anomaly = 26.8 − 24.2 = 2.6°C, anomaly percentage = 2.6 ÷ 24.2 = 10.7%, standardized anomaly σ = 2.6 ÷ 1.1 = 2.36, in the 2-3 range, graded \"significantly high\".",
"How far below normal is the precipitation",
"A month's precipitation is 48 mm, the climatological normal 120 mm and the standard deviation 35 mm. Anomaly = −72 mm, anomaly percentage = −60.0%, σ = −72 ÷ 35 = −2.06, reaching \"significantly low\"; if the normal month-to-month variation is small, the same millimeter amount yields a larger σ, so comparing σ across regions is fairer than comparing millimeters.",
"Why must we divide by the standard deviation",
"Station A has small climatological temperature variation (standard deviation 0.4°C) and station B large variation (1.5°C). With the same +1.2°C anomaly, station A's σ = 3.0 is already anomalously high while station B's σ = 0.8 is still within the normal range. The standard deviation brings the background information \"how large the local interannual variation is\" into the grading.",
"Which period should the climatological normal use?",
"Meteorological practice usually uses the average over the WMO-recommended 30-year climate normal period (e.g. 1991-2020) as the normal. Computing a short-term average yourself (e.g. the last 5 years) makes the multi-year mean drift and biases anomalies systematically to one side.",
"What σ counts as an extreme event?",
"A common convention is |σ| below 1 normal, 1-2 slightly strong or weak, 2-3 significant, and not less than 3 usually recorded in extreme climate event monitoring. Business rules vary between units; when publishing external materials, grade per your industry's rules.",
"Can this be used for heavily skewed elements like precipitation?",
"It can be computed, but note that precipitation is strongly right-skewed, so the symmetric grading of σ is distorted. In practice, percentile thresholds or the Standardized Precipitation Index (SPI) are often used for drought grading, and the anomaly percentage is better for quickly describing magnitude.",
'About the "Climate (Forecast/Anomaly/Extreme) Analysis"',
"Climate (Forecast/Anomaly/Extreme) Analysis. A free online tool with pure front-end processing; data is not uploaded, protecting privacy and security.",
],
'analysis-tide': [
"⛅ Tidal (Astronomical) Harmonic Analysis",
"Astronomical",
"Harmonic analysis decomposes the measured tide level into a superposition of several astronomical constituents: each is described by amplitude H and phase lag g, while the angular speed σ is determined by astronomical parameters (M₂ is 28.9841°/hour, S₂ 30.0000, K₁ 15.0411, O₁ 13.9430). Enter the harmonic constants of each constituent and the local mean sea level to synthesize the tide level over the next several hours and pick out high/low tide times and ranges. F below 0.25 is a regular semidiurnal tide, 0.25-1.5 an irregular semidiurnal tide, 1.5-3.0 an irregular diurnal tide, and above 3.0 a regular diurnal tide. Take the harmonic constants from charts or tide tables; results are for operational planning reference.",
'📖 View the "Tidal (Astronomical) Harmonic Analysis User Guide"',
"Tidal form factor F = (H_K1 + H_O1) ÷ (H_M2 + H_S2)",
"Mean sea level Z₀ (m)",
"M₂ amplitude H (m)",
"M₂ phase lag g (°)",
"S₂ amplitude H (m)",
"S₂ phase lag g (°)",
"K₁ amplitude H (m)",
"K₁ phase lag g (°)",
"O₁ amplitude H (m)",
"O₁ phase lag g (°)",
"Forecast duration (hours)",
"Predicted tide level",
"📚 In-depth: Tidal Harmonic Analysis and Tide Prediction",
"Enter the harmonic constants of the four main constituents and the mean sea level to synthesize the tide level over the next several hours and read the high and low tide times.",
"The synthesis directly gives the highest and lowest tide levels and the maximum tidal range in the forecast period, used to schedule berthing and construction windows.",
"Use the tidal form factor F to distinguish semidiurnal from diurnal tides and judge roughly how many high tides occur per day and what work rhythm suits.",
"Reading the tidal range from harmonic constants",
"A station has Z₀=2.00 m, M₂ amplitude 1.20 m with phase lag 0°, S₂ 0.35 m/40°, K₁ 0.30 m/120°, O₁ 0.25 m/200°. After synthesizing 24 hours, a high tide of 3.85 m (12:30) and a low tide of 0.29 m (19:00) are obtained, with a maximum tidal range of 3.56 m, clearly larger than half the sum of amplitudes, showing that several constituents superpose in this period.",
"Work window",
"A ship with a 4 m draft and a 0.5 m safety margin needs a tide height of at least 4.5 m. If the forecast shows the day's highest tide is only 3.85 m, the berthing condition is never met all day, so you must move to a date with higher tides or use a lighter-load plan.",
"How are semidiurnal and diurnal tides distinguished?",
"About 2 high tides per day is a semidiurnal tide and about 1 is a diurnal tide; determined by the moon's declination and geographic location, most of China has semidiurnal tides.",
"What is the impact of a large tidal range?",
"Ports with a large tidal range require tide-riding entry and risk grounding at low tide, so operations are strongly constrained by tidal windows.",
'About the "Tidal (Astronomical) Harmonic Analysis"',
"Tidal (Astronomical) Harmonic Analysis. A free online tool with pure front-end processing; data is not uploaded, protecting privacy and security.",
],
'apparent-temperature': [
"Apparent Temperature AT",
"Estimate the human apparent temperature from air temperature, relative humidity and wind speed using the Steadman formula.",
"Apparent Temperature (Steadman) Calculator",
"/ Apparent Temperature Calculator",
"Apparent Temperature Calculator",
'📖 View the "Apparent Temperature AT User Guide"',
"AT = apparent temperature (combining temperature, humidity and wind)",
"Wind speed ws (m/s)",
"When humidity is high and wind is low it feels hotter; when wind is strong it feels colder.",
"The simplified formula ignores the solar radiation term; use as an approximation.",
"📚 In-depth: Apparent Temperature (Australian method)",
"With no wind or radiation, estimate the apparent temperature from air temperature and vapor pressure.",
"On humid days, explain why it feels \"muggier than the actual temperature\".",
"Compare the difference in feel between dry heat and humid heat.",
"Humid-heat example",
"70%: vapor pressure e=0.7×6.105×exp(17.27×30/(237.7+30)) ≈29.6 hPa; apparent AT=30+0.33×29.6−4.0 ≈35.8°C, noticeably muggier than 30°C.",
"Dry-heat comparison",
"Also 30°C but 30% humidity: e≈12.7 hPa, AT=30+0.33×12.7−4≈30.2°C, close to the actual temperature; dry heat is not muggy.",
"Apparent temperature",
"can it be higher than the actual temperature?",
"With high humidity and no wind it is often higher than the actual temperature (poor heat dissipation); with wind the wind-chill effect makes it lower; it depends on the dominant factor.",
"How does it differ from the heat index?",
"The heat index is mostly used for high temperature and high humidity, while this formula is the simplified Australian apparent temperature; they apply to different ranges.",
],
'beaufort-scale': [
"Beaufort Wind Scale",
"Map the 10-meter wind speed (m/s) to the Beaufort wind scale (0-12) and its name.",
"Beaufort Wind Scale Calculator",
"/ Beaufort Wind Scale Calculator",
"Beaufort Wind Scale Calculator",
'📖 View the "Beaufort Wind Scale User Guide"',
"Wind speed v ↔ Beaufort number n",
"Wind speed v (at 10 m) (m/s)",
"The Beaufort scale describes sea-surface/land wind force: force 0 calm, force 12 hurricane.",
"📚 In-depth: Beaufort Wind Scale Reference",
"Convert wind speed (m/s) into a 0-12 force text description.",
"Match sea-surface/land phenomena to judge the actual wind force.",
"Set safety limits for navigation and outdoor work by wind force.",
"Converting wind speed to force",
"Wind speed 10 m/s → falls in the 8.0-10.7 range = force 5 (fresh breeze), small trees sway; 20 m/s → 17.2-20.7 = force 8 (gale), twigs break off; 25 m/s → 24.5-28.4 = force 10 (storm).",
"Back-calculating from phenomena",
"\"Sea foam in streaks, fishing boats reefing sails\" corresponds to force 8, back-calculating to a wind speed of about 17-20 m/s, consistent with the anemometer.",
"What wind speed is force 12?",
"≥32.7 m/s is force 12 (hurricane/typhoon level), rare over land with extreme damage.",
"Where does it apply?",
"It was originally designed for the sea and later extended to land phenomena; modern practice mostly uses m/s quantitatively, with the wind force as a popular reference.",
],
'cloud-base-height': [
"Cloud Base Height",
"Estimate the cloud base height from the air temperature − dew point spread using the empirical rule H ≈ (T − Td) × 125 (m/°C).",
"Cloud Base Height (Lifting Condensation Level) Estimation",
"/ Cloud Base Height Estimation Calculator",
"Cloud Base Height Estimation Calculator",
'📖 View the "Cloud Base Height User Guide"',
"Empirical rule (about 125 m/°C), related to pressure and lifting rate; an approximation.",
"📚 In-depth: Cloud Base Height Estimation",
"Estimate the cloud base height above ground from the temperature-dew point spread.",
"For aviation/general aviation, judge whether the cloud base is low enough to affect takeoff and landing.",
"Forecasters use the dry-wet bulb difference to quickly estimate cloud height.",
"Estimating cloud height from the temperature spread",
"Air temperature 20°C, dew point 10°C, spread 10°C →",
"=10/2.5×1000=4000 ft≈1220 m (empirical rate about 400 ft per 1°C of spread).",
"Low-cloud warning",
"Spread only 2°C → cloud base ≈800 ft≈240 m, a low cloud; general aviation should be cautious.",
"Where does the coefficient 2.5 come from?",
"The difference between the dry adiabatic lapse rate (9.8°C/km) and the dew-point lapse rate (about 2°C/km) is about 8°C/km, which converts to about 125 m per °C of spread; empirically 122 m (400 ft) is used.",
"Is the cloud base height accurate?",
"It is an approximation assuming clouds form from surface air lifted and condensed; it is fairly accurate for stratus, while cumulus tends to be lower due to convection.",
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
    print('gen_meteorology_b1 done')
