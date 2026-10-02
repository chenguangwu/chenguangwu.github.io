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
    write('magnitude-comparator', build('magnitude-comparator', [
        "⚖️ Magnitude Brightness Comparator",
        "Calculates the brightness ratio of two celestial bodies from their apparent magnitudes. Formula: F2/F1 = 2.512^(m1-m2), that is, the brightness ratio is 2.512 raised to the magnitude difference. The smaller the magnitude, the brighter the object; a difference of 5 magnitudes means a brightness ratio of 100.",
        "\"Calculates the brightness ratio of two celestial bodies from their apparent magnitudes. Formula: F2/F1 = 2.512^(m1-m2), that is, the brightness ratio is 2.512 raised to the magnitude difference. The smaller the magnitude, the brighter the object; a difference of 5 magnitudes means a brightness ratio of 100.\" performs a professional calculation on the input parameters and outputs the result.",
        "📖 View the usage guide for the Magnitude Brightness Comparator",
        "Fill in object A",
        "Fill in object B",
        "🅰️ Object A",
        "Apparent magnitude m1",
        "🅱️ Object B",
        "Apparent magnitude m2",
        "🔍 Calculate the brightness ratio",
        "🌌 Catalogue of common objects (click to fill in the current object)",
        "Currently filled target:",
        "Object A",
        ". Click an object below to fill in the comparison quickly.",
        "📊 Brightness comparison result",
        "Pogson ratio",
        ": for each difference of 1 magnitude the brightness differs by 2.512 times; a difference of 5 magnitudes corresponds exactly to 100 times. Formula F2/F1 = 2.512^(m1-m2); a result greater than 1 means object B is brighter, and less than 1 means object A is brighter.",
        "📚 Deep dive: Magnitude Brightness Comparator",
        "From the apparent magnitude difference of two stars, calculate their brightness ratio F2/F1 = 2.512^(m1-m2).",
        "Understand intuitively the Pogson scale, where a difference of 5 magnitudes means a brightness difference of 100 times.",
        "In observation planning, judge how much a bright star interferes with observing a faint one.",
        "Example: the brightness ratio for a magnitude difference of 2.5",
        "F2/F1 = 2.512^(m1-m2) = 2.512^2.5, about 10. That is, at a difference of 2.5 magnitudes the brighter star is about 10 times the brightness of the fainter one (each magnitude is about 2.512 times, and the smaller the number the brighter).",
        "Why does a smaller magnitude number mean brighter?",
        "Historically, stars visible to the naked eye were assigned small numbers, and the Pogson scale sets 100 times brighter as a magnitude difference of 5, so the smaller the value the brighter.",
        "Where does the base 2.512 come from?",
        "It is defined as 100^(1/5), about 2.512, ensuring that a magnitude difference of 5 corresponds exactly to a brightness ratio of 100. This convention was set by Pogson in 1856.",
        "This tool uses",
        "apparent magnitude",
        ", that is, the brightness observed from Earth, not the absolute luminosity",
        "The magnitudes of planets and of the Moon are reference values close to maximum brightness; in reality they vary with phase and distance",
        "The brightness ratio is a ratio of energy flux, and the bar chart uses",
        "a logarithmic scale",
        "to accommodate huge differences (for example the Sun and Polaris differ by about 10^10 times)",
        "This tool runs purely in the front end and data is not uploaded to a server, so it can be used with confidence",
        "About the Magnitude Brightness Comparator",
        "The Magnitude Brightness Comparator is an online astronomy tool for amateur astronomers, students and popular science workers. Based on the classic Pogson magnitude system, it calculates the apparent brightness ratio of two celestial bodies with the formula F2/F1 = 2.512^(m1-m2). The tool has a built-in catalogue of apparent magnitudes for more than 20 common objects such as the Sun, the full Moon, Venus, Jupiter, Sirius and Polaris; click one to fill in the comparison, and a logarithmic bar chart shows the brightness difference intuitively. All calculations are performed locally in the browser, with no network needed and no data uploaded.",
        "Precise brightness ratio by the Pogson formula",
        "Built-in catalogue of 20+ common object apparent magnitudes",
        "Click the catalogue to fill in object A or B with one click",
        "Logarithmic bar chart visualizes the brightness difference",
        "Supports one-click A/B swap and copying the result",
        "Large-span ratios shown automatically in scientific notation",
        "Amateur astronomers comparing stellar brightness",
        "Students learning magnitude and brightness conversion",
        "Popular science explanations of the apparent magnitude concept",
        "Assessing the visibility of a target before observing",
        "Verifying the brightness relation between planets and stars",
        "Estimating exposure reference for astrophotography",
        "Select the target to fill in",
        "Object name",
        "Swap A / B",
        "Swap A and B",
    ]))

    write('moon-illumination', build('moon-illumination', [
        "Illuminated fraction (k = (1 - cos(2 x pi x D/29.53)) / 2)",
        "Estimates the fraction of the Moon that is lit from the day in the lunar cycle.",
        "Moon illumination fraction calculator",
        "/ Moon illumination fraction",
        "Moon illumination fraction",
        "📖 View the usage guide for Illuminated fraction (k = (1 - cos(2 x pi x D/29.53)) / 2)",
        "Days after new moon (days)",
        "k = (1 - cos(2 x pi x D/29.53)) / 2; D = 0 is new moon and 14.77 is full moon.",
        "At D about 7.4 it is about half lit (quarter moon).",
        "📚 Deep dive: illuminated fraction (k = (1 - cos(2 x pi x D/29.53)) / 2)",
        "Enter day D of the lunar cycle to estimate the fraction of the Moon lit by the Sun, to help plan Moon watching.",
        "Predict the lunar surface brightness and sky background for night activities, photography or astronomical observation.",
        "Compare the effect of a full moon and a new moon on observing faint objects.",
        "Example: the illuminated fraction on the eighth day of the lunar month (D = 8)",
        "k = (1 - cos(2 x pi x 8/29.53)) / 2. Here 2 x pi x 8/29.53 is about 1.702 rad, cos is about -0.129, so k is about (1 - (-0.129))/2, about 0.564, that is about 56% illuminated, close to the first quarter.",
        "Why use 29.53 days?",
        "This is the mean length of the synodic month (the phase cycle), that is, the interval between two successive new moons; it is about 2.2 days longer than the sidereal month because the Earth also moves around the Sun.",
        "How precisely can the illuminated fraction indicate the waxing and waning days?",
        "The formula is an ideal approximation that ignores the inclination and ellipticity of the lunar orbit; precise phases require astronomical ephemerides and a phase angle calculation.",
        "How to use Illuminated fraction (k = (1 - cos(2 x pi x D/29.53)) / 2)",
        "The lunar illuminated fraction k is the fraction of the visible lunar disk lit by the Sun, ranging from 0 (new moon) to 1 (full moon).",
        "Calculation basis",
        "Using the synodic month of 29.53 days as the approximation: k = (1 - cos(2 x pi x D/29.53)) / 2, where D is the number of days since new moon; 0.5 corresponds to the first or last quarter (half disk).",
        "The inclination and ellipticity of the lunar orbit make the actual lit fraction deviate slightly from the ideal circular model; this result is a periodic approximation for star gazing and photography planning.",
    ]))

    write('observation-conditions', build('observation-conditions', [
        "🧮 Astronomical Observation Conditions Calculator",
        "Enter the date, location and observing environment to estimate the moon phase, moonrise and moonset and a composite observation condition score in real time",
        "Core formulas (by input variable): moonScore x 0.35 + bortleScore x 0.40 + weatherScore x 0.25; (ss.sunrise x 60 + shiftMin) / 60; (ss.sunset x 60 + shiftMin) / 60",
        "📖 View the usage guide for the Astronomical Observation Conditions Calculator",
        "Observation date",
        "Bortle dark-sky class (1 darkest to 9 brightest)",
        "1 - Excellent dark sky (natural darkness)",
        "2 - Typical truly dark sky",
        "3 - Rural sky",
        "5 - Suburban sky",
        "6 - Bright suburban sky",
        "7 - Suburban/urban transition",
        "9 - Inner city",
        "Latitude (-90 to 90)",
        "Longitude (-180 to 180)",
        "Cloud cover (0% clear to 100% overcast): weather factor",
        "💡 Note: the moon phase is estimated from the synodic month cycle (about 29.53 days), and moonrise and moonset are local solar time approximations (no time zone correction), so the actual times may deviate by about 30 minutes. The score combines moonlight interference (35%), light pollution (40%) and cloud cover (25%).",
        "This tool runs purely in the front end; all calculations are completed locally in the browser and the data is not uploaded",
        "The moon phase uses a simplified algorithm and may differ from astronomical ephemerides by several hours; it is for planning reference only",
        "Latitude affects sunrise, sunset, moonrise and moonset, so please enter the actual coordinates of the observing site",
        "The Bortle class can be checked against the",
        "light pollution map",
        "to look up the class for your location",
        "Cloud cover is a manual estimate; it is advisable to judge it together with the local weather forecast",
        "🌌 Bortle dark-sky class reference table",
        "The currently selected class is highlighted; the data comes from the International Dark-Sky Association (IDA) standard",
        "📚 Deep dive: Astronomical Observation Conditions Calculator",
        "Enter the observation date, latitude and longitude and the light pollution class to estimate the moon phase, moonrise and moonset and the composite observation score.",
        "Based on the IDA (International Dark-Sky Association) dark-sky standard, help amateurs pick a window with low light pollution and no moon interference.",
        "When planning deep-sky photography or meteor shower observing, assess the sky quality for that night.",
        "Example: observing around new moon in a suburban Bortle class 4 area",
        "If on that night the",
        "moon illumination fraction",
        "is below 10% and the Moon sets before midnight, then with Bortle 4 (rural sky) a fairly high score is reached; in a city at Bortle 8 near full moon the score drops markedly, so it is better to change the date or switch to planetary imaging.",
        "What is the Bortle class?",
        "A night sky brightness scale proposed by John Bortle: 1 is the darkest pristine sky and 9 is the city centre; the smaller the number, the better suited it is to deep-sky observation.",
        "Why does the Moon affect observation so much?",
        "The brightness of a full moon lights up the atmosphere and raises the background level, drowning out faint galaxies and nebulae; with no Moon and far from light pollution the deepest visible magnitude is reached.",
        "About the Astronomical Observation Conditions Calculator",
        "The Astronomical Observation Conditions Calculator is a pure front-end online tool for amateur astronomers and deep-sky photographers. Enter the observation date, geographic latitude and longitude, Bortle dark-sky class and cloud cover, and it estimates the moon phase, the moon illumination percentage and moonrise and moonset times in real time, and gives a 1-10 observation condition score plus targeted advice combining moonlight interference, light pollution and weather, helping you judge whether tonight is worth setting up your gear.",
        "Real-time moon phase calculation (8 phases plus illumination percentage)",
        "Moonrise and moonset time estimation (including polar day and polar night detection)",
        "1-10 composite observation score with gauge visualization",
        "Three-dimensional score breakdown: moonlight, light pollution and cloud cover",
        "Complete Bortle dark-sky class reference table",
        "Smart observing advice (deep sky, planets, Moon)",
        "Pure front-end processing; data is not uploaded, privacy and security protected",
        "Planning deep-sky imaging sessions",
        "Choosing a date for a Messier marathon",
        "Scheduling planetary and lunar observation",
        "Siting star camps and dark-sky parks",
        "Scheduling astronomy popular science events",
        "Judging whether it is worth carrying the gear out",
        "Calculation principle",
        "The moon phase is estimated from the reference new moon of 2000-01-06 and the 29.53-day synodic month; moonrise and moonset are derived from the fact that the Moon comes about 50.47 minutes later each day than the Sun, combined with the sunrise and sunset for the local latitude (local solar time). The score = moonlight interference (35%) + light pollution (40%) + cloud cover (25%); the fuller the Moon, the higher the Bortle class and the greater the cloud cover, the lower the score.",
        "How to use the Astronomical Observation Conditions Calculator",
        "Observation date",
        "Bortle dark-sky class",
        "Latitude",
        "Longitude",
        "Cloud cover",
    ]))

    write('schwarzschild-radius', build('schwarzschild-radius', [
        "Event horizon (r_s = 2 x G x M / c^2)",
        "The event horizon radius when a mass M collapses into a black hole.",
        "Schwarzschild radius calculator",
        "/ Schwarzschild radius",
        "Schwarzschild radius",
        "📖 View the usage guide for Event horizon (r_s = 2 x G x M / c^2)",
        "The event horizon radius when a mass M collapses into a black hole.",
        "r_s = 2GM/c^2; one solar mass is about 2.95 km.",
        "📚 Deep dive: event horizon (r_s = 2 x G x M / c^2)",
        "Enter a mass M and, using the Schwarzschild radius formula, estimate the size of the event horizon if it collapsed into a black hole.",
        "Compare intuitively the horizon scales for different masses (a star, a galactic centre black hole, the Earth).",
        "In popular science, show that a greater mass means a larger horizon, and how small the Earth's Schwarzschild radius is.",
        "Example: the Schwarzschild radius of the Sun",
        "r_s = 2GM/c^2 = 2 x 6.674 x 10^-11 x 1.989 x 10^30 / (2.998 x 10^8)^2, about 2.95 x 10^3 m, about 2.95 km. That is, the Sun would have to be compressed into a sphere of about 3 km radius to become a black hole, while the Earth would need to be compressed to about 9 mm.",
        "What is the event horizon?",
        "It is the one-way boundary of a black hole: light inside it cannot escape either, and outside observers can only see information from beyond the horizon, hence the name event horizon.",
        "Does a larger mass mean a larger or a smaller horizon?",
        "Larger. r_s is proportional to the mass: a solar-mass black hole is about 3 km, while a supermassive black hole such as one at a galactic centre can reach tens of millions of kilometres.",
    ]))

    write('solar-declination', build('solar-declination', [
        "Declination (delta about 23.44 degrees x sin(360 degrees x (284+N)/365))",
        "Estimates the solar declination from day N of the year (Cooper approximation).",
        "Solar declination approximation calculator",
        "/ Solar declination",
        "Solar declination",
        "📖 View the usage guide for Declination (delta about 23.44 degrees x sin(360 degrees x (284+N)/365))",
        "Day of year N",
        "delta about 23.44 degrees x sin(360 x (284+N)/365); N = 172 (summer solstice) gives about +23.44 degrees.",
        "N = 355 (winter solstice) gives about -23.44 degrees.",
        "📚 Deep dive: declination (delta about 23.44 degrees x sin(360 degrees x (284+N)/365))",
        "Enter day N of the year and use the Cooper approximation to estimate the solar declination, for sunlight and solar angle analysis.",
        "Track the north-south movement of the subsolar point around the summer and winter solstices.",
        "In building design or photovoltaic array orientation calculations, estimate the noon solar altitude.",
        "Example: the declination on day 172 (about 21 June)",
        "delta about 23.44 degrees x sin(360 degrees x (284+172)/365) = 23.44 degrees x sin(360 degrees x 1.2466) = 23.44 degrees x sin(448.8 degrees) = 23.44 degrees x sin(88.8 degrees), about 23.44 degrees x 0.9998, about 23.43 degrees, close to the summer solstice extreme of the Sun directly overhead at the Tropic of Cancer.",
        "Why is the declination between -23.44 and +23.44 degrees?",
        "This is the obliquity of the ecliptic, the tilt of the Earth's rotation axis of about 23.44 degrees, which makes the subsolar point swing annually between the Tropics of Cancer and Capricorn.",
        "Is the Cooper approximation accurate enough?",
        "For sunlight and solar energy estimates the error is usually within 1 degree; precise astronomical calculation requires more complete Earth orbit parameters and nutation corrections.",
    ]))


if __name__ == '__main__':
    main()
