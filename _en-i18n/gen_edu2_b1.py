#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'edu2')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'edu2')
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
    out = {'slug': slug, 'industry': 'edu2', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

#!/usr/bin/env python3


def main():
    # ===== exam-analysis (19) =====
    write('exam-analysis', build('exam-analysis', [
        'Exam Score Analysis',
        'Enter student scores to auto-compute the average, highest/lowest, standard deviation, pass rate, and excellence rate, and generate a score-band distribution with rankings.',
        'Core formulas (by input variable): b.count ÷ maxBand × 100; full × excelPct ÷ 100; full × passPct ÷ 100',
        'View the Exam Score Analysis User Guide',
        ': measures how spread out the scores are; the larger the value, the more dispersed the distribution.',
        'Deep Dive: Exam Score Analysis',
        'Batch statistics for class/grade scores: paste the whole class’s scores (comma- or newline-separated); the tool gives the count, mean,',
        ', highest/lowest, pass rate, and excellence rate at once, avoiding per-student calculation.',
        'Band distribution and teaching diagnosis: split counts by full-score proportions into 90/80/70/60 bands to quickly locate weak score ranges, aiding review and remediation.',
        'Compatibility with different full-score scales: when the full score is not 100 (e.g. 120/150), by the pass/excellence line',
        'the tool auto-converts the cutoff scores, avoiding manual conversion errors.',
        'Example: 8 students’ scores 88/92/76/65/95/58/83/70, full score 100, pass 60%, excellent 85%',
        'Count n=8, sum=627, mean=78.38, std≈12.48, highest 95/lowest 58; pass line=100×60%=60 → 7 pass (58 fails), pass rate 87.5%; excellence line=100×85%=85 → 3 excellent (88/92/95), excellence rate 37.5%; bands: 90-100% 2, 80-89% 2, 70-79% 2, 60-69% 1, below 60% 1.',
        'What does the standard deviation represent?',
        'The standard deviation reflects how spread out the scores are (here it is the population standard deviation σ=√(Σ(x−mean)²/n)); a larger value means wider gaps and clearer polarization among students, a smaller value means the class is more balanced — an important statistic for diagnosing a two-pole split in the class.',
        'How do I compute the pass/excellence rate correctly?',
        'Pass rate = count reaching the pass line ÷ total count × 100%, excellence rate similarly; the key is that pass/excellence cutoff lines must be converted by the full-score scale (line percent × full score), not fixed at 60/85 points — at full score 150 the pass line is 90. This tool auto-converts by full score.',
        'Exam Score Analysis is an online tool in the education and learning domain.',
        'Name,Score example: Zhang San,92 Li Si,85 Wang Wu,78 or enter scores directly: 92 85 78',
    ]))

    # ===== exam-countdown (20) =====
    write('exam-countdown', build('exam-countdown', [
        'Exam Countdown',
        'Compute the remaining days, weekdays, and weekend days until the exam, and generate a study-pace plan.',
        'View the Exam Countdown User Guide',
        'Count weekends',
        'Include statutory holidays (by adjusted schedule)',
        'Deep Dive: Exam Countdown',
        'Study-day planning: enter the exam date; the tool computes days remaining and separately gives',
        'weekdays',
        'and weekend days, for arranging your review pace.',
        'Holiday schedule handling: after checking “deduct statutory holidays”, long holidays like National Day / Spring Festival are removed from weekdays and counted separately, avoiding mistaking a holiday for a study day.',
        'Managing multiple exams in parallel: build a',
        'countdown',
        'for each exam, compare their remaining weekdays, and prioritize the one that is near and tight on weekdays.',
        'Example: today 2026-09-10, exam 2026-10-01',
        'Total days to exam = ceil((10-01 − 09-10)) = 21 days; of these, counting Monday–Friday as weekdays ≈ 15 days, weekends 6 days (holidays not deducted); if 10-01 falls on the National Day holiday, checking “deduct statutory holidays” removes the holiday from weekdays and counts it as holiday. (Another example, exam 09-30: total 20 days, weekdays ≈14, weekends 6.)',
        'Why does the countdown use ceil instead of rounding?',
        'Rounding the remaining days up (less than a day counts as a day) avoids underestimating study time — even if only a few hours remain it still counts as “one day left”, reminding the candidate to review that day; this is a conservative and safe rounding strategy.',
        'Is the statutory-holiday data accurate?',
        'This tool has built-in common statutory holidays (e.g. National Day 10-01~10-07, Spring Festival, etc.) for deduction, but each year’s specific adjusted schedule follows the State Council’s announcement for that year, and makeup workdays are not auto-extended; for important exams follow the school/exam institution calendar — results are for planning reference only.',
        'Exam Countdown is an online tool in the education and learning domain.',
    ]))

    # ===== schedule-conflict (16) =====
    write('schedule-conflict', build('schedule-conflict', [
        'Class Schedule Conflict Detector',
        'Enter course arrangements to auto-detect teacher conflicts and room conflicts in the same time slot, and output a conflict list with a visual timetable.',
        'View the Class Schedule Conflict Detector User Guide',
        'Conflict detection indexes on two dimensions — (time slot + teacher) and (time slot + room): the same teacher appearing twice in one slot is a teacher conflict, the same room twice in one slot is a room conflict; conflict count = teacher conflicts + room conflicts; conflict-free rate = conflict-free slots ÷ total slots × 100%; the visual timetable grids courses by week × period and highlights conflicting cells for easy adjustment.',
        'Deep Dive: Class Schedule Conflict Detector',
        'Pre-check before scheduling: paste the planned courses (weekday, period, teacher, room) into the tool; it automatically compares overlaps pairwise and flags teacher conflicts (same teacher, same time, two courses) and room conflicts (same room, same time, two courses).',
        'Room resource optimization: room-conflict hints reveal a room double-booked, so you can adjust in time or request expansion, avoiding class “collisions”.',
        'Teacher workload check: teacher conflicts usually mean the schedule underestimates staffing, hinting that more teachers are needed or classes should be staggered.',
        'Example: 3 courses share Monday periods 1-2',
        'Course A: Monday 1-2, Teacher Zhang, Room 101; Course B: Monday 1-2, Teacher Zhang, Room 102; Course C: Monday 1-2, Teacher Li, Room 101. A and B overlap in time and share a teacher → 1 teacher conflict, different rooms so no room conflict; A and C overlap in time and share Room 101 → 1 room conflict, different teachers so no teacher conflict; total: 3 courses, 1 teacher conflict, 1 room conflict.',
        'What is the basis for conflict detection?',
        'Two courses conflict if they share the same weekday and their period ranges overlap (a.start<b.end and b.start<a.end); on top of the overlap, compare whether teacher/room are the same, recording teacher or room conflicts separately. The tool only does time + resource conflict detection, not course reasonableness.',
        'Can it detect cross-week or odd/even-week conflicts?',
        'Currently it compares by fixed weekday + period, without distinguishing odd/even weeks or alternating weeks; if a course has odd/even-week scheduling, list the conflicting weeks separately before comparing, or mark the week in the input to avoid missed detection. Results are for initial scheduling checks only.',
        'Class Schedule Conflict Detector is an online tool in the education and learning domain.',
        'Course,Teacher,Room,Weekday,Start,End example: Advanced Math,Teacher Zhang,A101,1,1,2 Linear Algebra,Teacher Zhang,B202,1,1,2 English,Teacher Li,A101,1,3,4',
    ]))

    # ===== study-progress (16) =====
    write('study-progress', build('study-progress', [
        'Study Progress Dashboard',
        'Enter each subject’s task completion to visualize overall and per-subject progress, estimate the expected completion time, and save data locally.',
        'View the Study Progress Dashboard User Guide',
        'Deep Dive: Study Progress Dashboard',
        'Multi-subject progress overview: register “done / total tasks / hours per task” per subject; the tool aggregates total progress',
        'and remaining total hours, so you see overall completion at a glance.',
        'Completion-date forecast and catch-up: from the daily available hours, back-calculate remaining days and the expected finish date from remaining hours, and compare with the target date to judge if you are off track.',
        'Review and rebalance: when a subject lags, raise its daily input or adjust the target; the tool updates overall progress and the expected finish date in real time.',
        'Example: Math 8/10 (1.5h) · English 12/20 (1h) · Physics 5/8 (2h), daily input 4h, target 2026-10-01',
        'Remaining hours = (10−8)×1.5 + (20−12)×1.0 + (8−5)×2.0 = 3+8+6 = 17 h; total progress = (8+12+5)/(10+20+8) = 25/38 ≈ 65.8%; days needed = ceil(17/4) = 5 days → expected completion 2026-09-15; 21 days to target 2026-10-01, 5 ≤ 21 → on track.',
        'Why is the expected completion date sometimes much earlier than expected?',
        'Completion date = today + remaining hours ÷ daily input hours, rounded up to whole days; fewer remaining hours or higher daily input naturally brings it earlier. Note it assumes the ideal of “stable daily input”; actual leave/interruption delays it, so keep a buffer.',
        'How can I estimate hours per task more accurately?',
        'Use the average time of several recently completed tasks in that subject as hours — more accurate than guessing; after finishing, backfill the actual value and the tool gets closer to the real pace as data accumulates. Progress counts by task number regardless of difficulty; split heavy tasks for a smoother curve.',
        'Study Progress Dashboard is an online tool in the education and learning domain.',
        'Subject,Done,Total,HoursPerTask example: Math,45,80,1.5 English,30,60,1 MajorCourse,20,100,2',
    ]))

    # ===== wrong-book (18) =====
    write('wrong-book', build('wrong-book', [
        'Wrong-Question Notebook',
        'Auto-categorize wrong questions by subject, record the error reason and mastery status, and auto-remind review when due. Data is saved in the local browser.',
        'View the Wrong-Question Notebook User Guide',
        'Deep Dive: Wrong-Question Notebook',
        'Structured collection: register by subject, question type (multiple choice / fill-in / short answer / calculation), error reason, correct answer, and review status to build a searchable personal wrong-question bank, leaving paper copying behind.',
        'Filter by condition: filter by subject or status (not mastered / reviewing / mastered) and only drill “not mastered” and “reviewing” questions before exams to boost efficiency.',
        'Spaced-review reminders: record each question’s review-interval days and schedule re-viewing by the forgetting curve, avoiding “learned then dropped” causing repeated exam mistakes.',
        'Example: collect a math calculation wrong question',
        'Subject “Math”, type “Calculation”, problem “evaluate ∫₀¹ x² dx”, error reason “wrong substitution of integral limits”, correct answer “1/3”, status “Reviewing”, review interval 3 days; filter in the notebook by “Subject=Math + Status=Reviewing” to list it; when due (last time +3 days) it prompts review, and a correct re-view can change status to “Mastered”.',
        'Where is the notebook data stored? Is it safe?',
        'Data is stored in the browser’s local localStorage, no network, no upload; switching devices / clearing cache loses it; for important content, export and back up regularly. It is positioned as a personal study aid, with no account or cloud sync.',
        'How to use the notebook most efficiently?',
        'Stick to the “three elements”: the error reason must be specific (not “careless” but “wrong integral-limit substitution”), the answer complete, and the status updated with review; combined with spaced review (e.g. increasing 1/3/7 days) it converts better to long-term memory than one-time copying. This tool is only a management aid; the study method must be maintained by yourself.',
        'Wrong-Question Notebook is an online tool in the education and learning domain.',
        'e.g. Math',
        'e.g. Multiple choice',
        'Enter the problem content...',
        'Correct answer or solution approach...',
    ]))


if __name__ == '__main__':
    main()
