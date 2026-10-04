#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'shipping')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'shipping')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    return mp


def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'shipping', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

#!/usr/bin/env python3


def main():
    write('calc-76', build('calc-76', [
        '🚢 Vessel Displacement and Deadweight Calculation',
        'Enter the length between perpendiculars, moulded breadth, forward, mid and aft draught, block coefficient and water density to calculate displacement, TPC, MTC, trim and deadweight',
        'Core formulas (by input variables): Tm-(Tf+Ta)÷2; min(1,max(0,Cb)); Cw×Cw×L×L×L×B÷12',
        '📖 View the Vessel Displacement and Deadweight Calculation user guide',
        'Length between perpendiculars LBP (m)',
        'Moulded breadth B (m)',
        'Forward draught Tf (m)',
        'Mid draught Tm (m)',
        'Aft draught Ta (m)',
        'Block coefficient Cb',
        'Water density ρ (t/m³)',
        'Waterplane coefficient Cw, leave blank for automatic',
        'Lightship weight (t, optional)',
        '💡 The mean draught uses the mean of means, (Tf + 6Tm + Ta)/8; when Cw is left blank it is estimated as (2Cb + 1)/3; GML ≈ BM_L is used for the MTC estimate.',
        'Press',
        'to calculate quickly; the result can be copied with one click',
        'Displacement Δ = Cb·L·B·T_mean·ρ in tonnes',
        'Trim = Ta − Tf, where a positive value means trim by the stern; DWT = Δ − lightship weight',
        'This tool runs entirely in the browser and the results are estimates, for reference only',
        '📚 In-depth analysis: Vessel Displacement and Deadweight Calculation',
        'When checking the loading of a new or operating vessel, compute the hydrostatic parameters of displacement, TPC and MTC from LBP, moulded breadth, the draught at each station, the block coefficient and the water density.',
        'For trim calculation, get the direction and size of the trim from the difference between the forward and aft draughts, and use MTC to estimate the weight that must be shifted to adjust the trim.',
        'For load capacity accounting, subtract the lightship weight from the displacement to get DWT and check it against the cargo quantity for the voyage.',
        'Hydrostatic example for a 100 m dry cargo ship',
        'LBP = 100 m, moulded breadth = 16 m, forward, mid and aft draught = 5.0, 5.2 and 5.4 m, block coefficient 0.7, sea water density 1.025: waterplane coefficient Cw = (2 × 0.7 + 1)/3 = 0.8, mean draught 5.20 m, displacement 5969.6 t, waterplane area 1280 m², TPC = 13.12 t/cm, longitudinal metacentric height GML ≈ 146.5 m, MTC = 87.47 t·m/cm; trim by the stern 0.4 m, and with a lightship of 2000 t, DWT = 3969.6 t; changing the trim by 1 cm requires shifting about 87.5 t.',
        'How is the waterplane coefficient chosen?',
        'When it is not given, estimate it as (2 × Cb + 1)/3 by experience; if it is known, enter it directly. The coefficient affects the waterplane area, TPC and stability.',
        'What is the difference between MTC and TPC?',
        'TPC is the change in displacement for each additional centimetre of draught in t/cm, while MTC is the moment needed to produce 1 cm of trim in t·m/cm; the two reflect loading sensitivity in the vertical and longitudinal directions respectively.',
        'About Vessel Displacement and Deadweight Calculation',
        'From the principal dimensions and draught of the vessel, it calculates displacement, deadweight DWT, tonnes per centimetre immersion TPC, moment to change trim by one centimetre MTC, plus trim and midship deformation; it suits draft survey and loading estimation. It runs entirely in the browser and data is not uploaded.',
        'Draught correction using the mean of means',
        'TPC and MTC calculated together',
        'Trim direction and hogging or sagging judgement',
        'Supports a custom waterplane coefficient',
        'Draft survey',
        'Vessel loading and draught adjustment',
        'Port draught limit verification',
        'Quick estimation of hull parameters',
        'Automatic',
    ]))

    write('convert-speed-1', build('convert-speed-1', [
        '🏎️ Speed (Through Water / Over Ground) Conversion',
        'Ship speed from knots to kilometres per hour, where 1 kn = 1.852 km/h',
        '📖 View the Speed (Through Water / Over Ground) Conversion user guide',
        'Speed unit conversion: result = input value × source unit factor ÷ target unit factor; the common relations are 1 knot = 1.852 kilometres per hour, 1 metre per second = 3.6 kilometres per hour and 1 mile per hour = 1.609344 kilometres per hour.',
        'Knot (kn)',
        'Kilometres per hour (km/h)',
        '📚 In-depth analysis: Ship Speed Unit Conversion in knots, metres per second and kilometres per hour',
        'Nautical data usually gives speed in knots, which must be converted to m/s or km/h for use in formulas or for comparison with land references.',
        'Weather or current data is often given in m/s and must be converted to knots for comparison with the ship speed.',
        'When units differ across borders or between instrument readings, unify them to avoid errors in distance and time calculations.',
        'Conversion example for 20 knots',
        '1 knot = 1 nautical mile per hour = 1.852 km/h = 0.5144 m/s, so 20 knots ≈ 10.289 m/s ≈ 37.040 km/h ≈ 23.016 mph. Note that 1 nautical mile is about 1852 m and the conversion between knots and km/h is fixed, so keep a sensible number of decimals.',
        'Why does navigation use knots?',
        'The knot comes from the knots on the log line used to measure speed at sea; 1 knot = 1 nautical mile per hour, which naturally matches latitude and longitude distances and makes it easy to estimate distance from minutes of latitude.',
        'Are speed through water and speed over ground the same?',
        'No. Speed through water is the speed relative to the water, while speed over ground also adds the current, positive with the current and negative against it. This tool offers a plain ',
        ' only, so the actual distance made good must be corrected for current set and drift.',
        'About Speed (Through Water / Over Ground) Conversion',
        'A speed through water and over ground conversion tool. A free online tool that runs entirely in the browser; data is never uploaded, keeping your privacy safe.',
        'Unifying ship speed units in nautical data, converting between knots, metres per second and kilometres per hour',
        'Converting weather or current data in m/s into knots for comparison',
        'Aligning units when readings differ across borders or between instruments',
        'Standardising speed units before estimating distance and time',
    ]))

    write('convert-time-speed', build('convert-time-speed', [
        '🏎️ Ship Speed / Distance / Voyage Time Conversion',
        'An online tool for converting ship speed, distance and voyage time',
        '📖 View the Ship Speed / Distance / Voyage Time Conversion user guide',
        'Ship speed',
        'Milli ship speed',
        'Kilo ship speed',
        'Milli distance',
        'Kilo distance',
        '📚 In-depth analysis: Ship Speed, Distance and Voyage Time Conversion',
        'In voyage planning, with the average speed and voyage time known, compute the total distance to check fuel and the arrival window.',
        'With the distance and planned speed known, back-calculate the voyage time needed for scheduling.',
        'Under a restricted speed, such as in narrow channels or under environmental speed limits, recompute the leg time at the limiting speed.',
        'Example: 15 knots for 10 hours',
        'Distance = speed × time: 15 knots × 10 hours = 150 nautical miles, which is about 277.8 km, since 1 nautical mile = 1.852 km. If the distance is 150 nautical miles and the speed limit is 12 knots, then 12.5 hours are needed.',
        'How do I convert nautical miles to kilometres?',
        '1 nautical mile = 1852 metres, about 1.852 kilometres; multiply the distance in nautical miles by 1.852 to get kilometres.',
        'How is the average speed taken?',
        'Take the planned or actual over-ground ',
        'average speed',
        ', and include the current; for legs with separate speed limits, add up the time and distance leg by leg at each limit rather than simply using a whole-voyage average.',
        'About Ship Speed / Distance / Voyage Time Conversion',
        'A ship speed, distance and voyage time conversion tool. A free online tool that runs entirely in the browser; data is never uploaded, keeping your privacy safe.',
        'Estimating the total distance of a voyage from the average speed and voyage time',
        'Back-calculating the voyage time needed from a known distance and planned speed',
        'Recomputing leg time at the limiting speed in narrow channels or environmental zones',
        'Accounting for leg-by-leg time and distance totals',
    ]))

    write('estimate-length', build('estimate-length', [
        '📏 Anchoring Cable Length Estimation',
        'Enter the water depth, wind speed, current speed, vessel tonnage and bottom type to estimate the recommended cable length at a scope of 3-7:1, and the holding grade',
        'Core formulas (by input variables): 0.5×1.225×1.3×A×windMs×windMs; min(8,max(3,scope)); windKn×0.514444',
        '📖 View the Anchoring Cable Length Estimation user guide',
        'Water depth (m)',
        'Knot kn',
        'Current speed (kn)',
        'Vessel tonnage (t)',
        'Bottom type',
        'Mud, good holding',
        'Sand, good holding',
        'Gravel, moderate holding',
        'Weed, poor holding',
        'Rock, poor holding and prone to dragging',
        'Bow height above water (m)',
        '💡 Cable length = scope × (water depth + bow height). The scope rises with wind speed, current speed and bottom type, from 3:1 to 7:1; in severe conditions 7:1 or more is recommended, plus a second bow anchor.',
        'Press',
        'to estimate quickly; the result can be copied with one click',
        'Scope base value 3, plus 1 for each wind band at 10, 20 and 30 kn, plus 0.5 for each current band',
        'Bottom correction: mud or sand +0, gravel +0.5, weed or rock +1',
        'The holding assessment is a qualitative reference; in practice combine it with the anchor type, chain weight and sea state',
        '📚 In-depth analysis: Anchoring Cable Length and Holding Estimation',
        'Before anchoring, estimate the safe cable length, the scope, from the water depth, the forecast wind and current, the vessel tonnage and the bottom type.',
        'With a poor bottom such as weed or rock, or with strong wind, current and swell, increase the scope, set a second anchor, or move to a sheltered anchorage.',
        'When estimating the windage area, derive it from the tonnage together with the wind force, to help judge the risk of dragging.',
        'Example: 20 m depth, wind 15 m·s⁻¹, gravel bottom',
        'Water depth 20 m, wind speed 15 m/s, about 29.16 kn, current 1.5 kn, tonnage 5000 t, gravel bottom with k = 0.5, bow height 8 m: wind increment 2, current increment 0.5, bottom increment 0.5, base 3, giving a scope of 6.0:1 and a cable length of 6.0 × (20 + 8) = 168 m; windage area ≈ 175.4 m², wind force ≈ 31431 N, or 3204 kgf, rated good.',
        'What scope is normally used?',
        'In open water 3:1 to 5:1 is common, rising to 6:1 to 8:1 in strong wind and sea or with a poor bottom; this tool combines wind, current and bottom and limits the result to 3-8.',
        'How much does the bottom affect holding?',
        'Mud and sand hold well with k = 0, gravel is moderate at k = 0.5, and weed or rock is poor at k = 1; a poor bottom needs a larger scope or a different anchorage.',
        'About Anchoring Cable Length Estimation',
        'Combining water depth, wind speed, current speed, vessel tonnage and bottom type, it estimates the cable length needed for anchoring at a scope of 3-7:1 plus the holding grade, and gives a reference wind force. It runs entirely in the browser and data is not uploaded.',
        'Scope calculated dynamically from wind, current and bottom',
        'Supports wind speed units in knots and m/s',
        'Windage area and wind force estimation',
        'Qualitative assessment of the holding grade',
        'Cable length decisions when anchoring a vessel',
        'Berthing planning for yachts and sailing boats',
        'Anchoring review in severe weather',
        'Maritime training and teaching',
    ]))

    write('tide', build('tide', [
        '⛅ Tide (High / Low Water) Prediction',
        'Enter the four tides of the reference station, with time, height and high or low, plus the secondary port differences and ratios, to predict the times and heights of high and low water at the secondary port and plot the tide curve',
        'Core formulas (by input variables): ((Math.max.apply(null,highs))-(Math.min.apply(null,lows)))',
        '/ Tide Prediction',
        '📖 View the Tide (High / Low Water) Prediction user guide',
        'Reference station tide data',
        'Secondary port differences and ratios, relative to the reference station',
        'High water time difference (minutes)',
        'High water height ratio (times)',
        'Low water time difference (minutes)',
        'Low water height ratio (times)',
        '🧮 Predict',
        '💡 Secondary port tide time = reference station tide time + time difference; secondary port tide height = reference station tide height × height ratio. The curve is drawn by cosine interpolation and is only an indication of the trend.',
        'Press',
        'to predict quickly; the result can be copied with one click',
        'Enter the four tides in time order; a time may exceed 24:00 across days, for example 25:30',
        'A height ratio above 1 means the tidal range at the secondary port is larger than at the reference station, below 1 the opposite',
        'The tide curve is a cosine interpolation approximation; actual tides are affected by topography and weather',
        '🕘 Recent predictions',
        '📚 In-depth analysis: Tide (High / Low Water) Prediction for a Secondary Port',
        'In voyage or operation planning, with the times and heights of high and low water at the main port, the reference station, known, predict the tide at the secondary port from its time difference and height ratio.',
        'When assessing the tidal range, take the largest range from the high and low waters at the secondary port to judge the window for berthing, unberthing and passing shallow sections.',
        'When drawing the tide curve, use cosine interpolation to reconstruct the tide process at the secondary port, helping to judge depths at the anchorage or in the channel.',
        'Example: prediction from secondary port differences',
        'Main port reference: high water 03:00 at 2.0 m and 15:00 at 2.2 m, low water 09:00 at 0.5 m and 21:00 at 0.4 m. Secondary port high water time difference +30 min with a ratio of 0.95, low water time difference +20 min with a ratio of 1.05: secondary port high water 03:30 at 1.9 m and 15:30 at 2.09 m, low water 09:20 at 0.53 m and 21:20 at 0.42 m, with a maximum tidal range at the secondary port of 2.09 − 0.42 = 1.67 m.',
        'Where do the time difference and height ratio come from?',
        'They come from the tidal tables or port regulations giving the harmonic constants of the secondary and main ports, and are used as fixed values; when the error is large, local measurement should prevail.',
        'Is the height ratio a constant?',
        'The same port usually has fixed ratios and time differences given separately for high and low water; in extreme astronomical tides or meteorological tides such as storm surge the prediction drifts and must be corrected against the forecast.',
        'About Tide Prediction',
        'From the measured tide data at the reference station, the main port, and the differences and ratios of the secondary port, it predicts the times and heights of high and low water at the secondary port and plots the tide curve. It uses the standard method of time differences and height ratios. It runs entirely in the browser and data is not uploaded.',
        'Complete prediction for four tides',
        'Separate differences and ratios for high and low water',
        'Supports time input across days',
        'Tide curve by cosine interpolation',
        'Fishing trips and port operations',
        'Intertidal harvesting and tide watching',
        'Choosing tidal windows for shipping',
        'Tide level estimation for coastal engineering',
        'High water time difference in minutes',
        'High water height ratio',
        'Low water time difference in minutes',
        'Low water height ratio',
    ]))


if __name__ == '__main__':
    main()
