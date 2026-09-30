# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sports_apply import apply_tool

# ---------------- 1. 战术（攻防）视频分析 ----------------
apply_tool('analysis-19', '战术（攻防）视频分析', 'Tactical Attack/Defense Video Analysis', {
 '🎯 战术（攻防）视频分析': '🎯 Tactical Attack/Defense Video Analysis',
 '攻防片段标注': 'Structurally tag attack and defense clips from match video, tally attack-defense transitions and key rounds, and support coaching tactical review with clean statistics.',
 '进攻成功率 = 进攻成功次数 ÷ 进攻次数 ×100%；防守成功率 = 防守成功次数 ÷ 防守次数 ×100%。': 'Attack success rate = successful attacks ÷ total attacks × 100%; defense success rate = successful defenses ÷ total defenses × 100%.',
 '攻防转换次数统计相邻回合类型发生切换的频率，反映比赛攻守节奏的快慢。': "The attack-defense transition count measures how often consecutive rounds switch type, reflecting the pace of the match's attack and defense rhythm.",
 '评估口径：进攻成功率 ≥50% 且防守成功率 ≥60% 视为攻防表现良好。': 'Assessment rule: an attack success rate ≥50% together with a defense success rate ≥60% counts as good attack-defense performance.',
 '标注数据（每行「回合,进攻/防守,成功/失败」）': 'Tagged data (each line: "round,attack/defense,success/fail")',
 '1,进攻,成功\n2,进攻,失败\n3,防守,成功': '1,Attack,Success\n2,Attack,Fail\n3,Defense,Success',
 '战术统计': 'Tactical statistics',
 '📚 深度解析：比赛攻防片段统计与战术复盘': '📚 In-Depth: Match Attack/Defense Clip Statistics & Tactical Review',
 '赛后战术复盘': 'Post-match tactical review',
 '攻防效率统计': 'Attack/defense efficiency statistics',
 '训练重点定位': 'Locating training priorities',
 '进攻成功率 = 进攻成功次数 ÷ 进攻次数 ×100%；防守成功率同理；转换次数统计相邻回合类型切换的次数。': 'Attack success rate = successful attacks ÷ total attacks × 100%; the same applies to defense; the transition count tallies how often consecutive rounds switch type.',
 '8 个回合（进攻 4 成功 3、防守 4 成功 3）→ 进攻成功率 75.00%、防守成功率 75.00%、攻防转换 5 次、综合成功率 75.00%，评估为攻防表现良好。': 'Over 8 rounds (4 attacks with 3 successful, 4 defenses with 3 successful) → attack success rate 75.00%, defense success rate 75.00%, 5 attack-defense transitions, overall success rate 75.00%, assessed as good attack-defense performance.',
 '转换次数高说明什么？': 'What does a high transition count indicate?',
 '说明攻守节奏快、球权更迭频繁，对体能与阵型保持要求更高，可据此安排轮换与专项训练。': 'It indicates a fast attack-defense tempo with frequent changes of possession, placing higher demands on fitness and shape retention; use it to plan rotations and specific training.',
 '成功率口径如何统一？': 'How do you standardize the success-rate definition?',
 '需在赛前明确「成功」的定义（如进攻形成射门、防守夺回球权），同一场比赛全队保持同一口径才可比。': 'Define "success" before the match (e.g. an attack producing a shot, a defense recovering possession); only if the whole team keeps the same definition is a match comparable.',
 '战术（攻防）视频分析。体育竞技工具，帮助计算与分析运动数据。': 'Tactical Attack/Defense Video Analysis. A sports tool that helps calculate and analyze athletic data.',
 '1,进攻,成功': '1,Attack,Success',
})

# ---------------- 2. 滑雪坡度角度计算 ----------------
apply_tool('calc-angle-slope', '滑雪坡度角度计算（百分比度）', 'Ski Slope Angle & Grade Calculator', {
 '🗺️ 百分比计算器（运动）': '🗺️ Ski Slope Angle & Grade Calculator',
 '计算数值的百分比、占比、增长率等': 'Enter vertical drop and horizontal distance to convert a slope percentage into the slope angle, for ski-run difficulty grading and safety notes.',
 '滑雪坡度角度计算（百分比度）': 'Ski Slope Angle & Grade Calculator',
 '/ 滑雪坡度角度计算（百分比↔度）': '/ Ski Slope Angle & Grade Calculator',
 '百分比坡度 = tanθ × 100%': 'Percentage grade = tan θ × 100%',
 '📚 深度解析：百分比坡度计算器（运动）': '📚 In-Depth: Ski Slope Angle & Grade Calculator',
 '跑步/骑行坡度换算。': 'Slope conversion for running and cycling.',
 '野雪路线用落差与水平距算坡度，识别 >30° 雪坡的雪崩风险等级。': 'For backcountry routes, use vertical drop and horizontal distance to compute the slope and identify the avalanche-risk class of slopes over 30°.',
 '坡度角': 'Slope angle',
 '坡度=tan5°×100≈8.75%；10% 坡对应约 5.7°。': ' grade = tan 5° × 100 ≈ 8.75%; a 10% slope corresponds to about 5.7°.',
 '百分比坡含义？': 'What does a percentage grade mean?',
 '每水平 100 上升高度，如 8% 即百米升 8 米。': 'Rise per 100 horizontal units; 8% means 8 metres of rise over 100 metres.',
 '坡度角比百分比更直观？': 'Is the slope angle more intuitive than the percentage?',
 '工程常用百分比，滑手常用角度；>35° 属陡坡，救援与滑行难度陡增。': 'Engineering commonly uses the percentage while skiers commonly use degrees; over 35° is a steep slope where rescue and skiing difficulty rise sharply.',
})

# ---------------- 3. 力量（1RM/最大力量）换算 ----------------
apply_tool('convert-47', '力量（1RM/最大力量）换算', 'One-Rep Max (1RM) Estimator', {
 '🏋️ 力量（1RM/最大力量）换算': '🏋️ One-Rep Max (1RM) Estimator',
 '1RM 估算（Epley 公式：1RM = 重量 × (1 + 次数/30)）': 'A one-rep-max (1RM) estimator: enter a weight lifted for a given number of repetitions and estimate the single maximal repetition from estimation formulas for strength-load setting.',
 '一次最大重复估算（Epley 公式）1RM = 训练重量 × (1 + 重复次数 ÷ 30)；Brzycki 对照 1RM = 重量 × 36 ÷ (37 − 次数)；训练强度占 1RM 比例 = 训练重量 ÷ 1RM × 100%。': 'One-rep-max estimate (Epley formula) 1RM = training weight × (1 + reps ÷ 30); Brzycki comparison 1RM = weight × 36 ÷ (37 − reps); training intensity as a share of 1RM = training weight ÷ 1RM × 100%.',
 '完成次数': 'Reps completed',
 '📚 深度解析：力量（1RM/最大力量）换算': '📚 In-Depth: One-Rep Max (1RM) Estimator',
 '由多次重复推单次最大（': 'Estimate the one-rep max from multiple repetitions (',
 '力量周期用多次数推 1RM 安排负荷': 'During a strength cycle, estimate the 1RM from higher reps to set the load ',
 '，避免每次实测 1RM 的疲劳风险。': ' and avoid the fatigue risk of testing the 1RM every session.',
 '100 kg 做 5 次 → 1RM=100×(1+5/30)=116.7 kg（Epley 公式）。': '100 kg for 5 reps → 1RM = 100 × (1 + 5/30) = 116.7 kg (Epley formula).',
 'Epley 与 Brzycki？': 'Epley versus Brzycki?',
 '两式近似，次数越少估算越准。': 'The two formulas are close; the fewer the reps the more accurate the estimate.',
 '不同公式结果差很多怎么办？': 'What if different formulas give very different results?',
 'Epley 偏乐观、Brzycki 偏保守，固定选一公式纵向比较，别混用导致数据漂移。': 'Epley tends to be optimistic and Brzycki conservative; pick one formula and compare longitudinally rather than mixing them and letting the data drift.',
 '力量（1RM/最大力量）换算。体育竞技工具，帮助计算与分析运动数据。': 'One-Rep Max (1RM) Estimator. A sports tool that helps calculate and analyze athletic data.',
})

# ---------------- 4. 铁人三项转换时间（游泳/骑车/跑步） ----------------
apply_tool('convert-time', '铁人三项转换时间（游泳/骑车/跑步）', 'Triathlon Transition Time Calculator', {
 '🏊 铁人三项转换时间（游泳/骑车/跑步）': '🏊 Triathlon Transition Time Calculator',
 '铁人三项总完赛时间 = 游泳 + 骑车 + 跑步': 'A triathlon transition-time calculator: sum swim, bike and run segment times with transition times to get the total time and each segment’s share for race-pace analysis.',
 '总时长 = 各段秒数之和；折合分钟 = 总秒数 ÷ 60；折合小时 = 总秒数 ÷ 3600；时分秒显示中，小时 = 向下取整(总秒 ÷ 3600)、分钟 = 向下取整(总秒 模 3600 ÷ 60)、秒 = 四舍五入(总秒 模 60)。': 'Total = sum of segment seconds; minutes = total seconds ÷ 60; hours = total seconds ÷ 3600; in the h:min:sec display, hours = floor(total seconds ÷ 3600), minutes = floor(total seconds mod 3600 ÷ 60), seconds = round(total seconds mod 60).',
 '游泳 (秒)': 'Swim (sec)',
 '骑车 (秒)': 'Bike (sec)',
 '跑步 (秒)': 'Run (sec)',
 '📚 深度解析：铁人三项转换时间（游泳/骑车/跑步）': '📚 In-Depth: Triathlon Transition Time Calculator',
 '核算 T1/T2 转换耗时。': 'Account for T1/T2 transition time.',
 '铁三按三项成绩算转换时间占比，识别转换短板针对性练换项。': 'In triathlon, compute the transition share from the three segment times, identify the transition weakness and train it specifically.',
 'T1（泳→骑）目标 ≤90 s，T2（骑→跑）≤60 s；慢转换可丢名次。': 'Target T1 (swim → bike) ≤90 s and T2 (bike → run) ≤60 s; slow transitions can cost places.',
 '转换怎么练？': 'How should transitions be trained?',
 '专项模拟换项，减少多余动作。': 'Simulate transitions specifically and cut out unnecessary movements.',
 '转换训练常被忽视？': 'Is transition training often neglected?',
 '常被忽略却直接影响总时，专项换项演练性价比高，精英间差距常在换项。': 'It is often overlooked yet directly affects total time; targeted transition practice gives a high return, and among elites the difference is often in transition.',
 '铁人三项转换时间（游泳/骑车/跑步）。体育竞技工具，帮助计算与分析运动数据。': 'Triathlon Transition Time Calculator. A sports tool that helps calculate and analyze athletic data.',
})

# ---------------- 5. 瑜伽体式随机生成（内置常见体式） ----------------
apply_tool('generator-random-3', '瑜伽体式随机生成（内置常见体式）', 'Yoga Pose Generator', {
 '🎲 瑜伽体式随机生成（内置常见体式）': '🎲 Yoga Pose Sequence Generator',
 '内置常见体式': 'Generate a yoga sequence from a built-in pose library with tips, adjustable duration and intensity, for home practice planning — generated locally.',
 '瑜伽体式序列生成：从内置体式库（站姿/前屈/后弯/扭转/倒立/休息）按强度与时长随机抽取并排序，生成可跟随的居家练习序列。': 'Yoga sequence generation: randomly draw and order poses from a built-in library (standing / forward bend / backbend / twist / inversion / rest) by intensity and duration to produce a follow-along home practice sequence.',
 '📚 深度解析：瑜伽体式随机生成（内置常见体式）': '📚 In-Depth: Yoga Pose Sequence Generator',
 '编排练习随机体式序列。': 'Build a practice by randomizing a pose sequence.',
 '晨间唤醒按难度与时长生成流瑜伽序列，避免每次重复相同体式导致练习盲区。': 'For a morning wake-up, generate a vinyasa sequence by difficulty and duration to avoid repeating the same poses and creating practice blind spots.',
 '随机序列如 山式→下犬式→战士二→婴儿式（仅演示，非医疗建议）。': "A random sequence such as Mountain → Downward Dog → Warrior II → Child's pose (illustration only, not medical advice).",
 '新手能用？': 'Can beginners use it?',
 '需量力，避免勉强高难体式。': 'Work within your ability and avoid forcing difficult poses.',
 '序列会考虑热身与放松吗？': 'Does the sequence account for warm-up and cool-down?',
 '生成按顺序前置站姿热身、后置仰卧放松，保证序列结构完整不突兀。': 'Generation puts standing warm-ups first and supine relaxation last, keeping the sequence structurally complete and not abrupt.',
 '瑜伽体式随机生成（内置常见体式）。体育竞技工具，帮助计算与分析运动数据。': 'Yoga Pose Generator. A sports tool that helps calculate and analyze athletic data.',
})

# ---------------- 6. 平衡（闭眼单脚）时长 ----------------
apply_tool('pingheng-biyandanjiao-shichang', '平衡（闭眼单脚）时长', 'Balance (Eyes-Closed Single-Leg Stand) Timer', {
 '⏱️ 平衡（闭眼单脚）时长': '⏱️ Balance (Eyes-Closed Single-Leg Stand) Timer',
 '按实测闭眼单脚站立时长与年龄，对照年龄常模评估平衡能力等级，给出训练建议。': 'A balance (eyes-closed single-leg stand) duration recorder: log stand time and compare against norms to assess balance ability for rehab and fitness testing.',
 '年龄常模期望(s) = (70 − 年龄) × 0.4；实测/常模≥1.5 优、≥1.0 良、否则弱': 'Age norm expected (s) = (70 − age) × 0.4; measured/norm ≥1.5 excellent, ≥1.0 good, otherwise weak',
 '闭眼单脚站立时长是平衡能力常用指标：年龄常模期望≈(70−年龄)×0.4秒。实测/常模比≥1.5为优、≥1.0为良、否则偏弱。比值越高平衡越好，偏弱者建议加强本体感觉与核心稳定训练。': 'Eyes-closed single-leg stand time is a common balance indicator: the age-norm expectation ≈ (70 − age) × 0.4 s. A measured/norm ratio ≥1.5 is excellent, ≥1.0 good, otherwise weak. The higher the ratio the better the balance; those on the weaker side should strengthen proprioception and core stability.',
 '闭眼单脚时长 (s)': 'Eyes-closed single-leg time (s)',
 '💡 年龄常模 ≈ (70−年龄)×0.4 s；实测/常模 ≥1.5 优、≥1.0 良。': '💡 Age norm ≈ (70 − age) × 0.4 s; measured/norm ≥1.5 excellent, ≥1.0 good.',
 '📚 深度解析：平衡（闭眼单脚）时长': '📚 In-Depth: Balance (Eyes-Closed Single-Leg Stand) Timer',
 '闭眼单脚站测平衡。': 'The eyes-closed single-leg stand tests balance.',
 '防伤筛查用闭眼单脚站时长评估本体感觉，时间短提示踝膝不稳风险。': 'Injury-prevention screening uses eyes-closed single-leg stand time to assess proprioception; a short time signals ankle and knee instability risk.',
 '成绩': 'Score',
 '闭眼单脚站立 ≥30 s 为平衡良好；老年人 <10 s 提示跌倒风险。': 'An eyes-closed single-leg stand of ≥30 s indicates good balance; under 10 s in older adults signals fall risk.',
 '睁眼差异？': 'What about the difference with eyes open?',
 '睁眼借视觉，闭眼更依赖前庭与本体感觉。': 'With eyes open you rely on vision; with eyes closed you depend more on the vestibular system and proprioception.',
 '睁眼闭眼差大说明啥？': 'What does a large eyes-open/eyes-closed gap indicate?',
 '差大提示依赖视觉代偿、本体感觉弱，易在不平地面崴脚，应练平衡。': 'A large gap indicates reliance on visual compensation and weak proprioception, making ankle sprains more likely on uneven ground; balance training is needed.',
 '平衡（闭眼单脚）时长。体育竞技工具，帮助计算与分析运动数据。': 'Balance (Eyes-Closed Single-Leg Stand) Timer. A sports tool that helps calculate and analyze athletic data.',
 '数值 A (min)': 'Value A (min)',
 '数值 B (min)': 'Value B (min)',
})

# ---------------- 7. 乒乓球（相持/发球）得分 ----------------
apply_tool('pingpangqiu-xiangchi-faqiu-defen', '乒乓球（相持/发球）得分', 'Table Tennis Rally / Serve Scoring', {
 '⚽ 乒乓球（相持/发球）得分': '⚽ Table Tennis Rally / Serve Scoring Analysis',
 '按相持与发球得分计算乒乓球单局总分与平均得分，用于技术结构分析。': 'A table-tennis rally/serve scoring tool: log rally and serve-round points to compute scoring rate and key-point performance for technique-tactics analysis.',
 '总分 = 相持得分 + 发球得分；平均分 = 总分 ÷ 2': 'Total = rally points + serve points; average = total ÷ 2',
 '乒乓球得分由相持与发球等环节构成：总分=相持+发球，平均=总分÷2，差距=|相持−发球|。据此分析得分结构，优化技战术侧重与训练安排。': 'Table-tennis points come from phases such as rallies and serves: total = rally + serve, average = total ÷ 2, gap = |rally − serve|. Use these to analyze the scoring structure and optimize the technique-tactics emphasis and training plan.',
 '相持得分': 'Rally points',
 '发球得分': 'Serve points',
 '💡 总分 = 相持 + 发球；平均分 = 总分 ÷ 2。': '💡 Total = rally + serve; average = total ÷ 2.',
 '📚 深度解析：乒乓球（相持/发球）得分': '📚 In-Depth: Table Tennis Rally / Serve Scoring',
 '11 分制得分统计。': 'Scoring statistics for the 11-point format.',
 '对抗训练统计发球直接得分率与相持回合胜率，定位发球抢攻与相持短板。': 'In competitive drills, tally the direct serve-scoring rate and the rally win rate to locate weaknesses in serve-attack and rally play.',
 '发球得分率=发球直接得分/发球总数；相持得分率=相持赢球/相持总数。': 'Serve scoring rate = direct serve points / total serves; rally scoring rate = rally wins / total rallies.',
 '11 分制？': 'The 11-point format?',
 '先到 11 且领先 2 分胜。': 'Win by reaching 11 first with a two-point lead.',
 '发球得分率多少算优秀？': 'What serve-scoring rate counts as excellent?',
 '业余顶尖约 15–25%，职业更高；更关键看发球后第三板衔接得分率。': 'Around 15-25% for top amateurs, higher for professionals; the more telling metric is the scoring rate on the third ball after the serve.',
 '乒乓球（相持/发球）得分。体育竞技工具，帮助计算与分析运动数据。': 'Table Tennis Rally / Serve Scoring. A sports tool that helps calculate and analyze athletic data.',
 '相持': 'Rally',
 '发球': 'Serve',
})

# ---------------- 8. 损伤（预防/康复）动作 ----------------
apply_tool('rehab-motion', '损伤（预防/康复）动作', 'Injury Prevention & Rehab Exercise Library', {
 '🦿 损伤（预防/康复）动作': '🦿 Injury Prevention & Rehab Exercise Library',
 '按体重与动作重复次数估算康复动作总负荷、单组时长与渐进增量，指导安全进阶。': 'An injury-prevention and rehab exercise library: recommend preventive or rehabilitative movements by injury site and rehab phase and track completion for injury management.',
 '总负荷 = 体重 × 次数；单组时长 ≈ 次数 × 3s；周增量 ≈ 总负荷 × 10%': 'Total load = body weight × reps; set duration ≈ reps × 3 s; weekly increment ≈ total load × 10%',
 '康复动作负荷以体重与重复次数估算：总负荷(kg)=体重×次数，单组建议时长≈次数×3秒，渐进增量≈总负荷×10%（每周）。循序增加负荷可促进组织适应，避免过度训练导致再损伤。': 'Rehab exercise load is estimated from body weight and reps: total load (kg) = body weight × reps, recommended set duration ≈ reps × 3 s, progressive increment ≈ total load × 10% (weekly). Gradually increasing the load promotes tissue adaptation and avoids re-injury from overtraining.',
 '重复次数 (次)': 'Repetitions (reps)',
 '💡 总负荷 = 体重 × 次数；单组 ≈ 次数 × 3s；周增量 ≈ 总负荷 × 10%。': '💡 Total load = body weight × reps; set ≈ reps × 3 s; weekly increment ≈ total load × 10%.',
 '📚 深度解析：损伤（预防/康复）动作': '📚 In-Depth: Injury Prevention & Rehab Exercise Library',
 '康复与预防训练动作库。': 'A rehab and prevention exercise library.',
 '膝伤康复按阶段选动作库，从激活到负重渐进防过早回归致再伤。': 'For knee-injury rehab, pick from the library by phase, progressing from activation to loading to avoid returning too early and re-injuring.',
 '动作': 'Exercise',
 '如靠墙静蹲（膝康复）、臀桥（髋稳定）；按阶段递增负荷。': 'For example wall sits (knee rehab) and glute bridges (hip stability); increase the load by phase.',
 '疼了还练？': 'Should I keep training when it hurts?',
 '锐痛停，酸胀可接受，遵医嘱。': 'Stop on sharp pain; a dull ache is acceptable; follow medical advice.',
 '康复动作越多越好？': 'Are more rehab exercises better?',
 '重质量与阶段匹配，过量或跳阶反而延时愈合并增加再伤风险。': 'Quality and phase-matching matter; too much or skipping phases actually delays healing and raises the risk of re-injury.',
 '损伤（预防/康复）动作。体育竞技工具，帮助计算与分析运动数据。': 'Injury Prevention & Rehab Exercise Library. A sports tool that helps calculate and analyze athletic data.',
 '预防': 'Prevention',
 '康复': 'Rehabilitation',
})

# ---------------- 9. 柔韧（前屈/侧屈）进步 ----------------
apply_tool('rouren-qianqu-cequ-jinbu', '柔韧（前屈/侧屈）进步', 'Flexibility (Forward / Side Bend) Progress Tracker', {
 '⚽ 柔韧（前屈/侧屈）进步': '⚽ Flexibility (Forward / Side Bend) Progress Tracker',
 '按训练前后坐位体前屈成绩计算柔韧进步量与相对提升率，用于训练效果追踪。': 'A flexibility (forward/side bend) progress tracker: log sit-and-reach and similar tests, convert to improvement margin and rating for flexibility training tracking.',
 '柔韧进步 = 后测 − 前测；相对提升 = 进步 ÷ 前测 × 100%': 'Flexibility improvement = post-test − pre-test; relative gain = improvement ÷ pre-test × 100%',
 '柔韧素质以坐位体前屈(cm)衡量：进步=后测−前测，相对提升=进步÷前测。正值表示柔韧改善，用于训练前后效果对比。': 'Flexibility is measured by the sit-and-reach (cm): improvement = post-test − pre-test, relative gain = improvement ÷ pre-test. A positive value means improved flexibility, used to compare pre- and post-training effects.',
 '前测前屈 (cm)': 'Pre-test forward bend (cm)',
 '后测前屈 (cm)': 'Post-test forward bend (cm)',
 '💡 进步 = 后测 − 前测；相对提升 = 进步 ÷ 前测 × 100%。': '💡 Improvement = post-test − pre-test; relative gain = improvement ÷ pre-test × 100%.',
 '📚 深度解析：柔韧（前屈/侧屈）进步': '📚 In-Depth: Flexibility (Forward / Side Bend) Progress Tracker',
 '坐位体前屈记录进步。': 'Track progress with the sit-and-reach test.',
 '久坐人群记录体前屈与侧屈月度变化，量化柔韧改善验证拉伸方案有效。': 'Sedentary people can log monthly forward- and side-bend changes to quantify flexibility gains and verify the effectiveness of a stretching plan.',
 '初始 −2 cm、8 周后 +8 cm → 进步 10 cm（坐位体前屈）。': 'Initial −2 cm and +8 cm after 8 weeks → a 10 cm improvement (sit-and-reach).',
 '每天拉更有效？': 'Is stretching every day more effective?',
 '规律温和拉伸+热身更佳，避免弹振拉伤。': 'Regular gentle stretching plus a warm-up is better; avoid ballistic stretching that strains muscles.',
 '柔韧进步慢正常吗？': 'Is slow flexibility progress normal?',
 '神经适应快、结构改变慢，前 2–4 周多为暂时性改善，持续 8 周以上才稳定。': 'Neural adaptation is fast while structural change is slow, so the first 2-4 weeks are mostly temporary gains, stabilizing only after 8 weeks or more.',
 '柔韧（前屈/侧屈）进步。体育竞技工具，帮助计算与分析运动数据。': 'Flexibility (Forward / Side Bend) Progress Tracker. A sports tool that helps calculate and analyze athletic data.',
 '前屈': 'Forward bend',
 '侧屈': 'Side bend',
})

# ---------------- 10. 高原（低氧）适应模拟 ----------------
apply_tool('simulator-18', '高原（低氧）适应模拟', 'High-Altitude Hypoxia Adaptation Simulator', {
 '🧪 高原（低氧）适应模拟': '🧪 High-Altitude Hypoxia Adaptation Simulator',
 '低氧': 'A high-altitude hypoxia adaptation simulator: model blood-oxygen and ventilation changes at different altitudes to understand altitude-adaptation physiology for training education.',
 '伯努利试验蒙特卡洛模拟：每次试验独立以概率 p 判定成功，进行 n 次；实际频率 = 成功次数 / n；理论概率为 p；实际频率与理论值之差即抽样偏差，其标准误为 sqrt(p*(1-p)/n)，随 n 增大而减小。': 'Bernoulli-trial Monte-Carlo simulation: each trial independently succeeds with probability p, run n times; observed frequency = successes / n; the theoretical probability is p; the difference between the observed frequency and the theoretical value is the sampling deviation, with standard error sqrt(p*(1-p)/n), which shrinks as n grows.',
 '📚 深度解析：高原（低氧）适应模拟': '📚 In-Depth: High-Altitude Hypoxia Adaptation Simulator',
 '模拟低氧训练刺激。': 'Simulate hypoxic training stimulus.',
 '登山前模拟目标海拔血氧适应，预演何时需补氧与降速。': 'Before a climb, simulate blood-oxygen adaptation at the target altitude to rehearse when oxygen supplementation and slowing down are needed.',
 '间歇低氧（IHT）设 FiO₂≈15% 模拟约 2500 m，刺激红细胞生成。': 'Intermittent hypoxic training (IHT) sets FiO₂ ≈ 15% to simulate about 2500 m and stimulate red-blood-cell production.',
 '替代实地高原？': 'Does it replace real altitude?',
 '部分，但实地更综合。': 'Partly, but real altitude is more comprehensive.',
 '模拟能替代实地适应？': 'Can simulation replace on-site acclimatization?',
 '可预演反应但无法替代真高原红细胞增生，仍需现场渐进适应。': 'It can rehearse the response but cannot replace the red-blood-cell proliferation at real altitude; on-site gradual acclimatization is still required.',
 '高原（低氧）适应模拟。体育竞技工具，帮助计算与分析运动数据。': 'High-Altitude Hypoxia Adaptation Simulator. A sports tool that helps calculate and analyze athletic data.',
})
