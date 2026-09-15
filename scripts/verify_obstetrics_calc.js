#!/usr/bin/env node
/**
 * 第 40 道门禁：obstetrics 分类计算正确性验证（13 个确定性数值工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，且期望值经「假通过自检」复核不等于默认输出，杜绝假通过。
 * 排除：
 *   - gestational / gestational-age：计算依赖 new Date()（今日孕周），stub 无法还原 → 无验证意义；
 *   - 其余 16 个计算类页面除本表 13 个外，多为纯展示/模板类或单位换算，已并入对应确定性函数。
 * 用法: node scripts/verify_obstetrics_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "obstetrics/afi-normal",
    inputs: { ruq: "2", luq: "2", rlq: "2", llq: "2" },
    expect: ["8.0", "偏少"],
    ref: "AFI=2+2+2+2=8.0cm，落入 ≤8 → 偏少(临界)（默认示例=12→正常，避开）" },

  { slug: "obstetrics/ectopic-hcg",
    inputs: { hcg1: "1000", hcg2: "2000", interval: "48" },
    expect: ["+100.0%", "48.0小时"],
    ref: "变化率=(2000-1000)/1000×100=+100.0%；DT=48×0.693/ln2=48.0h（默认示例值不同，避开）" },

  { slug: "obstetrics/fetal-weight-hadlock",
    inputs: { bpd: "9", hc: "32", ac: "30", fl: "7" },
    expect: ["2562", "2.56", "正常体重"],
    ref: "Hadlock四参数 log10w=1.3596-0.00386·30·7+0.0064·32+0.00061·9·30+0.0424·30+0.174·7=3.4085→EFW=10^3.4085=2562g=2.56kg（默认空→请至少输入一个参数，避开）" },

  { slug: "obstetrics/postpartum-hemorrhage",
    inputs: { wetWeight: "2000", dryWeight: "1000", preWeight: "60", hr: "100", sbp: "100" },
    expect: ["952", "1.00"],
    ref: "失血量=(2000-1000)/1.05=952mL（calcWeight）；SI=100/100=1.00（calcShock→轻度休克）（默认空→返回，避开）" },

  { slug: "obstetrics/preeclampsia-prediction",
    inputs: { sflt: "6000", pigf: "50", onset: "late" },
    expect: ["120.00", "确诊子痫前期"],
    ref: "比值=6000/50=120.00；晚发确诊界值110，120≥110→确诊（默认空→请输入有效数值，避开）" },

  { slug: "obstetrics/ovarian-reserve",
    inputs: { amh: "7.0", fsh: "6", e2: "35", afc: "12", age: "30" },
    expect: ["7.00", "卵巢高反应(可能PCOS)"],
    ref: "amh=7.0≥6→amhLevel极高且score-=1→总分-1；其余0分→amh>6分支→卵巢高反应(可能PCOS)；AMH显示7.00（默认/示例=0.6→DOR、2.5→正常，均不命中，避开）" },

  { slug: "obstetrics/endometrial-thickness",
    inputs: { cycleDay: "20", thickness: "5" },
    expect: ["偏薄"],
    ref: "育龄期 D20→分泌期(10–14mm)，实测5mm<minT-1=9→偏薄（默认周期类型非绝经后，避开绝经后分支）" },

  { slug: "obstetrics/fetal-movement-count",
    inputs: { morn: "1", noon: "1", even: "1", h1: "1" },
    expect: ["异常(减少)"],
    ref: "12h胎动=(1+1+1)×4=12<20→异常(减少)（避开 '12' 命中默认标签 '12小时胎动'；默认示例=5/4/6/6→36正常）" },

  { slug: "obstetrics/ctg-fhr",
    inputs: { baseline: "105", variability: "10", accel: "present", decel: "none", contractions: "4" },
    expect: ["可疑", "105"],
    ref: "基线105→可疑(100–110)；变异10→正常；加速present；无减速；宫缩4→正常；abnCount=0,susCount=1→可疑CTG（默认140/10→正常、示例95/3/late→异常，均不命中，避开）" },

  { slug: "obstetrics/heart-rate",
    inputs: { baseline: "95", variability: "2", accel: "0", decel: "late" },
    expect: ["病理性 CTG（Pathological）"],
    ref: "基线95<100→病理性；变异2<3→病理性；晚期减速→病理性→病理性CTG（默认140/10/2/none→正常，避开）" },

  { slug: "obstetrics/yangshuizhishu-afi-zhengchangfanwei",
    inputs: { q1: "2", q2: "3", q3: "3", q4: "3" },
    expect: ["11.0"],
    ref: "AFI=2+3+3+3=11.0cm→羊水量正常（默认4/3/3/3=13.0，避开）" },

  { slug: "obstetrics/down-screening",
    inputs: { age: "28", afp: "0.75", bhcg: "1.7", ue3: "0.75" },
    expect: ["1/90"],
    ref: "年龄先验1/(1300·e^-0.18)=1/1085.9；afpLR(0.75<0.8→3)×hcgLR(1.7>1.5→2)×ue3LR(0.75<0.8→2)=12；调整后→riskN=round(1/(12/1085.9))=90→1/90,<1/270高风险（默认=25/1/1/1→1/1300；预设loadHigh=38/0.65/2.8/0.65→1/25，避开）" },

  { slug: "obstetrics/calc-risk",
    inputs: { age: "40", weight: "60", ga: "16", afp: "0.6", bhCG: "2.5" },
    expect: ["1:28", "高风险"],
    ref: "先验1/100×afpLR(0.6→1.6)×hcgLR(2.5→2.2)=0.0352→1/28；≥1/270→高风险（weight/ga仅作非空校验，默认空→请完整输入，避开）" },
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
  console.log("==== obstetrics calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();