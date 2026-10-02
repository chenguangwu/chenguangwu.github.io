#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'gastroenterology')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'gastroenterology')
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
    out = {'slug': slug, 'industry': 'gastroenterology', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
DISCL_M = " A professional medical tool based on authoritative medical standards, for reference only."

def main():
    write('gastrin-level', build('gastrin-level', [
        "\U0001F4DA Gastrin Normal Range Assessor",
        "Enter the fasting gastrin value and combine it with gastric pH to judge the cause of hypergastrinemia.",
        "Gastrin Normal Range Assessor",
        "/ Gastrin Assessment",
        "Fasting gastrin (pg/mL)",
        "Gastric fluid pH",
        "Acidic (pH<2, normal/high gastric acid)",
        "Alkaline/achlorhydric (pH>2, low gastric acid)",
        "Currently using PPI",
        "Hypercalcemia/hyperparathyroidism",
        "\U0001F4CB Gastrin reference range and clinical meaning",
        "Gastrin (pg/mL)",
        "Physiological range",
        "PPI use, Hp infection, atrophic gastritis",
        "Need to rule out gastrinoma",
        "Highly suspicious for gastrinoma (ZES)",
        "Normal fasting gastrin reference ranges vary slightly by laboratory, typically 13-115 pg/mL or <100 pg/mL. Blood must be drawn fasting.",
        "\U0001F4CA Differential diagnosis of hypergastrinemia",
        "Normal/high gastric acid + elevated gastrin",
        "Gastrinoma (ZES)",
        ": markedly elevated gastrin + high gastric acid, refractory ulcers/diarrhea",
        "G-cell hyperplasia",
        ": antral G-cell hyperfunction",
        "Gastric outlet obstruction",
        ": antral dilatation stimulates G cells",
        "Short bowel syndrome",
        ": decreased enterogastric peptide",
        "Low/achlorhydric gastric acid + elevated gastrin (feedback)",
        "Atrophic gastritis (type A)",
        ": autoimmune, parietal cell antibody positive",
        "Pernicious anemia",
        ": vitamin B12 deficiency, megaloblastic anemia",
        "Long-term PPI use",
        ": recovers after discontinuation",
        "H2 receptor blockers",
        ": less influence than PPI",
        "Note: Confirming ZES requires a secretin stimulation test (gastrin rise \u2265120 pg/mL after IV secretin is positive). Those with MEN1 should be tested for parathyroid hormone and pituitary hormones. Recheck gastrin 2 weeks after PPI discontinuation. For clinical reference only.",
        "\U0001F4DA Deep Dive: Gastrin Level and Differential Diagnosis of Hypergastrinemia",
        "ZES screening: rule out gastrinoma when high gastrin accompanies high gastric acid",
        "Atrophic gastritis differentiation: high gastrin with low acid indicates feedback elevation",
        "Follow-up monitoring: recheck 2 weeks after PPI discontinuation to avoid false positives",
        "Algorithm: the reference range is usually 13~115 pg/mL. Decision: <100 normal; 100~500 mild elevation; 500~1000 moderate elevation (rule out gastrinoma); \u22651000 marked elevation (highly suspicious for ZES). Combined with gastric pH: at high acid (pH<2) elevation mostly points to gastrinoma/ZES; at low acid (pH>2) it is mostly atrophic gastritis, pernicious anemia, or PPI-induced feedback elevation. PPI and hypercalcemia can raise gastrin.",
        "Example: fasting gastrin 150 pg/mL, low gastric pH (acidic) \u2192 mild elevation (needs attention); check Hp, recheck gastrin, and if persistently elevated with refractory ulcers perform a secretin stimulation test. If 850 pg/mL with low pH \u2192 moderate elevation (500~1000), highly suspicious for gastrinoma (ZES); secretin stimulation test plus imaging localization (CT/MRI/68Ga-DOTATATE PET-CT) is advised, and check PTH and pituitary hormones to exclude MEN1.",
        "Does gastrin >1000 always mean gastrinoma?",
        "With high gastric acid it is highly suspicious for ZES, but confirmation requires a secretin stimulation test (gastrin rise >120 pg/mL is positive). If gastric acid is low, it is mostly feedback elevation from severe atrophic gastritis/pernicious anemia; recheck after PPI discontinuation rather than treating it directly as a tumor.",
        "How much can PPI raise gastrin?",
        "Long-term high-dose PPI can raise gastrin several-fold through feedback, mostly still in the hundreds pg/mL range, and it falls within 1~2 weeks after discontinuation. If the elevation is marked (>1000) with high acid, gastrinoma should still be ruled out rather than simply attributed to PPI.",
        "About the Gastrin Normal Range Assessor",
        "The Gastrin Normal Range Assessor takes the fasting gastrin value together with gastric pH to judge the cause of hypergastrinemia, providing differential reference for conditions such as Zollinger-Ellison syndrome." + DISCL_M,
    ]))
    write('gastroscopy-atlas', build('gastroscopy-atlas', [
        "\U0001F5BC Gastroscopy (Gastritis/Ulcer) Image Recognition Reference",
        "Classification descriptions, diagnostic points, and differential tips for common gastroscopic lesions.",
        "Gastroscopy Image Recognition Reference",
        "/ Gastroscopy Image Recognition",
        "Gastroscopy atlas lookup: classified by site (esophagus/fundus/body/antrum/duodenum) and lesion type (gastritis/ulcer/polyp/tumor), giving typical endoscopic appearances, diagnostic points, and differential tips.",
        "Gastritis",
        "Ulcer",
        "Tumor",
        "\U0001F4CB Commonly used gastroscopy grading systems",
        "Sydney system (chronic gastritis classification)",
        "Non-atrophic gastritis: antral predominant / body predominant / pangastritis",
        "Atrophic gastritis: antral predominant / body predominant / pangastritis",
        "Special types: chemical, radiation, lymphocytic, granulomatous, eosinophilic",
        "Kimura-Takemoto atrophy grading",
        "C-1: atrophy limited to the lesser curvature of the antrum",
        "C-2: atrophy reaching the lesser curvature of the lower body",
        "C-3: atrophy reaching the lesser curvature side of the cardia",
        "O-1: atrophy crossing the cardia to the anterior/posterior walls",
        "O-2: atrophy reaching most of the gastric body",
        "O-3: total gastric atrophy (including greater curvature)",
        "Forrest grading of active bleeding",
        "Ia: spurting bleeding",
        "Ib: oozing bleeding",
        "IIa: visible vessel (no bleeding)",
        "IIb: adherent clot",
        "IIc: black base (bleeding has stopped)",
        "III: clean base, no bleeding signs",
        "Note: This tool is a gastroscopy image recognition reference and cannot replace biopsy for confirmation. Early gastric cancer (type 0-IIc) is easily missed; confirmation with NBI/BLI magnified endoscopy and biopsy is advised. For learning reference only.",
        "\U0001F4DA Deep Dive: Gastroscopy (Gastritis/Ulcer/Tumor) Atlas and Diagnostic Points",
        "Reading reference: compare against typical appearances of chronic/atrophic/verrucous gastritis and bile reflux",
        "Ulcer staging: distinguish active phase (A1/A2), healing phase (H1/H2), and neoplastic ulcer",
        "Early cancer detection: focus on irregular borders of 0-IIa/0-IIc and magnified microvessels (V/S classification)",
        "Classification points: chronic atrophic gastritis is characterized by thinned mucosa and visible vessels, requiring biopsy to confirm intestinal metaplasia and OLGA/OLGIM staging; gastric ulcer active phase A1 (thick coating, marked edema) \u2192 A2 (coating thins), healing phase H1 (red halo regenerating epithelium) \u2192 H2; duodenal bulb ulcers perforate easily on the anterior wall and bleed easily on the posterior wall, with Hp infection near 100%; early gastric cancer 0-IIc (shallow depression, irregular border) and 0-IIa (shallow elevation) need NBI/BLI magnification to observe microvessels.",
        "Example: gastric angle ulcer with white coating, surrounding congestion and edema, regular shape \u2192 active phase A2; after Hp eradication, recheck. If a duodenal bulb ulcer is also seen \u2192 combined ulcer, with high bleeding risk, Hp eradication is mandatory. Another example: erythematous antral mucosa with irregular border and irregular microvessels (type V) on NBI \u2192 possible early gastric cancer 0-IIc; multi-point biopsy should be taken, and ESD performed after confirmation.",
        "Does atrophic gastritis always turn into cancer?",
        "Atrophic gastritis with intestinal metaplasia is a precancerous lesion, but the annual cancer transformation rate is only about 0.1%~0.3%. Risk rises with OLGA/OLGIM stage (stages III-IV significantly higher); the key is Hp eradication plus regular gastroscopy and biopsy follow-up rather than excessive anxiety.",
        "Does an irregular ulcer shape always mean malignancy?",
        "Irregular ulcers carry high malignant risk, but active benign ulcers can also have irregular edges. Differentiation relies on the white-coating pattern, surrounding regenerating epithelium, and biopsy (sample the ulcer edge rather than the necrotic center), with staining/NBI magnification and EUS for invasion depth if needed.",
        "About the Gastroscopy Image Recognition Reference",
        "The Gastroscopy Image Recognition Reference provides quick-reference classification descriptions and diagnostic points for common gastroscopic appearances such as gastritis, gastric ulcer, duodenal ulcer, and early gastric cancer." + DISCL_M,
        "e.g. ulcer, atrophy, early cancer...",
    ]))
    write('glasgow-pancreatitis', build('glasgow-pancreatitis', [
        "\U0001F4CB Acute Pancreatitis Glasgow Severity Assessor",
        "Glasgow-Imrie scoring system, assessed within 48 hours of admission, \u22653 points indicates severe acute pancreatitis.",
        "Glasgow-Imrie scoring system, assessed within 48 hours of admission, \u22653 points indicates severe acute pancreatitis. Computes professionally from the input parameters and outputs the result.",
        "Pancreatitis Glasgow Severity Assessor",
        "/ Glasgow Pancreatitis Assessment",
        "\U0001F4D6 View the Acute Pancreatitis Glasgow(Imrie) Severity Score Usage Guide",
        "White blood cells (\u00D710\u2079/L)",
        "Blood glucose (mmol/L)",
        "Calcium (mmol/L)",
        "Urea (mmol/L)",
        "\U0001F4CB Glasgow-Imrie scoring criteria",
        "Positive criterion (1 point)",
        ">55 years",
        "White blood cells",
        ">10 mmol/L (no diabetes history)",
        "Urea",
        "Scoring timing: within 48 hours of admission. 9 items total, 1 point each.",
        "\U0001F4CA Result interpretation",
        "0-2 points",
        ": mild acute pancreatitis most likely, mortality <3%",
        "\u22653 points",
        ": severe acute pancreatitis, mortality 15-30%, requires ICU monitoring",
        "\u22656 points",
        ": critical, mortality >50%, requires multidisciplinary resuscitation",
        "Note: The Glasgow score complements APACHE II, Ranson, and BISAP. Combining it with the CT severity index (Balthazar CTSI) improves accuracy. For clinical reference only.",
        "\U0001F4DA Deep Dive: Acute Pancreatitis Glasgow(Imrie) Severity Score",
        "Admission assessment: compute the Glasgow score from 9 indicators within 48 hours to judge mild/severe/critical",
        "ICU decision: \u22653 points indicates severe disease requiring monitoring and organ support",
        "Dynamic recheck: recompute within 48 hours to catch deterioration",
        "Algorithm (9 items, each +1): age >55 years; WBC >15\u00D710\u2079/L; glucose >10 mmol/L; LDH >600 U/L; AST >200 U/L; calcium <2.0 mmol/L; albumin <32 g/L; urea >16 mmol/L; PaO2 <60 mmHg. Total 0~9: <3 mild (mortality <3%), 3~5 severe (15~30%), \u22656 critical (>50%).",
        "Example: age 60, WBC 16, glucose 11, LDH 620, AST 210, calcium 1.9, albumin 30, urea 18, PaO2 55 \u2192 all 9 items triggered, score 9, critical (mortality >50%), requires ICU resuscitation. If age 60, WBC 16, glucose 11, LDH 620, others normal (AST 200, calcium 2.0, albumin 32, urea 16, PaO2 60) \u2192 only 4 items triggered, score 4, severe (15~30%); ICU monitoring and dynamic CT are advised.",
        "How to choose between Glasgow and APACHE II?",
        "Glasgow(Imrie) uses only 9 routine labs, is simple and can be computed on admission, suiting quick triage; APACHE II has more indicators and a more complete overall critical illness assessment. Clinically the two are often used together, while the Ranson criteria emphasize admission and 48h dynamic indicators.",
        "What if the score is 2 but the patient looks very ill?",
        "The score only reflects lab abnormalities within the first 48 hours and cannot replace clinical judgment. If persistent organ failure, abdominal compartment syndrome, or CT showing extensive necrosis appears, severe management with dynamic rescoring is warranted even when the score is low.",
        "About the Pancreatitis Glasgow Severity Assessor",
        "The Glasgow-Imrie acute pancreatitis severity assessor evaluates severe pancreatitis risk from 9 indicators including age, white blood cells, glucose, LDH, AST, calcium, albumin, urea, and PaO2." + DISCL_M,
    ]))

if __name__ == '__main__':
    main()
