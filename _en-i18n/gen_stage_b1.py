#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'stage')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'stage')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
EXTRA = {'power-load': {'功率因数': 'power factor'}}


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
    out = {'slug': slug, 'industry': 'stage', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

#!/usr/bin/env python3


def main():
    write('beam-angle', build('beam-angle', [
        '🧮 Fixture Beam Angle Calculation',
        'Compute the illuminated spot diameter and area from throw distance and beam angle',
        'Beam Angle',
        '/ Beam Angle',
        '📖 View the Fixture Beam Angle Calculation user guide',
        'D = 2 × distance × tan(beam angle / 2)',
        'Throw distance (m)',
        'Center beam intensity (cd)',
        'Diameter D = 2 × distance × tan(beam angle / 2); area A = π × (D/2)²; illuminance E = intensity / distance² (inverse-square law).',
        'Common fixture beam angle reference',
        '📚 In-depth analysis: Fixture Beam Angle Calculation',
        'When rigging stage lighting, derive the floor spot diameter from the beam angle using the fixture mounting height and throw distance, to judge whether the performance area and proscenium are covered.',
        'Before buying or replacing fixtures, compare the beam angles of spot (5–15°) and flood (30–60°) units to match the different wash requirements of front light, side light or cyclorama.',
        'Given the centre beam intensity (cd) and distance, use the inverse-square law to estimate centre illuminance (lux) and check whether brightness at key stage positions meets the target.',
        'Worked example: 25° beam over a 10 m throw',
        'Take a beam angle of 25°, throw distance 10 m and centre beam intensity 50000 cd. Half angle 12.5°, spot radius = 10 × tan(12.5°) ≈ 2.22 m, diameter ≈ 4.43 m, illuminated area ≈ 15.44 m²; centre illuminance = 50000 / 10² = 500.0 lux (about 50.0 fc). A 25° beam is a medium beam (15–30°), covering roughly 7% (of a 360° sphere).',
        'Does a smaller beam angle always mean higher illuminance?',
        'Not necessarily. A smaller beam angle concentrates the spot and raises illuminance per unit area, but reduces coverage; with total luminous flux unchanged, a narrow beam is brighter and tighter while a wide beam is more even and broader.',
        'When does the inverse-square law deviate?',
        'It applies only to the ideal case of a point source in the near field, ignoring fixture size and reflections; at short distances or with reflector fixtures, correct it using the photometric distribution curve.',
        'About Beam Angle',
        'Beam angle calculator: computes the illuminated-spot diameter and area from throw distance and beam angle, for stage lighting layout. A creative design tool with visual operation, one-click CSS code generation.',
        'Stage lighting design and fixture selection (front, side and back light combinations)',
        'Pre-rehearsal preview of lighting parameters and three-phase load calculation',
        'On-site tuning of dimmer curves and unified color temperature by the lighting designer',
        'Theatre and venue lighting compliance and electrical safety checks',
    ]))

    write('dimmer-curve', build('dimmer-curve', [
        '🎭 Dimmer Curve Calculation',
        'Compute the actual output brightness corresponding to a DMX input value under different dimmer curves',
        'Dimmer Curve',
        '/ Dimmer Curve',
        '📖 View the Dimmer Curve Calculation user guide',
        'Dimmer curve description ',
        'Output brightness vs input signal',
        ' (0–100%, or 0–255 for DMX512). Common types:',
        ': output is proportional to input.',
        ': simulates an incandescent lamp — perceived brightness is roughly related to the square root of power, giving finer and more natural low-end control.',
        ': gentle at both ends and steep in the middle, suited to emphasising mid-tone transitions.',
        ': an inverse curve, used for special looks.',
        'Choosing the wrong curve causes visible "jumps" in fades or crushed blacks; choose according to fixture characteristics and on-site needs.',
        'Dimmer curve type',
        'Linear curve',
        'Square-law curve',
        'Sine curve',
        'S-Curve',
        'Exponential curve',
        'Logarithmic curve',
        'DMX input value (0-255)',
        'Curve comparison (input values 0-255)',
        'Curve notes: ',
        'Square law is the curve that looks most linear to the human eye and is the DMX512 default. The S-curve gives smoother transitions in shadows and highlights. A linear curve looks uneven to the eye at low brightness.',
        '📚 In-depth analysis: Dimmer Curve Calculation',
        'Incandescent and halogen dimming should use the square law so perceived brightness is close to linear, avoiding "jumps" in the low end.',
        'Use the S-curve when smooth shadow and highlight transitions are needed, commonly for fades and breathing effects in programming.',
        'Compare the output of the same DMX value under different curves to predict the brightness curve before programming the console, and unify the look across fixtures.',
        'Worked example: DMX 128 under the square-law curve',
        'DMX input 128 (about 50.2%). Square-law output = (128/255)² × 255 ≈ 64.3 / 255 (about 25.2%), a brightness gain of about 0.50×; at the same input, the linear curve outputs 128.0 (50.2%), the S-curve about 128.2 (50.3%) and the exponential curve about 45.5 (17.9%). Curve type strongly affects low-end brightness, and the square law is closest to human perception.',
        'Why does a linear DMX curve look uneven?',
        'Human brightness perception follows a power law, so a linear mapping makes the low end too dark and the high end too bright; square-law and logarithmic curves match vision better.',
        'Must all fixtures use the same curve?',
        'Mixing curves in the same scene makes fades inconsistent; use the same curve type for fixtures of the same batch and perform greyscale calibration.',
        'About Dimmer Curve',
        'Stage dimmer curve calculator supporting calculation and comparison of linear, square-law and S-curve dimming curves. A creative design tool with visual operation, one-click CSS code generation.',
        'Stage lighting design and fixture selection (front, side and back light combinations)',
        'Pre-rehearsal preview of lighting parameters and three-phase load calculation',
        'On-site tuning of dimmer curves and unified color temperature by the lighting designer',
        'Theatre and venue lighting compliance and electrical safety checks',
    ]))

    write('light-position', build('light-position', [
        '🧮 Fixture Angle and Position Calculation',
        'Compute the fixture mounting angle and horizontal offset from throw distance and height',
        'Performs a professional calculation of "fixture mounting angle and horizontal offset from throw distance and height" using the input parameters and outputs the result.',
        'Light Position',
        '/ Light Position',
        '📖 View the Fixture Angle and Position Calculation user guide',
        'Throw angle',
        'Mounting position',
        'Fixture height (m)',
        'Horizontal distance (m)',
        'Throw angle (°)',
        'Angle reference: ',
        '45° is standard front light; 30°-45° is front-side light (side fill); 45°-60° is side light; above 60° is top light or back light. Throw angle = arctan(height / horizontal distance).',
        'Stage fixture angle reference',
        '📚 In-depth analysis: Fixture Angle and Position Calculation',
        'Front light usually uses a 40–50° throw angle; work back from the proscenium height and the distance to the fixture hanging point to derive the mounting angle.',
        'Side light uses 30–60°; compute the depression angle and slant distance from height and horizontal distance to avoid heavy shadows on the performer\'s face.',
        'Given the throw angle and height, back-calculate the horizontal mounting distance and combine it with the ',
        'Beam Angle',
        ' to obtain the spot coverage diameter and area.',
        'Worked example: front light at 6 m height, 5 m distance',
        'Fixture height 6 m, horizontal distance 5 m: throw angle = arctan(6/5) ≈ 50.2°, depression angle ≈ 39.8°, slant distance ≈ 7.81 m, height/distance ratio 1.20, i.e. front light (40–50°). Then with a throw angle of 45°, height 6 m and beam angle 25°: horizontal mounting distance = 6 / tan45° = 6.00 m, slant distance ≈ 8.49 m, spot radius ≈ 1.88 m, diameter ≈ 3.76 m, illuminated area ≈ 11.12 m².',
        'Is a larger throw angle always better?',
        'No. Too large an angle approaches top or back light, reducing facial brightness and deepening shadows; front light works best at 40–50° and side light at 45–60°, combined according to the shaping goal.',
        'Which affects spot size more, height or distance?',
        'At a fixed beam angle, spot diameter ≈ 2 × slant distance × tan(half angle); slant distance grows with both height and distance, so together they determine the coverage area.',
        'About Light Position',
        'Stage fixture angle and position calculator: computes fixture mounting position and coverage from throw distance, height and throw angle. A creative design tool with visual operation, one-click CSS code generation.',
        'Stage lighting design and fixture selection (front, side and back light combinations)',
        'Pre-rehearsal preview of lighting parameters and three-phase load calculation',
        'On-site tuning of dimmer curves and unified color temperature by the lighting designer',
        'Theatre and venue lighting compliance and electrical safety checks',
    ]))

    write('power-load', build('power-load', [
        '🎭 Total Lighting Power and Load Calculation',
        'Compute total stage lighting power, current and three-phase load distribution',
        'Core formulas (by input variable): threePhasePower ÷ (√(3) × voltage × pf) ÷ 3 + singlePhasePower ÷ (220 × pf); max(|(threePhasePower ÷ 3 - 0)|, |(singlePhasePower)|); totalPower ÷ (√(3) × voltage × pf)',
        'Power Load',
        '/ Power Load',
        '📖 View the Total Lighting Power and Load Calculation user guide',
        'Supply voltage (V)',
        '220 V (single phase)',
        '380 V (three phase)',
        'Safety margin (%)',
        'Fixture list',
        '+ Add fixture',
        'Calculate load',
        'Load notes: ',
        'Total current = total power / (voltage × power factor). Three-phase loads should be distributed as evenly as possible, with per-phase unbalance no more than 15%. Total load should not exceed 80% of the circuit breaker rating.',
        'Common stage fixture power reference',
        '📚 In-depth analysis: Total Lighting Power and Load Calculation',
        'Before a show, total up the power and quantity of every fixture, compute total power and current, and check whether the supply capacity and circuit breakers are sufficient.',
        'Distribute three-phase loads as evenly as possible, put high-power single-phase equipment (follow spots, haze machines) on separate circuits, and keep per-phase unbalance under control.',
        'Allow a safety margin on total current (for example 20%) and round up when selecting the circuit breaker, to avoid tripping at full load.',
        'Worked example: a typical stage lighting rig (380 V three phase)',
        'Fixture list: LED PAR 200 W ×24, moving head 700 W ×8, halogen profile spot 1000 W ×12 (three phase), follow spot 2500 W ×2, haze machine 1500 W ×2 (single phase). Total power 30.40 kW (three phase 22.40 kW, single phase 8.00 kW), 48 units in total. At 380 V three phase, ',
        '0.9, with a 20% safety margin: total current ≈ 51.3 A, about 53.0 A per phase, current after safety margin ≈ 61.6 A, recommended circuit breaker 64 A; single-phase share about 26.3%.',
        'How are three-phase and single-phase currents calculated?',
        'Three-phase total current = total power / (√3 × voltage × power factor); single-phase equipment current = power / (voltage × power factor). Three-phase loads must be split evenly across the three phases before adding the single-phase circuits.',
        'Why keep total load below 80% of the circuit breaker?',
        'The margin absorbs lamp inrush and temperature rise, reducing the risk of tripping and overheating; long-term full load accelerates insulation ageing.',
        'About Power Load',
        'Stage lighting total power and load calculator: computes total power, current and three-phase load distribution from fixture count and power. A creative design tool with visual operation, one-click CSS code generation.',
        'Stage lighting design and fixture selection (front, side and back light combinations)',
        'Pre-rehearsal preview of lighting parameters and three-phase load calculation',
        'On-site tuning of dimmer curves and unified color temperature by the lighting designer',
        'Theatre and venue lighting compliance and electrical safety checks',
        'How to use Total Lighting Power and Load Calculation',
        'What does Total Lighting Power and Load Calculation do?',
        'Add multiple fixtures with their power ratings to compute total stage lighting power, total current and three-phase load distribution, for distribution capacity planning, breaker selection and electrical safety checks.',
        'How do I use Total Lighting Power and Load Calculation?',
        'What scenarios is Total Lighting Power and Load Calculation suitable for?',
    ]))

    write('stage-color-filter', build('stage-color-filter', [
        '⚖️ Stage Color Temperature and Filter Comparison',
        'Reference for common light source color temperatures, filter models and color temperature conversion',
        'Performs a professional calculation of "common light source color temperatures, filter models and color temperature conversion" using the input parameters and outputs the result.',
        'Stage Color Filter',
        '/ Stage Color Filter',
        '📖 View the stage-color-filter user guide',
        'Light source color temperature',
        'Filter',
        'Color temperature conversion',
        'Search filters',
        'Source color temperature (K)',
        'Target color temperature (K)',
        'Color temperature notes: ',
        'Color temperature is measured in kelvin (K). 3200 K is warm white (tungsten) and 5600 K is daylight white. Mired value = 1000000 / color temperature in K, used for color temperature conversion.',
        '📚 In-depth analysis: Stage Color Temperature and Filter Comparison',
        'When unifying 3200 K tungsten sources to 5600 K daylight, use the mired difference to choose a CTB filter so all fixtures match in color.',
        'When mixing LEDs (adjustable 2700–6500 K) with conventional halogen lamps, first fix a reference color temperature, then choose CTO/CTB correction for the fixtures that deviate.',
        'Natural light at golden hour is about 2000–3500 K; use this when designing outdoor or window-scene projection to mix warm ambient light.',
        'Worked example: choosing a filter for 3200 K → 5600 K',
        'Source color temperature 3200 K, target 5600 K. Source mired = 1000000 / 3200 ≈ 313, target = 1000000 / 5600 ≈ 179, difference = −134 mired. A negative value means the color temperature must be raised, so use CTB (color temperature blue); |Δ| ≈ 134 ≥ 131 corresponds to a full CTB.',
        'What is mired, and why is the difference used to choose filters?',
        'Mired = 1,000,000 / color temperature (K), a reciprocal scale of color temperature. Filters are graded by mired difference (full / half / quarter CTO·CTB); the larger the difference, the stronger the correction needed.',
        'Can filters replace color temperature adjustment on LED fixtures?',
        'For tunable-white LEDs, use their own adjustment first: it is more accurate and loses no light; filters suit fixed-color-temperature sources or special tones, but they attenuate luminous flux.',
        'About Stage Color Filter',
        'Stage lighting color temperature and filter comparison table, with common source color temperatures, filter models and color temperature conversion parameters. A creative design tool with visual operation, one-click CSS code generation.',
        'Stage lighting design and fixture selection (front, side and back light combinations)',
        'Pre-rehearsal preview of lighting parameters and three-phase load calculation',
        'On-site tuning of dimmer curves and unified color temperature by the lighting designer',
        'Theatre and venue lighting compliance and electrical safety checks',
        'e.g. 201, RBO...',
    ]))


if __name__ == '__main__':
    main()
