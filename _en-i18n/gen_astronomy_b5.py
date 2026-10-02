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
    write('solar-elevation', build('solar-elevation', [
        "📏 Solar Elevation Angle Calculator",
        "Enter the date, time, latitude and longitude to calculate the solar elevation angle, azimuth angle, declination and hour angle, and draw the solar track for the day.",
        "Core formulas (by input variable): Math.round(rect.height x dpr); Math.round(rect.width x dpr); xOf(((hour % 24) + 24) % 24)",
        "📖 View the usage guide for the Solar Elevation Angle Calculator",
        "Harbin",
        "Urumqi",
        "Lhasa",
        "Haikou",
        "Sydney",
        "Time (local time)",
        "Latitude (degrees, north positive)",
        "Longitude (degrees, east positive)",
        "Results are calculated automatically once the parameters are entered and update in real time.",
        "📐 Real-time calculation results",
        "🌅 Sunrise / noon / sunset",
        "📊 Solar track chart for the day",
        "The curves show how the solar elevation and azimuth angles change over the day; the vertical dashed lines mark sunrise, noon, sunset and the current moment.",
        "Solar elevation angle (left axis 0-90 degrees)",
        "Solar azimuth angle (right axis 0-360 degrees, north = 0)",
        "📋 Hourly data",
        "📚 Deep dive: Solar Elevation Angle Calculator",
        "Enter the date, time, latitude and longitude to calculate the solar elevation angle, azimuth angle, declination and hour angle.",
        "In photovoltaics, building daylighting or crop growing, assess the sunlight conditions in different seasons.",
        "Draw the solar track for the day to assist shading and window orientation design.",
        "Example: noon solar elevation at the equator on an equinox",
        "With declination delta about 0 and hour angle omega = 0 (noon), the elevation alpha = 90 degrees - |phi - delta| = 90 - |0 - 0| = 90 degrees, so the Sun is almost directly overhead; at latitude phi = 40 degrees, alpha = 90 - 40 = 50 degrees.",
        "What is the difference between the elevation angle and the azimuth angle?",
        "The elevation angle is the Sun's angle above the horizon, while the azimuth angle is its direction on the horizon circle (east, south, west); together they locate the Sun.",
        "Why is the Sun lower in winter?",
        "In winter the solar declination is negative (in the southern hemisphere), making the noon elevation about 2 x 23.44, about 47 degrees lower than in summer, so the sunlight is more oblique and the days shorter.",
        "Tool introduction and usage",
        "Based on classic astronomical formulas, the Solar Elevation Angle Calculator computes the position of the Sun in the sky in real time from the date, local time, latitude and longitude, including the elevation angle, azimuth angle, declination and hour angle, and automatically derives sunrise, sunset and the noon solar elevation.",
        "Solar declination by the Cooper formula",
        "Hour angle and solar time conversion",
        "Real-time calculation of the elevation and azimuth angles",
        "Sunrise, sunset and day length derivation",
        "Canvas solar track chart",
        "Preset coordinates for common cities",
        "Hourly data table",
        "Photovoltaic panel orientation and tilt design",
        "Building sunlight and daylighting analysis",
        "Planning the golden hour for photography",
        "Outdoor activities and campsite siting",
        "Agricultural greenhouse light assessment",
        "Astronomical observation and teaching demonstrations",
        "Calculation formulas",
        "Solar declination delta = 23.45 degrees x sin(360 degrees x (n + 284) / 365)",
        "Hour angle H = 15 degrees x (solar time - 12)",
        "Elevation angle alpha = arcsin(sin delta x sin phi + cos delta x cos phi x cos H)",
        "Azimuth angle A = arctan2(sin H, cos H x sin phi - tan delta x cos phi) + 180 degrees",
        "Here n is the day of the year and phi is the latitude. The time zone is estimated from the longitude (round(longitude/15)), and the equation of time (EoT) correction is applied.",
        "The calculation uses a simplified astronomical model; the results are for reference only and do not replace professional astronomical data",
        "The time zone is estimated automatically from the longitude; for regions spanning time zones, convert according to the local legal time",
        "Altitude, atmospheric refraction and daylight saving time are not considered, so sunrise and sunset may be off by a few minutes",
    ]))

    write('stellar-parallax', build('stellar-parallax', [
        "Parallax distance (d = 1 / p pc)",
        "The annual parallax p (in arcseconds) and the distance (in parsecs) are reciprocals of each other.",
        "Stellar parallax distance calculator",
        "/ Stellar parallax distance measurement",
        "Stellar parallax distance measurement",
        "📖 View the usage guide for Parallax distance (d = 1 / p pc)",
        "Parallax p (arcsec)",
        "d(pc) = 1/p(arcsec); p = 0.1 arcsec corresponds to 10 pc.",
        "📚 Deep dive: parallax distance (d = 1 / p pc)",
        "Enter the annual parallax angle p (arcseconds) of a star and use d = 1/p to obtain the distance in parsecs.",
        "Understand how satellites such as Hipparcos and Gaia measure the distances of nearby stars by the parallax method.",
        "Compare the distance scales corresponding to different parallaxes, and learn the range limit of the parallax method.",
        "Example: the distance of a star with a parallax of 0.1 arcsec",
        "d = 1/p = 1/0.1 = 10 pc, about 32.6 light-years. If the parallax is 0.01 arcsec, then d = 100 pc, about 326 light-years. A smaller parallax means a more distant star, and the measurement error is larger too.",
        "What is annual parallax?",
        "The Earth's orbit around the Sun makes a nearby star show, over half a year relative to the distant background, a maximum",
        "angular displacement",
        "of which half is the annual parallax.",
        "How far can the parallax method reach?",
        "Ground-based and early satellite measurements reached only a few hundred pc; the Gaia satellite has pushed precise parallax out to several thousand pc, and beyond that the error is too large, so other distance methods must be used.",
    ]))

    write('sunrise-sunset', build('sunrise-sunset', [
        "🧮 Sunrise and Sunset Time Calculator",
        "Based on the NOAA solar algorithms, accurately calculates sunrise and sunset, solar noon, day length and the real-time solar position from the date, latitude and longitude and time zone",
        "Core formulas (by input variable): now.getUTCHours() x 60 + now.getUTCMinutes() + now.getUTCSeconds() / 60; ((utcMin + tz x 60) % 1440 + 1440) % 1440; 720 - 4 x lon - p.EoT + tz x 60",
        "📖 View the usage guide for the Sunrise and Sunset Time Calculator",
        "Time zone (UTC offset)",
        "Common city presets",
        "📍 Beijing",
        "📍 Shanghai",
        "📍 New York",
        "📍 London",
        "📍 Tokyo",
        "🌐 Locate my current position",
        "🕐 Daylight timeline for the day",
        "The orange area is the daytime period (including the atmospheric refraction correction); the red line marks solar noon and the purple line the current moment",
        "🧭 Current solar position",
        "The solar elevation and azimuth angles calculated from the solar parameters of the selected date and the current local time",
        "Sky dome projection (centre = directly overhead, edge = horizon)",
        "📐 Notes on the NOAA solar algorithm",
        "Calculation flow",
        "1. Compute the",
        "Julian day (JD)",
        "from the Gregorian date, then obtain the",
        "Julian century T = (JD - 2451545) / 36525",
        "2. From T compute the",
        "geometric mean longitude of the Sun L0",
        "the mean anomaly M",
        "and the Earth's orbital eccentricity e",
        "3. The equation of centre gives the",
        "true longitude of the Sun",
        ", and after nutation and aberration corrections the",
        "apparent longitude",
        "4. From the",
        "obliquity of the ecliptic",
        "and the apparent longitude, obtain the",
        "solar declination delta",
        "5. From L0, M, e and the obliquity, obtain the",
        "equation of time EoT",
        "(minutes)",
        "6. Hour angles of sunrise and sunset:",
        "Solar noon = 720 - 4 x longitude - EoT + time zone x 60",
        "Sunrise = noon - 4 x H",
        "Sunset = noon + 4 x H",
        "Key parameters",
        ": the zenith angle for sunrise and sunset, = 90 degrees + 0.266 degrees (solar semi-diameter) + 0.566 degrees (atmospheric refraction), accounting for the fact that the Sun can be seen before it has fully risen above the horizon.",
        ": the deviation of the Sun's actual position from clock time caused by the elliptical orbit and the tilt of the Earth's axis, ranging from about -14 to +16 minutes over the year.",
        "Solar noon",
        ": the moment when the Sun reaches its highest point on the local meridian; it is not necessarily exactly 12:00 and depends on the difference between the longitude and the central meridian of the time zone.",
        "The results are theoretical astronomical values that do not account for terrain obstruction, altitude or local weather. The accuracy of the sunrise and sunset times is about 1-2 minutes, with slightly larger errors at high latitudes.",
        "📚 Deep dive: Sunrise and Sunset Time Calculator",
        "Based on the NOAA solar algorithms, calculates sunrise, sunset, solar noon and day length from the date, latitude and longitude and time zone.",
        "Plan outdoor shooting, sailing or daily routines, and understand how day length varies with the seasons.",
        "Combine altitude and terrain obstruction for a more realistic estimate of the visible period.",
        "Example: sunrise at about 4:30 at latitude 40 degrees north on the summer solstice",
        "Under the NOAA algorithm, at latitude 40 degrees north on the summer solstice (delta about +23.44 degrees) the day length reaches about 15 hours, with sunrise at about 4:30 local time and sunset at about 19:30; at the winter solstice the day length is about 9 hours, with sunrise at about 7:30.",
        "Why does the algorithm distinguish civil, nautical and astronomical twilight?",
        "They are divided by the Sun's centre being 6, 12 and 18 degrees below the horizon, corresponding to the twilight conditions needed for different activities.",
        "Do altitude and terrain affect the result?",
        "Yes. The geometric horizon on a mountain or at the coast differs from standard sea level, so terrain obstruction must be added to obtain the actual visible sunrise and sunset.",
        "Positive latitude means the northern hemisphere and negative the southern hemisphere; positive longitude means east and negative west",
        "The time zone supports decimals (such as +5.5 for India and +6.5 for Myanmar), in the range -12 to +14",
        "Locate my current position requires the browser geolocation permission and only works in an HTTPS environment",
        "It is recommended to use a mainstream browser (the last two versions of Chrome, Safari, Firefox or Edge)",
        "About the Sunrise and Sunset Time Calculator",
        "The Sunrise and Sunset Time Calculator is an online astronomy tool that uses the standard solar calculation algorithm published by the US National Oceanic and Atmospheric Administration (NOAA). From the date, latitude, longitude and time zone entered by the user, it accurately calculates the sunrise time, sunset time, solar noon, day length and sunshine duration for any location on that day, and shows the current solar elevation and azimuth angles in real time. All calculations are performed locally in the browser, with no network needed and no data uploaded.",
        "NOAA standard solar algorithm, accurate to about 1-2 minutes",
        "Built-in presets for Beijing, Shanghai, New York, London, Tokyo and other cities",
        "Supports one-click browser geolocation to get the current position",
        "Real-time calculation and visualization of the solar elevation and azimuth angles",
        "The daylight timeline for the day shows the daytime distribution intuitively",
        "Supports fractional time zones (such as +5.5 and +6.5)",
        "Automatic detection of polar day and polar night",
        "Pure front-end operation, data not uploaded, safe and reliable",
        "Planning the golden hour and blue hour for photography",
        "Arranging daylight activities for travel",
        "Building daylighting and photovoltaic power assessment",
        "Calculating light cycles for crop growing",
        "Astronomical observation and outdoor activity planning",
        "Learning astronomy, geography and the laws of solar motion",
        "Calculation principle",
        "The tool first converts the Gregorian date into the Julian day (JD), then obtains the Julian century T, and computes in turn the geometric mean longitude of the Sun, the mean anomaly and the Earth's orbital eccentricity; through the equation of centre and nutation and aberration corrections it obtains the apparent longitude of the Sun, and combined with the obliquity of the ecliptic it derives the solar declination and the equation of time (EoT). Sunrise and sunset use a zenith angle of 90.833 degrees (including the solar semi-diameter and atmospheric refraction corrections), and through the hour angle formula",
        "it obtains the hour angles of sunrise and sunset, and hence the local sunrise, sunset and solar noon times.",
    ]))

    write('tide-estimator', build('tide-estimator', [
        "📏 Tide Height Estimator",
        "Estimates the tide height, tidal range, spring and neap tides and the tide type from the lunar and solar tidal forces (equilibrium tide theory), and plots a 24-hour tide curve.",
        "Core formulas (by input variable): julianDay(+parts[0], +parts[1], +parts[2] + 0.0); wSemi x cos(2 x pi x (t - phaseS)/M2_PERIOD); sqrt(L x L + S x S + 2 x L x S x cos(2 x phaseRad))",
        "📖 View the usage guide for the Tide Height Estimator",
        "Mean tidal range (m)",
        "Calculate the moon phase automatically (derived from the date)",
        "Select the moon phase manually",
        "Start estimation",
        "Reset to today",
        "24-hour tide height curve",
        "Unit: metres (relative to mean sea level)",
        "Tide curve",
        "High tide",
        "Low tide",
        "Mean sea level",
        "High tide / low tide time estimation",
        "This tool is based on the",
        "equilibrium tide theory",
        "and considers only the tidal forces of the Moon and the Sun, the distance variation and the combined effect of the moon phase. Actual tides are strongly affected by local factors such as seabed topography, coastline shape and water depth resonance, so the results are",
        "for reference and teaching demonstration only",
        "and must not be used for navigation, engineering or disaster-prevention decisions.",
        "Pure front-end calculation; all data is processed locally in the browser and is not uploaded to a server",
        "For the mean tidal range, enter the long-term mean tidal range of the location (the long-term average of the height difference between high and low tide), used to convert the theoretical equilibrium tide into the local actual magnitude",
        "The moon phase, the Moon-Earth distance and the Sun-Earth distance are derived automatically from the date (simplified astronomical formulas, error about 1-3%)",
        "The tide type by latitude is an approximate model; the real tide type depends on the geographic conditions of the sea area",
        "The high and low tide times are theoretical estimates; actual tide times are affected by the tidal harmonic constants and harbour tide corrections",
        "📚 Deep dive: Tide Height Estimator",
        "Based on the equilibrium tide theory of lunar and solar tidal forces, estimate the tide height, tidal range and spring or neap tides.",
        "Judge the tide strength at syzygy (spring tide) and at the quarters (neap tide), to assist shore gathering and navigation.",
        "Draw a 24-hour tide curve to understand the difference between semidiurnal and diurnal tide types.",
        "Example: spring tides around syzygy",
        "The lunar tidal force is about 2.2 times that of the Sun; at new moon and full moon the solar and lunar tidal forces point the same way and add up, producing the spring tide with the largest range; at the first and last quarters the two are perpendicular, giving the smallest range, the neap tide. A semidiurnal tide has about two rises and two falls per day, with a period of about 12 hours 25 minutes.",
        "Why are there two tides a day?",
        "In the Moon's tidal force field the Earth bulges both on the side facing the Moon and on the side facing away, and one rotation passes through both bulges, giving a high tide about every 12 h 25 m.",
        "What is the equilibrium tide theory?",
        "It treats sea water as an ideal fluid covering the whole Earth and estimates the tide height from the gravitational balance of the bodies alone, ignoring the distribution of land and sea and inertia; real tides need terrain and resonance corrections added.",
        "About the Tide Height Estimator",
        "The Tide Height Estimator is an online tidal calculation tool based on the tidal forces of celestial bodies. From the date, moon phase, mean tidal range and latitude entered, it combines the tidal forces of the Moon and the Sun (equilibrium tide theory) to estimate the combined tide height and predict the tidal range, judges whether the day has a syzygy spring tide or a quadrature neap tide, determines the tide type by latitude (semidiurnal, mixed or diurnal), and finally draws a 24-hour tide height curve with Canvas and estimates the times of high and low tide. All calculations are completed locally in the browser, and data is not uploaded, protecting your privacy.",
        "Lunar tidal force calculation (including Moon-Earth distance variation)",
        "Solar tidal force calculation (including Sun-Earth distance variation)",
        "Combined lunar and solar tide height and tidal range prediction",
        "Automatic judgement of syzygy spring tide and quadrature neap tide",
        "Tide type determined by latitude",
        "Canvas visualization of the 24-hour tide curve",
        "Estimation of high and low tide times",
        "Marine science teaching and classroom demonstration",
        "Astronomy and geography enthusiasts exploring the causes of tides",
        "A rough tidal reference before shore gathering or tide watching",
        "Introductory learning for navigation and fisheries",
        "Preliminary assessment of tidal power feasibility",
        "Tide facts",
        "Tides are produced by the tidal forces of the Moon and the Sun, and the tidal force is inversely proportional to the cube of the distance to the body. The lunar tidal force is about 2.17 times the solar one (the Sun accounts for about 46%). At new moon and full moon the solar and lunar tidal forces align and add to form a",
        "spring tide",
        "; at the first and last quarters (quadrature) the two partly cancel to form a",
        "neap tide",
        ". At lunar perigee the tidal force increases by about 25%, which can produce a perigean spring tide. Near the equator semidiurnal tides dominate (two high and two low tides per day), while at high latitudes diurnal characteristics are more pronounced.",
    ]))


if __name__ == '__main__':
    main()
