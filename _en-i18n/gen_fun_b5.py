# -*- coding: utf-8 -*-
"""fun 行业正文英文化 batch5（第 41~50 工具）。位置对齐法。"""
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

# ---------------- riddle-generator ----------------
G1 = build('riddle-generator', [
    '✨ Riddle Generator',
    'Quickly generate word riddles / object riddles by type, with answer reveal support.',
    "📖 View 'Riddle Generator Guide'",
    'Riddles are drawn randomly from a bank and can be filtered by keyword: candidate count = number of riddles matching the keyword; when picking 1 at random each has probability 1 / candidates; clues and answers are stored in pairs, and the correct rate = correct answers / total asked x 100%; within a round, deduplication avoids repeats.',
    'Theme word (optional)',
    'Generate one',
    'Show answer',
    '📚 Deep Dive: Riddle Generator',
    'Party interaction: draw questions randomly from a bank and let everyone buzz in to liven the mood.',
    'Language fun: answers can be toggled, for classroom or family guessing.',
    'Quiz practice: generate related clues by keyword for lesson prep or events.',
    'How it works (question rules)',
    'Draw clues randomly from a built-in bank, with one-tap answer toggle; keep drawing without repeats (dedup by drawn set) until the bank loops. Pure-frontend, replayable.',
    "Draw #1: 'A hemp house, a red curtain, inside lives a white chubby one (a plant fruit)' → answer: peanut; draw #2: 'A knife, floating on water, has eyes but no brows (an animal)' → answer: fish. Draw 5 in a row with no repeats; answers always viewable.",
    'Are the answers always accurate?',
    'The bank holds preset standard answers; common riddles are accurate, and for the few with multiple solutions the primary answer is used.',
    'Can I add my own riddles?',
    'Currently it draws randomly; a custom bank needs a data-source extension and can be added later.',
])
apply_tool('riddle-generator', '谜语生成器', 'Riddle Generator', G1, ind=IND)

# ---------------- rock-paper-scissors ----------------
G2 = build('rock-paper-scissors', [
    '🎮 Rock Paper Scissors',
    'Play vs computer, with scoreboard and win streak',
    '/ Entertainment / Rock Paper Scissors',
    "📖 View 'Rock Paper Scissors Guide'",
    '🎮 Start Game',
    '📖 Game Rules',
    '📊 History Stats',
    'Win',
    '👤 You',
    '🤖 Computer',
    'Choose your move!',
    '🔄 Reset Score',
    '✊ Rock beats ✌️ Scissors',
    '✌️ Scissors beats 🖐️ Paper',
    '🖐️ Paper beats ✊ Rock',
    'Same move is a draw',
    'Consecutive wins show a streak record',
    'Keyboard shortcuts',
    'Press',
    'for Rock',
    'for Scissors',
    'for Paper',
    '📚 Deep Dive: Rock Paper Scissors',
    'Casual play: you and the computer throw, with scoreboard and streak.',
    'Decision mini-game: leave a toss-up to randomness.',
    'Algorithm demo: observe AI strategy (random / pattern-reading).',
    'How it works (win/loss rules)',
    'Rock beats scissors, scissors beats paper, paper beats rock; a tie replays. With a purely random AI, long-term you are about 1/3 win, 1/3 draw, 1/3 loss (even odds). Includes scoreboard and streak.',
    "Player wins 5 in a row → streak +5; if the AI uses a 'mimic your last move' strategy, you must vary on purpose to break its read. Rock/scissors/paper cycle beats each other with no absolute best move.",
    'Can you reliably beat the AI?',
    'Against a purely random AI it is even long-term; against a pattern-reading AI you can randomize to break its prediction, but there is no guaranteed win.',
    'Can there be a draw?',
    'Same move is a draw; it counts as a draw and does not add to the streak.',
    "About 'Rock Paper Scissors'",
    'Rock Paper Scissors is an online tool in the entertainment & games category. A casual game tool—pure frontend, no install, playable offline.',
])
apply_tool('rock-paper-scissors', '石头剪刀布', 'Rock Paper Scissors', G2, ind=IND)

# ---------------- sequence-memory ----------------
G3 = build('sequence-memory', [
    '🔢 Sequence Memory',
    'This is a pure-frontend online tool. Data is processed locally in your browser and never uploaded to a server. Calculations follow relevant domain standards and are for reference only. Tool name: Sequence Memory — an online tool in the entertainment & games category.',
    "📖 View 'Sequence Memory Game Guide'",
    'Remember the number sequence and input it in order',
    '📚 Deep Dive: Sequence Memory Game',
    'Order memory: show/play a sequence in turn and ask you to reproduce it exactly.',
    'Adjustable length and speed: grow and speed up step by step to challenge working memory.',
    'Brain training: records the length you reach.',
    'How it works (reproduce rules)',
    'Present a number or shape sequence in order (set speed and length); after it vanishes, reproduce it in the original order; one mistake ends it and records the length reached.',
    "Sequence [red, green, blue, yellow] reproduced correctly → pass; length grows from 4 to 12, recording the longest. Same origin as color-memory, but this sequence may include digits/symbols, not just colors.",
    'How is it different from color-memory?',
    'Same sequence-memory rules; this tool sequence can be digits/symbols, while color-memory fixes a color sequence.',
    'How do I remember longer?',
    'Build a story / group the sequence—larger capacity than rote memorization.',
    "About 'Sequence Memory'",
    'Sequence Memory is an online tool in the entertainment & games category. A casual game tool—pure frontend, no install, playable offline.',
])
apply_tool('sequence-memory', '序列记忆', 'Sequence Memory', G3, ind=IND)

# ---------------- sequence-puzzle ----------------
G4 = build('sequence-puzzle', [
    '🔢 Sequence Puzzle',
    'This is a pure-frontend online tool. Data is processed locally in your browser and never uploaded to a server. Calculations follow relevant domain standards and are for reference only. Tool name: Sequence Puzzle — an online tool in the entertainment & games category.',
    "📖 View 'Number Sequence Puzzle Guide'",
    'Question #:',
    'Score:',
    'Observe the sequence pattern and find the value at "?"',
    '📚 Deep Dive: Number Sequence Puzzle',
    'Logic training: given a number/shape sequence, infer the next term.',
    'Pattern coverage: arithmetic, geometric, Fibonacci, primes, shape rotation, etc.',
    'With explanation: on a wrong answer you can view the pattern walkthrough to learn.',
    'How it works (reasoning rules)',
    'Look at adjacent-term relations: arithmetic (constant difference), geometric (constant ratio), Fibonacci (each = sum of previous two), squares/primes, etc.; for shape questions see rotation/count changes. With explanation.',
    "2,4,8,16,? → geometric, next 32; 1,4,9,16,? → squares, next 25; 1,1,2,3,5,? → Fibonacci, next 8. Once the pattern is identified the next term is unique.",
    'Only arithmetic and geometric?',
    'No. There are also primes, Fibonacci, factorial, shape rotation/symmetry, etc.; the bank covers many types.',
    'Is there an explanation if I get it wrong?',
    'Yes. After submitting it shows the correct next term and explains the pattern used, for learning.',
    "About 'Sequence Puzzle'",
    'Sequence Puzzle is an online tool in the entertainment & games category. A casual game tool—pure frontend, no install, playable offline.',
])
apply_tool('sequence-puzzle', '序列谜题', 'Sequence Puzzle', G4, ind=IND)

# ---------------- shape-memory ----------------
G5 = build('shape-memory', [
    '🔷 Shape Memory',
    'This is a pure-frontend online tool. Data is processed locally in your browser and never uploaded to a server. Calculations follow relevant domain standards and are for reference only. Tool name: Shape Memory — an online tool in the entertainment & games category.',
    "📖 View 'Shape Position Memory Guide'",
    'Remember the shape sequence and click in order',
    '📚 Deep Dive: Shape Position Memory Game',
    'Spatial memory: briefly flash several shape positions then ask you to restore them.',
    'Increasing difficulty: more shapes as levels progress.',
    'Brain training: records level progress.',
    'How it works (restore rules)',
    'Briefly highlight several shapes in a grid, then after they vanish click to restore their positions; count grows with the level, one miss ends the round.',
    "Flash 3 shape positions → restore to pass; later levels flash up to 8. Use the coordinate method (row/column) to encode positions more accurately than rote memory, same origin as pattern-memory.",
    'How is it different from pattern-memory?',
    'Both train spatial position memory; this tool uses shapes, pattern-memory uses abstract',
    ' icons—pick either.',
    'How do I remember more?',
    'Assign each cell a row/column coordinate and group them—larger capacity.',
    "About 'Shape Memory'",
    'Shape Memory is an online tool in the entertainment & games category. A casual game tool—pure frontend, no install, playable offline.',
])
apply_tool('shape-memory', '形状记忆', 'Shape Memory', G5, ind=IND)

# ---------------- sliding-puzzle ----------------
G6 = build('sliding-puzzle', [
    '🧩 Sliding Puzzle',
    'Classic number sliding puzzle (Klondike / 15-puzzle): slide tiles to restore order. Supports number and image modes.',
    "📖 View 'Sliding Puzzle (15-Puzzle) Guide'",
    'Numbers',
    'Upload image',
    'Use default image',
    'Shuffle moves',
    'Auto solve',
    'Click or use arrow keys to move a tile · arrange the numbers in order to win',
    'Game intro and how to play',
    'The Sliding Puzzle, also called the number Klondike or 15-puzzle, is a classic brain game. You slide tiles to rearrange the scrambled numbers from small to large.',
    'How to play',
    'Click a tile adjacent to the empty space to slide it',
    'Use keyboard arrow keys to control',
    'Arrange all numbers in order with the empty space at bottom-right',
    'Fewer steps and less time mean a better score',
    '3x3 - Easy (8 tiles)',
    '4x4 - Classic (15 tiles)',
    '5x5 - Hard (24 tiles)',
    'Image mode',
    'After switching to image mode you can upload a custom image or use the default. The image is cut into tiles and you slide them to restore the full picture.',
    'Tips',
    'Restore the first row first, then go row by row downward',
    'Use special techniques for the last two rows',
    'Avoid moving already-placed tiles back and forth',
    'Start from a corner and work toward the center',
    '📚 Deep Dive: Sliding Puzzle (15-Puzzle)',
    'Mind training: slide tiles to restore the 1~n order.',
    'Two modes: number or image puzzle.',
    'Casual challenge: compete on fewest steps.',
    'How it works (solve rules)',
    "Click a tile next to the empty space to slide into it, gradually ordering the numbers (top-left to bottom-right, last cell empty). A legal shuffle is always solvable; use the layer strategy 'restore first row and column first'.",
    'After shuffling a 3×3 (8-puzzle), the minimum steps depend on shuffle depth (commonly 20~30); a 4×4 (15-puzzle) gets much harder. Fix the first row/column first then shrink inward, avoiding back-and-forth moves.',
    'Is it always solvable?',
    'A layout generated by random legal slides is always solvable; a direct random permutation is about half unsolvable, but this tool guarantees solvability.',
    'How do I solve faster?',
    'Layer by layer: first row/column, then the next layer, then corners—more efficient than blind sliding.',
])
apply_tool('sliding-puzzle', '滑动拼图', 'Sliding Puzzle', G6, ind=IND)

# ---------------- snake-game ----------------
G7 = build('snake-game', [
    '🎮 Snake',
    'Arrow keys / WASD to steer, Space to pause',
    "📖 View 'Snake Guide'",
    'Game',
    'Leaderboard',
    '🐢 Easy',
    '🏃 Medium',
    '⚡ Hard',
    '🔥 Expert',
    'Length',
    '🏆 High Score',
    'Control the snake, eat food to grow',
    'Hitting a wall or its own body ends the game',
    'Each food gives 10 points',
    'The longer the snake, the more challenging',
    '🎯 Difficulty',
    'Easy',
    ': slow, for beginners',
    'Medium',
    ': normal speed',
    'Hard',
    ': fast, tests reaction',
    'Expert',
    ': very fast, for experts',
    'Keyboard',
    ': arrow keys or WASD',
    'Pause',
    ': Space or P key',
    'Mobile',
    ': virtual direction keys',
    '📚 Deep Dive: Snake',
    'Casual: arrow keys control the snake as it eats and grows.',
    'Reaction challenge: avoid hitting walls or yourself.',
    'High score: saved locally.',
    'How it works (growth rules)',
    'When the head eats food, length +1 and score +10; hitting a wall or its own body ends the game. Classic 20×20 grid, arrow-key controlled.',
    'One food = +1 length +10 points; at length 10 the score is 100; a wall hit ends instantly. Experts loop and keep turning room to avoid self-collision and chase high scores.',
    'How do I get a high score?',
    'Keep the snake compact in loops and reserve U-turn room; do not greedily rush straight into walls.',
    'Are there boundaries?',
    'Yes. A wall hit or self-bite is death; some versions have a wrap-around mode.',
    'Game Over',
    'Try again!',
    "About 'Snake'",
    'Snake is an online tool in the entertainment & games category. A casual game tool—pure frontend, no install, playable offline.',
])
apply_tool('snake-game', '贪吃蛇', 'Snake', G7, ind=IND)

# ---------------- solitaire ----------------
G8 = build('solitaire', [
    '🎮 Klondike Solitaire',
    'Classic Klondike Solitaire - move all cards by suit from A to K onto the foundations',
    "📖 View 'Klondike Solitaire Guide'",
    '🔄 New Game',
    '↺ Undo',
    '⚡ Auto Complete',
    '📚 Deep Dive: Klondike Solitaire',
    'Classic card casual',
    'Strategy and patience training',
    'Time killer',
    'Stack the 52 cards alternating red/black and decreasing in rank, moving A-to-K by suit onto the foundations; the stock and waste piles help scheduling, and all home means a win.',
    'Deal 7 columns of 28 cards and a stock of 24; first tidy movable red-6 to black-7, prioritize flipping empty columns for K; move A♠A♥A♣A♦ to foundations and collect 4 A-K sets to win. Pure frontend, no network.',
    'Can I undo?',
    'Depends on the build; the basic version can reset, the advanced adds single-step undo.',
    'Is it always solvable?',
    'A random deal is not always solvable; it is a probabilistic game—restart for a new layout.',
    'Game Rules',
    'Goal',
    'Move all 52 cards to the 4 foundations, ordered by suit from A to K.',
    'Basic Operations',
    'Click the stock',
    ': flip one card to the waste; once the stock is empty, click to recycle it',
    'Drag to move',
    ': drag a card to a legal spot. Tableau columns alternate red/black in descending order',
    'Double-click',
    ': auto-move the card to the foundation',
    'Mobile',
    ': tap to select a card, then tap the target to move',
    'Rules',
    'Tableau: alternate red/black, descending from K to A',
    'An empty column accepts only a K',
    'Foundation: same suit, ascending A to K',
    'The top waste card can move to the tableau or foundation',
    'Scoring',
    'To foundation: +10',
    'Flip a face-down card: +5',
    'Move back from foundation: -15',
    '🎉 Congratulations! You won!',
    'Time 0:00, 0 moves, score 0',
    '🔄 Play Again',
    "About 'Klondike Solitaire'",
    'Classic Klondike Solitaire, pure frontend, with drag-and-drop, timer, move counter and undo. A casual game tool—no install, playable offline.',
])
apply_tool('solitaire', '纸牌接龙', 'Klondike Solitaire', G8, ind=IND)

# ---------------- space-shooter ----------------
G9 = build('space-shooter', [
    '🎯 Space Shooter',
    'Pilot your ship to destroy enemies, grab power-ups, and chase the high score!',
    "📖 View 'Space Shooter (Casual) Guide'",
    'Power-ups',
    'Controls',
    ': on desktop use the left/right arrow keys to move, Space to fire, P to pause; on mobile use the on-screen buttons.',
    'About Space Shooter',
    'Space Shooter is a classic vertical shooter. Pilot your ship through the starfield and wipe out wave after wave of alien enemies!',
    'Three enemy types: normal, fast, tough',
    'Three power-ups: triple shot, shield, extra life',
    'Level-up system',
    'Explosion particle effects',
    'Dynamic starfield background',
    'Mobile touch support',
    'Game Rules',
    'Hit enemies for points',
    'Enemies reaching the bottom or colliding cost a life',
    'Level up every 500 points, rising difficulty',
    'Game over when all 3 lives are gone',
    'Collect power-ups to boost abilities',
    'A shield blocks one hit',
    '📚 Deep Dive: Space Shooter (Casual)',
    'Quick-session relaxation challenge',
    'Beat and refresh the high score',
    'Demonstrates collision detection and object pooling',
    'The ship moves left/right and fires; enemy craft appear in waves from the top; bullets hit them for points, while misses or collisions cost health, ending at zero health.',
    'Wave 1: 5 enemies at 10 each = 50; after a speed power-up fire rate doubles, wave 2: 8 enemies at 15 each = 120, total 170 and a new high. Scores are stored locally only.',
    'Are scores saved?',
    'The high score is stored in the browser locally—no network, no upload; clearing cache resets it.',
    'What if it lags?',
    'Lower quality / turn off effects or use another device; the game is pure-frontend Canvas, so performance depends on the browser and hardware.',
    "About 'Space Shooter'",
    'A space shooter mini-game—pilot a ship to destroy aliens, grab power-ups, and chase high scores. Pure-frontend Canvas, no download. A casual game tool—no install, playable offline.',
])
apply_tool('space-shooter', '太空射击', 'Space Shooter', G9, ind=IND)

# ---------------- stats-3 ----------------
G10 = build('stats-3', [
    '📊 Hand Size vs Height Correlation (Stats)',
    'Statistics',
    "📖 View 'Palm-length vs Height Correlation (Fun Stats) Guide'",
    'Enter paired palm-length and height data, compute Pearson r, R² and a simple linear regression, to gauge the linear correlation strength between palm length and height; data is processed only locally in the browser, never uploaded.',
    'r = Σ(xᵢ−x̄)(yᵢ−ȳ) / √(Σ(xᵢ−x̄)² · Σ(yᵢ−ȳ)²)  ·  Regression: height = a + b × palm length, b = Σ(xᵢ−x̄)(yᵢ−ȳ) / Σ(xᵢ−x̄)²',
    'Palm length (cm, paired with height, separated by comma or newline)',
    'Height (cm, paired with palm length, separated by comma or newline)',
    'Compute correlation',
    '📚 Deep Dive: Palm-length vs Height Correlation (Fun Stats)',
    'Statistics teaching demo',
    'Fun data observation',
    'Science popularization',
    'Correlation coefficient',
    'Meaning',
    'Enter several samples of palm length and height, compute Pearson r ∈ [-1,1]: |r|≥0.8 strong, 0.5~0.8 medium, 0.3~0.5 weak, <0.3 extremely weak; r>0 means a positive-correlation trend.',
    '5-person sample palm(cm)/height(cm): (17,163)(18,170)(19,176)(16,160)(20,180) → mean (18,169.8), Σdx·dy=53, Σdx²=10, Σdy²=284.8, r=53/√2848≈0.99 strong positive. A demo, not a medical conclusion.',
    'Does correlation imply causation?',
    'No. The coefficient only measures linear association strength; it does not mean palm length determines height, for reference only.',
    'How many samples for stability?',
    'Smaller samples are more accidental; 5–10 suffice to see a trend in teaching demos, but do not extrapolate the conclusion.',
    "About 'Hand Size vs Height Correlation (Stats)'",
    'Hand Size vs Height Correlation (Stats). A casual game tool—pure frontend, no install, playable offline.',
])
apply_tool('stats-3', '手掌大小与身高相关性（统计）', 'Hand Size vs Height Correlation (Stats)', G10, ind=IND)

print('gen_fun_b5 done')
