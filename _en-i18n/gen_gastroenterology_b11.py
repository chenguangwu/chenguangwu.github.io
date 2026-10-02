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
def main():
    write('index', build('index', [
        "\U0001FA7B Gastroenterology Tools",
        "Gastroenterology",
        "Gastroenterology Tools",
        "Capsule Endoscopy Bowel Transit Time Calculator",
        "Capsule Endoscopy (Intestinal Transit Time) Calculator",
        "Direct/Indirect Bilirubin Ratio Calculator",
        "Crohn's Disease CDAI Activity Index Calculator",
        "Crohn's Disease CDAI Activity Index Calculator",
        "Child-Pugh Liver Function Grading",
        "The Child-Pugh Liver Function Grading tool. Enter bilirubin, albumin, INR, and ascites/hepatic encephalopathy grades to compute a 5\u201315 point score and grade (A/B/C), assessing hepatic functional reserve and surgical risk in cirrhosis patients, for medical reference only.",
        "Intestinal Metaplasia Atrophy Extent Assessor",
        "Based on the OLGIM staging system, assess the extent of gastric mucosal intestinal metaplasia and stratify gastric cancer risk, aiding clinical follow-up decisions.",
        "NAFLD FibroScan Assessor",
        "Non-Alcoholic Fatty Liver Disease (NAFLD) FibroScan Assessor",
        "Liver Function Child-Pugh Grading Tool",
        "Liver Function Child-Pugh Grading Tool",
        "Pancreatitis Glasgow Severity Assessor",
        "Acute Pancreatitis Glasgow Severity Assessor",
        "Gastroscopy Image Recognition Reference",
        "Gastroscopy (Gastritis/Ulcer) Image Recognition Reference",
        "The H. pylori antibiotic resistance detection tool. Evaluates the resistance pattern from susceptibility results of 6 common antibiotics (such as clarithromycin and amoxicillin), outputting detection analysis and medication guidance, for medical reference only.",
        "IBD Nutrition Risk Screener",
        "IBD nutrition risk screening based on a modified NRS-2002, assessing nutritional status and nutrition support needs",
        "Esophageal Varices Bleeding Risk Assessor",
        "ERCP Stone Removal and Stent Success Probability Assessor",
        "ERCP (Stone Removal/Stent) Success Probability Assessor",
        "Stool Occult Blood Quantitative and Calprotectin Assessor",
        "Gastrointestinal Motility Gastric Emptying Tester",
        "Enter radionuclide gastric emptying scan retention rates at each time point to compute the gastric half-emptying time (GET1/2) and emptying rate, assessing gastric motility function such as gastroparesis, for dyspepsia diagnosis.",
        "Hp Breath Test DOB Value Interpreter",
        "H. pylori Antibiotic Resistance Reference",
        "H. pylori (Antibiotic) Resistance Reference",
        "Hepatic Encephalopathy West Haven Grading Tool",
        "Hepatic Encephalopathy (West Haven Grading) Tool",
        "Gastrin Normal Range Assessor",
        "Gastrin Normal Range Assessor",
        "Ascites SAAG Differentiator",
        "Ulcerative Colitis Mayo Score Tool",
        "Ulcerative Colitis Mayo Score Tool",
        "Colonoscopy Adenoma/Polyp Classification Reference",
        "Colonoscopy (Adenoma/Polyp) Classification Reference",
        "About the Gastroenterology Tools",
        "The Gastroenterology Tools collection includes 22 free online tools covering common calculation, conversion, and lookup needs in gastroenterology scenarios. Whether you are a practitioner, student, or general user in the field, you can find ready-to-use practical tools here. All tools run purely in the frontend, with no data uploaded to servers, protecting your privacy and security.",
        "The gastroenterology tools on this page include (representative tools):",
        "These tools help you quickly complete common gastroenterology-related tasks without memorizing complex formulas or manual conversions; just input and get results.",
        "Do the gastroenterology tools need to be downloaded or registered?",
        "No. All gastroenterology tools on this page are pure-frontend online tools; open the page and use them directly, with no software installation, no account registration, and no data upload.",
        "Are the calculation results of the gastroenterology tools accurate? Is the data secure?",
        "The tools compute locally in your browser based on public mathematical formulas and general industry standards, with instant results. All calculations are completed locally on your device, and data is never uploaded to servers, ensuring privacy and security.",
    ]))

if __name__ == '__main__':
    main()
