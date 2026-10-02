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
    write('hp-resistance', build('hp-resistance', [
        "\U0001F48A H. pylori (Antibiotic) Resistance Reference",
        "Quick reference for H. pylori common antibiotic resistance rates and eradication regimen selection.",
        "H. pylori Antibiotic Resistance Reference",
        "/ Hp Resistance Reference",
        "Clarithromycin susceptibility result",
        "Metronidazole susceptibility result",
        "Levofloxacin susceptibility result",
        "Previous eradication history",
        "Initial treatment",
        "1 previous failure",
        "\u22652 previous failures",
        "Penicillin allergy",
        "Bismuth available",
        "\U0001F4CB H. pylori common antibiotic resistance rates (China data)",
        "Resistance rate",
        "Resistance mechanism",
        "Clarithromycin",
        "23S rRNA mutation",
        "Resistance markedly lowers eradication rate",
        "rdxA/nifA gene mutation",
        "Resistance rate high, but bismuth quadruple therapy can overcome it",
        "Levofloxacin",
        "gyrA gene mutation",
        "Second-line/third-line drug",
        "pbpA gene mutation",
        "Resistance rate extremely low, first choice",
        "Tetracycline",
        "16S rRNA mutation",
        "Resistance rate extremely low, but hard to obtain",
        "Furazolidone",
        "Rare detoxifying enzyme mutation",
        "Second-line drug, watch for side effects",
        "Resistance rates vary greatly by region; refer to local resistance surveillance data. When clarithromycin resistance exceeds 15%, clarithromycin-containing triple therapy should not be used.",
        "\U0001F4CA Common eradication regimens",
        "First-line regimens",
        "Bismuth quadruple therapy",
        "(recommended): PPI bid + bismuth bid + amoxicillin 1g bid + clarithromycin 0.5g bid, 14 days",
        "High-dose dual therapy",
        ": PPI bid/qid + amoxicillin 1g tid/bid, 14 days",
        "Concomitant therapy",
        ": PPI bid + amoxicillin 1g bid + clarithromycin 0.5g bid + metronidazole 0.4g bid/tid, 14 days",
        "Second-line/salvage regimens",
        "Levofloxacin-containing quadruple therapy",
        ": PPI + bismuth + amoxicillin + levofloxacin, 14 days",
        "Furazolidone-containing quadruple therapy",
        ": PPI + bismuth + amoxicillin + furazolidone, 14 days",
        "Tetracycline-containing quadruple therapy",
        ": PPI + bismuth + tetracycline + metronidazole/furazolidone, 14 days",
        "Note: Clarithromycin resistance is the main cause of eradication failure. Individualized treatment guided by susceptibility testing can raise the eradication rate. Those with repeated failures should undergo susceptibility testing or whole-genome resistance detection. For clinical reference only.",
        "\U0001F4DA Deep Dive: H. pylori Resistance Regimen Recommendation (Reference)",
        "Susceptibility-guided: choose the regimen from clarithromycin/metronidazole/levofloxacin resistance status and penicillin allergy",
        "Initial treatment: prefer bismuth quadruple therapy for 14 days, avoiding resistant drugs",
        "Refractory cases: those with repeated failures should undergo susceptibility testing to guide individualized therapy",
        "Algorithm: penicillin allergy with bismuth available \u2192 bismuth quadruple therapy (PPI + bismuth + tetracycline + metronidazole, or clarithromycin + metronidazole as substitute); initial treatment with clarithromycin resistance \u2192 clarithromycin-free bismuth quadruple therapy / high-dose dual therapy; metronidazole resistance can be overcome by bismuth quadruple therapy; 1 previous failure with levofloxacin susceptibility \u2192 levofloxacin-containing quadruple therapy; \u22652 failures \u2192 tetracycline/furazolidone regimen or susceptibility-guided therapy. All courses are 14 days.",
        "Example: penicillin allergy, bismuth available, clarithromycin susceptible \u2192 bismuth quadruple therapy (PPI + bismuth + tetracycline 500mg qid + metronidazole 0.4g tid) for 14 days. If initial treatment, clarithromycin resistant, metronidazole susceptible, no bismuth \u2192 avoid clarithromycin and choose concomitant therapy (PPI + amoxicillin + metronidazole + ...) or high-dose dual therapy (esomeprazole 40mg qid + amoxicillin 1g tid) for 14 days.",
        "Why is high-dose dual therapy valued now?",
        "High-dose dual therapy (double-dose PPI + high-dose amoxicillin, often qid/tid) raises the intragastric amoxicillin concentration through sustained acid suppression, achieving an eradication rate around 90%, with few antibiotics and few side effects, suiting those who cannot use bismuth or have complex resistance.",
        "What special precautions apply to furazolidone?",
        "Furazolidone can cause a disulfiram-like reaction (no alcohol during treatment); long-term use risks peripheral neuropathy. The dose is usually 0.1g bid for 14 days; use cautiously with abnormal liver or kidney function and under physician guidance.",
        "About the H. pylori Antibiotic Resistance Reference",
        "The H. pylori antibiotic resistance reference provides resistance rates for common antibiotics such as clarithromycin, amoxicillin, and metronidazole, plus eradication regimen selection reference." + DISCL_M,
    ]))
    write('ibd-nutrition', build('ibd-nutrition', [
        "\U0001F957 IBD (Nutrition Risk) Screener",
        "IBD nutrition risk screening based on a modified NRS-2002, assessing nutritional status and nutrition support needs.",
        "Core formula (by input variables): max(diseaseScore,1); max(diseaseScore,2); max(nutriScore,2)",
        "IBD Nutrition Risk Screener",
        "/ IBD Nutrition Screening",
        "Disease severity score",
        "IBD activity",
        "Remission phase",
        "Disease extent",
        "Limited (E1/U1)",
        "Extensive (E3/U3)",
        "Total colon/total small bowel",
        "Nutritional status score",
        "Weight loss in the last 3 months (%)",
        "Dietary intake (versus usual)",
        "Reduced by 25-50%",
        "Reduced by 50-75%",
        "Reduced by >75% or almost no eating",
        "Age bonus",
        "Complications",
        "Fistula/abscess",
        "Short bowel syndrome/obstruction",
        "Assess nutrition risk",
        "\U0001F4CB NRS-2002 scoring criteria",
        "Nutritional status",
        "Disease severity",
        "1 point (mild)",
        "BMI 18.5-20.5 + poor general condition / intake reduced 25-50%",
        "Acute exacerbation of chronic disease",
        "2 points (moderate)",
        "BMI 17-18.5 / 3-month weight loss 5% / intake reduced 50-75%",
        "Major abdominal surgery / severe pneumonia",
        "3 points (severe)",
        "BMI <17 / 3-month weight loss >10% / intake reduced >75%",
        "Head injury / intensive care",
        "A total score \u22653 indicates nutrition risk and requires a nutrition support plan. Age \u226570 adds 1 point.",
        "\U0001F4CA Characteristics of malnutrition in IBD",
        "Malnutrition incidence in CD is higher than UC (30-50% vs 5-10%)",
        "Common deficiencies: iron, vitamin B12, folate, zinc, vitamin D",
        "Small-bowel involvement in CD more often causes malabsorption and micronutrient deficiency",
        "Growth failure is an important manifestation in children and adolescents with IBD",
        "Malnutrition increases surgical complication and infection risk",
        "\U0001F4CA Nutrition support strategies",
        "Mild malnutrition",
        ": dietary guidance + oral nutrition supplementation (ONS)",
        "Moderate malnutrition",
        ": mainly ONS, enteral nutrition (EN) if needed",
        "Severe malnutrition",
        ": enteral nutrition (EN) is first choice, combine PN if needed",
        "CD active phase",
        ": exclusive enteral nutrition (EEN) can induce remission (especially in children/adolescents)",
        "Perioperative period",
        ": nutritional support 7-14 days before surgery lowers complications",
        "Note: IBD patients should routinely undergo nutrition screening. CD patients, those with extensive disease, and those in the active phase carry higher nutrition risk. Iron and vitamin B12 deficiency need regular monitoring and supplementation. Enteral nutrition is superior to parenteral nutrition. For clinical reference only.",
        "\U0001F4DA Deep Dive: IBD Nutrition Risk Screening (Modified NRS-2002)",
        "Nutrition screening: assess nutrition risk level in the IBD active phase / perioperative period",
        "Support plan: formulate ONS/EN/PN plans for moderate-to-high risk",
        "Micronutrient correction: supplement iron, B12, folate, vitamin D",
        "Algorithm: nutritional status takes the highest item \u2014",
        "<17\u21923, 17~18.5\u21922, 18.5~20.5\u21921 point; weight loss >10%\u21923, 5~10%\u21922, <5%\u21921 point; intake reduced >75%\u21923, 50~75%\u21922, 25~50%\u21921 point; albumin <30\u2192+2, 30~35\u2192+1 point. Disease severity (activity 1~3 + extent + complications) 0~3 points; age \u226570 adds 1 point. Total \u22655 severe, \u22653 moderate, <3 low nutrition risk.",
        "Example: BMI 18.5, weight loss 8%, albumin 32 g/L, intake reduced 25~50%, mild activity, limited disease, no complications, age 45 \u2192 nutrition 2 (weight loss) + disease 1 + age 0 = 3 points, moderate nutrition risk; mainly ONS is advised. If BMI 16, weight loss 12%, albumin 28, intake reduced >75%, severe activity, total colon, 2 complications, age 45 \u2192 nutrition 3 + disease 3 + age 0 = 6 points, severe nutrition risk; early EN (PN if necessary) is advised, and CD should consider EEN to induce remission.",
        "Should IBD patients follow a low-fiber diet?",
        "No strict fiber restriction is needed in remission; during the active phase or with stricturing/penetrating lesions, a low-residue diet reduces stool irritation. Nutrition support should first guarantee energy 25~30 kcal/kg/d and protein 1.0~1.5 g/kg/d rather than blindly fasting.",
        "Why check albumin during the active phase?",
        "Albumin reflects both inflammatory and nutritional status, and in the IBD active phase it often falls due to inflammatory consumption and intestinal loss; <30 g/L indicates moderate-to-severe nutrition risk, requiring active supplementation, and only controlling inflammation can fundamentally improve it.",
        "About the IBD Nutrition Risk Screener",
        "The IBD nutrition risk screener, based on NRS-2002 and IBD-specific nutrition assessment, evaluates nutrition risk and nutrition support needs in patients with inflammatory bowel disease." + DISCL_M,
    ]))

if __name__ == '__main__':
    main()
