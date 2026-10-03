#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'antiques')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'antiques')
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
    out = {'slug': slug, 'industry': 'antiques', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # ---------------- bronze-identification (36) ----------------
    write('bronze-identification', build('bronze-identification', [
        "⚖️ Bronze Vessel Identification Reference Table",
        "Comparison of bronze vessel characteristics across periods, including identification essentials of vessel shape, ornament, inscription and casting technique.",
        "/ Bronze Identification",
        "📖 Read the \"Bronze Vessel Identification Reference Table User Guide\"",
        "This table collects the vessel shape, ornament, inscription and casting technique characteristics of bronzes from the Shang, Western Zhou, Spring and Autumn, Warring States to Han periods, for quick comparison during appreciation, dating and authentication. Identification conclusions must combine the physical object with professional testing and are for reference and learning only.",
        "Xia dynasty (Erligang)",
        "Shang dynasty",
        "Western Zhou",
        "Spring and Autumn / Warring States",
        "Qin and Han",
        "📋 Bronze Identification Essentials",
        "Vessel shape: ",
        "Different periods favored different vessel shapes. Xia shapes are simple (mainly wine vessels); Shang wine vessels are advanced (jue, gu, jia); the Western Zhou ritual vessel system is complete (ding-gui combinations); daily utensils increase in the Spring and Autumn / Warring States.",
        "Ornament: ",
        "Shang taotie masks (beast-face motifs) are mysterious and frightening; Western Zhou ornament is simplified; Spring and Autumn / Warring States panchi and panhui dragon motifs are fine and dense; Qin and Han ornament is realistic and restrained.",
        "Inscription: ",
        "Shang inscriptions are brief (clan emblems / sacrifices); Western Zhou has long inscriptions (appointment records, wars); Spring and Autumn / Warring States inscriptions have beautiful script (bird-and-insect script); Qin and Han inscriptions decrease.",
        "Casting: ",
        "Xia used the ceramic piece-mold method (cast in one piece); the separate-casting method became widespread in the Western Zhou; the lost-wax method appeared in the Spring and Autumn; welding technology matured in the Warring States. Mold lines and spacer traces are the basis for judging the technique.",
        "Patina: ",
        "Excavated bronzes have patina on the surface, and the patina color varies with the burial environment. Natural patina has rich layers and is hard and firm; fake patina floats on the surface with a uniform color. This table is for reference and learning.",
        "📚 Deep dive: Bronze Vessel Identification Reference Table",
        "Collectors need to quickly compare vessel shape, ornament and inscription characteristics across periods to make a preliminary dating and authenticity judgment of a bronze at a street stall or auction preview.",
        "Museum and heritage students organize the dating essentials of Shang-Zhou to Han bronzes, building a systematic framework of identification knowledge.",
        "Before an identification institution issues a preliminary opinion, use the table to verify whether core elements such as patina, mold lines and inscriptions are self-consistent.",
        "Preliminary dating of a Western Zhou bronze by \"ornament + inscription\"",
        "A bronze ritual vessel with phoenix-bird ornament and a long inscription: the Shang emphasizes taotie masks and mostly has no inscriptions, the Western Zhou popularizes phoenix-bird ornament and begins to produce long narrative inscriptions (such as the Mao Gong Ding); the Spring and Autumn shifts to panchi dragon motifs, and the Warring States often uses gold and silver inlay. Combining the evolution of the ornament with the presence or absence of inscriptions points initially to the Western Zhou.",
        "Can \"red patches and green patina\" alone prove a bronze is genuine?",
        "Red patches and green patina are common signs of long-term oxidation, but modern forgers can imitate them chemically or by burial, so they cannot alone establish authenticity. You must judge comprehensively by whether the patina layer penetrates into the metal, the bronze quality of the vessel wall, mold lines and weight, and do",
        "alloy composition",
        "testing if necessary.",
        "How can casting technique distinguish Shang-Zhou bronzes from later copies?",
        "Shang and Zhou bronzes were mostly cast with ceramic piece molds, so mold lines and spacer marks are visible on the body; the lost-wax method appears mostly in finely made Spring and Autumn / Warring States pieces. Later copies (especially Ming and Qing) often miss the spirit of the ornament and the bronze quality; mold line positions that do not follow the patterns of the period are an important flaw.",
        "About \"Bronze Vessel Identification Reference Table\"",
        "The bronze vessel identification reference table is an online tool in everyday life scenarios. An everyday life tool that is close to life, practical and convenient.",
        "e.g.: ding, taotie motif, inscription...",
    ]))

    # ---------------- calligraphy-style (35) ----------------
    write('calligraphy-style', build('calligraphy-style', [
        "📚 Calligraphy Style Identification Reference Table",
        "Comparison of calligraphy style characteristics across historical periods, including script evolution, brushwork features, representative calligraphers and works.",
        "/ Calligraphy Style Identification",
        "📖 Read the \"Calligraphy Style Identification Reference Table User Guide\"",
        "This table organizes calligraphy style characteristics by script evolution and representative calligraphers, for reference in calligraphy appreciation, copybook selection and art history study. Style judgment must combine brushwork, character structure and transmitted works for a comprehensive assessment.",
        "Shang-Zhou (oracle bone / bronze script)",
        "Qin dynasty (small seal script)",
        "Han dynasty (clerical script)",
        "Wei-Jin (regular / running / cursive)",
        "Tang dynasty (peak of regular script)",
        "Song dynasty (emphasis on yi / free spirit)",
        "Ming dynasty (tai-ge / romanticism)",
        "Qing dynasty (revival of stele studies)",
        "📋 A Short History of Script Evolution",
        "Script evolution: ",
        "Oracle bone script (Shang) → bronze script (Zhou) → great seal script (Spring and Autumn / Warring States) → small seal script (Qin) → clerical script (Han) → regular / running / cursive (standardized in Wei-Jin) → in use to this day.",
        "Brushwork evolution: ",
        "Rounded seal script with center-tip strokes → angular clerical script with wave tails → regular script with lift-press and pause-stroke → flowing running script with connected strokes → concise, unrestrained cursive script.",
        "Period style: ",
        "\"the Jin people admire yi (resonance), the Tang people admire fa (method), the Song people admire yi (intent), the Ming people admire tai (manner), the Qing people admire bei (stele)\". Each period has a different calligraphic aesthetic, which is an important basis for dating.",
        "Identification essentials: ",
        "Paper / silk material, ink color, seals, colophons and catalogues all assist dating. Brushwork, structure and spirit must be compared with transmitted standard pieces. This table is for reference and learning; authenticity determination requires a professional institution.",
        "📚 Deep dive: Calligraphy Style Identification Reference Table",
        "Calligraphy learners select copybooks by script (seal, clerical, cursive, regular, running) and representative calligraphers, and compare brushwork features to determine the direction of their practice.",
        "Stele and copybook collectors compare the brushwork and character structure of a given master (such as Yan Zhenqing or Liu Gongquan) to judge the school affiliation of a rubbing or a copy.",
        "Art history teaching organizes the main evolutionary thread of \"Jin resonance — Tang method — Song intent — Yuan and Ming return to the ancient\".",
        "Distinguishing the Yan style from the Liu style by \"brushwork + structure\"",
        "Yan Zhenqing (Yan style) uses full, majestic and vigorous brushwork with an expansive outward structure, and broad, dignified characters (such as the Duobaota and Yan Qinli Stele); Liu Gongquan (Liu style) uses lean, hard and taut brushwork drawn inward, with characters tightened at the center (such as the Xuanmita Stele). The so-called \"fleshy Yan bones and lean Liu bones\" refers precisely to this difference of one full and one lean in brushwork, and the two major schools of Tang regular script can be distinguished this way.",
        "How can brushwork tell whether a work is closer to the Jin or the Tang people?",
        "The Jin people (such as Wang Xizhi) emphasize resonance, with agile turning strokes and naturally slanted character structures; the Tang people emphasize method, with regulated brushwork and rigorous, even structures. A regular script stressing lift-press, pause-strokes and a normative framework is closer to Tang method, while a running script with flowing connected strokes and a free natural air is closer to Jin resonance.",
        "How are \"stele studies\" and \"copybook studies\" distinguished in style identification?",
        "Copybook studies take ink copybooks as the authority, with delicate brushwork and a beautiful style (the line of the Two Wangs); stele studies honor stele and stone carving, taking a square, stern, raw quality with a stone-inscription spirit (such as Northern Wei epitaphs and cliff carvings). Stele studies rose in the middle of the Qing, and their works often appear heavy and vast, forming a contrast to the flowing beauty of copybook studies.",
        "About \"Calligraphy Style Identification Reference Table\"",
        "The calligraphy style identification reference table is an online tool in everyday life scenarios. An everyday life tool that is close to life, practical and convenient.",
        "e.g.: Wang Xizhi, Yan Zhenqing, clerical script...",
    ]))

    # ---------------- index (17) ----------------
    write('index', build('index', [
        "🏺 Antique Identification Tools",
        "Antique identification",
        "Antique Identification Tools",
        "A porcelain dating reference table organizing the identification essentials of body and glaze, shape, ornament and reign marks by dynasty, assisting dating and authentication of antique porcelain.",
        "Calligraphy Style Identification Reference Table",
        "Comparison of calligraphy styles across historical periods, including script evolution, brushwork features, representative calligraphers and works, for reference in calligraphy appreciation, copybook selection and art history study.",
        "A comparison of Ming / Qing and classical furniture characteristics, including identification essentials of material, shape, technique and ornament, for reference in classical furniture appreciation, dating and collection authentication.",
        "A comparison of bronze characteristics across periods, including identification essentials of vessel shape, ornament, inscription and casting technique, for reference in antique bronze appreciation, dating and collection study.",
        "A seal identification reference table organizing the material, knob, seal text and use characteristics of seals across periods, assisting seal carving, dating and authentication.",
        "About \"Antique Identification Tools\"",
        "The Antique Identification Tools collection gathers 5 free online tools covering the common calculation, conversion and lookup needs of antique identification scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you will find ready-to-use utilities here. Every tool runs entirely in the browser and never uploads data to the server, so your privacy is protected.",
        "The antique identification tools listed on this page include (a few representative tools):",
        "These tools help you finish common antique identification tasks quickly, with no need to memorize complex formulas or do manual conversions - just enter the inputs and get the result.",
        "Do the antique identification tools require a download or an account?",
        "No. Every tool on this page is a pure front-end online tool: open the page and use it right away, with no software to install, no account to register, and no data uploaded.",
        "Are the antique identification tool results accurate? Is the data safe?",
        "The tools compute locally in your browser based on public mathematical formulas and general industry standards, so results are available instantly. All computation happens locally on your device and no data is uploaded to the server, so your privacy is fully protected.",
    ]))


if __name__ == '__main__':
    main()
