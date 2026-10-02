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
    write('gh-stimulation-test', build('gh-stimulation-test', [
        "\U0001F4CB Growth Hormone (GH) Stimulation Test Assessor",
        "Enter the GH peak at each time point of different stimulation drugs to assess growth hormone deficiency (GHD) diagnosis",
        "Core formulas (by input): min(100, (peak\u00F715)\u00D7100)",
        "\U0001F4D6 See the \"Growth Hormone (GH) Stimulation Test Assessor User Guide\"",
        "Insulin tolerance test (ITT)",
        "Arginine stimulation test",
        "Clonidine stimulation test",
        "Levodopa test",
        "Glucagon test",
        "Height SDS (standard deviation)",
        "GH value at each time point (ng/mL)",
        "Assess the test",
        "GHD example",
        "GH stimulation test diagnostic criteria and interpretation",
        "GH peak",
        "GHD excluded",
        "Partial deficiency",
        "A second stimulation test is needed",
        "Complete deficiency",
        "Both tests under 5 are needed for diagnosis",
        "Note: thresholds differ slightly between guidelines. The Growth Hormone Research Society (GRS) consensus suggests using under 7ng/mL as the paediatric GHD threshold. Diagnosis needs at least two different drug stimulation tests to be abnormal.",
        "Comparison of common stimulation drugs",
        "Insulin (ITT)",
        "Hypoglycaemia stimulates GH secretion",
        "Gold standard, also assesses ACTH",
        "Carries hypoglycaemia risk and needs close monitoring",
        "Arginine",
        "Suppresses somatostatin",
        "Safe with few side effects",
        "Lower sensitivity",
        "Clonidine",
        "\u03B12 receptor agonist",
        "Safe and oral",
        "May cause hypotension and drowsiness",
        "Levodopa",
        "Dopaminergic stimulation",
        "Easy to take orally",
        "Nausea and vomiting are common",
        "Glucagon",
        "Multipathway stimulation",
        "Safe and suitable for outpatients",
        "Long test time (3h)",
        "Test precautions:",
        "Fast for 8 hours beforehand, with no food the night before. ITT needs glucose monitoring, and the test is only a valid stimulus once glucose has fallen below 2.2mmol/L (or to under 50% of baseline). Contraindications: epilepsy, heart disease and low baseline glucose rule out ITT. Tests must be performed by trained staff under monitoring.",
        "\U0001F4DA In-depth analysis: Growth Hormone (GH) Stimulation Test Assessor",
        "GHD screening in short children with slowing yearly growth velocity.",
        "Adult GHD assessment after pituitary tumour surgery or radiotherapy.",
        "Standardised interpretation of stimulation test results.",
        "GH peak threshold example",
        "After stimulation with arginine plus clonidine the GH peak is 3.2 ng/mL (this centre's cut-off of under 5 ng/mL indicates deficiency; some adults use under 3). Combined with slow height velocity and low IGF-1 this supports GHD, and constitutional delay of growth and puberty must be excluded.",
        "Why use two stimulation drugs?",
        "A single stimulation has insufficient and highly variable sensitivity, so guidelines usually require two drugs with different mechanisms (such as arginine plus clonidine, or insulin hypoglycaemia) to be low, which reduces false positives.",
        "Why do the peak cut-offs differ?",
        "It depends on the GH assay (immunoassay versus chemiluminescence), age and sex, so the reference cut-off of your own laboratory must be used.",
        "About \"Growth Hormone (GH) Stimulation Test Assessor\"",
        "GH stimulation testing is the core functional test for diagnosing growth hormone deficiency (GHD); two different drugs must both fail to reach the target before GHD is confirmed.",
        "Choice of five common stimulation drugs",
        "Automatic GH peak detection at each time point",
        "Combined assessment with height SDS and IGF-1",
        "Graded reading against diagnostic thresholds",
        "GHD diagnosis in short children",
        "Growth hormone treatment indication assessment",
        "Assessment of hypopituitarism",
        "Paediatric endocrinology teaching",
    ]))

    write('graves-trab', build('graves-trab', [
        "\U0001F4CB Graves Disease (TRAb Titre) Significance Assessor",
        "Enter the TRAb (thyroid-stimulating hormone receptor antibody) result to assess Graves disease diagnosis, activity and relapse risk after stopping treatment",
        "Core formulas (by input): min(100, (trab \u00F7 15) \u00D7 100)",
        "\U0001F4D6 See the \"Graves Disease (TRAb Titre) Significance Assessor User Guide\"",
        "TRAb result (IU/L)",
        "Assay reference upper limit",
        "TRAb (third generation) under 1.75 IU/L",
        "TRAb (some reagents) under 1.5 IU/L",
        "TRAb (high sensitivity) under 1.22 IU/L",
        "Treatment stage",
        "Newly diagnosed (untreated)",
        "On antithyroid drug therapy",
        "Assessing drug withdrawal",
        "Postpartum assessment",
        "Clinical significance grading of the TRAb titre",
        "TRAb level",
        "Under 1.75 IU/L (negative)",
        "Normal, does not support Graves disease",
        "Graves excluded (combine with clinical picture)",
        "Mildly raised, Graves possible",
        "Combine with ultrasound and radionuclide imaging",
        "Moderately raised, active Graves",
        "Confirms Graves, start treatment",
        "Markedly raised, severe activity",
        "High relapse risk, follow up closely",
        "TRAb at each stage",
        "Clinical value",
        "Differential diagnosis at presentation",
        "Distinguishes Graves disease from other causes of hyperthyroidism (sensitivity 97%, specificity 99%)",
        "Monitoring treatment response",
        "A falling titre suggests treatment works and becoming negative suggests possible remission",
        "Predicting relapse after stopping",
        "TRAb positive at withdrawal gives a 70-80% relapse rate; negative gives 10-20%",
        "Pregnancy management",
        "Measuring TRAb in mid-pregnancy; positive results raise the risk of neonatal hyperthyroidism",
        "Eye disease assessment",
        "The TRAb level correlates positively with Graves orbitopathy activity",
        "TRAb basics:",
        "TRAb is the TSH receptor antibody, the pathogenic antibody of Graves disease; it stimulates the TSH receptor and causes excess thyroid hormone secretion. Third-generation TRAb assays (TRAb III, using a binding inhibition method) have the highest specificity and can separate TSI (stimulating) from TBII (binding-blocking).",
        "\U0001F4DA In-depth analysis: Graves Disease (TRAb Titre) Significance Assessor",
        "Differential diagnosis of hyperthyroidism (Graves disease versus painless thyroiditis or toxic nodular goitre).",
        "Relapse of antithyroid drug (ATD) therapy before it is stopped.",
        "Monitoring fetal and neonatal hyperthyroidism risk in pregnancy with Graves disease.",
        "TRAb reading example",
        "TRAb 2.8 IU/L (reference under 1.75 IU/L) with suppressed TSH and raised FT4 supports Graves disease; if ATD is to be stopped while TRAb is still clearly raised, the relapse risk is high, so extending treatment or considering definitive therapy is advisable.",
        "Is TRAb the same as TSI?",
        "TRAb is the umbrella term for receptor antibodies, and TSI (stimulating antibody) is the pathogenic subset; clinical reports usually give total TRAb, and a raised level supports Graves disease.",
        "Why test during pregnancy?",
        "Maternal TRAb crosses the placenta and can stimulate the fetal thyroid, so monitoring in the second and third trimesters helps predict neonatal hyperthyroidism and guides newborn follow-up.",
        "About \"Graves Disease (TRAb Titre) Significance Assessment\"",
        "TRAb (thyroid-stimulating hormone receptor antibody) is the pathogenic antibody of Graves disease and the diagnostic gold standard; this tool assesses the diagnostic, monitoring and relapse-prediction value of its titre.",
        "Titre grading",
        "Advice for each treatment stage",
        "Relapse risk prediction after stopping",
        "Graves orbitopathy risk alerts",
        "Differential diagnosis of Graves disease",
        "Monitoring antithyroid drug efficacy",
        "Withdrawal decision assessment",
        "Hyperthyroidism management in pregnancy",
        "How to use the Graves Disease (TRAb Titre) Significance Assessor",
        "To distinguish the cause of hyperthyroidism (Graves disease versus others), predict relapse after stopping antithyroid drugs, and monitor fetal and neonatal hyperthyroidism risk in pregnancy.",
        "What does the Graves Disease (TRAb Titre) Significance Assessor do?",
        "How do I use the Graves Disease (TRAb Titre) Significance Assessor?",
        "Which scenarios suit the Graves Disease (TRAb Titre) Significance Assessor?",
    ]))

    write('glycated-albumin', build('glycated-albumin', [
        "\u2697\uFE0F Glycated Albumin (GA) and Glycaemia Correlation Assessor",
        "Assess the glycated albumin (GA) level, which reflects average glucose over the past 2-3 weeks, and analyse glycaemic control quality against HbA1c",
        "Core formulas (by input): min(100, (ga \u00F7 30) \u00D7 100); 1.59\u00D7A1C - 2.59 (mmol\u00F7L); a1c \u00D7 2.5 - 2",
        "\U0001F4D6 See the \"Glycated Albumin (GA) and Glycaemia Correlation Assessor User Guide\"",
        "Glycated albumin GA (%)",
        "Poorly controlled",
        "GA reference ranges and targets",
        "Corresponding mean glucose (mmol/L)",
        "Corresponding HbA1c (%)",
        "Under 17.1 (male) / under 16.5 (female)",
        "GA versus HbA1c testing characteristics",
        "Glycated albumin (GA)",
        "Glycated haemoglobin (HbA1c)",
        "Reflects period",
        "2-3 weeks",
        "2-3 months",
        "Glycated protein",
        "Albumin (half-life 17 days)",
        "Haemoglobin (half-life 120 days)",
        "Sensitive to short-term glucose change",
        "Gold standard for long-term glucose",
        "Effect of anaemia / haemolysis",
        "Not affected",
        "Affected (falsely low)",
        "Effect of kidney disease / low albumin",
        "Affected (toluidine blue method)",
        "Suitable (red cell lifespan change)",
        "Interpret with caution",
        "Postoperative / acute phase",
        "Sensitive to recent change",
        "Clinical use cases:",
        "GA is an important complement to HbA1c: (1) assessing short-term glycaemic control, such as the response 2-3 weeks after a medication change; (2) gestational diabetes management, where red cell lifespan change makes HbA1c unreliable; (3) haemodialysis patients, where HbA1c cannot be trusted; (4) perioperative glycaemic management; (5) patients with iron deficiency or haemolytic anaemia.",
        "Cautions:",
        "Hypoalbuminaemia (under 35g/L), nephrotic syndrome, abnormal thyroid function and cirrhosis all affect GA accuracy. Reference ranges for older adults and children differ slightly. Reading GA together with HbA1c gives a fuller picture of glycaemic control.",
        "\U0001F4DA In-depth analysis: Glycated Albumin (GA) and Glycaemia Correlation Assessor",
        "An alternative or complement to HbA1c for monitoring glucose in haemodialysis patients.",
        "Short-term glycaemic trend assessment in gestational diabetes.",
        "Judging glucose when anaemia or a haemoglobin variant makes HbA1c unreliable.",
        "GA reading example",
        "Glycated albumin 4.2 mg/dL with albumin 4.0 g/dL: GA(%)=glycated albumin/albumin\u00D717.1\u224818% (some laboratories use the GA/albumin ratio AGR). The normal GA reference is about 11%-16%, and a raised value indicates glucose has been high over the past 2-4 weeks.",
        "How does GA differ from HbA1c?",
        "HbA1c reflects about 2-3 months of mean glucose while GA reflects about 2-4 weeks, a shorter window that is more sensitive to recent change.",
        "When is GA distorted too?",
        "Severe kidney disease, liver disease, abnormal thyroid function and large albumin infusions all shift albumin levels and skew GA interpretation.",
        "About \"Glycated Albumin (GA) and Glycaemia Correlation Assessor\"",
        "Glycated albumin (GA) reflects average glucose over the past 2-3 weeks and is an important complement to HbA1c, especially valuable when HbA1c is unreliable in anaemia, pregnancy and haemodialysis.",
        "Graded control assessment with GA",
        "GA-HbA1c concordance analysis",
        "Estimated recent mean glucose",
        "Albumin interference alerts",
        "Short-term glycaemic control assessment",
        "Gestational diabetes management",
        "Glucose monitoring in anaemia and haemodialysis",
    ]))


if __name__ == '__main__':
    main()
