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
    write('bilirubin-ratio', build('bilirubin-ratio', [
        "\U0001F9EE Bilirubin (Direct/Indirect) Ratio Calculator",
        "Calculate indirect bilirubin and the direct bilirubin ratio to help differentiate jaundice types.",
        "Direct/Indirect Bilirubin Ratio Calculator",
        "/ Bilirubin ratio calculation",
        "Direct bilirubin ratio = DBIL / TBIL \u00d7 100%",
        "Total bilirubin TBIL (\u03bcmol/L)",
        "Direct bilirubin DBIL (\u03bcmol/L)",
        "Upper limit of normal reference",
        "TBIL\u226421, DBIL\u22646.8 (routine adult values)",
        "TBIL\u226425, DBIL\u22648.0 (some laboratories)",
        "\U0001F4CB Jaundice classification criteria",
        "Direct bilirubin ratio",
        "Hemolytic (indirect predominates)",
        "Hemolytic anemia, Gilbert syndrome",
        "Hepatocellular",
        "Viral hepatitis, drug-induced liver injury",
        "Obstructive (direct predominates)",
        "Bile duct stones, cholangiocarcinoma, pancreatic head cancer",
        "Direct bilirubin ratio = DBIL / TBIL \u00d7 100%. Indirect bilirubin = TBIL - DBIL.",
        "\U0001F4CA Differential diagnosis essentials",
        "Indirect bilirubin predominates",
        "Gilbert syndrome: mild elevation (<85 \u03bcmol/L), hereditary",
        "Crigler-Najjar syndrome: rare, severe elevation",
        "Hemolytic anemia: LDH\u2191, reticulocytes\u2191, haptoglobin\u2193",
        "Impaired hepatocyte uptake: heart failure, drugs, etc.",
        "Direct bilirubin predominates",
        "Biliary obstruction: stones, tumor, stricture (confirmed by imaging)",
        "Dubin-Johnson syndrome: rare, black liver",
        "Rotor syndrome: rare",
        "Intrahepatic cholestasis: drug-induced, PBC, PSC",
        "Note: The bilirubin ratio is only an initial screening aid for differentiating jaundice; confirmation requires ALT/AST, ALP, GGT, and imaging (ultrasound/MRCP) judged together. In Gilbert syndrome, indirect bilirubin can rise further after fasting or stress. For clinical reference only.",
        "\U0001F4DA Deep Dive: Bilirubin (Direct/Indirect) Ratio and Jaundice Type Differentiation",
        "Finding the cause of jaundice: compute the direct bilirubin ratio from total and direct bilirubin to separate hemolytic / hepatocellular / obstructive",
        "Follow-up monitoring: track changes in the DBIL/TBIL ratio during hepatobiliary treatment to judge disease course",
        "Health-check interpretation: quickly separate Gilbert syndrome from cholestasis when a single bilirubin item is mildly elevated",
        "Algorithm: indirect bilirubin IBIL = TBIL \u2212 DBIL; direct bilirubin ratio = DBIL/TBIL\u00d7100% (capped at TBIL when DBIL>TBIL). Decision: TBIL\u2264reference (default 21 \u03bcmol/L) is normal; ratio <20% suggests indirect-predominant elevation (hemolysis/Gilbert); 20%~35% mixed (leaning hemolytic); 35%~60% hepatocellular jaundice; >60% obstructive jaundice (direct-predominant). Common differentiation directions and suggested tests (LDH, reticulocytes, Coombs, hepatitis markers, ALP/GGT, CA19-9, MRCP, etc.) are listed alongside.",
        "Example: TBIL 85 \u03bcmol/L, DBIL 55 \u03bcmol/L, reference 21 \u03bcmol/L \u2192 IBIL 30 \u03bcmol/L, direct bilirubin ratio 64.7%, judged obstructive jaundice (direct-predominant); ultrasound/MRCP is advised soon to localize the obstruction. If TBIL 120 \u03bcmol/L, DBIL 18 \u03bcmol/L \u2192 ratio 15.0%, judged indirect-predominant elevation (hemolytic/Gilbert); check LDH, reticulocytes, Coombs test, and UGT1A1 genotyping to exclude Gilbert syndrome.",
        "Does a ratio >60% always require surgery?",
        "The ratio only indicates cholestasis with direct bilirubin predominating, common in bile duct stones, cholangiocarcinoma, pancreatic head cancer, or intrahepatic cholestasis, but it cannot by itself decide the treatment plan. ALP/GGT, abdominal imaging (ultrasound/MRCP/CT), and tumor markers must be judged together, and hepatobiliary surgery or gastroenterology determines whether to intervene.",
        "Is Gilbert syndrome significant?",
        "Gilbert syndrome is a benign hereditary hyperbilirubinemia caused by partial deficiency of UGT1A1 enzyme activity, featuring mild indirect-predominant elevation with normal liver function and good prognosis, and generally needs no treatment. The key is to distinguish it from pathological elevation such as hemolysis or hepatitis, avoiding excessive testing.",
        "About the Direct/Indirect Bilirubin Ratio Calculator",
        "The Direct/Indirect Bilirubin Ratio Calculator computes indirect bilirubin and the ratio from total and direct bilirubin, aiding differential diagnosis of jaundice types." + DISCL_M,
    ]))
    write('calc-1', build('calc-1', [
        "\U0001F4CB Child-Pugh Liver Function Grading",
        "Assess hepatic functional reserve and surgical risk in cirrhosis patients.",
        "Assess hepatic functional reserve and surgical risk in cirrhosis patients. Computes professionally from the input parameters and outputs the result.",
        "Mild / controllable with medication",
        "Moderate-severe / refractory",
        "Grade I-II",
        "Grade III-IV",
        "\U0001F4DA Deep Dive: Child-Pugh Liver Function Grading (with unit conversion)",
        "Surgery",
        ": assess hepatic functional reserve and risk grading before abdominal surgery in cirrhosis patients",
        "Prognosis: give 1-year/2-year survival reference by grade to assist treatment decisions",
        "Follow-up stratification: recompute the score periodically to monitor the trend of liver function deterioration",
        "Algorithm (with",
        "): bilirubin mg = \u03bcmol/17.1, <2\u21921 point, \u22643\u21922, >3\u21923; albumin g/L = g/dL\u00d710, >35\u21921, \u226528\u21922, <28\u21923; INR <1.7\u21921, \u22642.3\u21922, >2.3\u21923; ascites (none/mild/moderate-severe) 1~3 points; hepatic encephalopathy (none/I-II/III-IV) 1~3 points. Total 5~15 points; 5~6 is grade A (1-year \u2248100%, 2-year \u224885%), 7~9 is grade B (1-year \u224880%, 2-year \u224860%), \u226510 is grade C (1-year \u224845%, 2-year \u224835%).",
        "Example: bilirubin 34 \u03bcmol/L (\u22481.99 mg\u21921 point), albumin 30 g/L (\u226528\u21922 points), INR 1.5 (<1.7\u21921 point), ascites 1 point, encephalopathy 1 point \u2192 total 6 points, grade A, well-compensated liver function. If bilirubin 85 \u03bcmol/L (\u22484.97 mg\u21923 points), albumin 25 g/L (<28\u21923 points), INR 2.5 (>2.3\u21923 points), ascites 2 points, encephalopathy 2 points \u2192 total 13 points, grade C, decompensated with major surgery contraindicated; evaluate for liver transplantation.",
        "Is grade A safe for surgery?",
        "Grade A indicates good hepatic functional reserve and tolerance for most elective surgeries, but albumin, prothrombin activity, and nutritional status must still be assessed together. In grade C (\u226510 points) major-surgery mortality rises markedly, so usually only emergency lifesaving surgery or transplant evaluation is performed.",
        "How to convert bilirubin units umol/L and mg/dL?",
        "1 mg/dL \u2248 17.1 \u03bcmol/L, and the tool has this conversion built in. Domestic reports mostly use \u03bcmol/L while European and American literature uses mg/dL; after conversion you can substitute the value directly into the score.",
        "How to use Child-Pugh Liver Function Grading",
        "What does Child-Pugh Liver Function Grading do?",
        "The Child-Pugh Liver Function Grading tool. Enter bilirubin, albumin, INR, and ascites/hepatic encephalopathy grades to compute a 5-15 point score and grade (A/B/C), assessing hepatic functional reserve and surgical risk in cirrhosis patients, for medical reference only.",
        "How to use Child-Pugh Liver Function Grading?",
        "Which scenarios suit Child-Pugh Liver Function Grading?",
        "e.g. 35",
        "e.g. 32",
        "e.g. 1.5",
    ]))

if __name__ == '__main__':
    main()
