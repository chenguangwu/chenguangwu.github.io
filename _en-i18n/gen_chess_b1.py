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
    # ---------------- bridge-scoring (28) ----------------
    write('bridge-scoring', build('bridge-scoring', [
        "♟️ Bridge Scoring",
        "Compute the bridge score from the contract, tricks, vulnerability and doubling status",
        "Core formulas (by input variable): level+6",
        "📖 Read the \"Bridge Scoring User Guide\"",
        "♣ Clubs",
        "♦ Diamonds",
        "♥ Hearts",
        "♠ Spades",
        "NT No trump",
        "♟️ Scoring",
        "📚 Deep dive: Bridge Scoring",
        "Contract score calculation: compute the base score from the contract level and suit (♠/♥ 30 per trick, ♦/♣ 20 per trick, no trump 40 for the first trick then 30), then add the doubling.",
        "Bonus point accounting: bonuses (small slam made 6 / grand slam made 7), vulnerability bonuses, over-trick bonuses and the doubling/redoubling bonuses are each listed separately.",
        "Penalty for failing the contract: when the contract is not made, the penalty is computed from the doubling status and vulnerability, and failing while vulnerable is penalized more heavily.",
        "4♠ doubled, made with 1 overtrick (vulnerable) worked example",
        "Entering contract 4♠, doubled, 1 overtrick, vulnerable, the tool outputs a contract base score of 120, 240 after doubling, an over-trick bonus of 60, a vulnerability bonus of 500 and a doubling bonus of 50, totalling about 850 points, and shows the penalty rule if the contract fails.",
        "How are the high and low suit base scores computed?",
        "High suits ♠/♥ score 30 points per trick, low suits ♦/♣ score 20 per trick; no trump is 40 for the first trick then 30 per trick. After doubling the base score is doubled.",
        "How much does vulnerability affect scoring?",
        "When vulnerable, the bonuses for making a game or slam are higher and the penalty for failing is heavier; when not vulnerable the penalty is lighter. Vulnerability is determined by the dealer rotation table.",
        "What are the slam bonuses?",
        "A small slam (made 6) scores 500 (not vulnerable) / 750 (vulnerable), a grand slam (made 7) scores 1000 / 1500; with redoubling the bonuses increase again.",
        "How to use the Bridge Scoring tool",
        "Suitable for bridge competition scoring and review: compute contract points, slam / over-trick / vulnerability bonuses and failure penalties from the contract level, suit, doubling status and vulnerability, assisting players in checking scores, analyzing bidding strategy and learning the scoring rules.",
        "What does the Bridge Scoring tool do?",
        "The bridge scoring calculator computes the score from the contract, tricks, vulnerability and doubling status, helping players check scores and keep competition records.",
        "How do you use Bridge Scoring?",
        "Which scenarios suit Bridge Scoring?",
    ]))

    # ---------------- elo-rating (15) ----------------
    write('elo-rating', build('elo-rating', [
        "🔮 Elo Rating Estimate",
        "Compute the Elo rating change and expected win rate from the game result",
        "📖 Read the \"Elo Rating Estimate User Guide\"",
        "📚 Deep dive: Elo Rating Estimate",
        "Single-game rating change: from R_A, R_B and the result (win / loss / draw) compute ΔE and the updated ratings.",
        "Expected win rate: computed from the rating difference as P_A = 1/(1+10^((R_B−R_A)/400)), predicting the tendency of the game.",
        "Multi-game running total: accumulate the rating change over consecutive games to simulate the rise and fall over a stretch of competition.",
        "1500 vs 1600, win, K=32 worked example",
        "Entering R_A=1500, R_B=1600, result win, K=32, the tool outputs an expected win rate of about 36.4%, ΔE ≈ +22.7, new rating ≈ 1522.7, and notes that an upset by the weaker side gains more points.",
        "How do you choose the K value?",
        "Use a large K for new players (such as 40) to converge quickly, and a small K for established players (10/20); many platforms default to 32. The larger the K, the larger the per-game fluctuation.",
        "What is the expected win rate formula?",
        "P = 1/(1+10^(−ΔR/400)); a rating difference of 400 corresponds to a win rate of about 0.91, and a zero difference gives 0.5 each.",
        "Do ratings rise without limit?",
        "They converge to true strength over time; with a balanced win / loss record the rating is stable, while winning or losing streaks automatically slow as the rating difference grows.",
    ]))

    # ---------------- go-territory (17) ----------------
    write('go-territory', build('go-territory', [
        "♟️ Go Territory Count",
        "Compute the territory of both black and white plus the komi, quickly determining the winner and the margin",
        "📖 Read the \"Go Territory Count User Guide\"",
        "Territory method (Japanese / Korean rules): black score = black surrounded territory + black prisoners, white score = white surrounded territory + white prisoners + komi (usually 6.5 points); stone counting method (Chinese rules): black = black living stones + black surrounded territory, white likewise, and black must reach more than 185 stones to win (361 points, half plus komi stones); the score difference = the difference of the two scores, with a positive value meaning black is better and a negative value meaning white is better.",
        "♟️ Count territory",
        "📚 Deep dive: Go Territory Count",
        "Japanese territory count: surrounded points + prisoners + komi, computing the territory difference to determine the winner.",
        "Chinese stone count: living stones + surrounded territory, judged by the stone counting method (with komi stones).",
        "Komi and komi stones compared: the effect of different rules' komi (such as 6.5 points in Japanese / Korean and 3¾ stones ≈ 7.5 points in Chinese) on the result.",
        "Black territory 70 + 5 prisoners, komi 6.5 worked example",
        "Entering black territory 70, 5 prisoners, komi 6.5 and white territory 75, the tool outputs a black total of 81.5 and white 75 under the territory method, so black wins by 6.5 points, and notes that the stone counting method usually agrees.",
        "What is the difference between territory and stone counting?",
        "Japanese territory counting counts surrounded points + prisoners + komi; Chinese stone counting counts living stones + surrounded territory + komi stones. When the rules agree the winner is usually the same.",
        "What is the komi usually?",
        "It depends on the rules: Japanese / Korean usually use 6.5 points (to prevent draws), while Chinese uses 3¾ stones (about 7.5 points).",
        "How are neutral points handled?",
        "Neutral points are not counted under the territory method; under the stone counting method they are assigned to whoever controls them, which is a subtle effect but the rule is clear.",
    ]))


if __name__ == '__main__':
    main()
