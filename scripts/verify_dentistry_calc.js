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
  "expect": [
    "1.00"
  ],
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
  "slug": "dentistry/calc-1",
  "inputs": {
    "d": "5",
    "m": "3",
    "f": "4"
  },
  "expect": [
    "D+M+F = 12（恒牙龋坏、缺失、充填牙数之和）"
  ],
  "ref": "DMFT = D+M+F = 5+3+4 = 12 > 10 ⇒ classify 返回「龋病风险较高」（默认 d/m/f 全 0 ⇒ 风险较低）。结论串随输入连续变化，且非静态文案（原 expect「DMFT」相关单值零判别力）。"
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
  "expect": [
    "11.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/oral-cancer-screening",
  "inputs": {
    "t": "1"
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
    "color": "normal"
  },
  "expect": [
    "保持均衡饮食与口腔卫生"
  ],
  "ref": "auto-restore"
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
    "winter": "mesioangular"
  },
  "expect": [
    "mesioangular"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/zirconia-aesthetics",
  "inputs": {
    "position": "premolar"
  },
  "expect": [
    "premolar"
  ],
  "ref": "auto-restore"
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
  console.log("==== dentistry calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
