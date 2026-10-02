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
    write('child-pugh', build('child-pugh', [
        "\U0001F4CB Liver Function Child-Pugh Grading Tool",
        "Assess hepatic functional reserve in cirrhosis from 5 clinical and laboratory indicators, for prognosis and surgical risk assessment.",
        "Liver Function Child-Pugh Grading Tool",
        "/ Child-Pugh Grading",
        "\U0001F4D6 View the Liver Function Child-Pugh Grading (PT/INR higher score) Usage Guide",
        "Child-Pugh grade = sum of bilirubin + albumin + prothrombin time/INR + ascites + hepatic encephalopathy (each 1 to 3 points); 5\u20136 points grade A, 7\u20139 grade B, 10\u201315 grade C.",
        "Prothrombin time prolongation (seconds)",
        "Small amount (easy to control)",
        "Moderate-to-large (hard to control)",
        "\U0001F4CB Child-Pugh scoring criteria",
        "PT prolongation (seconds)",
        "Small amount, easy to control",
        "Moderate-to-large, hard to control",
        "Note: Score either PT prolongation or INR and take the higher one. For primary biliary cholangitis the bilirubin criteria are adjusted: 1 point <68, 2 points 68-170, 3 points >170.",
        "Grade A (5-6 points)",
        ": liver function well compensated, 1-year survival 100%, 2-year survival 85%. Tolerates most surgeries.",
        "Grade B (7-9 points)",
        ": liver function moderately impaired, 1-year survival 80%, 2-year survival 60%. Elective surgery requires careful evaluation.",
        "Grade C (10-15 points)",
        ": liver function decompensated, 1-year survival 45%, 2-year survival 35%. Major surgery contraindicated.",
        "Note: The Child-Pugh grade is commonly used for cirrhosis prognosis assessment, surgical risk stratification, and TIPS indication decisions. It works best when combined with the MELD score. For clinical reference only.",
        "\U0001F4DA Deep Dive: Liver Function Child-Pugh Grading (PT/INR higher score)",
        "Hepatic functional reserve: compute the grade from 5 indicators to assess cirrhosis severity",
        "Surgical contraindication: grade C indicates decompensation with high risk for major surgery",
        "Transplant evaluation: repeated grade C or complications warrant starting liver transplant evaluation",
        "Algorithm: total bilirubin >51\u21923, 34~51\u21922, <34 \u03bcmol/L\u21921 point; albumin <28\u21923, 28~35\u21922, >35 g/L\u21921 point; coagulation takes the higher of PT prolongation and INR (PT>6s\u21923, \u22654s\u21922, <4s\u21921; INR>2.3\u21923, \u22651.7\u21922, <1.7\u21921); ascites (none/small/moderate-severe) 1~3 points; hepatic encephalopathy (none/I-II/III-IV) 1~3 points. \u22646 points grade A, 7~9 points grade B, \u226510 points grade C.",
        "Example: total bilirubin 35 \u03bcmol/L (34~51\u21922 points), albumin 30 g/L (28~35\u21922 points), PT prolongation 4s (\u22654\u21922 points), INR 1.7 (\u22651.7\u21922 points, higher score 2 taken), ascites 2 points, encephalopathy 2 points \u2192 total 10 points, grade C. If total bilirubin 20 \u03bcmol/L (<34\u21921 point), albumin 40 g/L (>35\u21921 point), PT 2s (<4\u21921 point), INR 1.2 (<1.7\u21921 point), ascites 1 point, encephalopathy 1 point \u2192 total 5 points, grade A, well compensated.",
        "Why take the higher score of PT prolongation and INR?",
        "PT prolongation in seconds and INR both reflect coagulopathy, but each fluctuates under the influence of testing conditions. Taking the higher of the two avoids underestimating coagulation abnormalities, making the grading more conservative and safer, especially for borderline patients.",
        "What is the difference between Child-Pugh and MELD?",
        "Child-Pugh uses 5 clinical/laboratory indicators; the grading is intuitive but subjective items (ascites, encephalopathy) vary by physician judgment. MELD uses creatinine, bilirubin, INR, and sodium, and is more suitable for end-stage liver disease queueing and short-term survival prediction. Clinically the two are often combined.",
        "About the Liver Function Child-Pugh Grading Tool",
        "The Liver Function Child-Pugh grading tool assesses the hepatic functional reserve grade of cirrhosis patients from five indicators: bilirubin, albumin, INR, ascites, and hepatic encephalopathy." + DISCL_M,
    ]))
    write('colonoscopy-polyp', build('colonoscopy-polyp', [
        "\u26A1 Colonoscopy (Adenoma/Polyp) Classification Reference",
        "Quick reference for Paris morphology, Kudo pit pattern, NICE classification, and size-based risk stratification.",
        "Colonoscopy Adenoma/Polyp Classification Reference",
        "/ Colonoscopy Polyp Classification",
        "Polyp morphology (Paris classification)",
        "Ip - Pedunculated",
        "Isp - Subpedunculated",
        "Is - Sessile",
        "IIa - Superficial elevated",
        "IIb - Completely flat",
        "IIc - Superficial depressed",
        "IIa+IIc - Elevated with depression",
        "Pit pattern (Kudo classification)",
        "Type I - Round",
        "Type II - Star-shaped / papillary",
        "Type IIIS - Tubular / round (small)",
        "Type IIIL - Large tubular / round",
        "Type IV - Grooved / branched",
        "Type VI - Irregular",
        "Type VN - Structureless",
        "Polyp diameter (mm)",
        "NICE classification",
        "NICE 1 - Hyperplastic",
        "NICE 2 - Adenoma",
        "NICE 3 - Deep submucosal cancer",
        "View analysis",
        "\U0001F4CB Paris morphology classification",
        "Pedunculated elevation",
        "Subpedunculated elevation",
        "Sessile elevation",
        "Superficial elevated (<2.5mm)",
        "Depends on size",
        "Completely flat",
        "Easily missed",
        "Superficial depressed",
        "Elevated with central depression",
        "\U0001F4CB Kudo pit pattern classification",
        "Pathological meaning",
        "Normal mucosa",
        "Star-shaped / papillary",
        "Hyperplastic polyp",
        "Observe / resect",
        "Tubular / round (small)",
        "Adenoma (depressed type)",
        "Endoscopic resection",
        "Large tubular / round",
        "Adenoma (elevated type)",
        "Grooved / branched",
        "Adenoma (villous-tubular)",
        "Irregular",
        "Suspected malignancy (M/SM shallow)",
        "Endoscopic resection (depth assessment needed)",
        "Structureless",
        "Deep SM cancer",
        "Surgical operation",
        "\U0001F4CA Size-based risk stratification",
        ": tiny polyp, mostly hyperplastic, may be observed or removed with cold snare",
        ": small polyp, adenoma proportion rises, endoscopic resection recommended",
        ": medium size, malignant transformation risk increases, EMR resection recommended",
        ": large polyp, high malignant transformation risk (10-20%+), ESD or piecemeal EMR recommended",
        "Note: Depressed lesions (IIc, IIa+IIc) and Kudo type V (VI/VN) carry markedly elevated malignant risk. The NICE classification is based on NBI narrow-band imaging and requires no staining. Final diagnosis follows pathology. For clinical reference only.",
        "\U0001F4DA Deep Dive: Colon Polyp/Adenoma Paris\u00b7Kudo\u00b7NICE Classification Quick Reference",
        "Endoscopic classification: define lesion nature by morphology (Paris), pit pattern (Kudo), and narrow-band imaging (NICE)",
        "Resection strategy: choose cold snare / EMR / ESD based on size and classification",
        "Malignant transformation",
        ": identify high-risk types (IIc, V_I, V_N, NICE 3)",
        "Criteria: Paris morphology (Ip pedunculated / Isp subpedunculated / Is sessile / IIa superficial elevated / IIb flat / IIc superficial depressed / IIa+IIc elevated with depression); Kudo pit pattern (I normal / II hyperplastic / III-S\u00b7III-L adenoma / IV villous adenoma / V_I suspected malignancy / V_N deep submucosal invasion); NICE (1 hyperplastic / 2 adenoma / 3 deep cancer). Size risk: <10mm low risk, 10~20mm medium risk, \u226520mm submucosal invasion risk can reach 20%~50%, \u226550mm lymph node metastasis risk rises.",
        "Example: Paris Is + Kudo III-L + NICE 2 + 12mm \u2192 sessile elevation, large tubular adenoma, adenomatous, 12mm diameter; en bloc EMR resection with pathology submission is advised. If Paris IIc + Kudo V_I + NICE 3 + 18mm \u2192 superficial depression, irregular pit pattern (suspected intramucosal/shallow submucosal cancer), disordered deep brown vessels, 18mm; high risk, en bloc ESD with invasion depth evaluation is advised, adding surgery if necessary.",
        "Why can Kudo V_N not be resected endoscopically?",
        "Kudo V_N indicates loss of the pit pattern and a structureless surface, corresponding to deeply invasive (deep SM) carcinoma with high lymph node metastasis risk. Endoscopic resection is hard to cure en bloc and prone to residual tissue, so surgical operation is the route.",
        "Is NICE 1 always benign?",
        "NICE 1 (pale, absent vessels) mostly corresponds to hyperplastic polyps or SSL (sessile serrated lesions), but SSL has latent malignant potential, especially when located in the proximal colon or >1cm in diameter, and still requires resection plus pathology confirmation; NBI alone cannot decide.",
        "About the Colonoscopy Adenoma/Polyp Classification Reference",
        "The Colonoscopy Adenoma/Polyp Classification Reference provides quick-reference for Paris morphology, Kudo pit pattern, NICE classification, and diameter-based risk stratification." + DISCL_M,
    ]))

if __name__ == '__main__':
    main()
