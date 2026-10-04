#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'tunnel')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'tunnel')
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
    out = {'slug': slug, 'industry': 'tunnel', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

#!/usr/bin/env python3


def main():
    write('advance-rate', build('advance-rate', [
        '🏎️ Tunnel Advance Rate Estimation',
        'Estimates drill-and-blast cycle time, advance per cycle and daily advance',
        'Advance Rate',
        '/ Advance Rate',
        '📖 View the Tunnel Advance Rate Estimation user guide',
        'Drilling parameters',
        'Blasthole depth l (m)',
        'Blasthole utilisation η',
        'Cycle operation durations (hours)',
        'Drilling time',
        'Charging and blasting',
        'Ventilation and fume clearing',
        'Mucking time',
        'Support time',
        'Maximum cycles per day',
        'Advance per cycle',
        'Daily advance',
        'Monthly advance',
        'Advance per cycle = l × η; daily advance = advance per cycle × number of cycles',
        'Advance per cycle = blasthole depth × blasthole utilisation (η is typically 0.85~0.95)',
        'Cycle time = drilling + charging + ventilation + mucking + support',
        'Daily advance = advance per cycle × cycles per day',
        'Monthly advance = daily advance × 30 (estimated at full capacity)',
        '💡 Drill-and-blast advance is typically 3~9 m per day; TBM advance can reach 15~40 m per day. Actual progress is strongly affected by geological conditions, equipment matching and management level.',
        '📚 In-depth analysis: Tunnel Advance Rate Estimation',
        'Advance per cycle: advance per cycle = blasthole depth × blasthole utilisation η (typically 0.85~0.95, decided by rock properties and drilling accuracy); increasing hole depth raises the advance, but η usually falls as a result.',
        'Cycle time and number of cycles: cycle time = the sum of the durations of drilling, blasting, ventilation, mucking and support; cycles allowed by time = floor(24 ÷ cycle time), actual cycles = min(planned cycles, cycles allowed by time), i.e. constrained by both the plan and the available time.',
        'Advance and schedule: daily advance = advance per cycle × actual cycles, monthly advance = daily advance × 30; the tool also estimates the schedule in months for a 1000 m single-face drive as 1000 ÷ daily advance ÷ 30, to compare the marginal benefit of different operation combinations (for example adding a jumbo to shorten drilling, or optimising mucking to shorten the cycle).',
        'Worked example: daily advance of a full-face method with 3 m hole depth and 0.9 utilisation',
        'Input: hole depth 3 m, utilisation 0.9, drilling 3 h, blasting 1 h, ventilation 0.5 h, mucking 3 h, support 2 h, planned cycles 3 per day. Advance per cycle = 3 × 0.9 = 2.70 m; cycle time = 3 + 1 + 0.5 + 3 + 2 = 9.50 h; cycles allowed by time = floor(24 ÷ 9.5) = 2 per day; actual cycles = min(3, 2) = 2 per day (time-constrained rather than plan-constrained); daily advance = 2.70 × 2 = 5.40 m; monthly advance (full capacity) = 162 m; a 1000 m drive takes about 6.2 months. For comparison: hole depth 4 m with drilling 4 h (all else unchanged) → advance 3.60 m, cycle 10.50 h, 2 cycles per day, daily advance 7.20 m, 216 m per month, 4.6 months; a short-advance fast-cycle scheme (hole depth 2 m, η = 0.85, drilling 2 h, blasting 0.5 h, ventilation 0.5 h, mucking 2 h, support 1.5 h, 4 planned cycles per day) → advance 1.70 m, cycle 6.50 h, floor(24 ÷ 6.5) = 3 cycles per day, daily advance 5.10 m, 153 m per month, 6.5 months.',
        'Why is the actual number of cycles often lower than the planned number I enter?',
        'Because the tool takes min(planned cycles, floor(24 ÷ cycle time)). When the sum of the five operation durations is large, the planned number simply cannot be fitted into a day, so the bottleneck is cycle time rather than planning. To speed up, optimise the longest operation: when drilling dominates, add a jumbo or multi-boom drill and switch to deeper-hole blasting; when mucking has a high share, increase loading and hauling capacity and shorten the haul distance; when support takes long, separate temporary initial shotcreting from the later permanent lining.',
        'What value is normally used for blasthole utilisation η, and does a larger hole depth always mean faster progress?',
        'η is usually 0.85~0.95: use 0.90~0.95 for intact hard rock with high drilling accuracy, and around 0.85 or lower for fracture zones and soft rock. Increasing hole depth raises the advance per cycle, but deep holes take longer to drill, show stronger confinement and η tends to drop; the longer cycle also reduces the number of cycles per day, so an optimum hole depth exists. Compare 2~4 combinations of hole depth and operations with this tool and take the scheme with the largest daily advance.',
        'About Advance Rate',
        'Tunnel advance rate estimator - a calculation tool for drill-and-blast cycle time and daily advance. A scientific research tool that uses standard scientific formulas for accurate calculation.',
    ]))

    write('gas-monitor', build('gas-monitor', [
        '📚 Tunnel Gas Monitoring Reference',
        'Enter the gas concentration to look up the safety level and response measures (based on the Coal Mine Safety Regulations and the Technical Code for Railway Gas Tunnels)',
        'Gas Monitor',
        '/ Gas Monitor',
        '📖 View the Tunnel Gas Monitoring Reference user guide',
        'Gas concentration classification (Coal Mine Safety Regulations): when the concentration reaches 1.0% work must stop, power must be cut and personnel withdrawn; 1.0% to 5.0% is the danger zone, 5% to 16% is the explosive range, and at 16% the oxygen content is insufficient; near electrical equipment the same 1.0% power-cut threshold applies, with continuous monitoring and graded response.',
        'Gas concentration (%)',
        'Monitoring location',
        'Working face / return airflow',
        'General roadway',
        'Near electrical equipment',
        '📊 Gas concentration safety levels',
        '📋 Gas concentration limit standards',
        'Response measures',
        'Normal work, continuous monitoring',
        'Increase ventilation and monitoring frequency',
        'Alert',
        'Stop part of the work and evacuate non-essential personnel',
        'Stop work, cut power and withdraw personnel',
        'Extremely dangerous',
        'Evacuate immediately, seal the working face and report for handling',
        '⚡ Gas power-cut concentration near electrical equipment',
        'Power-cut concentration',
        'Power-restore concentration',
        'Excavation working face',
        'Return airway',
        'Series ventilation',
        'Chamber',
        '🌋 Gas explosibility',
        'Explosive concentration range of gas (methane): ',
        ', with the most explosive concentration around',
        'Ignition temperature: ',
        '. Below 5% it does not explode but can burn; above 16% it does not explode because of oxygen deficiency but can burn.',
        'The gas explosion triangle requires all of the following: concentration 5%~16% + oxygen ≥12% + ignition source ≥650 °C.',
        '⚠️ This tool is for safety reference only; gas tunnel construction must be equipped with professional gas detection equipment and ventilation systems, and must strictly follow gas inspection procedures and explosion-prevention measures.',
        '📚 In-depth analysis: Tunnel Gas Monitoring Reference',
        'Five concentration levels and responses: <0.5% safe (normal work, continuous monitoring), 0.5%~0.8% caution (increase ventilation and monitoring frequency), 0.8%~1.0% alert (stop part of the work, evacuate non-essential personnel), 1.0%~1.5% danger (stop work, cut power, withdraw personnel), ≥1.5% extremely dangerous (evacuate immediately, seal the working face, report for handling).',
        'Power-cut threshold: a concentration reaching or exceeding 1.0% means power must be cut immediately; the page labels the measuring point by monitoring location (working face / return airflow, general roadway, near electrical equipment), and the threshold at all three is 1.0%.',
        'Explosibility judgement: a concentration falling in the 5%~16% range is judged to be within the explosive concentration range (extremely dangerous); below 5% it is under the lower explosive limit and will not explode; above 16% it is above the upper explosive limit and will not explode because of oxygen deficiency. The page uses a five-segment colour bar (safe green / caution blue / alert yellow / danger red / extreme-danger dark red) to show which range the current concentration falls in.',
        'Worked example: classification and response for eight concentration points',
        '0.30% → safe, normal work with continuous monitoring, no power cut, below the lower explosive limit; 0.50% → caution, increase ventilation and monitoring frequency, no power cut; 0.65% → caution, same as above; 0.90% → alert, stop part of the work and evacuate non-essential personnel, no power cut (below 1.0%); 1.20% → danger, stop work, cut power and withdraw personnel, power cut required; 2.00% → extremely dangerous, evacuate immediately, seal the working face and report, power cut required; 8.00% → extremely dangerous and within the explosive concentration range (5%~16%); 20.00% → extremely dangerous, but above the upper explosive limit and non-explosive because of oxygen deficiency.',
        'Why must power be cut and personnel withdrawn when the gas concentration reaches 1.0%?',
        '1.0% is far below the 5% lower explosive limit, and the margin allows for monitoring lag, local accumulation and rapid concentration rises. Gas distribution underground is highly uneven, and local high concentrations easily form at the roof, in corners and in unventilated areas, so when a measuring point reads 1.0% the local value may already be far higher. The regulations therefore require stopping work, cutting power and withdrawing personnel at 1.0%, then ventilating and re-testing until acceptable before resuming, rather than waiting until the concentration approaches the lower explosive limit.',
        'If the concentration exceeds 16% it "does not explode" — does that mean it is no longer dangerous?',
        'No. Being above the upper explosive limit only means the mixture at that point cannot be ignited because of oxygen deficiency, but it is extremely dangerous: first, anyone entering will suffocate from lack of oxygen; second, once the gas mixes with fresh air and is diluted back into the 5%~16% range it immediately becomes an explosive mixture. Accumulations of high-concentration gas must therefore be sealed and kept strictly off-limits; they are handled by a professional rescue team following gas drainage procedures with slow release and continuous monitoring of the concentration in the return airflow.',
        'About Gas Monitor',
        'Gas monitoring reference tool - look up tunnel gas concentration safety standards; enter a concentration to automatically determine the safety level and response measures. A scientific research tool that uses standard scientific formulas for accurate calculation.',
    ]))

    write('lining-thickness', build('lining-thickness', [
        '📏 Tunnel Lining Thickness Calculation',
        'Estimates primary support and secondary lining thickness from the surrounding rock grade and excavation span',
        'Lining Thickness',
        '/ Lining Thickness',
        '📖 View the Tunnel Lining Thickness Calculation user guide',
        'Primary lining shotcrete thickness',
        'Secondary lining thickness',
        'Total support thickness',
        'Secondary lining reinforcement',
        '📐 Empirical estimation formula',
        'h₂ = k · B, where k = 0.04~0.10 by surrounding rock grade',
        'The secondary lining thickness h₂ is estimated as a multiple of the span (k = 0.04~0.10, using the larger value for poorer rock);',
        'primary support shotcrete thickness is generally 5~25 cm;',
        'the secondary lining is generally cast-in-place concrete, 30~60 cm thick;',
        'the actual thickness should be determined by a load-structure or ground-structure calculation.',
        '💡 This tool gives an empirical estimate; for grade IV and poorer rock the secondary lining should be designed as a load-bearing structure with load-carrying reinforcement; the final thickness is governed by code calculations and monitoring measurement feedback.',
        '📚 In-depth analysis: Tunnel Lining Thickness Calculation',
        'Secondary lining thickness: the secondary lining coefficient k is taken by surrounding rock grade (grade I 0.04, II 0.05, III 0.06, IV 0.075, V 0.09, VI 0.10), h₂ = k × excavation span B, rounded up to 0.1 m and not less than 0.3 m; the poorer the rock, the larger k and the thicker the secondary lining.',
        'Primary support: apply sprayed ',
        ' at a thickness fixed by rock grade (grade I 5 cm, II 8, III 12, IV 15, V 20, VI 25 cm); total support thickness = primary lining thickness + secondary lining thickness.',
        'Reinforcement and quantities: grade IV and above (grade ≥ 5) is judged to require reinforcement (reinforced concrete), grades I–III use plain concrete; the concrete volume per metre is also estimated from the secondary lining thickness as ≈ h₂ × 2 × (B + 5) m³ (perimeter approximation), for material preparation and cost estimating.',
        'Worked example: lining thickness for six rock grades at a 10 m excavation span',
        'Take B = 10 m: grade I k = 0.04 → h₂ = 0.4 m (40 cm), primary lining 5 cm, total 45 cm, plain concrete, about 12.0 m³ of secondary lining per metre; grade II k = 0.05 → h₂ = 0.5 m, primary lining 8 cm, total 58 cm, about 15.0 m³; grade III k = 0.06 → h₂ = 0.6 m, primary lining 12 cm, total 72 cm, about 18.0 m³; grade IV k = 0.075 → h₂ = 0.8 m, primary lining 15 cm, total 95 cm, reinforcement required, about 24.0 m³; grade V k = 0.09 → h₂ = 0.9 m, primary lining 20 cm, total 110 cm, reinforcement required, about 27.0 m³; grade VI k = 0.10 → h₂ = 1.0 m, primary lining 25 cm, total 125 cm, reinforcement required, about 30.0 m³. The secondary lining thickens linearly as the span grows: grade IV with B = 14 m → h₂ = k × 14 = 1.05 m, rounded to 1.1 m (110 cm), total thickness 125 cm, about 41.8 m³ per metre.',
        'Why is the secondary lining thickness estimated as k × span instead of calculated from loads?',
        'k × B is an empirical value from the engineering analogy method: it compresses the two main factors, rock grade (a composite rating of integrity, strength, groundwater and so on) and excavation span, into a single coefficient for rapid thickness estimation and material preparation at the scheme stage. Formal design should model the structure with the load-structure or ground-structure method, including rock pressure, water pressure, seismic force and self weight, and verify the reinforcement of the secondary lining; the result of this tool cannot replace a structural calculation report.',
        'What is the basis for requiring reinforcement at grade IV and above, and when is a plain concrete secondary lining used?',
        'The tool judges reinforcement to be required when grade ≥ 5 (grade IV and above). The reason is that with poor rock the secondary lining must carry significant rock pressure and differential settlement, while plain concrete has low tensile strength and cracks easily. Grades I–III have strong self-supporting capacity, so the secondary lining mostly serves as a safety reserve and crack-limiting structure and may be plain concrete; but where there is unsymmetrical loading, shallow cover, a portal section or groundwater attack, reinforcement or steel-fibre concrete should be used even in better rock.',
        'About Lining Thickness',
        'Tunnel lining thickness calculator - estimates primary support and secondary lining thickness from the surrounding rock grade and excavation span. A scientific research tool that uses standard scientific formulas for accurate calculation.',
    ]))

    write('support-design', build('support-design', [
        '📐 Tunnel Support Parameter Design',
        'Estimates support parameters such as rock bolts and shotcrete from the surrounding rock grade and excavation span',
        'Support Design',
        '/ Support Design',
        '📖 View the Tunnel Support Parameter Design user guide',
        'Excavation height H (m)',
        'Bolt length',
        'Bolt spacing',
        'Shotcrete thickness',
        'Bolts per metre',
        '📐 Empirical estimation formula',
        'The bolt length L is estimated from the height of the caving arch (generally 1/3~1/4 of the span and not less than 2 m);',
        'The bolt spacing S is usually 0.8~1.5 m, with S ≤ L/2;',
        'The shotcrete thickness t is 5~25 cm depending on the surrounding rock grade;',
        'The actual design must be determined comprehensively from rock mechanical parameters, in-situ stress and monitoring measurement data.',
        '💡 This tool gives empirical reference values only; the actual support parameters should be determined according to the Code for Design of Highway Tunnels or the Code for Design of Railway Tunnels, combined with numerical simulation.',
        '📚 In-depth analysis: Tunnel Support Parameter Design',
        'Bolt length: L = coefficient × excavation span B, with the coefficient increasing by rock grade (grade I 0.20, II 0.25, III 0.30, IV 0.35, V 0.40, VI 0.45), and not less than 2.0 m; the result is given to one decimal place.',
        'Bolt spacing: S = min(L/2, grade upper limit) — 1.5 m for grades I–II, 1.2 m for grade III and 1.0 m for grade IV and above, laid out in a staggered (quincunx) pattern; the poorer the rock, the closer the spacing.',
        'Shotcrete thickness and quantities: sprayed ',
        ' thickness by grade is 5/8/12/18/22/25 cm (grades I–VI); the number of bolts per metre = ceil(support perimeter ÷ S²), where the support perimeter is approximated as 2 × (B + H), and multiplying by L gives the total bolt length per metre; support recommendations are given by grade as combinations (grades I–II local bolts + thin shotcrete, grades III–IV systematic bolts + mesh + shotcrete, grades V–VI systematic bolts + double mesh + steel-fibre shotcrete plus steel arches where needed).',
        'Worked example: support parameters for a 12 × 8 m section in six rock grades',
        'Take B = 12 m and H = 8 m (support perimeter ≈ 2 × (12 + 8) = 40 m): grade I L = 12 × 0.20 = 2.4 m, S = min(1.2, 1.5) = 1.2 m, shotcrete 5 cm, ceil(40 ÷ 1.44) = 28 bolts per metre, total length 67.2 m, recommended local bolts + thin shotcrete; grade II L = 3.0 m, S = 1.5 m, shotcrete 8 cm, 18 bolts, 54.0 m; grade III L = 3.6 m, S = 1.2 m, shotcrete 12 cm, 28 bolts, 100.8 m, recommended systematic bolts + mesh + shotcrete; grade IV L = 4.2 m, S = 1.0 m, shotcrete 18 cm, 40 bolts, 168.0 m; grade V L = 4.8 m, S = 1.0 m, shotcrete 22 cm, 40 bolts, 192.0 m; grade VI L = 5.4 m, S = 1.0 m, shotcrete 25 cm, 40 bolts, 216.0 m, with grades V–VI recommended as systematic bolts + double mesh + steel-fibre shotcrete plus steel arches where necessary.',
        'Is it safe to compute the bolt length as "coefficient × span"?',
        'This is an empirical value from the engineering analogy method, used for preliminary parameter selection and quantity estimation; it cannot replace design verification. The bolt length must ensure the anchored section reaches deep enough into stable rock (generally not less than 0.5~1.0 m) and satisfy checks based on the suspension theory or the composite arch theory; special conditions such as shallow cover, unsymmetrical loading, fault fracture zones and swelling rock must be calculated specifically by the design unit, with longer bolts or cables where necessary.',
        'Why is the number of bolts per metre computed as ceil(perimeter ÷ spacing²)?',
        'The tool approximates the support surface as an unfolded plane with bolts laid out on an S × S grid, using the perimeter 2 × (B + H) as the unfolded width per metre, so bolts per metre = ceil(perimeter ÷ S²), rounded up so no position is missed. This is a simplified estimate: with an actual staggered layout adjacent rows are offset by half a grid, so the count differs slightly, and the spacing at the arch and the sidewalls may also be set separately, so quantity checks should follow the construction drawings.',
        'About Support Design',
        'Tunnel support design calculator - estimates bolt length, spacing and shotcrete thickness from the surrounding rock grade and excavation span. A scientific research tool that uses standard scientific formulas for accurate calculation.',
    ]))

    write('ventilation-calc', build('ventilation-calc', [
        '🧮 Tunnel Ventilation Calculation',
        'Computes the required tunnel air volume, control air velocity and fan selection reference',
        '📖 View the Tunnel Ventilation Calculation user guide',
        '💨 Control velocity method',
        '🏭 CO dilution method',
        'Tunnel cross-sectional area A (m²)',
        'Design control velocity v (m/s)',
        'Tunnel length L (m)',
        'Hourly traffic volume N (vehicles/h)',
        'CO emission per vehicle q (m³/km·vehicle)',
        'Allowable CO concentration δ (ppm)',
        'Required air volume Q',
        'Required air volume per second',
        'Control velocity v',
        'Air changes per hour',
        'Control velocity method: required air volume Q = tunnel cross-sectional area × design control velocity',
        'CO dilution method: Q = q · N · L / δ (back-calculating the required air volume from the allowable CO concentration)',
        'Air changes n = Q / (A · L) (per hour)',
        '💡 The design air velocity for a general road tunnel should be 2~4 m/s and must not exceed 8 m/s; the allowable CO concentration is 100 ppm in normal operation and 150 ppm under traffic congestion.',
        '📚 In-depth analysis: Tunnel Ventilation Calculation',
        'Velocity-controlled (velocity mode): required air volume Q = cross-sectional area A × control velocity v × 3600 (m³/h), with Q ÷ 3600 (m³/s) also given; air changes are estimated as v × 3600 ÷ 100 (i.e. hourly air changes based on a 100 m tunnel section). The tool also gives a ',
        'Fan Sizing Calculator',
        ' reference: with two units in parallel, the air volume per unit = Q ÷ 3600 ÷ 2 (m³/s).',
        'CO dilution (CO mode): total CO emission = emission per vehicle q × hourly traffic volume N × tunnel length L; required air volume Q = q × N × L ÷ δ (δ is the allowable CO concentration, substituted directly as the ppm value); the required control velocity v = Q ÷ 3600 ÷ A and air changes n = v × 3600 ÷ L are then back-calculated.',
        'Cross-checking the two modes and selection: first use the velocity method to obtain the air volume that satisfies the minimum velocity, then use the CO method to check the demand for diluting harmful gases, and take the larger of the two as the design air volume; fan selection is determined from the number of units in parallel and an air volume margin (generally a further 1.1~1.2 standby factor).',
        'Worked example: velocity method for a 60 m² section at a control velocity of 2.5 m/s',
        'Velocity mode with A = 60 m² and v = 2.5 m/s: required air volume Q = 60 × 2.5 × 3600 = 540000 m³/h = 150.00 m³/s; air changes = 2.5 × 3600 ÷ 100 = 90.00 per hour; fan selection reference = 75.00 m³/s per unit × 2 units. Another set, A = 80 m² and v = 2.0 m/s → Q = 576000 m³/h = 160.00 m³/s, 72.00 air changes per hour, 80.00 m³/s per unit.',
        'Why is the air volume from CO mode much smaller than from the velocity method, and can it be used directly?',
        'No, it cannot be used directly. The CO mode of this tool substitutes values directly into Q = q × N × L ÷ δ: with the defaults q = 0.02, N = 800 vehicles/h, L = 1000 m and δ = 100 it outputs Q = 160 m³/h (0.04 m³/s) and v = 0.001 m/s. Here L is entered in metres and δ as the ppm value, without converting to km and a volume ratio as engineering practice requires (100 ppm = 1 × 10⁻⁴). Using the standard form Q = q × N × L (km) ÷ δ (volume ratio), the same physical conditions give 0.02 × 800 × 1.0 ÷ 1e-4 = 160000 m³/h ≈ 44.4 m³/s. The CO mode result can therefore only be used as a relative comparison on the same basis; for engineering calculations convert to standard units yourself and take the larger of the velocity method result and the code limit.',
        'What does the 100 in the air change calculation mean?',
        'The tool estimates hourly air changes as v × 3600 ÷ 100, i.e. it takes a 100 m long tunnel section as the basis by default (the velocity multiplied by the distance travelled in one hour, divided by the 100 m section length). If the actual ventilation section length differs, convert using v × 3600 ÷ actual section length yourself, otherwise the air change rate will be systematically over- or under-estimated.',
        'About Ventilation Calc',
        'Tunnel ventilation calculator - computes required tunnel air volume and control velocity, supporting section ventilation and CO dilution air volume calculations. A scientific research tool that uses standard scientific formulas for accurate calculation.',
    ]))


if __name__ == '__main__':
    main()
