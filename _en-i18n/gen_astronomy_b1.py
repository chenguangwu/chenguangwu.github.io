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
    write('apparent-magnitude-distance', build('apparent-magnitude-distance', [
        "Distance modulus (d = 10^(1 + (m-M)/5) pc)",
        "Derives the distance of a celestial object from the difference between its apparent and absolute magnitude.",
        "Apparent magnitude distance calculator",
        "/ Distance from apparent magnitude",
        "Distance from apparent magnitude",
        "📖 View the usage guide for Distance modulus (d = 10^(1 + (m-M)/5) pc)",
        "Apparent magnitude m",
        "Absolute magnitude M",
        "m - M = 5 x log10(d) - 5; d is in parsecs.",
        "When m = M, d = 10 pc.",
        "📚 Deep dive: distance modulus (d = 10^(1 + (m-M)/5) pc)",
        "From the measured apparent magnitude m and a known absolute magnitude M, quickly estimate the approximate distance of a star or galaxy, for astronomical distance measurement and magnitude conversion.",
        "Compare the distance moduli of different member stars in the same cluster to judge whether they lie at roughly the same distance layer, assisting distance calibration.",
        "In popular science or teaching, convert textbook magnitude data into intuitive distance units such as parsecs and light-years.",
        "Example: distance of a star with apparent magnitude 15 and absolute magnitude 5",
        "Substituting into the distance modulus formula (m-M) = 5 x log10(d) - 5 gives d = 10^((m-M)/5+1) = 10^((15-5)/5+1) = 10^3 = 1000 pc, or about 3260 light-years. If the absolute magnitude is -5, then (15-(-5))/5+1 = 5, so d = 100000 pc, about 326 000 light-years.",
        "Is the distance from the distance modulus accurate?",
        "It assumes interstellar extinction is negligible. In reality starlight is absorbed by dust (reddening), and uncorrected extinction causes the distance to be underestimated, which matters especially for distant stars within the Milky Way.",
        "How do apparent magnitude and absolute magnitude differ?",
        "Apparent magnitude m is the brightness seen from Earth and depends on distance; absolute magnitude M is the brightness the object would have at the standard distance of 10 pc and reflects its intrinsic luminosity.",
    ]))

    write('atmospheric-refraction', build('atmospheric-refraction', [
        "Refraction (R = 1.02 / tan(h + 10.3/(h+5.11)) arcmin)",
        "The atmosphere near the ground raises the apparent altitude of a celestial object (Bennett approximation, in arcminutes).",
        "Atmospheric refraction calculator",
        "/ Atmospheric refraction",
        "Atmospheric refraction",
        "📖 View the usage guide for Refraction (R = 1.02 / tan(h + 10.3/(h+5.11)) arcmin)",
        "True altitude angle (degrees)",
        "R = 1.02 / tan(h + 10.3/(h+5.11)) arcminutes (Bennett approximation).",
        "The lower the altitude, the greater the refraction; it approaches 0 at the zenith.",
        "📚 Deep dive: refraction (R = 1.02 / tan(h + 10.3/(h+5.11)) arcmin)",
        "When observing at low altitude angles, the atmosphere near the ground raises the apparent altitude of the object; the Bennett approximation estimates the refraction to correct the telescope pointing.",
        "When reducing the position of the Sun or Moon close to the horizon, correct the apparent position that looks flattened and raised.",
        "In astronomical navigation or geodetic observation, convert the observed apparent altitude back to the true altitude angle.",
        "Example: atmospheric refraction at a true altitude of 30 degrees",
        "Substituting into the Bennett formula R = 1.02/tan(h + 10.3/(h+5.11)) (in arcminutes), at h = 30 degrees the bracket is about 30.29 degrees, tan is about 0.5846, giving R about 1.02/0.5846, about 1.74 arcmin. The true position of the object is therefore about 1.74 arcmin lower than the observed apparent position.",
        "Why is refraction most obvious near the horizon?",
        "The path the line of sight travels through the atmosphere lengthens sharply as the altitude angle decreases, so refraction accumulates more; as the altitude approaches 0 degrees the refraction can reach about 34 arcmin, close to one apparent solar diameter.",
        "Over what range does the Bennett approximation apply?",
        "It is good enough for ordinary ground-based observation (from a few degrees up to the zenith); very close to the horizon, or when arcsecond precision is needed, a more complete refraction table is required together with pressure, temperature and water vapour.",
        "How to use Refraction (R = 1.02 / tan(h + 10.3/(h+5.11)) arcmin)",
        "The atmospheric refraction R is the apparent angular offset by which an object is raised by the atmospheric density gradient; the larger the result, the lower the true position is relative to what the eye sees.",
        "The unit is usually arcminutes or degrees. Near the horizon the refraction is about 34 arcmin (about 0.57 degrees), approaching 0 at the zenith.",
        "Scope, limits and cautions",
        "It uses the approximation R about 1.02/tan(h + 10.3/(h+5.11)), where h is the altitude angle above the horizon in degrees. Refraction varies significantly with air temperature, pressure and humidity; this formula is an average atmospheric model, and precision astronomy or geodesy must use measured meteorological corrections.",
    ]))

    write('convert-15', build('convert-15', [
        "⚡ Earthquake Magnitude and Energy Conversion (Richter to Joules)",
        "Richter to joules",
        "Earthquake magnitude and energy conversion (Richter and joules)",
        "📖 View the usage guide for Earthquake Magnitude and Energy Conversion (Richter to Joules)",
        "This tool converts between Richter or moment magnitude and released energy using the Gutenberg-Richter relation log10(E) = 4.8 + 1.5M (E in joules), and gives the corresponding TNT equivalent for reference. It is a pure front-end local conversion and the results are for popular-science estimation only.",
        "Earthquake magnitude",
        "Milli-earthquake magnitude",
        "Kilo-earthquake magnitude",
        "Milli-energy conversion",
        "Kilo-energy conversion",
        "📚 Deep dive: earthquake magnitude and energy conversion (Richter to joules)",
        "Convert the Richter or moment magnitude quoted in news reports into released energy (joules) to feel the difference in earthquake intensity intuitively.",
        "Compare the energy ratio between adjacent magnitudes to understand that each increase of 1 in magnitude means about 31.6 times more energy.",
        "In popular science or emergency drills, convert the magnitude of historic great earthquakes into a TNT equivalent for analogy.",
        "Example: energy released by a moment magnitude Mw 6.0 event",
        "Using the Gutenberg-Richter relation log10(E) = 4.8 + 1.5M (E in joules), at M = 6, log10(E) = 13.8, so E = 10^13.8, about 6.3 x 10^13 J, roughly equal to 15 kilotons of TNT. At M = 7 it is about 2.0 x 10^15 J, about 31.6 times the energy of a magnitude 6 event.",
        "How much does the energy differ per magnitude unit?",
        "The energy differs by about 10^1.5, or about 31.6 times; a difference of 2 magnitudes is about 1000 times. So the destructive power of a great earthquake far exceeds the intuition given by the difference in the magnitude number.",
        "Are the Richter magnitude and the moment magnitude the same thing?",
        "No. The Richter magnitude suits small local earthquakes and saturates for large ones; modern large earthquakes mostly use the moment magnitude Mw, which better reflects the energy actually released by the rupture.",
        "About the Earthquake Magnitude and Energy Conversion (Richter to Joules)",
        "Earthquake Magnitude and Energy Conversion (Richter to Joules). A free online tool with pure front-end processing; data is not uploaded, protecting your privacy and security.",
        "How to use the Earthquake Magnitude and Energy Conversion (Richter to Joules)",
        "From",
        "To",
    ]))

    write('convert-17', build('convert-17', [
        "⏲️ Time Zone Converter (built-in world time zones)",
        "World time zone conversion (standard time, daylight saving time not included)",
        "📖 View the usage guide for the Time Zone Converter (built-in world time zones)",
        "This tool converts time between built-in world time zones by UTC offset and adjusts according to the daylight saving rules of the selected date. It is a pure front-end local calculation and does not change the time zone setting of the device.",
        "Anchorage (UTC-9)",
        "Brasilia (UTC-3)",
        "Dubai (UTC+4)",
        "Dhaka (UTC+6)",
        "Tokyo/Seoul (UTC+9)",
        "Solomon Islands (UTC+11)",
        "Auckland (UTC+12)",
        "📚 Deep dive: Time Zone Converter (built-in world time zones)",
        "When planning a trip across time zones or scheduling an international meeting, convert the departure location",
        "into the local time at the destination.",
        "In astronomical observation planning, convert the local observation time to UTC to align star catalogues, ephemerides and observatory coordinates.",
        "When reading overseas events, live streams or deadlines, quickly obtain the corresponding local time.",
        "Example: converting Beijing time 12:00 to UTC",
        "Beijing is UTC+8, so subtracting 8 hours gives UTC 04:00. If the destination is UTC-5 (such as US Eastern Standard Time), the difference from UTC+8 is 13 hours, so Beijing time 12:00 corresponds to 23:00 of the previous day there.",
        "How does daylight saving time affect the conversion?",
        "Regions observing daylight saving advance the clock by 1 hour in summer, so the corresponding UTC offset changes (for example UTC-5 becomes UTC-4 during daylight saving); it must be judged by the date.",
        "Why is UTC commonly used in astronomical observation?",
        "Global observations and ephemerides use UTC uniformly, which avoids confusion from local time zones and daylight saving and facilitates continuous time counting with the Julian day.",
        "About the Time Zone Converter (built-in world time zones)",
        "Time Zone Converter (built-in world time zones). A free online tool with pure front-end processing; data is not uploaded, protecting your privacy and security.",
    ]))

    write('convert-18', build('convert-18', [
        "🎚️ Atmospheric Pressure and Altitude Converter (barometer reading)",
        "Barometer reading",
        "📖 View the usage guide for the Atmospheric Pressure and Altitude Converter (barometer reading)",
        "This tool converts between a barometer reading and altitude using the pressure-altitude approximation h = 44330 x (1 - (P/P0)^(1/5.255)), with P0 taken as the standard sea-level pressure of 1013.25 hPa. It is a pure front-end local calculation, and the result is affected by temperature, pressure and weather, so it is for reference only.",
        "Atmospheric pressure",
        "Milli-atmospheric pressure",
        "Kilo-atmospheric pressure",
        "Altitude conversion",
        "Milli-altitude conversion",
        "Kilo-altitude conversion",
        "📚 Deep dive: Atmospheric Pressure and Altitude Converter (barometer reading)",
        "When mountaineering or surveying in the field, infer the current altitude from the barometer reading.",
        "Convert a known altitude into standard atmospheric pressure as a reference baseline for meteorological or instrument calibration.",
        "In altitude estimation for drones, sounding balloons and similar, use the pressure change to judge ascent and descent.",
        "Example: the altitude corresponding to a pressure of 540 hPa",
        "Using the isothermal approximation h = 44330 x (1 - (P/P0)^(1/5.255)) with P0 = 1013.25 hPa: P/P0 is about 0.533, its 1/5.255 power is about 0.879, so h is about 44330 x (1 - 0.879), about 5360 m.",
        "Is estimating altitude from pressure accurate?",
        "It is markedly affected by weather systems, temperature and humidity. At the same altitude, high and low pressure weather can shift the reading by several hundred metres, so a temperature correction or a measured sea-level pressure is needed.",
        "Why does pressure drop noticeably at high altitude?",
        "The weight of the atmosphere decreases with height, roughly halving for every 5500 m of ascent; as altitude increases the air column becomes shorter and the density falls, so the reading drops accordingly.",
        "About the Atmospheric Pressure and Altitude Converter (barometer reading)",
        "Atmospheric Pressure and Altitude Converter (barometer reading). A free online tool with pure front-end processing; data is not uploaded, protecting your privacy and security.",
    ]))


if __name__ == '__main__':
    main()
