#!/usr/bin/env python3
# eco batch5 (5 tools, 含行业 index)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'eco')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'eco')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

BOIL = ("Results are estimated according to public standards and environmental factors, "
        "for science outreach, teaching and emission-reduction estimates; actual accounting "
        "should follow official guidelines (such as the GHG Protocol and provincial carbon "
        "emission factors) and measured data.")

def gen_desc(name):
    return (name + " is a free online eco & environmental tool: enter parameters to get results in real time; "
            "fully client-side, no data upload, no registration, just open it in a browser. Suitable for "
            "engineering estimates, everyday conversions and quick checks, with one-click copy of results.")

EN = {
'ecological-footprint': [
"🔮 Ecological Footprint Estimation",
"Roughly estimate the per-capita ecological footprint with empirical coefficients.",
'📖 View the "Ecological Footprint Estimation Guide"',
"Meat per week (kg)",
"Driving per week (km)",
"Electricity per month (kWh)",
"Flights per year",
"gha ≈ meat×0.0018 + driving×0.00012 + electricity×0.0005 + flights×0.3 (per year)",
"Global per-capita biocapacity is about 1.6 gha, for reference only.",
"📚 In-Depth Analysis: Ecological Footprint Estimation",
"Personal or regional estimate: enter the consumption mix to convert it into the biocapacity occupied by each category.",
"Overshoot assessment: compare the ecological footprint with the available biocapacity to judge whether there is a deficit.",
"Teaching demo: show that high-consumption regions far exceed local biocapacity.",
"Example: 2000 kWh of electricity per year ≈ 0.3 gha",
"Carbon Footprint",
" + food, timber and so on, often totalling more than 2 gha; the globally available figure is about 1.6 gha per person.",
"What is gha?",
"Global hectare, a unit of land area normalised to average global productivity, which makes different land uses comparable. " + BOIL,
"What is the relation to the carbon footprint?",
"The carbon footprint is the carbon component of the ecological footprint (the forest land needed to absorb CO₂) and is one of its largest items. " + BOIL,
"What does a deficit mean?",
"A footprint greater than biocapacity means ecological overshoot, which is unsustainable in the long run and requires greater efficiency or emission cuts. " + BOIL,
],
'electricity-carbon': [
"♻️ Electricity Carbon Emission Calculation",
"Estimate CO₂ emissions from electricity use and an emission factor.",
'📖 View the "Electricity Carbon Emission Calculation Guide"',
"Emission factor (kgCO₂/kWh)",
"CO₂ = electricity use × emission factor",
"One tree absorbs about 18.3 kg CO₂ per year",
"The average factor for China's grid is about 0.581, and green power can be as low as 0.",
"📚 In-Depth Analysis: Electricity Carbon Emission Calculation",
"Corporate accounting: enter sub-meter electricity and multiply by the factor to obtain Scope 2 emissions.",
"Reduction baseline: compare before and after switching to green power to quantify the carbon cut.",
"Teaching demo: show how the factor differs (high for coal power, low for hydro) and affects the result.",
"Example: 100000 kWh of electricity per year at 0.58 kgCO₂/kWh gives emissions = 100000×0.58 = 58 tCO₂.",
"Which factor should be used?",
"Use the average factor of the local grid (about 0.5–0.6), or deduct accordingly when purchasing green power or certificates. " + BOIL,
"How is green power counted?",
"For self-generated self-consumed power, or purchased green power with its attributes claimed, the corresponding electricity can be excluded or deducted from Scope 2 emissions. " + BOIL,
"What is Scope 2?",
"Under the GHG Protocol, Scope 2 covers indirect emissions from purchased electricity and heat, which is exactly what this tool calculates. " + BOIL,
"How to use Electricity Carbon Emission Calculation",
"Estimates related to energy consumption, carbon emissions and environmental protection.",
"What is Electricity Carbon Emission Calculation for?",
"An electricity carbon emission calculator that estimates CO₂ from electricity use and an emission factor (China's average grid factor about 0.581), supporting carbon footprint accounting.",
"How do I use Electricity Carbon Emission Calculation?",
"Which scenarios suit Electricity Carbon Emission Calculation?",
],
'env-impact-score': [
"♻️ Environmental Impact Score",
"Score energy use, water use, waste and emissions together.",
'📖 View the "Environmental Impact Score Guide"',
"Energy score (0-100)",
"Water score",
"Waste score",
"Emission score",
"Overall = (energy + water + waste + emissions) / 4",
"A higher score means a greater environmental impact; for comparison only.",
"📚 In-Depth Analysis: Environmental Impact Score",
"Option comparison: enter each indicator and its weight to obtain the overall score and choose the low-impact option.",
"Disclosure: score a product or process to support environmental disclosure.",
"Teaching demo: show how normalisation and weighting affect the overall score.",
"Example: energy at weight 0.4 scoring 70, water at 0.3 scoring 60 and emissions at 0.3 scoring 50 give an overall score = 0.4×70+0.3×60+0.3×50 = 62.",
"How should weights be set?",
"Set them by indicator importance or regulatory priority; they should be transparent and verifiable to avoid subjective bias. " + BOIL,
"What if the indicators have different units?",
"Normalise them to a common scale (for example 0–100) before weighting, otherwise the indicator with the largest unit will dominate. " + BOIL,
"Is a lower score better?",
"Usually a lower score means a smaller environmental impact; the scoring direction should be stated clearly and explained in the disclosure. " + BOIL,
"How to use Environmental Impact Score",
"Estimates related to energy consumption, carbon emissions and environmental protection.",
"What is Environmental Impact Score for?",
"Enter energy use, water use, waste and emissions to obtain a composite score quantifying the environmental impact of a product or project (a higher score means greater impact), for comparing options.",
"How do I use Environmental Impact Score?",
"Which scenarios suit Environmental Impact Score?",
],
'fuel-carbon': [
"♻️ Fuel Carbon Emissions",
"Estimate CO₂ from fuel consumption and an emission factor.",
'📖 View the "Fuel Carbon Emissions Guide"',
"Fuel volume (L)",
"Emission factor (kgCO₂/L)",
"Distance travelled (km)",
"CO₂ = fuel volume × emission factor (about 2.31 for petrol)",
"The diesel factor is about 2.68 kgCO₂/L.",
"📚 In-Depth Analysis: Fuel Carbon Emissions",
"Fleet accounting: enter diesel or petrol consumption to obtain annual carbon emissions.",
"Equipment emissions: enter fuel use for construction machinery to estimate emissions over the construction period.",
"Teaching demo: show the difference between the petrol (about 2.3) and diesel (about 2.7) factors.",
"Example: 5000 L of diesel per year at 2.68 kgCO₂/L gives emissions = 5000×2.68 = 13400 kg = 13.4 tCO₂.",
"Why do the factors differ?",
"Because the carbon content differs: about 2.3 for petrol, about 2.7 for diesel and about 2.5 kgCO₂/L for jet fuel. " + BOIL,
"Does it include exhaust after-treatment?",
"The combustion emission factor already covers the oxidation process; after-treatment changes local pollutants but has little effect on CO₂. " + BOIL,
"How does it compare with electricity?",
"For the same energy, direct fuel emissions count as Scope 1 while electricity is Scope 2; the boundaries differ and must not be mixed. " + BOIL,
],
'index': [
"🌱 Eco & Environmental Tools",
"Eco & Environment",
"Eco & Environmental Tools",
"A noise summation calculator that combines the decibel levels of multiple sources by energy (adding or removing sources) to obtain the total noise level, for environmental noise assessment.",
"Waste Reduction Calculation",
gen_desc("Waste generation calculator"),
"Converts between the air quality index (AQI) and PM2.5, PM10, O3 and other pollutant concentrations per HJ 633-2012, making daily air quality bulletins and health advice easier to read.",
"Air Quality Index (AQI) Category Conversion",
"An electricity carbon emission calculator that estimates CO₂ from electricity use and an emission factor (China's average grid factor about 0.581), supporting carbon footprint accounting.",
"Noise Level Summation",
"Enter the sound pressure levels of several sources and use the logarithmic summation formula to obtain the total level (decibels cannot be added directly), for assessing the combined effect of noise sources.",
"A wastewater discharge calculator that obtains the daily volume and total pollutant discharge, supporting corporate environmental compliance and discharge permit accounting (results for reference only).",
"An energy efficiency converter that converts different energy units into standard coal equivalent or kWh for comparison, supporting energy use and conservation assessment.",
"Enter the water use before and after water-saving measures to compute the volume saved and the saving rate, for evaluating the actual effect of fixtures and management.",
"Carbon Footprint Offsetting",
gen_desc("Carbon footprint calculation and offsetting"),
"Enter energy use, water use, waste and emissions to obtain a composite score quantifying the environmental impact of a product or project (a higher score means greater impact), for comparing options.",
"Enter annual carbon emissions to estimate the number of trees and the forest area needed to offset them, giving a rough reference for the scale of carbon-neutral forestation.",
gen_desc("Waste sorting guide"),
"A fuel carbon emission calculator that estimates CO₂ from fuel consumption and an emission factor (about 2.68 kgCO₂/L for diesel), supporting transport and logistics carbon accounting.",
"Enter consumption data to roughly estimate the per-capita ecological footprint (gha) with empirical coefficients and compare it with global per-capita biocapacity, as a reference for sustainable consumption.",
"Enter methane emissions to convert them into CO₂ equivalent using the GWP100 global warming potential, for consistent accounting and comparison in greenhouse gas inventories.",
"Enter the rotor swept area, wind speed and air density to compute the turbine output power with the power formula, with cut-in and cut-out wind speed limits flagged, for wind power assessment.",
"Enter the product type and output to estimate its virtual water consumption (often far higher than direct water use), for product water footprint and supply chain water assessment.",
"Solid Waste Generation Coefficient",
"Based on the industry pollutant generation coefficient manual, enter the product output to estimate solid waste generation, as a reference for industrial solid waste management and compliance accounting.",
"Enter the total waste and the recycled amount to compute the sorting recovery rate and the remaining landfill volume, for assessing waste sorting performance and progress towards reduction targets.",
"Enter the amount of organic waste landfilled to estimate methane production and its CO₂ equivalent, with the emission-reduction potential of landfill gas power generation flagged, for solid waste management assessment.",
"Enter the PV installed capacity, sunshine hours and efficiency to estimate generation over a period, for estimating the returns and environmental benefits of a PV project.",
"Enter the water use before and after adopting water-saving fixtures or habits to estimate the cumulative volume saved, for a clear display of water-saving results in households and public institutions.",
"A battery storage capacity calculator that estimates usable energy from capacity, voltage and depth of discharge, supporting storage system and off-grid power planning.",
"Enter the forestation area, species and unit price to estimate the investment and annual carbon uptake of an afforestation carbon sink project, supporting the cost estimate of a carbon neutrality plan.",
"A rainwater harvesting calculator that estimates the collectable rainwater from roof area and rainfall, supporting rainwater recovery system and water-saving planning.",
"Enter the congested distance and the vehicle fuel consumption to estimate the extra fuel burnt and CO₂ emitted by idling and low-speed driving, for assessing the environmental benefit of congestion management.",
"Enter annual PV generation to estimate the CO₂ reduction in equivalent trees (each absorbing 18 kg CO₂ per year), for demonstrating the environmental benefit of green power.",
"Enter the source sound pressure level and distance to estimate the point-source attenuation (dB) with the free-field model, for noise impact assessment and boundary prediction.",
"An AQI health level tool that gives a health impact level and activity advice from the air quality index, supporting travel and protection decisions on polluted days.",
"Enter building energy use and floor area to compute the energy use index per unit area (kWh/m²/year), for building energy benchmarking and efficiency assessment.",
"Enter the treated water volume and electricity use to estimate the specific energy consumption of a wastewater treatment plant (kWh/m³), for process efficiency comparison and energy retrofit assessment.",
"Enter annual wind generation to convert it into the CO₂ reduction at the equivalent car's annual emissions, for estimating the environmental benefit of a wind project.",
"Enter the wastewater flow and pollutant concentration to estimate the daily COD and other pollutant load in the influent, for process design and compliance assessment.",
"A solid waste generation estimator that estimates total municipal solid waste from population and per-capita generation, supporting municipal sanitation and treatment facility planning.",
"Enter the forest area, species and stand age to estimate the annual carbon sink of a forest or afforestation project, as a reference for carbon sink assets and carbon neutrality estimates.",
"Green Coverage Ratio",
"Enter the green space area and total site area to compute the green coverage ratio (tree canopy projection counted at half), for landscaping and urban planning indicator accounting.",
"Enter electricity, gas and other energy consumption to estimate carbon dioxide emissions with emission factors, for a rough carbon footprint accounting of an organization or individual.",
'About "Eco & Environmental Tools"',
"The Eco & Environmental Tools collection gathers 38 free online tools covering common calculation, conversion and lookup needs in the eco & environmental field. Whether you are a professional, a student or an ordinary user, you will find practical grab-and-go tools here. All tools run fully client-side, upload no data and keep your privacy safe.",
"The eco & environmental tools on this page include (a selection of representative tools):",
"These tools help you complete common eco & environmental tasks quickly, with no need to memorise complex formulas or convert by hand — just enter the values to get results.",
"Do the eco & environmental tools need downloading or registration?",
"No. All the eco & environmental tools on this page are purely client-side online tools that work as soon as you open the page; no software to install, no account to register and no data uploaded.",
"Are the results of the eco & environmental tools accurate? Is my data safe?",
"The tools compute locally in your browser using public mathematical formulas and common industry standards, with results available instantly. All computation happens on your own device, no data is uploaded to a server, and your privacy is protected.",
],
}

def build(slug, en_list):
    path = os.path.join(WORK, slug + '.json')
    wj = json.load(open(path, encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('!! %s length mismatch %d vs %d' % (slug, len(en_list), len(items)))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        # 坑 28：关联卡片（related-tool）名在 EN 态被 cleanRelatedName() 截断成短形态，
        # 运行时查表键是短形态而非 zh_src 的长形态 ⇒ 此类条目以 zh 为键。
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if not en or not isinstance(en, str):
            print('!! %s empty translation' % slug)
            sys.exit(1)
        if CJK.search(en) or CNP.search(en):
            print('!! %s CJK/CNP violation: %s' % (slug, en[:60]))
            sys.exit(1)
        mp[z] = en
    return mp

def write(slug, mp):
    os.makedirs(OUT, exist_ok=True)
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('name', slug)
    out = {'slug': slug, 'industry': 'eco', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

for slug, en_list in EN.items():
    write(slug, build(slug, en_list))
