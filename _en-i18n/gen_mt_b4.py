#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'metallurgy')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'metallurgy')
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
    out = {'slug': slug, 'industry': 'metallurgy', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('decarburization', build('decarburization', [
        "\U0001F52E Decarburised Layer Estimation",
        "Estimate the depth of the decarburised layer on the surface of a steel part from the heating temperature and holding time, based on a carbon diffusion model.",
        "Core formula (over the input variables): 2\u00d7\u221a(effD\u00d7t\u00d73600)\u00d7erfInv(ratio); D0\u00d7Math.exp(-Q\u00f7(R\u00d7Tk)); 2.0e-5",
        "Heating Temperature T (\u00b0C)",
        "Holding Time t (h)",
        "Original Carbon Content C0 (%)",
        "Furnace Atmosphere",
        "Air (oxidising)",
        "Weakly decarburising atmosphere",
        "Neutral / protective atmosphere",
        "Decarburisation Threshold Cs/C0",
        "Estimate Decarburised Layer",
        "\U0001F4CB Model Description",
        "Diffusion model:",
        "the surface carbon concentration follows the semi-infinite body diffusion equation, with carbon concentration C(x,t)/C0 = erf(x/(2\u221a(D\u00b7t))).",
        "Decarburised layer depth:",
        "x = 2\u00b7\u221a(D\u00b7t)\u00b7erf\u207b\u00b9(Cs/C0), where D is the diffusion coefficient of carbon in austenite.",
        "Diffusion coefficient (Arrhenius):",
        "Atmosphere correction:",
        "Air uses full decarburisation (surface C\u22480), a weak decarburising atmosphere is reduced to 0.6 and a protective atmosphere to 0.1.",
        "Note: this is an engineering estimate; actual decarburisation is affected by many factors such as alloying elements, grain size and oxygen partial pressure.",
        "\U0001F4DA In-Depth Analysis: Decarburised Layer Estimation",
        "Estimate the depth of the decarburised layer on the steel surface from heating temperature, holding time and atmosphere, to judge whether the machining allowance is sufficient.",
        "Use the diffusion equation to give the C(x,t)/C0 distribution quantitatively along the depth, locating the depth at which carbon content falls to a threshold.",
        "Compare the correction factors for air, weakly oxidising and protective atmospheres to optimise the heating schedule.",
        "Diffusion Model",
        "Surface carbon concentration distribution C(x,t)/C0 = erf( x / (2\u221a(D\u00b7t)) ), depth x = 2\u221a(D\u00b7t)\u00b7erf\u207b\u00b9(Cs/C0). Diffusion coefficient D = D0\u00b7exp(\u2212Q/(R\u00b7T)), D0=2.0\u00d710\u207b\u2075 m\u00b2/s, Q=142 kJ/mol, R=8.314. Atmosphere correction factors: air 1.0, weakly oxidising 0.6, neutral or protective 0.1.",
        "At 1000\u00b0C (T=1273 K) held for 2 hours in air: D=2e-5\u00d7exp(\u2212142000/(8.314\u00d71273))\u22483.0\u00d710\u207b\u00b9\u00b9 m\u00b2/s; with Cs/C0=0.5, x=2\u00d7\u221a(3.0e-11\u00d77200)\u00d70.477\u22482\u00d7\u221a(2.16e-7)\u00d70.477\u22482\u00d74.65e-4\u00d70.477\u22484.4\u00d710\u207b\u2074 m\u22480.44 mm. Switching to a protective atmosphere (\u00d70.1) reduces the depth to about 0.04 mm.",
        "How much allowance for the decarburised layer?",
        "Set it from the final hardness or case depth requirement. If decarburisation is 0.4 mm, rough machining should leave more than that and remove it in finish machining, otherwise the soft surface layer affects wear resistance and fatigue.",
        "Why does temperature matter so much?",
        "D grows exponentially with temperature, so raising the temperature by about 50 to 100\u00b0C can double the diffusion coefficient. Controlling heating temperature and dwell time is therefore the core of suppressing decarburisation.",
        "About \"Decarburised Layer Estimation\"",
        "Decarburised Layer Estimation is an online tool in the business and office domain. A business and office tool that improves work efficiency with local data processing that protects privacy.",
    ]))
    write('index', build('index', [
        "\U0001F529 Metallurgy and Materials Tools",
        "Metallurgy and Materials",
        "Metallurgy and Materials Tools",
        "Steel Section Weight Calculator",
        "The Steel Section Weight Calculator is a free online metallurgy and materials tool; steel purchasing and transport are charged by weight. Choose a section type, enter dimensions and length, and the theoretical weight formula (density 7.85 g/cm\u00b3) converts weight automatically. It runs purely in the browser, uploads no data and needs no registration, opening the",
        "Based on the Chvorinov rule t = C \u00d7 (V/A)\u00b2, entering the cross-section shape and dimensions automatically computes the modulus M and solidification time t, supporting ranking of solidification order across multiple sections.",
        "Cast solidification time calculation (modulus method / Chvorinov rule), estimating the time to full solidification from the casting modulus and solidification coefficient.",
        "Compute the amount of each ferroalloy raw material from the target element content (Cr/Ni/Mo and so on), with recovery correction.",
        "Enter the target composition, charge composition and ratio to compute the weighted average charge composition, compare it with the target after allowing for element burn loss, and support cast iron and cast steel melting charge.",
        "Enter the target alloy mass, target element contents and raw material composition, and compute the charge quantity of each raw material by mass conservation, for charge calculation before alloy melting.",
        "Brinell (HB), Rockwell (HRC/HRB) and Vickers (HV) hardness conversion using approximate values per ASTM E140 / GB/T 33362.",
        "Forging temperature, deformation and force-energy calculation tools estimate the forging temperature window, deformation amount and required equipment force-energy from input parameters, suited to forging process design and equipment selection.",
        "Steel Structure Weld Calculation",
        "The Steel Structure Weld Calculation tool is a free online metallurgy and materials tool; input parameters and you get results in real time. It runs purely in the browser, uploads no data, needs no registration and works as soon as you open it. Suited to engineering estimates, daily conversion and quick verification, with results copyable in one click.",
        "Enter workpiece dimensions and heating parameters to estimate heating time, holding time and total process time, and generate a heat treatment time-temperature curve to support process planning.",
        "The Brinell, Rockwell and Vickers hardness conversion table gives approximate conversion and reference lookup between the three hardness scales, suited to unifying hardness in material testing, quality inspection and heat treatment reports.",
        "Tailings (Grade / Loss / Utilisation) Analysis",
        "The Tailings (Grade / Loss / Utilisation) Analysis tool is a free online metallurgy and materials tool. Tailings (Grade / Loss / Utilisation) Analysis. A free online tool processed entirely in the browser with no data upload, protecting your privacy. It runs purely in the browser, uploads no data, needs no registration and works as soon as you open it.",
        "Based on a carbon diffusion model, enter the heating temperature and holding time of a steel part to estimate the surface decarburised layer depth, providing a reference for heat treatment process design and surface quality control.",
        "Enter raw material input and product output to compute yield rate and product rate, compare against process baselines to assess loss, and support smelting and production accounting with purely front-end statistics.",
        "Price (Quote / Volatility / Hedging) Analysis",
        "The Price (Quote / Volatility / Hedging) Analysis tool is a free online metallurgy and materials tool: enter a price series to compute the mean, amplitude, volatility and hedging benchmark band. It runs purely in the browser, uploads no data, needs no registration and works as soon as you open it.",
        "Metallurgical thermodynamics, equilibrium and phase diagram analysis tools evaluate alloy phase transformations and equilibrium states on the basis of engineering models, suited to materials R&D, heat treatment process work and phase diagram application analysis.",
        "Metallurgical quality, spectrometry and chemical analysis tools evaluate smelting composition and quality inspection metrics on the basis of standard engineering formulae, suited to process analysis and quality control in ferrous and non-ferrous metallurgy.",
        "Metallurgical energy consumption tools estimate energy use and energy-saving potential per tonne of steel or aluminium, suited to energy accounting, carbon assessment and process optimisation in metallurgical plants.",
        "Electric furnace smelting calculation tools estimate steelmaking power consumption and smelting rhythm from parameters such as arc power and electrodes, suited to electric arc furnace process optimisation and energy management.",
        "About \"Metallurgy and Materials Tools\"",
        "This Metallurgy and Materials Tools collection gathers 19 free online tools covering the common calculation, conversion and lookup needs of metallurgy and materials scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you will find ready-to-use practical utilities here. All tools run entirely in the browser, never upload data to a server, and protect your privacy.",
        "The metallurgy and materials tools included on this page include (a few representative ones):",
        "These tools help you finish common metallurgy and materials tasks quickly without memorizing complex formulas or converting by hand; enter the values and get the answer.",
        "Do the metallurgy and materials tools require a download or registration?",
        "No. All tools on this page are pure front-end online tools: open the page and use them directly. No software to install, no account to register, and no data is uploaded.",
        "Are the calculation results accurate, and is my data safe?",
        "Tools compute locally in your browser based on public mathematical formulas and general industry standards, so results are immediate. All computation happens on your own device, data is never uploaded to a server, and your privacy is protected.",
    ]))


if __name__ == '__main__':
    main()