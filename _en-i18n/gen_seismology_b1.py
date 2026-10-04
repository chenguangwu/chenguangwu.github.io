#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'seismology')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'seismology')
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
    out = {'slug': slug, 'industry': 'seismology', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

#!/usr/bin/env python3


def main():
    write('analysis-stress', build('analysis-stress', [
        '🌋 Focal Mechanism (Mechanism / Solution / Stress Field) Analysis',
        'Focal mechanism solution and stress axis calculation',
        '📖 View the Focal Mechanism (Mechanism / Solution / Stress Field) Analysis user guide',
        'Enter one nodal plane per line as plane name, strike, dip, rake, in degrees. Following the Aki and Richards nodal plane solution, the fault plane normal n and slip vector d give T = (n+d)/√2, P = (n−d)/√2 and B = n×d, converted to azimuth, measured clockwise from north, and plunge, and the rake determines whether the mechanism is strike-slip, normal or thrust.',
        'Nodal plane parameters, one per line as plane name, strike, dip, rake',
        'Plane 1,45,60,0',
        'Solve stress axes',
        '📚 In-depth analysis: Focal Mechanism Solution and P/B/T Stress Axes',
        'After obtaining a nodal plane solution with strike, dip and rake, seismology researchers convert the azimuth and plunge of the P, B and T axes for regional tectonic stress field analysis.',
        'In field geology and geophysics teaching, this tool demonstrates the spatial orientation of the stress axes for the three focal mechanism types: strike-slip, normal and thrust.',
        'In rapid post-earthquake assessment, the distribution of mechanism types shows whether the seismogenic structure is dominated by strike-slip or dip-slip motion.',
        'Trial calculation with two nodal plane solutions',
        'Entering plane A, 30, 60, −90 and plane B, 45, 80, 10, plane A is classified as normal, with the P axis at 300.0°/75.0°, the B axis at 30.0°/0.0° and the T axis at 120.0°/15.0°; plane B is classified as strike-slip, with the P axis at 359.1°/0.1°, the B axis at 89.6°/75.9° and the T axis at 269.1°/14.1°.',
        'What do the P, B and T axes represent?',
        'The P axis is the pressure axis, the direction of maximum principal compressive stress; the T axis is the tension axis, the direction of minimum principal stress; and the B axis is the null axis. The three are mutually orthogonal and together describe the stress state at the source.',
        'Why is the plunge always non-negative?',
        'Stress axes are axes rather than vectors and have no directional polarity; the tool consistently takes the upward component as positive in the conversion, so the plunge falls in the range from 0° to 90°.',
        'On what basis is the mechanism type determined?',
        'By the rake λ: |λ| ≤ 30° or ≥ 150° is strike-slip, from 30° to 150° is thrust, and from −150° to −30° is normal. This is the commonly used simplified convention for classifying focal mechanisms.',
        'About Focal Mechanism (Mechanism / Solution / Stress Field) Analysis',
        'A focal mechanism, mechanism solution and stress field analysis tool. A free online tool that runs entirely in the browser; data is never uploaded, keeping your privacy safe.',
        'Plane A,30,60,-90',
    ]))

    write('assessor-30', build('assessor-30', [
        '📋 Seismic Intensity Assessment (GB/T 17742)',
        'Based on the Chinese seismic intensity scale (GB/T 17742-2020), enter ground motion parameters and macroseismic damage phenomena to determine the seismic intensity grade from I to XII automatically.',
        'Core formulas (by input variables): max(pgaIntensity, pgvIntensity, diIntensity, macroIntensity); max(humanIndoor+2, humanOutdoor+3, objects+3, ground+4); desc[p.intensity-1]||desc[0]',
        'Intensity (Ground Motion / Damage / Assessment) Standard',
        '/ Seismic Intensity Assessment',
        '📖 View the Seismic Intensity Assessment (GB/T 17742) user guide',
        '1. Ground motion parameters (instrumental records)',
        'Peak ground acceleration PGA (cm/s²)',
        'Peak ground velocity PGV (cm/s)',
        '2. Human perception (macroseismic phenomena)',
        'Perception indoors',
        'Not felt',
        'Felt as slight vibration by a few people',
        'Felt by most people',
        'Felt by almost everyone indoors, causing alarm',
        'Difficulty standing and moving',
        'People fall and cannot move',
        'Perception outdoors',
        'Felt by a few people standing still',
        'Felt by most people',
        'Felt by almost everyone, running in alarm',
        'Difficulty moving, people fall',
        '3. Building damage (damage index)',
        'Mean building damage index',
        'Class A, brick-concrete or timber structure',
        'Class B, reinforced concrete',
        'Class C, steel structure or seismic design',
        '4. Other macroseismic phenomena',
        'Object response or furniture movement',
        'Hanging objects swing',
        'Furniture moves slightly',
        'Furniture moves or overturns',
        'Furniture shifts substantially or is thrown',
        'Ground surface damage',
        'No visible damage',
        'Slight cracks',
        'Obvious cracks, sand boils and water spouts',
        'Large-scale cracks, landslides or collapse',
        'Assess intensity',
        'Based on GB/T 17742-2020, the Chinese seismic intensity scale',
        'PGA reference values: degree V 45 cm/s², VI 90, VII 180, VIII 350, IX 700, X 1400',
        'Damage index: 0 = no damage, 0.1 = slight, 0.3 = moderate, 0.5 = severe, 0.7 = partial collapse, 1.0 = total destruction',
        'Instrumental parameters and macroseismic phenomena are judged together, taking the higher value',
        '📚 In-depth analysis: Seismic Intensity Assessment (GB/T 17742)',
        'Rapid on-site intensity assessment: enter the peak acceleration PGA, peak velocity PGV, damage index and macroseismic phenomena (human perception, object response, ground surface phenomena), and the tool determines the seismic intensity comprehensively under GB/T 17742.',
        'Building type correction: select the building class A, B or C, and the intensity corresponding to the damage index is corrected by +1 for class B and +2 for class C, reflecting the different seismic resistance of the structures.',
        'Initial disaster judgement: from the description corresponding to the assessed intensity from I to XII, for example degree VIII with buildings severely damaged and a few collapsed, quickly form a disaster assessment and response recommendation.',
        'Worked example: comprehensive judgement from multiple indicators',
        'Input PGA = 200 cm/s², PGV = 20 cm/s, damage index 0.35 for class A, indoor perception 4, outdoor 3, objects 3, ground phenomena 4. PGA gives degree 7, PGV degree 8, the damage index 0.35 gives degree 8 with no correction for class A, and the macroseismic phenomena give max(4+2, 3+3, 3+3, 4+4) = degree 8; taking the highest value and capping at 12, the assessment is degree VIII, with buildings severely damaged and a few collapsed. This shows that the velocity measure and the damage dominate here, reaching degree VIII.',
        'How is intensity converted from PGA or PGV?',
        'By the GB/T 17742 thresholds: PGA ≥ 180 gives degree 7, ≥ 350 degree 8, ≥ 700 degree 9; PGV ≥ 15 gives degree 8, ≥ 30 degree 9, ≥ 80 degree 11 and so on, as listed in the threshold table built into the tool. Different physical quantities give reference intensities independently, and the higher value is finally taken.',
        'What is the significance of the class A/B/C building correction?',
        'The same degree of damage corresponds to different intensities for buildings of different seismic fortification classes: class B, an important building, corresponds to an intensity one degree higher for the same damage, and class C two degrees higher. This reflects the difference in structural resistance and brings the intensity assessment closer to the actual damage.',
        'About Seismic Intensity Assessment',
        'A seismic intensity assessment tool: based on GB/T 17742-2020, the Chinese seismic intensity scale, it judges seismic intensity from I to XII using instrumental records, PGA and PGV, together with macroseismic phenomena, human perception, building damage, object response and ground damage, and outputs the intensity description and assessment conclusion automatically.',
        'Based on the national standard GB/T 17742-2020',
        'Automatic intensity conversion from PGA and PGV instrumental parameters',
        'Dual assessment by the damage index method and the macroseismic phenomenon method',
        'Damage correction for the three building classes A, B and C',
        'Side-by-side display of the intensity grade table',
        'Rapid on-site seismic intensity assessment',
        'Damage investigation and loss assessment',
        'Reference for seismic fortification standards',
        'Earthquake science education',
    ]))

    write('assessor-31', build('assessor-31', [
        '📋 Comprehensive Earthquake Damage Assessment',
        'Assess the damage to buildings, lifeline engineering and the geological environment, compute the damage index and give the loss grade and emergency recommendations.',
        'Core formulas (by input variables): (minor×0.1+moderate×0.3+severe×0.5+partial×0.7+total×1.0)÷totalBldg; bldgScore÷100×0.40+lifelineScore÷100×0.35+geoScore÷100×0.25; (waterScore+powerScore+gasScore+roadScore+commScore)÷5',
        'Earthquake Damage (Buildings / Lifelines / Landslides) Assessment',
        '/ Comprehensive Earthquake Damage Assessment',
        '📖 View the Comprehensive Earthquake Damage Assessment user guide',
        '1. Building damage (weight 40%)',
        'Total number of buildings',
        'Slightly damaged (buildings)',
        'Moderately damaged (buildings)',
        'Severely damaged (buildings)',
        'Partially collapsed (buildings)',
        'Completely collapsed (buildings)',
        '2. Lifeline engineering (weight 35%)',
        'Water supply network damage rate (sites/km)',
        'Power supply system damage rate (%)',
        'Gas pipeline damage rate (sites/km)',
        'Road damage rate (%)',
        'Communication interruption rate (%)',
        '3. Geological hazards (weight 25%)',
        'Landslide area (10,000 m²)',
        'Collapses or rockfalls (sites)',
        'Ground fissures (km)',
        'Sand liquefaction area (10,000 m²)',
        'Assess damage',
        'Building damage index: slight 0.1, moderate 0.3, severe 0.5, partial collapse 0.7, total destruction 1.0',
        'Lifeline damage rates follow the damage grade classification of GB/T 17742',
        'Geological hazard areas need to be combined with field investigation or remote sensing interpretation',
        'Comprehensive damage index: 0-0.1 slight, 0.1-0.3 moderate, 0.3-0.5 severe, 0.5-0.7 extreme, above 0.7 devastating',
        '📚 In-depth analysis: Comprehensive Earthquake Damage Assessment',
        'Building damage accounting: enter the number of buildings in each category, slight, moderate, severe, partial collapse and complete collapse, plus the total, and compute the building damage index, weighted 0.1, 0.3, 0.5, 0.7 and 1.0 and normalised, to quantify the degree of building damage.',
        'Lifeline and geological scoring: assess the interruption of water, power, gas, transport and communications and the scale of geological hazards such as landslides, collapses, ground fissures and liquefaction, converting them into a score from 0 to 100.',
        'Comprehensive grading: weight buildings 40%, lifelines 35% and geology 25% to obtain the comprehensive damage index, divided into five grades — slight, moderate, severe, extreme and devastating — to support the activation of the emergency response level.',
        'Worked example: comprehensive damage assessment for a town',
        'Of 1000 buildings: slight 200, moderate 100, severe 50, partial collapse 20, complete collapse 10; lifeline interruption: water 30, power 40, gas 2, transport 50, communications 60; geological hazards: landslides 20, collapses 10, ground fissures 5, liquefaction 3. Building damage index = (200×0.1 + 100×0.3 + 50×0.5 + 20×0.7 + 10×1.0)/1000 = 0.099, i.e. 9.9 points; lifelines = (100+40+40+50+60)/5 = 58.0; geology = (100+20+50+30)/4 = 50.0; comprehensive index = 9.9% × 0.40 + 58% × 0.35 + 50% × 0.25 = 0.3676, assessed as severe damage, so a level II response should be activated to organise rescue. It is worth noting that few buildings collapsed, but the lifeline and geological damage raised the overall grade.',
        'How is the comprehensive damage index weighted?',
        'Comprehensive index = building score × 0.40 + lifeline score × 0.35 + geological hazard score × 0.25, with each score normalised to 0-100. The weights express the post-disaster assessment logic of building damage first, with lifelines and geology also important.',
        'What are the thresholds for the grade division?',
        'A comprehensive index ≥ 0.7 is devastating, ≥ 0.5 extreme, ≥ 0.3 severe, ≥ 0.1 moderate, and anything else slight; these correspond to activating level I for devastating or extreme, or levels II to IV otherwise. The thresholds can be fine-tuned in the tool to local standards.',
        'About Comprehensive Earthquake Damage Assessment',
        'A comprehensive earthquake damage assessment tool: it evaluates earthquake losses from three dimensions, building damage with a damage index from a five-level damage classification, lifeline engineering with damage rates in the five systems of water, power, gas, roads and communications, and geological hazards including landslides, collapses, fissures and liquefaction, and outputs the damage grade and emergency response recommendations.',
        'Damage index from the five-level building damage classification',
        'Quantitative assessment of damage rates in the five lifeline systems',
        'Comprehensive evaluation of four types of geological hazard',
        'Rough estimate of the collapse rate and the population needing shelter',
        'Five damage grades with emergency response recommendations',
        'Rapid post-earthquake loss assessment',
        'Aggregation and analysis of disaster survey data',
        'Determination of the emergency response level',
        'Earthquake science communication and damage research',
    ]))

    write('generator-drill', build('generator-drill', [
        '🚑 Emergency Plan (Automatic Generation / Drill)',
        'Automatic generation and drill',
        '📖 View the Emergency Plan (Automatic Generation / Drill) user guide',
        'Plan generation elements: according to the scenario, earthquake, fire or flood, and the role, list the division of responsibilities, warning signals, evacuation routes and assembly points, and the contact and reporting procedure. The drill steps cover five phases, preparation, warning, evacuation, headcount and debrief, each with a time limit and a responsible person, and can be exported for training.',
        '📚 In-depth analysis: Emergency Plan (Automatic Generation / Drill)',
        'Unit safety drill planning: the safety officer enters the number needed, for example 5, and the tool randomly generates the corresponding drill list from 8 categories of site plan templates — office building, home, shopping mall, metro, hospital, school, high-rise residential and outdoor — covering different scenarios.',
        'Community or household plan making: quickly generate shelter plans for residences and high-rise households, covering drop, cover and hold on, shutting off gas and power, and evacuating by the stairs, and state the recommended drill cycle.',
        'Emergency training material generation: training organisations export batches of plans as case studies, each containing key steps and a recommended drill frequency, ready for training or drill scheduling.',
        'Example: generating 5 drill plans',
        'Entering a count of 5, the tool randomly draws 5 plans from the template pool of 8 categories and outputs them in turn, for example "1. Earthquake emergency evacuation plan for office buildings, schools and other crowded places — key steps: shelter nearby, protect the head, evacuate in order, count heads, assemble and report — drill cycle: once every six months", and so on up to the fifth. Each plan contains the scenario, the key steps and the recommended drill cycle, and can be used directly for drill scheduling or training material.',
        'What types of sites do the plans cover?',
        'Eight built-in templates: earthquake emergency evacuation for crowded places, household shelter, shopping mall crowd control, metro suspension, hospital patient transfer, school desk shelter, high-rise residential escape and outdoor shelter, which basically cover common scenarios.',
        'Why random drawing rather than a fixed order?',
        'Random drawing avoids repeating the same plan at every drill, making it easier for an organisation to rotate through different scenarios; if you need to fix a certain type, generate several times or filter manually after export.',
        'About Emergency Plan (Automatic Generation / Drill)',
        'An emergency plan, automatic generation and drill tool. A free online tool that runs entirely in the browser; data is never uploaded, keeping your privacy safe.',
    ]))

    write('stats-attenuation', build('stats-attenuation', [
        '🌋 Aftershock Frequency and Attenuation Model',
        'Estimate the b and a values from the G-R relation, and estimate the aftershock decay rate with Omori’s law',
        '📖 View the Aftershock (Statistics / Probability / Attenuation) Model user guide',
        'First, the Gutenberg-Richter frequency relation: estimate the b value from the aftershock magnitude sequence by maximum likelihood as lg e ÷ (mean − Mmin + ΔM/2) with ΔM = 0.1, and the a value as lg N + b·Mmin. Second, the modified Omori’s law n(t) = K/(t+c)^p: enter K, c, p and the number of days t since the main shock to estimate the aftershock frequency per unit time at time t.',
        'Aftershock magnitude sequence, separated by commas or line breaks',
        'Omori law parameters K, c in days, p, t in days',
        'Start analysis',
        '📚 In-depth analysis: Aftershock Frequency (G-R Relation) and Decay (Omori’s Law) Models',
        'Gutenberg-Richter frequency analysis: enter the aftershock magnitude sequence and estimate the b value, which reflects the ratio of large to small earthquakes, and the a value by maximum likelihood. A low b value means relatively few small and moderate events and energy concentrated in strong events.',
        'Omori decay estimation: given the parameters K, c and p and the origin time t, compute the modified Omori decay rate n(t) = K/(t+c)^p to assess how fast the aftershock frequency decays with time.',
        'Example: eight aftershock magnitudes',
        'For 3.0, 3.5, 4.0, 4.5, 5.0, 3.2, 4.1, 4.8 with a bin width ΔM = 0.1: mean 4.0125, Mmin = 3.0, b = lg e / (mean − Mmin + ΔM/2) = 0.4343/1.0625 ≈ 0.41; number of events N = 8, a = lg N + b·Mmin ≈ 2.13.',
        'What does the size of the b value tell us?',
        'A b value close to 1 means the ratio of large to small earthquakes matches typical tectonic seismicity, with the count increasing about tenfold for each magnitude unit decrease. A b value clearly below 1 often corresponds to specific mechanisms such as fluid injection or mining-induced events, and must be judged against the tectonic setting.',
        'How is the p value of Omori’s law used?',
        'The classic value is p ≈ 1; a larger p means faster aftershock decay and a shorter window of residual risk. c is the time smoothing constant in days, t is the number of days since the main shock, and n(t) is the estimated aftershock frequency per unit time at time t.',
        'About Aftershock (Statistics / Probability / Attenuation) Model',
        'An aftershock statistics, probability and attenuation model tool. A free online tool that runs entirely in the browser; data is never uploaded, keeping your privacy safe.',
        'e.g. 3.0,3.5,4.0,4.5',
    ]))


if __name__ == '__main__':
    main()
