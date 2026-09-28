#!/usr/bin/env node
/**
 * life 分类关键计算逻辑独立验证（收口批次 C）。
 *
 * 复用 scripts/verify_it_calc.js 的 DOM stub 与 runCase 框架。
 * 期望值一律由页面公式独立复算得出，不取页面输出。
 *
 * 用法：
 *   node scripts/verify_life_calc.js
 *   node scripts/verify_life_calc.js parking-fee percentage-calculator
 */
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  // ── 停车费（先扣免费时长，再按费率，最后套封顶）────────────────
  {
    slug: "life/parking-fee",
    inputs: { hours: "5.5", rate: "10", free: "1", cap: "60" },
    expect: ["45.00"],
    ref: "计费时长 = 5.5 − 1 = 4.5 h；费用 = 4.5 × 10 = 45.00（未触及封顶 60）",
  },
  // ── 百分比（占比）────────────────────────────────────────────
  {
    slug: "life/percentage-calculator",
    inputs: { isWhatX: "30", isWhatY: "150" },
    expect: ["30 是 150 的 20%"],
    ref: "30 ÷ 150 × 100 = 20 → 显示 20%（单断言“20%”会被页面默认 ofWhatPct=20 的区块命中 → 逃生项）",
  },
  // ── 温度换算（°F = °C×9/5+32）────────────────────────────────
  {
    slug: "life/temperature-converter",
    inputs: { celsius: "12.5" },
    expect: ["54.50", "285.65", "当前体感： 凉爽 12.5°C"],
    ref: "12.5×9/5+32 = 54.50°F；12.5+273.15 = 285.65K；体感 <15°C → 凉爽"
       + "（默认 25°C → 77.00°F / 298.15K / 舒适，注入失败即不命中）",
  },
  // ── 每日热量（Mifflin-St Jeor 男式）──────────────────────────
  {
    slug: "life/daily-calorie-needs",
    inputs: { bmrGender: "male", bmrAge: "30", bmrHeight: "175", bmrWeight: "70" },
    expect: ["1649"],
    ref: "10×70 + 6.25×175 − 5×30 + 5 = 1648.75 → round = 1649 千卡",
  },
  // ── 饮水计划（体重×30ml + 运动 + 高温 + 特殊）─────────────────
  {
    slug: "life/drinking-water-plan",
    inputs: { w: "70", act: "mid", temp: "26", stage: "normal" },
    expect: ["2,850.00"],
    ref: "基础 70×30 = 2100；运动中档 +500；26°C（≥25）+250；特殊 0 → 2850.00 ml",
  },
  // ── 罩杯换算（上下围差 → 罩杯索引）────────────────────────────
  {
    slug: "life/bra-size-converter",
    inputs: { under: "70", upper: "82.5" },
    expect: ["上下胸围差： 12.5 cm", "国际码： 70E", "罩杯： E 杯"],
    ref: "差 82.5−70 = 12.5 → cupIdx = round(12.5/2.5)−1 = 4 → cups[5] = E；下围 70 (<73) → 国际码 70E"
       + "（默认 75/90 → 差 15.0 cm、75F，注入失败即不命中）",
  },
  // ── 日期差（含开始日 +1）─────────────────────────────────────
  {
    slug: "life/date-difference-calculator",
    inputs: { startDate: "2025-12-25", endDate: "2026-01-01" },
    expect: ["7 天"],
    ref: "getDaysDiff(12-25 → 01-01) = 7 天",
  },
  // ── 生日悖论（23 人 ≈ 50.7%）────────────────────────────────
  {
    slug: "life/birthday-paradox",
    inputs: { n: "30", d: "365" },
    expect: ["70.6316%", "所有人生日不同的概率：29.3684%"],
    ref: "p = 1 − exp(Σ_{i=0..29} ln(1 − i/365)) = 1 − 0.29368432 = 0.70631568 → 70.6316%"
       + "（默认 23 人 → 50.7297%，注入失败即不命中）",
  },
  // ── 闰年判定（格里高利历规则）────────────────────────────────
  {
    slug: "life/leap-year-checker",
    inputs: { year: "1900", range: "12" },
    expect: ["1900 - 1911 年附近的闰年：", "1904、1908"],
    ref: "1900 能被 4 整除、但能被 100 整除且不能被 400 整除 ⇒ 平年（世纪非闰）；区间 1900..1911 内闰年仅 1904、1908"
       + "（默认 2024/range 10 → 2024、2028、2032，注入失败即不命中）",
  },
  // ── 单位换算（因子归一：m → cm）──────────────────────────────
  {
    slug: "life/unit-converter",
    inputs: { fromValue: "1", fromUnit: "meter", toUnit: "centimeter" },
    expect: ["100"],
    ref: "1 × factor(meter)=1 ÷ factor(cm)=0.01 = 100 → 结果 100",
  },
  // ── 选址加权模型（五项加权求和）──────────────────────────────
  {
    slug: "life/assessor-target",
    inputs: {
      traffic: "6000", competitors: "2", population: "4000",
      rent: "120", shopArea: "40", visibility: "7",
    },
    expect: ["综合评分： 70.5/100", "租金评分：80(15%)", "选址评级： 良好（推荐）"],
    ref: "人流 60×.30 + 竞争 70×.20 + 人口 80×.20 + 租金 80×.15 + 可见 70×.15 "
       + "= 18+14+16+12+10.5 = 70.5 → 60≤70.5<75 良好（推荐）"
       + "（默认 24+11+20+9+12 = 76.0 → 优秀，且租金档 60→80 跨档，注入失败即不命中）",
  },
  {
    "slug": "life/analysis-cost-9",
    "inputs": {
      "data": "研发,80\n营销,50\n生产,120\n管理,30"
    },
    "expect": [
      "成本合计： 280.00",
      "最大项： 生产"
    ],
    "ref": "成本结构：合计80+50+120+30=280.00、项均70.00、最大项生产120(42.86%)（独立复算；默认 原料42/人工31/物流15/能耗9 合计97、最大项原料，注入失败即不命中）"
  },
  {
    "slug": "life/analysis-80",
    "inputs": {
      "data": "A,8,100\nB,12,240\nC,5,50"
    },
    "expect": [
      "高发环节： C",
      "平均损耗率： 6.41%"
    ],
    "ref": "损耗率：A8/100=8.00%、B12/240=5.00%、C5/50=10.00%；损耗合计25、应售合计390、平均损耗率6.41%、高发环节C（独立复算；默认 进货5/货架10/报损3 应售100/200/50 → 平均5.14%、高发报损，注入失败即不命中）"
  },
  {
    "slug": "life/analysis-cost-10",
    "inputs": {
      "data": "原材料,8000,7400\n人工,5000,5600\n制造费用,3000,2900"
    },
    "expect": [
      "预算合计： 16000.00",
      "总差异： -100.00",
      "最大超支项： 人工"
    ],
    "ref": "预算8000+5000+3000=16000、实际7400+5600+2900=15900；总差异=-100.00、执行率=15900/16000=99.38%；最大超支项=人工(+600)，超支1项、节约2项（独立复算；默认 原材料10000/11200、人工6000/5800、制造费用4000/4200 → 总差异+1200、执行率106.00%，注入失败即不命中）"
  },

{
  "slug": "life/analysis-23",
  "inputs": {
    "data": "A栋,30,36\nB栋,45,50\nC栋,60,78\nD栋,24,27",
    "std": "1.2"
  },
  "expect": [
    "平均间距系数： 1.1840",
    "达标率： 50.00%",
    "极差： 0.1889"
  ],
  "ref": "系数=间距÷楼高：1.2000/1.1111/1.3000/1.1250；均值1.1840、极差0.1889、达标2/4=50.00%（默认3栋达标率66.67%、均值1.1884 避开）"
},
{
  "slug": "life/analysis-74",
  "inputs": { "data": "竞品A,19.9,32.5,8.0\n竞品B,24.6,21.0,-3.5\n竞品C,15.8,18.4,12.6\n竞品D,30.1,12.1,5.2" },
  "expect": [
    "价格均值： 22.60",
    "份额合计： 84.00%",
    "增速均值： +5.58%"
  ],
  "ref": "价格 (19.9+24.6+15.8+30.1)/4=22.60；份额 32.5+21.0+18.4+12.1=84.00%；增速 (8.0−3.5+12.6+5.2)/4=5.58%（默认两项 22.50/50.00%/+1.50%，避开；价格数据刻意取到 22.60 以避开 .xx5 舍入边界）"
},

{
  "slug": "life/report-profit",
  "inputs": {
    "rev": "400000",
    "cog": "260000",
    "payroll": "60000",
    "rent": "15000",
    "misc": "9000",
    "recv": "60",
    "cash0": "80000"
  },
  "expect": [
    "240,000.00",
    "-104,000.00"
  ],
  "ref": "营业收入 400,000 − 进货成本 260,000 = 毛利 140,000（毛利率 35.00%）；期间费用 60,000+15,000+9,000 = 84,000 ⇒ 营业利润 56,000（净利率 14.00%）；回款率 60% 时现金流入 240,000.00，付现支出 260,000+84,000 = 344,000 ⇒ 经营现金流净额 −104,000.00、期末现金 80,000−104,000 = −24,000.00（独立复算；默认 185,000/96,000/回款 85% 时净流入仅 1,250.00，注入值全不落在默认分支上）"
},

{
  "slug": "life/stats-13",
  "inputs": {
    "roster": "张三,2\n李四,3\n王五,1",
    "price": "25"
  },
  "expect": [
    "150.00",
    "50.00"
  ],
  "ref": "名单三行「姓名,份数」= 张三 2 + 李四 3 + 王五 1 ⇒ 人数 3、合计份数 6、人均 2.00 份；单价 25 元 ⇒ 预售金额 6×25 = 150.00 元、人均金额 150÷3 = 50.00 元（独立复算；默认名单为空 → 页面提示「请粘贴接龙名单」，注入失败即不命中）"
},

{
  "slug": "life/date-diff",
  "inputs": {
    "date1": "2025-03-10",
    "date2": "2025-08-15"
  },
  "expect": [
    "3792",
    "227520"
  ],
  "ref": "2025-03-10 → 2025-08-15 共 158 天 ⇒ 总小时 158×24 = 3792、总分钟 158×1440 = 227520，另完整周数 22、剩余 4 天（独立复算；默认 2026-01-01→2026-07-29 = 209 天 → 5024 小时，注入失败即不命中）"
},

{
  "slug": "life/csv-to-markdown",
  "inputs": {
    "input": "姓名,科目,成绩\n张三,数学,92\n李四,物理,88"
  },
  "expect": [
    "| 张三 | 数学 | 92 |",
    "| 李四 | 物理 | 88 |"
  ],
  "ref": "三列两行 CSV 以首行作表头解析 ⇒ 输出行 `| 张三 | 数学 | 92 |` 与 `| 李四 | 物理 | 88 |`（独立复算 parseCSV 与「| 单元格 | 」拼接规则；默认输入为空 → 输出空串，注入失败即不命中）"
},

{
  "slug": "life/generator-random-1",
  "inputs": {
    "min": "60",
    "max": "90",
    "cnt": "3"
  },
  "expect": [
    "生成结果（范围 60 ~ 90）"
  ],
  "ref": "区间 60~90、数量 3 ⇒ 表头「生成结果（范围 60 ~ 90）：」，三个数值虽随机但完全由注入区间决定（默认 min=1/max=100 → 「范围 1 ~ 100」，注入失败即不命中）"
},

{
  "slug": "life/generator-price",
  "inputs": {
    "cnt": "50"
  },
  "expect": [
    "50. 《设备维修合同》草案"
  ],
  "ref": "条数钳到上限 50 ⇒ 第 50 条取 services[49%10] = 设备维修，出现「50. 《设备维修合同》草案」（默认 cnt=5 只渲染第 1~5 条，注入失败即不命中）"
},

{
  "slug": "life/recommender-8",
  "inputs": {
    "cnt": "50"
  },
  "expect": [
    "50. 个人意外 场景"
  ],
  "ref": "条数钳到上限 50 ⇒ 第 50 条取 scenarios[49%8] = 个人意外，出现「50. 个人意外 场景」（默认 cnt=5 只渲染第 1~5 条，注入失败即不命中）"
},

{
  "slug": "life/music-practice-timer",
  "clicks": [ "loadTemplate('full')" ],
  "expect": [
    "20:00",
    "曲目"
  ],
  "ref": "点击切换到内置模板 full（6 段）⇒ 末段「曲目」时长 1200 s → 显示 20:00（默认 warmup 模板只有热身/休息两段、仅出现 05:00，注入失败即不命中）"
},

{
  "slug": "life/countdown-1",
  "clicks": [ "applyTarget()", "switchMode('down')" ],
  "inputs": {
    "setMin": "2",
    "setSec": "30"
  },
  "expect": [
    "02:30.00"
  ],
  "ref": "注入 2 分 30 秒后 applyTarget() 得 target = 150000 ms，再 switchMode('down') 切为倒计时 ⇒ 显示 02:30.00（默认为正计时模式，显示恒为 00:00.00，注入失败即不命中）"
},

{
  "slug": "life/countdown-2",
  "inputs": {
    "itemName": "结婚纪念日",
    "itemDate": "2026-11-11"
  },
  "expect": [
    "879"
  ],
  "ref": "加入纪念日「结婚纪念日 / 2026-11-11」且非每年重复 ⇒ 目标日即 2026-11-11，与固定基准日 2024-06-15 相隔 879 天（默认列表为空 → 「还没有纪念日」，注入失败即不命中）"
},  // ── 进制换算（自定义进制） ─────────────────────────────────
  {
    slug: "life/base-convert",
    inputs: { input: "4095", customBase: "2" },
    expect: ["111111111111", "7777", "FFF"],
    ref: "去默认化：4095 = 0xFFF ⇒ toString(2) = 111111111111（12 个 1）、toString(8) = 7777、"
       + "toString(16).toUpperCase() = FFF；customBase=2 走同一条 toString(2) 分支 ⇒ 111111111111。"
       + "默认态 input=255 / customBase=36 ⇒ 11111111 / 377 / FF，三条锚全部失配。"
       + "注：本页结果回填在 <input> 的 value 上（bin/oct/dec/hex/custom），仍可被 fullBlob 捕获；"
       + "若沿用默认输入 255，默认态会产出同值 ⇒ 逃生项，必须换输入。",
  },

  // ── 经营报表（毛利 / 净利 / 现金流） ────────────────────────
  {
    slug: "life/report-profit",
    inputs: { rev: "200000", cog: "80000", payroll: "45000", rent: "12000", misc: "8000", recv: "95", cash0: "30000" },
    expect: ["毛利： 120,000.00 元", "净利率 27.50%", "经营现金流净额： 45,000.00 元"],
    ref: "去默认化：毛利 = 200000 − 80000 = 120000（毛利率 60.00%）；期间费用 = 45000+12000+8000 = 65000；"
       + "营业利润 = 120000 − 65000 = 55000（净利率 27.50%）；现金流入 = 200000×95% = 190000（未回款 10000）；"
       + "付现支出 = 80000 + 65000 = 145000；经营现金流 = 190000 − 145000 = 45000；期末现金 = 30000+45000 = 75000；"
       + "利润>0 且现金流>0 ⇒ 诊断「盈利且现金同步回正」。"
       + "默认态 185000/96000/38000/15000/7000/85/50000 ⇒ 毛利 89000（48.11%）、费用 60000、利润 29000、"
       + "现金流 1250、期末 51250，三条锚全部失配。",
  },

  // ── AA 分账（含小费按份均摊） ──────────────────────────────
  {
    slug: "life/bill-splitter",
    inputs: { "total-amount": "960", "tip-percent": "15" },
    expect: ["总金额： ¥960.00 + 15%小费 = ¥1104.00", "¥276.00"],
    ref: "去默认化：含小费总额 = 960×(1+15%) = 1104.00；默认 4 人各 1 份 ⇒ 每份 1104/4 = 276.00。"
       + "默认态为 1000 + 0% 小费 = 1000.00、每份 250.00，两条锚全部失配。"
       + "「总份数： 4份」不可作锚——该量只由人数决定，默认态同样命中（逃生项）。",
  },

  // ── 工作日测算（排除周六日） ───────────────────────────────
  {
    slug: "life/workday-calculator",
    inputs: { startDate: "2026-01-01", endDate: "2026-01-31" },
    checkIds: ["skipSat", "skipSun"],
    expect: ["自然日总数： 30 天", "周末（已排除）： 8 天", "工作日数： 22 天"],
    ref: "去默认化：循环条件 d<end ⇒ 只统计 2026/1/1~1/30 共 30 个自然日（不含末日）。"
       + "其中周六/周日为 1/3、1/4、1/10、1/11、1/17、1/18、1/24、1/25 共 8 天 ⇒ 排除后工作日 22。"
       + "skipSat/skipSun 在 HTML 上默认 checked，但 harness 桩内 checkbox 恒未勾 ⇒ 必须显式 checkIds，"
       + "否则输出为「周末（已排除）： 0 天 / 工作日数： 30 天」。默认态 startDate/endDate 无 value ⇒「请选择日期」。",
  },

  // ── 日期加减 ──────────────────────────────────────────────
  {
    slug: "life/date-add-subtract",
    inputs: { baseTime: "2026-03-15T08:00", y: "1", m: "1", d: "10", h: "2", min: "30", s: "0" },
    expect: ["结果时间： 2027/4/25 10:30:00", "加减量： 1年 1月 10日 2时 30分 0秒"],
    ref: "去默认化：基准 2026-03-15 08:00；先 setFullYear(+1) ⇒ 2027-03-15，再 setMonth(+1) ⇒ 2027-04-15"
       + "（3 月 31 日溢出到 4/15，本例不触发月末钳制分支）；随后按毫秒叠加 d=10 天 ⇒ 2027-04-25、"
       + "h=2/min=30 ⇒ 10:30。默认态 baseTime 为空 ⇒「请选择基准日期」，两条锚全部失配。",
  },
  {
    slug: "life/angle-converter",
    inputs: { inputVal: "180" },
    expect: ["3.141592654"],
    ref: 'v=180° 基准值 180，弧度 = 180 ÷ 57.295779513 = 3.141592654（fmt 取 10 位有效数字）。默认态 90°→1.570796327 不命中；页面静态文本 3.1416/57.2958/360 均不干扰'
  },
  {
    slug: "life/angle-converter",
    inputs: { inputVal: "45" },
    expect: ["0.7853981634"],
    ref: 'v=45° 弧度 = 45 ÷ 57.295779513 = 0.7853981634（10 位有效数字）'
  },
  {
    slug: "life/angle-converter",
    inputs: { inputVal: "270" },
    expect: ["4.71238898"],
    ref: 'v=270° 弧度 = 270 ÷ 57.295779513 = 4.71238898'
  },
  {
    slug: "life/angle-converter",
    inputs: { inputVal: "360" },
    expect: ["6.283185307"],
    ref: 'v=360° 弧度 = 360 ÷ 57.295779513 = 6.283185307'
  },
  {
    slug: "life/angle-converter",
    inputs: { inputVal: "720" },
    expect: ["12.56637061"],
    ref: 'v=720° 弧度 = 720 ÷ 57.295779513 = 12.56637061'
  },
  {
    slug: "life/angle-converter",
    inputs: { inputVal: "100" },
    expect: ["1.745329252"],
    ref: 'v=100° 弧度 = 100 ÷ 57.295779513 = 1.745329252'
  },
  {
    slug: "life/length-converter",
    inputs: { inputVal: "5" },
    expect: ["0.01640419948 英尺"],
    ref: 'fromUnit 框架默认 mm；meters=v*0.001；锚取『实际:』后真值+单位，避开默认 v=1/mm 产物'
  },
  {
    slug: "life/length-converter",
    inputs: { inputVal: "100" },
    expect: ["0.3280839895 英尺"],
    ref: 'ft=0.1/0.3048'
  },
  {
    slug: "life/length-converter",
    inputs: { inputVal: "3" },
    expect: ["0.009842519685 英尺"],
    ref: 'ft=0.003/0.3048'
  },
  {
    slug: "life/length-converter",
    inputs: { inputVal: "0.5" },
    expect: ["0.01968503937 英寸"],
    ref: 'in=0.0005/0.0254'
  },
  {
    slug: "life/length-converter",
    inputs: { inputVal: "2" },
    expect: ["0.002187226597 码"],
    ref: 'yd=0.002/0.9144'
  },
  {
    slug: "life/length-converter",
    inputs: { inputVal: "10" },
    expect: ["0.3937007874 英寸"],
    ref: 'in=0.01/0.0254'
  },
  {
    slug: "life/weight-converter",
    inputs: { inputVal: "500" },
    expect: ["0.5 克"],
    ref: 'fromUnit 框架默认 mg；base=v*0.001；g=0.5/1'
  },
  {
    slug: "life/weight-converter",
    inputs: { inputVal: "1000" },
    expect: ["0.002204622622 磅"],
    ref: 'lb=1/453.59237'
  },
  {
    slug: "life/weight-converter",
    inputs: { inputVal: "200" },
    expect: ["0.00705479239 盎司"],
    ref: 'oz=0.2/28.349523125'
  },
  {
    slug: "life/weight-converter",
    inputs: { inputVal: "50" },
    expect: ["0.00005 千克"],
    ref: 'kg=0.05/1000'
  },
  {
    slug: "life/weight-converter",
    inputs: { inputVal: "10" },
    expect: ["0.05 克拉"],
    ref: 'ct=0.01/0.2'
  },
  {
    slug: "life/weight-converter",
    inputs: { inputVal: "5" },
    expect: ["0.025 克拉"],
    ref: 'ct=0.005/0.2'
  },
  {
    slug: "life/volume-converter",
    inputs: { inputVal: "5" },
    expect: ["0.005 L"],
    ref: 'base=5ml, L=5/1000=0.005'
  },
  {
    slug: "life/volume-converter",
    inputs: { inputVal: "10" },
    expect: ["0.002641720524 gal"],
    ref: 'base=10ml, gal=10/3785.411784'
  },
  {
    slug: "life/volume-converter",
    inputs: { inputVal: "100" },
    expect: ["0.2113376419 pt"],
    ref: 'base=100ml, pt=100/473.176473'
  },
  {
    slug: "life/volume-converter",
    inputs: { inputVal: "50" },
    expect: ["0.05283441047 qt"],
    ref: 'base=50ml, qt=50/946.352946'
  },
  {
    slug: "life/volume-converter",
    inputs: { inputVal: "200" },
    expect: ["0.8453505675 cup"],
    ref: 'base=200ml, cup=200/236.5882365'
  },
  {
    slug: "life/volume-converter",
    inputs: { inputVal: "3" },
    expect: ["0.6086524091 tsp"],
    ref: 'base=3ml, tsp=3/4.92892159'
  },
  {
    slug: "life/area-converter",
    inputs: { inputVal: "1000000" },
    expect: ["10000 cm²"],
    ref: 'base=1m², cm2=1/1e-4'
  },
  {
    slug: "life/area-converter",
    inputs: { inputVal: "5000000" },
    expect: ["0.0075 亩"],
    ref: 'base=5m², mu=5/666.6666667'
  },
  {
    slug: "life/area-converter",
    inputs: { inputVal: "2000000" },
    expect: ["0.0002 ha"],
    ref: 'base=2m², ha=2/1e4'
  },
  {
    slug: "life/area-converter",
    inputs: { inputVal: "10000000" },
    expect: ["0.002471053815 acre"],
    ref: 'base=10m², acre=10/4046.8564224'
  },
  {
    slug: "life/area-converter",
    inputs: { inputVal: "3000000" },
    expect: ["32.29173125 ft²"],
    ref: 'base=3m², ft2=3/0.09290304'
  },
  {
    slug: "life/area-converter",
    inputs: { inputVal: "1000000000" },
    expect: ["0.001 km²"],
    ref: 'base=1000m², km2=1000/1e6'
  }
];

// ---------------------------------------------------------------- main
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
  console.log("==== life calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();