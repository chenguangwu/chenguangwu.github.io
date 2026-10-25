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
  "inputs": {
    "fim_0": "7",
    "fim_1": "7",
    "fim_2": "7",
    "fim_3": "7",
    "fim_4": "7",
    "fim_5": "7",
    "fim_6": "7",
    "fim_7": "7",
    "fim_8": "7",
    "fim_9": "7",
    "fim_10": "7",
    "fim_11": "7",
    "fim_12": "7",
    "fim_13": "7",
    "fim_14": "7",
    "fim_15": "7",
    "fim_16": "7",
    "fim_17": "7"
  },
  "expect": [
    "运动功能分： 91/91（独立率100%）"
  ],
  "ref": "fim_0..12 为运动 13 项、fim_13..17 为认知 5 项，全填 7 ⇒ 运动分 13×7=91/91、独立率 100%。默认态未注入 ⇒ 运动分非 91，不含该串。原 expect「上下12-14级台阶」是说明文案，默认恒在（常量型逃生项）。"
},
{
  "slug": "rehabilitation/flacc-scale",
  "checks": [
    "2"
  ],
  "expect": [
    "10 / 10分 - 重度疼痛"
  ],
  "ref": "5 个项目各按 2 分（checks 注入 :checked ⇒ value=2）⇒ 总分 10 ⇒「/ 10分 - 重度疼痛」。默认态未勾选 ⇒ allSelected=false ⇒ showToast 早退不写结果，不含该串。原 expect「0分」是等级表「0分」档文案，默认恒在（常量型逃生项）。"
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
    "gender": "female"
  },
  "expect": [
    "female"
  ],
  "ref": "auto-restore"
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
    "holdTime": "45",
    "reps": "3",
    "dailySessions": "2",
    "targetImprove": "5"
  },
  "expect": [
    "每次保持45秒"
  ],
  "ref": "auto-restore"
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
    "elbowAngle": "38",
    "shoeHeight": "2"
  },
  "expect": [
    "38"
  ],
  "ref": "auto-restore"
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
