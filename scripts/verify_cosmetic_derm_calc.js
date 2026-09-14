#!/usr/bin/env node
/**
 * 第 38 道门禁：cosmetic-derm 分类计算正确性验证（25 个确定性数值/等级工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，且期望值经「假通过自检」复核不等于默认输出，杜绝假通过。
 * 期望串优先取「区分度足够」的数值/判定文案（避免 1~2 位数字串被输入框 value 命中而假通过）。
 * 跳过：
 *   - mesotherapy / cosmetic-injection / meso-cocktail：勾选态由 checkbox.checked 驱动，
 *     桩环境无法注入非默认勾选，改走默认态则与页面默认输出重合（无验证意义）；
 *   - fitzpatrick-wrinkle：光型为 radio（name=photo），非 id 注入；
 *   - injection / laser-parameters / jiguangbochangbadian / time-23 / wrinkle-dynamic-static 以外
 *     的纯文案页（无确定性数值输出）。
 * 用法: node scripts/verify_cosmetic_derm_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "cosmetic-derm/area-12",
    inputs: { area: "全脸", pct: "22", diam: "0.35" },
    expect: ["22.0", "0.35"],
    ref: "红斑面积占比 22% → 15≤22<30 属重度（III 级）；占比显示=22.0%、血管直径=0.35 μm（默认 面颊/10/0.2→10.0/0.20 避开）" },

  { slug: "cosmetic-derm/chemical-peel",
    inputs: { acidType: "lactic", concentration: "25", ph: "3.2", duration: "8", sensitivity: "1.2", firstTime: "0" },
    expect: ["20.51", "1.66"],
    ref: "乳酸 pKa=3.86：游离酸比例=1/(1+10^(3.2−3.86))=0.8191 → 浓度 25×0.8191=20.51%；"
       + "深度指数=20.51×8×(76/90)×1.2×1.0/100=1.66（默认 甘醇酸/35/2.5/5/1.0/首次 避开）" },

  { slug: "cosmetic-derm/concentration",
    inputs: { acid: "bha", conc: "25", ph: "2.8" },
    expect: ["10.08", "40.3"],
    ref: "BHA pKa=2.97：游离酸比例=10^(2.8−2.97)/(1+10^(2.8−2.97))=0.4032 → 游离酸浓度=25×0.4032=10.08%、"
       + "比例=40.3%（默认 aha/35/3.0→2.56/9.8 避开）" },

  { slug: "cosmetic-derm/formula-1",
    inputs: { total: "8", ha: "6", vc: "25", rHa: "40", rVc: "35", rPep: "25" },
    expect: ["3.20", "2.80", "19.20", "70.00"],
    ref: "配比合计=100：玻尿酸体积=8×0.40=3.20 ml、维生素C=8×0.35=2.80 ml；"
       + "含量：玻尿酸=3.20×6=19.20 mg、维C=2.80×25=70.00 mg（默认 10/5/20/50/30/20→5.00/3.00/2.00 避开）" },

  { slug: "cosmetic-derm/length-spacing",
    inputs: { len: "2.0", spacing: "300", dia: "200" },
    expect: ["1.60", "1111", "34.91"],
    ref: "穿透深度=2.0×0.8=1.60 mm；针密度=1/(0.03)²=1111 个/cm²（300 μm=0.03 cm）；"
       + "渗透面积占比=1111.11×π×0.01²×100=34.91%（默认 1.5/200/150→1.20/2500/44.18 避开）" },

  { slug: "cosmetic-derm/microneedle",
    inputs: { needleLength: "1.0", spacing: "1.0", diameter: "200", passes: "3", purpose: "delivery",
              mw: "5000", concentration: "2", area: "10" },
    expect: ["23.6", "20.03", "0.40"],
    ref: "有效深度=1.0×0.75=0.75 mm；密度=1/1²×100=100 孔/cm²、总孔数=100×10=1000；"
       + "单孔体积=π×0.1²×0.75/3=0.007854 mm³ → 总孔体积=1000×0.007854×3=23.56→23.6 μL；"
       + "MW 5kDa 因子 0.85 → 有效递送=23.56×0.85=20.03 μL；递送量=20.03×2/100=0.40 μg"
       + "（默认 1.5/0.5/150/4/50000/1/20 避开）" },

  { slug: "cosmetic-derm/ratio-composition-injection",
    inputs: { total: "7", ha: "10", rHa: "50", rVc: "25", rGsh: "15", rOther: "10" },
    expect: ["3.50", "1.75", "1.05", "87.50"],
    ref: "配比合计=100：体积 HA=7×0.50=3.50、VC=7×0.25=1.75、谷胱甘肽=7×0.15=1.05 ml；"
       + "含量：VC=1.75×50=87.50 mg（默认 5/8/60/20/10/10→3.00/1.00/0.50、24.00/50.00 避开）" },

  { slug: "cosmetic-derm/rf-tightening",
    inputs: { temp: "44", duration: "120", freq: "1", sessions: "3", interval: "4", cooling: "1" },
    expect: ["3.6", "44°C"],
    ref: "44℃∈[42,50] → 单次效果=(44−42)×120/180=1.3333；累积=1.3333×(1+0.9+0.81)=3.61→3.6"
       + "（默认 45/180/3 次→8.1 避开）" },

  { slug: "cosmetic-derm/sebumeter",
    inputs: { forehead: "100", nose: "160", cheek: "50", chin: "80", timePoint: "1", temp: "28" },
    expect: ["130", "95"],
    ref: "T区=(100+160)/2=130 μg/cm²；温度校正均值=97.5×(1−3×0.01)=94.58→95（默认 120/180/60/90/25→105/75/105 避开）" },

  { slug: "cosmetic-derm/spf-pa-calculator",
    inputs: { photo: "4", med: "10", uvi: "8", outdoorTime: "240", spf: "30", pa: "4",
              activity: "1", reapply: "60" },
    expect: ["3.1", "2.1", "SPF 50+", "PA++++"],
    ref: "UVI 8 → 有效 MED=10×5/8=6.25；理论=6.25×30=187.5 min；实际=187.5×1=187.5 min=3.1 h；"
       + "所需 SPF=⌈240/6.25/1⌉=39 → 推荐 SPF 50+；PPD(PA++++) =20 → UVA 保护=6.25×20=125 min=2.1 h；"
       + "UVI 8 >5 → 推荐 PA++++（默认 10/5/120/30/2/1→5.0/SPF 15+/PA+++ 避开）" },

  { slug: "cosmetic-derm/temp-time-4",
    inputs: { temp: "62", time: "8", rftype: "bi" },
    expect: ["40.6", "1.62"],
    ref: "62℃∈[60,70) → 分段收缩率=20+(62−60)/10×25=25%；时间因子=min(1+0.3×ln8,1.8)=1.6238；"
       + "收缩率=25×1.6238=40.6%（默认 60/5→20.3 避开）" },

  { slug: "cosmetic-derm/thread-lift",
    inputs: { zone: "jawline", threadType: "pcla", insertAngle: "50", liftAngle: "45",
              threadLength: "14", threadCount: "8", laxity: "1", anchorForce: "60" },
    expect: ["47.6", "381", "457"],
    ref: "下颌线最佳 55/50°、PCLA 系数 0.8：偏差 5°/5° → cos5°·cos5°=0.99240；"
       + "单线力=60×0.8×0.9924=47.6 g；总力=47.6×8=381 g；轻度松弛 ×1.2 → 有效 457 g"
       + "（默认 midface/单向锯齿/45/45/6/中度/50 避开）" },

  { slug: "cosmetic-derm/assessor-67",
    inputs: { cosType: "general", prodType: "cream", pb: "12", as: "2", hg: "0.5",
              methanol: "0.1", tvc: "100" },
    expect: ["不符合要求"],
    ref: "铅 12 > 普通化妆品限值 10 mg/kg → 任一项超标即「不符合要求」（默认 铅 5 ≤ 限值 → 符合，避开）" },

  { slug: "cosmetic-derm/calc-51",
    inputs: { uvb: "98", uva: "92" },
    expect: ["50.0", "12.5"],
    ref: "SPF=1/(1−0.98)=50.0；PFA=1/(1−0.92)=12.5，pfa∈[8,16) → PA+++（默认 96/85→25.0/6.7 避开）" },

  { slug: "cosmetic-derm/corneometer",
    inputs: { forehead: "70", cheek: "45", nose: "75", hand: "30", humidity: "60", product: "0" },
    expect: ["58"],
    ref: "湿度校正=(60−50)/10×3=+3 AU；四点=(73,48,78,33) → 均值=232/4=58 AU（默认 65/50/70/35/50→55 避开）" },

  { slug: "cosmetic-derm/telangiectasia-area",
    inputs: { areaPct: "20", density: "10", diameter: "0.4", vesselType: "venous", zone: "3", symptom: "1" },
    expect: ["81", "极重度毛细血管扩张"],
    ref: "评分=20×2.5+10×2+0.4×15+1×5=50+20+6+5=81 → ≥60 属极重度"
       + "（默认 15/8/0.3/面颊/偶发→67.0 也为极重度，故同时校验分数 81 区分）" },

  { slug: "cosmetic-derm/visia-spots",
    inputs: { spotCount: "6", areaPct: "4", depth: "2", zone: "2", spotType: "pih", percentile: "20" },
    expect: ["25.2", "中度色斑"],
    ref: "前额权重 1.0：评=(4×3+2×5+6/5+20/10)×1.0=(12+10+1.2+2)=25.2 → 20≤25.2<40 属中度色斑"
       + "（默认 15/8/5/颧骨/50→68.4 为极重度 避开）" },

  { slug: "cosmetic-derm/pore-grading",
    inputs: { noseTip: "2", nasalAla: "2", cheek: "3", forehead: "2", poreType: "oily", sebumLevel: "2" },
    expect: ["55", "中度毛孔粗大"],
    ref: "评=(2×3+2×3+3×2+2×2)/10×25=22/10×25=55 → 40≤55<60 属中度毛孔粗大"
       + "（默认 2/2/1/1→40 → 轻度 避开）" },

  { slug: "cosmetic-derm/glogau-photoaging",
    inputs: { wrinkle: "2", pigment: "4", keratosis: "3", makeup: "2", age: "4", photo: "3" },
    expect: ["2.9", "Ⅲ型"],
    ref: "评=(2×3+4×2+3×1.5+2×2+4×1.5)/10=28.5/10=2.85→2.9，Math.round(2.85)=3 → Ⅲ型"
       + "（默认 3/3/3/3/3→3.0 避开）" },

  { slug: "cosmetic-derm/aging-1",
    inputs: { wrinkle: "3", pigment: "1", age: "62" },
    expect: ["IV", "老年期"],
    ref: "Glogau 分型=['I','II','III','IV'][3]='IV'；评分=3×3+1×2+min(⌊62/20⌋,4)=9+2+3=14；"
       + "年龄 62 ≥60 → 老年期（默认 wrinkle=0/pigment=0/35→I、青中年期 避开）" },

  { slug: "cosmetic-derm/skin-ph",
    inputs: { phValue: "6.0", site: "cheek", postClean: "2", skincare: "1" },
    expect: ["6.00", "偏碱（偏高）"],
    ref: "pH 6.0 ∈(5.5,6.5] → 偏碱（偏高）；屏障健康分=100−|6.0−5.0|×30=70（默认 5.0→理想范围 避开）" },

  { slug: "cosmetic-derm/pifuphceding",
    inputs: { ph: "4.2", area: "面颊" },
    expect: ["4.2", "偏酸"],
    ref: "pH 4.2 ∈[4.0,4.5) → 偏酸；屏障健康度=100−|4.2−5.0|×25=80（默认 5.0→正常 避开）" },

  { slug: "cosmetic-derm/maokongcudafenji",
    inputs: { dia: "500", area: "鼻头", type: "aging" },
    expect: ["500", "中度粗大"],
    ref: "毛孔直径 500 μm ∈[400,800) → 2 级「中度粗大」（默认 350→轻度粗大 避开）" },

  { slug: "cosmetic-derm/eyebag-assessment",
    inputs: { fatHerniation: "3", skinLaxity: "2", tearTrough: "2", edema: "2", bagType: "fat", age: "4" },
    expect: ["48", "中度眼袋"],
    ref: "raw=3×3+2×2+2×2+2×2.5+4×0.5=24 → 评分=24×2=48 → 40≤48<60 属中度眼袋"
       + "（默认 2/2/2/1/40s-50s→40.0 为轻中度 避开）" },

  { slug: "cosmetic-derm/wrinkle-dynamic-static",
    inputs: { crow_d: "2", crow_s: "1", glab_d: "1", glab_s: "0", fore_d: "0", fore_s: "0",
              nas_d: "1", nas_s: "1", nl_d: "1", nl_s: "1" },
    expect: ["24", "0.5"],
    ref: "肉毒素合计=12(鱼尾 d2)+10(川字 d1)+0+2(鼻背 d1)+0=24 U；"
       + "填充合计=0+0+0+0+0.5(法令 s1)=0.5 ml（默认各部位 d/s=2/0,2/2,2/0,0/0,2/2 → 总 45U 避开）" },
];

async function main() {
  const only = process.argv.slice(2);
  const cases = only.length
    ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o))
    : CASES;
  let pass = 0;
  const errs = [];
  for (const c of cases) {
    const r = await runCase(c);
    if (r.ok) {
      pass++;
      console.log(`  OK ${c.slug} (${r.via})`);
    } else {
      errs.push(c);
      console.log(`  NG ${c.slug} -- expect ${JSON.stringify(c.expect)}`);
      console.log(`     ref: ${c.ref}`);
      if (r.why) console.log(`     why: ${r.why}`);
      if (r.errs && r.errs.length) console.log(`     errs: ${JSON.stringify(r.errs)}`);
      if (r.sample) console.log(`     got: ${String(r.sample).slice(0, 400)}`);
    }
  }
  console.log(`\n==== cosmetic-derm calc ${pass}/${cases.length} ====`);
  if (errs.length) {
    console.log("\nfailed:");
    errs.forEach((c) => console.log(`  - ${c.slug}: ${JSON.stringify(c.expect)}`));
    process.exit(1);
  }
}

main();
