#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'endocrinology')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'endocrinology')
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
    out = {'slug': slug, 'industry': 'endocrinology', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
#!/usr/bin/env python3

def main():
    write('whipple-triad', build('whipple-triad', [
        "\u2697\uFE0F Hypoglycaemia (Whipple's Triad) Verifier",
        "Verify Whipple's triad to confirm true hypoglycaemia and guide the differential diagnosis of causes such as insulinoma",
        "\U0001F4D6 See the \"Hypoglycaemia (Whipple's Triad) Verifier User Guide\"",
        "Whipple's triad verification",
        "1. Glucose during the episode (mmol/L)",
        "Sampling state",
        "Fasting / spontaneous episode",
        "Post-meal / reactive",
        "Hypoglycaemia symptoms during the episode",
        "Hypoglycaemia symptoms present (palpitations, sweating, tremor, hunger, altered consciousness, etc.)",
        "Glucose falls during the episode",
        "Currently entered glucose:",
        "Diagnostic criteria: under 2.8 mmol/L in non-diabetics; under 3.9 mmol/L in diabetics (or under 3.0 with symptoms)",
        "Symptoms ease after glucose is raised",
        "Symptoms ease or disappear after glucose is raised",
        "Verify the triad",
        "Insulinoma example",
        "Reactive hypoglycaemia",
        "Differential diagnosis of hypoglycaemia",
        "Key investigation",
        "Insulinoma",
        "Fasting hypoglycaemia with hyperinsulinaemia",
        "72h fast test, insulin/C-peptide, imaging localisation",
        "Drug-induced",
        "History of hypoglycaemic drugs or insulin",
        "Drug history, drug screen",
        "Low cortisol",
        "Cortisol, ACTH",
        "2-4h after a meal, Whipple incomplete",
        "Extended OGTT",
        "Hepatic",
        "Liver disease with hypoglycaemia",
        "Liver function, hepatic glycogen",
        "Insulin autoimmune syndrome",
        "IAA positive, high after meals and low when fasting",
        "Insulin antibody IAA",
        "Clinical value of Whipple's triad:",
        "A complete triad is required to confirm true hypoglycaemia and is the prerequisite for diagnosing organic causes such as insulinoma. If the triad is incomplete (especially without clear hypoglycaemia symptoms plus relief after glucose), watch for pseudo-hypoglycaemia, where stress or anxiety produces similar symptoms.",
        "\U0001F4DA In-depth analysis: Hypoglycaemia (Whipple's Triad) Verifier",
        "Cause screening for hypoglycaemia occurring while fasting or after exercise.",
        "Preliminary judgement of suspected insulinoma (symptoms plus biochemistry plus relief).",
        "Differentiating spontaneous hypoglycaemia in non-diabetics (drug-induced versus organic).",
        "Whipple's triad example",
        "Morning confusion with glucose 2.2 mmol/L during the episode and rapid relief after eating: the triad is met, indicating insulin-mediated hypoglycaemia (insulinoma possible), and a 72-hour fast test with insulin and C-peptide measurement should confirm it.",
        "Must the glucose cut-off be 2.8?",
        "The classic cut-off is 2.8 mmol/L (some guidelines use 3.0), but what matters is that symptoms and low glucose occur together and resolve after glucose is given; older adults and diabetics need individual thresholds.",
        "How is insulinoma confirmed?",
        "On the 72-hour fast test, inappropriately high insulin during hypoglycaemia (insulin/glucose ratio over 0.3, unsuppressed C-peptide) points to insulinoma, which is then localised with contrast CT/MRI or an octreotide scan.",
        "About \"Hypoglycaemia (Whipple's Triad) Verification\"",
        "Whipple's triad is the classic standard for confirming true hypoglycaemia, comprising hypoglycaemia symptoms, low glucose and relief after glucose, and is the prerequisite for diagnosing organic hypoglycaemia such as insulinoma.",
        "Interactive verification of each part of the triad",
        "Fasting versus post-meal differentiation",
        "Insulinoma high-risk alerts",
        "Differential diagnosis table",
        "Confirmation of true hypoglycaemia",
        "Insulinoma screening",
        "Reactive hypoglycaemia differentiation",
    ]))

    write('catecholamine-test', build('catecholamine-test', [
        "\U0001F50D Catecholamine (Metabolite) Assay Assessor",
        "Enter 24-hour urinary or plasma catecholamines and their metabolites to assess the risk of phaeochromocytoma / paraganglioma (PPGL)",
        "Core formulas (by input): nmn \u00F7 0.90; mn \u00F7 0.50",
        "\U0001F4D6 See the \"Catecholamine (Metabolite) Assay Assessor User Guide\"",
        "Sample type",
        "Plasma free metanephrines (PMN)",
        "24h urinary metanephrines",
        "24h urinary catecholamines",
        "Any paroxysmal episodes?",
        "Phaeochromocytoma example",
        "Biochemical reference ranges and thresholds",
        "Sample",
        "Plasma free MN",
        "Plasma",
        "Over 2x upper limit \u2192 PPGL highly likely",
        "Plasma free NMN",
        "Urinary metanephrine (MN)",
        "24h urine",
        "Raised \u2192 imaging needed",
        "Urinary normetanephrine (NMN)",
        "Urinary noradrenaline (NE)",
        "Markedly raised \u2192 PPGL",
        "Urinary adrenaline (E)",
        "Raised \u2192 adrenal PPGL",
        "Urinary dopamine (DA)",
        "Metastatic / head and neck PGL",
        "PPGL diagnostic pathway",
        "1. Clinical clues",
        ": paroxysmal hypertension (triad: headache, palpitations and sweating), orthostatic hypotension, hypertensive crisis, dramatic intraoperative blood pressure swings",
        "2. Biochemical screening",
        "(first choice): plasma free PMN/NMN (sensitivity 96%, specificity 85%) or 24h urinary MN/NMN",
        "3. Imaging localisation",
        ": CT/MRI for anatomical localisation, MIBG scintigraphy or \u2076\u2078Ga-DOTATATE PET for functional localisation",
        "4. Genetic testing",
        ": about 30-40% are hereditary, so SDHA/B/C/D/AF2 and other gene screening is recommended",
        "5. Preoperative preparation",
        ": alpha-blockade (phenoxybenzamine) for over 2 weeks with adequate volume expansion, then add a beta-blocker",
        "Interference reminders:",
        "Avoid testing during acute stress, heart failure or stroke. Stop interfering drugs: tricyclic antidepressants, sympathomimetic cold remedies, labetalol, alpha-methyldopa; caffeine and alcohol can also cause false positives. Stop for at least 48-72 hours. Rest supine for 20-30 minutes before the draw (supine sampling).",
        "\U0001F4DA In-depth analysis: Catecholamine (Metabolite) Assay Assessor",
        "Screening for the paroxysmal triad of headache, palpitations and sweating with hypertension.",
        "Functional assessment of an adrenal incidentaloma.",
        "Recurrence monitoring after surgery or in hereditary syndromes.",
        "Catecholamine reading example",
        "24-hour urinary metanephrine (MN) and normetanephrine (NMN) raised about 3-fold with paroxysmal blood pressure spikes makes phaeochromocytoma highly likely, and contrast imaging of the adrenals and pelvis plus genetic testing (such as MEN2/SDHx) should follow.",
        "Which is better, fractionated blood or urine?",
        "Fractionated plasma (MN/NMN) is more sensitive while 24-hour urine fractionation is more specific; combining both is safest, and interfering drugs must be stopped and urine collection done correctly beforehand.",
        "Which drugs affect the result?",
        "Tricyclic antidepressants, sympathomimetics, labetalol, paracetamol and similar drugs interfere; stop them as advised before collecting the sample and avoid bananas, chocolate and vanilla.",
        "About \"Catecholamine (Metabolite) Assay Assessment\"",
        "Catecholamines and their metabolites (metanephrines) are the first-choice biochemical diagnostic markers for phaeochromocytoma and paraganglioma (PPGL).",
        "Multiple plasma and 24h urine markers",
        "Automatic fold-rise calculation",
        "PPGL risk stratification",
        "Interference factor reminders",
        "Phaeochromocytoma screening",
        "Paroxysmal hypertension assessment",
        "Adrenal incidentaloma follow-up",
        "Preoperative hypertensive crisis prevention",
    ]))

    write('index', build('index', [
        "\U0001F9EC Endocrinology Tools",
        "Endocrinology",
        "Endocrinology Tools",
        "Enter continuous glucose monitoring (CGM) data to compute the mean amplitude of glycaemic excursions (MAGE) and assess glycaemic variability quality",
        "Compute HOMA-IR (the steady-state model of insulin resistance) and HOMA-\u03B2 to assess insulin sensitivity and beta-cell function",
        "Compute the aldosterone/renin ratio (ARR) to screen for primary aldosteronism and guide the confirmatory test",
        "Verify Whipple's triad to confirm true hypoglycaemia and guide the differential diagnosis of causes such as insulinoma",
        "Enter the six sex hormone results with the cycle phase to interpret hypothalamic-pituitary-gonadal axis function",
        "Enter the GH peak at each time point of different stimulation drugs to assess growth hormone deficiency (GHD) diagnosis",
        "Based on the ATA dynamic risk stratification system, assess recurrence risk and follow-up strategy after surgery for differentiated thyroid cancer (DTC)",
        "Genetic target height calculation plus height SDS assessment, bone-age height prediction and GHD risk stratification",
        "Enter calcium and PTH levels together with phosphate and vitamin D to read the parathyroid feedback axis and its causes",
        "Classify pituitary tumours by maximum diameter (micro, macro, giant adenoma) and secretory function (prolactin, ACTH and so on), with management advice and follow-up strategy, as a reference for endocrinology (not a diagnosis).",
        "Enter the six sex hormone values (LH, FSH, E2, T and so on) with the cycle day to match follicular or luteal reference ranges automatically with interpretation notes, supporting fertility and ovarian function assessment.",
        "Enter serum cortisol at several time points such as morning and afternoon to assess whether the diurnal secretion rhythm shows the normal falling curve, supporting first-line screening for Cushing syndrome and other endocrine disorders.",
        "Enter the TRAb (thyroid-stimulating hormone receptor antibody) result to assess Graves disease diagnosis, activity and relapse risk after stopping treatment",
        "Based on the NCEP ATP III criteria (Chinese revision), meeting 3 of 5 items diagnoses metabolic syndrome",
        "Enter 24h urinary or plasma catecholamines and their metabolites to assess the risk of phaeochromocytoma / paraganglioma (PPGL)",
        "Based on the ACR TI-RADS (2017) criteria, score the ultrasound features to stratify thyroid nodule risk and give management advice",
        "Assess the glycated albumin (GA) level, which reflects average glucose over the past 2-3 weeks, and analyse glycaemic control quality against HbA1c",
        "Enter the blood glucose at each time point of an oral glucose tolerance test (OGTT) and get an automatic reading of diabetes or impaired glucose tolerance",
        "Based on a basal-bolus regimen, calculate insulin dose adjustment advice from blood glucose monitoring data",
        "Enter 24-hour urine VMA and HVA plus blood catecholamine results and judge their clinical meaning against the reference ranges",
        "Assess PCOS from the Rotterdam criteria (2 of 3 required), with phenotype classification and metabolic risk stratification",
        "Estimate 10-year major osteoporotic and hip fracture probability from the FRAX model to support treatment decisions",
        "About \"Endocrinology Tools\"",
        "This collection holds 22 free online tools covering the common calculations, conversions and lookups of endocrinology work. Whether you are a practitioner, a student or an everyday user, you will find ready-to-use utilities here. Everything runs in the browser, uploads nothing to a server and keeps your privacy safe.",
        "The endocrinology tools collected on this page include (a few representative tools):",
        "These tools help you finish common endocrinology tasks quickly, with no need to memorise formulas or convert units by hand.",
        "Do the Endocrinology Tools need a download or registration?",
        "No. Every tool on this page is a pure front-end online utility: open the page and use it straight away, with no software to install, no account to create and no data uploaded.",
        "Are the Endocrinology Tools accurate, and is my data safe?",
        "Each tool computes locally in your browser from public mathematical formulas and general industry standards, so results are immediate. All arithmetic runs on your own device and no data is uploaded to any server, so your privacy is protected.",
    ]))


if __name__ == '__main__':
    main()
