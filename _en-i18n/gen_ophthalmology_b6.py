#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ophthalmology 第6批（收尾）：iol-power / self-assess-2 / tear-breakup-time / ishihara-test / calc-1 / convert-42"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'ophthalmology')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'ophthalmology')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        for i, it in enumerate(items):
            print('   ', i, repr((it.get('zh') or it.get('zh_src', ''))[:50]))
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
    out = {'slug': slug, 'industry': 'ophthalmology', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))


# ---------------- iol-power (31) ----------------
write('iol-power', build('iol-power', [
    "\U0001F441\uFE0F Intraocular Lens (IOL) Power (SRK-T) Calculator",
    "Enter axial length (AL), corneal curvature (K) and IOL A constant, compute IOL power and support target refraction reserve.",
    "/ Intraocular Lens (IOL) Power Calculator",
    '\U0001F4D6 View the "Intraocular Lens (IOL) Power (SRK-T) Calculator User Guide"',
    "SRK II: P = A' - 0.9K - 2.5L (A' segment-corrected by axial length); SRK/T: P = 1336/(AL - ELP) - 1336/(1336/K - ELP), ELP = pACD + H, pACD = 0.62467A - 68.747, R = 337.5/K, H = R - sqrt(R\u00b2 - (Cw/2)\u00b2)",
    "SRK II is a linear regression; SRK/T uses the vergence formula corrected by ELP (effective lens position). Target refraction reserve is back-solved by vergence: P = 1336/(AL - ELP) - 1336/(1336/K - ELP) - target refraction. Each 1 mm axial error affects ~2.5 D.",
    "Axial length AL (mm)",
    "Mean corneal curvature K (D)",
    "A constant",
    "Target refraction:",
    "Emmetropia 0D",
    "\U0001F4D0 Intermediate Parameters and Formula",
    "P = A1 - 0.9\u00b7K - 2.5\u00b7AL, A1 adjusted by AL (AL<20:+3, <21:+2, <22:+1, <24.5:0, <26:-1, >=26:-2).",
    "SRK/T (estimate)",
    "\u26A0\uFE0F IOL power is affected by biometry precision, post-op refractive state, etc. SRK/T estimate may differ \u00b11D from instrument reports; final power must be set by the surgeon clinically.",
    'About "IOL Power Calculator"',
    "Estimates IOL power from SRK II and SRK/T formulas, supports target refraction reserve, for pre-cataract power rehearsal and teaching.",
    "\U0001F4DA Deep Dive: Intraocular Lens Power (SRK-II / SRK/T)",
    "SRK-T uses effective lens position ELP: P = 1336/(AL-ELP) - 1336/(1336/K-ELP).",
    "SRK-II empirical formula for comparison.",
    "Post-cataract target refraction planning.",
    "Long axial length",
    "If AL=26, ELP and denominator changes lower P to about 16-17D; longer axis needs lower power.",
    "What is 1336?",
    "Aqueous/vitreous",
    "refractive index",
    "~1.336, so 1336 mm is used as the intraocular medium refractive-index constant.",
    "Why is SRK/T more accurate?",
    "It obtains ELP by regression rather than empirical correction, more reliable for extreme axial lengths.",
    'About "Intraocular Lens (IOL) Power (SRK-T) Calculator"',
    "Intraocular lens power calculator: from axial length (AL), corneal curvature (K) and A constant, uses SRK II and SRK/T to estimate IOL power and target refraction reserve. A medical professional tool based on authoritative standards, for reference only.",
]))

# ---------------- self-assess-2 (31) ----------------
write('self-assess-2', build('self-assess-2', [
    "\U0001F4CB Dry Eye (OSDI) Self-Assessment Scale",
    "OSDI dry-eye self-assessment scale (12 items, 3 dimensions, each 0-4, OSDI index = total x 25/48)",
    '\U0001F4D6 View the "Dry Eye (OSDI) Self-Assessment Scale User Guide"',
    "OSDI dry-eye index = sum of item scores (\u03a3 12 items, each 0-4) x 25 \u00f7 48 x 100, max 100; <=12 normal, 13-22 mild, 23-32 moderate, >32 severe; split into A(1-5)/B(6-9)/C(10-12) segments.",
    "1. Photophobia",
    "2. Foreign-body sensation",
    "3. Eye pain or soreness",
    "4. Blurred vision",
    "5. Poor/fluctuating vision",
    "6. Reading (due to eye discomfort)",
    "7. Driving/night driving",
    "8. Using computer/phone",
    "9. Watching TV",
    "10. In wind/AC environment",
    "11. In dry environment",
    "12. In smoky/dusty environment",
    "Calculate OSDI",
    "\U0001F4DA Deep Dive: Dry-Eye Self-Assessment (OSDI Brief)",
    "12 self-rated items, OSDI = total x25/48 (\u2248 x0.521, 0-100).",
    "Quick dry-eye risk self-assessment.",
    "Compare with standard OSDI.",
    "12 items total 24",
    "OSDI = 24 x 25/48 = 12.5, mild dry eye; if total 48 then full 100 is severe.",
    "Total 12",
    "OSDI = 12x25/48 = 6.25, essentially normal.",
    "Consistent with the osdi-scale formula?",
    "Essentially the same (normalized to 0-100 by answered items); this brief fixes 12 items, coefficient 25/48 approximates the standard normalization.",
    "Can a high self-score replace a visit?",
    "No, only a screening hint; confirmation needs slit-lamp and tear tests.",
    'About "Dry Eye (OSDI) Self-Assessment Scale"',
    "Dry eye (OSDI) self-assessment scale. Free online tool, pure front-end processing, data not uploaded, privacy-safe.",
]))

# ---------------- tear-breakup-time (31) ----------------
write('tear-breakup-time', build('tear-breakup-time', [
    "\U0001F4CB Tear Film Break-Up Time (BUT) Standard Assessor",
    "Enter tear film break-up time (BUT, seconds), assess tear-film stability by Asian dry-eye consensus and Chinese dry-eye guideline.",
    "/ Tear Film Break-Up Time (BUT) Assessor",
    '\U0001F4D6 View the "Tear Film Break-Up Time (BUT) Standard Assessor User Guide"',
    "Tear film break-up time BUT/TBUT (seconds) grading: >=10 normal, 5-10 unstable tear film (mild-moderate dry eye), <5 clearly abnormal (moderate-severe dry eye); lower value means less stable film.",
    "First break-up BUT (seconds)",
    "Average break-up TBUT (seconds, optional)",
    "\U0001F4CB Grading standard",
    "BUT (seconds)",
    "Tear-film stability",
    "Tear film stable",
    "Tear film unstable",
    "Suggests dry eye (mild-moderate)",
    "Clearly abnormal",
    "Moderate-severe dry eye",
    "Chinese dry-eye consensus: BUT<10s is unstable tear film; <5s suggests severely unstable film. Often combined with Schirmer test and corneal fluorescein staining.",
    "\u26A0\uFE0F BUT is affected by environment, blinking and operation; take 3 averages. Results for reference only; dry-eye diagnosis needs symptoms and multiple exams.",
    'About "BUT Assessor"',
    "Grades tear-film stability by break-up time, aiding dry-eye screening and follow-up.",
    "\U0001F4DA Deep Dive: Tear Film Break-Up Time (BUT/TBUT)",
    "After fluorescein, record first black-spot time (seconds), pct = value/20x100.",
    "Dry-eye diagnosis (<10s abnormal, <5s marked).",
    "Multiple measurements, take average.",
    "pct = 8/20x100 = 40%; borderline (5-10s), with symptoms consider evaporative dry eye.",
    "Markedly shortened (<5s), very unstable film, typical dry-eye presentation.",
    "What is normal BUT?",
    "Generally >10s normal, 5-10s borderline, <5s clearly abnormal.",
    "Relation with OSDI?",
    "BUT is objective, OSDI subjective; combining both diagnoses dry eye.",
    'About "Tear Film Break-Up Time (BUT) Standard Assessor"',
    "Tear film break-up time (BUT/TBUT) assessor: enters break-up time in seconds, grades by dry-eye standard and interprets tear-film stability. A medical professional tool based on authoritative standards, for reference only.",
]))

# ---------------- ishihara-test (28) ----------------
write('ishihara-test', build('ishihara-test', [
    "\U0001F4DD Color Vision (Ishihara) Pseudoisochromatic Plate Tester",
    "Observe the number in each pseudoisochromatic plate and choose the answer. Normal color vision reads all numbers; red-green deficiency misreads or cannot read them. This tool is a screening version, not diagnostic.",
    "/ Color Vision (Ishihara) Tester",
    '\U0001F4D6 View the "Color Vision (Ishihara) Pseudoisochromatic Plate Tester User Guide"',
    "\u2705 Scoring",
    "\U0001F4CB Score Interpretation",
    "Correct count (of 6 plates)",
    "Normal color vision (screening level)",
    "Borderline, suggest recheck or formal exam",
    "Suggests red-green deficiency",
    "Display color and ambient light affect results. Confirmation needs standard Ishihara 38-plate or anomaloscope exam.",
    "\u26A0\uFE0F This test is for education/screening, cannot replace professional color-vision exam. For occupational exams use the medical institution's standard test.",
    'About "Color Vision Tester"',
    "Generate red-green-confusion pseudoisochromatic plates with Canvas for color-vision screening and scoring, suitable for teaching and first screening.",
    "\U0001F4DA Deep Dive: Ishihara Color-Vision Test",
    "Read pseudoisochromatic-plate numbers; interpret color vision by correct plate count.",
    "Red-green color blindness screening.",
    "Recheck advice for borderline values.",
    "Correct 11/12",
    "High accuracy, basically normal; only 1 error may be accidental.",
    "Correct 3/12",
    "Many misreads, strongly suggests red-green defect, recommend further specialized color-vision exam.",
    "From what age?",
    "Generally age 4-5+ who can recognize numbers; young children use the picture version.",
    "All wrong must be color blindness?",
    "Could also be non-cooperation/cannot count; confirm with other exams.",
    'About "Color Vision (Ishihara) Pseudoisochromatic Plate Tester"',
    "Color-vision Ishihara pseudoisochromatic online tester: screens red-green deficiency with pseudoisochromatic plates, auto-scores and interprets results. A medical professional tool based on authoritative standards, for reference only.",
]))

# ---------------- calc-1 (21) ----------------
write('calc-1', build('calc-1', [
    "\U0001F441\uFE0F IOP Correction (Corneal Thickness Correction)",
    "Estimate-correct measured IOP by central corneal thickness (CCT), aiding glaucoma risk assessment.",
    "IOP correction",
    "/ IOP correction",
    '\U0001F4D6 View the "IOP Correction (Corneal Thickness Correction) User Guide"',
    "Corrected IOP (linear method) = measured IOP - (CCT - 544) / 10 x 0.7 mmHg; standard corneal thickness is 544 \u00b5m, each 10 \u00b5m deviation corrects ~0.7 mmHg, thick cornea measured high needs lowering, thin cornea measured low needs raising.",
    "Measured IOP (mmHg)",
    "Central corneal thickness CCT (\u00b5m)",
    "Calculate corrected IOP",
    "\U0001F4DA Deep Dive: IOP Correction (Central Corneal Thickness)",
    "Correct Goldmann IOP by central corneal thickness CCT: corrected = IOP - ((CCT-544)/10)x0.7.",
    "Correction for thick-cornea overestimation and thin-cornea underestimation.",
    "Avoid misjudgment in glaucoma screening.",
    "Corrected = 18 - ((560-544)/10)x0.7 = 18 - 1.6x0.7 = 18 - 1.12 = 16.88 mmHg (thick cornea measured high, lower after correction).",
    "Corrected = 18 - ((500-544)/10)x0.7 = 18 + 3.08 = 21.08 mmHg (thin cornea measured low, raise after correction).",
    "Why baseline 544 \u00b5m?",
    "544 \u00b5m is about the population mean CCT; Goldmann IOP is calibrated at that thickness.",
    "Is one correction enough?",
    "This formula is a simplified approximation; the iop-correction tool also gives Ehlers/Doughty/Feltgen multi-formula mean.",
    "Example 18",
    "Example 540",
]))

# ---------------- convert-42 (17) ----------------
write('convert-42', build('convert-42', [
    "\U0001F441\uFE0F Visual Acuity Chart (Snellen/logMAR) Conversion",
    "Visual acuity decimal / logMAR / Snellen (20/x) mutual conversion",
    '\U0001F4D6 View the "Visual Acuity Chart (Snellen/logMAR) Conversion User Guide"',
    "Acuity conversion: decimal acuity dec and logMAR satisfy logMAR = -log10(dec); Snellen denominator = 20 / dec; 5-point record = 5 - logMAR = 5 + log10(dec); visual angle (arcmin) = 1 / dec, 1.0 acuity corresponds to 1 arcmin.",
    "Snellen denominator x",
    "\U0001F4DA Deep Dive: Visual Acuity Notation Conversion (Snellen/logMAR)",
    "Snellen (20/20, 6/6) \u2194 logMAR \u2194 decimal acuity mutual conversion.",
    "Unify notation when making or reading charts.",
    "ETDRS row-number conversion.",
    "Decimal = 20/40 = 0.5; logMAR = -log10(0.5) ~ 0.301; 5-point record ~ 4.70; ETDRS row ~ (1.10-0.301)/0.02 ~ 40.",
    'Decimal 1.0, 5-point record 5.0, ETDRS row 55, all notations consistently mean "normal vision".',
    "logMAR vs decimal relation?",
    "Decimal = 10^(-logMAR); each 0.1 logMAR increase means ~one line worse (1.26x).",
    "How to unify different denominators (20/6/5)?",
    "All first convert to decimal (denominator / numerator reciprocal), then to logMAR, so notations are interchangeable.",
    'About "Visual Acuity Chart (Snellen/logMAR) Conversion"',
    "Visual acuity chart (Snellen/logMAR) conversion. Free online tool, pure front-end processing, data not uploaded, privacy-safe.",
]))
