#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'safety')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'safety')
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
    out = {'slug': slug, 'industry': 'safety', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('index', build('index', [
        "🦺 Work Safety Production Tools",
        "Work Safety Production",
        "Work safety production tools",
        "File Hash Verification (MD5/SHA-1, existing)",
        "Compute MD5, SHA-1 and SHA-256 hashes of text or files, for integrity verification and consistency comparison. Computed locally in the browser with no data uploaded to the server.",
        "Hazard inspection checklist generator: structurally generates hazard inspection checklists by industry and work scenario, covering inspection items, risk levels and closed-loop remediation records, to support corporate safety management.",
        "Generate a first aid kit item list by travel, home or outdoor scenario, tickable and exportable, for disaster preparedness reference. Generated purely in the browser with no network access.",
        "Password Strength Checker",
        "Enter a password to evaluate its security strength in real time. It analyzes character types, length, complexity and common patterns from multiple dimensions, estimates cracking time and gives improvement suggestions. Passwords are processed locally only and never uploaded.",
        "Anti-fraud knowledge card tool: randomly shows cards of common telecom and online fraud methods and prevention points, helping the public recognize scams such as order-brushing refund schemes and fake customer service, and raising fraud awareness.",
        "Import a local security log to statistically analyze anomalies by time, IP and event type, generating an overview for troubleshooting. The file is parsed in the browser with no data uploaded.",
        "Hazard Inspection Checklist",
        "Pick a work or premises scenario and the tool generates the matching hazard inspection checklist with one click, tracks each item's remediation progress, computes the closed-loop rate and supports export. Data is stored locally for routine safety management and audit trails.",
        "Password Manager Tool",
        "On first use, set a master password to encrypt and store your credentials. The master password cannot be recovered, so be sure to remember it.",
        "Randomly draw 10 work safety knowledge questions covering fire safety, electrical safety, chemical, construction, special equipment, emergency response and other areas. Answers are scored automatically with detailed explanations.",
        "Enter the number of evacuees, floors and start/end times to automatically compute total evacuation duration, evacuation flow and time per floor, and assess drill efficiency against the per-floor baseline",
        "Accident Frequency Statistics",
        "Accident Frequency / Severity Rate Report",
        "Personal protective equipment (PPE) replacement and inspection tracking, with a built-in replacement cycle database, sorted by due urgency, reminding you to replace and inspect on time.",
        "Records replacement dates and cycles of labor protective equipment, automatically computes due dates and sends reminders, supports list export and keeps data in the local browser for safety management.",
        "A 15-question safety knowledge self-test covering fire, electrical, protection and hazardous chemicals, with instant feedback after each answer, for corporate safety training and employee safety literacy assessment.",
        "About \"Work Safety Production Tools\"",
        "The Work Safety Production Tools collection gathers 14 free online tools covering the common calculation, conversion and lookup needs of work safety scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you will find ready-to-use practical tools here. Every tool runs purely in the browser and never uploads data to a server, so your privacy is protected.",
        "Work safety production tools included on this page (some representative tools):",
        "These tools help you finish common work safety tasks quickly, with no need to memorize complex formulas or convert by hand — enter the inputs and you get the result.",
        "Do the work safety production tools need a download or sign-up?",
        "No. Every tool on this page is a pure front-end online tool. Open the page and you can use it right away, with no software to install, no account to create, and no data uploaded at all.",
        "Are the results of the work safety production tools accurate? Is the data secure?",
        "Each tool computes locally in your browser from public mathematical formulas and general industry standards, so results are available instantly. All computation happens on your own device and data is never uploaded to a server, so privacy and security are guaranteed.",
    ]))
    write('detector-strength', build('detector-strength', [
        "🔑 Password Strength Checker (Security)",
        "Enter a password to evaluate its security strength in real time. It analyzes character types, length, complexity and common patterns from multiple dimensions, estimates cracking time and gives improvement suggestions. Passwords are processed locally only and never uploaded.",
        "Password Strength Checker",
        "📖 Read the Password Strength Checker (Security) user guide",
        "Strength score accumulates by dimension: length score (under 8 characters 0 points, 8 to 11 characters 10 points, 12 to 15 characters 20 points, 16 characters or more 30 points) + character set score (upper and lower case, digits, symbols 15 to 25 points each) − penalties (consecutive or repeated characters, weak password dictionary hits); cracking time = character set size ^ length ÷ attempts per second (about 10¹⁰ per second offline), under 1 second is extremely weak and over 100 years is very strong.",
        "Passwords are analyzed locally in the browser and never sent to any server, so use it with confidence",
        "Scoring dimensions: character types (upper/lower case, digits, special symbols), length, character diversity, common pattern detection",
        "Cracking time is estimated on the basis of 10 billion hashes per second on an ordinary computer; the real figure depends on the attacker's computing power",
        "Password length ≥12 characters is recommended, including upper and lower case letters, digits and special symbols, and avoid using personal information",
        "Use different passwords for different websites and services, and a password manager is recommended",
        "📚 Deep dive: Password Strength Checker (Security)",
        "Enter a password to instantly estimate its entropy, quantifying how hard it is to brute force, and flag whether it is up to standard.",
        "Assess by character set size: digits only, then adding letters, then adding symbols makes entropy grow logarithmically.",
        "Compare against a target security level (such as 60 bit or more) and give improvement suggestions.",
        "Entropy formula",
        "Password entropy (bit) = length × log2(pool size). Pool: digits only 10, adding lowercase 36, adding",
        "62, adding symbols about 95. Higher entropy is harder to brute force; generally ≥ 60 bit is advised, high security ≥ 80 bit.",
        "8 digits only: 8×log2(10)≈26.6 bit (very weak); 8 characters of upper/lower case plus digits: 8×log2(62)≈47.6 bit; 12 characters with symbols: 12×log2(95)≈78.6 bit (passes). \"password\" is long but has a small and common character pool, so dictionary words should still be avoided.",
        "Is high entropy always secure?",
        "Not necessarily. If the password is a common dictionary word or follows a keyboard pattern (such as asdf1234), it can still be cracked by dictionary or rule-based attacks even with a large character set; randomness and non-dictionary structure matter.",
        "How long is enough?",
        "12 characters or more including symbols usually reaches ≥ 75 bit, and generating random passwords with a password manager is safest; add two-factor authentication for important accounts.",
        "About \"Password Strength Checker\"",
        "A real-time password strength evaluation tool that scores comprehensively across character types, length, information entropy and common weak password patterns, estimates brute force time, and helps users set secure and reliable passwords.",
        "Real-time password strength analysis with visual presentation",
        "Detection of common weak passwords, consecutive sequences and repeated characters",
        "Information entropy computation and brute force time estimation",
        "Pure front-end processing, passwords never uploaded to the server",
        "Security check before setting an important account password",
        "Security awareness training demonstrations",
        "Password policy compliance verification",
    ]))
    write('self-test', build('self-test', [
        "📖 Work Safety Knowledge Online Self-Test Question Bank",
        "Randomly draw 10 work safety knowledge questions covering fire safety, electrical safety, chemical, construction, special equipment, emergency response and other areas. Answers are scored automatically with detailed explanations.",
        "📖 Read the Work Safety Knowledge Online Self-Test Question Bank user guide",
        "The work safety knowledge self-test randomly draws 10 questions and scores them: score = correct answers × 10 (100 full marks); 90 or above is excellent, 80 to 89 is good, 60 to 79 is pass, and below 60 is fail and requires retraining. Questions cover fire safety, electrical safety, chemical, construction, special equipment and emergency response, and after answering, error types are attributed by knowledge point with targeted revision suggestions.",
        "The question bank covers fire safety, electrical safety, chemical safety, building construction, special equipment, occupational health, emergency response and more",
        "Each round randomly draws 10 questions, 10 points each, 100 full marks, 80 is the pass mark",
        "After answering you can review the explanation and correct answer for every question",
        "Question bank content is compiled from Work Safety Law, Fire Protection Law and other regulations, for learning reference only",
        "📚 Deep dive: Work Safety Knowledge Online Self-Test Question Bank",
        "Randomly draw 10 safety questions (fire, electricity, first aid, occupational health and more) for a self-test, score them instantly and give the correct answers.",
        "Review wrong answers to consolidate weak knowledge points, for pre-job training and daily revision.",
        "Questions are drawn randomly in pure front-end with a different combination each time.",
        "Question drawing and scoring",
        "Draw 10 random non-repeating questions from the bank, single choice each; after submission compare against standard answers to score, where score = correct answers ×10 (out of 100), and list the wrong answers with explanations.",
        "Of 10 randomly drawn questions you answer 8 correctly, scoring 80; the wrong answers concentrate on \"fire extinguisher selection\" and \"electric shock first aid\", so reviewing the explanations and retesting targets the improvement.",
        "Can the self-test replace certification training?",
        "No. The self-test is for consolidating memory; special operations and first aid still require formal training and certified qualification.",
        "Will questions repeat?",
        "Each round draws 10 random non-repeating questions from the bank, and with a large bank the overlap between two adjacent rounds is low; repeat practice to cover all knowledge points.",
        "About \"Work Safety Knowledge Online Self-Test Question Bank\"",
        "An online work safety knowledge self-test tool with a built-in multi-domain question bank covering fire safety, electrical safety, chemical safety, building construction, special equipment, occupational health, emergency response and more. It randomly draws 10 questions, scores automatically and provides detailed explanations.",
        "10 random questions each round to avoid repetition",
        "Covers 7 major safety domains",
        "Automatic scoring and rating (100 full marks, 80 pass)",
        "Per-question explanations with correct answers marked",
        "Tiered safety education assessment for new employees",
        "Safety Production Month knowledge contest practice",
        "Special operations personnel renewal exam prep",
        "Daily safety knowledge self-study",
    ]))
    write('safety-quiz', build('safety-quiz', [
        "📝 Safety Knowledge Self-Test",
        "Instant feedback after each answer, 15 questions in total, covering fire, electrical, protection and hazardous chemicals",
        "📖 Read the Safety Knowledge Self-Test user guide",
        "Question 1 / 15",
        "Current score:",
        "📊 Test Results",
        "View wrong answers",
        "📚 Deep dive: Safety Knowledge Self-Test",
        "15 random safety common sense questions covering fire, electricity, traffic, first aid and occupational health.",
        "Scores on submission and shows correct answers to help you find gaps.",
        "Suitable for team safety activities and new-hire baseline checks.",
        "Self-test and scoring",
        "Randomly draw 15 single-choice questions, compare answers on submission, score = correct answers ÷ 15 × 100; review the wrong answer bank to consolidate, and retake as many times as needed.",
        "Answering 12 of 15 questions correctly scores 80; the wrong answers are mostly about \"looking up the chemical MSDS\" and \"fire extinguisher steps\", and after targeted study the retest score rises to 93.",
        "Which domains do the questions cover?",
        "Fire four-understands four-can-do, electrical safety, work at height, confined spaces, first aid basics (CPR and bleeding control), occupational disease protection and more; the question bank is authoritative.",
        "Does 80 count as a pass?",
        "The self-test has no mandatory cutoff, but critical safety positions usually require higher mastery; aim to clear all wrong answers and retest weak areas repeatedly.",
        "About \"Safety Knowledge Self-Test\"",
        "A built-in safety knowledge question bank with random question drawing, instant scoring and explanations, plus wrong-answer review, suitable for safety training and self-assessment.",
        "Random question drawing from the bank",
        "Instant scoring and explanations",
        "Wrong-answer review",
        "Grade assessment",
        "Tiered safety education",
        "Pre-shift safety study",
        "Safety Month activities",
    ]))
    write('haxijisuan', build('haxijisuan', [
        "#️⃣ Hash Calculation",
        "Compute MD5 / SHA-1 / SHA-256 hashes of text",
        "File Hash Verification (MD5/SHA-1, existing)",
        "/ File Hash Verification (MD5/SHA-1, existing)",
        "📖 Read the Hash Calculation user guide",
        "Hashing maps input of any length to a fixed-length digest: MD5 outputs 128 bits (32 hex characters), SHA-1 outputs 160 bits (40 hex characters), SHA-256 outputs 256 bits (64 hex characters); the digest is constant for the same input and a tiny change produces an avalanche effect (about half the bits flip); it suits integrity and consistency verification, but MD5 and SHA-1 already have collision risks, so security scenarios should use SHA-256 or above.",
        "📚 Deep dive: Hash Calculation",
        "Compute",
        "/SHA-1/SHA-256 digests of text or files, for integrity verification and deduplication comparison.",
        "After downloading a file, compare against the",
        "published by the official site to confirm it was not tampered with.",
        "Computation is local and offline, suitable for quick consistency verification.",
        "How hashing works",
        "Hashing maps input of any length to a fixed-length digest, is one-way and irreversible, and a tiny input change produces a very different output (avalanche effect). MD5 outputs 128 bits (no longer recommended for security), SHA-1 outputs 160 bits (weakened), SHA-256 outputs 256 bits (currently recommended).",
        "The MD5 of the text hello is = 5d41402abc4b2a76b9719d911017c592 and its SHA-256 = 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824; changing one character to hellp makes both hashes completely different, showing the avalanche effect.",
        "What is the difference between hashing and encryption?",
        "Hashing is one-way and irreversible, used for verification; encryption is reversible and used for confidentiality. Use hash comparison to verify files and encryption to protect content.",
        "Why not use MD5 for security verification?",
        "Collision attacks have been found for MD5/SHA-1, so different files can be constructed with the same hash; use SHA-256 or stronger in security scenarios.",
        "Hash computation completes locally in the browser",
        "MD5/SHA-1 are no longer recommended for security scenarios",
        "SHA-256 suits verification and digital signatures",
    ]))
    write('analysis-3', build('analysis-3', [
        "📜 Security Log Analyzer (Local Log Import)",
        "Import logs locally",
        "📖 Read the Security Log Analyzer (Local Log Import) user guide",
        "Security log analysis: parse \"IP event type\" logs line by line, aggregate counts by event type and IP, and flag suspected attack or anomaly sources where the same IP shows the same event above a frequency threshold. All parsing is local with nothing uploaded.",
        "Log lines (one event per line, format: IP event type, separated by spaces)",
        "High-frequency threshold (the same IP + event reaching this count is treated as suspicious)",
        "Analyze log",
        "📚 Deep dive: Security Log Analyzer (Local Log Import)",
        "Server and firewall log triage: paste \"IP event type\" line by line, aggregate counts by event type and source IP, and quickly identify high-frequency attack sources.",
        "Brute force preliminary screening: set a threshold (such as ≥10 failed logins from the same IP within 5 minutes) to automatically flag suspicious sources for blocking or hardening checks.",
        "Worked example (5 log lines, threshold=3)",
        "The log contains 203.0.113.7 ssh_fail ×4 and 192.168.1.5 login_fail ×1; aggregated by type ssh_fail=4, login_fail=1; counting by IP + event, 203.0.113.7/ssh_fail reaches 4 times ≥ threshold 3 and is judged a suspicious high-frequency source. All parsing is local with no data uploaded.",
        "Can log analysis discover every attack?",
        "It can only find anomalies that leave traces in the log; low-frequency, low-speed or tunneled attacks are easily missed, so pair it with IDS/IPS and behavior baselines. This tool is positioned as a local quick-aggregation pre-screen, not real-time intrusion detection.",
        "Will large logs lag?",
        "Parsing is line-streamed with aggregated counts and low memory use; filter by time window or type before counting, and very large data can be imported in batches.",
        "About \"Security Log Analyzer (Local Log Import)\"",
        "Security log analyzer (local log import). Free online tool, pure front-end processing, data is not uploaded, privacy and security protected.",
        "e.g.\n192.168.1.10 login_fail\n203.0.113.7 ssh_fail",
    ]))
    write('generator-21', build('generator-21', [
        "🚑 First Aid Kit Item List (Generated by Scenario)",
        "Generated by scenario",
        "📖 Read the First Aid Kit Item List (Generated by Scenario) user guide",
        "First aid kits are configured by scenario: a base group (disinfecting wipes, band-aids, gauze, bandages, medical tape, scissors, tweezers, a thermometer and common medicines) plus a scenario group (travel adds motion sickness medicine and insect repellent, home adds burn ointment and fever patches, outdoor adds a tourniquet, triangular bandage, emergency blanket and whistle); item count = base group + scenario group, and medicines should be checked and replaced every 6 to 12 months.",
        "📚 Deep dive: First Aid Kit Item List (Generated by Scenario)",
        "Quickly list the first aid items to stock for travel, home or outdoor scenarios, as disaster preparedness reference.",
        "Check item by item whether band-aids, sterile gauze, povidone iodine and tourniquets are stocked, and fill in the missing ones.",
        "Export the list for organizing household, vehicle or team emergency kits. Generated purely in the browser with no network access.",
        "Common items and their uses",
        "Band-aids (cuts and abrasions), sterile gauze + medical tape (dressing larger wounds), povidone iodine swabs (wound disinfection), saline (irrigating wounds/eyes), elastic bandages (compression for sprains), disposable gloves (avoiding cross infection), scissors (cutting bandages/clothing), thermometer, tourniquet (major limb bleeding, note the time of application), burn ointment, antihistamine, flashlight, emergency blanket (preventing hypothermia).",
        "Selecting the \"outdoor\" scenario generates 10 items prioritizing the tourniquet, emergency blanket and flashlight; the home scenario focuses on band-aids, gauze, povidone iodine and burn ointment; the travel scenario recommends adding a thermometer and antihistamine, scaled by the number of people and days.",
        "Can the list replace professional first aid guidance?",
        "No. The list only helps stock items; for injury treatment follow professional first aid procedures or seek medical care, and devices such as tourniquets require training.",
        "How often should medicines be checked?",
        "Check expiry dates and integrity every 3–6 months and replace anything expired or damp immediately; consumables such as emergency blankets and bandages also need periodic replenishment.",
        "About \"First Aid Kit Item List (Generated by Scenario)\"",
        "First aid kit item list (generated by scenario). Free online tool, pure front-end processing, data is not uploaded, privacy and security protected.",
    ]))
    write('generator-hazard', build('generator-hazard', [
        "✨ Hazard Inspection Checklist Generation and Closed-Loop",
        "Hazard inspection checklist generation and closed-loop online tool",
        "📖 Read the Hazard Inspection Checklist Generation and Closed-Loop user guide",
        "Hazard inspection is generated structurally by industry and scenario: inspection item coverage = generated items ÷ total standard inspection items for that industry × 100%; risk level is rated by likelihood (1 to 5) × consequence severity (1 to 5), with risk value 15 or above major, 10 to 14 larger, 5 to 9 moderate and below 5 low; hazard closed-loop rate = rectified items ÷ identified hazards × 100%.",
        "📚 Deep dive: Hazard Inspection Checklist Generation and Closed-Loop",
        "Generate by work type (electricity, fire, working at height, confined space, etc.)",
        "hazard inspection checklist",
        ", inspect item by item and mark the risk level.",
        "Rate identified hazards as high / medium / low, formulate corrective measures, owners and deadlines, and form closed-loop tracking.",
        "Closed-loop rate = rectified count ÷ total hazards, used for safety performance assessment.",
        "Risk grading and closed loop",
        "Risk level is rated by likelihood × consequence: high (stop work and rectify immediately), medium (rectify within a deadline), low (include in routine monitoring). Closed-loop rate = rectified and closed hazards ÷ total hazards ×100%; overdue items count as not closed and are escalated.",
        "A workshop identifies 12 hazards, of which 2 are high, 5 medium and 5 low; 9 have been rectified and closed (high 2, medium 4, low 3), so the closed-loop rate = 9/12 = 75%; the remaining 3 (medium 1, low 2) are overdue and must be escalated for supervision.",
        "What is the relationship between hazards and accidents?",
        "A hazard is an unsafe state or behavior that can lead to an accident, and rectifying hazards is the prerequisite for preventing accidents; a low closed-loop rate means weak management and rising accident risk.",
        "Must high-risk hazards stop work?",
        "High risks (such as electric leakage or flammable gas leaks) should immediately take the relevant area out of service until rectified and accepted; working with a known hazard is not allowed.",
        "About \"Hazard Inspection Checklist Generation and Closed-Loop\"",
        "Hazard inspection checklist generation and closed loop. Free online tool, pure front-end processing, data is not uploaded, privacy and security protected.",
    ]))
    write('random-13', build('random-13', [
        "🎲 Anti-Fraud Knowledge Cards (Random Display)",
        "Random display",
        "📖 Read the Anti-Fraud Knowledge Cards (Random Display) user guide",
        "Anti-fraud cards are displayed by type: common methods include order-brushing rebates, fake customer service refunds, bogus loans, impersonation of police or prosecutors, and romance pig-butchering scams; each card has identification points (such as being asked to transfer to a safe account or asking for SMS verification codes) and prevention steps (do not click unknown links, do not reveal verification codes, call 96110 for advice); when the self-test accuracy is below 80%, it suggests strengthening study and focusing on error-prone types.",
        "📚 Deep dive: Anti-Fraud Knowledge Cards (Random Display)",
        "Randomly display 10 highly frequent telecom and online fraud methods such as order-brushing rebates, impersonation of police or prosecutors and bogus investments, together with prevention points, for education and training.",
        "Compare against \"common patterns\" to identify suspected scams around you, and take actions from \"prevention points\" such as no upfront payment, no screen sharing and no clicking unknown links.",
        "Draw cards at random during team morning meetings or community outreach to reinforce memory.",
        "Frequent methods and prevention",
        "Order-brushing rebates (advance payment then large continuous orders → do not pay upfront), impersonation of police or prosecutors (phone investigation demanding transfer to a \"safe account\" → police and prosecutors have no safe account), bogus investments (high return zero risk inducing deposits → use official channels), fake customer service refunds (inducing screen sharing → operate on the official platform), pig-butchering romance scams (be alert as soon as money is requested → do not transfer or invest), bogus loans (any upfront fee is fraud → legitimate loans charge nothing upfront).",
        "If you draw the \"phishing link\" card: the pattern is fake bank SMS luring you into entering account and password, and the prevention point is do not click unknown links,",
        "verification codes",
        "and never give them to anyone; if you draw \"impersonated acquaintance asking to borrow money\": the pattern is a stolen photo claiming an emergency, and the prevention point is to verify identity by phone or video before transferring.",
        "Can card content be used as evidence when reporting a crime?",
        "The cards are educational reminders and cannot replace evidence; if you are defrauded, keep chat and transfer records and call the 96110 anti-fraud hotline.",
        "Why emphasize \"no screen sharing\"?",
        "Screen sharing exposes SMS verification codes and bank app interfaces, letting scammers transfer funds directly; customer service refunds never require screen sharing.",
        "About \"Anti-Fraud Knowledge Cards (Random Display)\"",
        "Anti-fraud knowledge cards (random display). Free online tool, pure front-end processing, data is not uploaded, privacy and security protected.",
    ]))

if __name__ == '__main__':
    main()