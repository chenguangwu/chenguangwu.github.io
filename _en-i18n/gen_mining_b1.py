#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'mining')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'mining')
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
    out = {'slug': slug, 'industry': 'mining', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('calc-ventilation', build('calc-ventilation', [
        "🧮 Mine Ventilation Airflow Calculator",
        "Computes the required airflow by four methods from the number of people working underground, diesel equipment power, the explosive quantity per blast and the gas emission rate, takes the maximum and multiplies it by the leakage factor to give the design airflow.",
        "Core formula (by input variables): design÷60",
        "Number of people working underground",
        "Total diesel equipment power (kW)",
        "Explosive quantity per blast (kg)",
        "Gas emission rate (m³/min)",
        "Allowable gas concentration (%)",
        "Leakage factor",
        "💡 By headcount Q₁=4N; by diesel equipment Q₂=4P; by explosive quantity Q₃=25A; by gas Q₄=100q/C; design airflow = max(Q₁,Q₂,Q₃,Q₄) × leakage factor.",
        "📊 Calculation Methods and Unit Airflow Reference",
        "By headcount: 4 m³/min per person (required airflow for underground personnel in the Coal Mine Safety Regulations)",
        "By diesel equipment: 4 m³/min per kW of power",
        "By explosive quantity: 25 m³/min per kg of explosive (empirical value for diluting toxic gas after blasting)",
        "By gas emission rate: Q = 100q/C, where C is the allowable concentration (%, CH₄ taken as 1%)",
        "The formulas are general empirical values; in practice they must be verified against the mine gas classification, roadway cross-section and ventilation mode",
        "The design airflow must satisfy the maximum of all methods and leave leakage margin",
        "📚 In-Depth Analysis: Mine Ventilation Airflow Calculator",
        "Compute required airflow with parallel criteria per the mine safety regulations: headcount, diesel equipment, explosive quantity and gas emission, taking the maximum as the controlling item.",
        "Airflow comparison at the design stage: adjust the leakage factor k and watch how the design airflow (m³/min and m³/s) changes, reserving fan margin.",
        "Ventilation system review: after measured gas emission changes, back-calculate whether the gas item is still the controlling item and judge whether the fan capacity is sufficient.",
        "Formula definitions",
        "Four required airflows: by headcount Q1=4N; by diesel equipment Q2=4P (P total power in kW); by explosive quantity Q3=25A (A explosive per blast in kg); by gas Q4=100q/C (q emission in m³/min, C allowable concentration in %). Controlling item=max(Q1..Q4); design airflow=controlling item×leakage factor k; design airflow (m³/s)=design airflow/60.",
        "Underground 30 people, diesel equipment 120 kW, 50 kg per blast, gas emission 3 m³/min, allowable concentration 1%, leakage factor 1.2. Q1=120, Q2=480, Q3=1250, Q4=300; controlling item Q3=1250 m³/min (by explosive quantity), design airflow=1250×1.2=1500 m³/min=25.00 m³/s.",
        "Boundary: controlling item switching",
        "When the gas emission q grows to around q=100×C, Q4 approaches and exceeds Q3. For example with q=15 and C=1, Q4=1500>Q3 and the controlling item switches to the gas item. Design should be based on the most adverse condition (maximum explosive quantity or maximum gas emission) and ensure the fan still has margin under the controlling condition.",
        "Why take the maximum of the four criteria?",
        "Required airflow must simultaneously satisfy dilution of all contaminants and oxygen supply for people; any insufficient item becomes a safety bottleneck, so the maximum across criteria becomes the controlling item (the weakest link of the barrel). This is the parallel checking approach required by the regulations, not a weighted average.",
        "What does a leakage factor of 1.2 mean?",
        "The leakage factor k is the multiplier by which the fan must supply more than the effective airflow at the working point to offset leakage in roadways (k≥1). k=1.2 means the fan must supply 20% more air to offset losses. With long roadways, many air doors and poor sealing, k is larger, and design should use measured or empirical values.",
        "About \"Mine Ventilation Airflow Calculator\"",
        "Used to estimate required airflow for mine ventilation design. The required airflow is computed by four methods from underground headcount, diesel equipment power, explosive quantity per blast and gas emission rate, and the maximum is multiplied by the leakage factor to give the design ventilation airflow (m³/min and m³/s).",
        "Four methods computed in parallel",
        "Automatically identifies the controlling item",
        "Supports custom leakage factor and allowable gas concentration",
        "Preliminary mine ventilation system design",
        "Main fan selection airflow check",
        "Gas mine ventilation safety assessment",
        "Post-blast airflow verification",
        "Working headcount",
        "Diesel equipment power",
        "Explosive quantity",
        "Gas emission rate",
        "Allowable gas concentration",
        "Leakage factor",
    ]))

    write('haulage-optimization', build('haulage-optimization', [
        "❤️ Mine Cart Haulage Optimisation",
        "Compute mine cart loading, cycle time, shift capacity and the number of carts required, optimising haulage efficiency",
        "Core formula (by input variables): shiftMinutes × utilization ÷ 100",
        "Haulage task",
        "Total haulage per shift (tonnes)",
        "Shift working time (min)",
        "Cart parameters",
        "Cart rated load (tonnes)",
        "Loading factor (0.8-1.0)",
        "Time parameters (minutes)",
        "Loading time",
        "Loaded travel time",
        "Dumping time",
        "Empty return time",
        "Waiting / dispatch time",
        "Equipment utilisation (%)",
        "Optimised calculation",
        "📖 Haulage Optimisation Notes",
        "Actual load",
        "= rated load × loading factor",
        "Cycle time",
        "= loading + loaded travel + dumping + empty return + waiting",
        "Effective working time",
        "= shift time × equipment utilisation",
        "Trips per cart per shift",
        "= effective working time ÷ cycle time",
        "Output per cart per shift",
        "= trips per shift × actual load",
        "Number of carts required",
        "= total haulage per shift ÷ output per cart per shift (rounded up)",
        "Optimisation advice",
        "A low loading factor means the cart is not filled, so loading method can be improved",
        "A high waiting time share means dispatch needs optimising; add passing bays or adjust shifts",
        "When equipment utilisation falls below 70%, investigate faults or waiting for material",
        "The number of carts and loaders must be matched to avoid \"carts waiting for loader\" or \"loader waiting for carts\"",
        "📚 In-Depth Analysis: Mine Cart Haulage Optimisation",
        "Fleet sizing: given shift output, working duration and per-cart parameters, find the minimum number of carts required and look at the capacity margin.",
        "Efficiency diagnosis: analyse loading factor, waiting time and equipment utilisation to locate the haulage bottleneck and get optimisation tips.",
        "Scheme comparison: adjust cycle time (such as shortening waiting or reversing) and see how vehicle demand and capacity utilisation change.",
        "Formula definitions",
        "Actual load=carriage capacity×loading factor; cycle time=loading+loaded travel+dumping+empty return+waiting; effective working time=shift hours×utilisation/100; trips per shift=effective time/cycle; output per cart per shift=trips×actual load; carts required=ceil(shift output/output per cart); capacity margin=(total capacity−shift output)/shift output; effective running ratio=(load+travel+dump+return)/cycle×100.",
        "Shift output 1500 t, shift time 480 min, carriage 20 t, loading factor 0.9, load 5 / travel 12 / dump 3 / return 10 / wait 3 min, utilisation 75%. Actual load 18 t, cycle 33 min, effective 360 min, trips 10.909, output per cart 196.36 t, carts needed ceil(1500/196.36)=8, total capacity 1570.9 t, margin 4.73%, effective running ratio 90.9%.",
        "Boundary: cart count rounding and margin",
        "The required cart count is rounded up (7.64→8), and the 8th cart is often not fully loaded, so the margin looks small (4.73%). If utilisation drops to 70% or the waiting share exceeds 15%, the cart count rises sharply; slight fluctuation can turn \"just enough\" into \"not enough\", so configure 1–2 carts of margin.",
        "Utilisation of 75% is already decent — why still leave a margin?",
        "Cycle time is an average, and in reality there are random fluctuations from loading queues, road conditions and shift handovers; at 75% utilisation the effective running ratio is 90.9%, leaving about 9% as non-productive time. After rounding the 8th cart often runs partly empty so the margin is only 4.73%, and any delay could leave the shift short, so sites normally add 1–2 carts to absorb fluctuation.",
        "What does a high waiting time share indicate?",
        "Waiting above 15% of the cycle usually points to a dispatch or loading/unloading point bottleneck (such as a cart waiting for the excavator, or too few dumping positions). The optimisation direction is to add loading/dumping points, stagger dispatch or balance the cycle stages, rather than simply adding carts — which can actually worsen queuing.",
        "About \"Mine Cart Haulage Optimisation\"",
        "Mine Cart Haulage Optimisation is an online tool in the scientific research field. A scientific research tool using standard scientific formulas with precise calculation.",
    ]))

    write('reserve-estimate', build('reserve-estimate', [
        "🔮 Reserve Estimator",
        "Geological block method reserve estimation: compute tonnage and metal content from block area, average thickness, ore density and grade",
        "Volumetric reserve: ore volume V = block area × average thickness; tonnage Q = V × density; metal content = Q × grade × recovery rate, converted accordingly when the grade unit is % or g/t; the block method weights each block's area and thickness to get the total reserve, for preliminary mine evaluation and reporting.",
        "Block parameters",
        "Block area (m²)",
        "Average thickness (m)",
        "Ore density (t/m³)",
        "Average grade (g/t or %)",
        "g/t (grams per tonne, precious metals)",
        "% (percentage, non-ferrous metals)",
        "Recovery rate (%)",
        "Estimate reserve",
        "📖 Principle of the Block Method",
        "Ore volume",
        "= block area × average thickness",
        "Tonnage (geological reserve)",
        "= ore volume × ore density",
        "Metal content",
        "= tonnage × grade (g/t ÷ 1000 gives kg, % ÷ 100 gives t)",
        "Recoverable reserve",
        "= geological reserve × recovery rate",
        "Common Ore Density Reference",
        "Magnetite ore: 3.5-4.5 t/m³",
        "Hematite ore: 2.5-3.5 t/m³",
        "Copper ore: 2.6-3.0 t/m³",
        "Gold ore: 2.6-2.8 t/m³",
        "Lead-zinc ore: 3.0-3.5 t/m³",
        "Coal: 1.3-1.5 t/m³",
        "Reserve Classification",
        "Proven reserve",
        ": high exploration level, error ≤ 10%",
        "Probable reserve",
        ": moderate exploration level, error 10%-30%",
        "Inferred reserve",
        ": low exploration level, error > 30%",
        "📚 In-Depth Analysis: Reserve Estimator",
        "Quick estimate of a single orebody: enter area, average thickness, density, grade and recovery to get geological reserve, metal content and recoverable reserve.",
        "Preliminary judgement of deposit size: use the geological reserve classification (very large / large / medium / small) to guide exploration investment and development decisions.",
        "Recoverability assessment: convert the geological reserve into recoverable reserve using the recovery rate, flagging resource loss.",
        "Formula definitions",
        "Volume=area×thickness; geological reserve (tonnes)=volume×density; metal content: g/t mode=reserve×grade/1000 (kg), % mode=reserve×grade/100 (t); recoverable reserve=geological reserve×recovery/100; recoverable metal=metal content×recovery/100. Size: ≥100 million t very large, ≥10 million large, ≥1 million medium, ≥100,000 small, below that a mineral occurrence.",
        "Area 50,000 m², thickness 12.5 m, density 2.8 t/m³, grade 3.2 g/t, recovery 85%. Volume 625,000 m³, geological reserve 1,750,000 t (1.75 million t, a \"medium deposit\"), metal content 5,600 kg (5.60 t), recoverable reserve 1,487,500 t, recoverable metal 4.76 t.",
        "Boundary: switching between g/t and %",
        "The default is g/t (precious metals). If % is chosen by mistake with grade 3.2, metal content becomes 1,750,000×3.2/100=56,000 t (a factor of 10,000 off). The grade unit must match the mineral: gold and silver use g/t, copper/iron/lead/zinc use %.",
        "What is the difference between geological and recoverable reserve?",
        "Geological reserve is the total in-situ resource converted with density, while recoverable reserve is the part actually extractable after mining loss (recovery <100%). At 85% recovery, a geological reserve of 1,750,000 t yields 1,487,500 t recoverable (about 15% lost). Recovery is affected by mining method, host rock stability and grade distribution.",
        "Is 1.75 million tonnes medium or large?",
        "By common classification: ≥100 million tonnes very large, ≥10 million large, ≥1 million medium. 1.75 million t falls in the medium range. Thresholds differ by mineral and country (coal and metal ore differ substantially), so these thresholds are for quick preliminary judgement; a formal reserve report should follow the applicable code (such as the DZ/T standard).",
        "About \"Reserve Estimator\"",
        "Reserve Estimator is an online tool in the scientific research field. A scientific research tool using standard scientific formulas with precise calculation.",
    ]))

    write('checker-training-hr', build('checker-training-hr', [
        "✅ Safety (Regulations / Inspection / Training) System",
        "Compliance assessment of the mine safety regulation / inspection / training system, scoring five dimensions against the Coal Mine Safety Regulations and judging the safety level",
        "The compliance assessment of the mine safety regulation / inspection / training system scores five dimensions against the Coal Mine Safety Regulations from the input parameters and outputs the result.",
        "Return airway gas concentration CH₄ (%)",
        "Actual airflow (m³/min)",
        "Mine required airflow (m³/min)",
        "Safety equipment intact rate (%)",
        "All-staff safety training completion rate (%)",
        "Annual training hours per person",
        "Safety hazard rectification rate (%)",
        "Monitoring coverage rate (%)",
        "Run safety assessment",
        "About \"Safety (Regulations / Inspection / Training) System\"",
        "A compliance assessment tool for mine safety regulations / inspection / training systems, scoring and judging the safety level across five dimensions — gas concentration, ventilation, equipment, training and hazard rectification — against the Coal Mine Safety Regulations.",
        "Five-dimension safety system assessment",
        "Real-time gas concentration judgement",
        "Ventilation safety calculation",
        "Training hours verification",
        "Safety hazard management advice",
        "Monthly mine safety inspection",
        "Safety management system audit",
        "Emergency management department inspection",
        "Work safety standardisation review",
        "📚 In-Depth Analysis: Safety (Regulations / Inspection / Training) System Assessment",
        "Self-assessment for work safety standardisation: enter measured gas, ventilation, equipment, training, rectification and monitoring values item by item to get the number of compliant items and the grade automatically.",
        "Inspection preparation: check each threshold against the standardisation score sheet (such as airflow ratio ≥1.0, equipment intact rate ≥95%) to locate non-compliant items.",
        "Rectification tracking: record the hazard rectification rate and monitoring coverage and observe whether the grade rises from basically compliant to standardised.",
        "Formula definitions",
        "Six checks: ①gas concentration ≤1.0% compliant; ②airflow ratio=measured/required ≥1.0 compliant; ③equipment intact rate ≥95% compliant; ④training pass rate ≥90% and training hours ≥24h compliant; ⑤hazard rectification rate ≥90% compliant; ⑥monitoring coverage ≥95% compliant. 6 compliant items = level 1, ≥5 level 2, ≥4 level 3, ≥3 basically compliant, <3 non-compliant requiring production suspension.",
        "Gas 0.6%, ventilation measured 8000 / required 7500 (ratio 1.067), equipment intact 96%, training pass 95% with 28h hours, rectification rate 92%, monitoring coverage 98%. All six compliant, airflow ratio 1.067≥1.0, judged \"work safety standardisation (level 1)\".",
        "Boundary: threshold judgements",
        "Training pass 95% but only 20 hours; since 20<24 it is judged non-compliant and the overall drops to level 2. Gas 1.0% is exactly compliant (≤1.0) while 1.01% is not. Threshold values use closed intervals (≤/≥), so leave safety margin when entering data.",
        "What is the basis for grading from standardisation level 1 to non-compliant?",
        "It follows the thinking of the metal and non-metal mine work safety standardisation specification, grading by the number of compliant key safety thresholds: all compliant is level 1, missing 1 item level 2, missing 2 items level 3, missing 3 items basically compliant, and missing 4 or more is non-compliant requiring suspension and rectification. This tool uses a simplified six-item threshold; an actual review has more items, so follow the current score sheet.",
        "Why does training look at both hours and pass rate?",
        "The pass rate is the outcome, the hours are the process. A good pass rate with insufficient hours (such as crammed make-up training) does not guarantee solid knowledge and emergency response; both conditions (pass ≥90% and hours ≥24h) must hold for training to be compliant, which avoids padding the numbers with certificates.",
        "Gas concentration follows the Coal Mine Safety Regulations: return airway CH₄ ≤1%",
        "Airflow must meet the mine required airflow; production beyond ventilation capacity is strictly forbidden",
        "All-staff safety training at least 24 hours per year, new workers at least 72 hours",
        "Safety equipment intact rate should be ≥95%, with full monitoring and control coverage",
        "Safety hazard investigation follows closed-loop management; major hazards require listed supervision with public notice",
    ]))


if __name__ == '__main__':
    main()