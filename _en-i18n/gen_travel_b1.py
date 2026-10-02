#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'travel')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'travel')
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
    out = {'slug': slug, 'industry': 'travel', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('emergency-phrasebook', build('emergency-phrasebook', [
        "\U0001F4DA Emergency Phrasebook",
        "Essential emergency phrases for travel abroad; tap the speaker to hear them read aloud (browser support required)",
        "Emergency phrases are grouped by scenario: help (police, theft, lost), medical (allergy, fever, injury), transport (rebooking, lost documents) and so on. Each group lists the local-language phrase beside the Mandarin equivalent with pronunciation notes, and roughly 10 to 20 common expressions cover most emergencies. Emergency numbers differ by country (China 110/120/119, EU 112, US 911) and can be tapped to hear them read aloud.",
        "\U0001F4DA In-Depth Analysis: Emergency Phrasebook",
        "Medical Care Abroad",
        "Police / Getting Help",
        "Hotel / Transport Emergencies",
        "English to Japanese for Medical Care",
        "The English \"I need a doctor\" corresponds to the Japanese \"ish\u3044-\u3044\u3048\u3057\u3084 \u3044\u3048\u3057\u3088\u3046 \u304f\u3060\u3055\u3044\" (romanized; hanzi omitted); tap the read-aloud button to play it with SpeechSynthesis, which works even offline.",
        "Multi-language Coverage",
        "Six built-in languages: en/ja/ko/th/fr/es. Switching the tab swaps the phrase list; for example the Thai phrase meaning \"help me\" or the French \"Appelez la police\" (call the police).",
        "Does it support offline reading?",
        "Depends on the browser",
        ". Most environments need no network connection; on some mobile devices the voice pack needs one initial download.",
        "Can I add a local language?",
        "The phrase list is a fixed built-in set. A new language requires editing the source code rather than being entered at runtime.",
        "About \"Emergency Phrasebook\"",
        "Emergency Phrasebook. A travel tool that is essential for trips and works offline.",
    ]))
    write('passport-validator', build('passport-validator', [
        "\U0001F6C2 Passport Number Format Validator",
        "This validator checks legitimacy against the relevant data format and syntax rules, reporting the result and pinpointing errors in real time. It runs entirely in the browser and no code ever leaves it. Tool name: Passport Number Format Validator - a free validator tool for online passport number format validation, free to use.",
        "Input (passport number)",
        "\U0001F4DA In-Depth Analysis: Passport Number Format Validation",
        "Pre-check Before Check-in",
        "Visa Form Cross-check",
        "Multi-country Format Recognition",
        "Chinese E-passport",
        "Entering \"E12345678\" (E plus 8 digits) matches the Chinese e-passport format and reports valid; the older \"G1234567\" (G plus 8 digits) is recognized too.",
        "Wrong Format",
        "Entering \"1234\" has too few digits and no letter prefix, so after filtering nothing matches and the tool reports that it fits none of the known formats and needs checking.",
        "Is this check authoritative?",
        "It only validates the format against each country's number pattern, does not look up whether a number is genuine online, and cannot replace border control.",
        "Which countries are supported?",
        "A table of common country and region formats is built in; anything not listed may be falsely reported as non-matching.",
        "About \"Passport Number Format Validator\"",
        "Passport Number Format Validator. A travel tool that is essential for trips and works offline.",
        "e.g., E12345678",
    ]))
    write('timezone-lookup', build('timezone-lookup', [
        "\U0001F550 Time Zone Lookup (IANA)",
        "Time Zone Lookup is an online tool for travel. A travel tool that is essential for trips and works offline.",
        "Time Zone Lookup",
        "/ Time Zone Lookup",
        "Input (IANA time zone name or city name)",
        "\U0001F4DA In-Depth Analysis: IANA Time Zone Lookup",
        "Time Zone Name Search",
        "Current Time",
        "UTC Offset",
        "Entering \"Tokyo\" matches Asia/Tokyo with offset +9 and shows the current local time (such as 14:23:05), which is useful for checking itinerary times.",
        "Fuzzy Search",
        "Entering \"lon\" matches Europe/London (offset 0/+1). A single result goes straight to the detail view, while multiple results list the candidates.",
        "Does the offset include daylight saving time?",
        "It is computed in real time for the current date, so London shows +1 in summer time and 0 in winter time.",
        "What is returned?",
        "The time zone name, the UTC offset, and the current local time; no future scheduling conversion is performed.",
        "About \"Time Zone Lookup\"",
        "e.g., Asia/Shanghai or Beijing",
    ]))
    write('world-timezone-converter', build('world-timezone-converter', [
        "⏲\ufe0f World Time Zone Converter",
        "View the time in major cities worldwide to schedule cross-time-zone calls with ease",
        "Add a city...",
        "\U0001F4DA In-Depth Analysis: World Time Zone Converter",
        "Many Cities at Once",
        "Day-Change Hint",
        "Daylight Saving Time",
        "20:00 Beijing Across the Globe",
        "20:00 Beijing gives Tokyo +1 = 21:00, London -8 = 12:00, and New York -13 (summer) = 07:00; New York shows \"same day\" because the date has not changed.",
        "Day-Change Labels",
        "02:00 Beijing becomes 13:00 on the previous day in New York, where dayDiff = -1 is labelled \"yesterday\"; the tool adds date annotations automatically to avoid booking mistakes.",
        "Which cities are included by default?",
        "Beijing/Shanghai, Tokyo, London, New York, Los Angeles, and Sydney are built in, and you can add or remove cities with local saving.",
        "What about daylight saving time?",
        "It is judged from each city's offset and the month using empirical rules, which is accurate for the major cities.",
        "About \"World Time Zone Converter\"",
        "World Time Zone Converter. A travel tool that is essential for trips and works offline.",
    ]))


if __name__ == '__main__':
    main()