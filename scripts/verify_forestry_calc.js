#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "forestry/area-18",
  "inputs": {
    "scale": "4",
    "coords": "0,0\n100,0\n100,80\n0,80"
  },
  "expect": [
    "128000.00"
  ],
  "ref": "独立复算：矩形顶点 100×80 = 8000 m²；比例尺 1:4 ⇒ 面积按 4²=16 倍放大，8000×16 = 128000.00 m²。"
},
{
  "slug": "forestry/calc-57",
  "inputs": {
    "total": "150",
    "covered": "65"
  },
  "expect": [
    "0.43 郁闭度",
    "43.3% 覆盖率"
  ],
  "ref": "独立复算：郁闭度 = 覆盖点 65 ÷ 总样点 150 = 0.4333 ⇒ 0.43（两位小数）；覆盖率 = 43.3%；判别档 0.40~0.69 ⇒ 中郁闭度。原 expect「65/150」只是输入回显。"
},
{
  "slug": "forestry/concentration-5",
  "inputs": {
    "conc": "2700"
  },
  "expect": [
    "2700"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。"
},
{
  "slug": "forestry/density-5",
  "inputs": {
    "area": "900",
    "n": "80",
    "dbh": "16"
  },
  "expect": [
    "17.87"
  ],
  "ref": "独立复算：单株断面积 g = π/4×D² = 0.7854×0.16² = 0.020106 m²；样地 900 m² 内 80 株 ⇒ 公顷断面积 = 80×0.020106÷900×10000 = 17.872 ⇒ 17.87 m²/ha。默认态（n 60 / dbh 14）为 10.26。"
},
{
  "slug": "forestry/density-6",
  "inputs": {
    "sp": "2",
    "rp": "3",
    "area": "100",
    "cost": "2.5",
    "species": "马尾松"
  },
  "expect": [
    "41666.88"
  ],
  "ref": "独立复算：马尾松选种会覆盖株行距为 2×2 ⇒ 单株占地 4.00 m²；每亩 = 666.67÷4 = 166.6675 ⇒ 167；每公顷 = 10000÷4 = 2500；总株数 = 166.6675×100 = 16666.75 ⇒ 16667；总成本 = 16666.75×2.5 = 41666.875 ⇒ 41666.88；每亩成本 = 416.67。注意注入的 rp=3 被 species 预设改写，实际按 2×2 复算。"
},
{
  "slug": "forestry/estimate-32",
  "inputs": {
    "area": "1001",
    "n": "120",
    "dbh": "14",
    "h": "12",
    "f": "0.5"
  },
  "expect": [
    "110.72"
  ],
  "ref": "独立复算：单株材积 = π/4×0.14²×12×0.5 = 0.092363 m³；120 株合计 11.0836 m³；样地 1001 m² ⇒ 每公顷 = 11.0836÷1001×10000 = 110.724 ⇒ 110.72 m³/ha。"
},
{
  "slug": "forestry/estimate-33",
  "inputs": {
    "len": "8",
    "w": "25",
    "n": "12",
    "tarea": "50"
  },
  "expect": [
    "30.000"
  ],
  "ref": "独立复算：样带覆盖面积 = 2×样线长 8 km×单侧距离 25 m = 0.400 km²；种群密度 = 12÷0.400 = 30.000 只/km²；区域面积输入 50 km² ⇒ 50×100 = 5000 ha；估算种群 = 30×50 = 1500 只。"
},
{
  "slug": "forestry/forest-area",
  "inputs": {
    "slope": "7",
    "len1": "50",
    "len2": "80",
    "len3": "50",
    "pointCount": "4",
    "px'+i+'": "'+pts[i].x+'",
    "py'+i+'": "'+pts[i].y+'"
  },
  "expect": [
    "7°"
  ],
  "ref": "⚠ 输入回显（结构性不可修）：坡度量卡直接回显注入的 slope=7，其余样地顶点由动态键注入、非固定输入，无可独立复算的派生量，维持原断言不制造逃生。"
},
{
  "slug": "forestry/log-volume",
  "inputs": {
    "diameter": "30",
    "length": "4",
    "quantity": "1"
  },
  "expect": [
    "0.3438"
  ],
  "ref": "独立复算（GB 4814，D=30 cm ≥ 14 走长公式）：V = 0.00007854×4×(30 + 0.5×4 + 0.005×16 + 0.000125×4×(14−4)²×(30−10))² = 0.00031416×(32.08+1.00)² = 0.00031416×1094.29 = 0.34377 ⇒ 0.3438 m³。"
},
{
  "slug": "forestry/pest-1",
  "inputs": {
    "damaged": "53",
    "total": "200"
  },
  "expect": [
    "26.50% 发生率",
    "147 健康株数"
  ],
  "ref": "独立复算：发生率 = 受害 53 ÷ 总 200 × 100 = 26.50%；健康株数 = 200 − 53 = 147；发生率 26.5% ≥ 重度阈值 ⇒ 判「重度」。原 expect「53/200」只是输入回显。"
},
{
  "slug": "forestry/shengwuduoyangxingshannon",
  "inputs": {
    "data": "30 10 5 3"
  },
  "expect": [
    "1.029",
    "0.743"
  ],
  "ref": "独立复算：N=48，p=0.625/0.2083/0.1042/0.0625 ⇒ H=−Σp ln p=1.029；J=H/ln4=0.743；Simpson D=1−Σp²=0.551；Margalef=(4−1)/ln48=0.775。默认态 23/15/12/8/5 ⇒ H=1.488、J=0.925，两条均不命中。"
},
{
  "slug": "forestry/strength-4",
  "inputs": {
    "stock": "270",
    "ratio": "25",
    "cycle": "10",
    "area": "500"
  },
  "expect": [
    "202.50"
  ],
  "ref": "独立复算：采伐量 = 蓄积 270 × (1 − 保留率 25%) = 270×0.75 = 202.50 m³；采伐周期 10 年 ≠ 0 时只影响年均量卡，本条锚单次采伐量；面积 500 不参与该式。"
},
{
  "slug": "forestry/yield",
  "inputs": {
    "area": "150",
    "density": "55",
    "yield": "15",
    "price": "8",
    "rate": "85"
  },
  "expect": [
    "841500.00"
  ],
  "ref": "独立复算：总株数 = 面积 150 亩×密度 55 株/亩 = 8250 株；产材 = 8250×单株 15 kg×出材率 85% = 105,187.5 kg；产值 = 105,187.5×8 元/kg = 841,500.00 元。"
},
{
  "slug": "forestry/tree-volume",
  "inputs": {
    "dbh": "26",
    "height": "16",
    "formFactor": "0.41",
    "quantity": "37",
    "species": "0.41"
  },
  "expect": [
    "二元材积 0.3816 100%",
    "一元材积 0.2281 60%",
    "实验形数 0.4136 108%",
    "平均形数 0.3483 91%"
  ],
  "ref": "注入非默认（默认 dbh=20/height=14/formFactor=0.42/quantity=1；实测默认四值为 0.2033 / 0.1205 / 0.2243 / 0.1847）。独立复算（D=26、H=16、f=0.41，断面积 g=0.00007854×26²=0.05309304 m²）：① 二元材积 V=0.00005877×D^1.963×H^0.8594 = 0.00005877×599.2288×10.8348 = 0.381565 ⇒ 0.3816（相对值基准 100%）；② 一元材积 V=0.0000826×26^2.432=0.228137 ⇒ 0.2281，相对 0.228137÷0.381565=59.8% ⇒ 60%；③ 实验形数 V=g×(H+3)×f=0.05309304×19×0.41=0.413595 ⇒ 0.4136，相对 108.4% ⇒ 108%；④ 平均形数 V=g×H×f=0.05309304×16×0.41=0.348290 ⇒ 0.3483，相对 91.3% ⇒ 91%。四条均取「多公式对比」表，与当前选中公式 tab 无关（真机 Chrome 实测与桩输出逐值一致）；单株主值随 tab 切换（默认「实验形数」0.4136），故不锚主值，避免 tab 状态差异造成假红。默认态 0.2033/0.1205/0.2243/0.1847 与四锚全不命中。"
},
{
  "slug": "forestry/growth-rate",
  "inputs": {
    "v1": "0.08",
    "v2": "0.22",
    "years": "8",
    "metric": "dbh"
  },
  "expect": [
    "11.67% 普雷斯勒",
    "13.48% 复利",
    "0.0175 年生长量"
  ],
  "ref": "注入非默认（默认 v1=0.1/v2=0.15/years=5/metric=volume）并把计量单位切到 dbh（年生长量单位随之由 m³ 变 cm）。独立复算：总生长量 = V₂ − V₁ = 0.22 − 0.08 = 0.14 cm；普雷斯勒生长率 = (V₂/V₁^(1/n) − 1) × 100 = (0.22/0.08^(1/8) − 1) × 100；0.08^(1/8) = e^(ln0.08/8) = e^(−2.5257/8) = e^(−0.31571) = 0.72931 ⇒ 0.22/0.72931 = 0.30167 ⇒ 11.67%（按页面四舍五入口径 11.67%）。复利生长率 = ((V₂/V₁)^(1/n) − 1) × 100 = ((2.75)^(1/8) − 1) × 100；(2.75)^(1/8) = e^(1.01160/8) = e^0.126450 = 1.134815 ⇒ 13.48%。连年生长量 = 0.14 / 8 = 0.0175 cm/年。默认态（0.1→0.15、5 年、m³）输出 8.00% / 8.45% / 0.0100，三条均不命中。"
  },

  // ── §7.4 零用例加固 · forestry 余 4 页（探针实测取锚；输入区动态渲染，注入全部控件值）────
  {
    "slug": "forestry/carbon-sequestration",
    "inputs": {"species": "2", "area": "50", "volume": "200", "age": "30", "carbonPrice": "100"},
    "expect": ["146.7 生物量(t/ha)", "13.4 总CO₂(千吨)", "134.5 碳汇价值(万元)"],
    "ref": "蓄积量法：species=2（杨树 ρ=0.378、BEF=1.94、CF=0.5）、V=200 m³/ha ⇒ 生物量=200×0.378×1.94=146.664→146.7 t/ha；碳=73.3；CO₂=73.332×3.667=268.9 t/ha；总面积 50 ha ⇒ 总CO₂=13,445 t=13.4 千吨；碳价 100 ⇒ 13,445×100=134.5 万元。默认（杉木/10/120/20/60）各锚均不命中。原期望 183.3/336.1/56.02 来自旧参数模型，已按现行公式独立复算更正。"
  },
  {
    "slug": "forestry/forest-volume",
    "inputs": {"fConst": "2", "count": "30", "avgH": "20", "formFactor": "0.50", "area": "50"},
    "expect": ["600.0", "30000", "15000"],
    "ref": "注入非默认（默认 fConst=1/count=15/avgH=12/f=0.42/area=10，角规测树法）：G=F×Z=2×30=60；每公顷蓄积=60×20×0.50=600.0 m³；总蓄积=600×50=30000；出材率70%⇒21000、商品材50%⇒15000。默认态 37.8/378/265/189，三锚均不命中。"
  },
  {
    "slug": "forestry/planting-density",
    "inputs": {"spacing": "5", "rowSpacing": "5", "area": "200", "site": "poor"},
    "expect": ["25.00 m²", "5m × 5m", "27 株/亩"],
    "ref": "注入非默认（默认 spacing=2/rowSpacing=3/area=100/site=中）：株距×行距=5×5=25 m²/株 ⇒ 每株占地面积 25.00 m²、株行距配置 5m × 5m、每亩株数 666.67/25≈27 株/亩（默认 2×3=6 ⇒ 6.00 m²、2m × 3m、111 株/亩）。三锚均不命中；不锚面积 200（输入回显）。"
  },
  {
    "slug": "forestry/tree-age",
    "inputs": {"dbh": "30", "height": "20", "growthPerYear": "1.5", "seedlingAge": "3"},
    "expect": ["1.50 年均生长", "18-32 区间", "23 估算树龄"],
    "ref": "注入非默认（默认 dbh=20/h=12/g=0.8/seedlingAge=2）：年均生长=1.5 ⇒ 1.50 年均生长；估算树龄=23、区间 18-32（默认 0.8/27/21-38）。三锚均不命中。"
  },
  // ── 立地修正方向：好地 adj=1.15 应减小树龄（旧实现乘在年龄上反而放大）──
  {
    "slug": "forestry/tree-age",
    "inputs": {"dbh": "30", "height": "20", "growthPerYear": "1.5", "seedlingAge": "3"},
    "checkIds": ["considerSite"],
    "expect": ["1.72 年均生长", "16-28 区间", "20 估算树龄"],
    "ref": "勾选立地修正（adj=1.15）后生长量 = 1.5×1.15 = 1.725（JS toFixed(2) 落为 1.72）；年龄 = 30÷1.725+3 = 20.39 → 20；区间 = 30÷(1.725×1.3)+3 = 16.38 → 16、30÷(1.725×0.7)+3 = 27.84 → 28。旧实现把 adj 乘在年龄上（30÷1.5×1.15+3 = 26）方向相反；未勾选默认态为 23/18-32，三锚均不命中。"
  },
  // ── 造林密度：造林面积留空/为 0 时需苗量恒为 0，应拦截 ──────────
  {
    "slug": "forestry/planting-density",
    "inputs": { "spacing": "5", "rowSpacing": "5", "area": "0", "site": "poor" },
    "expect": ["请输入有效的株距、行距和造林面积"],
    "ref": "面积 0 ⇒ 需苗量 = 密度×0 = 0 株，旧实现照常给结论；修复后必须拦截。默认 100 亩不触发。"
  },
  // ── 定义域收紧：实验形数 / 根茎比 / 回归年 / 区域面积 ──────────────
  {
    "slug": "forestry/estimate-32",
    "inputs": { "area": "667", "n": "120", "dbh": "14", "h": "12", "f": "1.5" },
    "expect": ["实验形数 f 应在 0.1–0.9 之间"],
    "ref": "输入框声明 f 域 0.1–0.9（min/max/placeholder），旧校验只要求 f>0，f=1.5 会照算并放大 3 倍材积；改为超域显式拒绝。默认 0.5 不触发。"
  },
  {
    "slug": "forestry/strength-4",
    "inputs": { "stock": "270", "ratio": "25", "cycle": "0.5", "area": "500" },
    "expect": ["回归年 ≥ 1 年"],
    "ref": "回归年输入框声明 min=1、step=1，旧校验只要求 cycle>0，0.5 年会把年均采伐量放大一倍；改为 <1 显式拒绝。默认 10 年不触发。"
  },
  {
    "slug": "forestry/estimate-33",
    "inputs": { "len": "5", "w": "25", "n": "12", "tarea": "-5" },
    "expect": ["区域面积留空或 ≥ 0"],
    "ref": "区域面积为可选字段，旧实现遇负数直接静默跳过估算（NaN），用户无从察觉；改为负值显式拒绝、留空仍按不估算处理。默认 50 不触发。"
  },
  {
    "slug": "forestry/carbon-sequestration",
    "inputs": {},
    "clicks": ["selectMethod(1);document.getElementById('rootRatio').value='0.8';calc()"],
    "expect": ["根茎比应在 0.1–0.5 之间"],
    "ref": "生物量法下根茎比输入框声明 0.1–0.5，旧校验只要求 >0，0.8 会把总生物量放大到 1.8 倍；改为超域显式拒绝。默认方法 0（蓄积量法）不渲染该输入、不触发。"
  },
  {
    "slug": "forestry/shengwuduoyangxingshannon",
    "inputs": { "data": "30 10 5_X" },
    "expect": ["个体数须逐项为正数"],
    "ref": "旧实现 parseFloat('5_X') 会静默截成 5 继续统计，非法记号被悄悄吞掉；改为逐项校验有限正数并显式拒绝。默认合法数据不触发。"
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

  console.log("==== forestry calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
