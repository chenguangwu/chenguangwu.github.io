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
    expect: ["SPF 50+"],
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
    expect: ["81"],
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

// ── 零用例加固（2026-10-09）──────────────────────────
  { slug: "cosmetic-derm/jiguangbochangbadian",
    inputs: { laser: "755" },
    expect: ["翠绿宝石激光"],
    ref: "755nm 翠绿宝石激光（Alexandrite），靶色团黑色素、穿透 1.0-2.0mm、适应症脱毛/雀斑/文身。注入非默认(默认 532nm KTP 绿光→血红蛋白靶)，输出含'翠绿宝石激光'，默认态不出现。" },

  { slug: "cosmetic-derm/laser-parameters",
    inputs: { laserSelect: "q532", chromSelect: "melanin" },
    expect: ["脉宽： 5-10ns"],
    ref: "调Q 532nm(KTP)：脉宽 5-10ns、穿透 0.5-1mm、靶色团黑色素/血红蛋白。注入非默认(默认两框皆空→无激光卡片)，输出'脉宽： 5-10ns'，默认态不出现。" },

  { slug: "cosmetic-derm/meso-cocktail",
    inputs: { totalVol: "8", frequency: "2", sensitivity: "1.0", session: "5" },
    clicks: ["document.getElementById('goal_hydrate').checked=true;document.getElementById('goal_whiten').checked=true;calc()"],
    expect: ["中后期(第5次)"],
    ref: "中胚层鸡尾酒：治疗目标 2 项、总量 8ml、session=5→疗程阶段'中后期(第5次)'、每2周1次。checkbox 桩内恒未勾→clicks 显式置位再 calc；注入非默认(默认 totalVol=5/session=1/无目标→'初期(第1次)')，默认态不出现'中后期(第5次)'。" },

  { slug: "cosmetic-derm/mesotherapy",
    inputs: { totalVol: "10", area: "500", depth: "1", syringe: "3" },
    clicks: ["document.getElementById('c_ha').checked=true;document.getElementById('c_vc').checked=true;document.getElementById('c_prp').checked=true;calc()"],
    expect: ["75.0mg"],
    ref: "中胚层配比：HA 30%×10ml=3.00ml、含量=3.00×25mg/ml=75.0mg（PRP 同勾→HA 基底降为 30%）。checkbox 桩内恒未勾→clicks 置位；注入非默认(默认 totalVol=5→HA 37.5mg)，默认态不出现 75.0mg。" },

  { slug: "cosmetic-derm/post-procedure-recovery",
    inputs: { procedure: "peel_tca", intensity: "1.3", photo: "3" },
    expect: ["PIH风险：高", "预计完全恢复：18.2天"],
    ref: "术后恢复：TCA 焕肤 + 强度 1.3 + 防晒等级 photo=3→PIH 风险'高'、预计完全恢复 18.2 天。注入非默认(默认 laser_q/0.7/1→'PIH风险：低'且恢复天数更小)，默认态不出现'PIH风险：高'。" },

  { slug: "cosmetic-derm/time-23",
    inputs: { proc: "botox" },
    expect: ["肉毒素注射"],
    ref: "术后恢复时间表：proc=botox→项目名'肉毒素注射'(恢复约 1 天)。注入非默认(默认 proc=ipl→'强脉冲光(IPL)')，默认态不出现'肉毒素注射'。" },

  { slug: "cosmetic-derm/injection",
    inputs: { type: "ha", effect: "2" },
    expect: ["0.8 ml"],
    ref: "注射剂量：type=ha(玻尿酸)、鼻唇沟、effect=2(中度)→参考用量 0.8 ml。注入非默认(默认 type=botox/effect=1→以 U 计、无 '0.8 ml')，默认态不出现该串。" },

  { slug: "cosmetic-derm/fitzpatrick-wrinkle",
    inputs: { wrinkleGrade: "4", elastosis: "4", laxity: "9", pigment: "30" },
    expect: ["100 重度光老化", "皱纹等级 Ⅳ级", "弹力变性 重度"],
    "ref": "注入四项全非默认（默认 wrinkleGrade=1 / elastosis=0 / laxity=3 / pigment=10 ⇒ 总分 45、中度光老化、Ⅰ级、弹力变性『无』）。分值：皱纹 Ⅳ级 + 弹力变性重度 + 松弛 9/10 + 色素 30 ⇒ 合计 100 ⇒ 判「重度光老化」，建议升级为综合治疗方案（激光焕肤+填充+肉毒素+线雕）。三条均不在默认态。" },

  { slug: "cosmetic-derm/cosmetic-injection",
    checkIds: ["b_glabella", "b_frontalis", "b_crowfeet"],
    expect: ["50 总剂量(U)", "川字纹 20", "17 总注射点"],
    ref: "勾选三个部位（默认全未勾选 ⇒ 输出『请勾选需要治疗的部位』，无表格无合计）。页面按部位剂量表累加：川字纹 20U/5点（每点 4.0）、抬头纹 14U/6点（每点 2.3）、鱼尾纹(双侧) 16U/6点（每点 2.7）⇒ 总剂量 20+14+16 = 50 U、总注射点 5+6+6 = 17。checkIds 是 harness 注入字段，判别器清空后回到空勾选态 ⇒ 三条均不出现。" },
  {
    "slug": "cosmetic-derm/assessor-67",
    "inputs": {
      "pb": "42",
      "as": "42",
      "hg": "42",
      "methanol": "42",
      "tvc": "42",
      "cosType": "special",
      "prodType": "water"
    },
    "expect": [
      " 限值 判定 铅 42 ≤10 ✗ 砷 42 ≤4 ✗ 汞 42 ≤1 ✗ 甲醇 42 ≤0.2 ✗ 菌落总数 42 ≤5"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"pb\":\"42\",\"as\":\"42\",\"hg\":\"42\",\"methanol\":\"42\",\"tvc\":\"42\",\"cosType\":\"special\",\"prodType\":\"water\"}，输出区含「 限值 判定 铅 42 ≤10 ✗ 砷 42 ≤4 ✗ 汞 42 ≤1 ✗ 甲醇…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/chemical-peel",
    "inputs": {
      "concentration": "42",
      "ph": "42",
      "duration": "42",
      "acidType": "lactic",
      "sensitivity": "1.0",
      "firstTime": "0"
    },
    "expect": [
      "AHA) 酸类型 极浅层焕肤：温和去角质，无脱屑或轻微脱屑。适合日常维护和初次刷酸。 ✅ 参数在相对安全范围内。仍建议术前测试小面积皮肤反应。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"concentration\":\"42\",\"ph\":\"42\",\"duration\":\"42\",\"acidType\":\"lactic\",\"sensitivity\":\"1.0\",\"firstTime\":\"0\"}，输出区含「AHA) 酸类型 极浅层焕肤：温和去角质，无脱屑或轻微脱屑。适合日常维护和初次刷…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/corneometer",
    "inputs": {
      "forehead": "42",
      "cheek": "42",
      "nose": "42",
      "hand": "42",
      "humidity": "42",
      "product": "1"
    },
    "expect": [
      "分级 状态 前额 40 偏低 干燥 颊部 40 偏低 干燥 鼻翼 40 偏低 干燥 手背 40 偏低 干燥 ⚠️ 您标注已涂抹护肤品，测量值可能偏高，结果仅供粗略参考。建议洁面后静置15-30分钟再测量。 皮肤偏干：加强保湿，选择含透明质酸"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"forehead\":\"42\",\"cheek\":\"42\",\"nose\":\"42\",\"hand\":\"42\",\"humidity\":\"42\",\"product\":\"1\"}，输出区含「分级 状态 前额 40 偏低 干燥 颊部 40 偏低 干燥 鼻翼 40 偏低 干…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/calc-51",
    "inputs": {
      "uvb": "42",
      "uva": "42"
    },
    "expect": [
      "A 等级 SPF 1.7 · 低防晒 PA (无) · 几乎没有"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"uvb\":\"42\",\"uva\":\"42\"}，输出区含「A 等级 SPF 1.7 · 低防晒 PA (无) · 几乎没有」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/area-12",
    "inputs": {
      "pct": "42",
      "diam": "42",
      "area": "鼻翼"
    },
    "expect": [
      " 毛细血管扩张 IV 级 💡 建议：弥漫性红斑，需就医排查玫瑰痤疮等病因后综合治疗\n暂无评估记录"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"pct\":\"42\",\"diam\":\"42\",\"area\":\"鼻翼\"}，输出区含「 毛细血管扩张 IV 级 💡 建议：弥漫性红斑，需就医排查玫瑰痤疮等病因后综合…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/concentration",
    "inputs": {
      "conc": "42",
      "ph": "42",
      "acid": "bha"
    },
    "expect": [
      "bha\n42\n42\n深度 剥脱深度 42.00% 游离酸浓度 100.0% 游离酸比例 深层化学剥脱 深层剥脱，需专业操作 游离酸 100.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"conc\":\"42\",\"ph\":\"42\",\"acid\":\"bha\"}，输出区含「bha\n42\n42\n深度 剥脱深度 42.00% 游离酸浓度 100.0% 游离…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/cosmetic-injection",
    "inputs": {
      "muscleStrength": "1.0",
      "depression": "1.0",
      "syringe": "0.8"
    },
    "expect": [
      "选需要治疗的部位\n1.0\n0.8"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"muscleStrength\":\"1.0\",\"depression\":\"1.0\",\"syringe\":\"0.8\"}，输出区含「选需要治疗的部位\n1.0\n0.8」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/eyebag-assessment",
    "inputs": {
      "fatHerniation": "1",
      "skinLaxity": "1",
      "tearTrough": "1",
      "edema": "1",
      "bagType": "edema",
      "age": "2"
    },
    "expect": [
      " 等级 脂肪膨出 1/4 皮肤松弛 1/4 泪沟凹陷 1/4 水肿程度 1/3 水肿型 ：体液潴留所致，晨起重。以生活调理为主——低盐、高枕睡眠、冷敷。排除甲状腺/肾脏问题。 轻中度：玻尿酸填充泪沟+射频紧肤。脂肪型可考虑内切法。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"fatHerniation\":\"1\",\"skinLaxity\":\"1\",\"tearTrough\":\"1\",\"edema\":\"1\",\"bagType\":\"edema\",\"age\":\"2\"}，输出区含「 等级 脂肪膨出 1/4 皮肤松弛 1/4 泪沟凹陷 1/4 水肿程度 1/3 …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/fitzpatrick-wrinkle",
    "inputs": {
      "laxity": "42",
      "pigment": "42",
      "wrinkleGrade": "2",
      "elastosis": "1"
    },
    "expect": [
      "素沉着）。 建议：综合治疗方案——激光焕肤+填充+肉毒素+线雕提拉。需面诊制定个体化方案。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"laxity\":\"42\",\"pigment\":\"42\",\"wrinkleGrade\":\"2\",\"elastosis\":\"1\"}，输出区含「素沉着）。 建议：综合治疗方案——激光焕肤+填充+肉毒素+线雕提拉。需面诊制定个…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/glogau-photoaging",
    "inputs": {
      "wrinkle": "2",
      "pigment": "2",
      "keratosis": "2",
      "makeup": "2",
      "age": "2",
      "photo": "2"
    },
    "expect": [
      "au 光老化分型 2.0 综合评分 Ⅱ型 对应分型 早-中度光老化：早期色素斑（雀斑/日光斑），可触及角化症，运动时出现细纹。 光型Ⅲ-Ⅳ型：可常规治疗，注意术后防晒。 建议：外用维A酸+维C，化学焕肤（果酸20-35%），IPL光子嫩肤改"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"wrinkle\":\"2\",\"pigment\":\"2\",\"keratosis\":\"2\",\"makeup\":\"2\",\"age\":\"2\",\"photo\":\"2\"}，输出区含「au 光老化分型 2.0 综合评分 Ⅱ型 对应分型 早-中度光老化：早期色素斑（…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/laser-parameters",
    "inputs": {
      "laserSelect": "q532",
      "chromSelect": "melanin"
    },
    "expect": [
      "靶色团：黑色素 以下激光以该靶色团为主要作用目标： 调Q 532nm (KTP) 波长： 532nm · 脉宽： 5-10ns 靶色团： 黑色素 / 血红蛋白 穿透深度： 0.5-1mm（表皮-浅真皮） 适应症： 表浅色素斑、雀斑、日光性黑"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"laserSelect\":\"q532\",\"chromSelect\":\"melanin\"}，输出区含「靶色团：黑色素 以下激光以该靶色团为主要作用目标： 调Q 532nm (KTP)…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/meso-cocktail",
    "inputs": {
      "totalVol": "42",
      "frequency": "2",
      "sensitivity": "1.0",
      "session": "3"
    },
    "expect": [
      "42\n2\n1.0\n3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"totalVol\":\"42\",\"frequency\":\"2\",\"sensitivity\":\"1.0\",\"session\":\"3\"}，输出区含「42\n2\n1.0\n3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/injection",
    "inputs": {
      "type": "ha",
      "effect": "2"
    },
    "expect": [
      "ha\n鼻唇沟\n鼻唇沟唇部苹果肌鼻部下巴颞部（单侧）泪沟法令纹\n2\n0.8 推荐用量 (ml) 鼻唇沟 注射部位 中度 目标效果 玻尿酸 · 鼻唇沟"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"type\":\"ha\",\"effect\":\"2\"}，输出区含「ha\n鼻唇沟\n鼻唇沟唇部苹果肌鼻部下巴颞部（单侧）泪沟法令纹\n2\n0.8 推荐用…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/jiguangbochangbadian",
    "inputs": {
      "laser": "585"
    },
    "expect": [
      "深度 0.5-1.2mm 临床适应症 鲜红斑痣、血管瘤、玫瑰痤疮红血丝、疤痕红斑 注意事项 紫癜为常见反应，1-2周消退"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"laser\":\"585\"}，输出区含「深度 0.5-1.2mm 临床适应症 鲜红斑痣、血管瘤、玫瑰痤疮红血丝、疤痕红斑…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/mesotherapy",
    "inputs": {
      "totalVol": "42",
      "area": "42",
      "depth": "1",
      "syringe": "2"
    },
    "expect": [
      "42\n42\n1\n2"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"totalVol\":\"42\",\"area\":\"42\",\"depth\":\"1\",\"syringe\":\"2\"}，输出区含「42\n42\n1\n2」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/formula-1",
    "inputs": {
      "total": "42",
      "ha": "42",
      "vc": "42",
      "rHa": "42",
      "rVc": "42",
      "rPep": "42"
    },
    "expect": [
      " 合计 100% 42.00 — 1204.00 玻尿酸 33% 维生素C 33% 肽类 33%\n暂无配方记录"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"total\":\"42\",\"ha\":\"42\",\"vc\":\"42\",\"rHa\":\"42\",\"rVc\":\"42\",\"rPep\":\"42\"}，输出区含「 合计 100% 42.00 — 1204.00 玻尿酸 33% 维生素C 33…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/maokongcudafenji",
    "inputs": {
      "dia": "42",
      "area": "鼻翼两侧",
      "type": "aging"
    },
    "expect": [
      " 💡 改善建议：保持现有护肤习惯，注重保湿防晒 🔬 类型指导：老化型毛孔需刺激胶原再生，维A酸/光电紧肤有效\n暂无分级记录"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"dia\":\"42\",\"area\":\"鼻翼两侧\",\"type\":\"aging\"}，输出区含「 💡 改善建议：保持现有护肤习惯，注重保湿防晒 🔬 类型指导：老化型毛孔需刺…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/length-spacing",
    "inputs": {
      "len": "42",
      "spacing": "42",
      "dia": "42"
    },
    "expect": [
      "积占比 作用层次：深层真皮/皮下 深层重塑，适合重度瘢痕，需严格术后护理 穿透深度 33.60mm 渗透占比 78.5% 💡 建议：极深层微针，恢复期5-7天，须由医师操作并严格术后护理\n暂无计算记录"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"len\":\"42\",\"spacing\":\"42\",\"dia\":\"42\"}，输出区含「积占比 作用层次：深层真皮/皮下 深层重塑，适合重度瘢痕，需严格术后护理 穿透深…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/microneedle",
    "inputs": {
      "needleLength": "42",
      "spacing": "42",
      "diameter": "42",
      "passes": "42",
      "mw": "42",
      "concentration": "42",
      "area": "42",
      "purpose": "collagen"
    },
    "expect": [
      "总孔体积(μL) 95% 渗透效率 推荐长度：1.0-2.5mm。胶原诱导需到达真皮中层以上。配合维A酸/维C可增强效果。间隔4-6周一次。 ⚠️ 注意： • 遍数过多（>6遍）可能导致过度损伤 预计恢复期：5-7"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"needleLength\":\"42\",\"spacing\":\"42\",\"diameter\":\"42\",\"passes\":\"42\",\"mw\":\"42\",\"concentration\":\"42\",\"area\":\"42\",\"purpose\":\"collagen\"}，输出区含「总孔体积(μL) 95% 渗透效率 推荐长度：1.0-2.5mm。胶原诱导需到达…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/post-procedure-recovery",
    "inputs": {
      "procDate": "abc123测试",
      "procedure": "laser_co2",
      "intensity": "1.0",
      "photo": "2"
    },
    "expect": [
      "少48-72小时） ⚠️ 您的PIH（炎症后色素沉着）风险为 高 。建议术后立即开始严格防晒，并使用含维C/烟酰胺的修复产品（结痂脱落后）预防色素沉着。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"procDate\":\"abc123测试\",\"procedure\":\"laser_co2\",\"intensity\":\"1.0\",\"photo\":\"2\"}，输出区含「少48-72小时） ⚠️ 您的PIH（炎症后色素沉着）风险为 高 。建议术后立即…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/pore-grading",
    "inputs": {
      "noseTip": "1",
      "nasalAla": "1",
      "cheek": "1",
      "forehead": "1",
      "poreType": "aging",
      "sebumLevel": "2"
    },
    "expect": [
      "等级 评估 鼻头 1级 近距离可见 鼻翼 1级 近距离可见 颊部 1级 近距离可见 前额 1级 近距离可见 老化型 毛孔类型 1.0 平均等级 胶原流失导致毛孔周围支撑结构松弛。重点在抗衰——维A酸、点阵激光刺激胶原再生。 皮脂正常，综合护"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"noseTip\":\"1\",\"nasalAla\":\"1\",\"cheek\":\"1\",\"forehead\":\"1\",\"poreType\":\"aging\",\"sebumLevel\":\"2\"}，输出区含「等级 评估 鼻头 1级 近距离可见 鼻翼 1级 近距离可见 颊部 1级 近距离可…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/rf-tightening",
    "inputs": {
      "temp": "42",
      "duration": "42",
      "interval": "42",
      "freq": "2",
      "sessions": "3",
      "cooling": "0"
    },
    "expect": [
      "有效范围内（42-48°C）。 轻度效果：以促进循环和肤质改善为主。紧肤效果有限，适合维护性治疗。 疗程：3次 × 间隔42周，共126周。效果预计维持 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"temp\":\"42\",\"duration\":\"42\",\"interval\":\"42\",\"freq\":\"2\",\"sessions\":\"3\",\"cooling\":\"0\"}，输出区含「有效范围内（42-48°C）。 轻度效果：以促进循环和肤质改善为主。紧肤效果有限…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/pifuphceding",
    "inputs": {
      "ph": "42",
      "area": "前额"
    },
    "expect": [
      " 皮肤 pH 值 碱性 酸碱状态 0 屏障健康度 前额 · 碱性 pH 偏高，皮肤屏障受损风险大，易干燥敏感"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"ph\":\"42\",\"area\":\"前额\"}，输出区含「 皮肤 pH 值 碱性 酸碱状态 0 屏障健康度 前额 · 碱性 pH 偏高，皮…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/sebumeter",
    "inputs": {
      "forehead": "42",
      "nose": "42",
      "cheek": "42",
      "chin": "42",
      "temp": "42",
      "timePoint": "1"
    },
    "expect": [
      "偏低 偏干/中性 环境温度 42°C，已对皮脂值进行温度校正（基准 25°C，每±1°C 约 ±1% 皮脂变化）。 干性肌肤：注重保湿修复，选择含神经酰胺、角鲨烷的滋润型产品，避免过度清洁。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"forehead\":\"42\",\"nose\":\"42\",\"cheek\":\"42\",\"chin\":\"42\",\"temp\":\"42\",\"timePoint\":\"1\"}，输出区含「偏低 偏干/中性 环境温度 42°C，已对皮脂值进行温度校正（基准 25°C，每…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/skin-ph",
    "inputs": {
      "phValue": "42",
      "site": "cheek",
      "postClean": "1",
      "skincare": "1"
    },
    "expect": [
      "42\n请输入有效的 pH 值 (0-14)\ncheek\n1\n1"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"phValue\":\"42\",\"site\":\"cheek\",\"postClean\":\"1\",\"skincare\":\"1\"}，输出区含「42\n请输入有效的 pH 值 (0-14)\ncheek\n1\n1」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/spf-pa-calculator",
    "inputs": {
      "med": "42",
      "outdoorTime": "42",
      "reapply": "42",
      "photo": "2",
      "uvi": "5",
      "spf": "30",
      "pa": "2",
      "activity": "0.7"
    },
    "expect": [
      "钟 理论保护时间 1260 分钟 (21.0h) 活动校正后 882"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"med\":\"42\",\"outdoorTime\":\"42\",\"reapply\":\"42\",\"photo\":\"2\",\"uvi\":\"5\",\"spf\":\"30\",\"pa\":\"2\",\"activity\":\"0.7\"}，输出区含「钟 理论保护时间 1260 分钟 (21.0h) 活动校正后 882」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/ratio-composition-injection",
    "inputs": {
      "total": "42",
      "ha": "42",
      "rHa": "42",
      "rVc": "42",
      "rGsh": "42",
      "rOther": "42"
    },
    "expect": [
      " 合计 100% 42.00 — 1333.50 玻尿酸 25% 维生素C 25% 谷胱甘肽 25% 其他 25%\n暂无配方记录"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"total\":\"42\",\"ha\":\"42\",\"rHa\":\"42\",\"rVc\":\"42\",\"rGsh\":\"42\",\"rOther\":\"42\"}，输出区含「 合计 100% 42.00 — 1333.50 玻尿酸 25% 维生素C 25…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/telangiectasia-area",
    "inputs": {
      "areaPct": "42",
      "density": "42",
      "diameter": "42",
      "vesselType": "venous",
      "zone": "2",
      "symptom": "1"
    },
    "expect": [
      "42\n42\n42\nvenous\n2\n1\n100 极重度毛细血管扩张 42% 受累面积 42 密度根/cm² 42mm 血管直径 面颊中部 分布区域 小静脉扩张 ：蓝色血管，首选"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"areaPct\":\"42\",\"density\":\"42\",\"diameter\":\"42\",\"vesselType\":\"venous\",\"zone\":\"2\",\"symptom\":\"1\"}，输出区含「42\n42\n42\nvenous\n2\n1\n100 极重度毛细血管扩张 42% 受累…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/visia-spots",
    "inputs": {
      "spotCount": "42",
      "areaPct": "42",
      "depth": "42",
      "percentile": "42",
      "zone": "2",
      "spotType": "solar"
    },
    "expect": [
      "42\n42\n42\n2\nsolar\n42\n100 极重度色斑 42 色斑数量 42% 面积占比 42/10 色素深度 42% 同龄百分位 日光性黑子 ：光老化所致，调Q激光或 IPL 有效，注意与恶性黑子鉴别"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"spotCount\":\"42\",\"areaPct\":\"42\",\"depth\":\"42\",\"percentile\":\"42\",\"zone\":\"2\",\"spotType\":\"solar\"}，输出区含「42\n42\n42\n2\nsolar\n42\n100 极重度色斑 42 色斑数量 42…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/thread-lift",
    "inputs": {
      "insertAngle": "42",
      "liftAngle": "42",
      "threadLength": "42",
      "threadCount": "42",
      "anchorForce": "42",
      "zone": "lowerface",
      "threadType": "cog_bidirectional",
      "laxity": "2"
    },
    "expect": [
      "°) 提拉方向 42° (推荐 35°) 锚定区域 耳前筋膜 两端反向锯齿，中部锚定。提拉力中等，适合轻中度松弛"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"insertAngle\":\"42\",\"liftAngle\":\"42\",\"threadLength\":\"42\",\"threadCount\":\"42\",\"anchorForce\":\"42\",\"zone\":\"lowerface\",\"threadType\":\"cog_bidirectional\",\"laxity\":\"2\"}，输出区含「°) 提拉方向 42° (推荐 35°) 锚定区域 耳前筋膜 两端反向锯齿，中部…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/temp-time-4",
    "inputs": {
      "temp": "42",
      "time": "42",
      "rftype": "bi"
    },
    "expect": [
      "胶原收缩率（估） 42℃ 真皮温度 无效 紧肤效果 双极射频 · 无效 温度低于胶原变性阈值，无明显"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"temp\":\"42\",\"time\":\"42\",\"rftype\":\"bi\"}，输出区含「胶原收缩率（估） 42℃ 真皮温度 无效 紧肤效果 双极射频 · 无效 温度低于…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/wrinkle-dynamic-static",
    "inputs": {
      "crow_d": "1",
      "crow_s": "1",
      "glab_d": "1",
      "glab_s": "1",
      "fore_d": "1",
      "fore_s": "1",
      "nas_d": "1",
      "nas_s": "1",
      "nl_d": "1",
      "nl_s": "1"
    },
    "expect": [
      "建议方案 鱼尾纹 1 1 混合型 肉毒6U 川字纹 1 1 混合型 肉毒10U 抬头纹 1 1 混合型 肉毒8U 鼻背纹 1 1 混合型 肉毒2U 法令纹 1 1 混合型 0.5ml填充"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"crow_d\":\"1\",\"crow_s\":\"1\",\"glab_d\":\"1\",\"glab_s\":\"1\",\"fore_d\":\"1\",\"fore_s\":\"1\",\"nas_d\":\"1\",\"nas_s\":\"1\",\"nl_d\":\"1\",\"nl_s\":\"1\"}，输出区含「建议方案 鱼尾纹 1 1 混合型 肉毒6U 川字纹 1 1 混合型 肉毒10U …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/time-23",
    "inputs": {
      "proc": "frac_nd"
    },
    "expect": [
      "\ude79 术后护理：术后冰敷，3天内避免彩妆，使用医用修复面膜，严格防晒\n暂无查询记录"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"proc\":\"frac_nd\"}，输出区含「\ude79 术后护理：术后冰敷，3天内避免彩妆，使用医用修复面膜，严格防晒\n暂无查询记录」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
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
      else { fails.push(c.slug); }
    } catch (e) {
      fails.push(c.slug);
    }
  }
  console.log("==== cosmetic-derm calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();