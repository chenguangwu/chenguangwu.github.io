#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sports (75) 分类英文态数据源根治：同步三端 + 清孤儿键。

三处数据源（与 science 同坑，§6「英文态数据源三处」）：
  ① i18n/tools/sports-body.json   -> build `_prerender_tool_body` 预渲染 h2 + 首个 <p>
  ② i18n/tools/sports.json en-US  -> industry JSON 的 ed 最高优先级源
  ③ i18n/tools/_en_override.json  -> 运行时 en（h2/h1）与 ed

用法：
  python3 scripts/fix_sports_body_i18n.py --dry-run
  python3 scripts/fix_sports_body_i18n.py --apply
"""
import argparse
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools', 'sports')
OV = os.path.join(ROOT, 'i18n', 'tools', '_en_override.json')
BODY = os.path.join(ROOT, 'i18n', 'tools', 'sports-body.json')
GIS = os.path.join(ROOT, 'i18n', 'tools', 'sports.json')

# NAME = 英文名（h2 / h1 / 导航 / 英文态标题），INTRO = 真实英文描述（intro / ed）。
# 依据 sports 工具中文名与描述撰写，避免 "free online tool" 类套话。
NAME = {
    'altitude-acclimatization': 'Altitude Acclimatization Schedule',
    'analysis-19': 'Tactical Attack/Defense Video Analysis',
    'analysis-20': 'Shooting Score & Stability Analysis',
    'assessor-risk-2': 'Sports Injury Risk Assessment (Questionnaire)',
    'baofali-zongtiao-lidingtiaoyuan': 'Explosive Power Calculator (Vertical Jump / Long Jump)',
    'calc-61': 'Activity Calorie Expenditure Calculator (MET)',
    'calc-62': 'Baseball Batting & Pitching Statistics',
    'calc-angle-slope': 'Ski Slope Angle & Grade Calculator',
    'calc-heart-rate-1': 'Heart Rate Reserve (Karvonen) Calculator',
    'calc-length-cutting': 'Kinesiology Tape Cutting Length Calculator',
    'calc-time': 'Dive No-Decompression Limit (NDL) Calculator',
    'calculator-calc-9': 'Cycling Gear Ratio Calculator',
    'calculator-calc-time': 'Marathon Pace Calculator',
    'climbing-grade-converter': 'Climbing Grade Converter (V / YDS / French / UK)',
    'convert-13': 'Climbing Grade Converter (V ↔ YDS)',
    'convert-47': 'One-Rep Max (1RM) Estimator',
    'convert-time': 'Triathlon Transition Time Calculator',
    'detector-14': 'Anaerobic Threshold (AT) Detector',
    'dianjiezhi-diushi-buchong': 'Electrolyte Loss & Replacement Calculator',
    'diving-no-decompression': 'Dive No-Decompression Limit Calculator',
    'estimate-22': 'Hydration Strategy Estimator',
    'estimate-35': 'Sweat Rate Estimator',
    'estimate-tester': 'VO2max Estimator (Running Test)',
    'generator-random-3': 'Yoga Pose Sequence Generator',
    'heart-rate-1': 'Maximum Heart Rate Calculator',
    'heart-rate-2': 'Heart Rate Variability (HRV) Analyzer',
    'heart-rate-3': 'Heart Rate Recovery (HRR) Index',
    'hongxibao-xieyang-shiyingxing': 'Red Blood Cell Oxygen-Carrying Adaptation Calculator',
    'jianzhong-tuoshui-buye-kongzhi': 'Weight-Cut (Dehydration / Rehydration) Control Calculator',
    'jixianwei-kuai-man-leixingtuice': 'Muscle Fiber Type (Fast/Slow) Estimator',
    'juzhongzongchengji-sinclair-xishu': 'Weightlifting Total & Sinclair Coefficient Calculator',
    'lanqiumingzhonglv-lanbanxiaolv': 'Basketball Shooting & Rebound Efficiency',
    'lingmin-zhefanpao-chengji': 'Agility (Shuttle Run) Score Calculator',
    'pilaohuifuqushi': 'Fatigue Recovery Trend Calculator (CK / BUN)',
    'pingheng-biyandanjiao-shichang': 'Balance (Eyes-Closed Single-Leg Stand) Timer',
    'pingpangqiu-xiangchi-faqiu-defen': 'Table Tennis Rally / Serve Scoring Analysis',
    'rater-34': 'Volleyball Skill Rating (Pass / Spike)',
    'rater-35': 'Judo Technique Rating (Tachi-waza / Ne-waza)',
    'rater-36': 'Equestrian Performance Rating (Gait / Jumping)',
    'rater-motion': 'Movement Stability Rating (Standard Deviation)',
    'ratio-18': 'Fat Oxidation Energy Ratio Calculator',
    'rehab-motion': 'Injury Prevention & Rehab Exercise Library',
    'rouren-qianqu-cequ-jinbu': 'Flexibility (Forward / Side Bend) Progress Tracker',
    'shejiansanbubanjing': 'Archery Group Radius (CEP) Calculator',
    'sheyangdonglixuebanshi': 'Oxygen Uptake Kinetics Half-Time Calculator',
    'shuimianhuifuzhiliang': 'Sleep Recovery Quality Index',
    'simulator-18': 'High-Altitude Hypoxia Adaptation Simulator',
    'sleeping-bag-rating': 'Sleeping Bag Temperature Rating Lookup (EN13537)',
    'speed-5': 'Speed / Acceleration Decomposition Calculator',
    'speed-6': 'Fencing Lunge Speed Analysis',
    'sports-calculator': 'Sports & Outdoor Calculator Hub',
    'sports-reference': 'Sports & Outdoor Reference Hub',
    'sports-schedule': 'Weekly Workout Schedule Generator',
    'sports-stats': 'Workout Data Statistics Tracker',
    'stats-8': 'Soccer Match Statistics (Possession / Pass)',
    'strength-5': '80/20 Polarized Training Week Planner',
    'swimming-stroke-efficiency': 'Swimming Stroke Efficiency Calculator (DPS / SR / SWOLF)',
    'taiquandao-hengti-xiapi-defen': 'Taekwondo Kick Scoring Analysis',
    'tent-wind-rating': 'Tent Wind Resistance Rating Lookup',
    'tester-1': 'Bodyweight Max-Rep 1RM Estimator (Push-up / Pull-up)',
    'tester-7': 'Endurance Test Evaluator (AT / VO2max)',
    'tester-8': 'Maximal Accumulated Oxygen Deficit (MAOD) Test',
    'time-30': 'Swimming SWOLF Efficiency Calculator',
    'time-31': 'Wrestling Match Time Allocation',
    'tongqibizhifenxi': 'Ventilatory Equivalents & Threshold (VE/VO2) Analysis',
    'training-load': 'Supercompensation Training Load Scheduler',
    'training-planner': 'Personalized Training Plan Generator',
    'triathlon-transition': 'Triathlon Transition Time Calculator',
    'wangqiudefenlvfenxi': 'Tennis Serve Statistics Analysis',
    'xuerusuanyuzhiceding': 'Blood Lactate Threshold Tester',
    'yangmaiboxiaolv': 'Oxygen Pulse Efficiency Calculator',
    'yoga-pose-generator': 'Yoga Pose Random Generator',
    'youyonghuashuixiaolv-swolf': 'Swimming Stroke Efficiency (SWOLF) Calculator',
    'yumaoqiushaqiuxiaolv': 'Badminton Smash Efficiency Calculator',
    'zhangpengfangfengxishu': 'Tent Wind-Resistance Coefficient Calculator',
}

INTRO = {
    'altitude-acclimatization': 'Enter your start and target altitude to generate a day-by-day ascent plan, assess altitude-sickness risk and get a recommended ascent rate for safe mountaineering and high-plateau travel.',
    'analysis-19': 'Structurally tag attack and defense clips from match video, tally attack-defense transitions and key rounds, and support coaching tactical review with clean statistics.',
    'analysis-20': 'Enter each shot’s ring score to compute the mean, within-group spread and stability metrics, then generate a score trend for shooting-training review.',
    'assessor-risk-2': 'A sports-injury risk questionnaire based on Functional Movement Screen (FMS) and injury-risk factors, scoring risk across exercise habits, injury history, flexibility, core strength and recovery management.',
    'baofali-zongtiao-lidingtiaoyuan': 'Enter jump height or distance and body weight to estimate power output and an explosive-power index for athlete physical assessment.',
    'calc-61': 'Based on a MET (metabolic equivalent) activity database, pick an activity and enter body weight and duration to compute calories burned for fitness tracking, fat-loss planning and energy-balance checks.',
    'calc-62': 'Compute baseball batting average (AVG), on-base percentage (OBP), slugging (SLG) and OPS, plus pitching ERA and WHIP from game stats.',
    'calc-angle-slope': 'Enter vertical drop and horizontal distance to convert a slope percentage into the slope angle, for ski-run difficulty grading and safety notes.',
    'calc-heart-rate-1': 'Using the Karvonen formula with age and resting heart rate, compute target training heart-rate zones (heart-rate-reserve method) for scientific aerobic-intensity control.',
    'calc-length-cutting': 'Pick a taping site and enter the measured length to compute the kinesiology-tape length, anchor positions and cutting shape for personalized sports-taping prep.',
    'calc-time': 'Based on the PADI metric no-decompression table, compute the no-decompression limit, maximum operating depth and pressure group for a given depth.',
    'calculator-calc-9': 'Enter chainring, cog and wheel diameter to compute gear ratio, distance per crank revolution, gear inches and speed at different cadences for road and mountain bike setup.',
    'calculator-calc-time': 'Enter a target finish time or target pace to compute marathon pace, average speed and per-kilometre splits for training plans and race pacing strategy.',
    'climbing-grade-converter': 'Convert climbing grades across major systems — V-scale bouldering, YDS, French and British — from V0 entry to V16 top, for cross-system training and route choice.',
    'convert-13': 'A climbing-grade converter between the V scale and YDS: enter either grade for a two-way mapping of the two climbing-difficulty systems.',
    'convert-47': 'A one-rep-max (1RM) estimator: enter a weight lifted for a given number of repetitions and estimate the single maximal repetition from estimation formulas for strength-load setting.',
    'convert-time': 'A triathlon transition-time calculator: sum swim, bike and run segment times with transition times to get total time and each segment’s share for race-pace analysis.',
    'detector-14': 'Detect the anaerobic threshold (AT) breakpoint from heart-rate data at increasing exercise intensities: enter heart rates at different intensities to auto-identify the HR breakpoint and AT intensity.',
    'dianjiezhi-diushi-buchong': 'Estimate sodium, potassium and other electrolyte losses from sweat volume and exercise duration, and give fluid and replenishment advice for endurance-sport protection.',
    'diving-no-decompression': 'Based on the PADI/RDP no-decompression limit table, enter dive depth to compute the safe no-decompression bottom time at each depth for recreational dive planning and safety margin.',
    'estimate-22': 'From body weight, exercise duration, ambient temperature and intensity, predict sweat loss and dehydration level and suggest a scientific hydration rhythm.',
    'estimate-35': 'Enter pre- and post-exercise body weight and duration to estimate sweat rate and dehydration percentage by the weighing method, with recommended fluid replacement for endurance training and racing.',
    'estimate-tester': 'Estimate VO2max from a Cooper 12-minute run test using VO2max = (distance − 504.9) / 44.73, with several running-test methods supported.',
    'generator-random-3': 'Generate a yoga sequence from a built-in pose library with tips, adjustable duration and intensity, for home practice planning — generated locally.',
    'heart-rate-1': 'Compare several maximum-heart-rate formulas (such as 220 − age) to individualize HRmax and partition warm-up, fat-burn, aerobic and anaerobic training zones for scientific training.',
    'heart-rate-2': 'Enter an R-R interval series (milliseconds, space/comma/newline separated) to compute time-domain HRV metrics SDNN, RMSSD and pNN50 for autonomic-nervous-system assessment.',
    'heart-rate-3': 'Enter heart rate at exercise stop and after 1/2/3 minutes of recovery to compute the heart-rate recovery (HRR) value for cardiovascular-function and recovery assessment.',
    'hongxibao-xieyang-shiyingxing': 'Estimate red-cell augmentation and VO2max adaptation from altitude and training factors for evaluating high-altitude training effects.',
    'jianzhong-tuoshui-buye-kongzhi': 'A weight-cut (dehydration/rehydration) control calculator: estimate required dehydration/rehydration from target weight and weight-class, and flag a safe weight-loss range for weigh-in sports.',
    'jixianwei-kuai-man-leixingtuice': 'A muscle-fiber fast/slow type estimator: combine sport characteristics and test data to infer fast- or slow-twitch dominance and guide training direction.',
    'juzhongzongchengji-sinclair-xishu': 'Enter snatch and clean-and-jerk results and body weight to compute total, the Sinclair body-weight coefficient and a cross-weight predicted total for weightlifting scoring and comparison.',
    'lanqiumingzhonglv-lanbanxiaolv': 'Compute field-goal percentage, true shooting percentage (TS%), rebound rate and a Hollinger game score from basketball box-score inputs.',
    'lingmin-zhefanpao-chengji': 'A shuttle-run agility score calculator: convert shuttle-run time into an agility rating and improvement margin for athlete agility testing.',
    'pilaohuifuqushi': 'Enter creatine kinase (CK) and blood urea nitrogen (BUN) with sex to assess muscle damage and metabolic fatigue, compute a composite fatigue index and suggest recovery time.',
    'pingheng-biyandanjiao-shichang': 'A balance (eyes-closed single-leg stand) duration recorder: log stand time and compare against norms to assess balance ability for rehab and fitness testing.',
    'pingpangqiu-xiangchi-faqiu-defen': 'A table-tennis rally/serve scoring tool: log rally and serve-round points to compute scoring rate and key-point performance for technique-tactics analysis.',
    'rater-34': 'A volleyball skill rater scoring technique from two core dimensions — pass accuracy and spike success — combined with serve and block for a composite rating.',
    'rater-35': 'A judo technique rater scoring from two dimensions — standing throws (Tachi-waza) and ground techniques (Ne-waza) — combined with ippon, waza-ari and yuko scoring.',
    'rater-36': 'An equestrian performance rater scoring from four dimensions — gait quality, jumping technique, rider posture and course accuracy — for dressage and show jumping.',
    'rater-motion': 'A movement-stability rater: analyze the deviation of repeated lifts/throws to quantify technique stability; smaller standard deviation means higher stability.',
    'ratio-18': 'From exercise intensity (%VO2max) estimate the fat vs carbohydrate energy ratio and predict fat burned during exercise, for fat-loss and endurance training.',
    'rehab-motion': 'An injury-prevention and rehab exercise library: recommend preventive or rehabilitative movements by injury site and rehab phase and track completion for injury management.',
    'rouren-qianqu-cequ-jinbu': 'A flexibility (forward/side bend) progress tracker: log sit-and-reach and similar tests, convert to improvement margin and rating for flexibility training tracking.',
    'shejiansanbubanjing': 'Enter the landing coordinates of several arrows relative to the target center (cm) to compute the mean point of impact, group radius (CEP), extreme spread and radial standard deviation for shooting precision.',
    'sheyangdonglixuebanshi': 'Enter resting VO2, target (steady-state) VO2 and the time to 50% change to compute the oxygen-uptake kinetics time constant τ, half-time and time to reach each percentage of steady state.',
    'shuimianhuifuzhiliang': 'Enter sleep duration, deep-sleep ratio and sleep-onset latency to compute a sleep-recovery index, assess recovery state and suggest the day’s training intensity.',
    'simulator-18': 'A high-altitude hypoxia adaptation simulator: model blood-oxygen and ventilation changes at different altitudes to understand altitude-adaptation physiology for training education.',
    'sleeping-bag-rating': 'An EN13537 sleeping-bag temperature-rating lookup: enter expected ambient temperature to recommend a suitable comfort/limit temperature bag for outdoor camping gear choice.',
    'speed-5': 'Enter initial velocity, final velocity, time and mass to compute acceleration, resultant force, displacement, kinetic-energy change and power output for sprint, cycling and throwing mechanics.',
    'speed-6': 'Enter lunge distance, front-foot displacement and completion time to compute average lunge speed, peak speed, acceleration and attack effect for fencing technique assessment.',
    'sports-calculator': 'A one-stop sports and outdoor calculator hub: running pace, heart-rate zones, cycling gear ratio, strength training, ski slope and pace-speed conversion.',
    'sports-reference': 'A one-stop sports and outdoor reference hub: climbing grades, sleeping-bag ratings, tent wind resistance, yoga poses, dive safety and fitness assessment.',
    'sports-schedule': 'A weekly workout-schedule generator: auto-build a week of training from goal (fat loss / muscle gain / endurance) and level, balancing intensity and recovery.',
    'sports-stats': 'A workout data statistics tool: log distance, pace and heart rate from running, cycling and other activities and generate trend charts for training management.',
    'stats-8': 'A soccer match statistics tool: enter possession, pass-success rate and shots to summarize team technique-tactics metrics for post-match analysis.',
    'strength-5': 'A weekly training-intensity distributor following the 80/20 polarized-training principle: allocate weekly training volume into low- and high-intensity and generate a daily plan.',
    'swimming-stroke-efficiency': 'Compute distance per stroke (DPS), stroke rate (SR) and the SWOLF efficiency index to assess swimming technique and economy.',
    'taiquandao-hengti-xiapi-defen': 'A taekwondo kick (roundhouse/axe) scoring tool: log effective strikes and scoring moves to compute scoring rate and technique-application distribution for targeted training.',
    'tent-wind-rating': 'Cross-reference the Beaufort wind scale with tent wind-resistance grades and give a suitable tent type and wind-safety advice by wind speed for camping tent choice and weather-risk assessment.',
    'tester-1': 'Enter body weight, movement type and reps-to-failure and combine bodyweight load ratios with the Epley and Brzycki formulas to estimate the movement 1RM and relative strength.',
    'tester-7': 'An endurance-test evaluator combining anaerobic threshold (AT) and VO2max to assess aerobic-endurance level, with training-zone advice and an endurance grade.',
    'tester-8': 'A maximal accumulated oxygen deficit (MAOD) test tool: estimate anaerobic capacity from an incremental-load test by computing accumulated oxygen deficit for anaerobic ability and lactate tolerance.',
    'time-30': 'Enter pool length, stroke count and completion time to compute the SWOLF index, distance per stroke, stroke rate and pace for swimming technical efficiency.',
    'time-31': 'Enter total match time and number of rounds to compute each round duration, rest time and per-round pacing strategy for wrestling rhythm and energy allocation.',
    'tongqibizhifenxi': 'Enter ventilation (VE) and oxygen uptake (VO2) at graded incremental loads to compute the VE/VO2 ventilatory equivalent, auto-detect the ventilatory threshold (VT) and assess the aerobic-anaerobic transition.',
    'training-load': 'Enter training load (rTSS), planned recovery time and personal adaptation coefficient to compute peak timing, current recovery phase and optimal next-session timing from a supercompensation model.',
    'training-planner': 'A personalized training-plan generator: build a tailored plan from goal, level and available time, with exercises, sets/reps and progressive loading.',
    'triathlon-transition': 'Enter swim, bike and run segment results and transition-zone times to compute total time and visualize each segment’s share for triathlon post-race review and weakness analysis.',
    'wangqiudefenlvfenxi': 'Enter serve-related data to compute ace rate, double-fault rate, first-serve in-rate, break-point save rate and a composite serve-efficiency index for serve performance and key-point ability.',
    'xuerusuanyuzhiceding': 'Fit a curve from heart-rate and blood-lactate data at graded-load testing to estimate lactate-threshold heart rate for endurance training-intensity zoning.',
    'yangmaiboxiaolv': 'Enter oxygen uptake (VO2) and heart rate (HR) to compute oxygen pulse (O2 pulse = VO2 ÷ HR), estimate stroke volume (SV) and assess cardiopulmonary and heart-pump efficiency.',
    'yoga-pose-generator': 'Choose difficulty and practice duration to randomly generate a yoga sequence with 30+ common poses and an order suggestion for home practice and class planning.',
    'youyonghuashuixiaolv-swolf': 'Enter stroke, pool length, single-length time and stroke count to compute SWOLF, distance per stroke, stroke rate and an efficiency grade for swimming economy and technique.',
    'yumaoqiushaqiuxiaolv': 'Enter smash average speed, count, direct points and errors to compute smash scoring rate, error rate, efficiency and an attack-efficiency composite for offensive quality.',
    'zhangpengfangfengxishu': 'Choose tent type, pole material and pole count to estimate maximum wind speed resistance, Beaufort grade and safe-camping advice as a wind-environment safety reference.',
}

DEFAULT_NOTE = [
    '本工具纯前端运行，数据不会上传到服务器',
    '建议在主流浏览器（Chrome/Safari/Firefox/Edge）中使用',
    '计算结果仅供参考，请以实际应用场景为准',
]


def load(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--apply', action='store_true')
    a = ap.parse_args()
    if not a.dry_run and not a.apply:
        ap.error('需指定 --dry-run 或 --apply')

    slugs = sorted(
        os.path.basename(f)[:-5]
        for f in glob.glob(os.path.join(TOOLS, '*.html'))
        if os.path.basename(f) != 'index.html'
    )
    missing_name = [s for s in slugs if s not in NAME]
    missing_intro = [s for s in slugs if s not in INTRO]
    if missing_name or missing_intro:
        print('!! NAME/INTRO 缺条目:', missing_name, missing_intro)
        return 1

    ov = load(OV)
    body = load(BODY)
    gis = load(GIS)

    chg_en = chg_ed = chg_body = added_body = added_gis = 0

    for slug in slugs:
        name = NAME[slug]
        intro = INTRO[slug]
        k = 'sports/' + slug

        e = ov.get(k)
        if not isinstance(e, dict):
            e = {'ind': 'sports'}
        if e.get('en') != name:
            chg_en += 1
        if e.get('ed') != intro:
            chg_ed += 1
        e['en'] = name
        e['ed'] = intro
        e.setdefault('ind', 'sports')
        ov[k] = e

        b = body.get(slug)
        if not isinstance(b, dict):
            b = {}
            added_body += 1
            print('  + sports-body.json 新增条目:', slug)
        if b.get('title') != name or b.get('h1') != name or b.get('intro') != intro:
            chg_body += 1
        b['title'] = name
        b['h1'] = name
        b['intro'] = intro
        en = b.get('en')
        if not isinstance(en, dict):
            en = {}
        en['title'] = name
        en['h1'] = name
        en['intro'] = intro
        b['en'] = en
        body[slug] = b

        g = gis.get(slug)
        if not isinstance(g, dict):
            g = {}
            added_gis += 1
            print('  + sports.json 新增条目:', slug)
        eu = g.get('en-US')
        if not isinstance(eu, dict):
            eu = {}
        eu['title'] = name
        eu['h1'] = name
        eu['intro'] = intro
        g['en-US'] = eu
        if 'note' not in g:
            g['note'] = list(DEFAULT_NOTE)
        gis[slug] = g

    # 孤儿键：body 中存在但全站无对应页面 -> 删除（保持数据源干净，与 science cycle 处理一致）
    all_basenames = {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(ROOT, 'tools', '*', '*.html'))}
    orphans = [key for key in list(body.keys()) if key not in all_basenames]
    for key in orphans:
        del body[key]
    print('\n--- 汇总 ---')
    print('sports 工具页:', len(slugs))
    print('_en_override  en 更新:', chg_en, ' ed 更新:', chg_ed)
    print('sports-body 更新:', chg_body, ' 新增:', added_body)
    print('sports.json 更新 en-US:', len(slugs), ' 新增条目:', added_gis)
    print('sports-body 孤儿键:', orphans)

    if a.dry_run:
        for s in slugs[:3]:
            print('\n预览 %s:\n  name = %r\n  intro= %r' % (s, NAME[s], INTRO[s]))
        return 0

    json.dump(ov, open(OV, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(body, open(BODY, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    json.dump(gis, open(GIS, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('\n已写入：_en_override.json(indent=1) / sports-body.json(indent=2) / sports.json(indent=2)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
