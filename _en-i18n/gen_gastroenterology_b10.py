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
    write('nafld-fibroscan', build('nafld-fibroscan', [
        "\U0001F4CB Non-Alcoholic Fatty Liver Disease (NAFLD) FibroScan Assessor",
        "Assess fibrosis staging and steatosis degree from liver stiffness measurement (LSM) and controlled attenuation parameter (CAP).",
        "Assess fibrosis staging and steatosis degree from liver stiffness measurement (LSM) and controlled attenuation parameter (CAP). Computes professionally from the input parameters and outputs the result.",
        "NAFLD FibroScan Assessor",
        "/ NAFLD FibroScan Assessment",
        "\U0001F4D6 View the NAFLD FibroScan Fibrosis and Steatosis Assessment Usage Guide",
        "Liver stiffness measurement (LSM)",
        "LSM liver stiffness (kPa)",
        "Measurement validity",
        "Valid (IQR/median\u22640.3, \u226510 successful measurements)",
        "Reliability questionable",
        "Controlled attenuation parameter (CAP)",
        "CAP fat attenuation (dB/m)",
        "Probe transmit frequency",
        "M probe (standard adult)",
        "XL probe (obese patients)",
        "S probe (children/petite)",
        "\U0001F4CB NAFLD LSM fibrosis staging reference (M probe)",
        "Fibrosis stage",
        "F0-F1 (none/mild)",
        "Rule out significant fibrosis",
        "F2 (significant fibrosis)",
        "Needs attention, interventional treatment",
        "F3 (advanced fibrosis)",
        "Progressive fibrosis",
        "F4 (cirrhosis)",
        "Screen for complications",
        "NAFLD-specific thresholds. LSM<8 kPa rules out significant fibrosis (NPV>90%), LSM>15 kPa diagnoses cirrhosis (PPV>80%). The 8-15 kPa range is a gray zone; combining with serum scores such as FIB-4/NAST is recommended.",
        "\U0001F4CB CAP steatosis grading",
        "Steatosis",
        "Pathological grade",
        "No steatosis (S0)",
        "Fat <5%",
        "Mild (S1)",
        "Fat 5-33%",
        "Moderate (S2)",
        "Fat 33-66%",
        "Severe (S3)",
        "Fat >66%",
        "CAP thresholds differ slightly by device and probe. CAP can semi-quantitatively assess hepatic steatosis but cannot distinguish steatohepatitis (NASH) from simple fatty liver (NAFL).",
        "\U0001F4CA FIB-4 score",
        "FIB-4 = (age \u00D7 AST) / (platelets \u00D7 \u221AALT)",
        "<1.3: rules out significant fibrosis (NPV 90%), observation is fine",
        "1.3-2.67: gray zone, FibroScan assessment recommended",
        ">2.67: suggests significant fibrosis, liver biopsy recommended",
        "Note: FibroScan is an important non-invasive assessment tool for NAFLD. LSM assesses fibrosis degree, CAP assesses steatosis degree. BMI>30 kg/m\u00B2 suggests using the XL probe. ALT>5 times the upper limit of normal, cholestasis, and right heart failure can affect LSM accuracy. For clinical reference only.",
        "\U0001F4DA Deep Dive: NAFLD FibroScan Fibrosis and Steatosis Assessment",
        "Fibrosis staging: determine F0-F4 from LSM (kPa), distinguishing cirrhosis",
        "Steatosis grading: determine S0-S3 from CAP (dB/m), guiding weight loss and medication",
        "Combined judgment: LSM\u226515 is managed directly as F4, screening for varices and hepatocellular carcinoma",
        "Algorithm: LSM <8kPa \u2192 F0-F1 (significant fibrosis ruled out, NPV>90%), 8~10 \u2192 F2, 10~15 \u2192 F3, \u226515kPa \u2192 F4 (cirrhosis); CAP <248 \u2192 S0, 248~269 \u2192 S1, 269~295 \u2192 S2, \u2265295 dB/m \u2192 S3. AST/PLT >0.15 suggests FIB-4 may be elevated; complete calculation is recommended. When the measurement is invalid (IQR/median>0.3) the result is questionable and retesting is needed.",
        "Example: LSM 7.0 kPa, CAP 240 dB/m \u2192 F0-F1 (significant fibrosis ruled out), S0 (no steatosis), low hepatic steatosis risk, health follow-up suffices. If LSM 18.0 kPa, CAP 310 dB/m \u2192 F4 (cirrhosis), S3 (severe steatosis); completing blood count/coagulation/ultrasound to assess complications, gastroscopy for varices, and ultrasound + AFP every 6 months for HCC screening are advised.",
        "What makes LSM read falsely high?",
        "Acute hepatitis, hepatic congestion (right heart failure), cholestasis, postprandial state, and thick subcutaneous fat in obesity can all falsely raise LSM; reliable results require \u226510 valid consecutive measurements on the same slice with IQR/median \u22640.3. When questionable, combine with FIB-4, APRI, and imaging.",
        "Can CAP replace biopsy for assessing steatosis?",
        "CAP non-invasively reflects the degree of hepatic steatosis and correlates well with controlled attenuation, but it is affected by the probe type (M/XL) and inflammation, and cannot replace biopsy assessment of inflammation and ballooning (NASH activity). S3 warrants active weight loss and metabolic management.",
        "About the NAFLD FibroScan Assessor",
        "The Non-Alcoholic Fatty Liver Disease (NAFLD) FibroScan Assessor evaluates liver fibrosis degree and steatosis degree from liver stiffness measurement (LSM) and controlled attenuation parameter (CAP)." + DISCL_M,
    ]))
    write('saag-ascites', build('saag-ascites', [
        "\U0001FA7B Ascites SAAG (Serum-Ascites Albumin Gradient) Differentiator",
        "Compute the SAAG value to differentiate portal hypertensive from non-portal hypertensive ascites.",
        "Ascites SAAG Differentiator",
        "/ SAAG Ascites Differentiation",
        "\U0001F4D6 View the Ascites SAAG (Serum-Ascites Albumin Gradient) Differentiator Usage Guide",
        "SAAG = serum albumin \u2212 ascites albumin (g/L)",
        "Ascites albumin (g/L)",
        "Compute SAAG",
        "\U0001F4CB SAAG computation and interpretation",
        "Sampling requirement: draw blood and ascites samples on the same day. Note: testing immediately after albumin infusion is unsuitable; an interval of \u226524 hours is required.",
        "Portal hypertensive",
        "High SAAG, increased portal pressure",
        "Non-portal hypertensive",
        "Low SAAG, normal portal pressure",
        "SAAG accuracy is high (about 97%), replacing the traditional exudate/transudate classification.",
        "\U0001F4CA Common causes of high SAAG (\u226511)",
        "Cirrhosis (most common, about 80%)",
        "Fulminant hepatic failure",
        "Budd-Chiari syndrome",
        "Right heart failure / constrictive pericarditis",
        "Portal vein thrombosis",
        "\U0001F4CA Common causes of low SAAG (<11)",
        "Peritoneal carcinomatosis (ovarian cancer, gastric cancer, etc.)",
        "Tuberculous peritonitis",
        "Nephrotic syndrome",
        "Pancreatic ascites",
        "Biliary ascites",
        "Malnutrition-related (hypoproteinemia)",
        "Note: SAAG is an important indicator for differentiating the cause of ascites, but it must be combined with ascites routine, cytology, ADA, amylase, culture, etc. High SAAG + high total ascites protein suggests a cardiac or Budd-Chiari cause. For clinical reference only.",
        "\U0001F4DA Deep Dive: Ascites SAAG (Serum-Ascites Albumin Gradient) Differentiation",
        "Nature differentiation: use SAAG to distinguish portal hypertensive from non-portal hypertensive ascites",
        "Etiology narrowing: for portal hypertension, combine total ascites protein to determine hepatic/cardiac/Budd-Chiari origin",
        "Sampling discipline: sample on the same day, and retest after an interval following albumin infusion",
        "Algorithm: SAAG = serum albumin \u2212 ascites albumin (g/L). \u226511 g/L indicates portal hypertensive ascites (cirrhosis about 80%, Budd-Chiari, right heart failure, portal vein thrombosis, fulminant hepatic failure); <11 g/L indicates non-portal hypertensive (peritoneal carcinomatosis, tuberculous peritonitis, nephrotic syndrome, pancreatic, biliary). Portal hypertension with total ascites protein <25 mostly cirrhosis, \u226525 requires ruling out cardiac/Budd-Chiari. Sampling requires serum and ascites collected together with no albumin infusion.",
        "Example: serum albumin 28 g/L, ascites albumin 12 g/L \u2192 SAAG = 16.0 g/L (\u226511), portal hypertensive ascites; with low total ascites protein it leans toward cirrhosis, so liver function plus abdominal ultrasound is advised. If serum 30 g/L, ascites 25 g/L \u2192 SAAG = 5.0 g/L (<11), non-portal hypertensive; ascites cytology/ADA/amylase is advised to exclude malignancy, tuberculosis, or pancreatic origin.",
        "Why does albumin infusion affect SAAG?",
        "Albumin infusion raises serum albumin and artificially widens the gradient, creating a false impression of portal hypertension. Therefore serum and ascites should be collected together when no albumin has been infused, or retested after a sufficient interval following infusion, otherwise the result is unreliable.",
        "Does SAAG\u226511 always mean cirrhosis?",
        "Not necessarily. SAAG\u226511 only indicates the presence of portal hypertension, most commonly cirrhosis, but it is also seen in Budd-Chiari syndrome, right heart failure, portal vein thrombosis, and fulminant hepatic failure. Total ascites protein, cardiac ultrasound, abdominal imaging, and history are needed to pin down the cause.",
        "About the Ascites SAAG Differentiator",
        "The Ascites SAAG (serum-ascites albumin gradient) differentiator computes the SAAG value to differentiate portal hypertensive from non-portal hypertensive ascites." + DISCL_M,
    ]))
    write('stool-occult-quant', build('stool-occult-quant', [
        "\U0001FA7B Stool Occult Blood (Quantitative) and Calprotectin Assessor",
        "Combined interpretation of FIT quantitative values and fecal calprotectin to assess colorectal tumor and intestinal inflammation risk.",
        "Stool Occult Blood Quantitative and Calprotectin Assessor",
        "/ Occult Blood and Calprotectin Assessment",
        "Fecal immunochemical test (FIT): <10 negative, 10\u201320 borderline, 20\u2013100 positive, \u2265100 strongly positive; combined with age and fecal calprotectin (FC) to assess colorectal lesion risk.",
        "FIT (immunochemical fecal occult blood test)",
        "FIT value (\u03BCg/g)",
        "Fecal calprotectin (FC)",
        "Fecal calprotectin (\u03BCg/g)",
        "Test indication",
        "Screening (asymptomatic)",
        "IBD follow-up",
        "IBS differentiation",
        "\U0001F4CB FIT quantitative reference ranges",
        "Routine screening interval",
        "Pay attention, assess with age",
        "Colonoscopy recommended",
        "Colonoscopy as soon as possible",
        "The FIT positive threshold varies by manufacturer (10-20 \u03BCg/g), and the positive predictive value rises with age. FIT is immunological, specifically detecting human hemoglobin, and is unaffected by animal hemoglobin or iron supplements.",
        "\U0001F4CB Fecal calprotectin reference ranges",
        "No intestinal inflammation",
        "Mild inflammation, etiology differentiation needed",
        "Suggests IBD, colonoscopy recommended",
        "Strongly suggests active IBD",
        "FC is a neutrophil-derived calcium-binding protein reflecting the degree of intestinal inflammation. It is unaffected by upper GI bleeding (degraded) and reflects lower GI inflammation more specifically than FIT.",
        "\U0001F4CA Combined interpretation strategy",
        "FIT positive + FC normal",
        ": indicates GI bleeding without marked inflammation; prioritize ruling out tumor/polyp",
        "FIT negative + FC elevated",
        ": indicates intestinal inflammation; prioritize ruling out IBD",
        "FIT positive + FC elevated",
        ": inflammatory bowel disease with bleeding or tumor with inflammation; colonoscopy needed to clarify",
        "FIT negative + FC normal",
        ": low risk, routine follow-up",
        "Note: FIT and FC are complementary non-invasive markers. FIT sensitively detects lower GI bleeding (colorectal tumor screening), while FC specifically reflects intestinal inflammation (IBD screening and follow-up). Combining the two improves differentiation efficiency. For clinical reference only.",
        "\U0001F4DA Deep Dive: Fecal Occult Blood (FIT) Quantitation and Calprotectin Combined Interpretation",
        "Colorectal cancer screening: FIT positive prioritizes ruling out colorectal tumor/polyp",
        "IBD differentiation: FIT negative with high calprotectin indicates intestinal inflammation",
        "Combined decisions: both positive warrants colonoscopy soon, both negative is low risk",
        "Algorithm: FIT <10 \u2192 negative, 10~20 \u2192 borderline, 20~100 \u2192 positive, \u2265100 \u03BCg/mL \u2192 strongly positive; fecal calprotectin (FC) <50 \u2192 normal, 50~200 \u2192 mildly elevated, 200~500 \u2192 moderate, \u2265500 \u03BCg/g \u2192 markedly elevated. Combined: FIT\u226520 and FC<50 \u2192 bleeding positive, inflammation negative (prioritize tumor); FIT<10 and FC\u2265200 \u2192 bleeding negative, inflammation positive (prioritize IBD); FIT\u226520 and FC\u2265200 \u2192 both positive (clarify with colonoscopy); both negative \u2192 low risk.",
        "Example: FIT 150 \u03BCg/mL (strongly positive), FC 300 \u03BCg/g (moderately elevated) \u2192 both positive, possibly IBD with bleeding or tumor with inflammation; prompt full colonoscopy plus biopsy is advised. If FIT 5 (negative), FC 300 (elevated) \u2192 bleeding negative, inflammation positive, indicating intestinal inflammation (not supporting IBS); colonoscopy plus biopsy to exclude IBD is advised. If FIT 50, FC 120 \u2192 both borderline (positive/mild); recheck in 2~4 weeks, and if persistently elevated, perform colonoscopy.",
        "Can FIT and calprotectin substitute for each other?",
        "No. FIT reflects lower GI bleeding (tumor/polyp/active inflammation can all be positive), while calprotectin reflects intestinal neutrophil inflammation (sensitive for IBD). The two complement each other: strongly positive FIT prioritizes tumor workup, and high calprotectin with negative FIT prioritizes IBD workup.",
        "Does a positive FIT mean cancer?",
        "No. Polyps, hemorrhoids, colitis, ulcers, even diet and medications can raise FIT. But a positive FIT (especially \u226520) counts as a positive colorectal cancer screening result and requires colonoscopy confirmation per protocol; follow-up alone is not acceptable.",
        "About the Stool Occult Blood Quantitative and Calprotectin Assessor",
        "The Stool Occult Blood quantitative and fecal calprotectin assessor takes FIT and fecal calprotectin values to assess GI bleeding and intestinal inflammation risk." + DISCL_M,
    ]))

if __name__ == '__main__':
    main()
