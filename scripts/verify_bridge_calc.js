#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const fs = require("fs");
globalThis.__tbFs = fs; // 供 clicks 内做源码形态判别（harness 点击串无 require）
const CASES = [
  // 原为 all_default 弱用例 + expect「满足要求」是判定文案（二值判读词，逃生项）。
  // 均布模式（calcMode 默认 uniform）：f = 5qL⁴/(384EI)，[f] = L/limitN。注入值刻意让校核不通过（跨分支）。
  { slug: "bridge/deflection-calc", inputs: {"inL":"30","inE":"32.5","inI":"0.08","inQ":"60","inLimit":"600"},
    expect: ["跨中最大挠度 f： 243.389 mm", "挠跨比： 1/123 （限值 1/600）"],
    ref: "EI = 32.5e9×0.08 = 2.6e9；q = 60 kN/m = 60000 N/m；f = 5×60000×30⁴/(384×2.6e9) = 0.243389 m → 243.389 mm；[f] = 30/600 = 0.05 m → 50.00 mm；挠跨比 = 30/0.243389 = 123.3 → 1/123 ⇒ 校核不通过（默认 12.821 mm / 1/1560 为通过）。**判定词「不满足/满足要求」一律不作 expect**（二值判读词）。" },
  // 原为 all_default 弱用例 + expect「单桩承担」是标签片段（逃生项）。
  // up = πd、Ap = πd²/4、侧阻 = up×Σ(qsi×li)、端阻 = qp×Ap、Ra = 侧阻+端阻、桩数 = ceil(N/Ra)。
  { slug: "bridge/foundation-calc", inputs: {"inD":"1.5","inL":"30","inQp":"1500","inQs1":"50","inL1":"8","inQs2":"70","inL2":"10","inQs3":"90","inN":"20000"},
    expect: ["单桩承载力经验估算值 Ra： 12923.7 kN", "总侧阻力： 10273.0 kN（侧阻合计 2180.0 kPa·m）", "需要桩数（初步）： 2 根（单桩承担 10000.0 kN）"],
    ref: "up = π×1.5 = 4.712 m；Ap = π×1.5²/4 = 1.7671 m²；侧阻区间和 = 50×8 + 70×10 + 90×(30−8−10) = 400+700+1080 = 2180 kPa·m；总侧阻 = 4.712×2180 = 10273.0 kN；端阻 = 1500×1.7671 = 2650.7 kN；Ra = 12923.7 kN；桩数 = ceil(20000/12923.7) = 2 根，单桩承担 10000.0 kN。（默认 d=1.2/L=25 得 Ra=6823.5、侧阻 5466.4，均失配）" },
  // 桩长截断：L=15、l1=10、l2=10 ⇒ 有效层厚 10/5/0（l1+l2>L），超桩长部分不计侧阻。
  // 修复前按 l1=10、l2=10 全长累加：侧阻合计 1050、总侧阻 3958.4、Ra 5315.6、需 4 根。
  { slug: "bridge/foundation-calc", inputs: {"inD":"1.2","inL":"15","inQp":"1200","inQs1":"45","inL1":"10","inQs2":"60","inL2":"10","inQs3":"80","inN":"20000"},
    expect: ["总侧阻力： 2827.4 kN（侧阻合计 750.0 kPa·m）", "单桩承载力经验估算值 Ra： 4184.6 kN", "需要桩数（初步）： 5 根（单桩承担 4000.0 kN）"],
    ref: "up = π×1.2 = 3.770 m；Ap = π×1.2²/4 = 1.1310 m²；有效层厚 e1=min(10,15)=10、e2=min(10,15−10)=5、e3=15−10−5=0；侧阻合计 = 45×10+60×5+80×0 = 750 kPa·m；总侧阻 = 3.770×750 = 2827.4 kN；端阻 = 1200×1.1310 = 1357.2 kN；Ra = 4184.6 kN；桩数 = ceil(20000/4184.6) = 5 根，单桩承担 4000.0 kN。默认 d=1.2/L=25 得 Ra=6823.5，不命中。" },
  // 原为 all_default 弱用例 + expect「活载」是标签片段（逃生项）。
  // factor(等级) 与 laneReduction(车道数) 双系数同时切换：Ⅱ级 0.75、4 车道 0.67（默认 Ⅰ级 1.0、3 车道 0.78）。
  { slug: "bridge/load-calc", inputs: {"inL":"40","inB":"10","inG":"150","inGrade":"2","inLane":"4","inQp":"4.0","inBw":"1.5"}, clicks: ["calc()"],
    expect: ["组合跨中弯矩 M： 54274.2 kN·m（均布 45269.4 + 集中 9004.8）", "组合支点剪力 V： 4977.2 kN", "集中荷载 Pk：基准 240.0 kN × 4 车道 × 折减 0.67 = 643.2 kN"],
    ref: "标准值：qk=7.875、Pk=240；qLane=21.105、qPeople=12、qTotal=183.105。按 1.2 恒载 + 1.4 活载：qDesign=1.2×150+1.4×(21.105+12)=226.347、PkDesign=336；Pk 基准=320×0.75=240，集中总值=240×4×0.67=643.2，PkDesign=900.48。M=226.347×40²/8+900.48×40/4=45269.4+9004.8=54274.2；V=226.347×20+900.48/2=4977.2。旧版集中荷载只计一次，三串均失配。默认（Ⅰ级/3 车道）亦不同。" },
  // 原为 all_default 弱用例 + expect「万元」是单位词（逃生项）。
  // 主梁混凝土 = 面积×跨径×梁数×孔数；铺装 = 桥宽×跨径×厚度×孔数；钢筋 = 混凝土×含筋率/1000；
  // 造价 = 混凝土量×单价 + 钢筋吨数×单价。
  { slug: "bridge/material-qty", inputs: {"inL":"25","inNbeam":"8","inArea":"1.0","inB":"9","inT":"0.2","inSpan":"6","inRatio":"150","inPc":"650","inPs":"5000"},
    expect: ["混凝土合计（主梁+铺装）： 1470.00 m³", "主梁钢筋估算： 180000 kg = 180.00 t（仅按主梁混凝土 × 含筋率 150 kg/m³，不含铺装/墩台/基础钢筋）", "材料造价（部分）：混凝土 95.55 万 + 主梁钢筋 90.00 万 = 185.55 万元"],
    ref: "主梁/孔 = 1.0×25×8 = 200 m³ → 全桥 200×6 = 1200 m³；铺装 = 9×25×0.2×6 = 270 m³；总量 = 1470 m³；钢筋 = 1200×150/1000 = 180.00 t（180000 kg）；造价 = 1470×650/10000 = 95.55 万 + 180×5000/10000 = 90.00 万 = 185.55 万元。默认（30/6/1.2/12/0.15/5/120/600/4500）总量 1350.00、钢筋 129.60 t、造价 139.32 万元，三串均失配。" },
  // 原为 all_default 弱用例 + expect「单孔总荷载」是标签片段（逃生项）。
  // 注意：harness 的 select 默认取**首个 option**（simple），而真机取 `selected`（continuous）⇒ 必须显式注入 inType。
  // 连续梁：内支点 M = wL²/12、跨中 M = wL²/24（简支则为 wL²/8）—— 注入后走连续梁分支。
  { slug: "bridge/span-calc", inputs: {"inLt":"400","inN":"4","inType":"continuous","inG":"180","inQ":"80"}, clicks: ["calc()"],
    expect: ["内支点最大弯矩： 216666.7 kN·m（M=(g+q)L²/12）", "单孔总荷载： 26000.0 kN", "中间桥墩： 3 个"],
    ref: "L = 400/4 = 100.00 m、桥墩 = 4−1 = 3 个；w = 180+80 = 260.0 kN/m；内支点 M = 260×100²/12 = 216666.7、跨中 M = 260×100²/24 = 108333.3；单孔总荷载 = 260×100 = 26000.0 kN。默认（300/5/150/60，harness 取首个 option=simple）落在简支分支：L=60.00、桥墩 4 个、跨中 M=94500.0、单孔总荷载 12600.0，三串均失配。" },
  {
    "slug": "bridge/deflection-calc",
    "inputs": {
      "inL": "42",
      "inE": "42",
      "inI": "42",
      "inQ": "42",
      "inP": "42",
      "inLimit": "800"
    },
    "expect": [
      "42\n42\n42\n800\n42\n0.965 mm\n52.50 mm\n1/43537"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"inL\":\"42\",\"inE\":\"42\",\"inI\":\"42\",\"inQ\":\"42\",\"inP\":\"42\",\"inLimit\":\"800\"}，输出区含「42\n42\n42\n800\n42\n0.965 mm\n52.50 mm\n1/4353…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "bridge/foundation-calc",
    "inputs": {
      "inD": "42",
      "inL": "42",
      "inQp": "42",
      "inQs1": "42",
      "inL1": "42",
      "inQs2": "42",
      "inL2": "42",
      "inQs3": "42",
      "inN": "42"
    },
    "expect": [
      "总侧阻力： 232754.3 kN（侧阻合计 1764.0 kPa·m）",
      "单桩承载力经验估算值 Ra： 290942.9 kN"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"inD\":\"42\",\"inL\":\"42\",\"inQp\":\"42\",\"inQs1\":\"42\",\"inL1\":\"42\",\"inQs2\":\"42\",\"inL2\":\"42\",\"inQs3\":\"42\",\"inN\":\"42\"}：有效层厚 e1=min(42,42)=42、e2=0、e3=0 ⇒ 侧阻合计 42×42=1764、总侧阻 π×42×1764=232754.3 kN、端阻 42×π×42²/4=58188.6 kN、Ra=290942.9 kN（修复前侧阻合计 3528、总侧阻 465508.6、Ra 523697.2）；默认 1.2/25 不命中 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "bridge/load-calc",
    "inputs": {
      "inL": "42",
      "inB": "42",
      "inG": "42",
      "inLane": "42",
      "inQp": "42",
      "inBw": "42",
      "inGrade": "2"
    },
    "clicks": ["calc();document.getElementById('__tbProbe').textContent='LANEBAD '+document.getElementById('resM').textContent;"],
    "expect": [
      "LANEBAD --"
    ],
    "ref": "车道数 42 越界（合法 1–8），calc 必须清空 resM 为 --；原自动用例按未校验的 42 车道算 829879.7 kN·m。默认 3 车道为 24899.0，不命中该探针值。"
  },
  {
    "slug": "bridge/span-calc",
    "inputs": {
      "inLt": "42",
      "inN": "42",
      "inG": "42",
      "inQ": "42",
      "inType": "continuous"
    },
    "clicks": ["calc()"],
    "expect": [
      "单孔跨径 L： 1.00 m",
      "中间桥墩： 41 个",
      "内支点最大弯矩： 7.0 kN·m"
    ],
    "ref": "L=42/42=1.00 m、桥墩 41 个；w=84、M内支点=84×1²/12=7.0。显式 clicks 调 calc，避免桩环境初始调用差异；默认 300/5 得 60.00 m、4 个、63000.0，三串均失配。"
  },
  {
    "slug": "bridge/material-qty",
    "inputs": {
      "inL": "42",
      "inNbeam": "42",
      "inArea": "42",
      "inB": "42",
      "inT": "42",
      "inSpan": "42",
      "inRatio": "42",
      "inPc": "42",
      "inPs": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42\n42\n42\n42\n42\n6223392.0 m³\n130691.23 t\n3111696.0 m³\n26687.15"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"inL\":\"42\",\"inNbeam\":\"42\",\"inArea\":\"42\",\"inB\":\"42\",\"inT\":\"42\",\"inSpan\":\"42\",\"inRatio\":\"42\",\"inPc\":\"42\",\"inPs\":\"42\"}，输出区含「42\n42\n42\n42\n42\n42\n42\n42\n42\n6223392.0 m³\n…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "bridge/deflection-calc",
    "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/bridge/deflection-calc.html','utf8');document.getElementById('__tbProbe').textContent='BRIDGEEX '+(h.indexOf('≈ 10.1 mm，约 L/594')<0&&h.indexOf('≈ 0.0017 mm')>=0?'OK':'BAD');"],
    "expect": ["BRIDGEEX OK"],
    "ref": "12-G6 算例纠偏：q=20、L=6、EI=2e8 按页内式 5qL⁴/(384EI)=1.69e-6 m≈0.0017 mm，旧深度解析误写「10.1 mm、L/594」（差约6000倍）。源码形态断言旧错串消失、新正确值出现；默认态不执行 clicks ⇒ 零逃生。"
  }
,
{
  "slug": "bridge/foundation-calc",
  "inputs": {"inD":"1.2","inL":"25","inQp":"1200","inQs1":"45","inL1":"10","inQs2":"60","inL2":"10","inQs3":"80","inN":"12000"},
  "clicks": ["calc();document.getElementById('inL').value='';calc();document.getElementById('__tbProbe').textContent='FDMISS '+document.getElementById('resRa').textContent+' '+(window._lastResult===null);"],
  "expect": ["FDMISS -- true"],
  "ref": "先算出有效结果，再清空桩长：calc 必须清空 resRa 为 -- 且 _lastResult=null，防止复制/历史沿用旧值。默认 L=25 为 6823.5 kN，不命中。"
},
{
  "slug": "bridge/foundation-calc",
  "inputs": {"inD":"1.2","inL":"25","inQp":"0","inQs1":"0","inL1":"10","inQs2":"0","inL2":"10","inQs3":"0","inN":"12000"},
  "clicks": ["calc();document.getElementById('__tbProbe').textContent='FDZERO '+document.getElementById('resNum').textContent+' '+(window._lastResult===null);"],
  "expect": ["FDZERO -- true"],
  "ref": "qp 与各层侧阻均为 0 ⇒ Ra=0，正荷载 12000 kN 下必须提示无法计算桩数，不再显示 0 根；resNum=-- 且不保留结果快照。"
},
{
  "slug": "bridge/foundation-calc",
  "inputs": {"inD":"1.2","inL":"25","inQp":"1200","inQs1":"45","inL1":"10","inQs2":"60","inL2":"10","inQs3":"80","inN":"0"},
  "clicks": ["calc();document.getElementById('__tbProbe').textContent='FDN0 '+(window._lastResult&&window._lastResult.nPile);"],
  "expect": ["FDN0 0"],
  "ref": "上部荷载 0 为合法零：Ra=6823.5 正常，nPile=0（无需按承载力布桩），不再因 N=0 早退。"
},
{
  "slug": "bridge/material-qty",
  "inputs": {"inL":"30","inNbeam":"6","inArea":"1.2","inB":"12","inT":"0.15","inSpan":"5","inRatio":"120","inPc":"600","inPs":"4500"},
  "clicks": ["calc();document.getElementById('inL').value='';calc();document.getElementById('__tbProbe').textContent='MQMISS '+document.getElementById('resConc').textContent+' '+(window._lastResult===null);"],
  "expect": ["MQMISS -- true"],
  "ref": "先算出有效结果，再清空桥梁长度：必须清空混凝土结果与复制快照，避免复制与当前输入不符的旧工程量。"
},
{
  "slug": "bridge/material-qty",
  "inputs": {"inL":"30","inNbeam":"6.5","inArea":"1.2","inB":"12","inT":"0.15","inSpan":"5","inRatio":"120","inPc":"600","inPs":"4500"},
  "clicks": ["calc();document.getElementById('__tbProbe').textContent='MQDEC '+document.getElementById('resConc').textContent+' '+(window._lastResult===null);"],
  "expect": ["MQDEC -- true"],
  "ref": "主梁片数 6.5 不是整数（原 parseInt 会截成 6 继续算），现拒绝并清空结果。"
},
{
  "slug": "bridge/load-calc",
  "inputs": {"inL":"30","inB":"12","inG":"0","inGrade":"1","inLane":"3","inQp":"3.0","inBw":"2"},
  "clicks": ["calc();document.getElementById('__tbProbe').textContent='LDG0 '+(window._lastResult?window._lastResult.qDesign.toFixed(3):'null');"],
  "expect": ["LDG0 51.198"],
  "ref": "恒载 0 为合法零（仅有活载）：qDesign=1.2×0+1.4×(24.57+12)=51.198 kN/m，不再因 g=0 早退。默认 g=120 的 qDesign=195.198，不命中。"
},
{
  "slug": "bridge/load-calc",
  "inputs": {"inL":"30","inB":"12","inG":"","inGrade":"1","inLane":"3","inQp":"3.0","inBw":"2"},
  "clicks": ["calc();document.getElementById('__tbProbe').textContent='LDMISS '+document.getElementById('resM').textContent+' '+(window._lastResult===null);"],
  "expect": ["LDMISS -- true"],
  "ref": "恒载为空（区别于合法 0）必须拒绝并清空结果/快照。"
},
{
  "slug": "bridge/span-calc",
  "inputs": {"inLt":"300","inN":"1","inType":"continuous","inG":"150","inQ":"60"},
  "clicks": ["calc();document.getElementById('__tbProbe').textContent='SPC1 '+document.getElementById('resL').textContent+' '+(window._lastResult===null);"],
  "expect": ["SPC1 -- true"],
  "ref": "连续梁 1 跨没有内支点，必须拒绝并提示改选简支梁；resL=-- 且不输出 L²/12、L²/24 系数。"
},
{
  "slug": "bridge/span-calc",
  "inputs": {"inLt":"300","inN":"1","inType":"simple","inG":"150","inQ":"60"},
  "clicks": ["calc();document.getElementById('__tbProbe').textContent='SPS1 '+document.getElementById('resL').textContent+' '+document.getElementById('resMmid').textContent;"],
  "expect": ["SPS1 300.00 m 2362500.0 kN·m"],
  "ref": "简支梁单跨合法：L=300 m、M=(150+60)×300²/8=2362500.0 kN·m，不受连续梁最少两跨限制。"
},
{
  "slug": "bridge/deflection-calc",
  "inputs": {"inL":"20","inE":"32.5","inI":"0.15","inQ":"0","inP":"200","inLimit":"400"},
  "clicks": ["calcMode='uniform';calc();document.getElementById('__tbProbe').textContent='DFQ0 '+document.getElementById('resF').textContent+' '+document.getElementById('resRatio').textContent;"],
  "expect": ["DFQ0 0.000 mm ∞（f=0）"],
  "ref": "均布荷载 0 合法：f=0，挠跨比显示 ∞（f=0），不再因 q=0 拒绝或除零。默认 q=30 得 12.821 mm，不命中。"
},
{
  "slug": "bridge/deflection-calc",
  "inputs": {"inL":"20","inE":"32.5","inI":"0.15","inQ":"","inP":"200","inLimit":"400"},
  "clicks": ["calcMode='uniform';calc();document.getElementById('__tbProbe').textContent='DFMISS '+document.getElementById('resF').textContent+' '+(window._lastResult===null);"],
  "expect": ["DFMISS -- true"],
  "ref": "均布荷载为空（区别于合法 0）必须拒绝并清空结果/快照。"
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

  console.log("==== bridge calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();