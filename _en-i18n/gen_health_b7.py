#!/usr/bin/env python3
# health batch7 (2 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'health')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'health')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'waist-hip-ratio': [
"🧮 Waist-to-Hip Ratio (WHR) Calculator",
"Calculate the waist-to-hip ratio and assess central obesity and cardiovascular risk",
"Waist-to-Hip Ratio Calculator",
"/ Waist-to-Hip Ratio Calculator",
'📖 View the "Waist-to-Hip Ratio Calculator User Guide"',
"WHR = waist ÷ hip",
"Central obesity cutoffs: men ≥ 0.90, women ≥ 0.85",
"👨 Male",
"👩 Female",
"Height (cm, optional)",
"Please enter waist and hip measurements",
"Waist-to-height ratio",
"📋 Details",
"Assessment standard",
"Health risk",
"Measurement guide",
"🏥 WHO waist-to-hip ratio standard",
"WHR range",
"Apple-shape obesity risk low",
"Tendency to central obesity",
"Apple-shape obesity",
"Pear shape, lower risk",
"📏 Waist-to-height ratio (WHtR) standard",
"WHtR range",
"Metabolic syndrome risk low",
"Metabolic syndrome high risk",
"💡 Why does waist-to-hip ratio matter?",
"The waist-to-hip ratio is an important indicator for assessing",
"fat distribution type",
". An \"apple\" shape (thick waist, thin hips) carries higher cardiovascular and diabetes risk than a \"pear\" shape (thin waist, thick hips), because abdominal (visceral) fat is metabolically active and more readily causes insulin resistance and inflammation.",
"Enter data to view the health risk assessment",
"📏 How to measure your waist correctly",
"Measurement steps:",
"1. Measure on an empty stomach or 2 hours after a meal",
"2. Stand upright and breathe naturally; do not suck in or push out your belly",
"3. Wrap the tape horizontally around your waist at the navel",
"4. Keep the tape against the skin without pressing into the soft tissue",
"5. Read at the end of an exhale, to the nearest 0.1 cm",
"• Remove thick outerwear and measure in thin clothing",
"• Keep the measurement time and position consistent for easier comparison",
"• Measuring after waking in the morning is recommended",
"🍑 How to measure your hips correctly",
"1. Stand upright with feet together",
"2. Wrap the tape around the fullest part of your hips",
"3. Keep the tape horizontal, passing over the pubic symphysis at the front",
"4. Keep the tape against the skin without pressing",
"5. Accurate to 0.1 cm",
"• Measure while wearing close-fitting underwear",
"• Do not deliberately push out or tuck in your hips",
"🌍 Reference standards for different groups",
"Chinese adult central obesity standard (WS/T 428-2013):",
"• Men waist ≥ 90 cm",
"• Women waist ≥ 85 cm",
"International Diabetes Federation (IDF) standard:",
"• Chinese men waist ≥ 90 cm",
"• Chinese women waist ≥ 80 cm",
"⚠️ This tool is for reference only and cannot replace professional medical diagnosis. Waist-to-hip ratio is only one health assessment indicator; consult a doctor if you have health concerns.",
"📚 In-depth: Waist-to-Hip Ratio (WHR) Calculator",
"Compute the waist-to-hip ratio WHR: WHR = waist / hip (both measured horizontally at the widest point, cm). Men ≥0.9 and women ≥0.85 indicate central (apple-shape) obesity with higher cardiovascular/metabolic risk.",
"Combine with the waist-to-height ratio WHtR and",
": the tool also gives the waist-to-height ratio = waist / height, where >0.5 suggests excess visceral fat; combined with BMI it reflects abdominal fat more sensitively than BMI alone.",
"Sex-specific thresholds differ: men's scale 0.7-1.2, women's 0.65-1.1; men's risk bands: <0.9 low, 0.9-1.0 medium, >1.0 high; women: <0.85 low, 0.85-0.95 medium, >0.95 high.",
"Example: waist 80 cm, hip 95 cm (man)",
"WHR = 80 / 95 = 0.84, below 0.9 so low risk; if waist 100 and hip 90, WHR = 1.11, above 1.0 so high risk, markedly increasing the risk of related conditions (type 2 diabetes, cardiovascular disease, fatty liver, etc.). For the same measurements, women have lower thresholds (0.85/0.95).",
"Why does waist-to-hip ratio reflect risk better than BMI?",
"BMI does not distinguish fat distribution, whereas abdominal (visceral) fat is more closely linked to metabolic disease. Among people with the same BMI, the apple shape (abdominal obesity) carries higher risk than the pear shape, and WHR/WHtR captures this.",
"Where is the correct position to measure the waist?",
"Stand and breathe naturally, wrap the tape horizontally about 1-2 cm above the navel (or at the midpoint between the lower rib and the iliac crest), read at the end of an exhale and do not hold your breath or suck in your belly. Measure the hip at the widest point horizontally.",
'About the "Waist-to-Hip Ratio Calculator"',
"Waist-to-Hip Ratio Calculator. A health-metric calculation tool based on authoritative medical standards, with all data processed locally to protect privacy.",
"Calculate waist-to-height ratio",
"Calculate BMI",
],
'protein-needs': [
"🥗 Daily Protein Requirement Calculator",
"Calculate your daily recommended protein intake from weight, activity level and goal",
"Protein Requirement Calculator",
"/ Protein Requirement Calculator",
"📖 View the User Guide",
"Requirement (g) = weight (kg) × activity factor (goal takes the lower bound: muscle gain ≥1.6, fat loss ≥1.8, recovery ≥1.5, elderly ≥1.2)",
"If age ≥ 65, take the higher value of the elderly lower bound",
"Sedentary (0.8 g/kg)",
"Light activity (1.0 g/kg)",
"Moderate activity (1.2 g/kg)",
"Regular training (1.4 g/kg)",
"Muscle-building training (1.7 g/kg)",
"High-intensity training (2.0 g/kg)",
"Competitive athlete (2.2 g/kg)",
"Maintain health",
"Build muscle and shape",
"Post-surgery/injury recovery",
"Prevent sarcopenia in the elderly",
"Protein source",
"Mainly animal protein",
"Mixed diet",
"Vegetarian (eggs and dairy)",
"Plant protein only",
"g/day recommended intake",
"Minimum requirement",
"Safe upper limit",
"🍽️ Food equivalents",
"📖 Nutrition guide",
"Protein content of common foods",
"Protein intake reference by population",
"Recommended (g/kg/day)",
"Ordinary adult",
"Basic physiological need",
"Daily work and life",
"Fitness enthusiasts",
"Strength trainers",
"High-intensity resistance training",
"Fat-loss phase",
"Preserve muscle mass",
"Elderly (65+)",
"Prevent sarcopenia",
"Pregnancy/lactation",
"Add 25 g/day extra",
"Injury recovery",
"Needed for tissue repair",
"Sources: Chinese Dietary Reference Intakes (DRIs), International Society of Sports Nutrition (ISSN)",
"Healthy protein intake advice",
"✅ Quality protein sources",
"• Animal protein: eggs, milk, fish and shrimp, chicken breast, lean beef (good amino acid profile, high absorption)",
"• Plant protein: soy and soy products, quinoa, nuts, legumes (combine for complementary amino acids)",
"⏰ Best times to consume",
"• Distribute evenly across meals: 20-40 g of quality protein per meal works best",
"• 30-60 minutes after training: the protein synthesis window, good for muscle repair",
"• Before bed: slow-release protein (e.g. casein) can reduce overnight muscle breakdown",
"• People with renal impairment should limit protein intake as advised by a doctor",
"• Protein intake must be combined with strength training to build muscle",
"• Do not rely on supplements; natural foods come first",
"• A high-protein diet requires adequate water intake",
"⚠️ This calculator is for reference only and cannot replace the advice of a professional dietitian. Special groups (kidney disease, liver disease, gout, etc.) should follow medical advice.",
"📚 In-depth: Daily Protein Requirement Calculator",
"Ordinary healthy adults: about 0.8-1.0 g/kg/day meets basic needs for most adults; sedentary people take the lower bound, and those with higher activity take 1.0-1.2.",
"Athletes / muscle-building: regular strength trainers are advised 1.4-2.0 g/kg/day to protect muscle and promote synthesis; during a fat-loss phase, raising it to 1.6-2.2 g/kg reduces muscle loss.",
"Split intake and energy share: spread the daily total over 3-4 meals, with 25-40 g per meal for better absorption and use; protein provides 4 kcal per gram, and 15-25% of total calories is appropriate.",
"Example: weight 65 kg, factor 1.4 g/kg",
"Daily protein = 65 × 1.4 = 91 g, spread over 3 meals at about 30 g each; energy = 91 × 4 = 364 kcal (about 18% of 2000 kcal daily). The tool defaults to 1.4, giving 30 g per meal and 364 kcal.",
"Is there an upper limit to protein?",
"For healthy people, exceeding 2.5-3 g/kg/day long-term brings no extra benefit and increases the kidneys' metabolic burden; those with chronic kidney disease should limit it as advised by a doctor. Evenly split meals are used better than a single large dose.",
"How do I choose between plant and animal protein?",
"Animal protein (eggs, dairy, meat, fish) has a more complete amino acid profile; plant proteins often lack some essential amino acids, so combining grains with legumes is recommended. Vegetarians can meet the target by modestly increasing the total and diversifying sources.",
'About the "Protein Requirement Calculator"',
"Protein Requirement Calculator. A health-metric calculation tool based on authoritative medical standards, with all data processed locally to protect privacy.",
],
}

def build(slug, en_list):
    path = os.path.join(WORK, slug + '.json')
    wj = json.load(open(path, encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('!! %s length mismatch %d vs %d' % (slug, len(en_list), len(items)))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src'):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if not en or not isinstance(en, str):
            print('!! %s empty translation' % slug)
            sys.exit(1)
        if CJK.search(en) or CNP.search(en):
            print('!! %s CJK/CNP violation: %s' % (slug, en[:60]))
            sys.exit(1)
        mp[z] = en
    return mp

def write(slug, mp):
    os.makedirs(OUT, exist_ok=True)
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('name', slug)
    out = {'slug': slug, 'industry': 'health', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

if __name__ == '__main__':
    for slug, en_list in EN.items():
        mp = build(slug, en_list)
        write(slug, mp)
    print('gen_health_b7 done')
