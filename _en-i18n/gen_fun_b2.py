# -*- coding: utf-8 -*-
"""fun 行业正文英文化 batch2（第 11~20 个工具）。位置对齐法：从 work json 读取原始 zh，与英文列表按序配对。"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_biz_apply import apply_tool

IND = 'fun'
WORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'work', 'fun')

def build(slug, name_zh, en_list):
    path = os.path.join(WORK, slug + '.json')
    with open(path, encoding='utf-8') as f:
        wj = json.load(f)
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('!! %s 长度不一致: en=%d items=%d' % (slug, len(en_list), len(items)))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        z = it['zh'].strip()
        if not en or not isinstance(en, str):
            print('!! %s 空译文 for %r' % (slug, z))
            sys.exit(1)
        mp[z] = en
    return mp

# ---------------- coin-flip ----------------
G = build('coin-flip', '抛硬币', [
    '🪙 Coin Flip',
    'Classic coin-flip decision tool: heads or tails?',
    '📖 View "Coin Flip Decider User Guide"',
    'Each flip draws a random number: result = heads if random() >= 0.5 else tails, each with 50% probability; the chance of the same face n times in a row = 0.5 to the n (e.g. 5 heads in a row ~3.125%); the expected heads count over many flips = flips x 0.5, and by the law of large numbers the heads/tails ratio approaches 1:1.',
    'Heads',
    'Tails',
    'Tap the button to flip',
    'Flip 10 times in a row',
    'Heads',
    'Tails',
    '📜 Recent results',
    '📚 Deep Dive: Coin Flip Decider',
    'Either-or decision: when torn between "which restaurant / buy or not", leave it to a 50:50 random.',
    'Game call: act as a fair referee in board games or bets (heads/tails, each half).',
    'Random draw: quickly produce heads or tails when an unbiased result is needed.',
    'Method (random rule)',
    'Each click randomly outputs heads or tails, theoretical probability 50% each; front-end pseudo-random is enough for entertainment decisions, no network, no storage.',
    'Click once -> heads; by the law of large numbers, 100 flips should approach 50:50 (e.g. 48 heads 52 tails), and a single result has no memory. Use it for even choices like "hotpot or stir-fry today".',
    'Is it truly random?',
    'Browser pseudo-random, statistically ~50:50, enough for fun; not cryptographic-grade random, do not use for serious draws.',
    'Can I set a bias?',
    'This tool is fixed at fair 50:50; for weighted results use a weighted random picker.',
    'About "Coin Flip"',
    'Coin Flip is an online tool in the entertainment category. Pure front-end, no install, playable offline.',
])
apply_tool('coin-flip', '抛硬币', 'Coin Flip', G, ind=IND)

# ---------------- coin-toss-streak ----------------
G = build('coin-toss-streak', '抛硬币连胜统计', [
    '📈 Coin Flip Streak Stats',
    'This tool is a pure front-end online tool; data is processed locally in your browser and not uploaded to any server, computed per relevant standards and specs, for reference only. Tool name: Coin Flip Streak Stats - a free fun game tool, online Coin Flip Streak Stats, free to use.',
    '📖 View "Coin Flip Streak Stats User Guide"',
    'Streak: 0',
    'Click "Start" to begin flipping',
    'Longest streak',
    'Heads rate',
    'Flip once',
    'Flip 10 in a row',
    '📚 Deep Dive: Coin Flip Streak Stats',
    'Probability demo: flip continuously and record the longest streak (consecutive heads) to feel the runs of randomness.',
    'Streak record: challenge "most consecutive heads" and save your personal best.',
    'Fun stats: compare the actual distribution with the theoretical (1/2)^k probability.',
    'Method (streak stats)',
    'Flip continuously and record the sequence, counting the longest streak (consecutive heads) and the frequency of each length; pure front-end local run. The theoretical probability of a single "k heads in a row" = (1/2)^k.',
    'A 20-flip sequence "H H T H H H H T H T H H H H H T H T": longest heads run = 6 (positions 6-11), theoretical probability of 6 heads in a row (1/2)^6 = 1/64 ~ 1.56%; 8 heads in a row is only 0.39%, so long runs are rare but eventually appear.',
    'Does a streak affect the next flip?',
    'No. Each flip is independent and memoryless; "tails is due" is the gambler fallacy, long runs are rare but the probability stays constant.',
    'How does it differ from coin-flip?',
    'coin-flip gives only a single heads/tails; this tool records the whole sequence and stats the longest streak and distribution, suited to probability demos.',
    'About "Coin Flip Streak Stats"',
    'Coin Flip Streak Stats. An entertainment game tool, pure front-end, no install, playable offline.',
])
apply_tool('coin-toss-streak', '抛硬币连胜统计', 'Coin Flip Streak Stats', G, ind=IND)

# ---------------- color-guess ----------------
G = build('color-guess', '猜颜色', [
    '🎨 Color Guessing',
    'This tool is a pure front-end online tool; data is processed locally in your browser and not uploaded to any server, computed per relevant standards and specs, for reference only. Tool name: Color Guessing - an online tool in the entertainment category.',
    '📖 View "Color Recognition Guessing Game User Guide"',
    '📚 Deep Dive: Color Recognition Guessing Game',
    'Color training: see a random color swatch and guess by eye',
    'color name',
    'or HEX code.',
    'Design primer: learn common colors and their HEX mapping, training your color intuition.',
    'Scoring challenge: instant right/wrong feedback, recording accuracy and best score.',
    'Method (color guessing rules)',
    'Show a random swatch (with HEX); the player enters a color name or HEX to answer; correct within tolerance with instant feedback, scoring over multiple rounds. Difficulty can narrow the range by color family.',
    'Show #3CB371 (mediumseagreen) -> guessing "green" is correct; show #FF6347 (tomato) -> guessing HEX must be close (passes within tolerance). 7/10 correct gives 70 points; keener color sense scores higher.',
    'Must the HEX be exact digit by digit?',
    'No. Correct within the set color-difference tolerance; the focus is broad hue recognition, not memorizing codes.',
    'Can color-blind users use it?',
    'It can serve as training, but for those with color-vision deficiency the result is for reference only; do not use it for professional color decisions.',
    'About "Color Guessing"',
    'Color Guessing is an online tool in the entertainment category. Pure front-end, no install, playable offline.',
])
apply_tool('color-guess', '猜颜色', 'Color Guessing', G, ind=IND)

# ---------------- color-memory ----------------
G = build('color-memory', '颜色记忆', [
    '🌈 Color Memory (Simon)',
    'This tool is a pure front-end online tool; data is processed locally in your browser and not uploaded to any server, computed per relevant standards and specs, for reference only. Tool name: Color Memory - an online tool in the entertainment category.',
    'Color Memory',
    '/ Color Memory',
    '📖 View "Color Memory (Simon) Game User Guide"',
    'Watch and repeat the color sequence',
    '📚 Deep Dive: Color Memory (Simon) Game',
    'Brain training: follow and reproduce a gradually lengthening color sequence, challenging short-term memory.',
    'Multi-sensory aid: the sequence comes with lights and sound, helping encode and recall.',
    'Level progression: each cleared level adds 1 to the sequence, recording the longest length achieved.',
    'Method (sequence rules)',
    'The tool plays the color sequence by lighting up and sounding each in turn; the player reproduces it exactly; each level adds 1 item, and one mistake ends the round, recording the length achieved.',
    'Level 1 sequence [red, blue], level 3 [red, blue, green, yellow]; if the player errs at item 4, the "achieved length 3" is recorded. Experts recall 20+; grouping or naming (e.g. turning "red blue green yellow" into a word) extends memory markedly.',
    'How to remember longer sequences?',
    'Turn colors into rhythm or words and recall in chunks rather than rote single lists; sound cues also help encoding.',
    'Is there sound?',
    'Yes. Lights pair with tone cues; multi-sensory input lowers memory load.',
    'About "Color Memory"',
    'Color Memory is an online tool in the entertainment category. Pure front-end, no install, playable offline.',
])
apply_tool('color-memory', '颜色记忆', 'Color Memory (Simon)', G, ind=IND)

# ---------------- convert-speed-stride ----------------
G = build('convert-speed-stride', '步幅与速度换算（步频×步长）', [
    '🏎️ Stride & Speed Converter (Cadence x Stride)',
    'Cadence x stride',
    '📖 View "Cadence & Stride Converter User Guide"',
    'Velocity = cadence x stride',
    'Stride',
    'Stride (mm)',
    'Stride (km)',
    'Speed (mm)',
    'Speed (km)',
    '📚 Deep Dive: Cadence & Stride Converter',
    'Walking pace: estimate walk/run speed from cadence x stride to set a target pace.',
    'Gait analysis: back-solve the needed cadence or stride from a target speed to adjust form.',
    'Workout log: convert phone step data into distance and pace to verify the track.',
    'Method (conversion formula)',
    'Velocity = cadence (steps/min) x stride (m/step); inversely cadence = speed / stride. Stride can be measured as "distance of 10 steps / 10".',
    'Cadence 110 steps/min, stride 0.75 m -> speed = 110 x 0.75 = 82.5 m/min = 4.95 km/h (walking pace ~12 min/km); for a 6 km/h target with 0.75 m stride, required cadence = 6000/60/0.75 ~ 133 steps/min. Running stride is often 0.9-1.4 m.',
    'How to measure stride accurately?',
    'Walk 10 normal steps on flat ground, measure total distance / 10 for average stride; measure separately while running, since running stride is clearly larger.',
    'Why does the converted speed differ a lot from my watch?',
    'Watches fuse GPS/accelerometer; this tool is a theoretical conversion; only with a measured stride does it come close, so use it for estimation only.',
    'About "Stride & Speed Converter (Cadence x Stride)"',
    'Stride & Speed Converter (Cadence x Stride). An entertainment game tool, pure front-end, no install, playable offline.',
])
apply_tool('convert-speed-stride', '步幅与速度换算（步频×步长）', 'Stride & Speed Converter (Cadence x Stride)', G, ind=IND)

# ---------------- cps-test ----------------
G = build('cps-test', 'CPS 测试', [
    '🖱️ CPS Test',
    'This tool is a pure front-end online tool; data is processed locally in your browser and not uploaded to any server, computed per relevant standards and specs, for reference only. Tool name: CPS Test - a free fun game tool, online CPS Test, free to use.',
    '📖 View "CPS Click Speed Test User Guide"',
    'Click count: ',
    'Best CPS: ',
    'Click as many times as possible within 10 seconds',
    '📚 Deep Dive: CPS Click Speed Test',
    'Hand-speed challenge: click frantically within the time limit to find your CPS ceiling.',
    'Device comparison: test mouse / trackpad / touchscreen separately to compare input differences.',
    'Fun rating: rate as slow / average / good / strong by CPS threshold, recording your best.',
    'Method (rating rule)',
    'Click continuously within the set duration; CPS = total clicks / duration (clicks/sec); grade by threshold: slow <4, average 4-7, good 8-11, strong >12.',
    '40 clicks in 5 s -> CPS = 40/5 = 8.0, rated "good"; 65 clicks gives 13.0, "strong". Ordinary players commonly hit 6-10; >14 is mostly auto-clickers or extreme speed.',
    'How does it differ from click-speed?',
    'Both share the same origin; cps-test emphasizes the CPS rating threshold, while click-speed leans toward real-time count and hand-speed comparison, complementing each other.',
    'Why is the touchscreen lower?',
    'The system debounces continuous touches, capping click rate; mechanical mice more easily reach high CPS.',
    'About "CPS Test"',
    'CPS Test. An entertainment game tool, pure front-end, no install, playable offline.',
])
apply_tool('cps-test', 'CPS 测试', 'CPS Test', G, ind=IND)

# ---------------- daily-riddle ----------------
G = build('daily-riddle', '每日谜题挑战', [
    '🧩 Daily Riddle Challenge: Date Seed · 3-tier Hints · Combo Points',
    "One Chinese riddle or brain teaser per day, seeded by the current date so everyone gets the same puzzle on the same day and a new one appears the next day. Supports 3-tier keyword hints, scoring, combo records and difficulty choice, plus a 'beat x% of players' percentile estimate; scores and combos are saved locally and survive refresh.",
    'Daily Riddle Challenge',
    '/ Daily Riddle Challenge',
    '📖 View "Daily Riddle Challenge User Guide"',
    'Easy',
    'Medium',
    'Hard',
    'Total points',
    'Current combo',
    'Best combo',
    'Loading...',
    'Use your brain; hints are available below.',
    'No hints used yet. Click the buttons below to reveal keywords one by one.',
    'Hint 1',
    'Hint 2',
    'Hint 3',
    'Reveal answer',
    'History of answers (saved locally)',
    'Note: the "beat x% of players" percentile here is a fun estimate simulated from the difficulty baseline and number of hints used, not real statistics; riddle answers are mainly Chinese, and spaces and punctuation are auto-ignored on submission.',
    '📚 Deep Dive: Daily Riddle',
    'Daily challenge: same puzzle worldwide on the same day, seeded by date; race friends to solve first.',
    'Tiered hints: 3 difficulty levels + 3 hint levels, gradually revealing keywords when stuck.',
    'Points and combo: consecutive correct answers build a combo multiplier; an answer calendar tracks your streak days.',
    'Method (puzzles and scoring)',
    'Puzzles are generated from a date seed (same for everyone on the same day), with 3 difficulty levels and 3 expandable hints; correct answers score, consecutive correct answers trigger a combo multiplier, and the answer calendar marks consecutive check-in days. The puzzle bank keeps expanding.',
    'On a certain day a medium puzzle gives 3 hints in order: "animal / can fly / migratory bird" -> answer "wild goose"; correct +10 points, and if combo x3 then +30 that day. 7 consecutive correct days unlock a calendar badge; a missed day resets the combo but the calendar keeps history.',
    'Does everyone get the same puzzle on the same day?',
    'Yes. Generated by date seed, same worldwide, convenient for fair competition and discussion.',
    'Do hints deduct points?',
    'Hints themselves do not subtract points, but expanding a hint breaks the combo multiplier; to score high, use fewer hints.',
])
apply_tool('daily-riddle', '每日谜题挑战', 'Daily Riddle Challenge', G, ind=IND)

# ---------------- emoji-memory ----------------
G = build('emoji-memory', 'Emoji 记忆游戏', [
    '😊 Emoji Memory Game',
    'This tool is a pure front-end online tool; data is processed locally in your browser and not uploaded to any server, computed per relevant standards and specs, for reference only. Tool name: Emoji Memory Game - a free fun game tool, online Emoji Memory Game, free to use.',
    '📖 View "Emoji Memory Matching Game User Guide"',
    '📚 Deep Dive: Emoji Memory Matching Game',
    'Memory training: flip cards to find matching Emoji pairs, training visual memory and focus.',
    'Level up: the number of pairs grows with levels, difficulty rising gradually.',
    'Casual relax: pure front-end, playable offline, records fewest steps / time.',
    'Method (matching rules)',
    'The board starts all covered; flip two each turn; if identical they clear, otherwise they cover again; clear all pairs to pass. Higher levels have more pairs.',
    'Level 1 has 6 pairs (12 cells), clear all to pass; level 3 has 10 pairs (20 cells). Record fewest flips and time; more mis-flips mean more steps, and "position coding" reduces re-flipping.',
    'How to memorize cards faster?',
    'Number positions in your head when flipping the first card; after a mismatch, remember where those two were and pair them next time.',
    'Are there hints?',
    'A wrong flip auto-covers, which is itself a "negative hint"; some versions offer a timed preview.',
    'About "Emoji Memory Game"',
    'Emoji Memory Game. An entertainment game tool, pure front-end, no install, playable offline.',
])
apply_tool('emoji-memory', 'Emoji 记忆游戏', 'Emoji Memory Game', G, ind=IND)

# ---------------- fingerprint-types ----------------
G = build('fingerprint-types', '指纹纹路分类演示', [
    '🎮 Fingerprint Pattern Demo',
    'Human fingerprints are mainly divided into three basic types: loop, whorl and arch. Switch to view the features and illustration of each pattern.',
    '📖 View "Fingerprint Type Identifier User Guide"',
    'Fingerprints are classified by the number of triradii into three categories: arch (no triradius, ridges form an arch, ~5%), loop (one triradius, ridges enter from one side and return on the same side, ~60%-65%), whorl (two triradii, ridges form concentric rings or spirals, ~30%-35%); a simple dermatoglyphic trait analysis can be done from the count of whorl and loop fingers.',
    '🎯 Whorl',
    '🔁 Loop',
    '🏔️ Arch',
    '📊 Fingerprint Distribution & Trivia',
    'Loop (most common)',
    'Whorl',
    'Arch',
    'Probability of identical fingerprints',
    'Fingerprints form at about 10-24 weeks of fetal life, determined by genes and the uterine environment, unchanged for life and unique.',
    'Even identical twins have different fingerprints because of micro-environmental differences during development.',
    'Whorl, also called spiral, has a center of spirals or concentric circles; loop has a triradius and ridges open to one side; arch has smoothly raised ridges without a triradius.',
    '📚 Deep Dive: Fingerprint Type Identifier',
    'Science awareness: learn the three basic fingerprint types and their features.',
    'Forensic primer: understand the rough distribution of whorl/loop/arch as a hobby.',
    'Creative reference: quickly grab pattern descriptions for character design or art.',
    'Method (three-way classification)',
    'By Galton three-way classification, fingerprints split into whorl (spiral/concentric, central swirl), loop (like a dustpan opening to one side) and arch (parallel raised ridges, no swirl); switch to view each pattern illustration.',
    'Rough population distribution: loop ~60%-70%, whorl ~25%-35%, arch ~5%-10% (varies by population). Note: the pattern is only a broad class; individual identification relies on minutiae (detail points), not the class.',
    'Can fingerprints uniquely identify a person?',
    'Yes, but it relies on the spatial relationships of ridge minutiae (endings/bifurcations), not the whorl/loop/arch class; the class is only a coarse split.',
    'Why only three classes?',
    'Galton three-way is the most classic framework, with finer subtypes later; this tool focuses on the three basic types for science popularization.',
    'About "Fingerprint Pattern Demo"',
    'Fingerprint Pattern Demo is an online tool in the quick-reference category, introducing the features, proportions and identification points of the three basic fingerprint types whorl, loop and arch, with SVG illustrations.',
    'Classification of the three fingerprint patterns',
    'SVG illustration with triradius annotation',
    'Population proportion and identification points',
    'Fingerprint trivia',
    'Biometrics knowledge',
    'Dermatoglyphics interest',
    'Classroom and parent-child interaction',
    'Fun forensic common-sense reading',
])
apply_tool('fingerprint-types', '指纹纹路分类演示', 'Fingerprint Pattern Demo', G, ind=IND)

# ---------------- generator-2 ----------------
G = build('generator-2', '数独生成器 / 求解器', [
    '🧩 Sudoku Generator / Solver',
    'Sudoku Generator / Solver online tool',
    '📖 View "Sudoku Generator/Solver User Guide"',
    'Sudoku is a 9x9 grid divided into 9 blocks of 3x3; the constraint is that each row, column and block contains 1-9 without repetition. Generation first fills a valid solution by backtracking (trying 1-9 per cell and checking constraints), then digs holes by difficulty (easy keeps ~36-45 given, hard ~26-30) and verifies a unique solution; solving uses backtracking with candidate pruning.',
    '📚 Deep Dive: Sudoku Generator/Solver',
    'Casual practice: pick difficulty to generate a puzzle with one click, with a reference answer.',
    'Solve aid: paste a stuck puzzle and the tool backtracks to give the full grid.',
    'Teaching demo: understand constraint satisfaction and backtracking algorithms.',
    'Method (generation and solving)',
    'On a 9x9 board, generation digs holes by difficulty and guarantees a unique solution; solving uses backtracking to try numbers cell by cell satisfying no-repeat in row/column/block. Pasted puzzles can also be solved in reverse.',
    'Holes by difficulty: easy ~40, medium ~50, hard ~55+ (of 81 cells). Valid complete Sudoku grids number about 6.67x10^21; the generator guarantees a unique solution per puzzle to avoid multi-solution disputes.',
    'Is the generated puzzle guaranteed unique?',
    'Yes. The generation flow verifies uniqueness, ensuring exactly one valid filling.',
    'Can I adjust difficulty myself?',
    'Choose difficulty by number of holes; for extreme difficulty you can dig more manually, but too many may break uniqueness.',
    'About "Sudoku Generator / Solver"',
    'Sudoku Generator / Solver. An entertainment game tool, pure front-end, no install, playable offline.',
])
apply_tool('generator-2', '数独生成器 / 求解器', 'Sudoku Generator / Solver', G, ind=IND)

print('gen_fun_b2 done')
