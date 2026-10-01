#!/usr/bin/env python3
# meteorology batch3 (6 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'meteorology')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'meteorology')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'nongyeqixiangjianyi': [
"🌾 Agrometeorological Advice",
"Enter temperature, precipitation and effective accumulated temperature, and combining the crop growth-stage requirements, get advice on sowing, harvesting, irrigation and other farm operations.",
'📖 View the "Agrometeorological Advice User Guide"',
"📐 Calculation Method",
"Agrometeorological advice is based on crop GDD: growth progress = accumulated GDD ÷ the crop's upper GDD requirement ×100, dividing stages such as sowing-emergence / seedling-tillering / jointing-heading / filling-boll / maturity; sowing suitability is judged by temperature T against the crop's sowing temperature range [sowT] and optimum range [optT]; precipitation P<10 mm indicates irrigation is needed, and harvest and waterlogging advice is given by growth stage and precipitation.",
"Maize (GDD 2500-3000)",
"Rice (GDD 2200-3500)",
"Winter wheat (GDD 2000-2200)",
"Cotton (GDD 3000-4000)",
"Current daily mean temperature T (°C)",
"Recent precipitation P (mm/week)",
"Accumulated effective growing degree days GDD (°C·d)",
"💡 Effective accumulated temperature = Σ(daily mean temperature − biological base temperature), with the base temperature usually taken as 10°C; growth progress = accumulated GDD / GDD required for maturity ×100%.",
"The GDD thresholds are reference values for common varieties; varieties with different maturity periods have different requirements",
"Precipitation is assessed on a weekly scale; in practice it must be combined with soil moisture",
"Advice is an empirical judgment based on weather conditions; for specific farm operations please consult your local agricultural technology department",
"📚 In-depth: Agrometeorological Advice",
"Give irrigation/sowing/spraying advice from soil moisture, temperature and precipitation.",
"Warning and defense against frost and dry hot wind.",
"Arrange the farming calendar by GDD and precipitation.",
"Irrigation advice",
"10cm soil moisture 12% (on the dry side) + no rain forecast for 7 days + above-normal temperature → recommend irrigating 30-40 mm and mulching to preserve moisture.",
"Frost defense",
"Predawn minimum temperature forecast 1°C, crop tolerates −1°C → critical; recommend smoke or sprinkler irrigation to raise temperature and prevent light frost.",
"What soil moisture counts as drought?",
"It varies with crop and soil texture; commonly below 60% of field capacity needs attention and below 40% is drought-stressed, with sandy soil having lower thresholds.",
"For spraying, watch wind or rain?",
"Both: wind above 4 m/s causes drift and rain within 6 hours of spraying washes it off, so choose a calm, rain-free period.",
'About the "Agrometeorological Advice"',
"Enter temperature, precipitation and effective accumulated temperature; combining the GDD requirements of crops such as maize, rice, wheat and cotton, it computes growth progress and gives advice on sowing suitability, harvest timing and irrigation/drainage.",
"GDD growth progress for multiple crops",
"Sowing temperature suitability judgment",
"Harvest timing advice",
"Irrigation and drainage guidance",
"Farm activity planning",
"Crop growth-stage monitoring",
"Irrigation and drainage decision-making",
"Agrometeorological services",
],
'capeduiliuyouxiaoweineng': [
"🧮 CAPE Convective Available Potential Energy",
"Enter the parcel temperature, environmental temperature and the pressures of the level of free convection (LFC) and equilibrium level (EL) to compute the convective available potential energy CAPE and the theoretical maximum updraft speed.",
"CAPE Convective Available Potential Energy Calculation",
"/ CAPE Instability Energy",
'📖 View the "CAPE Convective Available Potential Energy User Guide"',
"📐 Calculation Method",
"Convective available potential energy CAPE = g × (ΔT / Te) × Δz, where ΔT = parcel temperature − environmental temperature (K), Te is the environmental temperature (K), and Δz is the buoyancy layer thickness from LFC to EL (m, estimated by the hypsometric equation Δz = R_d·Tm/g·ln(p_LFC/p_EL), with Tm the mean parcel/environment temperature), g = 9.80665 m/s² and R_d = 287.04 J/(kg·K); CAPE>0 indicates available convective potential energy, and the larger it is the easier it is for severe convection to develop, often paired with CIN (convective inhibition) to judge whether strong lift is needed to trigger it. Common thresholds: 0-1000 J/kg weak (isolated thunderstorm), 1000-2500 J/kg moderate (thunderstorm likely), 2500-4000 J/kg strong (severe thunderstorm/hail), ≥4000 J/kg extreme (explosive convection).",
"Parcel temperature Tp (°C)",
"Environmental temperature Te (°C)",
"Level of free convection LFC (hPa)",
"Equilibrium level EL (hPa)",
"💡 Formula: CAPE = g × (Tp − Te) / Te × Δz, where Δz = R_d·Tm/g·ln(p_LFC/p_EL) is the buoyancy layer thickness (m), Tm is the mean parcel/environment temperature, R_d = 287.04 J/(kg·K), g = 9.80665 m/s², and temperatures are in kelvin; maximum updraft speed w_max = √(2×CAPE).",
"This tool uses a simplified constant-buoyancy method to estimate CAPE, assuming the parcel-environment temperature difference is constant across the whole LFC-EL layer",
"Actual CAPE requires full sounding data with layer-by-layer integration; this result is an approximation",
"The buoyancy layer thickness Δz is estimated by the hypsometric equation using the mean parcel/environment temperature; under warm stratification it is larger than the actual layer thickness, so the result is conservative (on the high side)",
"CAPE > 0 indicates conditional instability, and the larger the value the stronger the convective potential",
"Positive CAPE requires the parcel temperature to be higher than the environment (Tp > Te) and the LFC pressure to be greater than the EL pressure",
"📚 In-depth: CAPE Convective Available Potential Energy",
"Severe convection potential: estimate CAPE from the parcel/environment temperature and the LFC and EL pressures to judge the likelihood of thunderstorm development.",
"Updraft strength: w_max = √(2×CAPE), estimating the theoretical maximum updraft speed.",
"Potential grading: 0-1000 weak, 1000-2500 moderate, 2500-4000 strong, ≥4000 J/kg extreme, against convective strength.",
"Method and magnitude",
"Algorithm: CAPE = g×(ΔT/Te)×Δz (J/kg, g=9.80665 m/s², temperatures in kelvin), Δz is the buoyancy layer thickness from LFC→EL, estimated by the hypsometric equation Δz = R_d·Tm/g·ln(p_LFC/p_EL) (R_d=287.04 J/(kg·K), Tm the mean parcel/environment temperature); theoretical maximum updraft speed w_max = √(2×CAPE). Grading: ≤0 stable, 0-1000 weakly unstable (isolated thunderstorm), 1000-2500 moderate (thunderstorm likely), 2500-4000 strong (severe thunderstorm/hail), ≥4000 extreme (explosive convection). Note that the layer thickness uses the geometric thickness corresponding to the pressure difference, not the pressure difference itself.",
"Example: parcel 25°C, environment 20°C, LFC 700 hPa, EL 300 hPa → ΔT=5 K, Δz≈7.3 km, CAPE = 9.80665×(5/293.15)×7330 ≈ 1226 J/kg (moderately unstable), w_max ≈ 49.5 m/s (theoretical upper limit; in practice reduced by about 30%-50% due to entrainment and precipitation drag).",
"Does high CAPE mean hail is certain?",
"Not necessarily. CAPE represents only buoyancy potential; triggering conditions (low-level convergence, frontal or thermal lift), suitable 0°C/−20°C level heights and 0-6 km wind shear are also needed; with very high CAPE but large CIN or no trigger, convection often fails to develop all day.",
"Why is the theoretical maximum updraft speed on the high side?",
"w_max = √(2×CAPE) assumes all buoyancy converts to vertical kinetic energy and ignores entrainment and precipitation drag, so it is an ideal upper limit; measured updraft speeds are typically 50%-70% of this value.",
'About the "CAPE Convective Available Potential Energy"',
"Convective available potential energy (CAPE) is an important thermodynamic parameter for measuring the atmospheric convective potential. This tool takes the parcel temperature, environmental temperature and the pressures of the level of free convection (LFC) and equilibrium level (EL), and uses a simplified constant-buoyancy method to estimate the CAPE value and the theoretical maximum updraft speed, assisting severe convection weather forecasting.",
"Compute CAPE from thermodynamic formulas",
"Estimate the theoretical maximum updraft speed w_max",
"Five-level convective instability grade determination",
"Buoyancy layer thickness and convective inhibition notice",
"Severe convection weather forecast support",
"Thunderstorm and hail potential assessment",
"Meteorological teaching and sounding analysis",
"Aviation weather safety assurance",
],
'temp': [
"🌡️ Apparent Temperature (Temperature-Humidity-Wind Effect) Calculation",
"Enter the air temperature, relative humidity and wind speed to automatically compute the heat index, wind chill index and apparent temperature, and select the primary reference value by temperature range",
'📖 View the "Apparent Temperature (Temperature-Humidity-Wind Effect) Calculation User Guide"',
"📐 Calculation Method",
"The temperature-humidity-wind apparent temperature integrates three empirical models: for high temperature (T≥27°C) the heat index HI=heatIndexC(T,RH), for low temperature (T≤10°C) the wind chill index WC=windChillC(T,Vkmh), and for the middle range the apparent temperature AT=apparentTempC(T,RH,Vms); all three convert temperature, humidity and wind speed into an apparent temperature via empirical formulas, with wind speed converted as Vkmh=V×3.6 and Vms=V÷3.6.",
"Air temperature (°C)",
"💡 For high temperature and humidity use the heat index (HI), for low temperature and wind use the wind chill index (WC), and otherwise use the apparent temperature (AT). Wind chill is only valid when the wind speed is ≥ 4.8 km/h.",
"By",
"quick calculation; the result can be copied in one click",
"The heat index (Rothfusz regression) applies to high-temperature, high-humidity environments with air temperature ≥ 27°C",
"The wind chill index (TWC/NWS formula) applies to air temperature ≤ 10°C with wind speed ≥ 4.8 km/h",
"The apparent temperature (AT, Steadman) combines temperature, humidity and wind speed and has the widest applicability",
"📚 In-depth: Temperature Conversion and Apparent Temperature",
"°C/°F/K mutual conversion.",
"Compute the apparent temperature from the base air temperature with wind/humidity.",
"Compare historical temperature records.",
"Unit conversion",
"37°C=98.6°F=310.15 K; −40°C=−40°F (the only equal point); unify units in cross-unit reports to avoid misreading.",
"Apparent temperature coupling",
"Base 0°C with a wind speed of 15 m/s → wind chill ≈−12°C, a reminder to keep warm rather than just looking at the air temperature.",
"How much do K and °C differ?",
"K=°C+273.15, a constant offset; thermodynamic formulas require conversion to K.",
"Is it normal for the apparent temperature to be lower than the air temperature?",
"With wind (wind chill) or damp-cold evaporation it is lower than the actual temperature; conversely, in hot humid conditions the heat index is higher.",
'About the "Apparent Temperature (Temperature-Humidity-Wind Effect) Calculation"',
"The apparent temperature calculator combines the three factors of air temperature, relative humidity and wind speed to give the heat index (Rothfusz regression), the wind chill index (TWC/NWS) and the apparent temperature (Steadman AT), automatically selecting the primary reference value by temperature range. Runs purely on the front end; data is not uploaded.",
"Three internationally common formulas computed at once",
"Supports both m/s and km/h wind speed units",
"Intelligently select the primary reference value by temperature range",
"Show the apparent-temperature risk level in real time",
"Safety assessment for high-temperature summer work",
"Warmth reference for winter outdoor activities",
"Planning sports training intensity",
"Apparent-temperature forecast for travel",
"Air temperature in Celsius",
"Relative humidity percentage",
"Wind speed value",
],
'calc-84': [
"☢️ Solar Radiation Calculation",
"Enter the latitude, the day of the year and the sunshine hours to estimate the extraterrestrial radiation, the solar radiation reaching the surface and the photovoltaic power potential via the Angstrom-Prescott formula.",
'📖 View the "Solar Radiation Calculation User Guide"',
"Solar radiation amount = irradiance × duration",
"Latitude (°, positive for north)",
"Day of the year (1-366)",
"Actual sunshine hours n (h/day)",
"PV installed capacity (kW)",
"System efficiency (0-1)",
"💡 Formula: Ra = 37.6·dr·(ωs·sinφ·sinδ + cosφ·cosδ·sinωs); Rs = Ra·(0.25+0.5·n/N); daily generation = (Rs/3.6)·capacity·efficiency. δ is the solar declination, ωs the sunset hour angle and N the daylight duration.",
"Uses the FAO Angstrom-Prescott empirical formula with coefficients a=0.25, b=0.5 (common values for temperate zones)",
"Results may be anomalous in polar-day/polar-night regions at high latitudes and are for reference only",
"System efficiency combines inverter, line, temperature and dust losses, typically 0.75-0.85",
"📚 In-depth: Precipitation and Evaporation Balance Calculation",
"From",
"precipitation",
"and evaporation, compute the regional water balance.",
"Agricultural irrigation quota = evapotranspiration − effective precipitation.",
"Drought warning looks at a persistently negative balance.",
"Water balance",
"Monthly precipitation 40 mm, potential evapotranspiration 80 mm → balance = 40−80 = −40 mm (deficit); about 40 mm of supplemental irrigation is needed to balance crop water demand.",
"Persistent deficit",
"Three consecutive months each with a 30 mm deficit, cumulating −90 mm, lowers soil moisture and triggers a mild drought warning.",
"Is evapotranspiration the same as evaporation?",
"Evapotranspiration ET = soil evaporation + vegetation transpiration, closer to farmland water consumption than plain water-surface evaporation.",
"Does a negative balance mean irrigate?",
"It depends on crop drought tolerance and root-zone storage; short-term negative values can be covered by soil water, and only long-term negative values require irrigation.",
'About the "Solar Radiation Calculation"',
"Based on the FAO-recommended Angstrom-Prescott formula, it computes the solar declination and sunset hour angle from latitude and date, then estimates the extraterrestrial radiation, daylight duration and total solar radiation reaching the surface, converting them into peak sun hours and photovoltaic power potential.",
"Extraterrestrial radiation and daylight duration calculation",
"Surface solar radiation Rs estimation",
"Peak sun hours conversion",
"PV daily/monthly/annual power generation estimation",
"PV plant siting assessment",
"Solar energy resource survey",
"Agrometeorological sunshine analysis",
"Building daylighting and energy-saving calculation",
],
'qiyaxitongyidonglujing': [
"🎚️ Pressure System Movement Path",
"Enter the current station pressure and the pressure change over the last 3 hours to determine the pressure system type, its trend and the future weather direction.",
'📖 View the "Pressure System Movement Path User Guide"',
"Classification by station pressure: not below 1025 hPa strong high, 1020 to 1024 high, 1010 to 1019 normal, 1000 to 1009 low, below 1000 strong low; trend by 3-hour tendency: tendency not below +1.5 hPa rapid rise (high approaching, weather improving but windy), +0.5 to 1.4 slow rise, −0.5 to +0.4 steady, −1.5 to −0.6 slow fall, below −1.5 rapid fall (low or front approaching, often turning rainy and windy).",
"Current station pressure P (hPa)",
"3-hour pressure change ΔP (hPa, positive for rising, negative for falling)",
"💡 High pressure (P>1020) brings mostly fine weather and low pressure (P<1000) mostly rain; a 3-hour pressure change ΔP>1.5 means the system is approaching fast, and <-1.5 means the low is deepening and the weather is worsening.",
"Station pressure must be reduced to sea level (this tool assumes the input is sea-level pressure)",
"The 3-hour pressure tendency is an important indicator of pressure system movement and intensity change",
"The weather direction is an empirical judgment and in practice must be combined with wind field, humidity and other factors",
"📚 In-depth: Pressure System Movement Path",
"Estimate the direction and speed of high/low movement from the pressure gradient and geostrophic wind.",
"Short-term forecast of when the system will affect the local area.",
"Compare trough/ridge positions to judge weather transitions.",
"Movement estimation",
"A strong gradient 500 km west of the surface low center; the geostrophic wind steers it eastward at about 30 km/h → it affects the local area in about 16 hours, bringing precipitation.",
"Transition interpretation",
"After the westerly trough moves east and passes, ridge control follows → from rainy to fine, and the path and movement speed determine the time of transition.",
"How do pressure systems move?",
"They move approximately along the steering flow (upper-level wind), with speed related to their intensity/gradient, and in practice are disturbed by terrain and the underlying surface.",
"How many days can it forecast?",
"The path can only be roughly nowcast (1-2 days); accurate direction and speed rely on numerical models.",
'About the "Pressure System Movement Path"',
"Enter the current station pressure and the pressure change over the last 3 hours; the pressure level determines the pressure system type, the tendency judges the system's movement direction and intensity change, and an empirical outlook of the future weather direction is given.",
"Pressure system type determination",
"3-hour pressure tendency analysis",
"System movement direction judgment",
"Empirical outlook of weather direction",
"Single-station weather situation analysis",
"Marine and aviation meteorology reference",
"Surface weather chart interpretation",
"Meteorological observation teaching",
"How to use Pressure System Movement Path",
"What does Pressure System Movement Path do?",
"How do I use Pressure System Movement Path?",
"What scenarios is Pressure System Movement Path suitable for?",
],
'calc-55': [
"🧮 Moon Phase Illumination Calculation",
"Enter a date (or directly enter the moon age in days) to compute the moon age, illumination fraction, phase name and moonrise/moonset estimate",
'📖 View the "Moon Phase Illumination Calculation User Guide"',
"Moon phase illumination = (1+cos φ)/2",
"Calculate by date",
"Calculate by moon age (days)",
"Moon age (days, 0-29.53)",
"💡 The moon phase cycle (synodic month) is about 29.5306 days, with the reference new moon at 2000-01-06 18:14 UTC. Moonrise/moonset are geometric estimates, affected by latitude and season.",
"By",
"quick calculation; the result can be copied in one click",
"Illumination formula: illumination = (1 − cos(2π·moon age/29.5306)) / 2",
"Phase names are divided into 8 segments of about 3.69 days each",
'Moonrise/moonset are estimated by the rule of "about 50 minutes later each day", for reference only',
"📚 In-depth: Meteorological Parameter Conversion",
"Derive one quantity from another (e.g. dew point, vapor pressure).",
"Unify units in reports for comparison.",
"Pressure units",
"Standard atmosphere 1013.25 hPa = 760 mmHg = 1 atm; on a given day 900 hPa ≈ 675 mmHg, a low value suggesting an active weather system.",
"Temperature conversion",
"25°C = 77°F = 298.15 K; unify to K or °C in cross-unit reports to avoid misreading.",
"Is hPa the same as hectopascal?",
"Yes, 1 hPa=100 Pa=1 millibar (mbar); meteorology uses them interchangeably but the values are identical.",
"Why use K?",
"Thermodynamic formulas (such as ideal gas and saturation pressure) only hold with absolute temperature K; substituting °C directly leads to errors.",
'About the "Moon Phase Illumination Calculation"',
"Based on a date or moon age, it computes the moon phase illumination, phase name and estimated moonrise/moonset times and provides a moon phase visualization. It uses the synodic month period of 29.5306 days and the J2000 reference new moon. Runs purely on the front end; data is not uploaded.",
"Supports both date and moon-age inputs",
"Precise formula computation of illumination",
"8-segment phase naming (bilingual Chinese and English)",
"Geometric moonrise/moonset estimation",
"SVG moon-phase visualization",
"Moonlight framing planning for photography",
"Astronomical observation and moon viewing",
"Predicting light for night fishing and running",
"Reference for the lunar calendar and traditional festivals",
"Moon age in days",
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
    print('gen_meteorology_b3 done')
