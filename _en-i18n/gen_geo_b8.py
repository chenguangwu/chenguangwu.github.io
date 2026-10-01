#!/usr/bin/env python3
# geology batch8 (3 slugs: mineral-hardness, generator-37, index)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'geology')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'geology')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'mineral-hardness': [
"🪨 Mineral Hardness Table",
"A Mohs hardness 1-10 standard mineral comparison, with scratching-test references given for the estimated hardness.",
'📖 View the "Mineral Hardness Table Guide"',
"The Mohs hardness 1 to 10 are, in order, talc, gypsum, calcite, fluorite, apatite, orthoclase, quartz, topaz, corundum and diamond; the scratching rule is that the harder one scratches the softer (quartz 7 can scratch glass at about 5.5, and diamond 10 can scratch any mineral); gemstone hardness references are jadeite 6.5 to 7, Hetian jade 6 to 6.5, rock crystal 7 and ruby/sapphire 9; minerals of similar hardness can be cross-scratched to establish their order.",
"Estimated mineral hardness (1-10)",
"Mohs hardness standard minerals",
"Scratching rule: a harder mineral scratches a softer one. Common references: fingernail about 2.5, copper coin about 3, iron nail about 5, glass about 5.5, steel file about 6.5.",
"📚 In-Depth Analysis: Mohs Hardness Standard Mineral Comparison and Scratch Identification",
"Mineral identification: cross-scratch minerals of known hardness to determine the hardness range of an unknown mineral",
"Jewellery identification: quickly distinguish common gemstone/jade materials such as quartz, feldspar and calcite",
"Teaching reference: memorise the 1-10 standard mineral sequence to aid field and classroom identification",
"Mohs hardness is a relative scratching grade (1 softest to 10 hardest): 1 talc, 2 gypsum, 3 calcite, 4 fluorite, 5 apatite, 6 orthoclase, 7 quartz, 8 topaz, 9 corundum, 10 diamond. Rule: if A can scratch B then A is harder; a fingernail is about 2.5, a copper coin about 3.5, glass about 5.5 (local reference, no network needed).",
"Example: a mineral that scratches glass (5.5) but is scratched by quartz (7) → hardness between 5.5 and 7, most likely orthoclase (6) from the table; also calcite (3), which effervesces strongly with dilute hydrochloric acid, can be distinguished from gypsum (2) by chemical reaction, and diamond (10) can scratch any mineral.",
"Is Mohs hardness a multiple of absolute hardness?",
"No. It is a relative scratching order and the gaps between adjacent grades are not equal (e.g. the absolute-hardness difference between diamond 10 and corundum 9 is far larger than between calcite 3 and gypsum 2). For absolute hardness you need micro-indentation (Vickers) hardness conversion.",
"How do you test a weathered sample by scratching?",
"A weathered surface is softer, so scratch on a fresh fracture, or use a knife/copper coin as an aid. When weathering is suspected, take several points and use the mode to avoid a single-point misjudgement.",
'About "Mineral Hardness Table"',
"Mineral Hardness Table is an online tool in the scientific research field. A scientific research tool that uses standard scientific formulas for accurate calculation.",
],
'generator-37': [
"✨ Geological (Map/Section/Column) Generator",
"Map/section/column",
'📖 View the "Geological (Map/Section/Column) Generator Guide"',
"A geological column arranges strata from top to bottom (youngest to oldest): layer thickness = top boundary depth − bottom boundary depth, cumulative thickness = Σ layer thicknesses; the scale converts to drawn length = actual thickness ÷ scale denominator (e.g. at 1:1000, 1 m is drawn as 1 mm); the section is drawn on a strike- and dip-oriented cut, and the attitude is defined by the three elements strike, dip angle and dip direction, with dip angle = arctan(vertical drop ÷ horizontal distance).",
"📚 In-Depth Analysis: Geological Column/Section Text Generation",
"Log-to-map: convert borehole or strata logging data into copyable column text for direct pasting into a report",
"Teaching illustration: quickly generate a standard layered column to aid field teaching and courseware",
"Data organisation: output the lithology sequences of several boreholes in a unified archive format",
"Usage: enter each stratum from top to bottom (lithology, thickness, symbol, etc.) and the tool renders the column/section text in layer order. It is recommended to note the lithology, thickness (m) and main markers (such as fossils, mineralisation) for each layer; a single layer is commonly 0.5-5 m thick and the total is often 10-30 m, with thickness units unified to m (generated locally, not uploaded).",
"Example: enter 5 layers — sandstone 2.0 m, mudstone 3.0 m, limestone 5.0 m, shale 1.0 m, basalt 4.0 m, total thickness 15.0 m; the tool generates top-down column text and labels the cumulative depth on each layer (2/5/10/11/15 m).",
"Does it generate an image or text?",
"This tool outputs a structured text column, easy to copy directly into Word/LaTeX reports; for a vector graphic, redraw it in GIS or professional column software in the same layer order.",
"Can thickness units be mixed?",
"No. All layer thicknesses must use the same unit (m recommended), otherwise the cumulative depth and the column scale are distorted.",
'About "Geological (Map/Section/Column) Generator"',
"Geological (Map/Section/Column) Generator. A free online tool, processed fully client-side, with no data uploaded, protecting your privacy.",
],
'index': [
"🪨 Geological Exploration Tools",
"Geological Exploration",
"Geological Exploration Tools",
"Based on the Gy sampling formula: enter particle size, sample mass and target grade to compute the relative sampling error and the minimum representative sample mass",
"Compute strata attitude by the three-point method: enter the coordinates and elevations of three points on the same rock surface to find the strike, dip direction and dip angle",
"Enter the arrival-time difference between the P and S waves to estimate the epicentral distance (P-wave velocity 6 km/s, S-wave velocity 3.5 km/s)",
"Enter the background value, anomaly value (and optional standard deviation) to compute the contrast coefficient, enrichment factor, anomaly threshold and anomaly intensity",
"Choose a geophysical method such as gravity, magnetic, electrical or seismic and enter the corresponding array and formation parameters to compute anomaly values or forward responses, for rapid processing of geophysical exploration data and verification of field measurements.",
"A geological map generation tool. From the entered strata parameters it generates column, section and other geological map text that can be copied directly into reports, for geological logging and data organisation.",
"Rock RQD Index",
"Compute the rock quality designation (RQD) from core-run lengths and assess the rock mass quality by the Deere grading standard.",
"Compute the ultimate bearing capacity and characteristic value of a strip footing from the Terzaghi formula (safety factor 2), for building foundation design and bearing-capacity checks.",
"A fault (nature/displacement/activity) assessment tool. Enter the fault-plane attitude and the displacement data of the two blocks to determine the fault nature (normal/reverse/strike-slip) and activity, for regional structure and engineering geology reference.",
"An underground exploration (cross-cut/drift/sampling) method tool. Enter the underground exploration parameters to get layout advice for cross-cuts, drifts and sampling, for underground exploration design and logging reference.",
"Enter the ore-body area, average thickness, ore bulk density and average grade to estimate the ore tonnage and metal content, for preliminary reserve assessment and resource estimation in mineral exploration.",
"An exploration (equipment/efficiency/cost) analysis tool. Enter the exploration equipment, efficiency and cost data to compute the unit exploration cost and cost-effectiveness, for economic assessment of geological survey projects (results for reference only).",
"Enter the survey area and sampling density to compute the number of sampling points, the grid spacing and a total workload estimate, for layout design and resource budgeting of regional geochemical surveys and environmental geochemical sampling plans.",
"A fold (anticline/syncline/axial plane) analysis tool. Enter the strata attitude and geometric parameters to determine the fold type (anticline/syncline) and estimate the axial-plane attitude, for geological structure teaching and field interpretation reference.",
"Ore Grade and Cut-off Grade Screening",
"Enter two adjacent section areas, the section spacing, ore bulk density and grade to compute the volume and reserve by the cross-section (parallel section) method",
"A trenching (trench/channel/sampling) design tool. Enter the trenching parameters to get trench specifications and channel-sampling layout advice, for surface exposure of mineral deposits and sampling engineering design reference.",
"Choose a geophysical method and enter the array parameters to estimate the depth of investigation and vertical resolution and evaluate the ability of different arrays to identify subsurface targets, for geophysical scheme design, survey-line layout and feasibility analysis of exploration depth.",
"Enter the element content, background value and standard deviation to compute the standardised anomaly value (Z value) and determine the anomaly class and intensity",
"Rock (mechanical/physical/hydraulic) Testing",
"Compute rock parameters such as uniaxial compressive strength (mechanical), dry density (physical), water absorption and softening coefficient (hydraulic): enter the test data and the tool calculates automatically and gives a rock quality assessment.",
"Enter slope angle, lithology, rainfall and slope height to comprehensively assess the hazard grade of geohazards such as landslides and collapses, for slope stability assessment and disaster-prevention zoning.",
"A geotechnical (parameter/test/statistics) analysis tool. Enter the geotechnical test parameters to statistically analyse the mechanical indices by engineering methods and give recommended values, for geotechnical parameter selection reference (results for reference only).",
"A joint (density/strike/filling) statistics tool. Enter the joint attitude and density data to statistically analyse joint density, preferred strike and filling, for rock-mass structural-plane analysis and slope stability reference.",
"Enter a set of geological data (comma- or space-separated) to compute the mean, standard deviation, coefficient of variation, confidence interval and other statistics",
"A Chinese chronostratigraphic standard correlation table, matching erathem (era) to system (period), age range and typical rocks and fossils",
"An assay (quality/internal check/external check) control tool. Enter the internal-check, external-check and overall quality data of an assay batch to assess the assay acceptance rate by engineering methods, for geological assay quality-control reference.",
"Earthquake Magnitude",
"Enter the Richter magnitude to compute the energy released by an earthquake and its TNT equivalent from the energy-magnitude relation, providing a comparison between magnitudes to help intuitively understand the link between energy scale and damage level.",
"A comparison table of the mineral composition, texture, structure and typical representatives of the three main rock classes — igneous, sedimentary and metamorphic — to aid field rock identification and geological learning.",
"A Mohs hardness 1-10 standard mineral comparison table with scratching-test references, for mineral identification, geological teaching and quick hardness discrimination of gems and jade.",
"An exploration (grid/spacing/engineering) layout tool. Enter the exploration type and grid parameters to compute the engineering spacing and overall layout, for mineral exploration engineering density design and resource-grading reference.",
"Enter the borehole layer depth, lithology, colour, structure and other logging information to automatically generate a standardised geological logging record sheet; supports accumulation and summarisation of multiple layers and can be exported for geological reports and survey data archiving.",
"Based on the Dupuit steady-flow formula for a fully penetrating well, enter the drawdown, pumping rate and well radius of a pumping test to compute the aquifer permeability coefficient K, for assessing the water-transmitting capacity and water yield of groundwater in hydrogeological surveys.",
"From morphological characteristics such as the anomaly amplitude, half-width and gradient, infer the likely type and depth of the geological body and give an ambiguous inference with a confidence level, aiding the qualitative interpretation of geophysical results and prospecting target screening.",
"Enter the geological relic type, scale, integrity and scientific value for weighted scoring, outputting a composite score, a five-level protection grade (national to ordinary) and protection advice, aiding applications.",
"Enter the borehole apparent thickness, strata dip and ore-body size to compute modelling parameters such as true thickness, true area and volume",
"Enter the measured contaminant concentration, background value and assessment standard to compute the pollution index, exceedance factor and geo-accumulation index",
"Enter the measured values and assessment standards of each environmental factor and use the Nemerow composite index method to compute the composite environmental quality index",
'About "Geological Exploration Tools"',
"The Geological Exploration Tools collection includes 37 free online tools covering common calculation, conversion and lookup needs in geological exploration. Whether you are a professional in the field, a student or an ordinary user, you can find ready-to-use practical tools here. All tools run fully client-side with no data uploaded to a server, protecting your privacy.",
"The geological exploration tools listed on this page include (some representative tools):",
"These tools help you quickly complete common geological exploration tasks without memorising complex formulas or doing manual conversions — just enter the data to get the result.",
"Do the geological exploration tools require downloading or registration?",
"No. All geological exploration tools on this page are fully client-side online tools that can be used directly by opening the web page, with no software installation, no account registration and no data uploaded.",
"Are the calculation results of the geological exploration tools accurate? Is the data safe?",
"The tools compute locally in your browser based on public mathematical formulas and common industry standards, with instant results. All calculations are done locally on your device and no data is uploaded to a server, so your privacy is protected.",
],
}

EXTRA = {
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
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('!! %s EXTRA CJK/CNP violation: %s' % (slug, en[:60]))
            sys.exit(1)
        mp[z] = en
    return mp

def write(slug, mp):
    os.makedirs(OUT, exist_ok=True)
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('name', slug)
    out = {'slug': slug, 'industry': 'geology', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

for slug, en_list in EN.items():
    write(slug, build(slug, en_list))
