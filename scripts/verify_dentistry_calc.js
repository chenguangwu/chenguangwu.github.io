#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "dentistry/alveolar-bone-loss",
  "inputs": {
    "remaining": "12",
    "rootLen": "14"
  },
  "expect": [
    "85.7%"
  ],
  "ref": "auto-restore"
},
  // 注：dentistry/analysis-11 已于 2026-09-19 改为 TOOLBOX-REDIRECT 存根（重定向到同义真工具），不再是工具页，用例移除。
{
  "slug": "dentistry/assessor-5",
  "inputs": {
    "thk": "3.5"
  },
  "expect": [
    "5.6%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/bite-contact",
  "inputs": {
    "lf": "38",
    "rf": "25",
    "lb": "30",
    "rb": "20"
  },
  "expect": [
    "33.6%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/bridge-span",
  "inputs": {
    "missingNum": "2"
  },
  "expect": ["2\nincisor\nincisor\npremolar\nmolar\n🦷 基牙 前磨牙 138mm² ⬛ 桥体 切牙 126mm² ⬛ 桥体 切牙 126mm² 🦷 基牙 磨牙 310mm² 448 基牙面积和 (mm²) 252 缺失牙面积和 (mm²) 1.78 面积比 基牙/缺失牙面积比 0 0.8 临界 1.0 达标 1.5 充足 符合Ante法则 建议：基牙支持力充足，固定桥设计可行。"],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/bruxism-force",
  "inputs": {
    "episodes": "23",
    "duration": "8",
    "emg": "60",
    "mvc": "600",
    "sleep": "7"
  },
  "expect": [
    "66240"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/bruxism-force",
  "inputs": {
    "episodes": "20",
    "duration": "8",
    "emg": "90",
    "mvc": "600",
    "sleep": "7"
  },
  "expect": [
    "重度磨牙症",
    "86400"
  ],
  "ref": "自建复合分：事件 20 次/夜→3 分、EMG 90%MVC→3 分，合计 6 分 ⇒ 重度磨牙症；峰值力 600×90%=540N，累计负荷 540×20×8=86400 N·s。"
     + "默认态（12 次/60%MVC ⇒ 4 分中度）不含「重度磨牙症」与 86400 ⇒ 强判别。该分档为工具自建，页面已标注非 ICSD 原文分级。"
},
{
  "slug": "dentistry/calc-1",
  "inputs": {
    "d": "5",
    "m": "3",
    "f": "4"
  },
  "expect": [
    "D+M+F = 12（恒牙龋坏、缺失、充填牙数之和）"
  ],
  "ref": "DMFT = D+M+F = 5+3+4 = 12 > 10 ⇒ classify 返回「龋病风险较高」（默认 d/m/f 为空 ⇒ 显示空态提示）。结论串随输入连续变化，且非静态文案（原 expect「DMFT」相关单值零判别力）。"
},
// 已移除 dentistry/calc-1 的空态守卫用例（inputs 0/0/0 + click 清空，expect「请填写龋坏（D）…」）。
// 原因：该页 DOMContentLoaded 启动即执行 `calc(1)`（explicit=1），而三个输入默认 value 均为空 ⇒
// 默认加载态**本来**就渲染同一条 tip-error「请填写…」，清空再点计算与默认态逐字节相同 ⇒ 判别力 0。
// 该 slug 另保留「5/3/4 ⇒ D+M+F = 12」与「0/0/0 ⇒ D+M+F = 0」两条可判别用例，故按纪律删除本条。
{
 "slug": "dentistry/calc-1",
 "inputs": {
   "d": "0",
   "m": "0",
   "f": "0"
 },
 "expect": [
   "D+M+F = 0（恒牙龋坏、缺失、充填牙数之和）"
 ],
 "ref": "0 是合法牙数（不是空输入）：d=m=f=0 → DMFT=0、风险较低，必须正常输出；若守卫误把数值 0 当空、或页面仍吞掉 0，则该串不出现。默认态为空 ⇒ 显示提示，故本用例非 all_default。"
},
{
  "slug": "dentistry/caries-risk",
  "inputs": {
    "f1": "1"
  },
  "expect": [
    "94%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/complete-denture",
  "inputs": {
    "rest": "113",
    "occlusal": "72",
    "age": "65",
    "targetFS": "3"
  },
  "expect": [
    "110.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/dental-arch-development",
  "inputs": {
    "age": "12",
    "ucWidth": "28",
    "lcWidth": "22",
    "leeway": "0"
  },
  "expect": [
    "12岁"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/gingival-index",
  "inputs": {
    "t16_0": "3",
    "t16_1": "3",
    "t16_2": "3",
    "t16_3": "3",
    "t16_bop": "1",
    "t21_0": "0",
    "t21_1": "0",
    "t21_2": "0",
    "t21_3": "0",
    "t21_bop": "0",
    "t24_0": "0",
    "t24_1": "0",
    "t24_2": "0",
    "t24_3": "0",
    "t24_bop": "0",
    "t36_0": "0",
    "t36_1": "0",
    "t36_2": "0",
    "t36_3": "0",
    "t36_bop": "0",
    "t41_0": "0",
    "t41_1": "0",
    "t41_2": "0",
    "t41_3": "0",
    "t41_bop": "0",
    "t44_0": "0",
    "t44_1": "0",
    "t44_2": "0",
    "t44_3": "0",
    "t44_bop": "0"
  },
  "expect": [
    "17% BOP阳性率"
  ],
  "ref": "6 牙 × 4 位点全部显式注入（动态 id `<tooth>_<si>`，未注入的位点 parseInt('')=NaN 会让 GI 整体变 NaN）：t16 四位点均 3、其余 0 ⇒ GI = 12/24 = 0.50（轻度牙龈炎）；BOP 仅 t16 为 1 ⇒ 1/6 = 16.67% → toFixed(0) = 17%（默认全 0 ⇒ GI 0.00「牙龈健康」/ BOP 0%「BOP阴性/极少」）。"
},
{
  "slug": "dentistry/implant-dimensions",
  "inputs": {
    "boneWidth": "11.5",
    "boneHeight": "12"
  },
  "expect": [ "9.5 最大可用直径" ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/oral-cancer-screening",
  "inputs": {
    "t": "1",
    "n": "0",
    "m": "0"
  },
  "expect": [
    "5年生存率75-85%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/oral-ulcer",
  "inputs": {
    "size": "8"
  },
  "expect": [
    "中间型/需进一步评估"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/orthodontic-force",
  "inputs": {
    "force": "90",
    "rsa": ""
  },
  "expect": [
    "0.692"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/periodontal-pocket",
  "inputs": {
    "pd": "8",
    "gmcej": "1"
  },
  "expect": [
    "9.0mm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/rater-risk-2",
  "inputs": {
    "d_exp": "2",
    "d_ms": "2",
    "d_diet": "2",
    "d_plaque": "2",
    "d_fluoride": "1",
    "d_flow": "0",
    "d_buffer": "0"
  },
  "expect": [
    "风险总分： 9 / 14 分"
  ],
  "ref": "7 维（exp/ms/diet/plaque/fluoride/flow/buffer）取 2+2+2+2+1+0+0 = 9 > 8 ⇒ 「高风险」（默认全 0 ⇒ 总分 0 「低风险」）。动态 id `d_<key>` 由 DIMS 模板拼接，harness 的 getElementById 按需建元素故可注入。"
},
{
  "slug": "dentistry/root-canal-length",
  "inputs": {
    "xray": "36",
    "mag": "5",
    "file": "20",
    "remain": "1",
    "safe": "0.5"
  },
  "expect": [
    "27.62"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/salivary-flow",
  "inputs": {
    "volume": "6.5",
    "time": "5"
  },
  "expect": [
    "1248"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/sialography",
  "checkIds": [
    "f_punctate",
    "f_globular",
    "f_cavitary"
  ],
  "expect": [
    "舍格伦综合征(Sjögren)"
  ],
  "ref": "勾选点状/球状/囊状扩张三项 ⇒ 「舍格伦综合征」命中 3 个特征（慢性复发性涎腺炎仅命中点状+球状 2 项）居首，confidence = 3/5 = 60% ⇒ 「较符合」。默认无勾选 ⇒ calc 早退输出「请勾选观察到的影像特征后判读。」"
},
{
  "slug": "dentistry/tongue-oral-health",
  "inputs": {
    "color": "red"
  },
  "expect": [
    "主要体质 阴虚内热",
    "调护建议 滋阴清热"
  ],
  "ref": "color=red（红舌）⇒ 主要体质「阴虚内热」（符合度 100%）、调护建议「滋阴清热：忌辛辣煎炸…」。⚠ 原注入 color=normal 恰为页面 select 默认选中项 ⇒ 默认态输出同样命中「保持均衡饮食与口腔卫生」（真逃生），故改注入非默认舌色。默认态为「正常/平和」，不含阴虚内热/滋阴清热。"
},
{
  "slug": "dentistry/tooth-preparation",
  "inputs": {
    "angle": "15",
    "height": "5",
    "diameter": "8"
  },
  "expect": [
    "7.5°"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/wisdom-tooth",
  "inputs": {
    "winter": "distoangular"
  },
  "expect": [ "4 方向评分", "远中阻生去骨量大" ],
  "ref": "winter=distoangular（远中阻生）⇒ Winter 方向评分 4（默认 mesioangular 为 1）、附加因素「远中阻生去骨量大」、总难度分 8（默认 5）。⚠ 原注入 mesioangular 恰为页面 select 默认选中项 ⇒ 默认态即输出「1 方向评分」（真逃生），故改注入非默认方向。"
},
{
  "slug": "dentistry/zirconia-aesthetics",
  "inputs": {
    "position": "premolar"
  },
  "expect": [ "1100 抗弯强度" ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/oral-cancer-screening",
  "inputs": { "t": "", "n": "", "m": "" },
  "expect": ["请输入原发肿瘤 T、淋巴结 N 与远处转移 M 后再分期。"],
  "ref": "原生缺陷修复：T/N/M 三个下拉改为「请选择…」空值默认，首屏不再直接给出 III 期与治疗方案。"
},
{
  "slug": "dentistry/oral-cancer-screening",
  "inputs": { "t": "is", "n": "0", "m": "0" },
  "expect": ["0期"],
  "ref": "正例：选择 Tis/N0/M0 后照常出 0 期（恢复原结论，空值占位不改变计算）。"
},
{
  "slug": "dentistry/caries-risk",
  "clicks": ["var __b=document.getElementById('result').innerHTML.replace(/<[^>]+>/g,' ');var __ok=/龋病风险分数/.test(__b)&&/当前为默认评分/.test(__b)&&!/风险等级|风险分级|建议|诊断|治疗/.test(__b);document.getElementById('result').innerHTML=__ok?'__CR_DEF_OK__':'__CR_DEF_FAIL__ '+__b;"],
  "expect": ["__CR_DEF_OK__"],
  "ref": "批 4 默认态：只出龋病风险分数 0/100 与避免新龋机会，结果区不含风险等级/建议/诊断/治疗。"
},
{
  "slug": "dentistry/caries-risk",
  "inputs": {"f1":"3","f2":"3","f3":"3","f4":"3","f5":"3","f6":"3","f7":"3","f8":"3","f9":"3"},
  "expect": ["极高风险"],
  "ref": "批 4 改动态：九项因素均取 3 分 ⇒ 加权总分 3 ⇒ 风险分 100 落「极高风险」；确认 dirty 置位后分级文案才出现。"
},
{
  "slug": "dentistry/caries-risk",
  "inputs": {"f1":"3","f2":"3","f3":"3","f4":"3","f5":"3","f6":"3","f7":"3","f8":"3","f9":"3"},
  "clicks": ["resetAll();var __b=document.getElementById('result').innerHTML.replace(/<[^>]+>/g,' ');var __ok=/龋病风险分数/.test(__b)&&/当前为默认评分/.test(__b)&&!/风险等级|风险分级|建议|诊断|治疗/.test(__b);document.getElementById('result').innerHTML=__ok?'__CR_RST_OK__':'__CR_RST_FAIL__ '+__b;"],
  "expect": ["__CR_RST_OK__"],
  "ref": "批 4 重置态：resetAll() 九项归 0 并清 dirty，风险等级与建议消失。"
},
{
  "slug": "dentistry/rater-risk-2",
  "clicks": ["var __b=document.getElementById('res').innerHTML.replace(/<[^>]+>/g,' ');var __ok=/风险总分/.test(__b)&&/当前为默认评分/.test(__b)&&!/风险等级|风险分级|建议|诊断|治疗/.test(__b);document.getElementById('res').innerHTML=__ok?'__DIMS_DEF_OK__':'__DIMS_DEF_FAIL__ '+__b;"],
  "expect": ["__DIMS_DEF_OK__"],
  "ref": "批 4 默认态：只出风险总分 0/14，结果区不含风险分级/建议。"
},
{
  "slug": "dentistry/rater-risk-2",
  "inputs": {"d_exp":"2","d_ms":"2","d_diet":"2","d_plaque":"2","d_fluoride":"2","d_flow":"2","d_buffer":"2"},
  "expect": ["高风险"],
  "ref": "批 4 改动态：七项因素均取 2 分 ⇒ 总分 14 落「高风险」；确认 dirty 置位后分级文案才出现。"
},
{
  "slug": "dentistry/rater-risk-2",
  "inputs": {"d_exp":"2","d_ms":"2","d_diet":"2","d_plaque":"2","d_fluoride":"2","d_flow":"2","d_buffer":"2"},
  "clicks": ["resetForm();var __b=document.getElementById('res').innerHTML.replace(/<[^>]+>/g,' ');var __ok=/风险总分/.test(__b)&&/当前为默认评分/.test(__b)&&!/风险等级|风险分级|建议|诊断|治疗/.test(__b);document.getElementById('res').innerHTML=__ok?'__DIMS_RST_OK__':'__DIMS_RST_FAIL__ '+__b;"],
  "expect": ["__DIMS_RST_OK__"],
  "ref": "批 4 重置态：resetForm() 七项归 0 并清 dirty，风险分级与防龋建议消失。"
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

  console.log("==== dentistry calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
