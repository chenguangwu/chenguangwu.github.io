#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'misc')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'misc')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
DISCL = "Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected."
EXTRA = {}
def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items)); sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en)); sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en)); sys.exit(1)
        mp[z] = en
    return mp
def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'misc', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('magic-square', build('magic-square', [
        "✨ Magic Square Generator",
        "Generates odd-order magic squares using the Siamese (continuous placement) method. In a magic square, every row, column and the two diagonals sum to the same value.",
        "Odd-order magic square: magic sum M = n(n² + 1) / 2; generation uses the Siamese method - place the first number in the middle of the top row, then move up-right for each subsequent number, wrapping around at the boundaries, and if the target cell is occupied move down one row; verify that every row, column and both diagonals sum to the magic sum.",
        "Order n (odd, 3 ~ 15)",
        "Generate magic square",
        "Copy magic square",
        "📐 Magic Square and the Siamese Method",
        "Magic square:",
        "An n×n matrix filled with numbers 1 to n² so that every row, column and the two diagonals have the same sum.",
        "Magic constant:",
        "M = n(n²+1)/2, i.e. the sum of each row / column / diagonal.",
        "Siamese method (odd order only):",
        "1. Place 1 in the middle of the top row;",
        "2. Move each subsequent number one cell up-right (row-1, col+1);",
        "3. If it goes past the top edge, move to the bottom row; if past the right edge, move to the leftmost column;",
        "4. If the target cell is already filled, go back one cell directly below and continue.",
        "Order",
        "Magic constant",
        "Number range",
        "📚 In-Depth: Magic Square Generator",
        "In math teaching, use odd-order magic squares to demonstrate the construction rule of the Siamese method, training induction and pattern recognition.",
        "In number theory and combinatorial games, magic squares serve as interesting puzzles for understanding constant constraints and permutation symmetry.",
        "In introductions to art and cryptography, the equal-sum property of rows, columns and diagonals is used to design patterns or verify structures.",
        "Example: Magic constant of a 5th-order square",
        "Magic constant M = n(n²+1)/2. For n=5, M = 5×(25+1)/2 = 65. In the generated square, every row, every column and both main diagonals sum to 65.",
        "Example: Verifying equal-sum property",
        "Take a 5th-order square from the Siamese method: the first-row sum = 65, the main diagonal (top-left to bottom-right) sum = 65, and the other rows/columns/anti-diagonal are the same. Derivation: the total of 1...n² = n²(n²+1)/2, divided evenly into n rows gives each row sum = n(n²+1)/2.",
        "Are the construction methods the same for odd-order and even-order magic squares?",
        "No. Odd order (n odd) can use the Siamese method: start from the top row center, move up-right, wrap at boundaries, move down one cell if occupied. Even order (singly/doubly even) needs different algorithms (e.g. Strachey method, diagonal method); this tool generally supports odd order most completely.",
        "Where does the magic constant come from?",
        "The sum of numbers 1...n² is n²(n²+1)/2, evenly distributed over n rows (or n columns), so each row should equal the total divided by n, i.e. n(n²+1)/2. This is the equal-sum baseline that any n-th order magic square must satisfy.",
        "About 'Magic Square Generator'",
        "The magic square generator is an online tool in the scientific research field. A scientific research tool that uses standard scientific formulas for accurate calculation.",
    ]))
    write('number-puzzle', build('number-puzzle', [
        "🎮 24 Game",
        "Use 4 numbers and +, -, ×, ÷, parentheses to form an expression that equals 24. Each number must be used exactly once.",
        "Best streak",
        "Click numbers and operators to form an expression",
        "New puzzle",
        "Show solution",
        "Click 'New puzzle' to start the game",
        "📐 Game Rules",
        "Goal:",
        "Use the 4 cards' numbers with + - × ÷ and parentheses to make 24.",
        "Rules:",
        "Each number must be used exactly once; A=1, J=11, Q=12, K=13 (can switch to a 1-10 mode).",
        "Tips:",
        "First think of factors of 24 (e.g. 3×8, 4×6, 2×12), then build the factors; use parentheses wisely to change the operation order.",
        "Not every combination has a solution; 'Show solution' gives a feasible expression (or a no-solution notice if unsolvable).",
        "📚 In-Depth: 24 Game",
        "In math enlightenment and mental-arithmetic training, use the four operations to combine 4 cards into 24, exercising expression construction and parentheses usage.",
        "In algorithm teaching, use the 24 game as an intro to exhaustive search / backtracking, demonstrating the search space of operators and parentheses.",
        "In party puzzle games, timed solving adds fun and can be extended to other target numbers (e.g. 1, 10).",
        "Example: [3,3,8,8] -> 24",
        "Classic solution: 8/(3-8/3). First 8/3≈2.6667, 3-2.6667=0.3333, 8/0.3333=24. Note you must use all 4 numbers exactly once, and only + - × ÷ and parentheses are allowed.",
        "Example: Unsolvable determination",
        "Not all 4 cards are solvable. The solver iterates all permutations of the 4 numbers, the 4³ combinations of 3 operators, and the 5 bracket structures (Catalan number C₃=5). After exhaustive search, if none equals 24, it is declared unsolvable and a notice is shown.",
        "How many combinations are there in the 24 game?",
        "Taking 4 cards (with repetition allowed) from 1-13 (including A=1...K=13), after de-duplication there are about 1820 combinations, most of which are solvable; a few like [1,1,1,1], [1,1,1,2] are unsolvable. The tool usually judges solvability directly rather than enumerating for the user.",
        "Which operations are allowed?",
        "Standard rules allow only addition, subtraction, multiplication, division and parentheses; each card must be used exactly once, with the result 24 (floating-point error usually relaxed to |result-24| < 1e-6). Fractional intermediate results (e.g. 8/3) are allowed, which is the key to solving [3,3,8,8].",
        "About '24 Game'",
        "The 24 game is an online tool in the scientific research field. A scientific research tool that uses standard scientific formulas for accurate calculation.",
    ]))

if __name__ == '__main__':
    main()
