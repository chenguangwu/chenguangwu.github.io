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
    write('detector-7', build('detector-7', [
        "\U0001F48A Helicobacter pylori (Antibiotic) Resistance Detection",
        "Antibiotic",
        "H. pylori resistance guidance: count resistant antibiotics from susceptibility results; no resistance \u2192 standard bismuth quadruple therapy; 1\u20132 resistances \u2192 avoid that drug and adjust the regimen; multi-resistance \u2192 choose a regimen containing furazolidone/tetracycline.",
        "H. pylori antibiotic resistance detection analysis (6 common antibiotics)",
        "1. Clarithromycin",
        "2. Amoxicillin",
        "3. Metronidazole",
        "4. Levofloxacin",
        "5. Tetracycline",
        "6. Furazolidone",
        "Previous eradication attempts",
        "Analyze resistance",
        "\U0001F4DA Deep Dive: H. pylori Antibiotic Resistance Detection and Regimen Recommendation",
        "Susceptibility interpretation: assess the resistance pattern from susceptibility results of 6 common antibiotics",
        "First-line selection: avoid resistant drugs on initial treatment, prefer bismuth quadruple therapy",
        "Refractory management: multi-resistance or repeated failures should switch to susceptibility-guided individualized therapy",
        "Algorithm: for the 6 antibiotics (clarithromycin/amoxicillin/metronidazole/levofloxacin/tetracycline/furazolidone) record susceptible 0 or resistant 1; resistance count 0 \u2192 standard bismuth quadruple therapy (eradication rate >90%); 1~2 without clarithromycin and without amoxicillin \u2192 quadruple therapy containing susceptible drugs; with clarithromycin and without amoxicillin \u2192 clarithromycin-free regimen (switch to tetracycline/furazolidone); \u22653 \u2192 multi-resistance needing individualized therapy; previous failures \u22652 \u2192 precision therapy under susceptibility guidance.",
        "Example: clarithromycin resistant, metronidazole resistant, the rest susceptible (2 resistances) \u2192 take the clarithromycin-free route; bismuth quadruple therapy (PPI + bismuth + amoxicillin + tetracycline or furazolidone) for 14 days is recommended. If clarithromycin + amoxicillin + metronidazole are all resistant (3 resistances) \u2192 multi-resistance; susceptibility testing is advised, choosing a tetracycline/furazolidone combination or high-dose dual therapy extended to 14 days, with Chinese herbal adjunct if necessary.",
        "Why is bismuth quadruple therapy emphasized now?",
        "As clarithromycin and metronidazole resistance rates rise, the eradication rate of classic triple therapy has fallen below 70%~80%. Bismuth quadruple therapy (PPI + bismuth + 2 antibiotics, 14 days) overcomes part of the resistance, and domestic consensus puts eradication at 85%~90%, making it the preferred regimen.",
        "Is amoxicillin resistance common?",
        "Primary H. pylori resistance to amoxicillin is very low (often <5% domestically), so most regimens keep amoxicillin; only penicillin-allergic patients switch to tetracycline/furazolidone, which clearly limits regimen choice.",
        "About the H. pylori (Antibiotic) Resistance Detection",
        "The H. pylori (Antibiotic) Resistance Detection. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
        "How to use the H. pylori (Antibiotic) Resistance Detection",
        "What does the H. pylori (Antibiotic) Resistance Detection do?",
        "The H. pylori antibiotic resistance detection tool. Evaluates the resistance pattern from susceptibility results of 6 common antibiotics (such as clarithromycin and amoxicillin), outputting detection analysis and medication guidance, for medical reference only.",
        "How to use the H. pylori (Antibiotic) Resistance Detection?",
        "Which scenarios suit the H. pylori (Antibiotic) Resistance Detection?",
    ]))
    write('ercp-success', build('ercp-success', [
        "\U0001F4CB ERCP (Stone Removal/Stent) Success Probability Assessor",
        "Assess the success probability of ERCP stone removal and stent placement based on procedural difficulty factors.",
        "Assess the success probability of ERCP stone removal and stent placement based on procedural difficulty factors. Computes professionally from the input parameters and outputs the result.",
        "ERCP Stone Removal and Stent Success Probability Assessor",
        "/ ERCP Success Probability Assessment",
        "Stone/obstruction related factors",
        "Maximum stone diameter (mm)",
        "Number of stones",
        "Single",
        "2-3 stones",
        "\u22654 stones",
        "Distal common bile duct",
        "Middle common bile duct",
        "Proximal common bile duct / hilum",
        "Intrahepatic bile duct",
        "Purpose of procedure",
        "Stone removal",
        "Stenting for benign stricture",
        "Stenting for malignant obstruction",
        "Patient and anatomic factors",
        "Common bile duct diameter (mm)",
        "History of gastric surgery",
        "Billroth II anastomosis",
        "Roux-en-Y anastomosis",
        "History of ERCP sphincterotomy",
        "Yes (EST already performed)",
        "Duodenal papilla diverticulum",
        "Assess success rate",
        "\U0001F4CB ERCP difficulty grading (simplified Cotton criteria)",
        "Procedure type",
        "Estimated success rate",
        "Grade 1 (standard)",
        "Biliary duct cannulation, standard stone removal (<10mm), single plastic stent",
        "Grade 2 (advanced)",
        "Large stone (\u226510mm) removal, multiple stones, dual stent placement",
        "Grade 3 (complex)",
        "Intrahepatic bile duct stone removal, malignant stricture stenting, peripapillary diverticulum",
        "Success rate is jointly influenced by operator experience, equipment conditions, and patient anatomic factors.",
        "\U0001F4CA Factors affecting ERCP success",
        "Unfavorable factors",
        "Stone >15mm (requires mechanical or laser lithotripsy)",
        "Impacted stone or high position (intrahepatic bile duct)",
        "Post Billroth II / Roux-en-Y (difficult cannulation)",
        "Periampullary duodenal diverticulum (changed cannulation direction)",
        "Distal biliary stricture",
        "Previous difficult or failed ERCP",
        "Adjunct techniques",
        "EUS-guided biliary drainage (EUS-BD): when cannulation is difficult",
        "Peroral cholangioscopy (SpyGlass): lithotripsy under direct vision",
        "Balloon dilation (EPBD): assists stone removal",
        "Precut (needle-knife/short guidewire): when cannulation is difficult",
        "Note: ERCP is an important diagnostic and therapeutic tool for biliary-pancreatic disease, but it is a high-difficulty procedure with a complication rate of about 5-10% (pancreatitis, bleeding, perforation, infection). High-difficulty cases should be referred to experienced centers or consider alternatives such as EUS-BD. For clinical reference only.",
        "\U0001F4DA Deep Dive: ERCP Stone Removal/Stent Success Probability Assessment",
        "Preoperative decision: estimate procedural difficulty from stone size, number, location, and anatomic factors",
        "Risk disclosure: explain the estimated success rate and possible adjunct techniques to the patient",
        "Referral judgment: complex difficulty should be referred to a high-volume center or use EUS assistance",
        "Algorithm (stone removal): stone >15mm\u2192+3 (lithotripsy needed), 10~15mm\u2192+2, <10mm\u2192+1; number \u22654\u2192+2, 2~3\u2192+1, single\u21920; location intrahepatic\u2192+3, proximal CBD/hilum\u2192+2, middle\u2192+1, distal\u21920; benign stricture stent +3, malignant obstruction +2; post Roux-en-Y +3, Billroth II +2; periampullary diverticulum +1; EST already performed \u22121 (take 0 when difficulty <0). Difficulty \u22642 \u2192 grade 1 (success 90~95%), \u22645 \u2192 grade 2 (80~90%), >5 \u2192 grade 3 (60~80%).",
        "Example: middle CBD stone 12mm, 2~3 stones, no surgical history \u2192 +2+1+1 = difficulty 4, grade 2 (estimated success 80~90%), routine EST + basket extraction. If intrahepatic bile duct stone 20mm, \u22654 stones, post Roux-en-Y, with diverticulum \u2192 +3+2+3+3+1 = difficulty 12, grade 3 (60~80%); a high-volume center or EUS-BD/SpyGlass direct vision with staged procedures is advised.",
        "Does grade 3 difficulty mean ERCP cannot be done?",
        "It is not that it cannot be done, but the success rate drops to 60%~80% with higher complication risk, so it needs an experienced endoscopist or referral. EUS-guided puncture, peroral cholangioscopy (SpyGlass) for direct-vision lithotripsy, and balloon-assisted endoscopy can raise the success rate.",
        "Why does EST lower the difficulty?",
        "Endoscopic sphincterotomy (EST) dilates the papillary opening so the extraction basket/balloon can pass, hence EST already performed scores \u22121. But for patients not yet cut, the first cut itself also counts toward difficulty, so comprehensive assessment is needed.",
        "About the ERCP Stone Removal and Stent Success Probability Assessor",
        "The ERCP stone removal and stent success probability assessor evaluates ERCP procedural difficulty and success rate based on factors such as bile duct stone size, number, location, and anatomy." + DISCL_M,
    ]))

if __name__ == '__main__':
    main()
