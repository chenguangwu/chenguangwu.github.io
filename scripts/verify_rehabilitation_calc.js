#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  // 注：rehabilitation/analysis-time 已于 2026-09-19 改为 TOOLBOX-REDIRECT 存根（重定向到同义真工具），不再是工具页，用例移除。
{
  "slug": "rehabilitation/asia-impairment-scale",
  "inputs": {
    "sens_C2_lt_l": "2",
    "sens_C2_lt_r": "2",
    "sens_C2_pp_l": "2",
    "sens_C2_pp_r": "2",
    "sens_C3_lt_l": "2",
    "sens_C3_lt_r": "2",
    "sens_C3_pp_l": "2",
    "sens_C3_pp_r": "2",
    "sens_C4_lt_l": "2",
    "sens_C4_lt_r": "2",
    "sens_C4_pp_l": "2",
    "sens_C4_pp_r": "2",
    "sens_C5_lt_l": "2",
    "sens_C5_lt_r": "2",
    "sens_C5_pp_l": "2",
    "sens_C5_pp_r": "2",
    "sens_C6_lt_l": "2",
    "sens_C6_lt_r": "2",
    "sens_C6_pp_l": "2",
    "sens_C6_pp_r": "2",
    "sens_C7_lt_l": "2",
    "sens_C7_lt_r": "2",
    "sens_C7_pp_l": "2",
    "sens_C7_pp_r": "2",
    "sens_C8_lt_l": "2",
    "sens_C8_lt_r": "2",
    "sens_C8_pp_l": "2",
    "sens_C8_pp_r": "2",
    "sens_T1_lt_l": "2",
    "sens_T1_lt_r": "2",
    "sens_T1_pp_l": "2",
    "sens_T1_pp_r": "2",
    "sens_T2_lt_l": "2",
    "sens_T2_lt_r": "2",
    "sens_T2_pp_l": "2",
    "sens_T2_pp_r": "2",
    "sens_T3_lt_l": "2",
    "sens_T3_lt_r": "2",
    "sens_T3_pp_l": "2",
    "sens_T3_pp_r": "2",
    "sens_T4_lt_l": "2",
    "sens_T4_lt_r": "2",
    "sens_T4_pp_l": "2",
    "sens_T4_pp_r": "2",
    "sens_T5_lt_l": "2",
    "sens_T5_lt_r": "2",
    "sens_T5_pp_l": "2",
    "sens_T5_pp_r": "2",
    "sens_T6_lt_l": "2",
    "sens_T6_lt_r": "2",
    "sens_T6_pp_l": "2",
    "sens_T6_pp_r": "2",
    "sens_T7_lt_l": "2",
    "sens_T7_lt_r": "2",
    "sens_T7_pp_l": "2",
    "sens_T7_pp_r": "2",
    "sens_T8_lt_l": "2",
    "sens_T8_lt_r": "2",
    "sens_T8_pp_l": "2",
    "sens_T8_pp_r": "2",
    "sens_T9_lt_l": "2",
    "sens_T9_lt_r": "2",
    "sens_T9_pp_l": "2",
    "sens_T9_pp_r": "2",
    "sens_T10_lt_l": "2",
    "sens_T10_lt_r": "2",
    "sens_T10_pp_l": "2",
    "sens_T10_pp_r": "2",
    "sens_T11_lt_l": "2",
    "sens_T11_lt_r": "2",
    "sens_T11_pp_l": "2",
    "sens_T11_pp_r": "2",
    "sens_T12_lt_l": "2",
    "sens_T12_lt_r": "2",
    "sens_T12_pp_l": "2",
    "sens_T12_pp_r": "2",
    "sens_L1_lt_l": "2",
    "sens_L1_lt_r": "2",
    "sens_L1_pp_l": "2",
    "sens_L1_pp_r": "2",
    "sens_L2_lt_l": "2",
    "sens_L2_lt_r": "2",
    "sens_L2_pp_l": "2",
    "sens_L2_pp_r": "2",
    "sens_L3_lt_l": "2",
    "sens_L3_lt_r": "2",
    "sens_L3_pp_l": "2",
    "sens_L3_pp_r": "2",
    "sens_L4_lt_l": "2",
    "sens_L4_lt_r": "2",
    "sens_L4_pp_l": "2",
    "sens_L4_pp_r": "2",
    "sens_L5_lt_l": "2",
    "sens_L5_lt_r": "2",
    "sens_L5_pp_l": "2",
    "sens_L5_pp_r": "2",
    "sens_S1_lt_l": "2",
    "sens_S1_lt_r": "2",
    "sens_S1_pp_l": "2",
    "sens_S1_pp_r": "2",
    "sens_S2_lt_l": "2",
    "sens_S2_lt_r": "2",
    "sens_S2_pp_l": "2",
    "sens_S2_pp_r": "2",
    "sens_S3_lt_l": "2",
    "sens_S3_lt_r": "2",
    "sens_S3_pp_l": "2",
    "sens_S3_pp_r": "2",
    "sens_S4-S5_lt_l": "2",
    "sens_S4-S5_lt_r": "2",
    "sens_S4-S5_pp_l": "2",
    "sens_S4-S5_pp_r": "2",
    "motor_0_l": "5",
    "motor_0_r": "5",
    "motor_1_l": "5",
    "motor_1_r": "5",
    "motor_2_l": "5",
    "motor_2_r": "5",
    "motor_3_l": "5",
    "motor_3_r": "5",
    "motor_4_l": "5",
    "motor_4_r": "5",
    "motor_5_l": "5",
    "motor_5_r": "5",
    "motor_6_l": "5",
    "motor_6_r": "5",
    "motor_7_l": "5",
    "motor_7_r": "5",
    "motor_8_l": "5",
    "motor_8_r": "5",
    "motor_9_l": "5",
    "motor_9_r": "5"
  },
  "expect": [
    "感觉平面 S4-S5 · 运动平面 S1 · AIS E（正常）· 感觉总分 224/224 · 运动总分 100/100"
  ],
  "ref": "门诊记录：全量注入 28 皮节×4 位点（sens_*_lt_l/pp_l/lt_r/pp_r）+ 10 组关键肌×双侧（motor_i_l/r）共 132 键，感觉 224/224、运动 100/100 全正常 ⇒ AIS E，门诊记录输出平面与总分（与 applyAsiaPreset('normal') 等价）。注意本页 select 由 renderSensory()/renderMotor() 运行期拼 innerHTML 生成、**不在静态源码里**，桩取不到默认值 ⇒ parseInt('')=NaN，默认态既非 E 也拿不到有效总分，零交集。旧 expect 锚在桩假象「NaN/112」上（分母 112 系量纲错，28×4×2=224），已修。"
},
{
  "slug": "rehabilitation/adl-task-breakdown",
  "inputs": {
    "activitySelect": "进食",
    "levelSelect": "verbal"
  },
  "expect": [
    "🍴 进食（口语提示）· 训练步骤 10 步 · 所需能力：上肢功能、手眼协调、口腔运动、吞咽功能"
  ],
  "ref": "门诊记录（该页原为零用例，本次新增）：activitySelect/levelSelect 的值是纯中文键，inputs 可直接注入；进食任务共 10 步、四项能力，训练等级取 verbal ⇒「口语提示」。默认态 activitySelect 为空 ⇒ adlData[''] 为 undefined，showSteps() 里取 data.icon 直接抛错、不产生门诊记录，零交集。"
},
{
  "slug": "rehabilitation/assistive-device-fitting",
  "inputs": {
    "orthoPart": "kfo"
  },
  "expect": [
    "重量约1.5-3kg"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rehabilitation/assistive-device-fitting",
  "inputs": {
    "wcHeight": "170",
    "wcWeight": "110",
    "wcSitHeight": "85",
    "wcHipWidth": "40",
    "wcCalfLength": "40"
  },
  "expect": [
    "身高 170cm · 体重 110kg · 坐高 85cm · 臀宽 40cm · 小腿长 40cm → 座宽 42cm · 座深 37cm · 座高 45cm · 靠背高 40cm · 承重 ≥165kg"
  ],
  "ref": "门诊记录：座宽=臀宽 40+2=42；座深=小腿长 40−3=37；座高=小腿长 40+5=45；靠背高=max(坐高 85−座高 45,25)=40；承重=ceil(110×1.5)=165。默认态 wcHeight 为空 ⇒ calcWheelchair 早退回「请输入身高、体重和臀宽」、不产生门诊记录，零交集。（本页三个 tab 各有独立计算函数，上方 orthoPart 用例覆盖矫形器分支，本条覆盖轮椅分支。）"
},
{
  "slug": "rehabilitation/berg-balance-scale",
  "checks": [
    "4"
  ],
  "expect": [
    "56 / 56分（已完成14/14项）"
  ],
  "ref": "14 项各按 4 分（checks 注入 input[name=itemN]:checked ⇒ value=4）⇒ 总分 56、已完成 14/14，串随勾选数/分值连续变化。默认态 answered=0 ⇒ 早退输出「请先为测试项目评分」，不含该串。原 expect「站立位原地360度转身」是 bbsItems 列表项名，默认恒在（常量型逃生项）。"
},
{
  "slug": "rehabilitation/boston-aphasia",
  "clicks": [
    "selectGrade(3)"
  ],
  "expect": [
    "3级（中度）· 交流能力：日常交流基本可行，但效率和质量降低"
  ],
  "ref": "门诊记录：clicks 调 selectGrade(3)（REC 加 typeof grade==='number' && bostonGrades[grade] 守卫，兜底无参调用不覆盖），输出 Boston 失语症 3 级（中度）与其交流能力原文。默认态 querySelectorAll('.ref-card') 只渲染选项卡片、不产生 note ⇒ blob 无该串，零交集。"
},
{
  "slug": "rehabilitation/fim-scale",
  "clicks": [
    "var __m={};for(var i=0;i<18;i++)__m['fim_'+i]='4';var __g=document.getElementById;document.getElementById=function(id){if(__m[id]!==undefined)return {value:__m[id],checked:false};return __g.call(document,id);};calcScore()"
  ],
  "expect": [
    "【FIM 功能独立性评定（18 项 · 运动 13 + 认知 5）】 结果：总分 72/126（运动 52/91、认知 20/35）→ 分级：轻度依赖",
    "康复预期：预计可提升约 22 分（预期出院 94 分）；运动独立率 57%、认知独立率 57%"
  ],
  "ref": "门诊记录（EMR note）：18 项下拉 `fim_0..17` 由 renderItems() 动态生成、stub 中不存在，故 clicks 覆写 getElementById 统一给 4 分 ⇒ 运动 13×4=52/91、认知 5×4=20/35、总分 72 ⇒ 72≥72 落「轻度依赖」；康复预期 total<80 分支 20+(80-72)×0.3=22.4→22 分、预期出院 94。默认态 18 项全 7（满分 126）⇒「完全独立」，与本用例零交集。"
},
{
  "slug": "rehabilitation/flacc-scale",
  "checks": [
    "2"
  ],
  "expect": [
    "【FLACC 儿童疼痛行为评估（5 项 · 0–10）】 结果：总分 10/10 → 分级：重度疼痛",
    "各项目得分：面部表情 2/2、腿部活动 2/2、活动度 2/2、哭闹 2/2、可安慰性 2/2；处理：强效镇痛（阿片类），必要时静脉给药"
  ],
  "ref": "门诊记录：5 项各勾 2 分（checks 注入 :checked ⇒ value=2）⇒ 总分 10 ≥7 落「重度疼痛」；处理建议取重度分支（阿片类、必要时静脉、1-2 小时复评）。默认态未勾选 ⇒ allSelected=false ⇒ showToast 后 return，不渲染结果，与本用例零交集。"
},
{
  "slug": "rehabilitation/gait-analysis",
  "inputs": {
    "cycleTime": "1.0",
    "stanceTime": "0.75",
    "doubleStance": "0.2",
    "cadence": "110",
    "stepLength": "0.7",
    "stanceTime2": "0.72"
  },
  "ref": "门诊记录：cycle=1.0、stance=0.75 ⇒ 支撑 75.0%/摆动 25.0%、比 3.00 ⇒「支撑相明显延长」（>70%）；cadence 110 × stepLen 0.7 ⇒ 步速 1.28 m/s；双支撑 0.2s/20%、对侧 0.72 vs 0.75 ⇒ 对称差异 4.0%。默认态 cycle/stance 为空 ⇒ 早退提示，与本用例零交集。",
  "expect": [
    "【步态时空参数分析】 结果：步态周期 1 s、支撑相 0.75 s → 支撑相占比 75.0%、摆动相 25.0%、支撑/摆动比 3.00 → 判定：支撑相明显延长 步频 110 步/分、步长 0.7 cm、双支撑相 0.2 s、对侧支撑相 0.72 s；正常参考：支撑相 58–62%、双支撑相约占周期 20% 临床提示：支撑相延长：常见于负重疼痛、下肢肌力下降、平衡信心不足或对侧摆动相缩短；建议减痛步态训练、髋膝伸肌力量训练与平衡训练，配合减重支持或助行器具。 评估日期：__________ 评估者：__________ （自评/筛查量表，结果仅供临床沟通参考，不作为诊断依据）"
  ]
},
{
  "slug": "rehabilitation/mmse-scoring",
  "checks": [
    "1"
  ],
  "expect": [
    "总分 30/30 → 认知功能正常 · 定向力 10/10 · 记忆力 3/3 · 注意力/计算 5/5 · 回忆力 3/3 · 语言力 9/9"
  ],
  "ref": "门诊记录：30 项全选「正确」（checks 注入 input[name=qN]:checked ⇒ value=1，页面按 sel.value==='1' 计数）⇒ total=30 落 ≥27 档「认知功能正常」，同时打印五个领域满分。默认态 total=0 ⇒ 输出「总分 0/30 → 重度认知障碍」，零交集。"
},
{
  "slug": "rehabilitation/mmt-grading",
  "checks": [
    "5"
  ],
  "expect": [
    "MMT 5 级（正常）· 正常肌力比例 100%"
  ],
  "ref": "门诊记录：checks 注入 input[name=grade]:checked ⇒ value=5，evaluate() 读选中项后 REC 捕获分级，输出「MMT 5 级（正常）· 正常肌力比例 100%」。默认态 evaluate() 读不到选中项直接 return、不产生 note ⇒ 零交集。"
},
{
  "slug": "rehabilitation/nine-hole-peg",
  "inputs": {
    "gender": "female",
    "ageGroup": "70-79",
    "domTime": "30",
    "nonDomTime": "34"
  },
  "expect": [
    "【九孔柱插板试验（Nine-Hole Peg Test · 手精细操作）】 结果：年龄组 70-79 · 女 → 优势手 30.0 秒（参考 19.5±3.5 秒，Z=3.00）分级：中度异常；非优势手 34.0 秒（参考 21.5±4.0 秒）→ 重度异常",
    "偏离参考值 +53.8%"
  ],
  "ref": "门诊记录：70-79 岁女性参考 19.5±3.5 秒 ⇒ 30.0 秒超 +3SD（Z=3.00）但不超过 ref+3SD 的上界判定（<= ref+3SD 归「中度异常」），非优势手 34.0 秒 > 21.5+3×4.0=33.5 ⇒「重度异常」；偏离 (30-19.5)/19.5=+53.8%。默认态 domTime 为空 ⇒「请输入优势手测试时间」早退、不渲染，零交集。"
},
{
  "slug": "rehabilitation/proprioception-error",
  "inputs": {
    "target1": "30",
    "target2": "45",
    "target3": "60",
    "target4": "75",
    "reproduce1": "37",
    "reproduce2": "49",
    "reproduce3": "66",
    "reproduce4": "84",
    "testJoint": "knee",
    "testSide": "left"
  },
  "clicks": [
    "calcError();finalizeResult();"
  ],
  "expect": [
    "左侧膝关节 · 平均误差 6.5° · 最大 9.0° · 最小 4.0° · 标准差 1.8° → 轻度异常"
  ],
  "ref": "门诊记录：clicks 先 calcError() 填 errors（|37-30|,|49-45|,|66-60|,|84-75| = 7,4,6,9）再 finalizeResult() 汇总，平均 6.5°、最大 9.0°、最小 4.0°、SD 1.79→1.8°，落 5<avg≤10 档「轻度异常」。默认态 repro/其它角为空 ⇒ errors 为空、finalizeResult 早退不渲染门诊记录，零交集。旧 expect「68」属输入回显（无法证明计算正确），已废弃。"
},
{
  "slug": "rehabilitation/prosthesis-alignment",
  "inputs": {
    "prosthesisType": "transtibial",
    "stumpLength": "15",
    "stumpWidth": "12",
    "bodyWeight": "70",
    "heelHeight": "4",
    "footType": "carbon"
  },
  "ref": "门诊记录：小腿假肢段 70kg→686N，单侧 343N；残端面积 15×12=180cm² ⇒ 压强 343/180=1.9 N/cm²（=kPa）<150 ⇒「可接受」分支；跟高 4>2 ⇒ 假足后移 10mm；初始屈曲固定 7°。默认态为 transfemoral 且跟高 2 ⇒ 走大腿分支、无「后移 10 mm」，与本用例零交集。",
  "expect": [
    "【假肢对线与残端承重评估】 结果：类型 小腿假肢（截肢平面经胫骨） · 残肢 15×12 cm · 体重 70 kg → 单侧承重 343 N、残端面积 180 cm²、压强 1.9 kPa 对线角度：接受腔初始屈曲 7°（小腿假肢常规 5–8°）；假足前后位置：后移 10 mm；鞋跟高 4 cm；假足型号：carbon 临床提示：残端压强在可接受范围：保持每日检查残端皮肤（发红&gt;30 分钟不消退需减量），穿戴后 15 分钟与 1 小时各复查一次对线标记。 评估日期：__________ 评估者：__________ （自评/筛查量表，结果仅供临床沟通参考，不作为诊断依据）"
  ]
},
{
  "slug": "rehabilitation/respiratory-training",
  "inputs": {
    "gender": "male",
    "age": "70",
    "height": "170",
    "weight": "60",
    "currentMIP": "45",
    "condition": "copd"
  },
  "ref": "门诊记录：男 70 岁 170cm ⇒ 预测 MIP 70 / MEP 127；实测 45 ⇒ 64% 预测值落「轻度下降」（60–79%）；目标 MIP 42 低于实测 ⇒ 走「已高于目标 3 cmH₂O」分支（原代码此处输出 NaN 周，已修）；BMI 60/1.7²=20.8。默认态 currentMIP 空 ⇒ 早退，与本用例零交集。",
  "expect": [
    "【吸气肌力量（MIP/MEP）评估与训练处方】 结果：预测 MIP 70 / MEP 127 cmH₂O（男、70 岁）→ 实测 MIP 45 cmH₂O（达预测 64%，轻度下降）；目标 MIP 42、训练强度 13 cmH₂O 基础疾病：COPD，实测已高于目标值 3 cmH₂O；BMI 20.8 临床提示：轻度下降（60–79% 预测值）：开始吸气肌训练（IMT），强度从 30% MIP 起步、每次 30 呼吸、每日 2 次，每周递增 5–10%，4 周复评。 评估日期：__________ 评估者：__________ （自评/筛查量表，结果仅供临床沟通参考，不作为诊断依据）"
  ]
},
{
  "slug": "rehabilitation/stretch-duration",
  "inputs": {
    "stretchPart": "knee",
    "riskLevel": "high",
    "holdTime": "10",
    "reps": "2",
    "dailySessions": "1",
    "restrictedAngle": "30",
    "targetImprove": "3"
  },
  "expect": [
    "【牵伸（拉伸）处方剂量评估】 结果：部位：knee · 风险等级 高 → 保持 10 秒 × 2 组 × 每日 1 次（单次 0.3 分钟，每日 0.3 分钟，每周 2 分钟）",
    "参考剂量（高风险）：保持 30-60 秒 × 4-5 组 × 每日 3-5 次；方案评估：需调整；当前受限 30°，按每周 3° 预计 10 周"
  ],
  "ref": "门诊记录：10 秒×2 组×1 次 = 20 秒/日 ⇒ 单次 0.33→0.3 分钟、每日 0.3 分钟、每周 120 秒→2 分钟；hold=10<15 且 high 风险每日总量 <180 秒 ⇒ adequate=false ⇒「需调整」；受限 30°、每周 3° ⇒ 10 周。默认态 hold=30/reps=3/daily=2、风险 low、部位 shoulder ⇒ 60 秒×.../每日 3 分钟，与本用例零交集。"
},
{
  "slug": "rehabilitation/tester-rater",
  "inputs": {
    "b1": "1",
    "b2": "1",
    "b3": "1",
    "b4": "1",
    "b5": "1",
    "b6": "1",
    "b7": "1",
    "b8": "1",
    "b9": "1",
    "b10": "1",
    "b11": "1",
    "b12": "1",
    "b13": "1",
    "b14": "1"
  },
  "ref": "门诊记录：14 项全勾 1 分 ⇒ Berg 总分 14/56 <40 ⇒「高跌倒风险」+ 轮椅/监护下行走建议分支；默认态未勾选 ⇒ 提示先完成评分，与本用例零交集。",
  "expect": [
    "【Berg 平衡量表（BBS · 14 项 · 满分 56）】 结果：Berg 总分 14/56 → 跌倒风险分级：高跌倒风险 界值：&lt;40 高、40–44 中、45–53 低、54–56 平衡正常；单项满分 4 分，≤2 分的项目提示该任务需重点训练 临床提示：Berg &lt;40 分：跌倒风险高，需使用轮椅或助行器并在监护下行走，强化平衡（重心转移、单腿站立、动态平衡）与下肢力量训练，居家做环境改造（扶手、防滑、夜灯）。 评估日期：__________ 评估者：__________ （自评/筛查量表，结果仅供临床沟通参考，不作为诊断依据）"
  ]
},
{
  "slug": "rehabilitation/walker-height",
  "inputs": {
    "height": "170",
    "age": "72",
    "elbowAngle": "45",
    "wristHeight": "",
    "shoeHeight": "3",
    "scenario": "stairs"
  },
  "expect": [
    "【助行器 / 拐杖高度适配】 结果：身高 170 cm（年龄 72 岁，肘屈 45°）→ 手柄高度 95.9 cm（大转子 96.9 cm、腋窝 130.9 cm、前臂套环 125.8 cm）（楼梯使用降低2cm）",
    "适配校验 1/2 项通过"
  ],
  "ref": "门诊记录：170 cm ⇒ 大转子 96.9、腋窝 130.9、套环 125.8；未填腕横纹 ⇒ 手柄取大转子 96.9，鞋底 3 cm 补 +1，楼梯再 -2 ⇒ 95.9 cm；肘屈 45° 超出 20–30° ⇒ 适配校验仅 1/2 通过（其余 4 项中 1 项失败）。默认态 height 为空 ⇒「请输入身高」早退、不渲染，零交集。"
},
{
  "slug": "rehabilitation/rom-normal-value",
  "inputs": {
    "jointSelect": "肩关节",
    "motionSelect": "屈曲",
    "measuredAngle": "100"
  },
  "expect": [
    "关节 肩关节 · 动作 屈曲 · 测值 100°（正常参考 0-180°，达上限 56%）→ 中度受限"
  ],
  "ref": "门诊记录（该页原为零用例，本次新增）：jointSelect/motionSelect 虽由 JS 生成 option，但值是纯字符串键，inputs 可直接注入；measuredAngle=100 对肩关节屈曲（max 180）⇒ pct = round(100/180*100) = 56 ⇒ 落 50≤pct<75 档「中度受限」。默认态 measuredAngle 为空、isNaN 分支提前 return 不产生 note；且默认 jointSelect 为空时 romData[''] 为 undefined 直接抛错，故零交集。取 100 而非 90 是避开 pct=50 的档位边界。"
},
{
  "slug": "rehabilitation/water-swallow-test",
  "inputs": {
    "drinkTime": "8",
    "drinkCondition": "1"
  },
  "expect": [
    "饮水用时 8 秒 → Ⅱ级（可疑异常），由 Ⅰ级 修正"
  ],
  "ref": "门诊记录：drinkCondition=1（Ⅰ级）但 drinkTime=8 秒 > 5 秒 ⇒ evaluate() 内按页面规则把 grade 修正为 2 级，REC 同时记下原分级与修正后分级，输出「饮水用时 8 秒 → Ⅱ级（可疑异常），由 Ⅰ级 修正」。默认态 drinkCondition 为空 ⇒ 只显示「请选择饮水情况」、无 note，零交集。"
},
{
  "slug": "rehabilitation/wheelchair-posture",
  "inputs": {
    "weight": "70",
    "sitHeight": "85",
    "hipWidth": "40",
    "seatWidth": "46",
    "seatDepth": "42",
    "seatHeight": "48",
    "backHeight": "40",
    "cushionType": "gel"
  },
  "ref": "门诊记录：70kg→686N，坐骨界面压 686/(2×300)/133.322×1e4=86 mmHg，凝胶减压 45% ⇒ 47 mmHg（<60 ⇒「可接受」）；座宽 46 vs 理想 42（臀宽+2）⇒ 偏宽 4cm。默认态坐垫 none、输入空 ⇒ 早退，与本用例零交集。",
  "expect": [
    "【轮椅坐姿与坐垫减压评估】 结果：体重 70 kg · 臀宽 40 cm → 座宽 46 cm（理想 42 cm）、座深 42 cm、座高 48 cm、靠背高 40 cm；坐骨压力 86 mmHg → 使用凝胶坐垫减压后 47 mmHg（减压率 45%） 座宽应为臀宽 +2 cm（误差 ±1 cm）；座深应比大腿长度短 2–5 cm，避免腘窝受压；坐骨结节处压力 &gt;32 mmHg 即有毛细血管闭塞风险，减压后仍 &gt;60 mmHg 需更换坐垫 临床提示：减压效果可接受：保持坐垫正确方向（前后不可颠倒）、每日检查坐垫是否漏气或变形，配合定时减压动作。 评估日期：__________ 评估者：__________ （自评/筛查量表，结果仅供临床沟通参考，不作为诊断依据）"
  ]
}
,
  {
    "slug": "rehabilitation/physiotherapy-dose",
    "inputs": {"usArea":"20","usHead":"5","usIntensity":"1.5","usFreq":"1"},
    "checks": ["pulsed"],
    "expect": ["超声波 1MHz 脉冲1:4 1.5W/cm² × 4.0 分钟 · 辐射头 5cm² · 治疗面积 20cm² · 总功率 7.5W · 总能量 360J · 有效深度 4-5cm（深部） · 病程分期 慢性期"],
    "ref": "门诊记录：usArea=20、usHead=5 ⇒ 时间=20/5=4.0 分钟（未触 3–10 分钟上下限）；总功率=1.5×5=7.5W；checks 注入 usMode:pulsed ⇒ 脉冲 1:4 能量=7.5×4×60×0.2=360J；强度 1.5>0.5 ⇒ 慢性期；freq=1 ⇒ 深部 4-5cm。默认态 usArea 为空 ⇒ calcUS 早退显示「请输入治疗面积」、不产生门诊记录，零交集。原先那条超长 expect 混合了三段 tab 的原始 blob，已收敛为门诊记录单串。"
  }
  ,{
    "slug": "rehabilitation/berg-balance-scale",
    "checks": ["2"],
    "expect": [
      "【Berg 平衡量表（BBS · 14 项 · 满分 56）】 结果：总分 28/56，分级：中度平衡障碍，跌倒风险：中高跌倒风险",
      "已完成 14/14 项；估算跌倒风险增加约 119%"
    ],
    "ref": "门诊记录（EMR note）：14 项各按 2 分（checks 注入 input[name=itemN]:checked ⇒ value=2）⇒ 总分 28 落 21–40 段「中度平衡障碍」/「中高跌倒风险」；跌倒风险估算 (45-28)×7=119%。默认态 answered=0 ⇒ 门诊记录整段不渲染（done<14 直接 return），零交集。"
  }
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; }
      else {
        fails.push(c.slug);
        console.log("❌ " + c.slug + "  " + (r.why || "no expect match"));
        if (r.errs && r.errs.length) console.log("     errs: " + JSON.stringify(r.errs));
        if (r.sample) console.log("     got: " + String(r.sample).slice(0, 300));
      }
    } catch (e) {
      fails.push(c.slug);
      console.log("❌ " + c.slug + "  THROWN: " + ((e && e.message) ? e.message : String(e)));
    }
  }

  console.log("==== rehabilitation calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
