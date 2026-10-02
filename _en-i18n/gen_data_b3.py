#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'data')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'data')
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
    out = {'slug': slug, 'industry': 'data', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('random-3', build('random-3', [
        "🔑 Random Password (existing, can be strengthened)",
        "Existing, can be strengthened",
        "A random password samples characters uniformly from the character set: available characters = 26 uppercase + 26 lowercase + 10 digits + about 32 symbols; the number of combinations = charset size ^ length (62 to the 12th power is about 3.2 × 10²¹); entropy = length × log₂(charset size) bits, and anything under 60 bits counts as a weak password; a length of at least 12 characters mixing all four classes is recommended.",
        "📚 Deep Dive: Random Password (existing, can be strengthened)",
        "Account signup: generate a high-strength random passcode so you never reuse a weak password.",
        "Temporary credential: create a short-lived credential for test accounts or one-time access.",
        "Key fragment: use it as a salt value or an auxiliary fragment of a random seed (not a complete key).",
        "Generate a 16-character strong password",
        "Set the length to 16 with",
        "+ digits + symbols, and the tool outputs something like \"Kp9#mQ2xLb8@Wn3v\", ready to copy; it is generated locally and not retained.",
        "Is the randomness secure enough?",
        "It is based on the browser's",
        "random number",
        "source, so the strength depends on the length and character set; for important accounts use at least 12 characters and store them safely.",
        "Are passwords saved?",
        "No, they are only generated locally and nothing remains after you close the page, so never generate sensitive credentials on a public device.",
        "Can confusing characters be excluded?",
        "Some versions can exclude 0/O, 1/l and similar pairs; the page's options are authoritative, and it helps when people have to type the value by hand.",
        "About Random Password (existing, can be strengthened)",
        "Random password (existing, can be strengthened). Data analysis tools that help you process and visualize data quickly.",
    ]))
    write('random-4', build('random-4', [
        "🎲 Random Verification Code (digits / letters / mixed)",
        "Digits / letters / mixed",
        "A verification code draws characters at random from the character set: 10 characters for the digit type, 26 for letters (or 52 with both cases), 36 or 62 for the mixed type; the number of combinations for an n-digit code = charset size ^ n (a 6-digit numeric code is 10⁶); confusing characters such as 0 versus O and 1 versus l can be excluded to avoid misreading, and each character is drawn independently with equal probability.",
        "📚 Deep Dive: Random Verification Code (digits / letters / mixed)",
        "Form demo: create sample values for a",
        "verification code",
        "input to check the refresh and comparison logic.",
        "Teaching sample: generate a reproducible code on the spot when explaining randomness and verification.",
        "Local testing: generate codes in bulk to test length and charset constraints.",
        "Generate a 6-character alphanumeric code",
        "Set the length to 6 and the charset to letters + digits; the tool outputs something like \"a3F9kZ\", which can demo the refresh behavior and case-insensitive",
        "comparison of verification codes.",
        "Can confusing characters be excluded?",
        "The page's options are authoritative; some versions can exclude 0/O, 1/l and similar pairs to make manual reading easier.",
        "Is this a real verification service?",
        "No, it only generates local samples with no anti-bot and no expiry check; use a professional service for production verification.",
        "Is anything recorded?",
        "Everything is generated locally with no upload, and nothing remains after you close the page.",
        "About Random Verification Code (digits / letters / mixed)",
        "Random verification code (digits, letters or mixed). Data analysis tools that help you process and visualize data quickly.",
    ]))
    write('random-5', build('random-5', [
        "🎲 Random Chinese Names (built-in surname and given-name pools)",
        "Built-in surname and given-name pools",
        "A Chinese name is randomly assembled from the pools: name = 1 character drawn at random from the surname pool + 1 to 2 characters drawn at random from the given-name pool; the total number of candidates = number of surnames × number of given names (for single-character names) or number of surnames × the square of the number of given names (for two-character names); the pool can be filtered by gender and constrained by name length, and the collision rate falls as the pools grow.",
        "📚 Deep Dive: Random Chinese Names (built-in surname and given-name pools)",
        "Test data: create sample Chinese names for a user table to check display and sorting.",
        "Character naming: draw a few candidate names at random while writing and then pick one.",
        "Anonymized placeholders: replace names in real samples with simulated ones.",
        "Generate 5 male names",
        "Set the gender to male and the length to 2 characters; the tool outputs names such as \"Chen Yu / Li Ming / Wang Hao\", ready to paste into a test sheet or a draft.",
        "Are these real people's names?",
        "They are random combinations and may coincidentally match a real name, but they are not real identities and must not be used to impersonate anyone.",
        "Can gender and length be chosen?",
        "Gender and name length can be set through the page's options; the page is authoritative.",
        "Is the data safe?",
        "It is generated locally with no upload and nothing remains after you close the page, which suits samples containing name fields.",
        "About Random Chinese Names (built-in surname and given-name pools)",
        "Random Chinese names (built-in surname and given-name pools). Data analysis tools that help you process and visualize data quickly.",
    ]))
    write('random-6', build('random-6', [
        "🎲 Random Number (integer / float)",
        "Integer / float",
        "A random integer is drawn from a closed interval: x = floor(random() × (max − min + 1)) + min; a random float = random() × (max − min) + min truncated to the given number of decimals; for batch deduplication, values are checked against a set and redrawn, or a Fisher-Yates shuffle is used to guarantee equal-probability sampling without repeats.",
        "📚 Deep Dive: Random Number (integer / float)",
        "Draws and sampling: take random integers from a numbered range for a fair draw or sample selection.",
        "Simulated inputs: feed random float inputs to an algorithm to check boundaries and stability.",
        "Test data: generate values in bulk to fill tables or API payloads.",
        "Draw 3 distinct integers",
        "Set the range to 1-100, the count to 3 and enable deduplication; the tool outputs values like \"17 / 42 / 88\", ready for a draw or sample numbering.",
        "Can it deduplicate in bulk?",
        "You can set the count and tick deduplication; when the count exceeds the range it warns that uniqueness cannot be guaranteed, and the page is authoritative.",
        "How is float precision handled?",
        "Values are generated with the configured number of decimals, purely for simulation and testing, and statistical uniformity is not guaranteed.",
        "Are the results retained?",
        "They are only generated locally with no upload, and closing the page clears them, which suits temporary sampling.",
        "About Random Number (integer / float)",
        "Random numbers (integers and floats). Data analysis tools that help you process and visualize data quickly.",
    ]))
    write('random-7', build('random-7', [
        "📅 Random Date (within a given range)",
        "Given range",
        "A random date is drawn between the start and end: random timestamp = start timestamp + random() × (end timestamp − start timestamp), then output in the target format; you can restrict it to weekdays only (skipping Saturday and Sunday), a specific month or a specific year; across a leap year the number of days in February is automatically corrected to 29 or 28 following the Gregorian calendar rules.",
        "📚 Deep Dive: Random Date (within a given range)",
        "Test fill: create random samples for date fields to check range validation and sorting.",
        "Schedule simulation: pick several dates at random inside a project window to draft a Gantt chart or milestones.",
        "Demo sample: quickly build a stretch of dates for placeholder display on a page.",
        "Generate a random day within 2026",
        "Set the start to 2026-01-01 and the end to 2026-12-31; the tool outputs something like \"2026-07-14\", and you can switch to formats such as YYYY/MM/DD and copy it into a form.",
        "Which formats are supported?",
        "Common date formats can be switched through the page's options; the page is authoritative, and everything is generated locally.",
        "Are the endpoints included?",
        "It follows the inclusion rule the page uses; the page's description is authoritative, and checking the boundaries after sampling is recommended.",
        "Is anything recorded?",
        "Everything is generated locally with no upload, and nothing remains after you close the page.",
        "About Random Date (within a given range)",
        "Random date (within a given range). Data analysis tools that help you process and visualize data quickly.",
    ]))
    write('random-9', build('random-9', [
        "🎲 Random Sentence / Paragraph (built-in corpus)",
        "Built-in corpus",
        "Random text is stitched together from the corpus: a sentence = one sentence drawn uniformly at random from the corpus; a paragraph = n consecutive sentences drawn (n can be set from 3 to 8) and joined with periods; removing repeated sentences improves readability; the combination space = number of corpus sentences to the power of n, which suits placeholder copy, layout demos and writing inspiration.",
        "📚 Deep Dive: Random Sentence / Paragraph (built-in corpus)",
        "Placeholder copy: fill a design mockup with random paragraphs to check the layout before swapping in real content.",
        "Layout demo: use paragraphs of varying length to test line breaks, indentation and fonts.",
        "Writing inspiration: draw a random sentence to trigger an idea, then expand on it.",
        "Generate 2 placeholder paragraphs",
        "Set the paragraph count to 2 and the tool stitches two coherent paragraphs from the corpus; paste them into the prototype to see the layout, then replace them with the final copy later.",
        "Is the content original?",
        "It is randomly stitched from a built-in corpus, so it reads coherently but does not constitute an original work, and it is only for placeholders and demos.",
        "Can the length be set?",
        "The sentence or paragraph count can be set through the page's options; the page is authoritative.",
        "Is anything recorded?",
        "Everything is generated locally with no upload, and nothing remains after you close the page.",
        "About Random Sentence / Paragraph (built-in corpus)",
        "Random sentences and paragraphs (built-in corpus). Data analysis tools that help you process and visualize data quickly.",
    ]))


if __name__ == '__main__':
    main()
