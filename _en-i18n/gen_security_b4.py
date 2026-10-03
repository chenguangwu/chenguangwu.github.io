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
    write('typhoon-scale', build('typhoon-scale', [
        "📚 Typhoon Grade Reference Table",
        "Beaufort wind scale and China tropical-cyclone grade table, including wind-speed conversion, destructiveness description and prevention advice.",
        "Tropical cyclones are graded by the maximum wind speed near the bottom center: tropical depression 10.8-17.1 m/s (grade 6-7), tropical storm 17.2-24.4 (grade 8-9), severe tropical storm 24.5-32.6 (grade 10-11), typhoon 32.7-41.4 (grade 12-13), severe typhoon 41.5-50.9 (grade 14-15), super typhoon 51.0 and above (grade 16 and above); wind-speed conversion 1 m/s = 3.6 km/h, and the Beaufort scale and wind speed can be estimated by v ≈ 0.836 × grade^1.5.",
        "Wind-speed converter",
        "m/s (meters per second)",
        "km/h (kilometers per hour)",
        "knot",
        "mph (miles per hour)",
        "🌀 China tropical-cyclone grade (national standard GB/T 19201)",
        "Graded by maximum wind near center (2-minute average)",
        "🌬️ Beaufort wind-scale table",
        "Wind-force 0-12 reference, with land/sea behavior",
        "🏠 Typhoon prevention guide",
        "⚠️ Before the typhoon arrives",
        "Follow meteorological warnings, stock over 3 days of food, drinking water and medicine",
        "Check and reinforce doors and windows, tape glass to prevent shattering and splashing",
        "Clear balcony clutter, move flower pots etc. indoors to prevent falling and injury",
        "Check drainage pipes to prevent blockage and standing water",
        "Fully charge phones and power banks, prepare flashlight and spare batteries",
        "Park vehicles in high safe areas, avoid low-lying spots and under trees",
        "🏠 During the typhoon",
        "Stay indoors, away from windows and glass doors",
        "If power outage, turn off appliance switches to prevent short circuit when power returns",
        "Don't stay in dilapidated houses or temporary structures",
        "Avoid open flames, guard against gas leakage",
        "If flooded, never wade through (risk of electric shock or falling into manholes)",
        "✅ After the typhoon",
        "Go out only after officials lift the alert",
        "Stay away from downed wires, fallen trees and damaged buildings",
        "Check house structural safety before returning",
        "Cooperate with the community on post-disaster cleanup and epidemic prevention",
        "Tool introduction and usage",
        "The typhoon grade reference table provides the complete Beaufort-scale and tropical-cyclone-grade comparison, including wind-speed conversion and prevention guide.",
        "Beaufort scale grade 0-12 reference",
        "China tropical-cyclone 6-grade classification",
        "Wind-speed unit conversion",
        "Wind-force destructiveness description",
        "Typhoon prevention guide",
        "Typhoon-season safety",
        "Meteorology knowledge learning",
        "Emergency disaster-prevention education",
        "📚 In-Depth Analysis: Typhoon Grade Reference Table",
        "When watching typhoon warnings, cross-reference the wind-force grade to understand its destructiveness and judge the likely impact on your locality.",
        "Before navigation, going to sea or coastal work, assess wind-grade risk by tropical-cyclone grade and adjust plans.",
        "In emergency preparation, decide the intensity of reinforcement, school/work suspension and supply stockpiling by grade (e.g. severe typhoon / super typhoon).",
        "Example: cross-reference 'central wind 38 m/s'",
        "China tropical-cyclone grading (by maximum wind near center): tropical depression TD (grade 6-7, 10.8-17.1 m/s), tropical storm TS (grade 8-9, 17.2-24.4), severe tropical storm STS (grade 10-11, 24.5-32.6), typhoon TY (grade 12-13, 32.7-41.4), severe typhoon STY (grade 14-15, 41.5-50.9), super typhoon SuperTY (≥16 grade, ≥51.0). 38 m/s falls in the 32.7-41.4 range -> belongs to 'typhoon TY (grade 12-13)', destructiveness 'severe'; km/h conversion: 38 × 3.6 = 136.8 km/h. Accordingly, reinforce doors and windows, stop outdoor activities and stock emergency supplies.",
        "How to convert m/s and km/h?",
        "1 m/s = 3.6 km/h. For example, the lower bound of tropical storm 17.2 m/s ≈ 62 km/h, the lower bound of severe typhoon 41.5 m/s ≈ 149 km/h. The tool provides both unit references for easy understanding in different scenarios (navigation commonly uses m/s, daily broadcast commonly uses km/h).",
        "Does a tropical depression count as a typhoon?",
        "No. A tropical depression (TD, grade 6-7) is the embryo of a tropical cyclone; reaching grade 8 (17.2 m/s) it is called a tropical storm, and only from grade 12 (32.7 m/s) is it called a typhoon. In warnings, 'typhoon' usually refers to TY and above, whose destructiveness is significantly stronger than the depression and storm stages.",
    ]))

    write('virtual-safe', build('virtual-safe', [
        "🛡️ Virtual Safe",
        "Encrypt text with a password and store it in the local browser to protect your private information. All data is saved only on this machine's localStorage, not uploaded to any server.",
        "Safe is locked",
        "Please enter the master password to unlock the safe. First-time users should set a master password.",
        "Unlock / Create",
        "Reset safe",
        "Add encrypted entry",
        "Entry title",
        "Encrypt and save",
        "Lock safe",
        "Safe contents (",
        " entries)",
        "Encryption notes",
        "🔒 Encryption principle",
        "This tool uses a password-based XOR stream cipher combined with a salt value to enhance security:",
        "Each entry uses an independent random salt to prevent identical plaintext producing identical ciphertext",
        "The password is expanded through multiple hash rounds to generate the key stream",
        "Plaintext is XORed with the key stream to produce ciphertext, stored in localStorage",
        "Without the password it cannot be decrypted, and the password is not stored locally",
        "Note: this is a teaching-grade simplified encryption, suitable for daily memo protection, not for storing highly sensitive information. For strong encryption use a professional password manager (such as KeePass, 1Password). Forgetting the password will make data unrecoverable.",
        "Data storage location: browser localStorage; clearing browser data will cause safe contents to be lost, so export and back up regularly.",
        "Tool introduction and usage",
        "The virtual safe uses password-encryption technology to securely store your private text information in the local browser.",
        "Password-encrypted local storage",
        "Independent salt for enhanced security",
        "Real-time password-strength detection",
        "Supports entry management",
        "Exportable encrypted backup",
        "Data not uploaded to server",
        "Store private memos",
        "Temporarily store sensitive text",
        "Personal password memo",
        "Encrypted notes",
        "📚 In-Depth Analysis: Virtual Safe",
        "Temporarily keep infrequently used account passwords, serial numbers or private memos, avoiding plaintext scattered in notes or documents.",
        "Keep a private note locally in the browser, viewable only after entering the correct passphrase to 'unlock'.",
        "Teaching demo: intuitively show that passphrase + salt is hashed then stored, and compared on verification",
        " process.",
        "Example: 'storing a private text'",
        "The tool uses the FNV-1a hash algorithm (seed=0x811c9dc5) to hash 'password + salt', then stores the text and hash value in the browser localStorage. On verification, it recomputes hashStr(pwd + storedSalt) for the entered passphrase and compares it with the stored pwdHash: match unlocks, mismatch rejects. Since the hash is irreversible, the original is never stored in recoverable form - this is also its 'teaching-grade' manifestation: even with local data one cannot reverse the passphrase and original.",
        "Is it safe stored locally? Is it suitable for bank-card passwords?",
        "Data is stored only on this machine's localStorage and not uploaded, but a compromised machine, cleared cache or reinstall will lose it; and it is teaching-grade simplified encryption (hash + fixed salt), not suitable for storing bank cards, master passwords and other highly sensitive information. For highly sensitive scenarios use professional password managers such as KeePass and 1Password.",
        "Can a forgotten passphrase be recovered?",
        "No. The hash is irreversible and there is no backend service; the system stores neither the original nor provides a recovery channel; a forgotten passphrase means the data is permanently ununlockable, so please memorize it or separately back up the plaintext before use.",
    ]))


if __name__ == '__main__':
    main()
