#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'pet')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'pet')
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
    out = {'slug': slug, 'industry': 'pet', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('checker-diagnosis', build('checker-diagnosis', [
        "💊 Pet Diagnostic Assistance Workflow",
        "Enter the pet's basic information and symptoms; the system helps generate examination suggestions, differential diagnosis and medication reference plans. For study reference only; it cannot replace a licensed veterinarian's diagnosis.",
        "The text \"Enter the pet's basic information and symptoms; the system helps generate examination suggestions, differential diagnosis and medication reference plans. For study reference only; it cannot replace a licensed veterinarian's diagnosis.\" is computed professionally based on the input parameters and the result is output.",
        "Diagnostic (Examination/Diagnosis/Prescription) Workflow",
        "/ Diagnostic (Examination/Diagnosis/Prescription) Workflow",
        "📖 View the \"Pet Diagnostic Assistance Workflow User Guide\"",
        "Pet species",
        "Rabbit",
        "Body temperature (°C)",
        "Main symptoms (multi-select)",
        "Fever",
        "Diarrhea",
        "Cough",
        "Sneezing",
        "Lethargy",
        "Loss of appetite",
        "Ocular/nasal discharge",
        "Skin itching",
        "Lameness",
        "Abnormal urination",
        "Seizures",
        "Symptom duration (days)",
        "Assisted diagnosis",
        "Normal dog temperature: 37.5-39.2°C; normal cat temperature: 38.0-39.5°C",
        "This tool only provides differential-diagnosis reference and cannot replace an on-site diagnosis by a licensed veterinarian",
        "Medication plans must be prescribed by a licensed veterinarian based on actual examination results",
        "If emergency symptoms such as seizures/severe vomiting/difficulty breathing appear, seek veterinary care immediately",
        "📚 In-Depth Analysis: Pet Diagnostic Assistance Workflow",
        "When a dog or cat shows cough/sneezing/nasal discharge, combined with temperature and mental symptoms, quickly obtain differential directions such as upper respiratory infection, canine distemper/feline panleukopenia, etc.",
        "When vomiting+diarrhea occurs with fever in a young animal, prioritize ruling out infectious diseases such as parvovirus, and suggest the antigen/CBC tests to perform.",
        "When a cat shows abnormal urination, combined with breed and symptoms it indicates the risk of feline lower urinary tract disease (FLUTD) and guides the examinations to seek.",
        "Example: Dog Fever + Respiratory Symptoms",
        "A dog with temperature 39.8°C (normal dog 37.5-39.2°C, indicating fever), checking cough+nasal discharge+lethargy: the tool pushes 'canine distemper/feline panleukopenia (viral infectious disease)' as high probability, suggesting CDV antigen test and CBC; it also indicates 'upper respiratory infection' as medium probability. Note: this result is for reference only; confirmation requires laboratory testing.",
        "Can this tool replace a veterinarian's diagnosis?",
        "No. It gives 'suspected directions and suggested examinations/treatments' based on symptom combinations, helping owners judge urgency and care priorities; the final diagnosis must be determined by a veterinarian through physical examination and lab tests.",
        "How to interpret body temperature?",
        "Normal dog about 37.5-39.2°C, cat about 38.0-39.5°C; above the upper limit is fever (marked red), below the lower limit is low temperature (marked yellow). In a young animal + fever + typical symptoms, infectious disease has top priority.",
        "About the \"Pet Diagnostic Assistance Workflow\"",
        "A pet diagnostic-assistance tool: enter the pet's species/age/temperature/weight and 12 common symptoms, and the system automatically generates a differential-diagnosis list, recommended examination workflow and weight-based common medication dosage reference, helping pet owners understand the condition initially.",
        "Multi-select input of 12 common symptoms",
        "Smart differential diagnosis (probability ranking)",
        "Automatic generation of recommended examination workflow",
        "Weight-based medication dosage reference",
        "Urgency assessment for veterinary visits",
        "Initial symptom assessment for pet owners",
        "Study reference for veterinary students' diagnosis",
        "Triage assistance for pet hospitals",
        "Primary-level pet diagnostic assistance",
    ]))

    write('reminder-vaccine-deworming', build('reminder-vaccine-deworming', [
        "🐾 Vaccine/Deworming Due-Date Reminder System",
        "Manage pet profiles, automatically calculate vaccine and deworming due dates, color-coded warnings, never miss a due date.",
        "📖 View the \"Vaccine/Deworming Due-Date Reminder System User Guide\"",
        "➕ Add pet profile",
        "🐶 Dog",
        "🐱 Cat",
        "📋 All records log",
        "Clear all data",
        "💡 Tip: clicking 'Mark complete' records today's date. To backfill past records, enter the actual date in 'Backfill'.",
        "📚 In-Depth Analysis: Vaccine/Deworming Due-Date Reminder System",
        "Build a health profile for each pet (birthday, last vaccine/deworming date, interval cycle), and automatically calculate and remind the next due date.",
        "Manage the first-immunization pace of puppies and kittens by week age (e.g. vaccine interval 21 days, internal deworming every 30 days) to avoid missed doses.",
        "Multi-pet households view the unified due list, and export records for presentation at the clinic.",
        "Example: Next Due-Date Calculation",
        "Logic: next due = last date + interval days. Puppy first immunization 2026-01-01, interval 21 days -> next 2026-01-22; internal deworming every 30 days, last 2026-01-01 -> next 2026-01-31. Week age = (today - birthday) / 7, used to judge the first-immunization window. Data is stored in the local browser and not uploaded.",
        "Where is the data stored? Is it safe?",
        "Stored only in the local browser's localStorage, running purely on the front end and not uploaded to any server; changing devices or clearing cache loses it, so regular export backups are recommended.",
        "How are the interval days determined?",
        "Set per the vaccine/deworming instructions and veterinarian's advice (e.g. core vaccine first-immunization interval 2-4 weeks, internal deworming monthly when young / every 3 months when adult). The tool only does date calculation and does not replace the vaccination program; follow your veterinarian's plan.",
        "This tool runs purely on the front end; data is saved only in this browser and will not be uploaded to any server",
        "Vaccine and deworming plans reference general advice; follow your veterinarian's instructions and local regulations for specifics",
        "Data is lost after switching browsers or clearing the cache; regular export backups are recommended",
        "About the \"Vaccine/Deworming Due-Date Reminder System\"",
        "Build health profiles for dogs and cats with built-in standard vaccine immunization schedules and internal/external deworming cycles, automatically calculate the next due date and give color-coded warnings by urgency, helping owners immunize and deworm on time.",
        "Built-in dog/cat immunization schedule",
        "Automatic calculation of internal/external deworming cycles",
        "Color-coded countdown warning for due dates",
        "Supports backfilling historical records",
        "First-immunization vaccine scheduling for puppies and kittens",
        "Annual booster due-date reminder",
        "Regular deworming cycle management",
        "Multi-pet household health profiles",
        "Example: Xiaohei",
    ]))

    write('training-planner', build('training-planner', [
        "📚 Pet Training Plan Generator",
        "Based on pet species, age and goals, create a scientific daily training plan",
        "Pet Training Plan",
        "/ Pet Training Plan",
        "📖 View the \"Pet Training Plan Generator User Guide\"",
        "Puppy/Kitten stage (0-6 months)",
        "Adolescent stage (6-18 months)",
        "Adult stage (1.5-7 years)",
        "Daily training duration",
        "10 minutes (light)",
        "20 minutes (recommended)",
        "30 minutes (standard)",
        "45 minutes (high intensity)",
        "Training goals (multi-select)",
        "📋 Generate training plan",
        "📅 Training plan overview",
        "🗓️ 7-day training schedule",
        "💡 Training tips",
        "📈 Advanced guide",
        "📊 Training progress reference",
        "Training cycle",
        "Expected effect",
        "Week 1",
        "Build trust, basic commands",
        "Name response, sit",
        "Week 2",
        "Consolidate basics, simple socialization",
        "Down, stay, meet strangers",
        "Week 3",
        "Complex commands, distraction training",
        "Recall, leave it, environmental adaptation",
        "Week 4",
        "Skill combinations, consolidation review",
        "Connected movements, stable performance",
        "Months 2-3",
        "Advanced skills, ongoing reinforcement",
        "Complex tricks, stable obedience",
        "⚠️ Training principles:",
        "1. Primarily positive reinforcement, reward promptly (treats + praise)",
        "2. Short and frequent sessions, 10-15 minutes each is optimal",
        "3. Stay patient, no scolding or physical punishment",
        "4. Progress gradually in difficulty, do not skip levels",
        "5. Exercise appropriately before training to burn off energy",
        "6. Train when the pet is in a good state",
        "📋 Saved plans",
        "⚠️ This tool is for reference only. Every pet has a different personality; please adjust the training pace to the actual situation. For behavioral problems, consult a professional dog/cat trainer.",
        "📚 In-Depth Analysis: Pet Training Plan Generator",
        "Based on pet species, age stage and selected training goals, automatically generate a one-week training schedule (days / duration per session / number of items).",
        "Break multiple goals (e.g. housebreaking, heel, recall) into daily tasks, progressing step by step and avoiding overloading at once.",
        "Trainers check in per the plan (check to complete), intuitively tracking weekly training coverage.",
        "Example: Generate a one-week plan",
        "Select 2 training goals, 20 minutes per day: the tool outputs a 7-day cycle overview (7 days / 20 minutes·day / several training sessions / several training items), and rotates the tasks across daily time slots, showing the specific training action and its goal each day.",
        "How is the plan generated?",
        "Take the corresponding goal library by current pet species, merge the tasks of selected goals, then rotate-assign them to Monday through Sunday by the 'daily time-slot table'; the overview card shows the number of days, daily minutes, training sessions and total items.",
        "Can I specify a certain day to practice a certain action?",
        "Currently it is auto-rotated; if you need to fix a certain day's content, you can manually adjust the order after generation. The plan is a training framework; actual progress should be flexibly advanced by combining the pet's state with positive reinforcement.",
        "About the \"Pet Training Plan\"",
        "Pet training plan. A pet-care tool that helps calculate pet diet and health metrics.",
    ]))


if __name__ == '__main__':
    main()
