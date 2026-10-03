#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'bonding')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'bonding')
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
    out = {'slug': slug, 'industry': 'bonding', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # ---------------- analysis-cost-4 (22) ----------------
    write('analysis-cost-4', build('analysis-cost-4', [
        "⚡ Bonding Process Cost and Efficiency Comparison (Including Alternatives)",
        "Enter the material cost, labor time and yield rate of each bonding option row by row, and convert them to cost per part and effective labor time",
        "Bonding process selection cannot compare only the glue unit price: labor time (dispensing, positioning, curing wait) converted into labor and equipment occupancy often exceeds the material itself, and the yield rate spreads rework losses back onto each part. The formula combines the three into a cost per part (material plus labor cost, then divided by the yield rate), and uses \"effective labor time = labor time ÷ yield rate\" to reflect the extra capacity consumed by rework. The baseline option is the first row, the optimal option is the one with the lowest cost per part, and both the savings rate and the efficiency gain are computed relative to the baseline. Data is calculated only in the local browser and never uploaded.",
        "Cost per part = (glue cost + labor time × labor rate) ÷ yield rate; effective labor time = labor time ÷ yield rate",
        "Enter \"option name, glue cost (CNY/part), labor time (minutes), labor rate (CNY/min), yield rate %\" for each row, e.g.: epoxy,3.5,4,0.5,98",
        "Epoxy,3.5,4,0.5,98\nInstant glue,2.0,2,0.5,95",
        "📚 Deep dive: Bonding Process Cost and Efficiency Comparison",
        "Bonding process selection",
        "Economic comparison of alternative processes (welding / riveting / tape)",
        "Cost reduction and capacity assessment",
        "Cost per part = (glue cost + labor time × labor rate) ÷ yield rate; effective labor time = labor time ÷ yield rate.",
        "Epoxy AB glue 4.0 CNY, 5 minutes, 0.6 CNY/min, yield 96% → per part (4.0+3.0)÷0.96 = 7.29 CNY; hot melt glue 1.8 CNY, 1.5 minutes, 92% → (1.8+0.9)÷0.92 = 2.93 CNY; structural tape 6.0 CNY, 2 minutes, 99% → 7.27 CNY. The best is hot melt glue, saving 59.75% against the baseline, with effective labor time dropping from 5.21 to 1.63 minutes (a 68.70% gain).",
        "Why does the yield rate have to be included?",
        "Reworked parts consume material and labor too, so dividing by the yield rate spreads the rework loss back onto each part and avoids underestimating the true cost of a low-yield option.",
        "What is the savings rate relative to?",
        "It is relative to the first-row option (the baseline): the percentage drop in cost per part is the savings rate. Put the current process in the first row to use it as the comparison baseline.",
        "Free to use, no registration or login required",
        "Supports Simplified / Traditional Chinese / English interface",
        "When selecting an adhesive, use the mean and range of the adhesive cost between batches to judge which is cheaper and less variable",
        "For the same formula across multiple batches, monitor incoming material consistency with the standard deviation of measured unit consumption, with an alert when it goes out of tolerance",
        "Compare the unit connection cost of structural adhesive versus mechanical fastening to support substitution decisions",
        "e.g.: epoxy,3.5,4,0.5,98",
    ]))

    # ---------------- analysis-resolution (38) ----------------
    write('analysis-resolution', build('analysis-resolution', [
        "📊 Bonding (Case Analysis / Failure / Resolution)",
        "Case analysis / failure / resolution",
        "Based on the common causes and troubleshooting paths of bonding failures, enter the operating conditions and failure symptoms to output a list of possible causes and corrective actions, assisting localization and review; pure front-end calculation, data never leaves the browser.",
        "Failure symptom",
        "Adhesive debonding / detachment",
        "Brittle fracture",
        "Interface failure",
        "Bubbles / voids",
        "Whitening / haze",
        "Temperature resistance failure",
        "Incomplete curing",
        "Ageing cracking",
        "Substrate type",
        "Plastic",
        "Operating temperature (°C)",
        "Curing time (min)",
        "Surface treatment",
        "None",
        "Cleaning only",
        "Sanding",
        "Primer treatment",
        "📚 Deep dive: Bonding (Case Analysis / Failure / Resolution)",
        "Bonding failure case review: for a batch of debonding / cracking failure samples, tally them by \"severity score\", using the mean to judge the overall risk level and the distribution to locate high-frequency failure modes.",
        "Before-and-after process improvement comparison: take one set of quality scores before and after improvement, and compare the mean and",
        "to quantify whether the improvement effect is significant.",
        "Supplier quality check: score the bonding appearance / strength spot checks of incoming batches, and use the range and standard deviation to decide whether a batch is abnormal.",
        "Example: severity scores of 10 failure cases (1-5)",
        "Enter the severity scores (1 = minor, 5 = severe) of 10 bonding failure cases: 3, 4, 2, 5, 4, 3, 5, 2, 4, 3. Data size 10; sum 35; mean 3.50;",
        "3.50; minimum 2; maximum 5; range 3; variance 1.05; standard deviation 1.02. Conclusion: the average severity of 3.5 (moderate to high), and the individual cases scoring 5 need focused root cause analysis; the distribution is fairly concentrated (standard deviation 1.02), indicating the failure degree is relatively consistent and probably caused by the same class of process factors.",
        "How many samples are needed to be statistically meaningful?",
        "In engineering practice at least 5 are needed to see an initial trend, and 20~30 allow a fairly stable mean / standard deviation estimate; with too few samples the mean is easily skewed by a single case, so the specific failure mode should be considered rather than only looking at the number.",
        "How do you use this data to guide process changes?",
        "First compute the baseline mean and standard deviation, then collect a comparison set after the improvement: if the mean drops and the standard deviation shrinks, both the severity and the controllability have improved; also watch whether the maximum drops (whether the worst case has converged).",
        "Free to use, no registration or login required",
        "Supports Simplified / Traditional Chinese / English interface",
        "Tally bonding failure cases by severity score and use the mean to locate the overall risk level",
        "Take one set of scores before and after process improvement and compare the mean and standard deviation to quantify the effect",
        "Use the range and standard deviation of incoming batch bonding spot-check scores to decide whether a batch is abnormal",
    ]))

    # ---------------- assessor-cycle-lifespan (20) ----------------
    write('assessor-cycle-lifespan', build('assessor-cycle-lifespan', [
        "😴 Fatigue (Performance / Cycle / Life) Assessment",
        "Performance / cycle / life",
        "Based on the stress-cycle relation of fatigue life (S-N curve and the Miner linear cumulative damage criterion), enter the load spectrum and material parameters to estimate the achievable cycle count and safe life, assisting durability judgement; pure front-end calculation, data never leaves the browser.",
        "📚 Deep dive: Fatigue (Performance / Cycle / Life) Assessment",
        "Fatigue check for adhesive / metal joints: given the material σb, stress amplitude Δσ, mean stress σm,",
        "stress concentration",
        "Kt, estimate the achievable cycle life and safety factor, and judge whether a higher-strength material or lower stress is needed.",
        "Surface treatment selection: polishing / grinding / turning / rough machining correspond to different surface factors β; compare their effect on the fatigue limit and life to choose the best process.",
        "Design life compliance: enter the target design cycle count and use the safety factor sf = N/designN to judge \"safe (sf≥2) / critical (1-2) / unsafe (<1)\".",
        "Example: σb800 / Δσ200 / σm100 / Kt2.0 / design 500,000 cycles / ground β0.8",
        "Input: σb=800 MPa, Δσ=200 MPa, σm=100 MPa, Kt=2.0, design life 500,000 cycles, surface ground β=0.8. Fatigue limit σE = σb×0.5×β/Kt = 800×0.5×0.8/2.0 = 160.0 MPa; Goodman equivalent stress σEq = Δσ/2/(1−σm/σb) = 200/2/(1−100/800) = 114.29 MPa; with the S-N curve (exponent m=5) the achievable life N = (σE/σEq)^5×10⁶ = (160/114.29)^5×10⁶ ≈ 5.378 million cycles; safety factor sf = N/designN = 537.8/50 = 10.76 → safe. By comparison the default (σb600 / Kt2.0 / design 1,000,000) gives σE=120, σEq=120, N=1 million cycles, sf=1.00 → critical, showing that raising the material strength improves life exponentially.",
        "What are the Goodman correction and the S-N curve?",
        "The Goodman line linearly converts the weakening effect of mean stress on fatigue strength into an equivalent stress; the S-N curve describes the power-law relation between stress amplitude and the number of cycles to failure, and this tool takes m=5 (a common approximation for steel and adhesive joints). Together they give an engineering estimate when no experimental curve is available.",
        "Does a safety factor sf=1 mean it is just good enough?",
        "No. sf=1 only means the theoretical life equals the design life, with no margin; engineering practice requires sf≥2 (actual life ≥2× the design life) to count as reliable. sf between 1 and 2 is \"critical\" and needs optimization (lower stress / change material / reduce Kt), and <1 is \"unsafe\" and requires a design change.",
        "Free to use, no registration or login required",
        "Supports Simplified / Traditional Chinese / English interface",
        "Enter material parameters for an adhesive / metal joint to estimate the achievable cycle life and safety factor",
        "Compare the effect of different surface factors for polishing / grinding / turning / rough machining on fatigue life",
        "Enter the target design cycle count to judge safe (sf≥2) / critical / unsafe",
    ]))


if __name__ == '__main__':
    main()
