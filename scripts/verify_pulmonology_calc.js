#!/usr/bin node
"use strict";
// 第十七批（pulmonology）弱用例去默认化：
// 全部用例采用「非默认输入 + 独立复算 expect」，expect 必须依赖被测点的计算结果，
// 不得取页面源码字面量或输入值回显（注入失败时用例必须 FAIL）。
const { runCase } = require("./verify_it_calc.js");
const fs = require("fs");
globalThis.__tbFs = fs;
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
  // 心源性肺水肿固定档：EPAP 8 + PS 5 = IPAP 13
  "slug": "pulmonology/niv-settings",
  "inputs": {
    "indication": "cardiac",
    "ph": "7.30"
  },
  "expect": [
    "EPAP(呼气相正压)= 8 cmH₂O",
    "压力支持 PS = IPAP − EPAP = 13 − 8 = 5 cmH₂O"
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
  "expect": ["10.0% 肺压缩估计 少量气胸但有症状","BTS 最大胸膜间距 ≥2 cm"],
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
  "slug": "pulmonology/gina-asthma",
  "inputs": {
    "a1": "3",
    "a2": "4",
    "a3": "3",
    "a4": "4",
    "a5": "3"
  },
  "expect": [
    "17/25 ACT总分 未良好控制（部分控制）"
  ],
  "ref": "D-N104 四档回归：3+4+3+4+3=17 落 16–19「未良好控制（部分控制）」；旧实现把 <20 一律判「未控制」，与预设「部分控制」自相矛盾。默认首屏为空值提示，零交集。"
},
{
  "slug": "pulmonology/gina-asthma",
  "inputs": {
    "a1": "3",
    "a2": "3",
    "a3": "3",
    "a4": "3",
    "a5": "3"
  },
  "expect": [
    "15/25 ACT总分 控制很差"
  ],
  "ref": "D-N104 下界：15 分属 ≤15「控制很差」，旧实现统称「未控制」；与 17 分档互斥，可判别四档是否真正拆开。"
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
  "slug": "pulmonology/lung-rads",
  "inputs": {
    "type": "solid",
    "size": "15"
  },
  "expect": [
    "Lung-RADS 4B"
  ],
  "ref": "D-N108 边界：实性 15mm 按同页公式「不低于 15mm 为 4B」应判 4B；旧实现 `size<15 → 4A` 之外的分支虽为 4B，但引入 15 整边界用例锁定。默认 9mm ⇒ 4A，不命中。"
},
{
  "slug": "pulmonology/lung-rads",
  "inputs": {
    "type": "solid",
    "size": "3"
  },
  "checkIds": ["malignant"],
  "clicks": [
    "calc();var b=document.getElementById('result').innerHTML;document.getElementById('result').innerHTML=(/Lung-RADS类别/.test(b)&&/>2</.test(b))?'__LR3_OK__':'__LR3_FAIL__'+b"
  ],
  "expect": [
    "__LR3_OK__"
  ],
  "ref": "D-N110 4X 守卫：3mm 实性属 2 类，即使勾选典型恶性征象也不得升 4X；旧实现对任意大小升 4X。clicks 校验结果卡类别仍为 2，默认 9mm 不勾征象为 4A，若守卫失效则输出 FAIL。"
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
    "极低依赖。以行为干预为主"
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
  "slug": "pulmonology/stop-bang",
  "checkIds": [
    "s",
    "t"
  ],
  "clicks": [
    "calc();var b=document.getElementById('result').innerHTML;document.getElementById('result').innerHTML=(/2\\/8/.test(b)&&/低危/.test(b))?'__SB2_OK__':'__SB2_FAIL__'+b"
  ],
  "expect": [
    "__SB2_OK__"
  ],
  "ref": "D-N113 性别默认值：G 项原为 `checked`，女性用户不主动取消时只会打鼾/疲倦也会被抬成 3 分中危；改为默认不勾选后 S+T=2 分应落「2/8 低危」。clicks 读结果区比对分数与等级后写标记，若默认仍勾选则得 3/8 中危 ⇒ FAIL。"
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
    "document.getElementById('smear').value='3+';document.getElementById('culture').value='pos';document.getElementById('xpert').value='rif_r';document.getElementById('d_rif').checked=false;calc();var r=document.getElementById('result');r.innerHTML+=' 列表一致='+(r.innerHTML.indexOf('利福平（GeneXpert 分子提示）')>=0&&r.innerHTML.indexOf('耐药：无')<0);"
  ],
  "expect": ["列表一致=true"],
  "ref": "Xpert rif_r 已足以判 RR-TB，但药敏勾选未勾利福平时旧版耐药列表写「无」，同屏矛盾。新版列表补「利福平（GeneXpert 分子提示）」。"
},
{
  "slug": "pulmonology/tb-resistance",
  "clicks": [
    "document.getElementById('smear').value='3+';document.getElementById('culture').value='pos';document.getElementById('xpert').value='rif_s';document.getElementById('d_rif').checked=false;document.getElementById('d_inh').checked=true;document.getElementById('d_fq').checked=true;calc();var r=document.getElementById('result');r.innerHTML+=' INHFQ='+(r.innerHTML.indexOf('常规「RZE + 氟喹诺酮」方案不适用')>=0)+' 含左氧='+(r.innerHTML.indexOf('左氧氟沙星')>=0);"
  ],
  "expect": ["INHFQ=true 含左氧=false"],
  "ref": "INH 单耐药 + FQ 耐药：旧版固定推荐 RZE+氟喹诺酮，会把已耐药的左氧/莫西写进方案；新版必须提示方案不适用且结果不列左氧。"
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
},
  { slug: "pulmonology/light-criteria",
    inputs: { pfProt: "", sProt: "", pfLdh: "", sLdh: "", sLdhUl: "" },
    expect: ["请填写胸水与血清蛋白/LDH（均需大于 0）后再判读。"],
    ref: "空态守卫：五项全清空时不再按 0 计算（旧实现 → 蛋白比值 0.00/LDH 比值 0.00 → 判「漏出液」），改为只输出填写提示。默认态 42/65/320/200/250 有值 ⇒ 提示串不出现。" },
{
  "slug": "pulmonology/gina-asthma",
  "inputs": { "g1": "1", "g2": "0", "g3": "0", "g4": "0" },
  "clicks": ["document.getElementById('g4').value='';calcGina();document.getElementById('result').textContent='PARTIAL:'+document.getElementById('result').innerHTML.replace(/<[^>]*>/g,'').trim();"],
  "expect": ["PARTIAL:请输入四项 GINA 控制问题（是/否）后再评估控制水平。"],
  "ref": "原生缺陷修复：GINA 四项（是/否）与 ACT 五题（1-5 分）共 9 个下拉全部改为「请选择」空值默认，首屏不再直接给「未控制/完全控制」分级与升级/降级治疗建议。"
}

,
{
  "slug": "pulmonology/gina-asthma",
  "clicks": ["(function(){var recs=[];globalThis.TBKit={util:{isEn:function(){return false;},exportTable:function(){},diffBox:function(){}},matrix:{table:function(){}},chart:{line:function(){}},preset:{bar:function(){}},history:{list:function(){return recs.slice().reverse();},last:function(){return recs.length?recs[recs.length-1]:null;},record:function(r){recs.push(r);},mount:function(){}}};var oS=__gina_asthmaSnap,oR=__gina_asthmaResText;__gina_asthmaSnap=function(){return {g1:'1',a1:'5'};};var call=0;__gina_asthmaResText=function(){call++;return call===1?'GINA 良好控制':'ACT 25/25 完全控制';};__gina_asthma_skip=false;__gina_asthmaExtras('gina');__gina_asthmaExtras('act');__gina_asthmaSnap=oS;__gina_asthmaResText=oR;var ok=(recs.length===2&&recs[0].__tbType==='gina'&&recs[1].__tbType==='act');document.getElementById('__tbProbe').textContent='GINAREC '+(ok?'OK':'BAD n='+recs.length+' t0='+(recs[0]&&recs[0].__tbType)+' t1='+(recs[1]&&recs[1].__tbType));})()"],
  "expect": ["GINAREC OK"],
  "ref": "第307批：两个包装共用 __gina_asthmaExtras 有 now-last<1000 时间节流，预设回调同步 calcGina();calcAct() 会吞掉第二条致 ACT 不入库；且记录须带评估类型。连续两次 Extras('gina')/Extras('act') 且结果文本不同，须各入库一条并分别标记 __tbType；修复前节流使 n=1、或类型缺失 ⇒ BAD。"
},
{
  "slug": "pulmonology/gina-asthma",
  "clicks": ["(function(){var cb=null;globalThis.TBKit={util:{isEn:function(){return false;},exportTable:function(){},diffBox:function(){}},matrix:{table:function(){}},chart:{line:function(){}},preset:{bar:function(){}},history:{list:function(){return [{t:1700000000000,d:{__tbScore:1,'结果':'x'}}];},last:function(){return null;},record:function(){},mount:function(s,c){cb=c;}}};__gina_asthmaRender(['g1','a1'],'结果',false);var calls=[];var oG=calcGina,oA=calcAct;calcGina=function(){calls.push('gina');};calcAct=function(){calls.push('act');};if(cb)cb({g1:'1',g2:'0',g3:'0',g4:'0','结果':'GINA 良好控制',__tbScore:1,__tbType:'gina'});calcGina=oG;calcAct=oA;var ok=(!!cb&&calls.length===1&&calls[0]==='gina');document.getElementById('__tbProbe').textContent='GINAREPLAY '+(ok?'OK':'BAD '+calls.join(',')+' cb='+(!!cb));})()"],
  "expect": ["GINAREPLAY OK"],
  "ref": "第307批：GINA 与 ACT 共用 #result，历史回放旧版无条件先 calcGina() 后 calcAct()，后者覆盖前者 ⇒ 回放 GINA 记录却显示 ACT。修复后按记录 __tbType 重算，回放 __tbType=gina 的记录须只调 calcGina（calls=[gina]）；修复前 calls=[gina,act] ⇒ BAD。"
},
{
  "slug": "pulmonology/pulmonary-function",
  "inputs": { "fev1": "2", "fvc": "3", "fev1pp": "60", "fvcpp": "" },
  "expect": ["请输入有效的 FEV1%pred 与 FVC%pred"],
  "ref": "03-112 核销：FEV1%pred/FVC%pred 空值不再按 0 判「混合性通气功能障碍 GOLD 4」，改为拦截提示。"
},
{
  "slug": "pulmonology/pneumothorax",
  "inputs": { "a": "", "b": "2", "c": "2" },
  "expect": ["请填写 A/B/C 三处胸膜间距"],
  "ref": "03-117 核销：三处间距任一空值即拦截，不再按 0 输出「0% 少量气胸，可观察吸氧」。"
},
{
  "slug": "pulmonology/self-assess-3",
  "expect": ["当前为默认评分（6 题均为默认选项）"],
  "ref": "03-152 核销：默认未作答时只显示「当前为默认评分…请按实际修改后查看解读」，不再直接输出 7 分「高度依赖」与戒烟处方。"
},
{
  "slug": "pulmonology/bronchoscopy-grading",
  "inputs": { "stenGrade": "3" },
  "expect": ["管腔狭窄71%-99%", "III级 重度"],
  "ref": "03-167 去默认化：注入 III 级（页面首屏默认 II 级）⇒ 管腔狭窄 71%-99%、分级「III级 重度」；旧实现写 25%–50% 或缺分级文案，两锚均失配。判别器纯默认态为 II 级 50%-70%，不含本串（早期写 II 级是逃生项，已改 III 级）。"
},
{
  "slug": "pulmonology/wells-pe",
  "clicks": ["document.getElementById('hr').checked=true;calc();"],
  "expect": ["1.5 Wells总分", "总分 = 1.5"],
  "ref": "03-158 核销：仅勾选心率得 1.5 分，Wells 三分类 <2 为低危 1.3%（原 score<=1 会误判中危），首屏不再预置 hr。原「低危 (PE概率 ～1.3%)」在纯默认快照也命中（逃生），改用注入勾选决定的总分双锚。"
},
{
  "slug": "pulmonology/curb65",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+\"/tools/pulmonology/curb65.html\",\"utf8\");var reg=h.indexOf(\"TBKit.preset.bar(\")>=0;var p0=h.indexOf(\"0 \u5206 \u00b7 \u4f4e\u5371\u95e8\u8bca\")>=0;var p2=h.indexOf(\"2 \u5206 \u00b7 \u4e2d\u5371\u4f4f\u9662\")>=0;var p4=h.indexOf(\"4 \u5206 \u00b7 \u9ad8\u5371 ICU \u8bc4\u4f30\")>=0;document.getElementById(\"__tbProbe\").textContent=(reg&&p0&&p2&&p4)?\"__CURB_PRESET_OK__\":\"__CURB_PRESET_BAD__ \"+[reg,p0,p2,p4].join(\",\");"],
  "expect": [
    "__CURB_PRESET_OK__"
  ],
  "ref": "第1102批 N32：预设函数旧为空壳、预设tab空白；补 3 个预设（0分门诊/2分住院/4分高危），显式设置 c/u/r/b1/b2/age65 六项。源码形态五哨兵，旧版必红。"
},{
  "slug": "pulmonology/curb65",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/pulmonology/curb65.html','utf8');var dd=JSON.parse(globalThis.__tbFs.readFileSync(process.cwd()+'/i18n/tools/content_deepdive.json','utf8'))['pulmonology/curb65'];var ok=h.indexOf('var mortByScore=[0.7,2.1,9.2,14.5,40,null]')>=0&&h.indexOf('<td>40%</td>')>=0&&h.indexOf('<td>数据不确定</td>')>=0&&h.indexOf('<td>0.7%</td>')>=0&&h.indexOf('死亡风险</th>')<0&&h.indexOf('高(≥15%)')<0&&h.indexOf('4–5 分重点考虑 ICU/HDU')>=0&&h.indexOf('score>=4?')>=0&&dd.examples[0].body.indexOf('14.5%')>=0&&dd.examples[1].body.indexOf('0.7%')>=0;document.getElementById('__tbProbe').textContent='CURBMORT '+(ok?'OK':'BAD');"],
  "expect": ["CURBMORT OK"],
  "ref": "12-N31：CURB-65 死亡率原 0–1 合并 1.5%、≥3 统一 ≥15%，4/5 分（Lim 2003 为 40%/57%）被严重低估；ICU 阈值公式框 ≥3、表格/代码 ≥4、深解 3 分三处冲突。现代码按逐分数组 [0.7,2.1,9.2,14.5,40,57] 展示、表格逐分、公式框与深解统一 4–5 分重点 ICU。源码形态哨兵，旧版必红。"
},{
  "slug": "pulmonology/curb65",
  "checkIds": ["c", "u", "r", "b1", "age65"],
  "expect": ["具体死亡率不确定", "考虑ICU/HDU"],
  "ref": "Five criteria selected: retain high-risk assessment without assigning the conflicting 57% to the derivation cohort."
},{
  "slug": "pulmonology/oxygenation-index",
  "inputs": { "pao2": "65", "fio2": "150", "spo2": "95" },
  "expect": ["FiO2 应在 21–100% 之间，请重新填写。"],
  "ref": "03-192 FiO2 范围校验：旧版 parseFloat||21 无范围校验，150% 算出 P/F≈43「重度ARDS」、-10% 走兜底 P/F 0 且 FiO₂ 显示负值。本批用原始字符串判空 + 21–100 拦截。默认 fio2=40 合法不命中，零逃生。"
},{
  "slug": "pulmonology/respiratory-failure",
  "inputs": { "pao2": "", "paco2": "40", "fio2": "21", "age": "65" },
  "expect": ["请输入 PaO₂（>0 mmHg）与 PaCO₂（>0 mmHg）后再判断呼吸衰竭类型。"],
  "ref": "03-165 血气呼衰空值守卫：旧版 pao2/paco2 空值 ||0 → pao2=0<60 直接判「I型呼衰」并算虚假 A-a 梯度。本批 PaO2/PaCO2 必填 >0，空/0/非法拦截不出分型。保留 paco2=40/fio2=21/age=65 合法，仅清空 pao2 命中；默认 pao2=55 合法不命中，零逃生。"
},{
  "slug": "pulmonology/oxygenation-index",
  "inputs": { "pao2": "", "fio2": "40", "spo2": "92" },
  "expect": ["请输入 PaO₂（>0 mmHg）后再计算氧合指数与 ARDS 分级。"],
  "ref": "03-190 氧合指数 PaO2 空值守卫：旧版 ||0 → P/F=0 落入「重度ARDS」+PEEP默认勾选直接给 ECMO 建议。本批 PaO2 必填 >0，空/0 拦截。保留 fio2=40/spo2=92 合法，仅清空 pao2 命中（先过 FiO2 校验）；默认 pao2=65 合法不命中，零逃生。"
},{
  "slug": "pulmonology/light-criteria",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/pulmonology/light-criteria.html','utf8');var noOld=h.indexOf('0.67')<0&&h.indexOf('above 0.67')<0;var hasNew=(h.match(/>0\.6 /g)||[]).length>=1&&h.indexOf('LDH ratio above 0.6,')>=0;document.getElementById('__tbProbe').textContent='LIGHT164 '+(noOld&&hasNew?'OK':'BAD');"],
  "expect": ["LIGHT164 OK"],
  "ref": "03-164 Light 标准引据表 LDH 阈值口径：公式框/表格/代码均为 0.6（Light 1972 原值），独引据表 data-zh 中文与英文写 0.67。本批改为 0.6 并同步英文。源码形态哨兵：无 0.67、含新 0.6；默认态不产哨兵（仅 clicks 读源码），零逃生。"
},
{ slug:"pulmonology/anti-tb-dosing", inputs:{"wt":"","age":""}, expect:["请填写必要的输入参数后再计算"], ref:"全部输入留空不得输出 0/0.00 假结果（NUMCLR）" },
{ slug:"pulmonology/sputum-analysis", inputs:{"vol":""}, expect:["请填写必要的输入参数后再计算"], ref:"全部输入留空不得输出 0/0.00 假结果（NUMCLR）" },
  {
    "slug": "pulmonology/anti-tb-dosing",
    "inputs": {"wt": "-10", "age": "40"},
    "expect": ["⚠ 体重须在 0–250 kg（不含 0），年龄须在 0–120 岁。"],
    "ref": "负体重按分段给量会得到负剂量而非报错；新守卫应拒绝。默认 55/40 不含该提示。"
  },
{
  "slug": "pulmonology/lung-cancer-tnm",
  "inputs": {"t":"T2b","n":"N0","m":"M0"},
  "expect": ["分期 = ⅡA期"],
  "ref": "AJCC 第 8 版 T2bN0M0 为 ⅡA；旧实现返回 ⅠB。"
},
{
  "slug": "pulmonology/lung-cancer-tnm",
  "inputs": {"t":"T3","n":"N2","m":"M0"},
  "expect": ["分期 = ⅢB期"],
  "ref": "AJCC 第 8 版 T3N2M0 为 ⅢB；旧实现落入 ⅢA。"
},
{
  "slug": "pulmonology/copd-cat",
  "inputs": {"q0":"3","q1":"3","q2":"3","q3":"3","q4":"3","q5":"3","q6":"3","q7":"5"},
  "expect": ["21/40 CAT总分 重度影响"],
  "ref": "第 8 题反向计分：其余 7 题各 3 分 =21；q7=5（完全没有精力）反向计 0，总分 21。按 CAT 分级 21–30 为重度影响；旧实现同向计 5 得 26，同样落入重度但总分错误。"
},
{
  "slug": "pulmonology/smoking-cessation",
  "inputs": {"q1":"1","q2":"1","q3":"1","q4":"1","q5":"1","q6":"0"},
  "expect": ["中度依赖","需专业/药物辅助"],
  "ref": "5 分属中度依赖，卡片与分级应一致；旧卡片 >=6 才提示药物辅助。"
},
{
  "slug": "pulmonology/anti-tb-dosing",
  "inputs": {"wt":"20","age":"30"},
  "expect": ["本页为成人固定剂量方案"],
  "ref": "低体重不得套用成人固定剂量；旧实现 20 kg 给 PZA 1500（75 mg/kg）。"
},
{
  "slug": "pulmonology/oxygenation-index",
  "inputs": {"pao2":"65","fio2":"40","spo2":"92"},
  "checkIds": ["peep"],
  "expect": ["未满足柏林前提","未排除（不满足柏林前提）"],
  "ref": "PEEP 已建立但未勾选非心源性：旧实现仍直接定级中度 ARDS；现拦截并提示前提未满足。"
},
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
