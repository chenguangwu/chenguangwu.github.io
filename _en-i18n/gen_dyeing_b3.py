#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'dyeing')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'dyeing')
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
    out = {'slug': slug, 'industry': 'dyeing', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('shumayinhuacanshu', build('shumayinhuacanshu', [
        "🎨 Digital Printing Parameters",
        "Enter the resolution, print area and ink type to compute ink usage and printing precision",
        "Core formula (by input variables): (dpi÷2.54)^2; id.g×(cover÷100); totalG÷1.1",
        "📖 Read the \"Digital Printing Parameters Usage Guide\"",
        "Print area (m²)",
        "Ink type",
        "Reactive ink",
        "Disperse ink",
        "Pigment ink",
        "Acid ink",
        "Coverage (%)",
        "💡 Droplet spacing = 25.4/dpi (mm); ink usage = area × coverage × unit ink laydown",
        "Common resolutions: 360/720/1440 dpi; the higher the dpi the finer the detail but the slower the speed",
        "Unit laydown is an empirical average and actually varies with the pattern and settings",
        "📚 In-Depth Analysis: Digital Printing Parameters",
        "Digital printing cost estimation: estimate the ink cost per piece from area, coverage and ink unit price.",
        "Trade-off between printing precision and speed: high dpi is more precise but slower, so pick a level according to how fine the pattern is.",
        "Ink procurement planning: accumulate ink consumption by order volume and arrange stock of reactive/disperse/pigment/acid inks.",
        "Example ink consumption for reactive ink digital printing",
        "For a print area of 1.0 m², average coverage 8%, 720 dpi and reactive ink density about 1.05 g/mL, the estimated ink volume converts to a few tens of grams; multiply by the unit price for the per-piece ink cost, then by the order quantity for stock planning.",
        "Is higher dpi always better?",
        "High dpi gives sharper detail but slows jetting and raises ink consumption; 360~720 dpi is enough for ordinary patterns, and higher dpi is only needed for image-level fine detail.",
        "What is the difference between ink types?",
        "Reactive (cotton and linen), disperse (polyester), acid (silk, wool, nylon) and pigment (universal for mixed fibres) suit different fibres and use different fixation processes, so ink consumption and unit price differ.",
        "How is coverage estimated?",
        "From the pixel share of the pattern or by visual estimate; solid fills approach 100% while sparse line work may be below 5%, which affects the accuracy of ink consumption estimates.",
        "About \"Digital Printing Parameters\"",
        "Digital printing forms images by ejecting ink droplets; resolution determines precision and ink type determines the unit laydown. This tool estimates ink usage and droplet density from dpi, print area, coverage and ink type, and assesses the printing precision grade.",
        "Ink usage (g/mL) and droplet spacing calculation",
        "Supports reactive/disperse/pigment/acid inks",
        "Resolution precision grading",
        "Digital printing cost estimation",
        "Trade-off between printing precision and speed",
        "Ink procurement planning",
        "Digital printing process teaching",
        "Print area",
        "Coverage",
    ]))

    write('temp-time-humidity-1', build('temp-time-humidity-1', [
        "📋 Steaming Condition Assessment",
        "Enter temperature, humidity and time to assess the effect of saturated steam steaming",
        "Entering temperature, humidity and time to assess the effect of saturated steam steaming is computed professionally from the input parameters and the results are output.",
        "📖 Read the \"Steaming Condition Assessment Usage Guide\"",
        "Steaming temperature (℃)",
        "Steam humidity (%)",
        "Steaming time (min)",
        "Reactive dye steaming",
        "Vat dye steaming",
        "Pigment printing steaming",
        "💡 Saturated steam steaming: temperature 100～105℃, humidity ≥95%; time varies by dye",
        "Excessively high saturated steam temperature causes superheating, and lowering humidity affects fixation",
        "Insufficient steaming time gives incomplete fixation, while too long easily causes blotching or dye hydrolysis",
        "📚 In-Depth Analysis: Steaming Condition Assessment",
        "Printing steaming fixation step: compare temperature, humidity and time reference ranges by reactive/vat/pigment process to judge compliance.",
        "Vat dye leuco compound steaming: confirm that saturated steam and holding time fully oxidise and fix the leuco compound.",
        "Steaming process parameter checking: quickly check steaming conditions when using a new formula or changing product to avoid insufficient fixation.",
        "Example condition check for reactive printing steaming",
        "Reference conditions for reactive printing: temperature 102~104℃,",
        ">90%, time 6~10 min; measured 100℃, humidity 85%, 8 min — temperature and humidity are slightly low, suggesting the steam carries gas or humidification is insufficient, so fixation may be too pale and needs adjustment.",
        "Which scenarios suit the steaming condition assessment?",
        "It is used for parameter review, condition checking and teaching demonstrations of the steaming fixation step in vat/reactive/pigment printing.",
        "How do temperature, humidity and time work together?",
        "Saturated steam supplies both heat and moisture so the dye diffuses and fixes; insufficient temperature or low humidity lowers the fixation rate, so all three must fall inside the process window at once.",
        "Can the result be used directly as a process instruction?",
        "It is for parameter review and teaching reference; actual steaming conditions depend on equipment capability, fabric and dye system and the customer's sealed sample, and do not replace a formal process sheet.",
        "About \"Steaming Condition Assessment\"",
        "Steaming is the key step for fixing colour in printing and dyeing, and temperature, humidity and time together determine the fixation effect. This tool assesses whether steaming conditions meet the standard by process type, helping control steaming quality.",
        "Gives reference ranges by reactive/vat/pigment process",
        "Graded assessment of temperature, humidity and time",
        "Overall compliance judgement",
        "Printing steaming fixation step",
        "Vat dye leuco compound steaming",
        "Steaming process parameter checking",
        "Steaming temperature",
        "Steam humidity",
        "Steaming time",
    ]))

    write('tester-9', build('tester-9', [
        "💊 AATCC 100 Antibacterial Test",
        "Computes the bacterial reduction rate and antibacterial activity value (log reduction) under the AATCC 100 quantitative antibacterial test method, for reading textile antibacterial performance. Enter the viable counts for the \"0 hour control\" and the \"24 hour sample\".",
        "Antibacterial (AATCC) Test",
        "/ Antibacterial (AATCC) Test",
        "📖 Read the \"AATCC 100 Antibacterial Test Usage Guide\"",
        "Bacterial reduction rate = (A − B) / A × 100%",
        "Test organism",
        "Staphylococcus aureus (Gram positive)",
        "Escherichia coli (Gram negative)",
        "Klebsiella pneumoniae",
        "Candida albicans (fungus)",
        "24 hours",
        "6 hours",
        "A: viable count of the 0h control (CFU/mL)",
        "B: viable count on the sample after contact (CFU/mL)",
        "C: viable count of the control after contact (CFU/mL, optional)",
        "Compute the bacterial reduction rate",
        "Bacterial reduction rate = (A − B) / A × 100%; antibacterial activity value R = log₁₀(A) − log₁₀(B)",
        "AATCC 100 requires a 0h inoculum of about 1×10⁵~3×10⁵ CFU/mL; a reduction rate ≥99% (R≥2) is normally regarded as antibacterial pass",
        "If B>A the sample has no antibacterial action or the bacteria have grown, so the reduction rate is negative",
        "📚 In-Depth Analysis: AATCC 100 Antibacterial Test",
        "Efficacy evaluation of antibacterial textiles: compare the viable count reduction between treated and blank samples to quantify antibacterial effect.",
        "Antibacterial agent screening and process optimisation: compare reduction rates across different finishes or concentrations to pick the best.",
        "Quality report data checking: quickly compute the reduction rate / log value from measured colony counts, assisting report preparation and claim compliance judgement.",
        "Example antibacterial calculation for silver-ion finished fabric",
        "The blank sample has viable counts of 2.0×10⁵ at 0h and 1.8×10⁵ CFU/mL at 18h, and the treated sample is 3.0×10² CFU/mL at 18h; reduction rate=(1-3.0×10²/1.8×10⁵)×100%≈99.8%, log reduction=log10(1.8×10⁵/3.0×10²)≈2.8.",
        "What is the difference between reduction rate and log reduction?",
        "The reduction rate is the percentage drop in viable count, which is intuitive; the log reduction expresses the drop in orders of magnitude and is more sensitive for highly antibacterial samples, so evaluating both is more complete.",
        "How are the inoculum and contact time set?",
        "Follow AATCC 100 for the organism (such as Staphylococcus aureus or Escherichia coli), the inoculum concentration and the contact time; deviating from the standard affects comparability of results.",
        "Can the result be used directly for product claims?",
        "The calculation is based on the colony counts you entered and is for evaluation reference only; antibacterial product claims must be reported by a qualified laboratory using the standard method and comply with the relevant regulations.",
        "About \"AATCC Antibacterial Test\"",
        "AATCC 100 is the American Association of Textile Chemists and Colorists quantitative antibacterial test standard. It compares the viable counts at 0 hours after inoculation and on the sample after contact, computes the reduction rate and log reduction, and evaluates textile antibacterial performance.",
        "Dual metrics of reduction rate and log reduction",
        "Multiple organisms with configurable contact time",
        "Control growth accounting",
        "Efficacy evaluation of antibacterial textiles",
        "Antibacterial agent screening and process optimisation",
        "Quality report data checking",
        "Compliance judgement for antibacterial product claims",
        "Used for control growth accounting",
    ]))

    write('time-35', build('time-35', [
        "📚 Steaming Time Lookup",
        "Recommend a saturated steam steaming time based on fabric type and dye type",
        "📖 Read the \"Steaming Time Lookup Usage Guide\"",
        "Viscose / rayon",
        "Shade depth",
        "💡 Saturated steam 100～105℃; time adjusts with dye type and shade depth",
        "The recommended times are empirical ranges and need fine-tuning in practice with the equipment and process",
        "Dark shades usually need longer steaming time to ensure adequate fixation",
        "📚 In-Depth Analysis: Steaming Time Lookup",
        "Steaming process parameter setting: take the midpoint of the recommended time by dye and shade depth as the initial process point.",
        "New formula steaming time estimation: quickly look up the recommended range when changing the dye or the shade, reducing trial and error.",
        "Steaming step quality troubleshooting: when fixation is insufficient, check whether the time was too short or the dye does not match.",
        "Example steaming time for a dark reactive shade",
        "For a dark reactive dye on cotton, the recommended steaming is 8~12 min (midpoint 10 min) at 102~104℃ saturated steam; if measured fixation is too pale, first confirm whether the steam is saturated and the humidity meets spec rather than simply extending the time.",
        "What affects steaming time?",
        "Mainly the dye class, fibre, shade depth and steam conditions; dark shades need longer than light ones, and disperse/acid dyes often need high-temperature dry steaming rather than saturated steam.",
        "How much longer for dark than light shades?",
        "With the same dye, dark shades are typically 2~5 min longer than light ones; the recommended range governs, and excessive time can cause bleeding or a poorer hand feel.",
        "What happens if the dye and fibre do not match?",
        "For example using a dye on polyester that needs vat steaming fails to fix when the conditions do not match; the tool identifies fibre/dye mismatches and prompts you to check the process system.",
        "About \"Steaming Time Lookup\"",
        "Steaming time directly affects dye fixation. Based on fabric type, dye type and shade depth, this tool gives the recommended time range and midpoint for saturated steam steaming, helping determine steaming step parameters quickly.",
        "Covers six dye classes: reactive, vat, sulphur, direct, disperse and acid",
        "Adjusts the time range for light/medium/dark shades",
        "Identifies fibre and dye mismatches",
        "Steaming process parameter setting",
        "New formula steaming time estimation",
        "Teaching reference for dyeing and printing processes",
        "Steaming step quality troubleshooting",
    ]))

    write('index', build('index', [
        "🎨 Dyeing and Printing Tools",
        "Dyeing and printing",
        "Dyeing and Printing Tools",
        "Exhaust and fixation rate calculator; enter the dye liquor concentrations before and after dyeing and apply the exhaustion method to get the exhaustion and fixation rates and assess the dyeing result.",
        "Dye dosage calculator; uses percentage on weight of fabric (% o.w.f) to get dye dosage and liquor formulation, assisting exhaust recipe preparation.",
        "Wash efficiency calculator; enter soaping temperature, wash count and water per wash to estimate wash efficiency and residual rate, assessing the soaping process.",
        "Simple Colour Difference ΔE(CMC) Assessment",
        "Enter the Lab values and tolerance of the standard and test samples, compute the colour difference ΔE with the CMC(l:c) formula and judge acceptability, for colour quality control in dyeing and printing and coatings.",
        "Steaming condition calculator; enter temperature, humidity and time to assess saturated steam steaming and assist post-printing processing.",
        "Enter the print paste concentration, binder ratio and total formula weight to compute the amount of each paste component (pigment, binder, auxiliary), for print sampling and production formulation preparation.",
        "Dyeing liquor ratio calculator; enter the liquor ratio, fabric weight and dye concentration to get the water volume, dye and auxiliary dosages, standardising the dyeing process.",
        "Fabric pH adjustment calculator; enter the current pH, target pH and fabric weight to estimate the acid/alkali adjusting agent dosage, assisting pretreatment before dyeing and finishing.",
        "Pad dyeing colour difference controller; enter the pickup and the before/after colour difference ΔE to assess the pad dyeing process and pass rate, assisting dyeing and printing quality control.",
        "Antibacterial (AATCC) Test",
        "AATCC 100 Antibacterial Test",
        "Steaming time lookup; recommends saturated steam steaming time by fabric and dye type, assisting determination of printing steaming parameters.",
        "Digital Printing Parameters",
        "Digital printing parameter calculator; enter resolution, print area and ink type to get ink usage and printing precision, assisting digital printing cost accounting.",
        "Enter washing, rubbing (dry rub) and light fastness grades to assess colour fastness comprehensively (grade 1～5, grade 5 is best)",
        "About \"Dyeing and Printing Tools\"",
        "Dyeing and Printing Tools collects 13 free online tools covering the common calculation, conversion and lookup needs of dyeing and printing scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you can find practical small tools here that are ready to use the moment you open them. All tools run purely on the front end and data is not uploaded to the server, protecting privacy.",
        "The dyeing and printing tools collected on this page include (some representative tools):",
        "These tools help you quickly complete common dyeing and printing tasks without memorising complex formulas or doing manual conversions — just enter and the result appears.",
        "Do the Dyeing and Printing Tools need a download or registration?",
        "No. All dyeing and printing tools on this page are purely front-end online tools; open the page and use them directly, with no software to install, no account to register and no data uploaded.",
        "Are the Dyeing and Printing Tools results accurate, and is the data secure?",
        "The tools compute locally in your browser from public mathematical formulas and general industry standards, so results are available immediately. All computation runs locally on your device, the data is never uploaded to the server, and privacy is well protected.",
    ]))


if __name__ == '__main__':
    main()