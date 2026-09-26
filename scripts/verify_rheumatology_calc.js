#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  // 原 expect「观察滴度变化」是输出文案片段（词串型，不依赖被测点）；改为依赖勾选的分级断言。
  // 小关节 + 对称性关节炎 → 关节受累 +3；叠加 inputs 血清学（ccp=120 ≥40 → +2）、病程 +1、
  // CRP/ESR 异常 +1 → 7 分 ≥ 6 → 符合RA分类标准。不勾选时仅 4 分 → 疑诊RA（故具判别力）。
  "slug": "rheumatology/anti-ccp",
  "inputs": {
    "ccp": "120",
    "rf": "45",
    "crp": "12",
    "esr": "28"
  },
  "checkIds": [
    "smalljoint",
    "symmetric"
  ],
  "expect": [
    "(≥6分, 符合RA)",
    "小关节对称受累(+3)"
  ],
  "ref": "2010 ACR/EULAR 简化：小关节对称受累 +3（血清学 +2、病程 +1、CRP/ESR +1）= 7 ≥ 6 → 诊断「符合RA」（输出尾部带「(≥6分, 符合RA)」）；默认不勾选 = 4 → 疑诊RA。注：不可用「符合RA分类标准」作 expect —— 该串在页面静态参考表里已出现 2 次（逃生项）"
},
{
  // 原 expect「发数周」是输出文案片段（词串型）；改为依赖勾选的分级断言。
  // 勾选 5 项系统受累：尿检异常 +2、神经精神症状 +2、发热 +1、疲劳 +1、皮疹 +1 = +7，
  // 叠加 c3=0.5 / c4=0.08 的补体降低项 → activityScore ≥ 7 → 高活动度。
  // 不勾选时 = 低活动度（故具判别力）。
  "slug": "rheumatology/complement-level",
  "inputs": {
    "c3": "0.5",
    "c4": "0.08",
    "ch50": "15"
  },
  "checkIds": [
    "renal",
    "cns",
    "fever",
    "fatigue",
    "rash"
  ],
  "expect": [
    "高活动度",
    "尿检异常 (+2)"
  ],
  "ref": "activityScore：尿检异常 +2、神经精神症状 +2、发热 +1、疲劳 +1、皮疹 +1 = +7，叠加补体降低（c3=0.5/c4=0.08）→ ≥7 → 高活动度"
},
{
  // 原为 all_default 弱用例（注入值全等于页面默认），expect「抑制剂」是建议文本词（逃生项）。
  // DAS28(ESR) = 0.56×√12 + 0.28×√8 + 0.70×ln8 + 0.014×50 = 4.89 → 中等活动度（3.2–5.1）。
  // 默认态（markerVal=20/tjc=5/sjc=3/gh=30）算得 4.25 —— 同为中等活动度但数值不同：
  // 等级词在本页无判别力（默认与注入态同为「中等活动度」），必须断言数值串。
  "slug": "rheumatology/das28",
  "inputs": {
    "marker": "esr",
    "markerVal": "8",
    "tjc": "12",
    "sjc": "8",
    "gh": "50"
  },
  "expect": [
    "4.89 DAS28 评分",
    "结果：DAS28 = 4.89 中等活动度"
  ],
  "ref": "DAS28(ESR)=0.56×√(TJC28)+0.28×√(SJC28)+0.70×ln(ESR)+0.014×GH = 1.9399+0.7920+1.4556+0.7000 = 4.8875 → 4.89（中等活动度）；默认值 4.2541 → 4.25，两串均失配。"
},
{
  // 原为 all_default 弱用例（注入值全等于页面默认），expect「肝素」是临床建议文本词（逃生项）。
  // 筛查 60/35 = 171% > 110%（延长）+ 混合未纠正 + 确认比值 60/55 = 1.09 ≤ 1.1（非阳性）
  // → 命中 isth1 && isth2 && !isth3 分支 → 「非磷脂依赖性抑制物」（默认态为 LA 阳性）。
  "slug": "rheumatology/detector-8",
  "inputs": {
    "screen": "60",
    "confirm": "55",
    "normal": "35",
    "mixing": "uncorrected",
    "aptt": "70",
    "apttNormal": "32"
  },
  "expect": [
    "非磷脂依赖性抑制物 判读结论",
    "1.09 dRVVT比值（>1.2阳性）"
  ],
  "ref": "dRVVT 比值 = 60/55 = 1.0909 → 1.09（≤1.1 阴性）、筛查% = 60/35 = 171%（>110% 延长）、混合试验未纠正 ⇒ isth1&&isth2&&!isth3 → 「非磷脂依赖性抑制物」；默认 42/33 → 1.2727 > 1.2 → 「狼疮抗凝物（LA）阳性」。"
},
{
  // 原 expect「病理诊断」是输出文案片段（词串型）；改为依赖勾选的分级断言。
  // 器官受累：胰腺 +4、胆管 +3、肾脏 +3 = +10；叠加 igg4=5.8（落在 5.0–10 g/L 档 → +6）= 16，
  // 落在 10–19 区间 → 疑诊IgG4-RD。不勾选器官时 = 6 分 → 更低档（故具判别力）。
  "slug": "rheumatology/igg4-level",
  "inputs": {
    "igg4": "5.8",
    "igg": "18",
    "ige": "350",
    "eos": "0.6",
    "c3": "1.3"
  },
  "checkIds": [
    "pancreas",
    "biliary",
    "kidney"
  ],
  "expect": [
    "疑诊IgG4-RD",
    "胰腺受累 → +4"
  ],
  "ref": "score：胰腺 +4、胆管 +3、肾脏 +3 = 10，加 igg4=5.8（5.0–10 档 +6）= 16（10–19）→ 疑诊IgG4-RD；≥20 才是高度提示"
},
{
  // 原为 all_default 弱用例：6 项指标全等于页面默认，expect「肝酶」是疾病建议表里的常量词（逃生项）。
  "slug": "rheumatology/il6-inflammation",
  "inputs": {
    "il6": "1200",
    "crp": "8",
    "esr": "45",
    "ferritin": "500",
    "plt": "450",
    "fib": "5.5"
  },
  "checkIds": [
    "organ"
  ],
  "expect": [
    "IL-6：1200 pg/mL → 极度升高(炎症风暴)",
    "IL-6>1000 (+5, 炎症风暴)"
  ],
  "ref": "IL-6=1200 ≥1000 → 判读「极度升高(炎症风暴)」且炎症负荷 +5（明细条「IL-6>1000 (+5, 炎症风暴)」）；organ 勾选 → 脏器功能不全 +3（总分 11 → 炎症风暴风险）。回退默认（il6=25）→ 「中度升高」且无 +5 明细。"
},
{
  // 原 expect「但需评估血栓风险因素」是输出文案片段（词串型）；改为依赖勾选的分级断言。
  // 抗体谱阳性（aCL/β2GPI）+ 临床标准（血栓/妊娠并发症）同时满足 → 符合APS分类标准。
  // 不勾选时仅为「抗磷脂抗体阳性(aPL携带者)」（故具判别力）。
  "slug": "rheumatology/lupus-anticoagulant",
  "inputs": {
    "dsc": "45",
    "dcc": "35",
    "dnm": "32",
    "ssc": "42",
    "scc": "35",
    "snm": "33"
  },
  "checkIds": [
    "acl",
    "ab2gpi",
    "vte",
    "arte",
    "pregloss",
    "preeclampsia",
    "thrombocytopenia"
  ],
  "expect": [
    "符合APS分类标准"
  ],
  "ref": "抗体谱阳性（aCL + β2GPI）+ 临床标准（血栓事件/妊娠并发症）同时满足 → 符合APS分类标准；默认不勾选 = aPL携带者"
},
{
  // 原 expect「抑制剂」是输出文案片段（词串型）；改为依赖勾选的分级断言。
  // rpild（快速进展型 ILD）是「极高风险」的独立触发条件（rpild || riskScore ≥ 8）。
  // 不勾选时 riskScore = 6（MDA5阳性+3、铁蛋白800+2、LDH+1）→ 高风险（故具判别力；
  // 注意「极高风险」含子串「高风险」，expect 必须取更长的「极高风险」）。
  "slug": "rheumatology/mda5-antibody",
  "inputs": {
    "ferritin": "800",
    "ck": "150",
    "crp": "15",
    "ldh": "300"
  },
  "checkIds": [
    "rpild"
  ],
  "expect": [
    "极高风险"
  ],
  "ref": "rpild（快速进展型ILD）→ 直接命中「极高风险」分支（rpild || riskScore ≥ 8）；默认不勾选 = 6 分 → 高风险"
},
{
  // 原 expect「评估治疗反应」是输出文案片段（词串型）；改为依赖勾选的分级断言。
  // 诊断分：前胸壁 +3、骨肥厚 +2、掌跖脓疱病 +2、重度痤疮/HS +2、骶髂关节炎 +1、脊柱 +1、
  // 脓疱型银屑病 +1 = 12（未勾 culture）→ 高度提示SAPHO。不勾选时 = 低档（故具判别力）。
  "slug": "rheumatology/sapho-syndrome",
  "inputs": {
    "duration": "3",
    "vas": "5"
  },
  "checkIds": [
    "chestwall",
    "acquired",
    "palmoplantar",
    "severeAcne",
    "sacro",
    "spine",
    "pustular"
  ],
  "expect": [
    "高度提示SAPHO",
    "前胸壁受累(+3, 特征性表现)"
  ],
  "ref": "dxScore：前胸壁 +3、骨肥厚 +2、掌跖脓疱病 +2、重度痤疮/HS +2、骶髂关节炎 +1、脊柱 +1、脓疱型银屑病 +1 = 12 → 高度提示SAPHO"
},
{
  "slug": "rheumatology/anca-classification",
  "inputs": {
    "iif": "canca"
  },
  "expect": [
    "疑似PR3"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rheumatology/assessor-10",
  "inputs": {
    "d'+i+'": "'+lv.v+'"
  },
  "expect": [
    "+lv.v+"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rheumatology/basdai",
  "inputs": {
    "q1": "6",
    "q2": "4",
    "q3": "2",
    "q4": "3",
    "q5": "5",
    "q6": "4"
  },
  "expect": [
    "(6.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rheumatology/behcet-hla",
  "inputs": {
    "age": "middle"
  },
  "expect": [
    "middle"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rheumatology/bvas",
  "inputs": {},
  "clicks": [
    "var __q=document.querySelectorAll;document.querySelectorAll=function(s){if(s==='.g1')return [{checked:true},{checked:true},{checked:true},{checked:true}];if(s==='.g2')return [{checked:true},{checked:true},{checked:true},{checked:true},{checked:true}];if(s==='.g3')return [{checked:true},{checked:true},{checked:true},{checked:true},{checked:true}];if(s==='.g4')return [{checked:true},{checked:true},{checked:true},{checked:true},{checked:true},{checked:true}];if(s==='.g5')return [{checked:true},{checked:true},{checked:true},{checked:true},{checked:true}];if(s==='.g6')return [{checked:true},{checked:true},{checked:true},{checked:true}];if(s==='.g7')return [{checked:true},{checked:true},{checked:true}];if(s==='.g8')return [{checked:true},{checked:true},{checked:true},{checked:true},{checked:true},{checked:true},{checked:true}];if(s==='.g9')return [{checked:true},{checked:true},{checked:true},{checked:true}];return __q.call(document,s);};calc();document.querySelectorAll=__q;"
  ],
  "expect": [
    "总分 = 63",
    "高活动度"
  ],
  "ref": "（2026-09-24 曾记为「静态 class 批量复选框不在 DYN 表 ⇒ 不可注入」，本批次推翻）calc() 只读 document.querySelectorAll('.'+g.cls) 的 el.checked，与 DOM 树无关 ⇒ 覆写 querySelectorAll 返回「全 checked 的哑元素」即等价「用户勾选全部项」，用完即恢复原函数。独立复算：每组各按 weights 累加后被 g.max 幂等封顶（3/6/6/6/6/6/9/12/9）⇒ 总分 63、受累系统 9、level>15 ⇒ 高活动度。锚「总分 = 63 + 高活动度」；旧锚「定期监测ANCA滴度和脏器功能」是 total===0 分支的常驻文案，默认态必命中、判别力 0，已弃。注意「受累系统数」是页面常驻 stat-card 标签，也不能当锚。"
},
{
  "slug": "rheumatology/essdai",
  "inputs": {
    "d1": "1"
  },
  "expect": [
    "+1分"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rheumatology/gout-uric-acid",
  "inputs": {
    "ua": "720"
  },
  "expect": [
    "需降低360"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rheumatology/guguanjieyan-womac-zhishu",
  "inputs": {
    "' + name + '_' + v + '": "' + v + '_X"
  },
  "expect": [
    "_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rheumatology/itp-immune",
  "inputs": {
    "plt": "38"
  },
  "expect": [
    "定期监测血小板(每1-3月)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rheumatology/mctd-diagnosis",
  "inputs": {
    "rnp": "low"
  },
  "expect": [
    "low"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rheumatology/mrss",
  "inputs": {
    "s1": "1"
  },
  "expect": [
    "1/51"
  ],
  "ref": "auto-restore"
},
{
  // 原为 no_inputs 弱用例（inputs 空），expect「CH50/C3/C4低于正常下限」是条目表静态 desc（逃生项）。
  // 复选框 id 由 JS 模板拼为 cb_<key>，须用 checkIds 声明选中态（注入 .value 无效）。
  // SLEDAI-2K 权重 8/4/2/1：癫痫发作(8) + 精神症状(8) + 关节炎(4) = 20 > 14 → 重度活动。
  "slug": "rheumatology/rater-16",
  "inputs": {},
  "checkIds": [
    "cb_seizure",
    "cb_psychosis",
    "cb_arthritis"
  ],
  "expect": [
    "20 SLEDAI-2K总分（最高105）",
    "SLEDAI-2K评分：20分 — 重度活动"
  ],
  "ref": "神经系统/血管组 8 分 ×2（癫痫发作、精神症状）+ 肌肉关节组 4 分（关节炎）= 20 分 > 14 → 重度活动；清空勾选（模拟注入失败）→ 0 分「无疾病活动」，两串均失配。"
},
{
  // 原为 no_inputs 弱用例（inputs 空），expect「肌酐125-249」是肾脏组条目静态 desc（逃生项）。
  // BVAS v3 按组封顶（Math.min(原组和, max)）：皮肤病变组 溃疡(4)+坏疽(4) = 原始 8 → 封顶 6；
  // 腹部组 腹痛(3) = 3；总分 6+3 = 9（6–10 → 中等活动度）。
  "slug": "rheumatology/rater-17",
  "inputs": {},
  "checkIds": [
    "cb_ulcer",
    "cb_gangrene",
    "cb_abdpain"
  ],
  "expect": [
    "9 BVAS总分（最高63）",
    "8 (>上限)"
  ],
  "ref": "皮肤病变组 max=6，溃疡(4)+坏疽(4)=原始 8 被幂等封顶到 6；腹部组 max=9，腹痛 3 → 3；总分 9 → 中等活动度。期望串「8 (>上限)」同时验证封顶标记（原始 8 / 上限 6 / 实计 6）；清空勾选 → 0 分，两串均失配。"
},
{
  "slug": "rheumatology/sledai",
  "inputs": {},
  "clicks": [
    "var __q=document.querySelectorAll;document.querySelectorAll=function(s){if(s==='.s8')return [{checked:true},{checked:true},{checked:true},{checked:true},{checked:true},{checked:true},{checked:true},{checked:true}];if(s==='.s4')return [{checked:true},{checked:true},{checked:true},{checked:true},{checked:true},{checked:true}];if(s==='.s2')return [{checked:true},{checked:true},{checked:true},{checked:true},{checked:true},{checked:true},{checked:true}];if(s==='.s1')return [{checked:true},{checked:true},{checked:true}];return __q.call(document,s);};calc();document.querySelectorAll=__q;"
  ],
  "expect": [
    "总分 = 105",
    "极重度活动"
  ],
  "ref": "与 bvas 同源通道（覆写 querySelectorAll 返回全 checked 哑元素）。独立复算：s8 8×8=64、s4 6×4=24、s2 7×2=14、s1 3×1=3 ⇒ 总分 105 > 19 ⇒ 极重度活动；details 非空 ⇒ 渲染「总分 = 105」明细行。默认态全 0 ⇒ 「无活动」+「病情稳定…」，两串均失配。旧锚「SLEDAI-2K」是静态卡片标题，默认态必命中，判别力 0，已弃。"
},
{
  "slug": "rheumatology/ssa-ssb",
  "inputs": {
    "ssa": "ro60"
  },
  "expect": [
    "补体C3/C4"
  ],
  "ref": "auto-restore"
},
{
  // 原为 no_inputs 弱用例（inputs 空），expect「(0-100)」是维度标签静态串（逃生项）。
  // 24 个 select 由 JS 模板生成（HTML 中无字面 <select id>，getEl 只能惰性造桩），
  // 因此必须显式注入全部 p0-p4 / s0-s1 / f0-f16 共 24 个分值键，否则取空值 → Σ=NaN。
  // 疼痛 3+3+2+3+3=14/20、僵硬 2+2=4/8、功能 2×17=34/68 → 原始 52/96 → 标准化 54 → 重度。
  "slug": "rheumatology/womac",
  "inputs": {
    "p0": "3", "p1": "3", "p2": "2", "p3": "3", "p4": "3",
    "s0": "2", "s1": "2",
    "f0": "2", "f1": "2", "f2": "2", "f3": "2", "f4": "2", "f5": "2", "f6": "2", "f7": "2", "f8": "2",
    "f9": "2", "f10": "2", "f11": "2", "f12": "2", "f13": "2", "f14": "2", "f15": "2", "f16": "2"
  },
  "expect": [
    "54 WOMAC标准化总分",
    "52/96 原始总分"
  ],
  "ref": "WOMAC：疼痛 Σ14/20、僵硬 Σ4/8、功能 Σ34/68 → 原始总分 52/96 → 标准化 round(52/96×100) = 54 → 重度（51–75）；未注入时各 select 取空串 → Σ=NaN，两串均失配。"
}
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try { const r = await runCase(c); if (r.ok) pass++; else fails.push(c.slug); }
    catch (e) { fails.push(c.slug); }
  }
  console.log("==== rheumatology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
