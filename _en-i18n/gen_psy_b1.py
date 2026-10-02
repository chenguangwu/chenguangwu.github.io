#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'psychology')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'psychology')
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
    out = {'slug': slug, 'industry': 'psychology', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('tester-3', build('tester-3', [
        "📖 Learning Style Test (VARK)",
        "The VARK learning style test uses 12 scenario questions to assess your learning preference: Visual (V), Auditory (A), Read/Write (R) and Kinesthetic (K), helping you find the way of learning that suits you best.",
        "VARK learning style",
        "Question 1 / 12",
        "Loading...",
        "← Previous question",
        "Pick the option closest to you for each question; you can also use keys 1-4 / ← →",
        "Question number overview (click any number to go back and change that answer)",
        "⚠️ Before you start",
        "The 4 options of each question correspond to one learning style: Visual (V) / Auditory (A) / Read/Write (R) / Kinesthetic (K). Choose the one closest to you",
        "There are no right answers; go with your first instinct and pick the most natural option",
        "Most people are a \"mixed type\" — the result shows the share of all four styles plus your dominant style",
        "Your progress is stored only in this local browser. Click \"Restart test\" to clear it; no data is uploaded",
        "Restart test",
        "VARK is a learning style classification model proposed by Neil Fleming",
        "Most people have a mixed learning style; purely single-type profiles are rare",
        "Understanding your learning style helps you pick efficient study strategies",
        "VARK does not limit ability; it only describes different preferences",
        "📚 Deep dive: Learning Style Test (VARK)",
        "Study planning: when preparing for an exam or learning a new skill, first work out whether you lean Visual (V), Auditory (A), Read/Write (R) or Kinesthetic (K), then shape your notes and exercises around the dominant style.",
        "Teaching and training fit: teachers and trainers can adapt delivery accordingly, for example giving kinesthetic learners more hands-on practice and read/write learners more text material.",
        "Teamwork: in cross-department projects, knowing how members prefer to take information in reduces the \"I told them but they did not remember\" communication loss.",
        "What each of the four types means",
        "V Visual (diagrams, slides), A Auditory (listening, discussion), R Read/Write (text, checklists), K Kinesthetic (experience, practice). Most people are a \"mixed type\"; this test lists your dominant and secondary types by score from high to low.",
        "What are the four VARK types?",
        "V = Visual, A = Auditory, R = Read/Write, K = Kinesthetic. They describe the way you find it easier to receive and remember information, not how smart you are.",
        "What if two styles tie as dominant?",
        "That is very common. The result lists both, for example a \"VA type\" means you are most efficient when combining listening and seeing, so you can pair the two learning styles.",
        "Do learning styles change?",
        "Styles are relatively stable, but deliberately practising other channels helps too. Treat this as a reference for optimizing study, not a fixed label.",
        "About \"Learning Style Test (VARK)\"",
        "The VARK learning style test assesses your learning preference through 12 scenario questions: Visual (looking at charts and video), Auditory (listening to explanations and discussion), Read/Write (reading and writing) and Kinesthetic (hands-on practice), helping you find the way of learning that fits you best.",
        "12 scenario-based questions",
        "Analysis of 4 learning styles",
        "Mixed-type style detection",
        "Personalized study advice",
        "Learning style self-assessment",
        "Study method optimization",
        "Reference for education and training",
        "Guidance for teaching to individual strengths",
        "How to use the Learning Style Test (VARK)",
        "Read each scenario and go with your first instinct, picking the option closest to you (Visual / Auditory / Read/Write / Kinesthetic).",
        "Use \"Previous / Next question\" or the keys 1-4 and ← → to move around; click a question number to go back and change it.",
        "After all 12 questions the result appears automatically, and you can also click \"View result\" at any time.",
        "The result section shows the share of each of the four styles, your dominant style and matching study strategies, and can be copied or saved.",
        "How scoring works",
        "The 4 options of each question map to V (Visual) / A (Auditory) / R (Read/Write) / K (Kinesthetic)",
        "Choosing an option gives that style 1 point; with 12 questions each style scores 0-12",
        "The highest score is your dominant style; a tie for highest means a \"multi-dominant mixed type\"",
        "Share = score of a style ÷ total answered questions × 100%",
        "Learning style self-assessment, study method optimization, and reference for education, training and teaching to individual strengths.",
        "What does the Learning Style Test (VARK) do?",
        "Through 12 scenario questions it assesses your preference and share across the four learning styles Visual (V), Auditory (A), Read/Write (R) and Kinesthetic (K), helping you find the most efficient way to learn.",
        "Are the results accurate?",
        "This tool computes everything in real time inside your local browser with no server involved. The result reflects your answer preferences and is a self-awareness reference only, not any kind of ability judgement.",
        "Who is VARK suitable for?",
        "Students, teachers, trainers and parents can all use it to optimize study strategies, lesson preparation and tutoring approaches.",
        "Nothing is required to sign in. All computation happens locally on your device, progress is kept only on this machine, and no data is uploaded to any server.",
    ]))

    write('tester-2', build('tester-2', [
        "💭 MBTI Personality Type Test",
        "A full MBTI (Myers-Briggs Type Indicator) test: 60 questions across 4 dimensions, 5 options per question (including neutral), answered one at a time with the ability to go back and change any answer, producing a 16-type result plus the tendency percentage of each dimension.",
        "MBTI personality type test",
        "/ MBTI personality type test",
        "📖 Read the \"MBTI vocational personality test usage guide\"",
        "MBTI distinguishes 16 personality types with 4 preference pairs: E/I for energy source, S/N for how information is gathered, T/F for basis of decision making, and J/P for lifestyle structure. This tool has 60 questions in total, 15 per dimension (with items in both directions to avoid agreement bias), scored on a 5-point scale: strongly agree ±2, somewhat agree ±1, neutral 0, somewhat disagree ∓1, strongly disagree ∓2. Within a dimension the signed values are summed and then converted into a 0-100% tendency share where both sides always add up to 100%. Neutral counts as 0, meaning that dimension contributes no tendency — when unsure pick neutral, which is closer to the truth than forcing a binary choice. Everything is computed in the browser and no answer is uploaded.",
        "Extraversion / Introversion",
        "Question 1 / 60",
        "Loading...",
        "← Previous question",
        "Click the option text to answer; you can also use keys 1-5 / ← →",
        "Question number overview (click any number to go back and change that answer)",
        "⚠️ Before you start",
        "MBTI describes preferences, not ability, and it is not a psychological diagnostic tool",
        "The 60 questions are arranged as 15 per dimension across 4 dimensions, including reverse-scored items to avoid the bias of simply agreeing",
        "Each question offers 5 options; when unsure choose \"Neutral / hard to say\", which is closer to reality than forcing a binary choice",
        "The closer the percentage is to 50%, the less clear that preference is; retaking the test in a different state may flip the letters",
        "Your progress is stored only in this local browser. Click \"Restart test\" to clear it; no data is uploaded",
        "Restart test",
        "📚 Deep dive: MBTI Personality Type Test",
        "Self-exploration: set aside 10 uninterrupted minutes and answer with your first reaction instead of scoring an \"ideal self\" — the test measures preference, not how capable you are.",
        "Career direction reference: once you have the 4 letters, focus on \"commonly matched directions\" and the \"cognitive function stack\", and compare them with the day-to-day work of your target role — far more useful than staring at the type name alone.",
        "Teamwork: let each member finish the test and then share results. Focus the discussion on T/F (logic first or feelings first) and J/P (plan first or adjust as you go) — these two pairs create the most collaboration friction.",
        "Retest comparison: test again in 3-6 months. If a dimension shifts from 70/30 to 45/55, that dimension was close to neutral to begin with, so do not treat a single result as a fixed label.",
        "What is the difference between 70% / 30% and 52% / 48%",
        "70/30 means the preference on that dimension is clear and the result is fairly stable; 52/48 means you are naturally balanced there, and switching context (work / life, high-pressure / relaxed) can easily flip the answer. When a dimension is near 50/50, do not force a letter on yourself — reading it as \"I can use both sides\" is more accurate.",
        "Are 60 questions too many? Can I do only part of it?",
        "You can, but each dimension is scored over 15 questions, so skipping items distorts the percentage. The page lets you jump straight to a question number, and closing it midway does not lose progress (it lives in this local browser) — reopening resumes from the first unanswered question.",
        "Why is there a \"Neutral / hard to say\" option?",
        "Many questions have no black-or-white answer, and forcing a binary choice pushes people who are near neutral randomly to one side. The neutral option scores 0, meaning that dimension contributes no tendency, which is closer to reality than guessing.",
        "Can the MBTI result be used for hiring screening or psychological diagnosis?",
        "Neither. MBTI measures preferences in how information is gathered and decisions are made; it does not reflect ability, performance or mental health. Using it for hiring screening is both inaccurate and a compliance risk. It suits self-awareness and understanding communication differences.",
        "This time the result differs from last time — is it inaccurate?",
        "First look at which dimension differs. If that dimension",
        "was already close to 50/50, a flip is normal fluctuation; if it flips sharply, think back to your state during the two attempts (student / professional, high-pressure / relaxed) — most people's expression does shift with their role.",
        "About \"MBTI Personality Type Test\"",
        "MBTI (Myers-Briggs Type Indicator) uses 4 preference pairs to describe how a person habitually draws energy, takes in information, makes decisions and structures life: E/I Extraversion vs Introversion, S/N Sensing vs Intuition, T/F Thinking vs Feeling, J/P Judging vs Perceiving. The four pairs combine two by two into 16 personality types. This tool is the full 60-question version with 5 options per question (including neutral), answered one at a time with the ability to go back and change any answer, giving a 4-letter type, the tendency percentage of each dimension, the cognitive function stack and development advice.",
        "A full 60-question bank, 15 per dimension across 4 dimensions, with reverse-scored items",
        "5-point answering scale with a \"Neutral / hard to say\" middle value",
        "One question at a time with a progress bar; click the text to select, no native radio buttons",
        "A 60-cell question number overview; click any number to jump back and change that answer",
        "Keys 1-5 to choose, ← → to page",
        "Outputs tendency percentage bars for the four dimensions plus a raw score table",
        "Full interpretation of all 16 types: core traits, strengths, blind spots, matched directions, cognitive function stack",
        "Progress saved locally, safe to close midway; one-click result copy",
        "Runs entirely in the browser, answers are never uploaded to a server",
        "Self-awareness and personality exploration",
        "Career planning and role fit reference",
        "Understanding communication and decision differences in a team",
        "A reference for how to get along in intimate relationships",
        "Introductory psychology teaching and team-building activities",
    ]))

if __name__ == '__main__':
    main()
