#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'logistics')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'logistics')
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
    out = {'slug': slug, 'industry': 'logistics', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('checker-6', build('checker-6', [
        "⚖️ Quality Control (Operation / Quality / Inspection) Process",
        "Express service quality control metrics calculator. Enter business data to automatically compute loss rate / delay rate / damage rate / appeal rate and rate the grade against the YZ/T 0168 standard.",
        "Core formulas (by input variable): comp÷total×1000000; delayed÷total×100; damaged÷total×100",
        "/ Quality Control (Operation / Quality / Inspection) Process",
        "⚖️ Quality Control (Operation / Quality / Inspection) Process",
        "Total parcels handled (items)",
        "Statistical period",
        "Monthly",
        "Lost items",
        "Delayed items",
        "Damaged items",
        "Valid appeals",
        "Delivery feedback satisfaction (%)",
        "Compute QC metrics",
        "Copy QC report",
        "Competition (analysis / strategy / differentiation)",
        "About \"Quality Control (Operation / Quality / Inspection) Process\"",
        "An express service quality control metrics calculator. Enter the handled volume and the counts of lost, delayed, damaged and appealed items to automatically compute four quality control rates and rate the grade against the YZ/T 0168 standard.",
        "Four-dimension quality control metrics",
        "Automatic pass grade determination",
        "Quality control report generation",
        "Checked against industry standard YZ/T 0168",
        "Trend analysis suggestions",
        "Monthly QC assessment for express outlets",
        "Service quality improvement analysis",
        "Industry regulator inspections",
        "Internal corporate quality audits",
        "📚 Deep dive: Quality Control (Operation / Quality / Inspection) Process",
        "For monthly assessment, an express outlet enters total volume and the counts of lost, delayed, damaged and appealed items, automatically computing four quality control rates and checking them against the YZ/T 0168 limits to see whether they pass.",
        "When reviewing service quality improvement, compare quality control grades across different periods (month / quarter / year) to locate the stages that persistently exceed limits and focus remediation there.",
        "For internal audits or regulator inspections, generate a quality control report with one click (including standard limits, measured values and A–E grades) as compliance record material.",
        "Quality control report example",
        "Total volume 100 000 items, lost 3, delayed 20, damaged 15, valid appeals 1, satisfaction 96%: loss rate 0.003%, delay rate 0.02%, damage rate 0.015%, valid appeal rate 1 item per million, all four pass, overall grade \"Good (Grade B)\".",
        "Where do the standard limits come from?",
        "Loss rate ≤0.01%, delay rate ≤0.05%, damage rate ≤0.03%, valid appeal rate ≤2 items per million, based on the YZ/T 0168 national standard for express services; satisfaction ≥95% distinguishes Grade A from Grade B. For formal assessment, always defer to the latest standard text.",
        "How are grades determined?",
        "All four metrics passing with satisfaction ≥95% is Excellent (Grade A); all four passing is Good (Grade B); three passing is Qualified (Grade C); two is Basically Qualified (Grade D); fewer than two is Unqualified (Grade E).",
        "Total parcel loss rate should be ≤0.01% per YZ/T 0168",
        "Total parcel delay rate should be ≤0.05% per YZ/T 0168",
        "Total parcel damage rate should be ≤0.03% per YZ/T 0168",
        "Valid appeal rate should be ≤2 items per million",
        "Quality control data should be compiled monthly and continuously improved",
    ]))
    write('detector-30', build('detector-30', [
        "🔍 Quality Control (Process / Standard / Inspection) Mechanism",
        "Enter fresh produce quality parameters to rate the freshness grade and shelf life against industry standards.",
        "Quality Control (Process / Standard / Inspection) Mechanism",
        "/ Quality Control (Process / Standard / Inspection) Mechanism",
        "📖 Read the Fresh Produce Freshness Inspection and Shelf Life Estimation user guide",
        "Overall freshness score = appearance (0 to 3) + odor (0 to 3) + texture (0 to 3) − temperature and time penalty; each 5 ℃ above the suitable storage temperature costs 1 point; remaining shelf life = base shelf life × score factor × (1 − time already stored ÷ base shelf life), and when the temperature is above 10 ℃ apply accelerated decay for refrigerated goods then multiply by 0.5; an overall score of 7 or above is fresh, 4 to 6 is sub-fresh, and below 4 is not fresh and must be removed from the shelf.",
        "Fresh produce category",
        "Leafy vegetables",
        "Fruits",
        "Fresh meat",
        "Seafood",
        "Storage temperature (°C)",
        "Storage time (h)",
        "Appearance score (1-10)",
        "Odor score (1-10)",
        "Texture score (1-10)",
        "Assess quality",
        "📚 Deep dive: Fresh Produce Freshness Inspection and Shelf Life Estimation",
        "Incoming quality control: score leaf vegetables / fruits / fresh meat / seafood on arrival on temperature, appearance, odor and texture on a 10-point scale each, automatically rating freshness and estimating remaining shelf life.",
        "Cold chain verification: temperature violations (e.g. leaf vegetables >2℃, seafood >0℃) significantly cut the temperature score and shorten estimated shelf life, used to judge whether the cold chain broke.",
        "Display management: combined with time already stored, prioritize promotions or removal for near-expiry items (short remaining shelf life) to reduce spoilage loss.",
        "Temperature score ts: measured temp ≤ category limit tl scores 10, ≤tl+4 scores 5, otherwise 2; overall score avg=(appearance+odor+texture+temperature score)/4; grade: avg≥8 grade 1 (fresh), ≥6 grade 2 (fairly fresh), ≥4 grade 3 (average), otherwise unqualified; temperature factor tf: temp ≤tl is 1, ≤tl+4 is 0.8, otherwise 0.3; remaining shelf life = max(0, round((category max shelf hours ms − hours already stored)×tf)). Category limits / max shelf: leafy vegetables 2℃/72h, fruits 5℃/168h, fresh meat 2℃/48h, seafood 0℃/24h.",
        "Leafy vegetables, measured temp 4℃, stored 24h, appearance 8, odor 8, texture 7: tl=2, 4>2 and ≤6 → temperature score 5; avg=(8+8+7+5)/4=7.0 → grade 2 (fairly fresh); tf=0.8; remaining shelf life = round((72−24)×0.8)=round(38.4)=38 hours. If the temperature rises to 8℃ (>tl+4), the temperature score drops to 2, tf=0.3, and remaining shelf life is only round((72−24)×0.3)=14 hours, clearly shortened.",
        "How does the scoring relate to GB/T 31081?",
        "The temperature thresholds and shelf references in this tool follow the cold chain ranges in GB/T 31081 for fresh agricultural product delivery services, but the overall score is a demonstration model. Actual acceptance should defer to corporate quality control standards and sensory judgment.",
        "Why does remaining shelf life fall sharply with temperature?",
        "The temperature factor tf drops from 1 or 0.8 to 0.3 once the limit is exceeded, and stored time keeps consuming ms; the longer the cold chain break lasts, the shorter the remaining shelf life. So testing on arrival and storing cold is what preserves shelf life.",
        "Fresh produce quality control is based on GB/T 31081 for fresh agricultural product delivery services",
        "Key cold chain temperatures: leafy vegetables 2-8°C, fruits 5-10°C, fresh meat 2-7°C, seafood 0-4°C",
        "Every 10°C rise speeds quality degradation by roughly 2-3 times",
        "Sensory scores should be given independently by at least 2 quality control staff",
        "Any score below 4 points on appearance, odor or texture should be judged unqualified",
        "Competition (analysis / strategy / differentiation)",
        "Loss (control / prevention / analysis) system",
        "About \"Quality Control (Process / Standard / Inspection) Mechanism\"",
        "A fresh produce quality assessment tool that takes appearance, odor, texture scores and storage temperature, comprehensively rates the freshness grade and estimates remaining shelf life.",
        "Quality control standards for four fresh produce categories",
        "Automatic temperature compliance scoring",
        "Remaining shelf life estimation",
        "Multi-dimension sensory quality assessment",
        "Fresh produce e-commerce quality control",
        "Supermarket fresh produce acceptance",
        "Cold chain logistics monitoring",
        "Fresh produce grading",
    ]))
    write('assessor-carbon', build('assessor-carbon', [
        "📋 Logistics Carbon Emissions and New Energy Assessment",
        "Computes the carbon emissions of different transport modes, compares the emission reduction of new-energy vehicles, assesses green logistics level, and outputs a carbon emission report with reduction suggestions.",
        "\"Computes the carbon emissions of different transport modes, compares the emission reduction of new-energy vehicles, assesses green logistics level, and outputs a carbon emission report with reduction suggestions.\" Computed professionally from the input parameters, with results output.",
        "Green (new energy / carbon) assessment",
        "/ Green (new energy / carbon) assessment",
        "Carbon emission calculation",
        "New energy comparison",
        "Diesel truck (0.062 kgCO₂/ton-km)",
        "Gasoline truck (0.045 kgCO₂/ton-km)",
        "Rail transport (0.010 kgCO₂/ton-km)",
        "Inland waterway shipping (0.016 kgCO₂/ton-km)",
        "Ocean shipping (0.008 kgCO₂/ton-km)",
        "Air transport (0.602 kgCO₂/ton-km)",
        "Battery-electric truck (0.020 kgCO₂/ton-km)",
        "Cargo weight (tons)",
        "Transport distance (km)",
        "Trips per year",
        "Diesel consumption per 100 km (L)",
        "Electric consumption per 100 km (kWh)",
        "Daily mileage (km)",
        "Operating days per year",
        "Diesel CO₂ emission factor 2.73 kg/L; grid CO₂ emission factor 0.581 kg/kWh; diesel price 7.5 CNY/L; electricity price 1.0 CNY/kWh",
        "Emission factors reference GB/T 32150 and common industry values; actual values vary by vehicle type and road conditions",
        "Air transport has the highest carbon emissions and sea shipping the lowest; rail and water transport are the first choice for low-carbon transport",
        "The full life cycle carbon emissions of battery-electric trucks are still lower than diesel trucks (accounting for grid emission factors)",
        "This tool is for carbon emission estimation and does not replace professional carbon verification",
        "📚 Deep dive: Transport Carbon Emissions and New Energy Substitution Assessment",
        "Compare the carbon emissions of the same batch of cargo by diesel truck, rail and waterway to provide a basis for selecting a green transport plan.",
        "Replace diesel trucks with battery-electric trucks and estimate annual emission reduction and diesel saved, to support new-energy vehicle purchase justification.",
        "Account for scope 3 (purchased transport) emissions in the annual ESG report, accumulating by transport mode × ton-km.",
        "Comparing transport modes for 10 tons over 800 km",
        "Weight 10 t, distance 800 km, 24 trips per year. Diesel truck factor 0.062 kgCO₂/ton-km: single trip 0.062×10×800=496 kg, annual 11 904 kg≈11.9 tCO₂. Switching to rail (0.010): single trip 80 kg, annual 1 920 kg≈1.92 tCO₂, annual reduction about 9.98 tCO₂, a drop of about 84%. If switched to a battery-electric truck (0.020): single trip 160 kg, annual 3.84 tCO₂, a reduction of about 68%.",
        "Where do the emission factors come from?",
        "The tool has default factors for common modes built in (diesel truck 0.062, gasoline truck 0.045, rail 0.010, inland waterway 0.016, ocean 0.008, air 0.602, battery-electric truck 0.020 kgCO₂/ton-km). For formal disclosure, replace them with the latest factors for your local grid and fuel mix.",
        "Are battery-electric trucks zero emission?",
        "No. The tool counts indirect emissions from electricity generation at 0.020 kgCO₂/ton-km; if you use green power or charge with your own photovoltaic, you can lower the transmission and distribution factors accordingly.",
        "About \"Logistics Carbon Emissions and New Energy Assessment\"",
        "A logistics transport carbon emission calculator and new energy reduction assessment tool that supports carbon emission computation and comparison across multiple transport modes, and evaluates the carbon reduction effect and economics of replacing diesel trucks with battery-electric trucks.",
        "Carbon emission factor calculation for 7 transport modes",
        "Carbon emission comparison across transport modes",
        "Battery-electric vs diesel truck reduction and economics analysis",
        "Carbon emission grading and reduction suggestions",
        "Logistics company carbon accounting",
        "Green logistics plan assessment",
        "New energy vehicle replacement decisions",
        "ESG report carbon emission data support",
    ]))

if __name__ == '__main__':
    main()