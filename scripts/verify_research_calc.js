#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const NL = "String.fromCharCode(10)";
const CASES = [
{
  "slug": "research/analysis-49",
  "clicks": ["document.getElementById('matrix').value=['1,2','3,4','5'].join(String.fromCharCode(10));calc();"],
  "expect": ["第 3 行有 1 列，与首行 2 列不一致"],
  "ref": "单列记录不再被静默丢弃：第 3 行只有 1 列，必须报错并阻止计算。默认矩阵无单列行，0 逃生。"
},
{
  "slug": "research/analysis-49",
  "clicks": ["document.getElementById('matrix').value=['1,,3','2,,6','3,,9','4,,12'].join(String.fromCharCode(10));calc();"],
  "expect": ["第 1 行第 2 列为空或不是数值"],
  "ref": "空字段保留并按原行列定位报错，不再 filter 掉空列后照常计算。默认矩阵无空字段。"
},
{
  "slug": "research/analysis-49",
  "clicks": ["document.getElementById('matrix').value=['1,2','2,1','3,0','4,-1'].join(String.fromCharCode(10));calc();"],
  "expect": ["总分方差为 0"],
  "ref": "每行总分均为 3，方差为 0，α 无定义；旧版会给出 α=0 并判信度不足。默认矩阵方差>0，0 逃生。"
},
{
  "slug": "research/analysis-50",
  "clicks": ["document.getElementById('data').value=['甲公司,300','乙公司,200','丙公司,100'].join(String.fromCharCode(10));document.getElementById('market').value='600';calc();"],
  "expect": ["覆盖率： 100.00%", "口径判定： 高度集中"],
  "ref": "市场总规模 600 与已录合计 600 一致，覆盖率 100% 才允许套用集中度阈值：HHI=3888.89，高度集中。"
},
{
  "slug": "research/analysis-50",
  "clicks": ["document.getElementById('data').value=['甲公司,300','乙公司,200','丙公司,100'].join(String.fromCharCode(10));document.getElementById('market').value='10000';calc();"],
  "expect": ["覆盖率：6.00%", "不套用 2500/1500 阈值判定"],
  "ref": "市场总规模 10000 时覆盖率仅 6%，CR/HHI 只能标为样本内/已知部分，不得套用完整市场阈值。默认未填 market，0 逃生。"
},
{
  "slug": "research/analysis-50",
  "clicks": ["document.getElementById('data').value=['甲,300','乙,12abc','丙,100'].join(String.fromCharCode(10));calc();"],
  "expect": ["第 2 行：「12abc」不是有效正数营收"],
  "ref": "营收带尾随文字不再被 parseFloat 截成 12，必须按原行号报错并阻止计算。默认数据合法。"
},
{
  "slug": "research/analysis-51",
  "clicks": ["document.getElementById('data').value='X,1000,0,10';document.getElementById('absTh').value='5';calc();"],
  "expect": ["低比例不代表影响小"],
  "ref": "负面率 0.99% 低于关注阈值，但绝对负面量 10 条达到提示阈值 5 条，必须提示低比例不代表影响小。默认 18 条也触发，但默认阈值 100 不触发；此用例把阈值降到 5 以隔离判据。"
},
{
  "slug": "research/analysis-51",
  "clicks": ["document.getElementById('data').value='D1,-50,30,10';calc();"],
  "expect": ["第 1 行：正面/中性/负面必须是非负整数条数"],
  "ref": "负声量按原行号报错并阻止计算；旧版 parseFloat 后直接汇总。默认两行合法。"
},
{
  "slug": "research/analysis-52",
  "clicks": ["document.getElementById('codes').value=['A,10,5','B,6,2'].join(String.fromCharCode(10));calc();"],
  "expect": ["CR3 不适用：当前只有 2 个编码"],
  "ref": "不足 3 个编码时「前三项合计」恒为 100%，不得据此判观点集中；旧版会输出 100%。默认 5 个编码。"
},
{
  "slug": "research/analysis-52",
  "clicks": ["document.getElementById('codes').value='A,10.5,5';calc();"],
  "expect": ["第 1 行提及次数「10.5」必须是非负整数"],
  "ref": "提及次数只接受非负整数，小数按原行号报错；旧版 parseFloat 接受小数。默认整数。"
},
{
  "slug": "research/analysis-54",
  "clicks": ["document.getElementById('data').value=['\"访谈1，内容含逗号、分号\",价格,服务','访谈2|价格敏感,含逗号|服务','访谈3,价格'].join(String.fromCharCode(10));calc();"],
  "expect": ["资料条目：3 条，已编码：3 条（覆盖率 100.0%）", "总编码数：5"],
  "ref": "双引号包住正文中的逗号/分号、竖线优先作分隔符：3 条资料全部保留，总编码 5，正文里的逗号不被误切。"
},
{
  "slug": "research/analysis-54",
  "clicks": ["document.getElementById('data').value=[',主题',',服务'].join(String.fromCharCode(10));calc();"],
  "expect": ["第 1、2 行缺少资料文本（逗号/竖线前为空）"],
  "ref": "空正文资料行必须按原行号报错并整表不统计；旧版会把空正文当空行跳过。默认资料正文非空。"
},
{
  "slug": "research/calc-97",
  "inputs": { "N": "20000", "p": "45", "e": "4" },
  "expect": ["578 所需样本量（满足±4%）", "4.83% 实际抽样误差（n=400）"],
  "ref": "非默认 N=20000、p=45%、e=4%：有限总体校正后所需 578；n=400 时误差 4.83%；默认 p=50/e=3 输出 965、4.8%，不命中。"
},
{
  "slug": "research/calc-97",
  "clicks": ["document.getElementById('n').value='2';calc();"],
  "expect": ["合计 10,000 100% 2 100%"],
  "ref": "分层配额用最大余数法：n=2、四层规模 2000/5000/3000 时，高收入余数 0.4、中收入 0、低收入 0.6，剩余 1 个名额给低收入 → 0/1/1，合计严格等于 2；旧版按比例取整后可能 0/0/0。"
},
{
  "slug": "research/calc-97",
  "clicks": ["document.getElementById('N').value='-5';calc();"],
  "expect": ["有限总体规模 N 必须是 >0 的整数"],
  "ref": "未勾选无限总体时负数 N 必须报错，不得把负数当总体；默认 N=10000。"
},
{
  "slug": "research/calc-97",
  "clicks": ["document.getElementById('n').value='2.5';calc();"],
  "expect": ["「实际样本量 n」必须是 ≥1 的整数，不能是小数"],
  "ref": "实际样本量只接受 ≥1 的整数，小数按字段报错；旧版 parseFloat 后照算。默认 400。"
},
{
  "slug": "research/assessor-50",
  "inputs": { "reach": "20000", "frequency": "2", "ctr": "4", "cost": "20" },
  "expect": ["广告效果指数AEI 20.0%", "¥5000.00 CPM(元/千次曝光)"],
  "ref": "非默认触达 20000、频次 2、CTR 4%、投入 20 万元：AEI 20.0%、CPM ¥5000.00；默认 50000/3.5/2.5/50 输出 AEI 50.0%、CPM ¥2857.14，不命中。"
},
{
  "slug": "research/assessor-50",
  "clicks": ["document.getElementById('reach').value='0';calc();"],
  "expect": ["CPM=未定义（触达人数或平均频次为 0）"],
  "ref": "触达为 0 是合法输入，但 CPM 无定义；旧版把 0 当未填写直接整页拦死。默认 50000。"
},
{
  "slug": "research/assessor-50",
  "clicks": ["document.getElementById('cost').value='0';calc();"],
  "expect": ["CPM=¥0.00元/千次曝光", "免费投放：投入为 0"],
  "ref": "成本 0 合法：CPM 与每回忆用户成本均为 0，并提示确认免费资源；旧版按空值或分母为 0 拦死。默认 50。"
},
{
  "slug": "research/assessor-50",
  "clicks": ["document.getElementById('unaidedRecall').value='0';calc();"],
  "expect": ["每回忆用户成本=未定义（触达人数或无辅助回忆率为 0）"],
  "ref": "无辅助回忆率 0 合法：每回忆成本无定义，但记忆维度按 0 计分并继续输出 AEI；旧版整页拦截。默认 20。"
},
{
  clicks: ["calc()"],
  "slug": "research/tester-17",
  "expect": ["中点参考价（非 OPP）", "不是标准 PSM"],
  "ref": "未录逐位数据时只能给四个汇总价的算术参考，明确标非 OPP、不称最优；旧版把简化结果直接称 PSM 和最优价格。"
},
{
  "slug": "research/tester-17",
  "clicks": [
    "var a=[];for(var i=0;i<20;i++){a.push((i+1)+','+(10+0.8*i)+','+(30+2.5*i)+','+(55+2.5*i)+','+(70+2.5*i));}document.getElementById('psmData').value=a.join(String.fromCharCode(10));document.getElementById('sampleSize').value='20';calc();document.getElementById('__tbProbe').textContent=String(document.getElementById('res').innerHTML);"
  ],
  "expect": ["PMC 边际便宜点（下限） ¥40.10", "OPP 最优价格点 ¥66.22", "PME 边际昂贵点（上限） ¥73.75"],
  "ref": "20 位受访者四问数据：PMC=40.10、OPP=66.22、PME=73.75、IDP=47.63，区间宽 50.8%；来自标准累计曲线交点，非汇总价算术。"
},
{
  "slug": "research/tester-17",
  "clicks": ["document.getElementById('psmData').value=['1,10,30,55,70','2,20,40,60,80','3,10,30,55,70'].join(String.fromCharCode(10));calc();"],
  "expect": ["逐位数据只有 3 人，无法形成稳定累计曲线；至少录入 5 人"],
  "ref": "逐位数据少于 5 人时拒绝给交点结论；旧版无逐位模式。"
},
{
  "slug": "research/tester-17",
  "clicks": ["document.getElementById('psmData').value='';document.getElementById('tooCheap').value='130';document.getElementById('tooExpensive').value='30';calc();"],
  "expect": ["四个汇总价必须严格递增：太便宜"],
  "ref": "四个汇总价倒置必须拒绝计算，不再输出负的区间宽度；默认 29/49/89/129 合法。"
}
];
(async () => {
let failed = 0;
for (const c of CASES) {
  const r = await runCase(c);
  if (r && r.ok) {
    console.log("✅ " + c.slug + " via " + r.via);
  } else {
    failed++;
    console.log("❌ " + c.slug + " 未匹配期望值");
    if (r && r.errs && r.errs.length) console.log("     errs: " + JSON.stringify(r.errs));
    if (r && r.got) console.log("     got: " + String(r.got).slice(0, 300));
  }
}
console.log("==== research calc " + (CASES.length - failed) + "/" + CASES.length + " ====");
process.exit(failed ? 1 : 0);
})();
