#!/usr/bin/env node
/**
 * biz 分类关键计算逻辑独立验证（收口批次 C）
 *
 * 复用 scripts/verify_it_calc.js 的 DOM stub 与 runCase 框架。
 * 期望值一律由页面公式独立复算得出，不取页面输出。
 *
 * 用法：
 *   node scripts/verify_biz_calc.js
 *   node scripts/verify_biz_calc.js checker-8 meeting-cost-calculator
 */
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  // ── 服务质量检查（四维度加权 + 响应时间折算 + 投诉超额扣分）────
  {
    slug: "biz/checker-8",
    inputs: {
      certRate: "90", trainRate: "85", uniform: "95", attendance: "90",
      patrol: "92", accessLog: "88", responseTime: "4", logComplete: "90",
      monitorCov: "95", equipOk: "90", comm: "85",
      csat: "88", complaintRes: "86", complaintCnt: "6",
    },
    expect: ["满意度88%/投诉解决86%/月投诉6次"],
    ref: "人员=(90+85+95+90)/4=90；流程=(92+88+80+90)/4=87.5→88（响应 4 分钟→80 分）；"
       + "装备=(95+90+85)/3=90；满意度=(88+86)/2−(6−5)×3=84；"
       + "总分=90×.25+88×.30+90×.20+84×.25=87.9→88 → 良好",
  },

  // ── 会议成本（人·小时计价）────────────────────────────────────
  {
    slug: "biz/meeting-cost-calculator",
    inputs: { duration: "60", attendees: "5", hourlyRate: "100", roomCost: "200" },
    expect: ["¥700.00", "¥11.67", "¥140.00"],
    ref: "hours=60/60=1；人力=1×5×100=500；总成本=500+200=700.00；"
       + "每分钟=700/60=11.666→11.67；人均=700/5=140.00",
  },

  // ── 胜任力评估（岗位权重加权平均）─────────────────────────────
  {
    slug: "biz/assessor-49",
    inputs: { jobType: "tech", d1: "8", d2: "7", d3: "9", d4: "7", d5: "7", d6: "8" },
    expect: ["7.90", "优秀"],
    ref: "技术岗权重 [.30,.10,.25,.10,.15,.10]："
       + "8×.30+7×.10+9×.25+7×.10+7×.15+8×.10=2.4+.7+2.25+.7+1.05+.8=7.90 → ≥7 优秀",
  },

  // ── 单价对比（单位归一化到克后比较）───────────────────────────
  {
    slug: "biz/unit-price-compare",
    inputs: { a_q: "400", a_u: "g", a_p: "10", b_q: "2", b_u: "kg", b_p: "36" },
    expect: ["0.0250 元/g", "1.39 倍", "商品 B（每克更低 0.0180 元）"],
    ref: "A=10/400=0.0250 元/g；B=36/(2×1000)=0.0180 元/g；B 更划算；"
       + "倍数=0.0250/0.0180=1.3889→1.39（独立复算）。"
       + "原注入 500g/12 元 与 1kg/20 元 = 页面默认值 ⇒ 默认态同样命中（all_default）；"
       + "改后默认态 0.0240/0.0200/1.20 倍，与本例三个锚点零交集。",
  },

  // ── 风险矩阵（可能性×影响分级）────────────────────────────────
  {
    slug: "biz/assessor-risk-8",
    inputs: { scene: "production" },
    clicks: [
      "riskData=[{name:'设备点检缺失',likelihood:5,impact:4},{name:'作业许可未落实',likelihood:4,impact:4},{name:'培训不到位',likelihood:2,impact:2}];calc()",
    ],
    expect: ["设备点检缺失", "极高风险-需立即处置", "安全培训/设备点检/作业许可/防护装置/应急演练"],
    ref: "顶层 var riskData 用 clicks 覆写：5×4=20、4×4=16、2×2=4 ⇒ maxRisk=20 ⇒ 极高风险-需立即处置；"
       + "scene=production（非默认 building）⇒ 防控方向=sceneMeasures['production']（独立复算）。"
       + "原注入 scene=building 且沿默认 riskData（3×3=9/2×5=10/3×2=6 ⇒ maxRisk=10）⇒ 默认态同样命中「高风险-需优先整改」（all_default）。"
       + "改后默认态为 高风险-需优先整改 + building 门禁措施，与本例三个锚点零交集。"
       + "注：兜底阶段会无参调用 removeRisk/addRisk 破坏 riskData（删首项、加「新风险点」），"
       + "但 expect 在 clicks 执行后立即判定（阶段 2），早于该破坏 ⇒ 「设备点检缺失」仍可命中。",
  },

  // ── 演示计时（总时长均分到每页）───────────────────────────────
  {
    slug: "biz/presentation-timer",
    inputs: { slideCount: "4", totalMin: "1" },
    expect: ["00:15"],
    ref: "总秒=1×60=60；每页=⌊60/4⌋=15 → fmtTime(15)=00:15",
  },

  // ── 文本折行（字符模式定长切分）───────────────────────────────
  {
    slug: "biz/text-wrap",
    inputs: { input: "abcdefghij", wrapWidth: "4" },
    expect: ["abcd efgh ij"],
    ref: "stub 下「按单词换行」复选框默认未选中 → 字符模式；宽度 4 切分为 abcd/efgh/ij，"
       + "换行符默认 LF（stub 采集时空白归一化为空格）",
  },

  // ── 字符画边框（视觉宽度 + 左右内边距）───────────────────────
  {
    slug: "biz/text-box-drawing",
    inputs: { input: "Hi", style: "single", padX: "1", padY: "0" },
    expect: ["┌────┐", "│ Hi │"],
    ref: "视觉宽=2；内容宽=2+2×1=4 → 顶边 ┌+─×4+┐；内容行 │+空格+Hi+空格+│；"
       + "上下填充 0，底边 └+─×4+┘",
  },
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
  console.log("==== biz calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();