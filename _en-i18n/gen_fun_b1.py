# -*- coding: utf-8 -*-
"""fun 行业正文英文化 batch1（前 10 个工具）。逐条语义化翻译；值纯英文避开 CJK/中文标点。
采用位置对齐法：从 work json 读取原始 zh（保证键零误差），与本文件中的英文列表按序配对。
每次新增/调整只需保证英文列表与 work json 条目顺序一致、长度一致。
校验：长度一致、无空译文、apply_tool 再做零 CJK/零中文标点硬校验。"""
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

# ---------------- 1a2b-guess ----------------
G1 = build('1a2b-guess', '1A2B 猜数字', [
    '🎮 1A2B Number Guessing: Logic Puzzle · Bulls & Cows',
    'Classic 1A2B (Bulls and Cows) logic game: the computer generates a set of non-repeating digits, you guess a combination each round, and the system gives an xAyB hint — A means digit and position both correct, B means digit correct but position wrong. With a reasoning aid table and possible-solution counter, crack the answer in the fewest steps.',
    '1A2B Number Guessing',
    '/ 1A2B Number Guessing',
    '📖 View "1A2B Number Guessing (Bulls & Cows) User Guide"',
    '4 digits · no repeat',
    '4 digits · repeatable',
    '5 digits · no repeat',
    'Best: —',
    'No guesses yet; enter your first combination to start reasoning.',
    'Guess!',
    'Show number pad (mobile-friendly)',
    'New round',
    'Give up / reveal answer',
    'Clear input',
    'This round stats',
    'Steps used',
    'Possible solutions',
    'Current mode',
    'Chances left',
    'Unlimited',
    'Rule cheat-sheet',
    ': digits and positions all correct',
    ': digit correct but wrong position',
    'e.g. answer',
    ', guess',
    '(1 correct, 3 misplaced).',
    'Best record',
    'Tip: prioritize "probing" combinations to cover more digits and narrow down by xAyB step by step; the "possible solutions" count on the right shrinks fast with each valid guess and is basically locked once it nears 1. All data is stored only in your local browser.',
    '📚 Deep Dive: 1A2B Number Guessing Game',
    'Logic warm-up: given a 4-digit non-repeating answer, after each guess you get xAyB feedback (A = digit and position both correct, B = digit correct but position wrong) and narrow the candidates round by round.',
    'Teaching demo: use the feedback for elimination reasoning to train deductive thinking, suited to introductory math/programming lessons.',
    'Vs computer: set difficulty (4/5 digits) and challenge yourself to clear in the fewest steps, recording your best score.',
    'Method (xAyB rule)',
    'The answer is 4 distinct digits; after you guess 4 digits the system returns "xAyB": A = count of digits both correct in value and position, B = count of digits correct in value but wrong in position. Example: answer 1234, you guess 1243 -> 1 and 2 in position (2A), 3 and 4 correct values swapped (2B), giving 2A2B.',
    'Example (reasoning demo)',
    'Suppose the answer is 5072. Guess 1: 1234 -> 0A1B (only 2 correct value, wrong position); Guess 2: 5678 -> 1A1B (5 correct position, 7 correct value wrong position); Guess 3: 5076 -> 3A0B (5/0/7 all hit, 6 wrong); Guess 4: 5072 -> 4A0B, solved. Solved in 4 steps. Higher difficulty means more digits, and the candidate space grows factorially with digit count.',
    'Why sometimes few A but many B?',
    'B means the digit is in the answer but in the wrong column; A+B is the "total number of matched digits", so you can lock the already-positioned digits and only adjust the positions of the B-class digits.',
    'Fewest steps to guarantee a hit?',
    'There is no fixed upper bound; it depends on the information per feedback. Skilled players often solve 4 digits in 5-8 steps; the key is to intersect candidate sets with each xAyB rather than guessing blindly.',
])
apply_tool('1a2b-guess', '1A2B 猜数字', '1A2B Number Guessing', G1, ind=IND)

# ---------------- 2048-game ----------------
G2 = build('2048-game', '2048 游戏', [
    '🎮 2048 Game',
    'Arrow keys / WASD to move, U to undo',
    '📖 View "2048 Number Merge Game User Guide"',
    'Game',
    'Leaderboard',
    'Current score',
    'Largest tile',
    '↩️ Undo',
    '🏆 Records',
    'Best score: ',
    'Largest tile: ',
    'Use arrow keys or swipe to move all tiles',
    'Two tiles with the same number merge into their sum on collision',
    'After each move a new 2 or 4 appears at random',
    'Merge up to 2048 to win!',
    'The game ends when no move is possible',
    'Keep the largest number in a corner',
    'Keep one row or column monotonic (increasing/decreasing)',
    'Avoid moving the large number frequently',
    'Keyboard',
    ': arrow keys or WASD',
    ': U key',
    'Mobile',
    ': swipe the screen',
    '📚 Deep Dive: 2048 Number Merge Game',
    'Casual challenge: slide on a 4x4 grid; identical numbers merge into double, aim to reach the 2048 tile.',
    'Strategy training: keep the largest tile in a corner and same values adjacent in a column; avoid a fragmented board that cannot merge.',
    'Algorithm demo: understand the deterministic rules of grid move and merge, suited to explaining state transitions.',
    'Method (merge rules)',
    'Each slide in one direction first packs all tiles in that row/column, then merges adjacent equal pairs once from left to right (or the corresponding direction): two equal numbers merge into double and score; each tile merges at most once per slide. After each valid move a new 2 (90%) or 4 (10%) spawns in an empty cell.',
    'Example (merge demo)',
    'A row [2,2,4,empty] slid left -> 2+2 merges into 4, giving [4,4,empty,empty]; slide left again -> 4+4 merges into 8, giving [8,empty,empty,empty], scoring +8 this step. Reaching 2048 needs at least 11 levels of "2" merges (2^11=2048), so about 11 effective merges minimum.',
    'Why do I keep getting stuck at 512?',
    'Common cause: the largest tile drifts away from the corner and several different large tiles cannot sit adjacent; fix the largest in a corner and stack the second-largest next to it in the same column.',
    'Is spawning a 4 harder than a 2?',
    'Each new tile is 90% a 2 and 10% a 4; a 4 speeds up slightly but fills cells faster, so you still must manage empty space and avoid early gridlock.',
    'Game over',
    'No more moves available',
    'Congratulations!',
    'You merged 2048!',
    'Keep challenging',
    'About "2048 Game"',
    '2048 Game. An entertainment game tool, pure front-end, no install needed, playable offline.',
])
apply_tool('2048-game', '2048 游戏', '2048 Game', G2, ind=IND)

# ---------------- anagram-game ----------------
G3 = build('anagram-game', '字谜游戏', [
    '🔤 Anagram Game',
    'Make as many English words as possible from the given letters (at least 3 letters)',
    '📖 View "Letter Rearrangement Word Game User Guide"',
    'Anagram combinations = n! / product of (each repeated letter count!); enumerate subsets of length >=3 from the letter set, generate full permutations, compare against a dictionary and deduplicate to get all spellable words; output sorted by descending length or alphabetical order, with scores often based on word length or rarity.',
    '📚 Deep Dive: Letter Rearrangement Word Game',
    'Vocabulary training: given a set of English letters, find all spellable English words of >=3 letters to practice vocabulary and spelling.',
    'English teaching: sort results by length or alphabetical order for classroom vocabulary expansion and spelling contests.',
    'Brain exercise: within a time limit, spell as many words as possible and record the hit count and longest word.',
    'Method (rearrangement rules)',
    'Input or randomly get a set of letters (e.g. 6), the tool exhaustively enumerates all subsequences that use each letter at most once and have length >=3, checks each against a word list, and lists the hits; results can be sorted by descending length or alphabetical order.',
    'Example (word demo)',
    'The letter set LISTEN can rearrange into SILENT, TINSEL, ENLIST, INLETS, LISTEN, etc.; taking 5-letter subsets yields LINES, TILES, SLIME, EMITS, ISLET, etc. The full permutations of 6 distinct letters is 6! = 720, but valid English words are a small fraction, so the tool only outputs dictionary hits.',
    'Can letters be reused?',
    'By default each given letter is used at most once per word (matching the letter multiplicity of the source); if the source has repeated letters, reuse within that multiplicity is allowed.',
    'Why are results fewer than',
    'the permutation count',
    '?',
    'Of the 720 permutations, the vast majority are scrambled non-words; only those passing the word-list check are listed, so the valid words usually number from a dozen to a few dozen.',
    'About "Anagram Game"',
    'The Anagram Game is an online tool in the entertainment category. Pure front-end, no install, playable offline.',
])
apply_tool('anagram-game', '字谜游戏', 'Anagram Game', G3, ind=IND)

# ---------------- bbq-portion ----------------
G4 = build('bbq-portion', '烧烤食材分量计算器', [
    '🧮 BBQ Ingredient Portion Calculator',
    'Outdoor BBQ shopping is easy to over- or under-buy. Enter the number of people and appetite to get quantity suggestions for skewers, seafood, vegetable sticks and drinks, balancing meat and vegetables.',
    '/ BBQ Ingredient Portion Calculator',
    '📖 View "Outdoor BBQ Shopping Calculator User Guide"',
    'Meat ~ people x 150-200 g; seafood ~ people x 100-150 g; vegetables ~ people x 100 g; drinks ~ people x 500 mL',
    'Outdoor BBQ is estimated by per-person intake per meal: meat 150-200 g, seafood 100-150 g, vegetables ~100 g, drinks 500 mL; then multiply by an appetite factor (small 0.8 / medium 1.0 / large 1.3), and adjust the meat-veg ratio to about 2:1, with charcoal amount scaled to grilling time and food volume, to avoid over-buying waste or under-buying shortage.',
    'BBQ type',
    'Chinese skewers',
    'Korean BBQ',
    'Steak / roast',
    'Include drinks',
    'Include alcohol',
    '📚 Deep Dive: Outdoor BBQ Shopping Calculator',
    'Party shopping: enter the number of people and category (Chinese skewers / Korean BBQ / steak) to estimate total skewers, meat, vegetables and drinks, avoiding over-buying waste or under-buying shortage.',
    'Meat-veg balance: give vegetable and staple/snack ratios by per-person reference amount to balance the meal structure.',
    'Drink budget: when alcohol is included, estimate total consumption at 700 mL per person to ease case purchasing.',
    'Method (per-person reference)',
    'Chinese skewers: 12 skewers and 350 g meat per person; Korean BBQ: 450 g meat per person (no skewers); steak/roast: 400 g meat per person; 200 g vegetables per person; 150 g staples/snacks per person; 700 mL per person with drinks. Total = per-person amount x people.',
    '6 people, Chinese skewers, with drinks: skewers = 6x12 = 72; meat = 6x350 = 2100 g (2.1 kg); vegetables = 6x200 = 1200 g (1.2 kg); staples = 6x150 = 900 g; drinks = 6x700 = 4200 mL (4.2 L, about two 2 L bottles or six 700 mL cans). Switching to Korean BBQ removes skewers and meat = 6x450 = 2700 g.',
    'How to adjust for big eaters?',
    'This tool gives a per-person baseline; in practice raise meat by "+20%-30% for big eaters", or reserve 10% extra to handle unplanned guests.',
    'Why no skewer count for Korean style?',
    'Korean BBQ is measured by meat weight (450 g per person), not by skewers; Chinese skewers list skewer counts separately, so the two use different units.',
    'Chinese skewers: 12 skewers and 350 g meat per person; Korean BBQ: 450 g meat per person',
    'Vegetables 200 g and staples/snacks 150 g per person as reference',
    'Drinks estimated at 700 mL per person (with alcohol)',
    'The above are shopping references; adjust to your gathering habits in practice',
])
apply_tool('bbq-portion', '烧烤食材分量计算器', 'BBQ Ingredient Portion Calculator', G4, ind=IND)

# ---------------- bingo-generator ----------------
G5 = build('bingo-generator', '活动随机号码生成器', [
    '🎱 Event Random Number Generator',
    'This tool is a pure front-end online tool; data is processed locally in your browser and not uploaded to any server, computed per relevant standards and specs, for reference only. Tool name: Classroom / Event Random Number Generator - an online tool in the entertainment category.',
    'Event Random Number Generator',
    '/ Classroom / Event Random Number Generator',
    'Classroom / Event Random Number Generator',
    '📖 View "Bingo Card Generator User Guide"',
    '⚠️ This tool is an aid for random draws / number generation at annual parties, classrooms, team-building and similar events; the process is open and reproducible, results are random, and it involves no gambling, prizes or money transactions. Do not use it for betting.',
    'Click cells to mark them; connect a row / column / diagonal to win',
    'Generate new card',
    'Reset marks',
    '📚 Deep Dive: Random Number Generator (Classroom / Event)',
    'Party game: generate printable 5x5 bingo cards with a center FREE cell, randomly filled from the selected word bank and deduplicated.',
    'Classroom activity: map the word bank to knowledge points; players cross off words they hear and form a line for bingo, livening up the atmosphere.',
    'Fun draw interaction: fill cells with prizes / names and spin or flip for a fun draw.',
    'Method (card structure)',
    'Standard bingo is 5 columns x 5 rows = 25 cells; the center 13th cell is fixed as FREE, and the other 24 are randomly drawn without repetition from the word bank; columns may map to B-I-N-G-O letter themes.',
    'Generate 1 card from a 30-word bank: the system randomly draws 24 distinct words to fill the non-FREE cells (center FREE fixed), each row/column/diagonal has 5 cells. For 5 people each with a different card, each independently draws 24 distinct combinations from the 30 words; repeated words are normal and the chance of an identical whole card is extremely low.',
    'What if the word bank has fewer than 24 words?',
    'It will warn that the word count is insufficient to fill 24 cells; you need at least 24 distinct words (or allow repeated fills); a word bank >=30 is recommended to keep each card non-repeating.',
    'Must the FREE cell be in the center?',
    'In classic play FREE is the center 13th cell; it can be customized, but a center FREE is the conventional "starting cell".',
    'About "Classroom / Event Random Number Generator"',
    'The Classroom / Event Random Number Generator is an online tool in the entertainment category. Pure front-end, no install, playable offline.',
])
apply_tool('bingo-generator', '活动随机号码生成器', 'Event Random Number Generator', G5, ind=IND)

# ---------------- blink-counter ----------------
G6 = build('blink-counter', '眨眼次数统计', [
    '📊 Blink Count Tracker',
    'Pick a duration, start the timer, and tap the button each time you blink to track your blink rate (normal adults ~15-20 blinks/min).',
    '📖 View "Blink Rate Counter User Guide"',
    'Blink rate = count / duration (min); resting normal adults ~15-20/min, dropping to 5-10/min when reading or on screens; average interval = total seconds / count; below 10/min signals eye fatigue, so every 20 minutes look far for 20 seconds and blink actively to keep the tear film stable.',
    'Test duration',
    '120 seconds',
    '300 seconds',
    'Blink count',
    '👆 Tap to record one blink',
    'After clicking "Start Test", timing and counting begin.',
    '💡 Blink trivia',
    'Average adult blinks per minute',
    '15-20 times',
    ', about 0.1-0.4 seconds each.',
    'Blink rate drops to',
    '5-7 times/min',
    ', easily causing dry, tired eyes.',
    'Too few blinks may trigger dry eye; follow the 20-20-20 rule: every 20 minutes of screen use, look 20 feet away for 20 seconds.',
    '📚 Deep Dive: Blink Rate Counter',
    'Eye-care self-assessment: set a duration (30/60/120/300 s), tap once per blink, and count blinks per unit time.',
    'Focused observation: compare blink rate when reading intently vs zoning out to understand the "staring, fewer blinks" effect in front of screens.',
    'Science demo: verify the common range of "normal adults ~15-20 blinks/min".',
    'Method (',
    'frequency conversion',
    'Recording total blinks N over duration T seconds, frequency = N / T x 60 (per min); average interval = T / N (sec/blink) can also be computed.',
    'Pick 60 s and tap 18 times: rate = 18/60x60 = 18/min, within the normal 15-20 range; average interval = 60/18 ~ 3.3 s/blink. If you blink only 5 times in 60 s of screen use, that is 5/min, interval 12 s, clearly low (staring, fewer blinks), so blink more actively to prevent dry eye.',
    'Is below 15 blinks/min normal?',
    'Screen use or focus often drops it to 5-10; chronically low easily dries the eyes. It is a reminder signal, not a disease; consciously complete your blinks.',
    'Why do results fluctuate a lot each time?',
    'Blinking is strongly affected by attention, dry environment and fatigue; a single measurement is for reference only, so take the average of several.',
    'About "Blink Count Tracker"',
    'Blink Count Tracker is an online tool in the entertainment category; by manually tapping to record blinks it counts blinks per minute, helping you understand eye health, with history and eye-care tips.',
    'Adjustable timer with countdown ring',
    'Tap to count with blink animation feedback',
    'Auto-convert to blinks per minute',
    'Eye-health self-test',
    'Eye-care science interaction',
    'Fun classroom experiment',
    'Reminder to relax after prolonged eye use',
])
apply_tool('blink-counter', '眨眼次数统计', 'Blink Count Tracker', G6, ind=IND)

# ---------------- blood-type-personality ----------------
G7 = build('blood-type-personality', '血型性格分析', [
    '📊 Blood Type Personality Analysis',
    'Explore the personality traits, strengths/weaknesses and interpersonal compatibility of the four blood types A, B, O, AB (for fun reference only).',
    '📖 View "Blood Type Personality Compatibility User Guide"',
    'Blood-type personality typing is fun content, not scientific statistics: Type A tends to be precise and meticulous, Type B free-spirited, Type O decisive and outgoing, Type AB a mix of contradictory traits; interpersonal compatibility is rated by empirical rules like same-type attraction, A complements O, B tolerates AB, with no epidemiological evidence, for entertainment only.',
    'Type A',
    'Type B',
    'Type O',
    'Type AB',
    'Friendly reminder',
    '📊 Blood Type Distribution & Compatibility Quick Lookup',
    'Type A (China)',
    'Type B (China)',
    'Type O (China)',
    'Type AB (China)',
    'The blood-type personality theory is popular in East Asia as a fun cultural phenomenon with no rigorous scientific consensus; view it rationally and treat it as entertainment.',
    '📚 Deep Dive: Blood Type Personality Compatibility',
    'Fun compatibility: pick your and your partner blood type to see a compatibility index and interpretation (A/B/O/AB four-way combos).',
    'Social icebreaker: use as a light topic to spark discussions of personality differences, with no serious judgment.',
    'Creative reference: quickly grab blood-type personality tropes for novels / character design.',
    'Method (fun compatibility)',
    'The tool uses a built-in compatibility table for A/B/O/AB pairings to output a compatibility index and "getting-along advice" text; it is pop-culture blood-type lore, not a scientific assessment.',
    'Pick A (earnest, meticulous) x O (easygoing, optimistic): shows "complementary type, O helps A relax, A helps O catch details" advice and a higher compatibility index (A/O are often tagged complementary among the 4 types); pick AB x AB: shows the interpretation "both changeable, need space for each other". Results are fixed mappings, for entertainment only.',
    'Is the compatibility index accurate?',
    'No. Blood-type compatibility is a pop-culture meme with no empirical basis; this tool is for entertainment and icebreaking only; for romance / collaboration rely on real interaction.',
    'How does it differ from analysis-4?',
    'analysis-4 looks at a single blood type personality label, while this tool looks at the compatibility of two people blood type combinations, shifting the dimension from individual to pairing.',
    'About "Blood Type Personality Analysis"',
    'Blood Type Personality Analysis is an online tool in the entertainment category, providing personality traits, strengths/weaknesses, romance style, career tendency and interpersonal compatibility for the four blood types A, B, O, AB.',
    'Full-dimension interpretation for the four blood types',
    'Strengths/weaknesses shown as tags',
    'Romance and career tendency analysis',
    'Blood type compatibility quick lookup',
    'Fun social-topic icebreaker',
    'Learn different personality traits',
    'Team-building interaction',
    'Fun reading in spare moments',
])
apply_tool('blood-type-personality', '血型性格分析', 'Blood Type Personality Analysis', G7, ind=IND)

# ---------------- breakout ----------------
G8 = build('breakout', '打砖块', [
    '🎮 Breakout',
    'Classic Breakout brick-breaking game: clear all bricks to win!',
    '📖 View "Breakout Game User Guide"',
    'Level',
    'Move paddle',
    'Launch / pause',
    'Mouse controls paddle position',
    'Breakout is a classic arcade ball game: bounce the ball with a paddle to smash the bricks above and score.',
    'How to play',
    'Move the bottom paddle to bounce the ball',
    'Ball smashes bricks for points',
    'Clear all bricks to advance to the next level',
    'Ball drops to the bottom, lose a life',
    'Out of three lives, game over',
    'Ball speed rises each level, difficulty up',
    'Multi-level challenge',
    'Brick color scoring',
    'Keyboard / mouse / touch',
    'Speed-increment mechanism',
    'Pause / resume',
    'Dark theme support',
    '📚 Deep Dive: Breakout Game',
    'Casual challenge: move the bottom paddle to bounce the ball and smash all bricks above to clear the level.',
    'Hand-eye coordination: use paddle angle to control the ball path and avoid dropping it.',
    'Strategy demo: prioritize edge bricks to create multi-bounce paths and clear the screen faster.',
    'Method (rules)',
    'Move the paddle left/right to catch the ball; the ball vanishes and bounces on hitting a brick; a missed ball (dropping to the bottom) costs a life; clear all bricks to win. Score = bricks smashed x per-brick value; consecutive catches without missing keep the ball-speed rhythm.',
    'A row of 10 bricks at 10 points each: clearing all gives 100 points; a mid-game miss costs 1 life (3 total) but you can continue with the remaining lives. Ball speed rises with level, so the paddle must predict the landing point earlier - a classic "reflection angle = incidence angle" geometry: catching left of center sends the ball up-right.',
    'How to make the ball path more controllable?',
    'Catch with the paddle "edge" rather than center to change the exit angle; catch off-center to send the ball up high, catch center to keep it safe.',
    'What if the ball gets faster and faster?',
    'This is the difficulty-increase design; keep the ball near the bottom centerline and move the paddle ahead to catch it, which is steadier than chasing the ball.',
    'About "Breakout"',
    'Breakout is an online tool in the entertainment category. Pure front-end, no install, playable offline.',
])
apply_tool('breakout', '打砖块', 'Breakout', G8, ind=IND)

# ---------------- chess-fen-viewer ----------------
G9 = build('chess-fen-viewer', '国际象棋 FEN 查看器', [
    '♟️ Chess FEN Viewer',
    'This tool is a pure front-end online tool; data is processed locally in your browser and not uploaded to any server, computed per relevant standards and specs, for reference only. Tool name: Chess FEN Viewer - a free fun game tool, online Chess FEN Viewer, free to use.',
    '📖 View "Chess FEN Viewer User Guide"',
    'Initial',
    'Checkmate',
    'Endgame',
    'FEN string: ',
    'Enter a FEN string to view the board',
    '📚 Deep Dive: Chess FEN Viewer',
    'Score reading: paste a FEN string, the front end renders the initial position, quickly grasping the situation.',
    'Game review: load each FEN from a game one by one and replay step by step.',
    'Position sharing: generate / copy a FEN and send it to a chess friend; restore the board without a screenshot.',
    'Method (FEN structure)',
    'FEN has 6 segments: 1) piece placement (a8 to h1, digits for consecutive empty squares) 2) side to move (w/b) 3) castling rights (KQkq) 4) en passant target square (or -) 5) halfmove clock 6) fullmove number. The tool parses and renders the board.',
    'Initial position FEN: `rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1` -> rendered as the opening, White to move, both sides may castle, no en passant; if the trailing castling segment is `-` that side has lost castling rights, e.g. `w - - 0 1` means White cannot castle.',
    'What are the six FEN segments?',
    'position / side to move / castling rights / en passant square / halfmove clock (50-move rule) / fullmove number; a missing segment causes parse failure.',
    'How to read en passant?',
    'Segment 4 shows the en passant target square (e.g. e3); a "-" means no such right currently.',
    'About "Chess FEN Viewer"',
    'Chess FEN Viewer. An entertainment game tool, pure front-end, no install, playable offline.',
])
apply_tool('chess-fen-viewer', '国际象棋 FEN 查看器', 'Chess FEN Viewer', G9, ind=IND)

# ---------------- click-speed ----------------
G10 = build('click-speed', '点击速度测试', [
    '⚡ Click Speed Test',
    'This tool is a pure front-end online tool; data is processed locally in your browser and not uploaded to any server, computed per relevant standards and specs, for reference only. Tool name: Click Speed Test - a free fun game tool, online Click Speed Test, free to use.',
    '📖 View "Click Speed Test (CPS) User Guide"',
    '10 seconds',
    'Click inside the area as many times as possible',
    '📚 Deep Dive: Click Speed Test (CPS)',
    'Hand-speed challenge: click as fast as possible within the time limit to find your CPS ceiling.',
    'Device comparison: test with mouse / trackpad / touchscreen to compare input-latency differences.',
    'Fun ranking: record your best CPS and race friends for fastest hands.',
    'Method (CPS calculation)',
    'Click continuously within a set duration (e.g. 10 s); CPS = total clicks / duration (clicks/sec); rate as slow / average / good by thresholds. Pure front-end local timing.',
    '85 clicks in 10 s -> CPS = 85/10 = 8.5/sec, rated "good"; only 40 clicks gives 4.0, average. Human limit is about 14+ CPS (needs an auto-clicker / extreme speed); ordinary players commonly hit 6-10.',
    'What CPS counts as fast?',
    '>=8 is good, >=12 is strong; above 14 is mostly auto-clickers or extreme speed; for normal fun 6-10 is fine.',
    'Is the difference between phone and mouse large?',
    'Continuous touchscreen taps are limited by system debounce and usually lower than mouse; mechanical keys and trackpads also differ slightly.',
    'About "Click Speed Test"',
    'Click Speed Test. An entertainment game tool, pure front-end, no install, playable offline.',
])
apply_tool('click-speed', '点击速度测试', 'Click Speed Test', G10, ind=IND)

print('gen_fun_b1 done')
