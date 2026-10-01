#!/usr/bin/env python3
# geology batch7 (5 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'geology')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'geology')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'rock-identify': [
"🔍 Rock Identification",
"A comparison of the mineral composition, texture, structure and typical representatives of the three main rock classes: igneous, sedimentary and metamorphic.",
'📖 View the "Rock Identification Guide"',
"Distinguish the three rock classes by origin and texture: igneous rocks form by cooling of magma — intrusive rocks such as granite are coarsely crystalline, extrusive rocks such as basalt are dense and vesicular; sedimentary rocks such as sandstone, shale and limestone have bedding and fossils, often with clastic or chemical sedimentary textures; metamorphic rocks such as gneiss, schist, marble and slate have foliation and gneissose structure with oriented minerals; the criteria are texture and structure, mineral assemblage and mode of occurrence.",
"All rock classes",
"Igneous",
"Metamorphic",
"Identification points: first look at the structure (bedding → sedimentary, foliation/gneissosity → metamorphic, massive/vesicular → igneous), then the texture (crystalline/clastic/crystalloblastic) and mineral composition (quartz, feldspar, calcite, etc.).",
"📚 In-Depth Analysis: Field Identification of the Three Rock Classes (Igneous/Sedimentary/Metamorphic)",
"Class discrimination: distinguish igneous, sedimentary and metamorphic rocks by mineral composition, texture and structure",
"Representative confirmation: compare with typical representatives in the field (such as granite, sandstone, gneiss) for quick naming",
"Teaching: build a \"composition-texture-structure\" three-way identification approach",
"Decision chain: ① look at the structure — bedding → sedimentary, foliation/gneissosity → metamorphic, massive → mostly igneous; ② look at the texture — clastic/argillaceous → sedimentary, crystalloblastic → metamorphic, holocrystalline/porphyritic → igneous; ③ look at the minerals — quartz + feldspar + dark minerals and coarse grains → granite family. Igneous rocks are classed by SiO₂ as acidic (>65%)/intermediate/basic/ultrabasic (local correlation table, no network needed).",
"Example: a rock with obvious quartz and potassium feldspar, holocrystalline medium-coarse grains, massive structure, SiO₂≈72% → granite (acidic plutonic igneous); another black, dense, porphyritic/cryptocrystalline, vesicular → basalt (basic extrusive, SiO₂≈48%); one that effervesces strongly with dilute hydrochloric acid and has bedding → limestone (chemical/biogenic sedimentary rock).",
"How do you distinguish granite and rhyolite, which have similar compositions?",
"Both are rich in quartz + potassium feldspar (acidic); the difference lies in the mode of occurrence and texture: granite is plutonic, holocrystalline and medium-coarse grained, while rhyolite is extrusive, porphyritic/cryptocrystalline and has flow banding. Look at the texture rather than the composition to distinguish them.",
"Do marble and limestone have the same composition?",
"Their main component is both calcite, but marble is limestone recrystallised by regional/contact metamorphism into a granular crystalloblastic, massive rock; both effervesce with acid. The difference lies in the texture (crystalloblastic vs biogenic/chemical) and whether a metamorphic mineral assemblage is present.",
'About "Rock Identification"',
"Rock Identification is an online tool in the scientific research field. A scientific research tool that uses standard scientific formulas for accurate calculation.",
"Search rock / composition / texture / structure...",
],
'duanceng-xingzhi-weiyi-huodongxing-panding': [
"🪨 Fault (Nature/Displacement/Activity) Assessment",
"Estimate the annual displacement rate from the fault displacement and active period, and determine the activity grade and engineering risk.",
'📖 View the "Fault (Nature/Displacement/Activity) Assessment Guide"',
"Annual displacement = displacement ÷ active period; ≥0.01 mm/year active fault, ≥0.001 suspected, otherwise stable",
"Fault activity is the rate converted from displacement and time: annual displacement = displacement (mm) ÷ active period (years). ≥0.01 mm/year is an active fault, ≥0.001 suspected active, otherwise stable. Active faults carry high engineering risk, and site selection and seismic design must be raised in grade.",
"Displacement (mm)",
"Active period (years)",
"💡 Annual displacement = displacement ÷ active period; ≥0.01 active, ≥0.001 suspected, otherwise stable.",
"📚 In-Depth Analysis: Field Identification of Fault Nature and Activity (Normal/Reverse/Strike-slip · Activity Grading)",
"Nature identification: determine a normal/reverse/strike-slip fault from the pitch of slickensides on the fault plane, the steps and the relative displacement of the two blocks",
"Activity assessment: judge active/inactive from the latest offset strata, the freshness of the fault scarp and the trench displacement",
"Engineering avoidance: provide fault avoidance distances and seismic design advice for linear projects and building sites",
"Key points: a slickenside pitch near horizontal (<15°) → strike-slip fault; near vertical (>75°) with the hanging wall rising → reverse fault; hanging wall falling → normal fault. The scarp of the steps (feather-tension fractures) points in the movement direction of the opposite block. Activity is graded by the age of the offset strata, the scarp height and the displacement rate (local reference; combine with measured sections).",
"Example: a strike-slip fault with a slickenside pitch of 10° and a horizontal offset of 50 m, offsetting Holocene strata 8 m thick → strike-slip in nature, active since the Late Pleistocene; the horizontal slip rate is about 50 m/(8×10³ a)≈6.25 mm/a, so an engineering avoidance zone of ≥30 m and higher seismic design are recommended.",
"How do you judge the nature if the slickensides are destroyed?",
"Use the steps, the tectonite zonation (cataclasite → mylonite) and the repetition/missing relationship of the strata on the two blocks to judge comprehensively. When a single marker is unreliable, dig trenches or shallow boreholes for direct displacement evidence.",
"What is the activity grading based on?",
"Mainly the age of the latest offset geological body: offsetting Holocene strata is an active fault, offsetting Upper Pleistocene is Late Pleistocene activity, and older is inactive. The exact thresholds follow engineering site fault-activity assessment codes such as GB/T 36072.",
'About "Fault (Nature/Displacement/Activity) Assessment"',
"Fault (Nature/Displacement/Activity) Assessment. A free online tool, processed fully client-side, with no data uploaded, protecting your privacy.",
"Displacement",
],
'analysis-33': [
"⚖️ Assay (Quality/Internal Check/External Check) Control",
"Internal check/external check",
'📖 View the "Assay (Quality/Internal Check/External Check) Control Guide"',
"Relative deviation RD = |primary assay − check assay| ÷ their mean × 100%; RD not exceeding the allowed limit (default 5%) is considered acceptable.",
"Internal-check acceptance rate = number of items within tolerance ÷ number of checked items × 100%; by quality-management convention, an acceptance rate ≥ 90% marks the whole batch as acceptable.",
"The tool is a client-side statistic that computes the deviation sample by sample and lists the out-of-tolerance items, making it easy to locate samples needing re-check.",
"Check data (each line \"sample ID,primary assay,check assay\")",
"Allowed relative deviation limit (%)",
"Quality assessment",
"📚 In-Depth Analysis: Internal and External Check Control of Assay Quality",
"Quality spot-check of an assay batch",
"Deviation assessment of internal-check replicate analyses",
"Comparison of external-check laboratory results",
"Relative deviation RD = |A−B| ÷ [(A+B)÷2] ×100%; internal-check acceptance rate = number of items within tolerance ÷ number of checked items ×100%. Out of tolerance means RD greater than the allowed limit.",
"S-01 12.5/12.1, S-02 8.4/8.9, S-03 20.0/19.2 with an allowed limit of 5% → RD are 3.25%, 5.78% and 4.08%, mean 4.37%; 1 item out of tolerance, acceptance rate 66.67%, judged unacceptable.",
"What acceptance rate counts as acceptable?",
"A batch acceptance rate ≥90% is acceptable; out-of-tolerance items must be re-checked and the cause found; below 90% the spot-check proportion should be increased.",
"How is the allowed limit set?",
"Look it up by analysis method and content level in the quality-management code; 5% is common for high content, and low content can be relaxed to 10%-20%. The tool allows you to set it yourself.",
'About "Assay (Quality/Internal Check/External Check) Control"',
"Assay (Quality/Internal Check/External Check) Control. A free online tool, processed fully client-side, with no data uploaded, protecting your privacy.",
],
'stats-analysis-2': [
"⛰️ Geotechnical Parameter Test Statistics and Standard Value",
"Enter a group of geotechnical test values to compute the mean and coefficient of variation and obtain the standard value by code-based correction.",
"Geotechnical parameters cannot take the test mean directly as the design value: the more dispersed the data and the fewer the samples, the more the value should be reduced. The code approach is to first compute the coefficient of variation δ = σ/μ to measure the dispersion, then apply the statistical correction factor γs = 1 −(1.704/√n + 4.678/n²)·δ to reduce the mean and obtain the standard value (recommended value). A larger sample size n gives a smaller reduction; when δ is very large the test data are severely dispersed and the cause should be found or more tests added rather than mechanically reducing. The standard deviation uses the sample basis (n−1). All calculations are done locally in the browser; no data is uploaded.",
'📖 View the "Geotechnical (Parameter/Test/Statistics) Analysis Guide"',
"Coefficient of variation δ = standard deviation ÷ mean; statistical correction factor γs = 1 −(1.704/√n + 4.678/n²)·δ; standard value = γs × mean",
"Enter one test value per line, or \"ID,value\", e.g. T1,12.5",
"📚 In-Depth Analysis: Geotechnical Parameter Test Statistics and Standard Value",
"Geotechnical test data processing",
"Design values of geotechnical parameters",
"Test dispersion assessment",
"÷ mean; statistical correction factor γs = 1 −(1.704/√n + 4.678/n²)·δ; standard value = γs × mean, with the standard deviation computed on the sample basis (n−1).",
"20.4, 18.6, 22.1, 19.3, 21.5 → mean 20.38, standard deviation 1.462, coefficient of variation 7.17%; with n=5, γs = 1 −(1.704/√5 + 4.678/25)×0.0717 = 0.9319 → standard value = 0.9319 × 20.38 = 18.99.",
"Why not use the mean directly?",
"Test data are dispersed and the sample is limited, so taking the mean directly is unsafe; the code uses a statistical correction factor to reduce it by the dispersion and ",
", taking the result as the standard value.",
"How large a coefficient of variation is abnormal?",
"Geotechnical parameters usually have δ of 0.05-0.30; above 0.3 the data are severely dispersed, so the cause (test or soil-layer difference) should be found and, if necessary, statistics done by group.",
'About "Geotechnical (Parameter/Test/Statistics) Analysis"',
"Geotechnical (Parameter/Test/Statistics) Analysis. A free online tool, processed fully client-side, with no data uploaded, protecting your privacy.",
"e.g. T1,12.5",
],
'richter-scale': [
"🌋 Earthquake Magnitude",
"A Richter magnitude and seismic energy comparison: enter the magnitude to compute the released energy and the TNT equivalent.",
'📖 View the "Earthquake Magnitude Guide"',
"M_L = log10(A) + distance correction",
"Richter magnitude M",
"Magnitude and impact comparison",
"Energy formula: log₁₀E = 1.5M + 4.8 (E in joules); 1 tonne TNT ≈ 4.184×10⁹ J. For every +1 in magnitude the energy increases by about 32 times.",
"📚 In-Depth Analysis: Richter Magnitude and Released Energy/TNT Equivalent Conversion",
": given the magnitude, estimate the released seismic-wave energy and the corresponding TNT equivalent",
"Damage comparison: grade by magnitude (micro to great) to intuitively understand the impact and damage level",
"Science teaching: use the energy-magnitude relation to explain why each +1 in magnitude increases the energy about 31.6 times",
"Formula: energy E = 10^(1.5·M + 4.8) joules (J); TNT equivalent (tonnes) = E / 4.184×10⁹ (1 tonne TNT ≈ 4.184×10⁹ J). Each +1 in magnitude multiplies the energy by about 10^1.5≈31.6 (computed locally; the 1-tonne-TNT constant is fixed).",
"Example: M=6.0 → E=10^13.8≈6.31×10¹³ J, TNT equivalent = 6.31×10¹³/4.184×10⁹≈15080 tonnes≈15.08 kilotonnes (about 1.5×10⁴ tonnes TNT); in the comparison table M6 is a strong earthquake with building damage and partial collapse.",
"Does +1 in magnitude really mean about 31.6 times the energy?",
"Yes. Since E∝10^1.5M, ΔM=1 → energy ratio = 10^1.5≈31.6. This is why M7 is far more destructive than M6 — it is not linear.",
"Can the TNT equivalent be equated directly with destructive power?",
"No. Seismic energy spreads as seismic waves, acts over a long time and depends on focal depth/geology; the TNT equivalent is an energy-scale comparison, not equal to the destruction pattern of an equivalent TNT explosion, and is only for intuitively understanding the scale.",
'About "Earthquake Magnitude"',
"Earthquake Magnitude is an online tool in the scientific research field. A scientific research tool that uses standard scientific formulas for accurate calculation.",
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
