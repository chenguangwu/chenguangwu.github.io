#!/usr/bin/env python3
from head_pet-training import build, write


def main():
    write('clicker-timing', build('clicker-timing', [
        '❤️ Clicker Timing Trainer',
        'Click the instant the green light appears to train precise clicker timing',
        '/ Clicker Timing',
        '📖 View the Clicker Timing Trainer user guide',
        'Marking delay = click moment − moment the green light turns on (ms); hit rate = number of clicks whose delay falls inside the ±200 ms window ÷ total clicks × 100%; average reaction time = Σ delay ÷ number of clicks; the shorter the delay, the more precise the marking — a key skill indicator that decides success or failure in clicker training.',
        'Clicker!',
        '📚 In-depth analysis: Clicker Timing Trainer',
        'Before formal training, warm up with the green-dot game and drill the finger response of pressing the clicker the instant the behavior appears down to under 300 ms.',
        'Practice progressively across the difficulty levels (intervals of 0.5–4 seconds) to shorten the delay from behavior onset to click and improve marking precision.',
        'Record the reaction time and hit rate of every trial to identify whether your errors are usually too early or missed, then work on that specifically.',
        'What a 280 ms reaction means',
        'Green dot on = the behavior appears, red dot = the behavior ends. A click delay of 280 ms falls in the <350 ms excellent band (<200 ms perfect, <500 ms good, <800 ms fair). The training target is an average reaction under 300 ms: at that speed the clicker marks the exact moment the behavior occurs, so the pet builds the correct association; a delay over 1 second may mark the wrong behavior.',
        'Why is within 200 ms stressed as optimal?',
        'The clicker sound must mark the exact instant the correct behavior occurs; a click within 1–2 seconds after the behavior appears can still be associated by the pet, but within 200 ms is the most precise. This trainer replaces real behavior with a visual green dot to drill finger reaction speed, so your marking is more accurate in real training.',
        'What happens if you click too early or miss?',
        'Clicking too early (before the green dot lights up) marks waiting rather than the behavior; missing (the red dot already showing) marks the end of the behavior or even the next action. Both confuse the pet about which behavior the clicker refers to, so repeated calibration using the recorded history is needed.',
        'About Clicker Timing',
    ]))

    write('command-repetition', build('command-repetition', [
        '🔑 Command Memory Curve',
        'Based on the forgetting curve, calculate the optimal repetition interval for command training and plan a scientific training schedule',
        'Core formulas (by input variables): Math.exp(-s×hoursAgo÷(reps)^0.5); max(0,min(1,retention)); retention×100',
        '/ Command Memory Curve',
        '📖 View the Command Memory Curve user guide',
        '📈 Forgetting curve chart',
        '📚 In-depth analysis: Command Memory Curve',
        'When teaching a new command, use the forgetting curve to plan an 8-level spaced review schedule, avoiding one long session that is quickly forgotten.',
        'Compare the age-factor difference between puppies and adult dogs to adjust review density — puppies forget more slowly but also learn more slowly, so they need tighter reinforcement.',
        'Model commands of different difficulty (sit / play dead) separately; complex actions have a higher coefficient and decay faster, so they should be prioritized for near-term review.',
        'Command "down" practiced 5 times · medium difficulty · 4 hours since the last session',
        'Forgetting coefficient s = difficulty coefficient 0.5 × age factor (6 months = 1.0) = 0.5. Current retention = e^(−0.5×4/√5) ≈ e^(−0.894) ≈ 40.9%, which falls in the band of memory starting to decay, review as soon as possible. Front part of the 8-level interval table: 5th→6th repetition after about 1 hour (retention ≈80%), 6th→7th after about 4 hours (≈44%), 7th→8th after about 12 hours (≈10%), 8th→9th after about 1 day (≈1%). So beyond 12 hours without review the command is essentially forgotten; schedule several short sessions within the same day.',
        'Why do puppies need more frequent review?',
        'The age factor is 1.3 for puppies (<6 months) and 1.4 for adults (>36 months), which amplifies s and makes the curve steeper and decay faster; but puppies learn more slowly in a single session, so they need short and frequent practice (5–10 minutes each, 2–3 times a day) to offset the rapid forgetting.',
        'Below what retention level must you review?',
        'The tool sets 40% as the warning line: ≥80% means the interval can be extended, 50–80% review soon, 30–50% review as soon as possible, <30% retrain. In practice, schedule the next review before retention drops below 40%.',
        'About Command Memory Curve',
    ]))

    write('elimination-predict', build('elimination-predict', [
        '🔮 Elimination Pattern Predictor',
        'Predict the next toilet time from your pet’s age and drinking or meal times to support spot elimination training',
        'Core formulas (by input variables): max(0,postDrinkTime-afterDrink); min(age+2,10); min(age+1,8)',
        '/ Elimination Predict',
        '📖 View the Elimination Pattern Predictor user guide',
        '📚 In-depth analysis: Elimination Pattern Predictor',
        'During puppy spot-elimination training, use the bladder rule of age in months + 1 hour to predict the maximum holding time and schedule outdoor trips.',
        'Log drinking or meal times and the moments after waking or play, then combine them with the elimination window to estimate the most likely time of the next toilet visit.',
        'In multi-pet households, model dogs and cats of different ages separately, and avoid applying an adult cat’s tolerance rhythm to a puppy.',
        'Toilet time window for a 3-month-old puppy',
        'Under the rule of age in months + 1 hour, a 3-month-old puppy can hold for about 3 + 1 = 4 hours (adult dogs are capped at 8 hours; cats use age in months + 2 hours, capped at 10 hours). Key elimination windows: within about 5 minutes after waking, 15–30 minutes after drinking or eating, and within about 10 minutes after play. So if a puppy has just woken up and drank 15 minutes ago, guide it to the spot immediately; 4 hours is the maximum holding time, and exceeding it risks indoor accidents.',
        'How much does bladder capacity differ between puppies and adults?',
        'Puppies roughly follow age in months + 1 hour (3 months ≈ 4 h, 5 months ≈ 6 h); adult dogs are uniformly counted as 6–8 hours; cats tolerate slightly longer (age in months + 2 hours, capped at 10 hours). The younger the animal, the shorter the window and the more often it needs to be taken out.',
        'Can the prediction result be used directly as a',
        'training plan',
        '?',
        'It can be used as a rhythm reference, but bladder development, water intake and activity level differ for every dog; record actual elimination times for 3–5 days first, then cross-check them against the windows given here and calibrate gradually.',
        'About Elimination Predict',
    ]))

    write('leash-length', build('leash-length', [
        '📏 Leash Safe Distance Calculator',
        'Calculate the safe control distance and braking distance from leash length, dog size and environment',
        'Core formulas (by input variables): maxReach×0.3×reactMod; 0.5+weight÷20',
        '/ Leash Length',
        '📖 View the Leash Safe Distance Calculator user guide',
        '📚 In-depth analysis: Leash Safe Distance Calculator',
        'On busy city sidewalks with dense pedestrian and vehicle traffic, reserve braking distance using the scenario coefficient to prevent your dog from darting out and causing an accident.',
        'In early training the heel response is not yet established, so combine body weight and the reaction coefficient to quickly assess whether the current leash length is enough to stay in control.',
        'When switching between parks, trails and crowds, use the same coefficient set to instantly convert the effective controllable distance and plan your walking route.',
        '15 kg dog · 1.5 m leash · city environment',
        'Dog body extension = 0.5 + weight / 20 = 0.5 + 15 / 20 = 1.25 m; maximum reach = 1.5 + 1.25 = 2.75 m. City coefficient 0.6 → safe distance 1.65 m; braking distance = 2.75 × 0.3 × 1.0 (normal reaction) = 0.82 m; net controllable distance = 1.65 − 0.82 ≈ 0.82 m. So in a city environment the actually controllable range is only about 0.8 m — keep the dog at heel or switch to a shorter leash. For comparison, with the park coefficient 1.0 the net controllable distance reaches 1.93 m, with the crowd coefficient 0.4 only 0.28 m, and on a trail (0.7) 1.1 m.',
        'Why do the park and crowd coefficients differ so much?',
        'Parks are open with few sudden disturbances, so the reach factor can stay at 1.0; in dense crowds a dog is easily startled and may bolt, so the factor drops to 0.4 to forcibly shorten the effective distance, squeezing the net controllable distance down to about 0.3 m and requiring the handler to keep the dog right at heel.',
        'How should a slow-reacting handler use this tool?',
        'The slow reaction coefficient of 1.4 magnifies braking distance and shrinks the net controllable distance; if the result is negative or very small (for example below 0.3 m), switch to a shorter leash, add a harness for secure attachment, or switch to close-at-heel training.',
        'About Leash Length',
    ]))

    write('treat-calories', build('treat-calories', [
        '⚡ Pet Treat Calorie Calculator',
        'Calculate the share of treat calories in total daily intake to keep treats under 10% of daily calories',
        'Core formulas (by input variables): Math.floor(maxTreatCal÷treatCal); totalTreatCal÷der×100; min(pct,100)',
        '/ Treat Calories',
        '📖 View the Pet Treat Calorie Calculator user guide',
        '📚 In-depth analysis: Pet Treat Calorie Calculator',
        'When giving treats frequently during training, use the RER/DER model to compute total daily calories and keep treats under the 10% safety line to prevent obesity.',
        'Compare the basal metabolism formulas for dogs and cats (dogs 70 × body weight^0.75, cats 40 × body weight + 20) and control portions separately.',
        'Adjust the DER factor by activity level and neuter status; neutered or low-activity pets have lower metabolism, so their treat allowance should be tightened accordingly.',
        '10 kg dog · 15 kcal per treat · 5 treats a day · normal activity · intact',
        'Resting energy RER = 70 × 10^0.75 ≈ 393.6 kcal; daily requirement DER = 393.6 × 1.6 (normal · intact) = 629.8 kcal. Total treat calories = 15 × 5 = 75 kcal, which is 11.9% of the daily total and already over the 10% safety cap (≈63 kcal). Reduce to at most 4 treats a day, or switch to small 2–5 kcal training treats. For comparison, a 4 kg cat with 5 kcal per treat × 3 treats accounts for only 6.94%, still within the safe range.',
        'Why do dogs and cats use different formulas?',
        'Dogs use the Kleiber power law RER = 70 × body weight^0.75 (better for scaling across body sizes), while cats use the linear RER = 40 × body weight + 20 (an empirical formula for small felids); both then multiply by activity, neuter and age factors to get DER. Mixing the formulas systematically overestimates or underestimates calories.',
        'Do you always have to cut the number of treats when over the limit?',
        'Prefer cutting the number of treats or switching to lower-calorie treats; if the excess is large (>20%), also reduce the main meal portion accordingly (in this example about 12 kcal should come out of the main food). The general veterinary rule is that treat calories should not exceed 10% of total daily calories.',
        'About Treat Calories',
    ]))


if __name__ == '__main__':
    main()
