#!/usr/bin/env python3
from head_martial import build, write


def main():
    write('breathing-rhythm', build('breathing-rhythm', [
        '🫁 Breathing and Power Generation Matching',
        'Compares breathing rate against the rhythm of power generation, providing breathing coordination schemes for each power phase',
        '/ Breathing and Power Matching',
        '📖 View the guide to breathing and power generation matching',
        '🫁 Matching analysis',
        '📚 In-depth: breathing and power generation matching',
        'Breathing coordination for power generation in martial arts: set the',
        'breathing rate',
        'and the inhale-to-exhale ratio by movement type (striking / throwing / grappling / kicking / forms / standing meditation), and the tool works out the duration of the inhaling, breath-holding and exhaling phases.',
        'Teaching the timing of power release: striking emphasizes inhaling to gather power, exhaling on release and holding the breath on recovery; the tool gives the exact number of seconds to help students build the rhythm.',
        'Matching by training level: four tiers from beginner to professional give an additional match bonus, quantifying how well the breathing fits the movement (the match index).',
        'Worked example: striking at 12 breaths/min, inhale-to-exhale ratio 1:2, intermediate',
        'For the movement type striking, the optimal rate is 8-16 breaths/min.\nBreathing cycle = 60/12 = 5.00 s; ratio 1:2 → total shares 1 + 1/0.5 = 3; inhale = 5/3 = 1.67 s; exhale = 5 − 1.67 = 3.33 s; breath hold = 5 × 0.05 = 0.25 s.\nA rate of 12 falls in the optimal range → rate fit 100%; with the intermediate bonus of +5 the match index = min(100, 100 + 5) = 100 (excellent).',
        'How is the duration of each breathing phase calculated?',
        'Cycle = 60 ÷ rate (breaths/min); inhale = cycle ÷ (1 + 1/ratio); exhale = cycle − inhale; breath hold ≈ cycle × 5%. The ratio is inhale:exhale (for example 1:2 means the exhale takes twice as long as the inhale).',
        'How is the match index rated?',
        'First score the rate fit from the optimal rate range of the chosen movement type (100% inside the range, scaled by the ratio if too low and by the upper bound if too high), then add the training level bonus (beginner 0 / intermediate 5 / advanced 10 / professional 15), capped at 100. The higher the value, the better the breathing fits the movement.',
        'About breathing and power generation matching',
    ]))

    write('kick-height', build('kick-height', [
        '📏 Kick Height Conversion',
        'Computes the ratio of kick height to body height and evaluates the flexibility grade and kicking technique',
        'Core formula (by input variables): Math.asin(min(1,kh÷(ll+h×0.5)))×180÷π; kh÷ll×100; kh÷h×100',
        '/ Kick Height Conversion',
        '📖 View the guide to kick height conversion',
        '📚 In-depth: kick height conversion',
        'Training assessment for martial arts and taekwondo: enter the height, leg length (estimated at 45% of height by default), the height of the kick above the ground and the kick type, and the tool computes the height ratio, leg-length ratio and estimated angle, quantifying flexibility and technique.',
        'Comparing techniques: different kicks (front / side / roundhouse / back / high) have different height coefficients, and the tool grades by the adjusted height ratio for easy comparison across kicks.',
        'Safety note: use it to set training target heights so you do not strain yourself chasing height; the angle estimate is for reference only, since the real angle also depends on hip mobility.',
        'Worked example: height 170 cm, front kick 165 cm above the ground',
        'Height 170 cm, default leg length = 170 × 45% = 76.5 cm, kick height 165 cm, front kick (coefficient 1.0).\nHeight ratio = 165/170 × 100 = 97.1%; leg-length ratio = 165/76.5 × 100 = 215.7%; estimated angle = asin(165/(76.5 + 85)) × 180/π = asin(1.0) = 90.0° (the limit is reached, and the formula truncates anything beyond it); adjusted height ratio = 97.1%/1.0 = 97.1% → grade good (≥ 85%). This means the kick can reach above head height.',
        'How should the height ratio and leg-length ratio be understood?',
        'Height ratio = kick height ÷ body height × 100%, reflecting how high you can kick relative to your height; leg-length ratio = kick height ÷ leg length × 100%, reflecting how far it exceeds the leg length. Using both avoids comparing absolute heights alone and ignoring differences in build.',
        'How is the kick angle estimated?',
        'It is approximated from the leg length and the height ratio: angle = asin(kick height ÷ (leg length + half the height)). This is a simplified model; the actual kick angle also depends on hip mobility and torso posture, so it is for training reference only — never chase height blindly and risk a strain.',
        'About kick height conversion',
    ]))

    write('routine-timer', build('routine-timer', [
        '⏱️ Forms Routine Timer',
        'Compares the standard duration with your own time, evaluating the speed of the routine and rhythm control',
        'Compares the standard duration with your own time, evaluates the speed of the routine and rhythm control, computes from the inputs and outputs the result.',
        '/ Routine Timing',
        '📖 View the guide to routine timing',
        'Completion time (seconds, can be entered manually)',
        '📚 In-depth: routine timing',
        'Martial arts and forms competition practice: each style sets its completion time (long boxing 70-90 s, southern boxing 65-85 s, tai chi 300-420 s, tai chi sword 180-240 s, broadsword / spear / straight sword / staff 70-90 s); the watch stops as soon as the weapon routine ends, and the tool compares the time with the standard and estimates deductions.',
        'Daily training self-test: use the on-page timer to record the time of one run of the routine, or type a known result straight into the completion time box, then compare it with the standard range to judge whether the rhythm is fast or slow and help correct your practice speed.',
        'Referee and coach review: enter the measured time and the standard for the event on site to get the deviation and whether it is within the allowed range immediately, supporting rhythm calibration before a competition.',
        'Worked example: comparison against the long boxing standard',
        'The standard duration range for long boxing is 70-90 s, the standard value = (70 + 90)/2 = 80 s and the tolerance is 2 s.\nMeasured 85 s: deviation = 85 − 80 = +5 s, and since 70 ≤ 85 ≤ 90 it is within the allowed range → status good, and as neither the upper nor the lower limit is exceeded the estimated deduction = 0.\nMeasured 95 s: deviation = +15 s, and since 95 > 90 it exceeds the upper limit → status slow, deduction = (95 − 90) × 0.5 = 2.5 points (0.5 points per second over).\nNote: tai chi styles are not subject to the lower-limit deduction (being slow at the lower bound is not penalized), while other styles are penalized by the same rule when below the lower limit.',
        'How is the standard duration set?',
        'The competition rules of each style set the practice time range (for example long boxing 70-90 s, tai chi 300-420 s) and the standard value is the midpoint of that range; a deviation within the tolerance is rated excellent, within the range good, and outside the range an estimated 0.5 points are deducted per second over.',
        'Why is tai chi not penalized at the lower bound?',
        'Tai chi emphasizes slow, even movement, and the rules usually do not deduct for being too fast at the lower bound (being too fast spoils the flavour), only for exceeding the time limit; other, faster styles are constrained by both the lower and upper bounds.',
        'Must I use the on-page timer?',
        'No. You can use Start / Stop to time the run, or enter a known result directly into the completion time (seconds) box (for example an old coaching record or a reading from another device); whichever valid time you have is used for the comparison. If no valid time is entered, the speed ratio and the deduction are not shown, avoiding meaningless ratios.',
        'About routine timing',
        'Or tap Start to time',
    ]))

    write('stance-center', build('stance-center', [
        '🧮 Stance Centre of Gravity Calculator',
        'Computes the centre of gravity position of a standing stance and the endurance score accumulated over time',
        'Core formula (by input variables): max(0,min(100,enduranceScore)); 100-|(fr-p.defRatio)|×1.5; max(0,min(100,stability))',
        '/ Stance Centre of Gravity',
        '📖 View the guide to stance centre of gravity calculation',
        '📚 In-depth: stance centre of gravity calculation',
        'Stance training in martial arts: choose a stance type such as horse, bow, empty or crouch, along with step width, height, front-foot load ratio, squat depth and duration, and the tool computes the height of the centre of gravity, its offset, and the stability and endurance scores.',
        'Teaching balance: adjust the front-foot load ratio towards the standard for that stance (for example horse stance 50%, bow stance 65%) to reduce the offset and raise the stability index.',
        'Quantifying endurance: it combines squat depth and duration to quantify the load of stance work, helping to plan the',
        'training programme',
        'and to progress the intensity.',
        'Worked example: horse stance, step width 80 cm, height 170 cm, front foot 50%, squat 30 cm, 5 minutes',
        'The horse stance has a standard front-foot load of 50%, a height coefficient of 0.45 and an intensity of 0.85.\nCentre of gravity offset cogX = (50/100 − 0.5) × 80 = 0 cm (right at the midpoint of the step);\ncentre of gravity height = 170 × 0.45 − 30 = 46.5 cm (27.4% of height);\nstability = 100 − |50 − 50| × 1.5 = 100;\nendurance = 50 + min(40, 5 × 2) − min(1.5, 0.85 × 30/30) × (5 × 2) = 50 + 10 − 0.85 × 10 = 51.5 → 52 (pass).\nIf the front-foot load is changed to 65% (15 points away from the standard of 50%), stability falls to 100 − 15 × 1.5 = 77.5.',
        'How are the centre of gravity offset and the stability calculated?',
        'Offset = (front-foot load % − 50%) × step width, positive meaning forward and negative backward; stability = 100 − |actual load − standard load| × 1.5, so the closer to the standard load the higher it is. The standard front-foot load is about 50% for the horse stance, 65% for the bow stance and 25% for the empty stance.',
        'What affects the endurance score?',
        'Endurance = 50 + min(40, duration × 2) − intensity × duration × 2. The deeper the squat, the greater the intensity of the stance and the longer it is held, the higher the load; the formula is an approximate quantification of training load, meant for comparison rather than as an absolute standard.',
        'About stance centre of gravity calculation',
    ]))

    write('strike-resistance', build('strike-resistance', [
        '📋 Impact Resistance Assessment',
        'Measures and evaluates the hardness index of body parts, providing a reference for impact resistance training',
        '/ Impact Resistance Assessment',
        '📖 View the guide to impact resistance assessment',
        'Hardness index = base value + (upper limit − base value) × training years coefficient × frequency coefficient; the years coefficient is taken from the number of years (0 for less than 1 year, 0.6 for 1 to 3 years, 0.8 for 3 to 5 years, 1.0 for more than 5 years); the frequency coefficient = min(1.5, 0.6 + sessions per week × 0.12); an index of at least 80 is advanced, 60 to 79 intermediate, 40 to 59 beginner and below 40 entry level; training should progress gradually and use protective gear, to avoid injury to the periosteum and soft tissue.',
        '📚 In-depth: impact resistance assessment',
        'Impact resistance training for martial arts and combat sports: from training years and weekly frequency, estimate the hardness index of each body part (forearm / shin / abdomen / chest / thigh / fist surface / palm / head) and quantify the degree of adaptation.',
        'Training planning: compare the hardness of different parts to locate weak spots (for example the abdomen and chest start low) and strengthen them specifically; the head should never be trained for impact resistance.',
        'Risk note: the hardness index is only an approximate quantification of training adaptation; genuine impact resistance requires gradual progress and professional guidance, and blindly taking hits is strictly forbidden.',
        'Worked example: the effect of training years and frequency on hardness',
        'Hardness index = base value + (upper limit − base value) × years coefficient × frequency coefficient; years coefficient [untrained 0 / 1 year 0.6 / 2 years 0.8 / 3 years 1.0], frequency coefficient = min(1.5, 0.6 + sessions per week × 0.12).\nForearm (base 40 / limit 95): 3 years of training, twice a week → years coefficient 1.0, frequency coefficient 0.84 → hardness = round(40 + 55 × 1.0 × 0.84) = 86 (fairly hard, able to take medium impact); untrained → 40 (weak); frequency 0 → 73.\nChest (base 38 / limit 80): 3 years of training, twice a week → round(38 + 42 × 0.84) = 73 (medium).\n⚠️ The head has a base of only 15 and a limit of 40, and impact training there carries extreme risk (possible brain injury), so the tool explicitly advises against it and issues a danger warning.',
        'How is the hardness index calculated?',
        'Hardness = base value + (upper limit − base value) × years coefficient × frequency coefficient. The longer you have trained and the more frequent the sessions, the higher the coefficients and the greater the hardness; the base and upper limits differ by part (the forearm and fist surface have high limits, the abdomen and chest lower ones).',
        'Why is the head not recommended for impact training?',
        'Impact to the head easily causes concussion, brain injury and other irreversible harm, far outweighing any training benefit. This tool issues a clear danger warning for the head and advises avoiding it; no gain in hardness is worth the cost to brain health.',
        'About impact resistance assessment',
    ]))


if __name__ == '__main__':
    main()
