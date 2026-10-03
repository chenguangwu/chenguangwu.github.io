#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'kids')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'kids')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    return mp


def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'kids', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

#!/usr/bin/env python3


def main():
    write('focus-timer', build('focus-timer', [
        '⏱️ Focus Timer',
        'A children’s version of the Pomodoro Technique: short focus bursts plus fun breaks, helping children build good concentration habits',
        'A children’s version of the Pomodoro Technique with short focus bursts and fun breaks that help children build good concentration habits — it computes from the inputs and outputs the result.',
        '/ Focus Timer',
        '📖 View the guide to the focus timer',
        '📚 In-depth: focus timing (the Pomodoro Technique)',
        'Builds a child’s concentration with a rhythm of 25 minutes of focus plus a 5 minute break.',
        'Time homework in segments to avoid fatigue from sitting too long.',
        'Scheduling 3 pomodoros',
        '3 focus blocks of 25 minutes each = 75 minutes, with 2 breaks of 5 minutes each = 10 minutes, 85 minutes in total; after the 3 blocks, take one long break of 15-30 minutes.',
        'Shorten the blocks for younger children',
        'Lower grades can use a simplified rhythm of 15 minutes of focus plus a 3 minute break; stand up and move at the end of each block to avoid eye and posture fatigue.',
        'Why 25 minutes?',
        'The pomodoro is a proven unit of attention, roughly equal to the comfortable length of one subject’s homework for an elementary school student; longer and attention drifts, shorter and it is hard to get into flow.',
        'What if it gets interrupted?',
        'If the interruption is internal (wanting to check a phone), mark an apostrophe and return to the current pomodoro at once without restarting the timer; if the interruption is unavoidable (someone needs you, something must be handled), the current pomodoro is void — restart after a break. After 4 pomodoros in a row, take a long break of 15-30 minutes. Batching errands into the breaks between pomodoros markedly cuts the number voided.',
        'About the focus timer',
    ]))

    write('memory-palace', build('memory-palace', [
        '🔤 Memory Palace Encoding',
        'Generates virtual grid position codes for numbers, and combines imagery mnemonics to memorize long number strings or word lists quickly',
        '/ Memory Palace Encoding',
        '📖 View the guide to memory palace encoding',
        'The memory palace (Method of Loci) encodes items to remember as vivid images and places them in order along a familiar spatial path (rooms, a route), retrieving them by walking the path again. Numbers commonly use a',
        '00-99 two-digit code',
        '(one image per number) to turn them into images that can be hooked.',
        'The more exaggerated and multi-sensory the image, the more firmly it is retrieved; the more familiar the path, the more stable it is.',
        'This tool generates a code table and practice sequences, purely local, with nothing uploaded.',
        '📚 In-depth: the memory palace method (Method of Loci)',
        'Attach what you need to remember to fixed positions in a familiar space and practice associative memory.',
        'Use it for memorizing vocabulary, lists and competition preparation.',
        '10 shopping items across 5 loci',
        'Pick 5 places at home (door / sofa / table / window / bed) and hang 2 items on each: milk and eggs at the door, apples and bread on the sofa, and so on; walk the route in order to recall, and the 10 items are hard to miss.',
        'Memorizing 5 English words',
        'Place apple, book, cat, dog and sun on 5 room loci, then close your eyes and walk the space once to recite them — more reliable than rote repetition.',
        'How should the loci be chosen?',
        'Use the most familiar route (the way home) with a fixed order; the loci should be vivid and contrasting, and the more exaggerated the image hung on them, the better. The number of loci grows with the content, with 10-20 loci being common.',
        'How many items per locus?',
        'Beginners do best with 1 item per locus; with practice 2-3 works, and more than 3 tend to interfere with each other. The key is that images must be exaggerated, dynamic and emotional (the more absurd, the more memorable), while static and similar items (such as a book lying on a table) get mixed up on recall. It helps to group every 10 loci into a block and leave an empty locus between blocks so adjacent groups do not bleed together.',
        'About memory palace encoding',
        'For example: phone numbers, pi, word lists',
    ]))

    write('mirror-letter', build('mirror-letter', [
        '🏦 Mirror Recognition Practice',
        'Distinguish upright from mirrored letters and numbers, train visual-spatial recognition and prevent reversed writing',
        '/ Mirror Recognition Practice',
        '📖 View the guide to mirror recognition practice',
        'Normal ✅',
        'Mirrored 🪞',
        '📚 In-depth: telling mirrored letters apart (b / d / p / q)',
        'Young children often write left-right mirrored letters backwards; do contrast practice.',
        'Use the baseline method to distinguish easily confused letter shapes.',
        'Telling b and d apart',
        'Take the vertical stroke as the body baseline: b is body plus belly on the right (the loop on the right), while d has the loop on the left; the rhyme is that b draws the stem first and then the loop on the right, and d draws the loop on the left and then the stem.',
        'Distinguishing p and q',
        'p has the loop on the right with the stem descending below the line, and q has the loop on the left with the stem descending below the line. Compare with b (stem up) and d (stem up): the four are located along two dimensions, loop left or right and stem up or down.',
        'Do mirrored letters need correcting?',
        'They are common before school age and mostly resolve with development; if reversals are still frequent after first grade, use tracing plus a baseline and multi-sensory practice (tracing in sand), and avoid attaching negative labels.',
        'How to practice at home?',
        'Use the hand-anchor method: make fists with both hands and extend the thumbs — the left thumb pointing right is b and pointing left is d (the left hand governs b/d), while the right hand corresponds to p/q; combine it with mouth shapes (b closes both lips first, d puts the tongue tip on the upper gum ridge) for more effective multi-channel memory. Practice in the order recognize first, then write: first pick the letter from the sound, then copy it, finally write it from memory, advancing only when each step is correct.',
        'About mirror recognition practice',
    ]))

    write('multiplication-practice', build('multiplication-practice', [
        '📝 Multiplication Table Practice',
        'Level-by-level challenges with an adjustable time limit: advance on a correct answer, retry on a wrong one, to consolidate the nine-times table',
        '/ Multiplication Table Practice',
        '📖 View the guide to multiplication table practice',
        '📚 In-depth: mental multiplication practice',
        'Random questions within a set range, timed, to build mental arithmetic fluency.',
        'Track the accuracy rate to locate weak tables.',
        'One random question from the 2-9 tables',
        'A random question in range such as 7 × 8, answered correctly as 56; do 20 questions in a row against the clock, and 18 correct means 90% accuracy, with mistakes concentrated in the 6/7/8 range that needs work.',
        'Focused practice on a single number',
        'Practice only ×9, from 9 × 1 through 9 × 9, using the trick of tens digit minus 1 and ones digit complement to 10 (9 × 7 = 63: 6 = 7 − 1, 3 = 10 − 7) to speed up.',
        'Why set a time limit?',
        'A time limit forces automatic responses and exposes weak points that are worked out instead of recalled; fix accuracy before speed, then speed up gradually.',
        'What if 7 × 8 and 6 × 7 always trip me up?',
        'These two are well-known high-frequency error points (the results 56 and 42 are adjacent and easy to mix up). Use decomposition instead of rote learning: 7 × 8 = 7 × 10 − 7 × 2 = 70 − 14 = 56; 6 × 7 = 6 × 5 + 6 × 2 = 30 + 12 = 42. Put the questions you miss into a separate wrong-answer book and go through it before each practice session, removing an item after 3 correct answers in a row — far more efficient than drilling the whole table over and over.',
        'About multiplication table practice',
    ]))

    write('stroke-order', build('stroke-order', [
        '🧸 Chinese Character Stroke Breakdown',
        'Demonstrates writing order stroke by stroke with adjustable speed and manual stepping, suited to children learning characters and practicing handwriting',
        '/ Stroke Breakdown',
        '📖 View the guide to Chinese character stroke breakdown',
        'Stroke order is demonstrated by rule: horizontal before vertical, left-falling before right-falling, top to bottom, left to right, outside before inside, middle before sides, enter then close (as in the character for country, write the outer frame first, then the inside, and close it last). Stroke count is taken stroke by stroke across the five basic stroke types — horizontal, vertical, left-falling, dot and turning. The animation holds each stroke for 0.5 to 1 second with a gap of 0.2 to 0.4 seconds between strokes. Writing accuracy = correct stroke order count ÷ total strokes × 100%, used to correct handwriting.',
        'Stroke',
        ' —',
        '📚 In-depth: Chinese character stroke order lookup',
        'Look up the standard writing order of a single character and correct common reversed strokes.',
        'Use it together with tracing practice for standard handwriting.',
        'Stroke order of the character for water',
        'Water (4 strokes): vertical hook → horizontal left-falling → left-falling → right-falling (the central vertical hook first, then the left horizontal left-falling, the right left-falling, closing with the right-falling stroke). A common mistake is putting the left left-falling stroke first.',
        'Stroke order of the character for fire',
        'Fire (4 strokes): dot → short left-falling → long left-falling → right-falling (the two dots first, then the person-shaped left and right falling strokes). Sides before the middle applies to characters such as fire and small.',
        'Is there a mandatory standard for stroke order?',
        'Yes — the Standard Stroke Order of Commonly Used Characters in Modern Chinese. It does not affect reading, but it affects writing speed and calligraphic beauty, and exams are written to that standard.',
        'Why does the way I write differ from the lookup?',
        'Three common reasons: ① mainland standards (horizontal before vertical, left-falling before right-falling, top to bottom, left to right, outside before inside then close) differ slightly from the stroke forms used in Hong Kong, China and Taiwan, China (for example the first stroke of the characters for heart and must); ② some characters have old and new forms (such as those for bone and to pass); ③ printed typefaces (Song style) and handwritten forms differ (such as the second stroke of the character for day). Write according to the Standard Stroke Order of Commonly Used Characters in Modern Chinese; in daily use it is enough not to reverse strokes or harm speed and legibility.',
        'About Chinese character stroke breakdown',
    ]))


if __name__ == '__main__':
    main()
