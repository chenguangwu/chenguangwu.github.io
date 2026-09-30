# -*- coding: utf-8 -*-
"""fun 行业正文英文化 batch3（第 21~30 个工具）。位置对齐法：从 work json 读取原始 zh，与英文列表按序配对。"""
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

# ---------------- generator-3 ----------------
G = build('generator-3', '迷宫生成器（自动生成并求解）', [
    '🧩 Maze Generator (Auto-generate & Solve)',
    'Auto-generate & solve',
    '📖 View "Maze Generator User Guide"',
    'Maze generation commonly uses three algorithms, each with distinct traits:',
    'Recursive backtracking (DFS)',
    ': generates "trunk + dead ends", usually',
    'a unique solution',
    ', with a long path.',
    '(random weights): generates more forks and a more open layout, with non-unique solutions.',
    'Recursive division',
    ': generates a symmetric room-like structure.',
    'Auto-solving uses BFS or A* for the shortest path; the larger the grid, the more complex the path. Purely for fun, generated results are copyright-free.',
    '📚 Deep Dive: Maze Generator',
    'Puzzle fun: randomly generate a maze and walk it to the exit with the keyboard.',
    'Algorithm demo: observe randomized generation and BFS/A* solution paths.',
    'Difficulty tuning: change the grid size to control complexity.',
    'Method (generation and solving)',
    'Use a randomized algorithm (e.g. recursive backtracking) to generate a perfect maze (fully connected, no loops), with built-in BFS/A* shortest-path solving and highlighting; grid size is adjustable.',
    'A 15x15 maze, start (0,0) end (14,14), BFS shortest path ~28-40 steps (depending on random structure); A* with Manhattan-distance heuristic searches fewer nodes. Generation guarantees connectivity, so a solution always exists.',
    'Is a maze always solvable?',
    'Yes. A perfect maze is fully connected; between any two cells there is a unique path, so it is never a dead end.',
    'How to make it harder?',
    'Increase the size or reduce corridors; you can also add "multiple ends / time limit" mechanics for more challenge.',
    'About "Maze Generator (Auto-generate & Solve)"',
    'Maze Generator (Auto-generate & Solve). An entertainment game tool, pure front-end, no install, playable offline.',
])
apply_tool('generator-3', '迷宫生成器（自动生成并求解）', 'Maze Generator (Auto-generate & Solve)', G, ind=IND)

# ---------------- generator-laugh ----------------
G = build('generator-laugh', '笑声音效生成器（合成）', [
    '✨ Laugh Sound Effect Generator (Synthesis)',
    'Synthesis',
    '📖 View "Laugh Sound Synthesizer User Guide"',
    'The laugh sound is',
    'synthesized in real time inside the browser, without any third-party audio assets:',
    'A base-frequency oscillator (sawtooth / square) simulates the staccato of the vocal-cord "ha".',
    'ADSR envelope',
    'controls the attack/decay/release of each "ha", forming the rhythm.',
    'LFO vibrato',
    '+ formant filtering approximates the human vowel timbre.',
    'Random parameter fine-tuning produces varied "hahaha". The synthesized audio is free to download and use, with no copyright risk.',
    '📚 Deep Dive: Laugh Sound Synthesizer',
    'Asset creation: synthesize laughs like "hahaha" locally, avoiding the search for licensed audio.',
    'Parameter fine-tuning: adjust base frequency, vibrato and duration to generate different laugh styles.',
    'Offline-capable: pure Web Audio API real-time synthesis, downloadable.',
    'Method (synthesis principle)',
    'Use the browser-native Web Audio API for real-time synthesis: base-frequency oscillation + vibrato (LFO) + envelope (attack/sustain/release) assemble the laugh waveform; after tuning parameters, export a local wav, with no third-party audio assets.',
    'Synthesize "hahaha": base frequency 200Hz, vibrato +/-15Hz, duration 1.2s, sounding close to a light laugh; export as a local wav file. Fully front-end synthesis, no upload, no copyright risk.',
    'Need internet?',
    'No. The sound is synthesized locally in the browser in real time, usable offline.',
    'Can it be used commercially?',
    'Self-synthesized, no third-party assets or copyright risk, free for personal use; for specific commercial use, confirm per platform rules.',
    'About "Laugh Sound Effect Generator (Synthesis)"',
    'Laugh Sound Effect Generator (Synthesis). An entertainment game tool, pure front-end, no install, playable offline.',
])
apply_tool('generator-laugh', '笑声音效生成器（合成）', 'Laugh Sound Effect Generator (Synthesis)', G, ind=IND)

# ---------------- gomoku ----------------
G = build('gomoku', '五子棋', [
    '🎮 Gomoku',
    '15x15 standard board, supports two-player and AI mode',
    '📖 View "Gomoku (Two-player/AI) User Guide"',
    'Two-player',
    'Vs AI',
    'Black to move',
    'Moves: ',
    'Rules & instructions',
    'Black moves first; players alternately place stones on line intersections',
    'Whoever connects five stones horizontally, vertically or diagonally wins',
    'A full board with no winner is a draw',
    'Pattern evaluation',
    'AI mode uses a heuristic evaluation algorithm, recognizing open-four, four-threat, open-three, sleeping-three patterns and computing the best move.',
    'Open five 100000 pts',
    'Four-threat/open-four 10000 pts',
    'Open three 1000 pts',
    'Sleeping four 1000 pts',
    'Open two 100 pts',
    'Sleeping three 100 pts',
    'Operation tips',
    'Click a board intersection to place a stone',
    'The last move is marked with a red square',
    'Undo reverts the previous move',
    'In AI mode the AI automatically plays white',
    '📚 Deep Dive: Gomoku (Two-player/AI)',
    'Two-player: take turns placing stones on a 15x15 board; first to connect five wins.',
    'AI practice: challenge the heuristic AI solo to train offense and defense.',
    'Algorithm demo: understand open-four, open-three, four-threat pattern evaluation, suited to explaining game-tree search.',
    'Method (win/loss rules)',
    'A 15x15 board (225 intersections), black and white alternate; first to connect 5 stones in any direction wins; an open-four (four-in-a-row with both ends open) cannot be blocked by the opponent and is a guaranteed win. The simplified version has no forbidden moves, so first player (black) has a clear edge.',
    'Black opens at (7,7), white blocks (7,8); black continues (7,9)(7,10) to form the five-in-a-row (7,7)->(7,11) and wins. If white preemptively blocks at (7,6), black shifts to (8,7) to create an open-three in another direction. The first player should actively build double open-threes to force the opponent to split defense.',
    'Why do I keep losing to the first player?',
    'Without forbidden-move rules, black moves first and can seize the center, a big advantage; the second player should build open-threes early to contain and avoid getting four-threatened.',
    'Are there forbidden moves?',
    'In formal play black has forbidden moves (double-three/double-four/overline); this tool is a casual version with no enforced forbidden moves, where five-in-a-row is the sole win condition.',
])
apply_tool('gomoku', '五子棋', 'Gomoku', G, ind=IND)

# ---------------- gomoku-ai ----------------
G = build('gomoku-ai', '五子棋人机对战', [
    '🎮 Gomoku vs AI',
    'A simplified human-vs-AI Gomoku; the AI scores points by surrounding board momentum.',
    '/ Gomoku vs AI',
    '📖 View "Gomoku vs AI User Guide"',
    'The Gomoku AI picks a point by pattern scoring: open-four (winning) weight 10000, four-threat 1000, open-three 1000, sleeping-three 100, open-two 100, sleeping-two 10; a candidate score = own five-threat score x attack factor + opponent threat score x defense factor; on a 15x15 board it scores each empty point within 2 cells of existing stones and takes the max, optionally layered with minimax and alpha-beta pruning.',
    'New game',
    'Undo 1 move',
    '📚 Deep Dive: Gomoku vs AI',
    'Vs AI: take turns with the built-in AI; first to five wins, good for solo practice.',
    'Difficulty tuning: the AI evaluates by search depth / pattern weights; adjustable to strong/medium/weak.',
    'Algorithm demo: observe how the AI prioritizes blocking open-fours and grabbing open-threes, to understand heuristic play.',
    'Method (AI strategy)',
    'Rules same as',
    '; the AI heuristically evaluates the board: prioritize making five > blocking opponent open-four > making own open-four/open-three > blocking four-threat. Higher difficulty means deeper search and fewer missed defenses.',
    'The player makes an open-three at (3,3)(3,4)(3,5); the AI blocks (3,2) or (3,6) to prevent a four; if the player also has another open-three at (5,5)(6,6), the AI can only block one, and the player wins by completing five in the other direction. Creating "double open-threes" is the key to beating the AI.',
    'How strong is the AI?',
    'Heuristic plus shallow search, about amateur intermediate; skilled players can force its mistakes with double open-threes / four-threats.',
    'Can the first move be adjusted?',
    'Usually the player takes black and moves first; for a challenge, you can let the AI move first to raise difficulty.',
])
apply_tool('gomoku-ai', '五子棋人机对战', 'Gomoku vs AI', G, ind=IND)

# ---------------- hangman ----------------
G = build('hangman', '猜单词游戏', [
    '🔤 Word Guessing Game',
    'This tool is a pure front-end online tool; data is processed locally in your browser and not uploaded to any server, computed per relevant standards and specs, for reference only. Tool name: Word Guessing Game - an online tool in the entertainment category.',
    '📖 View "Word Guessing Game (Hangman) User Guide"',
    '📚 Deep Dive: Word Guessing Game (Hangman)',
    'English vocabulary: a hidden English word is shown at random; guess by letter step by step to train spelling and vocabulary.',
    'Casual challenge: limit wrong guesses, record win rate and fewest steps.',
    'Classroom activity: the teacher picks word-bank difficulty; students guess in turn.',
    'Method (guessing rules)',
    'Draw a word at random from the built-in bank, using underscores for unguessed letters; each guess is one letter, a hit reveals all its positions, a miss accumulates wrong guesses; reaching the limit (usually 6) loses, revealing all wins.',
    'Word "PYTHON" (6 letters): guess P -> hit shows P _ _ _ _ _; guess A -> miss (1/6); guessing Y/T/H/O/N in turn hits, clearing in 6 steps. If 6 different wrong letters are guessed midway, it is "hanged" and lost. Win rate and average steps are recorded.',
    'What language is the word bank?',
    'The built-in bank is mostly English words; for Chinese word guessing use other character tools.',
    'How many misses to lose?',
    'Classic is 6 (matching the 6 strokes of the figure); some versions are adjustable, as long as it is consistent within the rules.',
    'About "Word Guessing Game"',
    'Word Guessing Game is an online tool in the entertainment category. Pure front-end, no install, playable offline.',
])
apply_tool('hangman', '猜单词游戏', 'Word Guessing Game', G, ind=IND)

# ---------------- hotpot-portion ----------------
G = build('hotpot-portion', '火锅食材分量计算器', [
    '🧮 Hot Pot Ingredient Calculator',
    'When friends gather for hot pot, the hardest part is deciding how much to buy. Enter the number of people and taste preference to get per-person suggestions for meat, vegetables, soy products and staples.',
    '/ Hot Pot Ingredient Calculator',
    '📖 View "Hot Pot Party Shopping Calculator User Guide"',
    'Meat ~ people x 200 g; balls/slides ~ people x 100 g; vegetables & mushrooms ~ people x 150 g; staples ~ people x 80 g; dipping sauce ~ people x 30 g',
    'Hot pot is estimated per person: meat 200 g, balls/slides 100 g, vegetables & mushrooms 150 g, staples 80 g, dipping sauce 30 g; with more people the shared broth and platters allow an overall 10%-15% reduction, while meat lovers raise the meat factor; broth and drinks are calculated separately by people and taste.',
    'Taste preference',
    'Meat lover',
    'Balanced meat & veg',
    'Mostly vegetarian',
    'Appetite',
    'Small eater',
    'Big eater',
    '📚 Deep Dive: Hot Pot Party Shopping Calculator',
    'Party shopping: enter the number of people and broth / taste to estimate meat, vegetables, soy products and staples, avoiding over-buying waste or under-buying shortage.',
    'Meat-veg balance: balance a meal structure by per-person reference amount, accommodating different appetites.',
    'Drink budget: when alcohol is included, estimate total consumption per person for easy purchasing.',
    'Method (per-person reference)',
    'Per person: meat 400 g, vegetables 300 g, soy products 150 g, staples 100 g; with drinks 700 mL per person. Total = per-person amount x people; spiciness / taste can be fine-tuned by +/-10%-20%. For a twin / mandarin-duck pot, count the two broths separately.',
    '8 people, spicy pot, with drinks: meat = 8x400 = 3200 g (3.2 kg), vegetables = 8x300 = 2400 g (2.4 kg), soy products = 8x150 = 1200 g (1.2 kg), staples = 8x100 = 800 g, drinks = 8x700 = 5600 mL (5.6 L, about three 2 L bottles). Switching to clear + spicy twin pot raises meat by 1.2x.',
    'How to adjust for big eaters?',
    'Raise meat and staples by +20%-30%, or reserve one table portion (~10%) for extra guests.',
    'Why no skewer count?',
    'Hot pot is measured by weight (meat slices / vegetable plates), not by skewers; skewer counts only appear in BBQ tools.',
    'Per-person ingredients ~600 g, broth ~250 mL per person',
    'Meat-veg ratio by taste preference: meat lover 55/25, balanced 40/40, vegetarian 20/60',
    'Big eater x1.2, small eater x0.85',
    'The above are reference suggestions; adjust to your appetite and dish choices in practice',
])
apply_tool('hotpot-portion', '火锅食材分量计算器', 'Hot Pot Ingredient Calculator', G, ind=IND)

# ---------------- keyboard-heatmap ----------------
G = build('keyboard-heatmap', '键盘热力图', [
    '⌨️ Keyboard Heatmap',
    'Type in the input box below to record keystroke distribution in real time and generate a heatmap. Data is stored locally only, no upload of any information.',
    '📖 View "Keyboard Keystroke Heatmap User Guide"',
    'The keyboard heatmap colors by keystroke frequency: per-key count = cumulative presses of that key; total keystrokes = sum of all key counts; share = per-key count / total keystrokes x 100%; color depth maps to count linearly or logarithmically (depth = count / max count x 100%), used to analyze high-frequency keys for optimizing layout or assessing typing habits.',
    'Type here (click the input box to start)',
    'Load sample text',
    'Clear stats',
    'Total keystrokes',
    'Distinct keys',
    'Most used key',
    'Low',
    'High',
    'After you start typing, the key ranking appears here.',
    '📚 Deep Dive: Keyboard Keystroke Heatmap',
    'Input analysis: type in the box; count each key press in real time and generate a heatmap.',
    'Habit observation: see your common-key distribution and discover input preferences.',
    'Local privacy: data is stored only in the browser, no upload.',
    'Method (statistics and rendering)',
    'Type normally in the input box below; the tool accumulates each physical key press in real time and colors by frequency (hotter = darker) to generate the heatmap; data is local only, no upload of any information.',
    'Typing "the quick brown fox" (covers all letters) -> each of the 26 letter keys +1, space key +5; on the heatmap space and vowels (e/a/o) are hottest, rare letters (q/z/x/j) coldest. Clear and re-test with different text.',
    'Are keystrokes uploaded?',
    'No. Pure front-end local stats; closing the page clears them (unless manually exported).',
    'Can I export the heatmap?',
    'For now you can save a screenshot; structured export needs a later extension.',
    'About "Keyboard Heatmap"',
    'Keyboard Heatmap is an online tool in the entertainment category; it records your keystroke distribution in the input box in real time and renders a visual heatmap by color depth, with data stored only in your local browser.',
    'Real-time keystroke heat visualization',
    'Total keystrokes and high-frequency key stats',
    'Keystroke frequency leaderboard',
    'Fun typing-habit analysis',
    'Keyboard preference self-test',
    'Input-method and key-layout research',
])
apply_tool('keyboard-heatmap', '键盘热力图', 'Keyboard Heatmap', G, ind=IND)

# ---------------- laugh-generator ----------------
G = build('laugh-generator', '笑声音效生成器', [
    '✨ Laugh Sound Effect Generator',
    'Uses the browser-native Web Audio API to synthesize various laughs in real time, no audio files, all generated locally.',
    '📖 View "Laugh Synthesizer User Guide"',
    'Big laugh',
    'Sneaky giggle',
    'Light titter',
    'Hearty chuckle',
    'Evil smirk',
    'Crazy cackle',
    'Parameter tuning',
    'Pitch',
    'Speed',
    '▶ Preview',
    'Click the buttons above to synthesize different laughs. The first playback needs a page click to activate audio.',
    '🔊 How it works',
    'This tool uses',
    ', generating the fundamental tone via an Oscillator, combining a gain Envelope to mimic the "ha" syllable undulation, then triggering repeatedly by rhythm to form the laugh sequence.',
    'Different laugh types are achieved by adjusting pitch, rhythm interval, syllable count and waveform, all synthesized locally in real time in the browser, loading no external audio files.',
    'Note: some browsers require interaction (a click) with the page before audio can play. If you hear nothing, make sure the device is not muted and you have clicked the page.',
    '📚 Deep Dive: Laugh Synthesizer',
    'Asset creation: synthesize laughs like "hehe/haha" locally, avoiding licensed audio.',
    'Parameter preview: tune base frequency, duration and vibrato to preview different laugh styles live.',
    'Offline-capable: pure Web Audio API synthesis, no internet needed.',
    'Method (synthesis principle)',
    'Use the browser-native Web Audio API to synthesize laugh waveforms in real time (base-frequency oscillation + vibrato LFO + envelope), with tunable parameters to preview, no audio files, no copyright risk.',
    'Base frequency 180Hz, duration 1.0s synthesizes a "hehe" light chuckle; it shares the same origin as this repo generator-laugh (the latter leans toward "download wav"), while this tool leans toward "various laugh presets with live preview". Fully front-end synthesis.',
    'How does it differ from generator-laugh?',
    'Same underlying tech; this tool focuses on multiple laugh presets for preview, generator-laugh focuses on exporting wav files; choose per need.',
    'Need internet?',
    'No, the sound is synthesized locally in real time.',
    'About "Laugh Sound Effect Generator"',
    'Laugh Sound Effect Generator is an online tool in the generator category; it uses the browser-native Web Audio API to synthesize various laughs in real time, with adjustable pitch, speed and volume, and shows a live waveform.',
    '6 laugh types synthesized live',
    'Pitch / speed / volume adjustable',
    'Live waveform visualization',
    'Pure front-end, no audio files',
    'Instant fun sound playback',
    'Short-video / livestream sound effects',
    'Web Audio API learning demo',
    'Party interaction & pranks',
])
apply_tool('laugh-generator', '笑声音效生成器', 'Laugh Sound Effect Generator', G, ind=IND)

# ---------------- maze-generator ----------------
G = build('maze-generator', '迷宫生成器', [
    '🧩 Maze Generator',
    'Random maze generation, playable, auto-solved, multiple sizes',
    '/ Entertainment / Maze Generator',
    '📖 View "Maze Walk-through Game User Guide"',
    'Randomized depth-first (Recursive Backtracker): from the start, randomly pick an unvisited neighbor, break the wall, backtrack and continue until fully connected',
    'Prim algorithm (optional): randomly expand the lowest-cost neighbor from the connected set, generating a more evenly branched maze',
    'A maze is represented as "grid cells + walls", cell count = width x height; after generation, BFS/DFS finds the shortest path as an auto-solve hint.',
    '🎮 Play',
    '⚙️ Settings',
    '❓ Help',
    '🧩 New maze',
    '🔍 Auto-solve',
    '🔄 Reset position',
    '📥 Download image',
    'Use',
    'arrow keys or',
    'to move; green is the exit',
    'Maze width (cells)',
    'Maze height (cells)',
    'Cell size (pixels)',
    'Generation algorithm',
    'Depth-first search (DFS)',
    'Prim algorithm',
    'Show solution path',
    'Apply & generate',
    'The blue square is you, the green square is the exit',
    'Use arrow keys or WASD to move',
    'Walk from top-left to bottom-right to clear',
    'The "Auto-solve" button shows the solution path',
    'DFS depth-first',
    ': classic algorithm, generates long corridors and few branches',
    ': generates more branches and a more complex maze',
    '📚 Deep Dive: Maze Walk-through Game',
    'Puzzle fun: randomly generate a maze and move with the keyboard from start to exit.',
    'Difficulty tuning: change the grid size to control complexity.',
    'Solve hint: the built-in auto-solve path can be highlighted as reference.',
    'Method (generation and walk-through)',
    'A randomized algorithm generates a perfect maze (fully connected); the keyboard moves the character from start to exit; the built-in BFS solution hint can be toggled. Size is adjustable.',
    'A 20x20 maze, start top-left (0,0) exit bottom-right (19,19), BFS shortest path ~38-50 steps (varies with random structure); enabling hints highlights the solution. Generation guarantees connectivity and a solution (shares the same origin as generator-3, this tool leans toward "playable walk-through + hints").',
    'Is a maze always solvable?',
    'Yes. A perfect maze is fully connected; between any two cells there is a unique path, so it is never a dead end.',
    'How does it differ from generator-3?',
    'Same origin; generator-3 leans toward "algorithm solve demo", this tool leans toward "interactive walk-through + hints".',
    'About "Maze Generator"',
    'Maze Generator is an online tool in the entertainment category. Pure front-end, no install, playable offline.',
])
apply_tool('maze-generator', '迷宫生成器', 'Maze Generator', G, ind=IND)

# ---------------- meditation-timer ----------------
G = build('meditation-timer', '冥想计时器', [
    '🧘 Meditation Timer',
    'Meditation needs a quiet countdown. Set the total duration and segment interval to auto-generate a segment plan, with a 4-7-8 breathing rhythm reference.',
    '/ Meditation Timer',
    '📖 View "Meditation Timer User Guide"',
    'Segment count = total duration / segment duration; one 4-7-8 breathing round = inhale 4 s + hold 7 s + exhale 8 s = 19 s',
    'The meditation timer splits the total duration into segments and gives a cue at each segment end; the 4-7-8 breathing method uses inhale 4 s, hold 7 s, exhale 8 s per round (~19 s), and by lengthening the exhale it activates the parasympathetic nerve to aid relaxation; beginners can start from 4-4-6 to avoid discomfort from holding too long.',
    'Total meditation time (minutes)',
    'Interval reminder (minutes)',
    'Meditation style',
    'Breath awareness',
    'Body scan',
    'Mantra',
    'Free meditation',
    '📚 Deep Dive: Meditation Timer',
    'Mindfulness meditation: set the total duration, quiet',
    'countdown',
    'and focus on breathing.',
    'Breathing exercise: use the 4-7-8 rhythm (inhale 4 s, hold 7 s, exhale 8 s) to relax and aid sleep.',
    'Segment plan: split a long session into small segments, each cueing a posture switch or focus point.',
    'Method (segmentation and breathing)',
    'Set the total duration and segment interval; the tool auto-generates a segment plan and cues at each segment end; built-in 4-7-8 breathing: inhale 4 s -> hold 7 s -> exhale 8 s, 19 s per round. Data is local, no upload.',
    'Total 10 minutes, 2 minutes per segment: 5 segments, a light cue at each end to switch; 4-7-8 breathing done 4 rounds ~ 4x19 = 76 s. Beginners should start at 5 minutes with halved holds to avoid breath-holding discomfort.',
    'What is the 4-7-8 breathing method for?',
    'By lengthening exhale and hold it activates the parasympathetic, slowing the heart rate, often used for sleep and anxiety relief; those with heart/lung disease should follow medical advice and not force holding.',
    'Must I segment?',
    'No. A single continuous long session is fine; segmentation only helps you stay aware and avoid drifting too long.',
    'Interval reminders split the total evenly; return to breathing at each segment end',
    '4-7-8 breathing: inhale 4 s - hold 7 s - exhale 8 s',
    'Meditation is not medical; for severe anxiety / insomnia see a doctor',
    'Mute the phone, use vibration or soft cues',
])
apply_tool('meditation-timer', '冥想计时器', 'Meditation Timer', G, ind=IND)

print('gen_fun_b3 done')
