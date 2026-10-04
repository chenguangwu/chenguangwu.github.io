#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'yi')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'yi')
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
    out = {'slug': slug, 'industry': 'yi', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

#!/usr/bin/env python3

def main():
    # 64-gua (18)
    write('64-gua', build('64-gua', [
        "📚 I Ching 64 Hexagrams Query (classical reference)",
        "Complete collection of the 64 hexagrams of the I Ching, with hexagram images, judgments, line texts, and plain-language explanations.",
        "I Ching 64 Hexagrams Query (classical reference)",
        "/ I Ching 64 Hexagrams Query (classical reference)",
        '📖 View the "I Ching 64 Hexagrams Query (classical reference)" User Guide',
        "📚 In-depth: I Ching 64 Hexagrams Query (classical reference)",
        "After casting a hexagram: derive the six lines from three coins or yarrow stalks (from bottom to top, initial to top), then look up the 64-hexagram table to read the name, sequence number, and upper/lower trigram combination.",
        "Study of classic and commentary texts: look up a hexagram's judgment, line texts, and the gist of the Tuan (Judgment) and Xiang (Image) commentaries to understand pronouncements such as 'Yuan Heng Li Zhen' (primordial, flourishing, beneficial, correct).",
        "Derivation of the inverse and complementary hexagrams: from the primary hexagram derive its inverse (all six lines flipped) and complementary (top and bottom swapped) hexagrams, helping understand how meanings transform.",
        'Reading a hexagram using "Qian (The Creative / Heaven)" as an example',
        "Qian is the 1st of the 64 hexagrams (sequence 1); both upper and lower trigrams are Qian (☰), all six lines are yang, its judgment is 'Yuan Heng Li Zhen' (primordial, flourishing, beneficial, correct), symbolizing strength and vigor. Its inverse is Kun (☷, all yin); its complementary is also Qian (self-symmetric). The changed hexagram, when the initial yang line changes, becomes Tian Feng Gou (䷫, Heaven and Wind, Coming to Meet). The table lets you quickly locate the name, sequence, upper/lower trigrams, and basic pronouncements.",
        "How are the 64 hexagrams formed from the 8 trigrams?",
        "The 64 hexagrams come from combining the 8 three-line trigrams in pairs (lower trigram x upper trigram), giving 8 x 8 = 64 six-line hexagrams. Each has a fixed sequence (the standard Zhouyi order or the Jing Fang Eight Palaces order) and is paired with a name and judgment; they are the core of I Ching divination and philosophical study.",
        "What are the sequence number and name for?",
        "The sequence aids lookup and memory (e.g., Qian 1, Kun 2, Zhun 3, Meng 4 …), and the name summarizes a hexagram's theme (e.g., 'Tai' denotes heaven and earth communicating, 'Pi' denotes heaven and earth not communicating). After casting, you can look up by sequence or by upper/lower trigram to locate the primary and changed hexagrams.",
        'About "I Ching 64 Hexagrams Query (classical reference)"',
        "I Ching 64 Hexagrams Query (classical reference). An I Ching / Bagua tool that helps arrange and interpret hexagrams.",
        "Hexagram name / image / judgment...",
    ]))

    # bagua-viewer (22)
    write('bagua-viewer', build('bagua-viewer', [
        "📐 Pre-Heaven Bagua Position Diagram (traditional culture illustration)",
        "Interactive post-heaven and pre-heaven Bagua position diagram (traditional culture illustration). Click each trigram for a detailed explanation (cultural reference, for learning only).",
        "Pre-Heaven Bagua Position Diagram (traditional culture illustration)",
        "/ Pre-Heaven Bagua Position Diagram (traditional culture illustration)",
        '📖 View the "Pre-Heaven Bagua Position Diagram (traditional culture illustration)" User Guide',
        "Pre-Heaven Bagua positions: Qian (Heaven) south, Kun (Earth) north, Li (Fire) east, Kan (Water) west, Dui (Lake) southeast, Zhen (Thunder) northeast, Xun (Wind) southwest, Gen (Mountain) northwest. A trigram is formed by three lines from bottom to top; a yang line is solid, a yin line is broken. The eight trigrams combined in pairs yield the 64 hexagrams; the position-to-trigram correspondence is used for traditional culture study.",
        "🗺️ Position Diagram",
        "📋 Trigram Details",
        "📖 Bagua Knowledge",
        "Qian Trigram",
        "📚 In-depth: Pre-Heaven Bagua Position Diagram (traditional culture illustration)",
        "I Ching primer: compare the Pre-Heaven Bagua (Fuxi) and Post-Heaven Bagua (King Wen) arrangements to understand the difference between 'Qian south, Kun north' and 'Li south, Kan north'.",
        "Position marking: mark room or house orientations by the Post-Heaven Bagua positions (Qian northwest, Kan north, Gen northeast, Zhen east, Xun southeast, Li south, Kun southwest, Dui west).",
        "Teaching demo: use the Bagua diagram to explain the three-line yin-yang combinations (☰ all yang to ☷ all yin) and their corresponding natural images (heaven / lake / fire / thunder / wind / water / mountain / earth).",
        'Marking the eight directions of a residence by the Post-Heaven Bagua',
        "The Post-Heaven Bagua is oriented with Li south and Kan north: due north is Kan (☵, water), due south is Li (☲, fire), due east is Zhen (☳, thunder), due west is Dui (☱, lake), southeast is Xun (☴, wind), southwest is Kun (☷, earth), northwest is Qian (☰, heaven), northeast is Gen (☶, mountain). Overlaying the Bagua diagram on a floor plan reveals each direction's trigram and Five Elements (Kan water / Li fire / Zhen and Xun wood / Qian and Dui metal / Kun and Gen earth).",
        "How to distinguish Pre-Heaven and Post-Heaven Bagua?",
        "The Pre-Heaven Bagua (Fuxi) emphasizes 'opposition': arranged as Qian south, Kun north, Li east, Kan west, Zhen northeast, Dui southeast, Xun southwest, Gen northwest, used to expound the principle of yin-yang opposition. The Post-Heaven Bagua (King Wen) emphasizes 'flow': arranged as Li south, Kan north, Zhen east, Dui west, Qian northwest, Kun southwest, Xun southeast, Gen northeast, used to correspond to actual directions and the flow of vital energy. Their uses differ and they must not be mixed.",
        "How do the Bagua's yin-yang and Five Elements correspond?",
        "All-yang three lines form Qian (heaven), all-yin form Kun (earth); Qian and Dui belong to metal, Kan to water, Zhen and Xun to wood, Li to fire, Kun and Gen to earth. The Bagua diagram commonly pairs each trigram with a Five Element and direction, forming a base symbol system shared by traditional culture such as feng shui, Chinese medicine, and fortune telling.",
        'About "Pre-Heaven Bagua Position Diagram (traditional culture illustration)"',
        "Pre-Heaven Bagua Position Diagram (traditional culture illustration) is an online tool in the I Ching / Bagua domain. An I Ching / Bagua tool that helps arrange and interpret hexagrams.",
    ]))

    # gua-interpretation (22)
    write('gua-interpretation', build('gua-interpretation', [
        "📐 Zhouyi Hexagram Judgment Annotation",
        "Input the yin-yang of six lines to derive the hexagram and interpretation.",
        "Zhouyi Hexagram Judgment Annotation",
        "/ Zhouyi Hexagram Judgment Annotation (classical reference)",
        "Zhouyi Hexagram Judgment Annotation (classical reference)",
        '📖 View the "Zhouyi Hexagram Judgment Annotation (classical reference)" User Guide',
        "🎲 Random Demo",
        "All Yang (Qian)",
        "All Yin (Kun)",
        "Tai",
        "📚 In-depth: Zhouyi Hexagram Judgment Annotation (classical reference)",
        "Primary + changed hexagram reading: cast to obtain the primary hexagram and moving lines, then set the reading focus by the number of moving lines (no moving line reads the primary judgment; one moving line reads that line's text, etc.).",
        "Line-position analysis: see which line is in use (initial / 2nd / 3rd / 4th / 5th / top) and whether it is yang or yin, and whether it is 'in position' (yang on a yang position, yin on a yin position), to judge the timing and fortune.",
        "Hexagram virtue and image-number: combine the virtues of the upper and lower trigrams (Qian is strong, Kun is yielding, Kan is perilous, Li is clinging, etc.) with the nuclear and resultant hexagrams to give an integrated image-number reading.",
        'Example: the initial line change of "Shui Huo Ji Ji (Water and Fire, After Completion)"',
        "Ji Ji (䷾, Li below Kan above, water over fire): when the initial yang line changes it becomes Shui Lei Zhun (䷂, Water and Thunder, Difficulty at the Beginning). By the ancient rule 'one moving line reads the changed line's text': Ji Ji's initial yang line says 'drag the wheel, wet the tail, no blame', meaning at the start of a matter one should stay steady and not rush. Combining the initial line's 'beginning of the matter' with Ji Ji's 'already accomplished' image yields the reading 'even at the start of success, proceed with caution'.",
        "How to read different numbers of moving lines?",
        "Traditional Zhouyi divination: no moving line reads the primary judgment; one moving line reads that line's text; two moving lines read both changed lines' texts, the upper one dominant; three moving lines read the primary and changed judgments; four moving lines read the two unchanged lines of the changed hexagram; five moving lines read the one unchanged line of the changed hexagram; all six changing reads the changed judgment (Qian and Kun use 'Use Nine / Use Six'). This tool locates the reading focus by these rules.",
        'What are "being in position" and "overriding, supporting, adjacent, corresponding"?',
        "'Being in position' means a yang line on an odd position (1/3/5, yang positions) or a yin line on an even position (2/4/6, yin positions) is proper; otherwise it is improper. 'Overriding, supporting, adjacent, corresponding' describes line relationships (support = lower bears upper; override = upper presses lower; adjacent = neighboring; correspond = initial-4th / 2nd-5th / 3rd-top respond). These are common terms in hexagram interpretation for refining fortune judgment.",
        'About "Zhouyi Hexagram Judgment Annotation (classical reference)"',
        "Zhouyi Hexagram Judgment Annotation (classical reference) is an online tool in the I Ching / Bagua domain. An I Ching / Bagua tool that helps arrange and interpret hexagrams.",
    ]))

    # yi-divination (24)
    write('yi-divination', build('yi-divination', [
        "🎲 I Ching Hexagram Random Demo",
        "Silently focus on your question, then click the button below to cast a hexagram.",
        "I Ching Hexagram Random Demo",
        "/ I Ching Hexagram Random Demo (entertainment, not fortune-telling)",
        "I Ching Hexagram Random Demo (entertainment, not fortune-telling)",
        '📖 View the "I Ching Hexagram Random Demo (entertainment, not fortune-telling)" User Guide',
        "🙏 Cast Demo",
        "📚 In-depth: I Ching Hexagram Random Demo (entertainment, not fortune-telling)",
        "Casting: focus on your question, shake three coins six times (or use a number/time method) to get the yin-yang of six lines, arranging them bottom-up into the primary hexagram.",
        "Determining the changed hexagram: set moving lines by 'old yang becomes yin, old yin becomes yang' to generate the changed hexagram; the primary shows the current state, the changed shows the trend.",
        "Interpreting: by the number of moving lines (0-6) look up the corresponding line/judgment rules and combine with the hexagram image to give an image-number level reference.",
        'Casting steps using "the Great Expansion number fifty"',
        "The ancient method 'the Great Expansion number is fifty, its use forty-nine': divide into two, set aside one, count by fours, and group the remainder as one change; three changes make one line (remainders 36/32/28/24 correspond to old yang 9 / young yin 8 / young yang 7 / old yin 6, with 36 and 24 as moving lines). Repeating three changes x six lines yields six lines; old yang (9) becomes yin, old yin (6) becomes yang, giving the primary and changed hexagrams. The tool simulates this process with equal probability and is a traditional-culture entertainment reference.",
        "What do the primary and changed hexagrams mean respectively?",
        "The primary hexagram (unchanged) reflects the current state of the matter; the changed hexagram, obtained by reversing the moving lines' yin-yang, reflects the evolution trend. With no moving line (static hexagram) read only the primary judgment; with moving lines read by the rules for that count (see the ",
        "Gua Interpretation Guide",
        " tool notes).",
        "Can the demo result be used as a decision basis?",
        "No. This tool is an entertainment demo of traditional culture and folklore; the result is generated by ",
        "Random",
        " simulations of the Great Expansion / coin-casting process and contains no scientific claim. For life and practical decisions, rely on real information, professional advice, and your own judgment; this tool offers no recommendation.",
        'About "I Ching Hexagram Random Demo (entertainment, not fortune-telling)"',
        "I Ching Hexagram Random Demo (entertainment, not fortune-telling) is an online tool in the I Ching / Bagua domain. An I Ching / Bagua tool that helps arrange and interpret hexagrams.",
        "Silently focus on the question you want to ask...",
    ]))

    # yi-yao (19)
    write('yi-yao', build('yi-yao', [
        "📚 Zhouyi Line Text Query (classical reference)",
        "Complete line texts of the 384 lines across 64 hexagrams; classic Zhouyi literature.",
        "Zhouyi Line Text Query (classical reference)",
        "/ Zhouyi Line Text Query (classical reference)",
        '📖 View the "Zhouyi Line Text Query (classical reference)" User Guide',
        "📚 In-depth: Zhouyi Line Text Query (classical reference)",
        "Reading lines: by hexagram name + line order (e.g., 'Qian · Initial Nine') look up the corresponding line text and line title (Initial Nine / Second Nine / Third Six, etc.) to trace the source of famous lines such as 'the hidden dragon does not act'.",
        "Xi Ci study: compare the upper and lower classics of the Zhouyi with the Xi Ci (Appended Judgments) commentary on the philosophical exposition of line texts, grasping 'the alternation of yin and yang is the Way'.",
        "Locating the used line: in divination, the moving line locates the line text to read (e.g., the third line moving reads 'Third Nine / Third Six'), connecting to the ",
        "Gua Interpretation Guide",
        " tool usage.",
        'Overview of the six line texts of "Qian Trigram"',
        "Qian's six lines are all yang, with titles from Initial Nine to Top Nine: Initial Nine 'the hidden dragon does not act', Second Nine 'the dragon appears in the field', Third Nine 'the noble-one toils all day', Fourth Nine 'he may leap into the abyss', Fifth Nine 'the flying dragon is in the heavens', Top Nine 'the arrogant dragon has regret'; plus 'Use Nine: see the flock of dragons without a head, auspicious'. The six lines show yang rising from hidden to extreme and then to 'fullness cannot last', a typical example for understanding the Zhouyi's line-position thought.",
        'How to read "Initial Nine" and "Third Six" in line titles?',
        "A line title combines 'line position + line nature': initial/2nd/3rd/4th/5th/top denote positions from bottom up, and nine = yang line, six = yin line. Thus 'Initial Nine' = the lowest yang line, 'Third Six' = the third yin line, 'Top Six' = the top yin line. To look up a line text, first fix the hexagram, then the moving line position.",
        'Why is a yang line called "nine" and a yin line called "six"?',
        "It originates from the Zhouyi marking yin-yang as 'old yang nine, old yin six' (related to the counting method: old yang stalks 36/4=9, old yin 24/4=6). Later generations used 'nine' for yang lines and 'six' for yin lines in line titles, corresponding one-to-one with the line images (— / --).",
        'About "Zhouyi Line Text Query (classical reference)"',
        "Zhouyi Line Text Query (classical reference) is an online tool in the I Ching / Bagua domain. An I Ching / Bagua tool that helps arrange and interpret hexagrams.",
    ]))

if __name__ == '__main__':
    main()
