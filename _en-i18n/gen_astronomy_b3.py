#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'astronomy')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'astronomy')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
DISCL = "Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected."
EXTRA = {}
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
    out = {'slug': slug, 'industry': 'astronomy', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('humidity-calculator', build('humidity-calculator', [
        "⛅ Relative Humidity Calculator (dry- and wet-bulb temperature method)",
        "Based on the dry-bulb and wet-bulb temperatures, uses the Sprung formula and the Magnus saturation vapour pressure formula to calculate air humidity parameters",
        "Relative humidity calculator",
        "/ Relative humidity calculator",
        "📖 View the usage guide for the Relative Humidity Calculator (dry- and wet-bulb method)",
        "Indoor in summer 25/20",
        "Indoor in spring and autumn 20/14",
        "Early winter 10/7",
        "Hot humid day 30/28",
        "Cold dry day 5/3",
        "Dry-bulb temperature t (degrees Celsius)",
        "Wet-bulb temperature t' (degrees Celsius)",
        "Atmospheric pressure p (hPa)",
        "Dew point temperature Td",
        "Vapour pressure e",
        "Relative humidity scale",
        "Saturation vapour pressure (Magnus formula):",
        "Actual vapour pressure (Sprung formula):",
        ", where A = 0.000662",
        "Relative humidity:",
        "Dew point temperature:",
        "Absolute humidity:",
        "📚 Deep dive: Relative Humidity Calculator (dry- and wet-bulb method)",
        "Use the dry-bulb and wet-bulb temperatures with the Magnus saturation vapour pressure formula and the Sprung equation to obtain the relative humidity and dew point.",
        "Monitor air moisture in meteorological observation, greenhouses or storage environments.",
        "Quantify how muggy it feels, to assist comfort and heat stress assessment.",
        "Example: relative humidity at a dry bulb of 30 degrees Celsius and a wet bulb of 25 degrees Celsius",
        "First use the Magnus formula to compute the",
        "saturation vapour pressure e_s",
        "(30) and the wet-bulb equilibrium value e_w(25) together with the wet-bulb coefficient, then substitute into the Sprung relation RH = (e_w - A x P x (T - T_w)) / e_s x 100%. A typical result is about 65%-70%, corresponding to a dew point of about 23-24 degrees Celsius.",
        "Why is the wet-bulb temperature lower than the dry-bulb temperature?",
        "Evaporation from the wet-bulb gauze absorbs heat and lowers the temperature; the drier the air, the stronger the evaporation and the larger the difference, so the dry-wet bulb difference can be inverted to give the humidity.",
        "What does a relative humidity of 100% mean?",
        "The air is saturated and water vapour begins to condense; at this point the dew point equals the current temperature, and further cooling produces condensation.",
        "The wet-bulb temperature should be less than or equal to the dry-bulb temperature; otherwise the input is flagged as abnormal",
        "The dry- and wet-bulb method applies when the wet-bulb temperature is above 0 degrees Celsius (the wet bulb is not frozen); when it is frozen, the saturation vapour pressure over ice must be used",
        "The psychrometric constant A = 0.000662 applies to a well-ventilated louvered screen or an Assmann ventilated psychrometer",
        "The results are for reference only; professional meteorological applications should rely on measured instrument readings",
        "About the Relative Humidity Calculator (dry- and wet-bulb method)",
        "The relative humidity calculator is based on the dry- and wet-bulb method: enter the dry-bulb temperature, wet-bulb temperature and atmospheric pressure to calculate the relative humidity, dew point temperature, vapour pressure and absolute humidity of the air. It suits meteorological observation, HVAC, agricultural greenhouses, moisture-proof storage and similar scenarios. Pure front-end processing; data is not uploaded, protecting your privacy and security.",
        "Dry- and wet-bulb method, compliant with meteorological standards",
        "Uses the Magnus saturation vapour pressure formula with reliable accuracy",
        "Four humidity parameters in a single calculation",
        "Real-time calculation, results as you type",
        "Visual humidity scale and comfort assessment",
        "Meteorological observation and data recording",
        "HVAC design and commissioning",
        "Environmental monitoring in agricultural greenhouses",
        "Moisture-proof storage and archive protection",
        "Laboratory environmental control",
        "Teaching demonstrations and meteorology study",
        "Calculation principle",
        "The dry- and wet-bulb method infers air humidity from the difference between the readings of the dry-bulb and wet-bulb thermometers. Evaporation of water lowers the wet-bulb temperature; the drier the air, the faster the evaporation and the larger the temperature difference. First the Sprung formula gives the actual vapour pressure e = e_s(t') - A x p x (t - t'), which is then compared with the saturation vapour pressure e_s(t) at the dry-bulb temperature (Magnus formula) to obtain the relative humidity.",
        "How to use the Relative Humidity Calculator (dry- and wet-bulb method)",
    ]))

    write('index', build('index', [
        "🔭 Astronomical Observation Tools",
        "Astronomical observation",
        "Astronomical Observation Tools",
        "Based on the NOAA solar algorithms, accurately calculates sunrise and sunset, solar noon, day length and the real-time solar position from the date, latitude and longitude and time zone",
        "Enter the observation date, latitude and longitude and the light pollution environment to estimate the moon phase, moonrise and moonset times and a composite observation condition score, helping amateur astronomers choose an ideal observing window according to the IDA dark-sky standard.",
        "Enter the date, time, latitude and longitude to calculate the solar altitude angle, azimuth angle, declination and hour angle, and draw the solar track for the day.",
        "Relative humidity calculator",
        "Based on the dry-bulb and wet-bulb temperatures, uses the Sprung formula and the Magnus saturation vapour pressure formula to calculate air humidity parameters",
        "Earth curvature calculator",
        "Enter the observer height and the target distance or height to calculate the visible horizon distance, the Earth curvature drop and the hidden height of the target, and draw a curvature diagram.",
        "Moon illumination fraction calculator",
        "Illuminated fraction (k = (1 - cos(2 x pi x D/29.53)) / 2)",
        "Kepler's third law orbital period calculator",
        "Orbital period (T = 2 x pi x sqrt(a^3 / (G x M)))",
        "Apparent magnitude distance calculator",
        "Distance modulus (d = 10^(1 + (m-M)/5) pc)",
        "Hubble redshift distance calculator",
        "Approximate distance (d = c x z / H0)",
        "Stellar parallax distance calculator",
        "Parallax distance (d = 1 / p pc)",
        "Light travel time calculator",
        "Propagation time (t = d / c)",
        "Enter the observer's eye height above the ground and estimate, from the Earth's curvature, the farthest visible horizon distance; suitable for quick estimates of visibility at sea, for sightseeing and for radio and television coverage.",
        "Atmospheric refraction calculator",
        "Refraction (R = 1.02 / tan(h + 10.3/(h+5.11)) arcmin)",
        "Solar declination approximation calculator",
        "Declination (delta about 23.44 degrees x sin(360 degrees x (284+N)/365))",
        "Universal gravitation calculator",
        "Gravitation (F = G x m1 x m2 / r^2)",
        "Schwarzschild radius calculator",
        "Event horizon (r_s = 2 x G x M / c^2)",
        "Converts time between built-in world time zones, supporting daylight saving and standard time switching; enter the time in one place to get the corresponding time in other cities, suitable for cross-time-zone travel and meeting scheduling.",
        "Converts a barometer reading into the corresponding altitude, or conversely estimates standard atmospheric pressure from the altitude, for height estimation in field surveying, mountaineering and meteorological observation.",
        "Earthquake magnitude and energy conversion (Richter and joules)",
        "Estimates tide height, tidal range, spring and neap tides and the tide type from the lunar and solar tidal forces (equilibrium tide theory), and plots a 24-hour tide curve.",
        "Magnitude brightness comparator",
        "Calculates the brightness ratio of two celestial bodies from their apparent magnitudes. Formula: F2/F1 = 2.512^(m1-m2), that is, the brightness ratio is 2.512 raised to the magnitude difference. The smaller the magnitude, the brighter the object; a difference of 5 magnitudes means a brightness ratio of 100.",
        "Meteorite impact crater estimator",
        "Enter meteorite parameters to estimate the impact kinetic energy, TNT equivalent, crater diameter, depth and damage radius based on the Schmidt-Holsapple scaling law. All calculations are performed locally in the browser.",
        "Kepler equation solver",
        "M = E - e x sinE (Newton iteration for E)",
        "About the Astronomical Observation Tools",
        "The Astronomical Observation tool collection includes 23 free online tools covering the common calculation, conversion and lookup needs in astronomical observation scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you will find practical, ready-to-use tools here. All tools run purely in the front end, and data is not uploaded to a server, protecting your privacy and security.",
        "The astronomical observation tools collected on this page include (some representative tools):",
        "These tools help you complete common astronomical observation tasks quickly, with no need to memorize complex formulas or convert manually - just enter the values and get the result.",
        "Do the astronomical observation tools require download or registration?",
        "No. All the astronomical observation tools on this page are pure front-end online tools; just open the page and use them directly, with no software to install, no account to register and no data uploaded.",
        "Are the calculation results of the astronomical observation tools accurate? Is the data secure?",
        "The tools calculate locally in your browser based on public mathematical formulas and general industry standards, and the results are available instantly. All computation is done locally on your device, and data is not uploaded to a server, so your privacy and security are protected.",
    ]))

    write('kepler-equation', build('kepler-equation', [
        "M = E - e x sinE (Newton iteration for E)",
        "Numerically solves the eccentric anomaly E from the mean anomaly M and the eccentricity e.",
        "Kepler equation solver",
        "/ Kepler equation",
        "Kepler equation",
        "📖 View the usage guide for the Kepler equation solver",
        "M = E - e x sinE; Newton iteration converges quickly. With e = 0.1 and M = 90 degrees, E is about 95.7 degrees.",
        "Mean anomaly M (degrees)",
        "Eccentricity e",
        "M = E - e x sinE; Newton iteration converges quickly.",
        "With e = 0.1 and M = 90 degrees, E is about 95.7 degrees.",
        "📚 Deep dive: Kepler equation solver",
        "Given the mean anomaly M and the eccentricity e, solve the eccentric anomaly E numerically by iteration, to derive the orbital positions of planets and satellites.",
        "In two-body orbit propagation, map time to the true anomaly and the spatial position.",
        "In teaching demonstrations, observe the non-uniform motion of high-eccentricity orbits such as comets.",
        "Example: solve for E with M = 1.0 rad and e = 0.3",
        "Solve M = E - e x sinE, that is E - 0.3 x sinE = 1.0. Using Newton iteration with the initial value E0 = 1.0: E1 = 1.0 - (1.0 - 0.3 x sin1.0 - 1.0)/(1 - 0.3 x cos1.0) = 1.0 + 0.2521/1.1620, about 1.2170; one more iteration gives E about 1.2189 rad.",
        "Why is iteration needed instead of a direct solution?",
        "E appears both in the linear term and",
        "inside the sine, so there is no elementary closed-form solution; the Newton-Raphson iteration is usually used because it converges quickly.",
        "Is it still accurate when the eccentricity e is large?",
        "The iterative method still applies, but the initial value must be good (for high e use M + 0.85e); near-parabolic orbits need a special initial value to avoid slow convergence.",
    ]))

    write('kepler-third-period', build('kepler-third-period', [
        "Orbital period (T = 2 x pi x sqrt(a^3 / (G x M)))",
        "The period of a circular orbit around a central body is determined by the semi-major axis and the central mass.",
        "Kepler's third law orbital period calculator",
        "/ Orbital period (Kepler III)",
        "Orbital period (Kepler III)",
        "📖 View the usage guide for Orbital period (T = 2 x pi x sqrt(a^3 / (G x M)))",
        "Semi-major axis (m)",
        "T = 2 x pi x sqrt(a^3/GM); the Earth's orbit around the Sun is about 365.2 days.",
        "Taking a = 1 AU and M = the solar mass gives one year.",
        "📚 Deep dive: orbital period (T = 2 x pi x sqrt(a^3 / (G x M)))",
        "From the semi-major axis a and the central body mass M, use Kepler's third law to obtain the circular or near-circular",
        "orbital period",
        "Compare how the orbital periods of Earth satellites, planets or exoplanets vary with radius.",
        "In mission design, estimate the orbital period of a probe around a given body.",
        "Example: the period of a low Earth circular orbit (a about 6771 km)",
        "If the semi-major axis doubles, how much does the period change?",
        "The period is proportional to a^(3/2), so doubling a makes the period 2^1.5, about 2.83 times longer.",
        "Is M in the formula the mass of the central body or of the satellite?",
        "It is the mass of the central body; when the satellite mass is not negligible use the total mass (M + m), though satellites are generally far smaller than the central body and can be ignored.",
    ]))

    write('light-travel-time', build('light-travel-time', [
        "Propagation time (t = d / c)",
        "The time light needs to cover a given distance in a vacuum.",
        "Light travel time calculator",
        "/ Light travel time",
        "Light travel time",
        "📖 View the usage guide for Propagation time (t = d / c)",
        "t = d/c; the light travel time for 1 AU is about 8.32 minutes.",
        "📚 Deep dive: propagation time (t = d / c)",
        "Convert astronomical distances into the time light needs to cover them, giving an intuitive sense of the space and time scales of the universe.",
        "Calculate the one-way delay of interplanetary communication, such as the round-trip delay of commands sent to Mars.",
        "In popular science, illustrate the look-back effect that seeing something 1 light-year away is like seeing 1 year into the past.",
        "Example: the time for sunlight to reach the Earth",
        "The mean Sun-Earth distance is about 1.496 x 10^11 m and c = 2.998 x 10^8 m/s, so t = d/c is about 499 s, about 8.3 minutes. The Sun we see is therefore the Sun of about 8 minutes ago.",
        "Why is it called light travel time?",
        "Information travels at a finite speed of light, so a distant object observed is actually as it was in the past; the farther away it is, the earlier the epoch we see.",
        "How much is 1 light-year?",
        "One light-year is about 9.46 x 10^12 km, about 63241 times the Sun-Earth distance; the nearest star, Proxima Centauri, is about 4.24 light-years away.",
    ]))


if __name__ == '__main__':
    main()
