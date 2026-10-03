#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'fire')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'fire')
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
    out = {'slug': slug, 'industry': 'fire', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('analysis-cost-price-8', build('analysis-cost-price-8', [
        "Price (Market/Cost/Competition) Analysis",
        "Market/cost/competition",
        "View the Price (Market/Cost/Competition) Analysis User Guide",
        "Analysis indicators",
        "Gross profit = selling price - unit cost; gross margin = gross profit / selling price",
        "Uses the selling price, unit cost and competitor price list to evaluate per-unit profit, gross margin and market price position.",
        "Current selling price (yuan/unit)",
        "Unit cost (yuan/unit)",
        "Competitor prices (separated by commas or line breaks, yuan/unit)",
        "Analyse the price",
        "In-Depth Analysis: Price (Market/Cost/Competition) Analysis",
        "Pricing and competitor analysis is the basis of a sales strategy: from the selling price, unit cost and competitor price band, quantify the gross profit,",
        "and market position.",
        "When pricing a new product or adjusting a price, compare against the competitor range to judge whether you sit at the high end, the low end or the middle, avoiding a price detached from the market.",
        "When the gross margin is below the industry benchmark, trace back to the cost structure or adjust the selling price; the competitor average is an important reference anchor.",
        "Worked example: selling price 100, cost 60, competitors [80,90,100,110,120]",
        "Per-unit gross profit = 100 - 60 = 40.00 yuan; gross margin = 40/100x100 = 40.00%; competitor average = (80+90+100+110+120)/5 = 100.00 yuan; selling price relative to the competitor average = (100/100-1)x100 = 0.00% -> sits in the competitor range.",
        "Worked example: price position judgement",
        "If the selling price is < the lowest competitor it is 'below all competitors', > the highest competitor it is 'above all competitors', otherwise 'within the competitor range'. The conclusion changes in real time with the competitor set and the selling price, and it is only meaningful with at least 1 valid competitor price entered.",
        "What is the difference between gross margin and per-unit gross profit?",
        "Per-unit gross profit = price - cost (an absolute amount, yuan), gross margin = gross profit / price x 100% (a relative ratio). Gross margin excludes the effect of the price magnitude and is better for comparison across categories and price levels.",
        "Will an incomplete competitor price band affect the conclusion?",
        "Yes. The lowest/highest competitor determines the 'above/below all competitors' judgement, and the average determines the relative position. Too few samples or missing key competitors distort the positioning, so cover the mainstream competitors before drawing a conclusion.",
        "About Price (Market/Cost/Competition) Analysis",
        "Price (Market/Cost/Competition) Analysis. Free online tool, pure front-end processing, data is not uploaded, privacy and security protected.",
        "For example: 105,110,125,130",
    ]))

    write('calc-water-pressure-hydrant', build('calc-water-pressure-hydrant', [
        "Hydrant Pressure at the Most Unfavourable Point Calculation",
        "Enter two parameters to automatically compute the common results",
        "View the Hydrant Pressure at the Most Unfavourable Point Calculation User Guide",
        "Static pressure, elevation difference, required nozzle pressure and pipe local/friction losses are all converted to MPa in a unified way, and the result is used for scheme review.",
        "Inlet static pressure (MPa)",
        "Elevation difference (m)",
        "Required pressure at the hydrant outlet (MPa)",
        "Pipe loss (MPa)",
        "Compute the required pressure",
        "Static pressure conversion for water: every 10.2 m of elevation produces about a 0.1 MPa pressure difference; please replace the default values with your project's measured or hydraulic calculation results.",
        "In-Depth Analysis: Hydrant Pressure at the Most Unfavourable Point Calculation",
        "In hydrant system design, it is necessary to check whether the source inlet pressure can satisfy the sum of the outlet pressure, friction loss and elevation loss.",
        "During fire acceptance and renovation, the required inlet pressure is back-calculated from the static pressure, elevation difference, nozzle demand and pipe loss.",
        "When pressure is insufficient, boosting or flow resistance reduction is needed (enlarging the pipe diameter, shortening the pipe run), otherwise the firefighting jet does not meet the standard.",
        "Worked example: static pressure 0.8 MPa, elevation 30m, outlet 0.25, pipe loss 0.1",
        "Elevation conversion = 30/102 = 0.294 MPa; required inlet pressure = 0.294 + 0.25 + 0.1 = 0.644 MPa; safety margin = 0.8 - 0.644 = +0.156 MPa >= 0 -> satisfied.",
        "Worked example: margin criterion",
        "Margin = static pressure - (elevation conversion + outlet demand + pipe loss). A margin >= 0 is judged 'satisfied', < 0 is judged 'insufficient' and needs boosting or flow resistance reduction. Elevation is converted at about 102 m of water column = 1 MPa.",
        "Why is elevation converted to MPa at 102?",
        "The unit weight of water is about 9.8 kN/m3, and 10 m of water column = about 0.098 MPa, so 102 m is about 1 MPa. This is the common approximate conversion coefficient for elevation loss in hydrant pressure checks.",
        "What if the margin is negative?",
        "Prioritise enlarging the pipe diameter or shortening the pipe run to reduce the pipe loss, or raise the source static pressure (adding a booster pump). It is strictly forbidden to lower the outlet demand just to make the numbers work, otherwise the jet will not meet the extinguishing requirement.",
        "About Hydrant Pressure at the Most Unfavourable Point Calculation",
        "Hydrant Pressure at the Most Unfavourable Point Calculation. Free online tool, pure front-end processing, data is not uploaded, privacy and security protected.",
    ]))

    write('estimate-time-flow', build('estimate-time-flow', [
        "Personnel Safe Evacuation Time Estimation (Flow Method)",
        "Enter two parameters to automatically compute the common results",
        "View the Personnel Safe Evacuation Time Estimation (Flow Method) User Guide",
        "Walking time, exit queueing time and pre-movement time are added together to estimate the time needed for personnel to complete evacuation.",
        "Total effective exit width W (m)",
        "Pre-movement time Tpre (s)",
        "Estimate the evacuation time",
        "The flow method is a preliminary engineering model; exit distribution, bottlenecks and stair sections should be verified separately in a formal assessment.",
        "In-Depth Analysis: Personnel Safe Evacuation Time Estimation (Flow Method)",
        "In evacuation design, the total is estimated from the number of people, exit width, walking speed and travel distance",
        "evacuation time",
        "When writing the plan, the walking time, exit queueing time and pre-movement time are summed to get the total time.",
        "Insufficient exit capacity creates a queueing bottleneck, which is the main source of evacuation time.",
        "Worked example: 100 people, exit width 2m, flow 1.5 persons/(s·m), distance 30m, speed 1.2m/s, pre-movement 30s",
        "Walking = 30/1.2 = 25.0 s; queueing = 100/(2x1.5) = 33.3 s; total evacuation = 25.0 + 33.3 + 30 = 88.3 s (about 1.47 min); exit capacity = 2x1.5 = 3.00 persons/s.",
        "Worked example: bottleneck identification",
        "Total time = walking + queueing + pre-movement, where 'queueing = persons / (exit width x flow per unit width)' is the most sensitive factor in the result. Widening the exit or splitting the flow can significantly cut the queueing time.",
        "What value should the flow per unit width take?",
        "A common design value is about 1.3-1.5 persons/(s·m) (for a level exit), slightly lower for stairs. The reality depends on the occupant mix and familiarity; this tool uses your input, and the value should reference the current evacuation design code.",
        "What is the pre-movement time?",
        "It is the reaction time from a person noticing the fire to starting evacuation (perception, judgement, alarm, getting up), usually in the 30-60 s range. It does not depend on exit capacity but accounts for a considerable share of the total evacuation time, and drills can shorten it significantly.",
        "About Personnel Safe Evacuation Time Estimation (Flow Method)",
        "Personnel Safe Evacuation Time Estimation (Flow Method). Free online tool, pure front-end processing, data is not uploaded, privacy and security protected.",
    ]))

    write('evacuation-time', build('evacuation-time', [
        "Evacuation Time Estimation (Flow Method)",
        "Estimates the required safe evacuation time RSET and compares it with the available safe egress time ASET",
        "Evacuation Time Estimation",
        "/ Evacuation Time Estimation",
        "View the Evacuation Time Estimation (Flow Method) User Guide",
        "t = N/(b·D·f) + walking time",
        "In-Depth Analysis: Evacuation Time Estimation (Flow Method)",
        "In performance-based evacuation assessment, the required",
        "evacuation time",
        "RSET is computed and compared with the available safe time ASET.",
        "RSET = pre-movement + max(flow time, travel time), while ASET comes from fire simulation (smoke layer / temperature reaching a danger threshold).",
        "The safety criterion is ASET > RSET with a safety factor; too small a ratio is judged unsafe.",
        "Worked example: 100 people, width 2m, flow 1.5, distance 30m, speed 1.2, pre-movement 30s, ASET 120s",
        "tflow = 100/(2x1.5) = 33.3 s; ttravel = 30/1.2 = 25.0 s; RSET = 30 + max(33.3,25.0) = 63.3 s; margin = 120 - 63.3 = 56.7 s; ASET/RSET = 1.89.",
        "Worked example: safety criterion",
        "If ASET <= RSET then personnel may not be able to get out before the danger arrives and it is judged unsafe; generally ASET/RSET >= 1.5 is required (including a safety factor). The larger the margin the safer, and a ratio < 1 must be rectified (widen exits / shorten distances / control fire).",
        "Why does RSET take the larger of flow time and travel time?",
        "The two represent different bottlenecks: flow time depends on exit throughput, travel time depends on walking from the farthest point. The actual evacuation is determined by the slower one, so the max is taken to conservatively estimate the required evacuation time.",
        "How is ASET generally obtained?",
        "ASET comes from fire dynamics simulation (for example the smoke layer descending to a danger height, temperature/toxic gas reaching a threshold), and is an external input to this tool. RSET must be clearly smaller than ASET with a safety factor to count as safe.",
        "About Evacuation Time Estimation",
    ]))

    write('response-drill', build('response-drill', [
        "Fire Alarm Response Drill",
        "Randomly draw fire alarm response procedure steps to test emergency response capability",
        "View the Fire Alarm Response Drill User Guide",
        "Change the scenario",
        "Current scenario",
        "Drill instructions",
        "The system randomly selects a fire scenario (office, factory, school, etc.)",
        "A set of emergency response steps is given in shuffled order",
        "Click each step in the correct order",
        "Correct scores 10 points, wrong deducts 5 points and shows the correct position",
        "After all steps are complete the total score and elapsed time are shown",
        "Repeated practice improves emergency response speed and accuracy",
        "In-Depth Analysis: Fire Alarm Response Drill",
        "In fire drill planning, drill scenarios (fire point, trapped persons, hazard linkage) are generated randomly to train the response process and role division.",
        "Scenarios are tailored by unit type (mall / factory / office), covering the alarm, evacuation, firefighting and linkage links.",
        "After the drill, review the elapsed time and handling correctness to iteratively optimise the emergency plan.",
        "Example: generating a comprehensive drill scenario",
        "After clicking generate you get a random scenario card (such as 'electrical fire on the 2nd floor of a warehouse, 1 person trapped, smoke exhaust and broadcast linkage required'), execute alarm -> evacuation -> initial firefighting -> linkage per the card, and record the elapsed time of each link.",
        "Example: review by role",
        "Break the scenario down by command, alarm, evacuation guiding, firefighting action and first aid, and check the arrival status item by item; items not in place go into rectification and become the focus of the next drill.",
        "Can the drill scenarios be fully random?",
        "Randomness is useful for training adaptability, but it should be controlled within the coverage of the plan and also consider the unit's real risk points. A fixed high-risk scenario plus random perturbations is recommended, training both proficiency and unexpected handling.",
        "Is there a requirement for drill frequency?",
        "Most premises require at least one comprehensive drill per year and a special or tabletop exercise every six months (subject to the latest regulations and the unit's own system). High frequency with review is better than low frequency as a formality.",
        "About Fire Alarm Response Drill",
        "Fire Alarm Response Drill is an online tool in the business office field. Business office tools to improve work efficiency, with data processed locally to protect privacy.",
    ]))


if __name__ == '__main__':
    main()
