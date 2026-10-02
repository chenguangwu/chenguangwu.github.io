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
    write('pituitary-tumor', build('pituitary-tumor', [
        "\U0001F9EC Pituitary Tumour (Size / Secretory) Classifier",
        "Classify pituitary tumours by size and secretory function, with management advice and follow-up strategy",
        "\U0001F4D6 See the \"Pituitary Tumour (Size / Secretory) Classifier User Guide\"",
        "By maximum diameter: 10mm or less is a microadenoma, 10 to 40mm a macroadenoma and over 40mm a giant adenoma. By secretory function: prolactinoma (raised PRL, first-line dopamine agonists), growth hormone tumour (raised GH and IGF-1), ACTH tumour (raised cortisol, Cushing disease), TSH tumour and non-functioning tumour. Follow-up is arranged by type: MRI and hormones every 1 to 2 years for a non-functioning microadenoma, and PRL rechecked 3 months after a prolactinoma starts medication.",
        "1. Tumour size",
        "Microadenoma",
        "Macroadenoma",
        "Giant adenoma",
        "Maximum tumour diameter (mm)",
        "Invading the cavernous sinus?",
        "Yes (Knosp grade 3-4)",
        "2. Secretory type",
        "Non-functioning",
        "Prolactinoma",
        "Growth hormone tumour",
        "ACTH tumour",
        "TSH tumour",
        "Gonadotroph tumour",
        "Pituitary tumour grading reference",
        "Classification dimension",
        "By size",
        "Under 10mm (intrasellar)",
        "10mm or more, may extend suprasellar or parasellar",
        "Over 40mm, widely invasive",
        "By function",
        "Functioning",
        "Secretes hormones (PRL/GH/ACTH/TSH/FSH-LH)",
        "Non-functioning",
        "No hormone secretion, may cause pressure symptoms",
        "By invasion",
        "Non-invasive",
        "Knosp grade 0-2",
        "Invasive",
        "Knosp grade 3-4, involving the cavernous sinus",
        "Knosp grading (cavernous sinus invasion)",
        "MRI appearance",
        "Possibility of complete surgical removal",
        "Does not reach the medial venous plexus",
        "Reaches the medial venous plexus",
        "Reaches between the medial and lateral venous plexus",
        "Reaches the lateral venous plexus (invades the cavernous sinus)",
        "Fully encases the internal carotid artery (complete invasion)",
        "Treatment principles:",
        "Prolactinomas are treated first with a dopamine agonist (bromocriptine or cabergoline). Other functioning macroadenomas and non-functioning macroadenomas with pressure symptoms go for transsphenoidal surgery first. Symptom-free microadenomas can be followed with periodic MRI. Pituitary function must be assessed after surgery and followed long term.",
        "\U0001F4DA In-depth analysis: Pituitary Tumour (Size / Secretory) Classifier",
        "Screening for prolactinoma in amenorrhoea with galactorrhoea and raised PRL.",
        "Evaluating raised GH/IGF-1 in acromegaly together with a sellar mass.",
        "Follow-up and surgical indications for a non-functioning macroadenoma compressing the optic chiasm.",
        "Pituitary tumour phenotype example",
        "PRL over 100 ng/mL with a microadenoma is most often a prolactinoma (dopamine agonist first-line); raised GH and IGF-1 with a sellar mass indicates acromegaly (GH tumour); a non-functioning macroadenoma is followed mainly on pressure symptoms and visual field loss.",
        "How are macroadenomas and microadenomas separated?",
        "A maximum diameter of 10mm is the boundary; macroadenomas are more likely to compress the optic chiasm and cavernous sinus, so visual fields and nerve compression must be assessed.",
        "Does a raised PRL always mean a tumour?",
        "Not always. Drugs (such as antipsychotics), pregnancy, primary hypothyroidism (TRH stimulation) and the hook effect (difficult sampling causing haemolysis) can all cause a false rise, so imaging is needed too.",
        "About \"Pituitary Tumour (Size / Secretory) Classification\"",
        "Pituitary tumours are classified by size (micro/macro/giant adenoma) and secretory function, with Knosp grading adding an invasion assessment, guiding surgical and drug treatment decisions.",
        "Dual-axis size and secretion classification",
        "Knosp invasion assessment",
        "Treatment strategy advice",
        "Preliminary pituitary tumour typing",
        "Reference for treatment decisions",
        "Postoperative follow-up planning",
        "Neuroendocrine teaching",
    ]))

    write('thyroid-cancer-risk', build('thyroid-cancer-risk', [
        "\U0001F4CB Thyroid Cancer (Recurrence Risk) Dynamic Assessor",
        "Based on the ATA dynamic risk stratification system, assess recurrence risk and follow-up strategy after surgery for differentiated thyroid cancer (DTC)",
        "\"Based on the ATA dynamic risk stratification system, assess recurrence risk and follow-up strategy after surgery for differentiated thyroid cancer (DTC)\" is computed from the input parameters and the result is reported.",
        "\U0001F4D6 See the \"Thyroid Cancer (Recurrence Risk) Dynamic Assessor User Guide\"",
        "Initial risk stratification (postoperative pathology)",
        "Tumour size (cm)",
        "Pathological type",
        "Papillary carcinoma (PTC)",
        "Follicular carcinoma (FTC)",
        "Hürthle cell carcinoma",
        "Extrathyroidal extension (ETE)",
        "Lymph node metastasis",
        "Vascular invasion",
        "Distant metastasis (M1)",
        "Aggressive histological subtype",
        "Radioactive iodine refractory (RAIR)",
        "Dynamic assessment (treatment response, 6-12 months after surgery)",
        "Tg thyroglobulin (ng/mL)",
        "Anti-Tg antibody",
        "Positive (interferes with Tg measurement)",
        "Imaging (neck ultrasound/CT)",
        "Indeterminate lesion",
        "Lesion detected",
        "Diagnostic scan after \u00B9\u00B3\u00B9I treatment",
        "Iodine uptake limited to the thyroid bed",
        "Iodine uptake outside the thyroid bed",
        "Dynamic risk assessment",
        "High-risk example",
        "Low-risk example",
        "ATA initial risk stratification",
        "10-year recurrence rate",
        "Intrathyroidal, no ETE, no metastasis, R0 resection",
        "Microscopic ETE, microscopic cervical node metastasis, vascular invasion, aggressive subtype",
        "Gross ETE, incomplete resection, distant metastasis, extensive node metastasis",
        "ATA dynamic risk stratification (treatment response)",
        "Follow-up",
        "Excellent response (ER)",
        "Tg<0.2 (suppressed)/<1 (stimulated), negative imaging",
        "Reduce TSH suppression and lengthen follow-up",
        "Biochemical incomplete response (bIR)",
        "Rising Tg, negative imaging",
        "Monitor the Tg trend and continue TSH suppression",
        "Structural incomplete response (sIR)",
        "Lesion detected on imaging (whatever the Tg)",
        "Individualised treatment (surgery/ablation/radiotherapy/targeted therapy)",
        "Indeterminate (IDR)",
        "Mildly abnormal Tg or indeterminate imaging",
        "Close follow-up, repeat assessment if needed",
        "Why dynamic assessment helps:",
        "ATA dynamic risk stratification predicts recurrence more accurately than initial stratification and lets you adjust TSH suppression intensity and the follow-up interval. Excellent responders can be downgraded, while structural incomplete responders need active intervention. Tg is the key follow-up marker, but positive TgAb interferes with the assay.",
        "\U0001F4DA In-depth analysis: Thyroid Cancer (Recurrence Risk) Dynamic Assessor",
        "Stratifying malignancy risk in thyroid nodules found at a health check.",
        "Dynamic assessment of changing nodule features during ultrasound follow-up.",
        "A reference for fine-needle aspiration (FNA) or surgical indications.",
        "Nodule risk example",
        "Solid hypoechoic, irregular margins, microcalcification, taller-than-wide with a maximum diameter of 1.2cm: several high-risk ultrasound features give a high malignancy risk (TI-RADS 4/5), so FNA is advised and central compartment nodes should be assessed.",
        "There are many TI-RADS versions, which one applies?",
        "ACR TI-RADS or the ATA guidelines are common; the grading logic is similar but the thresholds differ. This report scores by the five ACR TI-RADS features, and clinically you should follow the standard of the hospital you attend.",
        "How large must a nodule be for aspiration?",
        "Nodules with high-risk features are often aspirated at 1cm or more; low and intermediate risk can wait for a larger size or be followed up alone.",
        "About \"Thyroid Cancer (Recurrence Risk) Dynamic Assessment\"",
        "ATA dynamic risk stratification is the core tool for managing differentiated thyroid cancer (DTC) after surgery, adjusting TSH suppression intensity and follow-up strategy in real time from the treatment response.",
        "Two-stage initial plus dynamic assessment",
        "Combined judgement of Tg, imaging and scanning",
        "RAIR identification",
        "Postoperative thyroid cancer management",
        "TSH suppression decisions",
        "\u00B9\u00B3\u00B9I treatment response assessment",
        "Long-term thyroid cancer follow-up",
    ]))


if __name__ == '__main__':
    main()
