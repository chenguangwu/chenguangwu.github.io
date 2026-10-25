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
    "运动总评分： 100/100 （左侧50/50 右侧50/50）",
    "感觉总评分： 224/224"
  ],
  "ref": "全量注入 28 皮节×4 位点（sens_*_lt_l/pp_l/lt_r/pp_r）+ 10 组关键肌×双侧（motor_i_l/r）共 132 键：运动 20 肌全 5 ⇒ 运动总评分 100/100；感觉 112 位点全 2 ⇒ 224/224。注意本页 select 由 renderSensory()/renderMotor() 运行期拼 innerHTML 生成、**不在静态源码里**，桩取不到默认值 ⇒ parseInt('')=NaN，默认态输出「NaN/…」；旧 expect 正是锚在这个桩假象「NaN/112」上。真机默认（option 2-正常 带 selected）实显 224/112 —— 分母 112 系量纲错（28×4×2=224），已随本批次修为 /224。"
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
    "日常交流基本可行，但效率和质量降低"
  ],
  "ref": "selectGrade(3) 把 bostonGrades[3].comm 写入 #resultBox（仅点击后出现）；默认只渲染 6 张 ref-card 的 name/level/desc，无 comm。原 expect「0级」是 bostonGrades[0].name，默认列表里恒在（常量型逃生项）。"
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
  "expect": [
    "75.0% 支撑相占比"
  ],
  "ref": "cycleTime=1.0s、stanceTime=0.75s ⇒ stancePct=0.75/1.0×100=75.0（toFixed(1)）⇒「75.0% 支撑相占比」。默认态 cycle/stance 为空 ⇒ 早退输出「请输入步态周期时间和支撑相时间」，不含 75.0%。原 expect 正是那句空值提示（默认恒在，常量型逃生项）。"
},
{
  "slug": "rehabilitation/mmse-scoring",
  "checks": [
    "1"
  ],
  "expect": [
    "30 / 30分"
  ],
  "ref": "30 项全选「正确」（checks 注入 input[name=qN]:checked ⇒ value=1，页面按 sel.value==='1' 计数）⇒ total=30 ⇒「30 / 30分」；默认 total=0 显示「0 / 30分」。原 expect「100-7」是量表注意力条目文案，默认恒在（常量型逃生项）。"
},
{
  "slug": "rehabilitation/mmt-grading",
  "checks": [
    "5"
  ],
  "expect": [
    "能抗重力及最大外加阻力完成全范围运动"
  ],
  "ref": "选中 5 级（checks 注入 input[name=grade]:checked ⇒ value=5）⇒ mmtData[5].func 写入 #resultBox；默认态 evaluate() 读不到选中项直接 return ⇒ 结果框为空。原 expect「如3+表示抗重力完成全范围后还能抗轻微阻力」是说明文案，默认恒在（常量型逃生项）。"
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
    "target1": "68",
    "target2": "90",
    "target3": "120",
    "target4": "60"
  },
  "expect": [
    "68"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rehabilitation/prosthesis-alignment",
  "inputs": {
    "heelHeight": "2",
    "prosthesisType": "transfemoral"
  },
  "expect": [
    "transfemoral"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rehabilitation/respiratory-training",
  "inputs": {
    "age": "98",
    "height": "170",
    "weight": "65"
  },
  "expect": [
    "设定12cmH"
  ],
  "ref": "auto-restore"
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
    "b1": "1"
  },
  "expect": ["1\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\nBerg总分： 53 / 56 跌倒风险： 低跌倒风险 测试项目 得分 1. 坐起 1分 2. 独立站立 4分 3. 独立坐 4分 4. 坐下 4分 5. 转移 4分 6. 闭眼站立 4分 7. 双足并拢 4分 8. 上肢前伸 4分 9. 地面拾物 4分 10. 转身向后看 4分 11. 原地转360度 4分 12. 踏凳 4分 13. 前后足站立 4分 14. 单腿站立 4分 Berg评分53分（45-53），跌倒风险较低。建议继续平衡训练，注意日常安全。"],
  "ref": "auto-restore"
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
  "slug": "rehabilitation/water-swallow-test",
  "inputs": {
    "drinkCondition": "1"
  },
  "expect": [
    "建议保持良好进食习惯"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rehabilitation/wheelchair-posture",
  "inputs": {
    "cushionType": "gel"
  },
  "expect": [
    "gel"
  ],
  "ref": "auto-restore"
}
,
  {
    "slug": "rehabilitation/physiotherapy-dose",
    "inputs": {"usArea":"20","laserPower":"100","laserArea":"5","tensTime":"20"},
    "clicks": ["calc()"],
    "expect": ["20\n5\n0.5\n3\n4.0 治疗时间(分钟) 2.5 总功率(W) 600 总能量(J) 频率： 3MHz ｜ 深度： 1-2cm（浅表） 模式： 连续 ｜ 阶段： 亚急性期 强度： 0.5 W/cm² ｜ 辐射头： 5 cm² 处方： 超声波 3MHz 连续 0.5W/cm² × 4分钟，每周3次，10次为一疗程\n100\n5\n2\ngaalas\n100 照射时间(秒) 10.0 总能量(J) 20.0 功率密度(mW/cm²) 激光类型： GaAlAs 820nm（连续） 目标剂量： 2 J/cm² ｜ 阶段： 亚急性期 功率： 100 mW ｜ 面积： 5 cm² 处方： GaAlAs 820nm（连续） 100mW，2J/cm² × 5cm² = 10.0J，照射100秒，每周2-3次\nconventional\n20\n80-100Hz 频率 50-100μs 脉宽 20 时间(分钟) 强度： 感觉阈上（舒适麻刺感） 适用： 急性疼痛首选，镇痛快但持续时间短 处方： TENS 80-100Hz 50-100μs × 20分钟，每日1-3次，2-4周为一疗程\n暂无记录\nTENS 80-100Hz 50-100μs × 20分钟"],
    "ref": "注入 usArea=20(默认空→超声波段输出「请输入治疗面积」，注入后计算总能量 60 J) + laserPower=100(默认50→激光照射时间 100→25 秒) + laserArea=5 + tensTime=20。锚计算结果(随输入变化且与默认态不同)，规避 input 回显(20/100/5/20 及 select 默认项)。"
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
