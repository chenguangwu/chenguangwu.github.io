#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "archaeology/artifact-measurement",
  "inputs": {
    "len": "20",
    "wid": "10",
    "thk": "4",
    "mass": "800",
    "rim": "12",
    "base": "6"
  },
  "expect": [
    "800.0 近似体积 cm³",
    "0.40 厚宽比 T/W",
    "2.00 口底比"
  ],
  "ref": "非默认输入（默认 12.0/8.0/3.0/240/9.0/5.0）：近似体积 = 20×10×4 = 800.0 cm³；密度 = 800÷800 = 1.00 g/cm³；长宽比 = 20÷10 = 2.00；厚宽比 = 4÷10 = 0.40；口底比 = 12÷6 = 2.00。默认态为 288.0 / 0.83 / 1.50 / 0.38 / 1.80（三串均不含）。注：材质 select、编号/名称文本框与密度参考行只回显静态值 ⇒ 不锚。"
},
{
  "slug": "archaeology/site-grid",
  "inputs": { "len": "100", "wid": "60", "side": "10", "gap": "2", "mode": "cover" },
  "clicks": ["calc();"],
  "expect": ["54 探方总数", "2020.0 隔梁面积 m²"],
  "ref": "全覆盖：coverL=ceil((100+2)/(10+2))=9、coverW=ceil(62/12)=6 ⇒ 54；占地=(9×10+8×2)×(6×10+5×2)=106×70=7420，发掘=54×100=5400 ⇒ 隔梁 2020.0。旧实现 ceil(100/10)=10 忽略隔梁，得 60 个。"
},
{
  "slug": "archaeology/site-grid",
  "inputs": { "len": "100", "wid": "60", "side": "10", "gap": "2", "mode": "fit" },
  "clicks": ["calc();"],
  "expect": ["40 探方总数", "1452.0 隔梁面积 m²"],
  "ref": "边界内：fitL=floor(102/12)=8、fitW=floor(62/12)=5 ⇒ 40；占地=(8×10+7×2)×(5×10+4×2)=94×58=5452，发掘=4000 ⇒ 隔梁 1452.0；全部位于遗址范围内。"
},
{
  "slug": "archaeology/site-grid",
  "inputs": { "len": "60", "wid": "40", "side": "5", "gap": "" },
  "clicks": ["calc();"],
  "expect": ["请填写隔梁宽度"],
  "ref": "隔梁留空不再按 0 计算，明确提示；无隔梁须显式填 0。"
},
{
  "slug": "archaeology/site-grid",
  "inputs": { "len": "60", "wid": "40", "side": "5", "gap": "-1" },
  "clicks": ["calc();"],
  "expect": ["隔梁宽度不能为负数"],
  "ref": "负隔梁不再静默归零，停止计算并清空结果。"
},
{
  "slug": "archaeology/site-grid",
  "inputs": { "len": "1000", "wid": "1000", "side": "1", "gap": "0", "mode": "cover" },
  "clicks": ["calc();"],
  "expect": ["1000000 探方总数", "仅显示前 2000 个"],
  "ref": "1000×1000、1m 探方共 100 万个；坐标表限制为前 2000 行并提示，避免双重循环生成百万行冻结页面。"
},
{
  "slug": "archaeology/site-grid",
  "inputs": { "len": "3", "wid": "3", "side": "5", "gap": "1", "mode": "fit" },
  "clicks": ["calc();"],
  "expect": ["不足一个探方", "边界内无法布设完整探方"],
  "ref": "遗址小于一个探方（含隔梁）：fitL=fitW=0，边界内无完整探方，提示切换全覆盖或减小规格。"
},
{
  "slug": "archaeology/dating-method",
  "inputs": { "search": "radiocarbon", "grpFilter": "radiocarbon" },
  "clicks": ["render();"],
  "expect": ["碳-14测年", "含碳有机物"],
  "ref": "英文 radiocarbon 与中文“碳十四/碳14/c14”归一为“碳-14”，在放射性碳分组中命中“碳-14测年”；旧示例搜索“碳十四”而数据名为“碳-14测年”，连续字串不匹配返回空。"
},
{
  "slug": "archaeology/pottery-typology",
  "inputs": { "search": "漩涡纹", "stageFilter": "mid" },
  "clicks": ["render();"],
  "expect": ["马家窑文化", "漩涡纹"],
  "ref": "关键词“漩涡纹”在中期文化中唯一命中马家窑文化；旧实现只匹配中文，英文用户无法检索。"
},
{
  "slug": "archaeology/stats-density",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "archaeology/stats-density",
  "inputs": {
    "data": "10abc,10\n20,5"
  },
  "expect": [
    "第 1 行格式无效已拒绝"
  ],
  "ref": "修复前 parseFloat('10abc')=10 被当有效；现件数须为≥0整数、面积须正数，逐行拒绝并报行号。第 2 行 20/5=4.00 件/㎡ 正常参与合计。"
},
{
  "slug": "archaeology/stats-density",
  "inputs": {
    "data": "-10,10"
  },
  "expect": [
    "件数须为≥0整数"
  ],
  "ref": "修复前 -10 件/10 ㎡ 得 -1 件/㎡；现整行拒绝并提示格式要求（默认合法数据不含该文案）。"
},
{
  "slug": "archaeology/stats-density",
  "clicks": [
    "var got=null;TBKit={util:{isEn:function(){return false;}},export:{csv:function(f,r){got=r;}}};document.getElementById('data').value='12,4\\n6,3';__stats_densityExport();var ok=!!got&&got.length===4&&got[0][0]==='件数'&&got[1][0]===12&&got[1][1]===4&&Math.abs(parseFloat(got[1][2])-3)<1e-9&&got[2][0]===6&&got[3][0]==='合计'&&Math.abs(parseFloat(got[3][2])-2.57)<0.005;document.getElementById('__tbProbe').textContent='SDEXP '+(ok?'OK':'BAD:'+JSON.stringify(got));"
  ],
  "expect": ["SDEXP OK"],
  "ref": "修复前导出读 #stats_densityTable（历史记录表），与当前输入无关；现按当前 textarea 逐行重算，导出 件数/面积/密度（按密度降序）并附合计行。默认态无 TBKit.export.csv 调用、也无该探针串。"
},
{
  "slug": "archaeology/stratum-identify",
  "inputs": { "search": "仰韶文化", "ageFilter": "neo" },
  "clicks": ["render();"],
  "expect": ["仰韶文化", "人面鱼纹彩陶盆"],
  "ref": "仰韶文化属新石器（neo）而非旧石器（paleo）；旧示例把筛选设为 paleo，先过滤后搜索导致无匹配。"
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

  console.log("==== archaeology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
