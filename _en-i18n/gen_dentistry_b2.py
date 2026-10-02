#!/usr/bin/env python3
# gen_dentistry_head.py — shared head for dentistry batches b1..bN
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'dentistry')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'dentistry')
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
    out = {'slug': slug, 'industry': 'dentistry', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('calc-1', build('calc-1', [
        "DMFT Caries Index",
        "Records the number of permanent teeth that are decayed (D), missing due to caries (M), and filled due to caries (F), to assess an individual's caries experience.",
        'View "DMFT Caries Index User Guide"',
        "DMFT = decayed + missing + filled",
        "Decayed teeth D",
        "Missing due to caries M",
        "Filled due to caries F",
        "Calculate DMFT",
        "In-Depth: DMFT Caries Index",
        "After an individual oral exam, register the D/M/F tooth counts; the tool sums the DMFT total and identifies high-risk tooth positions.",
        "Population oral surveys stratify by age to compute average DMFT and compare caries prevalence.",
        "One year after caries-prevention intervention, recheck the DMFT increment to assess the measure's effect. (Results are for oral-health education and self-screening only, not a substitute for oral examination, periapical film/CBCT imaging, or diagnosis and treatment by dental, orthodontic or periodontal specialists; if you have toothache, gum bleeding, non-healing ulcers, abnormal oral mucosa or occlusal discomfort, please visit a regular hospital dental department promptly.)",
        "DMFT Scoring",
        "Input: decayed D=3, missing due to caries M=1, filled due to caries F=4\nCalculation: DMFT = D + M + F = 3 + 1 + 4 = 8\nNote: a higher score means more caries experience; strengthen topical fluoride and diet management.",
        "What is the difference between DMFT and dmft?",
        "DMFT is for permanent teeth, dmft for primary teeth (d decayed, m missing due to caries, f filled due to caries); during the mixed dentition of children they must be recorded separately.",
        "What are the scoring rules?",
        "Each tooth is counted once by its most severe status (one of D/M/F); the same tooth is not double-counted; a filled tooth with active caries is counted as D.",
        "What does DMFT=0 mean?",
        "It means, under this definition, no decayed, no missing-due-to-caries and no filled-due-to-caries teeth; it is the caries-free target state, but regular dental check-ups are still needed.",
    ]))
    write('caries-risk', build('caries-risk', [
        "Caries Risk Cariogram Scorer",
        'Integrates nine major risk factors to assess the "chance of avoiding new caries", referencing the Cariogram weighted model.',
        "Caries Risk Cariogram Scorer",
        "/ Caries Risk Cariogram Scorer",
        'View "Caries Risk Cariogram Scorer User Guide"',
        "Cariogram caries risk = weighted score",
        "1. Caries experience",
        "No new caries / no fillings",
        "Occasional new caries or fillings",
        "1-2 new caries per year",
        ">=3 new caries per year (high activity)",
        "2. Systemic disease",
        "No related disease",
        "Mildly related",
        "Moderately related",
        "Severely related (immunocompromised, etc.)",
        "3. Diet content",
        "Low-sugar balanced diet",
        "Occasional high sugar",
        "Frequent high sugar",
        "Sustained high-sugar diet",
        "4. Diet frequency",
        "<=3 times/day",
        "4-5 times/day",
        "6-7 times/day",
        ">=8 times/day",
        "5. Plaque amount",
        "Very little plaque (PI<10%)",
        "Small plaque (PI 10-30%)",
        "More plaque (PI 30-60%)",
        "Heavy plaque (PI>60%)",
        "6. Mutans streptococci level",
        "7. Fluoride exposure",
        "Adequate fluoride (fluoridated water + toothpaste)",
        "Regular fluoride toothpaste",
        "Occasional fluoride",
        "No fluoride exposure",
        "8. Saliva flow",
        ">1.0 mL/min (normal)",
        "<0.3 mL/min (dry mouth)",
        "9. Saliva buffer capacity",
        "High buffer (final pH>6)",
        "Medium buffer (pH 5-6)",
        "Low buffer (pH 4.5-5)",
        "Very low buffer (pH<4.5)",
        "This tool uses a simplified Cariogram algorithm; results are for risk assessment reference and cannot replace comprehensive clinical diagnosis.",
        "In-Depth: Caries Risk Cariogram Scorer",
        "For high-caries patients, enter nine factors such as diet, flora and fluoride exposure; the tool gives the chance of avoiding new caries",
        "and grades it.",
        "Assess caries risk during the child's mixed dentition; suggest strengthening topical fluoride and sugar control.",
        "Re-assess during fixed orthodontic treatment, monitoring risk rise from difficulty cleaning around brackets. (Results are for oral-health education and self-screening only, not a substitute for oral examination, periapical film/CBCT imaging, or diagnosis and treatment by dental, orthodontic or periodontal specialists; if you have toothache, gum bleeding, non-healing ulcers, abnormal oral mucosa or occlusal discomfort, please visit a regular hospital dental department promptly.)",
        "Chance-of-Avoiding-New-Caries Estimation",
        'Input: nine factors (high lactose intake, high mutans streptococci, low fluoride exposure, low saliva flow...)\nCalculation: Cariogram weighted model outputs "chance of avoiding new caries" = about 12%\nDetermination: lower chance means higher risk; recommend intensified prevention (fluoride, sealants, sugar control, follow-up).',
        "What are the nine Cariogram factors?",
        "Mainly caries experience, lactose intake, mutans streptococci, fluoride exposure, buffer capacity, saliva flow, sugar-metabolizing bacteria, social factors and past fillings, assessed by weighted integration.",
        "How to understand 'chance of avoiding new caries'?",
        "A percentage output by the model; higher means less likely to develop new caries and lower risk; lower means higher risk and needs personalized intervention.",
        "Can the score replace an oral exam?",
        "No. This tool is",
        "an aid; diagnosis and plan follow the dentist's examination and probing.",
        "About the Caries Risk Cariogram Scorer",
        "Caries Risk Cariogram Scorer - Integrates caries experience, diet, plaque, bacteria, saliva and other factors to assess new-caries risk. A professional medical tool based on authoritative standards, for reference only.",
    ]))
    write('complete-denture', build('complete-denture', [
        "Complete Denture (Jaw Relation) Transfer Tool",
        "Calculates the complete-denture vertical dimension (VDO), freeway space (FS) and centric relation (CR) to assist jaw-relation recording and articulator mounting.",
        "Complete Denture Jaw-Relation Transfer Tool",
        "/ Complete Denture Jaw-Relation Transfer Tool",
        'View "Complete Denture (Jaw Relation) Transfer Tool User Guide"',
        "Facial vertical dimension measurement",
        "Rest-position nasion-to-menton distance (mm)",
        "Existing occlusion-position nasion-to-menton distance (mm)",
        "Willis method (nasion-menton)",
        "Nose-tip to menton method",
        "Pupil-to-mouth method (reference)",
        "Centric Relation (CR) recording method",
        "CR recording technique",
        "Gothic arch tracer",
        "Wax-rim bite record",
        "Swallowing method",
        "Tactile feedback method",
        "Target freeway space (mm)",
        "Calculate jaw relation",
        "Jaw relation is the key to complete-denture success. Too-high vertical dimension causes muscle fatigue; too-low makes the face look aged; centric relation must be stable and reproducible.",
        "Jaw-Relation Principles",
        "Vertical dimension VDO = rest vertical dimension VDR - freeway space FS\nNormal freeway space: 2 - 4 mm\n\nEmpirical reference:\n  pupil-to-mouth distance approx nasion-to-menton distance (VDO)\n  in the elderly VDR slightly decreases with dentition wear/extraction",
        "Vertical dimension evaluation",
        "Freeway space FS",
        "FS > 5mm (VDO too small)",
        "FS < 1mm (VDO too large)",
        "Muscle fatigue, unclear speech",
        "Natural face, comfortable muscles",
        "Reference: Prosthodontics (complete denture) jaw-relation recording section.",
        "In-Depth: Complete Denture (Jaw Relation) Transfer Tool",
        "For edentulous jaw relation taking, measure the rest and smile positions; the tool back-calculates the normal vertical dimension (VDO) from the freeway space.",
        "For remaking an old denture, compare its vertical dimension with facial proportions to set a new restoration goal.",
        "After establishing centric relation (CR), transfer to the articulator to ensure stable artificial-tooth arrangement and occlusion. (Results are for oral-health education and self-screening only, not a substitute for oral examination, periapical film/CBCT imaging, or diagnosis and treatment by dental, orthodontic or periodontal specialists; if you have toothache, gum bleeding, non-healing ulcers, abnormal oral mucosa or occlusal discomfort, please visit a regular hospital dental department promptly.)",
        "Vertical Dimension Estimation",
        "Input: rest-position lower-face-third = 70mm, freeway space FS = 3mm\nCalculation: normal vertical dimension VDO = rest position - FS = 70 - 3 = 67mm\nNote: restoring VDO relates to speech, facial appearance and masticatory support; combine with facial proportions.",
        "What is the relationship between VDO and FS?",
        "VDO (vertical dimension) is obtained by subtracting the freeway space FS (about 2-4mm) from the rest position; it is the baseline for arranging teeth and restoring lower-face height.",
        "What is centric relation (CR)?",
        "The rearmost retruded contact relation of the mandible to the maxilla at the hinge position; a reference position for stable complete-denture occlusion, which may differ from centric occlusion.",
        "Can I set the vertical dimension myself?",
        "No. Too-low or too-high vertical dimension affects mastication and the joint; it must be set by a prosthodontist combining facial appearance, speech and muscle force.",
        "About the Complete Denture Jaw-Relation Transfer Tool",
        "Complete Denture Jaw-Relation Transfer Tool - Calculates vertical dimension, freeway space and centric relation to assist complete-denture jaw-relation recording and transfer. A professional medical tool based on authoritative standards, for reference only.",
    ]))
    write('dental-arch-development', build('dental-arch-development', [
        "Pediatric Dental Arch Development Assessor",
        "Judges the dental-development stage, space need and timing of early orthodontics from age and arch-measurement data.",
        'View "Pediatric Dental Arch Development Assessor User Guide"',
        "Child age (years)",
        "Maxillary primary-canine width (mm)",
        "Mandibular primary-canine width (mm)",
        "Mixed-dentition space deficiency (mm, positive = deficient)",
        "Current dentition stage",
        "Primary dentition",
        "Early mixed dentition",
        "Late mixed dentition",
        "Early permanent dentition",
        "Dental-arch development varies greatly among individuals; this tool gives stage judgment and intervention suggestions for reference; clinically combine cephalometric and full-mouth examination.",
        "Dentition Stage and Space",
        "Early mixed",
        "Late mixed",
        "Permanent",
        "leeway space (mixed-dentition space):\n  maxilla about 0.9mm per side, mandible about 1.7mm per side\n  mandibular leeway space can resolve mild anterior crowding\n\nPermanent-eruption reference ages:\n  central incisor 6-7y, lateral incisor 7-8y, canine 9-12y\n  first premolar 9-11y, second premolar 10-12y\n  first molar 6-7y, second molar 11-13y",
        "Intervention",
        "Primary teeth fully erupted",
        "Watch anterior crossbite / bad habits",
        "Incisors + first molar erupted",
        "Space maintenance, anterior crossbite correction",
        "Canine/premolar replacement",
        "Space management, serial-extraction assessment",
        "Permanent teeth (except third molars)",
        "Comprehensive orthodontic treatment",
        "Reference: Pediatric Dentistry / Moyers mixed-dentition space analysis.",
        "In-Depth: Pediatric Dental Arch Development Assessor",
        "For a mixed-dentition child with a narrow arch, enter age and width; the tool compares reference ranges and suggests expansion timing.",
        "For anterior crowding, assess the difference between available and required space to judge whether serial extraction or early orthodontics is needed.",
        "Screen for skeletal deformity, suggesting referral criteria for maxillary/mandibular developmental disharmony. (Results are for oral-health education and self-screening only, not a substitute for oral examination, periapical film/CBCT imaging, or diagnosis and treatment by dental, orthodontic or periodontal specialists; if you have toothache, gum bleeding, non-healing ulcers, abnormal oral mucosa or occlusal discomfort, please visit a regular hospital dental department promptly.)",
        "Space-Need Assessment",
        "Input: age 8y, required space SigmaW=82mm, available arch length L=76mm\nCalculation: space deficiency = SigmaW - L = 6mm\nNote: crowding exists; suggest orthodontic screening for early intervention.",
        "What stages does arch development have?",
        "Roughly primary dentition, mixed dentition and permanent dentition; the mixed-dentition period is the key window for space management and early orthodontics, needing regular monitoring.",
        "What are the consequences of a narrow arch?",
        "Easily leads to crowding, malposition and malocclusion; severe skeletal narrowing can be expanded at the growth peak, judged specifically by an orthodontist.",
        "When should I see an orthodontist?",
        "Obvious crowding, crossbite, lip-incompetence or mixed-dentition abnormality; suggest orthodontic screening around age 7; this tool is for reference only.",
        "About the Pediatric Dental Arch Development Assessor",
        "Pediatric Dental Arch Development Assessor - Assesses pediatric arch development and space-management need from the primary-permanent replacement period and arch measurements. A professional medical tool based on authoritative standards, for reference only.",
        "How to use the Pediatric Dental Arch Development Assessor",
        "Suitable for monitoring mixed-dentition arch width/length development, screening dental crowding and space deficiency, assessing early-orthodontic timing, and tracking arch changes before and after orthodontic treatment.",
        "What does the Pediatric Dental Arch Development Assessor do?",
        "Enter age and arch-measurement data to judge the dentition stage, space need and early-orthodontic timing, for orthodontic reference.",
        "How to use the Pediatric Dental Arch Development Assessor?",
        "Which scenarios suit the Pediatric Dental Arch Development Assessor?",
    ]))
    write('gingival-index', build('gingival-index', [
        "Gingival Index (GI) and Bleeding Index Assessor",
        "Assesses gingival inflammation from the Loe & Silness Gingival Index (GI) and bleeding on probing (BOP). Records four sites per tooth: mesial-buccal, buccal, distal-buccal, and lingual/palatal.",
        "Gingival Index and Bleeding Index Assessor",
        "/ Gingival Index and Bleeding Index Assessor",
        'View "Gingival Index (GI) and Bleeding Index Assessor User Guide"',
        "Gingival Index GI = graded score",
        "Select GI assessment sites (Ramfjord teeth: 16/21/24/36/41/44 or full-mouth simplified)",
        "Enter 4-site GI scores per index tooth (0=normal, 1=mild inflammation, 2=moderate inflammation, 3=severe inflammation) and check bleeding on probing (BOP).",
        "GI and BOP are common indicators for gingival inflammation. The BOP-positive rate is a sensitive indicator of active gingival inflammation.",
        "Loe & Silness Gingival Index (GI) criteria",
        "Normal gingiva",
        "Mild inflammation, slight color change, slight edema, no bleeding on probing",
        "Moderate inflammation, redness, edema, shininess, bleeding on probing",
        "Severe inflammation, marked redness, edema, ulceration, spontaneous bleeding tendency",
        "GI grading (mean):",
        "0.1 - 1.0: mild gingivitis",
        "1.1 - 2.0: moderate gingivitis",
        "2.1 - 3.0: severe gingivitis",
        "In-Depth: Gingival Index (GI) and Bleeding Index Assessor",
        "At periodontal first visit, record gingival color, texture and bleeding by tooth; the tool summarizes the GI mean and grades inflammation.",
        "After scaling, the BOP-positive rate drops, quantifying inflammation improvement.",
        "During fixed orthodontic treatment, monitor gingivitis and prompt strengthening of interproximal cleaning. (Results are for oral-health education and self-screening only, not a substitute for oral examination, periapical film/CBCT imaging, or diagnosis and treatment by dental, orthodontic or periodontal specialists; if you have toothache, gum bleeding, non-healing ulcers, abnormal oral mucosa or occlusal discomfort, please visit a regular hospital dental department promptly.)",
        "GI Grading Summary",
        "Input: 6 tooth-site GI scores [0,1,1,2,1,0]\nCalculation: GI mean = (0+1+1+2+1+0)/6 approx 0.83 -> mild gingivitis\nNote: higher score means more severe inflammation; judge with BOP-positive rate.",
        "How is the Gingival Index (GI) graded?",
        "Loe & Silness method: 0 normal, 1 mild inflammation, 2 moderate (red, swollen, bleeding on probing), 3 severe (spontaneous bleeding, ulceration). Record per tooth surface.",
        "What does BOP mean?",
        "Bleeding on Probing, a sensitive indicator of gingival inflammation; a high positive rate suggests the periodontium is in an active inflammatory phase.",
        "Can GI diagnose periodontitis?",
        "No. GI reflects gingival inflammation; periodontitis also needs probing depth and clinical attachment loss (CAL); for bleeding or suppuration, visit a periodontal specialist promptly.",
        "About the Gingival Index and Bleeding Index Assessor",
        "Gingival Index GI and Bleeding Index Assessor - Calculates the Loe-Silness gingival index and bleeding on probing BOP to assess gingival inflammation severity. A professional medical tool based on authoritative standards, for reference only.",
        "Is this tool free?",
        "Completely free, no registration, used directly in the browser.",
    ]))

if __name__ == "__main__":
    main()
