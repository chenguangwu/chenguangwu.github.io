#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fun (64) 分类英文态数据源根治：同步三端 + 清孤儿键。

三处数据源（与 science/sports 同坑，§6「英文态数据源三处」）：
  ① i18n/tools/fun-body.json   -> build `_prerender_tool_body` 预渲染 h2 + 首个 <p>
  ② i18n/tools/fun.json en-US  -> industry JSON 的 ed 最高优先级源
  ③ i18n/tools/_en_override.json -> 运行时 en（h2/h1）与 ed

用法：
  python3 scripts/fix_fun_body_i18n.py --dry-run
  python3 scripts/fix_fun_body_i18n.py --apply
"""
import argparse
import glob
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools', 'fun')
OV = os.path.join(ROOT, 'i18n', 'tools', '_en_override.json')
BODY = os.path.join(ROOT, 'i18n', 'tools', 'fun-body.json')
GIS = os.path.join(ROOT, 'i18n', 'tools', 'fun.json')

# NAME = 英文名（h2 / h1 / 导航 / 英文态标题），INTRO = 真实英文描述（intro / ed）。
# 依据 fun 工具中文名与描述撰写，避免 "free online tool" 类套话与 slug 代号残留。
NAME = {
    '1a2b-guess': '1A2B Number Guessing Game (Bulls & Cows)',
    '2048-game': '2048 Game',
    'anagram-game': 'Anagram Game',
    'analysis-4': 'Blood Type Personality Analyzer',
    'analysis-tester-rhythm': 'Typing Rhythm Analyzer',
    'bbq-portion': 'BBQ Portion Estimator',
    'bingo-generator': 'Random Bingo Card Generator',
    'blink-counter': 'Blink Counter',
    'blood-type-personality': 'Blood Type Personality',
    'breakout': 'Breakout',
    'caishuzi-1-100fanwei': 'Number Guessing Game (1-100)',
    'chess-fen-viewer': 'Chess FEN Viewer',
    'click-speed': 'Click Speed Test',
    'coin-flip': 'Coin Flip',
    'coin-toss-streak': 'Coin Toss Streak',
    'color-guess': 'Color Guess',
    'color-memory': 'Color Memory (Simon)',
    'convert-speed-stride': 'Stride & Speed Converter',
    'cps-test': 'CPS Test',
    'daily-riddle': 'Daily Riddle Challenge',
    'emoji-memory': 'Emoji Memory Game',
    'fingerprint-types': 'Fingerprint Pattern Types',
    'generator-2': 'Sudoku Generator & Solver',
    'generator-3': 'Maze Generator (Auto-solve)',
    'generator-laugh': 'Laugh Sound Generator (Web Audio)',
    'gomoku': 'Gomoku (Five in a Row)',
    'gomoku-ai': 'Gomoku AI',
    'hangman': 'Hangman Word Game',
    'hotpot-portion': 'Hot Pot Portion Estimator',
    'keyboard-heatmap': 'Keyboard Heatmap',
    'laugh-generator': 'Laugh Sound Generator',
    'maze-generator': 'Maze Generator',
    'meditation-timer': 'Meditation Timer',
    'memory-game': 'Memory Match Game',
    'minesweeper': 'Minesweeper',
    'number-guess': 'Number Guessing Game (1-100)',
    'othello': 'Othello / Reversi',
    'pattern-memory': 'Pattern Memory',
    'pong': 'Pong',
    'raffle-picker': 'Event Raffle Picker',
    'random-name-gen': 'Random Name Generator',
    'random-picker': 'Random Picker',
    'reaction-tester': 'Reaction Time Test',
    'riddle-generator': 'Riddle Generator',
    'rock-paper-scissors': 'Rock Paper Scissors',
    'sequence-memory': 'Sequence Memory',
    'sequence-puzzle': 'Sequence Puzzle',
    'shape-memory': 'Shape Memory',
    'sliding-puzzle': 'Sliding Puzzle',
    'snake-game': 'Snake Game',
    'solitaire': 'Solitaire (Klondike)',
    'space-shooter': 'Space Shooter',
    'stats-3': 'Palm Size vs Height Correlation',
    'stats-blink': 'Blink Counter (Auto Timer)',
    'step-stride': 'Stride & Speed Converter',
    'sudoku-generator': 'Sudoku Generator',
    'tetris': 'Tetris',
    'tic-tac-toe': 'Tic Tac Toe',
    'tongue-twister': 'Tongue Twister',
    'typing-rhythm': 'Typing Rhythm Test',
    'wedding-banquet': 'Wedding Banquet Calculator',
    'whack-a-mole': 'Whack-a-Mole',
    'word-scramble': 'Word Scramble',
    'zodiac-match': 'Zodiac Compatibility',
}

INTRO = {
    '1a2b-guess': 'Classic Bulls & Cows guessing game with 4- and 5-digit difficulty levels, xAyB feedback, candidate-number reasoning help and a best-score record.',
    '2048-game': 'Merge numbered tiles on a 4x4 grid by swiping: combine equal numbers to build up to 2048. Keyboard and touch both supported, fully playable offline.',
    'anagram-game': 'Given a set of letters, find every English word of three letters or more that can be formed, sorted by length or alphabetically — for word games and brain training.',
    'analysis-4': 'Built-in personality descriptions for blood types A, B, O and AB: pick a type to see its trait tags. Entertainment reference only, not a scientific assessment.',
    'analysis-tester-rhythm': 'Records the interval between consecutive keystrokes and scores your typing rhythm on beat stability and evenness — useful as rhythm feedback during typing practice.',
    'bbq-portion': 'Estimate how much meat, seafood, vegetables and charcoal you need per guest for a barbecue, so you neither run short nor overbuy.',
    'bingo-generator': 'Generate printable random number cards for classroom roll call, event grouping and party games. Everything is produced locally and downloadable.',
    'blink-counter': 'Pick a duration, tap the button each time you blink, and see your blinking rate — around 15 to 20 blinks per minute is typical for a healthy adult.',
    'blood-type-personality': 'Explore the traits, strengths, weaknesses and interpersonal compatibility of blood types A, B, O and AB. Provided for entertainment only.',
    'breakout': 'Classic Breakout: move the paddle with mouse or keyboard to bounce the ball and clear every brick above. Runs entirely in your browser.',
    'caishuzi-1-100fanwei': 'The tool picks a number from 1 to 100 and you guess it one try at a time, receiving higher/lower hints until you land it. Attempts and best score are tracked.',
    'chess-fen-viewer': 'Paste a FEN string and the position is parsed and drawn in the browser — side to move, castling rights, en passant target and move counters included.',
    'click-speed': 'Click as fast as you can within the time limit; the tool shows total clicks and live clicks-per-second (CPS) to test your hand speed and reaction limits.',
    'coin-flip': 'Tap to get heads or tails instantly for two-way decisions, game rulings and random draws. Runs locally with no data uploaded.',
    'coin-toss-streak': 'Simulates repeated coin tosses and tracks heads/tails streaks, showing streak counts and their distribution. A casual game that works offline.',
    'color-guess': 'A random swatch appears and you name the color or its HEX code, with instant scoring — trains color recognition for design and art work.',
    'color-memory': 'Watch and repeat a gradually growing color sequence to challenge short-term memory and reaction speed. Levels ramp up and it works fully offline.',
    'convert-speed-stride': 'Estimate walking or running speed from cadence and step length, or work backwards from a target speed to the cadence you need — for pacing and gait analysis.',
    'cps-test': 'Click as fast as possible within the set time; the tool counts clicks and grades you as slow, average or good against CPS thresholds so you can compare hand speed.',
    'daily-riddle': 'One shared riddle per day worldwide, with three difficulty levels, tiered hints, combo scoring and an answer calendar. The puzzle bank keeps growing.',
    'emoji-memory': 'Match pairs of Emoji across increasing levels to train visual memory and concentration. Runs entirely in the browser and offline.',
    'fingerprint-types': 'Human fingerprints fall into three basic patterns — whorl, loop and arch. Switch between them to see each pattern\'s features and diagram.',
    'generator-2': 'Generate Sudoku puzzles at several difficulties complete with reference solutions, or paste an existing puzzle to solve it — for practice and leisure.',
    'generator-3': 'Generates a random maze and solves it with BFS and A*, with an adjustable grid size. Created and solved locally in the browser.',
    'generator-laugh': 'Synthesizes a variety of laughs in real time with the Web Audio API, with randomized parameter tweaks and downloadable output.',
    'gomoku': 'Play Gomoku on a standard 15x15 board in two-player or AI mode; the engine evaluates open fours, open threes and other shapes heuristically.',
    'gomoku-ai': 'Play against a heuristic Gomoku AI on a 15x15 board. The engine scores open fours, open threes and other patterns to choose its moves.',
    'hangman': 'Guess the hidden word letter by letter with a limited number of misses and a tracked win/loss record — good for English vocabulary practice and leisure.',
    'hotpot-portion': 'Estimate how much meat, seafood, vegetables and dipping sauce to buy per person for a hot pot meal, so the table is neither short nor wasteful.',
    'keyboard-heatmap': 'Type in the box below and see a live heatmap of your key distribution. The data stays in your browser and nothing is uploaded.',
    'laugh-generator': 'Synthesizes various laughs in real time with the native Web Audio API — no audio files needed, everything is generated locally.',
    'maze-generator': 'Generates a maze of the size you choose and lets you walk it with the keyboard, with a built-in auto-solve path hint. Useful for puzzles or algorithm demos.',
    'meditation-timer': 'Set a meditation length with optional interval bells and a closing chime; session counts are kept locally so you can track your practice.',
    'memory-game': 'Flip two cards at a time to find matching pairs; clear the whole board to win. Trains memory and plays offline.',
    'minesweeper': 'Classic Minesweeper in three difficulties: use the number clues to deduce and flag every mine, then uncover all safe cells to win. Fully offline.',
    'number-guess': 'A number from 1 to 100 is chosen at random; you guess and get higher/lower hints, with the number of attempts and your best score tracked.',
    'othello': 'Place a disc to flip the opponent\'s discs caught between yours; whoever holds more discs when the board fills wins.',
    'pattern-memory': 'A grid pattern flashes briefly and you rebuild it, with difficulty ramping up to test visual memory. Level progress is recorded.',
    'pong': 'Classic Pong with two-player and AI modes; first to 11 points wins. Pure front-end with no install, playable offline.',
    'raffle-picker': 'Import or type in a name list and draw winners at random, with weighting and no-repeat options and a publicly reproducible process — for annual parties, classrooms and team events.',
    'random-name-gen': 'Generate random names in bulk for placeholders, characters, teams and test data, with style and count options. Everything is produced locally.',
    'random-picker': 'Pick one item at random from your options, with multiple draws and a no-repeat mode — for deciding where to eat or who speaks first.',
    'reaction-tester': 'Click the target as soon as it appears to measure your reaction time, with average and best scores tracked — a self-test for hand-eye coordination.',
    'riddle-generator': 'Draws riddles at random from a puzzle bank or by keyword, with answers you can reveal — for party interaction and language fun.',
    'rock-paper-scissors': 'Play rock-paper-scissors against the computer with a built-in scoreboard and win-streak record. Casual and fully offline.',
    'sequence-memory': 'A sequence is played or shown and you reproduce it exactly, with adjustable length and speed. Trains sequential and working memory and records your best length.',
    'sequence-puzzle': 'Given a number or shape sequence, infer the next item — covering arithmetic, geometric and pattern problems, with explanations you can study.',
    'shape-memory': 'Shapes flash at certain positions and you restore them in order or in place, with rising difficulty to train visual-spatial memory.',
    'sliding-puzzle': 'Classic number sliding puzzle: move the scrambled tiles until they run in order, in either number or picture mode. Good for logic training.',
    'snake-game': 'Classic Snake: steer with the arrow keys to eat and grow while avoiding collisions, with a high-score record. No network connection needed.',
    'solitaire': 'Classic Klondike Solitaire — move every card by suit from Ace to King onto the foundation piles.',
    'space-shooter': 'Vertical space shooter: fly, shoot and wipe out wave after wave of alien enemies while collecting power-ups to beat your high score.',
    'stats-3': 'Enter palm length and height samples to compute the correlation coefficient and judge how strong the relationship is. A light-hearted statistics demo.',
    'stats-blink': 'Counts blinks per unit of time with automatic timing, for eye-care reminders, focus observation and self-checking your screen habits.',
    'step-stride': 'Estimate walking speed from cadence and step length, or derive the cadence and step length needed for a target speed — for walking pace and gait analysis.',
    'sudoku-generator': 'Creates printable Sudoku puzzles with answers, letting you choose difficulty and the number of givens. Good for logic training and leisure; the board can be copied freely.',
    'tetris': 'Classic line-clearing puzzle: move, rotate and drop tetrominoes to fill and clear rows for points. Keyboard and touch supported, with speed rising by level.',
    'tic-tac-toe': 'Play against the computer or a second player, with automatic win and draw detection. Pure front-end, no network needed.',
    'tongue-twister': 'Shows tongue twisters at random with a read-aloud timer, spanning different sound difficulties — for pronunciation practice and voice warm-ups.',
    'typing-rhythm': 'Type the sample text character by character; the tool records the interval between keystrokes and scores the stability of your typing rhythm.',
    'wedding-banquet': 'Estimate tables, seats and per-table dish quantities from your guest count, so both the banquet seating plan and the catering order come out right.',
    'whack-a-mole': 'Classic Whack-a-Mole: click the moles as they pop up within the time limit to score. Trains reaction and hand-eye coordination, with a high-score record.',
    'word-scramble': 'English words are scrambled and you restore them within limited hints — builds vocabulary and spelling, with score and hint usage tracked.',
    'zodiac-match': 'Pick your sign and theirs to see a compatibility score and reading, computed from the four-element sign affinity algorithm.',
}

DEFAULT_NOTE = [
    '本工具纯前端运行，数据不会上传到服务器',
    '建议在主流浏览器（Chrome/Safari/Firefox/Edge）中使用',
    '计算结果仅供参考，请以实际应用场景为准',
]

# 中文 title / intro 缺口：这 6 个工具在 fun.json 的 zh-CN 为空，
# 导致构建出的 <title> / og:title 退化为英文 slug（如 "Bbq Portion"）。
# 仅填空缺，已有中文的一律不覆盖，避免误伤线上已验证内容。
ZH = {
    'bbq-portion': (
        '烧烤食材分量计算器',
        '户外烧烤备货最容易买多或买少。输入人数与食量档次，得到肉类、海鲜、蔬菜与饮品的数量建议，'
        '兼顾荤素搭配，纯前端本地计算。',
    ),
    'gomoku-ai': (
        '五子棋人机对战',
        '与 AI 在 15×15 标准棋盘上对弈五子棋，AI 按活四、活三等棋型做启发式评估选点，'
        '纯前端本地推理、可离线游玩。',
    ),
    'hotpot-portion': (
        '火锅食材分量计算器',
        '火锅聚餐备菜最怕剩或不够。输入人数、口味偏好与食量，得到肉类、丸滑、蔬菜、主食与蘸料的采购量建议，'
        '纯前端本地计算。',
    ),
    'meditation-timer': (
        '冥想计时器',
        '设置总时长与分段数，自动生成分段冥想计划并附 4-7-8 呼吸法节奏参考，'
        '纯前端本地计时，不上传任何数据。',
    ),
    'random-name-gen': (
        '随机姓名生成器',
        '批量生成随机姓名，可选风格与数量，用于占位示例、角色起名、分组抽签等场景，'
        '全部在浏览器本地生成。',
    ),
    'wedding-banquet': (
        '婚宴桌数估算器',
        '输入宾客人数与每桌人数，估算桌数与备用桌，并按常见荤素配比折算菜品采购量，'
        '便于婚宴筹备，纯前端本地计算。',
    ),
}


def load(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--apply', action='store_true')
    a = ap.parse_args()
    if not a.dry_run and not a.apply:
        ap.error('需指定 --dry-run 或 --apply')

    slugs = sorted(
        os.path.basename(f)[:-5]
        for f in glob.glob(os.path.join(TOOLS, '*.html'))
        if os.path.basename(f) != 'index.html'
    )
    missing_name = [s for s in slugs if s not in NAME]
    missing_intro = [s for s in slugs if s not in INTRO]
    if missing_name or missing_intro:
        print('!! NAME/INTRO 缺条目:', missing_name, missing_intro)
        return 1

    ov = load(OV)
    body = load(BODY)
    gis = load(GIS)

    chg_en = chg_ed = chg_body = added_body = added_gis = chg_zh = 0

    for slug in slugs:
        name = NAME[slug]
        intro = INTRO[slug]
        k = 'fun/' + slug

        e = ov.get(k)
        if not isinstance(e, dict):
            e = {'ind': 'fun'}
        if e.get('en') != name:
            chg_en += 1
        if e.get('ed') != intro:
            chg_ed += 1
        e['en'] = name
        e['ed'] = intro
        e.setdefault('ind', 'fun')
        ov[k] = e

        b = body.get(slug)
        if not isinstance(b, dict):
            b = {}
            added_body += 1
            print('  + fun-body.json 新增条目:', slug)
        if b.get('title') != name or b.get('h1') != name or b.get('intro') != intro:
            chg_body += 1
        b['title'] = name
        b['h1'] = name
        b['intro'] = intro
        en = b.get('en')
        if not isinstance(en, dict):
            en = {}
        en['title'] = name
        en['h1'] = name
        en['intro'] = intro
        b['en'] = en
        body[slug] = b

        g = gis.get(slug)
        if not isinstance(g, dict):
            g = {}
            added_gis += 1
            print('  + fun.json 新增条目:', slug)
        # 中文态缺口补齐：仅当 zh-CN.title 为空时补，已有中文不覆盖
        zh_t, zh_i = ZH.get(slug, ('', ''))
        zh = g.get('zh-CN')
        if not isinstance(zh, dict):
            zh = {}
        if not (zh.get('title') or '').strip() and zh_t:
            zh['title'] = zh_t
            chg_zh += 1
        if not (zh.get('intro') or '').strip() and zh_i:
            zh['intro'] = zh_i
        if zh_t and not (zh.get('h1') or '').strip():
            zh['h1'] = zh_t
        if not (zh.get('desc') or '').strip() and zh_t:
            zh['desc'] = zh_t
        g['zh-CN'] = zh

        eu = g.get('en-US')
        if not isinstance(eu, dict):
            eu = {}
        eu['title'] = name
        eu['h1'] = name
        eu['intro'] = intro
        g['en-US'] = eu
        if 'note' not in g:
            g['note'] = list(DEFAULT_NOTE)
        gis[slug] = g

    # ---- 孤儿键清理（三端统一）----
    # 判定口径：键名在全站无对应页面，或对应页面不在本行业目录（跨行业残留），一律删除。
    all_basenames = {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(ROOT, 'tools', '*', '*.html'))}
    fun_basenames = set(slugs)

    orphans = [k for k in list(body.keys())
               if k not in all_basenames or k not in fun_basenames]
    for k in orphans:
        del body[k]

    ov_orphans = [k for k in list(ov.keys())
                  if k.startswith('fun/') and k.split('/', 1)[1] not in fun_basenames]
    for k in ov_orphans:
        del ov[k]

    gis_orphans = [k for k in list(gis.keys()) if k not in fun_basenames]
    for k in gis_orphans:
        del gis[k]

    print('\n--- 汇总 ---')
    print('fun 工具页:', len(slugs))
    print('_en_override  en 更新:', chg_en, ' ed 更新:', chg_ed)
    print('fun-body 更新:', chg_body, ' 新增:', added_body)
    print('fun.json 更新 en-US:', len(slugs), ' 新增条目:', added_gis, ' 中文 title/intro 补齐:', chg_zh)
    print('fun-body 孤儿键删除:', len(orphans), orphans)
    print('_en_override 孤儿键删除:', len(ov_orphans))
    print('fun.json 孤儿键删除:', len(gis_orphans), gis_orphans)

    if a.dry_run:
        for s in slugs[:3]:
            print('\n预览 %s:\n  name = %r\n  intro= %r' % (s, NAME[s], INTRO[s]))
        return 0

    json.dump(ov, open(OV, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(body, open(BODY, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    json.dump(gis, open(GIS, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('\n已写入：_en_override.json(indent=1) / fun-body.json(indent=2) / fun.json(indent=2)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
