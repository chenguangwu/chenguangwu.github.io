#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'textile')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'textile')
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
    out = {'slug': slug, 'industry': 'textile', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # thread-count (19)
    write('thread-count', build('thread-count', [
        "🔄 Yarn Count & Density Conversion",
        "English count / metric count / denier / needle count / weight",
        "Core formulas (by input variables): Math.round((w + f) × width ÷ 10); Math.round(w × width ÷ 10); Math.round(f × width ÷ 10)",
        " / Yarn Count & Density",
        "📖 View 'Yarn Count & Density Conversion User Guide'",
        "📚 In-depth: Yarn Count & Density (Warp/Weft) Conversion",
        "Compute fabric total density from warp/weft density and width",
        "Link yarn tex and density to estimate GSM and hand feel",
        "Check if sample density matches the production order",
        "Total density",
        "Warp 130 ends/10cm, weft 70 picks/10cm → total 200 /10cm; at 150 cm width warp total = 150/10 × 130 = 1950 ends.",
        "Yarn linkage",
        "Warp 30 tex, weft 25 tex, with warp/weft density can estimate GSM; at same density smaller tex means lighter/softer cloth.",
        "Why do warp and weft densities differ?",
        "Weave structure and end-use decide; e.g. poplin warp density far exceeds weft; affects hand feel and strength direction.",
        "How to read density and yarn count together?",
        "High density + fine count = fine thin fabric; low density + coarse count = heavy coarse cloth.",
        "About 'Yarn Count & Density Conversion'",
        "Yarn count & density conversion. A textile tool that helps calculate fabric parameters and usage.",
    ]))

    # yarn-count (40)
    write('yarn-count', build('yarn-count', [
        "🧵 Yarn Count Conversion",
        "Convert among English count (Ne), metric count (Nm), denier (D), tex and dtex",
        "📖 View 'Yarn Count Conversion User Guide'",
        "Input system",
        "Decitex dtex",
        "Denier D",
        "English count Ne (cotton)",
        "📐 Conversion Formula (tex as base)",
        "Note: larger value means coarser yarn for fixed-length systems (tex/D); finer yarn for fixed-weight systems (Ne/Nm).",
        "📋 Common Yarn Fineness Reference",
        "Yarn type",
        "Coarse count yarn",
        "Denim, coarse cloth",
        "Medium count yarn",
        "Plain cloth, bed linen",
        "Fine count yarn",
        "Shirts, underwear",
        "Extra-fine count yarn",
        "High-end fabric",
        "📚 In-depth: Yarn Count Conversion",
        "Unify specs by converting yarn count units (Ne/Nm/tex/denier)",
        "Quickly align when suppliers quote different units",
        "Convert blended or plied yarn counts",
        "Multi-unit conversion",
        "30 English count → tex 590.5/30≈19.7, metric 1000/19.7≈50.8, denier 19.7×9≈177; i.e. 30Ne≈19.7tex≈50.8Nm≈177D.",
        "Plied yarn",
        "Two-ply 30Ne singles → about 15Ne (count halved, coarser); tex from 19.7 to about 39.4.",
        "How to compute plied count?",
        "Same-count ply roughly halves count (tex doubles); different counts average by weight.",
        "Is tex inverse to count?",
        "Yes, smaller tex means finer, larger count means finer; they are inversely related.",
        "About 'Yarn Count Conversion'",
        "Yarn count conversion tool supports five fineness units — Ne, Nm, D, tex, dtex — with a common fineness reference table.",
        "One-click convert among five systems",
        "Auto judge yarn coarseness",
        "Common yarn reference table",
        "Yarn fineness conversion",
        "Fabric spec comparison",
        "Textile process design",
        "Raw material procurement comparison",
    ]))

    # zuranyangzhishu-loi (36)
    write('zuranyangzhishu-loi', build('zuranyangzhishu-loi', [
        "📋 Limiting Oxygen Index (LOI)",
        "Enter material type and LOI value to judge flame-retardant grade and application",
        "Limiting Oxygen Index",
        " / Limiting Oxygen Index",
        "📖 View 'Limiting Oxygen Index (LOI) User Guide'",
        "LOI = limiting oxygen index, the minimum oxygen concentration to sustain combustion; air oxygen ~21%, materials with LOI > 21 self-extinguish in air",
        "Aramid",
        "Modacrylic",
        "Flame-retardant treated fabric",
        "LOI (%)",
        "💡 LOI ≥28 excellent retardancy; higher LOI is harder to burn, air oxygen ~21%",
        "LOI = limiting oxygen index, the minimum oxygen concentration to sustain combustion",
        "Air oxygen ~21%, materials with LOI > 21 self-extinguish in air",
        "📚 In-depth: Limiting Oxygen Index (LOI)",
        "Grade fabric flammability by LOI",
        "Compare LOI when selecting FR garment fabrics",
        "Verify LOI improvement before/after FR finishing",
        "LOI Grading",
        "LOI 32% → ≥28% flame-retardant (self-extinguish off flame, for protective/decorative); LOI 24% combustible (20–28); LOI 18% <20% flammable.",
        "Finishing improvement",
        "Raw cotton LOI≈18% (flammable), after FR finishing LOI rises to 28–32% (retardant), self-extinguishes off flame.",
        "What is LOI?",
        "Limiting oxygen index, minimum oxygen % to sustain combustion; higher means harder to burn, air oxygen ~21%.",
        "Is LOI≥28 always safe?",
        "Only means hard to sustain burning; also check heat protection, melt dripping and toxic smoke; FR garments need comprehensive metrics.",
        "About 'Limiting Oxygen Index'",
        "Limiting Oxygen Index (LOI) is a core metric for textile flame retardancy. Based on material type and LOI value, this tool grades retardancy (flammable/combustible/hard-to-burn/retardant), judges self-extinguish in air, and compares with reference values, supporting FR fabric selection and quality assessment.",
        "Supports 7 materials including cotton, polyester, aramid",
        "Automatic LOI retardancy grading",
        "Air self-extinguish ability judgment",
        "Comparison analysis with reference LOI values",
        "FR fabric selection and procurement",
        "Protective garment FR performance evaluation",
        "Decorative fabric fire-compliance check",
        "FR finishing effect verification",
        "LOI (oxygen index)",
    ]))

    # dyeing-time (49)
    write('dyeing-time', build('dyeing-time', [
        "🧵 Dyeing Time Calculator",
        "Calculate dyeing heating time, holding time and heating rate",
        "Performs professional calculation and outputs results based on input parameters for 'calculate dyeing heating time, holding time and heating rate'.",
        "Dyeing Time Calculator",
        " / Dyeing Time Calculation",
        "📖 View 'dyeing-time User Guide'",
        "🧮 Time Calculation",
        "📈 Heating Rate",
        "Start temperature (°C)",
        "Heating rate (°C/min)",
        "Holding time (min)",
        "Multi-stage heating process (optional)",
        "+ Add heating stage",
        "Required heating time (min)",
        "🔢 Time Formula",
        "Heating time",
        "= (target temp − start temp) ÷ heating rate",
        "Total dyeing time",
        "= heating time + holding time",
        "Heating rate",
        "= (target temp − start temp) ÷ heating time",
        "📊 Common Dyeing Process Reference",
        "Heating rate (°C/min)",
        "Dyeing temperature (°C)",
        "Holding (min)",
        "Disperse dye (high temp)",
        "Disperse dye (carrier)",
        "⚠️ Process Notes",
        "Too fast heating may cause poor leveling and shade bars",
        "Too slow heating hurts efficiency and raises energy use",
        "Holding time directly affects dye uptake and fixation",
        "Multi-stage heating optimizes leveling: slow at low temp, faster at high temp",
        "Actual process needs integrated adjustment by equipment, dye and fabric type",
        "Multi-stage heating is closer to real dyeing. After adding stages the system computes per-stage time and sums total.",
        "📚 In-depth: Dyeing Time Calculator",
        "Exhaust dyeing scheduling: estimate per-batch total dyeing time from start/target temp, heating rate and holding, for batch planning and delivery.",
        "Multi-stage heating: set each stage target temp and holding (e.g. 20→40→60°C), accumulate to total dyeing time.",
        "Heating rate back-calc: given target temp and time limit, derive the minimum heating rate needed.",
        "Single-stage example",
        "Start 20°C, target 60°C, rate 2°C/min, hold 30min → heating=(60−20)/2=20min, total=20+30=50min (~0.83h). If 40min to heat 20→100°C then hold 30min, rate=(100−20)/40=2.00°C/min, total 70min (~1.17h).",
        "What heating rate is typical?",
        "Typically 1–2°C/min; thick fabric, shade-bar-prone or cationic dye on acrylic use below 1°C/min slow rise. Follow dye/equipment process card; too fast causes bars, too slow hurts output.",
        "How to set holding time?",
        "Reactive 30–45min, disperse 30–45min, acid/direct 45–60min; balance leveling and uptake. Too short lowers uptake, too long may damage fiber or hand feel.",
        "About 'Dyeing Time Calculator'",
        "Dyeing Time Calculator — dyeing holding time and heating rate calculation, an online textile dyeing process tool, free to use. A business/office tool to boost efficiency, with local data processing for privacy.",
        "Estimate per-batch dyeing total time by schedule, check delivery and machine occupancy.",
        "Build multi-stage heating curves, enter holding and heating params per shade.",
        "Recheck heating rate meets time limits, avoiding rushed shade bars.",
    ]))

    # hardness-5 (42)
    write('hardness-5', build('hardness-5', [
        "🔢 Interlining Stiffness & Fusing",
        "Enter interlining weight, fusing temp, pressure and time to assess fusing effect and hand stiffness",
        "Core formulas (by input variables): (tempScore×0.4+pressureScore×0.3+timeScore×0.3); max(0,40-|(pressure-32)|×1.2); max(0,40-|(durtime-15)|×1.5)",
        "📖 View 'Interlining Stiffness & Fusing User Guide'",
        "Interlining weight (g/m²)",
        "Fusing temperature (℃)",
        "Fusing pressure (kPa)",
        "Fusing time (s)",
        "Interlining type",
        "Woven interlining",
        "Non-woven interlining",
        "Knit interlining",
        "💡 Fusing score weighs whether temp, pressure and time fall within the interlining hot-melt adhesive's optimal process window",
        "Common PA adhesive fusing 130–160℃, PES 150–170℃",
        "Higher weight feels stiffer, lower weight softer but less support",
        "📚 In-depth: Fabric Stiffness (Hand Feel) Assessment",
        "Score stiffness by weight, pressure and dwell time, grade hand feel",
        "Compare stiffness before/after stiffening finish",
        "Choose soft/stiff baseline by end use",
        "Stiffness score",
        "Sample 200 g/m², weight 10 g, dwell 30 s, little drape rebound → score 88 (good); after stiffening 92 (excellent).",
        "Grade application",
        "Score ≥85 excellent (crisp, for suit interlining), 70–84 good (regular wear), <70 soft (for underwear/skirt).",
        "What instrument measures stiffness?",
        "Commonly inclined-drape or heart-loop method for bending length/recovery angle; this tool gives a composite score from inputs.",
        "Is higher weight always stiffer?",
        "Generally yes, but weave and finish matter more; same weight plain weave is crisper than satin.",
        "About 'Interlining Stiffness & Fusing'",
        "Interlining stiffness & fusing effect assessment is key to garment interlining process. Based on weight, fusing temp, pressure and time, this tool scores fusing effect, judges hand stiffness and gives process adjustment suggestions to optimize fusing quality.",
        "Three-dimensional scoring model of temp, pressure, time",
        "Automatic hand stiffness judgment (soft/moderate/stiff/crisp)",
        "Supports woven, non-woven and knit interlining types",
        "Gives adjustment suggestions when process params deviate",
        "Fusing machine process setting",
        "Interlining selection and hand match",
        "Fusing quality troubleshooting",
        "New fabric fusing trial",
        "Interlining weight",
        "Fusing temperature",
        "Fusing pressure",
        "Fusing time",
        "Interlining type",
    ]))

if __name__ == "__main__":
    main()
