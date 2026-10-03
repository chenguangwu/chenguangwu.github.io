#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'misc2')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'misc2')
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
    out = {'slug': slug, 'industry': 'misc2', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('instrument-tuning', build('instrument-tuning', [
        "📡 Instrument Tuning Frequency Reference",
        "Equal temperament standard frequency table, reference A4 = 440 Hz, customizable reference pitch",
        "Equal temperament frequency = reference frequency × 2 to the (n ÷ 12) power, where n is the number of semitones from the reference; default reference A4 = 440 Hz gives C4 = 261.63 Hz, G4 = 392.00 Hz, C5 = 523.25 Hz; the octave frequency ratio is always 2, perfect fifth about 1.4983, perfect fourth about 1.3348; when customizing the reference, the same-note frequency scales proportionally by new reference ÷ 440 (e.g. at 442 Hz, C4 = 262.82 Hz).",
        "Reference Pitch (Hz)",
        "C0 - C8 (full keyboard)",
        "C1 - C6 (common)",
        "C2 - C5 (vocals/guitar)",
        "C3 - C4 (middle octave)",
        "Copy Table",
        "🎼 Frequency Calculation Principle",
        "Equal Temperament",
        ": divides one octave into 12 equal semitones, with adjacent semitone frequency ratio 2^(1/12) ≈ 1.059463",
        "Calculation Formula",
        "where n is the MIDI note number (A4 = 69) and A4 is the reference frequency (standard 440 Hz)",
        "Common Tuning Standards",
        ": A4 = 440 Hz (international standard), 442 Hz (symphony orchestra), 415 Hz (Baroque)",
        "Tip: when tuning, use the reference note as the standard; ambient temperature and string tension affect the actual pitch, so a professional tuner is recommended for calibration.",
        "📚 In-Depth Analysis: Instrument Tuning Frequency Reference",
        "Look up standard frequencies of each note name (equal temperament) when tuning instruments, setting choir pitch, or teaching acoustics.",
        "Generate a reference table with a custom reference pitch (e.g. A4=442 Hz for early/exotic tunings).",
        "Quickly locate target frequencies other than A4=440 Hz for transposition or ensemble calibration.",
        "Example: \"reference A4=440 Hz, generate C4–C5 range\"",
        "Equal temperament formula f = 440 × 2^((midi-69)/12). C4 (MIDI 60) = 440 × 2^(-9/12) ≈ 261.63 Hz, A4 (MIDI 69) = 440 Hz, C5 (MIDI 72) = 440 × 2^(3/12) ≈ 523.25 Hz. Each semitone multiplies frequency by 2^(1/12) ≈ 1.0595, and an octave multiplies by 2.",
        "What is equal temperament?",
        "Dividing one octave by frequency ratio 2 into 12 equal semitones, with adjacent semitone ratio always 2^(1/12) ≈ 1.0595, and 12 notes cycling back to the octave (×2). Modern pianos, guitars, and other fixed-pitch instruments all follow this temperament, facilitating modulation to any key.",
        "Why is A4=440 Hz commonly used?",
        "440 Hz is the standard pitch agreed internationally in 1939 (concert pitch); most instruments and scores are tuned to it; some classical or regional uses employ 442 Hz, 415 Hz (Baroque), etc., and the tool supports custom reference to generate the corresponding table.",
        "About \"Instrument Tuning Frequency Reference\"",
        "This tool generates a standard frequency reference table for each note name based on equal temperament, suitable for tuning reference of piano, guitar, violin, and other instruments, with support for custom reference pitch (e.g. 442 Hz symphonic tuning).",
        "Complete equal temperament frequency calculation",
        "Supports custom reference A4 frequency",
        "Multiple octave ranges available",
        "Instrument Tuning Frequency Reference Table - equal temperament standard frequency reference, A4=440 Hz, online lookup of frequencies for each note name on piano and guitar, supports custom reference pitch. Daily life tools, close to life, practical and convenient.",
    ]))
    write('insurance-fee', build('insurance-fee', [
        "🚚 Express Insurance Fee Calculator",
        "Enter the goods' declared value to automatically calculate insurance fees and maximum claim amounts for each courier",
        "Express Insurance Fee Calculation",
        "/ Express Insurance Fee Calculation",
        "Insurance fee = declared value × rate, with upper and lower limits by courier rules: the rate is usually 0.5% to 1% (e.g. SF Express about 0.5%, EMS about 1%), minimum charge starts at 1 CNY, and single-shipment maximum coverage is mostly 20,000 to 100,000 CNY; actual fee = min(max(declared value × rate, minimum charge), max cap), and losses beyond the covered amount are not compensated.",
        "Courier Company",
        "SF Express",
        "ZTO Express",
        "YTO Express",
        "Yunda Express",
        "STO Express",
        "China Post EMS",
        "JD Logistics",
        "Declared Value (CNY)",
        "📋 Insurance Rate Reference by Company",
        "Tip: the above rates are common reference standards; the actual rates are subject to each courier's official website and branch announcements. For valuables, full-value insurance and keeping value proof are recommended.",
        "📚 In-Depth Analysis: Express Insurance Fee Calculator",
        "Estimate insurance fees before shipping valuables, compare rates across couriers, and choose the cost-effective option.",
        "Judge the payout gap between insured and uninsured in case of loss or damage to make risk decisions.",
        "Summarize insurance costs for batch shipments to control logistics budget.",
        "Example: \"SF Express, declared value 10,000 CNY\"",
        "Insurance fee = declared value × 0.5% = 50 CNY (minimum 1 CNY, no cap); if China Post EMS (rate 1%) is chosen, insurance fee = 100 CNY. After insurance, if lost or damaged, payment is by declared value (deducting deductible); without insurance, usually only several times the shipping fee is paid, a huge difference.",
        "How is the insurance fee calculated?",
        "Major private couriers (SF/ZTO/YTO/Yunda/STO/JD) mostly charge declared value × 0.5%, minimum 1–2 CNY; EMS charges ×1%. Some companies cap high-value shipments; this table uses common public rates, and the actual rates are subject to each company's latest public notice.",
        "Does insurance guarantee full compensation?",
        "Not necessarily. Insurance pays by declared value, but there is often a deductible or proportional deductible, and you must prove the item's actual value (invoice or proof). Insurance fee is a risk-transfer cost, not the higher the better; declare by the item's true value.",
        "About \"Express Insurance Fee Calculation\"",
        "The express insurance fee calculator helps you quickly estimate insurance fees for major couriers; enter the goods' declared value to compare rates in one click and understand insurance cost and claim limits.",
        "Covers major couriers such as SF, ZTO, YTO, EMS",
        "Automatically calculates insurance fee and maximum claim amount",
        "Supports a rate comparison table for clarity",
        "Express Insurance Fee Calculator. Business office tools, improve work efficiency, data processed locally to protect privacy.",
    ]))
if __name__ == '__main__':
    main()
