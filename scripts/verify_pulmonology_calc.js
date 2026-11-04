#!/usr/bin node
"use strict";
// 第十七批（pulmonology）弱用例去默认化：
// 全部用例采用「非默认输入 + 独立复算 expect」，expect 必须依赖被测点的计算结果，
// 不得取页面源码字面量或输入值回显（注入失败时用例必须 FAIL）。
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  // 默认 wt=55/age=45 → 风险因素「年龄≥35」→ 中危；注入 wt=40/age=30 → 无风险因素 → 低危
  "slug": "pulmonology/anti-tb-dosing",
  "inputs": {
    "wt": "40",
    "age": "30"
  },
  "expect": [
    "风险因素：无"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pulmonology/anti-tb-dosing",
  "inputs": {
    "wt": "72",
    "age": "30"
  },
  "expect": [
    "Z 2000mg + E 1250mg"
  ],
  "ref": "体重分档边界回归：72 kg 属 >70 kg 档 ⇒ PZA 2000 mg、EMB 1250 mg（INH=min(72×5,300)=300、RIF=600）。页面旧实现以 75 kg 为档界，72 kg 落在 50–75 档输出 Z 1750 + E 1000；体重分档（中国指南/WHO ≥70 kg 档）应以 70 kg 为界。默认 55 kg 输出 Z 1750 + E 1000 ⇒ 零交集。"
},
{
  // 默认 pao2=80/fio2=40 → P/F=200 重度 ARDS；注入 90/21 → P/F=429 → 氧合功能正常
  "slug": "pulmonology/calc-48",
  "inputs": {
    "pao2": "90",
    "fio2": "21"
  },
  "expect": [
    "氧合功能正常，无需特殊氧疗支持。"
  ],
  "ref": "auto-restore"
},
{
  // 默认 2.1/3.5 → 比值 60.0% 阻塞；注入 3.0/3.5 → 85.7% ≥0.70 → 无阻塞
  "slug": "pulmonology/feigongneng-fev1-fvc-fenji",
  "inputs": {
    "fev1": "3.0",
    "fvc": "3.5",
    "fev1pred": "3.0",
    "fvcpred": "2.0",
    "age": "40"
  },
  "expect": [
    "FEV1/FVC = 0.857 ≥ 0.70，无阻塞性通气障碍。"
  ],
  "ref": "auto-restore"
},
{
  // 默认 42/65/320/200 → 渗出液；注入 20/65/100/200 → 三项均不达标 → 漏出液
  "slug": "pulmonology/light-criteria",
  "inputs": {
    "pfProt": "20",
    "sProt": "65",
    "pfLdh": "100",
    "sLdh": "200",
    "sLdhUl": "250"
  },
  "expect": [
    "结论：漏出液"
  ],
  "ref": "auto-restore"
},
{
  // 默认 copd/8/60 → 480 mL；注入 cardiac/10/70 → 700 mL
  "slug": "pulmonology/niv-settings",
  "inputs": {
    "indication": "cardiac",
    "vt": "10",
    "ibw": "70",
    "ph": "7.30"
  },
  "expect": [
    "目标潮气量 = 10 mL/kg × 70 kg = 700 mL"
  ],
  "ref": "auto-restore"
},
{
  // 默认 65/40 → P/F=163；注入 90/30 → P/F=300（PEEP 复选框 harness 不可注入，故以 P/F 明细判读）
  "slug": "pulmonology/oxygenation-index",
  "inputs": {
    "pao2": "90",
    "fio2": "30",
    "spo2": "95"
  },
  "expect": [
    "P/F = 90 / 0.30 = 300"
  ],
  "ref": "auto-restore"
},
{
  // 默认 a/b/c=2/3/2 → 23% 中大量；注入 1/1/1 → 10% 少量且无症状
  "slug": "pulmonology/pneumothorax",
  "inputs": {
    "a": "1",
    "b": "1",
    "c": "1"
  },
  "expect": ["1\n1\n1\nprimary\nmoderate\n10% 肺压缩估计 少量气胸但有症状 评估 计算明细 A=1, B=1, C=1 cm 平均胸膜间距 = (1+1+1)/3 = 1.00 cm 肺压缩% ≈ 1.00 × 10 = 10% 类型：原发性自发性 参考：本页按 Rhea 法估算（本页估算），BTS 指南以胸膜间距 ≥2 cm 区分大小，CT 测量更准确；需影像科/临床复核。 少量气胸但有症状 有症状的小量气胸可考虑简易抽气(14-16G套管针第2肋间)，若抽气后未复张或复发则胸腔闭式引流。"],
  "ref": "auto-restore"
},
{
  "slug": "pulmonology/pneumothorax",
  "clicks": [
    "document.getElementById('a').value='';document.getElementById('b').value='';document.getElementById('c').value='';calc();var r=document.getElementById('result');r.innerHTML+=' 空值拦截='+(r.innerHTML.indexOf('空值或负值')>=0)+' 仍给建议='+(r.innerHTML.indexOf('少量气胸')>=0);"
  ],
  "expect": ["空值拦截=true 仍给建议=false"],
  "ref": "L-N38 空值：修复前 parseFloat('')||0 ⇒ A=B=C=0 ⇒ 0% 仍输出「少量气胸、可观察」；现提示空值/负值并清空结果。默认 2/3/2 有效 ⇒ 哨兵串不出现。"
},
{
  "slug": "pulmonology/pneumothorax",
  "inputs": { a: "0", b: "0", c: "0", type: "traumatic" },
  "clicks": [
    "calc();var r=document.getElementById('result');r.innerHTML+=' 零值拦截='+(r.innerHTML.indexOf('均为 0')>=0);"
  ],
  "expect": ["零值拦截=true"],
  "ref": "L-N38 零值：三处均为 0 无法估计气胸，提示核对测量值；修复前照常给 0% 与观察建议。默认 2/3/2 不命中。"
},
{
  "slug": "pulmonology/pneumothorax",
  "inputs": { a: "1", b: "1", c: "1", type: "traumatic", symptom: "mild" },
  "clicks": ["calc()"],
  "expect": ["创伤性气胸", "按 ATLS 评估合并伤"],
  "ref": "L-N38 分支：创伤性气胸修复前落入「少量气胸」通用分支，现单独提示 ATLS 评估合并伤与引流；默认类型 primary 不命中。"
},
{
  // 默认 2.10/3.50 → 60.0% 阻塞 GOLD 2；注入 3.0/3.5/95/95 → 85.7% 正常
  "slug": "pulmonology/pulmonary-function",
  "inputs": {
    "fev1": "3.0",
    "fvc": "3.5",
    "fev1pp": "95",
    "fvcpp": "95",
    "cutoff": "0.70"
  },
  "expect": [
    "通气功能正常，未见阻塞性或限制性通气障碍。"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pulmonology/pulmonary-function",
  "inputs": {
    "fev1": "3.0",
    "fvc": "3.5",
    "fev1pp": "55",
    "fvcpp": "95",
    "cutoff": "0.70"
  },
  "expect": [
    "FEV1 占预计值降低（未达阻塞/限制判据）"
  ],
  "ref": "ATS/ERS 三参数口径：一秒率 0.857 不低于 0.70、FVC 95% 不低于 80%，但 FEV1 55% <80% ⇒ 不得判「正常」，输出 FEV1 降低分支。修复前该输入被判「通气功能正常」；默认态无此分型串 ⇒ 强判别。"
},
{
  "slug": "pulmonology/pulmonary-function",
  "inputs": {
    "fev1": "3.0",
    "fvc": "3.5",
    "fev1pp": "85",
    "fvcpp": "95",
    "cutoffCustom": "0.90"
  },
  "expect": [
    "轻度气流受限"
  ],
  "ref": "自定义阈值/LLN 输入生效：一秒率 0.857 < 自定义 0.90 ⇒ 阻塞性；FEV1%pred 85 ⇒ GOLD 1（轻度）。默认态（阈值 0.70、FEV1%pred 68）为 GOLD 2「中度」⇒ 「轻度气流受限」仅注入态出现。"
},
{
  // 默认 mip=45 → 高于下限 43（正常）；注入 mip=30 → 吸气肌无力
  "slug": "pulmonology/pulmonary-rehab",
  "inputs": {
    "mip": "30",
    "mep": "30",
    "age": "65"
  },
  "expect": [
    "吸气肌无力"
  ],
  "ref": "auto-restore"
},
{
  // 默认 pao2=55/paco2=62 → II型呼衰；注入 80/40 → 未达呼衰标准
  "slug": "pulmonology/respiratory-failure",
  "inputs": {
    "pao2": "80",
    "paco2": "40",
    "fio2": "21",
    "age": "65"
  },
  "expect": [
    "无低氧性呼衰"
  ],
  "ref": "auto-restore"
},
  // 注：pulmonology/analysis-14 已于 2026-09-19 改为 TOOLBOX-REDIRECT 存根（重定向到同义真工具），不再是工具页，用例移除。
{
  // 默认 tumorType=0 → 0级原位/表浅；注入 3 → 3级浸润型
  "slug": "pulmonology/bronchoscopy-grading",
  "inputs": {
    "tumorType": "3"
  },
  "expect": [
    "提示浸润性癌，评估分期，可能需放化疗/手术"
  ],
  "ref": "auto-restore"
},
{
  // 8 题（q0-q7）每题 0-5；注入全 5 → 总分 40 → 极重度影响
  "slug": "pulmonology/copd-cat",
  "inputs": {
    "q0": "5",
    "q1": "5",
    "q2": "5",
    "q3": "5",
    "q4": "5",
    "q5": "5",
    "q6": "5",
    "q7": "5"
  },
  "expect": [
    "影响极重，多学科综合管理"
  ],
  "ref": "auto-restore"
},
{
  // 勾选 C(意识模糊)+U(尿素氮>7) → CURB-65 = 2 分 → 中危、30天死亡风险约 9.2%、建议住院。
  // 默认态 0 分 → 低危（约1.5%）/门诊治疗，故本 expect 具判别力。
  // checkIds 注入复选框选中态（页面用 getElementById(id).checked 读取，见 harness 2026-09-24 升级）。
  "slug": "pulmonology/curb65",
  "checkIds": [
    "c",
    "u"
  ],
  "expect": [
    "中(约9.2%)",
    "住院治疗"
  ],
  "ref": "CURB-65 五项各 1 分：C(意识模糊)+U(尿素氮>7)=2 → 中危（30天死亡风险约 9.2%）→ 住院治疗"
},
{
  // ACT 五项 a1-a5 各 1-5；注入全 4 → 总分 20 → 良好控制
  "slug": "pulmonology/gina-asthma",
  "inputs": {
    "a1": "4",
    "a2": "4",
    "a3": "4",
    "a4": "4",
    "a5": "4"
  },
  "expect": [
    "20/25 ACT总分 良好控制"
  ],
  "ref": "auto-restore"
},
{
  // 默认 T1a → ⅠA1期；注入 T2a/N0/M0 → ⅠB期
  "slug": "pulmonology/lung-cancer-tnm",
  "inputs": {
    "t": "T2a",
    "n": "N0",
    "m": "M0"
  },
  "expect": [
    "分期 = ⅠB期"
  ],
  "ref": "auto-restore"
},
{
  // 默认 size=9 → 4A（3个月复查）；注入 size=5 → 2 类（年度复查）
  "slug": "pulmonology/lung-rads",
  "inputs": {
    "type": "solid",
    "size": "5"
  },
  "expect": [
    "Lung-RADS 2 年度低剂量CT复查。"
  ],
  "ref": "auto-restore"
},
{
  // Wells 7 项（q0-q6，动态 id）注入全「是」→ 3+3+1.5+1.5+1.5+1+1 = 12.5 → 高风险
  "slug": "pulmonology/rater-13",
  "inputs": {
    "q0": "1",
    "q1": "1",
    "q2": "1",
    "q3": "1",
    "q4": "1",
    "q5": "1",
    "q6": "1"
  },
  "expect": [
    "PE概率约 49.9%"
  ],
  "ref": "auto-restore"
},
{
  // FTND 6 题（q0-q5，动态 id）注入 3/1/1/3/1/1 → 总分 10 → 极高依赖
  "slug": "pulmonology/self-assess-3",
  "inputs": {
    "q0": "3",
    "q1": "1",
    "q2": "1",
    "q3": "3",
    "q4": "1",
    "q5": "1"
  },
  "expect": [
    "尼古丁依赖程度极高，生理依赖严重，自行戒烟极困难，需专业医疗干预。"
  ],
  "ref": "auto-restore"
},
{
  // q1-q6 注入全 0 → 总分 0 → 轻度依赖（默认组合为 7 分重度依赖）
  "slug": "pulmonology/smoking-cessation",
  "inputs": {
    "q1": "0",
    "q2": "0",
    "q3": "0",
    "q4": "0",
    "q5": "0",
    "q6": "0"
  },
  "expect": [
    "依赖程度轻。以行为干预为主(识别触发情境、延迟技巧)"
  ],
  "ref": "auto-restore"
},
{
  // 默认 char=浆液性 → 无警示；注入 bloody → 血性痰警示
  "slug": "pulmonology/sputum-analysis",
  "inputs": {
    "char": "bloody"
  },
  "expect": [
    "血性痰需排查肺结核、肺癌、支扩"
  ],
  "ref": "auto-restore"
},
{
  // 勾选 S/T/O/P/BMI 共 5 项 → 5/8 → 高危（强烈建议 PSG）。
  // 原用例 inputs 为空、expect 取默认态输出 "0/8"（注入失败亦命中）⇒ 零判别力，已去默认化。
  "slug": "pulmonology/stop-bang",
  "checkIds": [
    "s",
    "t",
    "o",
    "p",
    "bmi"
  ],
  "expect": [
    "5/8"
  ],
  "ref": "STOP-BANG 八项各 1 分：S(打鼾)+T(疲倦)+O(呼吸暂停)+P(高血压)+BMI>35 = 5 → 5/8 → 高危"
},
{
  // 默认（harness 首选项）smear=3+ / culture=pos ⇒ 有传染性；注入涂片阴性 ⇒ 传染性低
  "slug": "pulmonology/tb-resistance",
  "inputs": {
    "smear": "neg",
    "culture": "pending",
    "xpert": "rif_s"
  },
  "clicks": [
    "document.getElementById('d_rif').checked=false;calc()"
  ],
  "expect": [
    "传染性低",
    "药物敏感结核(DS-TB)"
  ],
  "ref": "涂片阴性 + 培养未回 + Xpert 利福平敏感 ⇒ 依据 Xpert 仍可分型 DS-TB；infective = smear!=='neg' || culture==='pos' ⇒ false ⇒「传染性低」。原用例期望「有传染性，需呼吸道隔离」，而页面默认态（涂片 3+、培养阳性）本就含该串 ⇒ 逃生；改锚默认态不产生的阴性分支。默认态类型为 RR-TB（Xpert rif_r）⇒ 两条均不命中。"
},
{
  "slug": "pulmonology/tb-resistance",
  "clicks": [
    "document.getElementById('smear').value='neg';document.getElementById('culture').value='neg';document.getElementById('xpert').value='na';calc();var r=document.getElementById('result');r.innerHTML+=' 无证据拦截='+(r.innerHTML.indexOf('无细菌学证据')>=0)+' 有方案='+(r.innerHTML.indexOf('2HRZE')>=0);"
  ],
  "expect": ["无证据拦截=true 有方案=false"],
  "ref": "L-N40 证据门槛：涂片阴性/培养阴性/GeneXpert 未做 ⇒ 修复前直接输出 DS-TB 与 2HRZE/4HR 方案；现提示无细菌学证据、不给分型与方案。默认即为该态 ⇒ 用 clicks 并比对哨兵；默认无「耐药分型」卡片，哨兵不出现。"
},
{
  "slug": "pulmonology/tb-resistance",
  "clicks": [
    "document.getElementById('smear').value='neg';document.getElementById('culture').value='pos';document.getElementById('xpert').value='rif_r';document.getElementById('d_rif').checked=false;document.getElementById('d_inh').checked=false;document.getElementById('d_fq').checked=true;calc();"
  ],
  "expect": ["Pre-XDR-TB(准广泛耐药)", "MDR/RR + 耐氟喹诺酮"],
  "ref": "L-N40 RR-TB+FQ：利福平耐药（GeneXpert）且异烟肼敏感、氟喹诺酮耐药 ⇒ WHO 2021 属 Pre-XDR（MDR/RR + FQ）；修复前仅 rifR&&dInh 分支才查 FQ，RR-TB 被降级为普通 RR-TB。默认 d_rif 勾选且 d_fq 未勾 ⇒ 不命中。"
},
{
  "slug": "pulmonology/tb-resistance",
  "clicks": [
    "document.getElementById('smear').value='3+';document.getElementById('culture').value='pos';document.getElementById('xpert').value='rif_r';document.getElementById('d_rif').checked=false;document.getElementById('d_inh').checked=true;document.getElementById('d_pza').checked=true;calc();var r=document.getElementById('result');r.innerHTML+=' 含PZA提示='+(r.innerHTML.indexOf('吡嗪酰胺')>=0&&r.innerHTML.indexOf('须避免含该药')>=0)+' 含Xpert确认='+(r.innerHTML.indexOf('需培养/表型药敏确认')>=0);"
  ],
  "expect": ["含PZA提示=true 含Xpert确认=true"],
  "ref": "L-N40 PZA/分子确认：MDR（R+I 耐药）且 PZA 耐药时方案提示须避开 PZA；GeneXpert rif_r 但未勾选利福平耐药表型时提示需表型确认。修复前 MDR 分支完全忽略 PZA/EMB，也不提示 Xpert 需确认。默认 d_rif 勾选 ⇒ 确认提示不出现。"
},
{
  // 默认 rul_ap → 右上叶尖段（叩击同侧肩胛上方）；注入 rml → 右中叶（叩击右侧乳头下方）
  "slug": "pulmonology/vibration-percussion",
  "inputs": {
    "lobe": "rml"
  },
  "expect": [
    "叩击右侧乳头下方区域"
  ],
  "ref": "auto-restore"
},
{
  // 勾选 DVT(3)+其他诊断(3)+心率>100(1.5) → 7.5 分 > 6 → 高危（概率约 37.5%，直接 CTPA）。
  // 仅心率>100 = 1.5 分：原版三档低危阈值为 <2（含 1.5），应落低危；旧实现 if(score<=1) 误判中危。
  "slug": "pulmonology/wells-pe",
  "checkIds": ["hr"],
  "expect": ["总分 = 1.5"],
  "ref": "Wells PE 仅心率>100 = 1.5 分；三档分层低危为 <2 分（约 1.3%）、中危 2–6（约 16.2%）、高危 ≥7（约 37.5%）。1.5 必须落低危；旧实现 if(score<=1) 会把它误判为中危，零交集。",
},
{
  "slug": "pulmonology/wells-pe",
  "checkIds": [
    "dvt",
    "alt",
    "hr"
  ],
  "expect": [
    "37.5%"
  ],
  "ref": "Wells PE 加权：DVT 3 + 其他诊断可能 3 + 心率>100 1.5 = 7.5 > 6 → 高危（～37.5%）"
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

  console.log("==== pulmonology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
