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
    "800.0 包围盒体积 cm³",
    "0.40 厚宽比 T/W",
    "2.00 口底比"
  ],
  "ref": "非默认输入（默认 12.0/8.0/3.0/240/9.0/5.0）：近似体积 = 20×10×4 = 800.0 cm³；密度 = 800÷800 = 1.00 g/cm³；长宽比 = 20÷10 = 2.00；厚宽比 = 4÷10 = 0.40；口底比 = 12÷6 = 2.00。默认态为 288.0 / 0.83 / 1.50 / 0.38 / 1.80（三串均不含）。注：材质 select、编号/名称文本框与密度参考行只回显静态值 ⇒ 不锚。"
},
{
  "slug": "archaeology/artifact-measurement",
  "inputs": { "len": "12", "wid": "8", "thk": "3", "mass": "240", "rim": "-1", "base": "5" },
  "clicks": ["calc();"],
  "expect": ["口径须为大于 0 的数值"],
  "ref": "口径填 -1 时明确报错并清空结果，不再生成负口底比或复制记录；留空仍可计算其他指标。"
},
{
  "slug": "archaeology/artifact-measurement",
  "inputs": { "len": "12", "wid": "8", "thk": "3", "mass": "240", "rim": "", "base": "-2" },
  "clicks": ["calc();"],
  "expect": ["底径须为大于 0 的数值"],
  "ref": "底径填 -2 时明确报错；口径留空不影响其他指标。"
},
{
  "slug": "archaeology/artifact-measurement",
  "inputs": { "len": "12", "wid": "8", "thk": "3", "mass": "240", "rim": "9", "base": "5", "volMeas": "250" },
  "clicks": ["calc();"],
  "expect": ["实测密度 g/cm³", "参考密度（陶器）", "实测 250.0cm³"],
  "ref": "实测体积 250 cm³ ⇒ 密度 240/250 = 0.96，标记为实测密度，可与参考范围对照；不再使用包围盒 288 cm³ 的表观值。"
},
{
  "slug": "archaeology/artifact-measurement",
  "inputs": { "len": "12", "wid": "8", "thk": "3", "mass": "240" },
  "clicks": ["calc();"],
  "expect": ["表观密度 g/cm³（包围盒估算）", "不能与材料参考密度直接比较", "包围盒估算 288.0cm³"],
  "ref": "未填实测体积时密度明确标为包围盒表观值，并说明不可直接与材质参考密度比较；复制记录同样带估算前提。"
},
{
  "slug": "archaeology/artifact-measurement",
  "inputs": { "len": "0", "wid": "8", "thk": "3", "mass": "240" },
  "clicks": ["calc();var v=window._recordValid;document.getElementById('__tbProbe').textContent='RV '+(v?'BAD':'OK');"],
  "expect": ["RV OK"],
  "ref": "无效输入时记录有效状态为 false，复制函数按状态拒绝，不再依赖中英文提示开头文本；英文提示也不会被当记录复制。"
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
  "inputs": { "data": "1,0.4\n2,2" },
  "clicks": ["calc();"],
  "expect": ["第 1 行：0.4000 ㎡ 出土 1 件", "2.50 件/㎡", "合计：3 件 / 2.400 ㎡"],
  "ref": "面积 0.4 ㎡ 不再显示为 0 ㎡：单条保留 4 位小数，密度按原始 0.4 得 2.50；合计面积 2.4 保留精度。"
},
{
  "slug": "archaeology/stats-density",
  "inputs": { "data": "\n10abc,10;20,5" },
  "clicks": ["calc();"],
  "expect": ["第 2 行第 1 条「10abc,10」", "第 2 行第 2 条：5.000 ㎡ 出土 20 件"],
  "ref": "空行不再吞掉行号；同一行用分号分隔的多条分别标为“第 2 行第 1/2 条”，错误定位对应原始输入位置。"
},
{
  "slug": "archaeology/stats-density",
  "inputs": { "data": "-10,10" },
  "clicks": ["calc();"],
  "expect": ["第 1 行「-10,10」", "件数须为≥0整数"],
  "ref": "负件数整条拒绝，提示原始输入与格式要求，不再算出 -1 件/㎡。"
},
{
  "slug": "archaeology/stats-density",
  "clicks": [
    "var got=null;TBKit={util:{isEn:function(){return false;}},export:{csv:function(f,r){got=r;}}};document.getElementById('data').value='12,4\\n6,3\\nABC,2';__stats_densityExport();var ok=!!got&&got.length===5&&got[0][0]==='类型'&&got[1][0]==='明细'&&got[1][2]===12&&got[1][3]===4&&Math.abs(parseFloat(got[1][4])-3)<1e-9&&got[2][2]===6&&got[3][0]==='拒绝'&&got[3][5]==='ABC,2'&&got[4][0]==='合计'&&got[4][2]===18&&got[4][3]===7&&Math.abs(parseFloat(got[4][4])-2.57)<0.005;document.getElementById('__tbProbe').textContent='SDEXP '+(ok?'OK':'BAD:'+JSON.stringify(got));"
  ],
  "expect": ["SDEXP OK"],
  "ref": "导出按当前输入逐条输出，含类型列：明细/拒绝/合计；合计行件数列为总件数 18、面积 7、总密度 2.57，拒绝行保留原始输入，不再把“合计”占在件数列致总件数丢失。"
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
