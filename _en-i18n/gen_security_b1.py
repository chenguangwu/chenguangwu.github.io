#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'security')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'security')
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
    out = {'slug': slug, 'industry': 'security', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('anti-fraud-cards', build('anti-fraud-cards', [
        "🔒 Anti-Fraud Knowledge Cards",
        "Detailed explanations of 50+ common scam tactics; knowing the scam patterns is the key to effective prevention. Supports random card drawing for learning and category browsing.",
        "Search scam type",
        "Telecom fraud",
        "Impersonation",
        "Online fraud",
        "Daily-life fraud",
        "🎲 Draw a random card",
        "Another card",
        "Scam tactic library (",
        " types)",
        "No matching scam type found",
        "🛡️ Six Don'ts Against Fraud",
        "Don't trust blindly",
        "- Don't trust unknown calls and texts",
        "Don't disclose",
        "- Don't disclose your own or family's identity, savings or bank-card information",
        "Don't transfer money",
        "- Never transfer money or remit to strangers",
        "Don't click",
        "- Don't click unfamiliar links or scan unknown QR codes",
        "Don't be greedy",
        "- Don't believe in 'pie falling from the sky' good deals",
        "Don't hesitate",
        "- In suspicious situations, immediately call 96110 or 110 to report to police",
        "National anti-fraud hotline:",
        ". If scammed, keep evidence such as call logs, chat records and transfer vouchers, and report to police immediately.",
        "Download the 'National Anti-Fraud Center' APP and enable the incoming-call warning feature to effectively identify and block scam calls.",
        "Tool introduction and usage",
        "The anti-fraud knowledge cards collect 50+ common scam tactics, helping recognize scam patterns and raise fraud-awareness.",
        "50+ scam tactics explained",
        "6 categories to browse",
        "Keyword search",
        "Random card learning",
        "Identify features and prevention tips",
        "Fraud-awareness learning",
        "Elderly anti-fraud education",
        "Community safety promotion",
        "Identify suspicious calls",
        "📚 In-Depth Analysis: Anti-Fraud Knowledge Cards",
        "When family or yourself receive a call claiming to be from 'public security/justice/procuratorate' or a 'safe account', use the cards to quickly cross-check identifying features and judge whether it is a scam pattern.",
        "For community anti-fraud promotion or family-group science popularization, systematically browse common tactics by the 6 categories (telecom fraud / investment & wealth / impersonation / online fraud / daily-life fraud / others).",
        "When encountering suspicious texts, links or 'customer-service refund', draw a random card to learn the corresponding pattern and raise vigilance.",
        "Example: the 'impersonating public-security/justice' card",
        "The card gives four identifying features: 1) claiming you are suspected of serious crimes such as money laundering or smuggling; 2) demanding secrecy from family and not telling others; 3) demanding funds be transferred to a so-called 'safe account'; 4) sending forged arrest warrants or summons. Corresponding prevention points: public security/justice/procuratorate never handles cases by phone, there is no 'safe account', any demand for transfer is a scam, hang up immediately and call 110 to verify. The tool collects 50+ tactics (including new patterns such as AI face-swapping/voice-cloning, screen sharing, points redemption), and can be filtered by category or learned by random card drawing.",
        "Do these scam tactics become outdated?",
        "The cards are based on common patterns, already including new tactics such as AI face-swapping, screen sharing and fake stock-touting; scam methods keep evolving, so in practice follow the latest notices from public security authorities and the anti-fraud center (96110); the cards build recognition awareness rather than exhaust all variants.",
        "Can the card content be used as a police report or evidence?",
        "No. The cards are only for identification and prevention education, and have no legal effect; once scammed, immediately call 110 and keep chat records, transfer vouchers, the other party's account and other information to cooperate with police fund-freezing and tracing.",
    ]))

    write('data-erase-simulator', build('data-erase-simulator', [
        "🧪 Data Destruction Simulator",
        "Demonstrates the working principles and steps of common data-erasure algorithms, visually simulating the process of data being overwritten. For safety-education purposes only.",
        "Select erasure algorithm",
        "Simulation settings",
        "Simulated data-block size (bytes)",
        "Animation speed",
        "Slow (800ms)",
        "Medium (400ms)",
        "Fast (150ms)",
        "Start simulation erase",
        "Current algorithm:",
        "Data-block visualization (each cell = 1 byte)",
        "Gray=original data, green=zero-fill, purple=random data, orange=complement, blue=DoD mode, red=Gutmann mode",
        "Erasure steps",
        "Algorithm comparison overview",
        "Overwrite passes",
        "Note: this tool only simulates the erasure process for teaching demonstration and does not actually delete any file. For real data destruction use professional tools (such as shred, DBAN, Eraser, etc.); SSDs should use cryptographic erasure or physical destruction.",
        "Tool introduction and usage",
        "The data-destruction simulator visually shows the working principles of common data-erasure algorithms, helping understand the differences among erasure methods of different security levels.",
        "4 mainstream erasure algorithms",
        "Byte-by-byte visualized overwrite process",
        "Step-by-step animated demonstration",
        "Algorithm security-level comparison",
        "Adjustable simulation speed",
        "Information-security teaching demo",
        "Data-destruction knowledge popularization",
        "Understand erasure-algorithm principles",
        "📚 In-Depth Analysis: Data Destruction Simulator",
        "Before disposing of old hard drives, USB drives or retired phones, understand the security differences among erasure methods and choose a plan matching the data sensitivity.",
        "In enterprise asset retirement, determine whether single-pass, three-pass or multi-pass erasure should be used by confidentiality level (general / confidential / top-secret).",
        "Information-security teaching demo: intuitively compare the recoverability difference between 'single-pass zero-fill' and '35-pass Gutmann'.",
        "Demonstrate overwrite using 1-byte original value 0xA5",
        "Zero-fill erase: overwrite the whole block with 0x00 (1 pass, security level low, suitable for daily non-sensitive data); random fill: write random hex per byte (1 pass, mid, suitable for generally sensitive data); DoD 5220.22-M: overwrite 0x00 -> 0xFF -> random in three passes (3 passes, high, suitable for confidential data / enterprise asset disposal); Gutmann method: overwrite with a fixed pattern sequence for 35 passes (max, suitable for top-secret / military grade). The visualization shows: single-pass zero-fill can be recovered from residual magnetic signal in some scenarios, while 35 passes is almost unrecoverable.",
        "Will this simulator really erase my disk?",
        "No. It is a pure front-end visual demo that only uses random bytes to simulate the overwrite animation on the page, reading and touching no real storage device; for real destruction use professional erasure tools or physical shredding in an offline environment.",
        "Which algorithm is safest? Which to use daily?",
        "Gutmann 35 passes has the highest security level (max), suitable for top-secret data; for daily disposal of sensitive data, DoD 5220.22-M three passes is enough. Note: due to wear-leveling in modern SSDs, logical erase may not cover physical cells; physical destruction should be prioritized in highly sensitive scenarios.",
    ]))

    write('detector-45', build('detector-45', [
        "⚖️ Quality (Standard/Certification/Testing) Assurance",
        "Enter key performance parameters of security products, judge the safety protection level per GB standards",
        "Quality (Standard/Certification/Testing) Assurance",
        "Security products are graded per national standards: anti-theft security doors are divided into four grades by GB 17565 by net anti-destruction working time - Grade A (30 min), Grade B (15 min), Grade C (10 min), Grade D (6 min); electronic anti-theft locks are graded by GA 374 by resistance time and lock-body steel-plate thickness; the judgement is based on anti-destruction time meeting the standard, material thickness not below the standard value, and lock and response times meeting requirements; any indicator failing means not qualified.",
        "Security product type",
        "Anti-theft security door",
        "Electronic anti-theft lock",
        "Video surveillance",
        "Intrusion alarm",
        "Protection / anti-destruction time (min)",
        "Door-leaf steel-plate thickness (mm)",
        "Lock anti-picking time (min)",
        "Environmental-adaptability score (1-10)",
        "📚 In-Depth Analysis: Quality (Standard/Certification/Testing) Assurance",
        "When purchasing anti-theft security doors or electronic anti-theft locks, enter anti-destruction time, steel-plate thickness and anti-picking time, and judge per national standard whether the protection grade is met.",
        "In engineering acceptance or product testing, substitute the measured parameters and issue a qualified conclusion against standards such as GB 17565 / GA 374.",
        "When selecting and comparing prices, use the same set of thresholds to quickly distinguish the protection gap between 'Grade A door' and 'Grade C door', 'Class C lock' and 'Class A lock'.",
        "Example: grading an 'anti-theft security door'",
        "Grading rule (standard GB 17565): anti-destruction time rt≥30 min AND steel-plate thickness sp≥1.8mm AND anti-picking lt≥10 min -> Special grade; rt≥15 AND sp≥1.2 AND lt≥5 -> Grade A; rt≥10 AND sp≥1.0 AND lt≥5 -> Grade B; rt≥6 AND sp≥1.0 AND lt≥1 -> Grade C; otherwise not qualified. Example: rt=20, sp=1.5, lt=8 meets Grade A thresholds (rt≥15, sp≥1.2, lt≥5) -> graded 'Grade A'. Electronic anti-theft lock (GA 374): lt≥30 -> Class C, ≥10 -> Class B, ≥5 -> Class A; video surveillance (GB/T 28181) and intrusion alarm (GB 15463) by environmental-adaptability score es: ≥8 -> Grade I, ≥6 -> Grade II, ≥4 -> Grade III, otherwise Grade IV.",
        "Why are door and lock grades judged separately?",
        "The two execute different standards (door GB 17565, lock GA 374) and differ in protection dimension: the door looks at overall anti-destruction time and steel-plate thickness, while the lock separately looks at anti-picking time. The safety of a whole anti-theft door takes the weaker of 'door body + lock', so the lock should at least reach a grade comparable to the door body (e.g. Grade A door with Class B/C lock).",
        "Can something graded 'not qualified' still be used?",
        "Not qualified means the minimum protection threshold for that category is not met; it is not recommended for scenarios requiring anti-theft; it may be due to too-thin steel plate, insufficient anti-destruction time or too-low lock grade. Regular products should obtain 3C certification; when purchasing, rely on the physical test report and certification mark, and this tool is only a parametric reference.",
        "Anti-theft security door per GB 17565: Grade A anti-destruction ≥15min, Grade B ≥10min, Grade C ≥6min",
        "Electronic anti-theft lock per GA 374: Class A anti-picking ≥5min, Class B ≥10min, Class C ≥30min",
        "Video surveillance tested per GB/T 28181",
        "Intrusion alarm tested per GB 15463",
        "Security products should pass 3C certification before sale",
        "About \"Quality (Standard/Certification/Testing) Assurance\"",
        "A security-product quality-testing tool that enters parameters such as anti-destruction time, steel-plate thickness and lock anti-opening time, and judges the safety protection grade per GB standards.",
        "Four security-product types selectable",
        "Automatic protection-grade judgement",
        "Grade A/B/C / Class A/B/C grading",
        "3C certification standard reference",
        "Security-product acceptance",
        "Anti-theft door quality testing",
        "Smart-lock purchase reference",
        "Security engineering acceptance",
    ]))


if __name__ == '__main__':
    main()
