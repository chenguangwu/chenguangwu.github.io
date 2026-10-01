#!/usr/bin/env python3
# energy batch3 (5 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'energy')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'energy')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'wind-power-estimator': [
"⛅ Wind Power Generation Estimation",
"Estimate the theoretical power and actual output power of a wind turbine from wind speed and blade parameters",
'📖 View the "Wind Power Generation Estimation User Guide"',
"Enter the wind speed to start estimating",
"Blade radius (m)",
"Wind energy utilization coefficient Cp",
"📊 Wind Energy Utilization Coefficient Cp Reference Table",
"Betz limit (theoretical maximum) = 0.593; the Cp of real wind turbines is usually between 0.2 and 0.5",
"Wind speed-power relationship:",
"Power is proportional to the wind speed's",
"cube",
"(P ∝ v³); doubling the wind speed increases the power to 8 times.",
"For example: wind speed from 6 m/s to 12 m/s, with the same parameters the power increases by 2³ =",
"8 times",
"Therefore, wind speed is the most critical factor determining the economics of wind power when siting.",
"📚 In-Depth Analysis: Wind Power Generation Estimation",
"Evaluate turbine + battery complementary supply for off-grid sites.",
"Compare the annual utilization hours of wind turbines and PV.",
"Quickly estimate annual generation by capacity factor.",
"Small turbine annual generation estimation",
"Rated 10 kW, local capacity factor 0.28, 8760 h/year: annual generation ≈10×8760×0.28≈24528 kWh. Tip: when the capacity factor is far lower than PV utilization hours, assess the wind resource stability and its match with winter heating electricity demand.",
"Is the capacity factor the same as the utilization rate?",
"Close. Capacity factor = actual annual generation / (rated × 8760), reflecting the combination of resource and downtime; wind power fluctuates greatly, so the capacity factor varies notably by region.",
"How do wind turbines and PV complement each other?",
"Wind is strong in winter and spring while sunlight is good in summer and autumn, so the two complement each other to smooth output; adding storage and diesel backup to an off-grid system improves reliability.",
'About the "Wind Power Generation Estimation"',
"Wind Power Generation Estimation is an online tool in the energy and power domain. Based on standard physical and engineering formulas, it calculates accurately with reliable results.",
"Based on standard physical and engineering formulas",
"Electricity and energy data analysis",
"Electric power and energy conversion",
"Energy solution assessment assistance",
"Learning energy and electricity knowledge",
],
'standby-power-calculator': [
"⚡ Standby Power Consumption Calculator",
"Check the home appliances and set their quantities to compute the total standby power and the electricity cost saved by turning standby off",
'📖 View the "Standby Power Consumption Calculator User Guide"',
"Standby power consumption = Σ(P_i × t_i)",
"Daily standby duration (h)",
"Check the appliances on standby",
"Electricity cost wasted on standby per year",
"Electricity cost saved by turning standby off",
"📊 Common Appliance Standby Power Reference",
"The following are typical standby power data for common home appliances; actual values vary by brand and model",
"Standby power",
"Daily standby consumption (20h)",
"Annual standby consumption",
'💡 Set-top boxes are a "standby power guzzler"; a single unit\'s annual standby electricity cost can reach dozens of CNY. It is advisable to fully power off appliances not used for a long time (unplug or use a switched power strip).',
"📚 In-Depth Analysis: Standby Power Consumption Calculator",
"Take stock of household standby appliances to find the guzzlers.",
"Estimate the annual savings from powering off with a smart power strip.",
"Compare the standby share of different appliances.",
"Household annual standby cost",
"Set-top box 15 W, router 6 W, TV 3 W, etc., totaling about 30 W on standby for 20 h/day: daily consumption 0.6 kWh, annual 219 kWh, electricity cost about 127 CNY. Powering everything off saves about 127 CNY per year and extends device life. Tip: the set-top box has a high standby share, so address it first.",
"Does standby really consume power?",
"Yes. Most appliances still have power circuit consumption on standby, which accumulates considerably over the years, especially set-top boxes, audio equipment and adapters.",
"What is the easiest way to eliminate standby?",
"Use a switched power strip or smart socket to cut power with one touch instead of unplugging one by one; timed ones can be set to power off automatically.",
'About the "Standby Power Consumption Calculator"',
"Standby Power Consumption Calculator is an online tool in the energy and power domain. Based on standard physical and engineering formulas, it calculates accurately with reliable results.",
"Based on standard physical and engineering formulas",
"Electricity and energy data analysis",
"Electric power and energy conversion",
"Energy solution assessment assistance",
"Learning energy and electricity knowledge",
],
'carbon-footprint': [
"♻️ Carbon Footprint Calculation",
"Estimate the annual carbon emissions of an individual/family (kgCO₂e)",
"/ Carbon Footprint",
'📖 View the "Carbon Footprint Calculation User Guide"',
"Carbon footprint = Σ(activity × emission factor)",
"🚗 Transportation",
"Gasoline car (km/year)",
"Electric car (km/year)",
"Airplane (km/year)",
"Bus/metro (km/year)",
"🏠 Home Energy",
"Electricity (kWh/year)",
"Natural gas (m³/year)",
"Water (m³/year)",
"🍔 Diet and Consumption",
"Meat (kg/year)",
"Dairy (kg/year)",
"👆 Click to calculate",
"📚 In-Depth Analysis: Carbon Footprint Calculation",
"Estimate the household annual electricity carbon emissions.",
"Carbon footprint statistics for commuting/business travel.",
"Compare emissions of different energy mixes.",
"Household electricity carbon emissions",
"Annual electricity 5475 kWh, grid factor 0.58 kgCO₂/kWh: annual emissions ≈3176 kgCO₂. With a green electricity factor of 0.02, only 110 kg. Tip: the factor varies greatly with the regional power mix, so use the locally published value.",
"Where do the emission factors come from?",
"Officially/institutionally published coefficients for electricity, heat, fuel and travel; the regional grid factor is updated annually, and using the wrong one causes significant deviation.",
"Can the carbon footprint be offset?",
"It can be offset through green electricity procurement, forestry carbon sinks or carbon credits, but emission reduction takes priority; offsets must be verified to prevent double counting.",
'About the "Carbon Footprint Calculation"',
"Carbon Footprint Calculation is an online tool in the energy and power domain. An energy and power tool that helps compute energy consumption and power parameters.",
],
'calculator-calc-4': [
"🔊 Noise Decibel Addition",
"Enter multiple sound source decibel values (one per line or separated by commas/spaces) to compute the total added decibels",
'📖 View the "Noise Decibel Addition User Guide"',
"Decibel addition L = 10·log₁₀(Σ10^(L_i/10))",
"Decibel value of each sound source (dB)",
"💡 Formula: decibels are logarithmic quantities and cannot be added directly. Total sound pressure level L = 10×log₁₀(Σ10^(Lᵢ/10)). Adding two equal decibels increases the level by only 3 dB.",
"Decibels (dB) are a logarithmic scale; to add them, first convert to sound energy and then sum",
"Adding two identical decibel sources gives +3 dB, and ten identical sources give +10 dB",
"Real noise evaluation also needs to consider frequency characteristics and time distribution",
"📚 In-Depth Analysis: Noise Decibel Addition",
"Given power and time, compute energy.",
"Given energy and time, compute average power.",
"Given energy and power, compute duration.",
"General energy conversion",
"Air conditioner 1.5 kW running 4 h: E=6 kWh; if the monthly energy is 180 kWh and you want the average daily running hours: t=180/(30×1.5)=4 h. Tip: note the actual part-load and standby addition.",
"How is this tool different from the power consumption calculator?",
"This tool focuses on general conversion among the three quantities E/P/t, while the power consumption calculator is oriented toward itemized list statistics.",
"The result doesn't match the meter?",
"Because the load is not constant and includes standby/other circuits, the general conversion gives a theoretical value; the meter measurement prevails.",
'About the "Noise Decibel Addition"',
"Noise decibel addition tool: enter multiple sound source decibel values to compute the total sound pressure level by the sound energy addition principle and analyze each source's contribution, suitable for environmental noise assessment and noise reduction design.",
"Accurate logarithmic energy addition",
"Analysis of each source's energy contribution share",
"Noise level evaluation",
"Supports batch sound source input",
"Environmental noise assessment",
"Industrial noise reduction design",
"Building acoustics analysis",
"Multi-source addition calculation",
"e.g.:\n60,65,70",
],
'lcoe': [
"Lifecycle Cost / Generation",
"LCOE = (CAPEX·CRF + O&M) / annual generation.",
"Levelized Cost of Energy (LCOE)",
"/ Levelized Cost of Energy (LCOE)",
'📖 View the "Lifecycle Cost / Generation User Guide"',
"LCOE = lifecycle cost / total generation",
"Term (years)",
"Discount rate r",
"Annual O&M (CNY)",
"Annual generation (kWh)",
"The lower the LCOE, the stronger the competitiveness.",
"📚 In-Depth Analysis: Lifecycle Cost / Generation",
"Compare the cost per kWh of PV/wind/gas turbines.",
"Sensitivity analysis of LCOE to changes in the discount rate.",
"Assess competitiveness after subsidy reduction.",
"5 MW PV LCOE",
"CAPEX 5 million CNY, 20 years, discount rate 6%, annual O&M 100,000 CNY, annual generation 1.2 million kWh: CRF=0.06·1.06²⁰/(1.06²⁰−1)≈0.0872; LCOE=(500×0.0872+10)/120≈(43.6+10)/120≈0.447 CNY/kWh. Tip: when the discount rate rises by 2%, the LCOE increases notably.",
"Is a lower LCOE always better?",
"Under equivalent reliability and grid-connection conditions, the lower the LCOE the stronger the competitiveness; but it must be viewed together with curtailment, volatility and ancillary costs.",
"Why does the discount rate have a large impact?",
"A high discount rate gives distant generation a lower present-value weight, increases the CAPEX recovery pressure and raises the LCOE; policy interest rates and risk premiums transmit directly.",
"How to use Lifecycle Cost / Generation",
"Initial investment, O&M and annual generation accounting for household PV and wind projects, comparing the cost per kWh and payback period of units of different capacities.",
"What does Lifecycle Cost / Generation do?",
"Compute the levelized cost of energy (LCOE) from CAPEX, discount rate, O&M and annual generation to compare the economics of power projects; a purely front-end estimate to assist investment judgment.",
"How do I use Lifecycle Cost / Generation?",
"What scenarios is Lifecycle Cost / Generation suitable for?",
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
        if it.get('src_diff') and it.get('zh_src'):
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
    out = {'slug': slug, 'industry': 'energy', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

for slug, en_list in EN.items():
    write(slug, build(slug, en_list))
