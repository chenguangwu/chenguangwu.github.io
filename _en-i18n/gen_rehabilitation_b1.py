#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'rehabilitation')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'rehabilitation')
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
    out = {'slug': slug, 'industry': 'rehabilitation', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
DISCL_M = " A professional medical tool based on authoritative medical standards, for reference only."

def main():
    write('adl-task-breakdown', build('adl-task-breakdown', [
        "\U0001F9BE Activities of Daily Living (ADL) Task Decomposer",
        "Break activities of daily living into step-by-step training steps, helping patients with cognitive impairment and motor dysfunction learn gradually.",
        "Select ADL activity",
        "Training difficulty level",
        "Full assistance (all prompts needed)",
        "Partial assistance (some prompts needed)",
        "Verbal prompts (language reminders only)",
        "Independent completion (under supervision)",
        "Please select an ADL activity to view the decomposition steps",
        "Save training plan",
        "Export plan",
        "\U0001F4DA ADL activity list",
        "\U0001F4CB Training plan record",
        "\U0001F4DA Deep Dive: Activities of Daily Living (ADL) Task Decomposition",
        "Dressing training",
        "Full assistance",
        "Verbal prompts",
        "Dressing 6 steps",
        "Dressing is broken into 6 steps; at the full level the therapist hand-over-hand does each step 3-5 times, 15-20 minutes each time, 1-2 times daily; at the partial level assistance is given only on difficult steps.",
        "Verbal level",
        "Give language prompts on forgotten steps, focus on movement quality, 30 minutes every other day, progressively increasing complexity to promote independent completion.",
        "How is graded training applied?",
        "Full = continuous assistance, partial = assistance on difficult steps, verbal = prompts only; progressively reduce assistance according to remaining function to improve self-care.",
        "How fine should the decomposition be?",
        "Use 'the smallest step the patient can complete independently' as the granularity: if a step fails 3 times in a row, split it one level finer; if it succeeds 3 times in a row, merge it back up one level. Too fine (e.g. splitting 'pick up the cup' into reach out / spread fingers / grip) makes training lengthy and frustrating; too coarse ('drink by yourself') leaves no way to find the bottleneck. During training, first demonstrate the full chain, then use backward chaining (therapist does the earlier steps, patient completes the last step) and gradually move forward.",
        "About the Activities of Daily Living (ADL) Task Decomposer",
        "\uFE0F The Activities of Daily Living (ADL) Task Decomposer. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))
    write('asia-impairment-scale', build('asia-impairment-scale', [
        "\U0001F3CB Paraplegia Level (ASIA) Sensory-Motor Assessor",
        "ASIA (American Spinal Injury Association) injury grading to determine the neurological level and degree of injury (AIS classification).",
        "Sensory function assessment",
        "Test light touch and pinprick on each dermatome on each side: 0=absent 1=altered 2=normal",
        "Motor function assessment",
        "10 key muscles (each side), 0-5 points (MMT grading)",
        "Please complete the sensory and motor assessments to view results",
        "Assessment grade",
        "\U0001F4CA ASIA injury grade (AIS)",
        "Degree of injury",
        "Complete",
        "No sensory or motor function preserved at S4-S5",
        "Incomplete sensory",
        "Sensation preserved below the injury level but no motor function",
        "Incomplete motor",
        "More than half of key muscles below the injury level grade <3",
        "More than half of key muscles below the injury level grade \u22653",
        "Sensory and motor function both normal",
        "\U0001F4CB Assessment record",
        "\U0001F4DA Deep Dive: Paraplegia Level (ASIA) Sensory-Motor Assessment",
        "Spinal cord injury",
        "Level determination",
        "Rehabilitation plan",
        "Grade A complete",
        "Sacral S4-S5 sensory and motor both absent, complete paralysis below the injury level is grade A (complete); rehabilitation focuses on wheelchair skills, upper-limb strengthening, and pressure ulcer prevention.",
        "Grade D incomplete",
        "More than half of key muscles below the motor level grade \u22653 is grade D (incomplete strong), allowing resistance training and gait training with a chance of community ambulation.",
        "What do the A-E grades mean?",
        "A = no sacral sparing, B = sensory sparing, C = motor weak (fewer than 50% of key muscles grade \u22653), D = motor strong, E = normal; sacral sparing is the dividing line.",
        "Is a mismatch between sensory and motor levels common?",
        "Very common. After spinal cord injury the sensory and motor levels often differ by 1-3 segments (the sensory level is usually higher than the motor level) because the anatomical course and blood supply of the sensory and motor tracts differ. When documenting, label them separately and identify the zone of partial preservation (ZPP) \u2014 in complete injury (grade A), partial preservation beyond 3 segments indicates potential for neurologic recovery, with a better prognosis than those without preservation.",
        "About the Paraplegia Level (ASIA) Sensory-Motor Assessor",
        "The Paraplegia Level (ASIA) sensory-motor assessor. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))
    write('berg-balance-scale', build('berg-balance-scale', [
        "\U0001F9BF Balance Function (Berg Score) Tester",
        "Berg Balance Scale (BBS) with 14 items, 0-4 points each, 56 points total, assessing static and dynamic balance ability.",
        "The Berg Balance Scale has 14 items (sit-to-stand, unsupported standing, unsupported sitting, sitting to standing, transfer, standing with eyes closed, feet together, reaching forward, picking an object from the floor, turning around to look behind, turning 360 degrees in place, stepping onto a stool, standing with one foot in front of the other, standing on one leg), each 0 to 4 points, total 0 to 56 points; 45 points or above means low fall risk, 40 to 44 means moderate risk, below 40 means high risk (assistive devices and supervision recommended); a single item scoring 4 means independent completion, 0 means unable to complete.",
        "Please complete the item scores to view results",
        "\U0001F4CA Scoring criteria and interpretation",
        "Balance ability",
        "Fall risk",
        "Severe impairment",
        "Needs wheelchair assistance, dedicated care",
        "Needs a walker, rehabilitation training",
        "Needs assistance, balance training",
        "Can walk independently, maintain training",
        "Very low",
        "Balance function normal",
        "Clinical meaning:",
        "BBS \u226445 points indicates fall risk; for every 1-point decrease the fall risk rises by about 6-8%. This scale is widely used in stroke, Parkinson disease, and geriatric rehabilitation assessment.",
        "\U0001F4CB Assessment record",
        "\U0001F4DA Deep Dive: Balance Function (Berg) Score",
        "Stroke balance",
        "Parkinson disease",
        "Total score 48",
        "14 items \u00D7 0-4 sum to 48/56, which is low risk (>44); if <45 the fall risk = (45 - total) \u00D7 7%, e.g. a score of 40 gives a risk of about 35.",
        "Total score 20",
        "Summing to 20 points (\u226420 red zone), balance is severely impaired; activity requires assistance and fall prevention, and sitting balance plus transfer training is advised.",
        "How is it graded?",
        "\u226420 high fall risk, 21-40 moderate risk, 41-44 low risk, 45-52 normal, 53-56 excellent; below 45 fall prevention should be implemented.",
        "How should 45 and 41 be interpreted?",
        "Berg totals 56; clinically 0-20 points suggests wheelchair use, 21-40 walking with assistance, 41-56 independent walking. But a more critical criterion is that a change of 8 points or more is needed to exceed measurement error and count as real functional change. Another point: Berg is sensitive to static balance but has limited discrimination for dynamic reactive balance (the response to being pushed), so high-risk fallers should also cross-validate with the Timed Up and Go (TUG) test.",
        "About the Balance Function (Berg Score) Tester",
        "\uFE0F The Balance Function (Berg Score) Tester. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))

if __name__ == '__main__':
    main()
