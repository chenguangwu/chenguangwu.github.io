#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'chess')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'chess')
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
    out = {'slug': slug, 'industry': 'chess', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # ---------------- gomoku-forbidden (21) ----------------
    write('gomoku-forbidden', build('gomoku-forbidden', [
        "📚 Gomoku Forbidden Move Check",
        "Judge the Gomoku forbidden moves for black (double-three, double-four, overline), with a detailed explanation of the forbidden move rules",
        "📖 Read the \"Gomoku Forbidden Move Check User Guide\"",
        "Based on the Chinese Gomoku competition rules, judge the forbidden moves for black (double-three, double-four, overline); after each move it automatically identifies open threes, closed fours and five-in-a-rows, assisting rule adjudication, game review and forbidden move tactics practice.",
        "📚 Judge",
        "→ Forms two open threes at once",
        "→ Six in a row = forbidden",
        "→ Seven in a row = forbidden",
        "→ White six in a row = win",
        "📚 Deep dive: Gomoku Forbidden Move Check",
        "Double-three forbidden move: one move that forms two open threes at once (each can be extended to a four) is a forbidden move.",
        "Double-four forbidden move: one move that forms two closed fours / open fours at once is a forbidden move.",
        "Overline forbidden move: black making six in a row or more (not exactly five) is a forbidden move and loses.",
        "A move that forms two open threes at once worked example",
        "Entering a position where a move forms an open three both horizontally and diagonally, the tool judges it a double-three forbidden move and marks the two open-three positions, and notes that black must not play there (white has no forbidden moves).",
        "Are forbidden moves limited to black?",
        "Yes. Black, moving first, has forbidden moves to balance the advantage; white has none, and an overline (6 or more) counts as a win for white.",
        "Does an overline count as a win for black?",
        "No. A black overline (six or more) is a forbidden move and loses; a white overline is a win.",
        "How is double-three determined?",
        "It requires two open threes (each can be extended to a four) formed at once after the move; if one of them is a sleeping three, it is not judged as a forbidden move.",
    ]))

    # ---------------- index (17) ----------------
    write('index', build('index', [
        "♟️ Board Game Tools",
        "Board games",
        "Board Game Tools",
        "Compute the territory of black and white from the surrounded points and prisoners on the board, supporting comparison of the stone counting and territory methods, helping quickly determine the balance of a Go game or review.",
        "Enter the current Elo ratings of both sides and the game result to estimate the rating change after this game, helping players judge how the result affects the ranking and the strength gap.",
        "The bridge scoring calculator computes the score from the contract, tricks, vulnerability and doubling status, helping players check scores and keep competition records.",
        "Gomoku Forbidden Move Check",
        "The Gomoku forbidden move checker judges forbidden moves for black such as double-three, double-four and overline, with a detailed explanation of the rules, assisting fair play and loss adjudication.",
        "The Chinese chess endgame helper provides one-move mates, two-move mates and solutions to classic \"jianghu\" endgames, assisting Chinese chess enthusiasts in studying mating patterns.",
        "About \"Board Game Tools\"",
        "The Board Game Tools collection gathers 5 free online tools covering the common calculation, conversion and lookup needs of board game scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you will find ready-to-use utilities here. Every tool runs entirely in the browser and never uploads data to the server, so your privacy is protected.",
        "The board game tools listed on this page include (a few representative tools):",
        "These tools help you finish common board game tasks quickly, with no need to memorize complex formulas or do manual conversions - just enter the inputs and get the result.",
        "Do the board game tools require a download or an account?",
        "No. Every tool on this page is a pure front-end online tool: open the page and use it right away, with no software to install, no account to register, and no data uploaded.",
        "Are the board game tool results accurate? Is the data safe?",
        "The tools compute locally in your browser based on public mathematical formulas and general industry standards, so results are available instantly. All computation happens locally on your device and no data is uploaded to the server, so your privacy is fully protected.",
    ]))

    # ---------------- xiangqi-endgame (20) ----------------
    write('xiangqi-endgame', build('xiangqi-endgame', [
        "📚 Chinese Chess Endgame Hints",
        "Common Chinese chess mating patterns, one-move mates, two-move mates and solutions to classic endgames",
        "📖 Read the \"Chinese Chess Endgame Hints User Guide\"",
        "Based on Chinese chess rules, it collects one-move mates, two-move mates and classic \"jianghu\" endgames; click to expand the solution steps and demonstrates common patterns such as the knight mate, the double cannon and the smothered palace, assisting mating-pattern study and endgame training.",
        "⚡ One-move mate",
        "🎯 Two-move mate",
        "📜 Classic endgames",
        "Double-chariot mate",
        "📚 Deep dive: Chinese Chess Endgame Hints",
        "One-move / two-move mate diagrams: given the position, present the shortest mating move and the follow-up check-evading steps.",
        "Classic jianghu endgames: study famous positions such as \"Seven Star Gathering\" and \"Lone Rider Travels a Thousand Miles\", appreciating precise move sequences.",
        "Common mating pattern demonstrations: the knight mate, double cannon, smothered palace, double-chariot, and the crouching horse are demonstrated one by one, 8 patterns in total.",
        "Knight mate (ma hou pao) steps worked example",
        "Entering a position, the tool shows the move sequence of the horse controlling the check and the cannon borrowing the horse's power, outputs steps such as \"horse from eight to seven — cannon from nine to four\" and judges it a one-move mate, noting to watch for the opponent interposing a piece to defuse the check.",
        "How is a one-move mate determined?",
        "Work backward from the checking move and confirm that no check evasion (interposition / avoidance / capture) works, which makes it a one-move mate.",
        "What are the characteristics of jianghu endgames?",
        "Few pieces, many traps and a high draw rate; they usually require precise moves, and one mistake loses or draws, so they suit training calculation.",
        "What are the common mating patterns?",
        "The knight mate, double cannon, smothered palace, double-chariot, crouching horse, corner horse, iron gate bolt and heaven-and-earth cannon, mostly formed by coordinated chariot, horse and cannon.",
    ]))


if __name__ == '__main__':
    main()
