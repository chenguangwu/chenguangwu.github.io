# -*- coding: utf-8 -*-
"""fun 行业正文英文化 batch4（第 31~40 工具）。位置对齐法：从 work json 读取原始 zh，
与本文件英文列表按序配对。长度一致 + 无空译文 + apply_tool 零 CJK/零中文标点校验。"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_biz_apply import apply_tool

IND = 'fun'
WORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'work', 'fun')

def build(slug, en_list):
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

# ---------------- memory-game ----------------
G1 = build('memory-game', [
    '🎮 Memory Card Match',
    "You're amazing!",
    "📖 View 'Memory Card Match Guide'",
    'Game',
    'Leaderboard',
    'Easy 4×3',
    'Medium 4×4',
    'Hard 6×4',
    'Expert 6×6',
    '🐾 Animals',
    '🍎 Fruits',
    '🔢 Numbers',
    '🔤 Letters',
    '😀 Emoji',
    'Match',
    '🔀 Shuffle',
    'Easy (4×3)',
    'Medium (4×4)',
    'Hard (6×4)',
    'Expert (6×6)',
    'Tap a card to flip it and memorize its symbol',
    'Flip two identical cards to make a match',
    'Match all cards to win',
    'Finish with the fewest moves and in the shortest time',
    'Focus on positions, not symbols',
    'Start from a corner and work toward the center',
    'Prioritize matching when you spot a duplicate',
    '🗂️ Themes',
    'Animals',
    ': cute animal emoji',
    'Fruits',
    ': fresh fruit emoji',
    'Numbers',
    ': digits 1–9, good for number memory training',
    'Letters',
    ': letters A–Z, good for alphabet memory training',
    'Emoji',
    ': a rich set of emoji',
    '📚 Deep Dive: Memory Card Match',
    'Memory training: flip cards to find pairs and train visual memory.',
    'Progressive levels: more pairs as you advance.',
    'Casual relaxation: runs offline in the browser.',
    'How it works (matching rules)',
    "The board starts face-down; flip two cards each turn—matching pairs are removed, non-matching pairs flip back. Clear all pairs to pass. Same origin as emoji-memory (this version uses generic icons).",
    'Clear 8 pairs (16 cells) to win; the fewest flips and shortest time are recorded. More mistakes mean more moves. Use position coding to reduce re-flips and speed up.',
    'How is it different from emoji-memory?',
    'Same rules, only the artwork differs (generic icons here, Emoji there)—pick either.',
    'How do I remember the cards?',
    "When you flip the first card, number its position in your mind; after a mismatch, remember those two and match them next time.",
    'Congratulations!',
    "About 'Memory Card Match'",
    'Memory card matching game. A casual game tool built as a pure frontend—no install needed, playable offline.',
])
apply_tool('memory-game', '记忆翻牌游戏', 'Memory Card Match', G1, ind=IND)

# ---------------- minesweeper ----------------
G2 = build('minesweeper', [
    '🎮 Minesweeper',
    'A classic Minesweeper game with three difficulty levels. Reveal all safe cells to win.',
    "📖 View 'Classic Minesweeper Guide'",
    'Easy 9x9',
    'Medium 16x16',
    'Hard 16x30',
    'Left click',
    'Reveal',
    'Right click',
    'Flag',
    'Long press',
    'Move flag',
    'Rules and Tips',
    'Minesweeper is a classic single-player puzzle game. The goal is to reveal all non-mine cells as quickly as possible while avoiding mines.',
    'Basic rules',
    'Left-click a cell to reveal it',
    'A number shows how many mines are among the 8 surrounding cells',
    'Right-click (or long-press) to flag a suspected mine',
    'Reveal all safe cells to win',
    'Advanced tips',
    'The first click is always safe (safe-start protection)',
    'Start from a corner or edge for easier deduction',
    'When the flags around a number match it, you can safely reveal its adjacent unflagged cells',
    'The 1-2-1 and 1-2-2-1 patterns are common safe-deduction patterns',
    '📚 Deep Dive: Classic Minesweeper',
    'Logical deduction: use number clues to infer and flag mine positions.',
    'Three levels: Beginner 9×9/10 mines, Intermediate 16×16/40 mines, Expert 30×16/99 mines.',
    'Casual challenge: reveal all non-mine cells to win.',
    'How it works (mine-count rules)',
    "Each number = the mines among its 8 neighbors; after flagging, reveal all safe cells to win. The first click is usually protected. A zero (empty) cell auto-expands its neighbors in a chain.",
    "Beginner 9×9 has 10 mines; opening a corner showing '1' means exactly one mine nearby—deduce from that and flagged mines. Revealing all 71 safe cells (81−10) wins. Intermediate has 40 mines and Expert has 99, ramping up sharply.",
    'Is the first click always safe?',
    'Most implementations protect the first click (it and its neighbors are mine-free) for a better experience; rules depend on the specific version.',
    'How can I improve my win rate?',
    'Open corners/edges to trigger chain expansion, then make certain deductions from numbers, and only flag by probability where it is ambiguous.',
    "About 'Minesweeper'",
    'Classic Minesweeper with Easy, Medium, and Hard difficulties. Left-click to reveal, right-click to flag, first-click protection, pure frontend playable. A casual game tool—no install, playable offline.',
])
apply_tool('minesweeper', '扫雷游戏', 'Minesweeper', G2, ind=IND)

# ---------------- number-guess ----------------
G3 = build('number-guess', [
    '🔢 Number Guessing (1-100)',
    'This is a pure-frontend online tool. Data is processed locally in your browser and never uploaded to a server. Calculations follow relevant domain standards and are for reference only. Tool name: Number Guessing — an online tool in the entertainment & games category.',
    'Number Guessing',
    '/ Number Guessing',
    "📖 View 'Number Guessing (1-100) Guide'",
    "Click 'Start' to begin the game",
    'Submit guess',
    '📚 Deep Dive: Number Guessing (1-100)',
    'Logic game: a random number 1–100, with higher/lower hints to guess it step by step.',
    'Algorithm tutorial: demonstrates binary search with a worst case of ≤7 steps.',
    'Score tracking: counts guesses and records your best.',
    'How it works (binary strategy)',
    'Guess the midpoint of the range to halve it each time; worst-case steps = ⌈log2(100)⌉ = 7. Track your count and best score.',
    'Answer 42: guess 50 (too high) → 25 (too low) → 37 (too high) → 43 (too low) → 40 (too high) → 42 (hit), 6 steps. Rational binary search stays ≤7; blind guessing averages ~50 steps.',
    'Why at most 7 steps?',
    '2^7=128>100, so halving 7 times distinguishes 100 numbers—the information-theoretic lower bound.',
    'How is it different from caishuzi-1-100fanwei?',
    'Same family: both do 1–100 binary guessing. caishuzi emphasizes range-hint text, while this tool focuses on guess-count tracking.',
    "About 'Number Guessing'",
    'Number Guessing is an online tool in the entertainment & games category. A casual game tool—pure frontend, no install, playable offline.',
])
apply_tool('number-guess', '猜数字（1-100）', 'Number Guessing (1-100)', G3, ind=IND)

# ---------------- othello ----------------
G4 = build('othello', [
    '🎮 Othello (Reversi)',
    'Othello / Reversi — place a piece to flip the opponent pieces you sandwich; most pieces at the end wins',
    "📖 View 'Othello / Reversi Guide'",
    'vs Computer',
    'Two Players',
    'Easy',
    'Medium',
    '⚫ Black’s Turn',
    'Hints: On',
    'Move Log',
    'Rules:',
    'Black moves first. After placing, flip all opponent pieces sandwiched in any of the 8 directions to your color. You must flip at least one opponent piece to place. When no legal move exists, the turn passes automatically; when neither side can move, the game ends and the side with more pieces wins.',
    'About Othello',
    'Othello (Reversi) is a classic two-player strategy board game that originated in 19th-century Britain and later flourished in Japan and the United States.',
    '8×8 standard board rendered on Canvas',
    'Two-player / AI play',
    'AI greedy strategy + positional-weight strategy',
    'Legal moves highlighted',
    'Undo move',
    'Move replay',
    'Touch support on mobile',
    'Casual fun to pass the time',
    'Train strategic thinking',
    'Learn Othello tactics',
    'Play two-player with friends',
    '📚 Deep Dive: Othello / Reversi',
    'Two-player: take turns on an 8×8 board, flipping sandwiched opponent pieces.',
    'Strategy demo: understand the game of legal moves must flip, grabbing corners wins.',
    'Casual play: the side with more pieces at the end wins.',
    'How it works (flipping rules)',
    'A move must sandwich at least one opponent piece in some direction (with all cells in between your own); after placing, flip all sandwiched opponent pieces. If no move is possible, you pass; when neither side can move, the game ends and the side with more pieces wins.',
    'Black plays (3,3) and sandwiches white (3,4) (right side is its own) → that white flips to black, black +2, white −1; on a 64-cell board, if black 34 / white 30 at the end, black wins. Corners (the four corners) are the safest, edges next; grabbing corners early greatly reduces flip risk.',
    'How do I win?',
    'Grab the four corners and force your opponent into few legal moves; corners are stable and never flip—the core strategy.',
    'Can there be a tie?',
    '64 is even, so the end usually splits; a perfectly even split is extremely rare.',
    "About 'Othello'",
    'Othello (Reversi) online game with two-player and AI modes, runs purely in the frontend, free to use. A casual game tool—no install, playable offline.',
])
apply_tool('othello', '黑白棋', 'Othello (Reversi)', G4, ind=IND)

# ---------------- pattern-memory ----------------
G5 = build('pattern-memory', [
    '🔲 Pattern Memory',
    'This is a pure-frontend online tool. Data is processed locally in your browser and never uploaded to a server. Calculations follow relevant domain standards and are for reference only. Tool name: Pattern Memory — an online tool in the entertainment & games category.',
    "📖 View 'Pattern Position Memory Guide'",
    'Remember the positions of the highlighted cells',
    '📚 Deep Dive: Pattern Position Memory',
    'Visual memory: briefly flash several lit cells in a grid and ask you to reproduce their positions.',
    'Increasing difficulty: more lit cells as levels progress.',
    'Brain training: records the level you reach.',
    'How it works (reproduce rules)',
    'Briefly highlight several cells in an N×N grid, then ask you to click to restore those positions after they vanish; the number of lit cells grows with the level, and one mistake ends the round and is recorded.',
    'A 4×4 grid flashes 3 lit cells → restore those 3 to pass; later levels flash up to 8. Use the coordinate method (e.g., row 2, column 3) to encode positions more accurately than rote memorization.',
    'How is it different from shape/emoji memory?',
    'The rules belong to position memory; this tool uses abstract',
    ' icons, while emoji/shape use concrete icons—both train spatial position memory.',
    'How do I remember more cells?',
    'Assign each cell a row/column coordinate and group them—this holds more than memorizing cell by cell.',
    "About 'Pattern Memory'",
    'Pattern Memory is an online tool in the entertainment & games category. A casual game tool—pure frontend, no install, playable offline.',
])
apply_tool('pattern-memory', '图案记忆', 'Pattern Memory', G5, ind=IND)

# ---------------- pong ----------------
G6 = build('pong', [
    '⚽ Pong Battle',
    'Classic Pong game with two-player and AI modes; first to 11 points wins',
    "📖 View 'Pong Guide'",
    '🤖 vs AI',
    '🤯 Two Players',
    'Player',
    'Computer',
    'Round 1',
    'Ball speed: 1.0x',
    'Control left paddle',
    'Control right paddle',
    'Space',
    'Pause/Resume',
    'Pong is one of the earliest video games, now recreated with pure frontend technology.',
    '🎯 Basic Rules',
    'Each side controls a paddle to hit the ball toward the opponent',
    'The ball bounces off top/bottom edges; if it exits the left/right edge, the opponent scores',
    'Hitting the ball at different paddle positions changes the bounce angle',
    'The first side to 11 points wins',
    '🌐 Two-Player Controls',
    'Left player:',
    'Move up /',
    'Move down',
    'Right player:',
    'Pause/resume game',
    '🤖 AI Mode',
    'The computer auto-controls the right paddle',
    'The AI has reaction delay and movement error',
    'The faster the ball, the more the AI tends to miss',
    '🚀 Increasing Ball Speed',
    'The ball speeds up slightly after each hit',
    'The longer the rally, the tenser the pace',
    'Ball speed shows in the info bar',
    '📱 Mobile Support',
    'Swipe up/down on the left half of the canvas to control the left paddle',
    'Swipe up/down on the right half to control the right paddle',
    '📚 Deep Dive: Pong',
    'Two-player: left/right paddles on the same screen, rally back and forth.',
    'AI mode: challenge the computer solo, with adjustable difficulty.',
    'Casual competition: first to the target score (default 11) wins.',
    'How it works (win/loss rules)',
    'Both sides use paddles to catch the rallying ball; a miss gives the opponent a point. First to the target score (default 11, adjustable) wins. Ball speed creeps up with rallies, and AI difficulty is adjustable.',
    'Player reaches 11, opponent 8 → player wins; but if you miss several in a row and the opponent scores 3 straight, you could be overtaken. Controlling paddle angle (edge hits change the exit angle) is key to defense and counterattack.',
    'Is the target score fixed at 11?',
    'Default 11, adjustable; official table tennis also uses 11 points (win by 2).',
    'How do I beat the AI?',
    'Use the paddle edge to change the ball path and make the AI miss; when the AI is weak, just rally to wear it down.',
    "About 'Pong Battle'",
    'Classic Pong battle with two-player and AI modes. Pure-frontend Canvas rendering, no install, play instantly. First to 11 wins, ball speed rises with rallies. A casual game tool—no install, playable offline.',
])
apply_tool('pong', '乒乓对战', 'Pong Battle', G6, ind=IND)

# ---------------- raffle-picker ----------------
G7 = build('raffle-picker', [
    '🎁 Event Random Draw',
    'This is a pure-frontend online tool. Data is processed locally in your browser and never uploaded to a server. Calculations follow relevant domain standards and are for reference only. Tool name: Event Random Draw — an online tool in the entertainment & games category.',
    'Event Random Draw',
    '/ Event Random Draw',
    "📖 View 'Event Random Draw Guide'",
    '⚠️ This tool assists random draws / number generation for annual parties, classrooms, and team-building events. The process is open and reproducible, results are random, and it involves no gambling, prizes, or money transactions. Do not use it for betting.',
    'Participant list (one per line):',
    'Zhang San\nLi Si\nWang Wu\nZhao Liu\nQian Qi\nSun Ba\nZhou Jiu\nWu Shi',
    'Number to draw:',
    "Click 'Start' to begin the draw",
    'Start Draw',
    '📚 Deep Dive: Event Random Draw (party/classroom/team-building)',
    'Event random draw: import a list and randomly pick winners, with an open rolling animation.',
    'Weighted draw: give important slots higher weight to raise their selection probability.',
    'Deduplicated draw: avoid picking the same person twice for fair allocation.',
    'How it works (draw rules)',
    'Import names one per line and set how many to draw; supports weights (duplicate name or set a weight) and deduplication (without replacement). Frontend randomness with an open rolling animation boosts credibility.',
    'From a 50-person list draw 3 winners: fairly and randomly pick 3 different people; if someone weight is 3, their selection probability is about weight 3 / total weight sum, higher than a normal 1. Deduplication ensures no repeat selection.',
    'Is it fair random?',
    'Frontend pseudo-random; a single draw is openly verifiable. Weights only adjust probability by set ratio—not cheating.',
    'How is it different from random-picker?',
    'Raffle leans toward list + weight + rolling-animation formal draws; random-picker is a lightweight option-level draw.',
    "About 'Event Random Draw'",
    'Event Random Draw is an online tool in the entertainment & games category. A casual game tool—pure frontend, no install, playable offline.',
])
apply_tool('raffle-picker', '活动随机抽取器', 'Event Random Draw', G7, ind=IND)

# ---------------- random-name-gen ----------------
G8 = build('random-name-gen', [
    '🎲 Random Name Generator',
    'Great for naming ideas, test data, or novel characters: pick gender and name length to batch-generate random Chinese names, with one-click copy of all.',
    '/ Random Name Generator',
    "📖 View 'Random Chinese Name Generator Guide'",
    'Mostly male',
    'Mostly female',
    'Name length',
    'Two-character',
    'Three-character',
    '📚 Deep Dive: Random Chinese Name Generator',
    'Naming reference: batch-name novel/game characters and quickly get a batch of readable Chinese name candidates.',
    'Test data: when developing or demoing, you need lots of fake names to fill forms and run through flows.',
    'Fun generation: limit gender and length, one-click copy multiple names for draws or grouping.',
    'How it works (generation rules)',
    'Choose gender (male/female) and name length (2/3 chars); the tool randomly combines a local surname pool (e.g., Zhao, Qian, Sun, Li) with a common given-name pool. Batch mode outputs N at once with one-click copy; all data is generated locally in the browser, never uploaded.',
    "Generate 10 'male, 2-char' names: e.g., Zhang Wei, Li Na, Wang Fang, Liu Yang, Chen Jing, Zhao Lei, Sun Qian, Zhou Qiang, Wu Min, Zheng Hao; switch to 3 chars and you get 'Zhang Zixuan, Li Zixuan' etc. Pure random does not guarantee meaning; common shared characters are normal.",
    'Will it generate obscure or weird names?',
    'By default it draws from common surname and given-name pools with good readability; but random combinations do not guarantee auspicious meaning—consult elsewhere for formal naming.',
    'Can I specify a surname or length?',
    'It supports gender and 2/3-char length; to fix a specific surname you would adjust manually or pick a favored result and tweak it.',
    'Surnames drawn from the top 100 most common in the Hundred Family Surnames',
    'Given-name characters are categorized by gender (male/female/neutral) and avoid repeated characters',
    'Generated results are for entertainment and reference only, not naming advice',
    'For formal naming, consider birth date and cultural meaning',
])
apply_tool('random-name-gen', '随机姓名生成器', 'Random Name Generator', G8, ind=IND)

# ---------------- random-picker ----------------
G9 = build('random-picker', [
    '🎲 Random Picker',
    'This is a pure-frontend online tool. Data is processed locally in your browser and never uploaded to a server. Calculations follow relevant domain standards and are for reference only. Tool name: Random Picker — an online tool in the entertainment & games category.',
    "📖 View 'Random Option Picker Guide'",
    'Option list (one per line):',
    'Hotpot\nBBQ\nPizza\nBurger\nSushi\nNoodles\nSalad\nSkip',
    'No repeat',
    "Click 'Start' to randomly pick one",
    '📚 Deep Dive: Random Option Picker',
    'Daily decisions: randomly pick one option from a list, solving where to eat / who speaks.',
    'Multiple draws: pick several at once, optionally without replacement.',
    'Lightweight random: instant frontend draw, repeatable.',
    'How it works (draw rules)',
    'Enter several items in the option list and randomly draw 1 or more; check without replacement so drawn items will not reappear until all are drawn.',
    'Options [Hotpot, Stir-fry, Japanese, Takeout] draw 1 → e.g., Japanese; draw 3 without replacement → 3 different items (1 left). Each option has equal probability 1/N.',
    'How is it different from raffle-picker?',
    'This tool is a lightweight option-level draw; raffle supports name files, weights, and rolling animation, suited to formal events.',
    'What happens when without-replacement runs out?',
    'After all options are drawn it shows empty; reset to draw again.',
    "About 'Random Picker'",
    'Random Picker is an online tool in the entertainment & games category. A casual game tool—pure frontend, no install, playable offline.',
])
apply_tool('random-picker', '随机选择器', 'Random Picker', G9, ind=IND)

# ---------------- reaction-tester ----------------
G10 = build('reaction-tester', [
    '⚡ Reaction Test',
    'This is a pure-frontend online tool. Data is processed locally in your browser and never uploaded to a server. Calculations follow relevant domain standards and are for reference only. Tool name: Reaction Test — an online tool in the entertainment & games category.',
    "📖 View 'Reaction Speed Test Guide'",
    'Best:',
    'Average:',
    "Click 'Start' or here",
    'Click immediately once it turns green',
    '📚 Deep Dive: Reaction Speed Test',
    'Self-test: click as fast as you can once the target appears, measuring visuomotor reaction time.',
    'Hand-eye coordination: test repeatedly to see stability.',
    'Fun challenge: record average and best scores.',
    'How it works (timing rules)',
    'After a random delay the target appears; on click it records that reaction time (ms); multiple tests compute the average and best. Pure-frontend local timing.',
    '5 reactions 250/230/280/240/260ms → average 252ms, best 230ms; adult visuomotor reaction is ~200–250ms, below 200ms is excellent. Touchscreens add ~20–50ms due to debounce.',
    'What counts as fast?',
    '≤200ms excellent, 200–250ms normal, >300ms slow (affected by device latency).',
    'Is the phone vs computer difference large?',
    'Touchscreen taps have system debounce, usually 20–50ms slower than a mouse; compare on the same device.',
    "About 'Reaction Test'",
    'Reaction Test is an online tool in the entertainment & games category. A casual game tool—pure frontend, no install, playable offline.',
])
apply_tool('reaction-tester', '反应测试', 'Reaction Test', G10, ind=IND)

print('gen_fun_b4 done')
