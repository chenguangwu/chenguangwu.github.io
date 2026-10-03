#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'gas')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'gas')
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
    out = {'slug': slug, 'industry': 'gas', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('calc-68', build('calc-68', [
        "Liquefied Gas Vaporisation Heat Calculation",
        "Select the liquefied gas type, enter the mass and vaporisation time, and compute the vaporisation heat and power",
        "Core formula (by input variable): Q/(t x 60)",
        "Liquefied gas type",
        "Liquefied petroleum gas LPG",
        "Liquefied natural gas LNG",
        "Liquid ammonia",
        "Liquid chlorine",
        "Mass (kg)",
        "Vaporisation time (min)",
        "Vaporisation heat: LPG about 400, LNG about 510, liquid ammonia about 1370, liquid chlorine about 280 kJ/kg; vaporiser selection needs a 1.2~1.5 times margin.",
        "The vaporisation heat coefficients are reference values at atmospheric boiling point and actually vary with temperature and pressure",
        "Vaporiser selection should consider the ambient temperature and the peak gas demand",
        "In-Depth Analysis: Liquefied Gas Vaporiser Selection (vaporisation heat / power / volume)",
        "LPG cylinder manifold station / vaporising station equipment selection, with the vaporisation capacity and storage tank determined by the peak gas demand",
        "LNG vaporising station heater power checking and operating energy consumption estimation",
        "Vapour volume assessment for emergency response to leaks of hazardous chemicals such as liquid ammonia and liquid chlorine",
        "Enter the liquefied gas type, mass m and planned vaporisation time t: total vaporisation heat Q=m·L (L is the latent heat of vaporisation kJ/kg), average heating power P=Q/(t·60), volume at standard state after vaporisation V=m·vol (vol is the specific volume at standard state m3/kg). Real vaporisers are selected with a 1.2~1.5 times power margin.",
        "LPG: m=100 kg, t=60 min, latent heat L=400 kJ/kg, specific volume vol=0.54 m3/kg -> Q=100x400=40000 kJ, P=40000/(60x60)=11.1 kW, V=100x0.54=54.0 m3. Select the vaporiser heating power at 11.1x1.3=about 14.4 kW.",
        "Why is a margin needed on the power?",
        "At low ambient temperatures and during continuous peak demand the actual vaporisation capacity drops, so selecting the heating power with a 1.2~1.5 times margin avoids insufficient gas supply.",
        "How is the liquid ammonia/liquid chlorine volume used?",
        "Convert via the specific volume at standard state into the volume of combustible gas or toxic gas after a leak, for ventilation and emergency dispersion assessment; but these are hazardous media and must be handled by professionals according to the code.",
        "About Liquefied Gas Vaporisation Heat Calculation",
        "Liquefied gas vaporisation heat calculation tool; select the liquefied gas type (LPG/LNG/liquid ammonia/liquid chlorine), enter the mass and vaporisation time, and compute the vaporisation heat coefficient, total vaporisation heat, average heating power and volume after vaporisation, assisting vaporiser selection and energy accounting.",
        "Four liquefied gas types",
        "Vaporisation heat and power calculation",
        "Volume after vaporisation estimation",
        "Vaporiser selection reference",
        "Vaporising station design and selection",
        "LNG/LPG vaporisation energy accounting",
        "Ambient temperature / electric heating vaporiser configuration",
        "Gas peak shaving vaporisation calculation",
        "Vaporisation time",
    ]))

    write('concentration-7', build('concentration-7', [
        "Fuel Gas Odorant Concentration Calculation",
        "Enter the gas flow and target concentration to compute the thiophene dosing amount and consumption",
        "Core formula (by input variable): doseMgh/(purity/100)/density/1000; doseDayx365/1000; doseMlhx24",
        "Gas flow (m3/h)",
        "Target concentration (mg/m3)",
        "Odorant purity (%)",
        "Odorant",
        "Thiophene THT",
        "Tert-butyl mercaptan TBM",
        "Sulphur-free odorant",
        "THT recommended concentration 15~25 mg/m3; dosing amount = flow x concentration; dosing pump range selected at 2 times the operating condition.",
        "The dosing concentration shall meet the requirements of codes such as CJJ 51",
        "Odorant stock should meet at least 30 days of consumption",
        "In-Depth Analysis: Fuel Gas Odorant Dosing Rate and Consumption",
        "Urban gas networks are dosed according to the code so that a leak can be detected by smell",
        "THT/thiophene dosing pump range and operating consumption accounting",
        "Odorant concentration check (whether it falls in the recommended band)",
        "Hourly dosing amount (mass) doseMgh = flow x target concentration; volume dosing doseMlh = doseMgh/(purity/100)/density/1000; daily/annual consumption derived from 24h/365d; dosing pump range takes 2 times the operating flow. THT recommended concentration 15~25 mg/m3.",
        "Natural gas flow 1000 m3/h, target 20 mg/m3, THT purity 100%, density 0.999 g/mL -> hourly dosing 20000 mg/h = 20.02 mL/h, daily consumption 480.5 mL, annual consumption about 175.4 L; 20 mg/m3 falls in the 15~25 recommended band (concentration suitable), choose a solenoid diaphragm metering pump with a range of about 41 mL/h.",
        "What concentration of odorant is appropriate?",
        "THT is usually 15~25 mg/m3 (not below 8 mg/m3 at the terminal for detection), specifically per GB 50028 and local codes; too low makes leaks hard to detect, too high wastes product and smells pungent.",
        "Why is the pump range taken at 2 times?",
        "To leave adjustment margin for flow fluctuation and ageing, avoiding long-term operation at full range which causes inaccurate metering or overpressure.",
        "About Fuel Gas Odorant Concentration Calculation",
        "Fuel gas odorant concentration calculation tool; select the odorant type (THT/TBM/sulphur-free odorant), enter the gas flow, target concentration and purity, and compute the hourly/daily/annual dosing amount and recommend a dosing pump selection, assisting odorant system design.",
        "Three odorant types",
        "Dosing amount and consumption calculation",
        "Concentration suitability assessment",
        "Dosing pump selection recommendation",
        "Gas odorant system design",
        "Odorant consumption accounting",
        "Dosing pump selection configuration",
        "Odorant concentration monitoring and management",
        "Gas flow",
        "Odorant purity",
    ]))

    write('concentration-8', build('concentration-8', [
        "Fuel Gas Leak Explosion Risk Judgement",
        "Enter the gas type and leak concentration to judge the explosion risk level",
        "View the Fuel Gas Leak Explosion Limit Risk Judgement User Guide",
        "Explosion risk is judged by comparing the concentration with the explosion limits: below the lower explosive limit LEL is safe, between LEL and the upper explosive limit UEL is the explosive hazard zone, and above UEL is too rich to burn (ventilation is still required); common explosion limits are natural gas 5% to 15%, liquefied petroleum gas 2% to 10%, manufactured gas 12.5% to 74%, and hydrogen 4% to 75%; once the concentration reaches 25% of LEL the alarm should sound, the gas source cut off and windows opened for ventilation; switching electrical appliances and using open flames is strictly forbidden.",
        "Gas type",
        "Natural gas (methane)",
        "Liquefied petroleum gas",
        "Manufactured gas",
        "Hydrogen",
        "Leak concentration (%)",
        "Combustible gas detector alarm settings: 20% LEL for warning, 60% LEL for high alarm with interlocked shut-off.",
        "The explosion limits vary with temperature, pressure and gas composition",
        "On site a calibrated combustible gas detector should be used for actual measurement",
        "In-Depth Analysis: Fuel Gas Leak Explosion Limit Risk Judgement",
        "Leak emergency handling: on-site detector readings quickly grade the level",
        "Before ventilating a confined space or pipeline,",
        "the initial grading for gas company inspection and resident reporting",
        "Enter the gas type and volume concentration c and look up the explosion limits LEL/UEL: the proportion of LEL pct=c/LELx100%. c within [LEL,UEL] is the explosive hazard; pct>=25 is high hazard, >=10 is hazard, >0 is alert; reaching 20% of LEL should raise the alarm and 60% should cut the power.",
        "Natural gas (LEL 5%, UEL 15%) at a concentration of 1.0% -> 20.0% of LEL, rated as the hazard level (strengthen ventilation, find the leak source, no open flames); if it rises to 5% it enters the explosive range and immediate evacuation and alarm are required.",
        "Why alarm at 20% of LEL?",
        "20% of LEL is the early warning threshold; although the lower explosive limit is not reached yet, it indicates a continuing leak, so a timely investigation is needed to avoid accumulation into the explosive range.",
        "Do the limits differ greatly between gas types?",
        "They differ greatly: natural gas 5~15%, LPG 2~10%, hydrogen 4~75%, manufactured gas 12.5~74%. The correct gas type must be selected when grading; a wrong choice seriously underestimates the risk.",
        "About Fuel Gas Leak Explosion Risk Judgement",
        "Fuel gas leak explosion risk judgement tool; select the gas type (natural gas/LPG/manufactured gas/hydrogen), enter the leak concentration, compute the proportion of the lower explosive limit and the risk level, and give handling suggestions, assisting leak safety assessment.",
        "Explosion limits of four fuel gases",
        "LEL proportion calculation",
        "Five-level risk rating",
        "Graded handling suggestions",
        "Fuel gas leak safety assessment",
        "Combustible gas detection data analysis",
        "Hazardous area risk determination",
        "Emergency response decision reference",
        "Leak concentration",
    ]))


if __name__ == '__main__':
    main()
