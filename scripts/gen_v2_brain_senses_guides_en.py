#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 19 篇 V2 脑科学/感官工具的【英文版使用指南】guides/<slug>-guide.en.html。

背景：站点指南当前 100% 中文，英文站（?lang=en）无英文指南，英文用户点进指南看到中文。
这是英文站最大的内容缺口。本生成器先交付一个低风险试点批次：
- 写出自包含的英文指南页（en-US 元数据 + 英文正文），可被英文搜索引擎独立收录；
- 中文指南页通过「🌐 English」芯片链到对应 .en.html（在 zh 指南渲染时注入，见下方 inject_en_link）；
- 暂不改动 _build.py / sitemap（避免 SEO 意外），待批量方案确认后再统一收录与 ?lang=en 切换。

复用与 gen_v2_brain_senses_guides.py 完全一致的 TPL 结构，仅语言与内容换为英文。
"""
import json, io, os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# slug -> 工具页相对路径（与 zh 指南一一对应）
TOOL_MAP = {
    'corsi-block-test': 'tools/cognition/corsi-block-test.html',
    'digit-span-test': 'tools/cognition/digit-span-test.html',
    'human-benchmark': 'tools/cognition/human-benchmark.html',
    'nback-training': 'tools/cognition/nback-training.html',
    'schulte-table': 'tools/cognition/schulte-table.html',
    'stroop-test': 'tools/cognition/stroop-test.html',
    'time-perception': 'tools/cognition/time-perception.html',
    'pure-tone-audiometry': 'tools/ent/pure-tone-audiometry.html',
    'temporal-resolution-hearing': 'tools/ent/temporal-resolution-hearing.html',
    '1a2b-guess': 'tools/fun/1a2b-guess.html',
    'daily-riddle': 'tools/fun/daily-riddle.html',
    'amsler-grid-test': 'tools/ophthalmology/amsler-grid-test.html',
    'astigmatism-chart': 'tools/ophthalmology/astigmatism-chart.html',
    'eye-chart-toolkit': 'tools/ophthalmology/eye-chart-toolkit.html',
    'vision-screening-21': 'tools/ophthalmology/vision-screening-21.html',
    'attachment-style-test': 'tools/psychology/attachment-style-test.html',
    'bubble-tea-personality-quiz': 'tools/psychology/bubble-tea-personality-quiz.html',
    'enneagram-test': 'tools/psychology/enneagram-test.html',
    'holland-career-test': 'tools/psychology/holland-career-test.html',
}

EN = [
 {'slug':'corsi-block-test','name':'Corsi Block-Tapping Test',
  'desc':'Corsi Block-Tapping Test guide: measure visual-spatial working memory span by replaying growing block sequences.',
  'intro':'The Corsi Block-Tapping Test assesses visual-spatial working memory. The system highlights a sequence of blocks; you tap them back in the same (forward) or reverse (backward) order. A staircase procedure adapts difficulty, and everything runs locally in your browser.',
  'features':['Forward and backward recall modes','Adaptive staircase difficulty','Visual-spatial span scoring','Product-score (sum of correct sequence lengths)','Age-norm reference (child ~4.8, adult ~5.5, elderly ~4.9)','100% client-side'],
  'scenarios':['Self-check of spatial memory','Clinical or research screening aid','Cognitive training and tracking'],
  'steps':['Pick a recall mode (forward/backward)','Watch the blocks light up in sequence','Tap the blocks back in order','Continue as length grows','Read your span and product score'],
  'tips':['Minimize distractions during the task','Backward span is harder and more sensitive','One low run is normal; trends matter','Use as a training tracker, not a diagnosis'],
  'faqs':[('Corsi vs digit span?','Corsi measures visual-spatial memory (location sequences); digit span measures verbal/phonological memory (number sequences).'),
          ('Is a low score a problem?','A single low run is usually not concerning; if it persists, consider a professional assessment.')]},

 {'slug':'digit-span-test','name':'Digit Span Test',
  'desc':'Digit Span Test guide: assess verbal working memory by recalling forward and backward digit sequences.',
  'intro':'The Digit Span Test measures verbal working memory. You listen to or read a sequence of digits and recall it forward or backward. It is a staple of cognitive assessment (e.g., WAIS).',
  'features':['Forward and backward recall','Adaptive length','Verbal working-memory span','Quick, no setup','100% client-side'],
  'scenarios':['Attention and memory self-check','Study or research screening','Warm-up before other tasks'],
  'steps':['Choose forward or backward','Read the digit sequence','Recall it in the requested order','Length increases as you succeed','See your span result'],
  'tips':['Say the digits quietly to yourself','Backward is more demanding','Avoid rushing','Track progress over time'],
  'faqs':[('What does backward span show?','Backward digit span loads executive control more heavily and is a sensitive attention/memory indicator.'),
          ('Normal digit span?','Typical forward span is about 7 ± 2 digits; backward is usually 1–2 shorter.')]},

 {'slug':'human-benchmark','name':'Human Benchmark',
  'desc':'Human Benchmark guide: a suite of reaction-time, memory and accuracy challenges to gauge cognitive performance.',
  'intro':'Human Benchmark bundles quick challenges — reaction time, memory, verbal fluency and accuracy — so you can compare your performance against yourself and rough population averages.',
  'features':['Reaction-time test','Memory and sequence challenges','Accuracy tasks','Self-comparison over time','100% client-side'],
  'scenarios':['Casual cognitive warm-up','Tracking reaction time','Fun self-experiment'],
  'steps':['Pick a challenge','Follow the on-screen prompt','Respond as fast and accurately as you can','Review your stats','Retest to compare'],
  'tips':['Use a wired connection for reaction tests','Fatigue lowers scores','Do a few practice rounds','Compare trends, not single runs'],
  'faqs':[('Are scores comparable to others?','They are self-referential; population numbers are rough averages, not a diagnosis.'),
          ('Why does reaction time vary?','Sleep, device input lag and attention all shift reaction time significantly.')]},

 {'slug':'nback-training','name':'N-Back Training',
  'desc':'N-Back working memory training: spot when the current stimulus matches the one N steps back.',
  'intro':'N-Back is a classic working-memory trainer. A stimulus (letter, position, sound) appears each round; press when it matches the one shown N steps earlier. Increasing N raises the load.',
  'features':['Adjustable N (1-back to dual n-back)','Visual and audio stimuli','Adaptive difficulty','Session scoring','100% client-side'],
  'scenarios':['Working-memory training','Research paradigms','Attention drills'],
  'steps':['Set your N level','Watch/listen to each stimulus','Respond when it matches N-back','Keep going through the block','Check accuracy and load'],
  'tips':['Start at 1–2 back','Dual n-back adds audio','Short daily sessions beat marathons','Track accuracy, not just N'],
  'faqs':[('Does n-back transfer to IQ?','Evidence is mixed; it reliably trains the task itself and may help related memory skills.'),
          ('What is dual n-back?','You track both a visual and an audio stream simultaneously, matching each N steps back.')]},

 {'slug':'schulte-table','name':'Schulte Table',
  'desc':'Schulte Table guide: an attention and processing-speed trainer — find numbers or symbols in order, fast.',
  'intro':'The Schulte Table is a grid of numbers (or symbols) you must find in ascending order as quickly as possible. It is widely used to train and measure selective attention and processing speed.',
  'features':['Configurable grid size','Numbers or symbols','Time and error tracking','Attention training','100% client-side'],
  'scenarios':['Attention training','Sports or driving focus drills','Quick mental warm-up'],
  'steps':['Open the table','Find 1, then 2, 3… in order','Tap each as fast as possible','Finish the grid','Review your time'],
  'tips':['Keep your gaze central, use peripheral vision','Avoid subvocal counting','Practice daily in short sets','Compare times, not single runs'],
  'faqs':[('What does a fast Schulte time mean?','It loosely reflects selective attention and visual search speed, not intelligence per se.'),
          ('Why peripheral vision?','Training central fixation with peripheral search is the classic Schulte method.')]},

 {'slug':'stroop-test','name':'Stroop Test',
  'desc':'Stroop Effect Test guide: measure selective attention and interference by naming ink colors of color words.',
  'intro':'The Stroop Test presents color words printed in conflicting ink colors (e.g., the word RED in blue). Naming the ink color — not reading the word — reveals the cognitive interference between reading and color naming.',
  'features':['Congruent and incongruent trials','Reaction-time measurement','Interference scoring','Attention assessment','100% client-side'],
  'scenarios':['Selective-attention checks','Cognitive psychology demos','Focus training'],
  'steps':['Read the instruction (name the ink color)','Respond to each item quickly','Mixed congruent/incongruent trials','See your interference effect','Repeat to compare'],
  'tips':['Say the color, not the word','Expect incongruent items to slow you','Stay relaxed','Use for demonstration, not diagnosis'],
  'faqs':[('Why is it slower for mismatched?','Reading is automatized; overriding it to name color creates interference.'),
          ('What does the effect measure?','It estimates the cost of resolving competing responses — a marker of executive control.')]},

 {'slug':'time-perception','name':'Time Perception Test',
  'desc':'Time Perception & Rhythm Accuracy Test: estimate and reproduce time intervals and rhythmic taps.',
  'intro':'This test probes your sense of time. You estimate a presented interval, then reproduce it, and tap along with a rhythm. It reveals how accurately you perceive and reproduce durations.',
  'features':['Interval estimation','Interval reproduction','Rhythm tapping','Accuracy feedback','100% client-side'],
  'scenarios':['Music and rhythm training','Self-awareness of time sense','Cognitive research'],
  'steps':['Watch/listen to a target interval','Estimate its length','Reproduce it as accurately as you can','Tap to a beat','Review your error'],
  'tips':['Count internally to calibrate','Fatigue widens error','Short intervals are harder','Track improvement over sessions'],
  'faqs':[('Why is timing imprecise?','Internal clock estimates drift with attention, arousal and interval length.'),
          ('What helps rhythm accuracy?','Subvocal counting and steady arousal improve reproduction.')]},

 {'slug':'pure-tone-audiometry','name':'Pure-Tone Audiometry',
  'desc':'Pure-Tone Hearing Screening: build a personal audiogram by finding the softest tones you can hear across frequencies.',
  'intro':'Pure-tone audiometry screens your hearing. Tones at different frequencies are played at decreasing volume; you indicate the softest you can hear at each frequency, building a personal audiogram.',
  'features':['Multiple frequencies','Descending threshold search','Personal audiogram plot','Left/right ear','100% client-side'],
  'scenarios':['Self hearing check','Baseline before loud events','Tracking changes over time'],
  'steps':['Put on headphones','Press when you hear a tone','Repeat per frequency/ear','View your audiogram','Compare across sessions'],
  'tips':['Quiet room, good headphones','Don’t guess on silence','Not a substitute for clinical audiometry','Retest in similar conditions'],
  'faqs':[('Is this a medical test?','No — it is a screening only; see an audiologist for diagnosis.'),
          ('Why per frequency?','Hearing loss often affects specific frequencies (e.g., high tones) first.')]},

 {'slug':'temporal-resolution-hearing','name':'Temporal Resolution Test',
  'desc':'Auditory Temporal Resolution Test: evaluate how precisely you distinguish rapid sounds or gaps.',
  'intro':'Temporal resolution is your ear’s ability to resolve rapid acoustic changes — gaps, rhythms and fast transitions. This test estimates that precision with brief signals.',
  'features':['Gap detection','Rapid sequence tasks','Threshold estimation','Left/right ear','100% client-side'],
  'scenarios':['Speech-in-noise difficulty checks','Auditory training baseline','Self monitoring'],
  'steps':['Use headphones','Detect gaps or rapid changes','Respond as precisely as possible','Repeat across conditions','Review your threshold'],
  'tips':['Quiet environment matters most','Fatigue reduces resolution','Not diagnostic','Pair with audiometry for context'],
  'faqs':[('What is temporal resolution?','The smallest time gap or change your auditory system can detect.'),
          ('Why does it matter?','Poor resolution can make speech in noise harder to follow.')]},

 {'slug':'1a2b-guess','name':'1A2B Number Guess',
  'desc':'1A2B (Bulls & Cows) number guessing: deduce the secret code using logic and A/B clues.',
  'intro':'1A2B is the classic code-breaking game (Bulls & Cows). Guess a hidden digit sequence; each attempt returns A (right digit, right place) and B (right digit, wrong place) to narrow it down logically.',
  'features':['Configurable digit length','A/B feedback','Attempt history','Logic training','100% client-side'],
  'scenarios':['Logical deduction practice','Ice-breaker or party game','Brain warm-up'],
  'steps':['Set the code length','Enter a guess','Read the A/B clues','Eliminate impossibilities','Crack the code'],
  'tips':['Start with a diverse first guess','Use A to fix positions, B to relocate','Keep a notes grid','Fewer guesses = sharper logic'],
  'faqs':[('What do A and B mean?','A = correct digit in correct place; B = correct digit in wrong place.'),
          ('Best strategy?','Maximize information per guess by covering many digits and positions.')]},

 {'slug':'daily-riddle','name':'Daily Riddle',
  'desc':'Daily Riddle Challenge: a fresh brain teaser every day with hints and answers.',
  'intro':'A daily riddle gives your brain a small, fun workout. Each day brings a new puzzle with progressive hints and a revealed answer so you can learn the trick.',
  'features':['New riddle daily','Tiered hints','Answer reveal','Share-friendly','100% client-side'],
  'scenarios':['Daily habit','Classroom warm-up','Light entertainment'],
  'steps':['Read today’s riddle','Think it through','Reveal hints if stuck','Check the answer','Come back tomorrow'],
  'tips':['Sleep on hard ones','Reread for double meanings','Share with friends','Treat as play, not pressure'],
  'faqs':[('Why daily?','Small consistent challenges build a thinking habit better than occasional marathons.'),
          ('Hints spoil it?','Hints are tiered so you control how much help you take.')]},

 {'slug':'amsler-grid-test','name':'Amsler Grid Test',
  'desc':'Amsler Grid macula self-test: check for signs of macular degeneration by watching for distortion in a grid.',
  'intro':'The Amsler Grid helps you self-monitor macular health. While fixating the center dot, you watch for wavy, blurry or missing areas — early signs of macular changes.',
  'features':['Standard grid','Monocular testing','Distortion checklist','Progress tracking','100% client-side'],
  'scenarios':['Macular self-monitoring','Baseline for at-risk users','Between-visit checks'],
  'steps':['Wear your reading glasses','Cover one eye','Fixate the center dot','Note any warping/blanks','Repeat with the other eye'],
  'tips':['Test in good light','Same distance each time','Report new distortions to a doctor','Not a diagnosis'],
  'faqs':[('What does distortion mean?','Wavy or missing grid areas can signal macular issues — get a professional exam.'),
          ('How often?','Many clinicians suggest a quick daily or weekly check for at-risk individuals.')]},

 {'slug':'astigmatism-chart','name':'Astigmatism Chart',
  'desc':'Astigmatism Fan Chart: self-screen for astigmatism by reading radial lines of varying clarity.',
  'intro':'The astigmatism chart shows radiating lines. If some directions look blurrier than others, it may indicate astigmatism — an uneven corneal curvature.',
  'features':['Radial line fan','Clarity comparison','Axis hint','Self-screen','100% client-side'],
  'scenarios':['Astigmatism self-check','Pre-eye-exam baseline','Tracking changes'],
  'steps':['View the fan at reading distance','Compare line sharpness by direction','Note the blurriest axis','Repeat per eye','Discuss with an optician'],
  'tips':['Even lighting helps','Don’t squint','One eye at a time','It screens, it does not prescribe'],
  'faqs':[('Blurry lines = astigmatism?','Often yes, but only an eye exam confirms axis and degree.'),
          ('Can I use it for glasses?','No — it only suggests a check is worthwhile.')]},

 {'slug':'eye-chart-toolkit','name':'Eye Chart Toolkit',
  'desc':'Professional Eye Chart Toolkit: multiple Snellen and logMAR charts with distance tools for quick visual-acuity checks.',
  'intro':'A toolkit of standard eye charts (Snellen and logMAR) with distance helpers, so you can do a quick, repeatable visual-acuity check at home or in a clinic.',
  'features':['Snellen and logMAR charts','Distance guidance','Per-eye testing','Printable-friendly','100% client-side'],
  'scenarios':['Rough acuity check','Classroom or workplace screen','Monitoring over time'],
  'steps':['Set the recommended distance','Cover one eye','Read the smallest line you can','Record the line','Switch eyes'],
  'tips':['Consistent lighting and distance','Don’t lean forward','Glasses as you normally wear them','Confirm with an optometrist'],
  'faqs':[('Is this accurate?','It is a rough screen, not a refraction; real acuity needs professional measurement.'),
          ('Snellen vs logMAR?','Both express acuity; logMAR is the modern, linearly scalable standard.')]},

 {'slug':'vision-screening-21','name':'Vision Screening 21',
  'desc':'21-Question Adaptive Vision Screening: estimate each eye’s refractive need through an adaptive questionnaire.',
  'intro':'This adaptive screening asks a short sequence of questions and tasks to estimate whether each eye may need correction, and roughly what type — a fast triage before a full eye exam.',
  'features':['Adaptive 21-question flow','Per-eye estimate','Refraction-type hint','Triage output','100% client-side'],
  'scenarios':['Pre-exam triage','Remote or rural screening','Self awareness'],
  'steps':['Answer the adaptive questions','Perform the simple visual tasks','Get a per-eye estimate','Review suggested next step','Book an eye exam if advised'],
  'tips':['Answer honestly, don’t guess','Same conditions each time','It estimates, never prescribes','Follow up professionally'],
  'faqs':[('Does it prescribe glasses?','No — it estimates need and type; only an optometrist prescribes.'),
          ('Why adaptive?','It asks fewer, more relevant questions, speeding the screen.')]},

 {'slug':'attachment-style-test','name':'Attachment Style Test',
  'desc':'Adult Attachment Style Test (ECR): discover your attachment pattern with the Experiences in Close Relationships scale.',
  'intro':'Based on the ECR (Experiences in Close Relationships) model, this test maps you onto anxious and avoidant dimensions to reveal your adult attachment style in close relationships.',
  'features':['ECR-based items','Anxious/avoidant scores','Style interpretation','Research-backed','100% client-side'],
  'scenarios':['Self-understanding in relationships','Couples or therapy context','Personal growth'],
  'steps':['Rate statements about relationships','Submit the full scale','See anxious/avoidant scores','Read your style','Reflect, don’t label'],
  'tips':['Answer about real relationships','Styles are dimensions, not boxes','Useful with a therapist','Re-test as you grow'],
  'faqs':[('What are the styles?','Secure, anxious, avoidant and fearful-avoidant, from two underlying dimensions.'),
          ('Can it change?','Attachment can shift with relationships, therapy and life experience.')]},

 {'slug':'bubble-tea-personality-quiz','name':'Bubble Tea Quiz',
  'desc':'What Bubble Tea Are You? A lighthearted personality quiz matching you to a bubble tea flavor.',
  'intro':'A fun, low-stakes personality quiz that maps your preferences to a bubble tea flavor. Pure entertainment — no data leaves your browser.',
  'features':['Playful questions','Flavor result','Shareable','No account','100% client-side'],
  'scenarios':['Party or break-ice','Social media fun','Light mood lift'],
  'steps':['Answer the fun questions','Get your flavor','Read the trait blurb','Share with friends','Retake for laughs'],
  'tips':['Don’t overthink','It’s for fun, not insight','Great group activity','No data stored'],
  'faqs':[('Is it serious?','No — it is entertainment, not psychology.'),
          ('Why bubble tea?','It is a relatable, playful frame for a quick personality match.')]},

 {'slug':'enneagram-test','name':'Enneagram Test',
  'desc':'Enneagram Personality Test: map your type across nine core motivations and traits.',
  'intro':'The Enneagram describes nine personality types rooted in core motivations and fears. This test scores you across the types to suggest your likely primary type and wings.',
  'features':['Nine-type scoring','Wing and instinct hints','Type descriptions','Reflection prompts','100% client-side'],
  'scenarios':['Self-exploration','Coaching and retreats','Team building'],
  'steps':['Answer the typed items','See your type ranking','Read your top type and wings','Reflect on motivations','Discuss with others'],
  'tips':['Answer for your inner pattern','High types may be close','Use for growth, not labeling','Revisit periodically'],
  'faqs':[('What are wings?','Adjacent types that flavor your core type.'),
          ('Enneagram vs MBTI?','Enneagram centers on motivation/fear; MBTI on cognitive preferences.')]},

 {'slug':'holland-career-test','name':'Holland Career Test',
  'desc':'Holland Code (RIASEC) Career Test: match your interests to six career themes and suggest directions.',
  'intro':'Based on Holland’s RIASEC model (Realistic, Investigative, Artistic, Social, Enterprising, Conventional), this test ranks your interest code and maps it to compatible career directions.',
  'features':['RIASEC six-type rating','Top three-letter code','Career direction matches','Type interpretation','100% client-side'],
  'scenarios':['Major/career choice','Career planning','Vocational counseling'],
  'steps':['Rate interest in six activity groups','Get your three-letter code','See matched careers','Weigh against ability and values','Talk with a counselor'],
  'tips':['Answer by genuine interest','The top code combo is informative','Interest ≠ ability — decide holistically','Codes shift with experience'],
  'faqs':[('What is RIASEC?','Six interest orientations combined into your career-interest profile.'),
          ('Does the result choose my job?','It suggests directions; final choices also need ability, values and opportunity.')]},
]

TPL = """<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - ToolBox</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="ToolBox">
<meta property="og:url" content="{canonical}">
<meta property="og:description" content="{desc}">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://chenguangwu.github.io/og-image.png">
<meta name="twitter:image:alt" content="ToolBox - Free Online Tools & Guides">
<meta property="og:image" content="https://chenguangwu.github.io/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="ToolBox - Free Online Tools & Guides">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{canonical}">
<script type="application/ld+json">{article_json}</script>
<script type="application/ld+json">{breadcrumb_json}</script>
<script type="application/ld+json">{faq_json}</script>
<style>
:root{--primary:#FF6B35;--text:#1F2937;--muted:#6B7280;--border:#E5E7EB;--bg:#FFFAF7;}
*{box-sizing:border-box;}
body{margin:0;font-family:"Plus Jakarta Sans","Noto Sans SC",system-ui,sans-serif;color:var(--text);background:var(--bg);line-height:1.75;}
.breadcrumb a{color:var(--primary);text-decoration:none;margin-right:6px;}
.breadcrumb a:hover{text-decoration:underline;}
main{max-width:820px;margin:0 auto;padding:28px 20px 60px;}
h1{font-size:28px;margin:0 0 8px;}
.lead{font-size:16px;color:var(--muted);margin:0 0 22px;}
h2{font-size:20px;margin:28px 0 10px;color:var(--primary);}
.toc{background:#fff;border:1px solid var(--border);border-radius:14px;padding:14px 18px;margin:18px 0;}
.toc ul{margin:0;padding-left:20px;}
.toc a{color:var(--text);text-decoration:none;}
.toc a:hover{color:var(--primary);}
ul,ol{padding-left:22px;}
li{margin:8px 0;}
.related{margin-top:26px;padding:16px;background:#fff;border:1px solid var(--border);border-radius:14px;}
.related h3{margin:0 0 10px;font-size:16px;color:var(--text);}
.tool-chip{display:inline-block;margin:4px 6px 4px 0;padding:6px 12px;border:1px solid var(--border);border-radius:999px;color:var(--primary);text-decoration:none;font-size:14px;}
.tool-chip:hover{background:var(--primary);color:#fff;}
.faq{margin-top:26px;}
.faq dt{font-weight:700;margin-top:14px;}
.faq dd{margin:4px 0 0;color:var(--muted);}
.back{margin-top:30px;padding:16px;background:#fff;border:1px solid var(--border);border-radius:14px;}
.back a{color:var(--primary);font-weight:700;text-decoration:none;}
</style>
<script src="/js/analytics.js" defer></script>
<link rel="stylesheet" href="../css/common.css">
<script src="../js/common.js" defer></script>
</head>
<body>
<nav class="breadcrumb"><a href="https://chenguangwu.github.io/">ToolBox</a> / <a href="https://chenguangwu.github.io/guides/index.html">Guides</a> / <span>{title}</span></nav>
<main>
<h1>{title}</h1>
<p class="lead">{intro}</p>
<div class="toc"><strong>Contents</strong><ul><li><a href="#s0">Key Features</a></li><li><a href="#s1">Use Cases</a></li><li><a href="#s2">How to Use</a></li><li><a href="#s3">Practical Tips</a></li><li><a href="#s4">FAQ</a></li></ul></div>
<h2 id="s0">Key Features</h2>
<ul>{features}</ul>
<h2 id="s1">Use Cases</h2>
<ul>{scenarios}</ul>
<h2 id="s2">How to Use</h2>
<ol>{steps}</ol>
<h2 id="s3">Practical Tips</h2>
<ul>{tips}</ul>
<div class="related"><h3>Related Tool</h3>{related_chips}</div>
<div class="faq"><h2 id="s4">FAQ</h2><dl>{faqs}</dl></div>
<div class="back"><a href="https://chenguangwu.github.io/guides/index.html">&larr; Back to Guides</a></div>
</main>
</body>
</html>"""


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            .replace('"', '&quot;'))


def li(items):
    return '\n'.join('<li>%s</li>' % esc(x) for x in items)


def faq_dl(items):
    out = []
    for q, a in items:
        out.append('<dt>%s</dt>' % esc(q))
        out.append('<dd>%s</dd>' % esc(a))
    return '\n'.join(out)


def inject_en_link():
    """给 19 个中文指南注入「🌐 English」芯片，链到对应 .en.html。
    幂等：已含 data-en-guide-link 则跳过。英文页借此 <a href> 被爬取、传 link equity。
    不改 _build.py / sitemap（试点边界：待批量方案确认再统一收录与 ?lang=en 切换）。"""
    for g in EN:
        slug = g['slug']
        zh_path = os.path.join(ROOT, 'guides', '%s-guide.html' % slug)
        if not os.path.exists(zh_path):
            print('  ! 中文指南缺失，跳过:', slug)
            continue
        with io.open(zh_path, encoding='utf-8') as f:
            html = f.read()
        if 'data-en-guide-link' in html:
            continue
        en_href = '%s-guide.en.html' % slug
        chip = '<a class="tool-chip" href="%s" data-en-guide-link>🌐 English</a>' % en_href
        m = re.search(r'(<div class="related">.*?</div>)\s*(<div class="faq">)', html, re.S)
        if not m:
            print('  ! 未找到注入点(related/faq):', slug)
            continue
        new_block = m.group(1)[:-6] + chip + '</div>'  # 去掉 .related 末尾 </div>
        html = html[:m.start()] + new_block + m.group(2) + html[m.end():]
        with io.open(zh_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print('  OK 注入英文芯片:', slug)


def main():
    guides_dir = os.path.join(ROOT, 'guides')
    n = 0
    for g in EN:
        slug = g['slug']
        tool = TOOL_MAP.get(slug)
        if not tool:
            print('  ! 无工具映射:', slug)
            continue
        title = g['name']
        canonical = 'https://chenguangwu.github.io/guides/%s-guide.en.html' % slug
        article_json = json.dumps({
            '@context': 'https://schema.org', '@type': 'Article',
            'inLanguage': 'en-US', 'headline': title,
            'description': g['desc'],
            'author': {'@type': 'Organization', 'name': 'ToolBox'},
            'datePublished': '2026-09-02', 'dateModified': '2026-09-02',
            'mainEntityOfPage': {'@type': 'WebPage', '@id': canonical}
        }, ensure_ascii=False)
        breadcrumb_json = json.dumps({
            '@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'ToolBox',
                 'item': 'https://chenguangwu.github.io/'},
                {'@type': 'ListItem', 'position': 2, 'name': 'Guides',
                 'item': 'https://chenguangwu.github.io/guides/index.html'},
                {'@type': 'ListItem', 'position': 3, 'name': title,
                 'item': canonical}]}, ensure_ascii=False)
        faq_json = json.dumps({
            '@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': q,
                            'acceptedAnswer': {'@type': 'Answer', 'text': a}}
                           for q, a in g['faqs']]}, ensure_ascii=False)
        zh_link = 'https://chenguangwu.github.io/guides/%s-guide.html' % slug
        related_chips = ('<a class="tool-chip" href="https://chenguangwu.github.io/%s?lang=en">%s &rarr;</a>'
                         '<a class="tool-chip" href="%s">🌐 中文</a>' % (tool, esc(title), zh_link))
        html = (TPL
                .replace('{title}', esc(title))
                .replace('{desc}', esc(g['desc']))
                .replace('{canonical}', canonical)
                .replace('{intro}', esc(g['intro']))
                .replace('{features}', li(g['features']))
                .replace('{scenarios}', li(g['scenarios']))
                .replace('{steps}', li(g['steps']))
                .replace('{tips}', li(g['tips']))
                .replace('{faqs}', faq_dl(g['faqs']))
                .replace('{related_chips}', related_chips)
                .replace('{article_json}', article_json)
                .replace('{breadcrumb_json}', breadcrumb_json)
                .replace('{faq_json}', faq_json))
        out = os.path.join(guides_dir, '%s-guide.en.html' % slug)
        with io.open(out, 'w', encoding='utf-8') as f:
            f.write(html)
        n += 1
        print('  OK: guides/%s-guide.en.html' % slug)
    print('英文指南生成完成：%d 篇' % n)
    print('--- 反向注入：中文指南 -> 英文芯片 ---')
    inject_en_link()


if __name__ == '__main__':
    main()
