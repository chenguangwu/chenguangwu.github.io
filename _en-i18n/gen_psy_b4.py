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
    write('bubble-tea-personality-quiz', build('bubble-tea-personality-quiz', [
        "🎮 Which Milk Tea Are You",
        "12 situational multiple-choice questions spanning four hidden dimensions of sweetness, strength, ice level and toppings, matching you with the cup that fits you best and generating a shareable result card.",
        "Which Milk Tea Are You",
        "/ Which Milk Tea Are You",
        "💭 Psychology and personality",
        "📖 Read the \"Which Milk Tea Are You usage guide\"",
        "💡 This quiz has 12 questions. Just pick the option closest to you for each one; it takes about 2 minutes.",
        "The result of this quiz is a self-test reference and does not replace professional psychological or medical diagnosis.",
        "Start the quiz →",
        "Question 1 / 12",
        "← Previous question",
        "📊 Your four-dimension profile",
        "📋 Copy the text",
        "🔗 Share the result",
        "🖼️ Export card PNG",
        "🔄 Take it again",
        "Clear my quiz records",
        "⚠️ This quiz is for entertainment and self-exploration only,",
        "the result is a self-test reference and does not replace professional psychological or medical diagnosis",
        ". Milk tea is nice but do not drink too much; if you have persistent emotional or psychological distress, consider seeking professional help.",
        "📚 Deep dive: Milk Tea Personality Fun Quiz",
        "Social icebreaker: play it at a gathering with friends and see what milk tea personality each person gets — the conversation opens up on its own.",
        "Fun for yourself: pick toppings and sweetness by instinct and get a light, fun \"personality label\" just for laughs.",
        "Content sharing: post the result image to your social feed or platform as a low-threshold way to express yourself.",
        "How the result is produced",
        "The test maps the preference behind each of your options (sweetness, ice level, main topping, topping style) onto a few personality archetypes. For example \"full sugar, no ice\" stands for warm and direct, while \"less sugar with coconut jelly\" stands for delicate and cautious. It reflects the style of your choices, not a rigorous psychological measurement.",
        "Is this test result accurate?",
        "It is an entertainment quiz, not a scientific scale. Treat the result as light-hearted self-mockery, do not take it seriously, and do not use it to label other people.",
        "How many results are there?",
        "A typical design maps to a number of personality archetypes (such as the passionate type, the rational type, the spontaneous type and so on); the page shows the specifics. Different combinations of choices land on different archetypes.",
        "Can I share it with friends to play together?",
        "Of course. These fun quizzes are best done as a group with everyone showing off their results. It runs entirely in the front end and locally, and collects no data at all.",
    ]))

    write('holland-career-test', build('holland-career-test', [
        "📝 Holland Career Interest Test (RIASEC)",
        "John Holland's career interest theory groups personality and work environment into six types: Realistic R, Investigative I, Artistic A, Social S, Enterprising E and Conventional C. This assessment has 60 items (10 per type) answered on a 3-level scale of \"like / unsure / dislike\", producing your three-letter Holland Code and a hexagonal interest profile, then matching the best-fitting top 10 occupations and university majors from a library of 120+ real occupations using cosine similarity. All computation happens locally in your browser and no data is uploaded.",
        "Holland Career Interest Test (RIASEC)",
        "/ Holland Career Interest Test (RIASEC)",
        "📖 Read the \"Holland Career Interest Test (RIASEC) usage guide\"",
        "Item scoring: like = 2 points, unsure = 1 point, dislike = 0 points; 10 items per type for a raw score of 0-20. Holland Code = the three highest raw-score types in descending order (the first is the \"dominant type\"). The hexagonal profile is drawn radially by each type's share of the total score. Career matching: your six dimension scores are normalized (÷20) into a user vector U; each occupation's three-letter code is mapped onto a six-dimension vector V with positional weights [1.0, 0.7, 0.5]; similarity = cos(U, V) = Σ(Uᵢ·Vᵢ) ÷ (‖U‖·‖V‖), and the top 10 are taken. Consistency is judged by the adjacency of the first two letters on the hexagon, and differentiation by the gap between the highest and lowest scores.",
        "🎯 Your Holland Code",
        "📊 Hexagonal interest profile",
        "📈 Scores of the six types (raw score 0-20)",
        "🔍 Consistency and differentiation",
        "💼 Best-fit occupations Top 10 (ranked by cosine similarity)",
        "🎓 University major suggestions (12 categories)",
        "Copy Holland Code",
        "Copy the text report",
        "Export report JSON",
        "⚠ Assessment disclaimer:",
        "The result of this assessment is a self-test reference and does not replace professional psychological or medical diagnosis. Career interest is only one dimension of career choice; judge it together with your own ability, values, academic background and the job market. If you remain persistently unsure about your career choice, consider consulting your school's career center or a certified career counselor.",
        "Filling tips:",
        "Answer with your first instinct and do not agonize over which option \"looks better\". There is no better or worse among the six types, only a difference in where your scores sit. After all 60 questions, click \"View result\".",
        "📚 Deep dive: Holland Career Interest Test (RIASEC)",
        "Choosing a major or application direction: the six dimension scores give you a ranking, so compare them against the work environments that match your interest structure.",
        "Career transition: retest a few years into work, watch whether your interests have drifted, and judge which direction to adjust toward.",
        "Career guidance: use the occupation groups tied to your high-scoring dimensions as the focus of your applications and research, so you stop applying blindly everywhere.",
        "How to read the RIASEC six-type scores",
        "Holland divides career interest into six types: Realistic R, Investigative I, Artistic A, Social S, Enterprising E and Conventional C. Your highest-scoring type represents the work environment you are most comfortable in. Adjacent types (such as R-I, A-S) have high congruence, and opposite types (such as R-S, I-E) have low congruence. Looking at the high-scoring combination of your top two letters (such as SEC or IRA) locates your suitable occupational field far better than looking at the single highest score.",
        "What do the six RIASEC letters stand for?",
        "R Realistic (hands-on operation, machinery and nature), I Investigative (analytical thinking, exploration), A Artistic (creative expression), S Social (helping and teaching people), E Enterprising (persuading and leading), C Conventional (order and rules, data handling). The six dimensions combined describe a person's career interest profile.",
        "Does a high score mean I must do that occupation?",
        "Not necessarily. Interest is only one dimension of career choice and has to be combined with ability, values and real opportunities. A high dimension suggests you are more likely to find satisfaction in that kind of environment — a reference, not a command.",
        "Is the result suitable for hiring screening?",
        "Not on its own. Interest assessments suit self-exploration and career planning, while hiring decisions should combine ability, experience and job requirements, so that people are not constrained by an interest label.",
    ]))

    write('enneagram-test', build('enneagram-test', [
        "💭 Enneagram Personality Test (144 items)",
        "Each group has two descriptions; pick the one closer to you. It reveals your dominant type, wing, tri-center and the dynamic shift under stress versus security, and draws a nine-pointed star chart.",
        "Enneagram Personality Test",
        "/ Enneagram Personality Test",
        "💭 Psychology and personality",
        "📖 Read the \"Enneagram Personality Test usage guide\"",
        "💡 This test has 144 forced-choice pairs and takes about 10-15 minutes. There is no right or wrong in each item; just go with your instinct and pick the statement closer to you.",
        "The result of this quiz is a self-test reference and does not replace professional psychological or medical diagnosis.",
        "Start the test →",
        "Group 1 / 144",
        "Group 1",
        "← Previous group",
        "📊 Enneagram score distribution",
        "🖼️ Export result card PNG",
        "🔄 Take it again",
        "⚠️ The Enneagram is a personality classification model in popular psychology,",
        "the result is a self-test reference and does not replace professional psychological or medical diagnosis",
        ". It describes motivation and focus rather than level of ability, and every type has room to grow. If you are experiencing persistent emotional distress, please seek professional psychological or medical help.",
        "📚 Deep dive: Enneagram Personality Test",
        "Self-exploration: answer with your first instinct to find the type you are closest to, plus its wing and instinctual subtype.",
        "Understanding people: learn which types the people around you may be, and understand how their behaviour differs under stress versus security.",
        "Team and growth: use the Enneagram to look at your core motivation (fear and desire), which locates your growth block far better than behaviour alone.",
        "How to read the Enneagram: dominant type plus wing",
        "The Enneagram splits personality into nine types: 1 Reformer, 2 Helper, 3 Achiever, 4 Individualist, 5 Investigator, 6 Loyalist, 7 Enthusiast, 8 Challenger and 9 Peacemaker. Most people lean toward two adjacent types at once, so a type 4 that leans more toward 3 or 5 is called 4w3 or 4w5 (w = wing). The dominant type locates your core motivation, while the wing explains style differences — a fuller picture than one number alone.",
        "What are the nine types of the Enneagram?",
        "In order: 1 Reformer (perfection), 2 Helper (altruism), 3 Achiever (efficacy), 4 Individualist (uniqueness), 5 Investigator (insight), 6 Loyalist (security), 7 Enthusiast (joy), 8 Challenger (power), 9 Peacemaker (harmony). Behind each type lies a specific core fear and core desire.",
        "What does a wing mean?",
        "Nobody is purely one type; you usually lean toward one of the two adjacent types, forming a combination such as 4w3 or 9w1, which is called a wing. The wing shapes how you express your dominant type, so two people of the same dominant type can differ noticeably.",
        "Can the Enneagram be used for hiring or psychological diagnosis?",
        "Not recommended. The Enneagram is a framework for self-awareness and growth, not an ability assessment, and it does not replace clinical diagnosis. Using it for hiring screening is unscientific and carries compliance risk.",
    ]))

    write('attachment-style-test', build('attachment-style-test', [
        "📝 Adult Attachment Style Test (ECR)",
        "Adult attachment describes the pattern of emotional bonding an individual forms in intimate relationships. The ECR (Experiences in Close Relationships) scale characterizes it along two orthogonal dimensions: anxiety (worrying about being abandoned, craving intense closeness) and avoidance (feeling uncomfortable with closeness, emphasizing independence). This assessment has 36 items (18 each, including 8 reverse-scored items) on a 1-7 point scale, and finally places your attachment style on a two-dimensional scatter plot: secure / preoccupied / dismissing / fearful, together with typical manifestations and growth directions. All computation happens locally in your browser and no data is uploaded.",
        "Adult Attachment Style Test (ECR)",
        "/ Adult Attachment Style Test (ECR)",
        "📖 Read the \"Adult Attachment Style Test (ECR) usage guide\"",
        "📐 Scoring and placement algorithm",
        "Each item is scored 1 (strongly disagree) to 7 (strongly agree); items marked \"reverse\" are converted as 8 - raw score. The anxiety score is the mean of the 18 anxiety items (1-7) and the avoidance score is the mean of the 18 avoidance items (1-7). A scatter plot is drawn with avoidance on the horizontal axis (low on the left, high on the right) and anxiety on the vertical axis (low at the bottom, high at the top), and the midpoint 4.0 divides it into four quadrants: low anxiety + low avoidance = secure, high anxiety + low avoidance = preoccupied, low anxiety + high avoidance = dismissing, high anxiety + high avoidance = fearful. Norm reference bands: anxiety/avoidance means below 3.0 count as low, 3.0-4.5 as moderate, above 4.5 as high (not a clinical diagnostic standard, for self-reference only).",
        "🎯 Your attachment style",
        "📍 Two-dimensional attachment map",
        "📊 Two-dimension scores with norm reference",
        "Copy the style conclusion",
        "Copy the text report",
        "Export report JSON",
        "⚠ Assessment disclaimer:",
        "The result of this assessment is a self-test reference and does not replace professional psychological or medical diagnosis. Attachment style is a relatively stable pattern that can still change through experience and awareness, and it is not a lifelong label. If persistent anxiety, depression or trauma responses appear in connection with relationship distress, consider seeking professional help from a certified counselor or psychiatrist.",
        "Filling tips:",
        "Use a stable intimate relationship (or the intimate relationship pattern you know best) as your reference and answer with your genuine feelings; even without a partner you can answer based on \"your typical state in a relationship\". After all 36 questions, click \"View result\".",
        "📚 Deep dive: Adult Attachment Style Test (ECR)",
        "Self-awareness: recall a recent intimate relationship, answer with your genuine feelings, and see where you sit on the two dimensions of \"anxiety\" (fear of abandonment) and \"avoidance\" (fear of getting too close).",
        "Communication with your partner: share the result and compare each side's high/low combination on \"anxiety / avoidance\" to explain why some conflicts have one person chasing and the other fleeing.",
        "Relationship review: look back at conflict patterns that keep repeating (such as one partner constantly seeking reassurance while the other feels trapped) and use the attachment dimensions to understand the difference in underlying security.",
        "Retest comparison: test once during a stable period and once during a high-pressure period, and see whether the avoidance score fluctuates with stress, so you do not mistake a temporary state for a fixed type.",
        "How to read the anxiety and avoidance scores",
        "ECR measures two independent dimensions: a high anxiety score means worrying about abandonment and craving excessive reassurance; a high avoidance score means discomfort with excessive closeness and a tendency to keep distance. The two dimensions cross to form four typical combinations: low anxiety + low avoidance = secure; high anxiety + low avoidance = preoccupied (clingy); low anxiety + high avoidance = dismissive (distant); both high = fearful (want it but afraid of being hurt). Do not look only at a total score; the two dimensions must be read separately.",
        "How are the ECR items scored?",
        "The standard ECR has 36 items, 18 measuring anxiety and 18 measuring avoidance, each scored 1-7. About half are reverse-scored items (for example \"I am not too worried about getting too close to others\"), where answering \"strongly agree\" records a low score, so the scoring has to be flipped first. Finally the mean of each dimension is taken, and a higher mean means that dimension is stronger.",
        "Does the result tell me what kind of person I am?",
        "It only shows your attachment tendency in intimate relationships, not a personality label. The same person can score differently with different partners and at different life stages; it helps you understand relationship patterns rather than define you.",
        "Can it be used for psychological diagnosis?",
        "No. ECR is a self-rating screening tool and does not replace clinical diagnosis. If relationship distress seriously affects your life, consider professional psychological counseling rather than judging yourself by the scale alone.",
    ]))

if __name__ == '__main__':
    main()
