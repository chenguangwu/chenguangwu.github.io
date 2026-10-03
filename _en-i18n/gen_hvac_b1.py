#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'hvac')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'hvac')
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
    out = {'slug': slug, 'industry': 'hvac', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('air-filter', build('air-filter', [
        "⚡ Air Filter Grade Lookup",
        "Select a standard and grade to view detailed parameters such as gravimetric efficiency, counting efficiency, face velocity, initial resistance and final resistance.",
        "Based on the entered parameters, the tool performs a professional calculation and outputs the result for the selected standard and grade, displaying gravimetric efficiency, counting efficiency, face velocity, initial resistance and final resistance.",
        "Air Filter Efficiency Grade Query Tool",
        "/ Air Filter Efficiency Grade Query Tool",
        "📖 View the \"Air Filter Grade Lookup User Guide\"",
        "Grade lookup",
        "Selection advice",
        "Resistance calculation",
        "Standard comparison table",
        "EN 779 (coarse G / medium F)",
        "ISO 16890 (ePM grades)",
        "Filter grade",
        "Copy parameters",
        "Calculate resistance with this grade →",
        "🎯 Filter selection advice",
        "Recommended filter-grade combinations and configuration schemes based on application scenario.",
        "Residential / home fresh-air",
        "Commercial / public buildings",
        "Hospital / medical",
        "Cleanroom / industrial",
        "💨 Filter resistance calculation",
        "Enter the airflow and filter cross-section dimensions to estimate the face velocity and initial/final resistance (linearly scaled from the rated parameters of the selected grade).",
        "Airflow Q (m³/h)",
        "Section width W (mm)",
        "Section height H (mm)",
        "Enter area A directly (m²)",
        "Calculate resistance",
        "📑 Comparison table of the three major standards",
        "Comparison of ISO 16890, EN 779 and EN 1822 grades, test methods and applications. EN 779 was withdrawn in 2016 and replaced by ISO 16890; EN 1822 still applies to EPA/HEPA/ULPA.",
        "📚 In-Depth Analysis: Selecting Air Filters by Grade and Airflow",
        "Select G/F/H grades for the fresh-air / return-air section of central air conditioning according to cleanliness requirements, balancing resistance and replacement cost.",
        "For cleanrooms, select H11 to H14 by particle-size efficiency and check whether the face velocity at rated airflow exceeds the limit.",
        "For retrofit projects, compare the total resistance and energy consumption of coarse + medium + high-efficiency three-stage configurations.",
        "592×592 frame, airflow 2000 m³/h",
        "Face velocity = 2000 ÷ (0.592×0.592) ÷ 3600 ≈ 1.58 m/s, within the normal 1.5–2.5 m/s range; coarse G4 has gravimetric efficiency ≥90% for ≥5 μm and a final resistance typically 100–150 Pa.",
        "Cleanroom selects H13",
        "H13 has counting efficiency ≥99.95% at 0.3 μm and a resistance of about 200–250 Pa at rated airflow, so the unit's external static pressure margin must be checked for sufficiency.",
        "How to distinguish G4/F7/H13?",
        "G is coarse (large dust), F is medium (fine dust), H is high-efficiency (sub-micron); they are graded by particle-size efficiency under EN 779 / ISO 29463, with larger numbers being finer.",
        "What happens if the face velocity is too high?",
        "Excessively high face velocity raises resistance and energy use and may blow through the media; below the lower limit the effective filtration area is wasted, so select according to the manufacturer's rated face velocity.",
        "About the Air Filter Efficiency Grade Query Tool",
        "The Air Filter Efficiency Grade Query Tool is an online reference tool for HVAC design and operation. It supports the three major air-filter standards ISO 16890, EN 779 and EN 1822, and queries key parameters of each grade such as gravimetric efficiency, counting efficiency, overall MPPS efficiency, rated face velocity, initial resistance and final resistance, while providing scenario-based selection advice and a filter resistance calculation. It runs entirely in the browser with no data uploaded.",
        "Comparison of three standards (ISO 16890 / EN 779 / EN 1822)",
        "Covers all grades G, F, EPA, HEPA, ULPA",
        "Gravimetric, counting and MPPS efficiency parameters",
        "Initial resistance, final resistance and rated face velocity lookup",
        "Selection advice for residential / commercial / hospital / cleanroom",
        "Airflow and cross-section resistance estimation",
        "Filter selection for HVAC systems",
        "Ventilation design for cleanrooms and operating rooms",
        "Filter-element configuration reference for fresh-air systems",
        "Filter resistance and replacement-interval estimation",
        "Filter standard comparison and study",
        "Semiconductor / pharmaceutical clean-environment planning",
        "Toggle dark mode",
        "Leave blank to calculate by width × height",
    ]))

    write('chiller-efficiency', build('chiller-efficiency', [
        "🧮 Chiller COP/EER Energy Efficiency Calculator",
        "Calculate the chiller's coefficient of performance COP, energy efficiency ratio EER and kW/RT, and determine the energy-efficiency grade against GB 19577-2015",
        "Based on the entered parameters, the tool performs a professional calculation and outputs the chiller's COP, EER and kW/RT and its energy-efficiency grade per GB 19577-2015.",
        "Chiller Energy Efficiency Calculator",
        "📖 View the \"Chiller COP/EER Energy Efficiency Calculator User Guide\"",
        "Cooling capacity input method",
        "kW (kilowatt)",
        "US.RT (refrigeration ton)",
        "Cooling capacity",
        "Compressor input power",
        "Chilled water inlet temperature",
        "Chilled water outlet temperature",
        "📊 Calculate efficiency",
        "📋 GB 19577-2015 Energy Efficiency Grade Reference Table",
        "COP limit value",
        "Highest efficiency, premium energy-saving product",
        "Energy-saving product",
        "Energy-efficiency limit (market entry)",
        "Below standard",
        "Below the limit value; sale prohibited",
        "GB 19577-2015 'Minimum Allowable Values of Energy Efficiency and Energy Efficiency Grades for Water Chillers' sets different limit values by unit type (air-cooled / water-cooled) and cooling-capacity band; the 6.1 / 5.6 / 5.0 in this table are reference values for water-cooled water chillers. In practice, follow the standard clauses for the corresponding unit type and capacity band.",
        "📈 IPLV Integrated Part-Load Value",
        "Enter the COP at each load point and compute the IPLV using the weighting factors of AHRI 550/590 and GB/T 18430",
        "Load point",
        "Weighting factor",
        "Weighted contribution",
        "100% load",
        "75% load",
        "50% load",
        "25% load",
        "📈 Calculate IPLV",
        ". The weighting factors reflect the share of operating time of each load segment in real building HVAC operation; the 50% load has the longest operating time (45%), so it has the greatest impact on IPLV.",
        "📚 In-Depth Analysis: Verifying Chiller COP/EER from Cooling Capacity and Electric Power",
        "During procurement or operation evaluation, divide cooling capacity by input power to obtain COP and compare unit efficiency horizontally.",
        "Summer and winter conditions differ; compute COP separately for design conditions and part-load to see actual energy savings.",
        "In energy-performance contracting, account for electricity savings and payback period from COP improvements.",
        "Cooling capacity 500 kW, power 142.17 kW",
        "COP = 500 ÷ 142.17 ≈ 3.52 kW/kW; if",
        "electric power",
        "is reduced to 125 kW, COP rises to 4.0, a significant efficiency improvement.",
        "EER basis",
        "In kcal/h vs W basis, EER and COP values are close; keep units consistent; at the same cooling capacity, lower power gives higher COP.",
        "What is a good COP?",
        "Centrifugal / screw chillers typically have COP 4.5–6.5, magnetic-bearing higher; it depends on unit type and design conditions and should not be compared across different conditions.",
        "Why is the actual value lower than the nameplate?",
        "The nameplate is at rated conditions; actual load rate, cooling-water temperature and fouling all lower COP, so part-load operating data should be used.",
        "About the Chiller COP/EER Energy Efficiency Calculator",
        "The Chiller COP/EER Energy Efficiency Calculator is a chiller energy-efficiency analysis tool for HVAC engineers. It computes the coefficient of performance COP, energy efficiency ratio EER, power per refrigeration ton kW/RT and integrated part-load value IPLV, and determines the energy-efficiency grade against GB 19577-2015. All calculations run locally in the browser with no data uploaded.",
        "Supports input switching between cooling capacity in kW and US refrigeration tons (RT)",
        "One-click calculation of COP, EER and kW/RT",
        "Chilled-water temperature difference and flow estimation",
        "IPLV part-load weighted calculation",
        "Automatic GB 19577-2015 efficiency-grade determination",
        "Result data cards + grade label visualization",
        "Chiller selection and efficiency evaluation",
        "Machine-room energy-retrofit effect analysis",
        "Equipment efficiency-grade compliance check",
        "HVAC design and scheme comparison",
        "Operating energy-consumption diagnosis and optimization",
        "HVAC study and teaching",
        "This tool runs entirely in the browser; all data are computed locally and never uploaded to a server",
        "The efficiency-grade limit values are GB 19577-2015 reference values for water-cooled water chillers; for different unit types and capacity bands follow the original standard text",
        "The IPLV weighting factors use the AHRI 550/590 and GB/T 18430 common coefficients (0.01 / 0.42 / 0.45 / 0.12)",
        "Chilled-water flow is estimated with specific heat 4.186 kJ/(kg·°C) and density 1000 kg/m³, for design reference only",
        "Results are for reference only; for actual engineering combine manufacturer catalogs with professional judgement",
        "Cooling capacity unit switch",
    ]))


if __name__ == '__main__':
    main()
